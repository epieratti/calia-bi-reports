# Instruções para agentes (calia-bi-reports)

Este repositório contém **relatórios e dossiês em HTML** publicados via **GitHub Pages** (`https://epieratti.github.io/calia-bi-reports/`). O trabalho típico é editar ou gerar HTML, scripts Python auxiliares e notas de pesquisa — não é uma aplicação web com build único na raiz.

**Ordem de leitura sugerida:** `PLAYBOOK_DOSSIES.md` (TL;DR no topo) → `docs/INDICE_METODOS.md` → README da pasta do cliente (`loterias2026/`, `caixa/`, etc.).

**Motor dossiê Loterias (HTML):** `tools/dossier_render.py` + `tools/md_dossier_source.py` (importados por `loterias2026/scripts/build_dossier_completo.py` e `loterias2026-20260406/scripts/build_dossier_completo.py` — **não duplicar** esses ficheiros noutras pastas).

## Estrutura principal

| Área | Caminho | Notas |
|------|---------|--------|
| Dossiê Embratur (referência) | `embratur/` | Página principal do site; `index.html` na raiz redireciona para cá. |
| Relatórios Caixa (no ar) | `caixa/` | **Artefatos servidos pelo Pages.** URLs em `caixa/README.md`. |
| Pesquisa / scripts Embratur | `embratur/research/`, `embratur/scripts/` | Ver `embratur/research/README.md`. |
| Loterias 2026 | `loterias2026/`, `loterias2026-20260406/` | `PLAYBOOK_DOSSIES.md`, `docs/INDICE_METODOS.md`. Build: `scripts/build_dossier_completo.py` (importa `tools/dossier_render.py`). Descoberta de @: `loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md`. Novo lote: `loterias2026/scripts/new_creator_dossier.py`. Legado Apify: `loterias2026/scripts/README_LEGADO.md`. |

Para os dossiês Loterias **`20260401-…`** e **`20260406-…`**, a **fonte de conteúdo** é **`dossier_loterias2026.md`** + **`dossier_loterias2026_panels.yaml`** em `loterias2026/data/` e `loterias2026-20260406/data/`; o HTML em **`caixa/`** é o artefato publicado (gerar com `build_dossier_completo.py` e copiar de `output/`). Ver `caixa/README.md` e `loterias2026/README.md`.

## Proteção por senha (client-side)

Vários HTML usam **hash SHA-256 no `<script>`** (ex.: `PASSWORD_SHA256_HEX_SET`). As senhas de referência estão documentadas em `README.md` e `caixa/README.md` (**não** as exponha em issues públicas desnecessariamente). Ao alterar lógica de acesso, mantenha o comportamento alinhado ao que o cliente já usa.

## Git e publicação

- Mensagens de commit em **português do Brasil**, claras (imperativo ou descrição direta do que mudou).
- Após implementar alterações pedidas: `git status` → `git add` (só o relevante) → `git commit` → push conforme o fluxo do branch em uso.
- Alterações em **`caixa/*.html`**, **`loterias*/output/*.html`** ou outros artefatos do Pages exigem que o remoto fique alinhado para o site refletir as mudanças (ver regra em `.cursor/rules/git-commit-apos-mudancas.mdc`).

## Boas práticas para mudanças

- **Escopo mínimo:** altere só o necessário; evite refatorações amplas não solicitadas.
- **Consistência:** siga o estilo e o padrão dos HTML e scripts existentes na mesma pasta.
- **Documentação:** não crie ficheiros `.md` novos por iniciativa própria, exceto quando o pedido pedir documentação **ou** forem notas de pesquisa em `research/` / atualizações a métodos já listados em `docs/INDICE_METODOS.md`.

## Referência rápida

- Playbook de dossiês (raiz): `PLAYBOOK_DOSSIES.md`
- Índice métodos: `docs/INDICE_METODOS.md`
- Visão geral e URLs: `README.md`
- Caixa (índice, senhas, dossiês): `caixa/README.md`
- Pipeline Loterias 2026: `loterias2026/README.md`
