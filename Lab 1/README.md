# MLOps Lab 1: Text Analysis & CI/CD

## 📌 Assignment Overview
The goal of this lab was to set up a professional Python development environment and implement **Continuous Integration (CI)** pipelines.

**Key Objectives:**
* Create a Python module with basic logic.
* Write unit tests using two different frameworks: **Pytest** and **Unittest**.
* Configure **GitHub Actions** to automatically run tests on every code push.
* Demonstrate proper project structure (`src` vs `test` folders).

---

## 📂 Project Solution: Text Analyzer
Instead of a simple calculator, I built a **Text Analysis Tool** to simulate a data engineering utility. This tool processes text strings and calculates key metrics.

### Features
1.  **Word Count:** Counts the number of words in a sentence.
2.  **Palindrome Check:** Checks if a word is the same forwards and backwards (e.g., "racecar").
3.  **Average Word Length:** Calculates the average number of characters per word.

### Directory Structure
```text
Lab01/
├── .github/workflows/   # CI/CD configurations
├── src/
│   ├── __init__.py
│   └── text_analyzer.py # Main logic
├── test/
│   ├── __init__.py
│   ├── test_pytest.py   # Pytest tests
│   └── test_unittest.py # Unittest tests
└── README.md

