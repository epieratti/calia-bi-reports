# Instruções para agentes (calia-bi-reports)

Este repositório contém **relatórios e dossiês em HTML** publicados via **GitHub Pages** (`https://epieratti.github.io/calia-bi-reports/`). O trabalho típico é editar ou gerar HTML, scripts Python auxiliares e notas de pesquisa — não é uma aplicação web com build único na raiz.

## Estrutura principal

| Área | Caminho | Notas |
|------|---------|--------|
| Dossiê Embratur (referência) | `embratur/` | Página principal do site; `index.html` na raiz redireciona para cá. |
| Relatórios Caixa (no ar) | `caixa/` | **Artefatos servidos pelo Pages.** URLs em `caixa/README.md`. |
| Pesquisa / scripts Embratur | `embratur/research/`, `embratur/scripts/` | Ver `embratur/research/README.md`. |
| Loterias 2026 (pipeline) | `loterias2026/` | Build: `python scripts/build_dossier_completo.py` a partir de `loterias2026/`. Ver `loterias2026/README.md`. |

Para **dossiês Loterias já publicados em `caixa/*.html`**, trate o **HTML em `caixa/`** como fonte da verdade operacional: edições de conteúdo no que está no ar devem ser feitas nesses arquivos (rodar geradores em `loterias2026/` pode sobrescrever trabalho manual — confira `caixa/README.md`).

## Proteção por senha (client-side)

Vários HTML usam **hash SHA-256 no `<script>`** (ex.: `PASSWORD_SHA256_HEX_SET`). As senhas de referência estão documentadas em `README.md` e `caixa/README.md` (**não** as exponha em issues públicas desnecessariamente). Ao alterar lógica de acesso, mantenha o comportamento alinhado ao que o cliente já usa.

## Git e publicação

- Mensagens de commit em **português do Brasil**, claras (imperativo ou descrição direta do que mudou).
- Após implementar alterações pedidas: `git status` → `git add` (só o relevante) → `git commit` → push conforme o fluxo do branch em uso.
- Alterações em **`caixa/*.html`**, **`loterias*/output/*.html`** ou outros artefatos do Pages exigem que o remoto fique alinhado para o site refletir as mudanças (ver regra em `.cursor/rules/git-commit-apos-mudancas.mdc`).

## Boas práticas para mudanças

- **Escopo mínimo:** altere só o necessário; evite refatorações amplas não solicitadas.
- **Consistência:** siga o estilo e o padrão dos HTML e scripts existentes na mesma pasta.
- **Documentação:** não crie arquivos `.md` novos por iniciativa própria, exceto quando o pedido explicitamente pedir documentação.

## Referência rápida

- Visão geral e URLs: `README.md`
- Caixa (índice, senhas, dossiês): `caixa/README.md`
- Pipeline Loterias 2026: `loterias2026/README.md`
