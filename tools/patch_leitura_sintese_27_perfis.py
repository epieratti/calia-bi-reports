#!/usr/bin/env python3
"""Atualiza Leitura rápida e Síntese do conjunto para listar e refletir os 27 perfis."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

CREATORS: list[tuple[str, str, str]] = [
    ("giovanna-pitel", "1", "Giovanna Pitel"),
    ("rafael-gratta", "2", "Rafael Gratta"),
    ("indio-behn", "3", "Índio Behn"),
    ("megh-melry", "4", "Megh Melry"),
    ("cleane-sampaio", "5", "Cleane Sampaio"),
    ("ivan-baron", "6", "Ivan Baron"),
    ("mila-costa", "7", "Mila Costa"),
    ("cristian-wariu", "8", "Cristian Wariu"),
    ("cereja", "9", "Cereja"),
    ("aline-costa", "10", "Aline Costa"),
    ("davi", "11", "Davi"),
    ("paula-mineira", "12", "Paula Mineira"),
    ("catraca-livre", "13", "Catraca Livre"),
    ("julia-ferrari", "14", "Julia Ferrari"),
    ("joao-vitor-mello", "15", "João Vítor Mello"),
    ("lorena-rufino", "16", "Lorena Rufino"),
    ("barbara-coura", "17", "Bárbara Coura"),
    ("raphael-vicente", "18", "Raphael Vicente"),
    ("rafael-saraiva", "19", "Rafael Saraiva"),
    ("pedro-ottoni", "20", "Pedro Ottoni"),
    ("ademara", "21", "Ademara"),
    ("linnyke-alves", "22", "Linnyke Alves"),
    ("felipe-hatori", "23", "Felipe Hatori"),
    ("julimara", "24", "Julimara"),
    ("raquel-real", "25", "Raquel Real"),
    ("morgana-camila", "26", "Morgana Camila"),
    ("paulo-victor-freitas", "27", 'Paulo Victor Freitas ("Seu Freitaz")'),
]


def name_list_plain() -> str:
    parts = [label for _, _, label in CREATORS]
    return ", ".join(parts[:-1]) + f" e {parts[-1]}"


def ul_creators() -> str:
    lis = []
    for slug, num, label in CREATORS:
        lis.append(
            f"<li><a class='toc-link' href='#{slug}'>{num}. {label}</a></li>"
        )
    return (
        "<ul class='grid sm:grid-cols-2 lg:grid-cols-3 gap-x-3 gap-y-1.5 list-none m-0 p-0 text-sm text-slate-700'>"
        + "".join(lis)
        + "</ul>"
    )


def new_leitura_inner() -> str:
    return f"""<p class='text-sm font-semibold text-slate-800 mb-5 leading-snug'>Dossiê do <strong class="font-semibold text-slate-900">Squad Always ON Loterias 2026</strong> com <strong class="font-semibold text-slate-900">27</strong> creators. A tabela-resumo, as secções <strong class="font-semibold text-slate-900">Perfis</strong> e <strong class="font-semibold text-slate-900">Métricas nas redes</strong> fecham os quatro eixos (Concorrência, Polêmicas, Política, Loterias 18+) com links. As datas na coluna <strong class="font-semibold text-slate-900">Coleta (ref.)</strong> mudam — valide de novo perto da veiculação.</p><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm mb-5'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Creators neste arquivo (ordem do pedido)</p>{ul_creators()}</div><div class='grid md:grid-cols-2 gap-4'><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Concorrência (bets / loterias)</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Sem publi paga homologada de casa de apostas ou loteria concorrente na coleta para o conjunto; calibrar humor e menções a apostas (Bárbara Coura, Raquel Real, Rafael Saraiva com sketch <strong class="font-semibold text-slate-900">Bet Kids</strong> — só o título) e cruzar brief com parcerias de outras categorias em perfis de alta exposição (ex.: Giovanna Pitel, Catraca Livre).</span></li></ul></div><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Polêmicas</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Maior ruído de mídia ou reputação em <strong class="font-semibold text-slate-900">Catraca Livre</strong>, <strong class="font-semibold text-slate-900">Rafael Gratta</strong>, <strong class="font-semibold text-slate-900">Raphael Vicente</strong> e <strong class="font-semibold text-slate-900">Ademara</strong>; demais perfis na faixa baixa a moderada na coleta. Casos pontuais: <strong class="font-semibold text-slate-900">Raquel Real</strong> (saúde mental — <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.terra.com.br/diversao/gente/estrela-do-tiktok-raquel-real-comenta-diagnostico-minha-cabeca-nao-para,2ad97a732c01178851689f9cf5d4bdb5m0e9wnlq.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Terra</strong></a>), <strong class="font-semibold text-slate-900">Morgana Camila</strong> (bullying — <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a>), <strong class="font-semibold text-slate-900">Paulo Victor Freitas</strong> (xenofobia de terceiros — <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>).</span></li></ul></div><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Política</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Pauta ou militância mais visível em <strong class="font-semibold text-slate-900">Ivan Baron</strong>, <strong class="font-semibold text-slate-900">Cristian Wariu</strong> e <strong class="font-semibold text-slate-900">Ademara</strong>; <strong class="font-semibold text-slate-900">Paulo Victor Freitas</strong> com discurso regional na imprensa sem partido citado (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>). Demais creators sem filiação clara nas fontes usadas.</span></li></ul></div><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Loterias 18+</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Mais atenção ao eixo em <strong class="font-semibold text-slate-900">Linnyke Alves</strong> (menor recorrente em miniaturas), <strong class="font-semibold text-slate-900">Morgana Camila</strong> (menores em desfile público — <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>; pista de audiência) e <strong class="font-semibold text-slate-900">Julimara</strong> (faixa baixa a moderada). <strong class="font-semibold text-slate-900">Felipe Hatori</strong> e a maior parte dos demais ficam em baixo na coleta; <strong class="font-semibold text-slate-900">Raquel Real</strong> e <strong class="font-semibold text-slate-900">Paulo Victor Freitas</strong> sem indício de público infantil na amostra (lista de redes da Raquel também em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Fashion Bubbles</strong></a>).</span></li></ul></div></div>"""


