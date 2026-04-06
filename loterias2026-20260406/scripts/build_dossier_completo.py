#!/usr/bin/env python3
"""
Gera dossiê HTML (Always ON Loterias 2026) a partir de data/dossier_loterias2026.yaml.
Saída: output/20260401-dossie-squad-always-on-loterias-2026.html
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = ROOT / "output"


def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


def build_revision_label() -> str:
    """Carimbo único por geração (compare com o HTML ao abrir no navegador)."""
    now = datetime.now(timezone.utc)
    br = now.astimezone(ZoneInfo("America/Sao_Paulo"))
    # Horário visível em pt-BR; UTC mantém comparação técnica.
    ts = (
        f"{br.strftime('%d/%m/%Y %H:%M')} Brasília · "
        f"UTC {now.strftime('%Y-%m-%d %H:%M')} · "
    )
    repo = ROOT.parent
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if r.returncode == 0 and (sha := (r.stdout or "").strip()):
            return f"{ts}{sha}"
    except (OSError, subprocess.SubprocessError):
        pass
    return f"{ts}(sem git)"


def _mini_md_bold_under(text: str) -> str:
    """**negrito** e __sublinhado__; sem links."""
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


def mini_md(s: object) -> str:
    """**negrito**, __sublinhado__, [rótulo](https://url) como link; restante escapado."""
    text = str(s or "")
    chunks: list[str] = []
    pos = 0
    for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        chunks.append(_mini_md_bold_under(text[pos : m.start()]))
        lab = m.group(1)
        url = (m.group(2) or "").strip()
        if re.match(r"https?://", url, re.I):
            chunks.append(
                '<a class="dossier-source-link text-blue-700 hover:text-blue-900 underline '
                'font-semibold decoration-calia-gold/70 hover:decoration-calia-gold underline-offset-2 '
                'break-words" href="'
                f'{esc(url)}" target="_blank" rel="noopener noreferrer">'
                f"{_mini_md_bold_under(lab)}</a>"
            )
        else:
            chunks.append(esc(m.group(0)))
        pos = m.end()
    chunks.append(_mini_md_bold_under(text[pos:]))
    return "".join(chunks)


def methodology_column_body_html(body: object) -> str:
    """Vários parágrafos no YAML separados por linha em branco (\\n\\n)."""
    b = str(body or "").strip()
    if not b:
        return ""
    parts = [p.strip() for p in b.split("\n\n") if p.strip()]
    if len(parts) == 1:
        return (
            "<p class='text-sm text-slate-600 mt-2 leading-relaxed'>"
            f"{mini_md(parts[0])}</p>"
        )
    return "".join(
        f"<p class='text-sm text-slate-600 mt-2 leading-relaxed'>{mini_md(p)}</p>"
        for p in parts
    )


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
        # Remove coluna Obs. (não entra no dossiê)
        if out_h:
            last = str(out_h[-1] or "").strip().lower().rstrip(".")
            if last in ("obs", "observações", "observacoes"):
                out_h = out_h[:-1]
                n = len(out_h)
                new_rows: list[list] = []
                for r in rows:
                    r = list(r)
                    if len(r) >= n:
                        new_rows.append(r[:n])
                    else:
                        new_rows.append(r + ["—"] * (n - len(r)))
                rows = new_rows
        return out_h, rows

    if key == "tiktok" and len(headers) >= 2:
        out_h = ["Nome", "Usuário"] + headers[2:]
        # Remove coluna "Seguindo" se ainda existir em YAML antigo
        try:
            si = next(
                i
                for i, h in enumerate(out_h)
                if str(h or "").strip().lower() in ("seguindo", "seguindo.")
            )
            out_h = out_h[:si] + out_h[si + 1 :]
            adj = si - 2  # índice na linha bruta após [tool, brief] = r[0], r[1]
            for ri, r in enumerate(rows):
                r = list(r)
                if len(r) > adj + 2:
                    del r[adj + 2]
                rows[ri] = r
        except StopIteration:
            pass
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
        ativo_label = "Posts recentes (checagem)"
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


def profiles_in_summary_order(profiles_cfg: list, tier_order: list) -> list[dict]:
    """Mesma ordem da Tabela resumo: tier_order, depois perfis sem tier conhecido."""
    known = set(tier_order)
    ordered: list[dict] = []
    for t in tier_order:
        ordered.extend([p for p in profiles_cfg if p.get("tier") == t])
    for p in profiles_cfg:
        if p.get("tier") not in known:
            ordered.append(p)
    return ordered


def name_tier_cell_html(name: object, _tier: object) -> str:
    """Primeira coluna dos painéis (Nome): só o nome; camada não é exibida na célula."""
    n = esc(name or "—")
    return f"<strong class='font-semibold text-slate-900'>{n}</strong>"


def panel_row_index_for_profile(panel_key: str, raw_rows: list[list], pc: dict) -> int | None:
    """Índice da linha no painel YAML: coluna 1 = @ do briefing (IG/TT/YT); X por nome ou @."""
    h = pc.get("handles") or {}
    name_l = str(pc.get("name") or "").strip().lower()
    if panel_key == "instagram":
        k = norm_handle(h.get("instagram"))
        if not k:
            return None
        for i, r in enumerate(raw_rows):
            if len(r) > 1 and norm_handle(r[1]) == k:
                return i
        return None
    if panel_key == "tiktok":
        k = norm_handle(h.get("tiktok"))
        if not k:
            return None
        for i, r in enumerate(raw_rows):
            if len(r) > 1 and norm_handle(r[1]) == k:
                return i
        return None
    if panel_key == "youtube":
        k = norm_handle(h.get("youtube"))
        if not k:
            return None
        for i, r in enumerate(raw_rows):
            if len(r) > 1 and norm_handle(r[1]) == k:
                return i
        return None
    if panel_key == "x":
        xk = norm_handle(h.get("x"))
        for i, r in enumerate(raw_rows):
            if len(r) < 2:
                continue
            if name_l and str(r[0] or "").strip().lower() == name_l:
                return i
            if xk and norm_handle(r[1]) == xk:
                return i
        return None
    return None


def _metric_cells_all_empty(rest_raw: list) -> bool:
    """True se não há dado em nenhuma coluna de métrica (só traço, vazio ou equivalente)."""
    miss = frozenset({"", "—", "–", "-", "n/a", "na", "N/A", "NA"})
    for v in rest_raw:
        t = str(v or "").strip().lower()
        if t in frozenset({"n/a", "na"}):
            t = ""
        if t not in frozenset({"", "—", "–", "-"}):
            return False
    return True


def build_ordered_panel_rows(
    panel_key: str,
    disp_headers: list[str],
    disp_rows: list[list],
    ordered_profiles: list[dict],
    raw_rows: list[list],
) -> tuple[list[str], list[list[str]]]:
    """Cabeçalho Nome + métricas; linhas na ordem da tabela resumo.
    Omite criador quando não há perfil na rede (todas as métricas vazias/—)."""
    h0 = "Nome"
    out_headers = [h0] + list(disp_headers[1:])
    n_rest = max(0, len(disp_headers) - 1)
    out_rows: list[list[str]] = []
    for pc in ordered_profiles:
        first = name_tier_cell_html(pc.get("name"), pc.get("tier"))
        idx = panel_row_index_for_profile(panel_key, raw_rows, pc)
        found = disp_rows[idx] if idx is not None and idx < len(disp_rows) else None
        if found and len(found) > 1:
            rest_raw = list(found[1 : 1 + n_rest])
        elif found:
            rest_raw = list(found[1:])
        else:
            rest_raw = []
        while len(rest_raw) < n_rest:
            rest_raw.append("—")
        rest_raw = rest_raw[:n_rest]
        if _metric_cells_all_empty(rest_raw):
            continue
        rest = [esc(str(x)) for x in rest_raw]
        out_rows.append([first] + rest)
    return out_headers, out_rows


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
            "Havia posts recentes na checagem",
            "bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/80",
        )
    if low in ("não", "nao"):
        return (
            "Sem posts recentes na checagem",
            "bg-slate-100 text-slate-700 ring-1 ring-slate-200",
        )
    return (raw or "—", "bg-slate-50 text-slate-600 ring-1 ring-slate-200")


