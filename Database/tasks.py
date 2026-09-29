import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "nova_memory.db")


def init_tasks_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        priority TEXT DEFAULT 'Medium'
    )
    """)

    conn.commit()
    conn.close()


def add_task(task, priority="Medium"):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id FROM tasks
        WHERE LOWER(task)=?
        """,
        (task.lower(),)
    )

    existing = cur.fetchone()

    if not existing:

        cur.execute(
            """
            INSERT INTO tasks
            (task, priority)
            VALUES (?, ?)
            """,
            (task, priority)
        )

    conn.commit()
    conn.close()


def show_tasks():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
        id,
        task,
        status,
        priority
        FROM tasks
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows


def complete_task(task_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status='Completed'
        WHERE id=?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM tasks
        WHERE id=?
        """,
        (task_id,)
    )

    conn.commit()
    conn.close()