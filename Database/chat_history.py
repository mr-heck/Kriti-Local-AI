import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nova_memory.db")


def init_chat_history():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def save_chat_message(role, message):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chat_history
        (
            role,
            message,
            timestamp
        )
        VALUES (?, ?, ?)
        """,
        (
            role,
            message,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()
    conn.close()


def get_today_chat():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        """
        SELECT role, message
        FROM chat_history
        WHERE timestamp LIKE ?
        ORDER BY id ASC
        """,
        (f"{today}%",)
    )

    rows = cur.fetchall()

    conn.close()

    if not rows:
        return "No conversation today."

    lines = []

    for role, message in rows:

        if role == "user":
            lines.append(f"USER: {message}")
        else:
            lines.append(f"KRITI: {message}")

    return "\n".join(lines)


def get_recent_chat(limit=50):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, message
        FROM chat_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cur.fetchall()

    conn.close()

    rows.reverse()

    return "\n".join(
        f"{role.upper()}: {message}"
        for role, message in rows
    )


def clear_chat_history():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM chat_history"
    )

    conn.commit()
    conn.close()


init_chat_history()