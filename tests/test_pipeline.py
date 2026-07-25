from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nilm.config import SAMPLE_DIR, SEED
from nilm.data import load_sample, validate
from nilm.evaluate import classification_report, regression_report
from nilm.features import build_features
from nilm.model import train
from nilm.viz import make_hero


def test_sample_exists():
    assert (SAMPLE_DIR / "sample.csv").exists()


def test_load_and_validate():
    df = validate(load_sample())
    assert len(df) >= 10


def test_features_numeric():
    feats = build_features(load_sample())
    assert len(feats) == len(load_sample())


def test_metrics_helpers():
    y = np.array([0.0, 1.0, 2.0, 3.0])
    pred = y + 0.1
    reg = regression_report(y, pred)
    assert "mae" in reg
    cls = classification_report(np.array([0, 1, 0, 1]), np.array([0, 1, 1, 1]))
    assert "f1_macro" in cls


def test_train_smoke(tmp_path, monkeypatch):
    import nilm.model as model_mod
    monkeypatch.setattr(model_mod, "ASSETS_DIR", tmp_path)
    metrics = train()
    assert "metrics" in metrics
    assert (tmp_path / "metrics.json").exists()


def test_hero_figure(tmp_path):
    out = make_hero(tmp_path / "hero.png")
    assert out.exists() and out.stat().st_size > 0


def test_seed_constant():
    assert SEED == 42
