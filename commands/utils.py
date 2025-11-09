"""General utility commands
This module contains utility functions for the console.
"""
import pyautogui
import webbrowser
from random import randint
from asteval import Interpreter
from pint import UnitRegistry
from PIL import ImageGrab
from datetime import datetime
import time
from pyperclip import copy

NAMES_FOR_REVOLUTIONS = []
with open('resources/paths', 'r') as f:
    screenshots_path = f.readlines()[0]

def cmd_where(console, args):
    """Outputs current mouse position, relative to top left of screen.
    FORMAT: where"""
    pt = pyautogui.position()
    console.output(f"({pt.x}, {pt.y})", "aqua")


def cmd_math(console, args):
    """Evaluates arithmetic expressions
    FORMAT: math [args]     """
    exp = ''.join(args)
    ast_eval = Interpreter(no_print=True)
    result = ast_eval(exp)
    if ast_eval.error is not None:
        console.output("expression couldn't be evaluated", "red")
        return
    console.output(str(result), "aqua")


def cmd_search(console, args):
    """Searches in the primary web browser.
    FORMAT: search [term]"""
    query = ' '.join(args)
    webbrowser.open(f"https://www.google.com/search?q={query}")
    console.output("success", "green")
    console.disappear()


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
            with open("resources/todo", "r") as f:
                items = f.read().splitlines()
                text = '\n'.join(f"{n + 1}. {item}" for n, item in enumerate(items))
            if text == "":
                console.output("To-do list is empty, add an item", "aqua")
                return
            console.output(text, "aqua")
            return

        match args[0]:
            case "add" | "a":
                if len(args) == 1:
                    console.output("no item specified", "red")
                    return
                item = " ".join(args[1:])
                with open("resources/todo", "a") as f:
                    f.write(item + "\n")
                console.output(f"Added {item} to to-do list", "green")
            case "edit" | "e":
                index = int(args[1])-1
                with open("resources/todo", "r") as f:
                    items = f.readlines()
                if len(items) <= index:
                    console.output("that item doesn't exist", "red")
                    return
                items[index] = " ".join(args[2:]) + "\n"
                with open("resources/todo", "w") as f:
                    f.write("".join(items))
                console.output(f"Set item {index+1} to {items[index][:-1]}", "green")
            case "remove" | "delete" | "del" | "rem" | "r":
                if len(args) > 1:
                    index = int(args[1]) - 1
                    with open("resources/todo", "r") as f:
                        items = f.readlines()
                    if len(items) <= index:
                        console.output("that item doesn't exist", "red")
                        return
                    popped = items.pop(index)
                    with open("resources/todo", "w") as f:
                        f.write(''.join(items))
                    console.output(f"Removed {popped[:-1]} from to-do list", "green")
                else:
                    console.output("no item specified", "red")
            case "clear" | "c":
                with open("resources/todo", "w") as f:
                    f.write("")
                console.output("Cleared to-do list", "green")
            case _:
                console.output("invalid syntax", "red")
    except IndexError:
        console.output("invalid syntax", "red")
    except FileNotFoundError:
        console.output("To-do list is empty, add an item", "aqua")
    except ValueError:
        console.output("Index must be a number", "red")


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


def cmd_flip(console, args):
    """Flips a coin.
    FORMAT: flip"""
    result = "heads" if randint(0, 1) == 0 else "tails"
    console.output(f"You got {result}!", "blue")


def cmd_unit(console, args):
    """Converts between various units.
    FORMAT: unit [count] [starting_unit] [ending_unit]"""
    try:
        ureg = UnitRegistry()
        val = 1
        x = 0
        if len(args) == 3:
            val = float(args[0])
            x = 1
        # handle revolutions (its useful for physics hush)
        if args[1] in NAMES_FOR_REVOLUTIONS:
            args[1] = "radian"
            val *= 2*3.14159
        if args[2] in NAMES_FOR_REVOLUTIONS:
            args[2] = "radian"
            val /= 2*3.14159
        # noinspection PyCallingNonCallable
        unit = val * ureg(args[0 + x])
        # noinspection PyCallingNonCallable
        x = round(unit.to(ureg(args[1 + x])), 2)

        console.output(f"Converted {val} {args[1]} to {x}.", "aqua")
    except IndexError:
        console.output("missing arguments")


