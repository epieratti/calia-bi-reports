#!/usr/bin/env python3
"""Remove notas longas em Métricas e reduz fonte da tabela-resumo (só essa tabela)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

# Parágrafos a remover (trecho único interno + contexto mínimo por âncora)
REMOVE_CONTAINS = [
    "Views totais (Social Blade, 11/05/2026):",
    "Médias por vídeo (Upfluence, Raquel e Morgana, 11/05/2026):",
    "Cruzamento de escala (11–12/05/2026):",
    "Percentagens de engajamento muito altas ou acima de 100% (ex.: Instagram):",
]

ANCHOR_RESUMO = "Uma linha por creator"

OLD_TD = "py-2 px-3 border-b border-slate-100 text-sm align-top"
NEW_TD = "py-2 px-3 border-b border-slate-100 text-xs align-top"
OLD_TH = "py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200"
NEW_TH = "py-2 px-3 text-left text-[10px] font-bold text-slate-600 border-b border-slate-200"


def remove_note_paragraph(html: str, contains: str) -> str:
    i = html.find(contains)
    if i == -1:
        return html
    p0 = html.rfind("<p", max(0, i - 500), i)
    p1 = html.find("</p>", i)
    if p0 == -1 or p1 == -1:
        raise SystemExit(f"parágrafo malformado para: {contains[:40]}")
    return html[:p0] + html[p1 + len("</p>") :]


def shrink_resumo_table(html: str) -> str:
    pos = html.find(ANCHOR_RESUMO)
    if pos == -1:
        raise SystemExit("âncora da tabela-resumo não encontrada")
    tstart = html.find("<table class='min-w-full'>", pos)
    if tstart == -1:
        raise SystemExit("tabela-resumo não encontrada após âncora")
    tend = html.find("</table>", tstart)
    if tend == -1:
        raise SystemExit("fechamento </table> da resumo não encontrado")
    tend += len("</table>")
    chunk = html[tstart:tend]
    chunk2 = chunk.replace(OLD_TD, NEW_TD).replace(OLD_TH, NEW_TH)
    return html[:tstart] + chunk2 + html[tend:]


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    for sub in REMOVE_CONTAINS:
        html = remove_note_paragraph(html, sub)
    html = shrink_resumo_table(html)
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
