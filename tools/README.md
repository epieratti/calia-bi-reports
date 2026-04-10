# `tools/` — compartilhado por todos os dossiês

- **Nome do `.html` (padrão playbook):** `dossier_html_filename.py` — `python3 tools/dossier_html_filename.py --md caminho/dossier_x.md` (opcional `--date YYYYMMDD`, `--suffix rev2`)
- **Entrega em um comando:** `dossier_publish.py` — valida → links → build → grava em `DEST` com nome automático → vazamento na pasta cliente  
  `python3 tools/dossier_publish.py --md loterias2026/data/dossier_loterias2026.md --dest caixa/loterias`  
  Atalho: `make dossie-entregar MD=... DEST=...` e `make dossie-filename MD=...` (ver `make help`).
- **HTML modo B:** `dossier_render.py`, `md_dossier_source.py`, `dossier_plain.py`, `validate_dossier_source.py` (`--hints`, `--strict-hints`), `check_dossier_links.py`
- **HTML publicado (anti-vazamento):** `check_client_html_leakage.py` — `python3 tools/check_client_html_leakage.py caixa embratur`
- **OSINT (pip):** `requirements-osint.txt` — `pip install -r tools/requirements-osint.txt` na raiz do repositório
- **Proxy Trends + Wikipedia:** `penetracao_mercados.py`, `requirements-penetracao.txt`, modelo `penetracao_entities_example.json`

Guia do agente (curto): **`PLAYBOOK_AGENTES.md`**. Referência completa: **`PLAYBOOK_DOSSIES.md`** (Toolbox, Coleta de dados, Mercado).