def cmd_screenshot(console, args):
    """Takes a screenshot of the current screen.
    FORMAT: screenshot"""
    reappear_later = False
    if console.isVisible():
        console.disappear()
        reappear_later = True
    ss = ImageGrab.grab()
    ss.save(f"{screenshots_path}screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
    if reappear_later:
        console.reappear()
    console.output("Screenshot saved!", "green")


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
        console.output(f"{curr_1_val} {curr_1} is equal to {curr_1_val * rate} {curr_2}", "blue")
    except IndexError:
        console.output("invalid syntax", "red")


def cmd_copy(console, args):
    """Copies last console output to clipboard.
    Format: copy"""
    text = console.output_area.text()
    copy(text.strip())
    console.output("copied to clipboard", "green")


class Stopwatch:
    def __init__(self, running=True):
        self.start = time.time()
        self.most_recent_start = self.start
        self.running = running
        self._elapsed = 0

    def pause(self):
        if self.running:
            self._elapsed += time.time() - self.most_recent_start
            self.running = False
        else:
            self.most_recent_start = time.time()
            self.running = True

    def __str__(self):
        return str(self.elapsed())

    def elapsed(self):
        if self.running:
            return round(self._elapsed + time.time() - self.most_recent_start, 2)
        else:
            return round(self._elapsed, 2)


def cmd_stopwatch(console, args):
    """Modifies stopwatches.
    FORMAT: stopwatch [list/start/pause/end/name]"""
    try:
        cmd = args[0]
        args = args[1:]
        match cmd:
            case "list": # lists all running stopwatches
                console.output(', '.join(console.stopwatches), "aqua")
            case "start": # creates new stopwatch starting at time of creation
                paused = False
                if "-p" in args:
                    paused = True
                    args.remove("-p")
                name = args[0]
                console.stopwatches[name] = Stopwatch(running=not paused)
                console.output(f"created stopwatch {name}", "green")
            case "pause" | "resume": # pauses or resumes a stopwatch
                name = args[0]
                sw = console.stopwatches.get(name, None)
                if sw:
                    sw.pause()
                    console.output(f"paused stopwatch {name}", "green")
                else:
                    console.output("No such stopwatch found", "red")
            case "end": # prints out a stopwatches information and deletes it
                name = args[0]
                sw = console.stopwatches.get(name, None)
                if sw:
                    time_elapsed = sw.elapsed()
                    del console.stopwatches[name]
                    console.output(f"stopped stopwatch {name} at {sw.elapsed()}s", "green")
                else:
                    console.output("No such stopwatch found", "red")
            case _: # search for specific stopwatch and give information about it
                name = cmd
                sw = console.stopwatches.get(name, None)
                if sw:
                    console.output(f"Stopwatch {name} is at {sw.elapsed()}s and is currently{'' if sw.running else ' not'} running.", "aqua")
                else:
                    console.output("no such stopwatch found", "red")
    except IndexError:
        console.output("invalid syntax", "red")\


# TODO - make work
# def cmd_define(console, args):
#     """Define a word. BROKEN!!!!!!
#     FORMAT: define [word] (-s)ynonyms (-a)ntonyms"""
#     antonyms = False
#     synonyms = False
#     if "-a" in args:
#         antonyms = True
#         args.remove("-a")
#     if "-s" in args:
#         synonyms = True
#         args.remove("-s")
#     term = " ".join(args)
#     text = dictionary.meaning(term)
#     if synonyms:
#         text += "\n" + dictionary.synonym(term)
#     if antonyms:
#         text += "\n" + dictionary.antonym(term)
    #console.output(text, "aqua")