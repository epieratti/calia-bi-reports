#!/usr/bin/env python3
"""Revisão de consistência textual do dossiê HTML (squad Loterias 20260511). Idempotente."""

from __future__ import annotations

from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"


def main() -> None:
    t = HTML.read_text(encoding="utf-8")
    orig = t

    # Ortografia pt-BR corrente em materiais digitais do projeto
    t = t.replace("secção", "seção")
    t = t.replace("secções", "seções")

    # Cabeçalho: alinhar às quatro coletas e à revisão consolidada
    t = t.replace(
        '<p class="text-xs opacity-75 mt-4">Atualização: Maio/2026 · Referência dos números: 04/05/2026 · Documento: 05/05/2026</p>',
        '<p class="text-xs opacity-75 mt-4">Atualização: maio/2026 · Coletas de referência (métricas e checagens): 01/04, 06/04, 04/05 e 11/05/2026 · Revisão textual do dossiê: 11/05/2026.</p>',
    )

    # Sumário: remover linha em branco extra; alinhar rótulo ao pedido 1–27
    t = t.replace(
        "</a></li>\n        \n        <li><a class=\"toc-link\" href=\"#perfis\">Perfis (ordem cronológica)</a></li>",
        "</a></li>\n        <li><a class=\"toc-link\" href=\"#perfis\">Perfis (ordem do pedido, 1–27)</a></li>",
    )
    t = t.replace(
        "Mesma ordem da seção <a class='toc-link' href='#perfis'>Perfis</a>: 01/04, 06/04, 04/05 e 11/05 de 2026.",
        "Mesma ordem da seção <a class='toc-link' href='#perfis'>Perfis</a> (1 a 27), coerente com as quatro datas de referência de painel: 01/04, 06/04, 04/05 e 11/05/2026.",
    )

    # Perfis — ordem do pedido + ondas de coleta (coerente com métricas)
    old_perfis = (
        "<p class=\"text-sm text-slate-600 mt-2 leading-relaxed max-w-3xl\">Um único bloco em "
        "<strong class=\"font-semibold text-slate-900\">ordem cronológica das coletas</strong> "
        "(mais antiga primeiro): <strong class=\"font-semibold text-slate-900\">01/04/2026</strong> "
        "(13 nomes), <strong class=\"font-semibold text-slate-900\">06/04/2026</strong> (8), "
        "<strong class=\"font-semibold text-slate-900\">04/05/2026</strong> (3) e "
        "<strong class=\"font-semibold text-slate-900\">11/05/2026</strong> (3).</p>"
    )
    new_perfis = (
        "<p class=\"text-sm text-slate-600 mt-2 leading-relaxed max-w-3xl\">Um único bloco na "
        "<strong class=\"font-semibold text-slate-900\">ordem do pedido</strong> (1 a 27), "
        "alinhado à progressão das coletas de painel: <strong class=\"font-semibold text-slate-900\">01/04/2026</strong> "
        "(13 nomes), <strong class=\"font-semibold text-slate-900\">06/04/2026</strong> (8), "
        "<strong class=\"font-semibold text-slate-900\">04/05/2026</strong> (3) e "
        "<strong class=\"font-semibold text-slate-900\">11/05/2026</strong> (3).</p>"
    )
    if old_perfis in t:
        t = t.replace(old_perfis, new_perfis, 1)

    # Leitura rápida — Coleta (ref.) existe nas tabelas de Métricas, não na tabela resumo
    old_leitura = (
        "<p class='text-sm font-semibold text-slate-800 mb-5 leading-snug'>Dossiê do "
        "<strong class=\"font-semibold text-slate-900\">Squad Always ON Loterias 2026</strong> com "
        "<strong class=\"font-semibold text-slate-900\">27</strong> creators. A <a class='toc-link' href='#tabela'>tabela-resumo</a>, as seções "
        "<a class='toc-link' href='#perfis'><strong class=\"font-semibold text-slate-900\">Perfis</strong></a> e "
        "<a class='toc-link' href='#metricas'><strong class=\"font-semibold text-slate-900\">Métricas nas redes</strong></a> "
        "fecham os quatro eixos (Concorrência, Polêmicas, Política, Loterias 18+) com links. As datas na coluna "
        "<strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> mudam — valide de novo perto da veiculação.</p>"
    )
    new_leitura = (
        "<p class='text-sm font-semibold text-slate-800 mb-5 leading-snug'>Dossiê do "
        "<strong class=\"font-semibold text-slate-900\">Squad Always ON Loterias 2026</strong> com "
        "<strong class=\"font-semibold text-slate-900\">27</strong> creators. A "
        "<a class='toc-link' href='#tabela'><strong class=\"font-semibold text-slate-900\">Tabela resumo</strong></a> "
        "sintetiza, por linha, os quatro eixos (Concorrência, Polêmicas, Política, Loterias 18+). Os "
        "<a class='toc-link' href='#perfis'><strong class=\"font-semibold text-slate-900\">Perfis</strong></a> "
        "trazem o parecer completo, links e calibragem. Em "
        "<a class='toc-link' href='#metricas'><strong class=\"font-semibold text-slate-900\">Métricas nas redes</strong></a>, "
        "cada tabela de rede inclui a coluna <strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> "
        "com a data da ferramenta ou da página pública. Números e datas mudam — valide de novo perto da veiculação.</p>"
    )
    if old_leitura in t:
        t = t.replace(old_leitura, new_leitura, 1)

    # Pedido — remover afirmação de “data da linha” na tabela sem coluna de data
    old_pedido_tail = (
        "(quarto bloco analítico de cada perfil). A data de referência da linha vale para o recorte resumido de todos os eixos."
    )
    new_pedido_tail = (
        "(quarto bloco analítico de cada perfil). A tabela não tem coluna exclusiva de data por linha: "
        "quando uma data importa, ela entra no próprio texto sintético. Para data sistemática por rede, "
        "use a coluna <strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> em "
        "<a class='toc-link' href='#metricas'><strong class=\"font-semibold text-slate-900\">Métricas nas redes</strong></a> "
        "e os blocos numerados em cada perfil."
    )
    if old_pedido_tail in t:
        t = t.replace(old_pedido_tail, new_pedido_tail, 1)

    # Tabela resumo — nota de rodapé coerente com ausência de coluna Coleta
    old_tab_note = (
        "Na coluna \"Loterias 18+\", o texto é sintético; use a data da linha e abra o perfil para o parecer integral, "
        "links e capturas do eixo."
    )
    new_tab_note = (
        "Na coluna \"Loterias 18+\", o texto é sintético; quando houver data no trecho, ela qualifica aquela amostra. "
        "Abra o perfil para o parecer integral, links e capturas do eixo e para cruzar com a coluna "
        "<strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> em "
        "<a class='toc-link' href='#metricas'>Métricas nas redes</a>."
    )
    if old_tab_note in t:
        t = t.replace(old_tab_note, new_tab_note, 1)

    # Síntese — alinhar lista de nomes à mesma sequência explícita
    old_sint = (
        "Creators neste dossiê (27), na ordem do pedido: Giovanna Pitel"
    )
    new_sint = (
        "Creators neste dossiê (27), na ordem do pedido (1 a 27, mesma sequência do sumário e da Tabela resumo): Giovanna Pitel"
    )
    if old_sint in t:
        t = t.replace(old_sint, new_sint, 1)

    # Métricas — mesmo vocabulário de “veiculação” usado no restante do dossiê
    t = t.replace(
        "valide de novo na data da campanha",
        "valide de novo perto da veiculação",
    )

    # Glossário do pedido: alinhar “Não encontramos” no corpo da tabela
    t = t.replace("Não achamos", "Não encontramos")

    if t == orig:
        print("Nenhuma alteração aplicada (já revisado ou texto divergente).")
    else:
        HTML.write_text(t, encoding="utf-8")
        print("OK:", HTML)


if __name__ == "__main__":
    main()
