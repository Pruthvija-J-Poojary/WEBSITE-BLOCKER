import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from database import initialize_database, register_user


# ------------------ INITIALIZE DATABASE ------------------
initialize_database()


# ------------------ REGISTER FUNCTION ------------------
def handle_register():
    name = entry_name.get().strip()
    username = entry_username.get().strip()
    phone = entry_phone.get().strip()
    age = entry_age.get().strip()
    password = entry_password.get().strip()
    confirm_password = entry_confirm.get().strip()

    # -------- VALIDATIONS --------
    if not all([name, username, phone, age, password, confirm_password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Age must be a positive number!")
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Phone number must be exactly 10 digits!")
        return

    if len(password) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters!")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # -------- DATABASE INSERT --------
    result = register_user(name, username, phone, int(age), password)

    if result == True:
        messagebox.showinfo(
            "Success",
            f"Registration Successful!\n\nWelcome, {name}!"
        )
        root.destroy()
        subprocess.Popen([sys.executable, "login_page.py"])

    elif result == "duplicate":
        messagebox.showerror(
            "Error",
            "Username or Phone Number already exists!"
        )


# ------------------ OPEN LOGIN PAGE ------------------
def open_login():
    root.destroy()
    subprocess.Popen([sys.executable, "login_page.py"])


# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Website Blocker - Registration")

# MAXIMIZE WINDOW
root.state("zoomed")
root.configure(bg="#f4f6f7")

# Screen size for scaling
screen_width = root.winfo_screenwidth()

# Dynamic font scaling
title_size = int(screen_width / 40)
label_size = int(screen_width / 90)
entry_size = int(screen_width / 90)
button_size = int(screen_width / 80)

# ------------------ HEADING ------------------
title = tk.Label(
    root,
    text="User Registration",
    font=("Arial", title_size, "bold"),
    bg="#f4f6f7",
    fg="#2c3e50"
)
title.pack(pady=30)


# ------------------ FORM FRAME ------------------
form_frame = tk.Frame(root, bg="white", padx=40, pady=40)
form_frame.pack(pady=20)

labels = ["Full Name", "Username", "Phone Number", "Age", "Password", "Confirm Password"]
entries = []

for i, label in enumerate(labels):
    tk.Label(
        form_frame,
        text=label,
        font=("Arial", label_size),
        bg="white"
    ).grid(row=i, column=0, sticky="w", pady=12, padx=10)

    if "Password" in label:
        entry = tk.Entry(form_frame, width=35, font=("Arial", entry_size), show="*")
    else:
        entry = tk.Entry(form_frame, width=35, font=("Arial", entry_size))

    entry.grid(row=i, column=1, pady=5)
    entries.append(entry)

# Assign entries
entry_name, entry_username, entry_phone, entry_age, entry_password, entry_confirm = entries


# ------------------ REGISTER BUTTON ------------------
register_btn = tk.Button(
    root,
    text="Register",
    font=("Arial", button_size, "bold"),
    bg="#3498db",
    fg="white",
    width=18,
    height=2,
    command=handle_register,
    cursor="hand2"
)
register_btn.pack(pady=30)


# ------------------ LOGIN LINK ------------------
login_link = tk.Label(
    root,
    text="Already have an account? Login",
    font=("Arial", label_size, "underline"),
    fg="#2980b9",
    bg="#f4f6f7",
    cursor="hand2"
)
login_link.pack()

login_link.bind("<Button-1>", lambda e: open_login())


# ------------------ FOOTER ------------------
footer = tk.Label(
    root,
    text="Block. Focus. Achieve.",
    font=("Arial", label_size),
    bg="#f4f6f7",
    fg="#7f8c8d"
)
footer.pack(side="bottom", pady=20)


root.mainloop()