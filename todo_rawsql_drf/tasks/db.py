import sqlite3
import logging
from django.conf import settings
from contextlib import contextmanager

logger = logging.getLogger('tasks')

def get_db_path():
    return str(settings.DB_FILE)

@contextmanager
def get_conn():
    conn = None
    try:
        conn = sqlite3.connect(get_db_path(), detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.exception("DB Error: %s", e)
        raise
    finally:
        if conn:
            conn.close()

def create_tasks_table():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending'
        );
        """)
        conn.commit()
        logger.info("Ensured tasks table exists.")

def fetch_all_tasks():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, description, due_date, status FROM tasks ORDER BY id DESC;")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def fetch_task(task_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, description, due_date, status FROM tasks WHERE id = ?;", (task_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def insert_task(title, description=None, due_date=None, status='pending'):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?);",
            (title, description, due_date, status)
        )
        conn.commit()
        return cur.lastrowid

def update_task(task_id, title=None, description=None, due_date=None, status=None):
    with get_conn() as conn:
        cur = conn.cursor()
        fields = []
        params = []

        if title is not None:
            fields.append("title = ?")
            params.append(title)
        if description is not None:
            fields.append("description = ?")
            params.append(description)
        if due_date is not None:
            fields.append("due_date = ?")
            params.append(due_date)
        if status is not None:
            fields.append("status = ?")
            params.append(status)

        if not fields:
            return False

        params.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?;"
        cur.execute(sql, params)
        conn.commit()

        return cur.rowcount > 0

def delete_task(task_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
        conn.commit()
        return cur.rowcount > 0
