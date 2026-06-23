#!/usr/bin/env bash
# Monta pasta _site/ só com o que o GitHub Pages deve servir (não o repo inteiro).
# Uso (na raiz): bash tools/prepare_pages_artifact.sh [_site]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE="${1:-$ROOT/_site}"

rm -rf "$SITE"
mkdir -p "$SITE"
cd "$ROOT"

if [[ -f .nojekyll ]]; then
  cp .nojekyll "$SITE/"
else
  touch "$SITE/.nojekyll"
fi

cp index.html "$SITE/"

for dir in assets caixa febraban embratur; do
  if [[ -d "$dir" ]]; then
    cp -a "$dir" "$SITE/"
  fi
done

FORBIDDEN=(
  loterias2026
  loterias2026-20260406
  loterias2026-20260504
  tools
  docs
  examples
  .github
  .cursor
)

for name in "${FORBIDDEN[@]}"; do
  if [[ -e "$SITE/$name" ]]; then
    echo "ERRO: '$name' não deve entrar no artefato Pages." >&2
    exit 1
  fi
done

count="$(find "$SITE" -type f | wc -l | tr -d ' ')"
echo "OK: artefato Pages em $SITE ($count arquivos)"
find "$SITE" -type f | sort
