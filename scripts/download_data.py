#!/usr/bin/env python3
"""Fetch the public dataset into data/raw (credentials never committed)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nilm.config import RAW_DIR, SAMPLE_DIR

print("=" * 60)
print("NILM Energy Disaggregation — data setup")
print("=" * 60)
print(f"Source: https://data.ukedc.rl.ac.uk/browse/edc/efficiency/residential/EnergyConsumption/Domestic/UK-DALE-2017")
print(f"Place files under: {RAW_DIR}")
print("Sample for CI already at:", SAMPLE_DIR / "sample.csv")
print("Do NOT commit raw downloads.")
RAW_DIR.mkdir(parents=True, exist_ok=True)
print("Ready. Implement provider-specific download here when credentials exist.")
