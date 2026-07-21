import tkinter as tk
import subprocess
import sys


# ------------------ GET LOGGED-IN USER ------------------
try:
    current_username = sys.argv[1]
except IndexError:
    print("User not identified. Please login again.")
    sys.exit()


# ------------------ FUNCTIONS ------------------
def open_add_website():
    root.destroy()
    subprocess.Popen([sys.executable, "addweb.py", current_username])


def open_settings():
    root.destroy()
    subprocess.Popen([sys.executable, "setting.py", current_username])


def open_weblist():
    root.destroy()
    subprocess.Popen([sys.executable, "weblist.py", current_username])


def open_about():
    root.destroy()
    subprocess.Popen([sys.executable, "about.py", current_username])


# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Website Blocker")

# ✅ FULL SCREEN
root.state("zoomed")

# Screen size for scaling
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dynamic font sizes
title_size = int(screen_width / 40)
button_size = int(screen_width / 80)

# ------------------ MAIN FRAME (CENTERED) ------------------
main_frame = tk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")


# ------------------ TITLE ------------------
title_label = tk.Label(
    main_frame,
    text=f"WEBSITE BLOCKER\nWelcome, {current_username}",
    font=("Arial", title_size, "bold"),
    justify="center"
)
title_label.pack(pady=screen_height * 0.05)


# ------------------ BUTTONS ------------------
add_website_btn = tk.Button(
    main_frame,
    text="Add Website Page",
    width=30,
    height=2,
    font=("Arial", button_size),
    command=open_add_website,
    cursor="hand2"
)
add_website_btn.pack(pady=15)


blocked_list_btn = tk.Button(
    main_frame,
    text="Blocked Websites List",
    width=30,
    height=2,
    font=("Arial", button_size),
    command=open_weblist,
    cursor="hand2"
)
blocked_list_btn.pack(pady=15)


settings_btn = tk.Button(
    main_frame,
    text="Settings Page",
    width=30,
    height=2,
    font=("Arial", button_size),
    command=open_settings,
    cursor="hand2"
)
settings_btn.pack(pady=15)


about_btn = tk.Button(
    main_frame,
    text="About Page",
    width=30,
    height=2,
    font=("Arial", button_size),
    command=open_about,
    cursor="hand2"
)
about_btn.pack(pady=15)


# ------------------ START APP ------------------
root.mainloop()