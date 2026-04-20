"""
decompose.py — Extended Time Series Decomposition & Diagnostics Module
ECON 5200, Lab 20
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL, MSTL
from statsmodels.tsa.stattools import adfuller, kpss
import ruptures as rpt


def run_stl(series: pd.Series, period: int = 12,
            log_transform: bool = True, robust: bool = True):
    if log_transform:
        if (series <= 0).any():
            raise ValueError('Series has non-positive values; cannot log-transform.')
        series = np.log(series)
    return STL(series, period=period, robust=robust).fit()


def run_mstl(series: pd.Series, periods: list, log_transform: bool = True):
    """
    Apply MSTL decomposition for multiple seasonal periods.

    MSTL works iteratively: it removes the first seasonal component,
    fits STL on the remainder to extract the second, and so on.
    Each pass isolates one cycle without contaminating the others.
    """
    if log_transform:
        if (series <= 0).any():
            raise ValueError('Series has non-positive values; cannot log-transform.')
        series = np.log(series)
    return MSTL(series, periods=periods).fit()


def block_bootstrap_trend(series: pd.Series, n_bootstrap: int = 200,
                           block_size: int = 8, period: int = 12,
                           log_transform: bool = True) -> dict:
    """
    Estimate trend uncertainty via moving block bootstrap.

    Why block bootstrap vs i.i.d. bootstrap:
        Residuals from economic time series are autocorrelated.
        i.i.d. bootstrap shuffles residuals independently, destroying
        that structure. Block bootstrap draws contiguous chunks,
        preserving within-block autocorrelation so resampled series
        behave like real data.
    """
    work = np.log(series) if log_transform and (series > 0).all() else series.copy()
    base = STL(work, period=period, robust=True).fit()
    resid = base.resid.values
    n = len(work)
    boot_trends = np.zeros((n_bootstrap, n))

    for b in range(n_bootstrap):
        boot_resid = np.zeros(n)
        idx = 0
        while idx < n:
            start = np.random.randint(0, n - block_size + 1)
            block = resid[start:start + block_size]
            end = min(idx + block_size, n)
            boot_resid[idx:end] = block[:end - idx]
            idx = end
        boot_series = pd.Series(
            base.trend.values + base.seasonal.values + boot_resid,
            index=work.index
        )
        boot_series.index.freq = work.index.freq
        boot_trends[b] = STL(boot_series, period=period, robust=True).fit().trend.values

    return {
        'trend': base.trend,
        'lower': pd.Series(np.percentile(boot_trends, 5, axis=0), index=work.index),
        'upper': pd.Series(np.percentile(boot_trends, 95, axis=0), index=work.index),
    }


def test_stationarity(series: pd.Series, alpha: float = 0.05) -> dict:
    adf_stat, adf_p, _, _, _, _ = adfuller(series, autolag='AIC', regression='ct')
    kpss_stat, kpss_p, _, _ = kpss(series, regression='ct', nlags='auto')
    adf_rej, kpss_rej = adf_p < alpha, kpss_p < alpha
    if adf_rej and not kpss_rej:
        verdict = 'stationary'
    elif not adf_rej and kpss_rej:
        verdict = 'non-stationary'
    elif adf_rej and kpss_rej:
        verdict = 'contradictory'
    else:
        verdict = 'inconclusive'
    return {'adf_stat': adf_stat, 'adf_p': adf_p,
            'kpss_stat': kpss_stat, 'kpss_p': kpss_p, 'verdict': verdict}


def detect_breaks(series: pd.Series, pen: float = 10) -> list:
    """
    Detect structural breaks using PELT.

    PELT's penalty parameter controls the bias-variance tradeoff:
        Low penalty  → many breaks (overfits noise)
        High penalty → few breaks (may miss real shifts)
    """
    signal = series.values
    breakpoints = rpt.Pelt(model='rbf').fit(signal).predict(pen=pen)
    return [series.index[i] for i in breakpoints if i < len(signal)]


if __name__ == '__main__':
    print('decompose.py loaded successfully.')