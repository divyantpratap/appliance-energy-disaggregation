"""Figure generation for README assets."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .config import ASSETS_DIR, SEED
from .viz_theme import apply_theme, save_figure


def make_hero(path: Path | None = None) -> Path:
    """Placeholder hero until real experiment figures land."""
    apply_theme(dark=False)
    rng = np.random.default_rng(SEED)
    fig, ax = plt.subplots()
    x = np.arange(24)
    ax.plot(x, rng.normal(size=24).cumsum(), label="series")
    ax.set_title("NILM Energy Disaggregation: placeholder hero (replace after make run)")
    ax.set_xlabel("index")
    ax.set_ylabel("value")
    ax.legend()
    out = path or (ASSETS_DIR / "hero.png")
    save_figure(out, fig)
    return out
