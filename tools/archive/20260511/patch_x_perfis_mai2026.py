#!/usr/bin/env python3
"""Atualiza cartões X e tabela 01/04 no dossiê consolidado (snapshot página pública X, 11/05/2026)."""
from pathlib import Path

P = Path("/workspace/caixa/20260511-dossie-squad-always-on-loterias-2026.html")
t = P.read_text(encoding="utf-8")

X_LORENA = (
    "<div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80 hover:border-slate-300 hover:shadow transition-shadow'>"
    "<div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div>"
    "<div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p>"
    "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@lorerufis</p>"
    "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
    "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
    "<span class='font-semibold tabular-nums text-slate-900'>24,2K</span></span></div>"
    "<div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'>"
    "<span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' "
    "title='Posts próprios visíveis em 2025 na página pública'>posts recentes</span>"
    "<p class='text-[9px] text-slate-500 leading-snug break-words'>Handle homologado no squad 06/04; seguidores na página pública em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>.</p>"
    "</div></div></div></div>"
)

X_RAPHAEL = (
    "<div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80 hover:border-slate-300 hover:shadow transition-shadow'>"
    "<div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div>"
    "<div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p>"
    "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raphaelviicente</p>"
    "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
    "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
    "<span class='font-semibold tabular-nums text-slate-900'>224,2K</span></span></div>"
    "<div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'>"
    "<span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-slate-100 text-slate-700 ring-1 ring-slate-200' "
    "title='Últimas datas visíveis na amostra pública ~2022'>sem posts recentes</span>"
    "<p class='text-[9px] text-slate-500 leading-snug break-words'>Conta homologada no dossiê 06/04; amostra pública em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong> ainda dominada por <strong class=\"font-semibold text-slate-900\">2022</strong> — X <strong class=\"font-semibold text-slate-900\">não</strong> é canal principal.</p>"
    "</div></div></div></div>"
)

X_ADEMARA = (
    "<div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm ring-1 ring-slate-100/80 hover:border-slate-300 hover:shadow transition-shadow'>"
    "<div class='flex gap-2 min-w-0'><div class='w-0.5 shrink-0 rounded-full bg-slate-900' aria-hidden='true'></div>"
    "<div class='min-w-0 flex-1'><p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p>"
    "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@ademaravilha</p>"
    "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
    "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
    "<span class='font-semibold tabular-nums text-slate-900'>196,9K</span></span></div>"
    "<div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'>"
    "<span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-amber-50 text-amber-900 ring-1 ring-amber-200/80' "
    "title='Poucos posts vs IG/TikTok; última amostra com 2024 visível'>pouca atividade</span>"
    "<p class='text-[9px] text-slate-500 leading-snug break-words'>Handle homologado no squad 06/04; seguidores na página pública em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>.</p>"
    "</div></div></div></div>"
)


def rep(old: str, new: str, label: str) -> None:
    global t
    c = t.count(old)
    if c != 1:
        raise SystemExit(f"{label}: esperado 1 ocorrência, tem {c}")
    t = t.replace(old, new)


# Raquel Real — cartão X
rep(
    (
        "<p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p>"
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raquelrealofc</p>"
        "<p class='mt-1.5 text-[9px] text-slate-500'>Lista de redes em <a class=\"dossier-source-link\" href=\"https://www.fashionbubbles.com/influencers/quem-e-raquel-real/\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Fashion Bubbles</strong></a>.</p>"
    ),
    (
        "<p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>X</p>"
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raquelrealofc</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>105,9K</span></span></div>"
        "<div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'>"
        "<span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' "
        "title='Posts próprios em 2025–2026 na página pública'>posts recentes</span>"
        "<p class='text-[9px] text-slate-500 leading-snug break-words'>Handle na lista de <a class=\"dossier-source-link\" href=\"https://www.fashionbubbles.com/influencers/quem-e-raquel-real/\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Fashion Bubbles</strong></a>; "
        "<strong class=\"font-semibold text-slate-900\">seguidores</strong> na página pública do X em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>.</p>"
        "</div>"
    ),
    "raquel_x",
)

