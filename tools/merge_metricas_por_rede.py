#!/usr/bin/env python3
"""Consolida a secção #metricas: uma tabela por rede (Instagram, TikTok, YouTube, X).

Preserva linhas de cada coleta e acrescenta coluna «Coleta (ref.)».
O bloco de texto do X (lote 3) mantém-se após a tabela unificada do X.
"""
from __future__ import annotations

import re
from pathlib import Path

HTML_PATH = Path(__file__).resolve().parents[1] / "caixa" / "20260511-dossie-squad-always-on-loterias-2026.html"

TD = "py-2 px-3 border-b border-slate-100 text-sm align-top"
TH = "py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200"

INTRO_OLD = (
    "<p class='text-sm text-slate-600 mb-6 leading-relaxed break-words'>Tabelas por <strong class=\"font-semibold text-slate-900\">data de referência</strong> da entrega de origem; o bloco final é o <strong class=\"font-semibold text-slate-900\">lote 3</strong> (coleta <strong class=\"font-semibold text-slate-900\">11/05/2026</strong>). Confrontar de novo os números próximo à veiculação.</p>"
)

INTRO_NEW = (
    "<p class='text-sm text-slate-600 mb-6 leading-relaxed break-words'>"
    "Uma <strong class=\"font-semibold text-slate-900\">tabela por rede</strong>, reunindo todas as coletas. "
    "A coluna <strong class=\"font-semibold text-slate-900\">Coleta (ref.)</strong> indica a data da captura "
    "na ferramenta ou na página pública. Confrontar de novo os números próximo à veiculação.</p>"
)


def find_balanced_section(html: str, open_pos: int) -> int:
    """open_pos no '<' do <section...> inicial; devolve índice após </section> de fecho."""
    depth = 0
    i = open_pos
    n = len(html)
    while i < n:
        if html.startswith("<section", i):
            depth += 1
            i = html.find(">", i) + 1
            continue
        if html.startswith("</section>", i):
            depth -= 1
            i += len("</section>")
            if depth == 0:
                return i
            continue
        i += 1
    raise ValueError("section não fechada")


def extract_ref_blocks(metricas_from_first_ref: str) -> list[tuple[str, str]]:
    """Lista de (rótulo_referência, html_interno_do_bloco arredondado)."""
    token = "<section class='mb-10 rounded-lg border border-slate-200 bg-slate-50/40 p-4'>"
    out: list[tuple[str, str]] = []
    pos = 0
    while True:
        a = metricas_from_first_ref.find(token, pos)
        if a == -1:
            break
        open_tag_end = metricas_from_first_ref.find(">", a) + 1
        close_outer = find_balanced_section(metricas_from_first_ref, a)
        inner_end = close_outer - len("</section>")
        block = metricas_from_first_ref[open_tag_end:inner_end]
        m = re.search(
            r"<h3 class='text-lg font-black text-calia-navy mb-3'>([^<]+)</h3>",
            block,
        )
        label = m.group(1).strip() if m else "Referência"
        out.append((label, block))
        pos = close_outer
    return out


def tbody_after_h3(block: str, network: str) -> str | None:
    h3 = f"<h3 class='text-lg font-black text-calia-navy mb-2'>{network}</h3>"
    i = block.find(h3)
    if i == -1:
        return None
    j = block.find("<tbody", i)
    if j == -1:
        return None
    gt = block.find(">", j) + 1
    k = block.find("</tbody>", j)
    if k == -1:
        return None
    return block[gt:k].strip()


def count_tds(tr: str) -> int:
    return len(re.findall(r"<td\b", tr))


def split_trs(tbody_inner: str) -> list[str]:
    return re.findall(r"<tr\b.*?</tr>", tbody_inner, flags=re.DOTALL)


def append_cells_before_tr_close(tr: str, cells_html: str) -> str:
    tr = tr.rstrip()
    if not tr.endswith("</tr>"):
        raise ValueError("esperado </tr> no fim da linha")
    return tr[:-5] + cells_html + "</tr>"


def normalize_instagram_tr(tr: str, ref: str) -> str:
    ref_cell = f"<td class='{TD}'><span class='text-xs text-slate-600'>{ref}</span></td>"
    n = count_tds(tr)
    if n == 8:
        return append_cells_before_tr_close(tr, ref_cell)
    if n == 7:
        parts = list(re.finditer(r"<td\b.*?</td>", tr, flags=re.DOTALL))
        if len(parts) < 3:
            return append_cells_before_tr_close(tr, ref_cell)
        after_seg = parts[2].end()
        dash = f"<td class='{TD}'>—</td>"
        tr = tr[:after_seg] + dash + tr[after_seg:]
        return append_cells_before_tr_close(tr, ref_cell)
    return append_cells_before_tr_close(tr, ref_cell)


def normalize_instagram_block(tbody_inner: str, ref: str) -> str:
    trs = split_trs(tbody_inner)
    return "\n".join(normalize_instagram_tr(tr, ref) for tr in trs)


