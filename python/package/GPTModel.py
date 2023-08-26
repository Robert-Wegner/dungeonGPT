import requests
import json
import os
import random
import re
import openai
import time
import os
from .files import read_file

def print_stream(string):
    for c in string:
        try:
            print(c, end="", flush=True)
            time.sleep(0.005)
        except KeyboardInterrupt:
            break


DEFAULT_SYSTEM_PROMPT = read_file("prompts/default_system_prompt.txt")
JSON_CORRECTOR_PROMPT = read_file("prompts/json_corrector_prompt.txt")
DICE_ROLL_PROMPT = read_file("prompts/dice_roll_prompt.txt")


class GPTModel:
  
    def __init__(self, model="gpt-3.5-turbo", system_prompt=DEFAULT_SYSTEM_PROMPT+DICE_ROLL_PROMPT):
        self.model = model
        self.conversation = [{"role": "system", "content": ""}]
        self.max_characters = 15000
        self.set_system_prompt(system_prompt)
        self.settings = {}
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.stream = False
        self.stream_callback = lambda text: print_stream(text)
        self.functions = []

    def get_system_prompt(self):
        return self.conversation[0]["content"]

    def set_system_prompt(self, new):
        if len(new) <= self.max_characters:
            self.conversation[0]["content"] = new
        else:
            print("Error: ", "system prompt too long")

    def reply_as_user(self, reply):
        if self.conversation[-1]["role"] in ["system", "assistant"]:
            self.conversation.append({"role": "user", "content": reply})
            return reply
        else:
            print("Error: ", "The user has already replied")
            return "Error: The user has already replied"
    
    def force_reply_as_user(self, reply):
        self.conversation.append({"role": "user", "content": reply})
        return reply

    def reply_as_assistant(self, reply):
        if self.conversation[-1]["role"] == "user":
            self.conversation.append({"role": "assistant", "content": reply})
            return reply

        else:
            print("Error: ", "The assistant has already replied")
            return "Error: The assistant has already replied"

    def force_reply_as_assistant(self, reply):
        self.conversation.append({"role": "assistant", "content": reply})
        return reply
        
    def generate(self):
        try:
            if len(self.functions) > 0:
                response = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.conversation,
                    temperature = 0,
                    stream = self.stream,  # this time, we set stream=True,
                    functions = self.functions
                )
            else:
                response = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.conversation,
                    temperature = 0,
                    stream = self.stream,  # this time, we set stream=True,
                )

            assistant_response = ""
            if self.stream:
                for chunk in response:
                    #print(chunk)
                    try:
                        char = chunk['choices'][0]['delta']['content']
                        #print(char, end="")
                        self.conversation[-1]['content'] += char
                        self.stream_callback(char)
                        assistant_response += char
                    except:
                        pass
            else:
                assistant_response = response['choices'][0]['message']['content']
                if assistant_response == None:
                    assistant_response = response['choices'][0]['message']['function_call']

            return assistant_response

        except Exception as error:
            print("Error: ", error)
            return "Error generating response."
        
    def generate_assistant_reply(self, message=False):
        if message:
            self.reply_as_user(message)

        reply = self.generate()
        if reply:
            self.reply_as_assistant(reply)

        self.prune()
        return reply
    
    def delete_last_message(self):
        self.conversation = self.conversation[:-1]

    def reset(self):
        self.conversation = self.conversation[:1]

    def character_count(self):
        return sum([len(c["content"]) for c in self.conversation])
    
    def prune(self):
        while self.character_count() > self.max_characters:
            del self.conversation[1]
            del self.conversation[1]

    def dump(self):
        print(self.conversation)
        return str(self.conversation)
    
