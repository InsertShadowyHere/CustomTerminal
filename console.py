"""Console code"""
import importlib
import pkgutil
import sys
import traceback
import webbrowser
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer

import commands.automation
from commands import __path__ as command_path
from time import sleep

class Console(QMainWindow):
    def __init__(self):
        super().__init__()

        # Terminal version and command dictionary
        self.version = 0.1
        self.commands = {}
        self.command_sources = {}
        self.load_commands()
        if 'link' in self.commands:
            self.links = commands.automation.get_links()
        else:
            self.links = {}
        self.macros = {}
        self.completer_words = None
        self.mode = None
        self.stopwatches = {}

        # self.load_completer()
        # print(self.completer_words)

        self.log_num = 0

        self.outputted = False

        self.history_pos = 0
        self.history = []
        self.output_log = ""

        # PySide6 window setup
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.showFullScreen()
        self.defaultOpacity = 0.85
        self.setWindowOpacity(self.defaultOpacity)

        self.setWindowTitle("Terminal")

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 127))
        self.setPalette(palette)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.addStretch()

        self.past_events_label = QLabel()
        self.past_events_label.setStyleSheet("color: white; font-size: 18px")
        self.layout.addWidget(self.past_events_label)

        self.output_area = QLabel()
        self.output_area.setWordWrap(True)
        self.output_area.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.output_area.setStyleSheet("color: white; font-size: 18px; background-color: black; border: 0px;")
        # self.output_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.layout.addWidget(self.output_area)

        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("""QLineEdit {
               color: white;
               background-color: rgba(0, 0, 0, 255);
               border: 0px solid #666;
               font-size: 18px;
           }""")
        # self.load_completer()
        # choosing not to use the completer cus its really ugly
        # self.completer = QCompleter(self.completer_words)
        # self.line_edit.setCompleter(self.completer)
        self.layout.addWidget(self.line_edit)

        self.setCentralWidget(self.container)

        self.reappear()

    def load_commands(self):
        """Reads all files from commands/ and loads all cmd_ functions."""
        self.commands = {}
        self.command_sources = {}
        for _, module_name, _ in pkgutil.iter_modules(command_path):
            full_name = f"commands.{module_name}"
            # if module is already loaded, refresh it to allow for new updates to get sent in
            if full_name in sys.modules:
                module = importlib.reload(sys.modules[full_name])
            else:
                module = importlib.import_module(full_name)

            self.command_sources[module_name] = [module.__doc__.strip().splitlines()[0]]

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and attr_name.startswith('cmd_'):
                    cmd_name = attr_name[4:]  # remove cmd_
                    self.commands[cmd_name] = logger(attr)  # make sure the command is wrapped in a logger
                    self.command_sources[module_name].append(cmd_name)
                    print(f"Loaded command: {cmd_name} from {module_name}")

    # def load_completer(self):
    #     self.completer_words = list(self.commands.keys()) + list(self.links.keys()) + list(self.macros.keys())

    def disappear(self):
        """Hides the console (wrapper for .hide(), only used as companion to reappear()
        because it's easy to remember lol"""
        self.hide()

    def reappear(self):
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
        next_cmd = None
        if "&" in args:
            next_cmd = ' '.join(args[args.index("&") + 1:])
            args = args[:args.index("&")]

        cmd = cmd[0]

        self.outputted = False

        if cmd in self.commands:
            func = self.commands[cmd]
            func(self, args)

        elif x := self.links.get(cmd, None):
            for i in map(str.strip, x):
                self.execute(i)
            self.output(f"link {cmd} executed!", "green")

        elif cmd in self.macros:
            self.clearFocus()
            self.hide()
            keyboard_events, mouse_events = self.macros[cmd]
            # play_macro(keyboard_events, mouse_events)
            self.setFocus()
            self.show()
            self.output("macro completed", "green")

        if not self.outputted:
            self.output("command not found", "red")

        if next_cmd:
            self.execute(next_cmd)

    def changeBackground(self, color):
        """Changes background color."""
        r, g, b, a = color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(int(r), int(g), int(b)))
        self.setPalette(palette)

    def output(self, text, color):
        """Sets the console output text."""
        self.outputted = True
        self.output_area.setText(text)
        self.output_area.setStyleSheet(f"color: {color}; font-size: 18px; background-color: black; border: 0px;")

    def log(self, tb):
        """Saves error logs in logs.txt"""
        self.log_num += 1
        with open(f"resources/log", "a") as f:
            f.write(f"[{datetime.now()}] {tb}")
        self.output("something went wrong (check the log!)", "red")

    def schedule(self, info, time, sch_type):
        if sch_type == "note":
            QTimer.singleShot(time * 1000, lambda: self.open_note(info))
        elif sch_type == "link":
            QTimer.singleShot(time * 1000, lambda: self.run_link(info))

    def run_link(self, link):
        if x := self.links.get(link, None):
            for i in map(str.strip, x):
                self.execute(i)
            self.output(f"link {link} executed!", "green")
        else:
            self.output(f"link {link} not found!", "red")

    def open_note(self, info):
        popup = QMessageBox(self)
        popup.setWindowIcon(QIcon("resources/icon.png"))
        popup.setWindowTitle("Reminder")
        popup.setText(info)
        popup.show()

    def run_console_line(self):
        """Handles processing of entering a line"""
        command = self.line_edit.text()
        self.line_edit.clear()
        if self.mode:
            if command == "exit" and "link _adding" not in self.mode:
                self.mode = None
                self.output(f"exiting mode {str(self.mode)}", "green")
            else:
                self.execute(f"{self.mode} {command}")
        else:
            self.execute(command)
        if len(self.history) > 19:
            self.history.pop(0)
        self.history.append(command)
        self.past_events_label.setText('\n'.join(self.history))
        self.history_pos = 0

    def keyPressEvent(self, event):
        if self.isVisible():
            if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_QuoteLeft:
                if self.line_edit.text() == "":
                    return
                self.run_console_line()
            elif event.key() == Qt.Key.Key_Escape:
                self.setVisible(not self.isVisible())
            elif event.key() == Qt.Key.Key_Up:
                # add one to history pos and then clamp
                self.history_pos = min(self.history_pos + 1, len(self.history))
                if self.history_pos == 0:
                    self.line_edit.clear()
                else:
                    self.line_edit.setText(self.history[-self.history_pos])
            elif event.key() == Qt.Key.Key_Down:
                self.history_pos = max(self.history_pos - 1, 0)

                if self.history_pos == 0:
                    self.line_edit.clear()
                else:
                    self.line_edit.setText(self.history[-self.history_pos])
        elif event.key() == Qt.Key.Key_QuoteLeft:
            self.setVisible(not self.isVisible())

def logger(cmd):
    """Returns logger-decorated function."""

    def wrapper(console, args):
        try:
            cmd(console, args)
        except Exception as e:
            full_tb = traceback.format_exc()
            console.log(full_tb)

    wrapper.__name__ = cmd.__name__
    wrapper.__doc__ = cmd.__doc__
    return wrapper

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Console()
    window.show()

    sys.exit(app.exec())
