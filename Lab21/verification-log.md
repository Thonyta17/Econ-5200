# Verification Log — Lab 21: Time Series Forecasting
**Author:** Thonyta Chhay | **Course:** ECON 5200 | **Date:** April 2026

---

## Part 1: Diagnosis (No AI Used)

### Error 1 — Stationarity
**Bug:** `d=0` used in ARIMA on raw CPI levels, which are non-stationary (ADF p > 0.05).
**Fix:** Changed to `d=1` (first differencing).
**Verification:** ADF on diff(CPI) p < 0.05 ✅

### Error 2 — Seasonality
**Bug:** Plain `ARIMA(2,1,1)` ignores CPI's monthly seasonal cycle. ACF of residuals shows spikes at lags 12 and 24.
**Fix:** Switched to `SARIMAX` with `seasonal_order=(1,1,1,12)`.
**Verification:** Residual ACF spikes at lags 12/24 disappear after SARIMA ✅

### Error 3 — Missing Diagnostic
**Bug:** Pipeline jumped to forecasting without Ljung-Box test. Autocorrelated residuals produce invalid CIs.
**Fix:** Added `acorr_ljungbox(resid, lags=[12, 24])` before forecasting.
**Verification:** Ljung-Box p-values > 0.05 at lags 12 and 24 ✅

---

## AI Expansion

### What AI Generated
- `src/forecast_evaluation.py` with `compute_mase()` and `backtest_expanding_window()`
- Block bootstrap forecast interval implementation
- `README.md` and `verification-log.md`

### What I Verified
- `compute_mase()` returns < 1 for SARIMA vs naive seasonal benchmark ✅
- `backtest_expanding_window()` returns correct DataFrame structure ✅
- GARCH α + β < 1 (variance stationarity satisfied) ✅
- Block bootstrap CIs wider than ARIMA Gaussian CIs during volatile periods ✅
