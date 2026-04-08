# Playbook — linha de produção de dossiês (Calia BI Reports)

Documento na **raiz do repositório**: vale para **qualquer cliente ou tema** (Caixa, Loterias, Embratur, campanhas futuras). Cada pasta do projeto tem detalhes técnicos; aqui fica o **fluxo comum** e **onde encaixar** cada tipo de entrega.

**Isto não é “o guia do projeto Loterias 2026”.** “Loterias 2026” no repo é **um exemplo** onde o **modo B** (fonte `.md` + gerador) já está montado — serve de **referência técnica**, não define todos os dossiês possíveis.

### Para o agente de IA (ler primeiro)

Este ficheiro existe para **orientar o agente** no fluxo certo. **Armadilha:** não confundir modo B com **YAML monolítico** (`dossier_*.yaml` com **toda** a narrativa em chaves) — isso foi **deixado de lado** no fluxo atual (texto “quadrado”, difícil de ajustar). O que vale:

- **Narrativa, perfis, links, eixos** → corpo **`dossier_*.md`** (Markdown com `##` / `###`).
- **Só números em tabela** (IG/TT/YT/X) → **`dossier_*_panels.yaml`**.
- YAML no topo do `.md` (front matter) = **meta curta** (título, listas de critérios), não o texto dos perfis.

Se encontrares `data/dossier_*_loterias*.yaml` **sem** par `.md` correspondente, trata como **legado** / migração; a fonte operacional do modo B é o **`.md` + `_panels.yaml`**.

## TL;DR — criar um dossiê novo (qualquer cliente)

1. **Este ficheiro (`PLAYBOOK_DOSSIES.md`)** — escolher **modo A, B ou C** (tabela abaixo). É o guia geral.
2. **Índice** — [`docs/INDICE_METODOS.md`](docs/INDICE_METODOS.md) para saltar a métodos concretos (pesquisa, métricas, publicação).
3. **Modo A (mais comum para one-off):** HTML direto em `caixa/`, `embratur/`, etc. — duplicar um `.html` existente ou seguir `caixa/README.md` / `README.md` raiz.
4. **Modo B (fábrica com muitos perfis):** hoje o **exemplo implementado** está em `loterias2026/` — `python3 loterias2026/scripts/new_creator_dossier.py SLUG` cria `dossier_SLUG.md` + painéis; `build_dossier_completo.py --md … --out …` gera HTML. Ver [`loterias2026/README.md`](loterias2026/README.md). Não é obrigatório o nome conter “loterias”; é só a pasta onde o tooling vive **por agora**.
5. **Validar** (se usares fonte `.md` no formato do gerador): `python3 tools/validate_dossier_source.py <teu/dossier_*.md>` — `make validate-dossier-13` só aponta para o **ficheiro de exemplo** do repo.
6. **Descobrir @** (nome ou nome + uma rede): [`loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md`](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) — método reutilizável; o caminho é histórico do primeiro lote.
7. **Motor HTML** (modo B): código único em **`tools/dossier_render.py`** + **`tools/md_dossier_source.py`**.

---

## O que este repositório entrega

- **HTML estático** publicado no **GitHub Pages** (pastas como `caixa/`, `embratur/`).
- Muitas páginas têm **senha no navegador** (hash SHA-256); não é segurança forte — é controle de acesso leve para link compartilhado.
- Pesquisa e notas podem viver em **`research/`**, **`*.md`**, CSVs ou scripts — o que importa é **rastreabilidade** (o quê, quando, com qual fonte).

## Três modos de trabalho (escolha por entrega)

| Modo | Quando usar | Onde costuma cair | Fluxo resumido |
|------|-------------|-------------------|----------------|
| **A — HTML direto** | Dossiê único, layout já definido, pouca repetição de estrutura | `embratur/*.html`, `caixa/*.html` que não usam gerador | Editar o `.html` (ou duplicar um existente), manter mesmo padrão visual; commit em `main` / pasta servida pelo Pages. |
| **B — Fonte textual + gerador** | Muitos perfis, mesma “fábrica” (brand safety, squad, auditoria tabular) | `loterias2026/`, `loterias2026-20260406/` | **`.md` = texto humano** (briefing + `##` perfis); **`_panels.yaml` = só métricas** em tabela. **Não** reintroduzir narrativa inteira em YAML. Script → HTML → `caixa/` se for Caixa. |
| **C — Pesquisa + entrega manual** | Dados em CSV/notas, HTML montado na mão no fim | Varia | Pesquisa em `research/` + planilhas; HTML final na pasta do cliente conforme convenção do repo. |

