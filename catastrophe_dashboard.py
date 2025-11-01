 -----------------------------------------------------------
# Catastrophe Loss Modelling Dashboard
# Author: Shweta Dwivedi
# Objective: Interactive Monte Carlo Simulation for EAL & PML
# -----------------------------------------------------------

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------------
st.sidebar.title("📊 Simulation Parameters")

num_years = st.sidebar.number_input("Number of simulated years", 1000, 100000, 10000, step=1000)
portfolio_value = st.sidebar.number_input("Portfolio Value (₹)", 1e6, 5e9, 1e9, step=1e8)
mean_damage_ratio = st.sidebar.slider("Mean Damage Ratio", 0.0, 0.2, 0.02, 0.005)
std_damage_ratio = st.sidebar.slider("Std. Dev. of Damage Ratio", 0.0, 0.2, 0.05, 0.005)
lambda_events = st.sidebar.slider("Average Events per Year (λ)", 0.5, 5.0, 2.0, 0.5)

st.sidebar.title("🏦 Insurance Structure")
deductible = st.sidebar.number_input("Deductible (₹)", 0, 500_000_000, 10_000_000, step=1_000_000)
policy_limit = st.sidebar.number_input("Policy Limit (₹)", 0, 1_000_000_000, 100_000_000, step=10_000_000)
reins_retention = st.sidebar.number_input("Reinsurance Retention (₹)", 0, 1_000_000_000, 100_000_000, step=10_000_000)
reins_limit = st.sidebar.number_input("Reinsurance Limit (₹)", 0, 1_000_000_000, 200_000_000, step=10_000_000)

# -----------------------------------------------------------
# Simulation Core
# -----------------------------------------------------------
np.random.seed(42)

# --- Single Event per Year Model ---
damage_ratios_single = np.random.normal(mean_damage_ratio, std_damage_ratio, num_years)
damage_ratios_single = np.clip(damage_ratios_single, 0, 1)
annual_losses_single = damage_ratios_single * portfolio_value

# --- Multiple Events per Year Model ---
annual_losses_multi = []
for _ in range(num_years):
    n_events = np.random.poisson(lambda_events)
    event_damages = np.random.normal(mean_damage_ratio, std_damage_ratio, n_events)
    event_damages = np.clip(event_damages, 0, 1)
    total_loss = np.sum(event_damages) * portfolio_value
    annual_losses_multi.append(total_loss)

annual_losses_multi = np.array(annual_losses_multi)

# -----------------------------------------------------------
# Insurance Layers
# -----------------------------------------------------------
insured_losses = np.maximum(annual_losses_multi - deductible, 0)
insured_losses = np.minimum(insured_losses, policy_limit)
reinsurer_payout = np.clip(annual_losses_multi - reins_retention, 0, reins_limit)
insurer_net_loss = insured_losses - reinsurer_payout

# -----------------------------------------------------------
# Key Metrics
# -----------------------------------------------------------
def loss_metrics(losses):
    return {
        "EAL": np.mean(losses),
        "PML_95": np.percentile(losses, 95),
        "PML_99": np.percentile(losses, 99)
    }

metrics = {
    "Gross Loss": loss_metrics(annual_losses_multi),
    "After Insurance": loss_metrics(insured_losses),
    "After Reinsurance": loss_metrics(insurer_net_loss)
}

metrics_df = pd.DataFrame(metrics).T.round(0)
metrics_df = metrics_df.rename(columns={"EAL": "Expected Annual Loss (₹)", 
                                        "PML_95": "95% PML (₹)", 
                                        "PML_99": "99% PML (₹)"})

# -----------------------------------------------------------
# Dashboard Layout
# -----------------------------------------------------------
st.title("🌪️ Catastrophe Loss Modelling Dashboard")
st.markdown("""
This dashboard simulates catastrophe risk losses using **Monte Carlo simulation**.
It estimates:
- **Expected Annual Loss (EAL)**
- **Probable Maximum Loss (PML)** at 95% and 99%
- Effects of **deductibles, policy limits, and reinsurance**
""")

st.header("📈 Portfolio Loss Metrics")
st.dataframe(metrics_df.style.format("{:,.0f}"))

# -----------------------------------------------------------
# Visualization
# -----------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Histogram(x=annual_losses_multi, name="Gross Loss", opacity=0.6))
fig.add_trace(go.Histogram(x=insured_losses, name="After Insurance", opacity=0.6))
fig.add_trace(go.Histogram(x=insurer_net_loss, name="After Reinsurance", opacity=0.6))

fig.update_layout(
    title="Distribution of Simulated Annual Losses",
    xaxis_title="Annual Loss (₹)",
    yaxis_title="Frequency",
    barmode="overlay",
    legend=dict(title="Loss Type"),
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------
# Insights Section
# -----------------------------------------------------------
st.header("💡 Analytical Insights")
st.markdown(f"""
- **EAL** represents the long-run average expected loss per year — a key pricing measure.
- **PML (95%, 99%)** represents high-severity, low-frequency tail risk.
- Applying **deductibles** and **policy limits** reduces insurer exposure.
- **Reinsurance** further reduces volatility and limits extreme losses.
- Increasing `λ` (event frequency) or `mean_damage_ratio` increases both EAL and PML.
""")
