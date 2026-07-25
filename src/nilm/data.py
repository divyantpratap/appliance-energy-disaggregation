"""Load and validate datasets (sample by default)."""
from __future__ import annotations

import pandas as pd

from .config import SAMPLE_DIR, SEED


def load_sample() -> pd.DataFrame:
    """Load the committed smoke-test sample."""
    path = SAMPLE_DIR / "sample.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing sample at {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("Sample dataset is empty")
    return df


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Basic schema sanity checks."""
    if df.isna().all(axis=None):
        raise ValueError("Dataset contains only NaNs")
    return df.reset_index(drop=True)
