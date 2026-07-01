# Relatórios Caixa

Pasta de **HTML publicados** do cliente Caixa no GitHub Pages: [índice `caixa/`](https://epieratti.github.io/calia-bi-reports/caixa/).

## Linhas de entrega

| Linha | Pasta publicada | Conteúdo |
|-------|-----------------|----------|
| **Institucional** | `caixa/` (raiz) | Auditorias, cartão, temas gerais |
| **Loterias / Always ON** | `caixa/loterias/` | Squads, creators, Quina, brand safety Loterias |

Arquivos na raiz de `caixa/` com redirect (`meta refresh`) apontam para `caixa/loterias/` — URLs canônicas na subpasta.

## Dossiês publicados

### Institucional (`caixa/`)

- `20260326-dossie-auditoria-personalidades-caixa-2026.html` — senha `caixa2026` ou `embratur2026`
- `20260506-dossie-isadora-cruz-cartao-caixa-2026.html` — senha `caixa2026` ou `embratur2026`

### Loterias (`caixa/loterias/`)

- Squads Always ON: `20260401`, `20260406`, `20260504`, `20260511`
- One-offs: `20260514` (Pulga), `20260515` (Rodolfo)
- Senha: `caixa2026`

Índice: [`caixa/loterias/index.html`](loterias/index.html)

## Fonte editável (modo B)

| HTML publicado | Projeto fonte |
|----------------|---------------|
| `loterias/20260401-…` | `projects/caixa/loterias/always-on-20260401/data/` |
| `loterias/20260406-…` | `projects/caixa/loterias/always-on-20260406/data/` |
| `loterias/20260504-…` | `projects/caixa/loterias/always-on-20260504/data/` |

Build e publicação:

```bash
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401
# ou
make dossie-entregar MD=projects/caixa/loterias/always-on-20260401/data/dossier_loterias2026.md DEST=caixa/loterias
```

Template novo lote: `projects/_template/` · `python3 engine/cli/new_creator_dossier.py SLUG --output-dir projects/.../data`

## Redirect legado

- `caixa/20260427-dossie-febraban-…` → `febraban/` (cliente Febraban)
