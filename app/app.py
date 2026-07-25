"""Minimal Streamlit shell for NILM Energy Disaggregation."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nilm.data import load_sample

st.set_page_config(page_title="NILM Energy Disaggregation", layout="wide")
st.title("NILM Energy Disaggregation")
st.caption("Split a household's whole-home smart-meter signal into per-appliance energy use — the core problem behind modern energy analytics.")
st.info("Scaffold UI — wire the full demo after the model pipeline lands.")
df = load_sample()
st.dataframe(df.head(50), use_container_width=True)
