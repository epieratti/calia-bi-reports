# Scripts legado (não usados na entrega atual ao cliente)

O fluxo operacional dos dossiês **Always ON / Brand Safety** no `caixa/` é:

`dossier_*.md` + `dossier_*_panels.yaml` → `build_dossier_completo.py` → HTML → copiar para `caixa/`.

Os ficheiros abaixo eram ou são um **pipeline experimental** com **Apify** e relatório HTML separado. **Apify foi retirado do fluxo** (não funcionou bem). Não configurar `APIFY_TOKEN` para trabalho normal.

| Script | Nota |
|--------|------|
| `collect.py` | Coleta com actors Apify (IG/TT/X). |
| `collect_open_web.py` | Wikipedia, notícias, busca. |
| `classify.py`, `aggregate_profiles.py` | Pós-processamento da coleta. |
| `report_html.py` | Gera `output/dossie-brand-safety-loterias-2026.html` (heurístico). |
| `run_pipeline.py` | Orquestra os passos acima. |

Métricas no dossiê cliente: **Social Blade** (IG/YT), **Upfluence** (TT, dados enviados), **X** (manual na plataforma) — ver `PLAYBOOK_DOSSIES.md`.
