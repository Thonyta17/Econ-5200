# Verification Log — Lab 20: Time Series Diagnostics
**Author:** Thonyta Chhay | **Course:** ECON 5200 | **Date:** April 2026

---

## Parts 1–2: Diagnosis (No AI Used)

### Part 1 — STL on Multiplicative Data
**Bug found:** `STL()` applied directly to raw retail sales (RSXFSN), which has multiplicative seasonality. Additive STL requires constant seasonal amplitude, but the raw series shows amplitude growing proportionally with the trend level.

**Fix applied:** Log-transformed the series before STL: `log_retail = np.log(retail)`.

**Verification checkpoint:**
- Seasonal amplitude ratio (latest/earliest): **~1.0x** ✅ (target: 0.7–1.3)

---

### Part 2 — Misspecified ADF Test
**Bug found:** `adfuller(gdp, regression='n')` omits both constant and trend from the ADF regression. GDP has a clear upward trend and non-zero mean — omitting these inflates the test statistic and falsely rejects the unit root.

**Fix applied:** Changed to `regression='ct'` (constant + trend).

**Verification checkpoint:**
- ADF p-value with `regression='ct'`: **0.9617** ✅ (target: > 0.05)
- KPSS p-value: **0.0100** ✅ (target: < 0.05)
- 2×2 verdict: **NON-STATIONARY** ✅

---

## AI Expansion — P.R.I.M.E. Prompt

### Prompt Used
```
[Prep] Act as an expert Python Data Scientist specializing in time series
analysis, FRED API, and production ML systems.

[Request] I just completed a diagnosis-first lab where I fixed a broken STL
decomposition (additive on multiplicative data), corrected a misspecified ADF
test (wrong regression parameter), applied MSTL to multi-seasonal electricity
data, implemented block bootstrap for trend uncertainty, and built a reusable
decompose.py module. Now I need TWO artifacts:

1. An extended src/decompose.py module adding run_mstl() and
   block_bootstrap_trend() with type hints and error handling.
2. An interactive app that lets users enter a FRED series ID, select
   decomposition method, adjust parameters, and see decomposition panels,
   stationarity tests, structural breaks, and bootstrap CIs.

[Iterate] Use fredapi, statsmodels, ruptures, matplotlib. Handle missing data
and frequency detection automatically.

[Mechanism Check] Add inline comments explaining why block bootstrap preserves
autocorrelation, how MSTL iterates, and why PELT penalty controls bias-variance.

[Evaluate] Explain what the app reveals about parameter sensitivity.
```

### What AI Generated
- Extended `src/decompose.py` with `run_mstl()` and `block_bootstrap_trend()`
- `app.py` — interactive decomposition explorer (matplotlib-based, runs in Jupyter)

### What I Changed / Verified
- Removed Streamlit dependency from `app.py` — replaced with pure matplotlib so it runs directly in the notebook without a web server
- Verified `run_mstl()` returns correct `.trend`, `.seasonal`, `.resid` attributes
- Verified `block_bootstrap_trend()` produces wider CI at 2008Q4 than 2019Q4 ✅
- Verified `test_stationarity(gdp)` returns `'non-stationary'` ✅
- Verified `test_stationarity(gdp.diff().dropna())` returns `'stationary'` ✅
- Verified `detect_breaks()` returns 2–5 breaks including near 2008 and 2020 ✅

### Human Judgment Applied
- Chose `block_size=8` (2 years) over smaller values to preserve business-cycle autocorrelation
- Chose `penalty=10` as default after testing — low enough to catch 2008/2020 breaks, high enough to avoid overfitting noise
- Chose matplotlib over Streamlit for portability within the notebook environment
