

from .files import read_file

SUMMARIZER_PROMPT = read_file("prompts/summarizer_prompt.txt")


def msg_to_string(msg):
    return msg['role'] + ": " + msg['content']

def count_conv_chars(conv):
    return sum([len(msg['content']) for msg in conv])

class SummarizedConversation:

    def __init__(self, model, max_chars=4000, recent_max_chars = 800, 
                 ancient_max_chars = 2000, current_max_chars = 800, ratio=0.5):
        self.conversation = []
        self.ancient = ""
        self.recent = ""
        self.current = ""
        self.model = model
        self.max_chars = max_chars
        self.recent_max_chars = recent_max_chars
        self.ancient_max_chars = ancient_max_chars
        self.current_max_chars = current_max_chars
        self.ratio = ratio
        self.current_characters = 0
        self.max_attempts = 5
        self.current_update_interval = 3
        self.current_update_counter = 0

    def dump(self, start=0):
        return '\n'.join([msg_to_string(msg) for msg in self.conversation[start:]])
    
    def add_message(self, role, content):
        self.conversation.append({'role': role, 'content': content})
        self.current_characters = count_conv_chars(self.conversation)
        if self.current_characters > self.max_chars:
            self.summarize_recent_()      
        if self.current_update_counter == self.current_update_interval:
            self.summarize_current()
            self.current_update_counter += 0
        else:
            self.current_update_counter += 1

    def summarize_current(self):
        self.model.reset()
        current_prompt = "Consider the following summary of a text: \n"
        current_prompt += self.ancient 
        current_prompt += "Here is a summary of the most recent part of the text: \n"
        current_prompt += self.recent
        current_prompt = "Given this context, please summarize this continuation of the text: " + self.dump() + "\n"
        
        self.current = self.model.generate_assistant_reply(current_prompt)

        while len(self.ancient) > self.current_max_chars and attempts < self.max_attempts:
            attempts += 1
            prompt = "The current summary is " + str(len(self.current)) + " characters long. \n"
            prompt += "Please shorten it to below " + str(self.current_max_chars) + " characters. \n"

            self.current = self.model.generate_assistant_reply(prompt)

        print("current attempts: ", attempts)

        if len(self.current) > self.current_max_chars:
            self.current = self.current[:self.current_max_chars]
            print("pruning necessary")

    def summarize_recent_ancient(self):
        print("summarizing")
        self.model.reset()

        new_start = 0
        while count_conv_chars(self.conversation[new_start:]) > self.ratio * self.max_chars:
            new_start += 1

        deleted_messages = self.conversation[:new_start]
        self.conversation = self.conversation[new_start:]

        if self.ancient == "": 
            ancient_prompt = "Please summarize this text: "
            ancient_prompt += self.dump()
        else:
            ancient_prompt = "Consider the following summary of a text: \n"
            ancient_prompt += self.ancient 
            ancient_prompt += "Here is a summary of the most recent part of the text: \n"
            ancient_prompt += self.recent
            ancient_prompt += "Please update the former summary to include the information of the latter summary."
            ancient_prompt += "Note that the former summary takes much higher priority here."
            ancient_prompt += "Try to only keep information from the latter summary that has the same level of importance"
            ancient_prompt += " as the information already contained in the former summary."
            ancient_prompt += "Sometimes the fomer summary will need barely any modification at all."

        ancient_prompt += "Please keep the length of your summary below " + str(self.ancient_max_chars) + " characters. \n"

        self.model.set_system_prompt(SUMMARIZER_PROMPT)
        self.ancient = self.model.generate_assistant_reply(ancient_prompt)
        print(self.ancient)
        attempts = 0

        while len(self.ancient) > self.ancient_max_chars and attempts < self.max_attempts:
            attempts += 1
            prompt = "The current summary is " + str(len(self.ancient)) + " characters long. \n"
            prompt += "Please shorten it to below " + str(self.ancient_max_chars) + " characters. \n"

            self.ancient = self.model.generate_assistant_reply(prompt)
            print(self.ancient)

        print("ancient attempts: ", attempts)

        if len(self.ancient) > self.ancient_max_chars:
            self.ancient = self.ancient[:self.ancient_max_chars]
            print("pruning necessary")
        
        self.model.reset()

        recent_prompt = "Consider the following summary of a text: \n"
        recent_prompt += self.ancient + "\n"
        recent_prompt += "The following is the most recent part of the text."
        recent_prompt += "Please summarize the content of only this section: \n"
        recent_prompt += '\n'.join([msg_to_string(msg) for msg in deleted_messages]) + "\n"
        recent_prompt += "Please keep the length of your summary below " + str(self.recent_max_chars) + "characters. \n"

        self.model.set_system_prompt(SUMMARIZER_PROMPT)
        self.recent = self.model.generate_assistant_reply(recent_prompt)

        attempts = 0

        while len(self.recent) > self.recent_max_chars and attempts < self.max_attempts:
            attempts += 1
            prompt = "The current summary is " + str(len(self.recent)) + " characters long. \n"
            prompt += "Please shorten it to below " + str(self.recent_max_chars) + " characters. \n"

            self.recent = self.model.generate_assistant_reply(prompt)

        print("recent attempts: ", attempts)
        if len(self.recent) > self.recent_max_chars:
            self.recent = self.recent[:self.recent_max_chars]
            print("pruning necessary")

        self.model.reset()