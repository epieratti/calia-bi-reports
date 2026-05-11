#!/usr/bin/env python3
"""
Uniformiza o bloco introdutório de cada perfil (#perfis): remove rótulos
«Quem é.» / «Homologação.» e troca o <p>…</p> por <div> com <p> filhos
(mesma tipografia base, space-y-3, text-pretty). Idempotente.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HTML_DEFAULT = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

OLD_OPEN = "<p class='text-sm text-slate-600 mb-6 leading-relaxed'>"
OLD_CLOSE = "</p><div class='grid md:grid-cols-2 gap-4'>"
GRID_AFTER = "<div class='grid md:grid-cols-2 gap-4'>"

NEW_OPEN = "<div class='text-sm text-slate-600 mb-6 leading-relaxed space-y-3 text-pretty'>"

QUEM = re.compile(
    r'<strong class="font-semibold text-slate-900">Quem é\.</strong>\s*',
)
HOMOLOG = re.compile(
    r'<strong class="font-semibold text-slate-900">Homologação\.</strong>\s*',
)
SPAN_BLOCK = re.compile(
    r"<span class=['\"]block(?:\s+mt-2)?['\"]>([\s\S]*?)</span>",
)


def build_intro_from_spans(inner: str) -> str:
    s = QUEM.sub("", inner)
    s = HOMOLOG.sub("", s)

    parts = [p.strip() for p in SPAN_BLOCK.findall(s) if p.strip()]
    if not parts:
        parts = [s.strip()] if s.strip() else []

    paras = "".join(
        f"<p class='m-0 leading-relaxed text-slate-600'>{p}</p>" for p in parts
    )
    return f"{NEW_OPEN}{paras}</div>"


def replace_perfis_block(html: str) -> tuple[str, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]

    pat = re.compile(
        re.escape(OLD_OPEN) + r"([\s\S]*?)" + re.escape(OLD_CLOSE),
    )
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        raw = m.group(1)
        intro = build_intro_from_spans(raw)
        n += 1
        return intro + GRID_AFTER

    chunk2 = pat.sub(repl, chunk)
    return head + chunk2 + tail, n


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else HTML_DEFAULT
    html = path.read_text(encoding="utf-8")
    html2, n = replace_perfis_block(html)
    if html2 == html:
        print("Nada alterado.")
        return 0
    path.write_text(html2, encoding="utf-8")
    print(f"OK: {n} intros uniformizadas em {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
