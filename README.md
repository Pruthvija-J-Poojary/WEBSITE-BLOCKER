# Website Blocker 🚫

A desktop productivity application built with **Python** and **Tkinter** that helps users
stay focused by blocking distracting websites at the system level.

## Features
- 🔐 User registration & login (with a separate admin login)
- 🌐 Add websites to a personal block list (edits the Windows `hosts` file)
- 📋 View and unblock previously blocked sites
- ♻️ Reset all blocked websites in one click
- ⚙️ Account settings — view profile, change password
- 🛠️ Admin dashboard — view all users and their blocked sites, delete users
- 💾 SQLite database for persistent storage

## Tech Stack
- **Python 3**
- **Tkinter** — GUI
- **SQLite3** — local database
- Windows `hosts` file manipulation for real blocking

## How It Works
Blocked websites are stored per-user in a SQLite database. When a site is blocked,
the app appends redirect entries to the system `hosts` file (`127.0.0.1`), and removes
them again when unblocked — requires running as Administrator on Windows.

## Note
This app must be run with Administrator privileges to modify the system hosts file.
