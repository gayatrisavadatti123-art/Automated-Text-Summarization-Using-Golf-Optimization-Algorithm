import pyttsx3
import threading
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

speaking_thread = None

# ---------------------------
# Text-to-Speech
# ---------------------------
def speak_text(text):
    global speaking_thread

    # Stop previous speech
    if speaking_thread and speaking_thread.is_alive():
        engine.stop()
        speaking_thread.join()

    # Thread target
    def run():
        engine.say(text)
        engine.runAndWait()  # Blocking call inside thread

    speaking_thread = threading.Thread(target=run, daemon=True)
    speaking_thread.start()

def stop_speaking():
    engine.stop()

# ---------------------------
# Voice Input
# ---------------------------
def listen_and_get_text(status_label=None, timeout=10, phrase_time_limit=60):
    r = sr.Recognizer()
    mic = sr.Microphone()
    text_result = None

    if status_label:
        status_label.config(text="🎙 Listening... Speak now")

    def listen():
        nonlocal text_result
        with mic as source:
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text_result = r.recognize_google(audio)
                if status_label:
                    status_label.config(text="✅ Voice captured successfully!")
            except sr.WaitTimeoutError:
                if status_label:
                    status_label.config(text="❌ No speech detected.")
            except Exception as e:
                if status_label:
                    status_label.config(text=f"❌ {str(e)}")

    thread = threading.Thread(target=listen, daemon=True)
    thread.start()
    thread.join()
    return text_result

