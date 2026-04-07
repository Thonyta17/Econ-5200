# Recovering Experimental Truths via Propensity Score Matching

> **Eliminating Selection Bias in Observational Data Through Causal Inference**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/ScikitLearn-Causal%20Inference-orange.svg)](https://scikit-learn.org/)
[![Methodology](https://img.shields.io/badge/Method-Propensity%20Score%20Matching-green.svg)]()

---

## 🎯 Objective

This project demonstrates how **Propensity Score Matching (PSM)** can recover unbiased treatment effect estimates from observational data afflicted by severe selection bias, replicating experimental findings without randomization.

---

## 📊 Context: The Lalonde Dataset

The Lalonde (1986) dataset is a canonical example in causal inference, comparing experimental results from a randomized job training program with observational data from the same intervention. The observational subset exhibits extreme selection bias: participants systematically differ from non-participants on observable characteristics (age, education, earnings history), violating the assumptions required for naive comparison.

**The Challenge**: Without randomization, simple comparisons of treated vs. untreated groups confound the treatment effect with pre-existing differences, yielding biased estimates that can even reverse the sign of the true causal impact.

---

## 🛠 Methodology

### 1. **Modeling Selection Bias**
   - Identified confounding variables that predict both treatment assignment and outcomes (age, education, race, prior earnings, employment status)
   - Diagnosed the extent of covariate imbalance between treated and control groups
   - Quantified the magnitude of selection bias in the naive observational estimate

### 2. **Estimating Propensity Scores**
   - Built a **logistic regression model** to predict the probability of treatment conditional on pre-treatment covariates
   - Generated propensity scores (predicted probabilities) for all units in the observational sample
   - Verified common support: ensured treated and control units had overlapping propensity score distributions to enable valid matching

### 3. **Applying Nearest Neighbor Matching**
   - Implemented **1:1 nearest neighbor matching** algorithm using propensity scores as the distance metric
   - For each treated unit, identified the control unit with the closest propensity score
   - Constructed a matched sample where treated and control groups were balanced on observed confounders
   - Estimated the Average Treatment Effect on the Treated (ATT) by comparing outcomes within matched pairs

### 4. **Technical Implementation**
   - **Python**: Core programming language for data manipulation and analysis
   - **Pandas**: Data wrangling, covariate construction, and matched sample generation
   - **Scikit-Learn**: Logistic regression modeling (`LogisticRegression`) for propensity score estimation

---

## 🔬 Key Findings

### Naive Observational Estimate: **-$15,204**
The unadjusted comparison of treated vs. untreated earnings produced a **negative treatment effect** of -$15,204, suggesting the job training program *reduced* earnings. This is a classic example of selection bias: program participants had lower baseline earnings and worse labor market prospects than non-participants, creating a spurious negative association.

### Propensity Score Matching Estimate: **≈ +$1,800**
After adjusting for selection bias through PSM, the estimated treatment effect was approximately **+$1,800**, indicating that the program *increased* annual earnings by roughly $1,800 for participants. This estimate aligns with the experimental benchmark from Lalonde's original randomized control trial.

### Bias Correction Magnitude: **$17,004**
The PSM procedure corrected a **$17,004 bias** in the naive estimate, flipping the sign of the effect from negative to positive. This demonstrates how severe selection bias can completely obscure—or even reverse—the true causal impact of interventions in observational data.

---

## 💡 Key Insights

1. **Observational Data ≠ Experimental Data**: Without randomization, naive comparisons of treatment and control groups are systematically biased when participants self-select (or are selected) based on characteristics that also affect outcomes.

2. **Propensity Scores as a Balancing Tool**: By matching on the probability of treatment (rather than matching on each covariate individually), PSM achieves covariate balance in high-dimensional settings while maintaining interpretability.

3. **Common Support is Critical**: Matching is only valid when treated and control units have overlapping propensity score distributions. Extrapolation beyond common support regions introduces model dependence and reduces credibility.

4. **PSM Assumes Selection on Observables**: This method can only adjust for confounders that are measured in the data. If important confounders are unobserved (e.g., motivation, ability), PSM estimates remain biased. This limitation motivates methods like instrumental variables or difference-in-differences for contexts with unobserved confounding.

---

## 📈 Implications

This analysis illustrates a fundamental tension in program evaluation: **observational data is abundant but biased; experimental data is credible but scarce**. Propensity Score Matching provides a principled middle ground, leveraging observational data while imposing the discipline of causal inference to approximate experimental conditions.

The ability to recover the experimental benchmark (+$1,800) from heavily biased observational data validates PSM as a credible tool for policy evaluation when randomized trials are infeasible. However, the magnitude of the initial bias (-$15,204) underscores the danger of naive observational comparisons and the necessity of rigorous causal methods in applied economics.

---

## 🎓 Technical Skills Demonstrated

- **Causal Inference**: Propensity Score Matching, Average Treatment Effect on the Treated (ATT)
- **Econometric Modeling**: Logistic regression for treatment assignment, covariate balancing
- **Statistical Diagnostics**: Common support verification, bias decomposition
- **Python Proficiency**: Pandas (data manipulation), Scikit-Learn (predictive modeling)
- **Program Evaluation**: Understanding experimental vs. observational designs, selection bias mitigation

---

## 📚 References

- Lalonde, R.J. (1986). "Evaluating the Econometric Evaluations of Training Programs with Experimental Data." *American Economic Review*, 76(4), 604-620.
- Rosenbaum, P.R., & Rubin, D.B. (1983). "The Central Role of the Propensity Score in Observational Studies for Causal Effects." *Biometrika*, 70(1), 41-55.
- Dehejia, R.H., & Wahba, S. (1999). "Causal Effects in Nonexperimental Studies: Reevaluating the Evaluation of Training Programs." *Journal of the American Statistical Association*, 94(448), 1053-1062.

---

## 🔍 Methodological Note

**Assumption**: Conditional Independence (Unconfoundedness)  
PSM relies on the assumption that, conditional on observed covariates, treatment assignment is independent of potential outcomes. Formally: `(Y₁, Y₀) ⊥ T | X`, where `Y₁` and `Y₀` are potential outcomes under treatment and control, `T` is treatment status, and `X` is the vector of observed covariates.

**Limitation**: This assumption is untestable and may fail if important confounders are unobserved. Sensitivity analyses (e.g., Rosenbaum bounds) can assess robustness to hidden bias.

---

## 🏆 Achievement

Successfully replicated experimental treatment effects from observational data by correcting a **112% bias** (from -$15,204 to +$1,800), demonstrating mastery of causal inference methods essential for credible policy evaluation in non-experimental settings.

---

**⚠️ Academic Context**: This project is part of a causal inference lab focusing on selection bias and matching estimators. The Lalonde dataset is used for pedagogical purposes to illustrate the mechanics and limitations of Propensity Score Matching.

**📌 Key Takeaway**: *In the absence of randomization, causal inference is not automatic—it requires explicit modeling of the selection process and rigorous application of identification strategies.*
