#!/usr/bin/env python3
"""Reestrutura #perfis: um único bloco com todos os creators, ordem cronológica dos pedidos."""
from __future__ import annotations

import re
from pathlib import Path

HTML = Path("/workspace/caixa/20260511-dossie-squad-always-on-loterias-2026.html")


def extract_sections(html: str) -> list[str]:
    sections: list[str] = []
    i = 0
    while True:
        start = html.find("<section id='", i)
        if start == -1:
            break
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
                    sections.append(html[start:j])
                    i = j
                    break
            j += 1
        else:
            raise RuntimeError("unbalanced section")
    return sections


def main() -> None:
    t = HTML.read_text(encoding="utf-8")
    a = t.find('<section id="perfis"')
    b = t.find('<section id="tabela"', a)
    if a < 0 or b < 0:
        raise SystemExit("perfis/tabela not found")

    chunk = t[a:b]
    hdr_open = chunk.find('<div class="section-header mb-6">')
    hdr_close = chunk.find("</div>", hdr_open) + len("</div>")
    header = chunk[hdr_open:hdr_close]

    inner = chunk[hdr_close:].lstrip()
    if not inner.rstrip().endswith("</section>"):
        raise SystemExit("unexpected perfis tail")
    inner_body = inner.rstrip()[: -len("</section>")].rstrip()

    sections = extract_sections(inner_body)
    if len(sections) != 27:
        raise SystemExit(f"expected 27 sections, got {len(sections)}")

    new_header = """<div class="section-header mb-6"><h2 class="text-xl font-black text-calia-navy">Perfis — todos os creators</h2><p class="text-sm text-slate-600 mt-2 leading-relaxed max-w-3xl">Um único bloco, na <strong class="font-semibold text-slate-900">ordem dos pedidos</strong> (mais antigo no topo): <strong class="font-semibold text-slate-900">01/04/2026</strong> (13 nomes), <strong class="font-semibold text-slate-900">06/04/2026</strong> (8), <strong class="font-semibold text-slate-900">04/05/2026</strong> (3) e <strong class="font-semibold text-slate-900">lote 3 — 11/05/2026</strong> (3).</p></div>"""

    body = (
        "<div id='squad-todos-pedidos' class='rounded-xl border border-slate-200 bg-slate-50/50 p-4 md:p-6 shadow-sm ring-1 ring-slate-100/80 "
        "space-y-8 md:space-y-10 scroll-mt-20'>\n"
        + "\n".join(sections)
        + "\n</div>\n"
    )

    new_perfis = f'<section id="perfis" class="scroll-mt-20">\n      {new_header}\n      {body}    </section>\n\n    '

    t = t[:a] + new_perfis + t[b:]

    # Sumário: remover link duplicado ao lote 3; lista única na ordem dos pedidos
    t = t.replace(
        '        <li><a class="toc-link" href="#squad-lote-3">Squad — lote 3 (mai/2026)</a></li>\n\n',
        "",
    )
    t = t.replace(
        '<li><a class="toc-link" href="#perfis">Perfis (todos os lotes)</a></li>',
        '<li><a class="toc-link" href="#perfis">Perfis (ordem dos pedidos)</a></li>',
    )

    old_subtoc = re.search(
        r'<p class="text-xs text-slate-500 mt-6 font-semibold uppercase tracking-wide">Perfis</p>\s*<ul class="toc-list">.*?</ul>',
        t,
        re.S,
    )
    if not old_subtoc:
        raise SystemExit("subtoc not found")

    toc_items: list[str] = []
    for idx, sec in enumerate(sections, start=1):
        m_id = re.search(r"<section id='([^']+)'", sec)
        m_h2 = re.search(
            r"<h2 class=['\"]text-xl font-black text-calia-navy['\"]>([^<]+)</h2>",
            sec,
        )
        if not m_id or not m_h2:
            raise SystemExit(f"parse fail section {idx}")
        sid = m_id.group(1)
        title = m_h2.group(1).strip()
        mnum = re.match(r"^\d+\.\s*(.+)$", title)
        label = mnum.group(1).strip() if mnum else title
        toc_items.append(
            f"<li><a class='toc-link' href='#{sid}'>{idx}. {label}</a></li>"
        )

    new_subtoc = (
        '<p class="text-xs text-slate-500 mt-6 font-semibold uppercase tracking-wide">Índice dos perfis</p>\n'
        '<p class="text-xs text-slate-500 mb-2 leading-snug">Mesma ordem do corpo: 01/04 → 06/04 → 04/05 → lote 3.</p>\n'
        '<ul class="toc-list text-sm max-h-[28rem] overflow-y-auto pr-1 md:columns-2 md:gap-x-8">\n'
        + "\n".join(f"        {x}" for x in toc_items)
        + "\n      </ul>"
    )
    t = t[: old_subtoc.start()] + new_subtoc + t[old_subtoc.end() :]

    HTML.write_text(t, encoding="utf-8")
    print("OK", HTML, "sections", len(sections))


if __name__ == "__main__":
    main()
