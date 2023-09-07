from package.GPTModel import GPTModel
from package.SummarizedConversation import SummarizedConversation
import eel
import os

eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')
#eel.init('C:/Users/rober/soure/dungeonGPT/python/web')
model = GPTModel()
conversation = SummarizedConversation(model=model)

model_alice = GPTModel(system_prompt="Please take the role of Alice. Please continue the conversation indefinetly. Do not end it. If it becomes repetitive, change the subject")
model_bob = GPTModel(system_prompt="Please take the role of Alice. Please continue the conversation indefinetly. Do not end it. If it becomes repetitive, change the subject")

@eel.expose
def add_message(role, content):
    conversation.add_message(role, content)

@eel.expose
def bob_reply(message):
    conversation.add_message("Alice", message)
    return model_bob.generate_assistant_reply(message)

@eel.expose
def alice_reply(message):
    conversation.add_message("Bob", message)
    return model_alice.generate_assistant_reply(message) 

@eel.expose
def get_conversation():
    #print(conversation.dump())
    return conversation.conversation

@eel.expose
def get_ancient():
    return conversation.ancient

@eel.expose
def get_recent():
    return conversation.recent

@eel.expose
def test_function():
    
    print("hello")
    #eel.cringe()
    eel.Conversation_addMessage("main_conversation", "user", "hello!");

eel.start("index.html")

