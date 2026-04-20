# Unsupervised Learning — Clustering & Dimensionality Reduction

**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics  
**Author:** Thonyta Chhay  
**Date:** April 2026

---

## Objective

Diagnose and correct a broken K-Means clustering pipeline applied to World Bank development indicators, extend the analysis to customer segmentation using synthetic behavioral data, and deliver a production-grade clustering module with K evaluation and PCA visualization.

---

## Methodology

- **Pipeline Diagnosis (4 Errors Fixed):**
  - *Missing standardization:* Raw features fed directly to K-Means; GDP/capita dominated distance. Fixed with `StandardScaler` applied before clustering.
  - *Wrong parameter name:* `k=4` raises `TypeError`; scikit-learn uses `n_clusters=4`.
  - *PCA before scaling:* PCA on raw data gives PC1 ~90% variance (all GDP). Fixed by standardizing first — PCA on scaled data yields 35–50% for PC1.
  - *Missing `random_state`:* Non-reproducible cluster assignments across runs. Fixed with `random_state=42`.

- **Customer Segmentation:** Applied corrected pipeline to 2,000 synthetic customers (6 behavioral features). Compared PCA vs UMAP for 2D visualization of cluster structure.

- **Clustering Module (`src/clustering_utils.py`):** Built `run_kmeans_pipeline()`, `evaluate_k_range()`, and `plot_pca_clusters()` for model-agnostic, reusable unsupervised learning workflows.

- **Hierarchical Clustering:** Fitted `AgglomerativeClustering(linkage='ward')` on WDI data, plotted dendrogram, and cross-tabulated assignments against K-Means to assess agreement.

---

## Key Findings

| Analysis | Result |
|----------|--------|
| PC1 variance (raw data) | ~90% — dominated by GDP per capita |
| PC1 variance (scaled data) | ~35–45% — balanced across features |
| Silhouette score (K=4, WDI) | 0.15–0.40 — moderate cluster separation |
| UMAP vs PCA | UMAP reveals tighter, more separated clusters for non-linear structure |
| Hierarchical vs K-Means | Ward linkage largely agrees with K-Means assignments |

---

## Repository Structure

```
Lab22/
├── notebooks/
│   └── lab-ch22-diagnostic.ipynb
├── src/
│   └── clustering_utils.py
├── figures/
├── README.md
├── requirements.txt
└── verification-log.md
```

---

## How to Reproduce

```bash
pip install -r requirements.txt
jupyter notebook notebooks/lab-ch22-diagnostic.ipynb
```
