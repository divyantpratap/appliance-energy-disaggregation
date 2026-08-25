"""Deterministic NILM demonstration signals and transparent baseline estimates."""
from __future__ import annotations

import numpy as np
import pandas as pd

APPLIANCES = ("fridge_w", "kettle_w", "washing_machine_w", "lighting_w")


def simulate_household(seed: int = 42, noise_w: float = 18.0) -> pd.DataFrame:
    """Return one day of minute-level aggregate and appliance ground truth."""
    rng = np.random.default_rng(seed)
    points = 24 * 60
    minute = np.arange(points)
    timestamp = pd.date_range("2025-01-15", periods=points, freq="min")

    fridge = np.where((minute % 48) < 18, 115.0, 4.0)
    kettle = np.zeros(points)
    for start in (7 * 60 + 22, 13 * 60 + 8, 18 * 60 + 45, 21 * 60 + 12):
        kettle[start : start + 4] = 1850.0

    washing = np.zeros(points)
    wash_start = 10 * 60 + 15
    phase = np.arange(82)
    washing[wash_start : wash_start + len(phase)] = (
        180 + 260 * (np.sin(phase / 7) ** 2) + np.where((phase > 42) & (phase < 53), 750, 0)
    )

    hour = minute / 60
    lighting = np.where((hour >= 18.2) & (hour <= 23.4), 210.0, 0.0)
    lighting += np.where((hour >= 5.8) & (hour <= 7.1), 95.0, 0.0)
    baseline = 72 + 11 * np.sin(minute / 95)
    aggregate = baseline + fridge + kettle + washing + lighting + rng.normal(0, noise_w, points)

    return pd.DataFrame(
        {
            "timestamp": timestamp,
            "aggregate_w": np.clip(aggregate, 0, None),
            "fridge_w": fridge,
            "kettle_w": kettle,
            "washing_machine_w": washing,
            "lighting_w": lighting,
            "baseline_w": baseline,
        }
    )


def estimate_appliances(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply an explainable rules baseline to aggregate power only."""
    aggregate = frame["aggregate_w"].to_numpy(float)
    series = pd.Series(aggregate)
    smooth = series.rolling(7, center=True, min_periods=1).median().to_numpy()
    kettle = np.where(aggregate - smooth > 1050, np.clip(aggregate - smooth, 0, 2100), 0.0)
    residual = np.clip(aggregate - kettle, 0, None)
    washing = np.where(
        (residual > 290) & (residual < 1250),
        np.clip(residual - 155, 0, 1000),
        0.0,
    )
    hour = pd.to_datetime(frame["timestamp"]).dt.hour.to_numpy()
    lighting = np.where(((hour >= 18) | (hour <= 7)) & (residual > 170), np.minimum(residual - 150, 260), 0.0)
    fridge = np.where((residual - lighting - washing) > 125, 112.0, 4.0)
    return pd.DataFrame(
        {
            "timestamp": frame["timestamp"],
            "fridge_w": fridge,
            "kettle_w": kettle,
            "washing_machine_w": washing,
            "lighting_w": lighting,
        }
    )


def energy_kwh(frame: pd.DataFrame, columns: tuple[str, ...] = APPLIANCES) -> pd.Series:
    """Convert minute-level watts into kWh totals."""
    return frame.loc[:, list(columns)].sum() / 60 / 1000


def mae_by_appliance(actual: pd.DataFrame, predicted: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            column: float(np.mean(np.abs(actual[column].to_numpy() - predicted[column].to_numpy())))
            for column in APPLIANCES
        }
    )