def normalize_tiktok_tr(tr: str, ref: str) -> str:
    ref_cell = f"<td class='{TD}'><span class='text-xs text-slate-600'>{ref}</span></td>"
    nota_dash = f"<td class='{TD}'>—</td>"
    n = count_tds(tr)
    if n == 12:
        return append_cells_before_tr_close(tr, nota_dash + ref_cell)
    if n == 8:
        cells = re.findall(r"<td\b.*?</td>", tr, flags=re.DOTALL)
        if len(cells) != 8:
            return append_cells_before_tr_close(tr, nota_dash + ref_cell)
        c0, c1, c2, c3, c4, c5, c6, c7 = cells
        dash = f"<td class='{TD}'>—</td>"
        m_split = re.search(r"([\d.,]+%)\s*/\s*([\d.,]+%)", c5)
        if m_split:
            f_mul = f"<td class='{TD}'>{m_split.group(1)}</td>"
            f_hom = f"<td class='{TD}'>{m_split.group(2)}</td>"
        else:
            f_mul = dash
            f_hom = dash
        # Ordem do cabeçalho Upfluence + notas: Nome, User, Engaj, Seg, Com, Curt, Comp, Repr, Total, Vídeos, %m, %h, Notas, Ref
        # Lote3: c2 seg, c3 eng — trocar para Engaj, Seg
        row = (
            f"<tr>{c0}{c1}{c3}{c2}{dash}{dash}{dash}{dash}{c4}{c6}"
            f"{f_mul}{f_hom}{c7}{ref_cell}</tr>"
        )
        return row
    return append_cells_before_tr_close(tr, nota_dash + ref_cell)


def normalize_tiktok_block(tbody_inner: str, ref: str) -> str:
    trs = split_trs(tbody_inner)
    return "\n".join(normalize_tiktok_tr(tr, ref) for tr in trs)


def normalize_youtube_tr(tr: str, ref: str) -> str:
    ref_cell = f"<td class='{TD}'><span class='text-xs text-slate-600'>{ref}</span></td>"
    dash = f"<td class='{TD}'>—</td>"
    n = count_tds(tr)
    if n == 5:
        return append_cells_before_tr_close(tr, ref_cell)
    if n == 3:
        cells = re.findall(r"<td\b.*?</td>", tr, flags=re.DOTALL)
        if len(cells) != 3:
            return append_cells_before_tr_close(tr, ref_cell)
        return f"<tr>{cells[0]}{cells[1]}{cells[2]}{dash}{dash}{ref_cell}</tr>"
    return append_cells_before_tr_close(tr, ref_cell)


def normalize_youtube_block(tbody_inner: str, ref: str) -> str:
    trs = split_trs(tbody_inner)
    return "\n".join(normalize_youtube_tr(tr, ref) for tr in trs)


def prose_after_h3(block: str, network: str) -> str | None:
    h3 = f"<h3 class='text-lg font-black text-calia-navy mb-2'>{network}</h3>"
    i = block.find(h3)
    if i == -1:
        return None
    rest = block[i + len(h3) :]
    if rest.lstrip().startswith("<p"):
        end = rest.find("</section>")
        return rest[:end] if end != -1 else rest
    return None


