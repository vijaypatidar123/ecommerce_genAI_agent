import sqlite3
from datetime import datetime
import uuid

DB_PATH = "./data/chat_history.db"


def init_chat_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions (
        session_id TEXT PRIMARY KEY,
        name TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        message TEXT,
        timestamp TEXT,
        FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
    )
    """)
    con.commit()
    con.close()


def create_new_session(name: str = None):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    session_id = str(uuid.uuid4())
    name = name or f"Chat - {datetime.now().strftime('%b %d, %H:%M')}"
    cur.execute("INSERT INTO chat_sessions (session_id, name, created_at) VALUES (?, ?, ?)",
                (session_id, name, datetime.utcnow().isoformat()))
    con.commit()
    con.close()
    return session_id


def list_sessions():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT session_id, name, created_at FROM chat_sessions ORDER BY created_at DESC")
    sessions = cur.fetchall()
    con.close()
    return sessions


def save_message(session_id: str, role: str, message: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("INSERT INTO chats (session_id, role, message, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, role, message, datetime.utcnow().isoformat()))
    con.commit()
    con.close()


def load_messages(session_id: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        SELECT role, message FROM chats
        WHERE session_id = ?
        ORDER BY id
    """, (session_id,))
    rows = cur.fetchall()
    con.close()
    return rows


def rename_session(session_id: str, new_name: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("UPDATE chat_sessions SET name = ? WHERE session_id = ?", (new_name, session_id))
    con.commit()
    con.close()


def delete_session(session_id: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("DELETE FROM chats WHERE session_id = ?", (session_id,))
    cur.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    con.commit()
    con.close()
