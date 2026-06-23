# `tools/` — compartilhado por todos os dossiês

- **Nome do `.html` (padrão playbook):** `dossier_html_filename.py` — `python3 tools/dossier_html_filename.py --md caminho/dossier_x.md` (opcional `--date YYYYMMDD`, `--suffix rev2`)
- **Entrega em um comando:** `dossier_publish.py` — valida → links → build → grava em `DEST` com nome automático → vazamento na pasta cliente  
  `python3 tools/dossier_publish.py --md loterias2026/data/dossier_loterias2026.md --dest caixa/loterias`  
  Atalho: `make dossie-entregar MD=... DEST=...` e `make dossie-filename MD=...` (ver `make help`).
- **PDF (HTML → PDF):** metodologia **[`docs/METODO_PDF_DOSSIE.md`](../docs/METODO_PDF_DOSSIE.md)** (fluxo Caixa Isadora: Playwright, servidor HTTP na **raiz** do repo, `../assets`, Chart.js com `--post-unlock-wait`, **`resize` após `emulate_media(print)`**). Script: **`dossier_export_pdf.py`** — `pip install -r tools/requirements-pdf.txt && playwright install chromium`. Senha: `--password` ou `DOSSIER_PDF_PASSWORD`; **`--skip-gate`** só uso interno. Opcional: **`--landscape`**, **`--margin-tight`**. `make dossie-pdf` (opcional `SKIP_GATE=1` `POST_UNLOCK_WAIT=5` `PDF_LANDSCAPE=1` `PDF_MARGIN_TIGHT=1`). Governança: [`docs/GOVERNANCA_ENTREGA.md`](../docs/GOVERNANCA_ENTREGA.md).
- **HTML modo B:** `dossier_render.py`, `md_dossier_source.py`, `dossier_plain.py`, `validate_dossier_source.py` (`--hints`, `--strict-hints`), `check_dossier_links.py`
- **HTML publicado (anti-vazamento):** `check_client_html_leakage.py` — `python3 tools/check_client_html_leakage.py caixa embratur febraban`
- **Artefato GitHub Pages (local):** `prepare_pages_artifact.sh` — `bash tools/prepare_pages_artifact.sh` → `_site/`
- **OSINT (pip):** `requirements-osint.txt` — `pip install -r tools/requirements-osint.txt` na raiz do repositório
- **Proxy Trends + Wikipedia:** `penetracao_mercados.py`, `requirements-penetracao.txt`, modelo `penetracao_entities_example.json`

Guia do agente (curto): **`PLAYBOOK_AGENTES.md`**. Referência completa: **`PLAYBOOK_DOSSIES.md`** (Toolbox, Coleta de dados, Mercado).
