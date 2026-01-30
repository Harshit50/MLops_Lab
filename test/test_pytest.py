# test/test_pytest.py
import pytest
from src.text_analyzer import count_words, is_palindrome, get_avg_word_length, analyze_text

def test_count_words():
    assert count_words("hello world") == 2
    assert count_words("") == 0

def test_is_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("hello") == False
    assert is_palindrome("Race car") == True 

def test_avg_word_length():
    assert get_avg_word_length("hi you") == 2.5 
    assert get_avg_word_length("") == 0

def test_analyze_text():
    result = analyze_text("madam")
    assert result["word_count"] == 1
    assert result["is_palindrome"] == True