
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Cigarette Tax Policy Dashboard", layout="wide")
st.title("Consulting Report: Causal Effect of Cigarette Prices on Consumption")
st.markdown("""
**Research question:** Does cigarette price (driven by state excise taxes) causally reduce consumption?  
**Method:** 2SLS (Instrumental Variables) | **Data:** CigarettesSW, 48 U.S. states, 1995
""")

# --- Pre-computed 2SLS results (update after running notebook) ---
BASELINE_ELASTICITY = -1.08   # TODO: replace with causal_estimate
BASELINE_SE         =  0.31   # TODO: replace with causal_se
PASS_THROUGH        =  0.9    # ~90% of tax increase passed to price (literature)
AVG_PRICE_1995      =  158.0  # average real price cents/pack, 1995

# --- Sidebar: What-If Controls ---
st.sidebar.header("What-If Scenarios")

tax_increase_pct = st.sidebar.slider(
    "Excise tax increase (%)",
    min_value=0, max_value=100, value=10, step=5
)

income_scenario = st.sidebar.selectbox(
    "Income scenario",
    ["Baseline (1995 levels)", "Low income (-20%)", "High income (+20%)"]
)

income_adj = {"Baseline (1995 levels)": 1.0,
              "Low income (-20%)": 0.8,
              "High income (+20%)": 1.2}[income_scenario]

# --- Compute What-If Estimate ---
price_pct_change  = tax_increase_pct * PASS_THROUGH
packs_pct_change  = BASELINE_ELASTICITY * (price_pct_change / 100) * 100
income_effect     = 0.5 * (income_adj - 1) * 100   # income elasticity ~ 0.5
total_pct_change  = packs_pct_change + income_effect
se_scaled         = abs(BASELINE_SE * (price_pct_change / 100) * 100)
ci_lower          = total_pct_change - 1.96 * se_scaled
ci_upper          = total_pct_change + 1.96 * se_scaled

# --- Display Results ---
col1, col2, col3 = st.columns(3)
col1.metric("Estimated Effect", f"{total_pct_change:.1f}%")
col2.metric("95% CI Lower", f"{ci_lower:.1f}%")
col3.metric("95% CI Upper", f"{ci_upper:.1f}%")

st.markdown(f"""
> **What-if interpretation:** A {tax_increase_pct}% excise tax increase raises prices by ~{price_pct_change:.1f}%,
> reducing per-capita packs sold by **{abs(total_pct_change):.1f}%** (95% CI: [{ci_lower:.1f}%, {ci_upper:.1f}%]).  
> *Key assumption: exclusion restriction holds — taxes affect consumption only through price.*
""")

# --- Uncertainty Visualization ---
tax_range  = np.arange(0, 105, 5)
price_chgs = tax_range * PASS_THROUGH
pack_chgs  = BASELINE_ELASTICITY * (price_chgs / 100) * 100 + income_effect
ses_range  = abs(BASELINE_SE * (price_chgs / 100) * 100)

fig = go.Figure()
fig.add_trace(go.Scatter(x=tax_range, y=pack_chgs + 1.96*ses_range,
    mode="lines", line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=tax_range, y=pack_chgs - 1.96*ses_range,
    mode="lines", line=dict(width=0), fill="tonexty",
    fillcolor="rgba(26,35,126,0.15)", name="95% CI"))
fig.add_trace(go.Scatter(x=tax_range, y=pack_chgs,
    mode="lines", line=dict(color="#1a237e", width=2.5), name="Estimated Effect"))
fig.add_vline(x=tax_increase_pct, line_dash="dash", line_color="red",
              annotation_text=f"Selected: {tax_increase_pct}%")
fig.add_hline(y=0, line_dash="dot", line_color="gray")
fig.update_layout(xaxis_title="Excise Tax Increase (%)",
                  yaxis_title="Change in Packs Sold (%)",
                  template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# --- Counterfactual Scenario ---
st.subheader("Counterfactual: What if the excise tax doubled?")
double_price_chg = AVG_PRICE_1995 * PASS_THROUGH
double_pack_chg  = BASELINE_ELASTICITY * (double_price_chg / AVG_PRICE_1995) * 100
double_se        = abs(BASELINE_SE * (double_price_chg / AVG_PRICE_1995) * 100)
double_ci        = (double_pack_chg - 1.96*double_se, double_pack_chg + 1.96*double_se)
st.write(f"If the average state excise tax doubled, per-capita packs sold would change by "
         f"**{double_pack_chg:.1f}%** (95% CI: [{double_ci[0]:.1f}%, {double_ci[1]:.1f}%]).")
