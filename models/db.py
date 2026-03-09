import sqlite3

DB_NAME = "database.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        weight REAL,
        program TEXT,
        calories INTEGER
    )
    """)

    conn.commit()
    conn.close()