"""General utility commands
This module contains utility functions for the console.
Functions:
define
translate
weather
imbored
monies
search
where
"""
import pyautogui
import webbrowser
from random import randint

def cmd_where(console, args):
    """Outputs current mouse position, relative to top left of screen.
    FORMAT: where"""
    pt = pyautogui.position()
    console.output(f"({pt.x}, {pt.y})", "aqua")


# TODO - make this safe
def cmd_math(console, args):
    """Evaluates arithmetic expressions
    NOTE: MAKE SAFER LATER?"""
    exp = ''.join(args)
    if "^" in exp:
        exp = exp.replace("^", "**")
    valid = "1234567890-+/*.()"
    for i in exp:
        if i not in valid:
            console.output("only numbers and operators allowed", "red")
            return

    console.output(str(eval(exp)), "aqua")


def cmd_search(console, args):
    query = ' '.join(args)
    webbrowser.open(f"https://www.google.com/search?q={query}")
    console.output("success", "green")


def cmd_imbored(console, args):
    """Outputs what to do when you're bored.
    FORMAT: imbored        note: DEV ONLY (sorry)"""
    try:
        with open("resources/imbored.txt", "r") as f:
            activities = f.read()
        console.output(activities, "aqua")
    except FileNotFoundError:
        console.output("no script kiddies allowed 🙅‍♂️🙅‍♂️🙅‍♂️ (developer only, sorry)", "red")


def cmd_todo(console, args):
    """Edits or displays the to-do list.
    FORMAT: todo [add/remove] [item/index]"""
    try:
        if not args:
            text = [f"{n+1}. {item}" for n, item in enumerate(console.todo)]
            console.output('\n'.join(text), "aqua")
            return

        match args[0]:
            case "add":
                if not args[1:]:
                    console.output("invalid syntax", "red")
                    return
                item = " ".join(args[1:])
                console.todo.append(item)
                console.output(f"Added {item} to to-do list", "green")

            case "remove" | "delete":
                index = int(args[1]) - 1
                popped = console.todo.pop(index)
                console.output(f"Removed {popped} from to-do list", "green")
    except IndexError:
        console.output("invalid syntax", "red")
    except Exception as e:
        console.log(e)


def cmd_roll(console, args):
    """Rolls a die with the given number of sides.
    FORMAT: roll [sides] -c (concise output, returns only the number)"""
    try:
        sides = 6
        concise = False

        for arg in args:
            if arg == "-c":
                concise = True
            else:
                sides = int(arg)

        if concise:
            console.output(f"{randint(1, sides)}", "aqua")
            return
        else:
            console.output(f"You rolled a {randint(1, sides)}", "aqua")
    except ValueError:
        console.output("number of sides must be a number", "red")
    except Exception as e:
        console.log(e)
        console.output("something went wrong", "red")


def cmd_flip(console, args):
    """Flips a coin.
    FORMAT: flip"""
    result = "heads" if randint(0, 1) == 0 else "tails"
    console.output(f"You got {result}!", "blue")


# TODO - actually find exchange rate
def cmd_monies(console, args):
    """Outputs exchange rates for various currencies.
    FORMAT: monies [num of] [currency1] [currency2]"""
    try:
        curr_1_val = args[0]
        curr_1 = args[1]
        curr_2 = args[2]
        print(curr_1)
        print(curr_2)
        rate = 1
        console.output(f"{curr_1_val} {curr_1} is equal to {curr_1_val*rate} {curr_2}", "blue")
    except IndexError:
        console.output("invalid syntax", "red")
    except Exception as e:
        console.log(e)
        console.output("something went wrong", "red")
