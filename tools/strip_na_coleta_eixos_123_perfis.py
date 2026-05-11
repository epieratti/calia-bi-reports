#!/usr/bin/env python3
"""
Remove menções a 'coleta' nos parágrafos dos eixos 1–3 (Concorrência, Polêmicas, Política)
dentro de #perfis, unificando o tom sem tocar em #metricas nem no eixo 4.
Idempotente: reexecutar não deve degradar o texto.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def clean_axis123_body(inner: str) -> str:
    s = inner
    if "coleta" not in s.lower():
        return inner

    s = s.replace("Sem bet na coleta.", "Sem casa de apostas identificada.")

    s = re.sub(r"\bnas fontes desta coleta\b", "nas fontes públicas consultadas", s, flags=re.I)
    s = s.replace("Complemento no X ", "No X ")
    s = re.sub(r"</a>,\s*\d{2}/\d{2}/\d{4}\):</strong>", "</a>):</strong>", s)

    s = re.sub(r":\s*na coleta,\s*", ": ", s, flags=re.I)

    s = re.sub(r"(\w)\s+na coleta\.", r"\1.", s, flags=re.I)
    s = re.sub(r"(\w)\s+na coleta;", r"\1;", s, flags=re.I)
    s = re.sub(r"(\w)\s+na coleta,", r"\1,", s, flags=re.I)

    s = re.sub(r" na coleta\.", ".", s, flags=re.I)
    s = re.sub(r" na coleta;", ";", s, flags=re.I)
    s = re.sub(r" na coleta,", ",", s, flags=re.I)
    s = re.sub(r" na coleta ", " ", s, flags=re.I)
    s = re.sub(r" na coleta(?=<)", "", s, flags=re.I)

    s = re.sub(r"\s+nesta coleta\b", "", s, flags=re.I)
    s = re.sub(r"^\s*Na coleta,?\s*", "", s, flags=re.I)

    s = re.sub(
        r"até a data do recorte\.?",
        "no material analisado.",
        s,
        flags=re.I,
    )
    s = re.sub(r"  +", " ", s)
    s = re.sub(r"\s+\.(?=[\s<])", ".", s)
    return s


def patch_html(html: str) -> tuple[str, int]:
    start = html.find('id="perfis"')
    end = html.find('id="metricas"', start)
    if start == -1 or end == -1:
        raise SystemExit("Marcadores id=perfis ou id=metricas não encontrados.")

    head, mid, tail = html[:start], html[start:end], html[end:]

    labels = (r"1\. Concorrência", r"2\. Polêmicas", r"3\. Política")
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        prefix, body, suffix = m.group(1), m.group(2), m.group(3)
        new_body = clean_axis123_body(body)
        if new_body != body:
            count += 1
        return prefix + new_body + suffix

    new_mid = mid
    for label in labels:
        pat = (
            rf"(<p class='text-xs font-black uppercase text-calia-gold mb-[12]'>{label}[^<]*</p>"
            r"<p class='text-sm text-slate-700 leading-relaxed'>)([\s\S]*?)(</p></div>)"
        )
        new_mid = re.sub(pat, repl, new_mid)

    return head + new_mid + tail, count


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    html = path.read_text(encoding="utf-8")
    new_html, n = patch_html(html)
    if new_html == html:
        print("Nenhuma alteração (já aplicado ou sem alvos).")
        return
    path.write_text(new_html, encoding="utf-8")
    print(f"Atualizado {path}: {n} parágrafo(s) de eixo 1–3 reescritos.")


if __name__ == "__main__":
    main()
