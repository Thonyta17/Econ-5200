"""
clustering_utils.py — Reusable Clustering Pipeline Module
ECON 5200, Lab 22
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from typing import List, Dict


def run_kmeans_pipeline(
    df: pd.DataFrame,
    features: List[str],
    k: int,
    random_state: int = 42
) -> Dict:
    """End-to-end K-Means pipeline: standardize, fit, return labels + metadata."""
    X = df[features].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = KMeans(n_clusters=k, init='k-means++', n_init='auto', random_state=random_state)
    labels = model.fit_predict(X_scaled)
    sil = silhouette_score(X_scaled, labels)
    return {
        'labels': labels,
        'scaler': scaler,
        'model': model,
        'X_scaled': X_scaled,
        'silhouette': sil,
        'inertia': model.inertia_
    }


def evaluate_k_range(
    X: np.ndarray,
    k_range: range,
    random_state: int = 42
) -> pd.DataFrame:
    """Compute WCSS and silhouette scores for a range of K values."""
    records = []
    for k in k_range:
        km = KMeans(n_clusters=k, init='k-means++', n_init='auto', random_state=random_state)
        km.fit(X)
        sil = silhouette_score(X, km.labels_)
        records.append({'k': k, 'wcss': km.inertia_, 'silhouette': sil})
    return pd.DataFrame(records)


def plot_pca_clusters(
    X: np.ndarray,
    labels: np.ndarray,
    feature_names: List[str]
) -> None:
    """PCA 2D scatter with cluster coloring + explained variance annotation."""
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='Set1', alpha=0.7, s=40)
    ax.set_title('PCA Cluster Projection', fontsize=13)
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
    plt.colorbar(scatter, ax=ax, label='Cluster')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    from sklearn.datasets import make_blobs
    X_test, _ = make_blobs(n_samples=200, centers=3, n_features=5, random_state=0)
    df_test = pd.DataFrame(X_test, columns=[f'f{i}' for i in range(5)])

    result = run_kmeans_pipeline(df_test, [f'f{i}' for i in range(5)], k=3)
    print(f'Labels shape: {result["labels"].shape}')
    print(f'Silhouette: {result["silhouette"]:.4f}')

    eval_df = evaluate_k_range(result['X_scaled'], range(2, 8))
    print(eval_df)

    plot_pca_clusters(result['X_scaled'], result['labels'], [f'f{i}' for i in range(5)])
    print('Self-test passed.')