Novos projetos: **comece pelo modo A** se for one-off; **prefira o modo B** se a estrutura for a de “muitos perfis + tabelas + mesmo layout” — use **`loterias2026/`** como **referência de implementação**, não como nome do teu projeto.

### Estrutura do HTML final (modo B) — inventário completo

Tudo abaixo já existe **numa versão** gerada por `tools/dossier_render.py`. **Referência no ar:** `caixa/20260401-dossie-squad-always-on-loterias-2026.html` e `caixa/20260406-dossie-squad-always-on-loterias-2026.html` (ou `output/` após build). **Modo A** (outros dossiês): não segue esta lista — duplicar o HTML mais parecido em `caixa/` / `embratur/`.

Para **mudar ordem, títulos fixos ou layout** destes blocos → editar **`tools/dossier_render.py`**. Para **mudar texto** → `.md` / front matter / `_panels.yaml` conforme a coluna “Fonte”.

| # | Bloco (título visível) | ID / âncora | O que é | Fonte no modo B |
|---|------------------------|-------------|---------|-----------------|
| 0 | **Acesso restrito** | `#access-gate` | Caixa escura, formulário senha (SHA-256), mensagens de erro, botão Entrar; ao acertar esconde gate e mostra `#dossier-root`. | `password_sha256_hex` no front matter; texto fixo no código. `--no-gate` no build remove o bloqueio para preview. |
| 1 | **Cabeçalho** | `#topo` | Faixa navy: linha cliente (dourado), **H1** título, subtítulo, linha “Atualização / Documento / Build” com hash git opcional. | `meta.client_line`, `meta.title`, `meta.subtitle`, `meta.periodo` |
| 2 | **Sumário** | (nav) | Lista com links: Pedido e critérios, Leitura rápida, Como foi analisado, Perfis…, Síntese, Tabela resumo, Métricas. Segundo bloco **Perfis** com árvore por **camada** (`#tier-1`, `#squad-8`, etc.) e cada nome (`#slug-do-nome`). | `briefing.tier_order` + perfis no corpo `.md` (`## Nome`) |
| 3 | **Pedido e critérios de análise** | `#pedido` | Parágrafos introdutórios; subtítulo “O que foi verificado…”; **lista numerada** de critérios; linha **Redes de ativação** (IG, TT, …). | `briefing.intro_paragraphs`, `briefing.criterios`, `briefing.redes` |
| 4 | **Leitura rápida** | `#leitura` | Fundo cinza claro. Opcional: subtítulo + tagline; depois **grelha de cards** (2 colunas em desktop) com título dourado/navy e bullets **•** dourados; ou só bullets/parágrafos. | `executive_summary` no front matter (`blocks` / `items`, ou `tagline` / `subtitle`) |
| 5 | **Como foi analisado** | `#como` | **Cards** em grelha 2 colunas: cada card = rótulo (uppercase navy) + um ou mais parágrafos (mini-Markdown). | `methodology.columns[]` → `label`, `body` |
| 6 | **Perfis — análise por camada** | `#perfis` | Por cada **tier**: `h3` com nome da camada + borda dourada. Dentro, **um card por pessoa** (`section.card-audit`, `id` = slug do nome): |
| 6a | (dentro do perfil) Cabeçalho do perfil | — | **H2** “N. Nome” + à direita **selo “Síntese de risco”** (cores: verde “baixo”, âmbar “moderado”, vermelho “alto” conforme palavras no texto). | `### Síntese de risco` + `risco_geral` implícito no mesmo bloco |
| 6b | **Redes · snapshot** (mini-cards) | — | Grelha de **cartões compactos** por rede com **barra vertical colorida** (rosa IG, cinza TT, vermelho YT, preto X): plataforma, **@handle**, **números em destaque** (Seg., Eng., Insc., Views…). YouTube pode ter rodapé “Canal · nome longo”. X: chip “posts recentes” / “sem posts recentes” + linha de **teor recente**. Se não houver dados: mensagem tracejada. | Dados vêm das **linhas** em `_panels.yaml` cruzadas com `### Handles` no `.md`. Texto do caption varia (`squad_13` vs `squad_8`). |
| 6c | **Narrativa** (“sobre” o creator) | — | Parágrafo(s) abaixo dos mini-cards; **mini-Markdown** (negrito, links). É o bloco “quem é / contexto / marcas citadas na imprensa” — **não há caixa separada “Marcas”**; marcas entram aqui ou nos eixos. | `### Narrativa` no `.md` |
| 6d | **Três caixas de análise** | — | Grelha 3 colunas: **1. Concorrência**, **2. Polêmicas**, **3. Política** — título dourado + texto com mini-Markdown. | `eixos.concorrencia`, `polemicas`, `politica` (corpo do perfil no `.md`) |
| 7 | **Síntese do squad / do conjunto** | `#sintese` | Título configurável; mesmo padrão de **cards + bullets** que a Leitura rápida (grelha 2 colunas). | `consolidated_narrative` (`title`, `blocks`…) |
| 8 | **Tabela resumo** | `#tabela` | Introdução curta + **tabela**: Nome (± camada), **Síntese de risco** (selo compacto), Concorrência, Polêmicas, Política (células com links/negrito). | Perfis + `resumo_tabela` + `risco_geral` no `.md` |
| 9 | **Métricas nas redes** | `#metricas` | Parágrafo intro (nota data/cobertura); subsecções **Instagram**, **TikTok**, **YouTube**, **X** com **tabela larga** + rodapé “Fonte: …” + notas de cobertura/traço (TikTok pode ter texto extra). Linhas ordenadas como na tabela resumo. | `panels` em `_panels.yaml` |
| 10 | **Rodapé** | — | Link “Voltar ao topo”, texto fixo Calia; parágrafo **Build** + lembrete de push `caixa/`. | Build stamp no código; texto parcialmente fixo (“Always ON Loterias 2026” no template — mudar no `dossier_render.py` se outro produto). |