def net_mini_card(
    bar_class: str,
    platform: str,
    handle_raw: str,
    stats_html: str,
    footer_html: str = "",
) -> str:
    """Mini-card compacto: barra de cor, plataforma, @ e métricas (texto completo, quebra de linha)."""
    h = str(handle_raw or "").lstrip("@")
    return (
        "<div class='group min-w-0 rounded-lg border border-slate-200/90 bg-white p-2 shadow-sm "
        "ring-1 ring-slate-100/80 hover:border-slate-300 hover:shadow transition-shadow'>"
        "<div class='flex gap-2 min-w-0'>"
        f"<div class='w-0.5 shrink-0 rounded-full {esc(bar_class)}' aria-hidden='true'></div>"
        "<div class='min-w-0 flex-1'>"
        f"<p class='text-[9px] font-bold uppercase tracking-wider text-slate-500 leading-none mb-1'>{esc(platform)}</p>"
        f"<p class='font-mono text-[11px] text-slate-700 break-all leading-snug'>@{esc(h)}</p>"
        f"<div class='mt-1.5 flex flex-wrap gap-x-2.5 gap-y-0.5 text-[11px] leading-tight'>{stats_html}</div>"
        f"{footer_html}"
        "</div></div></div>"
    )


def stat_pair(short_label: str, value: str) -> str:
    return (
        "<span class='inline-flex items-baseline gap-0.5'>"
        f"<span class='text-[9px] font-medium uppercase text-slate-400'>{esc(short_label)}</span>"
        f"<span class='font-semibold tabular-nums text-slate-900'>{esc(value)}</span>"
        "</span>"
    )


