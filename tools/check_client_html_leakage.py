#!/usr/bin/env python3
"""
Varre HTML publicados (Caixa, Embratur, etc.) em busca de strings que não
devem aparecer no texto visível ao cliente (caminhos do repo, nomes de fonte interna).

Uso (na raiz do repo):
  python3 tools/check_client_html_leakage.py
  python3 tools/check_client_html_leakage.py caixa/ embratur/

Saída: exit 0 se ok; 1 se encontrar ocorrências (lista arquivo + padrão).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Padrões que indicam vazamento de processo/repo no corpo visível
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("caminho loterias2026", re.compile(r"loterias2026[-/]", re.I)),
    ("caminho tools/", re.compile(r"tools/(?:dossier_|validate_|md_dossier|check_dossier)", re.I)),
    ("arquivo _panels.yaml", re.compile(r"_panels\.ya?ml", re.I)),
    ("extensão .md (fonte)", re.compile(r"dossier_[^\s\"'<>]+\.md\b", re.I)),
    ("script build interno", re.compile(r"build_dossier_completo", re.I)),
    ("validador interno", re.compile(r"validate_dossier_source", re.I)),
]


def strip_non_visible(html: str) -> str:
    """Remove comentários, script e style para aproximar o texto visível."""
    t = re.sub(r"<!--[\s\S]*?-->", "", html)
    t = re.sub(r"<script\b[\s\S]*?</script>", "", t, flags=re.I)
    t = re.sub(r"<style\b[\s\S]*?</style>", "", t, flags=re.I)
    return t


def scan_file(path: Path) -> list[tuple[str, str]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    visible = strip_non_visible(raw)
    hits: list[tuple[str, str]] = []
    for label, rx in PATTERNS:
        m = rx.search(visible)
        if m:
            snippet = visible[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
            hits.append((label, snippet.strip()))
    return hits


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    dirs = [Path(p) for p in (sys.argv[1:] or ["caixa", "embratur"])]
    bad = False
    for d in dirs:
        p = root / d if not d.is_absolute() else d
        if not p.is_dir():
            continue
        for html in sorted(p.rglob("*.html")):
            if "node_modules" in html.parts:
                continue
            hits = scan_file(html)
            if hits:
                bad = True
                rel = html.relative_to(root)
                for label, snip in hits:
                    print(f"{rel}: [{label}] …{snip}…")
    if bad:
        print(
            "\nCorrija o texto visível no HTML ou a fonte .md; comentários HTML e "
            "<script> são ignorados por este verificador.",
            file=sys.stderr,
        )
        return 1
    print("OK: nenhum padrão de vazamento encontrado no texto visível.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
