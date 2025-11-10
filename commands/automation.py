"""Automation commands
This module contains automation functions.
Functions:
link
schedule
macro
stopwatch
remind

"""
from unittest import case

# import keyboard
# import mouse
time_flags = {"-d": 60 * 60 * 24, "-h": 60 * 60, "-m": 60, "-s": 1}

# TODO - establish more types of links
def cmd_link(console, args):
    """Modifies the link system, which is ConsoleC's way of creating custom commands.
    Each link contains its own command information, and can contain an arbitrary number of
    individual commands.
    FORMAT: link [add/remove/edit/list]"""

    def get_link_list():
        with open("resource/links", "r") as f:
            file_data = f.readlines()
            link_list = {}
            link_inds = []
            for n, line in enumerate(file_data):
                if line[:8] == "LINK - ":
                    link_inds.append([n, line])

    try:
        match args[0]:
            case "add" | "a":
                name = args[1]
                with open("resources/links", "a") as f:
                    pass
            case "remove" | "delete" | "del" | "rem" | "r":
                pass
            case "edit" | "e":
                pass
            case "list" | "l":
                if len(args) == 1:
                    with open("resources/links", "r") as f:
                        pass

                pass
    except IndexError:
        console.output("invalid syntax", "red")

# TODO - make this work
# def cmd_macro(console, args):
#         try:
#             if args[0] == "record":
#                 name = args[1]
#                 mouse_events = []
#
#                 console.hide()
#                 console.clearFocus()
#
#                 keyboard.start_recording()
#                 mouse.hook(mouse_events.append)
#                 keyboard.wait('F9')
#                 keyboard_events = keyboard.stop_recording()
#                 mouse.unhook(mouse_events.append)
#                 console.show()
#
#                 console.macros[name] = keyboard_events, mouse_events
#
#             elif args[0] == "list":
#                 stuff = [name for name in console.macros]
#                 print('hi')
#                 console.output("\n".join(stuff), "aqua")
#
#             elif args[0] == "remove" or args[0] == "delete":
#                 if args[1] in console.macros:
#                     del console.macros[args[1]]
#                 console.output(f"deleted {args[1]}", "green")
#
#             else:
#                 console.output("invalid syntax", "red")
#
#         except IndexError:
#             console.output(f"incomplete syntax", "red")
#         except:
#             console.output("something went wrong", "red")


def cmd_remind(console, args):
    """Schedules a reminder popup. WARNING: these do not persist through restart right now
    FORMAT: schedule [task] (-d)ays (-h)ours (-m)inutes (-s)econds"""

    time_til = 0  # in seconds

    for flag in time_flags:
        if flag in args:
            ind = args.index(flag)
            time_til += time_flags[flag] * float(args[ind + 1])
            del args[ind:ind + 2]

    reminder = " ".join(args)
    console.schedule(reminder, time_til, "note")
    console.output("reminder set!", "green")
