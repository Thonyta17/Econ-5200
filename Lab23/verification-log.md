# Verification Log — Lab 23: FedSpeak 2.0
**Author:** Thonyta Chhay | **Course:** ECON 5200 | **Date:** April 2026

---

## Part 1: Diagnosis (No AI Used)

### Error 1 — Naive Tokenizer
**Bug:** `text.split()` splits on whitespace only — punctuation stays attached to tokens. `"rates,"` and `"rates"` become separate vocabulary entries; hyphens and contractions break incorrectly.  
**Fix:** Replace with `nltk.word_tokenize()` then `re.sub(r'[^a-z]', '', t)` to strip non-alpha chars.  
**Verification:** Zero non-alpha tokens in preprocessed text ✅

### Error 2 — Harvard GI Dictionary
**Bug:** Harvard GI classifies financial-neutral words (`capital`, `cost`, `liability`, `tax`, `debt`) as negative, inflating FOMC negative sentiment scores by ~30–50%.  
**Fix:** Switch to Loughran-McDonald (LM) word lists designed specifically for financial/economic text.  
**Verification:** LM false positive rate < 10% on FOMC first document ✅

### Error 3 — Bad TF-IDF Parameters
**Bug:** `min_df=1` keeps every typo; `max_df=1.0` keeps universal background words (`committee`, `meeting`) that appear in 100% of documents and carry zero discriminating power.  
**Fix:** Set `min_df=5, max_df=0.85, ngram_range=(1,2)` to filter noise and add bigrams.  
**Verification:** All top-15 TF-IDF terms appear in < 80% of documents ✅

---

## AI Expansion

### What AI Generated
- `src/fomc_sentiment.py` with `preprocess_fomc()`, `compute_lm_sentiment()`, `build_tfidf_matrix()`
- Embedding clustering comparison + AUC evaluation cells
- `README.md` and `verification-log.md`

### What I Verified
- `preprocess_fomc()` returns zero non-alpha tokens ✅
- `compute_lm_sentiment()` returns correct dict structure ✅
- `build_tfidf_matrix()` returns (sparse_matrix, feature_names, vectorizer) tuple ✅
- Silhouette score comparison between embeddings and TF-IDF runs ✅
- TimeSeriesSplit AUC evaluation runs without errors ✅
