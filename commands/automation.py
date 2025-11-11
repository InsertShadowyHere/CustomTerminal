"""Automation commands
This module contains automation functions.
Functions:
link
schedule
macro
stopwatch
remind

"""
time_flags = {"-d": 60 * 60 * 24, "-h": 60 * 60, "-m": 60, "-s": 1}
OPEN_AI_KEY = "sk-P3x8J8Wse2Zgz4RJ4F846I33dH4Pq7OVVLI04Rf72w9tItP3"

def get_links():
    with open("resources/links", "r") as f:
        file_data = f.readlines()
        links = {}
        current_name = None
        for n, line in enumerate(file_data):
            if line[:7] == "LINK - ":
                current_name = line[7:].strip()
                links[current_name] = []
            elif current_name:
                links[current_name].append(line)
    return links

def write_links(links):
    with open("resources/links", "w") as f:
        for name, link in links.items():
            f.write(f"LINK - {name}\n")
            for line in link:
                f.write(line)


def cmd_link(console, args):
    """Modifies the link system, which is ConsoleC's way of creating custom commands.
    Each link contains its own command information, and can contain an arbitrary number of
    individual commands.
    FORMAT: link [add/remove/edit/list]"""
    if console.links == {}:
        console.links = get_links()
    try:
        match args[0]:
            case "add" | "a":
                name = args[1]
                if name in console.links:
                    console.output("that link already exists!", "red")
                    return
                console.mode = f"link _adding {name}"
                console.links[name] = []
                console.output("creating link... type the first line!", "green")
            case "remove" | "delete" | "del" | "rem" | "r":
                if args[1] in console.links:
                    del console.links[args[1]]
                    write_links(console.links)
                    console.output(f"{args[1]} has been deleted", "green")
                else:
                    console.output(f"{args[1]} does not exist", "red")
            case "edit" | "e":
                name = args[1]
                if name in console.links:
                    console.mode = f"link _editing {name} 0"
                    console.line_edit.setText(console.links[name][0])
                    console.output("editing link... type the first line!", "red")
                else:
                    console.output(f"{args[1]} does not exist", "red")
            case "list" | "l":
                links = get_links()
                console.output("\n".join(links), "green")
            case "_adding":
                name = args[1]
                if args[2] == "done":
                    console.mode = None
                    if not console.links[name]:
                        console.output("you finished too early, link wasn't made. take your time bro", "red")
                        del console.links[name]
                        return
                    with open("resources/links", "a") as f:
                        f.write(f"LINK - {name}\n" + "".join([i + "\n" for i in console.links[name]]))
                    console.output(f"link {name} created!", "green")
                    return
                console.links[name].append(' '.join(args[2:]))
                console.output("line added!", "green")
            case "_editing":
                pos = int(args[2])
                name = args[1]
                console.links[name][pos] = " ".join(args[3:]) + "\n"
                pos += 1
                if pos == len(console.links[name]):
                    console.mode = None
                    write_links(console.links)
                    console.output("link fully edited!", "green")
                    return
                console.line_edit.setText(console.links[name][pos].strip())
                console.mode = f"link _editing {name} {pos}"
                console.output("line edited!", "green")

            case _:
                link = console.links.get(args[0], None)
                if link:
                    console.output("".join(link), "green")
                else:
                    console.output("no such link found", "red")
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
    if time_til != 0:
        console.schedule(reminder, time_til, "note")
    else:
        console.open_note(reminder)
    console.output("reminder set!", "green")


def cmd_schedule(console, args):
    """Schedules a link. WARNING: these do not persist through restart right now
    FORMAT: schedule [link] (-d)ays (-h)ours (-m)inutes (-s)econds"""

    time_til = 0  # in seconds

    for flag in time_flags:
        if flag in args:
            ind = args.index(flag)
            time_til += time_flags[flag] * float(args[ind + 1])
            del args[ind:ind + 2]

    if time_til != 0:
        console.schedule(args[0], time_til, "link")
    else:
        console.run_link(args[0])
    console.output("reminder set!", "green")