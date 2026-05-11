#!/usr/bin/env python3
"""Enxuga os quatro cards (eixos 1–4) dos perfis 25–27 para alinhar ao tamanho dos demais."""
from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

LINK = 'class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words"'

# (sid, n_eixo 1-4, inner)
INNERS: list[tuple[str, int, str]] = [
    (
        "raquel-real",
        1,
        f"""<strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas, cassino ou loteria concorrente nas fontes públicas consultadas. Em <a {LINK} href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Fashion Bubbles</strong></a>, listagem de entretenimento — sem CTA de jogo. No X (<a {LINK} href="https://x.com/raquelrealofc" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">@raquelrealofc</strong></a>), esquetes parodiam formato de publi de bet (<a {LINK} href="https://x.com/raquelrealofc/status/1922454410828959803" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">14/05/2025</strong></a>) e há fala social sobre dívida com apostas (<a {LINK} href="https://x.com/raquelrealofc/status/2050005628005814706" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">01/05/2026</strong></a>) — tratar como sátira, não parceria iGaming. <a {LINK} href="https://www.terra.com.br/diversao/gente/influenciadora-faz-piada-com-virginia-na-cpi-das-bets-e-bebe-reborn,f6a0354ca294b72240c1e0ee55d005115kla7moz.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Terra</strong></a> descreve ironia sobre CPI das Bets; no <a {LINK} href="https://www.tiktok.com/@raqrealoficial/video/7381957732682747141" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">TikTok</strong></a>, sketch em tom satírico institucional.""",
    ),
    (
        "raquel-real",
        2,
        f"""Imprensa e podcast tratam de <strong class="font-semibold text-slate-900">saúde mental</strong> e trabalho com tom informativo. No X, humor de reality (<a {LINK} href="https://x.com/raquelrealofc/status/2018508469658107969" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">03/02/2026</strong></a>) sem episódio grave documentado contra a artista nas fontes ligadas.""",
    ),
    (
        "raquel-real",
        3,
        f"""Sem filiação partidária nas fontes com URL. No X, ironia sobre governo e atualidades (<a {LINK} href="https://x.com/raquelrealofc/status/1986397720802730216" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">06/11/2025</strong></a>) — não configura filiação. Homônimo político na busca não é esta creator.""",
    ),
    (
        "raquel-real",
        4,
        f"""Humor adulto (<a {LINK} href="https://www.metropoles.com/entretenimento/diaba-do-tiktok-raquel-real-usa-humor-para-criticar-bizarrices-da-web" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Metrópoles</strong></a>). Podcast no <a {LINK} href="https://www.youtube.com/watch?v=ftztU7kx-ps" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">YouTube</strong></a> com pais no humor familiar — não é canal infantil; validar na veiculação.""",
    ),
    (
        "morgana-camila",
        1,
        f"""<strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas nas fontes citadas. <a {LINK} href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a> cita publis genéricas — sem iGaming.""",
    ),
    (
        "morgana-camila",
        2,
        f"""Bullying narrado como trajetória positiva (<a {LINK} href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a>).""",
    ),
    (
        "morgana-camila",
        3,
        f"""Sem filiação partidária com URL ligada à creator. Pauta: cultura local e desfile (<a {LINK} href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>).""",
    ),
    (
        "morgana-camila",
        4,
        f"""Em <a {LINK} href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>, desfile cívico com <strong class="font-semibold text-slate-900">escolas e fanfarras</strong> — <strong class="font-semibold text-slate-900">menores em cena</strong> no material público. No <a {LINK} href="https://www.youtube.com/watch?v=Xfmr1sHUvq0" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">YouTube</strong></a>, tom familiar; validar demos na veiculação.""",
    ),
    (
        "paulo-victor-freitas",
        1,
        f"""<strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas nas fontes citadas (<a {LINK} href="https://www.nessmgt.com/casting/seu-freitaz" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Ness</strong></a>; <a {LINK} href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>).""",
    ),
    (
        "paulo-victor-freitas",
        2,
        f"""<a {LINK} href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>: exposição a <strong class="font-semibold text-slate-900">comentários xenofóbicos</strong> — ambiente de rede, não conduta própria.""",
    ),
    (
        "paulo-victor-freitas",
        3,
        f"""Discurso de <strong class="font-semibold text-slate-900">identidade regional</strong> no <a {LINK} href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> e em <a {LINK} href="https://www.youtube.com/watch?v=MApD_rI0dfs" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Os Nordestinos pelo Mundo</strong></a> — <strong class="font-semibold text-slate-900">pauta social</strong>, não filiação. Na <strong class="font-semibold text-slate-900">Máxima</strong>, <a {LINK} href="https://www.youtube.com/watch?v=q7RMLYcLpuQ" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">D'Oamazônico</strong></a> como conteúdo de negócio, não campanha eleitoral.""",
    ),
    (
        "paulo-victor-freitas",
        4,
        f"""Humor adulto (<a {LINK} href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>). Parkour e rap na bio (<a {LINK} href="https://www.nessmgt.com/casting/seu-freitaz" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Ness</strong></a>) apontam jovem-adulto — não sustentam leitura de público infantil predominante no critério Loterias 18+; validar criativo na veiculação.""",
    ),
]

AXIS_LABEL = {
    1: r"1\. Concorrência",
    2: r"2\. Polêmicas",
    3: r"3\. Política",
    4: r"4\. Loterias 18\+",
}


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


def replace_axis_inner(sec: str, n: int, inner: str) -> tuple[str, bool]:
    lab = AXIS_LABEL[n]
    pat = rf"(<p class='text-xs font-black uppercase text-calia-gold mb-[12]'>{lab}[^<]*</p><p class='text-sm text-slate-700 leading-relaxed'>)([\s\S]*?)(</p></div>)"
    m = re.search(pat, sec)
    if not m:
        raise SystemExit(f"eixo {n} não encontrado no trecho")
    if m.group(2) == inner:
        return sec, False
    return sec[: m.start(2)] + inner + sec[m.end(2) :], True


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    orig = html
    for sid, n, inner in INNERS:
        a, b = section_bounds(html, sid)
        sec = html[a:b]
        sec2, ch = replace_axis_inner(sec, n, inner)
        if ch:
            html = html[:a] + sec2 + html[b:]
    if html == orig:
        print("Nada alterado (já aplicado).")
        return
    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
