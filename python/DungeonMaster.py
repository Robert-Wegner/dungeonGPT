#from prompts import PROMPTS
from package import GPTModel, SummarizedConversation, CharacterSheet
import json

PROMPTS = {
    'combat_system': '',
    'adventure_system': '',
    'dm_initial': '',
    'dm_base':'',
    'combat_initial': '',
    'adventure_initial': '',
    'combat_critic': '',
    'adventure_critic': ''
}
class DungeonMaster:

    def __init__(self):
        self.model_summarize = GPTModel.GPTModel()
        self.conversation = SummarizedConversation.SummarizedConversation(self.model_summarize,
                                                                          recent_max_chars = 500, 
                                                                          current_max_chars = 500,
                                                                          ancient_max_chars = 4000,
                                                                          max_chars = 4000)
        self.terminate = False
        self.model_dm = GPTModel.GPTModel(system_prompt=PROMPTS['dm_base'])
        self.encyclopedia = {}
        self.model_encyclopedia = GPTModel.GPTModel()
        self.model_controller = GPTModel.GPTModel()

        self.char = None
        self.experts = [
            {
                'name': 'combat',
                'version': 'gpt-4',
                'model': None,
                'memory': None,
                'systemPrompt': PROMPTS['combat_system'],
                'initialPrompt': PROMPTS['combat_initial'],
                'criticPrompt': PROMPTS['combat_critic']
            },
            {
                'name': 'adventure',
                'version': 'gpt-3.5-turbo',
                'model': None,
                'memory': None,
                'systemPrompt': PROMPTS['adventure_system'],
                'initialPrompt': PROMPTS['adventure_initial'],
                'criticPrompt': PROMPTS['adventure_critic']
            },
        ]
        self.max_drafts = 6

    def user_reply(self, message):
        self.conversation.add_message("User", message)

    def dm_reply(self, message):
        self.conversation.add_message("DM", message)

    def console_reply(self, message):
        self.conversation.add_message("Console", message)

    def initialize(self):

        for expert in self.experts:
            #expert.model = GPTModel(model=expert.version, system_prompt=expert.systemPrompt)
            #expert.memory = SummarizedConversation(GPTModel.GPTModel(), max_chars=2000, recent_max_chars = 400, 
                #ancient_max_chars = 1000, current_max_chars = 400)
            pass

        self.model_controller = GPTModel.GPTModel(model="gpt-4", temperature=0.5, system_prompt='''
            You are a controller for a Dungeons and Dragons 5th edition video game.
            This means that your task is to call functions that update the state of the system 
            depending on the conversation between the dungeon master and the user.
        ''')


    def get_context(self):
        context = "Here is a summary of the whole adventure so far: \n"
        context += self.conversation.ancient + "\n"
        context += "Here is a summary of only more recent events: \n"
        context += self.conversation.recent + "\n"
        context += "Here is a summary of the currently unfolding events: \n"
        context += self.conversation.current + "\n"
        context += "Finally, here are the most recent exchanges between the DM and the user: \n"
        context += self.conversation.dump(-4)

        context += "\n Character sheet: \n"
        context += self.char.print()

        return context
    
    def create_new_character(self, name, race, character_class, first_skill_proficiency, second_skill_proficiency, STR, DEX, CON, INT, WIS, CHA):
        self.char = CharacterSheet.CharacterSheet(name, race, character_class, first_skill_proficiency, second_skill_proficiency, STR, DEX, CON, INT, WIS, CHA)
        self.available_functions["level_up"] = self.char.level_up

    def execute_controller(self, context):

        available_functions_json = [
            {
                "name": "finish",
                "description": "Call this function to finish your operations when all the necessary changes have been implemented.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "required": []
            },
            {
                "name": "level_up",
                "description": "The character gains 1 level.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "required": []
            },
            {
                "name": "create_character",
                "description": "Creates a new main character. Overwrites the old one!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name"
                        },
                        "character_class": {
                            "type": "string",
                            "description": "Class"
                        },
                        "race": {
                            "type": "string",
                            "description": "Race"
                        },
                        "first_skill_proficiency": {
                            "type": "string",
                            "description": "Initial skill proficiency"
                        },
                        "second_skill_proficiency": {
                            "type": "string",
                            "description": "Initial skill proficiency"
                        },
                        "STR": {
                            "type": "number",
                            "description": "Strength"
                        },
                        "DEX": {
                            "type": "number",
                            "description": "Dexterity"
                        },
                        "CON": {
                            "type": "number",
                            "description": "Constitution"
                        },
                        "INT": {
                            "type": "number",
                            "description": "Intelligence"
                        },
                        "WIS": {
                            "type": "number",
                            "description": "Wisdom"
                        },
                        "CHA": {
                            "type": "number",
                            "description": "Charisma"
                        }
                    },
                },
                "required": []
            },
        ]

        self.available_functions = {
            "create_character": self.create_new_character
        } 

        self.model_controller.reset()
        self.model_controller.set_system_prompt('''
            You are an assistant for a Dungeons and Dragons 5th edition video game.
            You will be shown a summary of the recent events and then the most recent exchange between dungeon master and user.
            Your task is to create an ordered list of changes that have to be made to the user's character sheet. Be precise and detailed.
            The changes that are necessary will be evident from the conversation between the user and the dungeon master. 
            Please ONLY include changes in the list that were EXPLICITLY mentioned by the dungeon master. 
            Do not include changes that only the user has stated. Only the word of the dungeon master matters. Do not jump to conclusions. Do not jump ahead.
            It may be the case that no changes are necessary. In this case, please state so in your reply.
            Please do not elaborate before or after your reply on your task. 
            Start your reply with "Changes to be made to the character sheet". Then follow with the list.
        ''')

        todo_list = self.model_controller.generate_assistant_reply(f'Here is the relevant context: {context}')

        self.model_controller.reset()
        self.model_controller.set_system_prompt('''
            You are a controller for a Dungeons and Dragons 5th edition video game.
            This means that your task is to call functions that update the state of the system 
            depending on the conversation between the dungeon master and the user.
            Initially you will be shown a summary of the recent events and then the most recent exchange between dungeon master and user.
            Then you will be shown an ordered list of changes that should be made to the character sheet.
            You then have to call one or multiple functions that perform the appropriate operations. 
            When you have performed all the required changes, call the finish() function.
        ''')
        self.model_controller.functions = available_functions_json

        total_log = ''

        message = f'Here is the relevant context: {context}\n'
        message += f'{todo_list}\n'
        message += 'Please call a function: Either make a change to the character sheet, or call finish()'
        finished = False
        counter = 0
        fails = 0
        while not finished and fails <= 3 and counter <= 6:
            print(f"\nFails: {fails}\nCounter: {counter}\n")
            print(self.model_controller.pretty_dump())

            reply = self.model_controller.generate_assistant_reply(message, append=False)
            if not isinstance(reply, str):

                if reply.get("name") == "finish":
                    finished = True
                    return total_log
            
                elif reply.get("name"):
                    function_name = reply["name"]
                    function_to_call = self.available_functions[function_name]
                    function_args = json.loads(reply["arguments"])
                    function_to_call(**function_args)

                    total_log = self.char.print_log() + '\n'
                    self.model_controller.reply_as_assistant(f'The function {function_name} has been called. Here is the log of changes that resulted: {total_log}')
                    message = 'Please call a function: Either make another change to the character sheet, or call finish()'

                    self.char.clear_log()

            else:
                fails += 1
                self.model_controller.reply_as_assistant(reply)
                message = 'Please correctly call a function: Either make another change to the character sheet, or call finish()'
            counter += 1

    def get_experts_initial(context):
        return "No tips needed."
    
    def get_experts_criticism(context, draft):
        return "No feedback needed."
    
    def play(self, message):
        self.user_reply(message)

        self.model_dm.reset()
        context = self.get_context()

        initial_prompt = context + PROMPTS['dm_initial'] + self.get_experts_initial(context)
        draft = self.model_dm.generate_assistant_reply(initial_prompt)

        draft_num = 1
        finished = False
        while draft_num < self.max_drafts and not finished:
            criticism = self.get_experts_criticism(context, draft)

            controller_decision = self.model_controller.generate_assistant_reply(draft, criticism)
            
            self.model_dm.generate_assistant_reply(criticism)

            draft_num += 1


dm = DungeonMaster()
dm.initialize()
dm.execute_controller("DM: So what will be your character? User: My character will be a Cleric named Adric. He is a dwarf. His stats are, in order, 10, 11, 12, 13, 14, 15. His proficiencies are Athletics and Medicine.")