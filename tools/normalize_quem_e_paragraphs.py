#!/usr/bin/env python3
"""
Padroniza o parágrafo \"Quem é\" de cada perfil no dossiê HTML: mesma estrutura
(<span class=\"block\"> + rótulos Quem é. / Homologação.) e divisão automática
por frase quando o texto for longo. Idempotente.
"""
from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

QUEM_STRONG = '<strong class="font-semibold text-slate-900">Quem é.</strong> '
HOMOLOG_STRONG = '<strong class="font-semibold text-slate-900">Homologação.</strong> '

TRIANG_OPEN = re.compile(
    r"^\s*<strong class=\"font-semibold text-slate-900\">Quem é \(triangulação\):</strong>\s*",
    re.I,
)


def count_plain(html: str) -> int:
    t = re.sub(r"<[^>]+>", "", html)
    return len(re.sub(r"\s+", " ", t).strip())


def split_candidates(html: str) -> list[int]:
    in_tag = False
    cands: list[int] = []
    i = 0
    while i < len(html):
        c = html[i]
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            if i + 1 < len(html) and html[i : i + 2] == ". ":
                cands.append(i + 2)
            elif i + 1 < len(html) and html[i : i + 2] == "; ":
                cands.append(i + 2)
            elif c == "." and i + 1 < len(html) and html[i + 1] == "<":
                cands.append(i + 1)
        i += 1
    return cands


def plain_before(html: str, pos: int) -> int:
    return count_plain(html[:pos])


def best_split(html: str, min_first: int, min_rest: int) -> int | None:
    total = count_plain(html)
    if total < min_first + min_rest:
        return None
    cands = split_candidates(html)
    if not cands:
        return None
    target = total // 2
    best: int | None = None
    best_dist = 1e9
    for p in cands:
        a = plain_before(html, p)
        b = total - a
        if a < min_first or b < min_rest:
            continue
        d = abs(a - target)
        if d < best_dist:
            best_dist = d
            best = p
    return best


def already_normalized(inner: str) -> bool:
    s = inner.lstrip()
    return s.startswith('<span class="block"><strong class="font-semibold text-slate-900">Quem é.</strong>') or s.startswith(
        "<span class='block'><strong class='font-semibold text-slate-900'>Quem é.</strong>"
    )


def strip_leading_meta(inner: str) -> str:
    s = TRIANG_OPEN.sub("", inner)
    return s.lstrip()


def wrap_inner(core: str) -> str:
    core = strip_leading_meta(core).strip()
    if not core:
        return core
    if already_normalized(core):
        return core
    total = count_plain(core)
    sp = best_split(core, min_first=120, min_rest=80) if total >= 280 else None
    if sp is None:
        return f'<span class="block">{QUEM_STRONG}{core}</span>'
    part1, part2 = core[:sp].strip(), core[sp:].strip()
    if not part2:
        return f'<span class="block">{QUEM_STRONG}{core}</span>'
    return (
        f'<span class="block">{QUEM_STRONG}{part1}</span>'
        f'<span class="block mt-2">{HOMOLOG_STRONG}{part2}</span>'
    )


def replace_in_perfis(html: str) -> tuple[str, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]
    pat = re.compile(
        r"(<p class='text-sm text-slate-600 mb-6 leading-relaxed'>)([\s\S]*?)(</p><div class='grid md:grid-cols-2 gap-4'>)"
    )
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        inner = m.group(2)
        new_inner = wrap_inner(inner)
        if new_inner != inner:
            n += 1
        return m.group(1) + new_inner + m.group(3)

    chunk2 = pat.sub(repl, chunk)
    return head + chunk2 + tail, n


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    html2, n = replace_in_perfis(html)
    if html2 == html:
        print("Nada alterado.")
        return
    HTML_PATH.write_text(html2, encoding="utf-8")
    print(f"OK: {n} parágrafos \"Quem é\" normalizados em {HTML_PATH}")


if __name__ == "__main__":
    main()
