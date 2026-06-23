# Inventário de dossiês publicados

Mapa **canônico** de cada artefato no GitHub Pages: URL, modo de produção, fonte editável e senha. Atualizar ao publicar ou migrar um dossiê.

**Modos:** **A** = HTML editado diretamente (fonte é o próprio `.html`). **B** = `dossier_*.md` + `dossier_*_panels.yaml` → build → HTML. **Híbrido** = HTML gerado por scripts pontuais; migrar para **B** (ver roadmap Épico 4).

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
| [`febraban/20260427-dossie-febraban-concorrencia-creators-2026.html`](../febraban/20260427-dossie-febraban-concorrencia-creators-2026.html) | **B** | `loterias2026/data/dossier_febraban_concorrencia_2026.md` + `_panels.yaml` | `febraban2026` | 2026-04-27 |

**Redirect legado:** [`caixa/20260427-dossie-febraban-concorrencia-creators-2026.html`](../caixa/20260427-dossie-febraban-concorrencia-creators-2026.html) → pasta `febraban/`.

---

## Caixa — geral (não Loterias squad)

| Arquivo | Modo | Fonte editável | Senha | Entrega |
|---------|------|----------------|-------|---------|
| [`caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html`](../caixa/20260326-dossie-auditoria-personalidades-caixa-2026.html) | **A** | O próprio HTML | `caixa2026` ou `embratur2026` | 2026-03-26 |
| [`caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html`](../caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html) | **A** | O próprio HTML | `caixa2026` ou `embratur2026` | 2026-05-06 |
| [`caixa/20260514-dossie-pulga-oncoto-caixa-2026.html`](../caixa/20260514-dossie-pulga-oncoto-caixa-2026.html) | **A** | O próprio HTML | `caixa2026` ou `embratur2026` | 2026-05-14 |
| [`caixa/20260515-dossie-rodolfo-macedo-foiorodolfo-caixa-2026.html`](../caixa/20260515-dossie-rodolfo-macedo-foiorodolfo-caixa-2026.html) | **A** | O próprio HTML | `caixa2026` ou `embratur2026` | 2026-05-15 |

### PDF (Caixa geral)

| HTML | PDF versionado | Notas |
|------|----------------|-------|
| Isadora (20260506) | **Não** (pendente) | Regenerar: `make dossie-pdf HTML=caixa/20260506-….html OUT=caixa/20260506-….pdf` — ver [`METODO_PDF_DOSSIE.md`](METODO_PDF_DOSSIE.md) |
| Rodolfo (20260515) | **Não** (pendente) | Idem |

Enquanto o PDF não estiver no repo, o [`caixa/index.html`](../caixa/index.html) lista só o HTML (sem link PDF quebrado).

---

## Caixa — Always ON Loterias 2026

| Arquivo | Modo | Fonte editável | Senha | Entrega |
|---------|------|----------------|-------|---------|
| [`caixa/20260401-dossie-squad-always-on-loterias-2026.html`](../caixa/20260401-dossie-squad-always-on-loterias-2026.html) | **B** | `loterias2026/data/dossier_loterias2026.md` + `_panels.yaml` | `caixa2026` | 2026-04-01 (13 perfis) |
| [`caixa/20260406-dossie-squad-always-on-loterias-2026.html`](../caixa/20260406-dossie-squad-always-on-loterias-2026.html) | **B** | `loterias2026-20260406/data/dossier_loterias2026.md` + `_panels.yaml` | `caixa2026` | 2026-04-06 (8 perfis) |
| [`caixa/20260504-dossie-squad-always-on-loterias-2026.html`](../caixa/20260504-dossie-squad-always-on-loterias-2026.html) | **B** | `loterias2026-20260504/data/dossier_loterias2026.md` + `_panels.yaml` | `caixa2026` | 2026-05-04 (3 perfis) |
| [`caixa/20260511-dossie-squad-always-on-loterias-2026.html`](../caixa/20260511-dossie-squad-always-on-loterias-2026.html) | **Híbrido** ⚠️ | `tools/build_squad_always_on_consolidated_mai2026.py` + patches em `tools/` — **sem** `dossier_*.md` | `caixa2026` | 2026-05-11 (27 perfis) |

**Staging de build (modo B):** HTML gerado em `loterias2026*/output/` → copiar para `caixa/` antes do push. O artefato em `caixa/` é o servido pelo Pages.

**Débito técnico:** migrar 20260511 para modo **B** (Épico 4 do roadmap de organização).

---

## Regras de edição

| Modo | O que editar | Build |
|------|--------------|-------|
| **A** | O `.html` em `caixa/` ou `embratur/` | Não há |
| **B** | `.md` + `_panels.yaml` na pasta do lote | `make build-dossier-squad-*` ou `make dossie-entregar` |
| **Híbrido** | Evitar edição manual no HTML; priorizar migração para **B** | Scripts em `tools/` (legado transitório) |

Antes de publicar HTML novo: `python3 tools/check_client_html_leakage.py caixa embratur febraban`.

---

## Índices no site

| Pasta | Índice |
|-------|--------|
| Raiz | [`index.html`](../index.html) → redirect Embratur |
| Caixa | [`caixa/index.html`](../caixa/index.html) |
| Febraban | [`febraban/index.html`](../febraban/index.html) |

Ver também: [`caixa/README.md`](../caixa/README.md), [`febraban/README.md`](../febraban/README.md), [`docs/INDICE_METODOS.md`](INDICE_METODOS.md).
