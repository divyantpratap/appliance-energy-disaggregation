"""Paths and experiment parameters."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SAMPLE_DIR = DATA_DIR / "sample"
ASSETS_DIR = ROOT / "assets"
SEED = 42
PROJECT = "01-nilm-energy-disaggregation"
