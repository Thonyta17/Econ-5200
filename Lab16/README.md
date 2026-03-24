# High-Dimensional GDP Growth Forecasting with Regularized Regression

## Objective
Forecast 5-year average GDP per capita growth across 120+ countries using a high-dimensional World Bank indicator set, exposing the structural failure of OLS under feature abundance and benchmarking the predictive and interpretive gains from Ridge and Lasso regularization with cross-validated penalty selection.

---

## Data
**World Bank World Development Indicators (WDI), 2013–2019** — retrieved programmatically via the `wbgapi` Python API.

35+ indicators spanning eight macroeconomic and institutional dimensions:

| Domain | Representative Indicators |
|---|---|
| Macroeconomics | Inflation, fiscal balance, current account |
| Trade | Export/import ratios, trade openness |
| Education | Enrollment rates, human capital index |
| Infrastructure | Internet penetration, energy access |
| Health | Mortality rates, health expenditure |
| Finance | Credit to private sector, banking depth |
| Natural Resources | Resource rents as % of GDP |
| Governance | Rule of law, regulatory quality |

Cross-sectional sample: **120+ countries**. Target variable: **5-year average GDP per capita growth rate**.

---

## Methodology

- **Data Acquisition & Pipeline** — Pulled multi-domain WDI indicators via `wbgapi`, aggregated to country-level cross-sections, and resolved missing data through principled imputation to preserve sample breadth across heterogeneous economies.
- **Feature Standardization** — Applied `StandardScaler` to normalize all 50+ predictors to zero mean and unit variance, a prerequisite for penalty-based methods where regularization strength is scale-sensitive.
- **OLS Baseline** — Estimated an ordinary least squares model on the full feature set to establish an overfitting benchmark, documenting the divergence between in-sample explanatory power and out-of-sample forecast validity via `train_test_split`.
- **Ridge Regression (L2)** — Deployed `RidgeCV` with cross-validated lambda selection to shrink all coefficients proportionally, reducing variance while retaining the full predictor set — probing whether distributed signal across correlated macro indicators could improve generalization.
- **Lasso Regression (L1)** — Deployed `LassoCV` with cross-validated penalty tuning to enforce sparse solutions, allowing the model to perform simultaneous estimation and variable selection across a theoretically over-specified feature space.
- **Coefficient Path Analysis** — Visualized the Lasso regularization path using `lasso_path` to trace how individual indicators enter or exit the active model as the penalty parameter varies, providing a data-driven indicator relevance ranking.
- **Out-of-Sample Evaluation** — Compared OLS, Ridge, and Lasso on held-out test R² to quantify the real-world generalization gain from regularization under high-dimensional conditions.

**Stack:** Python · pandas · NumPy · scikit-learn (`StandardScaler`, `RidgeCV`, `LassoCV`, `lasso_path`, `train_test_split`) · matplotlib · wbgapi

---

## Key Findings

OLS exhibited a textbook high-dimensional failure: strong in-sample fit paired with sharply degraded — and in some specifications negative — out-of-sample R². With predictors outnumbering the effective degrees of freedom for cross-country identification, the model absorbed noise as signal, producing forecasts with no reliable generalization.

Ridge regularization recovered meaningful out-of-sample performance by constraining coefficient magnitude across the full indicator set, confirming that distributed predictive content across correlated development indicators can be stabilized through L2 shrinkage.

Lasso matched Ridge's test R² while retaining only a sparse subset of the original feature space. The coefficient path analysis revealed that the majority of WDI indicators contribute redundant predictive information once a core set of macro and institutional variables is selected — a finding with direct implications for parsimonious growth model design.

The experiment draws a critical empirical distinction: **feature redundancy is not economic irrelevance**. Lasso's sparsity reflects collinearity structure in the data, not a definitive ranking of development drivers. Structural interpretation of the retained variables requires causal identification beyond the scope of regularized prediction — a boundary this lab explicitly respects.

---

*Part of an ongoing econometrics lab series focused on applied machine learning for financial and macroeconomic forecasting.*
