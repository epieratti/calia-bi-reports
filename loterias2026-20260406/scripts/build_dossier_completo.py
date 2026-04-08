#!/usr/bin/env python3
"""
Gera o HTML do dossiê (lote 06/04/2026) a partir de data/dossier_loterias2026.md
e data/dossier_loterias2026_panels.yaml.

Saída: output/20260406-dossie-squad-always-on-loterias-2026.html
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

from dossier_render import render_loterias_dossier_html
from md_dossier_source import load_dossier_bundle, panels_only_path_for_md

DATA = _ROOT / "data"
OUT_DIR = _ROOT / "output"
MD_SOURCE = DATA / "dossier_loterias2026.md"
LEGACY_YAML = DATA / "dossier_loterias2026.yaml"
OUT_HTML = OUT_DIR / "20260406-dossie-squad-always-on-loterias-2026.html"


def load_bundle() -> dict:
    panels_path = panels_only_path_for_md(MD_SOURCE)
    if MD_SOURCE.is_file():
        return load_dossier_bundle(MD_SOURCE, panels_path)
    import yaml

    with open(LEGACY_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main(*, no_gate: bool = False) -> None:
    bundle = load_bundle()
    render_loterias_dossier_html(
        bundle,
        variant="squad_8",
        out_path=OUT_HTML,
        no_gate=no_gate,
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gera dossiê HTML (fonte .md + painéis YAML).")
    ap.add_argument(
        "--no-gate",
        action="store_true",
        help="Sem tela de senha (preview local).",
    )
    args = ap.parse_args()
    main(no_gate=args.no_gate)
