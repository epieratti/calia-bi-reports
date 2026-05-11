#!/usr/bin/env python3
"""
Remove profile links from Métricas nas redes (#metricas):
- Instagram: unwrap Social Blade user links for all rows; remove @pvfreitazzz note from Paulo row.
- TikTok / YouTube: unwrap profile links only for Raquel Real, Morgana Camila, Paulo Victor Freitas.
Idempotent: re-running leaves HTML unchanged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LOTE3 = ("Raquel Real", "Morgana Camila", "Paulo Victor Freitas")

H3_MARKER = r"<h3 class='text-lg font-black text-calia-navy mb-2'>"

SB_IG = re.compile(
    r'<a class="dossier-source-link" href="https://socialblade\.com/instagram/user/[^"]+"[^>]*>([^<]+)</a>'
)

SB_YT = re.compile(
    r'<a class="dossier-source-link" href="https://socialblade\.com/youtube/channel/[^"]+"[^>]*>([^<]+)</a>'
)
YT_AT = re.compile(
    r'<a class="dossier-source-link" href="https://www\.youtube\.com/[^"]+"[^>]*>([^<]+)</a>'
)
TT = re.compile(
    r'<a class="dossier-source-link" href="https://www\.tiktok\.com/[^"]+"[^>]*>([^<]+)</a>'
)

TR = re.compile(r"<tr>[\s\S]*?</tr>")


def extract_metricas(html: str) -> tuple[int, int, str] | None:
    start = html.find('<section id="metricas"')
    if start == -1:
        return None
    depth = 0
    i = start
    while i < len(html):
        if html.startswith("<section", i):
            depth += 1
            i = html.find(">", i) + 1
            continue
        if html.startswith("</section>", i):
            depth -= 1
            if depth == 0:
                end = i + len("</section>")
                return start, end, html[start:end]
            i += len("</section>")
            continue
        i += 1
    return None


def process_instagram(body: str) -> str:
    body = SB_IG.sub(r"\1", body)
    body = body.replace(
        '(principal SB; <strong class="font-semibold text-slate-900">@pvfreitazzz</strong> sem ficha)',
        "(principal SB)",
    )
    return body


def process_rows_lote3(body: str, network: str) -> str:
    def repl_row(m: re.Match[str]) -> str:
        row = m.group(0)
        if not any(name in row for name in LOTE3):
            return row
        if network == "TikTok":
            return TT.sub(r"\1", row)
        if network == "YouTube":
            row = SB_YT.sub(r"\1", row)
            row = YT_AT.sub(r"\1", row)
            return row
        return row

    return TR.sub(repl_row, body)


def transform_inner(inner: str) -> str:
    spl = re.split(rf"({H3_MARKER}(?:Instagram|TikTok|YouTube|X)</h3>)", inner)
    if len(spl) != 9:
        raise RuntimeError(
            f"Métricas: split por rede esperava 9 partes, veio {len(spl)} (HTML mudou?)"
        )
    ig = process_instagram(spl[2])
    tt = process_rows_lote3(spl[4], "TikTok")
    yt = process_rows_lote3(spl[6], "YouTube")
    return "".join(
        [
            spl[0],
            spl[1],
            ig,
            spl[3],
            tt,
            spl[5],
            yt,
            spl[7],
            spl[8],
        ]
    )


def transform_metricas_chunk(chunk: str) -> str:
    m = re.match(r'^(<section id="metricas"[^>]*>)([\s\S]*)(</section>)$', chunk)
    if not m:
        raise RuntimeError("Chunk #metricas com formato inesperado")
    prefix, inner, suffix = m.groups()
    return prefix + transform_inner(inner) + suffix


def main() -> int:
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("caixa/20260511-dossie-squad-always-on-loterias-2026.html")
    )
    html = path.read_text(encoding="utf-8")
    ext = extract_metricas(html)
    if ext is None:
        print("Seção #metricas não encontrada", file=sys.stderr)
        return 1
    start, end, chunk = ext
    new_chunk = transform_metricas_chunk(chunk)
    if new_chunk == chunk:
        print("Nenhuma alteração (já aplicado ou nada a trocar).")
        return 0
    path.write_text(html[:start] + new_chunk + html[end:], encoding="utf-8")
    print(f"Atualizado: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
