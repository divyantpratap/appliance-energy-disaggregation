"""Interactive, transparent NILM energy-disaggregation demonstration."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nilm.demo import (  # noqa: E402
    APPLIANCES,
    energy_kwh,
    estimate_appliances,
    mae_by_appliance,
    simulate_household,
)

st.set_page_config(page_title="NILM Energy Disaggregation", page_icon="⌁", layout="wide")

with st.sidebar:
    st.header("Household simulation")
    seed = st.slider("Household profile", 1, 100, 42)
    noise = st.slider("Meter noise (W)", 0, 60, 18)
    window = st.slider("Visible hours", 2, 24, 12)
    st.divider()
    st.caption(
        "This public demo uses synthetic appliance ground truth and an explainable "
        "rules baseline. It does not claim production model accuracy."
    )

st.title("NILM Energy Disaggregation")
st.caption("See how a single smart-meter trace can be separated into appliance-level demand.")

actual = simulate_household(seed=seed, noise_w=float(noise))
predicted = estimate_appliances(actual)
energy = energy_kwh(actual)
mae = mae_by_appliance(actual, predicted)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Whole-home energy", f"{actual.aggregate_w.sum()/60/1000:.1f} kWh")
c2.metric("Largest appliance", energy.idxmax().removesuffix("_w").replace("_", " ").title())
c3.metric("Kettle events", int((actual.kettle_w.diff() > 1000).sum()))
c4.metric("Baseline mean MAE", f"{mae.mean():.0f} W")

tab_signal, tab_energy, tab_method = st.tabs(["Signal explorer", "Energy breakdown", "How it works"])
with tab_signal:
    display_rows = window * 60
    view = actual.iloc[:display_rows].set_index("timestamp")
    st.line_chart(
        view[["aggregate_w", "fridge_w", "kettle_w", "washing_machine_w", "lighting_w"]],
        color=["#17211d", "#2f7d67", "#e07a32", "#5865a8", "#c79a2b"],
    )
    appliance = st.selectbox("Inspect baseline estimate", APPLIANCES, format_func=lambda x: x.removesuffix("_w").replace("_", " ").title())
    comparison = pd.DataFrame(
        {
            "actual": actual[appliance].iloc[:display_rows].to_numpy(),
            "estimated": predicted[appliance].iloc[:display_rows].to_numpy(),
        },
        index=actual.timestamp.iloc[:display_rows],
    )
    st.line_chart(comparison, color=["#2f7d67", "#e07a32"])

with tab_energy:
    breakdown = pd.DataFrame(
        {
            "appliance": [name.removesuffix("_w").replace("_", " ").title() for name in APPLIANCES],
            "energy_kwh": [energy[name] for name in APPLIANCES],
            "baseline_mae_w": [mae[name] for name in APPLIANCES],
        }
    )
    st.bar_chart(breakdown.set_index("appliance")["energy_kwh"], color="#2f7d67")
    st.dataframe(breakdown.round(2), use_container_width=True, hide_index=True)

with tab_method:
    st.markdown(
        """
        **What the baseline sees:** only the aggregate smart-meter series.

        1. A rolling median estimates the local background load.
        2. Short residual spikes above 1,050 W are classified as kettle events.
        3. Medium-duration variable loads are assigned to the washing machine.
        4. Evening and early-morning residual demand is assigned to lighting.
        5. Remaining periodic demand is treated as refrigeration.

        This transparent baseline is intentionally imperfect. A production NILM study
        would compare it with a trained seq2point model on held-out households.
        """
    )
