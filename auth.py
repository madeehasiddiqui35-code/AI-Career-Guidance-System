import sqlite3
import hashlib

# Create database and table
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, email, password):
    try:
        hashed_password = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


def login_user(email, password):
    hashed_password = hash_password(password)

    cursor.execute(
        """
        SELECT name, email
        FROM users
        WHERE email = ? AND password = ?
        """,
        (email, hashed_password)
    )

    user = cursor.fetchone()

    if user:
        return user

    return None
