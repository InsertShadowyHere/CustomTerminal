import keyboard
import sys
import subprocess

def open_terminal():
    print("running!")
    subprocess.Popen([sys.executable, "terminal.py"])

keyboard.add_hotkey("ctrl+;", open_terminal)

keyboard.wait()