def format_profile_networks_html(
    name: str,
    handles: dict,
    ig_rows: list,
    tt_rows: list,
    yt_rows: list,
    x_rows: list,
) -> str:
    """Handles e números a partir dos painéis — mini-cards em grade, compactos e sem estouro."""
    cards: list[str] = []

    # Mini-cards por perfil: só @handles — métricas ficam nas tabelas de painéis (evita repetir números no texto do creator).
    ig = panel_row_by_briefing(ig_rows, 1, handles.get("instagram"))
    if ig and len(ig) >= 7:
        u = str(ig[1]).lstrip("@")
        cards.append(net_mini_card("bg-gradient-to-b from-pink-500 to-rose-600", "Instagram", u, ""))

    tt = panel_row_by_briefing(tt_rows, 1, handles.get("tiktok"))
    if tt and len(tt) >= 4:
        raw_tool = str(tt[0] or "").strip()
        raw_brief_tt = str(tt[1] or "").strip()
        tt_user = raw_tool if raw_tool and " " not in raw_tool else raw_brief_tt
        u = tt_user.lstrip("@")
        cards.append(net_mini_card("bg-slate-800", "TikTok", u, ""))

    yt = panel_row_by_briefing(yt_rows, 1, handles.get("youtube"))
    if yt and len(yt) >= 5:
        yu = str(yt[1]).lstrip("@")
        ch_full = str(yt[0] or "").strip()
        footer = (
            "<p class='mt-1.5 pt-1 border-t border-slate-100 text-[9px] text-slate-500 break-words leading-snug'>"
            f"<span class='text-slate-400'>Canal · </span>{esc(ch_full)}</p>"
        )
        cards.append(net_mini_card("bg-red-600", "YouTube", yu, "", footer))

    # X: só mini-card se o YAML trata como canal oficial (handle preenchido).
    # Contas protegidas, homônimos ou com audiência muito baixa ficam vazias — como se não houvesse X.
    x_h = handles.get("x")
    xr = (
        panel_row_x(x_rows, name, x_h)
        if (x_h and str(x_h).strip())
        else None
    )
    if xr and len(xr) >= 5:
        xv = str(xr[1]).lstrip("@")
        act_txt, act_cls = humanize_x_ativo(xr[3])
        raw_act = str(xr[3] or "").strip().lower()
        if raw_act in ("sim", "s", "yes"):
            chip_label = "posts recentes"
        elif raw_act in ("não", "nao"):
            chip_label = "sem posts recentes"
        else:
            chip_label = str(xr[3] or "").strip() or "—"
        teor_full = str(xr[4] or "").strip()
        footer = (
            "<div class='mt-1.5 pt-1 border-t border-slate-100 space-y-1'>"
            f"<span class='inline-block max-w-full rounded px-1.5 py-0.5 text-[9px] font-semibold leading-snug break-words {act_cls}' "
            f"title='{esc(act_txt)}'>{esc(chip_label)}</span>"
            f"<p class='text-[9px] text-slate-500 leading-snug break-words'>{esc(teor_full)}</p>"
            "</div>"
        )
        cards.append(net_mini_card("bg-slate-900", "X", xv, "", footer))

    if not cards:
        return (
            "<p class='text-[11px] text-slate-500 mb-4 py-2 px-2.5 rounded-lg border border-dashed border-slate-200 "
            "bg-slate-50/90'>Sem linha nos painéis para este nome (Instagram / TikTok / YouTube).</p>"
        )
    n = len(cards)
    if n == 1:
        grid_cls = "grid-cols-1 max-w-[14rem] sm:max-w-[15rem]"
    elif n == 2:
        grid_cls = "grid-cols-2"
    else:
        grid_cls = "grid-cols-2 md:grid-cols-3"

    return (
        "<div class='mb-4'>"
        "<p class='text-[9px] font-bold uppercase tracking-widest text-slate-400 mb-2'>Redes · handles oficiais (métricas nas tabelas abaixo)</p>"
        f"<div class='grid {grid_cls} gap-2'>{''.join(cards)}</div>"
        "</div>"
    )


