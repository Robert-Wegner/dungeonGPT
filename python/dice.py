import os
import random
import re


def roll_dice(dice_expression):
    if not re.fullmatch(r"\d*d\d+", dice_expression):
        return "Invalid dice expression."

    num_dice, die_type = [int(x) for x in dice_expression.split('d') if x]
    rolls = [random.randint(1, die_type) for _ in range(num_dice)]

    return rolls

if __name__ == "__main__":
    print(roll_dice("100d12"))