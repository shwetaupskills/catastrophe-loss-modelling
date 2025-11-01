# 🌪️ Catastrophe Loss Modelling Dashboard

### Author: Shweta Dwivedi

This project simulates financial losses from natural catastrophe events using **Monte Carlo simulation** and visualizes the results through an **interactive Streamlit dashboard**.

---

## 🎯 Objective
Estimate:
- **Expected Annual Loss (EAL)**
- **Probable Maximum Loss (PML)** (95% and 99%)
under different assumptions of hazard frequency, severity, and insurance structures.

---

## 🧮 Simulation Framework

| Parameter | Description | Example |
|------------|--------------|----------|
| Iterations | Simulated years | 10,000 |
| Portfolio Value | Total insured exposure | ₹1,000,000,000 |
| Mean Damage Ratio | Average severity | 2% |
| Std. Deviation | Variability in severity | 5% |
| Event Frequency | Poisson-distributed | λ = 2 per year |

---

## 🏦 Insurance Structure
The model supports:
- **Deductibles / Policy Limits**
- **Reinsurance retention and limits**
- Gross vs. net loss comparison

---

## 📊 Dashboard Features
- Real-time adjustment of simulation parameters
- Live histograms of annual losses
- Comparative metrics table (Gross / After Insurance / After Reinsurance)
- Analytical insights for interpretation

---

## 🚀 Run Locally
```bash
pip install streamlit plotly numpy pandas
streamlit run catastrophe_dashboard.py