def new_sintese_inner() -> str:
    names_plain = name_list_plain()
    return f"""<p class='text-xs text-slate-500 mb-3 leading-relaxed break-words'>Creators neste dossiê (27), na ordem do pedido: {names_plain}.</p><p class='text-sm text-slate-700 mb-4 leading-relaxed'>No recorte agregado, <strong class="font-semibold text-slate-900">Catraca Livre</strong>, <strong class="font-semibold text-slate-900">Rafael Gratta</strong>, <strong class="font-semibold text-slate-900">Raphael Vicente</strong> e <strong class="font-semibold text-slate-900">Ademara</strong> concentram mais exposição a polêmica ou agenda sensível na imprensa aberta. <strong class="font-semibold text-slate-900">Ivan Baron</strong>, <strong class="font-semibold text-slate-900">Cristian Wariu</strong> e <strong class="font-semibold text-slate-900">Ademara</strong> carregam pauta política explícita ou proximidade noticiada com poder; <strong class="font-semibold text-slate-900">Paulo Victor Freitas</strong> entra por discurso regional sem partido citado. No eixo <strong class="font-semibold text-slate-900">Loterias 18+</strong>, o zoom maior fica em <strong class="font-semibold text-slate-900">Linnyke Alves</strong>, <strong class="font-semibold text-slate-900">Morgana Camila</strong> e <strong class="font-semibold text-slate-900">Julimara</strong>; os demais 24 perfis ficam majoritariamente em leitura de risco baixa a moderada na coleta, com nuances nos cards. Todos os nomes acima têm perfil numerado na secção <strong class="font-semibold text-slate-900">Perfis</strong> e linha nas tabelas de <strong class="font-semibold text-slate-900">Métricas nas redes</strong>.</p><div class='grid md:grid-cols-2 gap-4'><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Leitura para Caixa</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Tratar o dossiê como um <strong class="font-semibold text-slate-900">conjunto único de 27</strong>: priorizar checagem jurídica e de marca nos perfis marcados na tabela-resumo como moderado ou alto e, no 18+, cruzar criativo com indícios de público infantil onde o eixo subiu (Linnyke, Morgana, Julimara).</span></li><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Estilos variam de humor de massa e reality (<strong class="font-semibold text-slate-900">Giovanna Pitel</strong>, <strong class="font-semibold text-slate-900">Aline Costa</strong>, <strong class="font-semibold text-slate-900">Raquel Real</strong>) a causas, política e comunidade (<strong class="font-semibold text-slate-900">Ivan Baron</strong>, <strong class="font-semibold text-slate-900">Cristian Wariu</strong>, <strong class="font-semibold text-slate-900">Raphael Vicente</strong>, <strong class="font-semibold text-slate-900">Paulo Victor Freitas</strong>) e mídia nativa (<strong class="font-semibold text-slate-900">Catraca Livre</strong>); alinhar peça ao tom de cada creator listado no parágrafo acima e nos perfis.</span></li><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Números de alcance e engajamento por rede estão centralizados em <strong class="font-semibold text-slate-900">Métricas nas redes</strong>, com a coluna <strong class="font-semibold text-slate-900">Coleta (ref.)</strong> para saber a data de cada ficha.</span></li></ul></div><div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'><p class='text-xs font-black uppercase tracking-wide text-calia-navy border-l-4 border-calia-gold pl-3 -ml-px mb-3'>Cobertura do arquivo</p><ul class='list-none space-y-2.5 m-0 p-0'><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>Cada um dos <strong class="font-semibold text-slate-900">27</strong> nomes tem linha na <strong class="font-semibold text-slate-900">tabela-resumo</strong> (eixos), <strong class="font-semibold text-slate-900">perfil</strong> próprio na secção Perfis e entradas nas tabelas de Instagram, TikTok, YouTube e X em Métricas nas redes (quando houver handle homologado na coleta).</span></li><li class='flex gap-2.5 text-sm text-slate-700 leading-snug'><span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span><span>A ordem <strong class="font-semibold text-slate-900">1–27</strong> do sumário segue a ordem do pedido original do squad.</span></li></ul></div></div>"""


def patch() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    # --- leitura ---
    m_start = html.find('<section id="leitura"')
    if m_start == -1:
        raise SystemExit("secção leitura não encontrada")
    head_end = html.find("</h2></div>", m_start) + len("</h2></div>")
    sec_end = html.find("</section>", head_end)
    if sec_end == -1:
        raise SystemExit("fim leitura não encontrado")
    old_inner = html[head_end:sec_end]
    new_html = html[:head_end] + new_leitura_inner() + html[sec_end:]
    html = new_html

    # --- sintese ---
    m_start = html.find('<section id="sintese"')
    if m_start == -1:
        raise SystemExit("secção sintese não encontrada")
    head_end = html.find("</h2></div>", m_start) + len("</h2></div>")
    sec_end = html.find("</section>", head_end)
    if sec_end == -1:
        raise SystemExit("fim sintese não encontrado")
    html = html[:head_end] + new_sintese_inner() + html[sec_end:]

    HTML_PATH.write_text(html, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    patch()
