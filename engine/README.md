# Motor de dossiês (`engine/`)

| Pasta | Conteúdo |
|-------|----------|
| `core/` | `dossier_render.py`, `md_dossier_source.py`, `dossier_plain.py` |
| `cli/` | `build_dossier.py`, `publish_dossier.py`, `export_pdf.py`, `new_creator_dossier.py` |
| `qa/` | `validate_source.py`, `check_links.py`, `check_html_leakage.py` |
| `research/` | `penetracao_mercados.py` |
| `requirements/` | `pdf.txt`, `osint.txt`, `penetracao.txt` |

## Comandos

```bash
python3 engine/cli/build_dossier.py --project caixa/loterias/always-on-20260401
python3 engine/cli/publish_dossier.py --project caixa/loterias/always-on-20260401
python3 engine/qa/validate_source.py projects/.../dossier_*.md
python3 engine/qa/check_html_leakage.py caixa febraban embratur
```

Atalhos: `make help`