def build_new_metricas(html: str) -> str:
    m_start = html.find('<section id="metricas"')
    if m_start == -1:
        raise SystemExit("metricas não encontrada")
    m_end = html.find('<section id="como"', m_start)
    if m_end == -1:
        raise SystemExit("como não encontrada")
    old = html[m_start:m_end]

    inner_start = old.find("</div>", old.find("section-header")) + len("</div>")
    intro_end = old.find("<section class='mb-10 rounded-lg", inner_start)
    if intro_end == -1:
        raise SystemExit("estrutura metricas inesperada")
    header_and_intro = old[:intro_end]
    if INTRO_OLD not in header_and_intro:
        raise SystemExit("texto intro antigo não encontrado (HTML mudou?)")
    header_and_intro = header_and_intro.replace(INTRO_OLD, INTRO_NEW)

    ref_blocks = extract_ref_blocks(old[intro_end:])

    ref_short = {
        "Referência 01/04/2026": "01/04/2026",
        "Referência 06/04/2026": "06/04/2026",
        "Referência 04/05/2026": "04/05/2026",
        "Referência 11/05/2026 — lote 3": "11/05/2026",
    }

    ig_rows: list[str] = []
    tt_rows: list[str] = []
    yt_rows: list[str] = []
    x_rows: list[str] = []
    x_prose_lote3 = ""

    for label, block in ref_blocks:
        ref = ref_short.get(label, label.replace("Referência ", "").strip())

        tb = tbody_after_h3(block, "Instagram")
        if tb:
            ig_rows.append(normalize_instagram_block(tb, ref))

        tb = tbody_after_h3(block, "TikTok")
        if tb:
            tt_rows.append(normalize_tiktok_block(tb, ref))

        tb = tbody_after_h3(block, "YouTube")
        if tb:
            yt_rows.append(normalize_youtube_block(tb, ref))

        tb = tbody_after_h3(block, "X")
        if tb:
            for tr in split_trs(tb):
                x_rows.append(
                    append_cells_before_tr_close(
                        tr,
                        f"<td class='{TD}'><span class='text-xs text-slate-600'>{ref}</span></td>",
                    )
                )
        else:
            prose = prose_after_h3(block, "X")
            if prose and "lote 3" in label.lower():
                x_prose_lote3 = prose

    ref_th = f"<th class='{TH}'>Coleta (ref.)</th>"

    ig_thead = (
        f"<thead class='bg-slate-50'><tr>"
        f"<th class='{TH}'>Nome / camada</th>"
        f"<th class='{TH}'>Usuário</th>"
        f"<th class='{TH}'>Seguidores</th>"
        f"<th class='{TH}'>Variação 14 dias (%)</th>"
        f"<th class='{TH}'>Posts</th>"
        f"<th class='{TH}'>Curtidas méd.</th>"
        f"<th class='{TH}'>Coment. méd.</th>"
        f"<th class='{TH}'>Engaj.</th>"
        f"{ref_th}</tr></thead>"
    )

    tt_thead = (
        f"<thead class='bg-slate-50'><tr>"
        f"<th class='{TH}'>Nome / camada</th>"
        f"<th class='{TH}'>Usuário</th>"
        f"<th class='{TH}'>Engaj.</th>"
        f"<th class='{TH}'>Seguidores</th>"
        f"<th class='{TH}'>Com. méd.</th>"
        f"<th class='{TH}'>Curt. méd.</th>"
        f"<th class='{TH}'>Comp. méd.</th>"
        f"<th class='{TH}'>Repr. méd.</th>"
        f"<th class='{TH}'>Total curtidas</th>"
        f"<th class='{TH}'>Vídeos</th>"
        f"<th class='{TH}'>% mulheres</th>"
        f"<th class='{TH}'>% homens</th>"
        f"<th class='{TH}'>Notas / fonte painel</th>"
        f"{ref_th}</tr></thead>"
    )

    yt_thead = (
        f"<thead class='bg-slate-50'><tr>"
        f"<th class='{TH}'>Nome / camada</th>"
        f"<th class='{TH}'>Usuário</th>"
        f"<th class='{TH}'>Inscritos</th>"
        f"<th class='{TH}'>Visualizações</th>"
        f"<th class='{TH}'>Vídeos</th>"
        f"{ref_th}</tr></thead>"
    )

    xt_thead = (
        f"<thead class='bg-slate-50'><tr>"
        f"<th class='{TH}'>Nome / camada</th>"
        f"<th class='{TH}'>Usuário</th>"
        f"<th class='{TH}'>Seguidores</th>"
        f"<th class='{TH}'>Posts recentes (checagem)</th>"
        f"<th class='{TH}'>Teor recente (resumo)</th>"
        f"{ref_th}</tr></thead>"
    )

    def table_block(title: str, thead: str, tbody: str, foot: str) -> str:
        return (
            f"<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>{title}</h3>"
            f"<div class='overflow-x-auto rounded border border-slate-200'>"
            f"<table class='min-w-full'>{thead}<tbody>{tbody}</tbody></table></div>"
            f"{foot}</section>"
        )

    ig_foot = "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: Social Blade (Instagram), salvo indicação no perfil.</p>"
    tt_foot = (
        "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: Upfluence (TikTok) ou cabeçalho público quando indicado na coluna de notas.</p>"
        "<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>Traço (—): métrica indisponível naquela coleta ou coluna não aplicável ao formato do painel.</p>"
    )
    yt_foot = "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: Social Blade (YouTube) quando o canal está na base; traço (—) quando a ficha não trouxe o campo.</p>"
    xt_foot = "<p class='text-xs text-slate-500 mt-3 leading-relaxed break-words'>Fonte: checagem direta no X na data da coleta (tabela); complemento qualitativo do lote 3 abaixo.</p>"

    x_section = table_block("X", xt_thead, "\n".join(x_rows), xt_foot)
    if x_prose_lote3:
        x_section += x_prose_lote3

    new_inner = (
        header_and_intro
        + table_block("Instagram", ig_thead, "\n".join(ig_rows), ig_foot)
        + table_block("TikTok", tt_thead, "\n".join(tt_rows), tt_foot)
        + table_block("YouTube", yt_thead, "\n".join(yt_rows), yt_foot)
        + x_section
        + "\n    </section>\n\n    "
    )

    sec_end = find_balanced_section(html, m_start)
    return html[:m_start] + new_inner + html[sec_end:]


def main() -> None:
    t = HTML_PATH.read_text(encoding="utf-8")
    new_t = build_new_metricas(t)
    if new_t == t:
        raise SystemExit("nenhuma alteração")
    HTML_PATH.write_text(new_t, encoding="utf-8")
    print("OK:", HTML_PATH)


if __name__ == "__main__":
    main()
