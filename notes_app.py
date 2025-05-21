import customtkinter as ctk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from cryptography.fernet import Fernet
import base64
import hashlib
import os
import json

# App config
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Secure Notes")
app.geometry("1000x700")

# Layout frames
sidebar = ctk.CTkFrame(app, width=200)
sidebar.pack(side="left", fill="y")

main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", fill="both", expand=True)

# Tabs view for notes
tabs = ctk.CTkTabview(main_frame)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

# notes will map note names -> dict with tab, textbox, and password_entry
notes = {}
session_file = "session.json"

# Categories (unused in session saving for now, but kept for UI)
categories = ["School", "Personal", "Work"]
category_colors = {
    "School": "#6A5ACD",
    "Personal": "#FFD700",
    "Work": "#FF6347"
}

def generate_key(password):
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def save_note(tab_name, textbox, password_entry):
    content = textbox.get("1.0", "end-1c")
    password = password_entry.get()
    if not password:
        msgbox.showerror("Error", "Please enter a password.")
        return
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(content.encode())

    file_path = filedialog.asksaveasfilename(
        defaultextension=".note",
        filetypes=[("Encrypted Notes", "*.note")],
        initialfile=f"{tab_name}.note"
    )
    if file_path:
        with open(file_path, 'wb') as f:
            f.write(encrypted)
        msgbox.showinfo("Saved", f"Note saved securely to:\n{file_path}")
        save_session()

def load_note():
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted Notes", "*.note")])
    if not file_path:
        return

    pwd_dialog = ctk.CTkInputDialog(
        text="Enter the password used to encrypt this note:",
        title="Import Encrypted Note"
    )
    password = pwd_dialog.get_input()
    if password is None:
        return

    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()
        key = generate_key(password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted).decode()

        tab_name = os.path.basename(file_path).replace(".note", "")
        add_or_update_tab(tab_name, decrypted)
        save_session()
    except Exception:
        msgbox.showerror("Error", "Incorrect password or corrupted file.")

def create_note(category="Uncategorized"):
    name = f"Note {len(notes) + 1}"
    add_or_update_tab(name, "")
    save_session()

def add_or_update_tab(name, content):
    # if already exists update its textbox
    if name in notes:
        widget_info = notes[name]
        txt = widget_info["textbox"]
        txt.delete("1.0", "end")
        txt.insert("1.0", content)
        return

    # otherwise create a new tab
    tab = tabs.add(name)
    txt = ctk.CTkTextbox(tab)
    txt.insert("1.0", content)
    txt.pack(fill="both", expand=True, padx=5, pady=5)

    pwd_entry = ctk.CTkEntry(tab, placeholder_text="Password")
    pwd_entry.pack(pady=5)

    save_btn = ctk.CTkButton(
        tab,
        text="Save",
        command=lambda: save_note(name, txt, pwd_entry)
    )
    save_btn.pack(pady=5)

    # keep references so we can update later
    notes[name] = {
        "tab": tab,
        "textbox": txt,
        "password_entry": pwd_entry
    }

def save_session():
    # build a mapping name --------> current content
    session_data = {name: info["textbox"].get("1.0", "end-1c")
                    for name, info in notes.items()}
    with open(session_file, "w") as f:
        json.dump(session_data, f)

def restore_session():
    if not os.path.exists(session_file):
        return
    try:
        with open(session_file, "r") as f:
            session_data = json.load(f)
        for name, content in session_data.items():
            add_or_update_tab(name, content)
    except Exception:
        # ignore corrupt session
        pass

# Sidebar UI
ctk.CTkLabel(sidebar, text="Add New", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
for cat in categories:
    color = category_colors.get(cat, "#FFFFFF")
    ctk.CTkButton(
        sidebar,
        text=cat,
        fg_color=color,
        text_color="black",
        command=lambda c=cat: create_note(category=c)
    ).pack(pady=5, padx=10, fill="x")

ctk.CTkLabel(sidebar, text="\nOther", font=ctk.CTkFont(size=14)).pack(pady=5)
ctk.CTkButton(sidebar, text="📝 New Note", command=create_note).pack(pady=5, padx=10, fill="x")
ctk.CTkButton(sidebar, text="🔓 Import Note", command=load_note).pack(pady=5, padx=10, fill="x")


restore_session()
app.mainloop()