# Tier 1 / Catraca — cartões + tabela 01/04
rep(
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@giovannapitel</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>70,2K</span></span></div>"
    ),
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@giovannapitel</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>69,8K</span></span></div>"
    ),
    "giovanna_card",
)
rep(
    ">giovannapitel</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>70,2K</td>",
    ">giovannapitel</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>69,8K</td>",
    "giovanna_tab",
)
rep(
    (
        "<span class='font-semibold tabular-nums text-slate-900'>534</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-slate-100 text-slate-700 ring-1 ring-slate-200' title='Sem posts recentes na checagem'>sem posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Desenvolvimento pessoal e hábitos</p>"
    ),
    (
        "<span class='font-semibold tabular-nums text-slate-900'>546</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-slate-100 text-slate-700 ring-1 ring-slate-200' title='Sem posts recentes na checagem'>sem posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Desenvolvimento pessoal e hábitos</p>"
    ),
    "rafael_card",
)
rep(
    ">RafaGratta</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>534</td>",
    ">RafaGratta</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>546</td>",
    "rafael_tab",
)
rep(
    (
        "<span class='font-semibold tabular-nums text-slate-900'>187</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-slate-100 text-slate-700 ring-1 ring-slate-200' title='Sem posts recentes na checagem'>sem posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Retorno esporádico ao X</p>"
    ),
    (
        "<span class='font-semibold tabular-nums text-slate-900'>186</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-slate-100 text-slate-700 ring-1 ring-slate-200' title='Sem posts recentes na checagem'>sem posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Retorno esporádico ao X</p>"
    ),
    "indio_card",
)
rep(
    ">indiobehn</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>187</td>",
    ">indiobehn</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>186</td>",
    "indio_tab",
)
rep(
    (
        "<span class='font-semibold tabular-nums text-slate-900'>11,8K</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' title='Havia posts recentes na checagem'>posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Cotidiano, humor, esporte</p>"
    ),
    (
        "<span class='font-semibold tabular-nums text-slate-900'>11,7K</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' title='Havia posts recentes na checagem'>posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Cotidiano, humor, esporte</p>"
    ),
    "cristian_card",
)
rep(
    ">cristianwariu</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>11,8K</td>",
    ">cristianwariu</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>11,7K</td>",
    "cristian_tab",
)
rep(
    (
        "<span class='font-semibold tabular-nums text-slate-900'>1,5M</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' title='Havia posts recentes na checagem'>posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Conteúdo patrocinado e cultura</p>"
    ),
    (
        "<span class='font-semibold tabular-nums text-slate-900'>1,5 mi</span></span></div><div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'><span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80' title='Conta institucional; página pública em 11/05/2026 com 1,5 mi seg. e centenas de milhares de posts'>posts recentes</span><p class='text-[9px] text-slate-500 leading-snug break-words'>Conteúdo patrocinado e cultura</p>"
    ),
    "catraca_card",
)
rep(
    ">CatracaLivre</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>1,5M</td>",
    ">CatracaLivre</td><td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>1,5 mi</td>",
    "catraca_tab",
)

# Lorena — grid 3 colunas + X
rep(
    "<section id='lorena-rufino' class='card-audit scroll-mt-20'>"
    "<div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'>"
    "<h2 class='text-xl font-black text-calia-navy'>3. Lorena Rufino</h2>"
    "<span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'>"
    "<span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span>"
    "<span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/90 border border-emerald-100 shadow-sm'>Baixo</span></span></div>"
    "<div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 gap-2'>",
    "<section id='lorena-rufino' class='card-audit scroll-mt-20'>"
    "<div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'>"
    "<h2 class='text-xl font-black text-calia-navy'>3. Lorena Rufino</h2>"
    "<span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'>"
    "<span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span>"
    "<span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/90 border border-emerald-100 shadow-sm'>Baixo</span></span></div>"
    "<div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 md:grid-cols-3 gap-2'>",
    "lorena_grid",
)
rep(
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@lorerufis</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>3,5M</span></span>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>1,14%</span></span></div></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor e vida pessoal"
    ),
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@lorerufis</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>3,5M</span></span>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>1,14%</span></span></div></div></div></div>"
        + X_LORENA
        + "</div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor e vida pessoal"
    ),
    "lorena_x_insert",
)

