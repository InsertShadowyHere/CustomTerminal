"""Automation commands
This module contains automation functions.
Functions:
link
schedule
macro
stopwatch
remind

"""
import keyboard
import mouse


# TODO - establish more types of links
def cmd_link(console, args):
    try:
        if args[0] == "add":
            user_cmd = args[args.index("-c") + 1]
            link = args[args.index("-l") + 1]
            if user_cmd in console.commands:
                console.output("command already exists", "red")
                return
            link_type = "url"
            if '-t' in args:
                link_type = args[args.index("-t") + 1]

            if link_type == "url":
                if "www" not in link:
                    link = "www." + link
                if "https" not in link:
                    link = "https://" + link

                console.links[user_cmd] = (link, "url")
                console.output(f"link {user_cmd} to {link} added", "green")
            elif link_type == "file":
                # TODO - test file validity
                console.links[user_cmd] = (link, "file")
                console.output(f"link {user_cmd} to {link} added", "green")


        # Displays all available links
        elif args[0] == "list":
            stuff = [f"{key}: {value[0]}" for key, value in console.links.items()]
            console.output("\n".join(stuff), "aqua")


        # Remove a link
        elif args[0] == "remove" or args[0] == "delete":
            if args[1] in console.links:
                del console.links[args[1]]
            console.output(f"deleted {args[1]}", "green")

    except:
        console.output("invalid syntax", "red")

# TODO - make this work
def cmd_macro(console, args):
        try:
            if args[0] == "record":
                name = args[1]
                mouse_events = []

                console.hide()
                console.clearFocus()

                keyboard.start_recording()
                mouse.hook(mouse_events.append)
                keyboard.wait('F9')
                keyboard_events = keyboard.stop_recording()
                mouse.unhook(mouse_events.append)
                console.show()

                console.macros[name] = keyboard_events, mouse_events

            elif args[0] == "list":
                stuff = [name for name in console.macros]
                print('hi')
                console.output("\n".join(stuff), "aqua")

            elif args[0] == "remove" or args[0] == "delete":
                if args[1] in console.macros:
                    del console.macros[args[1]]
                console.output(f"deleted {args[1]}", "green")

            else:
                console.output("invalid syntax", "red")

        except IndexError:
            console.output(f"incomplete syntax", "red")
        except:
            console.output("something went wrong", "red")