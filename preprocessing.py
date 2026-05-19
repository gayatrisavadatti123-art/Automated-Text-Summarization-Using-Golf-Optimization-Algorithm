import re

def preprocess_text(text):
    """Basic cleaning of input text."""
    return " ".join(text.strip().split())


def is_random_text(text):
    """Detect gibberish/random text."""
    if len(text) < 10:
        return True
    if re.fullmatch(r"[A-Za-z0-9@#$%^&*()_+=-]+", text):  # Only junk chars
        return True
    return False


def is_probably_address(text):
    """
    Detects if input is an address (strict check).
    Triggers only if input has numbers + keywords like road/street/city/state/pincode.
    """
    address_keywords = ["road", "street", "st", "ave", "block", "lane", "nagar", "city", "state", "pincode", "india"]
    if any(word in text.lower() for word in address_keywords) and re.search(r"\d", text):
        return True
    return False














