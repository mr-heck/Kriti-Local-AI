import sqlite3
import os
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nova_memory.db")


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        summary TEXT NOT NULL,

        category TEXT,

        importance INTEGER DEFAULT 5,

        created_at TEXT,

        updated_at TEXT
    )
    """)    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        role TEXT NOT NULL,

        message TEXT NOT NULL,

        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        date TEXT UNIQUE,

        summary TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()



def save_memory(
    summary,
    category,
    importance
):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cur.execute(
        """
        INSERT INTO memories
        (
            summary,
            category,
            importance,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            summary,
            category,
            importance,
            now,
            now
        )
    )

    conn.commit()
    conn.close()

    return True


def show_all():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
        id,
        summary,
        category,
        importance,
        created_at
        FROM memories
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def delete_memory(memory_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM memories
        WHERE id=?
        """,
        (memory_id,)
    )

    conn.commit()
    conn.close()


def get_relevant_memories(question):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    words = question.lower().split()

    results = []

    for word in words:

        cur.execute(
            """
            SELECT
                id,
                summary,
                category,
                importance
            FROM memories
            WHERE LOWER(summary) LIKE ?
            """,
            (f"%{word}%",)
        )

        results.extend(cur.fetchall())

    conn.close()

    unique_results = []
    seen = set()

    for memory in results:

        if memory[0] not in seen:

            unique_results.append(memory)
            seen.add(memory[0])

    unique_results.sort(
        key=lambda x: x[3],
        reverse=True
    )

    return unique_results


def memory_count():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM memories"
    )

    count = cur.fetchone()[0]

    conn.close()

    return count


def backup_memory():

    backup_folder = os.path.join(
        BASE_DIR,
        "backups"
    )

    os.makedirs(
        backup_folder,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    backup_file = os.path.join(
        backup_folder,
        f"memory_backup_{timestamp}.db"
    )

    if os.path.exists(DB_NAME):

        shutil.copy2(
            DB_NAME,
            backup_file
        )

    return backup_file


def wipe_all_memories():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM memories"
    )

    conn.commit()
    conn.close()

    return True

def get_all_memories_text():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT summary
        FROM memories
        ORDER BY importance DESC, updated_at DESC
        LIMIT 50
    """)

    rows = cur.fetchall()

    conn.close()

    if not rows:
        return "No memories stored."

    return "\n".join(
        f"- {row[0]}"
        for row in rows
    )
def get_memories_by_category(category):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT summary
        FROM memories
        WHERE category=?
        ORDER BY importance DESC
        """,
        (category,)
    )

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]    
def save_chat_message(role, message):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

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
            now
        )
    )

    conn.commit()
    conn.close()

def get_today_chat():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, message
        FROM chat_history
        WHERE DATE(timestamp)=?
        ORDER BY id ASC
        """,
        (today,)
    )

    rows = cur.fetchall()

    conn.close()

    if not rows:
        return "No chat history."

    return "\n".join(
        f"{role.upper()}: {message}"
        for role, message in rows
    )
def get_recent_chat(limit=30):

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
def save_daily_summary(summary):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO daily_summaries
        (
            date,
            summary
        )
        VALUES (?, ?)
        """,
        (
            today,
            summary
        )
    )

    conn.commit()
    conn.close()

def search_chat(keyword):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, message, timestamp
        FROM chat_history
        WHERE LOWER(message) LIKE ?
        ORDER BY id DESC
        """,
        (
            f"%{keyword.lower()}%",
        )
    )

    rows = cur.fetchall()

    conn.close()

    return rows
def cleanup_old_chat(days=30):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM chat_history
        WHERE timestamp <
        datetime('now', ?)
        """,
        (
            f"-{days} days",
        )
    )

    conn.commit()
    conn.close()
    
init_db()