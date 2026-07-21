import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from database import check_login


# ---------------- LOGIN FUNCTION ----------------
def login_user():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    # -------- ADMIN LOGIN --------
    if username == "pj" and password == "pj2006":
        messagebox.showinfo("Admin Login", "Welcome Admin!")

        root.destroy()
        subprocess.Popen([sys.executable, "admin_module.py"])
        return

    # -------- NORMAL USER LOGIN --------
    try:
        user = check_login(username, password)

        if user:
            logged_username = user[0]

            messagebox.showinfo("Login Success", f"Welcome {logged_username}!")

            root.destroy()
            subprocess.Popen(
                [sys.executable, "selection.py", logged_username]
            )

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- OPEN REGISTER PAGE ----------------
def open_register():
    root.destroy()
    subprocess.Popen([sys.executable, "register_page.py"])


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Website Blocker - Login")

# ✅ FULL SCREEN
root.state("zoomed")   # Windows full screen
root.configure(bg="#f4f6f7")

# Screen width for scaling
screen_width = root.winfo_screenwidth()

# Dynamic font sizes
title_size = int(screen_width / 40)
label_size = int(screen_width / 90)
entry_size = int(screen_width / 90)
button_size = int(screen_width / 80)

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text=" Login",
    font=("Arial", title_size, "bold"),
    bg="#f4f6f7",
    fg="#2c3e50"
)
title.pack(pady=40)


# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(root, bg="white", padx=50, pady=40)
login_frame.pack(pady=20)


# ---------------- USERNAME ----------------
tk.Label(
    login_frame,
    text="Username",
    font=("Arial", label_size),
    bg="white"
).grid(row=0, column=0, sticky="w", pady=15, padx=10)

entry_username = tk.Entry(
    login_frame,
    width=35,
    font=("Arial", entry_size)
)
entry_username.grid(row=0, column=1)


# ---------------- PASSWORD ----------------
tk.Label(
    login_frame,
    text="Password",
    font=("Arial", label_size),
    bg="white"
).grid(row=1, column=0, sticky="w", pady=15, padx=10)

entry_password = tk.Entry(
    login_frame,
    width=35,
    font=("Arial", entry_size),
    show="*"
)
entry_password.grid(row=1, column=1)


# ---------------- LOGIN BUTTON ----------------
login_btn = tk.Button(
    root,
    text="Login",
    font=("Arial", button_size, "bold"),
    bg="#2ecc71",
    fg="white",
    width=18,
    height=2,
    command=login_user,
    cursor="hand2"
)
login_btn.pack(pady=30)


# ---------------- REGISTER LINK ----------------
register_link = tk.Label(
    root,
    text="Don't have an account? Register",
    font=("Arial", label_size, "underline"),
    fg="#2980b9",
    bg="#f4f6f7",
    cursor="hand2"
)
register_link.pack()

register_link.bind("<Button-1>", lambda e: open_register())


# ---------------- FOOTER ----------------
footer = tk.Label(
    root,
    text="Block. Focus. Achieve.",
    font=("Arial", label_size),
    bg="#f4f6f7",
    fg="#7f8c8d"
)
footer.pack(side="bottom", pady=20)


# ---------------- RUN APP ----------------
root.mainloop()