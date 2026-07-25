#!/usr/bin/env python3
"""Regenerate README figures into assets/."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nilm.viz import make_hero

if __name__ == "__main__":
    path = make_hero()
    print(f"Wrote {path}")
