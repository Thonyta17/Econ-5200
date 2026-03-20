# Forecasting Architecture and the Bias-Variance Tradeoff

## Objective
Diagnose the empirical consequences of model overparameterization by engineering a high-variance polynomial regressor on live NVIDIA revenue data, quantifying its out-of-sample failure, and validating the operational necessity of cross-validated model selection.

---

## Data
**NVIDIA Quarterly Financials (2024–2026)** — Total Corporate Revenue.
A compact but high-signal time series reflecting one of the most volatile and consequential growth trajectories in modern semiconductor markets.

---

## Methodology

- **Baseline Modeling** — Fit a standard linear regression on NVIDIA quarterly revenue to establish an interpretable, low-variance benchmark.
- **Polynomial Feature Expansion** — Engineered a 7th-degree polynomial transformation of the time index to aggressively maximize in-sample fit, deliberately inducing high model complexity.
- **Overfitting Diagnosis** — Compared training MSE across polynomial degrees to expose the near-zero training error achieved by the high-degree model — a classic symptom of variance domination over bias.
- **Out-of-Sample Stress Test** — Extrapolated the 7th-degree model one quarter forward to simulate a real forecasting deployment; recorded the resulting prediction collapse as the model hallucinated economically implausible revenue figures.
- **K-Fold Cross-Validation** — Applied K-Fold CV to both models to surface the *true* generalization error obscured by in-sample metrics, quantifying the operational risk of deploying an overfit forecaster in production.
- **Variance Decomposition & Regularization Case** — Used empirical CV error as evidence for the necessity of algorithmic regularization (e.g., Ridge/Lasso) to suppress variance without sacrificing structural fit.

**Stack:** Python · pandas · NumPy · scikit-learn (`PolynomialFeatures`, `LinearRegression`, `cross_val_score`) · Matplotlib

---

## Key Findings

A 7th-degree polynomial expansion drove training MSE toward zero — a superficially strong result that masked catastrophic model fragility. Upon extrapolation to an unseen quarter, the model produced hallucinated revenue projections with no economic grounding, exposing the sharp divergence between memorization and generalization.

K-Fold Cross-Validation revealed a true operational error several orders of magnitude larger than the training error, providing hard quantitative evidence that low training loss is not a valid proxy for forecast reliability. The experiment confirms a foundational principle of applied econometrics: **unconstrained model complexity is an operational liability**, and regularization is not optional — it is a structural requirement for any production-grade forecasting architecture.

---

*Part of an ongoing econometrics lab series focused on applied machine learning for financial and macroeconomic forecasting.*