def risco_badge_shell_classes(text: object) -> str:
    """Classes Tailwind do selo conforme palavras-chave no texto de risco."""
    low = str(text or "").lower()
    if re.search(r"\balto\b", low):
        return (
            "bg-red-50 text-red-900 ring-1 ring-red-200/90 border border-red-100 "
            "shadow-sm"
        )
    if "moderado" in low or "pouca prova" in low:
        return (
            "bg-amber-50 text-amber-950 ring-1 ring-amber-200/90 border border-amber-100 "
            "shadow-sm"
        )
    if "baixo" in low:
        return (
            "bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200/90 border border-emerald-100 "
            "shadow-sm"
        )
    return "bg-slate-100 text-slate-800 ring-1 ring-slate-200 border border-slate-200 shadow-sm"


def risco_badge_block_html(body: object, *, compact: bool = False) -> str:
    """Selo visível para síntese de risco (perfil ou tabela). Aceita mini-markdown (**negrito**)."""
    txt = str(body or "—").strip() or "—"
    shell = risco_badge_shell_classes(txt)
    inner = mini_md(txt)
    if compact:
        return (
            f"<span class='inline-flex max-w-[16rem] rounded-lg px-2.5 py-1.5 text-xs font-bold "
            f"leading-snug {shell}'>{inner}</span>"
        )
    return (
        "<span class='inline-flex flex-col items-end gap-1 shrink-0 max-w-full sm:max-w-[min(100%,30rem)]'>"
        "<span class='text-[9px] font-black uppercase tracking-wider text-calia-navy'>"
        "Síntese de risco</span>"
        f"<span class='inline-flex rounded-lg px-3 py-2 text-xs sm:text-sm font-bold leading-snug text-right "
        f"{shell}'>{inner}</span>"
        "</span>"
    )


