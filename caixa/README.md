# Relatórios Caixa

Pasta para **HTML e artefatos** do cliente Caixa, no mesmo padrão de `embratur/`: arquivos servidos pelo GitHub Pages na [pasta `caixa/`](https://epieratti.github.io/calia-bi-reports/caixa/) (caminho típico: `…/caixa/<arquivo>.html`).

**Convenção (playbook):**

- **Caixa — temas gerais** (ex.: auditoria de personalidades **sem** ser Loterias): HTML na **raiz** desta pasta — exemplo `20260326-dossie-auditoria-personalidades-caixa-2026.html`.
- **Caixa — linha Loterias / Always ON** (e similares): novos relatórios em **`caixa/loterias/`** (criar a subpasta se ainda não existir), nome `YYYYMMDD-dossie-….html`. Os ficheiros Loterias já na raiz de `caixa/` mantêm-se por histórico; migração para `loterias/` é opcional.

**Embratur** não usa esta pasta — relatórios ficam em **`embratur/`** na raiz do repo (ex.: `20260323-dossie-auditoria-personalidades-embratur-2026.html`).

**Índice:** [GitHub Pages — índice `caixa/`](https://epieratti.github.io/calia-bi-reports/caixa/) — lista os `.html` com links corretos (evita 404 por digitação). Se existir `caixa/loterias/index.html`, linkar a partir daqui também.

## Dossiês em `caixa/` (atualizado em abr/2026)

- **Febraban:** os HTML deste cliente ficam em **`febraban/`** na raiz do repo (não em `caixa/`). Ver **`febraban/README.md`** e [índice `febraban/` no Pages](https://epieratti.github.io/calia-bi-reports/febraban/) — senha **`febraban2026`**. Há **redirecionamento** de `caixa/20260427-dossie-febraban-concorrencia-creators-2026.html` para a URL em `febraban/` (links antigos).
- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`** — Lúcio Mauro Filho e Alessandra Maestrini (métricas IG, Trends, marcas, riscos).
- **`20260401-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **13** perfis (lista anterior). **Abrir no ar:** [dossiê Loterias 20260401](https://epieratti.github.io/calia-bi-reports/caixa/20260401-dossie-squad-always-on-loterias-2026.html) — **senha `caixa2026`**.
- **`20260406-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: squad **8** perfis (lote 06/04/2026), mesma estrutura (painéis IG/TT/YT/X + Brand Safety). **Senha:** `caixa2026`.
- **`20260504-dossie-squad-always-on-loterias-2026.html`** — Always ON **Loterias 2026**: **3 novos nomes** (lote 04/05/2026) — Linnyke Alves, Felipe Hatori e Julimara. **Senha:** `caixa2026`.
- **`20260506-dossie-isadora-cruz-cartao-caixa-2026.html`** — Perfil **Isadora Cruz** para apoio a ação de **cartão de crédito** (levantamento público: redes, marcas, política/religião, riscos). **Senha:** `caixa2026` (ou `embratur2026`, mesmo padrão do dossiê 20260326).
- **`20260326-dossie-auditoria-personalidades-caixa-2026.html`:** **Senha:** `caixa2026` (sem espaços; sensível a maiúsculas/minúsculas). O HTML também aceita `embratur2026` como alias. Para mudar, atualize `PASSWORD_SHA256_HEX_SET` no `<script>`.

## Fonte da verdade (dossiês Loterias)

Para **`20260401-…`**, **`20260406-…`** e **`20260504-dossie-squad-always-on-loterias-2026.html`**, a **fonte editável** está em:

- `loterias2026/data/dossier_loterias2026.md` + `dossier_loterias2026_panels.yaml` (squad 13)
- `loterias2026-20260406/data/dossier_loterias2026.md` + `dossier_loterias2026_panels.yaml` (squad 8)
- `loterias2026-20260504/data/dossier_loterias2026.md` + `dossier_loterias2026_panels.yaml` (squad 3 — Linnyke Alves, Felipe Hatori, Julimara)

Rode o build na pasta correspondente e **copie** o HTML gerado em `output/` para este diretório (`caixa/`) para publicar no GitHub Pages. O `.html` em `caixa/` é o artefato servido; mantê-lo alinhado ao build evita divergência.

**Febraban (abril/2026):** fonte editável em `loterias2026/data/dossier_febraban_concorrencia_2026.md` + `dossier_febraban_concorrencia_2026_panels.yaml`; build com `--variant squad_8`; copiar o `.html` gerado para **`febraban/`** (publicação Pages).

Modelo para **novos** dossiês no mesmo formato: `loterias2026/data/dossier_TEMPLATE.md`.

Para outros relatórios em `caixa/` que **não** usem esse pipeline, o HTML nesta pasta continua sendo a referência direta.

## Uso

- **Always ON Loterias — 13 e 8 perfis** (`20260401-…`, `20260406-…`): editar **`.md` + `_panels.yaml`** nas pastas `loterias2026/` ou `loterias2026-20260406/`, gerar o HTML, copiar para `caixa/` e commitar.
- Adicione outros relatórios como `.html` diretamente em `caixa/` (ou em subpastas, se preferir organizar por data/tema).
- Não é obrigatório ter `index.html` aqui; cada relatório pode ter sua própria URL.
- Se quiser uma página inicial em `/caixa/`, crie opcionalmente `caixa/index.html` com links para os relatórios.
