from package.GPTModel import GPTModel, DisplayedGPTModel
from package.SummarizedConversation import SummarizedConversation
import eel
import os

eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')

@eel.expose
def test_function():
    

    model = DisplayedGPTModel('main_grid', 'gpt_conversation', model='gpt-3.5-turbo')
    model2 = DisplayedGPTModel('main_grid', 'gpt_conversation2', model='gpt-3.5-turbo')
    reply = "Let's talk about a random subject!"

    eel.Grid_createAndAddConversation('main_grid', 'debugbox')
    eel.Grid_createAndAddConversation('main_grid', 'debugbox2')
    eel.Conversation_addMessage('debugbox', 'Console', '')
    eel.Conversation_addMessage('debugbox2', 'Console', '')

    model2.force_reply_as_assistant(reply)

    count = 0
    while True:
        count += 1
        reply = model.generate_assistant_reply(message=reply)
        reply = model2.generate_assistant_reply(message=reply)

        eel.Conversation_modifyMessage('debugbox', 0, 'Console', model.pretty_dump())
        eel.Conversation_modifyMessage('debugbox2', 0, 'Console', model2.pretty_dump())

        action = input("--> ")

        if action == "del first":
            model.delete_first_message()

        if action == "del last":
            model.delete_last_message()

eel.start("index.html")