def render_table(
    headers: list[str],
    rows: list[list[str]],
    *,
    html_safe_columns: frozenset[int] | None = None,
) -> str:
    th = "".join(
        f"<th class='py-2 px-3 text-left text-xs font-bold text-slate-600 border-b border-slate-200'>{esc(h)}</th>"
        for h in headers
    )
    trs = []
    for row in rows:
        tds_l: list[str] = []
        for j, c in enumerate(row):
            cell = c if (html_safe_columns is not None and j in html_safe_columns) else esc(c)
            tds_l.append(
                f"<td class='py-2 px-3 border-b border-slate-100 text-sm align-top'>{cell}</td>"
            )
        tds = "".join(tds_l)
        trs.append(f"<tr>{tds}</tr>")
    return (
        "<div class='overflow-x-auto rounded border border-slate-200'>"
        "<table class='min-w-full'>"
        f"<thead class='bg-slate-50'><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>"
    )


def main(*, no_gate: bool = False) -> None:
    bundle = load_yaml(DATA / "dossier_loterias2026.yaml")
    meta = bundle.get("meta") or {}
    generated = datetime.now(timezone.utc).strftime("%d/%m/%Y")
    build_revision = build_revision_label()

    title = esc(meta.get("title", "Squad Always ON Loterias 2026 — Brand Safety"))
    subtitle = esc(meta.get("subtitle", ""))
    client = esc(meta.get("client_line", ""))
    periodo = esc(meta.get("periodo", "Março–abril de 2026"))

    pw_set = bundle.get("password_sha256_hex") or [
        "992743c627cb5ed96392d34989de45a8935c3df8faa62587e073b933004c1f1b",
    ]
    pw_json = ",\n            ".join(f"'{p}'" for p in pw_set)

    gate_wrap_cls = "hidden" if no_gate else (
        "fixed inset-0 z-[100] flex items-center justify-center bg-[#252525] p-4"
    )
    root_wrap_cls = "max-w-4xl mx-auto" if no_gate else "hidden max-w-4xl mx-auto"

    # Pedido do briefing (texto fixo + opcional do YAML)
    briefing_intro = bundle.get("briefing", {}).get("intro_paragraphs") or []
    if not briefing_intro:
        briefing_intro = [
            "Levantamento dos nomes indicados pela criação para compor o squad de entregas ao longo de 2026, com foco em risco de imagem para uma campanha institucional de loterias.",
        ]
    briefing_html = "".join(
        f"<p class='text-sm text-slate-700 leading-relaxed mb-3'>{mini_md(p)}</p>" for p in briefing_intro
    )

    criterios = bundle.get("briefing", {}).get("criterios") or [
        "Trabalhos atuais ou anteriores com marcas concorrentes (outras loterias, casas de apostas, cassinos online ou jogos de azar).",
        "Falas, atitudes ou envolvimento em situações delicadas ou polêmicas.",
        "Posicionamento político declarado ou inferido (conteúdo recorrente, causas, filiações).",
    ]
    crit_html = "<ol class='list-decimal pl-5 text-sm text-slate-700 space-y-2'>" + "".join(
        f"<li>{mini_md(c)}</li>" for c in criterios
    ) + "</ol>"

    redes = bundle.get("briefing", {}).get("redes") or ["Instagram", "TikTok", "YouTube"]
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

    profiles_cfg = bundle.get("profiles") or []
    ordered_profiles = profiles_in_summary_order(profiles_cfg, tier_order)

    exec_summary_cfg = bundle.get("executive_summary") or {}
    exec_body_html = render_clevel_body(exec_summary_cfg)

    meth = bundle.get("methodology", {}).get("columns") or []
    meth_cards = ""
    for col in meth:
        meth_cards += (
            f"<div class='p-4 bg-white border border-slate-200 rounded'>"
            f"<p class='text-xs font-black text-calia-navy uppercase tracking-wide'>{esc(col.get('label', ''))}</p>"
            f"{methodology_column_body_html(col.get('body', ''))}</div>"
        )

    ig_for_panels = (bundle.get("panels", {}).get("instagram") or {}).get("rows") or []

    def format_panel_footnote(foot: str) -> str:
        t = (foot or "").strip()
        if not t:
            return ""
        if t.lower().startswith("fonte:"):
            return t
        return f"Fonte: {t}"

    _pn_all_pre = bundle.get("panels") or {}

    def esc_lines_br(s: str) -> str:
        """Quebras de linha no YAML viram <br> (texto escapado por linha)."""
        lines = (s or "").strip().splitlines()
        return "<br />".join(esc(line.strip()) for line in lines if line.strip())

    def coverage_block_html(base: str, cells_dash: str) -> str:
        b = (base or "").strip()
        d = (cells_dash or "").strip()
        if not b and not d:
            return ""
        paras: list[str] = []
        if b:
            paras.append(
                f"<p class='text-xs text-slate-500 mt-3 max-w-prose leading-relaxed'>{esc(b)}</p>"
            )
        if d:
            paras.append(
                f"<p class='text-xs text-slate-500 mt-2 max-w-prose leading-relaxed'>"
                f"{esc_lines_br(d)}</p>"
            )
        return "".join(paras)

    _cov_base = (
        (_pn_all_pre.get("coverage_note") or _pn_all_pre.get("missing_rows_note") or "")
        .strip()
    )
    _cov_dash = (_pn_all_pre.get("coverage_note_cells_dash") or "").strip()
    coverage_after_foot_short = coverage_block_html(_cov_base, "")
    coverage_after_foot_tiktok = coverage_block_html(_cov_base, _cov_dash)

    def panel_section(key: str, title_txt: str, foot: str, coverage_suffix: str) -> str:
        p = bundle.get("panels", {}).get(key) or {}
        if not p.get("headers") or not p.get("rows"):
            return ""
        raw_r = [list(r) for r in (p.get("rows") or [])]
        disp_h, disp_r = normalize_panel_for_display(key, p, ig_for_panels)
        oh, body_rows = build_ordered_panel_rows(
            key, disp_h, disp_r, ordered_profiles, raw_r
        )
        if not body_rows:
            empty_msg = (
                "<p class='text-sm text-slate-500 italic py-2'>Nenhum perfil da lista com dados nesta rede "
                "nesta coleta.</p>"
            )
            foot_fmt = format_panel_footnote(foot)
            foot_p = f"<p class='text-xs text-slate-500 mt-3'>{esc(foot_fmt)}</p>" if foot_fmt else ""
            return (
                f"<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>{esc(title_txt)}</h3>"
                f"{empty_msg}{foot_p}{coverage_suffix}</section>"
            )
        tbl = render_table(oh, body_rows, html_safe_columns=frozenset({0}))
        foot_fmt = format_panel_footnote(foot)
        foot_p = f"<p class='text-xs text-slate-500 mt-3'>{esc(foot_fmt)}</p>" if foot_fmt else ""
        return (
            f"<section class='mb-10'><h3 class='text-lg font-black text-calia-navy mb-2'>{esc(title_txt)}</h3>"
            f"{tbl}{foot_p}{coverage_suffix}</section>"
        )

    panels_intro = esc(
        bundle.get("panels", {}).get(
            "intro_note",
            "Números das ferramentas (alcance, engajamento). Só ajudam a ver tamanho de público; o risco da campanha segue os três critérios acima.",
        )
    )
    _pn_all = bundle.get("panels") or {}
    panels_html = (
        f"<p class='text-sm text-slate-600 mb-6'>{panels_intro}</p>"
        + panel_section(
            "instagram",
            "Instagram",
            _pn_all.get("instagram", {}).get("footnote", ""),
            coverage_after_foot_short,
        )
        + panel_section(
            "tiktok",
            "TikTok",
            _pn_all.get("tiktok", {}).get("footnote", ""),
            coverage_after_foot_tiktok,
        )
        + panel_section(
            "youtube",
            "YouTube",
            _pn_all.get("youtube", {}).get("footnote", ""),
            coverage_after_foot_short,
        )
        + panel_section(
            "x",
            "X",
            _pn_all.get("x", {}).get("footnote", ""),
            coverage_after_foot_short,
        )
    )

    cons = bundle.get("consolidated_narrative") or {}
    cons_title = esc(cons.get("title", "Síntese adicional do squad"))
    cons_body_html = render_clevel_body(cons) if (cons.get("blocks") or cons.get("bullets") or cons.get("paragraphs")) else ""

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
            f"<p class='text-sm text-slate-700 leading-relaxed'>{mini_md(txt or '—')}</p></div>"
        )

    def render_profile(idx: int, pc: dict) -> str:
        name = pc.get("name", "")
        slug = slug_id(name)
        h = pc.get("handles") or {}
        networks_html = format_profile_networks_html(
            name, h, ig_panel_rows, tt_panel_rows, yt_panel_rows, x_panel_rows
        )
        eixos = pc.get("eixos") or {}
        narr = mini_md(pc.get("narrativa", ""))
        risco_raw = pc.get("risco_geral", "—")
        risco_badge = risco_badge_block_html(risco_raw, compact=False)
        return (
            f"<section id='{esc(slug)}' class='card-audit scroll-mt-20'>"
            f"<div class='flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-3 mb-4'>"
            f"<h2 class='text-xl font-black text-calia-navy'>{idx}. {esc(name)}</h2>"
            f"{risco_badge}</div>"
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
            risco_cell = risco_badge_block_html(pc.get("risco_geral", "—"), compact=True)
            summary_rows.append(
                [
                    f"<strong>{esc(name)}</strong>",
                    risco_cell,
                    mini_md(rt.get("concorrencia", "—")),
                    mini_md(rt.get("polemicas", "—")),
                    mini_md(rt.get("politica", "—")),
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
            risco_cell_o = risco_badge_block_html(pc.get("risco_geral", "—"), compact=True)
            summary_rows.append(
                [
                    f"<strong>{esc(name)}</strong>",
                    risco_cell_o,
                    mini_md(rt.get("concorrencia", "—")),
                    mini_md(rt.get("polemicas", "—")),
                    mini_md(rt.get("politica", "—")),
                ]
            )
        toc_items += "</ul></li>"
        profile_sections += (
            f"<div id='{esc(oslug)}' class='scroll-mt-20 mb-10'>"
            f"<h3 class='text-lg font-black text-calia-navy border-b-2 border-calia-gold pb-2 mb-6'>Sem camada definida</h3>"
            f"{''.join(obl)}</div>"
        )

    sum_table = render_table(
        ["Nome", "Síntese de risco", "Concorrência", "Polêmicas", "Política"],
        summary_rows,
        html_safe_columns=frozenset({0, 1, 2, 3, 4}),
    )

    tier_order_label = esc(", ".join(tier_order))

    doc = f"""<!DOCTYPE html>
<!-- calia-dossier-build: {esc(build_revision)} -->
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
    /* Links de fonte: texto azul; sublinhado dourado (calia-gold), como antes do ajuste */
    #dossier-root a.dossier-source-link,
    #dossier-root a[href^="http"] {{
      color: #1d4ed8 !important;
      text-decoration: underline;
      text-decoration-color: rgba(249, 166, 25, 0.75);
      text-underline-offset: 3px;
      font-weight: 600;
    }}
    #dossier-root a.dossier-source-link:hover,
    #dossier-root a[href^="http"]:hover {{
      color: #1e3a8a !important;
      text-decoration-color: #f9a619;
    }}
  </style>
</head>
<body class="p-4 md:p-12">
  <div id="access-gate" class="{gate_wrap_cls}">
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

  <div id="dossier-root" class="{root_wrap_cls}">
    <header id="topo" class="bg-calia-navy text-white p-8 md:p-10 rounded-lg shadow-lg mb-8">
      <p class="text-calia-gold font-bold tracking-widest text-xs uppercase">{client}</p>
      <h1 class="text-2xl md:text-3xl font-black mt-2 leading-tight">{title}</h1>
      <p class="text-sm opacity-90 mt-3">{subtitle}</p>
      <p class="text-xs opacity-75 mt-4">Atualização: {periodo} · Documento: {esc(generated)} · Build: <code class="text-[10px] bg-white/10 px-1 rounded">{esc(build_revision)}</code></p>
    </header>

    <nav class="card-audit py-6" aria-label="Sumário">
      <div class="section-header"><h2 class="text-base font-black text-calia-navy uppercase">Sumário</h2></div>
      <ul class="toc-list text-sm">
        <li><a class="toc-link" href="#pedido">Pedido e critérios</a></li>
        <li><a class="toc-link" href="#leitura">Leitura rápida</a></li>
        <li><a class="toc-link" href="#como">Como foi analisado</a></li>
        <li><a class="toc-link" href="#perfis">Perfis por camada ({tier_order_label})</a></li>
        <li><a class="toc-link" href="#sintese">Síntese do conjunto</a></li>
        <li><a class="toc-link" href="#tabela">Tabela resumo</a></li>
        <li><a class="toc-link" href="#metricas">Métricas nas redes</a></li>
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
      <p class="text-xs text-blue-800 bg-blue-50 border border-blue-200 rounded px-3 py-2 mb-4">
        <strong>Fontes:</strong> trechos em <span class="text-blue-700 font-semibold underline decoration-calia-gold/80">azul com sublinhado dourado</span> são links para matérias ou páginas (abrem em nova aba).
      </p>
      {exec_body_html}
    </section>

    <section id="como" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Como foi analisado</h2></div>
      <div class="grid sm:grid-cols-2 gap-3">{meth_cards}</div>
    </section>

    <section id="perfis" class="scroll-mt-20">
      <div class="section-header mb-6"><h2 class="text-xl font-black text-calia-navy">Perfis — análise por camada</h2></div>
      {profile_sections}
    </section>

    <section id="sintese" class="card-audit scroll-mt-20 mb-6 bg-slate-50">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">{cons_title}</h2></div>
      {cons_body_html}
    </section>

    <section id="tabela" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Tabela resumo</h2></div>
      <p class="text-sm text-slate-600 mb-4">Uma linha por nome; o detalhe está em Perfis e nas métricas abaixo.</p>
      {sum_table}
    </section>

    <section id="metricas" class="card-audit scroll-mt-20">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy">Métricas nas redes</h2></div>
      {panels_html}
    </section>

    <footer class="text-center py-10 text-xs text-slate-400 border-t border-slate-200">
      <a class="toc-link" href="#topo">Voltar ao topo</a> · Agência Calia · Uso interno · Always ON Loterias 2026
      <p class="mt-3 text-[10px] text-slate-500 max-w-prose mx-auto leading-relaxed">
        <strong>Build:</strong> <code class="text-slate-600">{esc(build_revision)}</code>
        Se o <strong>GitHub Pages</strong> mostrar um build diferente do arquivo gerado localmente,
        falta <code class="text-slate-600">git push</code> do HTML em <code class="text-slate-600">caixa/</code>.
      </p>
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
    out_path = OUT_DIR / "20260406-dossie-squad-always-on-loterias-2026.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(out_path.relative_to(ROOT.parent))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gera dossiê HTML a partir do YAML.")
    ap.add_argument(
        "--no-gate",
        action="store_true",
        help="Sem tela de senha (útil para arquivo local / preview; conteúdo visível de imediato).",
    )
    args = ap.parse_args()
    main(no_gate=args.no_gate)
