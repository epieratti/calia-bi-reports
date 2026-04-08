#!/usr/bin/env python3
"""
Gera o HTML do dossiê a partir da fonte Markdown + painéis YAML.

Fonte principal: data/dossier_loterias2026.md (front matter + perfis em ## Nome)
Painéis (métricas): data/dossier_loterias2026_panels.yaml

Saída: output/20260401-dossie-squad-always-on-loterias-2026.html

Legado: data/dossier_loterias2026.yaml (monolítico) — use migrate_yaml_to_md_source.py
para gerar .md + _panels.yaml a partir dele.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Permite importar dossier_render ao rodar da pasta scripts/
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_ROOT / "scripts"))

from dossier_render import render_loterias_dossier_html
from md_dossier_source import load_dossier_bundle, panels_only_path_for_md

DATA = _ROOT / "data"
OUT_DIR = _ROOT / "output"
MD_SOURCE = DATA / "dossier_loterias2026.md"
LEGACY_YAML = DATA / "dossier_loterias2026.yaml"
OUT_HTML = OUT_DIR / "20260401-dossie-squad-always-on-loterias-2026.html"


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
        variant="squad_13",
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
