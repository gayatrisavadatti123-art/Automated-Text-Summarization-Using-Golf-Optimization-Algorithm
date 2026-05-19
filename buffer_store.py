import sqlite3

def init_db():
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT,
            output TEXT,
            mode TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_record(inp, out, mode):
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO summaries (input, output, mode) VALUES (?, ?, ?)", (inp, out, mode))
    conn.commit()
    conn.close()

def fetch_records(limit=20):
    conn = sqlite3.connect("summaries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT input, output, mode FROM summaries ORDER BY id DESC LIMIT ?", (limit,))
    records = cursor.fetchall()
    conn.close()
    return records

# Initialize DB
init_db()




