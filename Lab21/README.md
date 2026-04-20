# Time Series Forecasting — ARIMA, GARCH & Bootstrap

**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics  
**Author:** Thonyta Chhay  
**Date:** April 2026

---

## Objective

Diagnose and correct a broken ARIMA forecasting pipeline applied to FRED CPI data, extend the analysis with GARCH volatility modeling on S&P 500 returns, and deliver a production-grade forecast evaluation module with expanding-window backtesting and block bootstrap forecast intervals.

---

## Methodology

- **ARIMA Diagnosis (3 Errors Fixed):**
  - *Stationarity:* Original model used `d=0` on non-stationary CPI. Fixed by applying first differencing (`d=1`); ADF confirms stationarity of diff(CPI) with p < 0.05.
  - *Seasonality:* Plain ARIMA ignored CPI's monthly seasonal cycle. Fixed by switching to `SARIMAX` with `seasonal_order=(1,1,1,12)`; residual ACF spikes at lags 12 and 24 disappear.
  - *Diagnostics:* Pipeline skipped the Ljung-Box test before forecasting. Fixed by verifying all Ljung-Box p-values > 0.05 before trusting confidence intervals.

- **GARCH(1,1) on S&P 500:** Modeled conditional volatility of daily log returns (2000–2024). Verified variance stationarity (α + β < 1) and annotated crisis regimes (Sep 11, Lehman, COVID, 2022 Bear Market).

- **Forecast Evaluation Module (`src/forecast_evaluation.py`):** Built reusable functions `compute_mase()` and `backtest_expanding_window()` for model-agnostic forecast evaluation with expanding training windows.

- **Block Bootstrap Forecast Intervals:** Implemented distribution-free 95% forecast intervals by resampling overlapping residual blocks, preserving autocorrelation and heteroskedasticity structure absent from standard ARIMA Gaussian CIs.

---

## Key Findings

| Analysis | Result |
|----------|--------|
| CPI (CPIAUCNS) stationarity | Non-stationary in levels, stationary after first difference |
| SARIMA Ljung-Box (lags 12, 24) | p > 0.05 — residuals are white noise ✅ |
| GARCH α + β | ~0.98 — high volatility persistence |
| GARCH volatility half-life | ~35 days — shocks decay slowly |
| Peak conditional volatility | March 2020 (COVID crash) |

---

## Repository Structure

```
Lab21/
├── notebooks/
│   └── lab-ch21-diagnostic.ipynb
├── src/
│   └── forecast_evaluation.py
├── figures/
├── README.md
└── requirements.txt
```

---

## How to Reproduce

```bash
pip install -r requirements.txt
jupyter notebook notebooks/lab-ch21-diagnostic.ipynb
```

Set your FRED API key in cell 1 before running.
