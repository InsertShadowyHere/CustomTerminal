import keyboard, sys, threading

from PySide6.QtCore import QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from console import Console

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = Console()
    window.hide()

    # --- System Tray ---
    tray = QSystemTrayIcon(QIcon("icon.png"), parent=app)
    tray.setToolTip("Quick Console")

    menu = QMenu()
    toggle_action = QAction("Toggle Console", app)
    quit_action = QAction("Quit", app)
    menu.addAction(toggle_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()

    toggle_action.triggered.connect(lambda: toggle(window))
    quit_action.triggered.connect(app.quit)

    # apparently you use this as a dict to get around pythons lambda assignment rules
    toggle_requested = {"state": False}

    def toggle_window():
        toggle_requested["state"] = True

    threading.Thread(
        target=lambda: (keyboard.add_hotkey("`", toggle_window, suppress=True), keyboard.wait()),
        daemon=True
    ).start()

    # run in qt thread to check for tilde
    def check_toggle():
        if toggle_requested["state"]:
            toggle_requested["state"] = False
            toggle(window)


    timer = QTimer()
    timer.timeout.connect(check_toggle)
    timer.start(100)

    sys.exit(app.exec())

def toggle(window):
    if window.isVisible():
        window.hide()
    else:
        window.show()
        window.raise_()
        window.activateWindow()


if __name__ == "__main__":
    main()