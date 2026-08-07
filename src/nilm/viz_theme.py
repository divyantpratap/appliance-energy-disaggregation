"""Shared portfolio chart theme (vendored from energy-viz-lab)."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt

# Colorblind-safe categorical palette (max 6 series)
PALETTE: Sequence[str] = (
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#CC79A7",  # magenta
    "#56B4E9",  # sky
    "#D55E00",  # vermillion
)

LIGHT = {
    "figure.facecolor": "#FFFFFF",
    "axes.facecolor": "#FFFFFF",
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "grid.color": "#DDDDDD",
}

DARK = {
    "figure.facecolor": "#0E1117",
    "axes.facecolor": "#0E1117",
    "axes.edgecolor": "#AAAAAA",
    "axes.labelcolor": "#EEEEEE",
    "text.color": "#EEEEEE",
    "xtick.color": "#CCCCCC",
    "ytick.color": "#CCCCCC",
    "grid.color": "#333333",
}


def apply_theme(dark: bool = False) -> None:
    """Apply the portfolio house style to matplotlib."""
    base = {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.grid": True,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "axes.prop_cycle": mpl.cycler(color=list(PALETTE)),
    }
    base.update(DARK if dark else LIGHT)
    mpl.rcParams.update(base)


def save_figure(path, fig=None, width_px: int = 1600) -> None:
    """Save current (or given) figure at ~1600px wide, 2x DPI feel."""
    fig = fig or plt.gcf()
    w_in = width_px / fig.dpi
    fig.set_size_inches(w_in, fig.get_size_inches()[1] * (w_in / fig.get_size_inches()[0]))
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
