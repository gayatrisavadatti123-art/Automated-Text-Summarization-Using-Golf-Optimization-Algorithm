import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
import threading
import re
from collections import Counter

# Import your modules
from voice_module import speak_text, stop_speaking
from buffer_store import save_record

# ---------------------------
# Configuration
# ---------------------------
MAX_WORDS = 1000
MIN_WORDS = 5
history = []   # <-- History list (now working)
listening = False

# ---------------------------
# Summarization function
# ---------------------------
def summarize_text(text, max_sentences=3):
    text = text.strip()
    if not text:
        raise ValueError("Empty text cannot be summarized.")

    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) <= max_sentences:
        return "Summary: " + text

    words = re.findall(r'\w+', text.lower())

    stopwords = set([
        "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
        "this", "that", "an", "be", "by", "are", "it", "as", "at", "from"
    ])

    word_freq = Counter(w for w in words if w not in stopwords)
    if not word_freq:
        return "Summary: " + sentences[0]

    sentence_scores = {}
    for sent in sentences:
        score = sum(word_freq.get(w.lower(), 0) for w in re.findall(r'\w+', sent))
        sentence_scores[sent] = score

    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = " ".join(ranked[:max_sentences])
    return "Summary: " + summary

# ---------------------------
# Google Maps for addresses
# ---------------------------
def open_map(address):
    url = f"https://www.google.com/maps/search/{address.replace(' ', '+')}"
    webbrowser.open(url)

def is_address(text):
    address_keywords = ["street", "road", "lane", "avenue", "city", "state",
                        "karnataka", "hubli", "pincode", "near", "area", "house"]
    text_lower = text.lower()
    word_count = len(text_lower.split())
    numbers = re.findall(r'\b\d+\b', text_lower)
    if any(word in text_lower for word in address_keywords) and numbers and word_count >= 5:
        return True
    return False

# ---------------------------
# Process input
# ---------------------------
def process_input():
    user_input = text_input.get("1.0", tk.END).strip()
    
    if not user_input:
        messagebox.showerror("Error", "Please enter text or address!")
        return

    word_count = len(user_input.split())

    # 1️⃣ Word limit check
    if word_count > MAX_WORDS:
        messagebox.showerror(
            "Word Limit Exceeded",
            f"Input has {word_count} words. Maximum allowed is {MAX_WORDS}."
        )
        return

    # 2️⃣ Address detection
    if is_address(user_input):
        result_output.config(state=tk.NORMAL)
        result_output.delete("1.0", tk.END)
        result_output.insert(
            tk.END,
            f"Opening Google Map for: {user_input}\nDirections: Follow Google Maps guidance."
        )
        result_output.config(state=tk.DISABLED)
        open_map(user_input)
        return

    # 3️⃣ Text summarization
    if MIN_WORDS <= word_count <= MAX_WORDS:
        try:
            summary = summarize_text(user_input)

            # Show summary
            result_output.config(state=tk.NORMAL)
            result_output.delete("1.0", tk.END)
            result_output.insert(tk.END, summary)
            result_output.config(state=tk.DISABLED)

            # Save to DB
            save_record(user_input, summary, "Text")

            # Save to history
            history.append((user_input, summary))

            # Speak summary
            threading.Thread(target=speak_text, args=(summary,)).start()

        except Exception as e:
            messagebox.showerror("Summarization Error", str(e))
        return

    # 4️⃣ Invalid input
    messagebox.showerror("Invalid Input", "Input not recognized as valid text or address!")

# ---------------------------
# Voice input
# ---------------------------
import speech_recognition as sr

def voice_input():
    global listening
    r = sr.Recognizer()
    mic = sr.Microphone()
    listening = True
    voice_button.config(text="Listening...")

    def listen():
        global listening
        with mic as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=60)
                if not listening:
                    return
                text = r.recognize_google(audio)
                text_input.delete("1.0", tk.END)
                text_input.insert(tk.END, text)
            except sr.WaitTimeoutError:
                messagebox.showinfo("Voice Input", "No speech detected.")
            except Exception as e:
                messagebox.showerror("Voice Input Error", str(e))

        listening = False
        voice_button.config(text="Voice Input")

    threading.Thread(target=listen).start()

def stop_listening():
    global listening
    listening = False
    voice_button.config(text="Voice Input")

# ---------------------------
# View summarized history (COLORED)
# ---------------------------
def view_history():
    if not history:
        messagebox.showinfo("History", "No records available.")
        return

    hist_win = tk.Toplevel(root)
    hist_win.title("Summarized History")

    hist_text = scrolledtext.ScrolledText(hist_win, width=80, height=20)
    hist_text.pack()

    # Color tags
    hist_text.tag_config("input_box", background="#dce6ff")   # Light Blue
    hist_text.tag_config("output_box", background="#dfffe0")  # Light Green
    hist_text.tag_config("title", font=("Arial", 11, "bold"))

    for idx, (inp, outp) in enumerate(history, 1):
        hist_text.insert(tk.END, f"{idx}. Input:\n", "title")
        hist_text.insert(tk.END, inp + "\n", "input_box")

        hist_text.insert(tk.END, f"Output:\n", "title")
        hist_text.insert(tk.END, outp + "\n\n", "output_box")

    hist_text.config(state=tk.DISABLED)

# ---------------------------
# GUI Setup
# ---------------------------
root = tk.Tk()
root.title("Summarizer & Map GUI")
root.geometry("800x500")

tk.Label(root, text="Enter text or address:", font=("Arial", 12)).pack(pady=5)
text_input = tk.Text(root, height=10, width=90)
text_input.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

process_button = tk.Button(button_frame, text="Summarize / Go", font=("Arial", 12, "bold"), command=process_input)
process_button.grid(row=0, column=0, padx=5)

view_button = tk.Button(button_frame, text="View Summarized", font=("Arial", 12), command=view_history)
view_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(button_frame, text="Stop Reading", font=("Arial", 12), command=stop_speaking)
stop_button.grid(row=0, column=2, padx=5)

voice_button = tk.Button(button_frame, text="Voice Input", font=("Arial", 12), command=voice_input)
voice_button.grid(row=0, column=3, padx=5)

tk.Label(root, text="Result:", font=("Arial", 12)).pack(pady=5)
result_output = tk.Text(root, height=10, width=90, state=tk.DISABLED)
result_output.pack(pady=5)

root.mainloop()

