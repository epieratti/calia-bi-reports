#!/usr/bin/env python3
"""
Gera dossiê HTML único (Brand Safety — Always ON Loterias 2026) a partir de
`data/dossier_loterias2026.yaml` + `data/influencers.yaml`.

Saída: output/20260401-dossie-squad-always-on-loterias-2026.html

Uso: cd loterias2026 && python scripts/build_dossier_completo.py
"""
from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT_DIR = ROOT / "output"


def esc(s: object) -> str:
    return html.escape(str(s or ""), quote=True)


def slug_id(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return s or "perfil"


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_table(headers: list[str], rows: list[list[str]], css: str = "min-w-full text-sm") -> str:
    th = "".join(f"<th class='py-2 px-3 text-left text-xs uppercase text-slate-500 border-b border-slate-200'>{esc(h)}</th>" for h in headers)
    trs = []
    for row in rows:
        tds = "".join(f"<td class='py-2 px-3 border-b border-slate-100 align-top'>{c}</td>" for c in row)
        trs.append(f"<tr>{tds}</tr>")
    return (
        f"<div class='overflow-x-auto'><table class='{esc(css)}'>"
        f"<thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div>"
    )


def main() -> None:
    bundle = load_yaml(DATA / "dossier_loterias2026.yaml")
    influencers = load_yaml(DATA / "influencers.yaml")
    meta = bundle.get("meta") or {}
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    title = esc(meta.get("title", "Dossiê Brand Safety — Loterias 2026"))
    subtitle = esc(meta.get("subtitle", ""))
    client = esc(meta.get("client_line", ""))
    snapshot = esc(meta.get("snapshot", ""))

    pw_set = bundle.get("password_sha256_hex") or [
        "992743c627cb5ed96392d34989de45a8935c3df8faa62587e073b933004c1f1b",
        "dd21caa79adaf906f9607c301edb4336c61a2e4fb7021869758e9818e7d009e5",
    ]
    pw_json = ",\n            ".join(f"'{p}'" for p in pw_set)

    # --- Governance & methodology (from YAML markdown-ish blocks)
    gov_paras = bundle.get("governance", {}).get("paragraphs") or []
    gov_html = "".join(f"<p class='text-sm text-slate-700 leading-relaxed mb-3'>{esc(p)}</p>" for p in gov_paras)

    exec_bullets = bundle.get("executive_summary", {}).get("bullets") or []
    exec_html = "".join(
        f"<li class='flex gap-3'><span class='mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-calia-gold'></span><span>{esc(b)}</span></li>"
        for b in exec_bullets
    )

    meth = bundle.get("methodology", {}).get("columns") or []
    meth_cards = ""
    for col in meth:
        meth_cards += (
            f"<div class='p-4 bg-slate-50 border-t-2 border-calia-navy'>"
            f"<p class='text-[10px] font-black uppercase text-calia-gold tracking-widest'>{esc(col.get('label', ''))}</p>"
            f"<p class='text-sm text-slate-700 mt-2 leading-relaxed'>{esc(col.get('body', ''))}</p></div>"
        )

    # --- Panel tables
    def panel_section(key: str, title_txt: str, src_note: str) -> str:
        p = bundle.get("panels", {}).get(key) or {}
        if not p.get("headers") or not p.get("rows"):
            return ""
        headers = p["headers"]
        body_rows: list[list[str]] = []
        for r in p["rows"]:
            body_rows.append([esc(c) for c in r])
        tbl = render_table(headers, body_rows)
        return (
            f"<section class='card-audit'><div class='section-header mb-4'>"
            f"<h2 class='text-xl font-black text-calia-navy uppercase tracking-tight'>{esc(title_txt)}</h2>"
            f"<p class='source-tag'>{esc(src_note)}</p></div>{tbl}</section>"
        )

    panels_html = (
        panel_section(
            "instagram",
            "Painel Instagram",
            bundle.get("panels", {}).get("instagram", {}).get("source_note", ""),
        )
        + panel_section(
            "tiktok",
            "Painel TikTok",
            bundle.get("panels", {}).get("tiktok", {}).get("source_note", ""),
        )
        + panel_section(
            "youtube",
            "Painel YouTube",
            bundle.get("panels", {}).get("youtube", {}).get("source_note", ""),
        )
        + panel_section(
            "x",
            "Painel X (Twitter)",
            bundle.get("panels", {}).get("x", {}).get("source_note", ""),
        )
    )

    # --- Consolidated narrative block
    cons = bundle.get("consolidated_narrative") or {}
    cons_html = ""
    if cons.get("title"):
        cons_html += (
            f"<section class='card-audit border-l-4 border-calia-emerald'><div class='section-header'>"
            f"<h2 class='text-xl font-black text-calia-navy uppercase'>{esc(cons['title'])}</h2>"
            f"<p class='text-xs text-slate-500 mt-1'>{esc(cons.get('subtitle', ''))}</p></div>"
        )
        for para in cons.get("paragraphs") or []:
            cons_html += f"<p class='text-sm text-slate-700 leading-relaxed mb-3'>{esc(para)}</p>"
        cons_html += "</section>"

    # --- Profiles from bundle (order = YAML order)
    profiles_yaml = influencers.get("profiles") or []
    by_name = {p.get("name"): p for p in profiles_yaml}
    profiles_cfg = bundle.get("profiles") or []

    toc_items = ""
    profile_sections = ""
    summary_rows: list[list[str]] = []

    for i, pc in enumerate(profiles_cfg, 1):
        name = pc.get("name", "")
        slug = slug_id(name)
        toc_items += f"<li><a class='toc-link' href='#{slug}'>{i}. {esc(name)}</a></li>"

        h = pc.get("handles") or {}
        handles_html = ""
        for label, val in h.items():
            if val:
                handles_html += f"<span class='profile-handle mr-2 mb-2'>{esc(label)}: @{esc(str(val).lstrip('@'))}</span>"

        tier = esc(pc.get("tier", "—"))
        r_geral = esc(pc.get("risco_geral", "—"))

        eixos = pc.get("eixos") or {}
        eixo_rows = ""
        for k, lab in (("concorrencia", "Concorrência"), ("polemicas", "Polêmicas"), ("politica", "Política")):
            cell = eixos.get(k, "—")
            conf = eixos.get(f"{k}_confianca", "")
            extra = f" <span class='text-xs text-slate-400'>({esc(conf)})</span>" if conf else ""
            eixo_rows += f"<tr><td class='py-2 pr-4 font-semibold text-slate-700'>{lab}</td><td class='py-2 text-sm'>{esc(cell)}{extra}</td></tr>"

        narr = pc.get("narrativa") or ""
        narr_html = f"<div class='bio-intro text-sm text-slate-700 whitespace-pre-line'>{esc(narr)}</div>" if narr else ""

        fontes_note = pc.get("fontes_note", "")
        fn_html = f"<p class='text-xs text-slate-500 mt-4 border-t border-slate-200 pt-3'>{esc(fontes_note)}</p>" if fontes_note else ""

        profile_sections += (
            f"<section id='{esc(slug)}' class='card-audit scroll-mt-24'>"
            f"<div class='risk-analysis-box mb-6'>"
            f"<div class='risk-analysis-box__head'>Perfil {i} · {tier}</div>"
            f"<div class='risk-analysis-box__body'>"
            f"<div class='risk-analysis-box__name'>{esc(name)}</div>"
            f"<p class='text-xs font-bold text-slate-600 mb-2'>Risco geral (síntese): <span class='text-calia-navy'>{r_geral}</span></p>"
            f"<div class='handles flex flex-wrap'>{handles_html}</div>"
            f"</div></div>"
            f"{narr_html}"
            f"<div class='deep-dive-box'><h4 class='text-xs font-black uppercase text-calia-navy mb-2'>Três eixos (esta compilação)</h4>"
            f"<table class='w-full'>{eixo_rows}</table></div>"
            f"{fn_html}</section>"
        )

        def clip(s: object, n: int = 160) -> str:
            t = str(s or "—")
            return esc(t if len(t) <= n else t[: n - 1] + "…")

        summary_rows.append(
            [
                f"<strong>{esc(name)}</strong><br><span class='text-xs text-slate-500'>{tier}</span>",
                r_geral,
                clip(eixos.get("concorrencia")),
                clip(eixos.get("polemicas")),
                clip(eixos.get("politica")),
            ]
        )

    sum_table = render_table(
        ["Perfil", "Risco geral", "Concorrência (resumo)", "Polêmicas (resumo)", "Política (resumo)"],
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
    .card-audit {{ background: white; border-radius: 4px; border: 1px solid #e2e8f0; padding: 2.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); margin-bottom: 2.5rem; }}
    .section-header {{ border-left: 6px solid #252525; padding-left: 1.5rem; margin-bottom: 1.5rem; }}
    .profile-handle {{ display: inline-block; margin-top: 0.25rem; padding: 0.35rem 0.75rem; font-size: 0.8125rem; font-weight: 700; color: #252525; background: #f1f5f9; border: 1px solid #cbd5e1; border-left: 3px solid #f9a619; border-radius: 4px; font-family: ui-monospace, monospace; }}
    .toc-link {{ font-size: 0.875rem; font-weight: 600; color: #252525; text-decoration: underline; text-decoration-color: #f9a619; text-underline-offset: 3px; }}
    .source-tag {{ font-size: 9px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }}
    .deep-dive-box {{ background-color: #f1f5f9; border-radius: 4px; padding: 1.25rem; margin-top: 1.25rem; border-left: 4px solid #252525; }}
    .risk-analysis-box {{ margin-top: 0; border-radius: 6px; border: 2px solid #252525; overflow: hidden; }}
    .risk-analysis-box__head {{ background: #252525; color: #f9a619; padding: 0.65rem 1.25rem; font-size: 10px; font-weight: 900; letter-spacing: 0.14em; text-transform: uppercase; }}
    .risk-analysis-box__body {{ background: #f1f5f9; padding: 1.25rem 1.5rem; }}
    .risk-analysis-box__name {{ font-size: 0.9375rem; font-weight: 900; color: #252525; text-transform: uppercase; letter-spacing: 0.04em; }}
    .bio-intro {{ background-color: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; margin-bottom: 1rem; border-radius: 4px; border-left: 4px solid #f9a619; }}
    .toc-list {{ margin: 0; padding: 0; list-style: none; border-left: 2px solid #f9a619; padding-left: 1rem; }}
    .toc-list li {{ margin-top: 0.5rem; }}
  </style>
</head>
<body class="p-4 md:p-10">
  <div id="access-gate" class="fixed inset-0 z-[100] flex items-center justify-center bg-[#252525] p-4">
    <div class="w-full max-w-sm rounded border border-slate-600 bg-white p-8 shadow-2xl">
      <p class="text-xs font-bold uppercase tracking-wider text-calia-navy mb-1">Acesso restrito</p>
      <p class="text-sm text-slate-600 mb-4">Senha: a mesma do dossiê CAIXA de referência (<strong>caixa2026</strong>) ou <strong>embratur2026</strong>.</p>
      <form id="access-form" class="space-y-3">
        <input type="password" id="access-pw" required autocomplete="current-password" class="w-full rounded border border-slate-300 px-3 py-2 text-sm" placeholder="Senha">
        <p id="access-err" class="hidden text-sm font-medium text-red-600"></p>
        <button type="submit" class="w-full rounded-md bg-calia-gold py-3 text-sm font-black uppercase text-calia-navy">Entrar</button>
      </form>
      <p class="mt-6 text-center text-[10px] font-bold uppercase text-slate-500">Calia BI · uso interno</p>
    </div>
  </div>

  <div id="dossier-root" class="hidden max-w-6xl mx-auto space-y-4">
    <header id="topo" class="bg-calia-navy text-white p-10 rounded shadow-lg">
      <p class="text-calia-gold font-bold tracking-widest text-xs uppercase">{client}</p>
      <h1 class="text-3xl md:text-4xl font-black mt-2 uppercase tracking-tight">{title}</h1>
      <p class="text-sm opacity-90 mt-2 font-medium">{subtitle}</p>
      <p class="text-xs opacity-70 mt-4">Snapshot declarado: {snapshot} · HTML gerado em {esc(generated)}</p>
    </header>

    <nav class="card-audit py-8" aria-label="Sumário">
      <div class="section-header"><h2 class="text-lg font-black text-calia-navy uppercase">Neste dossiê</h2></div>
      <ul class="toc-list">
        <li><a class="toc-link" href="#governanca">Governança e limites</a></li>
        <li><a class="toc-link" href="#executiva">Leitura executiva</a></li>
        <li><a class="toc-link" href="#metodo">Metodologia e fontes</a></li>
        <li><a class="toc-link" href="#painéis">Painéis de métricas</a></li>
        <li><a class="toc-link" href="#consolidado">Relatório consolidado (Proposta P)</a></li>
        <li><a class="toc-link" href="#perfis">Perfis (detalhe)</a></li>
        <li><a class="toc-link" href="#matriz">Matriz comparativa</a></li>
        <li><a class="toc-link" href="#repo">Evidências no repositório (Markdown)</a></li>
      </ul>
      <h3 class="mt-8 mb-2 text-[10px] font-black uppercase text-slate-400">Perfis</h3>
      <ul class="toc-list">{toc_items}</ul>
    </nav>

    <section id="governanca" class="card-audit scroll-mt-24 border-l-4 border-calia-crimson">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy uppercase">Governança — sem dados primários proprietários</h2></div>
      {gov_html}
    </section>

    <section id="executiva" class="card-audit scroll-mt-24 bg-gradient-to-b from-white to-slate-50">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy uppercase">Leitura executiva</h2></div>
      <ul class="list-none space-y-2">{exec_html}</ul>
    </section>

    <section id="metodo" class="card-audit scroll-mt-24">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy uppercase">Metodologia e fontes</h2></div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">{meth_cards}</div>
    </section>

    <section id="painéis" class="scroll-mt-24">
      <div class="section-header px-1"><h2 class="text-xl font-black text-calia-navy uppercase">Painéis de métricas (quatro redes)</h2>
      <p class="text-sm text-slate-600 mt-2">Valores são snapshots de terceiros; conferir data no repositório (FONTES).</p></div>
      {panels_html}
    </section>

    <div id="consolidado">{cons_html}</div>

    <section id="perfis" class="scroll-mt-24">
      <div class="section-header"><h2 class="text-2xl font-black text-calia-navy uppercase">Análise por perfil</h2></div>
      {profile_sections}
    </section>

    <section id="matriz" class="card-audit scroll-mt-24">
      <div class="section-header"><h2 class="text-xl font-black text-calia-navy uppercase">Matriz comparativa (resumo)</h2></div>
      {sum_table}
    </section>

    <section id="repo" class="card-audit scroll-mt-24 bg-slate-50">
      <h2 class="text-sm font-black uppercase text-slate-500">Linha de base com URLs</h2>
      <p class="text-sm text-slate-700 mt-2">Toda evidência citável, tabelas de validação Perplexity/OSINT, relatórios externos e checklists permanecem em <code class='bg-white px-1 border rounded'>loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md</code> e <code class='bg-white px-1 border rounded'>METODO_BRAND_SAFETY_LOTERIAS2026.md</code>. Regenerar este HTML após editar <code class='bg-white px-1 border rounded'>data/dossier_loterias2026.yaml</code>.</p>
    </section>

    <footer class="text-center py-8 text-[10px] text-slate-400 font-bold uppercase tracking-widest border-t">
      <a class="toc-link" href="#topo">Voltar ao topo</a> · Calia BI · Always ON Loterias 2026
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
      if (!globalThis.crypto?.subtle) {{
        err.textContent = 'Use HTTPS (ex.: GitHub Pages).';
        err.classList.remove('hidden');
        return;
      }}
      const pw = document.getElementById('access-pw').value.trim();
      try {{
        if (!PASSWORD_SHA256_HEX_SET.has(await sha256Hex(pw))) {{
          err.textContent = 'Senha incorreta.';
          err.classList.remove('hidden');
          return;
        }}
      }} catch {{
        err.textContent = 'Validação indisponível.';
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
