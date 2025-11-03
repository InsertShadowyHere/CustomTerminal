import subprocess
import sys
import threading

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
import pyautogui
import webbrowser
import keyboard
from PySide6.QtCore import QTimer
import pickle
import mouse


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.commands = ["link", "macro", "google", "where"]
        self.links = {}
        self.macros = {}

        self.outputted = False

        self.past_events = []
        self.log = ""

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setWindowOpacity(0.8)

        self.setWindowTitle("Terminal")

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))  # 127/255 = ~50%
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

        self.activateWindow()
        self.raise_()
        self.line_edit.setFocus()

    def restore_focus(self):
        self.show()  # show the window if hidden
        self.raise_()  # bring to top
        self.activateWindow()  # request focus
        self.line_edit.setFocus()  # put cursor in input

    def execute(self, cmd):
        if not cmd:
            return
        cmd = cmd.split()

        self.outputted = False

        if cmd[0] in self.commands:
            if cmd[0] == "google":
                query = ' '.join(cmd[1:])
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.output("success", "green")


            elif cmd[0] == "where":
                self.output(str(pyautogui.position()), "green")


            elif cmd[0] == "link":
                self.output("statement has no effect", "yellow")
                self.link(cmd[1:])


            elif cmd[0] == "macro":
                self.output("statement has no effect", "yellow")
                self.macro(cmd[1:])


        elif cmd[0] in self.links.keys():
            link = self.links[cmd[0]]
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
            keyboard_events, mouse_events = self.macros[cmd[0]]
            play_macro(keyboard_events, mouse_events)
            self.setFocus()
            self.show()
            self.output("macro completed", "green")

        if not self.outputted:
            self.output("command not found", "red")
        QTimer.singleShot(100, self.restore_focus)


    def open_file_in_finder(self, link):
        try:
            subprocess.run(["open", "-R", link], check=True)
            self.output(f"opening file {link}", "green")
        except subprocess.CalledProcessError as e:
            self.output(f"couldn't open file: {e}", "red")

    # TODO - establish more types of links
    def link(self, cmd):
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
                stuff = [f"{key}: {value}" for key, value in self.links.items()]
                self.output("\n".join(stuff), "blue")


            # Remove a link
            elif cmd[0] == "remove" or cmd[0] == "delete":
                if cmd[1] in self.links:
                    del self.links[cmd[1]]
                self.output(f"deleted {cmd[1]}", "green")


        except:
            self.output("invalid syntax", "red")


    def open_file(self, url):
        pass


    def macro(self, cmd):
        try:
            if cmd[0] == "record":
                name = cmd[1]
                mouse_events = []

                self.hide()
                self.clearFocus()

                keyboard.start_recording()
                mouse.hook(mouse_events.append)
                keyboard.wait('`')
                keyboard_events = keyboard.stop_recording()
                mouse.unhook(mouse_events.append)

                self.show()

                self.macros[name] = keyboard_events, mouse_events

            elif cmd[0] == "list":
                stuff = [name for name in self.macros]
                print('hi')
                self.output("\n".join(stuff), "blue")

            elif cmd[0] == "remove" or cmd[0] == "delete":
                if cmd[1] in self.macros:
                    del self.macros[cmd[1]]
                self.output(f"deleted {cmd[1]}", "green")

            else:
                self.output("invalid syntax", "red")

        except IndexError:
            self.output(f"no options specified", "red")
        except:
            self.output("something went wrong", "red")


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


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.run_terminal_line()
        if event.key() == Qt.Key.Key_Escape:
            self.close()


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

    window = Terminal()
    window.show()

    sys.exit(app.exec())
