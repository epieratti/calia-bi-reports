#!/usr/bin/env python3
"""
Gera caixa/20260511-dossie-squad-always-on-loterias-2026.html a partir de
20260504 + conteúdos de perfis/tabelas/métricas dos dossiês 20260401 e 20260406.
Acrescenta o lote 3 (três creators) com os quatro eixos e métricas 11/05/2026.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAIXA = ROOT / "caixa"

FILES_ORDER = [
    ("20260401-dossie-squad-always-on-loterias-2026.html", "01/04/2026"),
    ("20260406-dossie-squad-always-on-loterias-2026.html", "06/04/2026"),
    ("20260504-dossie-squad-always-on-loterias-2026.html", "04/05/2026"),
]

LOTPLUS_TD = (
    "<td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>"
    "<strong class=\"font-semibold text-slate-900\">Limite desta consolidação (11/05/2026):</strong> "
    "o sub-eixo <strong class=\"font-semibold text-slate-900\">«Loterias 18+»</strong> "
    "<strong class=\"font-semibold text-slate-900\">não foi reexecutado</strong> neste arquivo para este nome; "
    "permanece a leitura da <strong class=\"font-semibold text-slate-900\">entrega anterior</strong> datada. "
    "Para veiculação, <strong class=\"font-semibold text-slate-900\">recomenda-se</strong> nova amostra visual do feed "
    "com o mesmo critério.</td>"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(html: str, section_id: str) -> str:
    needle = f'<section id="{section_id}"'
    alt = f"<section id='{section_id}'"
    pos = html.find(needle)
    if pos < 0:
        pos = html.find(alt)
    if pos < 0:
        raise ValueError(f"Section {section_id} not found")
    start = html.find(">", pos) + 1
    depth = 1
    i = start
    while i < len(html) and depth:
        open_s = html.find("<section", i)
        close_s = html.find("</section>", i)
        if close_s < 0:
            break
        if open_s != -1 and open_s < close_s:
            depth += 1
            i = open_s + 8
        else:
            depth -= 1
            if depth == 0:
                return html[start:close_s]
            i = close_s + 10
    raise ValueError(f"Unbalanced section {section_id}")


def strip_metricas_heading(inner: str) -> str:
    return re.sub(
        r'^\s*<div class="section-header"[^>]*>.*?</div>\s*',
        "",
        inner,
        count=1,
        flags=re.S,
    )


def extract_tbody(table_html: str) -> str:
    m = re.search(r"<tbody[^>]*>(.*?)</tbody>", table_html, re.S)
    if not m:
        raise ValueError("tbody not found")
    return m.group(1)


def add_loterias_column_to_rows(tbody: str) -> str:
    out = []
    for m in re.finditer(r"<tr[^>]*>.*?</tr>", tbody, re.S):
        row = m.group(0)
        n_td = len(re.findall(r"<td", row))
        if n_td >= 6:
            out.append(row)
        else:
            out.append(row.replace("</tr>", LOTPLUS_TD + "</tr>", 1))
    return "".join(out)


def merge_perfis_inner() -> str:
    chunks = []
    for fname, _ in FILES_ORDER:
        html = _read(CAIXA / fname)
        inner = extract_section(html, "perfis")
        inner = re.sub(
            r'^\s*<div class="section-header mb-6">.*?</div>\s*',
            "",
            inner,
            count=1,
            flags=re.S,
        )
        chunks.append(inner.strip())
    chunks.append(LOTE3_PERFIS_HTML.strip())
    return "\n\n".join(chunks)


def merge_tabela_inner() -> str:
    thead60504 = ""
    parts = []
    for fname, _ in FILES_ORDER:
        html = _read(CAIXA / fname)
        tab = extract_section(html, "tabela")
        if fname.startswith("20260504"):
            m = re.search(r"<thead[^>]*>.*?</thead>", tab, re.S)
            if m:
                thead60504 = m.group(0)
        parts.append(add_loterias_column_to_rows(extract_tbody(tab)))
    parts.append(LOTE3_TABELA_ROWS.strip())
    thead = thead60504
    return (
        f"<div class='overflow-x-auto rounded border border-slate-200'>"
        f"<table class='min-w-full'>{thead}<tbody>{''.join(parts)}</tbody></table></div>"
    )


def build_metricas_section() -> str:
    blocks = [
        "<div class='section-header'><h2 class='text-xl font-black text-calia-navy'>Métricas nas redes</h2></div>",
        "<p class='text-sm text-slate-600 mb-6 leading-relaxed break-words'>"
        "Tabelas por <strong class=\"font-semibold text-slate-900\">data de referência</strong> da entrega de origem; "
        "o bloco final é o <strong class=\"font-semibold text-slate-900\">lote 3</strong> (coleta <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>). "
        "Confrontar de novo os números próximo à veiculação.</p>",
    ]
    for fname, label in FILES_ORDER:
        html = _read(CAIXA / fname)
        inner = strip_metricas_heading(extract_section(html, "metricas"))
        blocks.append(
            "<section class='mb-10 rounded-lg border border-slate-200 bg-slate-50/40 p-4'>"
            f"<h3 class='text-lg font-black text-calia-navy mb-3'>Referência {label}</h3>{inner}</section>"
        )
    blocks.append(
        "<section class='mb-10 rounded-lg border border-slate-200 bg-slate-50/40 p-4'>"
        "<h3 class='text-lg font-black text-calia-navy mb-3'>Referência 11/05/2026 — lote 3</h3>"
        f"{LOTE3_METRICAS_HTML}</section>"
    )
    return "".join(blocks)


# --- Lote 3 (conteúdo editorial + URLs; sem nomes de ferramentas internas) ---

LOTE3_PERFIS_HTML = r"""
<div id='squad-lote-3' class='scroll-mt-20 mb-10'><h3 class='text-lg font-black text-calia-navy border-b-2 border-calia-gold pb-2 mb-6'>Squad — lote 3 (mai/2026)</h3>

