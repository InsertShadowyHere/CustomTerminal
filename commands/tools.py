"""
This module contains utility functions for the console.
Functions:
define
translate
weather
bored
monies
search
where
"""
import pyautogui
import webbrowser

def cmd_where(console, args):
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