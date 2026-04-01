#!/usr/bin/env python3
"""
Gera dossiê HTML (Always ON Loterias 2026) a partir de data/dossier_loterias2026.yaml.
Saída: output/20260401-dossie-squad-always-on-loterias-2026.html
"""
from __future__ import annotations

import html
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = ROOT / "output"


def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


def mini_md(s: object) -> str:
    """**negrito** e __sublinhado__ em strings do YAML; restante escapado."""
    text = str(s or "")
    out: list[str] = []
    pos = 0
    for m in re.finditer(r"\*\*(.+?)\*\*|__(.+?)__", text):
        out.append(esc(text[pos : m.start()]))
        if m.group(1) is not None:
            out.append(
                '<strong class="font-semibold text-slate-900">'
                f"{esc(m.group(1))}</strong>"
            )
        else:
            out.append(
                '<span class="underline decoration-calia-gold/80 decoration-2 '
                'underline-offset-2">'
                f"{esc(m.group(2))}</span>"
            )
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def render_clevel_body(cfg: dict) -> str:
    """Subtítulo opcional, tagline, depois blocos em cards ou fallback bullets/parágrafos."""
    parts: list[str] = []
    if cfg.get("subtitle"):
        parts.append(
            f"<p class='text-xs text-slate-500 mb-3'>{mini_md(cfg['subtitle'])}</p>"
        )
    if cfg.get("tagline"):
        parts.append(
            f"<p class='text-sm font-semibold text-slate-800 mb-5 leading-snug'>"
            f"{mini_md(cfg['tagline'])}</p>"
        )
    blocks = cfg.get("blocks")
    if blocks:
        cards: list[str] = []
        for b in blocks:
            tit = mini_md(b.get("title", ""))
            items = b.get("items") or []
            lis = "".join(
                (
                    "<li class='flex gap-2.5 text-sm text-slate-700 leading-snug'>"
                    "<span class='text-calia-gold font-bold shrink-0 mt-0.5'>•</span>"
                    f"<span>{mini_md(it)}</span></li>"
                )
                for it in items
            )
            cards.append(
                "<div class='rounded-lg border border-slate-200 bg-white p-4 md:p-5 shadow-sm'>"
                "<p class='text-xs font-black uppercase tracking-wide text-calia-navy "
                "border-l-4 border-calia-gold pl-3 -ml-px mb-3'>"
                f"{tit}</p>"
                f"<ul class='list-none space-y-2.5 m-0 p-0'>{lis}</ul></div>"
            )
        parts.append(f"<div class='grid md:grid-cols-2 gap-4'>{''.join(cards)}</div>")
        return "".join(parts)
    bullets = cfg.get("bullets") or []
    if bullets:
        lis = "".join(
            (
                "<li class='flex gap-2.5 text-sm text-slate-700 leading-snug'>"
                "<span class='text-calia-gold font-bold shrink-0'>•</span>"
                f"<span>{mini_md(b)}</span></li>"
            )
            for b in bullets
        )
        parts.append(f"<ul class='list-none space-y-2 m-0 p-0'>{lis}</ul>")
        return "".join(parts)
    for para in cfg.get("paragraphs") or []:
        parts.append(
            f"<p class='text-sm text-slate-700 leading-relaxed mb-3'>{mini_md(para)}</p>"
        )
    return "".join(parts)


