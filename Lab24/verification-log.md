# Verification Log — Lab 24: Causal ML — DML & Causal Forests
**Author:** Thonyta Chhay | **Course:** ECON 5200 | **Date:** April 2026

---

## Part A: Diagnosis (No AI Used)

### Bug 1 — Data Leakage in Cross-Fitting
**Bug:** `ml_l.fit(X[train_idx])` then `ml_l.predict(X[train_idx])` — training and predicting on the same fold. In-sample prediction inflates goodness of fit and produces biased residuals.  
**Fix:** Train on `train_idx`, predict on `test_idx` (held-out fold).  
**Verification:** Fixed ATE within 1.0 of TRUE_ATE=5.0 ✅

### Bug 2 — Missing Treatment Residualization
**Bug:** `V_tilde = D[train_idx]` — raw treatment used instead of residuals. DML requires residualizing both Y and D to remove confounding from X.  
**Fix:** Fit `ml_m` on D~X, compute `V_tilde[test_idx] = D[test_idx] - ml_m.predict(X[test_idx])`.  
**Verification:** Fixed ATE within 1.0 of TRUE_ATE=5.0 ✅

### Bug 3 — Wrong Estimator Formula
**Bug:** `theta = np.mean(V_tilde * Y_tilde)` — simple average, not the IV-style ratio. This gives a biased estimate even with correct residuals.  
**Fix:** Use `theta = sum(V_tilde * Y_tilde) / sum(V_tilde * D)` — the correct DML moment condition.  
**Verification:** Fixed ATE within 1.0 of TRUE_ATE=5.0 ✅

---

## AI Expansion

### What AI Generated
- Fixed DML implementation (`fixed_dml()`)
- DoubleML PLR setup and sensitivity analysis
- CausalForestDML fit, CATE extraction, histogram, subgroup comparison
- Reflection answer, `README.md`, `verification-log.md`

### What I Verified
- `fixed_dml()` passes verification checkpoint (bias < 1.0) ✅
- `DoubleMLPLR` ATE is statistically significant (p < 0.05) ✅
- Sensitivity robustness value is positive ✅
- `cate_predictions.shape == (n,)` ✅
- High-response subgroup has systematically different characteristics ✅
