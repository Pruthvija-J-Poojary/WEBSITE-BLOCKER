import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection, get_user_websites


# ---------------- FETCH USERS ----------------
def fetch_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, username, phonenumber, age
        FROM users
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------- REFRESH DATA ----------------
def refresh_data():
    users_tree.delete(*users_tree.get_children())

    for user in fetch_users():
        username = user[2]

        websites = get_user_websites(username)
        sites = [site[0] for site in websites]

        blocked_text = ", ".join(sites) if sites else "None"

        users_tree.insert("", tk.END, values=(*user, blocked_text))


# ---------------- DELETE USER ----------------
def delete_user():
    selected = users_tree.focus()

    if not selected:
        messagebox.showerror("Error", "Select a user to delete.")
        return

    user_id = users_tree.item(selected, "values")[0]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "User deleted successfully")
    refresh_data()


# ---------------- COLORS (MATCH LOGIN PAGE) ----------------
BG_COLOR = "#f4f6f7"   # same as login page
FRAME_COLOR = "#ffffff"
TEXT_COLOR = "#2c3e50"
HEADER_COLOR = "#2980b9"


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Admin Dashboard - Web Blocker")
root.geometry("1050x550")
root.configure(bg=BG_COLOR)


# ---------------- STYLE ----------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=FRAME_COLOR,
    foreground="black",
    rowheight=30,
    fieldbackground=FRAME_COLOR,
    font=("Arial", 10)
)

style.map("Treeview",
          background=[("selected", "#d6eaf8")])

style.configure(
    "Treeview.Heading",
    background=HEADER_COLOR,
    foreground="white",
    font=("Arial", 11, "bold")
)


# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="ADMIN CONTROL PANEL",
    font=("Arial", 24, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(pady=20)


# ---------------- TABLE FRAME ----------------
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(fill="both", expand=True, padx=20)


# ---------------- USERS TABLE ----------------
columns = ("ID", "Name", "Username", "phonenumber", "Age", "Blocked Sites")

users_tree = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    users_tree.heading(col, text=col)

users_tree.column("ID", width=60, anchor="center")
users_tree.column("Name", width=150)
users_tree.column("Username", width=150)
users_tree.column("phonenumber", width=220)
users_tree.column("Age", width=80, anchor="center")
users_tree.column("Blocked Sites", width=300)


# ---------------- SCROLLBAR ----------------
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=users_tree.yview)
users_tree.configure(yscrollcommand=scrollbar.set)

users_tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# ---------------- BUTTON FRAME ----------------
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=15)


# ---------------- BUTTONS ----------------
delete_btn = tk.Button(
    btn_frame,
    text="Delete Selected User",
    command=delete_user,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

refresh_btn = tk.Button(
    btn_frame,
    text="Refresh Dashboard",
    command=refresh_data,
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

delete_btn.grid(row=0, column=0, padx=10)
refresh_btn.grid(row=0, column=1, padx=10)


# ---------------- LOAD DATA ----------------
refresh_data()

root.mainloop()