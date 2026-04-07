# Fraud Detection Model Evaluation — Metrics That Matter

## Objective
Evaluate a logistic regression fraud classifier on a severely class-imbalanced real-world transaction dataset by constructing a rigorous diagnostic framework — spanning confusion matrices, ROC and Precision-Recall curves, and capacity-constrained threshold optimization — to demonstrate that accuracy is an operationally misleading performance metric when the cost of false negatives is asymmetric.

---

## Data
**Kaggle Credit Card Fraud Detection Dataset** — 284,807 real European credit card transactions.

| Feature | Description |
|---|---|
| `V1`–`V28` | PCA-anonymized transaction features (original features withheld for confidentiality) |
| `Amount` | Transaction value in euros |
| `Class` | Binary fraud label: 1 = fraud, 0 = legitimate |

**Class distribution: 0.172% positive (fraud).** 492 fraud cases out of 284,807 total transactions — a ratio that structurally disqualifies accuracy as a primary evaluation criterion.

---

## Methodology

- **Accuracy Paradox Demonstration** — Constructed a naive all-negative baseline classifier and documented its 99.83% accuracy with zero fraud recall, establishing the core case against accuracy as a standalone metric for imbalanced classification problems in financial risk contexts.
- **Logistic Regression Classifier** — Trained a `LogisticRegression` model on the PCA-transformed feature set, applying feature standardization to `Amount` prior to estimation to ensure scale consistency with the anonymized components.
- **Confusion Matrix Analysis** — Decomposed predictions into true positives, false positives, true negatives, and false negatives at the default 0.5 decision threshold, quantifying the real operational cost of misclassification across both error types.
- **Classification Report** — Extracted Precision, Recall, and F1-Score per class via `classification_report`, disaggregating performance by the majority and minority class to surface the fraud-specific signal obscured by aggregate metrics.
- **ROC Curve & AUC** — Plotted the Receiver Operating Characteristic curve using `roc_curve` and computed `roc_auc_score` to evaluate the model's discriminative capacity across the full threshold spectrum, independent of any fixed operating point.
- **Precision-Recall Curve & PR-AUC** — Constructed the Precision-Recall curve via `precision_recall_curve` to assess performance specifically on the fraud class — the preferred diagnostic for severely imbalanced datasets where ROC-AUC can overstate real-world utility.
- **F1-Optimal Threshold Selection** — Swept the decision threshold across the unit interval and identified the value that maximizes F1-Score on the fraud class, demonstrating that the default 0.5 cutoff is not operationally optimal under class imbalance.
- **Capacity-Constrained Operating Point** — Imposed a realistic business constraint of 500 maximum daily fraud investigations, selecting the decision threshold that maximizes fraud capture (recall) subject to that investigative bandwidth limit — translating model output into an actionable operational policy.

**Stack:** Python · pandas · NumPy · scikit-learn (`LogisticRegression`, `confusion_matrix`, `classification_report`, `roc_curve`, `roc_auc_score`, `precision_recall_curve`, `f1_score`) · matplotlib · seaborn

---

## Key Findings

The accuracy paradox was reproduced exactly as theory predicts: a naive classifier that labels every transaction as legitimate achieves 99.83% accuracy while detecting zero fraud. This result is not a curiosity — it is the default failure mode of any model trained or evaluated on raw accuracy in a highly imbalanced operational environment. In production fraud detection, a 99.83%-accurate model that misses every fraud case represents total system failure.

The logistic regression classifier achieved strong ROC-AUC, confirming meaningful discriminative separation between fraud and legitimate transactions across the threshold spectrum. PR-AUC on the fraud class — a stricter and more operationally relevant benchmark — remained substantial, indicating the model retains genuine predictive utility on the minority class rather than merely exploiting base-rate structure.

Threshold analysis revealed that the F1-optimal decision boundary differs materially from the default 0.5 cutoff. Deploying a model at the default threshold in a class-imbalanced context imposes an implicit, unexamined tradeoff between Precision and Recall that may bear no relationship to the actual cost structure of fraud versus false-positive investigation.

The capacity-constrained operating point analysis translates this into concrete operational terms: given a fixed investigative budget of 500 daily reviews, the threshold can be explicitly calibrated to maximize fraud recovery within that constraint. **This is the correct framing for real-world model deployment — not "what is the model's accuracy," but "at what threshold does the model maximize business-relevant outcomes given operational constraints."**

---

*Part of an ongoing econometrics lab series focused on applied machine learning for financial and macroeconomic forecasting.*