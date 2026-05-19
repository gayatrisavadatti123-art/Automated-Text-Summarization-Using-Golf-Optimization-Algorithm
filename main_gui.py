import tkinter as tk
from tkinter import messagebox, scrolledtext
from goa_logic import run_goa_summary
from db import save_summary, init_db
from view_data import show_summaries

# Initialize DB
init_db()

def summarize():
    text = input_text.get("1.0", "end").strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text to summarize.")
        return
    summary = run_goa_summary(text)
    output_text.delete("1.0", "end")
    output_text.insert("1.0", summary)
    save_summary(text, summary)

# GUI Setup
root = tk.Tk()
root.title("GOA Text Summarizer")
root.geometry("800x600")

tk.Label(root, text="Enter Text:", font=("Arial", 12, "bold")).pack()
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=15)
input_text.pack(padx=10, pady=5)

tk.Button(root, text="Summarize", command=summarize, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

tk.Label(root, text="Summary:", font=("Arial", 12, "bold")).pack()
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=10)
output_text.pack(padx=10, pady=5)

tk.Button(root, text="View Saved Summaries", command=show_summaries, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

root.mainloop()