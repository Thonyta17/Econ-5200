# FedSpeak 2.0 — NLP Pipeline for Central Bank Communications

**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics  
**Author:** Thonyta Chhay  
**Date:** April 2026

---

## Objective

Diagnose and correct a broken NLP pipeline for FOMC minutes analysis, extend with sentence-transformer embeddings, and deliver a production-grade text analysis module for central bank communication research.

---

## Methodology

- **Pipeline Diagnosis (3 Errors Fixed):**
  - *Naive tokenizer:* `text.split()` leaves punctuation attached; `"rates,"` and `"rates"` become different features. Fixed with `nltk.word_tokenize()` + `re.sub(r'[^a-z]', '', t)`.
  - *Wrong sentiment dictionary:* Harvard GI classifies `capital`, `cost`, `liability`, `tax` as negative — false positive rate ~40% in FOMC text. Fixed by switching to Loughran-McDonald (LM) dictionary designed for financial text.
  - *Bad TF-IDF parameters:* `min_df=1, max_df=1.0` includes OCR typos and universal background words. Fixed with `min_df=5, max_df=0.85, ngram_range=(1,2)` to retain discriminating bigrams like `"interest rate"`.

- **Sentence-Transformer Embeddings:** Encoded FOMC documents with `all-MiniLM-L6-v2` (384-dimensional dense vectors). Compared clustering quality (silhouette score) against TF-IDF+SVD representations.

- **Predictive Evaluation:** Used `TimeSeriesSplit` (5 folds) to compare AUC-ROC of TF-IDF vs embedding-based logistic regression for predicting Fed tightening cycles.

- **Text Analysis Module (`src/fomc_sentiment.py`):** Built `preprocess_fomc()`, `compute_lm_sentiment()`, and `build_tfidf_matrix()` for reusable FOMC NLP pipelines.

---

## Key Findings

| Analysis | Result |
|----------|--------|
| Fix 1: Tokenization | Zero non-alpha tokens after `word_tokenize` + regex strip |
| Fix 2: LM vs GI | LM false positive rate < 10% vs ~40% for GI on FOMC text |
| Fix 3: TF-IDF | Top terms all below 80% document frequency after filtering |
| Clustering (silhouette) | Embeddings tend to outperform TF-IDF on semantic coherence |
| Prediction (AUC) | Both representations predict tightening cycles above chance |

---

## Repository Structure

```
Lab23/
├── notebooks/
│   └── lab-ch23-diagnostic.ipynb
├── src/
│   └── fomc_sentiment.py
├── figures/
├── README.md
└── requirements.txt
```

---

## How to Reproduce

```bash
pip install -r requirements.txt
jupyter notebook notebooks/lab-ch23-diagnostic.ipynb
```
