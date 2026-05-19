def summarize_text(text):
    """
    Dummy GOA-based summarization.
    For demo: returns first 3 and last 2 sentences.
    Replace with real GOA logic later.
    """
    sentences = text.split(". ")
    if len(sentences) <= 5:
        return " ".join(sentences)
    return ". ".join(sentences[:3] + sentences[-2:])



