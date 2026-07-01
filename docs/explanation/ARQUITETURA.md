# Arquitetura do repositório — blueprint (estado-alvo)

Documento de **planejamento**. Nenhuma migração descrita aqui foi executada automaticamente — serve como contrato para as fases de reorganização.

**Última revisão:** 2026-07-01 — inclusão da divisão explícita **Caixa institucional × Caixa Loterias**.

---

## 1. Visão geral

`calia-bi-reports` é um **monorepo** de dossiês HTML publicados via GitHub Pages. Quatro zonas com fronteiras claras:

| Zona | Caminho | Publicado no Pages? |
|------|---------|---------------------|
| **Superfície** | `caixa/`, `febraban/`, `embratur/`, `assets/`, `index.html` | Sim |
| **Projetos (fonte)** | `projects/` | Não |
| **Motor** | `engine/` | Não |
| **Métodos** | `methods/` | Não |

**Princípio central:** HTML em `caixa/` (ou subpastas) é o artefato servido; `projects/` é onde se edita (modo B). Modo A edita o HTML diretamente na superfície.

---

## 2. Clientes e subdomínios

### 2.1 Mapa de clientes

| Cliente | Superfície publicada | Linhas de entrega |
|---------|---------------------|-------------------|
| **Caixa** | `caixa/` | **institucional** + **loterias** (ver §3) |
| **Febraban** | `febraban/` | due diligence / concorrência creators |
| **Embratur** | `embratur/` | auditoria de personalidades |

Febraban **não** fica em `caixa/` (exceto redirect legado até tráfego zero).

### 2.2 Caixa — duas linhas explícitas

Hoje os dois tipos coexistem na **raiz** de `caixa/`. O estado-alvo separa por subpasta na superfície **e** por namespace em `projects/`.

| Linha | O que é | Exemplos atuais | Destino na superfície |
|-------|---------|-----------------|----------------------|
| **institucional** | Auditorias, cartão, produtos Caixa, temas gerais **sem** campanha Loterias / Always ON | `20260326` (auditoria personalidades), `20260506` (Isadora / cartão) | `caixa/` (raiz) |
| **loterias** | Always ON Loterias 2026, squads, creators, Quina, brand safety da linha Loterias | `20260401`–`20260511` (squads), `20260514` (Pulga), `20260515` (Rodolfo) | `caixa/loterias/` |

**Nota:** `caixa/index.html` hoje lista Pulga e Rodolfo em «Caixa — geral»; no estado-alvo passam para **loterias** (são entregas da linha Loterias).

---

## 3. Superfície Caixa — estrutura alvo

```
caixa/
├── index.html                    # índice com duas seções + link para loterias/
├── README.md
│
├── 20260326-dossie-auditoria-personalidades-caixa-2026.html
├── 20260506-dossie-isadora-cruz-cartao-caixa-2026.html
│   … futuros dossiês institucionais …
│
└── loterias/
    ├── index.html                # índice só da linha Loterias
    ├── 20260401-dossie-squad-always-on-loterias-2026.html
    ├── 20260406-dossie-squad-always-on-loterias-2026.html
    ├── 20260504-dossie-squad-always-on-loterias-2026.html
    ├── 20260511-dossie-squad-always-on-loterias-2026.html
    ├── 20260514-dossie-pulga-oncoto-caixa-2026.html
    ├── 20260515-dossie-rodolfo-macedo-foiorodolfo-caixa-2026.html
    └── … futuros dossiês Loterias …
```

### 3.1 Regras de publicação por linha

| Regra | Institucional (`caixa/`) | Loterias (`caixa/loterias/`) |
|-------|---------------------------|------------------------------|
| **Novos HTML** | Publicar na **raiz** de `caixa/` | Publicar **sempre** em `caixa/loterias/` |
| **Modo típico** | A (HTML direto) ou B pontual | B (`.md` + gerador) ou A one-off |
| **Slug no nome** | `…-caixa-2026` ou tema no slug | Incluir `loterias` ou creator no slug quando fizer sentido |
| **Senha padrão** | `caixa2026` (alias `embratur2026` em alguns) | `caixa2026` |
| **Índice** | Listado em `caixa/index.html` § Institucional | Listado em `caixa/loterias/index.html`; link a partir do índice pai |
| **Makefile DEST** | `DEST=caixa` | `DEST=caixa/loterias` |

