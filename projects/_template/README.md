# Template — modo B

Par mínimo para novos dossiês:

- `dossier_TEMPLATE.md` — modelo completo (copiar e renomear)
- `dossier_minimo_exemplo.md` + `dossier_minimo_exemplo_panels.yaml` — exemplo com 1 perfil

## Novo lote

```bash
python3 engine/cli/new_creator_dossier.py meu_slug \
  --output-dir projects/caixa/loterias/meu-lote/data
```

## Teste local

```bash
make build-dossier-minimo-preview
make validate-dossier-minimo
```

Saída de preview: `projects/_template/preview.html` (gitignored)
