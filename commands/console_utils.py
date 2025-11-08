"""Console-related utility commands


"""

from pyperclip import copy


def cmd_meta(console, args):
    """Edits various console settings. Current settings include opacity (opacity),
    background color (bg), and text color (text).
    Format: meta [setting] [value]
    """
    try:
        match args[0]:
            # change window opacity
            case "opacity":
                if len(args) == 1:
                    console.setWindowOpacity(console.defaultOpacity)
                else:
                    console.setWindowOpacity(float(args[1]))
            # change background color
            case "bg":
                console.changeBackground(map(float, args[1:]))
            # change text color
            case "text":
                if len(args) == 1:
                    console.line_edit.setStyleSheet(f"""QLineEdit {{
                                               color: white;
                                               background-color: rgba(0, 0, 0, 255);
                                               border: 0px solid #666;
                                               font-size: 18px;
                                        }}""")
                else:
                    console.line_edit.setStyleSheet(f"""QLineEdit {{
                           color: rgb({int(args[1])}, {int(args[2])}, {int(args[3])});
                           background-color: rgba(0, 0, 0, 255);
                           border: 0px solid #666;
                           font-size: 18px;
                    }}""")
            # except for all other cases
            case _:
                console.output("invalid syntax", "red")
                return
        console.output("success", "green")
    except IndexError:
        console.output("incomplete syntax", "red")
    except Exception as e:
        console.log(e)
        console.output("something went wrong", "red")


def cmd_help(console, args):
    """Displays a list of available commands or detailed info about a specific command.
    Format: help [command_name] to return individual command info, or help to get all commands."""
    if args:
        cmd_name = args[0]
        if cmd_name in console.commands:
            func = console.commands[cmd_name]
            console.output(f"{cmd_name}:\n{func.__doc__}", "aqua")
        else:
            console.output("command not found", "red")
    else:
        text = []
        for source in console.command_sources:
            text.append(f"----{source} - {console.command_sources[source][0]}:----")
            for i in range(0, len(console.command_sources[source][1:]), 4):
                text.append('    '.join(console.command_sources[source][1:][i:i + 4]))
        text = "\n".join(text)
        console.output(f"Raphael's Console v{console.version} | Built-in Commands\n{text}", "aqua")


def cmd_about(console, args):
    """Displays information about the console.
    Format: about"""
    console.output(f"ConsoleC version {console.version}; Developed by InsertShadowyHere", "aqua")


def cmd_copy(console, args):
    """Copies last console output to clipboard.
    Format: copy"""
    text = console.output_area.text()
    copy(text.strip())
    console.output("copied to clipboard", "green")


def cmd_devhelp(console, args):
    """Returns information to help new developers (prints devhelp.txt contents lol)
    Format: devhelp [page]"""
    try:
        page = 0
        if args:
            page = int(args[0]) - 1
        with open("resources/devhelp.txt", "r") as f:
            info = f.read().split("PAGE")
            text = f"""Are you looking to develop with ConsoleC? Here are the dev notes!\nUse devhelp [page] to go to the next page. There are {len(info)} pages.\n"""
            info = text + info[page].strip()
        console.output(info, "aqua")
    except FileNotFoundError:
        console.output("the devhelp file was deleted! :(", "red")


def cmd_clear(console, args):
    """Clears the console.
    Format: clear"""
    console.history = []
    console.output("console cleared", "green")


def cmd_mode(console, args):
    """Sets the console to a mode, treating it as if the command was prefixed with the mode.
    For example, mode math means that the next time 5+5 is written, it returns 10 and not an error.
    This command can save subsettings too, so mode link add works fine. Use exit to exit the mode.
    FORMAT: mode [command]"""
    try:
        console.mode = ' '.join(args) + " "
        console.output(f"set mode to {' '.join(args)}", "green")
    except IndexError:
        console.output("invalid parameters", "red")
    except Exception as e:
        console.log(e)
        console.output("something went wrong", "red")


def cmd_quit(console, args):
    """Quits the console.
    Format: quit"""
    console.close()
