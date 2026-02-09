# test/test_unittest.py
import unittest
from src.text_analyzer import count_words, is_palindrome, get_avg_word_length, analyze_text

class TestTextAnalyzer(unittest.TestCase):
    
    def test_count_words(self):
        self.assertEqual(count_words("data engineering"), 2)
        self.assertEqual(count_words(""), 0)

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("level"))
        self.assertFalse(is_palindrome("python"))

    def test_avg_word_length(self):
        self.assertEqual(get_avg_word_length("a bc"), 1.5)

    def test_analyze_text(self):
        result = analyze_text("level")
        self.assertEqual(result["word_count"], 1)
        self.assertTrue(result["is_palindrome"])

if __name__ == '__main__':
    unittest.main()