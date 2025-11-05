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

def cmd_where(console, args):
    """Outputs current mouse position, relative to top left of screen.
    FORMAT: where"""
    pt = pyautogui.position()
    console.output(f"({pt.x}, {pt.y})", "green")


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
    try:
        with open("resources/imbored.txt", "r") as f:
            activities = f.read()
        console.output(activities, "aqua")
    except FileNotFoundError:
        console.output("no script kiddies allowed 🙅‍♂️🙅‍♂️🙅‍♂️ (developer only, sorry)", "red")


def cmd_todo(console, args):
    """Edits or displays the to-do list."""
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