#!/usr/bin/env python3
"""
Bloco introdutório de cada perfil (#perfis): estrutura uniforme em <div> com
<p> filhos (space-y-3), sem rótulo «Quem é»; divisão em dois <p> quando o texto
é longo. Idempotente. Preferir também tools/flatten_quem_e_intro_perfis.py
para remover spans/Quem é. de HTML legado.
"""
from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

NEW_OPEN = "<div class='text-sm text-slate-600 mb-6 leading-relaxed space-y-3 text-pretty'>"
GRID_AFTER = "<div class='grid md:grid-cols-2 gap-4'>"

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
    return s.startswith(NEW_OPEN)


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
        parts = [core]
    else:
        part1, part2 = core[:sp].strip(), core[sp:].strip()
        parts = [part1] + ([part2] if part2 else [])
    paras = "".join(
        f"<p class='m-0 leading-relaxed text-slate-600'>{p}</p>" for p in parts if p
    )
    return f"{NEW_OPEN}{paras}</div>"


def replace_in_perfis(html: str) -> tuple[str, int]:
    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    head, chunk, tail = html[:a], html[a:b], html[b:]
    pat = re.compile(
        r"(<p class='text-sm text-slate-600 mb-6 leading-relaxed'>)([\s\S]*?)(</p><div class='grid md:grid-cols-2 gap-4'>)"
    )
    # Saída: bloco <div>…</div> + grid (sem </p> antes do grid)
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        inner = m.group(2)
        new_inner = wrap_inner(inner)
        if new_inner != inner:
            n += 1
        return new_inner + GRID_AFTER

    chunk2 = pat.sub(repl, chunk)
    return head + chunk2 + tail, n


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    html2, n = replace_in_perfis(html)
    if html2 == html:
        print("Nada alterado.")
        return
    HTML_PATH.write_text(html2, encoding="utf-8")
    print(f"OK: {n} blocos introdutórios normalizados em {HTML_PATH}")


if __name__ == "__main__":
    main()
