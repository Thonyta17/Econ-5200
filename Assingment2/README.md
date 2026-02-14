# Audit 02: Deconstructing Statistical Lies

> **An Academic Exercise in Forensic Statistical Analysis**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Statistical%20Computing-green.svg)](https://numpy.org/)

---

## 🎯 Project Overview

**Assignment**: Module 2 - Probability, Robustness, & Sampling  
**Scenario**: Data Quality Auditor analyzing three fictional Series B companies  
**Objective**: Expose statistical fallacies hidden in "perfect" metrics

| Company | Claimed Metric | Reality Check | Finding |
|---------|---------------|---------------|---------|
| **NebulaCloud** | 35ms mean latency | MAD vs SD analysis | MAD (8ms) is robust; SD explodes with outliers |
| **IntegrityAI** | 98% accuracy | Bayesian analysis | 4.67% precision in honors seminars (95% false positives) |
| **FinFlash** | "Huge A/B win" | Chi-square test | χ² = 5.00 > 3.84 → experiment INVALID |
| **Crypto Tokens** | — | Survivorship bias | Survivors mean ($2.19) vs All mean ($0.25) = 8.76x inflation |

---

## 🔬 Key Findings

### Finding 1: The Latency Mirage (Robust Statistics)

**Problem**: Standard Deviation is fragile—outliers explode the metric through squaring.

```python
def calculate_mad(data):
    median = np.median(data)
    abs_dev = np.abs(data - median)
    return np.median(abs_dev)
```

**Results**:
- Median Latency: 34ms (typical user)
- MAD: 8ms (robust measure)
- Standard Deviation: ~500-600ms (exploded by 2% outlier spikes)

**Insight**: MAD uses absolute values from the median (resistant to outliers). SD uses squared deviations from the mean (amplifies outliers exponentially).

---

### Finding 2: The False Positive Epidemic (Bayesian Reasoning)

**Problem**: "98% accurate" is meaningless without base rates.

```python
def bayesian_audit(prior, sensitivity, specificity):
    false_positive_rate = 1 - specificity
    prob_positive = (sensitivity*prior) + (false_positive_rate*(1-prior))
    return (sensitivity*prior) / prob_positive
```

**Results** (98% sensitivity, 98% specificity):

| Environment | Base Rate | P(Cheater\|Flagged) | Verdict |
|-------------|-----------|---------------------|---------|
| Bootcamp | 50% | 98.0% | ✅ Works |
| Econ Class | 5% | 71.5% | ⚠️ Risky |
| Honors Seminar | 0.1% | **4.67%** | ❌ Catastrophic |

**Insight**: In honors seminars, **95% of flagged students are innocent**—the tool generates 20 false accusations per true case.

---

### Finding 3: The Phantom A/B Win (Sample Ratio Mismatch)

**Problem**: Allocation skew invalidates experiments.

```python
observed = np.array([50250, 49750])  # Control, Treatment
expected = np.array([50000, 50000])  # Expected 50/50 split
chi_stat = sum((observed - expected)**2 / expected)
# χ² = 5.00
```

**Verdict**: χ² = 5.00 > 3.84 (critical value) → **Experiment INVALID**

**Insight**: Missing 500 treatment users suggests app crash. Any revenue lift is confounded by selection bias.

---

### Finding 4: The Memecoin Graveyard (Survivorship Bias)

**Problem**: Platforms delete failed tokens, inflating perceived returns.

```python
# Simulate 10,000 tokens with Pareto distribution (α=5)
peak_market_caps = np.random.pareto(5, 10000)
df_all = pd.DataFrame({'Peak Market Cap': peak_market_caps})

# Extract top 1% survivors
num_survivors = int(10000 * 0.01)
df_survivors = df_all.sort_values(by='Peak Market Cap', ascending=False).head(num_survivors)
```

**Results**:
- All Tokens Mean: $0.25
- Survivors Mean: $2.19
- **Inflation: 8.76x**

**Insight**: Reporting only the top 1% creates an 8.76x distortion. The "graveyard" (99% of tokens near zero) disappears from analysis.

---

## 💡 Key Lessons

1. **Aggregation is a Policy Decision**: Choosing mean vs median, or including/excluding failures, encodes assumptions about whose experience matters.

2. **Context Matters**: 98% accuracy means nothing without base rates. Always report precision conditional on deployment environment.

3. **Robust Statistics for Real Data**: Real-world data (latencies, market returns) are NOT Gaussian. Use median/MAD, not mean/SD.

4. **Audit Experiments**: Even "statistically significant" results are invalid if allocation is compromised. Check for SRM (χ² < 3.84).

5. **Survivorship Bias is Everywhere**: VCs report only exits, researchers publish only successes, platforms show only survivors.

---

## 🛠 Technical Skills Demonstrated

- **Robust Statistics**: Custom MAD implementation, outlier detection
- **Bayesian Inference**: Posterior probability calculation, base rate fallacy
- **Hypothesis Testing**: Chi-Square Goodness of Fit, SRM detection
- **Simulation**: Pareto distribution modeling, power-law dynamics
- **Python**: NumPy, Pandas, Matplotlib

---

## 🚀 How to Run

```bash
# Install dependencies
pip install numpy pandas matplotlib seaborn

# Run analysis
python audit_02.py
```

**Expected Output**:
```
Median Latency: 34.00 ms
MAD (Robust): 8.00 ms
Standard Deviation: ~500-600 ms

Scenario A probability: 98.0%
Scenario B probability: 71.51%
Scenario C probability: 4.67%

Chi-Square statistic: 5.0
The A/B test is invalid

Mean Peak Market Cap for All Launches: $0.25
Mean Peak Market Cap for Survivors: $2.19
```

---

## 📚 References

- Tukey, J.W. (1977). *Exploratory Data Analysis* (MAD/robust statistics)
- Kahneman & Tversky (1973). Base rate fallacy
- Kohavi et al. (2020). *Trustworthy Online Controlled Experiments* (SRM detection)

---

**⚠️ Academic Context**: This is a student assignment using simulated data. All companies are fictional. Statistical methods are based on peer-reviewed literature.

**🔍 Key Takeaway**: *The average hides more than it reveals. Always ask: "Whose experience am I erasing by choosing this aggregation?"*
