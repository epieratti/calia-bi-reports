#!/usr/bin/env python3
"""
Remove sufixos negativos com 'Na coleta' nos parágrafos do eixo 4 (Loterias 18+)
em #perfis; ajusta casos especiais (Megh, Catraca, Paulo, Morgana, Bárbara, Rafael Saraiva, Raquel).
Não altera #metricas. Idempotente quando já aplicado.
"""
from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

# Frases finais repetidas (remover por completo — o critério 18+ fica no que veio antes)
TAILS_REMOVE = [
    " Na coleta (abr./2026) não apareceu formato voltado a crianças nem indício de que menores componham parcela relevante da audiência-alvo para loterias; manter checagem na data da veiculação.",
    " Na coleta não há foco infantil nem sinal de que menores sejam fração relevante da audiência no critério Loterias 18+.",
    " Na coleta não surgiu apelo sistemático a menores nem evidência de público infantil predominante.",
    " Na coleta não houve sinal desse perfil para o critério loterias.",
    " Na coleta não apareceu apelo a menores como núcleo da audiência.",
    " Na coleta não apareceu foco em crianças como público-alvo nem sinal de audiência infantil predominante.",
    " Na coleta não apareceu formato infantil nem indício de menores como fração relevante da audiência.",
    " Na coleta não apareceu formato infantil nem indício de público infantil predominante.",
    " Na coleta não apareceu formato voltado a crianças nem sinal de audiência infantil predominante.",
    " Na coleta não houve evidência de público infantil predominante nem de menores como fração relevante no critério loterias.",
    " Na coleta não houve foco infantil nem evidência de menores como fração relevante no critério 18+.",
    " Na coleta não houve indício de público infantil predominante para loterias.",
    " Na coleta não houve sinal de menores como fração relevante da audiência no critério loterias.",
    " Na coleta não surgiu apelo a menores como núcleo da audiência.",
    " Na coleta não surgiu canal infantil nem indício de menores como fração relevante da audiência.",
    " Na coleta não surgiu foco em crianças como público-alvo nem audiência infantil predominante.",
    " Na coleta não surgiu formato infantil nem indício de que crianças componham parcela relevante da audiência para campanha 18+.",
    " Na coleta não surgiu formato infantil nem sinal de menores como fração relevante da audiência no critério 18+.",
    " Na coleta não surgiu produção voltada a criança como público-alvo nem audiência infantil predominante.",
]

MEGH_TAIL = " — na coleta não houve sinal desse perfil para o critério loterias."
CATRACA_FIX = ("; na coleta o risco", "; o risco")

PAULO_INNER = (
    "Humor adulto (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">g1</strong></a>). Parkour e rap na bio (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.nessmgt.com/casting/seu-freitaz\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Ness</strong></a>) apontam jovem-adulto — não sustentam leitura de público infantil predominante no critério Loterias 18+."
)

MORGANA_INNER = (
    "Em <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">O Povo</strong></a>, desfile cívico com <strong class=\"font-semibold text-slate-900\">escolas e fanfarras</strong> — <strong class=\"font-semibold text-slate-900\">menores em cena</strong> no material público. No <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.youtube.com/watch?v=Xfmr1sHUvq0\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">YouTube</strong></a>, tom familiar; validar demos na veiculação."
)

BARBARA_INNER = (
    "Humor curto com temas adultos; ritmo típico de entretenimento jovem-adulto, sem sinal de que crianças sejam o núcleo da audiência no critério Loterias 18+."
)

RAFAEL_SARAIVA_INNER = (
    "Sketch com título \"Bet Kids\" (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://portadosfundos.com.br/videos/bet-kids/\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Porta dos Fundos</strong></a>) é ficção humorística para adultos: roteiro e elenco apontam público adulto; o título não configura, por si, apelo a menores como núcleo da audiência no critério Loterias 18+."
)

MARKER = "4. Loterias 18+ (audiência)</p><p class='text-sm text-slate-700 leading-relaxed'>"


def section_bounds(html: str, sid: str) -> tuple[int, int]:
    open_sq = f"<section id='{sid}'"
    a = html.find(open_sq)
    if a == -1:
        raise SystemExit(f"secção não encontrada: {sid}")
    tag_close = html.find(">", a) + 1
    m = re.search(r"<section\s+id=", html[tag_close:])
    if not m:
        raise SystemExit(f"próxima secção não encontrada após {sid}")
    return a, tag_close + m.start()


def replace_axis4_inner(html: str, sid: str, inner: str) -> str:
    a, b = section_bounds(html, sid)
    sec = html[a:b]
    i = sec.find(MARKER)
    if i == -1:
        raise SystemExit(f"marcador eixo 4 não encontrado em {sid}")
    start = i + len(MARKER)
    end = sec.find("</p>", start)
    if end == -1:
        raise SystemExit(f"</p> do eixo 4 não encontrado em {sid}")
    if sec[start:end] == inner:
        return html
    sec2 = sec[:start] + inner + sec[end:]
    return html[:a] + sec2 + html[b:]


def polish_chunk(chunk: str) -> str:
    t = chunk
    for tail in TAILS_REMOVE:
        t = t.replace(tail, "")
    t = t.replace(MEGH_TAIL, ".")
    t = t.replace(CATRACA_FIX[0], CATRACA_FIX[1])
    t = t.replace(
        " (Netflix etc.); registro político na imprensa não muda o recorte 18+.",
        " (Netflix etc.).",
    )
    t = re.sub(r"\.{2,}", ".", t)
    t = re.sub(r"\s+\.", ".", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    orig = html

    a = html.find('id="perfis"')
    b = html.find('id="metricas"', a)
    if a == -1 or b == -1:
        raise SystemExit("perfis/metricas não encontrados")
    html = html[:a] + polish_chunk(html[a:b]) + html[b:]

    for sid, inner in (
        ("paulo-victor-freitas", PAULO_INNER),
        ("morgana-camila", MORGANA_INNER),
        ("barbara-coura", BARBARA_INNER),
        ("rafael-saraiva", RAFAEL_SARAIVA_INNER),
    ):
        html = replace_axis4_inner(html, sid, inner)

    # Raquel: só o fecho do eixo 4 (sem lista do que “não” ocorre)
    html = html.replace(
        "No X o tom segue adulto e humorístico, sem incentivo a jogo para menores nem sexualização de menor; manter checagem de feed na veiculação.",
        "No X o tom segue adulto e humorístico; validar na veiculação.",
    )

    if html == orig:
        print("Nada alterado.")
        return
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
