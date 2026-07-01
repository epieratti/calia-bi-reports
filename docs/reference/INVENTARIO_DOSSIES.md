# Inventário de dossiês publicados

Mapa **canônico** de cada artefato no GitHub Pages. Atualizar ao publicar ou migrar um dossiê.

**Modos:** **A** = HTML editado diretamente. **B** = `dossier_*.md` + `_panels.yaml` → build → HTML.

**Base URL:** `https://epieratti.github.io/calia-bi-reports/`

---

## Embratur

| Arquivo | Modo | Fonte editável | Senha | Entrega |
|---------|------|----------------|-------|---------|
| [`embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html`](../embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html) | **A** | O próprio HTML | `embratur2026` | 2026-03-23 |

---

## Febraban

| Arquivo | Modo | Fonte editável | Senha | Entrega |
|---------|------|----------------|-------|---------|
| [`febraban/20260427-dossie-febraban-concorrencia-creators-2026.html`](../febraban/20260427-dossie-febraban-concorrencia-creators-2026.html) | **B** | `projects/febraban/concorrencia-creators-20260427/data/` | `febraban2026` | 2026-04-27 |

**Redirect legado:** [`caixa/20260427-…`](../caixa/20260427-dossie-febraban-concorrencia-creators-2026.html) → `febraban/`.

---

## Caixa — institucional

| Arquivo | Modo | Fonte | Senha | Entrega |
|---------|------|-------|-------|---------|
| [`caixa/20260326-…`](../caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html) | **A** | HTML | `caixa2026` / `embratur2026` | 2026-03-26 |
| [`caixa/20260506-…`](../caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html) | **A** | HTML | `caixa2026` / `embratur2026` | 2026-05-06 |

PDF Isadora: [`caixa/20260506-….pdf`](../caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.pdf)

---

## Caixa — Loterias (`caixa/loterias/`)

| Arquivo | Modo | Fonte editável | Senha | Entrega |
|---------|------|----------------|-------|---------|
| [`loterias/20260401-…`](../caixa/loterias/20260401-dossie-squad-always-on-loterias-2026.html) | **B** | `projects/caixa/loterias/always-on-20260401/data/` | `caixa2026` | 2026-04-01 (13) |
| [`loterias/20260406-…`](../caixa/loterias/20260406-dossie-squad-always-on-loterias-2026.html) | **B** | `projects/caixa/loterias/always-on-20260406/data/` | `caixa2026` | 2026-04-06 (8) |
| [`loterias/20260504-…`](../caixa/loterias/20260504-dossie-squad-always-on-loterias-2026.html) | **B** | `projects/caixa/loterias/always-on-20260504/data/` | `caixa2026` | 2026-05-04 (3) |
| [`loterias/20260511-…`](../caixa/loterias/20260511-dossie-squad-always-on-loterias-2026.html) | **A** | O próprio HTML (consolidado 27 perfis) | `caixa2026` | 2026-05-11 |
| [`loterias/20260514-…`](../caixa/loterias/20260514-dossie-pulga-oncoto-caixa-2026.html) | **A** | HTML | `caixa2026` | 2026-05-14 |
| [`loterias/20260515-…`](../caixa/loterias/20260515-dossie-rodolfo-macedo-foiorodolfo-caixa-2026.html) | **A** | HTML | `caixa2026` | 2026-05-15 |

Redirects na raiz de `caixa/` apontam para `caixa/loterias/` (URLs antigas).

**Build modo B:** `make dossie-entregar PROJECT=caixa/loterias/always-on-20260401` → publica em `caixa/loterias/`.

---

## Regras de edição

| Modo | O que editar | Build |
|------|--------------|-------|
| **A** | HTML em `caixa/`, `caixa/loterias/`, `febraban/`, `embratur/` | — |
| **B** | `projects/…/data/*.md` + `*_panels.yaml` | `make dossie-entregar PROJECT=…` |

QA: `python3 engine/qa/check_html_leakage.py caixa febraban embratur`

---

## Índices

| Pasta | Índice |
|-------|--------|
| Caixa | [`caixa/index.html`](../caixa/index.html) |
| Caixa Loterias | [`caixa/loterias/index.html`](../caixa/loterias/index.html) |
| Febraban | [`febraban/index.html`](../febraban/index.html) |
