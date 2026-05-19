import sqlite3
import tkinter as tk
from tkinter import scrolledtext

DB_NAME = "summaries.db"

def show_summaries():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM summaries")
    rows = cursor.fetchall()
    conn.close()

    window = tk.Toplevel()
    window.title("Saved Summaries")
    window.geometry("800x500")

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 10))
    text_area.pack(expand=True, fill="both")

    for i, row in enumerate(rows, start=1):
        text_area.insert("end", f"Record {i}:\nInput:\n{row[1]}\nSummary:\n{row[2]}\n{'-'*50}\n")
