#!/usr/bin/env bash
# Gera o dossiê do lote 06/04/2026 a partir do YAML e copia para caixa/ (fonte → publicação GitHub Pages).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOSSIER="20260406-dossie-squad-always-on-loterias-2026.html"

cd "$REPO_ROOT/loterias2026-20260406"
python3 scripts/build_dossier_completo.py
cp -f "output/${DOSSIER}" "$REPO_ROOT/caixa/${DOSSIER}"
echo "OK: $REPO_ROOT/caixa/${DOSSIER}"
