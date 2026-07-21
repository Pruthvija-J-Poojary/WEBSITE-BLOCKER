import tkinter as tk 
from tkinter import messagebox 
import subprocess 
import sys 
from database import initialize_database, add_blocked_site 
# ------------------ GET LOGGED-IN USER ------------------ 
try: 
    current_username = sys.argv[1] 
except IndexError: 
    print("User not identified. Please login again.") 
    sys.exit() 
# ------------------ INITIALIZE DATABASE ------------------ 
initialize_database() 
# ------------------ SYSTEM BLOCK FUNCTION ------------------ 
def block_website_system(website): 
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts" 
    redirect_ip = "127.0.0.1" 
    website = website.strip().lower() 
    website = website.replace("http://", "").replace("https://", "") 
    website = website.replace("www.", "") 
    try: 
        with open(hosts_path, "a") as file: 
            file.write(f"{redirect_ip} {website}\n") 
            file.write(f"{redirect_ip} www.{website}\n") 
    except PermissionError: 
        messagebox.showerror("Error", "Run the program as Administrator!") 
        return False 
    return True 
# ------------------ FUNCTIONS ------------------ 
def add_website(): 
    website = entry_website.get().strip() 
    if website == "": 
        messagebox.showerror("Error", "Please enter a website.") 
        return 
    success = block_website_system(website) 
    if success: 
        try: 
            add_blocked_site(current_username, website) 
            messagebox.showinfo("Success", f"{website} has been blocked.") 
            entry_website.delete(0, tk.END) 
        except Exception as e: 
            messagebox.showerror("Error", str(e)) 
def go_back(): 
    root.destroy() 
    subprocess.Popen([sys.executable, "selection.py", current_username]) 
# ------------------ MAIN WINDOW ------------------ 
root = tk.Tk() 
root.title("Add Website - Website Blocker") 
#    FULL SCREEN 
root.state("zoomed") 
root.configure(bg="#f4f6f7") 
# Screen size for scaling 
screen_width = root.winfo_screenwidth() 
screen_height = root.winfo_screenheight() 
# Dynamic font sizes 
title_size = int(screen_width / 40) 
label_size = int(screen_width / 90) 
entry_size = int(screen_width / 90) 
button_size = int(screen_width / 80) 
# ------------------ MAIN FRAME ------------------ 
main_frame = tk.Frame(root, bg="#f4f6f7") 
main_frame.place(relx=0.5, rely=0.5, anchor="center") 
# ------------------ TITLE ------------------ 
title = tk.Label( 
    main_frame, 
    text="Add Website", 
    font=("Arial", title_size, "bold"), 
    bg="#f4f6f7", 
    fg="#2c3e50" 
) 
title.pack(pady=screen_height * 0.03) 
# ------------------ FORM FRAME ------------------ 
frame = tk.Frame(main_frame, bg="white", padx=40, pady=30) 
frame.pack(pady=20) 
tk.Label( 
    frame, 
    text="Website URL", 
    font=("Arial", label_size), 
    bg="white" 
).grid(row=0, column=0, sticky="w", pady=15, padx=10) 
entry_website = tk.Entry(frame, width=35, font=("Arial", entry_size)) 
entry_website.grid(row=0, column=1) 
# ------------------ BUTTONS ------------------ 
add_btn = tk.Button( 
    main_frame, 
    text="Block Website", 
    font=("Arial", button_size, "bold"), 
    bg="#e74c3c", 
    fg="white", 
    width=18, 
    height=2, 
    command=add_website, 
    cursor="hand2" 
) 
add_btn.pack(pady=15) 
back_btn = tk.Button( 
    main_frame, 
    text="Back", 
    font=("Arial", label_size), 
    width=12, 
    command=go_back, 
    cursor="hand2" 
) 
back_btn.pack(pady=10) 
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