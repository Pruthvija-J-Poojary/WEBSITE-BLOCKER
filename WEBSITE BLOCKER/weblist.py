import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
from database import get_user_websites, delete_blocked_site, initialize_database


# ================== USER SESSION ==================
def get_logged_in_user():
    try:
        return sys.argv[1]
    except IndexError:
        print("User not identified. Please login again.")
        sys.exit()


current_username = get_logged_in_user()


# ================== INIT DATABASE ==================
initialize_database()


# ================== UTIL FUNCTIONS ==================
def clean_website(url):
    url = url.strip().lower()
    url = url.replace("http://", "").replace("https://", "")
    url = url.replace("www.", "")
    return url.split("/")[0]


# ================== SYSTEM UNBLOCK ==================
def unblock_website_system(website):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    website = clean_website(website)

    try:
        # Backup (only once)
        backup_path = hosts_path + ".bak"
        if not os.path.exists(backup_path):
            with open(hosts_path, "r") as original, open(backup_path, "w") as backup:
                backup.write(original.read())

        # Read file
        with open(hosts_path, "r") as file:
            lines = file.readlines()

        # Patterns to remove
        patterns = [
            f"127.0.0.1 {website}",
            f"127.0.0.1 www.{website}"
        ]

        # Rewrite file
        with open(hosts_path, "w") as file:
            for line in lines:
                if not any(p in line for p in patterns):
                    file.write(line)

    except PermissionError:
        messagebox.showerror("Error", "⚠ Please run as Administrator!")
        return False

    return True


# ================== MAIN APP ==================
class UnblockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Blocker - Unblock")
        self.root.state("zoomed")  # ✅ Maximize window
        self.root.configure(bg="#ecf0f1")

        self.create_ui()
        self.load_websites()

        # Auto refresh when window gains focus
        self.root.bind("<FocusIn>", lambda e: self.load_websites())

    # ---------- UI ----------
    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(expand=True, fill="both")

        # Title
        tk.Label(
            main_frame,
            text="Blocked Websites",
            font=("Segoe UI", 26, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=25)

        # Listbox Section
        list_frame = tk.Frame(main_frame, bg="#ecf0f1")
        list_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            width=60,
            height=20,
            font=("Segoe UI", 13),
            bd=2,
            relief="groove",
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, padx=5)

        scrollbar.config(command=self.listbox.yview)

        # Double-click unblock
        self.listbox.bind("<Double-Button-1>", lambda e: self.unblock_selected())

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="#ecf0f1")
        btn_frame.pack(pady=20)

        self.unblock_btn = tk.Button(
            btn_frame,
            text="Unblock Selected",
            font=("Segoe UI", 14, "bold"),
            bg="#2ecc71",
            fg="white",
            width=20,
            relief="flat",
            cursor="hand2",
            command=self.unblock_selected
        )
        self.unblock_btn.grid(row=0, column=0, padx=15)

        tk.Button(
            btn_frame,
            text="Back",
            font=("Segoe UI", 12),
            bg="#3498db",
            fg="white",
            width=12,
            relief="flat",
            cursor="hand2",
            command=self.go_back
        ).grid(row=0, column=1, padx=15)

        # Footer
        tk.Label(
            self.root,
            text="Block • Focus • Achieve",
            font=("Segoe UI", 11),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(side="bottom", pady=10)

    # ---------- LOAD DATA ----------
    def load_websites(self):
        self.listbox.delete(0, tk.END)

        try:
            websites = get_user_websites(current_username)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        if not websites:
            self.listbox.insert(tk.END, "No websites blocked")
            self.unblock_btn.config(state="disabled", bg="#bdc3c7")
        else:
            self.unblock_btn.config(state="normal", bg="#2ecc71")
            for site in websites:
                self.listbox.insert(tk.END, site[0])

    # ---------- UNBLOCK ----------
    def unblock_selected(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Select a website to unblock")
            return

        website = self.listbox.get(selected[0])

        if website == "No websites blocked":
            return

        confirm = messagebox.askyesno("Confirm", f"Unblock {website}?")
        if not confirm:
            return

        success = unblock_website_system(website)

        if success:
            try:
                delete_blocked_site(current_username, website)
                messagebox.showinfo("Success", f"{website} has been unblocked")
                self.load_websites()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    # ---------- NAVIGATION ----------
    def go_back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, "selection.py", current_username])


# ================== RUN APP ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = UnblockApp(root)
    root.mainloop()