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

### Estrutura do HTML final — o que o playbook cobre

| Situação | Onde está “ensinado” |
|----------|----------------------|
| **Modo B** (gerador Loterias) | A **ordem e os blocos** da página são **fixos no código** `tools/dossier_render.py` (não se monta o HTML à mão). **Referência visual no ar:** `caixa/20260401-dossie-squad-always-on-loterias-2026.html` (13 perfis / tiers) e `caixa/20260406-dossie-squad-always-on-loterias-2026.html` (8 perfis); equivalentes em `loterias2026/output/` e `loterias2026-20260406/output/` após o build. |
| **Modo A** (HTML direto) | Não há um único template no playbook: **duplicar o `.html` mais parecido** na mesma pasta do cliente (`caixa/`, `embratur/`) e adaptar conteúdo, mantendo classes/estrutura se quiseres o mesmo “look”. |

**Modo B — ordem das secções (de cima a baixo):** cabeçalho (`#topo`) → **Sumário** (links internos) → **Pedido e critérios** (`#pedido`) → **Leitura rápida** (`#leitura`) → **Como foi analisado** (`#como`) → **Perfis por camada** (`#perfis`, com subâncoras por tier e por pessoa) → **Síntese** (`#sintese`) → **Tabela resumo** (`#tabela`) → **Métricas nas redes** (`#metricas`) → rodapé. Tela de senha opcional no início (`#access-gate` / `#dossier-root`). Para **alterar** títulos, ordem ou layout de alto nível, é preciso **editar** `tools/dossier_render.py` (e regenerar o HTML), não só o `.md`.

**Variante `squad_13` vs `squad_8`:** mesmo esqueleto de secções; mudam detalhes (ex.: texto do sumário “Perfis por camada” vs “Perfis (Squad …)”, colunas da tabela de métricas, mini-cards). Comparar os dois HTML de referência acima.

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
