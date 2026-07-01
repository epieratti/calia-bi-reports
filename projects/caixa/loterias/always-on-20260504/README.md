# Always ON Loterias 2026 — squad 3 perfis (lote 04/05/2026)

Mesmo modelo dos lotes de referência (`always-on-20260401`, `always-on-20260406`).

## Build e publicação

```bash
make dossie-entregar PROJECT=caixa/loterias/always-on-20260504
python3 engine/qa/validate_source.py projects/caixa/loterias/always-on-20260504/data/dossier_loterias2026.md
```

Fonte: `data/dossier_loterias2026.md` + `data/dossier_loterias2026_panels.yaml`

**Publicado em:** `caixa/loterias/20260504-dossie-squad-always-on-loterias-2026.html` · senha `caixa2026`

## Pesquisa deste lote

- `research/PUBLICO_PERCEBIDO_LOTE3_AON_LOTERIAS_202605.md` — leitura qualitativa de público percebido

## Referência

- Lote 13 perfis: `projects/caixa/loterias/always-on-20260401/README.md`
- Índice Caixa: `caixa/README.md`
