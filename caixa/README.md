# Relatórios Caixa

Pasta para **HTML e artefatos** do cliente Caixa, no mesmo padrão de `embratur/`: arquivos servidos pelo GitHub Pages em:

`https://epieratti.github.io/calia-bi-reports/caixa/<arquivo>.html`

**Índice:** https://epieratti.github.io/calia-bi-reports/caixa/ — lista os `.html` com links corretos (evita 404 por digitação).

## Dossiê atual (mar/2026)

- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`** — Lúcio Mauro Filho e Alessandra Maestrini (métricas IG, Trends, marcas, riscos).
- **`20260401-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **13** perfis (lista anterior). **URL:** https://epieratti.github.io/calia-bi-reports/caixa/20260401-dossie-squad-always-on-loterias-2026.html — **senha `caixa2026`**.
- **`20260406-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **8** perfis (lote 06/04/2026), mesma estrutura (painéis IG/TT/YT/X + Brand Safety). **Senha:** `caixa2026`.
- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`:** **Senha:** `caixa2026` (sem espaços; sensível a maiúsculas/minúsculas). O HTML também aceita `embratur2026` como alias. Para mudar, atualize `PASSWORD_SHA256_HEX_SET` no `<script>`.

## Fonte da verdade (dossiês Loterias)

**O conteúdo publicado destes relatórios é o HTML nesta pasta (`caixa/*.html`).** Edições de texto, tabelas e riscos devem ser feitas **direto no arquivo `.html` servido pelo GitHub Pages**.

Os diretórios `loterias2026/` e `loterias2026-20260406/` (YAML + scripts de build) são **legado**: rodar o gerador pode **sobrescrever** alterações feitas à mão no HTML. Não use mais o YAML como referência operacional para o que está no ar.

## Uso

- **Always ON Loterias — 13 e 8 perfis** (`20260401-…`, `20260406-…`): editar **somente** o `.html` correspondente em `caixa/`. Commit e push para publicar.
- Adicione outros relatórios como `.html` diretamente em `caixa/` (ou em subpastas, se preferir organizar por data/tema).
- Não é obrigatório ter `index.html` aqui; cada relatório pode ter sua própria URL.
- Se quiser uma página inicial em `/caixa/`, crie opcionalmente `caixa/index.html` com links para os relatórios.
