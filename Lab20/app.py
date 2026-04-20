"""
Streamlit app — Interactive Time Series Decomposition Explorer
Run with: streamlit run app.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

from fredapi import Fred
from statsmodels.tsa.seasonal import seasonal_decompose
from src.decompose import (run_stl, run_mstl, block_bootstrap_trend,
                            test_stationarity, detect_breaks)

@st.cache_data(show_spinner='Fetching from FRED...')
def fetch_series(api_key: str, series_id: str) -> pd.Series:
    fred = Fred(api_key=api_key)
    s = fred.get_series(series_id).dropna()
    s.index = pd.DatetimeIndex(s.index)
    freq = pd.infer_freq(s.index)
    if freq:
        s.index.freq = freq
    return s

st.set_page_config(page_title='TS Decomposition Explorer', layout='wide')
st.title('Time Series Decomposition Explorer')
st.caption('ECON 5200 — Lab 20')

with st.sidebar:
    st.header('Data')
    api_key       = st.text_input('FRED API Key', type='password')
    series_id     = st.text_input('FRED Series ID', value='RSXFSN')
    log_transform = st.checkbox('Log-transform (multiplicative data)', value=True)

    st.header('Method')
    method = st.selectbox('Decomposition', ['STL', 'MSTL', 'Classical'])

    st.header('Parameters')
    period  = st.slider('Primary period', 2, 52, 12)
    robust  = st.checkbox('Robust STL', value=True)
    penalty = st.slider('Break detection penalty', 1, 50, 2)

    if method == 'MSTL':
        period2 = st.slider('Second period', 2, 365, 52)

    go_btn = st.button('Run', type='primary')

if not go_btn:
    st.info('Enter your FRED API key and series ID in the sidebar, then click Run.')
    st.stop()

if not api_key:
    st.error('FRED API key required.')
    st.stop()

try:
    series = fetch_series(api_key, series_id)
except Exception as e:
    st.error(f'Could not fetch {series_id}: {e}')
    st.stop()

st.subheader(f'{series_id} — {len(series)} observations '
             f'({series.index[0].date()} to {series.index[-1].date()})')

try:
    if method == 'STL':
        result = run_stl(series, period=period, log_transform=log_transform, robust=robust)
        trend, resid = result.trend, result.resid
        seasonal_cols = {'Seasonal': result.seasonal}
    elif method == 'MSTL':
        result = run_mstl(series, periods=[period, period2], log_transform=log_transform)
        trend, resid = result.trend, result.resid
        seasonal_cols = {f'Seasonal (p={p})': result.seasonal.iloc[:, i]
                         for i, p in enumerate([period, period2])}
    else:
        work = np.log(series) if log_transform and (series > 0).all() else series
        result = seasonal_decompose(work, model='additive', period=period, extrapolate_trend='freq')
        trend, resid = result.trend, result.resid
        seasonal_cols = {'Seasonal': result.seasonal}
except Exception as e:
    st.error(f'Decomposition failed: {e}')
    st.stop()

work_plot = np.log(series) if log_transform and (series > 0).all() else series
n_rows = 3 + len(seasonal_cols)
fig = make_subplots(rows=n_rows, cols=1, shared_xaxes=True,
                    subplot_titles=['Observed', 'Trend'] +
                                   list(seasonal_cols.keys()) + ['Residual'])
fig.add_trace(go.Scatter(x=series.index, y=work_plot, line=dict(color='#2c3e50', width=1)), row=1, col=1)
fig.add_trace(go.Scatter(x=trend.index, y=trend, line=dict(color='#e67e22', width=2)), row=2, col=1)
for r, (name, s) in enumerate(seasonal_cols.items(), start=3):
    fig.add_trace(go.Scatter(x=s.index, y=s, line=dict(width=0.8)), row=r, col=1)
fig.add_trace(go.Scatter(x=resid.index, y=resid, line=dict(color='#c0392b', width=0.8)), row=n_rows, col=1)
fig.update_layout(height=200 * n_rows, showlegend=False,
                  title_text=f'{method} Decomposition — {series_id}')
st.plotly_chart(fig, use_container_width=True)

st.subheader('Stationarity Tests')
col1, col2 = st.columns(2)
for label, s in [('Levels', series), ('First Difference', series.diff().dropna())]:
    res = test_stationarity(s)
    tbl = pd.DataFrame({'Test': ['ADF', 'KPSS'],
                         'Statistic': [f"{res['adf_stat']:.4f}", f"{res['kpss_stat']:.4f}"],
                         'p-value': [f"{res['adf_p']:.4f}", f"{res['kpss_p']:.4f}"]})
    with (col1 if label == 'Levels' else col2):
        st.markdown(f'**{label}** — verdict: `{res["verdict"].upper()}`')
        st.dataframe(tbl, hide_index=True)

st.subheader('Structural Breaks (PELT)')
breaks = detect_breaks(series.pct_change().dropna() * 100, pen=penalty)
fig_s = go.Figure()
fig_s.add_trace(go.Scatter(x=series.index, y=work_plot, line=dict(color='#2c3e50', width=0.8)))
for b in breaks:
    fig_s.add_vline(x=b, line=dict(color='red', dash='dash', width=1))
fig_s.update_layout(title=f'{len(breaks)} break(s) detected (penalty={penalty})', height=350)
st.plotly_chart(fig_s, use_container_width=True)
if breaks:
    st.write('Break dates:', [str(b.date()) for b in breaks])
