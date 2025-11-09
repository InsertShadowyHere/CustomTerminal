"""Commands used with automation
This module contains system utility functions for automation purposes.
Functions:
sys
"""
from time import sleep
from pyperclip import paste

time_flags = {"-d": 60*60*24*1000, "-h": 60*60*1000, "-m": 60*1000, "-s": 1000, "-ms": 1}


# TODO - make this
def cmd_sys(console, args):
    """Allows editing of system variables like
    volume, brightness, wifi, etc.
    Primarily used for automation, I guess
    """
    pass


# TODO - make this
def cmd_open_url(console, args):
    pass


# TODO - make this
def cmd_open_app(console, args):
    pass


# TODO - make this
def cmd_open_file(console, args):
    """Opens """
    pass


def cmd_run(console, args):
    """Runs a script or application with its path.
    FORMAT: run <path>"""
    pass


def cmd_sleep(console, args):
    """Makes the console sleep for the given time.         ONLY USE FOR AUTOMATION
    FORMAT: schedule[task] (-d)ays (-h)ours (-m)inutes (-s)econds -(ms)illiseconds"""
    time_til = 0 # in seconds
    for flag in time_flags:
        if flag in args:
            ind = args.index(flag)
            time_til += time_flags[flag] * float(args[ind+1])
            del args[ind:ind+2]
    sleep(time_til/1000)
    console.output(f"Slept for {round(time_til/1000, 2)} seconds", "green")

def cmd_hide(console, args):
    console.disappear()
    console.output("Console hidden!", "green")

def cmd_show(console, args):
    console.reappear()
    console.output("Console shown!", "green")

def cmd_echo(console, args):
    console.output(' '.join(args), "aqua")

def cmd_pasterun(console, args):
    """Runs most previous copy in the console.
    Format: pasterun"""
    console.execute(paste)
