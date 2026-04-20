# Causal ML — DML and Causal Forests for Policy Evaluation

**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics  
**Author:** Thonyta Chhay  
**Date:** April 2026

---

## Objective

Diagnose and correct a broken Double Machine Learning (DML) implementation, estimate the causal effect of 401(k) eligibility on net financial assets using the DoubleML package, and extend the analysis with Causal Forests to identify individual-level heterogeneous treatment effects.

---

## Methodology

- **Manual DML Diagnosis (3 Bugs Fixed):**
  - *Data leakage:* Training and predicting on the same fold violates cross-fitting, producing biased estimates. Fixed by training on fold A and predicting on fold B.
  - *Missing treatment residualization:* Only outcome Y was residualized; treatment D was passed raw. Fixed by fitting a separate nuisance model for D and computing D-residuals.
  - *Wrong estimator formula:* Used `np.mean(Ṽ · Ỹ)` instead of the IV-style ratio `Σ(Ṽ · Ỹ) / Σ(Ṽ · D)`. Fixed to recover ATE within 1.0 of the true value (5.0) on the simulated DGP.

- **DoubleML PLR (401k):** Estimated ATE of 401(k) eligibility (`e401`) on net financial assets (`net_tfa`) using `DoubleMLPLR` with Random Forest nuisance learners and 5-fold cross-fitting. Ran sensitivity analysis with `cf_y=0.03, cf_d=0.03`.

- **Causal Forests (EconML):** Fitted `CausalForestDML` to estimate individual-level CATEs. Identified high-response subgroup (CATE ≥ 75th percentile) and compared to low-response subgroup on income, age, education.

- **Heterogeneity Comparison:** Cross-tabulated Causal Forest CATEs against income quartile subgroup DML. Violin plots reveal within-quartile heterogeneity that coarse subgroup analysis misses.

---

## Key Findings

| Analysis | Result |
|----------|--------|
| Simulated DGP (TRUE_ATE=5.0) | Fixed DML recovers ATE within ±1.0 ✅ |
| 401(k) DML ATE | ~$7,000–$12,000 net financial assets (p < 0.05) |
| Sensitivity robustness value | Positive — estimate survives moderate confounding |
| Mean CATE (Causal Forest) | Close to DML ATE, with wide individual variation |
| Within-quartile CATE std | Large — income quartile alone misses fine heterogeneity |

---

## Repository Structure

```
Lab24/
├── notebooks/
│   └── lab-ch24-diagnostic.ipynb
├── figures/
├── README.md
└── requirements.txt
```

---

## How to Reproduce

```bash
pip install -r requirements.txt
jupyter notebook notebooks/lab-ch24-diagnostic.ipynb
```
