import requests
import json
import os
import random
import re
from package import GPTModel
def roll_dice(dice_expression):
    if not re.fullmatch(r"\d*d\d+(\+\d+)?", dice_expression):
        return "Invalid dice expression."

    num_dice, die_type_plus = [x for x in dice_expression.split('d') if x]
    die_type = die_type_plus.split('+')[0]
    modifier = die_type_plus.split('+')[1] if '+' in die_type_plus else 0
  
    num_dice = int(num_dice) if num_dice else 1
    die_type = int(die_type)
    modifier = int(modifier)

    rolls = [random.randint(1, die_type) for _ in range(num_dice)]
    rolls = [roll + modifier for roll in rolls]

    return rolls


if __name__ == "__main__":
    model = GPTModel.GPTModel()
    model.functions = [
        {
            "name": "greeting",
            "description": "Greets the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "friendliness": {
                        "type": "number",
                        "description": "How friendly the greeting should be"
                    },
                    "gender": {
                        "type": "number",
                        "enum": ["0", "3"]
                    }
                },
                "required": ["gender"]
            }
        },
        {
            "name": "goodbye",
            "description": "Wishes the user farewell",
            "parameters": {
                "type": "object",
                "properties": {
                    "friendliness": {
                        "type": "number",
                        "description": "How friendly the greeting should be"
                    },
                    "gender": {
                        "type": "number",
                        "enum": ["0", "3"]
                    }
                },
                "required": ["gender"]
            }
        }
    ]
    reply = model.generate_assistant_reply("Alright, see you later.")
    
    args = reply['arguments']
    args = json.loads(args)
    print(type(args['friendliness']))
    