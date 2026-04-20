# Verification Log — Lab 22: Clustering Economies
**Author:** Thonyta Chhay | **Course:** ECON 5200 | **Date:** April 2026

---

## Part 1: Diagnosis (No AI Used)

### Error 1 — Missing Standardization
**Bug:** K-Means applied to raw features. GDP/capita (300–120,000) dominates Euclidean distance; Gini (25–65) contributes almost nothing.  
**Fix:** Applied `StandardScaler` before `KMeans.fit()`.  
**Verification:** Standardized means ≈ 0, std ≈ 1 ✅

### Error 2 — Wrong Parameter Name
**Bug:** `KMeans(k=4)` raises `TypeError` — scikit-learn uses `n_clusters`, not `k`.  
**Fix:** Changed to `KMeans(n_clusters=4)`.  
**Verification:** Model fits without error ✅

### Error 3 — PCA Before Scaling
**Bug:** PCA on raw data; PC1 explains ~90% of variance (almost entirely GDP per capita).  
**Fix:** Standardize first, then apply PCA to scaled features.  
**Verification:** PC1 explains 35–50% of variance on scaled data ✅

### Error 4 — Missing `random_state`
**Bug:** Without `random_state`, K-Means re-initializes randomly — different cluster assignments each run.  
**Fix:** Set `random_state=42` in all `KMeans` calls.  
**Verification:** Identical cluster sizes across repeated runs ✅

---

## AI Expansion

### What AI Generated
- `src/clustering_utils.py` with `run_kmeans_pipeline()`, `evaluate_k_range()`, `plot_pca_clusters()`
- Hierarchical clustering + dendrogram challenge cell
- `README.md` and `verification-log.md`

### What I Verified
- `run_kmeans_pipeline()` returns correct dict structure with silhouette score ✅
- `evaluate_k_range()` returns DataFrame with k, wcss, silhouette columns ✅
- Silhouette score for K=4 on WDI data is in range 0.15–0.40 ✅
- UMAP gives tighter visual separation than PCA for customer segments ✅
- Agglomerative (Ward) and K-Means cluster assignments largely agree ✅
