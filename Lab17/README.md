# NY Fed Yield Curve Recession Model Replication

## Objective
Replicate the Federal Reserve Bank of New York's yield curve recession forecasting methodology by fitting a logistic regression on FRED macroeconomic data to predict NBER-defined recessions 12 months ahead, while exposing the structural failure of the Linear Probability Model as a probabilistic classifier on real financial data.

---

## Data
**Federal Reserve Economic Data (FRED), 1970–Present** — retrieved programmatically via the `fredapi` Python library.

| Series | Description | Frequency |
|---|---|---|
| `T10Y3M` | 10-Year minus 3-Month Treasury yield spread | Daily → resampled to monthly |
| `USREC` | NBER recession indicator (binary) | Monthly |

The yield spread series was lagged 12 months to align with the model's forward-looking forecasting horizon, producing a clean binary classification setup: predict whether the economy will be in recession one year from a given spread observation.

---

## Methodology

- **Data Acquisition & Pipeline** — Pulled `T10Y3M` and `USREC` directly from FRED via `fredapi`, resampled the daily yield spread to monthly frequency, applied a 12-month forward lag to the recession indicator, and merged on a common monthly time index spanning 1970 to present.
- **Linear Probability Model Benchmark** — Estimated OLS (`LinearRegression`) on the binary recession outcome to establish a diagnostic baseline, explicitly documenting the model's production of predicted probabilities below 0 and above 1 — a logical impossibility that disqualifies the LPM as a credible recession probability forecaster.
- **Logistic Regression (NY Fed Replication)** — Fitted a logistic regression (`LogisticRegression`) on the lagged yield spread, replicating the functional form of the NY Fed's published methodology and recovering the characteristic S-curve mapping from spread levels to recession probabilities.
- **Odds Ratio Estimation with Confidence Intervals** — Re-estimated the model in `statsmodels` (`Logit`) to extract the yield spread coefficient, exponentiated to recover the odds ratio, and constructed 95% confidence intervals to formally characterize the precision of the spread's predictive signal.
- **Time-Aware Validation** — Applied `TimeSeriesSplit` for cross-validation to respect the temporal ordering of macroeconomic data and prevent lookahead bias — a critical methodological discipline absent from naive cross-validation on financial time series.
- **Recession Probability Time Series** — Generated the full historical predicted probability series from 1970 to present, overlaying NBER recession bands to evaluate model calibration across multiple business cycles.
- **2022–2024 Inversion Analysis** — Isolated and examined the contested yield curve inversion episode, during which the model sustained elevated recession probability forecasts over an extended horizon without a subsequent NBER recession materialization.

**Stack:** Python · pandas · NumPy · scikit-learn (`LogisticRegression`, `LinearRegression`, `TimeSeriesSplit`) · statsmodels (`Logit`) · matplotlib · fredapi

---

## Key Findings

The Linear Probability Model produced predicted recession probabilities outside the unit interval on real FRED data — a textbook failure that is frequently cited in econometrics pedagogy but rarely demonstrated empirically. This result concretely motivates the logistic specification: the S-curve maps any yield spread level to a well-defined probability bounded between 0 and 1, making it suitable for operational risk communication.

The fitted logistic model closely replicated the NY Fed's published recession probability series, validating the replication methodology. The extracted odds ratio — estimated with 95% confidence intervals via `statsmodels` — confirmed a statistically significant negative relationship between the yield spread and 12-month-ahead recession probability: yield curve inversion is a meaningful, if imperfect, leading indicator.

The 2022–2024 inversion episode represents the model's most prominent recent stress test. The yield spread inverted sharply and persistently, driving predicted recession probabilities to historically elevated levels. No NBER recession materialized within the forecast window. This outcome does not invalidate the model — it surfaces a fundamental limitation of any reduced-form leading indicator: **elevated probabilistic risk and realized economic contraction are not equivalent**. The model correctly identified a period of structural vulnerability; whether that vulnerability translated into recession was contingent on factors outside the yield spread's predictive scope, including extraordinary fiscal intervention and labor market resilience.

---

*Part of an ongoing econometrics lab series focused on applied machine learning for financial and macroeconomic forecasting.*
