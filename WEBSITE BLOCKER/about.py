import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# ------------------ GET LOGGED-IN USER ------------------
try:
    current_username = sys.argv[1]
except IndexError:
    print("User not identified. Please login again.")
    sys.exit()

# ------------------ FUNCTIONS ------------------
def go_back():
    root.destroy()
    subprocess.Popen([sys.executable, "selection.py", current_username])

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("About - Website Blocker")
root.state("zoomed")   # Fullscreen (better than attributes)

root.configure(bg="#f4f6f7")

# Exit fullscreen with ESC
root.bind("<Escape>", lambda e: root.state("normal"))

# ------------------ TITLE ------------------
title = tk.Label(
    root,
    text="ABOUT WEBSITE BLOCKER",
    font=("Arial", 30, "bold"),
    bg="#f4f6f7",
    fg="#2c3e50"
)
title.pack(pady=40)

# ------------------ CONTENT FRAME ------------------
frame = tk.Frame(root, bg="white", padx=40, pady=30)
frame.pack(pady=10)

about_text = (
    "Website Blocker is a desktop application that helps users stay focused\n"
    "by blocking distracting websites.\n\n"

    "Main Functions:\n"
    "• User login and registration\n"
    "• Add websites to block list\n"
    "• Block websites using system hosts file\n"
    "• View and unblock blocked websites\n"
    "• Reset all blocked websites\n"
    "• Manage account settings (change password)\n\n"

    "How It Works:\n"
    "• Blocked websites are stored in the database\n"
    "• The application updates the system hosts file to restrict access\n"
    "• When unblocked, entries are removed from the hosts file\n\n"

    "This application is designed to improve focus and productivity\n"
    "by reducing access to distracting websites."
)

content = tk.Label(
    frame,
    text=about_text,
    font=("Arial", 14),
    bg="white",
    fg="#2c3e50",
    justify="left"
)
content.pack()

# ------------------ BUTTON FRAME ------------------
btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=20)

# Back Button
back_btn = tk.Button(
    btn_frame,
    text="Back",
    font=("Arial", 12),
    width=15,
    bg="#3498db",
    fg="white",
    cursor="hand2",
    command=go_back
)
back_btn.grid(row=0, column=0, padx=15)

# Exit Button
exit_btn = tk.Button(
    btn_frame,
    text="Exit",
    font=("Arial", 12),
    width=15,
    bg="#e74c3c",
    fg="white",
    cursor="hand2",
    command=exit_app
)
exit_btn.grid(row=0, column=1, padx=15)

# ------------------ FOOTER ------------------
footer = tk.Label(
    root,
    text=f"Logged in as: {current_username}  |  Block distractions. Boost productivity.",
    font=("Arial", 11),
    bg="#f4f6f7",
    fg="#7f8c8d"
)
footer.pack(side="bottom", pady=20)

# ------------------ RUN APP ------------------
root.mainloop()