import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Qt
import pyautogui
import webbrowser
import keyboard
from PySide6.QtCore import QTimer


class Terminal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.past_events = []

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
        self.past_events_label = QLabel("hola!")
        self.past_events_label.setStyleSheet("color: white; font-size: 18px")

        self.layout.addWidget(self.past_events_label)
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
        if cmd[0] == "google":
            query = ' '.join(cmd[1:])
            webbrowser.open(f"https://www.google.com/search?q={query}")

        if cmd[0] == "where":
            print(pyautogui.position())

        QTimer.singleShot(100, self.restore_focus)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Terminal()
    window.show()

    sys.exit(app.exec())
