#!/usr/bin/env python3
"""Normaliza o título do eixo 4 para '4. Loterias 18+ (audiência)' nos perfis que
ainda estavam só com '4. Loterias 18+'. Ajusta o parágrafo do eixo 4 de Morgana Camila
(remoção do preâmbulo metodológico redundante + entrada 'Na coleta, em …'). Idempotente."""

from __future__ import annotations

import re
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
    sid = "morgana-camila"
    start = html.find(f"<section id='{sid}'")
    if start == -1:
        raise SystemExit("secção morgana-camila não encontrada")
    end = html.find("<section id='", start + 10)
    if end == -1:
        raise SystemExit("fim de secção morgana não encontrado")
    sec = html[start:end]
    m = re.search(
        r"(4\. Loterias 18\+(?: \(audiência\))?</p><p class='text-sm text-slate-700 leading-relaxed'>)([\s\S]*?)(</p></div></div>)",
        sec,
    )
    if not m:
        raise SystemExit("bloco Loterias 18+ de Morgana não encontrado")
    head, body, tail = m.group(1), m.group(2), m.group(3)
    lb = body.lstrip()
    if lb.startswith("Na coleta, em <a"):
        return html
    if "Em <a" not in body:
        raise SystemExit("texto esperado com link (Em <a) ausente em Morgana")
    rest = body.split("Em <a", 1)[1]
    new_body = "Na coleta, em <a" + rest
    sec2 = sec.replace(head + body + tail, head + new_body + tail, 1)
    return html[:start] + sec2 + html[end:]


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
