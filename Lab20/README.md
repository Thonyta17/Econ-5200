# Time Series Diagnostics & Advanced Decomposition

**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics  
**Author:** Thonyta Chhay  
**Date:** April 2026

---

## Objective

Diagnose and correct common misspecifications in time series decomposition and stationarity testing, then extend the analysis with multi-seasonal decomposition, block bootstrap uncertainty quantification, and regime-specific structural break detection applied to FRED macroeconomic data.

---

## Methodology

- **STL Decomposition (Fixed):** Identified that FRED retail sales (RSXFSN) exhibit multiplicative seasonality — seasonal amplitude scales with the trend level. Applied log-transformation prior to STL to satisfy the additive decomposition assumption, reducing the seasonal amplitude ratio from >3x to ~1.0x.

- **ADF Test (Fixed):** Corrected a misspecified Augmented Dickey-Fuller test on Real GDP (GDPC1) that used `regression='n'` (no constant, no trend), which omits the deterministic components of a trending series and inflates the test statistic. Re-specified with `regression='ct'` (constant + trend), yielding an unbiased unit root test.

- **MSTL Decomposition:** Applied Multiple STL (MSTL) to simulated hourly electricity demand data containing overlapping daily (period=24) and weekly (period=168) seasonal cycles. Verified successful component separation with residual standard deviation ≈ 15 MW, matching the true noise level.

- **Block Bootstrap for Trend Uncertainty:** Implemented a moving block bootstrap (block size = 8 quarters) on log Real GDP to produce pointwise 90% confidence bands around the STL trend. Block resampling preserves residual autocorrelation — critical for capturing business-cycle dynamics that i.i.d. bootstrap destroys.

- **Structural Break Detection:** Applied PELT (Pruned Exact Linear Time) changepoint detection to quarterly GDP growth rates. Ran ADF and KPSS stationarity tests on each detected regime segment to assess whether stationarity conclusions are stable across economic eras.

- **Production Module (`src/decompose.py`):** Packaged the full analytical pipeline into a reusable Python module with functions `run_stl()`, `run_mstl()`, `test_stationarity()`, `detect_breaks()`, and `block_bootstrap_trend()` — each with full type hints, docstrings, and error handling.

---

## Key Findings

| Series | Test | Result |
|--------|------|--------|
| Retail Sales (RSXFSN) | STL — additive assumption | **Violated** — log-transform required |
| Real GDP (GDPC1) levels | ADF (`regression='ct'`) + KPSS | **Non-stationary** — I(1) |
| Real GDP (GDPC1) first difference | ADF + KPSS | **Stationary** |
| GDP structural breaks (PELT, pen=10) | Changepoint detection | Breaks near **2008** (financial crisis) and **2020** (COVID shock) |

- GDP is confirmed I(1): non-stationary in levels, stationary in first differences — consistent with standard macroeconomic theory.
- Bootstrap confidence bands widen notably around the 2008–2009 recession and 2020 contraction, reflecting elevated trend uncertainty during high-volatility regimes.
- MSTL successfully isolates daily and weekly electricity demand cycles with near-zero cross-contamination.

---

## Repository Structure

```
Lab20/
├── lab-ch20-diagnostic.ipynb   # Main diagnostic lab notebook
├── app.py                      # Interactive decomposition explorer
├── src/
│   └── decompose.py            # Production time series module
└── README.md
```

---

## Dependencies

```
fredapi
statsmodels
ruptures
matplotlib
plotly
numpy
pandas
```
