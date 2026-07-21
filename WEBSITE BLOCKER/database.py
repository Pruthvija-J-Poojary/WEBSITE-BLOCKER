import sqlite3


# -------------------- CONNECTION --------------------
def get_connection():
    conn = sqlite3.connect("webblock.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# -------------------- INITIALIZE DATABASE --------------------
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            phonenumber TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # BLOCKED SITES TABLE (Linked to username correctly)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            website TEXT NOT NULL,
            UNIQUE(username, website),
            FOREIGN KEY (username) 
                REFERENCES users(username) 
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


# ------------------ REGISTER USER ------------------
def register_user(name, username, phonenumber, age, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, username, phonenumber, age, password)
            VALUES (?, ?, ?, ?, ?)
        """, (name, username, phonenumber, age, password))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return "duplicate"

    finally:
        conn.close()


# ------------------ CHECK LOGIN ------------------
def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, name
        FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()
    return user


# ------------------ ADD BLOCKED WEBSITE ------------------
def add_blocked_site(username, website):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO blocked_sites (username, website)
            VALUES (?, ?)
        """, (username, website))
        conn.commit()

    except sqlite3.IntegrityError:
        raise Exception("Website already blocked.")

    finally:
        conn.close()


# ------------------ GET USER WEBSITES ------------------
def get_user_websites(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT website 
        FROM blocked_sites
        WHERE username=?
    """, (username,))

    websites = cursor.fetchall()
    conn.close()
    return websites


# ------------------ DELETE BLOCKED WEBSITE ------------------
def delete_blocked_site(username, website):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM blocked_sites
        WHERE username=? AND website=?
    """, (username, website))


    conn.commit()
    conn.close()
