# Relatórios Caixa

Pasta para **HTML e artefatos** do cliente Caixa, no mesmo padrão de `embratur/`: arquivos servidos pelo GitHub Pages em:

`https://epieratti.github.io/calia-bi-reports/caixa/<arquivo>.html`

**Índice:** https://epieratti.github.io/calia-bi-reports/caixa/ — lista os `.html` com links corretos (evita 404 por digitação).

## Dossiê atual (mar/2026)

- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`** — Lúcio Mauro Filho e Alessandra Maestrini (métricas IG, Trends, marcas, riscos).
- **`20260401-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **13** perfis (lista anterior). **URL:** https://epieratti.github.io/calia-bi-reports/caixa/20260401-dossie-squad-always-on-loterias-2026.html — **senha `caixa2026`**.
- **`20260406-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **8** perfis (lote 06/04/2026), mesma estrutura (painéis IG/TT/YT/X + Brand Safety). Gerado a partir de `loterias2026-20260406/data/dossier_loterias2026.yaml`. **Senha:** `caixa2026`.
- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`:** **Senha:** `caixa2026` (sem espaços; sensível a maiúsculas/minúsculas). O HTML também aceita `embratur2026` como alias. Para mudar, atualize `PASSWORD_SHA256_HEX_SET` no `<script>`.

## Uso

- **Always ON Loterias — 13 perfis** (`20260401-…`): YAML em `loterias2026/data/dossier_loterias2026.yaml`; script `loterias2026/scripts/build_dossier_completo.py` (ou `publish_to_caixa.sh` em `loterias2026/`).
- **Always ON Loterias — 8 perfis** (`20260406-…`): YAML em `loterias2026-20260406/data/dossier_loterias2026.yaml`; `python3 loterias2026-20260406/scripts/build_dossier_completo.py` e copiar o HTML para `caixa/`.
- Adicione outros relatórios como `.html` diretamente em `caixa/` (ou em subpastas, se preferir organizar por data/tema).
- Não é obrigatório ter `index.html` aqui; cada relatório pode ter sua própria URL.
- Se quiser uma página inicial em `/caixa/`, crie opcionalmente `caixa/index.html` com links para os relatórios.
