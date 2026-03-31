#!/usr/bin/env python3
"""
Gera dossiê HTML de Brand Safety a partir de data/processed/profile_summary.json.
Saída: output/dossie-brand-safety-loterias-2026.html
"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUT_DIR = ROOT / "output"


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def slug_id(name: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return s or "perfil"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path_json = PROCESSED / "profile_summary.json"
    if not path_json.is_file():
        data = {
            "campaign": "Always ON Loterias 2026",
            "profiles": [],
            "note": "Execute o pipeline após definir APIFY_TOKEN.",
        }
    else:
        with open(path_json, encoding="utf-8") as f:
            data = json.load(f)

    campaign = esc(data.get("campaign", "Always ON Loterias 2026"))
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    profiles = data.get("profiles") or []

    rows_html = []
    for p in profiles:
        r = p.get("risco") or {}
        rows_html.append(
            "<tr>"
            f"<td class='font-semibold'>{esc(p.get('name'))}</td>"
            f"<td class='text-center'>{esc(p.get('posts_classificados', 0))}</td>"
            f"<td class='text-center'>{esc(r.get('concorrencia', '—'))}</td>"
            f"<td class='text-center'>{esc(r.get('polemicas', '—'))}</td>"
            f"<td class='text-center'>{esc(r.get('politica', '—'))}</td>"
            f"<td>{esc(p.get('nivel_heuristico', ''))}</td>"
            "</tr>"
        )

    sections = []
    for p in profiles:
        name = esc(p.get("name"))
        terms = p.get("termos_detectados") or {}
        ev = p.get("evidencias") or {}
        blocks = []
        for axis, label in (
            ("concorrencia", "Concorrência (loterias / apostas / jogos)"),
            ("polemicas", "Polêmicas / cancelamento"),
            ("politica", "Política / pautas sensíveis"),
        ):
            ts = terms.get(axis) or []
            items = ev.get(axis) or []
            if not ts and not items:
                blocks.append(f"<p class='text-sm text-slate-500'>Sem match heurístico em <strong>{esc(label)}</strong>.</p>")
                continue
            ul_terms = "<ul class='list-disc pl-5 text-sm'>" + "".join(f"<li>{esc(t)}</li>" for t in ts) + "</ul>"
            ul_ev = ""
            if items:
                lis = []
                for it in items:
                    u = esc(it.get("url") or "")
                    pl = esc(it.get("platform") or "")
                    sm = esc(it.get("sample") or "")
                    lis.append(
                        f"<li class='mb-2'><span class='text-xs uppercase text-slate-400'>{pl}</span> "
                        f"<a class='text-amber-700 underline' href='{u}' target='_blank' rel='noopener'>{u or '—'}</a>"
                        f"<div class='text-xs text-slate-600 mt-1'>{sm}</div></li>"
                    )
                ul_ev = "<p class='text-xs font-bold uppercase tracking-wide text-slate-500 mt-3'>Amostras</p><ul class='text-sm'>" + "".join(lis) + "</ul>"
            blocks.append(
                f"<div class='mb-4'><h4 class='text-sm font-black uppercase tracking-wide text-slate-800'>{esc(label)}</h4>"
                f"{ul_terms}{ul_ev}</div>"
            )
        sections.append(
            f"<section class='card mb-10 scroll-mt-8' id='{esc(slug_id(p.get('name', '')))}'>"
            f"<h3 class='text-lg font-black uppercase border-b border-slate-200 pb-2 mb-4'>{name}</h3>"
            f"<p class='text-sm text-slate-600 mb-4'>Posts analisados (após coleta): <strong>{esc(p.get('posts_classificados', 0))}</strong></p>"
            + "".join(blocks)
            + "</section>"
        )

    note = data.get("note")
    note_block = ""
    if note:
        note_block = f"<div class='rounded border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900 mb-8'>{esc(note)}</div>"

    doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Brand Safety — {campaign}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ font-family: ui-sans-serif, system-ui, sans-serif; }}
    .card {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
  </style>
</head>
<body class="bg-slate-50 text-slate-800 p-6 md:p-12">
  <div class="max-w-5xl mx-auto">
    <header class="mb-10 rounded-lg bg-slate-900 text-white p-8">
      <p class="text-amber-400 text-xs font-bold uppercase tracking-widest">Brand Safety · Auditoria de conteúdo</p>
      <h1 class="text-3xl font-black mt-2 uppercase tracking-tight">{campaign}</h1>
      <p class="text-sm opacity-90 mt-2">Critérios: concorrência (loterias/apostas), polêmicas, política — classificação heurística por palavras-chave. Revisão humana recomendada.</p>
      <p class="text-xs opacity-70 mt-4">Gerado em {esc(generated)} · Fontes: Instagram, TikTok, YouTube, X (quando token Apify disponível)</p>
    </header>
    {note_block}
    <section class="card mb-10">
      <h2 class="text-sm font-black uppercase tracking-widest text-slate-500 mb-4">Matriz de risco (resumo)</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="border-b border-slate-200 text-left text-xs uppercase text-slate-500">
              <th class="py-2 pr-4">Perfil</th>
              <th class="py-2 pr-4 text-center">Posts</th>
              <th class="py-2 pr-4 text-center">Concorr.</th>
              <th class="py-2 pr-4 text-center">Polêm.</th>
              <th class="py-2 pr-4 text-center">Polít.</th>
              <th class="py-2">Nível (heur.)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            {"".join(rows_html) if rows_html else "<tr><td colspan='6' class='py-6 text-slate-500'>Nenhum dado agregado ainda. Rode a coleta com APIFY_TOKEN.</td></tr>"}
          </tbody>
        </table>
      </div>
    </section>
    <section class="mb-6">
      <h2 class="text-sm font-black uppercase tracking-widest text-slate-500 mb-4">Detalhe por perfil</h2>
      {"".join(sections) if sections else "<p class='text-slate-500'>Sem perfis no resumo.</p>"}
    </section>
    <footer class="text-xs text-slate-400 border-t border-slate-200 pt-6">
      Dados brutos: <code class='bg-slate-100 px-1 rounded'>loterias2026/data/raw/*.jsonl</code> · CSV: <code class='bg-slate-100 px-1 rounded'>data/processed/classified_posts.csv</code>
    </footer>
  </div>
</body>
</html>
"""

    out_path = OUT_DIR / "dossie-brand-safety-loterias-2026.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(str(out_path.relative_to(ROOT)))


if __name__ == "__main__":
    main()
