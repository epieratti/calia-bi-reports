#!/usr/bin/env bash
# Gera o dossiê a partir de data/dossier_loterias2026.md + _panels.yaml e copia para caixa/.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOSSIER="20260504-dossie-squad-always-on-loterias-2026-rev-nomes.html"

cd "$REPO_ROOT/loterias2026"
python3 scripts/build_dossier_completo.py
cp -f "output/${DOSSIER}" "$REPO_ROOT/caixa/${DOSSIER}"
echo "OK: $REPO_ROOT/caixa/${DOSSIER}"
