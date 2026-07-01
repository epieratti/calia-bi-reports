# Motor de dossiês (`engine/`)

Motor Python compartilhado por todos os projetos modo **B**. Não publicar esta pasta no GitHub Pages.

## Estrutura

| Pasta | Módulos | Função |
|-------|---------|--------|
| `core/` | `dossier_render.py`, `md_dossier_source.py`, `dossier_plain.py` | Parse `.md` + YAML → HTML |
| `cli/` | `build_dossier.py`, `publish_dossier.py`, `export_pdf.py`, `new_creator_dossier.py`, `html_filename.py` | Entrada de linha de comando |
| `qa/` | `validate_source.py`, `check_links.py`, `check_html_leakage.py` | Validação estrutural e anti-vazamento |
| `research/` | `penetracao_mercados.py` | Proxy Trends + Wikipedia (genérico) |
| `requirements/` | `pdf.txt`, `osint.txt`, `penetracao.txt` | Dependências pip por tarefa |

## Comandos

```bash
# Build a partir do manifest do projeto
python3 engine/cli/build_dossier.py --project caixa/loterias/always-on-20260401

# Pipeline completo até a pasta Pages
python3 engine/cli/publish_dossier.py --project caixa/loterias/always-on-20260401
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401

# Novo par .md + _panels.yaml
python3 engine/cli/new_creator_dossier.py SEU_SLUG --output-dir projects/.../data

# QA
python3 engine/qa/validate_source.py --hints projects/.../dossier_*.md
python3 engine/qa/check_links.py projects/.../dossier_*.md
python3 engine/qa/check_html_leakage.py caixa febraban embratur

# PDF (ver docs/how-to/METODO_PDF_DOSSIE.md)
python3 engine/cli/export_pdf.py --html caixa/....html --out caixa/....pdf
```

## Dependências

```bash
pip install pyyaml                    # obrigatório para build/validate
pip install -r engine/requirements/pdf.txt && playwright install chromium
pip install -r engine/requirements/osint.txt      # OSINT opcional
pip install -r engine/requirements/penetracao.txt  # Trends/Wikipedia
```

Atalhos na raiz: `make help`