<section id='raquel-real' class='card-audit scroll-mt-20'><div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'><h2 class='text-xl font-black text-calia-navy'>1. Raquel Real</h2><span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'><span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span><span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/90 border border-emerald-100 shadow-sm'>Baixo — humor adulto; calibrar «bet» só em título de obra de terceiros</span></span></div><div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 md:grid-cols-3 gap-2'><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-gradient-to-b from-pink-500 to-rose-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>Instagram</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raquelrealoficial</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span><span class='font-semibold tabular-nums text-slate-900'>—</span></span><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span><span class='font-semibold tabular-nums text-slate-900'>—</span></span></div></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-800' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>TikTok</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raqrealoficial</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span><span class='font-semibold tabular-nums text-slate-900'>252,8K</span></span><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Curtidas</span><span class='font-semibold tabular-nums text-slate-900'>12,8M</span></span></div></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-red-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>YouTube</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raquelrealoficial</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Insc.</span><span class='font-semibold tabular-nums text-slate-900'>12,9K</span></span></div></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raquelrealofc</p><p class='mt-1.5 text-[9px] text-slate-500'>Handle listado em matéria de apresentação; conferir bio e atividade no perfil.</p></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Comediante, roteirista e apresentadora; personagem da «diaba» e esquetes sobre absurdos da internet. Trajetória e redes em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Fashion Bubbles</strong></a> (acesso <strong class="font-semibold text-slate-900">11/05/2026</strong>, tipo: matéria agregadora com links para posts do Instagram e lista de redes). Biografia e pauta de saúde mental em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.terra.com.br/diversao/gente/estrela-do-tiktok-raquel-real-comenta-diagnostico-minha-cabeca-nao-para,2ad97a732c01178851689f9cf5d4bdb5m0e9wnlq.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Terra</strong></a> (<strong class="font-semibold text-slate-900">2024</strong>, entrevista). Sátira da cena digital em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.metropoles.com/entretenimento/diaba-do-tiktok-raquel-real-usa-humor-para-criticar-bizarrices-da-web" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Metrópoles</strong></a>.</p><div class='grid md:grid-cols-2 gap-4'><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>1. Concorrência (bets / loterias / jogos)</p><p class='text-sm text-slate-700 leading-relaxed'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de casa de apostas, cassino ou loteria concorrente nas fontes desta coleta. O humor trata de fenômenos da internet de forma genérica — sem CTA de jogo.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>2. Polêmicas e situações delicadas</p><p class='text-sm text-slate-700 leading-relaxed'>Matérias citadas tratam de <strong class="font-semibold text-slate-900">saúde mental</strong> com tom informativo (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.terra.com.br/diversao/gente/estrela-do-tiktok-raquel-real-comenta-diagnostico-minha-cabeca-nao-para,2ad97a732c01178851689f9cf5d4bdb5m0e9wnlq.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Terra</strong></a>) — <strong class="font-semibold text-slate-900">sem</strong> episódio documentado de risco reputacional para anunciante público além do recorte informativo.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>3. Política e pautas sensíveis</p><p class='text-sm text-slate-700 leading-relaxed'><strong class="font-semibold text-slate-900">Sem</strong> filiação partidária ou candidatura localizada nas fontes desta coleta. Humor pode citar comportamento social; <strong class="font-semibold text-slate-900">não</strong> confundir sátira de personagem com posicionamento eleitoral sem prova em post com link.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+</p><p class='text-sm text-slate-700 leading-relaxed'>Conteúdo majoritariamente de <strong class="font-semibold text-slate-900">humor adulto</strong> e crítica de «influencer/coach» (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.metropoles.com/entretenimento/diaba-do-tiktok-raquel-real-usa-humor-para-criticar-bizarrices-da-web" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Metrópoles</strong></a>; <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Fashion Bubbles</strong></a>). Há esquetes com <strong class="font-semibold text-slate-900">pai</strong> em cena em formato de entretenimento familiar citado na mesma matéria — <strong class="font-semibold text-slate-900">não</strong> é canal infantil; leitura qualitativa: <strong class="font-semibold text-slate-900">risco moderado/baixo</strong> de associação a público infantil <strong class="font-semibold text-slate-900">frente</strong> ao produto 18+, sujeito a amostra de feed na data da campanha.</p></div></div></section>

