import openai
import time
import os
import eel


try:
    from files import read_file
except:
    pass

try:
    from .files import read_file
except:
    pass

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
  
    def __init__(self, model="gpt-3.5-turbo", system_prompt=DEFAULT_SYSTEM_PROMPT, temperature=0.5, max_characters=40000):
        self.model = model
        self.conversation = [{"role": "system", "content": ""}]
        self.max_characters = max_characters
        self.set_system_prompt(system_prompt)
        self.settings = {}
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.stream = False
        self.stream_callback = lambda text: print_stream(text)
        self.functions = []
        self.temperature = temperature

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
                    temperature = self.temperature,
                    stream = self.stream,  # this time, we set stream=True,
                    functions = self.functions
                )
            else:
                response = openai.ChatCompletion.create(
                    model = self.model,
                    messages = self.conversation,
                    temperature = self.temperature,
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

                assistant_response = response['choices'][0]['message']
                if assistant_response.get('function_call'):
                    return assistant_response['function_call']
                else:
                    return assistant_response['content']
                

            return assistant_response

        except Exception as error:
            print("Error: ", error)
            return f"Error generating response: {error}"
        
    def generate_assistant_reply(self, message=False, append=True):
        if message:
            self.reply_as_user(message)

        reply = self.generate()
        if not append:
            return reply
        
        if reply:
            self.reply_as_assistant(str(reply))

        self.prune()
        return reply

    def delete_first_message(self):
        del self.conversation[1]
   
    def delete_last_message(self):
        self.conversation = self.conversation[:-1]

    def reset(self):
        self.conversation = self.conversation[:1]

    def character_count(self):
        return sum([len(c["content"]) for c in self.conversation])
    
    def prune(self):
        while self.character_count() > self.max_characters:
            print("pruning")
            self.delete_first_message()

    def dump(self):
        return str(self.conversation)
    
    def pretty_dump(self):
        return '\n\n'.join([f'{message["role"]}: {message["content"]}' for message in self.conversation])


class DisplayedGPTModel(GPTModel):

    def __init__(self, grid_id, conversation_id, model="gpt-3.5-turbo", system_prompt=DEFAULT_SYSTEM_PROMPT, temperature=0.5, max_characters=40000):

        self.grid_id = grid_id
        self.conversation_id = conversation_id

        eel.Grid_createAndAddConversation(self.grid_id, self.conversation_id)
        eel.Conversation_addRole(self.conversation_id, 'User', '#AA4010')
        eel.Conversation_addRole(self.conversation_id, 'Assistant', '#4A0072')
        eel.Conversation_addRole(self.conversation_id, 'System', '#1E70BB')
        eel.Conversation_addMessage(self.conversation_id, 'System', '')

        super().__init__(model, system_prompt, temperature, max_characters)
    


    def set_system_prompt(self, new):
        super().set_system_prompt(new)
        eel.Conversation_modifyMessage(self.conversation_id, 0, 'System', new)

    def reply_as_user(self, reply):
        response = super().reply_as_user(reply)
        eel.Conversation_addMessage(self.conversation_id, 'User', reply)
        return response
    
    def reply_as_user(self, reply):
        response = super().force_reply_as_user(reply)
        eel.Conversation_addMessage(self.conversation_id, 'User', reply)
        return response

    def reply_as_assistant(self, reply):
        response = super().reply_as_assistant(reply)
        eel.Conversation_addMessage(self.conversation_id, 'Assistant', reply)
        return response
    
    def force_reply_as_assistant(self, reply):
        response = super().force_reply_as_assistant(reply)
        eel.Conversation_addMessage(self.conversation_id, 'Assistant', reply)
        return response
    
    def delete_first_message(self):
        super().delete_first_message()
        eel.Conversation_removeMessages(self.conversation_id, 1, 2)

    def reset(self):
        super().reset()
        eel.Conversation_removeMessages(self.conversation_id, 1, len(self.conversation) - 1)

