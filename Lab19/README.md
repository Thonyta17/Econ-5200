# Tree-Based Models — Random Forests

## Objective
Benchmark ensemble tree-based methods against linear regression on the California Housing dataset, diagnosing common evaluation pitfalls and assessing the limits of feature importance as a causal inference tool.

## Data
California Housing dataset — 20,640 observations, 8 socioeconomic and geographic features, continuous target: median house value (in $100,000s).

## Methodology
- Trained and compared three model families: single Decision Tree, Ridge Regression, and Random Forest (default and tuned), evaluating each strictly on held-out test data to avoid train/test leakage
- Diagnosed a deliberate evaluation bug in which Random Forest was assessed on training data, inflating reported R² from ~0.80 to >0.97 — illustrating the risks of overfitting and in-sample evaluation
- Tuned Random Forest hyperparameters (`n_estimators`, `max_depth`, `max_features`) via 5-fold GridSearchCV and benchmarked the tuned model against Gradient Boosting Regressor (GBR)
- Extracted MDI (Mean Decrease in Impurity) feature importances and diagnosed the methodological flaw of using predictive importance scores to make causal policy recommendations
- Ran permutation importance on the test set as a statistically unbiased alternative to MDI, and compared rankings across methods
- Applied SHAP TreeExplainer to generate waterfall plots for individual predictions (high-value, low-value, and high-error observations) and a beeswarm plot for global feature attribution
- Built a reusable `shap_analysis.py` module with production-ready docstrings and type hints, encapsulating `explain_prediction`, `global_importance`, and `compare_importance` functions

## Key Findings
- The largest performance gain came from switching model family, not from tuning: Ridge R² = 0.5759 vs. Random Forest (default) R² = 0.8049, a gap of +0.23 attributable to the RF's ability to capture nonlinear feature interactions
- Hyperparameter tuning yielded only marginal improvement: RF (tuned) R² = 0.8147 vs. RF (default) R² = 0.8049 (+0.010), suggesting the default configuration was near-optimal for this dataset
- GBR achieved the highest test performance (R² = 0.8288, RMSE = 0.4736), outperforming tuned RF by +0.014 R² — a statistically detectable but practically modest margin that must be weighed against GBR's greater tuning complexity
- MDI ranked `MedInc` as the dominant predictor; SHAP confirmed this directionally but revealed meaningful divergences in mid-tier features, consistent with MDI's known bias toward high-cardinality continuous variables
- SHAP waterfall analysis showed that high-value predictions were driven overwhelmingly by `MedInc` and `Longitude`, while prediction errors were concentrated in observations with unusual geographic clustering — a finding not visible from global importance metrics alone

## Reusable Artifact
`src/shap_analysis.py` — a modular SHAP utility library for tree-based sklearn models, designed for reuse across projects requiring local and global model explainability.

## Tools & Libraries
Python, scikit-learn, SHAP, pandas, NumPy, Matplotlib

## Repository Structure
```
├── notebooks/
│   └── lab-ch19-diagnostic.ipynb
├── src/
│   └── shap_analysis.py
└── README.md
```