<section id='morgana-camila' class='card-audit scroll-mt-20'><div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'><h2 class='text-xl font-black text-calia-navy'>2. Morgana Camila</h2><span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'><span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span><span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Moderado no eixo 18+ — desfiles cívicos com escolas</span></span></div><div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 md:grid-cols-3 gap-2'><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-gradient-to-b from-pink-500 to-rose-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>Instagram</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@morganacamila</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span><span class='font-semibold tabular-nums text-slate-900'>—</span></span><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span><span class='font-semibold tabular-nums text-slate-900'>—</span></span></div></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-800' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>TikTok</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@morganacamila</p><p class='mt-1.5 text-[9px] text-slate-500 leading-snug'><strong class="font-semibold text-slate-900">Prova em 11/05/2026:</strong> a URL <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.tiktok.com/@morganacamila" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">tiktok.com/@morganacamila</strong></a> resolve para conta <strong class="font-semibold text-slate-900">sem bio e sem audiência</strong> (não bate com o alcance descrito na imprensa). <strong class="font-semibold text-slate-900">TikTok oficial com confiança alta não foi fechado</strong> nesta coleta — lacuna explícita.</p></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-red-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>YouTube</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@morganacamila</p><p class='mt-1.5 text-[9px] text-slate-500'>Canal identificado pelo handle; métricas na tabela.</p></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p><p class='text-sm text-slate-600'><strong class="font-semibold text-slate-900">Não</strong> consta perfil público com âncora segura nesta coleta (tentativa de acesso ao host <strong class="font-semibold text-slate-900">x.com</strong> retornou bloqueio automatizado no ambiente do agente).</p></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Criadora de conteúdo cearense conhecida pela narração humorística de desfiles cívicos em Maranguape; trajetória em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a> e cobertura adicional em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a>.</p><div class='grid md:grid-cols-2 gap-4'><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>1. Concorrência (bets / loterias / jogos)</p><p class='text-sm text-slate-700 leading-relaxed'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas ou loteria concorrente nas fontes citadas. Pauta principal: evento cívico e humor regional.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>2. Polêmicas e situações delicadas</p><p class='text-sm text-slate-700 leading-relaxed'>Matérias descrevem <strong class="font-semibold text-slate-900">bullying</strong> histórico por timbre de voz e superação profissional (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a>) — enquadramento positivo na imprensa, não «cancelamento» documentado.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>3. Política e pautas sensíveis</p><p class='text-sm text-slate-700 leading-relaxed'>Entrevistas giram em torno de <strong class="font-semibold text-slate-900">cultura local e desfile</strong> (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>). <strong class="font-semibold text-slate-900">Sem</strong> filiação partidária citada nas fontes desta coleta.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+</p><p class='text-sm text-slate-700 leading-relaxed'>O próprio relato em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a> descreve <strong class="font-semibold text-slate-900">escolas</strong> e <strong class="font-semibold text-slate-900">fanfarras</strong> no desfile — em vídeo, <strong class="font-semibold text-slate-900">menores costumam aparecer</strong> como parte do evento público narrado. Isso <strong class="font-semibold text-slate-900">não</strong> é público-alvo infantil do canal, mas gera <strong class="font-semibold text-slate-900">exposição recorrente a menores de idade em cena</strong> no material icônico da creator — ponto de atenção para <strong class="font-semibold text-slate-900">Loterias 18+</strong> (leitura qualitativa, sem painel de idade da audiência).</p></div></div></section>

