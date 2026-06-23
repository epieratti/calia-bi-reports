# Always ON Loterias 2026 — consolidado 11/05/2026

Dossiê **único** com **27 creators** (13 + 8 + 3 dos lotes anteriores + 3 do lote 3 mai/2026).

## Fonte editável

| Arquivo | Papel |
|---------|--------|
| `data/lote3_profiles_fragment.md` | Perfis novos (Raquel Real, Morgana Camila, Paulo Victor Freitas) |
| `data/dossier_loterias2026.md` | **Gerado** — merge dos lotes 20260401, 20260406, 20260504 + lote 3 |
| `research/SOCIAL_BLADE_SQUAD_LOTE3_20260511.md` | Notas de coleta Social Blade / Upfluence (lote 3) |

Regenerar o `.md` consolidado:

```bash
python3 tools/merge_loterias_consolidated_dossier.py
```

## Build HTML

O layout consolidado (métricas por data de referência, coluna «Loterias 18+» herdada) usa **`scripts/build_consolidated.py`** — merge de seções HTML dos artefatos publicados + bloco lote 3.

```bash
make build-dossier-consolidado-20260511
```

Saída: `output/20260511-dossie-squad-always-on-loterias-2026.html`. Para publicar em `caixa/`, use `--publish-to-caixa` após validar o diff (o HTML no ar passou por patches editoriais).

**Senha:** `caixa2026` (SHA-256 no front matter do `.md` consolidado).

## Lotes de origem

- [`../../data/dossier_loterias2026.md`](../../data/dossier_loterias2026.md) — squad 13
- [`../20260406/data/dossier_loterias2026.md`](../20260406/data/dossier_loterias2026.md) — squad 8
- [`../20260504/data/dossier_loterias2026.md`](../20260504/data/dossier_loterias2026.md) — squad 3 (abr/mai)

## Notas

- O consolidado **não** entra no `make check-dossier-publish-sync` padrão (layout diferente do motor modo B simples).
- Patches históricos de edição editorial: `tools/archive/20260511/`.
