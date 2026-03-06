# Assignment 3: The Causal Architecture
### Econ 5200 | Module 3: Bootstrapping, Permutation & Causal Inference
**Role:** Senior Data Economist | **Platform:** Google Colab

---

## Overview

This project tackles three core statistical challenges faced by SwiftCart Logistics using non-parametric and causal inference methods. Rather than relying on fragile parametric assumptions, the analysis uses heavy computation to build empirical evidence and isolate pure causality from spurious correlation.

---

## Phases

### Phase 1: Bootstrapping Non-Parametric Uncertainty
- Simulated a zero-inflated, right-skewed tip distribution of 250 driver tips (100 zeros + 150 exponential draws)
- Built a manual bootstrap engine with 10,000 resamples to estimate the median and 95% Confidence Interval
- **Key Finding:** Bootstrap CI (0.2817, 1.2990) is asymmetric around the median (0.7553), reflecting the true skewness of the data — unlike a parametric CI which assumes normality and is always symmetric

### Phase 2: Falsification in Logistics A/B Testing
- Generated synthetic A/B test data for 1,000 deliveries comparing Control (Normal) vs Treatment (Log-Normal) routing algorithms
- Built a manual Permutation Test with 5,000 iterations to compute an exact empirical p-value
- **Key Finding:** The permutation test provides a valid non-parametric alternative to the t-test, which is invalidated by the heavy skew and outliers in the treatment group

### Phase 3: Causal Control and Mitigation of Selection Bias
- Loaded real `swiftcart_loyalty.csv` dataset with pre-treatment covariates and post-treatment spending
- Calculated Naive SDO and applied Propensity Score Matching (PSM) using Logistic Regression + Nearest Neighbors
- **Key Finding:**
  - Naive SDO: **17.57** (biased — inflated by selection bias)
  - Causal ATT: **9.91** (true causal effect after matching)
  - Bias eliminated: **7.66** — proving the marketing team's claim overstates SwiftPass's true impact by nearly 44%

### Phase 4: AI Expansion — Love Plot Visualization
- Used AI (Claude) to generate a Love Plot showing Standardized Mean Differences (SMDs) before and after PSM
- **Key Finding:** All matched covariates fell within the ±0.1 SMD threshold after matching, confirming successful covariate balance and bias mitigation

---

## Libraries Used
- `numpy` — Bootstrap and Permutation engines
- `pandas` — Data loading and manipulation
- `matplotlib` / `seaborn` — Visualization
- `sklearn` — Logistic Regression, Nearest Neighbors (PSM)
- `scipy.stats` — Parametric CI comparison

---

## Key Results Summary

| Analysis | Result |
|---|---|
| Bootstrap 95% CI | (0.2817, 1.2990) |
| Median Estimate | 0.7553 |
| Naive SDO | 17.57 |
| Causal ATT | 9.91 |
| Selection Bias Eliminated | 7.66 |

---

## Files
- `Econ_5200_Assignment_3_Causal.ipynb` — Main notebook
- `swiftcart_loyalty.csv` — Loyalty program dataset
