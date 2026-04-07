## AI Capex Diagnostic Modeling: Econometric Integrity in AI Revenue Forecasting

### Objective
To implement a rigorous econometric diagnostic framework for NVIDIA-scale AI capital expenditure data, specifically identifying and correcting for structural heteroscedasticity to ensure statistically valid revenue projections.

---

### Methodology
The project utilizes high-frequency 2026 AI deployment metrics, leveraging **Python** and **statsmodels** to move beyond naive OLS assumptions. The technical workflow includes:

* **Baseline OLS Estimation:** Modeling AI Software Revenue as a function of Capital Expenditure (CapEx) and Deployment Velocity.
* **Structural Diagnostic Testing:** Application of the **Breusch-Pagan** and **White tests** to formally detect non-constant variance in the error terms across CapEx tiers.
* **Multicollinearity Assessment:** Calculating **Variance Inflation Factors (VIF)** to ensure deployment metrics are not conflating the marginal impact of CapEx.
* **Robust Covariance Correction:** Implementation of **HC3 (Davidson-MacKinnon)** robust standard errors to account for leverage points in the dataset and provide a more conservative, unbiased inference.
* **Residual Visualization:** Mapping standardized residuals against fitted values using **Seaborn** to visualize the "fan" effect of heteroscedasticity.

---

### Key Findings
* **Heteroscedasticity Identification:** Discovered a proportional relationship between the scale of investment and error variance. At high-tier CapEx levels, the dispersion of software revenue outcomes expanded significantly, violating the Gauss-Markov assumption of homoscedasticity.
* **False Confidence Bias:** The initial naive OLS model produced artificially narrow confidence intervals and inflated t-statistics ($p < 0.05$), creating a "false positive" environment for certain deployment sub-metrics.
* **Statistical Recalibration:** The application of HC3 robust estimators successfully widened the standard errors. This correction revealed that while CapEx remains a primary driver, the statistical significance of secondary deployment variables was previously over-leveraged, leading to more accurate and grounded revenue forecasting.
