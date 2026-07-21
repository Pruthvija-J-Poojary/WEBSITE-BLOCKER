import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
from database import get_connection, initialize_database


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


# ================== MAIN APP ==================
class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings - Website Blocker")
        self.root.state("zoomed")  # ✅ Maximize window

        self.create_ui()

    # ---------- UI ----------
    def create_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="SETTINGS",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        # Main Frame
        frame = tk.Frame(self.root, padx=40, pady=20)
        frame.pack()

        # -------- PROFILE --------
        profile_btn = tk.Button(
            frame,
            text="View My Profile",
            font=("Arial", 13),
            width=30,
            command=self.show_user_info
        )
        profile_btn.pack(pady=8)

        # -------- BLOCKED WEBSITES --------
        count_btn = tk.Button(
            frame,
            text="Show Total Blocked Websites",
            font=("Arial", 13),
            width=30,
            command=self.show_total_blocked
        )
        count_btn.pack(pady=8)

        reset_btn = tk.Button(
            frame,
            text="Reset All My Blocked Websites",
            font=("Arial", 13, "bold"),
            bg="#e74c3c",
            fg="white",
            width=30,
            command=self.reset_blocked_websites
        )
        reset_btn.pack(pady=8)

        # -------- PASSWORD --------
        tk.Label(
            frame,
            text="Change Password",
            font=("Arial", 14, "bold")
        ).pack(pady=(20, 5))

        self.entry_password = tk.Entry(
            frame,
            font=("Arial", 13),
            width=25,
            show="*"
        )
        self.entry_password.pack(pady=5)

        change_pass_btn = tk.Button(
            frame,
            text="Update Password",
            font=("Arial", 12),
            width=25,
            command=self.change_password
        )
        change_pass_btn.pack(pady=8)

        # -------- NAVIGATION --------
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=15)

        back_btn = tk.Button(
            nav_frame,
            text="Back",
            font=("Arial", 12),
            width=15,
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, padx=10)

        logout_btn = tk.Button(
            nav_frame,
            text="Logout",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.logout
        )
        logout_btn.grid(row=0, column=1, padx=10)

        # Footer
        footer = tk.Label(
            self.root,
            text=f"Logged in as: {current_username}",
            font=("Arial", 10)
        )
        footer.pack(side="bottom", pady=15)

    # ---------- FUNCTIONS ----------
    def show_total_blocked(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM blocked_sites WHERE username=?",
            (current_username,)
        )

        total = cursor.fetchone()[0]
        conn.close()

        messagebox.showinfo(
            "Blocked Websites",
            f"You have blocked {total} website(s)."
        )

    def show_user_info(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, phonenumber, age FROM users WHERE username=?",
            (current_username,)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            name, phonenumber, age = user
            messagebox.showinfo(
                "My Profile",
                f"Name: {name}\nphonenumber: {phonenumber}\nAge: {age}"
            )
        else:
            messagebox.showerror("Error", "User not found.")

    def change_password(self):
        new_password = self.entry_password.get().strip()

        if not new_password:
            messagebox.showerror("Error", "Enter a new password.")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_password, current_username)
        )

        conn.commit()
        conn.close()

        self.entry_password.delete(0, tk.END)

        messagebox.showinfo("Success", "Password updated successfully.")

    def reset_blocked_websites(self):
        confirm = messagebox.askyesno(
            "Confirm",
            "Remove ALL your blocked websites?"
        )

        if confirm:
            conn = get_connection()
            cursor = conn.cursor()

         # 🔹 Get all blocked websites before deleting
            cursor.execute(
                "SELECT website FROM blocked_sites WHERE username=?",
                (current_username,)
            )
            websites = cursor.fetchall()

        # 🔹 Delete from database
            cursor.execute(
                "DELETE FROM blocked_sites WHERE username=?",
                (current_username,)
            )
            conn.commit()
            conn.close()

        # 🔹 Remove from HOSTS file (browser level)
            hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

            try:
                with open(hosts_path, "r") as file:
                    lines = file.readlines()

                with open(hosts_path, "w") as file:
                    for line in lines:
                        if not any(site[0] in line for site in websites):
                            file.write(line)

            # 🔹 Flush DNS (real-time effect)
                subprocess.run("ipconfig /flushdns", shell=True)

                messagebox.showinfo(
                    "Done",
                    "All blocked websites removed from system & browser."
                )

            except PermissionError:
                messagebox.showerror(
                    "Error",
                    "Run this app as Administrator to update browser blocking."
                )

    def go_back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, "selection.py", current_username])

    def logout(self):
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if confirm:
            self.root.destroy()
            subprocess.Popen([sys.executable, "login.py"])


# ================== RUN ==================
if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()