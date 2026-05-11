#!/usr/bin/env python3
"""Correções pós-auditoria: notas de métricas lote 3, método, 18+ Morgana, microcopy, aspas, script de merge."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"


def main() -> None:
    t0 = HTML.read_text(encoding="utf-8")
    t = t0

    # --- Métricas: notas recuperadas (lote 3) + engajamento anómalo + cobertura X ---
    ig_anchor = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>"
        "Fonte: Social Blade (Instagram), salvo indicação no perfil.</p></section>"
        "<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>TikTok</h3>"
    )
    ig_insert = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>"
        "Fonte: Social Blade (Instagram), salvo indicação no perfil.</p>"
        "<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Cruzamento de escala (Coleta 11/05/2026 — lote 3):</strong> "
        "<strong class=\"font-semibold text-slate-900\">Raquel</strong> — ordem de grandeza em "
        "<a class=\"dossier-source-link\" href=\"https://www.famousbirthdays.com/people/raquel-real.html\" "
        "target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">Famous Birthdays</strong></a> "
        "(acesso <strong class=\"font-semibold text-slate-900\">12/05/2026</strong>). "
        "<strong class=\"font-semibold text-slate-900\">Morgana</strong> — menção a \"mais de 270 mil\" seguidores no "
        "<a class=\"dossier-source-link\" href=\"https://www.r7.com/entretenoinsta/influenciadora-que-narra-desfiles-civicos-diz-ter-sofrido-bullying-por-voz-hoje-e-ela-quem-me-sustenta-24102023/\" "
        "target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">R7</strong></a> "
        "(<strong class=\"font-semibold text-slate-900\">out/2023</strong>). "
        "<strong class=\"font-semibold text-slate-900\">Paulo</strong> — página de casting "
        "<a class=\"dossier-source-link\" href=\"https://www.nessmgt.com/casting/seu-freitaz\" target=\"_blank\" rel=\"noopener noreferrer\">"
        "<strong class=\"font-semibold text-slate-900\">Ness</strong></a> (acesso <strong class=\"font-semibold text-slate-900\">12/05/2026</strong>); "
        "<a class=\"dossier-source-link\" href=\"https://g1.globo.com/rn/rio-grande-do-norte/noticia/2025/10/08/nao-existe-o-brasil-sem-o-nordeste-influenciador-potiguar-viraliza-ao-valorizar-a-cultura-nordestina-e-quebrar-estereotipos.ghtml\" "
        "target=\"_blank\" rel=\"noopener noreferrer\"><strong class=\"font-semibold text-slate-900\">g1</strong></a> "
        "cita ~500 mil em <strong class=\"font-semibold text-slate-900\">uma</strong> rede em "
        "<strong class=\"font-semibold text-slate-900\">08/10/2025</strong>.</p>"
        "<p class='text-xs text-slate-500 mt-2 leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Percentagens de engajamento muito altas ou acima de 100% (ex.: Instagram):</strong> "
        "refletem a fórmula do painel na data da coleta, não erro de digitação deste dossiê.</p></section>"
        "<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>TikTok</h3>"
    )
    if "Cruzamento de escala (Coleta 11/05/2026" not in t:
        if ig_anchor not in t:
            raise SystemExit("âncora Instagram→TikTok não encontrada")
        t = t.replace(ig_anchor, ig_insert)

    tt_anchor = (
        "Traço (—): métrica indisponível naquela coleta ou coluna não aplicável ao formato do painel.</p></section>"
        "<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>YouTube</h3>"
    )
    tt_insert = (
        "Traço (—): métrica indisponível naquela coleta ou coluna não aplicável ao formato do painel.</p>"
        "<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Médias por vídeo (Upfluence, Raquel e Morgana, 11/05/2026):</strong> "
        "Raquel — com. méd. <strong class=\"font-semibold text-slate-900\">76,7</strong>, curt. méd. "
        "<strong class=\"font-semibold text-slate-900\">20,1K</strong>, part. méd. <strong class=\"font-semibold text-slate-900\">707</strong>, "
        "reprod. méd. <strong class=\"font-semibold text-slate-900\">137,0K</strong>, seguindo <strong class=\"font-semibold text-slate-900\">310</strong>. "
        "Morgana — com. méd. <strong class=\"font-semibold text-slate-900\">31,8</strong>, curt. méd. "
        "<strong class=\"font-semibold text-slate-900\">1,0K</strong>, part. méd. <strong class=\"font-semibold text-slate-900\">134,8</strong>, "
        "reprod. méd. <strong class=\"font-semibold text-slate-900\">90,4K</strong>, seguindo <strong class=\"font-semibold text-slate-900\">4</strong>. "
        "<strong class=\"font-semibold text-slate-900\">Paulo:</strong> cabeçalho público indica <strong class=\"font-semibold text-slate-900\">154</strong> "
        "contas seguidas (além de seguidores e curtidas totais na linha da tabela). Percentagens de audiência e engajamento do Paulo "
        "<strong class=\"font-semibold text-slate-900\">não</strong> fecharam nesta coleta (Upfluence devolveu "
        "<strong class=\"font-semibold text-slate-900\">not found</strong> para <strong class=\"font-semibold text-slate-900\">@seufreitaz</strong>).</p>"
        "</section><section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>YouTube</h3>"
    )
    if "Médias por vídeo (Upfluence, Raquel e Morgana" not in t:
        if tt_anchor not in t:
            raise SystemExit("âncora TikTok→YouTube não encontrada")
        t = t.replace(tt_anchor, tt_insert)

    yt_anchor = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: Social Blade (YouTube) quando o canal está na base; "
        "traço (—) quando a ficha não trouxe o campo.</p></section><section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>X</h3>"
    )
    yt_insert = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: Social Blade (YouTube) quando o canal está na base; "
        "traço (—) quando a ficha não trouxe o campo.</p>"
        "<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Views totais na ficha Social Blade (11/05/2026):</strong> "
        "<strong class=\"font-semibold text-slate-900\">Raquel Real</strong> "
        "<strong class=\"font-semibold text-slate-900\">500.657</strong>; "
        "<strong class=\"font-semibold text-slate-900\">Paulo Victor Freitas</strong> "
        "<strong class=\"font-semibold text-slate-900\">12.550.362</strong> "
        "(além dos inscritos na coluna). <strong class=\"font-semibold text-slate-900\">Morgana:</strong> "
        "<a class=\"dossier-source-link\" href=\"https://www.youtube.com/@morganacamila\" target=\"_blank\" rel=\"noopener noreferrer\">"
        "<strong class=\"font-semibold text-slate-900\">youtube.com/@morganacamila</strong></a> sem escala útil na mesma coleta — alinhado à nota no perfil.</p>"
        "</section><section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>X</h3>"
    )
    if "12.550.362" not in t:
        if yt_anchor not in t:
            raise SystemExit("âncora YouTube→X não encontrada")
        t = t.replace(yt_anchor, yt_insert)

    x_anchor = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: checagem direta no X na data da coleta (tabela); "
        "complemento qualitativo do lote 3 abaixo.</p></section><p class='text-sm text-slate-600 leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Raquel Real"
    )
    x_insert = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: checagem direta no X na data da coleta (tabela); "
        "complemento qualitativo do lote 3 abaixo.</p>"
        "<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>"
        "<strong class=\"font-semibold text-slate-900\">Cobertura tabular do X:</strong> as sete linhas são da checagem "
        "<strong class=\"font-semibold text-slate-900\">01/04/2026</strong> (squad desse pedido). Demais pedidos e o "
        "<strong class=\"font-semibold text-slate-900\">lote 3</strong> no X estão nos <strong class=\"font-semibold text-slate-900\">perfis</strong> "
        "e nos parágrafos seguintes (sem linha tabular homologada para Morgana/Paulo na mesma coleta).</p></section>"
        "<p class='text-sm text-slate-600 leading-relaxed'><strong class=\"font-semibold text-slate-900\">Raquel Real"
    )
    if "Cobertura tabular do X" not in t:
        if x_anchor not in t:
            raise SystemExit("âncora X→prose Raquel não encontrada")
        t = t.replace(x_anchor, x_insert)

    # --- Método (Redes sociais + Painéis) ---
    t = t.replace(
        "datas de coleta por bloco em Métricas",
        "a coluna <strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> em cada tabela da secção Métricas nas redes",
    )
    old_pain = (
        "No bloco <strong class=\"font-semibold text-slate-900\">«lote 3»</strong> em Métricas, Instagram e YouTube (exceto Morgana no YT) foram fechados com"
    )
    new_pain = (
        "As linhas com <strong class=\"font-semibold text-slate-900\">Coleta (ref.) 11/05/2026</strong> (lote 3) em cada tabela: Instagram e YouTube "
        "(exceto Morgana no YT) foram fechados com"
    )
    t = t.replace(old_pain, new_pain)
    t = t.replace(
        "No mesmo bloco, o TikTok foi fechado com",
        "O TikTok desse mesmo recorte foi fechado com",
    )
    t = t.replace("«Free TikTok Profile Audit»", "\"Free TikTok Profile Audit\"")

    # --- Leitura Caixa / Morgana ---
    t = t.replace(
        "<strong class=\"font-semibold text-slate-900\">Morgana</strong> (<strong class=\"font-semibold text-slate-900\">indício</strong> em material público com <strong class=\"font-semibold text-slate-900\">menores em cena</strong> no desfile escolar; confirmar demos) e o eixo",
        "<strong class=\"font-semibold text-slate-900\">Morgana</strong> (<strong class=\"font-semibold text-slate-900\">pista no eixo Loterias 18+</strong>: menores aparecem no <strong class=\"font-semibold text-slate-900\">material público</strong> do desfile escolar — não substitui dados de audiência, mas pede cruzar com <strong class=\"font-semibold text-slate-900\">indícios de público infantil</strong> e demos, se existirem) e o eixo",
    )

    t = t.replace(
        "Moderado no 18+ — indício: menores em cena no material público (desfile); confirmar demos",
        "Moderado no 18+ — pista: menores em cena no desfile público (cruzar com audiência; confirmar demos)",
    )
    t = t.replace(
        "Moderado no 18+ — menores em cena (desfile); demos",
        "Moderado no 18+ — pista: menores em desfile público; demos/audiência",
    )

    # --- Microcopy perfis ---
    t = t.replace(
        "Redes · handles e números (referência nas tabelas ao fundo)",
        "Redes · handles e números (ver Métricas nas redes)",
    )
    t = t.replace(
        "Redes · snapshot dos painéis",
        "Redes · snapshot local (totais por rede em Métricas nas redes)",
    )

    # --- Aspas francesas → aspas rectas (conteúdo visível) ---
    t = t.replace("\u00ab", '"').replace("\u00bb", '"')

    if t != t0:
        HTML.write_text(t, encoding="utf-8")
    print("OK:", HTML)


if __name__ == "__main__":
    main()