def slug_id(name: str) -> str:
    n = unicodedata.normalize("NFKD", name or "")
    n = "".join(c for c in n if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")
    return s or "perfil"


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def norm_handle(s: object) -> str:
    t = str(s or "").strip().lower()
    if t.startswith("@"):
        t = t[1:]
    return t


def panel_row_by_briefing(rows: list, brief_col: int, yaml_handle: object) -> list[str] | None:
    key = norm_handle(yaml_handle)
    if not key:
        return None
    for row in rows:
        if len(row) <= brief_col:
            continue
        if norm_handle(row[brief_col]) == key:
            return row
    return None


def ig_name_by_briefing(ig_rows: list, brief: object) -> str:
    k = norm_handle(brief)
    if not k:
        return ""
    for row in ig_rows:
        if len(row) > 1 and norm_handle(row[1]) == k:
            return str(row[0] or "").strip()
    return ""


def normalize_panel_for_display(key: str, panel: dict, ig_rows: list) -> tuple[list[str], list[list]]:
    """Tabelas de redes: só duas colunas de identificação — Nome e Usuário."""
    headers = list(panel.get("headers") or [])
    rows = [list(r) for r in (panel.get("rows") or [])]

    if key == "instagram":
        out_h = ["Usuário" if h == "@" else h for h in headers]
        return out_h, rows

    if key == "tiktok" and len(headers) >= 2:
        out_h = ["Nome", "Usuário"] + headers[2:]
        out_rows: list[list] = []
        for r in rows:
            if len(r) < 2:
                out_rows.append(r)
                continue
            brief = r[1]
            nome = ig_name_by_briefing(ig_rows, brief) or str(r[0] or "").strip()
            raw_tool = str(r[0] or "").strip()
            usuario = raw_tool if raw_tool and " " not in raw_tool else str(brief).strip()
            out_rows.append([nome, usuario] + r[2:])
        return out_h, out_rows

    if key == "youtube" and len(headers) >= 2:
        out_h = ["Nome", "Usuário"] + headers[2:]
        out_rows = []
        for r in rows:
            if len(r) < 2:
                out_rows.append(r)
                continue
            brief = r[1]
            nome = ig_name_by_briefing(ig_rows, brief) or str(r[0] or "").strip()
            usuario = str(brief).strip()
            out_rows.append([nome, usuario] + r[2:])
        return out_h, out_rows

    if key == "x" and rows and len(headers) >= 4:
        out_h = list(headers)
        ativo_label = "Postagens recentes (amostra)"
        try:
            ai = out_h.index("Ativo?")
        except ValueError:
            ai = 3
        if ai < len(out_h):
            out_h[ai] = ativo_label
        out_rows = []
        for r in rows:
            row = list(r)
            if len(row) > ai:
                txt, _ = humanize_x_ativo(row[ai])
                row[ai] = txt
            out_rows.append(row)
        return out_h, out_rows

    return headers, rows


def panel_row_x(rows: list, profile_name: str, yaml_x: object) -> list[str] | None:
    """Linha X: Nome, Usuário, Seguidores, Ativo?, Teor."""
    xk = norm_handle(yaml_x)
    pn = (profile_name or "").strip().lower()
    for row in rows:
        if len(row) < 5:
            continue
        if pn and str(row[0] or "").strip().lower() == pn:
            return row
        if xk and norm_handle(row[1]) == xk:
            return row
    return None


def humanize_x_ativo(cell: object) -> tuple[str, str]:
    """Retorna (texto legível, classe Tailwind do selo)."""
    raw = str(cell or "").strip()
    low = raw.lower()
    if low in ("sim", "s", "yes"):
        return (
            "Havia postagens recentes na amostra",
            "bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80",
        )
    if low in ("não", "nao"):
        return (
            "Sem postagens recentes na amostra",
            "bg-slate-100 text-slate-700 ring-1 ring-slate-200",
        )
    return (raw or "—", "bg-slate-50 text-slate-600 ring-1 ring-slate-200")


def x_ativo_compact(cell: object) -> str:
    """Frase curta para linha compacta de perfil."""
    raw = str(cell or "").strip()
    low = raw.lower()
    if low in ("sim", "s", "yes"):
        return "com posts na amostra"
    if low in ("não", "nao"):
        return "sem posts na amostra"
    return raw or "—"


def clip_txt(s: object, n: int = 42) -> str:
    t = str(s or "").strip()
    if len(t) <= n:
        return t
    return t[: n - 1] + "…"


def format_profile_networks_html(
    name: str,
    handles: dict,
    ig_rows: list,
    tt_rows: list,
    yt_rows: list,
    x_rows: list,
) -> str:
    """Handles e números só a partir das tabelas dos painéis; rede sem linha não aparece. Layout compacto."""
    segs: list[str] = []

    ig = panel_row_by_briefing(ig_rows, 1, handles.get("instagram"))
    if ig and len(ig) >= 10:
        u = esc(str(ig[1]).lstrip("@"))
        segs.append(
            "<span class='whitespace-nowrap'>"
            f"<span class='font-semibold text-slate-800'>IG</span> "
            f"<span class='font-mono text-slate-600'>@{u}</span> "
            f"<span class='text-slate-500'>·</span> {esc(ig[2])} seg "
            f"<span class='text-slate-500'>·</span> eng. {esc(ig[9])}"
            "</span>"
        )

    tt = panel_row_by_briefing(tt_rows, 1, handles.get("tiktok"))
    if tt and len(tt) >= 4:
        raw_tool = str(tt[0] or "").strip()
        raw_brief_tt = str(tt[1] or "").strip()
        tt_user = raw_tool if raw_tool and " " not in raw_tool else raw_brief_tt
        u = esc(tt_user.lstrip("@"))
        eng_raw = str(tt[2] or "").strip()
        eng_bit = f" · eng. {esc(eng_raw)}" if eng_raw and eng_raw != "—" else ""
        segs.append(
            "<span class='whitespace-nowrap'>"
            f"<span class='font-semibold text-slate-800'>TT</span> "
            f"<span class='font-mono text-slate-600'>@{u}</span> "
            f"<span class='text-slate-500'>·</span> {esc(tt[3])} seg{eng_bit}"
            "</span>"
        )

    yt = panel_row_by_briefing(yt_rows, 1, handles.get("youtube"))
    if yt and len(yt) >= 5:
        ch = esc(clip_txt(yt[0], 28))
        yu = esc(str(yt[1]).lstrip("@"))
        segs.append(
            "<span class='whitespace-nowrap'>"
            f"<span class='font-semibold text-slate-800'>YT</span> "
            f"<span class='font-mono text-slate-600'>@{yu}</span> "
            f"<span class='text-slate-500'>·</span> {esc(yt[2])} insc "
            f"<span class='text-slate-500'>·</span> {esc(yt[3])} views "
            f"<span class='text-slate-500'>·</span> {esc(yt[4])} víd."
            f"<span class='text-slate-400' title='{esc(str(yt[0] or ''))}'> ({ch})</span>"
            "</span>"
        )

    xr = panel_row_x(x_rows, name, handles.get("x"))
    if xr and len(xr) >= 5:
        xv = esc(str(xr[1]).lstrip("@"))
        act = esc(x_ativo_compact(xr[3]))
        teor = esc(clip_txt(xr[4], 36))
        segs.append(
            "<span class='whitespace-nowrap max-w-full'>"
            f"<span class='font-semibold text-slate-800'>X</span> "
            f"<span class='font-mono text-slate-600'>@{xv}</span> "
            f"<span class='text-slate-500'>·</span> {esc(xr[2])} seg "
            f"<span class='text-slate-500'>·</span> <span class='text-slate-600'>{act}</span>"
            f"<span class='text-slate-500'> · </span><span class='text-slate-500 italic'>{teor}</span>"
            "</span>"
        )

    if not segs:
        return (
            "<p class='text-[11px] text-slate-500 mb-3 py-1.5 px-2 rounded border border-dashed border-slate-200 bg-slate-50'>"
            "Sem linha nos painéis para este nome (IG / TT / YT / X).</p>"
        )
    inner = "<span class='text-slate-300 select-none px-0.5' aria-hidden='true'>|</span>".join(segs)
    return (
        "<div class='mb-3 rounded border border-slate-200 bg-slate-50/90 px-2 py-1.5'>"
        "<p class='text-[9px] font-bold uppercase tracking-wider text-slate-400 mb-1'>Redes · snapshot</p>"
        f"<div class='flex flex-wrap items-baseline gap-x-1 gap-y-0.5 text-[11px] leading-tight text-slate-700'>{inner}</div>"
        "</div>"
    )


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(
        f"<th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>{esc(h)}</th>"
        for h in headers
    )
    trs = []
    for row in rows:
        tds = "".join(f"<td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>{c}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return (
        "<div class='overflow-x-auto rounded border border-slate-200'>"
        "<table class='min-w-full'>"
        f"<thead class='bg-slate-50'><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>"
    )


def main() -> None:
    bundle = load_yaml(DATA / "dossier_loterias2026.yaml")
    meta = bundle.get("meta") or {}
    generated = datetime.now(timezone.utc).strftime("%d/%m/%Y")

    title = esc(meta.get("title", "Squad Always ON Loterias 2026 — Brand Safety"))
    subtitle = esc(meta.get("subtitle", ""))
    client = esc(meta.get("client_line", ""))
    periodo = esc(meta.get("periodo", "Março–abril de 2026"))

    pw_set = bundle.get("password_sha256_hex") or [
        "992743c627cb5ed96392d34989de45a8935c3df8faa62587e073b933004c1f1b",
    ]
    pw_json = ",\n            ".join(f"'{p}'" for p in pw_set)

    # Pedido do briefing (texto fixo + opcional do YAML)
    briefing_intro = bundle.get("briefing", {}).get("intro_paragraphs") or []
    if not briefing_intro:
        briefing_intro = [
            "Levantamento dos nomes indicados pela criação para compor o squad de entregas ao longo de 2026, com foco em risco de imagem para uma campanha institucional de loterias.",
        ]
    briefing_html = "".join(
        f"<p class='text-sm text-slate-700 leading-relaxed mb-3'>{esc(p)}</p>" for p in briefing_intro
    )

    criterios = bundle.get("briefing", {}).get("criterios") or [
        "Trabalhos atuais ou anteriores com marcas concorrentes (outras loterias, casas de apostas, cassinos online ou jogos de azar).",
        "Falas, atitudes ou envolvimento em situações delicadas ou polêmicas.",
        "Posicionamento político declarado ou inferido (conteúdo recorrente, causas, filiações).",
    ]
    crit_html = "<ol class='list-decimal pl-5 text-sm text-slate-700 space-y-2'>" + "".join(
        f"<li>{esc(c)}</li>" for c in criterios
    ) + "</ol>"

    redes = bundle.get("briefing", {}).get("redes") or ["Instagram", "TikTok", "YouTube", "X"]
    redes_html = "<p class='text-sm text-slate-700'><strong>Redes de ativação:</strong> " + esc(", ".join(redes)) + ".</p>"

    tier_order = bundle.get("briefing", {}).get("tier_order") or [
        "Tier 1",
        "Tier 2",
        "Mezzos",
        "Micros",
        "Página",
    ]
    tier_slug_map = {
        "Tier 1": "tier-1",
        "Tier 2": "tier-2",
        "Mezzos": "mezzos",
        "Micros": "micros",
        "Página": "pagina",
    }

    def tier_anchor(t: str) -> str:
        return tier_slug_map.get(t, slug_id(t))

    exec_summary_cfg = bundle.get("executive_summary") or {}
    exec_body_html = render_clevel_body(exec_summary_cfg)

    meth = bundle.get("methodology", {}).get("columns") or []
    meth_cards = ""
    for col in meth:
        meth_cards += (
            f"<div class='p-4 bg-white border border-slate-200 rounded'>"
            f"<p class='text-xs font-black text-calia-navy uppercase tracking-wide'>{esc(col.get('label', ''))}</p>"
            f"<p class='text-sm text-slate-600 mt-2 leading-relaxed'>{esc(col.get('body', ''))}</p></div>"
        )

    ig_for_panels = (bundle.get("panels", {}).get("instagram") or {}).get("rows") or []

    def panel_section(key: str, title_txt: str, foot: str) -> str:
        p = bundle.get("panels", {}).get(key) or {}
        if not p.get("headers") or not p.get("rows"):
            return ""
        disp_h, disp_r = normalize_panel_for_display(key, p, ig_for_panels)
        body_rows = [[esc(c) for c in r] for r in disp_r]
        tbl = render_table(disp_h, body_rows)
        foot_p = f"<p class='text-xs text-slate-500 mt-3'>{esc(foot)}</p>" if foot else ""
        return (
            f"<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>{esc(title_txt)}</h3>{tbl}{foot_p}</section>"
        )

    panels_intro = esc(
        bundle.get("panels", {}).get(
            "intro_note",
            "Números abaixo são retratos de ferramentas de mercado (alcance, engajamento, público). Servem só para contextualizar escala e formato — a decisão de risco deve seguir os três critérios do briefing.",
        )
    )
    panels_html = (
        f"<p class='text-sm text-slate-600 mb-6'>{panels_intro}</p>"
        + panel_section("instagram", "Instagram", bundle.get("panels", {}).get("instagram", {}).get("footnote", ""))
        + panel_section("tiktok", "TikTok", bundle.get("panels", {}).get("tiktok", {}).get("footnote", ""))
        + panel_section("youtube", "YouTube", bundle.get("panels", {}).get("youtube", {}).get("footnote", ""))
        + panel_section("x", "X", bundle.get("panels", {}).get("x", {}).get("footnote", ""))
    )

    cons = bundle.get("consolidated_narrative") or {}
    cons_title = esc(cons.get("title", "Síntese adicional do squad"))
    cons_body_html = render_clevel_body(cons) if (cons.get("blocks") or cons.get("bullets") or cons.get("paragraphs")) else ""

    profiles_cfg = bundle.get("profiles") or []
    _pn = bundle.get("panels") or {}
    ig_panel_rows = (_pn.get("instagram") or {}).get("rows") or []
    tt_panel_rows = (_pn.get("tiktok") or {}).get("rows") or []
    yt_panel_rows = (_pn.get("youtube") or {}).get("rows") or []
    x_panel_rows = (_pn.get("x") or {}).get("rows") or []

    toc_items = ""
    profile_sections = ""
    summary_rows: list[list[str]] = []

    def box(lab: str, txt: str | None) -> str:
        return (
            f"<div class='rounded border border-slate-200 p-4 bg-white'>"
            f"<p class='text-xs font-black uppercase text-calia-gold mb-2'>{esc(lab)}</p>"
            f"<p class='text-sm text-slate-700 leading-relaxed'>{esc(txt or '—')}</p></div>"
        )

    def render_profile(idx: int, pc: dict) -> str:
        name = pc.get("name", "")
        slug = slug_id(name)
        h = pc.get("handles") or {}
        networks_html = format_profile_networks_html(
            name, h, ig_panel_rows, tt_panel_rows, yt_panel_rows, x_panel_rows
        )
        eixos = pc.get("eixos") or {}
        narr = esc(pc.get("narrativa", ""))
        risco = esc(pc.get("risco_geral", "—"))
        tier_l = esc(pc.get("tier", "—"))
        return (
            f"<section id='{esc(slug)}' class='card-audit scroll-mt-20'>"
            f"<div class='flex flex-wrap items-baseline justify-between gap-2 border-b border-slate-200 pb-3 mb-4'>"
            f"<h2 class='text-xl font-black text-calia-navy'>{idx}. {esc(name)}</h2>"
            f"<span class='text-sm font-semibold text-slate-600'>Síntese de risco: {risco}</span></div>"
            f"<p class='text-xs text-slate-600 mb-2'><span class='font-bold text-calia-navy'>{tier_l}</span></p>"
            f"{networks_html}"
            f"<p class='text-sm text-slate-600 mb-6 leading-relaxed'>{narr}</p>"
            f"<div class='grid md:grid-cols-3 gap-4'>"
            f"{box('1. Concorrência (bets / loterias / jogos)', eixos.get('concorrencia'))}"
            f"{box('2. Polêmicas e situações delicadas', eixos.get('polemicas'))}"
            f"{box('3. Política e pautas sensíveis', eixos.get('politica'))}"
            f"</div></section>"
        )

    global_idx = 0
    for ti, tier_name in enumerate(tier_order):
        tslug = tier_anchor(tier_name)
        people = [p for p in profiles_cfg if p.get("tier") == tier_name]
        mt = "" if ti == 0 else " mt-4"
        toc_items += (
            f"<li class='{mt.strip()}'>"
            f"<a class='toc-link font-bold text-calia-navy' href='#{esc(tslug)}'>{esc(tier_name)}</a>"
        )
        if people:
            toc_items += "<ul class='mt-1 space-y-0.5 pl-0 list-none'>"
        blocks: list[str] = []
        for pc in people:
            global_idx += 1
            name = pc.get("name", "")
            slug = slug_id(name)
            toc_items += f"<li><a class='toc-link' href='#{esc(slug)}'>{global_idx}. {esc(name)}</a></li>"
            blocks.append(render_profile(global_idx, pc))
            rt = pc.get("resumo_tabela") or {}
            summary_rows.append(
                [
                    f"<strong>{esc(name)}</strong><br><span class='text-xs text-slate-500'>{esc(pc.get('tier', '—'))}</span>",
                    esc(rt.get("risco") or pc.get("risco_geral", "—")),
                    esc(rt.get("concorrencia", "—")),
                    esc(rt.get("polemicas", "—")),
                    esc(rt.get("politica", "—")),
                ]
            )
        if people:
            toc_items += "</ul>"
        toc_items += "</li>"

        if people:
            profile_sections += (
                f"<div id='{esc(tslug)}' class='scroll-mt-20 mb-10'>"
                f"<h3 class='text-lg font-black text-calia-navy border-b-2 border-calia-gold pb-2 mb-6'>{esc(tier_name)}</h3>"
                f"{''.join(blocks)}</div>"
            )
        elif tier_name == "Tier 2":
            profile_sections += (
                f"<div id='{esc(tslug)}' class='scroll-mt-20 mb-10'>"
                f"<h3 class='text-lg font-black text-calia-navy border-b-2 border-calia-gold pb-2 mb-4'>{esc(tier_name)}</h3>"
                f"<p class='text-sm text-slate-500 italic'>Nenhum nome nesta camada nesta versão do squad. Espaço reservado para inclusões futuras.</p></div>"
            )

    known_tiers = set(tier_order)
    orphan = [p for p in profiles_cfg if p.get("tier") not in known_tiers]
    if orphan:
        oslug = "sem-camada"
        toc_items += (
            f"<li class='mt-4'><a class='toc-link font-bold text-calia-navy' href='#{esc(oslug)}'>Sem camada definida</a>"
            "<ul class='mt-1 space-y-0.5 pl-0 list-none'>"
        )
        obl: list[str] = []
        for pc in orphan:
            global_idx += 1
            name = pc.get("name", "")
            slug = slug_id(name)
            toc_items += f"<li><a class='toc-link' href='#{esc(slug)}'>{global_idx}. {esc(name)}</a></li>"
            obl.append(render_profile(global_idx, pc))
            rt = pc.get("resumo_tabela") or {}
            summary_rows.append(
                [
                    f"<strong>{esc(name)}</strong><br><span class='text-xs text-slate-500'>—</span>",
                    esc(rt.get("risco") or pc.get("risco_geral", "—")),
                    esc(rt.get("concorrencia", "—")),
                    esc(rt.get("polemicas", "—")),
                    esc(rt.get("politica", "—")),
                ]
            )
        toc_items += "</ul></li>"
        profile_sections += (
            f"<div id='{esc(oslug)}' class='scroll-mt-20 mb-10'>"
            f"<h3 class='text-lg font-black text-calia-navy border-b-2 border-calia-gold pb-2 mb-6'>Sem camada definida</h3>"
            f"{''.join(obl)}</div>"
        )

    sum_table = render_table(
        ["Nome / camada", "Síntese de risco", "Concorrência", "Polêmicas", "Política"],
        summary_rows,
    )

    doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            'calia-navy': '#252525',
            'calia-gold': '#f9a619',
            'calia-emerald': '#009966',
            'calia-crimson': '#CC0033',
          }}
        }}
      }}
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    body {{ font-family: 'Inter', sans-serif; background-color: #f8fafc; color: #1e293b; }}
    .card-audit {{ background: white; border-radius: 6px; border: 1px solid #e2e8f0; padding: 1.75rem; margin-bottom: 1.5rem; }}
    .section-header {{ border-left: 4px solid #252525; padding-left: 1rem; margin-bottom: 1rem; }}
    .toc-link {{ font-size: 0.875rem; font-weight: 600; color: #252525; text-decoration: underline; text-decoration-color: #f9a619; text-underline-offset: 3px; }}
    .toc-list {{ margin: 0; padding: 0; list-style: none; border-left: 2px solid #f9a619; padding-left: 1rem; }}
    .toc-list li {{ margin-top: 0.35rem; }}
    .sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); border: 0; }}
  </style>
</head>
<body class="p-4 md:p-12">
  <div id="access-gate" class="fixed inset-0 z-[100] flex items-center justify-center bg-[#252525] p-4">
    <div class="w-full max-w-sm rounded border border-slate-600 bg-white p-8 shadow-2xl">
      <p class="text-xs font-bold uppercase tracking-wider text-calia-navy mb-1">Acesso restrito</p>
      <p class="text-sm text-slate-600 mb-4">Informe a senha para visualizar o conteúdo.</p>
      <form id="access-form" class="space-y-3">
        <label class="sr-only" for="access-pw">Senha</label>
        <input type="password" id="access-pw" required autocomplete="current-password" class="w-full rounded border border-slate-300 px-3 py-2 text-sm focus:border-calia-navy focus:outline-none focus:ring-1 focus:ring-calia-navy" placeholder="Senha">
        <p id="access-err" class="hidden text-sm font-medium text-red-600"></p>
        <div class="mt-5 border-t border-slate-200 pt-5">
          <button type="submit" class="w-full rounded-md bg-calia-gold py-3.5 text-sm font-black uppercase tracking-widest text-calia-navy shadow-md shadow-black/15 ring-1 ring-black/5 transition hover:brightness-105 active:brightness-95">Entrar</button>
        </div>
      </form>
      <p class="mt-6 border-t border-slate-200 pt-4 text-center text-[10px] font-bold uppercase tracking-[0.12em] text-slate-500">Agência Calia | Unidade de BI — Cliente CAIXA</p>
    </div>
  </div>

  <div id="dossier-root" class="hidden max-w-4xl mx-auto">
    <header id="topo" class="bg-calia-navy text-white p-8 md:p-10 rounded-lg shadow-lg mb-8">
      <p class="text-calia-gold font-bold tracking-widest text-xs uppercase">{client}</p>
      <h1 class="text-2xl md:text-3xl font-black mt-2 leading-tight">{title}</h1>
      <p class="text-sm opacity-90 mt-3">{subtitle}</p>
      <p class="text-xs opacity-75 mt-4">Atualização: {periodo} · Documento: {esc(generated)}</p>
    </header>

    <nav class="card-audit py-6" aria-label="Sumário">
      <div class="section-header"><h2 class="text-base font-black text-calia-navy uppercase">Sumário</h2></div>
      <ul class="toc-list text-sm">
        <li><a class="toc-link" href="#pedido">Pedido e critérios</a></li>
        <li><a class="toc-link" href="#leitura">Leitura rápida</a></li>
        <li><a class="toc-link" href="#como">Como foi analisado</a></li>
        <li><a class="toc-link" href="#perfis">Perfis por camada (Tier 1, Tier 2, Mezzos, Micros, Página)</a></li>
        <li><a class="toc-link" href="#sintese">Síntese do squad</a></li>
        <li><a class="toc-link" href="#tabela">Tabela resumo</a></li>
        <li><a class="toc-link" href="#metricas">Métricas nas redes (contexto)</a></li>
      </ul>
      <p class="text-xs text-slate-500 mt-6 font-semibold uppercase tracking-wide">Perfis</p>
      <ul class="toc-list">{toc_items}</ul>
    </nav>

    <section id="pedido" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Pedido e critérios de análise</h2></div>
      {briefing_html}
      <p class="text-sm font-bold text-calia-navy mt-4 mb-2">O que foi verificado para cada nome:</p>
      {crit_html}
      {redes_html}
    </section>

    <section id="leitura" class="card-audit scroll-mt-20 bg-slate-50">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Leitura rápida</h2></div>
      {exec_body_html}
    </section>

    <section id="como" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Como foi analisado</h2></div>
      <div class="grid sm:grid-cols-2 gap-3">{meth_cards}</div>
    </section>

    <section id="perfis" class="scroll-mt-20">
      <div class="section-header mb-6"><h2 class="text-xl font-black text-calia-navy">Perfis — análise por camada</h2></div>
      <p class="text-sm text-slate-600 mb-8">Ordem: Tier 1, Tier 2 (se houver nomes), Mezzos, Micros e Página.</p>
      {profile_sections}
    </section>

    <section id="sintese" class="card-audit scroll-mt-20 mb-6 bg-slate-50">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">{cons_title}</h2></div>
      {cons_body_html}
    </section>

    <section id="tabela" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Tabela resumo</h2></div>
      <p class="text-sm text-slate-600 mb-4">Síntese executiva por nome. O detalhe está em Perfis; números de rede vêm na seção seguinte.</p>
      {sum_table}
    </section>

    <section id="metricas" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Métricas nas redes (contexto)</h2></div>
      {panels_html}
    </section>

    <footer class="text-center py-10 text-xs text-slate-400 border-t border-slate-200">
      <a class="toc-link" href="#topo">Voltar ao topo</a> · Agência Calia · Uso interno · Always ON Loterias 2026
    </footer>
  </div>

  <script>
    const PASSWORD_SHA256_HEX_SET = new Set([ {pw_json} ]);
    async function sha256Hex(text) {{
      const buf = new TextEncoder().encode(text);
      const hash = await crypto.subtle.digest('SHA-256', buf);
      return Array.from(new Uint8Array(hash), (b) => b.toString(16).padStart(2, '0')).join('');
    }}
    document.getElementById('access-form').addEventListener('submit', async (e) => {{
      e.preventDefault();
      const err = document.getElementById('access-err');
      err.classList.add('hidden');
      err.textContent = 'Senha incorreta. Confira se não há espaços no início ou no fim; a senha é sensível a maiúsculas/minúsculas.';
      if (!globalThis.crypto?.subtle) {{
        err.textContent = 'Validação indisponível: abra a página em HTTPS (GitHub Pages) ou em contexto seguro; em arquivo local o navegador pode bloquear crypto.subtle.';
        err.classList.remove('hidden');
        return;
      }}
      const pw = document.getElementById('access-pw').value.trim();
      try {{
        if (!PASSWORD_SHA256_HEX_SET.has(await sha256Hex(pw))) {{
          err.classList.remove('hidden');
          return;
        }}
      }} catch {{
        err.textContent = 'Não foi possível validar a senha neste ambiente. Tente outro navegador ou a URL publicada no GitHub Pages.';
        err.classList.remove('hidden');
        return;
      }}
      document.getElementById('access-gate').classList.add('hidden');
      document.getElementById('dossier-root').classList.remove('hidden');
    }});
  </script>
</body>
</html>
"""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / "20260401-dossie-squad-always-on-loterias-2026.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(out_path.relative_to(ROOT.parent))


if __name__ == "__main__":
    main()
