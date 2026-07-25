"""Feature engineering."""
from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a model-ready feature frame (placeholder for domain logic)."""
    out = df.copy()
    numeric = out.select_dtypes(include="number")
    if numeric.shape[1] == 0:
        out["row_id"] = range(len(out))
        return out
    return numeric
