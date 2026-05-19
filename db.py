import sqlite3

DB_NAME = "summaries.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            summary_text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_summary(input_text, summary_text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO summaries (input_text, summary_text) VALUES (?, ?)", (input_text, summary_text))
    conn.commit()
    conn.close()