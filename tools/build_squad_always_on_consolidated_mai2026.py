#!/usr/bin/env python3
"""Wrapper legado — delega para loterias2026/lotes/20260511/scripts/build_consolidated.py."""
from __future__ import annotations

import runpy
from pathlib import Path

_TARGET = (
    Path(__file__).resolve().parents[1]
    / "loterias2026/lotes/20260511/scripts/build_consolidated.py"
)

if __name__ == "__main__":
    runpy.run_path(str(_TARGET), run_name="__main__")
