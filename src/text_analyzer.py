

def count_words(text):
    """Returns the number of words in the string."""
    if not text:
        return 0
    return len(text.split())

def is_palindrome(text):
    """Returns True if the text is the same forwards and backwards (case-insensitive)."""
    if not text:
        return False
    clean_text = text.replace(" ", "").lower() # Remove spaces and lowercase for accurate check
    return clean_text == clean_text[::-1]

def get_avg_word_length(text):
    """Calculates the average length of words in the text."""
    words = text.split()
    if not words:
        return 0
    total_chars = sum(len(word) for word in words)
    return total_chars / len(words)

def analyze_text(text):
    """Combines metrics: counts words and checks palindrome status."""
    return {
        "word_count": count_words(text),
        "is_palindrome": is_palindrome(text),
        "avg_length": get_avg_word_length(text)
    }

