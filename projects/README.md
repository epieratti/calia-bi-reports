# Projetos (fonte editável)

Cada entrega tem pasta em `projects/<cliente>/<linha?>/<slug>/` com **`manifest.yaml`** (contrato de build e publicação).

**Não** publicar esta árvore no GitHub Pages — o HTML canônico fica em `caixa/`, `caixa/loterias/`, `febraban/` ou `embratur/`.

## Layout

```
projects/
├── _template/                              # par mínimo modo B
├── caixa/
│   └── loterias/
│       ├── always-on-20260401/             # referência — 13 perfis
│       ├── always-on-20260406/             # 8 perfis
│       └── always-on-20260504/             # 3 perfis
├── febraban/concorrencia-creators-20260427/
└── embratur/auditoria-20260323/
```

## Conteúdo típico de um projeto modo B

| Arquivo | Papel |
|---------|--------|
| `manifest.yaml` | `source.md`, `source.panels`, `publish.dest`, `variant` |
| `data/dossier_*.md` | Narrativa, perfis (`## Nome`), front matter |
| `data/dossier_*_panels.yaml` | Métricas IG/TT/YT/X |
| `research/` | Notas de pesquisa (opcional) |
| `.build/` | HTML de staging (gitignored) |

## Comandos

```bash
make dossie-build PROJECT=caixa/loterias/always-on-20260401
make dossie-qa PROJECT=caixa/loterias/always-on-20260401
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401
```

Alternativa com paths explícitos: `make dossie-entregar MD=projects/.../dossier_x.md DEST=caixa/loterias`

## Novo projeto

1. Copiar `projects/_template/` ou rodar `engine/cli/new_creator_dossier.py`
2. Criar `manifest.yaml` (copiar de um lote existente)
3. Seguir `docs/tutorials/PRIMEIRO_DIA.md`

Ver também: [`docs/reference/INVENTARIO_DOSSIES.md`](../docs/reference/INVENTARIO_DOSSIES.md) · [`engine/README.md`](../engine/README.md)
