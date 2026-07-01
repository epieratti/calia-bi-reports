# Projetos (fonte editável)

Cada entrega tem pasta em `projects/<cliente>/<linha?>/<slug>/` com `manifest.yaml`.

## Caixa

```
projects/caixa/
├── institucional/     # auditorias, cartão — HTML em caixa/
└── loterias/          # Always ON — HTML em caixa/loterias/
```

## Outros clientes

- `projects/febraban/concorrencia-creators-20260427/`
- `projects/embratur/auditoria-20260323/`

## Template

- `projects/_template/` — par mínimo modo B + `dossier_TEMPLATE.md`

## Build

```bash
make dossie-build PROJECT=caixa/loterias/always-on-20260401
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401
```

Staging HTML: `projects/.../.build/` (gitignored). **Canônico publicado:** `caixa/`, `febraban/`, `embratur/`.
