# Architecting the Prediction Engine

## Objective

Deploy a multivariate Ordinary Least Squares (OLS) regression framework against the Zillow ZHVI 2026 Micro Dataset to engineer a real estate valuation forecasting system, with rigorous out-of-sample evaluation centered on economically interpretable loss minimization.

---

## Methodology

- **Data Sourcing & Preparation:** Ingested the Zillow Home Value Index (ZHVI) 2026 cross-sectional micro dataset using `pandas`, representing a contemporaneous snapshot of U.S. residential real estate market conditions. Applied preprocessing pipelines to enforce data integrity prior to model training.

- **Feature Engineering & Model Specification:** Leveraged the `statsmodels` Patsy Formula API to declaratively specify the multivariate OLS model, enabling transparent, reproducible formula syntax for feature selection and interaction term management.

- **Train/Test Split & Predictive Architecture:** Partitioned the dataset into in-sample training and held-out test sets to operationalize a strict out-of-sample evaluation protocol — deliberately shifting the analytical paradigm from classical inferential explanation toward predictive generalization.

- **Loss Function Computation:** Evaluated model performance using Root Mean Squared Error (RMSE), calculated in nominal U.S. Dollars to produce a financially grounded, business-interpretable error metric rather than a dimensionless statistical abstraction.

---

## Key Findings

The model successfully bridged the methodological gap between classical econometric explanation and applied predictive engineering. By expressing RMSE in real dollar terms, the analysis yielded a precise, actionable estimate of the model's financial error margin — directly quantifying the algorithmic risk exposure inherent in production valuation forecasts. This framing enables stakeholders to assess model viability not merely through statistical fit, but through concrete business-risk criteria relevant to real estate pricing and investment decision-making.

---

## Tech Stack

| Tool | Role |
|---|---|
| Python | Core runtime |
| pandas | Data ingestion & wrangling |
| numpy | Numerical computation |
| statsmodels (Patsy) | OLS model specification & estimation |

---

*Dataset: Zillow ZHVI 2026 Micro Dataset (Cross-sectional)*
