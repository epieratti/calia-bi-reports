#!/usr/bin/env python3
"""Renumera <h2> dos perfis para sequência 1..N na ordem do bloco #perfis."""
from __future__ import annotations

import re
from pathlib import Path

HTML = Path("/workspace/caixa/20260511-dossie-squad-always-on-loterias-2026.html")

# Ordem do consolidado (pedidos: 01/04 → 06/04 → 04/05 → lote 3)
SECTION_ORDER: list[str] = [
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


def extract_section(html: str, sid: str) -> tuple[int, int] | None:
    needle = f"<section id='{sid}' class='card-audit scroll-mt-20'>"
    start = html.find(needle)
    if start < 0:
        return None
    depth = 0
    j = start
    while j < len(html):
        if html.startswith("<section", j):
            depth += 1
            j = html.find(">", j) + 1
            continue
        if html.startswith("</section>", j):
            depth -= 1
            j += len("</section>")
            if depth == 0:
                return start, j
            continue
        j += 1
    return None


def main() -> None:
    t = HTML.read_text(encoding="utf-8")
    for idx, sid in enumerate(SECTION_ORDER, start=1):
        span = extract_section(t, sid)
        if not span:
            raise SystemExit(f"seção não encontrada: {sid}")
        s0, s1 = span
        block = t[s0:s1]
        m = re.search(
            r"<h2 class='text-xl font-black text-calia-navy'>([^<]+)</h2>",
            block,
        )
        if not m:
            raise SystemExit(f"h2 não encontrado: {sid}")
        title = m.group(1).strip()
        mm = re.match(r"^\d+\.\s*(.+)$", title)
        name = mm.group(1).strip() if mm else title
        new_h2 = f"<h2 class='text-xl font-black text-calia-navy'>{idx}. {name}</h2>"
        old_h2 = m.group(0)
        if old_h2 == new_h2:
            continue
        new_block = block.replace(old_h2, new_h2, 1)
        t = t[:s0] + new_block + t[s1:]
    HTML.write_text(t, encoding="utf-8")
    print("OK", len(SECTION_ORDER), "perfis")


if __name__ == "__main__":
    main()