**Estilo global:** Tailwind via CDN; cores `calia-navy`, `calia-gold`; classes `card-audit`, `section-header`, `toc-link`. Comentário HTML `<!-- calia-dossier-build: … -->` no topo (variante com build).

**O que este template *não* tem (hoje):** secção dedicada só **“Marcas”** ou **“Sobre”** fora da narrativa; **galeria**; **vídeo embutido**. Isso seria modo A ou evolução do `dossier_render.py`.

**Variante `squad_13` vs `squad_8`:** mesmo inventário; diferem rótulos do sumário, primeira coluna da tabela de métricas (nome+camada vs só nome), índice da coluna “Eng.” no mini-card Instagram, e regra do mini-card X (em `squad_8` só aparece se handle X preenchido no `.md`).

### Gráficos (modo A / referência Embratur + catálogo para reutilizar)

O **modo B** gerado por `tools/dossier_render.py` **não inclui gráficos** hoje: métricas vão em **tabelas** e **mini-cards**. Para **partes** (rosca, radar, área, etc.) use **modo A** (HTML manual) ou evolua o gerador.

**Referência no repo — Embratur (Chart.js):** `embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html` carrega [Chart.js](https://www.chartjs.org/) por CDN. Lá já existem, por perfil:

| Tipo no Chart.js | Uso no dossiê | Nota |
|------------------|---------------|------|
| **`doughnut`** (rosca, `cutout: '70%'`) | Distribuição geográfica da audiência (%) | “Rosca” = doughnut com furo grande. |
| **`radar`** | Aderência a eixos temáticos (%, mesma escala) | Cinco critérios no eixo radial. |

**Gráfico de área:** nesse ficheiro Embratur **não há** `line`/`area` ainda; é um bom candidato quando houver **série temporal** (ex.: evolução mensal de seguidores, menções, scores). Em Chart.js: `type: 'line'` com `fill: true` no dataset (e opcionalmente `tension` para curva suave).

**Catálogo sugerido para deixar “pronto na cabeça” / snippets reutilizáveis** (todos nativos no Chart.js, sem dependência extra):

| Tipo | Quando usar |
|------|-------------|
| **Barra** (`bar`) | Comparar poucas categorias (ex.: engajamento por rede). |
| **Barra horizontal** | Rótulos longos (países, creators). |
| **Barras empilhadas** | Composição que soma 100% ou totais por grupo. |
| **`doughnut` / `pie`** | Partes de um todo; rosca costuma ler melhor que pizza cheia. |
| **`line` + preenchimento** | Tendência no tempo → efeito “área”. |
| **`line` sem preenchimento** | Duas ou mais séries no mesmo período (comparar creators ou métricas). |
| **`radar`** | Vários eixos qualitativos na mesma escala (como no Embratur). |
| **`polarArea`** | Partes de um todo com ênfase no ângulo (alternativa visual à rosca). |
| **Dispersão** (`scatter`) / **bolhas** (`bubble`) | Correlação ou “tamanho = volume” (ex.: seguidores × engajamento). |

**Boas práticas rápidas:** um gráfico = uma leitura; bloco **“Leitura do gráfico”** abaixo do canvas (como no Embratur); cores alinhadas à paleta do dossiê; após senha/gate, chamar `initCharts()` com `requestAnimationFrame` duplo para o canvas medir largura corretamente.

## Princípios (valem para todos os modos)

1. **Um fato, uma prova pública** quando a afirmação for sensível (marca, política, aposta, polêmica): preferir link para matéria, post arquivável ou documento oficial.
2. **Snapshot no tempo** — datas de coleta, “até mês/ano”, e lembrar que métricas de rede envelhecem rápido.
3. **Desambiguação** — homônimos (nome + @ + contexto); registrar o que foi descartado quando isso já deu ruído em entregas passadas.
4. **“Não consta” / “não achamos”** — significa *nas fontes e no método deste trabalho*, não “não existe”.
5. **Linguagem do cliente** no HTML entregue — sem citar ferramentas internas, nomes de arquivos do repo ou processos que não interessam à leitura executiva (salvo pedido explícito).
6. **Publicação** — o que o Pages serve está em **`caixa/`**, **`embratur/`**, etc., conforme `README.md` na raiz; após mudar HTML publicado, **commit + push** alinhado às regras do projeto.

## Pipeline sugerido (adaptar ao modo A, B ou C)

### 1. Briefing fechado

- Cliente, objetivo do dossiê, público-leitor, prazo, **critérios** de análise (o que é “risco”, o que é concorrência, etc.).
- Onde o ficheiro vai morar no site (URL esperada) e se haverá **senha** (qual política de hash, alinhada a outros dossiês do mesmo cliente).

### 2. Estrutura e convenções

- **Nome do ficheiro:** preferir `YYYYMMDD-tema-cliente.html` (ou prefixo já usado na pasta).
- **Índice:** se a pasta tiver `index.html` (ex.: `caixa/`), incluir link para o novo relatório.
- Modo **B:** criar par `dossier_<slug>.md` + `dossier_<slug>_panels.yaml` — comandos e template em **`loterias2026/README.md`** e `loterias2026/scripts/new_creator_dossier.py` (referência atual; outro cliente pode usar o mesmo tooling noutra pasta no futuro).

### 3. Pesquisa e registo

- Notas e evidências: `research/` da pasta do projeto, ou `.md` dedicado; seguir metodologia local quando existir (ex.: brand safety em `loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md`).
- Manter rastreio do que foi consultado (queries, datas) para replicação.

### 4. Montagem e revisão

- Modo **A/C:** revisar HTML (acessibilidade básica, links, typos, senha).
- Modo **B:** `python3 scripts/build_dossier_completo.py` com `--md` / `--out` / `--variant` (executar dentro da pasta do lote; ver `loterias2026/README.md` como exemplo).

### 5. Publicação

- Colocar o HTML na pasta servida pelo Pages; **testar URL** e gate de senha em HTTPS.
- Commit com mensagem clara em português; push conforme fluxo do branch / `main`.

## Mapa rápido do repositório

| Entrega | Pasta típica | Documentação extra |
|---------|--------------|-------------------|
| Embratur | `embratur/` | `embratur/research/README.md` |
| Caixa (no ar) | `caixa/` | `caixa/README.md` |
| Loterias / gerador | `loterias2026/`, `loterias2026-20260406/` | `loterias2026/README.md` |
| Visão geral + URLs | raiz | `README.md` |
| Índice métodos → ficheiros | raiz | `docs/INDICE_METODOS.md` |
| Agentes / automação | raiz | `AGENTS.md` |

## Toolbox (raiz)

| Ferramenta | Comando | Função |
|------------|---------|--------|
| Validação estrutura + regra texto plano | `python3 tools/validate_dossier_source.py <caminho/dossier_*.md>` | Exige `##` perfis com `### Handles` e `### Síntese de risco`; avisa se `meta.title` (etc.) tiver `**` ou `#` colados do Markdown. `--strict` falha com avisos. Exemplo no repo: `loterias2026/data/dossier_loterias2026.md`. |
| Checagem de links (opcional) | `python3 tools/check_dossier_links.py <arquivo.md>` | Testa URLs http(s) do ficheiro (pode falhar por bloqueio de bot). |
| Makefile | `make help` / `make validate-dossier-13` / `make build-loterias-13` | Atalhos na raiz. |
| CI | `.github/workflows/dossier-validate.yml` | Em PR/push que tocam nos `.md`, corre o validador (com PyYAML). |

### Descoberta de perfis (nome ou nome + um @)

Quando a entrada for **só o nome do creator** ou **nome + um único user** de uma rede, seguir a metodologia passo a passo para achar **Instagram, TikTok, YouTube e X** com confirmação e desambiguação de homônimos:

**`loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md`**

### Coleta de dados (ferramentas já usadas no repo)

Não são os mesmos scripts que validam o `.md`; servem para **alimentar pesquisa** e **métricas** antes de escrever o dossiê. Respeitar ToS das redes e política de dados do cliente.

| Área | O quê | Onde / como |
|------|--------|-------------|
| **Métricas Instagram e YouTube** | **Social Blade** — consulta manual no site (navegador); copiar números para o painel do dossiê. | Preencher `instagram` e `youtube` em **`dossier_*_panels.yaml`** (mesma estrutura dos lotes em `loterias2026/data/`). Rodapés do HTML já citam “Social Blade” onde aplicável. |
| **Métricas TikTok** | **Upfluence (TikTok Audit)** — exportação ou captura que **você** faz; enviar os dados (CSV, print estruturado ou tabela) para **organizar no repositório** (inserção nas `rows` do bloco `tiktok` do `_panels.yaml`, alinhado aos cabeçalhos do template). | Coordenação humana + edição de `dossier_*_panels.yaml`; não há integração API automática no fluxo atual. |
| **Métricas X (Twitter)** | **Plataforma X**, consulta **manual** no perfil público (navegador ou app). O essencial para o painel: **número de seguidores** e se a conta está **ativa** — ou seja, se a pessoa **ainda usa** o X (posts recentes visíveis) ou se está **parada há muito tempo** (sem uso relevante / última atividade antiga). Não é preciso inventariar todo o conteúdo; basta o que sustenta essas duas leituras + uma **linha de teor recente** (resumo objetivo) na tabela, como nos dossiês já publicados. | Preencher o bloco `x` em **`dossier_*_panels.yaml`** (`headers` + `rows`: costuma haver colunas para seguidores, atividade Sim/Não e resumo do teor). Rodapé do HTML: checagem na data da coleta. |
| **Loterias — OSINT open source** | Instaloader, yt-dlp, Sherlock, etc.: suplemento quando a imprensa não cobre o handle; logs em `research/osint_runs/`. | `loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md` (secção *Ferramentas open source e fluxo OSINT*), `FONTES_BRAND_SAFETY_LOTERIAS2026.md`, `loterias2026/research/osint_runs/requirements-osint.txt` |
| **Loterias — lote 06/04** | CSVs, merge de baseline, notas de redes | `loterias2026-20260406/scripts/merge_creators_baseline.py`, `data/*.csv`, `research/*.md` |
| **Embratur — proxy Trends/Wikipedia** | Penetração mercados (índices relativos; ver limites no README). | `embratur/scripts/penetracao_mercados.py`, `embratur/research/README.md` |

**Resumo (modo B — qualquer campanha com esta fábrica):** HTML final = `dossier_*.md` + `_panels.yaml` + `build_dossier_completo.py`. **Apify não faz parte do fluxo operacional.** Métricas típicas neste modelo: **Social Blade** (IG/YT) + **Upfluence** (TT) + **X manual**. **OSINT** opcional para narrativa. O nome “Loterias 2026” nos caminhos é só o **primeiro produto** que usou este pipeline.

### Regra: não copiar Markdown para campos errados

- **Onde pode `**` e links `[x](url)`:** parágrafos do briefing (`intro_paragraphs`, `criterios`), blocos `executive_summary` / `consolidated_narrative`, e no **corpo** do perfil: `### Narrativa`, eixos longos, `### Resumo tabela` e células da matriz — o gerador aplica **mini Markdown** (negrito, links).
- **Onde deve ser texto plano:** `meta.title`, `meta.subtitle`, `meta.client_line`, `meta.periodo`, nomes em `briefing.redes`, rótulos `methodology.columns[].label`, **tabelas de painéis** (`_panels.yaml`), e identificadores estruturais (`## Nome`, `- **Camada:**`, handles). Não colar linhas com `##` ou `**` vindas de outras secções para esses campos.
- **Defesa no código:** `tools/dossier_plain.strip_markdown_to_plain()` remove `**`, cabeçalhos `#` e converte links em “texto (URL)” nos campos que são só escape HTML, e normaliza nome/camada/handles ao ler o `.md`, para o HTML do cliente não mostrar lixo literal se alguém colar errado.

## Evolução do método

- **Novo tipo de dossiê** que vá se repetir: considere extrair **template HTML** ou **script de build** para `loterias2026/scripts/` (ou uma futura pasta `tools/`) e acrescente uma linha na tabela acima.
- **Detalhe só de Loterias** (comandos, variantes `squad_13` / `squad_8`): continua em `loterias2026/README.md`; o playbook da raiz não substitui esses passos técnicos.
