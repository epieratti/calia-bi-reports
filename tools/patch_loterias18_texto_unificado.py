#!/usr/bin/env python3
"""Unifica voz do eixo 4 Loterias 18+ (sem separar coletas) e enxuga trechos negativos longos.
Atualiza células correspondentes na Tabela resumo. Idempotente se os trechos-alvo já forem os novos."""

from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

MARKER = "4. Loterias 18+ (audiência)</p><p class='text-sm text-slate-700 leading-relaxed'>"

# inner HTML (sem o <p> wrapper externo)
INNERS: dict[str, str] = {
    "morgana-camila": (
        "Em <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">O Povo</strong></a>, o desfile cívico envolve <strong class=\"font-semibold text-slate-900\">escolas e fanfarras</strong> — <strong class=\"font-semibold text-slate-900\">menores em cena</strong> no material público que viralizou. No <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.youtube.com/watch?v=Xfmr1sHUvq0\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">YouTube</strong></a>, tom de <strong class=\"font-semibold text-slate-900\">história familiar</strong> reforça leitura \"acessível\"; validar demos na veiculação."
    ),
    "raquel-real": (
        "Humor adulto e sátira de \"influencer/coach\" (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.metropoles.com/entretenimento/diaba-do-tiktok-raquel-real-usa-humor-para-criticar-bizarrices-da-web\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Metrópoles</strong></a>). O podcast no <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.youtube.com/watch?v=ftztU7kx-ps\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">YouTube</strong></a> traz pais no humor familiar — não é canal infantil. No X o tom segue adulto e humorístico; validar na veiculação."
    ),
    "paulo-victor-freitas": (
        "Humor sobre costumes adultos (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">g1</strong></a>). Parkour e rap na bio (<a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.nessmgt.com/casting/seu-freitaz\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Ness</strong></a> + <strong class=\"font-semibold text-slate-900\">g1</strong>) apontam público jovem-adulto — não sustentam, por si, leitura de público infantil predominante nem de menores em parcela relevante para o critério Loterias 18+. Validar criativo na veiculação."
    ),
    "linnyke-alves": (
        "Miniaturas do TikTok e trecho do feed do Instagram (capturas internas): <strong class=\"font-semibold text-slate-900\">menor de idade em várias miniaturas</strong> (vários posts), incluindo séries como <strong class=\"font-semibold text-slate-900\">“ditados populares”</strong> e rótulos <strong class=\"font-semibold text-slate-900\">“BIG PAUL / LITTLE PAUL”</strong>. Perfil <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.tiktok.com/@linnykealves\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">TikTok</strong></a>. Imprensa com menor em pauta social: <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.jornaldorap.com.br/noticias/linnyke-alves-mobiliza-redes-sociais-e-arrecada-mais-de-r-400-mil-para-realizar-o-sonho-da-casa-propria-de-crianca-carente/\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Jornal do Rap</strong></a>, <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.polemicaparaiba.com.br/cidades/em-joao-pessoa-humorista-cria-vaquinha-para-ajudar-crianca-que-encantou-a-internet-assista/\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Polêmica Paraíba</strong></a>."
    ),
    "felipe-hatori": (
        "Miniaturas do TikTok (capturas internas): sem menor em destaque; humor adulto urbano. Show <strong class=\"font-semibold text-slate-900\">18+</strong>: <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://guiafloripa.com.br/agenda/shows/vini-santos-felipe-hatori-e-edu-montone-no-floripa-comedy-club\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Guia Floripa</strong></a>. <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.tiktok.com/@felipehatori\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">TikTok</strong></a>."
    ),
    "julimara": (
        "Miniaturas do TikTok (capturas internas): turismo/lifestyle; sem menor em destaque. <a class=\"dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words\" href=\"https://www.tiktok.com/@julimaranasciment\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">TikTok</strong></a>."
    ),
}

# substituições na tabela resumo (texto plano da célula Loterias 18+)
TABELA_SUBS: list[tuple[str, str]] = [
    (
        "Humor adulto; YouTube familiar não infantil; X 11/05/2026 sem apelo a menores.",
        "Humor adulto; YouTube familiar não infantil; X sem apelo a menores.",
    ),
    (
        "Miniaturas com menores recorrentes (mai./2026); validar demos na veiculação.",
        "Miniaturas com menores recorrentes; validar demos na veiculação.",
    ),
    (
        "TikTok mai./2026: sem menor em destaque; humor adulto; show 18+ citado.",
        "TikTok: sem menor em destaque; humor adulto; show 18+ citado.",
    ),
    (
        "TikTok mai./2026: lifestyle; sem menor em destaque nas miniaturas.",
        "TikTok: lifestyle; sem menor em destaque nas miniaturas.",
    ),
    (
        "Humor adulto; apelo jovem (parkour/rap); coleta sem público infantil predominante.",
        "Humor adulto; apelo jovem (parkour/rap); sem público infantil predominante.",
    ),
]


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


def patch_tabela(html: str) -> str:
    t = html
    for old, new in TABELA_SUBS:
        if old in t:
            t = t.replace(old, new, 1)
    return t


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    orig = html
    for sid, inner in INNERS.items():
        html = replace_axis4_inner(html, sid, inner)
    html = patch_tabela(html)
    if html == orig:
        print("Nada alterado (já aplicado).")
        return
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
