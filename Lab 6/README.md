# MLOps Lab 06 — Data Labeling with Snorkel

## Overview

This lab teaches **programmatic data labeling** using **Snorkel** — a framework for building training datasets without manual annotation. Instead of hand-labeling thousands of tweets, you write heuristic functions that Snorkel combines to produce high-quality labels automatically.

### What You'll Learn

| Notebook | Concept | Description |
|---|---|---|
| `01_disaster_tweets_labeling.ipynb` | **Labeling Functions** | Write heuristic rules to programmatically label tweets as real disasters or not |
| `02_disaster_tweets_augmentation.ipynb` | **Transformation Functions** | Augment labeled data by applying text transformations (synonym swap, URL removal) |
| `03_disaster_tweets_slicing.ipynb` | **Slicing Functions** | Identify critical data subsets (retweets, tweets with links) and analyze each slice |

**Dataset:** Disaster Tweets — 7,613 tweets labeled as real disaster (`1`) or not (`0`), sourced from a Kaggle NLP competition.

---

## Prerequisites

- Python 3.9+
- Jupyter Lab installed

---

## Setup Instructions

1. **Navigate to the lab directory:**
   ```bash
   cd "Lab 6"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv snorkel_env
   ```

3. **Activate the environment:**
   ```bash
   # macOS / Linux
   source snorkel_env/bin/activate

   # Windows
   snorkel_env\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Link the environment to Jupyter:**
   ```bash
   python -m ipykernel install --user --name=snorkel_env
   ```

6. **Launch Jupyter Lab:**
   ```bash
   jupyter-lab
   ```
   Select `snorkel_env` as the kernel for each notebook.

> **Note:** The dataset (`disaster_tweets.csv`) is auto-downloaded on first run via `utils.py`. No manual download needed.

---

## Running the Lab

### Notebook 1: `01_disaster_tweets_labeling.ipynb`

Covers the full Snorkel labeling pipeline:
- Load unlabeled disaster tweet data using `load_disaster_dataset()`
- Define label constants: `ABSTAIN = -1`, `NOT_DISASTER = 0`, `REAL_DISASTER = 1`
- Write **3 labeling functions** using keyword heuristics:
  - `lf_emergency_keywords` — flags tweets with words like "earthquake", "wildfire", "evacuate"
  - `lf_metaphorical` — flags non-disaster tweets with words like "movie", "song", "literally"
  - `lf_first_responders` — flags tweets mentioning "police", "ambulance", "paramedic"
- Apply LFs with `PandasLFApplier` to produce a noisy label matrix
- Train `LabelModel` (500 epochs) to combine noisy labels intelligently
- Predict final probabilistic labels with `tie_break_policy="abstain"`

### Notebook 2: `02_disaster_tweets_augmentation.ipynb`

Covers data augmentation with transformation functions:
- Write **2 transformation functions**:
  - `tf_swap_disaster_synonyms` — replaces "fire" → "blaze", "police" → "cops"
  - `tf_remove_urls` — strips HTTP URLs from tweet text
- Apply TFs using `RandomPolicy` with `n_per_original=2` (3x dataset expansion)
- Compare dataset size before and after augmentation (e.g., 6,090 → 18,270 rows)

### Notebook 3: `03_disaster_tweets_slicing.ipynb`

Covers data slicing for targeted evaluation:
- Write **2 slicing functions** to identify critical subsets:
  - `slice_is_retweet` — tweets starting with "RT" or containing " RT "
  - `slice_has_link` — tweets containing "http"
- Apply SFs with `PandasSFApplier` on the test set
- Print a slice analysis summary (e.g., 14 retweets, 396 tweets with links out of 762 total)
- Inspect the actual text and labels of isolated slices using `display()`

---

## Project Structure

```
Lab 6/
├── README.md
├── requirements.txt
├── utils.py                                # load_disaster_dataset() helper
├── data/
│   └── disaster_tweets.csv                 # Auto-downloaded on first run
├── 01_disaster_tweets_labeling.ipynb       # Notebook 1: Labeling Functions
├── 02_disaster_tweets_augmentation.ipynb   # Notebook 2: Transformation Functions
└── 03_disaster_tweets_slicing.ipynb        # Notebook 3: Slicing Functions
```

---

## Key Concepts

| Term | Description |
|---|---|
| **Labeling Function (LF)** | A heuristic rule that assigns a label or `ABSTAIN` to a data point |
| **LabelModel** | Snorkel's generative model that learns LF accuracies and combines them |
| **Transformation Function (TF)** | A rule that modifies a data point to create augmented training examples |
| **Slicing Function (SF)** | A rule that identifies a specific subset of data for targeted analysis |
| **Tie-break Policy** | Strategy for handling conflicting LF votes — `"abstain"` discards ties |

---

