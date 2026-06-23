# Lotes Always ON Loterias 2026

Pastas **congeladas** por data de entrega. Cada lote tem `data/` (`.md` + `_panels.yaml`), `output/` (staging do build) e, quando houver, `research/` e `scripts/` auxiliares.

| Pasta | Entrega | Perfis | Build |
|-------|---------|--------|-------|
| [`20260406/`](20260406/) | 2026-04-06 | 8 | `make build-dossier-squad-8` |
| [`20260504/`](20260504/) | 2026-05-04 | 3 | `make build-dossier-squad-20260504` |
| [`20260511/`](20260511/) | 2026-05-11 | 27 (consolidado) | `make build-dossier-consolidado-20260511` |

**Squad 13 (2026-04-01):** fonte em [`../data/dossier_loterias2026.md`](../data/dossier_loterias2026.md) — `make build-dossier-squad-13`.

**Motor único:** `python3 loterias2026/scripts/build_dossier_completo.py --project-root loterias2026/lotes/YYYYMMDD`

Pastas antigas na raiz (`loterias2026-20260406/`, etc.) mantêm só README de redirecionamento.
