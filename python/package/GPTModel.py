import openai
import time
import os
import eel
import tiktoken

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
  
    _models = {
        "gpt-3.5-turbo": {
            "context_window": 4097,
            "prompt_token_price": 0.0000015,
            "completion_token_price": 0.000002
        },
        "gpt-3.5-turbo-16k": {
            "context_window": 16385,
            "prompt_token_price": 0.000003,
            "completion_token_price": 0.000004
        },
        "gpt-4": {
            "context_window": 8192,
            "prompt_token_price": 0.00003,
            "completion_token_price": 0.00006
        },
        "gpt-4-32k": {
            "context_window": 8192,
            "prompt_token_price": 0.00006,
            "completion_token_price": 0.00012,
        },
    }

    @staticmethod
    def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):         #openai-cookbook/examples/How_to_count_tokens_with_tiktoken.ipynb
        """Return the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            #print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
            return GPTModel.num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            #print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return GPTModel.num_tokens_from_messages(messages, model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens
    
    @staticmethod
    def num_tokens_from_functions(functions, model="gpt-3.5-turbo"):            #THIS IS ONLY AN APPROXIMATION
        functions_string = str(functions)
        return GPTModel.num_tokens_from_messages({"system", functions_string})

    def __init__(self, model="gpt-3.5-turbo", system_prompt=DEFAULT_SYSTEM_PROMPT, temperature=0.5, max_characters=40000):

        if model not in GPTModel._models:
            print("Please choose one of these models: ", str(self._models.keys()))
            model = "gpt-3.5-turbo"

        self.model = model
        self.conversation = [{"role": "system", "content": ""}]
        self.max_characters = max_characters
        self.settings = {}
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.stream = False
        self.stream_callback = lambda text: print_stream(text)
        self.functions = []
        self.temperature = temperature

        self.cost = 0
        self.context_window = 0
        self.cautious_context_window = 0
        self.cautious_context_window_factor = 0.6
        self.conversation_tokens = 0

        self.set_context_window({
            "gpt-3.5-turbo": 4097,
            "gpt-3.5-turbo-16k": 16385,
            "gpt-4": 8192
        }[model])

        self.set_system_prompt(system_prompt)


    def set_context_window(self, amount):
        self.context_window = amount
        self.cautious_context_window = int(self.cautious_context_window_factor * self.context_window)

    def set_conversation_tokens(self, amount):
        self.conversation_tokens = amount

    def update_conversation_tokens(self):
        conversation_tokens = GPTModel.num_tokens_from_messages(self.conversation, model=self.model)
        if len(self.functions) > 0:
            conversation_tokens += GPTModel.num_tokens_from_functions(self.functions, model=self.model)
        self.set_conversation_tokens(conversation_tokens)

    def increase_cost_by_tokens(self, prompt_tokens, completion_tokens):
        self.increase_cost(self._models[self.model]['prompt_token_price'] * prompt_tokens + self._models[self.model]['completion_token_price'] * completion_tokens)

    def set_cost(self, amount):
        self.cost = amount

    def increase_cost(self, amount):
        self.set_cost(self.cost + amount)

    def reset_cost(self):
        self.setcost(0)

    def get_system_prompt(self):
        return self.conversation[0]["content"]

    def set_system_prompt(self, new):
        if len(new) <= self.max_characters:
            self.conversation[0]["content"] = new
        else:
            print("Error: ", "system prompt too long")
        self.update_conversation_tokens()

    def add_message(self, role, content):
        self.conversation.append({"role": role, "content": content})
        self.update_conversation_tokens()

    def reply_as_user(self, reply):
        if self.conversation[-1]["role"] in ["system", "assistant"]:
            self.add_message("user", reply)
            return reply
        else:
            print("Error: ", "The user has already replied")
            return "Error: The user has already replied"
    
    def force_reply_as_user(self, reply):
        self.add_message("user", reply)
        return reply

    def reply_as_assistant(self, reply):
        if self.conversation[-1]["role"] == "user":
            self.add_message("assistant", reply)
            return reply

        else:
            print("Error: ", "The assistant has already replied")
            return "Error: The assistant has already replied"

    def force_reply_as_assistant(self, reply):
        self.add_message("assistant", reply)
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

            self.increase_cost_by_tokens(response['usage']['prompt_tokens'], response['usage']['completion_tokens'])
            assistant_response = ""
            if self.stream:
                for chunk in response:
                    try:
                        char = chunk['choices'][0]['delta']['content']
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
            self.force_reply_as_user(message)

        reply = self.generate()
        if not append:
            return reply
        
        if reply:
            self.force_reply_as_assistant(str(reply))

        self.prune()
        return reply

    def delete_first_message(self):
        del self.conversation[2]
        self.update_conversation_tokens()

    def delete_last_message(self):
        self.conversation = self.conversation[:-1]
        self.update_conversation_tokens()

    def reset(self):
        self.conversation = self.conversation[:1]
        self.update_conversation_tokens()
        print(self.conversation)

    def character_count(self):
        return sum([len(c["content"]) for c in self.conversation])
    
    def prune(self):
        count = 0
        while self.conversation_tokens > self.cautious_context_window:
            count += 1
            self.delete_first_message()
            self.update_conversation_tokens()
            print("pruning", count)

        
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
        eel.Conversation_addRole(self.conversation_id, 'Usage', '#1EBB70')

        eel.Conversation_addMessage(self.conversation_id, 'Usage', '')
        eel.Conversation_addMessage(self.conversation_id, 'System', '')

        super().__init__(model=model, system_prompt=system_prompt, temperature=temperature, max_characters=max_characters)
    

    def update_usage_message(self):
        eel.Conversation_modifyMessage(self.conversation_id, 0, 'Usage', f'Tokens: {self.conversation_tokens} / {self.context_window} \t \t Cost: ${round(self.cost, 2)}')

    def set_system_prompt(self, new):
        super().set_system_prompt(new)
        eel.Conversation_modifyMessage(self.conversation_id, 1, 'System', new)

    def add_message(self, role, content):
        super().add_message(role, content)
        eel.Conversation_addMessage(self.conversation_id, role.capitalize(), content)
    
    def delete_first_message(self):
        display_conversation_length = len(self.conversation) + 1
        super().delete_first_message()
        eel.Conversation_removeMessages(self.conversation_id, 2, 1)

    def delete_last_message(self):
        display_conversation_length = len(self.conversation) + 1
        super().delete_last_message()
        eel.Conversation_removeMessages(self.conversation_id, display_conversation_length - 1, 1)

    def reset(self):
        display_conversation_length = len(self.conversation) + 1
        super().reset()
        eel.Conversation_removeMessages(self.conversation_id, 2, display_conversation_length-2)

    def set_cost(self, amount):
        super().set_cost(amount)
        self.update_usage_message()

    def set_conversation_tokens(self, amount):
        super().set_conversation_tokens(amount)
        self.update_usage_message()

    def set_context_window(self, amount):
        super().set_context_window(amount)
        self.update_usage_message()

