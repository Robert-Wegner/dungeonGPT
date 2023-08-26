from package import GPTModel, SummarizedConversation
import json
import os
import random
import re

def parse_commands(s):
    # Define the regular expression pattern for commands
    pattern = r'(ROLL|WRITE|OVERWRITE|READ)\[(.+?)\]'
    
    # Search the string for commands and return the results as tuples
    return re.findall(pattern, s)

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

    return str(rolls)

def command_input(text, commands):
    command_results = []
    for com in commands:
        index = 0
        while index < len(text):
            index = text.find(com['name'] + '(', index)
            if index == -1:
                break
            j = text.find(')', index)
            if j != -1:
                i = index + len(com['name'])
                if j == i + 1:
                    args = []
                else:
                    args = [s.strip() for s in text[i + 1:j].split(',')]
                try:
                    if len(args) == 0:
                        res = com['function']()
                    else:
                        res = com['function'](*args)
                except:
                    print("Error executing command")
                    res = "Error"

                command_results.append({'name': com['name'], 'result': res})
            index += 1
    return command_results
    
COMMANDS = [
    {
        'name': 'ROLL',
        'function': lambda d: roll_dice(d)
    },
    {
        'name': 'HELLO',
        'function': lambda x: True
    },
    {
        'name': 'DUMP',
        'function': lambda x: True
    },
]

def system_message_from_command_results(command_results):
    system_message = "COMMAND RESULTS: \n"
    for com in command_results:
        #print("command_Results: ", command_results)
        system_message += com['name'] + ": " + com['result'] + "\n"
    return system_message


def dm_replies(message):
    
def user_replies(message):
    dm_replies(message)


def main():

    user_dm_conv = SummarizedConversation.SummarizedConversation()
    

    model = GPTModel.GPTModel()
    model.stream = False
    COMMANDS[2]['function'] = model.dump

    while True:
        user_message = input("\n User: ")
        command_results = command_input(user_message, COMMANDS)
        if len(command_results) > 0:
            system_message = system_message_from_command_results(command_results)
            print("\n System: " + system_message)
            user_message += "\n System: " + system_message

        reply = model.generate_assistant_reply(user_message)
        print("\n Assistant: " + reply, end="")
        command_results = command_input(reply, COMMANDS)

        if len(command_results) > 0: 
            system_message = system_message_from_command_results(command_results)
            print("\n System: " + system_message, end="")
            reply = model.generate_assistant_reply(system_message)
            print("\n Assistant: " + reply, end="")

        print("\n")

if __name__ == "__main__":
    main()