### 3.2 Compatibilidade de URLs (migração Loterias → subpasta)

Os HTML Loterias **já publicados** na raiz de `caixa/` mantêm redirects mínimos até o tráfego antigo zerar:

```
caixa/20260401-dossie-squad-always-on-loterias-2026.html
  → redirect para caixa/loterias/20260401-dossie-squad-always-on-loterias-2026.html
```

Padrão: **um** `<meta http-equiv="refresh">` ou JS de redirect no arquivo antigo; canônico = `caixa/loterias/`.

Exceção a manter na raiz sem mover: nenhum dos Loterias — todos migram para `loterias/`.

Redirect legado **Febraban** em `caixa/20260427-…` permanece até fase de limpeza (não é linha Caixa).

---

## 4. Projetos (fonte) — espelho da superfície

```
projects/
├── README.md
├── _template/                          # modelo modo B mínimo
│
└── caixa/
    ├── institucional/
    │   ├── auditoria-personalidades-20260326/
    │   │   ├── manifest.yaml
    │   │   └── …                        # modo A: notas; HTML editado em caixa/
    │   └── isadora-cartao-20260506/
    │
    └── loterias/
        ├── always-on-20260401/          # era loterias2026/
        ├── always-on-20260406/          # era loterias2026-20260406/
        ├── always-on-20260504/          # era loterias2026-20260504/
        ├── pulga-quina-20260514/        # modo A; HTML em caixa/loterias/
        └── rodolfo-always-on-20260515/
```

### 4.1 `manifest.yaml` — campo `line`

Cada projeto Caixa declara a linha explicitamente:

```yaml
# projects/caixa/loterias/always-on-20260401/manifest.yaml
client: caixa
line: loterias                    # institucional | loterias
delivery_date: 2026-04-01
slug: squad-always-on-loterias-2026
mode: B
variant: squad_13
source:
  md: data/dossier_loterias2026.md
  panels: data/dossier_loterias2026_panels.yaml
publish:
  dest: caixa/loterias
  password_ref: caixa2026
status: published
html_published: caixa/loterias/20260401-dossie-squad-always-on-loterias-2026.html
```

```yaml
# projects/caixa/institucional/isadora-cartao-20260506/manifest.yaml
client: caixa
line: institucional
delivery_date: 2026-05-06
slug: isadora-cruz-cartao-caixa-2026
mode: A
publish:
  dest: caixa
  password_ref: caixa2026
status: published
html_published: caixa/20260506-dossie-isadora-cruz-cartao-caixa-2026.html
```

### 4.2 Outros clientes em `projects/`

```
projects/
├── febraban/
│   └── concorrencia-creators-20260427/   # fonte sai de loterias2026/data/
└── embratur/
    └── auditoria-20260323/
        └── research/                     # era embratur/research/
```

---

## 5. Motor (`engine/`) — resumo

Substitui `tools/` com fronteiras internas:

```
engine/
├── core/           # dossier_render, md_dossier_source
├── cli/            # build_dossier (único), publish_dossier, export_pdf
├── qa/             # validate, check_links, check_html_leakage
├── research/       # penetracao_mercados
├── migrations/     # patch_*.py — deprecar com prazo
└── requirements/
```

**CLI unificado:**

```bash
make dossie-build   PROJECT=caixa/loterias/always-on-20260401
make dossie-entregar PROJECT=caixa/loterias/always-on-20260401
# DEST inferido do manifest (caixa/loterias vs caixa)
```

Shims temporários: `make qa-dossier-squad-13` → alias do projeto `always-on-20260401`.

---

## 6. Métodos (`methods/`)

Metodologia **genérica** (não presa a Loterias):

```
methods/
├── discovery/METODO_DESCOBERTA_PERFIS.md
├── brand-safety/METODO_BRAND_SAFETY.md
└── osint/README.md
```

Pesquisa **específica de um lote** fica em `projects/caixa/loterias/<entrega>/research/`.

---

## 7. Inventário canônico — seções Caixa

`docs/INVENTARIO_DOSSIES.md` passa a ter três blocos Caixa (em vez de «geral» + «Always ON» misturados sem path):

