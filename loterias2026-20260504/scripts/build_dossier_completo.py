#!/usr/bin/env python3
"""
Gera o HTML do dossiê (lote 04/05/2026) a partir de data/dossier_loterias2026.md
e data/dossier_loterias2026_panels.yaml.

Saída padrão: output/20260504-dossie-squad-always-on-loterias-2026.html
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = _ROOT.parent
if str(_REPO_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "tools"))

from dossier_render import render_loterias_dossier_html
from md_dossier_source import load_dossier_bundle, panels_only_path_for_md

DATA = _ROOT / "data"
OUT_DIR = _ROOT / "output"
DEFAULT_MD = DATA / "dossier_loterias2026.md"
LEGACY_YAML = DATA / "dossier_loterias2026.yaml"
DEFAULT_OUT = OUT_DIR / "20260504-dossie-squad-always-on-loterias-2026.html"
DEFAULT_VARIANT = "squad_8"


def load_bundle(md_path: Path, panels_path: Path | None) -> dict:
    if md_path.is_file():
        return load_dossier_bundle(md_path, panels_path)
    if md_path.resolve() == DEFAULT_MD.resolve() and LEGACY_YAML.is_file():
        import yaml

        with open(LEGACY_YAML, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    raise SystemExit(f"Arquivo fonte não encontrado: {md_path}")


def main(
    *,
    md_path: Path,
    panels_path: Path | None,
    out_path: Path,
    variant: str,
    no_gate: bool = False,
) -> None:
    bundle = load_bundle(md_path, panels_path)
    render_loterias_dossier_html(
        bundle,
        variant=variant,
        out_path=out_path,
        no_gate=no_gate,
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gera dossiê HTML (fonte .md + painéis YAML).")
    ap.add_argument("--md", type=Path, default=DEFAULT_MD, help="Arquivo fonte .md.")
    ap.add_argument(
        "--panels",
        type=Path,
        default=None,
        help="YAML dos painéis; default: <stem do --md>_panels.yaml",
    )
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Caminho do HTML gerado.")
    ap.add_argument(
        "--variant",
        choices=("squad_13", "squad_8"),
        default=DEFAULT_VARIANT,
        help="Layout (este lote usa squad_8 por padrão).",
    )
    ap.add_argument("--no-gate", action="store_true", help="Sem tela de senha.")
    args = ap.parse_args()
    md_path = args.md.resolve()
    panels_path = args.panels.resolve() if args.panels else None
    if panels_path is None and md_path.is_file():
        panels_path = panels_only_path_for_md(md_path)
        if not panels_path.is_file():
            panels_path = None
    out_path = args.out
    if not out_path.is_absolute():
        out_path = (_ROOT / out_path).resolve()
    main(
        md_path=md_path,
        panels_path=panels_path,
        out_path=out_path,
        variant=args.variant,
        no_gate=args.no_gate,
    )
