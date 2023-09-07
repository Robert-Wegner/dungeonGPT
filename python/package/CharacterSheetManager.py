from CharacterSheet import CharacterSheet
from GPTModel import GPTModel
import json

class CharacterSheetManager:

    def __init__(self):

        self.character = None
        self.update_functions()
        self.update_functions_json()

        self.log = ''
        self.total_log = ''
        self.model = GPTModel(model="gpt-3.5-turbo", temperature=0.6)
    
    def execute(self, context):
        extended_context = f'Here is the relevant context: {context}\n Character sheet: {("The user currently has no character sheet. " if not self.character else self.character.print())}'
        self.model.reset()
        self.model.set_system_prompt('''
            You are an assistant for a Dungeons and Dragons 5th edition video game.
            You will be shown a summary of the recent events and then the most recent exchange between dungeon master and user.
            Your task is to create an ordered list of changes that have to be made to the user's character sheet. Be precise and detailed.
            The changes that are necessary will be evident from the conversation between the user and the dungeon master. 
            Please ONLY include changes in the list that were EXPLICITLY mentioned by the dungeon master. 
            Do not include changes that only the user has stated. Only the word of the dungeon master matters. Do not jump to conclusions. Do not jump ahead.
            It may be the case that no changes are necessary. In this case, please state so in your reply.
            Sometimes a change is being created between the DM and the user but not all the information is determined yet. 
            Be patient in this case and only list changes once all the choices have been made.
            DO NOT make up information that the user or DM did not create if an argument is missing for a function.
            Often the DM and the usere are just having a chat and there are absolutely no changes necessary.
            Please do not elaborate before or after your reply on your task. 
            Start your reply with "Changes to be made to the character sheet". Then follow with the list.
        ''')

        #todo_list = self.model.generate_assistant_reply(f"CONTEXT: '''{extended_context}''' \n. Please reply with the list of necessary changes.")

        #print(f"\n \n ----- {todo_list} ------ \n \n")

        self.model.reset()
        self.model.set_system_prompt('''
            You are a controller for a Dungeons and Dragons 5th edition video game.
            This means that your task is to call functions that update the state of the system 
            depending on the conversation between the dungeon master and the user.
            Initially you will be shown a summary of the recent events and then the most recent exchange between dungeon master and user.
            Then you will be shown an ordered list of changes that should be made to the character sheet.
            You then have to call one or multiple functions that perform the appropriate operations. 
            Be patient in this case and call functions when a change is really necessary.
            DO NOT make up information that the user or DM did not create if an argument is missing for a function.
            Often the DM and the usere are just having a chat and there are absolutely no changes necessary.
            When you call a function, make sure to give ALL parameters, as all of them are strictly required.
            When you have performed all the required changes, call the finish() function.
            Please do not elaborate before or after your reply on your task. 
        ''')
        self.model.functions = self.functions_json

        self.log = ''
        self.total_log = ''

        message = extended_context
        #message += f'{todo_list}\n'
        initial_message = 'Please call a function: Call the finish function unless there are necessary changes to be made.'
        positive_message = 'Please call a function: Call the finish function unless there are still necessary changes to be made.'
        negative_message = 'Please correctly call a function: Call the finish function unless there are still necessary changes to be made.'
        message += initial_message
        finished = False
        counter = 0
        fails = 0
        while not finished and fails <= 3 and counter <= 6:
            print(f"\nFails: {fails}\nCounter: {counter}\n")
            print(self.model.pretty_dump())

            reply = self.model.generate_assistant_reply(message, append=False)
            if not isinstance(reply, str):

                if reply.get("name") == "finish":
                    finished = True
                    return self.total_log
            
                elif reply.get("name"):
                    function_name = reply["name"]
                    function_to_call = self.functions[function_name]
                    function_args = json.loads(reply["arguments"])
                    try:
                        #print("----------", function_to_call, function_args)
                        #function_to_call(**function_args)
                        print("------------ READY!!!")
                        self.create_new_character("testname", "Dwarf", "Wizard", "Medicine", "Athletics", 10, 11, 12, 13, 14, 15)
                        print("------------ SUCCESS!!!")
                        self.update_functions()
                        self.update_functions_json()
                        if self.character:
                            self.log = self.character.print_log() + '\n'
                            self.total_log += self.log + '\n'
                            self.character.clear_log()

                        self.model.reply_as_assistant(f'The function {function_name} has been called. Here is the log of changes that resulted: {self.log}')
                        message = positive_message

                    except Exception as error:
                        #print("----------", error, type(error).__name__)
                        self.log = f"Could not execute {function_name} with arguments {str(function_args)}.\n Error: {error}."
                        self.model.reply_as_assistant(f'The function {function_name} has been called but an error occured: {self.log}')
                        message = negative_message
                        fails += 1


            else:
                fails += 1
                self.model.reply_as_assistant(reply)
                message = negative_message
                counter += 1

    def create_new_character(self, name, race, character_class, first_skill_proficiency, second_skill_proficiency, STR, DEX, CON, INT, WIS, CHA):
        print("----------CLASS: ", character_class)
        self.character = CharacterSheet(name, race, character_class, first_skill_proficiency, second_skill_proficiency, STR, DEX, CON, INT, WIS, CHA)
        print("DONE")
        self.update_functions()
        self.update_functions_json()
        self.log = f'Created a new character: {name}, the {race} {character_class}! \n'

    def update_functions(self):
        self.functions = {
            'create_new_character': self.create_new_character
        }
        if self.character:
            self.functions.update({
                'set_spell_attack_bonus': self.character.set_spell_attack_bonus,
                'set_spell_save_DC': self.character.set_spell_save_DC,
                'set_proficiency_bonus': self.character.set_proficiency_bonus,
                'set_skill_bonus': self.character.set_skill_bonus,
                'add_skill_proficiency': self.character.add_skill_proficiency,
                'remove_skill_proficiency': self.character.remove_skill_proficiency,
                'set_AC': self.character.set_AC,
                'set_max_HP': self.character.set_max_HP,
                'set_HP': self.character.set_HP,
                'set_ability_score': self.character.set_ability_score,
                'use_spell_slots': self.character.use_spell_slots,
                'gain_spell_slots': self.character.gain_spell_slots,
                'use_sorcery_points': self.character.use_sorcery_points,
                'gain_sorcery_points': self.character.gain_sorcery_points,
                'create_spell_slot_from_sorcery_points': self.character.create_spell_slot_from_sorcery_points,
                'create_sorcery_points_from_spell_slot': self.character.create_sorcery_points_from_spell_slot,
                'activate_rage': self.character.activate_rage,
                'activate_wild_shape': self.character.activate_wild_shape,
                'deactivate_wild_shape': self.character.deactivate_wild_shape,
                'add_condition': self.character.add_condition,
                'remove_condition': self.character.remove_condition,
                'add_inventory_item': self.character.add_inventory_item,
                'remove_inventory_item': self.character.remove_inventory_item,
                'modify_inventory_item': self.character.modify_inventory_item,
                'add_equipmentitem': self.character.add_equipment_item,
                'remove_equipment_item': self.character.remove_equipment_item,
                'modify_equipment_item': self.character.modify_equipment_item,
                'add_spell': self.character.add_spell,
                'award_XP': self.character.award_XP,
                'level_up': self.character.level_up,
                'level_up_with_ability_score_improvement': self.character.level_up_with_ability_score_improvement,
                'level_up_with_feat': self.character.level_up_with_feat,
                'add_feature': self.character.add_feature,
                'remove_feature': self.character.remove_feature,
                'rest': self.character.rest,
            })

    def update_functions_json(self):

        self.functions_json = []

        self.functions_json.extend([
            {
                "name": "create_new_character",
                "description": "Creates a new main character. Overwrites the old one!",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name"
                        },
                        "race": {
                            "type": "string",
                            "description": "Race"
                        },
                        "character_class": {
                            "type": "string",
                            "description": "Class"
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
                "required": ["name", "character_class", "race", "first_skill_proficiency", "second_skill_proficiency", "STR", "DEX", "CON", "INT", "WIS", "CHA"]
            },
            {
                "name": "finish",
                "description": "Finish your work. Call this function when all the necessary changes to the character sheet have been implemented.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    }
                },
                "required": []
            }
        ])
        if not self.character:
            return 0

        if self.character.character_class == 'Barbarian':
            self.functions_json.extend([
                {
                    "name": "activate_rage",
                    "description": "Activates the Barbarian's rage ability.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        }
                    },
                    "required": []
                }
            ])
        
        if self.character.character_class == "Druid":
            self.functions_json.extend([
                {
                "name": "activate_wild_shape",
                "description": "Activates the Druid's wild shape ability.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "beast_name": {
                            "type": "string",
                            "description": "The beast the Druid will transform into"
                        }
                    }
                },
                "required": ["beast_name"]
                },
                {
                    "name": "deactivate_wild_shape",
                    "description": "Deactivates the Druid's wild shape ability.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        }
                    },
                    "required": []
                }
            ])

        if self.character.character_class == "Sorcerer":
            self.functions_json.extend([
                {
                    "name": "use_sorcery_points",
                    "description": "Uses up a number of sorcery points.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "amount": {
                                "type": "number",
                                "description": "Amount of sorcery points that are used."
                            },
                        }
                    },
                    "required": ["amount"]
                },
                {
                    "name": "gain_sorcery_points",
                    "description": "Gains up a number of sorcery points.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "amount": {
                                "type": "number",
                                "description": "Amount of sorcery points that are gained."
                            },
                        }
                    },
                    "required": ["amount"]
                },
                {
                    "name": "create_spell_slot_from_sorcery_points",
                    "description": "Creates a spell slot of desired level from sorcery points.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "number",
                                "description": "Level of spell slot created."
                            },
                        }
                    },
                    "required": ["level"]
                },
                {
                    "name": "create_sorcery_points_from_spell_slot",
                    "description": "Creates sorcery points from a spell slot of desired level.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "level": {
                                "type": "number",
                                "description": "Level of spell slot used."
                            },
                        }
                    },
                    "required": ["level"]
                },
            ])

        if self.character.level_up_state == "normal":
            self.functions_json.extend([
                {
                    "name": "level_up",
                    "description": "Increases the character's level by 1.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                        }
                    },
                    "required": []
                }
            ]),
        
        if self.character.level_up_state == "special":
            self.functions_json.extend([
                {
                    "name": "level_up_with_ability_score_improvement",
                    "description": "Increases the character's level by 1. In addition, two ability scores are increased by 1. The same ability can be chosen two times.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "first_ability_name": {
                                "type": "string",
                                "description": "One of 'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'."
                            },
                            "second_ability_name": {
                                "type": "string",
                                "description": "One of 'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'."
                            }
                        }
                    },
                    "required": ["first_ability_name", "second_ability_name"]
                },
                {
                    "name": "level_up_with_feat",
                    "description": "Increases the character's level by 1. In addition, a feat is obtained.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "feat_name": {
                                "type": "string",
                                "description": "Name of the feat."
                            },
                        }
                    },
                    "required": ["feat_name"]
                }
            ])
            
        self.functions_json.extend([
            {
                "name": "set_spell_attack_bonus",
                "description": "Sets the spell attack bonus to a new integer value.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_bonus": {
                            "type": "number",
                            "description": "The new spell attack bonus."
                        },
                    }
                },
                "required": ["new_bonus"]
            },
            {
                "name": "set_spell_save_DC",
                "description": "Sets the spell save DC to a new integer value.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_DC": {
                            "type": "number",
                            "description": "The new spell save DC bonus."
                        },
                    }
                },
                "required": ["new_DC"]
            },
            {
                "name": "set_proficiency_bonus",
                "description": "Sets the proficiency bonus to a new integer value and updates other impacted stats.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_bonus": {
                            "type": "number",
                            "description": "The new proficiency bonus."
                        },
                    }
                },
                "required": ["new_bonus"]
            },
            {
                "name": "set_skill_bonus",
                "description": "Sets the skill bonus for a skill (such as Athletics) to a new integer value. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": 'The name of the skill (capitalized).'
                        },
                        "new_bonus": {
                            "type": "number",
                            "description": "The new bonus."
                        },
                    }
                },
                "required": ["skill_name", "new_bonus"]
            },
            {
                "name": "add_skill_proficiency",
                "description": "Adds a skill proficiency by name. The name must be capitalized.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": 'The name of the skill (capitalized).'
                        },
                    }
                },
                "required": ["skill_name"]
            },
            {
                "name": "remove_skill_proficiency",
                "description": "Removes a skill proficiency by name. The name must be capitalized.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": 'The name of the skill (capitalized).'
                        },
                    }
                },
                "required": ["skill_name"]
            },
            {
                "name": "set_AC",
                "description": "Sets AC to a new integer value. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_AC": {
                            "type": "number",
                            "description": "The new AC."
                        },
                    }
                },
                "required": ["new_AC"]
            },
            {
                "name": "set_max_HP",
                "description": "Sets max_HP to a new integer value. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_max_HP": {
                            "type": "number",
                            "description": "The new max_HP."
                        },
                    }
                },
                "required": ["new_max_HP"]
            },
            {
                "name": "set_HP",
                "description": "Sets HP to a new integer value. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "new_HP": {
                            "type": "number",
                            "description": "The new HP."
                        },
                    }
                },
                "required": ["new_HP"]
            },
            {
                "name": "set_ability_score",
                "description": "Sets one of the abilities 'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA' to a new integer value and updated other impacted stats. ",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The ability score which is to be set to a new value."
                        },
                        "value": {
                            "type": "number",
                            "description": "The new value, must be an integer."
                        }
                    }
                },
                "required": ["name", "value"]
            },
            {
                "name": "use_spell_slots",
                "description": "Uses up a number of spell slots of a certain level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spell_level": {
                            "type": "number",
                            "description": "The level of spell slot to use."
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount of spell slots to use."
                        },
                    }
                },
                "required": ["spell_level", "amount"]
            },
            {
                "name": "gain_spell_slots",
                "description": "Gains up a number of spell slots of a certain level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spell_level": {
                            "type": "number",
                            "description": "The level of spell slot to gain."
                        },
                        "amount": {
                            "type": "number",
                            "description": "The amount of spell slots to gain."
                        },
                    }
                },
                "required": ["spell_level", "amount"]
            },
            {
                "name": "add_condition",
                "description": "Adds a temporary condition.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the condition."
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the condition."
                        },
                        "duration_days": {
                            "type": "number",
                            "description": "Number of days as an integer."
                        },
                        "duration_hours": {
                            "type": "number",
                            "description": "Number of hours as an integer."
                        },
                        "duration_minutes": {
                            "type": "number",
                            "description": "Number of_minutes as an integer."
                        },
                        "duration_seconds": {
                            "type": "number",
                            "description": "Number of seconds as an integer."
                        }
                    }
                },
                "required": ["name", "description", "duration_days", "duration_hours", "duration_minutes", "duration_seconds"]
            },
            {
                "name": "remove_condition",
                "description": "Removes a temporary condition.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the condition."
                        }
                    }
                },
                "required": ["name"]
            },
            {
                "name": "add_inventory_item",
                "description": "Adds an item to the character's inventory. This means that it is not currently equipped.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the item."
                        }
                    }
                },
                "required": ["name", "description"]
            },
            {
                "name": "remove_inventory_item",
                "description": "Removes an item from the character's inventory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        }
                    }
                },
                "required": ["name"]
            },
            {
                "name": "modify_inventory_item",
                "description": "Modifies the description of an item in the character's inventory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        },
                        "description": {
                            "type": "string",
                            "description": "New description of the item."
                        }
                    }
                },
                "required": ["name", "description"]
            },
            {
                "name": "add_equipment_item",
                "description": "Adds an item to the character's equipment. This means that it is now equipped and ready to use.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the item."
                        }
                    }
                },
                "required": ["name", "description"]
            },                                
            {
                "name": "remove_equipment_item",
                "description": "Removes an item from the character's equipment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        }
                    }
                },
                "required": ["name"]
            },
            {
                "name": "modify_equipment_item",
                "description": "Modifies an item of the character's equipment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the item."
                        },
                        "description": {
                            "type": "string",
                            "description": "New description of the item."
                        }
                    }
                },
                "required": ["name", "description"]
            }, 
            {
                "name": "add_spell",
                "description": "Adds a new spell to the character's knowledge.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "spell_name": {
                            "type": "string",
                            "description": "The name of the spell"
                        },
                        "spell_level": {
                            "type": "number",
                            "description": "The level of the spell"
                        },
                        "spell_description": {
                            "type": "string",
                            "description": "The description of the spell"
                        },
                    }
                },
                "required": ["spell_name", "spell_level", "spell_description"]
            },
            {
                "name": "award_XP",
                "description": "Awards XP (experience points).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "amount": {
                            "type": "number",
                            "description": "The number of experience points."
                        },
                    }
                },
                "required": ["amount"]
            },
            {
                "name": "add_feature",
                "description": "Adds a feature to the character. This can be essentially any additional property for the character.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature."
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the feat."
                        },
                    }
                },
                "required": ["feature_name", "description"]
            },
            {
                "name": "remove_feature",
                "description": "Removes a feature from the character.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "feature_name": {
                            "type": "string",
                            "description": "Name of the feature."
                        },
                    }
                },
                "required": ["feature_name"]
            },
            {
                "name": "rest",
                "description": "The character performs a rest according to the rules of Dungeons and Dragons 5e. Long rests and short rests are treated identically, meaning that any rest is a long rest.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    }
                },
            }
        ])


manager = CharacterSheetManager()

while True:
    manager.execute(input('--> '))

from pprint import pprint
pprint(char.functions_json)
