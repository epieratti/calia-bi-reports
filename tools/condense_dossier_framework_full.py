#!/usr/bin/env python3
"""Condensação em massa do dossiê HTML (frameworks: linguagem clara, corte de
pleonasmos, prioridade da informação), preservando tags, links e nuances.

1) Substitui intros longos (Paulo Victor, Raquel) por versões já editadas em
   tools/fragments/*.html
2) Aplica regras seguras só ao texto entre tags, dentro de #dossier-root

Idempotente: adiciona data-framework-full=\"1\" na div dossier-root.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_PATH = ROOT.parent / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"
FRAG = ROOT / "fragments"

TAG_SPLIT = re.compile(r"(<[^>]+>)")

# Regras conservadoras (sem mudar sentido jurídico de “não encontramos”).
PLAIN_RULES: list[tuple[str, str]] = [
    (r"[ \t\r\n]{2,}", " "),
    (r" ,", ","),
    (r" ;", ";"),
    (r" \.", "."),
    (r"\( ", "("),
    (r" \)", ")"),
    (r"Não localizada publi paga", "Sem publi paga"),
    (r"Não localizamos publi paga", "Sem publi paga"),
    (r"Não achamos contrato público com casa de aposta", "Sem contrato público com casa de aposta"),
    (r"Sem filiação partidária localizada nas fontes com URL para esta creator\.", "Sem filiação partidária nas fontes com URL."),
    (r"Sem filiação partidária localizada nas fontes com URL para esta creator", "Sem filiação partidária nas fontes com URL"),
    (r"nas fontes com URL usadas para", "nas fontes com URL para"),
    (r"de acordo com o que", "conforme"),
    (r"no âmbito de ", "em "),
    (r"no âmbito da ", "na "),
    (r"no âmbito do ", "no "),
    (r"no tocante a ", "sobre "),
    (r"no tocante ao ", "sobre o "),
    (r"no tocante à ", "sobre a "),
    (r"no que diz respeito a ", "quanto a "),
    (r"no que diz respeito ao ", "quanto ao "),
    (r"no que se refere a ", "quanto a "),
    (r"com relação a ", "sobre "),
    (r"em relação a ", "sobre "),
    (r"com o intuito de ", "para "),
    (r"com vistas a ", "para "),
    (r"a fim de que ", "para que "),
    (r"a fim de ", "para "),
    (r"de forma a que ", "para que "),
    (r"de forma a ", "para "),
    (r"de modo a que ", "para que "),
    (r"de modo a ", "para "),
    (r"uma vez que ", "pois "),
    (r"tendo em vista que ", "pois "),
    (r"em virtude de ", "por "),
    (r"em razão de ", "por "),
    (r"por parte de ", "por "),
    (r"vale ressaltar que ", ""),
    (r"Vale ressaltar que ", ""),
    (r"é importante salientar que ", ""),
    (r"É importante salientar que ", ""),
    (r"pode-se observar que ", ""),
    (r"Pode-se observar que ", ""),
    (r"é possível observar que ", ""),
    (r"É possível observar que ", ""),
    (r"há de se considerar que ", ""),
    (r"Há de se considerar que ", ""),
    (r"neste contexto, ", ""),
    (r"Neste contexto, ", ""),
    (r"neste contexto ", ""),
    (r"desta forma, ", "Assim, "),
    (r"Dessa forma, ", "Assim, "),
    (r"desse modo, ", "Assim, "),
    (r"Desse modo, ", "Assim, "),
    (r"de maneira geral, ", "Em geral, "),
    (r"De maneira geral, ", "Em geral, "),
    (r"de um modo geral, ", "Em geral, "),
    (r"o que se verifica é que ", ""),
    (r"O que se verifica é que ", ""),
    (r" — — ", " — "),
]

PLAIN_RES = [(re.compile(a), b) for a, b in PLAIN_RULES]


def condense_plain(text: str) -> str:
    t = text
    for rx, rep in PLAIN_RES:
        t = rx.sub(rep, t)
    return t


def condense_html_fragment(fragment: str) -> str:
    parts = TAG_SPLIT.split(fragment)
    out: list[str] = []
    for p in parts:
        if p.startswith("<"):
            out.append(p)
        elif not p.strip():
            out.append(p)
        else:
            out.append(condense_plain(p))
    return "".join(out)


def find_dossier_root_bounds(html: str) -> tuple[int, int]:
    start = html.find('<div id="dossier-root"')
    if start == -1:
        raise SystemExit("dossier-root não encontrado")
    depth = 0
    i = start
    while i < len(html):
        if html.startswith("<div", i):
            depth += 1
            gt = html.find(">", i)
            if gt == -1:
                raise SystemExit("tag div incompleta")
            i = gt + 1
            continue
        if html.startswith("</div>", i):
            depth -= 1
            i += len("</div>")
            if depth == 0:
                return start, i
            continue
        i += 1
    raise SystemExit("fechamento de dossier-root não encontrado")


def replace_first_intro_paragraph(block: str, section_id: str, new_inner: str) -> str:
    """Substitui o primeiro <p class='text-sm text-slate-600 mb-6...'> após <section id='...'>."""
    rx = (
        rf"(<section id='{re.escape(section_id)}'[\s\S]*?"
        r"<p class='text-sm text-slate-600 mb-6[^']*'[^>]*>)"
        r"([\s\S]*?)"
        r"(</p>)"
    )
    m = re.search(rx, block)
    if not m:
        return block
    old = m.group(2)
    if old.strip() == new_inner.strip():
        return block
    return block[: m.start(2)] + new_inner + block[m.end(2) :]


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    if 'data-framework-full="1"' in html:
        print("Já processado (data-framework-full=1).")
        return

    start, end = find_dossier_root_bounds(html)
    inner = html[start:end]

    paulo_new = (FRAG / "paulo_intro_condensed.html").read_text(encoding="utf-8").strip()
    raquel_new = (FRAG / "raquel_intro_condensed.html").read_text(encoding="utf-8").strip()

    inner2 = replace_first_intro_paragraph(inner, "paulo-victor-freitas", paulo_new)
    inner2 = replace_first_intro_paragraph(inner2, "raquel-real", raquel_new)
    inner2 = condense_html_fragment(inner2)

    inner2 = inner2.replace(
        '<div id="dossier-root"',
        '<div id="dossier-root" data-framework-full="1"',
        1,
    )

    if inner2 == inner:
        print("Sem alterações.")
        return

    new_html = html[:start] + inner2 + html[end:]
    HTML_PATH.write_text(new_html, encoding="utf-8")
    print("OK:", HTML_PATH, "delta:", len(inner2) - len(inner))


if __name__ == "__main__":
    main()
