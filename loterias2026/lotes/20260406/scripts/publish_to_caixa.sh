#!/usr/bin/env bash
# Gera o dossiê do lote 06/04/2026 e copia para caixa/.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
LOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOSSIER="20260406-dossie-squad-always-on-loterias-2026.html"

cd "$REPO_ROOT"
python3 loterias2026/scripts/build_dossier_completo.py --project-root "$LOT_DIR"
cp -f "$LOT_DIR/output/${DOSSIER}" "$REPO_ROOT/caixa/${DOSSIER}"
echo "OK: $REPO_ROOT/caixa/${DOSSIER}"
