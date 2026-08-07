"""Baseline + main model training entrypoint."""

from __future__ import annotations

import json

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split

from .config import ASSETS_DIR, SEED
from .data import load_sample, validate
from .evaluate import classification_report, regression_report
from .features import build_features


def _is_classification(y: np.ndarray) -> bool:
    return y.dtype.kind in "iu" and len(np.unique(y)) <= 8


def train() -> dict:
    """Train a simple baseline on the sample so `make run` works immediately."""
    rng = np.random.default_rng(SEED)
    df = validate(load_sample())
    feats = build_features(df)
    # Prefer an explicit target column when present
    if "target" in df.columns:
        y = df["target"].to_numpy()
        X = feats.drop(columns=["target"], errors="ignore").to_numpy()
    else:
        X = feats.to_numpy()
        # synthetic target from first column for smoke training
        y = X[:, 0] + rng.normal(0, 0.1, size=len(X))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=SEED)
    if _is_classification(y_train):
        model = LogisticRegression(max_iter=500, random_state=SEED)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = classification_report(y_test, pred)
        kind = "classification"
    else:
        model = LinearRegression()
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = regression_report(y_test, pred)
        kind = "regression"

    payload = {
        "project": "appliance-energy-disaggregation",
        "task": kind,
        "baseline": "sklearn linear/logistic smoke baseline",
        "main_planned": "seq2point CNN (PyTorch) per appliance",
        "metrics": metrics,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "note": "Replace with the full pipeline described in the README.",
    }
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "metrics.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))
    return payload


if __name__ == "__main__":
    train()
