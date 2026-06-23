#!/usr/bin/env python3
"""Wrapper — delega ao build canônico em loterias2026/scripts/build_dossier_completo.py."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

_PROJECT = Path(__file__).resolve().parents[1]
_CANONICAL = _PROJECT.parent / "loterias2026/scripts/build_dossier_completo.py"

if __name__ == "__main__":
    argv = list(sys.argv[1:])
    if "--project-root" not in argv:
        argv = ["--project-root", str(_PROJECT), *argv]
    sys.argv = [str(_CANONICAL), *argv]
    runpy.run_path(str(_CANONICAL), run_name="__main__")
