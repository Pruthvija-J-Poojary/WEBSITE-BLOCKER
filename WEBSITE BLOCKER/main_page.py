import tkinter as tk
from tkinter import messagebox
import os
import sys

def start_project():
    root.destroy()
    os.system(f'"{sys.executable}" front_page.py')

# Create main window
root = tk.Tk()
root.title("Website Blocker")

# Make full screen
root.state("zoomed")  # For Windows (maximized)
root.configure(bg="#f2f2f2")

# Get screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dynamic font scaling
title_size = int(screen_width / 30)
subtitle_size = int(screen_width / 60)
desc_size = int(screen_width / 70)
button_size = int(screen_width / 65)

# Main container (center everything)
main_frame = tk.Frame(root, bg="#f2f2f2")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label
title_label = tk.Label(
    main_frame,
    text="WEBSITE BLOCKER",
    font=("Arial", title_size, "bold"),
    bg="#f2f2f2",
    fg="#2c3e50"
)
title_label.pack(pady=screen_height * 0.03)

# Subtitle
subtitle_label = tk.Label(
    main_frame,
    text="“Manage internet usage for improved concentration.”",
    font=("Arial", subtitle_size),
    bg="#f2f2f2",
    fg="#34495e"
)
subtitle_label.pack(pady=screen_height * 0.02)

# Description
description = tk.Label(
    main_frame,
    text="“Stay focused. Block distractions.”",
    font=("Arial", desc_size),
    bg="#f2f2f2",
    fg="#555555"
)
description.pack(pady=screen_height * 0.03)

# Start Button
start_button = tk.Button(
    main_frame,
    text="Get Started",
    font=("Arial", button_size, "bold"),
    bg="#3498db",
    fg="white",
    width=20,
    height=2,
    command=start_project,
    cursor="hand2"
)
start_button.pack(pady=screen_height * 0.05)

# Footer
footer = tk.Label(
    root,
    text="Block. Focus. Achieve.",
    font=("Arial", subtitle_size),
    bg="#f2f2f2",
    fg="#888888"
)
footer.pack(side="bottom", pady=20)

root.mainloop()