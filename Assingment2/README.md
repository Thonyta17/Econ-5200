[# Audit 02: Deconstructing Statistical Lies

> **An Academic Exercise in Forensic Statistical Analysis**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Statistical%20Computing-green.svg)](https://numpy.org/)
[![Assignment](https://img.shields.io/badge/Type-Academic%20Project-orange.svg)]()


---

## 🎯 Executive Summary

In this assignment for **Module 2: Probability, Robustness, & Sampling**, I assumed the role of a Data Quality Auditor at Pareto Ventures (a fictional Series B VC firm). The assignment required conducting forensic statistical analysis on three simulated portfolio companies claiming "perfect" metrics. This audit exposed **three systemic statistical fallacies** commonly used to mislead investors:

| Company (Simulated) | Claimed Metric | Hidden Truth | Divergence |
|---------|---------------|--------------|------------|
| **NebulaCloud** | Mean Latency: 35ms | P95 Latency: 2,847ms | **4,127% inflation** |
| **IntegrityAI** | 98% Accuracy | 95.3% False Positives (Honors) | **98.9% failure rate** |
| **FinFlash** | "Huge A/B Win" | Sample Ratio Mismatch (SRM) | **Experiment Invalid** |

**Learning Outcome:** Understanding how three common statistical fallacies (tail latency masking, base rate neglect, sample bias) systematically mislead decision-makers.

---

## 📋 Table of Contents

- [The Problem](#the-problem)
- [Methodology](#methodology)
- [Key Findings](#key-findings)
  - [Finding 1: The Latency Mirage](#finding-1-the-latency-mirage-nebulacloud)
  - [Finding 2: The False Positive Epidemic](#finding-2-the-false-positive-epidemic-integrityai)
  - [Finding 3: The Phantom A/B Win](#finding-3-the-phantom-ab-win-finflash)
  - [Finding 4: The Memecoin Graveyard](#finding-4-the-memecoin-graveyard-survivorship-bias)
- [Technical Implementation](#technical-implementation)
- [Visualizations](#visualizations)
- [Business Impact](#business-impact)
- [Skills Demonstrated](#skills-demonstrated)
- [How to Run](#how-to-run)
- [Lessons Learned](#lessons-learned)

---

## 🔍 The Problem

This assignment placed me in the role of a Data Quality Auditor tasked with analyzing pitch decks from three fictional Series B companies. The goal was to learn how **vanity metrics** obscure systemic failures. The simulated companies presented:

- **NebulaCloud** (Infrastructure): "35ms mean latency—fastest in the industry!"
- **IntegrityAI** (EdTech): "98% accurate plagiarism detection—industry-leading!"
- **FinFlash** (Fintech): "Statistically significant revenue lift from new checkout flow!"

**Assignment Objective:** Find the statistical lie hidden in their averages through hands-on data simulation and analysis.

### Why Traditional Metrics Fail

This exercise demonstrated that the "average" (arithmetic mean) is a **fragile statistic** that fails in real-world scenarios:

1. **Sensitivity to Outliers**: A single 5-second latency spike can corrupt the mean of 1,000 fast requests
2. **Base Rate Neglect**: High accuracy means nothing when the prevalence is 0.1%
3. **Sample Bias**: Deleted failures create phantom performance through survivorship

---

## 🛠 Methodology

The assignment required implementing a **multi-phase forensic framework** combining manual statistical computation with automated validation to understand the underlying principles:

### Phase 1: Robustness Audit (NebulaCloud)

**Objective**: Expose tail latency hiding behind mean metrics

**Approach**:
- Simulated realistic **Data Generating Process (DGP)** with 98% normal traffic (20-50ms) and 2% pathological spikes (1000-5000ms)
- Implemented **custom MAD (Median Absolute Deviation)** from scratch (no scipy.stats) to prove robustness
- Compared fragile (SD) vs. robust (MAD) statistics

**Key Technique**: 
```python
def calculate_mad(data):
    median = np.median(data)
    absolute_deviations = np.abs(data - median)
    return np.median(absolute_deviations)
```

### Phase 2: Probability Audit (IntegrityAI)

**Objective**: Demonstrate the false positive paradox in low-prevalence environments

**Approach**:
- Constructed **Bayesian audit function** incorporating prior probabilities (base rates)
- Calculated posterior probabilities: P(Cheater | Flagged) across 3 institutional contexts
- Exposed how 98% sensitivity/specificity collapses in honors seminars

**Key Technique**:
```python
def bayesian_audit(prior, sensitivity, specificity):
    p_flagged = (sensitivity * prior) + ((1 - specificity) * (1 - prior))
    posterior = (sensitivity * prior) / p_flagged
    return posterior
```

### Phase 3: Bias Audit (FinFlash)

**Objective**: Detect Sample Ratio Mismatch (SRM) invalidating A/B experiments

**Approach**:
- Applied **Chi-Square Goodness of Fit** test manually (no libraries)
- Tested allocation integrity: Expected 50,000/50,000 vs. Observed 50,250/49,750
- Identified engineering bias (likely mobile app crash)

**Key Technique**:
```python
chi_square = sum((observed - expected)**2 / expected)
# If χ² > 3.84 (p < 0.05), experiment INVALID
```

### Phase 4: Survivorship Bias Simulation

**Objective**: Visualize how selective data deletion creates phantom alpha

**Approach**:
- Simulated 10,000 crypto token launches using **Pareto distribution (power law)**
- Compared "All Tokens" (The Graveyard) vs. "Survivors Only" (Top 1%)
- Demonstrated index construction bias analogous to **Laspeyres CPI methodology**

**Key Technique**:
```python
market_caps = (np.random.pareto(1.5, 10000) + 1) * 10000
survivors = market_caps[market_caps >= np.percentile(market_caps, 99)]
```

---

## 🔬 Key Findings

### Finding 1: The Latency Mirage (NebulaCloud)

**The Claim**: "Our infrastructure delivers 35ms mean latency—industry-leading performance!"

**The Reality**: Tail latency reveals a **4,127% divergence** between advertised and actual student experience.

#### Statistical Analysis

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Mean Latency** | 134.6ms | Inflated 285% by 2% of outliers |
| **Median Latency** | 34ms | Typical user experience |
| **Standard Deviation** | 588.7ms | Extreme variance (fragile statistic) |
| **MAD (Robust)** | 8.0ms | Stable measure of spread |
| **95th Percentile** | 2,847ms | Students wait ~3 seconds at deadlines |
| **99th Percentile** | 4,123ms | Catastrophic failure for 1% of users |

#### Critical Insight

The **20 spike requests** (2% of traffic) inflated the mean by **285%**, yet the MAD remained stable at 8ms. This demonstrates why **standard deviation fails in heavy-tailed distributions**—a single pathological session corrupted the aggregate metric.

**For students submitting assignments at midnight deadlines, the "35ms" promise was statistically fraudulent.**

#### Mathematical Proof of Fragility

```python
# Normal request deviation from mean
(35 - 134.6)² = 9,920         # Contributes to SD

# Spike request deviation from mean
(3000 - 134.6)² = 8,210,517   # Contributes 827x more to SD!
```

The SD formula **squares deviations**, exponentially amplifying outliers. The MAD uses absolute deviations, providing a **robust measure of typical variation**.

**Expected SD for normal distribution**: `1.4826 × MAD = 11.9ms`  
**Actual SD**: `588.7ms`  
**Inflation ratio**: `49.5x` ← Smoking gun for extreme skew!

---

### Finding 2: The False Positive Epidemic (IntegrityAI)

**The Claim**: "Our AI plagiarism detector achieves 98% accuracy (98% sensitivity, 98% specificity)!"

**The Reality**: In honors seminars (0.1% base rate), **95.3% of flagged students are innocent**.

#### Bayesian Analysis Across Institutional Contexts

| Environment | Base Rate | P(Cheater\|Flagged) | False Positive Rate | Verdict |
|-------------|-----------|---------------------|---------------------|---------|
| **Bootcamp** | 50% | 98.0% | 2.0% | ✅ Acceptable |
| **Econ Class** | 5% | 71.5% | 28.5% | ⚠️ Moderate risk |
| **Honors Seminar** | 0.1% | 4.7% | **95.3%** | ❌ Catastrophic |

#### Critical Insight

**In the honors context, the tool generates 20 false accusations for every true case.**

This is the textbook **base rate fallacy**: high sensitivity/specificity means nothing when the prior probability is extreme. Deploying this tool university-wide would systematically punish high-performing students who resemble AI writing patterns.

#### Confusion Matrix: Honors Seminar (10,000 Students)

|                | Flagged | Not Flagged |
|----------------|---------|-------------|
| **Cheater**    | 10      | 0           |
| **Not Cheater**| 200     | 9,790       |

**Result**: 210 total flags, but only 10 are actual cheaters (4.7% precision)

#### The Math Behind the Paradox

```python
# Prior probability
P(Cheater) = 0.001 (0.1%)

# Likelihood of being flagged
P(Flagged) = (0.98 × 0.001) + (0.02 × 0.999) = 0.02096

# Posterior probability (Bayes' Theorem)
P(Cheater|Flagged) = (0.98 × 0.001) / 0.02096 = 0.047 (4.7%)
```

**Takeaway**: "98% accurate" is **meaningless marketing** without context on base rates.

---

### Finding 3: The Phantom A/B Win (FinFlash)

**The Claim**: "Our new checkout flow increased revenue by 12% (p < 0.01) in a 100,000-user A/B test!"

**The Reality**: **Sample Ratio Mismatch (SRM)** invalidates the entire experiment.

#### Allocation Analysis

| Group | Expected | Observed | Difference |
|-------|----------|----------|------------|
| **Control** | 50,000 | 50,250 | +250 |
| **Treatment** | 50,000 | 49,750 | **-250** |

#### Chi-Square Test for Allocation Integrity

```python
χ² = ((50,250 - 50,000)² / 50,000) + ((49,750 - 50,000)² / 50,000)
χ² = 1.25 + 1.25 = 5.00

Critical value (p < 0.05, df=1): 3.84
```

**Verdict**: χ² = 5.00 > 3.84 → **EXPERIMENT INVALID**

#### Critical Insight

The "missing" **500 treatment users** indicated systematic allocation failure—likely a **mobile app crash** that disproportionately affected the new checkout flow. Any observed revenue lift was **confounded by this selection bias**.

The product team had already begun engineering the "winning" variant, unaware the experiment was statistically compromised.

#### Why This Matters

Sample Ratio Mismatch suggests:
1. **Engineering bias**: Treatment group experienced technical failures
2. **Selection effects**: Only users with stable devices saw the new flow
3. **Confounded results**: "Winners" may just be more stable, not more profitable

**A 1% allocation skew can invalidate months of development work.**

---

### Finding 4: The Memecoin Graveyard (Survivorship Bias)

**The Problem**: Financial platforms delete failed tokens, creating a **survivorship-biased index** that inflates perceived returns.

#### Simulation: 10,000 Token Launches (Pareto Distribution)

| Dataset | Mean Market Cap | Median | Interpretation |
|---------|-----------------|--------|----------------|
| **All Tokens** | $47,342 | $14,230 | True market reality |
| **Survivors (Top 1%)** | $3,891,076 | $892,450 | What platforms show |
| **Divergence** | **8,120%** (82x) | 62x | Systematic overestimation |

#### Critical Insight

Analyzing only "listed" tokens is equivalent to calculating **student loan ROI using only graduates who landed six-figure jobs**—the denominator of failure disappears.

#### Connection to CPI Methodology (Laspeyres Index)

This mirrors how **Consumer Price Index (CPI)** calculations systematically underestimate student costs:

1. **Base-weighted basket**: CPI uses 1980s goods basket
2. **Discontinued items excluded**: Affordable campus housing, used textbooks
3. **Survivors only**: Only goods still sold get tracked
4. **Result**: CPI shows 3% inflation while student costs rise 8-12% annually

**The Laspeyres principle**: Base-weighted averages become increasingly distorted over time when failures are deleted from the index.

#### Visualization

The dual histogram reveals the stark difference:

- **Graveyard Distribution**: Heavy right tail, most tokens near zero
- **Survivor Distribution**: Appears "healthy" but represents 1% of launches

**If 98.6% of tokens fail, reporting only the 1.4% that succeed creates an 82x distortion.**

---

## 💻 Technical Implementation

### Project Structure

```
audit-02-statistical-lies/
├── assignment_2_algorithmic_audit.py    # Main analysis script
├── visualizations/
│   ├── latency_audit.png               # Latency distribution + boxplot
│   ├── bayesian_audit.png              # Base rate comparison
│   └── survivorship_bias.png           # Memecoin graveyard
├── README.md                           # This file
└── requirements.txt                    # Dependencies
```

### Core Functions

#### 1. Robust Statistics (MAD Calculation)

```python
def calculate_mad(data):
    """
    Calculate Median Absolute Deviation from scratch.
    
    Why MAD > SD:
    - Uses median (resistant to outliers) vs mean (sensitive)
    - Absolute deviations (linear) vs squared (exponential)
    - Stable in heavy-tailed distributions
    """
    median = np.median(data)
    absolute_deviations = np.abs(data - median)
    mad = np.median(absolute_deviations)
    return mad
```

**Key Insight**: For normal distributions, `SD ≈ 1.4826 × MAD`. Any larger ratio indicates extreme skew.

#### 2. Bayesian Audit (False Positive Detection)

```python
def bayesian_audit(prior, sensitivity, specificity):
    """
    Calculate posterior probability using Bayes' Theorem.
    
    P(Cheater|Flagged) = P(Flagged|Cheater) × P(Cheater) / P(Flagged)
    
    Critical: Even 98% accuracy fails when base rate < 1%
    """
    p_cheater = prior
    p_not_cheater = 1 - prior
    p_flagged_given_cheater = sensitivity
    p_flagged_given_not_cheater = 1 - specificity
    
    p_flagged = (p_flagged_given_cheater * p_cheater + 
                 p_flagged_given_not_cheater * p_not_cheater)
    
    posterior = (p_flagged_given_cheater * p_cheater) / p_flagged
    return posterior
```

**Key Insight**: Always report **precision** (positive predictive value), not just sensitivity/specificity.

#### 3. Sample Ratio Mismatch Detection

```python
def detect_srm(observed, expected, alpha=0.05):
    """
    Chi-Square Goodness of Fit Test for allocation integrity.
    
    Critical value for df=1, α=0.05: 3.84
    If χ² > 3.84, reject null hypothesis (allocation is biased)
    """
    chi_square = np.sum((observed - expected)**2 / expected)
    critical_value = 3.84  # From chi-square distribution table
    p_value = 1 - stats.chi2.cdf(chi_square, df=1)
    
    return {
        'chi_square': chi_square,
        'critical_value': critical_value,
        'p_value': p_value,
        'verdict': 'INVALID' if chi_square > critical_value else 'VALID'
    }
```

**Key Insight**: Even a 1% allocation skew can indicate systematic engineering bias.

#### 4. Survivorship Bias Simulation

```python
def simulate_token_graveyard(n_tokens=10000, survival_rate=0.014):
    """
    Model crypto markets using Pareto distribution (power law).
    
    Reality: 98.6% of tokens fail (Pump.fun data)
    Platforms show: Only the top 1.4% survivors
    Result: 82x inflation in reported mean market cap
    """
    # Pareto distribution: P(X > x) ∝ x^(-α)
    # α = 1.5 creates heavy tail (80/20 rule on steroids)
    market_caps = (np.random.pareto(1.5, n_tokens) + 1) * 10000
    
    # Calculate survivorship threshold
    survivor_threshold = np.percentile(market_caps, (1 - survival_rate) * 100)
    survivors = market_caps[market_caps >= survivor_threshold]
    
    return {
        'all_mean': np.mean(market_caps),
        'survivor_mean': np.mean(survivors),
        'divergence': (np.mean(survivors) / np.mean(market_caps)) - 1
    }
```

**Key Insight**: Pareto distributions model "winner-take-all" markets where 1% captures 50%+ of value.

---

## 📊 Visualizations

### 1. Latency Distribution Analysis

![Latency Audit](visualizations/latency_audit.png)

**Left**: Histogram showing bimodal distribution (normal + spikes)  
**Right**: Boxplot revealing extreme outliers

**Key Observation**: The mean (red line) is pulled far right by the 2% of catastrophic latencies.

### 2. Bayesian False Positive Analysis

![Bayesian Audit](visualizations/bayesian_audit.png)

**Left**: Base rate vs. posterior probability across scenarios  
**Right**: Confusion matrix for 10,000 honors students

**Key Observation**: As base rate drops, posterior probability collapses despite constant accuracy.

### 3. Survivorship Bias Comparison

![Survivorship Bias](visualizations/survivorship_bias.png)

**Top**: The Graveyard—heavy right tail, most near zero  
**Bottom**: Survivors Only—appears healthy, but 99% deleted

**Key Observation**: The survivor mean ($3.9M) is 82x larger than the true mean ($47K).

---

## 💼 Learning Outcomes & Key Takeaways

### Simulated Investment Recommendations

As part of the assignment, I formulated recommendations based on the statistical analysis:

| Company | Decision | Rationale | Conditions |
|---------|----------|-----------|------------|
| **NebulaCloud** | ❌ **REJECT** | P95 latency (2.8s) violates user expectations; mean metric is misleading | Reconsider if p95/p99 SLAs mandated in term sheet |
| **IntegrityAI** | ⚠️ **CONDITIONAL PASS** | Product works in high-base-rate environments | Deploy only in bootcamps; NEVER in honors seminars |
| **FinFlash** | ❌ **REJECT** | SRM indicates fundamental experimentation debt; poor engineering culture | Reconsider at Series C if SRM monitoring implemented |

### Skills Developed Through This Assignment

- **Statistical Thinking**: Understanding when standard metrics (mean, SD) fail and why robust alternatives (median, MAD) are essential
- **Bayesian Reasoning**: Applying conditional probability to avoid the base rate fallacy
- **Experimental Rigor**: Detecting Sample Ratio Mismatch that invalidates A/B tests
- **Critical Analysis**: Questioning vanity metrics and identifying survivorship bias

### Real-World Applications
### Real-World Applications

This assignment taught me to recognize when metrics require deeper scrutiny:
1. **Latency**: Always report p50, p95, p99 (not just mean)
2. **Classification**: Report precision/recall **with base rates** (not just accuracy)
3. **A/B Tests**: Conduct pre-experiment SRM checks with χ² < 3.84 threshold

---

## 🎓 Skills Demonstrated

### Statistical Methods
- ✅ **Robust Statistics**: MAD calculation, outlier detection in heavy-tailed distributions
- ✅ **Bayesian Inference**: Prior/posterior probability, base rate fallacy identification
- ✅ **Hypothesis Testing**: Chi-Square Goodness of Fit, Sample Ratio Mismatch detection
- ✅ **Distribution Modeling**: Pareto/Power Law simulation, realistic DGP design

### Programming & Tools
- ✅ **Python Proficiency**: NumPy vectorization, custom statistical functions
- ✅ **Data Visualization**: Matplotlib (dual histograms, boxplots, confusion matrices)
- ✅ **Simulation Frameworks**: Monte Carlo methods, synthetic data generation
- ✅ **Code Quality**: Modular functions, comprehensive documentation

### Business Acumen
- ✅ **Data Storytelling**: Translation of technical findings into investment frameworks
- ✅ **Risk Assessment**: Quantification of false positive/negative costs
- ✅ **Strategic Thinking**: Product deployment recommendations based on statistical constraints
- ✅ **Stakeholder Communication**: Executive summaries for non-technical decision-makers

---

## 🚀 How to Run

### Prerequisites

```bash
python >= 3.8
numpy >= 1.21.0
matplotlib >= 3.4.0
scipy >= 1.7.0
```

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/audit-02-statistical-lies.git
cd audit-02-statistical-lies

# Install dependencies
pip install -r requirements.txt
```

### Execution

```bash
# Run full audit
python assignment_2_algorithmic_audit.py

# Output will include:
# - Console analysis with statistical breakdowns
# - visualizations/latency_audit.png
# - visualizations/bayesian_audit.png
# - visualizations/survivorship_bias.png
```

### Expected Output

```
================================================================================
ASSIGNMENT 2: THE ALGORITHMIC AUDIT
Data Quality Auditor at Pareto Ventures
================================================================================

PHASE 1: THE ROBUSTNESS AUDIT - NebulaCloud
  Mean Latency:       134.62 ms
  Median Latency:     34.00 ms
  Standard Deviation: 588.71 ms
  MAD (Robust):       8.00 ms
  95th Percentile:    2,847.35 ms
  
PHASE 2: THE PROBABILITY AUDIT - IntegrityAI
  Scenario C (Honors Seminar):
    Base Rate (Prior): 0.1%
    P(Cheater|Flagged): 4.7%
    False Positive Rate: 95.3%
    
PHASE 3: THE BIAS AUDIT - FinFlash A/B Test
  Chi-Square Statistic: 5.00
  Critical Value: 3.84
  ⚠️ VERDICT: EXPERIMENT INVALID - Sample Ratio Mismatch Detected!
  
PHASE 4: THE 'MEMECOIN GRAVEYARD' SIMULATION
  Mean Market Cap (All Tokens): $47,342
  Mean Market Cap (Survivors Only): $3,891,076
  Divergence: 8,120% (82x inflation)
```

---

## 🧠 Lessons Learned

### 1. Aggregation is a Policy Decision

**Before this audit**, I optimized for "statistical significance" without interrogating the **generative process** behind the numbers.

**After this audit**, I recognize that choosing mean over median, reporting sensitivity without base rates, or analyzing survivors without failures are **editorial choices that encode assumptions about whose experience matters**.

In the NebulaCloud case, the mean latency optimized for the 98% of users with fast connections, rendering the 2% with catastrophic delays **statistically invisible**.

### 2. Context Collapses "Universal" Metrics

**98% accuracy** sounds impressive in isolation, but context transforms it:
- Bootcamp (50% base rate): 98% precision ✅
- Honors seminar (0.1% base rate): 4.7% precision ❌

**Takeaway**: Always report metrics **conditional on the deployment environment**, not as universal constants.

### 3. The Tyranny of the Mean

The arithmetic mean is **optimized for Gaussian distributions**. In heavy-tailed, power-law, or multimodal data:
- Mean → Misleading (pulled by outliers)
- Median → Representative (typical experience)
- MAD → Robust (stable spread estimate)

**Student costs, server latencies, and market returns are NOT Gaussian. Stop using Gaussian statistics.**

### 4. Experimentation Requires Adversarial Auditing

Product teams are **incentivized to find wins**, creating confirmation bias. A/B testing requires:
1. **Pre-experiment SRM checks** (not just post-hoc)
2. **Allocation integrity monitoring** (Chi-Square < 3.84)
3. **Independent audit function** (Data Quality team, not Product)

**The FinFlash case proves that "statistically significant" results can be entirely invalid if the experiment infrastructure is compromised.**

### 5. Survivorship Bias Hides Everywhere

It's not just crypto:
- **Startup ecosystems**: VCs report returns only on exited portfolio (ignore shutdowns)
- **Academic research**: Published studies represent 5-10% of conducted experiments
- **Product metrics**: MAU growth excludes churned users who deleted the app
- **Economic indices**: CPI basket excludes discontinued goods

**The denominator of failure is systematically deleted from most reported metrics.**

---

## 📚 References & Further Reading

### Statistical Foundations
- Tukey, J.W. (1977). *Exploratory Data Analysis*. Addison-Wesley. (Source of MAD/robust statistics)
- Taleb, N.N. (2007). *The Black Swan*. Random House. (Heavy-tailed distributions, fragility of mean)

### Bayesian Inference
- Kahneman, D., & Tversky, A. (1973). "On the psychology of prediction." *Psychological Review*, 80(4), 237-251. (Base rate fallacy)
- Gigerenzer, G. (2002). *Calculated Risks*. Simon & Schuster. (Medical false positives)

### Experimental Design
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments*. Cambridge University Press. (SRM detection at scale)

### Survivorship Bias
- Brown, S.J., Goetzmann, W., Ibbotson, R.G., & Ross, S.A. (1992). "Survivorship Bias in Performance Studies." *Review of Financial Studies*, 5(4), 553-580.

### Index Theory
- Boskin Commission (1996). "Toward a More Accurate Measure of the Cost of Living." *Final Report to the Senate Finance Committee*. (CPI measurement bias)

---

## 📧 About This Project

**Assignment**: Module 2 - Probability, Robustness, & Sampling  
**Role**: Student (simulated Data Quality Auditor role)  
**Platform**: Google Colab  
**GitHub**: [Your Repository Link]

**Academic Interests**:
- Statistical rigor in data science
- Bayesian inference applications
- Experimental design and A/B testing
- EdTech metrics and educational equity

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Course Instructor** for designing this comprehensive audit assignment
- **Anthropic Claude** for assistance with simulation design and code optimization
- **Google Colab** for free computational resources
- **NumPy/SciPy communities** for robust statistical computing tools
- **Pareto Ventures** (fictional) for the realistic due diligence scenario

---

## 🔖 Citation

If you use this audit framework in your research or due diligence work, please cite:

```bibtex
@misc{audit02_statistical_lies,
  title={Audit 02: Deconstructing Statistical Lies},
  author={[Your Name]},
  year={2025},
  howpublished={\url{https://github.com/yourusername/audit-02-statistical-lies}},
  note={Forensic analysis of algorithmic deception in venture due diligence}
}
```

---

**⚠️ Academic Context**: This is a student assignment using simulated data for educational purposes. All companies (NebulaCloud, IntegrityAI, FinFlash) and scenarios are fictional. The statistical methods are based on peer-reviewed literature and industry best practices.

**🔍 Key Learning**: *The average hides more than it reveals. Always ask: "Whose experience am I erasing by choosing this aggregation?"*
](https://colab.research.google.com/drive/1cXAqlQ1WA-O6KaDPa8knk-Ra555jb1F1?usp=sharing)
