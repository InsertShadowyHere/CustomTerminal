import keyboard
import sys
import subprocess

def open_console():
    print("running!")
    subprocess.Popen([sys.executable, "console.py"])

keyboard.add_hotkey("`", open_console)
# TODO - make it so that you can only have one console at a time
keyboard.wait()