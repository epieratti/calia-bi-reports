#!/usr/bin/env python3
"""Normaliza o título do eixo 4 para '4. Loterias 18+ (audiência)' nos perfis que
ainda estavam só com '4. Loterias 18+'. Idempotente."""

from __future__ import annotations

from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

SHORT_TITLE = "<p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+</p>"
LONG_TITLE = "<p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+ (audiência)</p>"

PROFILE_IDS = [
    "giovanna-pitel",
    "rafael-gratta",
    "indio-behn",
    "megh-melry",
    "cleane-sampaio",
    "ivan-baron",
    "mila-costa",
    "cristian-wariu",
    "cereja",
    "aline-costa",
    "davi",
    "paula-mineira",
    "catraca-livre",
    "julia-ferrari",
    "joao-vitor-mello",
    "lorena-rufino",
    "barbara-coura",
    "raphael-vicente",
    "rafael-saraiva",
    "pedro-ottoni",
    "ademara",
    "linnyke-alves",
    "felipe-hatori",
    "julimara",
    "raquel-real",
    "morgana-camila",
    "paulo-victor-freitas",
]


def trim_morgana_axis4(html: str) -> str:
    """Mantido por compatibilidade; o texto do eixo 4 de Morgana é editado em patch dedicado."""
    return html


def verify_axis4_titles(html: str) -> None:
    missing: list[str] = []
    for sid in PROFILE_IDS:
        a = html.find(f"<section id='{sid}'")
        b = html.find("<section id='", a + 10)
        sec = html[a:b]
        if "4. Loterias 18+ (audiência)</p>" not in sec:
            missing.append(sid)
    if missing:
        raise SystemExit(f"perfis sem título 4. Loterias 18+ (audiência): {missing}")


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    n_short = html.count(SHORT_TITLE)
    html = html.replace(SHORT_TITLE, LONG_TITLE)
    html = trim_morgana_axis4(html)
    verify_axis4_titles(html)
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH, "| títulos curtos substituídos nesta execução:", n_short)


if __name__ == "__main__":
    main()
