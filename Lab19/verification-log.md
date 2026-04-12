# Verification Log — Lab 19: Tree-Based Models & Random Forests
**Course:** ECON 5200 — Causal Machine Learning & Applied Analytics
**Date:** April 2025

---

## Part 1: Bug Fix — Model Comparison

### What was wrong
`r2_score(y_train, rf.predict(X_train))` evaluated the Random Forest on training data instead of test data, inflating R² to >0.97.

### Fix applied
Changed to `r2_score(y_test, rf.predict(X_test))`.

### Verified output
RF Test R² = 0.8049 — within the expected range of 0.78–0.83. ✓

### Concept violated
**Overfitting (Ch 15).** Random Forests grown without depth constraints memorize training data, producing near-perfect in-sample fit that does not generalize. Evaluating on training data hides this completely.

---

## Part 2: Methodological Flaw — Feature Importance

### What was wrong
The code used MDI (Mean Decrease in Impurity) rankings to make a causal policy recommendation: *"to increase housing prices, policymakers should focus on increasing [top feature]."*

### Why this is wrong
1. **Prediction ≠ causation.** MDI measures how useful a feature is for splitting trees, not whether it causally drives the outcome.
2. **Confounding.** `MedInc` is correlated with neighborhood quality, amenities, and other omitted variables. Intervening on income alone would not produce the predicted effect on housing prices without accounting for the full causal DAG (Ch 10).
3. **MDI bias.** MDI systematically overstates the importance of high-cardinality continuous features due to the higher number of possible split points. This makes it an unreliable basis for any recommendation.

### What would be needed for a causal claim
A causal identification strategy — e.g., Double Machine Learning (DML, Ch 24) — that isolates the effect of a single variable while controlling for confounders.

### Fix applied
Ran permutation importance on the test set instead, which is unbiased and evaluated on held-out data. Interpreted results as predictive associations only, not causal levers.

---

## Part 3: Hyperparameter Tuning + Model Comparison

### GridSearchCV setup
```
param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [10, 20, None],
    'max_features': ['sqrt', 0.5],
}
cv=5, scoring='r2'
```

### Results

| Model         | RMSE   | R²     |
|---------------|--------|--------|
| Ridge         | 0.7455 | 0.5759 |
| RF (default)  | 0.5057 | 0.8049 |
| RF (tuned)    | 0.4928 | 0.8147 |
| GBR           | 0.4736 | 0.8288 |

### Interpretation
- **Ridge → RF:** Large, meaningful improvement (+0.229 R²). Tree models capture nonlinear interactions that Ridge cannot.
- **RF default → RF tuned:** Small gain (+0.010 R²). Default RF was already near-optimal for this dataset.
- **RF tuned → GBR:** Small gain (+0.014 R²). Not practically significant given added tuning complexity.

**Conclusion:** The biggest gain comes from switching model family, not from tuning within one. GBR wins marginally but the difference over a well-tuned RF is negligible.

### Bug encountered and fixed
`mean_squared_error(squared=False)` raised `TypeError` in scikit-learn 1.4+. Fixed by replacing with `root_mean_squared_error()`.

---

## Extension: SHAP Analysis

### P.R.I.M.E. Prompt Used

```
[Prep] Act as an expert Python Data Scientist specializing in SHAP
explanations, interactive visualizations, and scikit-learn production workflows.

[Request] I just completed a diagnosis-first lab where I compared Decision
Trees, Ridge, Random Forests, and Gradient Boosting on California Housing data.
I fixed evaluation bugs, diagnosed causal overclaiming from MDI, tuned
hyperparameters with GridSearchCV, and generated SHAP waterfall + beeswarm
plots. Now I need a reusable shap_analysis.py module with three functions:
   - explain_prediction(model, X, idx) -> SHAP waterfall
   - global_importance(model, X) -> SHAP beeswarm
   - compare_importance(model, X, y) -> MDI vs SHAP side-by-side
Include type hints, docstrings, and error handling.

[Iterate] Use shap, numpy, pandas, matplotlib, sklearn. Use the same variable
names: X_train, X_test, y_train, y_test, data.feature_names.

[Mechanism Check] Add inline comments explaining how TreeExplainer differs
from KernelExplainer and why SHAP values are additive (Shapley property).

[Evaluate] Explain what the results reveal about where MDI and SHAP
rankings diverge and why.
```

### What AI generated
- Full `shap_analysis.py` module with three functions: `explain_prediction`, `global_importance`, `compare_importance`
- Type hints and docstrings for all functions
- `compare_importance` returns a DataFrame with `Rank_Difference` column flagging divergences ≥ 2 positions
- Side-by-side MDI vs SHAP bar chart

### What I changed
- Added `sample_size` and `random_state` parameters to `global_importance` and `compare_importance` — full `X_test` caused 18+ min runtime; sampling to 200 rows reduced it to under a minute
- Fixed `base_values` bug: `explainer.expected_value` returned a 1-element numpy array, not a scalar — resolved with `float(np.array(explainer.expected_value).flat[0])`
- Fixed `y_test` indexing: converted numpy array to `pd.Series` with `index=X_test.index` to enable `.loc[]` alignment with sampled `X_sample`
- Replaced `mean_squared_error(squared=False)` with `root_mean_squared_error()` for scikit-learn 1.4+ compatibility

### What I verified
- Waterfall plots rendered correctly for high-value, low-value, and most surprising observations ✓
- Beeswarm plot showed `MedInc` as the dominant feature globally ✓
- MDI and SHAP rankings broadly agreed on top features; minor divergences in mid-ranked features consistent with known MDI bias ✓
- `compare_importance()` returned a clean DataFrame with rank differences ✓

### MDI vs SHAP — Where they diverge
Both methods ranked `MedInc` first. Minor rank differences appeared in mid-tier features, consistent with MDI's known bias toward high-cardinality continuous variables. SHAP rankings, computed on held-out data using Shapley values, are the more reliable measure for any interpretive use.

---

## Setup Issue: SSL Certificate Error

**Error:** `SSLCertVerificationError` when running `fetch_california_housing()` on Python 3.13 / macOS.

**Fix:** Ran `/Applications/Python 3.13/Install Certificates.command` in Terminal. Permanent fix — resolved SSL verification for all Python downloads going forward.

---

## Files Submitted
- `lab-ch19-diagnostic.ipynb` — completed notebook with all fixes and analysis
- `shap_analysis.py` — reusable SHAP module (portfolio artifact)
- `verification-log.md` — this file