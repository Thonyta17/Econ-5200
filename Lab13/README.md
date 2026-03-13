The Architecture of Dimensionality: Hedonic Pricing & the FWL Theorem
Objective
This econometrics lab demonstrates the mathematical equivalence of multivariate OLS coefficients and partialled-out residuals by manually proving the Frisch-Waugh-Lovell (FWL) Theorem within a 2026 California real estate hedonic pricing framework.

Methodology
The project utilizes a high-dimensional synthetic Zillow dataset—incorporating variables such as Sale_Price, Property_Age, and Distance_to_Tech_Hub—to execute the following technical workflow:

Multivariate Baseline: Construction of a global OLS model using statsmodels to establish benchmark coefficients for property valuation.

Dimensionality Reduction: Application of the FWL Theorem to isolate the unique variation of specific regressors.

Residual Extraction: 1.  Regressing the dependent variable (Sale_Price) against the control covariates to extract the "unexplained" price residuals.
2.  Regressing the primary independent variable against the same controls to isolate its unique variance.

Partialling Out: Execution of a bivariate regression on the resulting residuals to "strip out" shared covariance.

Numerical Verification: Cross-validating the residualized coefficient against the multivariate output to prove mathematical identity.

Key Findings
Omitted Variable Bias (OVB): Initial bivariate analysis revealed significant upward bias; omitting Distance_to_Tech_Hub forced the model to falsely attribute proximity-based premiums to the physical Property_Age of the assets.

Algorithmic Correction: By manually isolating residuals, the project successfully demonstrated the "partialling out" mechanism. This process eliminated the latent influence of location, resulting in an exact mathematical match to the multivariate model’s coefficients.

Ceteris Paribus Validation: The alignment of the residual-on-residual slope with the full-model coefficient provides a rigorous proof of algorithmic ceteris paribus, confirming that the model effectively "holds other factors constant" through orthogonal projection.
