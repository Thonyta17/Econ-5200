"""
shap_analysis.py
----------------
Reusable SHAP explanation utilities for tree-based sklearn models.

Functions:
    explain_prediction  -- SHAP waterfall plot for a single observation
    global_importance   -- SHAP beeswarm plot for global feature importance
    compare_importance  -- Side-by-side MDI vs SHAP ranking

Author: Thonyta
Course: ECON 5200 — Causal Machine Learning & Applied Analytics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
from sklearn.base import BaseEstimator
from typing import Optional


def explain_prediction(
    model: BaseEstimator,
    X: pd.DataFrame,
    idx: int,
    feature_names: Optional[list] = None,
) -> None:
    """
    Generate a SHAP waterfall plot explaining a single prediction.

    The waterfall plot shows how each feature pushes the prediction
    above or below the model's baseline (expected) value, making it
    easy to understand why the model predicted what it did for one
    specific observation.

    Parameters
    ----------
    model : BaseEstimator
        A fitted tree-based sklearn model (e.g. RandomForestRegressor,
        GradientBoostingRegressor).
    X : pd.DataFrame
        Feature matrix. The observation at position `idx` will be explained.
    idx : int
        Positional index (0-based) of the observation to explain.
    feature_names : list of str, optional
        Feature names to display on the plot. Defaults to X.columns.

    Returns
    -------
    None
        Displays the waterfall plot inline.

    Example
    -------
    >>> explain_prediction(best_rf, X_test, idx=0)
    """
    if feature_names is None:
        feature_names = X.columns.tolist()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X.iloc[idx : idx + 1])
    base_val = float(np.array(explainer.expected_value).flat[0])

    explanation = shap.Explanation(
        values=shap_values[0],
        base_values=base_val,
        data=X.iloc[idx].values,
        feature_names=feature_names,
    )

    print(f"Observation {idx} — Predicted: {model.predict(X.iloc[idx:idx+1])[0]:.4f}")
    shap.plots.waterfall(explanation)


def global_importance(
    model: BaseEstimator,
    X: pd.DataFrame,
    sample_size: int = 200,
    random_state: int = 42,
    feature_names: Optional[list] = None,
) -> None:
    """
    Generate a SHAP beeswarm plot showing global feature importance.

    The beeswarm plot displays the distribution of SHAP values for each
    feature across all observations, showing both the magnitude and
    direction of each feature's effect on predictions.

    Parameters
    ----------
    model : BaseEstimator
        A fitted tree-based sklearn model.
    X : pd.DataFrame
        Feature matrix. Will be sampled to `sample_size` rows for speed.
    sample_size : int, optional
        Number of rows to sample for SHAP computation. Default is 200.
    random_state : int, optional
        Random seed for reproducible sampling. Default is 42.
    feature_names : list of str, optional
        Feature names to display. Defaults to X.columns.

    Returns
    -------
    None
        Displays the beeswarm plot inline.

    Example
    -------
    >>> global_importance(best_rf, X_test, sample_size=200)
    """
    if feature_names is None:
        feature_names = X.columns.tolist()

    X_sample = X.sample(min(sample_size, len(X)), random_state=random_state)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    base_val = float(np.array(explainer.expected_value).flat[0])

    explanation = shap.Explanation(
        values=shap_values,
        base_values=base_val,
        data=X_sample,
        feature_names=feature_names,
    )

    shap.plots.beeswarm(explanation)


def compare_importance(
    model: BaseEstimator,
    X: pd.DataFrame,
    y: np.ndarray,
    sample_size: int = 200,
    random_state: int = 42,
    feature_names: Optional[list] = None,
) -> pd.DataFrame:
    """
    Compare MDI (Mean Decrease in Impurity) vs SHAP feature importance rankings.

    MDI is computed directly from the model's internal split statistics and
    is known to be biased toward high-cardinality continuous features. SHAP
    values are computed on a held-out sample and are theoretically grounded
    in Shapley values, making them a more reliable measure of true feature
    contribution. Divergences between the two rankings reveal where MDI
    may be misleading.

    Parameters
    ----------
    model : BaseEstimator
        A fitted tree-based sklearn model with a `feature_importances_` attribute.
    X : pd.DataFrame
        Feature matrix used for SHAP computation.
    y : np.ndarray
        Target values (used for display only; not needed for SHAP computation).
    sample_size : int, optional
        Number of rows to sample for SHAP computation. Default is 200.
    random_state : int, optional
        Random seed for reproducible sampling. Default is 42.
    feature_names : list of str, optional
        Feature names to display. Defaults to X.columns.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns: Feature, MDI_Importance, MDI_Rank,
        SHAP_Importance, SHAP_Rank, Rank_Difference.
        Also displays a side-by-side bar chart.

    Example
    -------
    >>> comparison = compare_importance(best_rf, X_test, y_test)
    >>> print(comparison)
    """
    if feature_names is None:
        feature_names = X.columns.tolist()

    # MDI importance
    mdi = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)

    # SHAP importance
    X_sample = X.sample(min(sample_size, len(X)), random_state=random_state)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    shap_imp = pd.Series(
        np.abs(shap_values).mean(axis=0), index=feature_names
    ).sort_values(ascending=False)

    # Build comparison DataFrame
    comparison = pd.DataFrame({
        "MDI_Importance": mdi,
        "MDI_Rank": mdi.rank(ascending=False).astype(int),
        "SHAP_Importance": shap_imp,
        "SHAP_Rank": shap_imp.rank(ascending=False).astype(int),
    })
    comparison["Rank_Difference"] = (
        comparison["MDI_Rank"] - comparison["SHAP_Rank"]
    )
    comparison = comparison.sort_values("SHAP_Rank")

    # Side-by-side bar chart
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    mdi.sort_values().plot(kind="barh", ax=axes[0], color="steelblue")
    axes[0].set_title("MDI Feature Importance", fontsize=13)
    axes[0].set_xlabel("Importance")

    shap_imp.sort_values().plot(kind="barh", ax=axes[1], color="coral")
    axes[1].set_title("SHAP Feature Importance (mean |SHAP|)", fontsize=13)
    axes[1].set_xlabel("Mean |SHAP value|")

    plt.suptitle("MDI vs SHAP Importance Ranking", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()

    print("\nRanking Comparison (sorted by SHAP rank):")
    print(comparison.round(4).to_string())

    diverged = comparison[comparison["Rank_Difference"].abs() >= 2]
    if not diverged.empty:
        print(f"\nFeatures with rank divergence >= 2 positions:")
        print(diverged[["MDI_Rank", "SHAP_Rank", "Rank_Difference"]].to_string())

    return comparison
