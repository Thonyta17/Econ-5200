"""
forecast_evaluation.py — Forecast Evaluation & Backtesting Module
ECON 5200, Lab 21
"""

import numpy as np
import pandas as pd
from typing import Callable


def compute_mase(
    actual: np.ndarray,
    forecast: np.ndarray,
    insample: np.ndarray,
    m: int = 1
) -> float:
    """Compute Mean Absolute Scaled Error.

    MASE < 1: model beats naive seasonal benchmark.
    MASE > 1: naive benchmark is better.

    Args:
        actual: True out-of-sample values
        forecast: Model predictions (same length as actual)
        insample: In-sample (training) data for naive baseline
        m: Seasonal period (1=random walk, 12=monthly seasonal)

    Returns:
        MASE score (float)
    """
    mae_forecast = np.mean(np.abs(actual - forecast))
    naive_errors = insample[m:] - insample[:-m]
    mae_naive = np.mean(np.abs(naive_errors))
    return mae_forecast / mae_naive


def backtest_expanding_window(
    series: pd.Series,
    model_fn: Callable,
    min_train: int = 120,
    horizon: int = 12,
    step: int = 12
) -> pd.DataFrame:
    """Expanding-window time series backtest.

    Args:
        series: Full series with DatetimeIndex
        model_fn: Callable(train) -> np.ndarray of length horizon
        min_train: Minimum training observations
        horizon: Forecast horizon per iteration
        step: Observations added per iteration

    Returns:
        DataFrame with columns: origin, horizon, actual, forecast,
        error, abs_error, mase
    """
    records = []
    for origin in range(min_train, len(series) - horizon + 1, step):
        train = series.iloc[:origin]
        actual = series.iloc[origin:origin + horizon].values
        forecast = model_fn(train)
        errors = actual - forecast
        mase = compute_mase(actual, forecast, train.values, m=1)
        for h in range(horizon):
            records.append({
                'origin': series.index[origin],
                'horizon': h + 1,
                'actual': actual[h],
                'forecast': forecast[h],
                'error': errors[h],
                'abs_error': abs(errors[h]),
                'mase': mase
            })
    return pd.DataFrame(records)


if __name__ == '__main__':
    print('forecast_evaluation.py loaded successfully.')
