"""This file contains the """
import importlib
import pkgutil
import subprocess
import sys
import threading
import webbrowser

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
import keyboard
from PySide6.QtCore import QTimer
import mouse

from commands import __path__ as command_path


class Console(QMainWindow):
    def __init__(self):
        super().__init__()

        # Terminal version and command dictionary
        self.version = 0.1
        self.commands = {"link": self.cmd_link,
                         "macro": self.cmd_macro,
                         "meta": self.cmd_meta,
                         "help": self.cmd_help,}
        self.load_commands()
        self.links = {}
        self.macros = {}

        self.todo = []

        self.outputted = False

        self.history_pos = 0
        self.past_events = []
        self.log = ""

        # PySide6 window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setWindowOpacity(0.8)

        self.setWindowTitle("Terminal")

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 127))  # 127/255 = ~50%
        self.setPalette(palette)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.addStretch()

        self.past_events_label = QLabel()
        self.past_events_label.setStyleSheet("color: white; font-size: 18px")
        self.layout.addWidget(self.past_events_label)

        self.output_label = QLabel()
        self.output_label.setStyleSheet("color: white; font-size: 18px")
        self.layout.addWidget(self.output_label)

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("""QLineEdit {
               color: white;
               background-color: rgba(0, 0, 0, 255);
               border: 0px solid #666;
               font-size: 18px;
           }""")
        self.layout.addWidget(self.line_edit)

        self.setCentralWidget(self.container)

        self.restore_focus()

    def load_commands(self):
        """Reads all files from commands/ and loads all cmd_ functions."""
        for _, module_name, _ in pkgutil.iter_modules(command_path):
            module = importlib.import_module(f"commands.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and attr_name.startswith('cmd_'):
                    cmd_name = attr_name[4:]  # Remove cmd_
                    self.commands[cmd_name] = attr
                    print(f"Loaded command: {cmd_name} from {module_name}")

    def restore_focus(self):
        """
        Brings terminal window back to top and puts it in focus.
        """
        self.show()  # show the window
        self.raise_()  # bring to top
        self.activateWindow()  # request focus
        self.line_edit.setFocus()  # put cursor in input

    def execute(self, cmd):
        """
        Determines command handling and routing to subfunctions.
        :rtype: None
        """
        if not cmd:
            return
        cmd = cmd.split()
        args = cmd[1:]
        cmd = cmd[0]

        self.outputted = False

        if cmd in self.commands:
            func = self.commands[cmd]
            func(self, args)

        elif cmd in self.links.keys():
            link = self.links[cmd]
            if link[1] == "url":
                webbrowser.open(link[0])
                self.output(f"opening link {link[0]}", "green")
            if link[1] == "file":
                # TODO write some code to open file in os's file viewer`
                self.open_file_in_finder(link[0])

        elif cmd[0] in self.macros:
            print('macroing!')
            self.clearFocus()
            self.hide()
            keyboard_events, mouse_events = self.macros[cmd]
            play_macro(keyboard_events, mouse_events)
            self.setFocus()
            self.show()
            self.output("macro completed", "green")

        if not self.outputted:
            self.output("command not found", "red")
        QTimer.singleShot(100, self.restore_focus)

    # TODO - make this
    def open_file_in_finder(self, link):
        try:
            subprocess.run(["open", "-R", link], check=True)
            self.output(f"opening file {link}", "green")
        except subprocess.CalledProcessError as e:
            self.output(f"couldn't open file: {e}", "red")

    # TODO - make this
    def open_file(self, url):
        pass

    # TODO - establish more types of links
    def cmd_link(self, cmd):
        try:
            if cmd[0] == "add":
                user_cmd = cmd[cmd.index("-c") + 1]
                link = cmd[cmd.index("-l") + 1]
                if user_cmd in self.commands:
                    self.output("command already exists", "red")
                    return
                link_type = "url"
                if '-t' in cmd:
                    link_type = cmd[cmd.index("-t") + 1]

                if link_type == "url":
                    if "www" not in link:
                        link = "www." + link
                    if "https" not in link:
                        link = "https://" + link

                    self.links[user_cmd] = (link, "url")
                    self.output(f"link {user_cmd} to {link} added", "green")
                elif link_type == "file":
                    #TODO - test file validity
                    self.links[user_cmd] = (link, "file")
                    self.output(f"link {user_cmd} to {link} added", "green")


            # Displays all available links
            elif cmd[0] == "list":
                stuff = [f"{key}: {value[0]}" for key, value in self.links.items()]
                self.output("\n".join(stuff), "aqua")


            # Remove a link
            elif cmd[0] == "remove" or cmd[0] == "delete":
                if cmd[1] in self.links:
                    del self.links[cmd[1]]
                self.output(f"deleted {cmd[1]}", "green")


        except:
            self.output("invalid syntax", "red")

    # TODO - make this work
    def cmd_macro(self, cmd):
        try:
            if cmd[0] == "record":
                name = cmd[1]
                mouse_events = []

                self.hide()
                self.clearFocus()

                keyboard.start_recording()
                mouse.hook(mouse_events.append)
                keyboard.wait('F9')
                keyboard_events = keyboard.stop_recording()
                mouse.unhook(mouse_events.append)
                self.show()

                self.macros[name] = keyboard_events, mouse_events

            elif cmd[0] == "list":
                stuff = [name for name in self.macros]
                print('hi')
                self.output("\n".join(stuff), "aqua")

            elif cmd[0] == "remove" or cmd[0] == "delete":
                if cmd[1] in self.macros:
                    del self.macros[cmd[1]]
                self.output(f"deleted {cmd[1]}", "green")

            else:
                self.output("invalid syntax", "red")

        except IndexError:
            self.output(f"incomplete syntax", "red")
        except:
            self.output("something went wrong", "red")

    def cmd_meta(self, cmd):
        try:
            match cmd[0]:
                # change window opacity
                case "opacity":
                    self.setWindowOpacity(float(cmd[1]))
                # change background color
                case "bg":
                    palette = self.palette()
                    palette.setColor(QPalette.Window, QColor(int(cmd[1]), int(cmd[2]), int(cmd[3])))
                    self.setPalette(palette)
                # change text color
                case "text":
                    if len(cmd) == 1:
                        self.line_edit.setStyleSheet(f"""QLineEdit {{
                                                   color: white;
                                                   background-color: rgba(0, 0, 0, 255);
                                                   border: 0px solid #666;
                                                   font-size: 18px;
                                            }}""")
                    else:
                        self.line_edit.setStyleSheet(f"""QLineEdit {{
                               color: rgb({int(cmd[1])}, {int(cmd[2])}, {int(cmd[3])});
                               background-color: rgba(0, 0, 0, 255);
                               border: 0px solid #666;
                               font-size: 18px;
                        }}""")
                # except for all other cases
                case _:
                    self.output("invalid syntax", "red")
                    return
            self.output("success", "green")
        except IndexError:
            self.output("incomplete syntax", "red")
        except:
            self.output("you messed something up", "red")

    def cmd_help(self, cmd):
        if cmd:
            pass
        else:
            text = "\n".join(self.commands)
            self.output(f"Raphael's Console v{self.version} | Built-in commands:\n{text}", "aqua")

    # TODO - make this
    def cmd_open_url(self, cmd):
        pass

    # TODO - make this
    def cmd_open_file(self, cmd):
        pass

    # TODO - make this
    def cmd_open_app(self, cmd):
        pass

    def output(self, text, color):
        self.outputted = True
        self.output_label.setText(text)
        self.output_label.setStyleSheet(f"color: {color}; font-size: 18px")

    def run_terminal_line(self):
        command = self.line_edit.text()
        self.execute(command)
        self.past_events.append(command)
        self.past_events_label.setText('\n'.join(self.past_events))
        self.line_edit.setText("")
        self.history_pos = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.run_terminal_line()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Up:
            # add one to history pos and then clamp
            self.history_pos += 1
            if self.history_pos > len(self.past_events):
                self.history_pos = len(self.past_events)

            if self.history_pos == 0:
                self.line_edit.clear()
            else:
                self.line_edit.setText(self.past_events[-self.history_pos])
        elif event.key() == Qt.Key.Key_Down:
            self.history_pos -= 1
            if self.history_pos < 0:
                self.history_pos = 0

            if self.history_pos == 0:
                self.line_edit.clear()
            else:
                self.line_edit.setText(self.past_events[-self.history_pos])


def play_macro(k_events, m_events):
    def play_mouse():
        mouse.play(m_events)

    def play_keyboard():
        keyboard.play(k_events)

    # Run both in parallel so timing feels natural
    t1 = threading.Thread(target=play_mouse)
    t2 = threading.Thread(target=play_keyboard)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Console()
    window.show()

    sys.exit(app.exec())
