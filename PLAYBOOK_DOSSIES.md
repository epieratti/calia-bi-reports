# Playbook — linha de produção de dossiês (Calia BI Reports)

Documento na **raiz do repositório**: vale para **qualquer cliente ou tema** (Caixa, Loterias, Embratur, campanhas futuras). Cada pasta do projeto tem detalhes técnicos; aqui fica o **fluxo comum** e **onde encaixar** cada tipo de entrega.

## O que este repositório entrega

- **HTML estático** publicado no **GitHub Pages** (pastas como `caixa/`, `embratur/`).
- Muitas páginas têm **senha no navegador** (hash SHA-256); não é segurança forte — é controle de acesso leve para link compartilhado.
- Pesquisa e notas podem viver em **`research/`**, **`*.md`**, CSVs ou scripts — o que importa é **rastreabilidade** (o quê, quando, com qual fonte).

## Três modos de trabalho (escolha por entrega)

| Modo | Quando usar | Onde costuma cair | Fluxo resumido |
|------|-------------|-------------------|----------------|
| **A — HTML direto** | Dossiê único, layout já definido, pouca repetição de estrutura | `embratur/*.html`, `caixa/*.html` que não usam gerador | Editar o `.html` (ou duplicar um existente), manter mesmo padrão visual; commit em `main` / pasta servida pelo Pages. |
| **B — Fonte textual + gerador** | Muitos perfis, mesma “fábrica” (brand safety, squad, auditoria tabular) | `loterias2026/`, `loterias2026-20260406/` | `.md` (narrativa + briefing) + `_panels.yaml` (métricas) → script → HTML → copiar para `caixa/` se for entrega Caixa. |
| **C — Pesquisa + entrega manual** | Dados em CSV/notas, HTML montado na mão no fim | Varia | Pesquisa em `research/` + planilhas; HTML final na pasta do cliente conforme convenção do repo. |

Novos projetos: **comece pelo modo A** se for one-off; **prefira o modo B** se a estrutura for a mesma dos dossiês Loterias (perfis, tabelas, eixos).

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
- Modo **B:** criar par `dossier_<slug>.md` + `dossier_<slug>_panels.yaml` (ver comandos em `loterias2026/README.md` e `scripts/new_creator_dossier.py`).

### 3. Pesquisa e registo

- Notas e evidências: `research/` da pasta do projeto, ou `.md` dedicado; seguir metodologia local quando existir (ex.: brand safety em `loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md`).
- Manter rastreio do que foi consultado (queries, datas) para replicação.

### 4. Montagem e revisão

- Modo **A/C:** revisar HTML (acessibilidade básica, links, typos, senha).
- Modo **B:** `python3 scripts/build_dossier_completo.py` com `--md` / `--out` / `--variant` conforme `loterias2026/README.md`.

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
| Agentes / automação | raiz | `AGENTS.md` |

## Toolbox (raiz)

| Ferramenta | Comando | Função |
|------------|---------|--------|
| Validação estrutura + regra texto plano | `python3 tools/validate_dossier_source.py loterias2026/data/dossier_loterias2026.md` | Exige `##` perfis com `### Handles` e `### Síntese de risco`; avisa se `meta.title` (etc.) tiver `**` ou `#` colados do Markdown. `--strict` falha com avisos. |
| Checagem de links (opcional) | `python3 tools/check_dossier_links.py <arquivo.md>` | Testa URLs http(s) do ficheiro (pode falhar por bloqueio de bot). |
| Makefile | `make help` / `make validate-dossier-13` / `make build-loterias-13` | Atalhos na raiz. |
| CI | `.github/workflows/dossier-validate.yml` | Em PR/push que tocam nos `.md`, corre o validador (com PyYAML). |

### Regra: não copiar Markdown para campos errados

- **Onde pode `**` e links `[x](url)`:** parágrafos do briefing (`intro_paragraphs`, `criterios`), blocos `executive_summary` / `consolidated_narrative`, e no **corpo** do perfil: `### Narrativa`, eixos longos, `### Resumo tabela` e células da matriz — o gerador aplica **mini Markdown** (negrito, links).
- **Onde deve ser texto plano:** `meta.title`, `meta.subtitle`, `meta.client_line`, `meta.periodo`, nomes em `briefing.redes`, rótulos `methodology.columns[].label`, **tabelas de painéis** (`_panels.yaml`), e identificadores estruturais (`## Nome`, `- **Camada:**`, handles). Não colar linhas com `##` ou `**` vindas de outras secções para esses campos.
- **Defesa no código:** `tools/dossier_plain.strip_markdown_to_plain()` remove `**`, cabeçalhos `#` e converte links em “texto (URL)” nos campos que são só escape HTML, e normaliza nome/camada/handles ao ler o `.md`, para o HTML do cliente não mostrar lixo literal se alguém colar errado.

## Evolução do método

- **Novo tipo de dossiê** que vá se repetir: considere extrair **template HTML** ou **script de build** para `loterias2026/scripts/` (ou uma futura pasta `tools/`) e acrescente uma linha na tabela acima.
- **Detalhe só de Loterias** (comandos, variantes `squad_13` / `squad_8`): continua em `loterias2026/README.md`; o playbook da raiz não substitui esses passos técnicos.