<section id='paulo-victor-freitas' class='card-audit scroll-mt-20'><div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'><h2 class='text-xl font-black text-calia-navy'>3. Paulo Victor Freitas («Seu Freitaz»)</h2><span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'><span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span><span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Moderado no eixo política/pauta — opinião regional e mídia</span></span></div><div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 md:grid-cols-3 gap-2'><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-gradient-to-b from-pink-500 to-rose-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>Instagram</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@seufreitaz</p><p class='mt-1.5 text-[9px] text-slate-500 leading-snug'>O <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.tiktok.com/@seufreitaz" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">TikTok @seufreitaz</strong></a> (bio, <strong class="font-semibold text-slate-900">11/05/2026</strong>) aponta também <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.instagram.com/pvfreitazzz/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">@pvfreitazzz</strong></a>; o <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> cita o mesmo projeto com link para <strong class="font-semibold text-slate-900">Instagram</strong> — triangulação para o titular.</p></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-800' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>TikTok</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@seufreitaz</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span><span class='font-semibold tabular-nums text-slate-900'>297,9K</span></span><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Curtidas</span><span class='font-semibold tabular-nums text-slate-900'>2,1M</span></span></div><p class='mt-1.5 text-[9px] text-slate-500'>Cabeçalho público do perfil, <strong class="font-semibold text-slate-900">11/05/2026</strong>.</p></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-red-600' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>YouTube</p><p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@seufreitaz</p><div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'><span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Insc.</span><span class='font-semibold tabular-nums text-slate-900'>18,3K</span></span></div><p class='mt-1.5 text-[9px] text-slate-500'>Página «About» pública, <strong class="font-semibold text-slate-900">11/05/2026</strong>.</p></div></div></div><div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80'><div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div><div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p><p class='text-sm text-slate-600'><strong class="font-semibold text-slate-900">Não</strong> fechado nesta coleta (bloqueio ao host no ambiente do agente).</p></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Publicitário e humorista potiguar; matéria de apresentação com números de alcance e contexto regional em <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> (<strong class="font-semibold text-slate-900">08/10/2025</strong>).</p><div class='grid md:grid-cols-2 gap-4'><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>1. Concorrência (bets / loterias / jogos)</p><p class='text-sm text-slate-700 leading-relaxed'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas ou loteria concorrente na matéria do <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> nem nas bios públicas citadas.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>2. Polêmicas e situações delicadas</p><p class='text-sm text-slate-700 leading-relaxed'>O <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> registra exposição a <strong class="font-semibold text-slate-900">comentários xenofóbicos</strong> — risco de imagem ligado a <strong class="font-semibold text-slate-900">discurso de ódio na rede</strong>, não a conduta do creator.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>3. Política e pautas sensíveis</p><p class='text-sm text-slate-700 leading-relaxed'>O mesmo texto do <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> descreve <strong class="font-semibold text-slate-900">opinião</strong> sobre identidade regional, estereótipo e valorização do Nordeste — <strong class="font-semibold text-slate-900">pauta social</strong>, não filiação partidária. Em <strong class="font-semibold text-slate-900">ano eleitoral</strong>, avaliar sensibilidade institucional a creators com forte discurso territorial.</p></div><div class='rounded border border-slate-200 p-4 bg-white'><p class='text-xs font-black uppercase text-calia-gold mb-2'>4. Loterias 18+</p><p class='text-sm text-slate-700 leading-relaxed'>Humor sobre <strong class="font-semibold text-slate-900">hábitos regionais</strong> e <strong class="font-semibold text-slate-900">adulto jovem</strong> na linha editorial descrita pelo <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>; <strong class="font-semibold text-slate-900">sem</strong> foco em público infantil nas fontes. Relato autobiográfico de uso de câmera na infância é <strong class="font-semibold text-slate-900">contexto de entrevista</strong>, não formato atual de conteúdo infantil.</p></div></div></section>
</div>
"""

LOTE3_TABELA_ROWS = r"""
<tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong>Raquel Real</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><span class='inline-flex max-w-full min-w-0 rounded-lg px-2.5 py-1.5 text-xs font-bold leading-snug break-words text-left bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/90 border border-emerald-100 shadow-sm'>Baixo — humor adulto; calibrar «bet» só em título de obra de terceiros</span></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas ou loteria concorrente nas fontes desta coleta.</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Pauta de saúde mental informativa (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.terra.com.br/diversao/gente/estrela-do-tiktok-raquel-real-comenta-diagnostico-minha-cabeca-nao-para,2ad97a732c01178851689f9cf5d4bdb5m0e9wnlq.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Terra</strong></a>).</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class="font-semibold text-slate-900">Sem</strong> filiação partidária localizada nas fontes desta coleta.</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Humor adulto; esquetes com família citadas na matéria (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">Fashion Bubbles</strong></a>) — <strong class="font-semibold text-slate-900">não</strong> é canal infantil; rever feed na data da campanha.</td></tr>
<tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong>Morgana Camila</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><span class='inline-flex max-w-full min-w-0 rounded-lg px-2.5 py-1.5 text-xs font-bold leading-snug break-words text-left bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Moderado no eixo 18+ — desfiles cívicos com escolas</span></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas nas fontes citadas.</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Bullying histórico narrado como superação (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">R7</strong></a>).</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class="font-semibold text-slate-900">Sem</strong> filiação partidária nas fontes desta coleta (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>).</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Desfiles com <strong class="font-semibold text-slate-900">escolas e fanfarras</strong> — menores em cena no material icônico (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://www.opovo.com.br/noticias/ceara/maranguape/2022/09/14/conheca-morgana-camila-famosa-pela-narracao-dos-desfiles-de-7-de-setembro-em-maranguape.html" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">O Povo</strong></a>).</td></tr>
<tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong>Paulo Victor Freitas</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><span class='inline-flex max-w-full min-w-0 rounded-lg px-2.5 py-1.5 text-xs font-bold leading-snug break-words text-left bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Moderado no eixo política/pauta — opinião regional e mídia</span></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class="font-semibold text-slate-900">Não</strong> localizada publi paga de apostas (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>).</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Exposição a comentários xenofóbicos descrita pelo <a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>.</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Discurso sobre <strong class="font-semibold text-slate-900">identidade regional</strong> e estereótipo (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>) — <strong class="font-semibold text-slate-900">sem</strong> filiação partidária citada.</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>Humor adulto sobre costumes; <strong class="font-semibold text-slate-900">sem</strong> foco infantil nas fontes; relato de infância é <strong class="font-semibold text-slate-900">entrevista</strong> (<a class="dossier-source-link text-slate-700 hover:text-slate-900 underline font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 break-words" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a>).</td></tr>
"""

LOTE3_METRICAS_HTML = r"""
<p class='text-sm text-slate-600 mb-4 leading-relaxed'><strong class="font-semibold text-slate-900">Instagram:</strong> painel manual (Social Blade) <strong class="font-semibold text-slate-900">não</strong> preenchido aqui para estes três nomes — células com <strong class="font-semibold text-slate-900">—</strong> até revisão humana. <strong class="font-semibold text-slate-900">TikTok:</strong> onde indicado, seguidores/curtidas do <strong class="font-semibold text-slate-900">cabeçalho público</strong> do perfil em <strong class="font-semibold text-slate-900">11/05/2026</strong> (prova primária com URL). <strong class="font-semibold text-slate-900">YouTube:</strong> inscritos via página pública «About» em <strong class="font-semibold text-slate-900">11/05/2026</strong> quando obtido.</p>
<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>Instagram</h3><div class='overflow-x-auto rounded border border-slate-200'><table class='min-w-full'><thead class='bg-slate-50'><tr><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Nome</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Usuário</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Seguidores</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Posts</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Curtidas méd.</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Coment. méd.</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Engaj.</th></tr></thead><tbody><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Raquel Real</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>raquelrealoficial</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Morgana Camila</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>morganacamila</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Paulo Victor Freitas</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>seufreitaz / pvfreitazzz</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td></tr></tbody></table></div><p class='text-xs text-slate-500 mt-3'>Pendência explícita: preencher após Social Blade manual. O <a class="dossier-source-link" href="https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml" target="_blank" rel="noopener noreferrer"><strong class="font-semibold text-slate-900">g1</strong></a> citou ~500 mil seguidores em <strong class="font-semibold text-slate-900">uma</strong> rede em <strong class="font-semibold text-slate-900">08/10/2025</strong> (não substitui coluna SB).</p></section>
<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>TikTok</h3><div class='overflow-x-auto rounded border border-slate-200'><table class='min-w-full'><thead class='bg-slate-50'><tr><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Nome</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Usuário</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Seguidores</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Curtidas totais (cabeçalho)</th></tr></thead><tbody><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Raquel Real</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><a class="dossier-source-link" href="https://www.tiktok.com/@raqrealoficial" target="_blank" rel="noopener noreferrer">raqrealoficial</a></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>252,8K</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>12,8M</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Morgana Camila</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Paulo Victor Freitas</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><a class="dossier-source-link" href="https://www.tiktok.com/@seufreitaz" target="_blank" rel="noopener noreferrer">seufreitaz</a></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>297,9K</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>2,1M</td></tr></tbody></table></div><p class='text-xs text-slate-500 mt-3'>TikTok: cabeçalho público do perfil, <strong class="font-semibold text-slate-900">11/05/2026</strong>. Para Morgana, ver lacuna no corpo do dossiê (URL @morganacamila não bate com imprensa).</p></section>
<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>YouTube</h3><div class='overflow-x-auto rounded border border-slate-200'><table class='min-w-full'><thead class='bg-slate-50'><tr><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Nome</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Usuário</th><th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>Inscritos</th></tr></thead><tbody><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Raquel Real</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>raquelrealoficial</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>12,9K</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Morgana Camila</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>morganacamila</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>—</td></tr><tr><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'><strong class='font-semibold text-slate-900'>Paulo Victor Freitas</strong></td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>seufreitaz</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>18,3K</td></tr></tbody></table></div><p class='text-xs text-slate-500 mt-3'>YouTube: inscritos via página pública do canal, <strong class="font-semibold text-slate-900">11/05/2026</strong>, quando disponível.</p></section>
<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>X</h3><p class='text-sm text-slate-600'>Raquel: <a class="dossier-source-link" href="https://x.com/raquelrealofc" target="_blank" rel="noopener noreferrer">@raquelrealofc</a> (confirmado como lista de redes em <a class="dossier-source-link" href="https://www.fashionbubbles.com/influencers/quem-e-raquel-real/" target="_blank" rel="noopener noreferrer">Fashion Bubbles</a>, <strong class="font-semibold text-slate-900">11/05/2026</strong>). Paulo Victor e Morgana: <strong class="font-semibold text-slate-900">sem</strong> métrica manual fechada nesta coleta — ver perfis.</p></section>
"""

NAV_EXTRA = r"""
        <li><a class="toc-link" href="#squad-lote-3">Squad — lote 3 (mai/2026)</a></li>
"""

NAV_LOTE3_SUB = r"""<li class=''><a class='toc-link font-bold text-calia-navy' href='#squad-lote-3'>Squad — lote 3 (mai/2026)</a><ul class='mt-1 space-y-0.5 pl-0 list-none'><li><a class='toc-link' href='#raquel-real'>1. Raquel Real</a></li><li><a class='toc-link' href='#morgana-camila'>2. Morgana Camila</a></li><li><a class='toc-link' href='#paulo-victor-freitas'>3. Paulo Victor Freitas</a></li></ul></li>"""


def patch_nav(html: str) -> str:
    html = html.replace(
        "<li><a class=\"toc-link\" href=\"#metricas\">Métricas nas redes</a></li>",
        "<li><a class=\"toc-link\" href=\"#metricas\">Métricas nas redes</a></li>" + NAV_EXTRA,
        1,
    )
    if "</ul>\n      <p class=\"text-xs text-slate-500 mt-6" in html:
        html = html.replace(
            "<p class=\"text-xs text-slate-500 mt-6 font-semibold uppercase tracking-wide\">Perfis</p>\n      <ul class=\"toc-list\">",
            "<p class=\"text-xs text-slate-500 mt-6 font-semibold uppercase tracking-wide\">Perfis</p>\n      <ul class=\"toc-list\">" + NAV_LOTE3_SUB,
            1,
        )
    return html


def patch_pedido_leitura_sintese(html: str) -> str:
    html = html.replace(
        "Risco de imagem — três novos nomes (lote 04/05/2026).",
        "Risco de imagem — consolidação dos lotes (abr.–mai./2026) + três novos nomes (lote 3).",
        1,
    )
    html = html.replace(
        "<li><a class=\"toc-link\" href=\"#perfis\">Perfis (Squad (3))</a></li>",
        "<li><a class=\"toc-link\" href=\"#perfis\">Perfis (todos os lotes)</a></li>",
        1,
    )
    ped = (
        "<p class='text-sm text-slate-700 leading-relaxed mb-3'>Este ficheiro <strong class=\"font-semibold text-slate-900\">consolida</strong> os perfis já entregues nos dossiês de <strong class=\"font-semibold text-slate-900\">01/04/2026</strong>, <strong class=\"font-semibold text-slate-900\">06/04/2026</strong> e <strong class=\"font-semibold text-slate-900\">04/05/2026</strong> e acrescenta o <strong class=\"font-semibold text-slate-900\">lote 3</strong> (três creators) com o mesmo quadro de <strong class=\"font-semibold text-slate-900\">quatro eixos</strong>. "
        "Para nomes herdados, a coluna <strong class=\"font-semibold text-slate-900\">«Loterias 18+»</strong> na tabela resumo explica que o sub-eixo <strong class=\"font-semibold text-slate-900\">não foi reexecutado</strong> aqui.</p>"
    )
    html = html.replace(
        "<p class='text-sm text-slate-700 leading-relaxed mb-3'>Levantamento de <strong",
        ped + "<p class='text-sm text-slate-700 leading-relaxed mb-3'>Levantamento de <strong",
        1,
    )
    return html


def main() -> None:
    base = _read(CAIXA / "20260504-dossie-squad-always-on-loterias-2026.html")

    perfis_block = (
        '<section id="perfis" class="scroll-mt-20">\n'
        '      <div class="section-header mb-6"><h2 class="text-xl font-black text-calia-navy">Perfis — análise por camada</h2></div>\n'
        + merge_perfis_inner()
        + "\n    </section>"
    )
    base = re.sub(
        r'<section id="perfis" class="scroll-mt-20">.*?</section>\s*<section id="tabela"',
        perfis_block + '\n\n    <section id="tabela"',
        base,
        count=1,
        flags=re.S,
    )

    tabela_inner = (
        '<section id="tabela" class="card-audit scroll-mt-20">\n'
        '      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Tabela resumo</h2></div>\n'
        '      <p class="text-sm text-slate-600 mb-4">Uma linha por nome; o detalhe está em Perfis e nas métricas. Linhas herdadas: coluna «Loterias 18+» com limite da consolidação.</p>\n'
        + merge_tabela_inner()
        + "\n    </section>"
    )
    base = re.sub(
        r'<section id="tabela" class="card-audit scroll-mt-20">.*?</section>\s*<section id="sintese"',
        tabela_inner + '\n\n    <section id="sintese"',
        base,
        count=1,
        flags=re.S,
    )

    metricas_block = (
        '<section id="metricas" class="card-audit scroll-mt-20">'
        + build_metricas_section()
        + "</section>"
    )
    base = re.sub(
        r'<section id="metricas" class="card-audit scroll-mt-20">.*?</section>\s*<section id="como"',
        metricas_block + '\n\n    <section id="como"',
        base,
        count=1,
        flags=re.S,
    )

    base = patch_nav(base)
    base = patch_pedido_leitura_sintese(base)

    base = re.sub(
        r"Perfis públicos no Instagram, TikTok, YouTube e X na data da coleta \(04/05/2026\)",
        "Perfis públicos no Instagram, TikTok, YouTube e X; datas de coleta por bloco em Métricas (última atualização do conteúdo novo: 11/05/2026)",
        base,
        count=1,
    )

    out = CAIXA / "20260511-dossie-squad-always-on-loterias-2026.html"
    out.write_text(base, encoding="utf-8")
    print("OK", out)


if __name__ == "__main__":
    main()
