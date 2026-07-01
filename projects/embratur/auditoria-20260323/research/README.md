# Pesquisa — Embratur auditoria 2026

Artefatos de **penetração de mercado** (Google Trends + Wikipedia proxy).

| Arquivo | Conteúdo |
|---------|----------|
| `penetracao_entities_embratur_2026.json` | Entidades pesquisadas |
| `penetracao_trends_wiki_2026.csv` / `.json` | Saída do script |

## Rodar de novo

```bash
pip install -r engine/requirements/penetracao.txt
python3 engine/research/penetracao_mercados.py \
  --entities-json projects/embratur/auditoria-20260323/research/penetracao_entities_embratur_2026.json \
  --output-prefix projects/embratur/auditoria-20260323/research/penetracao_trends_wiki_2026
```

HTML publicado: `embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html`
