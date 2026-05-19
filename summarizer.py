# summarizer.py
import nltk
from nltk.tokenize import sent_tokenize

# Download punkt if not present (quiet)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

def generate_summary(text: str, max_sentences: int = 3) -> str:
    """
    Simple extractive summary: choose up to `max_sentences` sentences (first ones).
    Keeps order (first N sentences). This matches requirement: short 2-3 sentence summaries.
    """
    if not text or not text.strip():
        return ""

    sents = sent_tokenize(text.strip())
    if len(sents) <= max_sentences:
        return " ".join(sents)

    # A conservative approach: take the first max_sentences sentences
    return " ".join(sents[:max_sentences])
