import keyboard
import pyautogui as pag
import subprocess
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
import sys
import terminal



listening = False

def open_youtube():
    print('running open yt')
    pag.hotkey("ctrl", "t")  # Open a new tab
    pag.write("https://www.youtube.com")  # Type YouTube URL
    pag.press("enter")  # Press Enter to navigate

hotkeys = [
    (";+y", open_youtube),
    (";+d+b", lambda: subprocess.Popen([r"C:\Program Files\JetBrains\PyCharm 2025.2.3\bin\pycharm64.exe"])),
]

def begin_hotkey_listener():
    global listening
    print("Hotkey listener started. Press 'ctrl+shift+h' to trigger the hotkey action.")
    listening = not listening
    if listening:
        for i in hotkeys:
            print(i[0], i[1])
            keyboard.add_hotkey(i[0], i[1])
    else:
        for i in hotkeys:
            keyboard.remove_hotkey(i[0])


keyboard.add_hotkey("ctrl+shift+h+k", begin_hotkey_listener)

keyboard.wait()