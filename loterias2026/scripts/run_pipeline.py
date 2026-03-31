#!/usr/bin/env python3
"""
Orquestra o fluxo completo do briefing: coleta → classificação → agregação → HTML.

Uso:
  python scripts/run_pipeline.py

Requer APIFY_TOKEN no ambiente para Instagram/TikTok/X. YouTube funciona sem Apify.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_step(name: str, args: list[str]) -> None:
    print(f"\n=== {name} ===", flush=True)
    r = subprocess.run([sys.executable, *args], cwd=str(ROOT))
    if r.returncode != 0:
        sys.exit(r.returncode)


def main() -> None:
    run_step("Coleta", [str(SCRIPTS / "collect.py")])
    run_step("Classificação", [str(SCRIPTS / "classify.py")])
    run_step("Agregação por perfil", [str(SCRIPTS / "aggregate_profiles.py")])
    run_step("Relatório HTML", [str(SCRIPTS / "report_html.py")])
    print("\nConcluído. Abra output/dossie-brand-safety-loterias-2026.html", flush=True)


if __name__ == "__main__":
    main()
