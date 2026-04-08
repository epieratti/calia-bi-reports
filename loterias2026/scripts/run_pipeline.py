#!/usr/bin/env python3
"""
Orquestra o fluxo legado: coleta (incl. Apify) → classificação → agregação → HTML.

Não faz parte do fluxo operacional de entrega: métricas no dossiê cliente vêm de
Social Blade + Upfluence → dossier_*_panels.yaml (ver PLAYBOOK_DOSSIES.md).

Uso (opcional / experimentação):
  python scripts/run_pipeline.py

Requer APIFY_TOKEN para IG/TT/X na coleta Apify. YouTube e web aberta seguem os scripts.
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
    run_step("Coleta redes sociais", [str(SCRIPTS / "collect.py")])
    run_step("Coleta web aberta (Wikipedia, notícias, busca)", [str(SCRIPTS / "collect_open_web.py")])
    run_step("Classificação", [str(SCRIPTS / "classify.py")])
    run_step("Agregação por perfil", [str(SCRIPTS / "aggregate_profiles.py")])
    run_step("Relatório HTML", [str(SCRIPTS / "report_html.py")])
    print("\nConcluído. Abra output/dossie-brand-safety-loterias-2026.html", flush=True)


if __name__ == "__main__":
    main()
