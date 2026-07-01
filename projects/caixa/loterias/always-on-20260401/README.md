# Always ON Loterias 2026 — squad 13 perfis (lote 01/04/2026)

Referência do **modo B** (`PLAYBOOK_DOSSIES.md`): fonte `.md` + `engine/cli/build_dossier.py`.

## Comandos

```bash
# Na raiz do repo
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401
make validate-dossier-squad-13
```

Novo lote: `python3 engine/cli/new_creator_dossier.py SEU_SLUG --output-dir projects/.../data`

## Fonte

| Arquivo | Papel |
|---------|--------|
| `data/dossier_loterias2026.md` | Narrativa + perfis (`## Nome`) |
| `data/dossier_loterias2026_panels.yaml` | Métricas IG/TT/YT/X |
| `data/influencers.yaml` | Handles do squad |
| `manifest.yaml` | Contrato de publicação |

Template novo dossiê: `projects/_template/dossier_TEMPLATE.md`

## Pesquisa deste lote

| Tema | Arquivo |
|------|---------|
| Descoberta de @ | `methods/discovery/METODO_DESCOBERTA_PERFIS.md` |
| Brand safety | `methods/brand-safety/METODO_BRAND_SAFETY.md` |
| Evidências (exemplo) | `methods/brand-safety/FONTES_BRAND_SAFETY_LOTERIAS2026.md` |
| OSINT (logs) | `research/osint_runs/` |

## Publicação

- **Canônico:** `caixa/loterias/20260401-dossie-squad-always-on-loterias-2026.html`
- **Senha:** `caixa2026`
- **URL:** https://epieratti.github.io/calia-bi-reports/caixa/loterias/20260401-dossie-squad-always-on-loterias-2026.html

Motor: `engine/core/dossier_render.py`, `engine/core/md_dossier_source.py`