| Seção no inventário | Path publicado | Linha |
|---------------------|----------------|-------|
| Caixa — institucional | `caixa/*.html` (exceto redirects) | `line: institucional` |
| Caixa — Loterias | `caixa/loterias/*.html` | `line: loterias` |
| Redirects legados | `caixa/20260427-…` (Febraban), redirects pós-migração Loterias | — |

---

## 8. CI/CD — impacto da divisão Caixa

| Workflow | Ajuste |
|----------|--------|
| `deploy-pages.yml` | Artefato `_site/` com `caixa/` **incluindo** `caixa/loterias/`; não publicar `projects/`, `engine/` |
| `client-html-leakage.yml` | Scan em `caixa/` **recursivo** (cobre `loterias/`), `febraban/`, `embratur/` |
| `dossier-validate-all.yml` | Glob `projects/**/data/dossier_*.md` |

**Anti-vazamento:** HTML publicado não pode citar `projects/`, `loterias2026/`, `engine/`, `.md`, `_panels.yaml`.

---

## 9. Mapa de migração (Caixa)

| Atual | Destino superfície | Destino fonte (`projects/`) |
|-------|-------------------|----------------------------|
| `caixa/20260326-…` | `caixa/` (inalterado) | `projects/caixa/institucional/auditoria-personalidades-20260326/` |
| `caixa/20260506-…` | `caixa/` (inalterado) | `projects/caixa/institucional/isadora-cartao-20260506/` |
| `caixa/20260401`–`20260511` (squads) | `caixa/loterias/` + redirect na raiz | `projects/caixa/loterias/always-on-YYYYMMDD/` |
| `caixa/20260514-…` (Pulga) | `caixa/loterias/` + redirect | `projects/caixa/loterias/pulga-quina-20260514/` |
| `caixa/20260515-…` (Rodolfo) | `caixa/loterias/` + redirect | `projects/caixa/loterias/rodolfo-always-on-20260515/` |
| `loterias2026/` | — | `projects/caixa/loterias/always-on-20260401/` |
| `loterias2026-20260406/` | — | `projects/caixa/loterias/always-on-20260406/` |
| `loterias2026-20260504/` | — | `projects/caixa/loterias/always-on-20260504/` |

---

## 10. Fases de execução (prioridade Caixa)

| Fase | Escopo | Entregável |
|------|--------|------------|
| **3a** | Criar `caixa/loterias/`, mover HTML Loterias, redirects na raiz, atualizar índices | URLs canônicas em `loterias/` |
| **3b** | Renomear `loterias2026*` → `projects/caixa/loterias/*` + manifests com `line: loterias` | Fonte alinhada à superfície |
| **3c** | `projects/caixa/institucional/*` para entregas modo A com notas opcionais | Manifests `line: institucional` |
| **1** | `engine/` + build unificado (paralelo ou antes de 3b) | `make dossie-entregar` com DEST do manifest |

**Critério de done (Caixa):** inventário com duas seções; `caixa/index.html` sem Pulga/Rodolfo em «geral»; novos Loterias só em `caixa/loterias/`; leakage verde.

---

## 11. Decisões registradas

| ID | Decisão | Motivo |
|----|---------|--------|
| ADR-01 | Monorepo (não polyrepo) | Motor, métodos e agentes IA compartilham contexto |
| ADR-02 | `caixa/` na raiz (URLs estáveis) | Cliente já tem links publicados |
| ADR-03 | Subpasta `caixa/loterias/` | Separa institucional de campanha Loterias na superfície |
| ADR-04 | `projects/caixa/{institucional,loterias}/` | Espelha a superfície; briefing aponta linha explicitamente |
| ADR-05 | Redirects na raiz pós-migração | Não quebrar links antigos de squads |
| ADR-06 | Deploy Pages só com artefato `_site/` | Não expor CSVs, scripts e notas de pesquisa |

---

## 12. Referências internas

- Playbook completo: [`PLAYBOOK_DOSSIES.md`](../../PLAYBOOK_DOSSIES.md)
- Inventário atual: [`docs/INVENTARIO_DOSSIES.md`](../INVENTARIO_DOSSIES.md)
- README Caixa: [`caixa/README.md`](../../caixa/README.md)