# Raphael — grid + X
rep(
    "<h2 class='text-xl font-black text-calia-navy'>5. Raphael Vicente</h2>"
    "<span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'>"
    "<span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span>"
    "<span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Baixo a moderado — exposição em segurança pública / comunidade (mídia)</span></span></div>"
    "<div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 gap-2'>",
    "<h2 class='text-xl font-black text-calia-navy'>5. Raphael Vicente</h2>"
    "<span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'>"
    "<span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>Síntese de risco</span>"
    "<span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 shadow-sm'>Baixo a moderado — exposição em segurança pública / comunidade (mídia)</span></span></div>"
    "<div class='mb-4'><p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles e números (referência nas tabelas ao fundo)</p><div class='grid grid-cols-2 md:grid-cols-3 gap-2'>",
    "raphael_grid",
)
rep(
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raphaelviicente</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>3,3M</span></span>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>1,08%</span></span></div></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor em vídeo"
    ),
    (
        "<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@raphaelviicente</p>"
        "<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Seg.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>3,3M</span></span>"
        "<span class='inline-flex items-baseline gap-0.5'><span class='text-[9px] font-medium uppercase text-slate-400'>Eng.</span>"
        "<span class='font-semibold tabular-nums text-slate-900'>1,08%</span></span></div></div></div></div>"
        + X_RAPHAEL
        + "</div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor em vídeo"
    ),
    "raphael_x_insert",
)

# Ademara — X após YouTube (antes de fechar mb-4)
rep(
    (
        "<span class='text-slate-400'>Canal · </span>Ademara (@ademara0)</p></div></div></div></div></div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor; série"
    ),
    (
        "<span class='text-slate-400'>Canal · </span>Ademara (@ademara0)</p></div></div></div></div>"
        + X_ADEMARA
        + "</div><p class='text-sm text-slate-600 mb-6 leading-relaxed'>Humor; série"
    ),
    "ademara_x_insert",
)

# Métricas lote 3 — parágrafo X (Raquel seguidores; Social Blade sem Twitter)
old_mx = (
    "<strong class=\"font-semibold text-slate-900\">Métricas de seguidores no X:</strong> não fechadas nesta coleta — ver quadro de risco no perfil.</p>"
)
new_mx = (
    "<strong class=\"font-semibold text-slate-900\">Seguidores no X (@raquelrealofc):</strong> "
    "<strong class=\"font-semibold text-slate-900\">105,9K</strong> na página pública em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong> "
    "(cartão no perfil). O <a class=\"dossier-source-link\" href=\"https://socialblade.com\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Social Blade</strong></a> "
    "<strong class=\"font-semibold text-slate-900\">descontinuou</strong> estatísticas de Twitter/X; a coleta de seguidores no X foi feita pela <strong class=\"font-semibold text-slate-900\">página pública</strong> do perfil.</p>"
)
rep(old_mx, new_mx, "metricas_lote3_raquel")

old_mpm = (
    "<strong class=\"font-semibold text-slate-900\">Morgana Camila</strong> e <strong class=\"font-semibold text-slate-900\">Paulo Victor Freitas:</strong> atividade oficial <strong class=\"font-semibold text-slate-900\">baixa</strong> no X na amostra; achados integrados nos respectivos perfis (complemento qualitativo, <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>). <strong class=\"font-semibold text-slate-900\">Métricas numéricas no X:</strong> <strong class=\"font-semibold text-slate-900\">sem</strong> fechamento manual nesta coleta.</p>"
)
new_mpm = (
    "<strong class=\"font-semibold text-slate-900\">Morgana Camila:</strong> o handle público <strong class=\"font-semibold text-slate-900\">@morganacamila</strong> no X mostra escala de seguidores <strong class=\"font-semibold text-slate-900\">incompatível</strong> com o Instagram homologado — <strong class=\"font-semibold text-slate-900\">não</strong> usar como painel da creator. "
    "<strong class=\"font-semibold text-slate-900\">Paulo Victor Freitas:</strong> tentativas <strong class=\"font-semibold text-slate-900\">@seufreitaz</strong> / <strong class=\"font-semibold text-slate-900\">@pvfreitazzz</strong> na página pública retornaram <strong class=\"font-semibold text-slate-900\">conta inexistente</strong> ou indisponível em <strong class=\"font-semibold text-slate-900\">11/05/2026</strong> — <strong class=\"font-semibold text-slate-900\">sem</strong> perfil X homologado nesta coleta; ver IG/TikTok/YouTube e <a class=\"dossier-source-link\" href=\"https://www.nessmgt.com/casting/seu-freitaz\" target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Ness</strong></a>.</p>"
)
rep(old_mpm, new_mpm, "metricas_lote3_morgana_paulo")

P.write_text(t, encoding="utf-8")
print("OK", P)
