# Playbook — linha de produção de dossiês (Calia BI Reports)

**Agentes:** leia primeiro o guia curto [`PLAYBOOK_AGENTES.md`](PLAYBOOK_AGENTES.md); este arquivo é a **referência completa**.

Documento na **raiz do repositório**: vale para **qualquer cliente ou tema** (marcas, campanhas, auditorias). Cada pasta do projeto tem detalhes técnicos; aqui fica o **fluxo comum** e **onde encaixar** cada tipo de entrega.

**Tipo de produto que este playbook otimiza:** dossiês de **brand safety**, **vetting de creators/influencers** e **disaster check** (avaliação de risco reputacional e de encaixe com a marca **antes** ou **durante** parcerias — histórico público, concorrência, polêmicas, política, snapshot de redes). O **modo B** (`.md` + `_panels.yaml` + `dossier_render.py`) materializa **esse** modelo: perfis, síntese de risco, três eixos de análise, tabela resumo e painéis de métricas. Outros relatórios (ex.: auditorias com outro recorte) podem usar **modo A/C** ou adaptar seções — o fluxo e o briefing continuam válidos, mas o **inventário HTML** do modo B não é obrigatório fora desse tipo de entrega.

**Isto não é o guia de um único produto.** No repositório existe **uma implementação de referência** do **modo B** (fonte `.md` + gerador) — ver [README do modo B](loterias2026/README.md) — que **não** define todos os dossiês possíveis, mas **é** o exemplo canônico de **brand safety / squad de creators**.

### Idioma do dossiê (regra primordial)

**Todo** o conteúdo do dossiê entregue ao cliente deve estar em **português do Brasil (pt-BR)** — incluindo **`.md`**, **`_panels.yaml`** (rótulos, notas, células de texto visíveis no HTML), **HTML** gerado ou manual (títulos, parágrafos, sumário, botões, mensagens do gate), e **metadados de leitura** (título, subtítulo, período no front matter). **Exceto** quando o usuário pedir **explicitamente** outro idioma no briefing. Podem manter-se **citações**, **nomes de marcas**, **handles** e **trechos de fonte** no idioma original entre aspas ou com tradução entre parênteses, quando a fidelidade à prova for relevante.

### Qualidade da redação dos textos finais

**Quem costuma ler:** em geral **planejamento** e/ou **atendimento** da agência e/ou **cliente** (marca) — perfis mistos que precisam de **decisão e clareza**, não de notas de investigador. Redija como se o próximo leitor fosse **apresentar o dossiê** em reunião sem tempo para “traduzir” o documento.

Todo **texto que o cliente lê** (briefing no HTML, leitura rápida, metodologia, perfis, eixos, tabela resumo, notas de rodapé, rótulos de tabela quando forem frases) deve ser:

| Objetivo | O que significa na prática |
|----------|----------------------------|
| **Humanizado** | Soar como **análise humana** clara, não como extrato de robô ou lista de tags; frases completas; evitar jargão vazio (“sinergia”, “robusto”) e **bulletese** sem contexto. |
| **Fácil compreensão** | **Planejamento, atendimento e cliente** entendem à primeira leitura (não pressupor quem fez a pesquisa); definir siglas na primeira vez; preferir **ordem** sujeito → verbo → complemento; uma ideia principal por parágrafo. |
| **Sucinto** | Cortar repetição entre seções (o mesmo fato não precisa aparecer idêntico em narrativa, resumo e tabela sem valor agregado); preferir **menos palavras** mantendo o sentido. |
| **Completo — sem deixar dúvida** | Para cada afirmação que importa para **decisão** ou **risco**: o leitor sabe **o quê**, **em que base** (fonte ou “neste método não localizamos”), **até quando** vale (data) e, se aplicável, **o que não foi possível** verificar. Ambiguidade (“pode ser problemático”) só com **por quê** na mesma frase ou no parágrafo seguinte. |

**Teste rápido antes de fechar:** alguém de **planejamento ou atendimento** que **não** fez a pesquisa consegue usar o trecho numa **call com o cliente** (responder **sim/não**, **baixo/médio/alto** ou explicar o risco) sem improvisar? Se surgir “mas e se…?”, completar o texto.

#### Documento autocontido e links de fonte

**Regra:** o leitor deve **entender a conclusão e o raciocínio só lendo o HTML**, sem ser obrigado a **abrir** um link. Toda informação **necessária** para a decisão (o que aconteceu, o que foi verificado, qual o risco, qual o número relevante, qual a limitação) deve estar **escrita no corpo** do dossiê em frases completas.

| Uso do link | Permitido? |
|-------------|------------|
| **Complemento / prova** — quem quiser ver a matéria, o post ou o documento original | Sim (sempre que houver URL estável). |
| **Substituir** o texto (“ver detalhes aqui”, “conforme link”, afirmação que só faz sentido depois do clique) | **Não** — incorpore o essencial no parágrafo; o link fica **ao lado** como apoio. |

**Exemplo ruim:** “Há menções negativas na imprensa” + só um hyperlink.  
**Exemplo bom:** “Em DD/MM/AAAA, o veículo X publicou que… (resumo objetivo em uma ou duas frases).” + link para a matéria.

**Citação com link (obrigatório quando houver URL):** **Fonte é prioridade.** Sempre que a evidência tiver endereço **http(s)** estável (matéria, post, ficha oficial, arquivo), o dossiê deve incluir **link clicável** (`[rótulo](url)` no `.md`, que vira link no HTML) **além** do resumo no texto. **Não** basta escrever “conforme Veículo X” ou “post no Instagram” sem URL se essa URL existir e for acessível ao leitor. O parágrafo continua **autocontido** (quem não abre o link já entende); o link **comprova** e permite auditoria.

| Situação | Link obrigatório? |
|----------|-------------------|
| Matéria, post, fio, página pública com URL | **Sim** |
| Perfil público como fonte de “o que diz a bio / último post visto” | **Sim** — preferir URL do **perfil** ou do **post** específico citado |
| Métricas agregadas (Social Blade, etc.) | Rodapé “Fonte: …” já usado nos painéis; se no **texto** citar um número tirado de uma **página** específica, incluir **link** para essa página |
| Consulta só no app / print / reunião / documento sem URL pública | Indicar tipo e data; **sem** link inventado |
| Wayback / archive para URL que mudou | Link para o **snapshot** quando for a evidência usada |

Esta regra aplica-se a **narrativa, eixos, leitura rápida, síntese, células da tabela resumo** e notas que forem texto; **não** exige copiar artigo inteiro — basta o **núcleo informativo** que remove a dúvida.

Esta revisão entra naturalmente na etapa **4b — Síntese crítica** e de novo no **6 — QA** (reler em voz alta mentalmente os blocos executivos).

### Para o agente de IA (ler primeiro)

Este arquivo existe para **orientar o agente** no fluxo certo. **Regra principal:** o **briefing que o usuário passa** (mensagem, arquivo ou lista de requisitos) é a **fonte de verdade** para **modo** (A/B/C), **ordem das tarefas**, **o que incluir ou omitir** e **quando parar**. A tabela **Fluxo em etapas (0→7)** abaixo é um **esqueleto** — o agente deve **adaptar**, **fundir** ou **pular** passos conforme o briefing.

**Lacunas no briefing:** se faltar qualquer informação necessária para executar bem o pedido (ver checklist em **Pipeline §1**), o agente deve **perguntar ao usuário** antes de avançar — **não** supor silenciosamente pasta de publicação, modo A/B/C ou âmbito de redes. **Padrão operacional Calia (salvo pedido explícito em contrário):** o HTML **sempre** sai **com gate/senha** e o fluxo **sempre** inclui **commit + push** ao remoto (GitHub Pages) conforme [`AGENTS.md`](AGENTS.md) / branch em uso — não é preciso “perguntar se vai publicar” nem “se tem senha”; só **perguntar o valor da senha** (ou “igual ao dossiê X”) quando isso não vier no briefing, e respeitar **exceções explícitas** (ex.: preview sem senha, rascunho só local).

**Vários agentes de IA no mesmo dossiê:** usar **briefing único**, **fonte canônica** (`dossier_*.md` + `_panels.yaml`), **um integrador** e **contrato entre etapas** — detalhes e armadilhas em [`docs/MULTI_AGENTES.md`](docs/MULTI_AGENTES.md).

**Armadilha:** não confundir modo B com **YAML monolítico** (`dossier_*.yaml` com **toda** a narrativa em chaves) — isso foi **deixado de lado** no fluxo atual (texto “quadrado”, difícil de ajustar). O que vale:

- **Narrativa, perfis, links, eixos** → corpo **`dossier_*.md`** (Markdown com `##` / `###`).
- **Só números em tabela** (IG/TT/YT/X) → **`dossier_*_panels.yaml`**.
- YAML no topo do `.md` (front matter) = **meta curta** (título, listas de critérios), não o texto dos perfis.

Se encontrar **`dossier_*.yaml` monolítico** (narrativa inteira dentro do YAML) **sem** par `.md` correspondente, trata como **legado** / migração; a fonte operacional do modo B é o **`.md` + `_panels.yaml`**.

## Fluxo em etapas (para o agente) — ordem de execução

**Antes de executar:** ler o **briefing do usuário** e produzir um **plano em 3–7 bullets** (modo, arquivos a tocar, validações, entrega) **alinhado a esse pedido**. Só depois aplicar a sequência — como **referência**, não como receita fixa.

A tabela abaixo resume a ordem **típica** quando o briefing for um dossiê “completo”. Os detalhes estão nas seções indicadas; no **modo B**, não pular **validação** (etapa 6) salvo se o briefing disser explicitamente *preview só* ou equivalente.

| Etapa | Ação | Saída / critério de “feito” |
|-------|------|-----------------------------|
| **0 — Modo** | A partir do **briefing**, escolher **A**, **B** ou **C** (tabela **Três modos de trabalho** mais abaixo neste arquivo). Se o pedido for ambíguo, propor modo + razão em 1 frase antes de avançar. | Modo escolhido e **coerente com o briefing**. |
| **1 — Briefing** | Extrair ou confirmar: objetivo, leitor, critérios de risco/concorrência, redes no âmbito, pasta/URL de entrega, **texto da senha** (ou referência a outro dossiê). **Padrão:** gate **sempre**; publicação **sempre** (push), salvo exceção explícita no pedido. O que o usuário **não** pediu fica fora do âmbito salvo combinado. | Lista explícita de requisitos; **perguntar** o que faltar (checklist §1) antes de executar. |
| **2 — Identidade** | Resolver **handles** e homônimos: [descoberta de perfis](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md). | Lista `@` confirmados por rede (ou “não localizado”) + nota de desambiguação. |
| **3a — Modo B: arquivos** | Na pasta do lote: `new_creator_dossier.py` ou editar par existente `dossier_*.md` + `dossier_*_panels.yaml`. Front matter + `##` perfis; painéis só métricas. | Par de arquivos consistente; ver [README do modo B](loterias2026/README.md). |
| **3b — Modo A/C: arquivos** | Duplicar `.html` de referência ou montar estrutura manual; aplicar seção **Esquema de cores** deste playbook se novo layout. | HTML base válido na pasta de entrega. |
| **4 — Pesquisa** | Narrativa, eixos, evidências; métricas conforme seção **Coleta de dados** (final deste arquivo) e [brand safety](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md) **só se** o briefing exigir esse nível de profundidade. | Afirmações sensíveis com fonte; datas de snapshot. |
| **4b — Síntese crítica** | **Depois** da coleta: leitura crítica do material, decisão do que entra, ordem, hierarquia e visuais — ver [Síntese crítica e arquitetura da entrega](#síntese-crítica-e-arquitetura-da-entrega-entre-coleta-e-montagem). | Plano explícito (bullet list, 5–20 itens) **antes** de montar HTML ou fechar `.md`; reduz retrabalho. |
| **5 — Montagem** | **B:** `build_dossier_completo.py --md … --out … --variant …`. **A/C:** editar HTML até fechado. | Artefato `.html` gerado ou atualizado. |
| **6 — QA** | **B:** `tools/validate_dossier_source.py` no `.md` (e opcional `check_dossier_links.py`). Revisar links, typos, gate de senha, impressão básica. | Validador sem erros (ou `--strict` conforme política). |
| **7 — Publicação** | Copiar para pasta servida pelo Pages se necessário; testar URL + senha; `git` conforme [`AGENTS.md`](AGENTS.md) / regras do projeto. | HTML acessível como esperado. |

**Ramificação rápida:** se **modo A** → pular **3a**, fazer **3b**; após **4** + **4b** ir a **5** no HTML. Se **modo C** → **3b** pode ser mínimo; **5** iterativo. Se **modo B** → **3a** obrigatório; **5** via script. Ajustes rápidos só métricas: **4b** pode ser só “painéis + ordem da tabela”; dossiê completo: **4b** completo.

### Síntese crítica e arquitetura da entrega (entre coleta e montagem)

**Quando:** sempre **após** a coleta (etapa **4**) e **antes** de fechar narrativa em massa ou rodar o build final (**5**). Objetivo: **editar** em vez de **acumular** — o leitor executivo não precisa de tudo que foi encontrado.

#### O que fazer nesta fase

1. **Inventário** — listar o que existe: por perfil (fatos, riscos, lacunas, URLs) e transversal (comparativos possíveis, outliers).
2. **Confronto com o briefing** — o que sustenta a **decisão** pedida? O que é ruído ou fora de escopo?
3. **Credibilidade** — marcar cada afirmação sensível: **forte** (fonte + data) / **média** / **fraca**; fraca → reescrever com ressalva, mover para nota ou cortar.
4. **Contradições** — redes vs imprensa, números inconsistentes, homônimo mal resolvido: **resolver no texto** ou declarar limitação.
5. **Hierarquia da leitura** — o que vai para **leitura rápida**, o que só no **perfil**, o que só na **tabela resumo** ou **métricas**? Evitar repetir o mesmo parágrafo em três lugares.
6. **Modo B vs A** — se **B**: encaixar no inventário de blocos já definido (`#pedido`, perfis, `#sintese`, `#tabela`, `#metricas`); se **A**: decidir seções extras (gráficos, caixas) sem quebrar identidade visual.
7. **Visuais** — precisa de gráfico, rosca, barra de progresso ou **só tabela/número**? Consultar seção **Gráficos** e **Barras de progresso**; um gráfico = uma pergunta; não adornar sem função.
8. **Ordem narrativa dentro do perfil** — snapshot de redes → narrativa → eixos costuma ser o mais legível; ajustar se o briefing pedir “risco primeiro”.
9. **Tom e compressão** — cortar adjetivos, unificar duplicatas; manter **pt-BR** e linguagem do cliente.
10. **Redação** — passar cada bloco executivo pelo critério [humanizado / claro / sucinto / completo](#qualidade-da-redação-dos-textos-finais); remover tom de “relatório de máquina”.
11. **Autocontido** — nenhuma conclusão importante depende de **abrir** link; conferir [Documento autocontido e links](#documento-autocontido-e-links-de-fonte).
12. **Links de fonte** — toda afirmação ancorada na web com URL conhecida tem **hyperlink** no `.md`; no **6 — QA**, reler trechos sensíveis e confirmar que não faltou `[]()`.

#### Saída obrigatória (para o agente)

Produzir um **plano em texto** (pode ser comentário interno na resposta ao usuário ou nota em `research/`), com por exemplo:

- **3 decisões principais** (o que destacar / o que omitir e por quê).
- **Riscos ou lacunas** aceitos explicitamente.
- **Lista de gráficos ou visuais** (tipo + pergunta que responde) ou “nenhum — tabelas bastam”.
- **Checagem final:** “Leitura rápida cobre X; síntese cobre Y; nada crítico ficou só na pesquisa bruta”.

#### O que mais pode entrar nesta reflexão (expansão)

| Ângulo | Perguntas úteis |
|--------|------------------|
| **Leitor** | **Planejamento/atendimento** precisam de **âncoras** para proposta e defesa com o cliente? **Cliente** quer **resumo** ou **matriz**? Jurídico exige **citação** por frase? |
| **Comparabilidade** | Perfis na **mesma régua** (mesmas colunas, mesma data de snapshot)? Onde um outlier distorce a leitura? |
| **Temporalidade** | O que **envelhece** em 30 dias? Vale um box “até DD/MM/AAAA” na leitura rápida? |
| **Sensibilidade** | Política/aposta/marca: cada bloco tem **âncora** (link ou “declaração pública”)? |
| **Acessibilidade / impressão** | Muito gráfico escuro? Quebra de página no PDF? |
| **Gate e anexos** | Conteúdo que não cabe no HTML vai para **anexo** referenciado ou fica só em `research/`? |
| **Dupla leitura** | Simular: “só li a leitura rápida + tabela” — ainda consigo decidir? |

#### Briefing do usuário → plano customizado (checklist)

Usar o briefing para decidir **o passo a passo ideal**. Exemplos de como a ordem muda:

| Se o briefing disser… | Ajuste típico |
|------------------------|----------------|
| “Só atualiza métricas / painel” | **4** focado em `_panels.yaml` (ou tabelas HTML); **5** build mínimo; **6** validar; narrativa **não** reescrever sem pedido. |
| “Só texto / um perfil / revisão de risco” | **4** + edição `.md`; **5** só se houver build; pode não haver **2** completo se os `@` já forem dados. |
| “HTML novo estilo X” | **0** = A; **3b** primeiro (estrutura + cores); **4** encaixa conteúdo depois. |
| “Não publiques / só branch” | **7** = commit na branch; **sem** copiar para pasta Pages até ordem. |
| “Sem TikTok” / “só IG e YT” | **4** e painéis: omitir rede; não seguir checklist completo de coleta. |
| “Dossiê completo N perfis” | Seguir **0→7** completo; **2** antes de **4**; **4b** completo antes de **5**; não pular síntese crítica. |
| (implícito) entrega **Caixa** tema geral (não Loterias) | Publicar em **`caixa/`** (raiz); ver **Pastas onde o HTML deve ficar**. |
| (implícito) entrega **Caixa** + linha Loterias | Publicar em **`caixa/loterias/`** (novos); mesma seção. |
| (implícito) entrega **Embratur** | Publicar em **`embratur/`**; mesma seção. |
| Novo cliente sem pasta | Criar `/<slug>/` na raiz + `README.md`; HTML dentro dessa pasta. |

Se o briefing **contradizer** o playbook (ex.: pedir narrativa monolítica em YAML), **avisar** o usuário e preferir **`.md` + `_panels.yaml`** no modo B.

**Mapa do documento (onde aprofundar):** começar por [`PLAYBOOK_AGENTES.md`](PLAYBOOK_AGENTES.md) (visão curta); neste arquivo, procurar pelos títulos **Síntese crítica e arquitetura da entrega**, **Estrutura do HTML final (modo B)**, **Esquema de cores**, **Gráficos**, **Mercado: metodologia típica**, **Pipeline sugerido**, **Toolbox**. Exemplo mínimo 1 perfil: [`examples/minimo/`](examples/minimo/).

## TL;DR — criar um dossiê novo (qualquer cliente)

1. **Este arquivo (`PLAYBOOK_DOSSIES.md`)** — escolher **modo A, B ou C** (tabela abaixo). É o guia geral.
2. **Índice** — [`docs/INDICE_METODOS.md`](docs/INDICE_METODOS.md) para pular a métodos concretos (pesquisa, métricas, publicação).
3. **Modo A (mais comum para one-off):** HTML direto na **pasta de entrega** servida pelo site — duplicar um `.html` existente ou seguir [`README.md`](README.md) na raiz e o README da pasta em causa (quando existir).
4. **Modo B (fábrica com muitos perfis):** o **exemplo implementado** está descrito no [README do modo B](loterias2026/README.md). Dentro da pasta desse projeto: `python3 scripts/new_creator_dossier.py SLUG` cria `dossier_SLUG.md` + painéis; `build_dossier_completo.py --md … --out …` gera HTML. O caminho da pasta no repo é **histórico**; o tooling pode mudar de sítio no futuro.
5. **Validar** (se usares fonte `.md` no formato do gerador): `python3 tools/validate_dossier_source.py <teu/dossier_*.md>` — `make validate-dossier-squad-13` só aponta para o **arquivo de exemplo** do repo.
6. **Descobrir @** (nome ou nome + uma rede): [metodologia passo a passo](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) (localização do arquivo = histórico do primeiro lote com este fluxo).
7. **Motor HTML** (modo B): código único em **`tools/dossier_render.py`** + **`tools/md_dossier_source.py`**.

---

## O que este repositório entrega

- **HTML estático** publicado no **GitHub Pages** (estrutura de pastas no [`README.md`](README.md) da raiz).
- Muitas páginas têm **senha no navegador** (hash SHA-256); não é segurança forte — é controle de acesso leve para link compartilhado.
- Pesquisa e notas podem viver em **`research/`**, **`*.md`**, CSVs ou scripts — o que importa é **rastreabilidade** (o quê, quando, com qual fonte).

## Três modos de trabalho (escolha por entrega)

| Modo | Quando usar | Onde costuma cair | Fluxo resumido |
|------|-------------|-------------------|----------------|
| **A — HTML direto** | Dossiê único, layout já definido, pouca repetição de estrutura | Pastas com `.html` servidos pelo Pages **sem** gerador (ver [README](README.md)) | Editar o `.html` (ou duplicar um existente), manter mesmo padrão visual; commit na branch acordada / pasta servida pelo Pages. |
| **B — Fonte textual + gerador** | Muitos perfis, mesma “fábrica” (brand safety, squad, auditoria tabular) | [Projeto modo B — referência](loterias2026/), [segundo lote no repo](loterias2026-20260406/) | **`.md` = texto humano** (briefing + `##` perfis); **`_panels.yaml` = só métricas** em tabela. **Não** reintroduzir narrativa inteira em YAML. Script → HTML → pasta de publicação do projeto. |
| **C — Pesquisa + entrega manual** | Dados em CSV/notas, HTML montado na mão no fim | Varia | Pesquisa em `research/` + planilhas; HTML final na pasta do cliente conforme convenção do repo. |

Novos projetos: **comece pelo modo A** se for one-off; **prefira o modo B** se a estrutura for a de “muitos perfis + tabelas + mesmo layout” — use a [pasta de referência do modo B](loterias2026/README.md) como **implementação exemplo**, não como nome do teu projeto.

### Estrutura do HTML final (modo B) — inventário completo

Tudo abaixo já existe **numa versão** gerada por `tools/dossier_render.py`. **Referência no repositório:** [HTML gerado — variante 13 perfis](caixa/20260401-dossie-squad-always-on-loterias-2026.html), [variante 8 perfis](caixa/20260406-dossie-squad-always-on-loterias-2026.html) — ou `output/` após build na pasta do lote. **Modo A** (outros dossiês): não segue esta lista — duplicar o HTML mais parecido na pasta de entrega correspondente.

Para **mudar ordem, títulos fixos ou layout** destes blocos → editar **`tools/dossier_render.py`**. Para **mudar texto** → `.md` / front matter / `_panels.yaml` conforme a coluna “Fonte”.

| # | Bloco (título visível) | ID / âncora | O que é | Fonte no modo B |
|---|------------------------|-------------|---------|-----------------|
| 0 | **Acesso restrito** | `#access-gate` | Overlay escuro, formulário senha (SHA-256), mensagens de erro, botão Entrar; ao acertar esconde gate e mostra `#dossier-root`. | `password_sha256_hex` no front matter; texto fixo no código. `--no-gate` no build remove o bloqueio para preview. |
| 1 | **Cabeçalho** | `#topo` | Faixa navy: linha cliente (dourado), **H1** título, subtítulo, linha “Atualização / Documento / Build” com hash git opcional. | `meta.client_line`, `meta.title`, `meta.subtitle`, `meta.periodo` |
| 2 | **Sumário** | (nav) | Lista com links: Pedido e critérios, Leitura rápida, Como foi analisado, **Painel executivo** (se ativo), Perfis…, Síntese, Tabela resumo, Métricas. Segundo bloco **Perfis** com árvore por **camada** (`#tier-1`, `#squad-8`, etc.) e cada nome (`#slug-do-nome`). | `briefing.tier_order` + perfis no corpo `.md` (`## Nome`) |
| 3 | **Pedido e critérios de análise** | `#pedido` | Parágrafos introdutórios; subtítulo “O que foi verificado…”; **lista numerada** de critérios; linha **Redes de ativação** (IG, TT, …). | `briefing.intro_paragraphs`, `briefing.criterios`, `briefing.redes` |
| 4 | **Leitura rápida** | `#leitura` | Fundo cinza claro. Opcional: subtítulo + tagline; depois **grelha de cards** (2 colunas em desktop) com título dourado/navy e bullets **•** dourados; ou só bullets/parágrafos. | `executive_summary` no front matter (`blocks` / `items`, ou `tagline` / `subtitle`) |
| 5 | **Como foi analisado** | `#como` | **Cards** em grelha 2 colunas: cada card = rótulo (uppercase navy) + um ou mais parágrafos (mini-Markdown). | `methodology.columns[]` → `label`, `body` |
| 5b | **Painel executivo** | `#painel-executivo` | **Cards** por perfil (ordem = tabela resumo): nome, **semáforo** (Alto / Moderado / Baixo / A definir) derivado da síntese de risco, trechos curtos de **Concorrência** e **Polêmicas**; **campo de filtro** (nome ou camada) que esconde cards e **seções de perfil** abaixo. | Gerado automaticamente; desligar com `presentation.executive_dashboard: false` no front matter (ver subsecção *presentation* abaixo). |
| 6 | **Perfis — análise por camada** | `#perfis` | Por cada **tier**: `h3` com nome da camada + borda dourada. Dentro, **um card por pessoa** (`section.card-audit`, `id` = slug do nome): |
| 6a | (dentro do perfil) Cabeçalho do perfil | — | **H2** “N. Nome” + à direita **selo “Síntese de risco”** (cores: verde “baixo”, âmbar “moderado”, vermelho “alto” conforme palavras no texto). | `### Síntese de risco` + `risco_geral` implícito no mesmo bloco |
| 6b | **Redes · snapshot** (mini-cards) | — | Grelha de **cartões compactos** por rede com **barra vertical colorida** (rosa IG, cinza TT, vermelho YT, preto X): plataforma, **@handle**, **números em destaque** (Seg., Eng., Insc., Views…). YouTube pode ter rodapé “Canal · nome longo”. X: chip “posts recentes” / “sem posts recentes” + linha de **teor recente**. Se não houver dados: mensagem tracejada. | Dados vêm das **linhas** em `_panels.yaml` cruzadas com `### Handles` no `.md`. Texto do caption varia (`squad_13` vs `squad_8`). |
| 6c | **Narrativa** (“sobre” o creator) | — | Parágrafo(s) abaixo dos mini-cards; **mini-Markdown** (negrito, links). É o bloco “quem é / contexto / marcas citadas na imprensa” — **não há caixa separada “Marcas”**; marcas entram aqui ou nos eixos. | `### Narrativa` no `.md` |
| 6d | **Três caixas de análise** | — | Grelha 3 colunas: **1. Concorrência**, **2. Polêmicas**, **3. Política** — título dourado + texto com mini-Markdown. | `eixos.concorrencia`, `polemicas`, `politica` (corpo do perfil no `.md`) |
| 7 | **Síntese do squad / do conjunto** | `#sintese` | Título configurável; mesmo padrão de **cards + bullets** que a Leitura rápida (grelha 2 colunas). | `consolidated_narrative` (`title`, `blocks`…) |
| 8 | **Tabela resumo** | `#tabela` | Introdução curta + **tabela**: Nome (± camada), **Síntese de risco** (selo compacto), Concorrência, Polêmicas, Política (células com links/negrito). | Perfis + `resumo_tabela` + `risco_geral` no `.md` |
| 9 | **Métricas nas redes** | `#metricas` | Parágrafo intro (nota data/cobertura); subsecções **Instagram**, **TikTok**, **YouTube**, **X** com **tabela larga** + rodapé “Fonte: …” + notas de cobertura/traço (TikTok pode ter texto extra). Linhas ordenadas como na tabela resumo. | `panels` em `_panels.yaml` |
| 10 | **Rodapé** | — | Link “Voltar ao topo”, “Agência Calia” + linha de produto configurável; parágrafo **Build** + lembrete de push na pasta do cliente; nota legal opcional. | `presentation.product_tagline`, `presentation.footer_note`; build stamp no código. |

#### Bloco opcional `presentation` (front matter do `.md`)

Chaves no **mesmo nível** que `meta` / `briefing` (não dentro de `meta`):

| Chave | Tipo | Default | Efeito |
|-------|------|---------|--------|
| `executive_dashboard` | bool | `true` | Mostra ou oculta o **Painel executivo** e o link no sumário. |
| `product_tagline` | string | `Uso interno — brand safety / vetting` | Texto curto após “Agência Calia ·” no rodapé. |
| `footer_note` | string | vazio | Parágrafo extra no rodapé (texto plano; disclaimer jurídico, etc.). |

**Estilo global:** Tailwind via CDN; cores `calia-navy`, `calia-gold`; classes `card-audit`, `section-header`, `toc-link`. Comentário HTML `<!-- calia-dossier-build: … -->` no topo (variante com build).

**O que este template *não* tem (hoje):** seção dedicada só **“Marcas”** ou **“Sobre”** fora da narrativa; **galeria**; **vídeo embutido**. Isso seria modo A ou evolução do `dossier_render.py`.

**Variante `squad_13` vs `squad_8`:** mesmo inventário; diferem rótulos do sumário, primeira coluna da tabela de métricas (nome+camada vs só nome), índice da coluna “Eng.” no mini-card Instagram, e regra do mini-card X (em `squad_8` só aparece se handle X preenchido no `.md`).

### Esquema de cores (Calia + interface)

Objetivo: **mesma identidade** em modo B (gerado) e modo A (HTML manual), **legibilidade** em ecrã e **impressão/PDF** aceitável. Tipografia padrão do modo B: **Inter** (Google Fonts), com corpo sobre fundo claro.

#### Tokens de marca (Tailwind `extend.colors` no HTML)

Definidos no gerador em `tools/dossier_render.py` (bloco `tailwind.config` inline). **Reutilizar estes hex** em modo A, gráficos e CSS à mão.

| Token | Hex | Uso |
|-------|-----|-----|
| `calia-navy` | `#252525` | Cabeçalho principal, títulos de seção, texto de ênfase escura, borda esquerda do `section-header`, foco de formulários no gate. |
| `calia-gold` | `#f9a619` | Destaques (linha cliente no topo, bordas de tier, títulos das três caixas de análise, bullets da leitura rápida, botão “Entrar”, sublinhado dos links do sumário). |
| `calia-emerald` | `#009966` | Semântica **positiva** / baixo risco quando o layout usa token de marca (ex.: alguns dossiês manuais). |
| `calia-crimson` | `#CC0033` | Acento de alerta de marca; pode alinhar com séries ou destaques em gráficos quando fizer sentido. |

#### Neutros (fundo, cartões, texto, tabelas)

| Elemento | Valor típico | Nota |
|----------|----------------|------|
| Fundo da página | `#f8fafc` (equiv. `slate-50`) | Corpo global no `<style>` do modo B. |
| Texto principal | `#1e293b` (equiv. `slate-800`) | Parágrafos corridos. |
| Bordas / divisores | `#e2e8f0` (`slate-200`), `slate-100` | Cartões (`card-audit`), tabelas, separadores. |
| Texto secundário | `slate-500` / `slate-600` | Legendas, rodapés, notas. |
| Fundo de destaque suave | `slate-50`, `bg-slate-50` | Leitura rápida, síntese, células de tabela header. |

#### Semântica de risco (selos no modo B)

O gerador usa **Tailwind** para chips de “Síntese de risco”, não os tokens `calia-emerald` / `calia-crimson` diretamente neste bloco:

- **Baixo:** fundo `emerald-50`, texto `emerald-900`, anel `emerald-200`.
- **Moderado:** fundo `amber-50`, texto `amber-950`, anel `amber-200`.
- **Alto:** fundo `red-50`, texto `red-900`, anel `red-200`.

Manter esta **tríade verde / âmbar / vermelho** ao acrescentar selos ou badges noutros sítios para não contradizer o resto do dossiê.

#### Mini-cards por rede (barra vertical do modo B)

Cores **funcionais** para identificar rede à primeira vista (em `dossier_render.py`):

- **Instagram:** gradiente `pink-500` → `rose-600`.
- **TikTok:** `slate-800`.
- **YouTube:** `red-600`.
- **X:** `slate-900`.

Não é obrigatório repetir estas cores fora dos mini-cards; dentro deles, **não** misturar com a paleta de risco acima.

#### Gráficos (Chart.js, ECharts, etc.)

- **Série principal / marca:** `calia-gold` (`#f9a619`) e `calia-navy` (`#252525`) como contraste.
- **“Outros” / residual:** cinza neutro tipo `#cbd5e1` (`slate-300`) ou equivalente, como no [HTML de referência com charts](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html).
- **Paleta curta sugerida** (múltiplas séries): `#f9a619`, `#009966`, `#252525`, `#CC0033` — depois neutros slate se precisares de mais fatias.

#### Modo A ou white-label

- Copiar o bloco `tailwind.config.theme.extend.colors` do modo B (ou as variáveis CSS equivalentes) e **substituir só os hex** se o cliente tiver manual de marca aprovado.
- Manter **contraste** WCAG em botões e links (texto sobre `calia-gold` → usar `calia-navy`, não branco puro sobre dourado claro sem testar).
- Evitar **novas cores sem função** (cada cor = hierarquia ou significado: marca, risco, rede, neutro).

### Gráficos (modo A + catálogo para reutilizar)

O **modo B** gerado por `tools/dossier_render.py` **não inclui gráficos** hoje: métricas vão em **tabelas** e **mini-cards**. Para gráficos use **modo A** (HTML manual) ou evolua o gerador.

Stack recomendada nos dossiês já feitos: **[Chart.js](https://www.chartjs.org/)** via CDN (um `<script>`, `<canvas id="…">`, um bloco JS que instancia `new Chart(...)`). **Exemplo completo no repo:** [HTML com doughnut + radar](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html).

#### Qual gráfico usar em cada caso (decisão rápida)

Responda primeiro: **a pergunta é “partes de um todo”, “comparar categorias”, “evolução no tempo” ou “vários eixos na mesma escala”?**

| Pergunta / cenário típico no dossiê | Gráfico | Tipo Chart.js | Porquê |
|-------------------------------------|---------|---------------|--------|
| “De onde é a audiência?” / mix % país ou região | **Rosca** | `doughnut` + `cutout` alto (~60–75%) | Poucas fatias, leitura imediata de participação; “outros” como última fatia neutra. |
| “Qual a fatia de cada rede / canal no alcance?” (partes que somam ~100%) | Rosca ou **polarArea** | `doughnut` ou `polarArea` | Rosca para executivo; polarArea se quiseres ênfase angular diferente. Evitar `pie` cheia se o cliente já usa rosca no resto do relatório. |
| “Quem tem mais X entre 5–15 categorias?” (uma métrica) | **Barras verticais** | `bar` | Comparação direta de magnitude; ordenar barras ajuda. |
| “Comparar países / creators com nomes longos” | **Barras horizontais** | `indexAxis: 'y'` no `bar` | Rótulos legíveis sem cortar texto. |
| “Como cada grupo se divide em subpartes?” (ex.: alcance por rede *e* tipo de conteúdo) | **Barras empilhadas** | `bar` com `stacked: true` nas escalas | Mostra total *e* composição; legenda clara por cor. |
| “Como evoluiu ao longo dos meses?” (uma série) | **Área** | `line` com `fill: true` no dataset | Ênfase no volume acumulado no tempo; `tension` leve (ex. 0.25) suaviza sem distorcer. |
| “Comparar 2–3 séries no mesmo período” (ex.: IG vs TT) | **Linhas** (sem preenchimento ou só uma com fill) | `line`, `fill: false` (ou uma série com fill) | Evita sobreposição de áreas ilegível; limitar número de linhas. |
| “Quão forte é este perfil em critérios A, B, C… **na mesma escala**?” | **Radar** | `radar` | Ex.: aderência 0–100% em vários eixos temáticos (ver [exemplo Chart.js no repo](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html)). |
| “Há relação entre seguidores e engajamento?” / posicionar creators num plano | **Dispersão** ou **bolhas** | `scatter` / `bubble` | Eixo X e Y numéricos; em `bubble`, `r` (raio) = terceira dimensão (ex. volume de posts). |

**Quando *não* usar gráfico:** poucos números (1–3), tabela já resolve, ou risco de dados frágeis — preferir **número + texto** ou **tabela** (como no modo B).

#### Como implementar (checklist)

1. **No `<head>`:** `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>` (ou pin de versão se quiseres reprodutibilidade).
2. **No HTML:** envolver o canvas num contentor com altura fixa ou `aspect-ratio`, por exemplo classe `chart-container` com `height: 320px` e `position: relative` (Chart.js usa `responsive: true`, `maintainAspectRatio: false`).
3. **Dados:** arrays alinhados — `labels: [...]` e `datasets: [{ data: [...], backgroundColor / borderColor, ... }]`. Percentagens: garantir que somam 100% (ou declarar no texto que “outros” fecha o total).
4. **Instanciar:** `new Chart(document.getElementById('idDoCanvas'), { type: '…', data: { … }, options: { … } })`.
5. **Depois do gate de senha:** o canvas começa oculto — chamar a função que cria os charts **só depois** de mostrar o conteúdo, com **dois** `requestAnimationFrame` em sequência (padrão no [exemplo Chart.js no repo](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html)) para o layout medir largura corretamente.
6. **Leitura executiva:** abaixo de cada gráfico, um parágrafo **“Leitura do gráfico”** (o que ver, limitação da fonte, data de corte) — copiar o padrão `.chart-reading` do [mesmo HTML de referência](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html).

#### Referência no repo (doughnut + radar já implementados)

| Tipo | Uso no dossiê | Opções que importam |
|------|---------------|---------------------|
| **`doughnut`** | Distribuição geográfica (%) | `cutout: '70%'`, legenda em baixo, cores da marca + cinza para “outros”. |
| **`radar`** | Aderência a eixos temáticos (mesma escala, ex. 0–100) | `scales.r.beginAtZero`, `max: 100`, ticks discretos se quiseres menos ruído. |

**Área / linha:** ainda não estão nesse HTML; para série temporal seguir o checklist acima com `type: 'line'` e `fill: true` na série principal.

#### Catálogo resumido (mesma família Chart.js)

| Tipo | `type` | Uso |
|------|--------|-----|
| Barra | `bar` | Comparação entre categorias. |
| Barra horizontal | `bar` + `indexAxis: 'y'` | Rótulos longos. |
| Empilhada | `bar` + escalas `stacked: true` | Composição por grupo. |
| Rosca / pizza | `doughnut` / `pie` | Partes de um todo (preferir rosca). |
| Área | `line` + `fill: true` | Tendência temporal, uma série destacada. |
| Linhas múltiplas | `line`, `fill: false` | Comparar séries no tempo. |
| Radar | `radar` | Vários critérios, mesma escala. |
| Polar area | `polarArea` | Alternativa à rosca. |
| Dispersão / bolha | `scatter` / `bubble` | Duas (ou três) dimensões numéricas. |

**Boas práticas:** um gráfico = **uma** pergunta; título ou primeira frase da leitura diz essa pergunta; cores alinhadas à paleta do dossiê; indicar **fonte e data** junto ao gráfico ou na leitura.

#### Panorama mais recente (ferramentas “de ponta”) e encaixe neste tipo de trabalho

“Vanguarda” em visualização hoje mistura **gramáticas declarativas** (descreves o gráfico em JSON/spec), **canvas/WebGL** para muitos pontos, **mapas e pequenos múltiplos** (facetas), e **geração assistida** (LLM → spec). Para **dossiês em HTML estático**, com **gate de senha**, leitura **executiva** e por vezes **PDF/impressão**, o critério não é o máximo de efeito — é **clareza, reprodutibilidade e peso da página**.

| Abordagem | O que traz de moderno | Encaixa quando… | Atenção para dossiê |
|-----------|----------------------|-----------------|---------------------|
| **[Apache ECharts](https://echarts.apache.org/)** | Muitos tipos prontos, **mapas** (choropleth, geo), **brush**, tooltips ricos, séries longas em canvas | Precisas de **mapa**, várias séries, ou painel “denso” dentro de um capítulo HTML | Bundle **maior** que Chart.js; alinhar tema às cores do relatório; testar após mostrar o conteúdo (gate), como com qualquer canvas. |
| **[Vega-Lite](https://vega.github.io/vega-lite/)** + [Vega-Embed](https://github.com/vega/vega-embed) | **Gramática** (JSON): facetas, camadas, agregações declaradas; bom para **pequenos múltiplos** e encadear gráficos coerentes | Queres **um arquivo de spec** versionável ao lado do HTML ou pipeline “dados → spec → embed” | Dependência extra no `<head>`; validar spec com dados reais; export/impressão pode precisar de captura estática. |
| **[Observable Plot](https://observablehq.com/plot/)** | API de alto nível sobre ideias D3; rápido para protótipos e gráficos estatísticos limpos | Exploração e **protótipo** antes de fixar no HTML final, ou geração de SVG via build | Menos habitual como “um script CDN” isolado no mesmo padrão do [exemplo Chart.js no repo](embratur/20260323-dossie-auditoria-personalidades-embratur-2026.html); pode integrar-se em bundler ou notebook. |
| **[Plotly.js](https://plotly.com/javascript/)** | Interatividade “científica”, alguns modos **3D**, violino, contour | Relatórios com **distribuições** ou exploração mais analítica (menos comum em brand safety puro) | **Peso** e tempo de carga; 3D raramente melhora leitura executiva. |
| **D3.js** | Controlo total: **layouts** custom (sankey, rede, calendário), animações finas | Um gráfico **é** o diferencial da entrega (ex.: rede de citações, fluxo marca→tema) | Custo de manutenção alto; só quando Chart.js/ECharts não chegam. |
| **deck.gl** / **[Mapbox GL](https://docs.mapbox.com/mapbox-gl-js/guides/)** | **WebGL**, milhões de pontos, mapas grandes | Dados **geo** pesados (não é o caso típico de perfil/redes) | Overkill para a maioria dos dossiês; acessibilidade e PDF são piores. |
| **AntV [G2](https://g2.antv.antgroup.com/) / [G2Plot](https://g2plot.antv.antgroup.com/)** | Gramática tipo “The Grammar of Graphics”, ecossistema forte em produtos enterprise | Equipa já usa AntV ou queres estética/behaviour semelhantes a dashboards asiáticos | Documentação mais dispersa em inglês; mesmo trade-off de bundle que ECharts. |

**Tendência útil com IA:** gerar ou iterar **especificações** (sobretudo **Vega-Lite** ou options JSON estilo ECharts) a partir de uma tabela e de um pedido — acelera o rascunho; **sempre** rever escalas, cores, rótulos e unidades antes de publicar (alucinação de dados ou de tipo de gráfico é comum).

**Regra prática para este repositório:** mantém **[Chart.js](https://www.chartjs.org/)** como **padrão** (já alinhado a exemplos no repo). Sobe para **ECharts** ou **Vega-Lite** quando o capítulo precisar de **mapa**, **facetas**, **muitas séries** ou spec versionável. Reserva **D3 / WebGL** a entregas onde o gráfico custom é **central** e há tempo de QA.

#### Barras de progresso (porcentagem “preenchida”) — não é gráfico

É um **indicador linear**: faixa de fundo + preenchimento com largura proporcional a um valor (muitas vezes **0–100%**). **Não usa Chart.js** — basta **HTML + CSS** (opcionalmente `aria-valuenow` / `role="progressbar"` para leitores de ecrã). Útil quando queres **um único número** com **impacto visual rápido**, sem eixos nem legenda de gráfico.

| Caso no dossiê | Faz sentido? | Nota |
|----------------|-------------|------|
| **Score ou aderência** numa escala fechada (ex.: 0–100% de aderência a um eixo, “completude” de checklist metodológico) | Sim | Mostrar o **valor ao lado** ou por cima (“72%”) para não forçar o leitor a adivinhar. |
| **Cobertura de pesquisa** (ex.: “% de redes com dados validados”, “períodos com histórico disponível”) | Sim | Deixar claro **o que** soma 100% (ex.: “das 4 redes pedidas”). |
| **Quota ou teto** (ex.: participação estimada vs. mercado, **share** numa única fatia destacada) | Às vezes | Se houver **várias fatias comparáveis**, preferir **barra horizontal** ou **rosca**; a barrinha serve sobretudo para **um** indicador protagonista. |
| **Comparar muitos creators na mesma métrica** | Melhor outra coisa | Lista de 10 barrinhas pode funcionar, mas **barras horizontais** ordenadas costumam escalar melhor. |
| **Dados incertos ou ordens de grandeza discutíveis** | Evitar | A barra sugere **precisão**; se o número é estimativa, dizê-lo no texto e evitar falso detalhe (ex.: não mostrar “73,4%” se a fonte é grosso modo). |
| **Duplicar o que o radar já mostra** | Redundante | Radar já compara vários eixos; barrinha entra quando queres **destacar um** eixo no texto ou num card. |

**Como fazer (mínimo):** contentor `position: relative`, fundo neutro, cantos arredondados; filho interno com `width: NN%` (inline style ou classe), cor de destaque da marca; altura fixa pequena (ex. 8–12px) ou maior se quiseres área clicável. Opcional: `aria-valuemin="0" aria-valuemax="100" aria-valuenow="72"` no contentor com `role="progressbar"`.

**Boas práticas:** rótulo à esquerda ou por cima (**o quê** é essa %); **nunca** apresentar como “progresso real” de algo que é só um **índice** — chamar de “indicador” ou “estimativa” quando aplicável; mesma paleta do resto do dossiê.

### Mercado: metodologia típica em auditorias de creators (BI / influencer intelligence)

Síntese do que **guias do setor**, fornecedores de *vetting* e relatórios de *creator fraud* costumam descrever — útil para alinhar o dossiê ao que clientes e concorrentes já esperam ouvir. Não substitui o **briefing** do teu projeto; adapta pesos e critérios ao pedido.

#### Como costuma estar organizado o trabalho

| Fase | O que fazem | Ligação ao nosso fluxo |
|------|-------------|-------------------------|
| **Enquadramento** | Definir objetivo (brand safety, parceria, licitação), público-leitor, risco aceitável, redes no âmbito. | Playbook → briefing fechado; critérios no `.md` / pedido. |
| **Inventário de identidade** | Confirmar **handles corretos** por rede, homônimos, contas oficiais vs fã. | [Descoberta de perfis](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md). |
| **Snapshot de métricas** | Seguidores, engagement onde existir, atividade recente, alcance só se houver fonte estável. | Painéis `_panels.yaml`; Social Blade / Upfluence / X manual (toolbox abaixo). |
| **Avaliação de conteúdo e reputação** | Temas sensíveis, parcerias passadas, menções na imprensa, concorrência, política — com **fonte** por afirmação forte. | Narrativa + eixos no `.md`; evidências em `research/`. |
| **Síntese e classificação** | Matriz de risco / recomendação, linguagem executiva, data de corte. | Tabela resumo, selos, HTML final. |

Muitos frameworks comerciais falam em **dimensões** parecidas: **risco de conteúdo** (O que a pessoa publica?), **qualidade/autenticidade de audiência** (bots, pods, padrões estranhos), **brand safety / compliance** (disclosure, categorias proibidas), **fit com a marca** (valores, tom, histórico de colabs). Há também tendência a **reavaliar** creators ao longo do tempo em campanhas longas; o dossiê em HTML costuma ser **fotografia** numa data — deixar isso explícito.

#### Sinais que o mercado costuma olhar (além do “número grande”)

- **Engagement vs. seguidores** — faixas de referência variam por rede, tamanho de conta e *niche*; usar como **alerta**, não como prova única. Guias técnicos sugerem cruzar com qualidade de comentários e estabilidade no tempo.
- **Picos abruptos** de seguidores ou *engagement* sem evento plausível.
- **Comentários** repetitivos, genéricos ou padrão de *engagement pod*.
- **Coerência multi-plataforma** (presença, identidade, datas).
- **Arquivo** de páginas ou *posts* removidos ([Wayback Machine](https://web.archive.org/), etc.) quando a decisão depende do histórico.
- **Exports oficiais** (quando o creator ou a marca os partilham) — ouro para campanhas, nem sempre disponíveis em pré-auditoria.

#### Ferramentas gratuitas, freemium ou open source (e ressalvas)

Respeitar **ToS** das redes, **LGPD/GDPR** e uso **legítimo** (pesquisa, due diligence contratual). Muitas ferramentas OSINT **não** são “neutras” perante as plataformas — risco de bloqueio ou violação de termos; documentar o método no dossiê quando for relevante.

| Tipo | Exemplos frequentes no ecossistema OSINT / BI | Nota |
|------|-----------------------------------------------|------|
| **Enumeração de @ em muitos sites** | [Sherlock](https://github.com/sherlock-project/sherlock) (open source) | A partir de um *username*; validar cada hit manualmente. |
| **Vídeo / áudio público** | [yt-dlp](https://github.com/yt-dlp/yt-dlp) (open source) | Arquivar ou transcrever conteúdo **público**; não contornar paywalls nem geo-bloqueios de forma abusiva. |
| **Galerias / outras plataformas** | [gallery-dl](https://github.com/mikf/gallery-dl) (open source) | Mesmas ressalvas de ToS. |
| **Instagram (ecossistema Python)** | [Instaloader](https://github.com/instaloader/instaloader) (open source) | Uso intensivo pode violar ToS do Instagram; preferir no nosso fluxo como **suplemento** documentado, não como única prova. |
| **Arquivo web** | [Internet Archive](https://web.archive.org/), *snapshots* | Recuperar páginas ou *posts* já indexados. |
| **Métricas públicas agregadas (freemium)** | Social Blade, páginas públicas de perfil | Social Blade: consulta manual no browser (já no fluxo operacional deste repo). |
| **Plataforma X** | Perfil público no browser | API paga ou scraping agressivo fogem do “gratuito e estável”; o playbook assume **leitura manual** para atividade e seguidores. |
| **Pesquisa web / imprensa (sem API)** | [Google News](https://news.google.com/), [Google Alerts](https://www.google.com/alerts), pesquisa no navegador com **operadores** (`site:`, aspas, `-termo`) | Menções, polêmicas, entrevistas; tudo manual e gratuito. |
| **Enumeração de @ (ampliada)** | [Maigret](https://github.com/soxoj/maigret) (open source, sem API keys) | Semelhante ao Sherlock, cobre **muitos** sites; gerar ruído — **validar cada URL**; pode instalar com `pip install maigret`. |
| **Foto de perfil suspeita** | [Google Imagens](https://images.google.com/) “pesquisar por imagem”, [TinEye](https://tineye.com/) (uso gratuito limitado) | Detetar stock, celebridade ou reutilização de avatar. |
| **Arquivo (além do IA)** | [archive.today](https://archive.today/) e espelhos | Quando `web.archive.org` não tem snapshot da URL. |
| **Email público no briefing** | [holehe](https://github.com/megadose/holehe) (open source) | Lista **em que sites** um email costuma estar registado (sinal fraco); **só** com email que o cliente autorizou analisar e dentro de base legal. |

Ferramentas históricas tipo **TWINT** (Twitter sem API) perderam relevância com as mudanças na rede X — tratar como **legado** e não como recomendação atual.

Plataformas **pagas** (ex.: suites de *influencer marketing*, *brand safety* com IA, bases de imprensa) são comuns em agências grandes; o quadro acima cobre sobretudo o que equipas pequenas ou *open source* combinam.

#### Alinhamento com este repositório

- **Método de descoberta de perfis:** [METODO_DESCOBERTA_PERFIS_CREATORS.md](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md).
- **Brand safety, busca aberta, OSINT:** [METODO_BRAND_SAFETY_LOTERIAS2026.md](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md) e [FONTES_BRAND_SAFETY_LOTERIAS2026.md](loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md).
- **Coleta operacional** (métricas nos painéis): seção **Coleta de dados** mais abaixo neste playbook (Social Blade, Upfluence, X manual).

## Princípios (valem para todos os modos)

1. **Português (Brasil)** — o dossiê na íntegra em **pt-BR**, salvo instrução explícita em contrário no briefing (ver [Idioma do dossiê](#idioma-do-dossiê-regra-primordial)).
2. **Redação final** — textos **humanizados**, de **fácil compreensão**, **sucintos** e **completos** para a decisão: sem deixar dúvida sobre o que foi verificado, o que falta e o que isso implica (ver [Qualidade da redação dos textos finais](#qualidade-da-redação-dos-textos-finais)).
3. **Um fato, uma prova pública** quando a afirmação for sensível (marca, política, aposta, polêmica): o **fato e a leitura** vão **no texto** do dossiê (**autocontido**); se existir **URL** da evidência, incluir **sempre** o **link** — nunca só o nome do veículo/plataforma sem hyperlink quando a URL estiver disponível (ver [Documento autocontido e links](#documento-autocontido-e-links-de-fonte)).
4. **Snapshot no tempo** — datas de coleta, “até mês/ano”, e lembrar que métricas de rede envelhecem rápido.
5. **Desambiguação** — homônimos (nome + @ + contexto); registrar o que foi descartado quando isso já deu ruído em entregas passadas.
6. **“Não consta” / “não achamos”** — significa *nas fontes e no método deste trabalho*, não “não existe”.
7. **Linguagem do cliente** no HTML entregue — sem citar ferramentas internas, nomes de arquivos do repo ou processos que não interessam à leitura executiva (salvo pedido explícito).
8. **Publicação** — pastas servidas pelo Pages estão descritas no [`README.md`](README.md) da raiz; após mudar HTML publicado, **commit + push** alinhado às regras do projeto.

### Limites operacionais (agentes e automação)

- **Login e paywall:** o agente **não** substitui acesso humano a Social Blade, Upfluence, bases de imprensa pagas ou redes com login obrigatório.
- **ToS e escala:** não contornar paywall, geo-bloqueio abusivo nem fazer coleta em massa que viole termos das plataformas ou LGPD.
- **Bloqueios:** se a API ou o site **bloquear** (403, captcha, conta necessária), documentar no dossiê a **limitação** e a **data** — não inventar métricas.
- **OSINT** (Instaloader, etc.): **opcional**; falhas são comuns — usar como suplemento com evidência, não como única prova de um fato sensível.

## Pipeline sugerido (adaptar ao modo A, B ou C)

### 1. Briefing fechado

- Cliente, objetivo do dossiê, público-leitor, prazo, **critérios** de análise (o que é “risco”, o que é concorrência, etc.).
- **Pasta** de publicação no site (URL esperada) e o **texto da senha** do gate (ou “igual ao dossiê X”) — **padrão:** sempre com senha; publicação **sempre** com commit + push, salvo exceção explícita no pedido. O **nome do arquivo `.html`** o **agente define** pelo padrão deste playbook (**§2 — Nomenclatura**); o usuário **não** precisa enviar o nome, salvo pedido explícito de um nome fixo.

#### Perguntas que o briefing deve responder (checklist)

**Exemplos reais** de como os pedidos costumam chegar (squad com tiers, delta de nomes, casting com métricas, link Google Docs, briefing mínimo): [`docs/EXEMPLOS_BRIEFINGS.md`](docs/EXEMPLOS_BRIEFINGS.md) — use para reconhecer o padrão e saber o que ainda falta perguntar.

**Legenda — obrigatoriedade:**

- **E (essencial):** se faltar → **perguntar** ao usuário antes de executar trabalho substancial; não inventar.
- **C (condicional):** torna-se **essencial** só quando a condição na coluna “Quando” se aplica; nesse caso, se faltar → **perguntar**.
- **O (opcional):** se faltar → o agente pode seguir com **padrão do playbook/repo** e **declarar na resposta** o que assumiu (linguagem, redes padrão, data de métricas “data do trabalho”, etc.). O usuário pode sempre apertar estes pontos no briefing.

Exceto se o usuário disser explicitamente *“para o que faltar usa o padrão do playbook / do último dossiê X”* — aí aplicam-se padrões também onde seria **E**, mas o agente **lista** tudo o que ficou por defeito.

| Tema | Obrig. | Pergunta | Quando importa / condição **C** |
|------|--------|----------|----------------------------------|
| **Cliente e produto** | **E** | Para **quem** é o dossiê (marca, unidade, campanha)? | Pasta de publicação (`caixa/`, `caixa/loterias/`, `embratur/`, nova pasta), tom e linha “cliente” no cabeçalho. |
| **Objetivo** | **E** | O que o leitor deve **decidir** ou **entender** ao final? | Profundidade, riscos a priorizar, âmbito do texto. |
| **Leitor** | **O** | Quem lê (planejamento, atendimento, cliente, jurídico)? Nível de detalhe? | Default típico: **planejamento + atendimento + cliente** — linguagem acessível a quem **não** esteve na coleta; textos **humanizados, claros, sucintos e completos** (*Qualidade da redação*). |
| **Modo de entrega** | **C** | **A** (HTML manual), **B** (`.md` + gerador) ou **C** (pesquisa → HTML na mão)? Ou “igual ao último dossiê X”? | **Obrigatório perguntar** se o pedido **não** deixar o modo óbvio (ex.: só “atualiza o dossier” sem dizer qual arquivo). |
| **Âmbito** | **E** | Lista de **nomes / @** ou “descobrir perfis a partir de…”? Quantos perfis? | Sem isto não há alvo de pesquisa. |
| **Redes** | **O** | Quais redes entram (IG, TT, YT, X, outras)? Alguma **fora** de âmbito? | Default modo B: as quatro redes do template; ajustar se o briefing disser outra coisa. |
| **Critérios** | **O** | O que conta como **risco alto/médio/baixo**? O que é **concorrência** / **política** / **polêmica** neste pedido? | Default: critérios do pedido do cliente no `.md` / template. |
| **Métricas** | **O** | Snapshot até **que data**? Fontes: padrão repo (Social Blade, Upfluence, X manual) ou só dados anexados? | Default: “coleta na data do trabalho” + fontes do playbook. |
| **Evidência** | **O** | Obrigatório **link** por afirmação sensível? Imprensa, arquivo, só plataforma? | Default: seção **Princípios** mais abaixo neste arquivo (um fato, uma prova quando sensível). |
| **Formato HTML** | **O** | Reutilizar **layout** de um arquivo existente? Gráficos? White-label? | Default: mesmo padrão Calia / arquivo de referência mais próximo. |
| **Pasta de publicação** | **E** | **Pasta** de entrega (`caixa/`, `caixa/loterias/`, `embratur/`, …)? | Mínimo: **saber o cliente/pasta**. O **nome** do `.html` **não** precisa vir no briefing: o agente aplica **`YYYYMMDD-dossie-<slug>.html`** (§2) e **declara** o nome escolhido na resposta / commit. **Exceção:** se o usuário pedir um nome **específico**, seguir o pedido. |
| **Acesso (senha)** | **E** | **Texto da senha** (para gerar o hash do gate) ou **“igual ao dossiê / arquivo: …”**? | **Padrão:** **sempre** HTML **com** gate/senha. **Só** usar `--no-gate` / preview aberto se o usuário pedir **explicitamente**. Se faltar o **valor** da senha (ou a referência), **perguntar**. |
| **Publicação (git)** | **O** | O usuário pediu **explicitamente** não publicar ou só rascunho local? | **Padrão:** **sempre** **commit + push** ao remoto (fluxo do branch / GitHub Pages), alinhado a [`AGENTS.md`](AGENTS.md). **Não** perguntar “se vai publicar” no fluxo normal. |
| **Prazo e prioridade** | **O** | O que é **MVP** vs “se der tempo”? | Default: entregar o pedido literal. |
| **Restrições** | **O** | Não usar OSINT, não tocar em `tools/`, etc.? | Default: sem restrições extra além do playbook. |
| **Idioma** | **O** | Idioma do dossiê **diferente de pt-BR**? | Default: **todo** o entregável em **português (Brasil)** — só perguntar ou mudar se o briefing pedir outro idioma de forma explícita. |
| **Síntese pós-coleta** | **O** | O usuário quer **revisão explícita** do plano (4b) antes de fechar HTML? | Default: o agente faz **4b** de qualquer forma de forma interna; se “sim”, devolver o plano em bullets **na resposta** antes do build. |

#### Modelo de briefing (copiar e preencher)

```text
## Briefing — [título curto]
# (E) = essencial  (C) = condicional  (O) = opcional — ver tabela acima

1. (E) Cliente / campanha: 
2. (E) Objetivo (o que o leitor deve conseguir fazer ou entender): 
3. (O) Leitor-alvo: [ planejamento | atendimento | cliente | outro: ______ ] — nível de detalhe: 
4. (C) Modo preferido: [ A | B | C | “igual a <arquivo ou projeto>” ] — obrigatório se não for óbvio pelo pedido
5. (E) Perfis: [lista Nome + @ quando souber] OU [“descobrir a partir de: …”]
6. (O) Redes no âmbito: [ IG, TT, YT, X ] — excluir: [ … ]
7. (O) Critérios de risco / concorrência / política (definições para ESTE pedido): 
8. (O) Métricas: data do snapshot desejada: ______ — fontes: [ padrão repo | só dados anexados | … ]
9. (O) Evidências: [ link obrigatório | flexível ] — fontes preferidas: 
10. (E) HTML: pasta [ caixa/ | caixa/loterias/ | embratur/ | ______ ] — o agente nomeia o `.html` com o padrão §2 (`YYYYMMDD-dossie-<slug>.html`); só preencher aqui se quiseres **impor** um nome exato
11. (E) Senha do gate (texto para hash): ______ OU “igual ao dossiê / arquivo: ______” — padrão: **sempre** com senha; só sem gate se pedires **explicitamente** preview aberto
12. (O) Publicação: [ padrão: commit + push ao remoto / Pages ] — só preencher se for **exceção** explícita (ex.: “não publicar”, “só local”)
13. (O) Prazo / MVP / fora de âmbito: 
14. (O) Restrições ou notas: 
15. (O) Idioma: [ PT-BR — padrão; não preencher ] OU [ outro: ______ ] — só se NÃO for português do Brasil
16. (O) Mostrar plano de síntese (4b) na resposta antes do build: [ sim | não — padrão: agente faz 4b internamente ]
```

**Versão mínima (pressa):** responder **todos os (E)** — itens **1, 2, 5, 10** (só **pasta**; nome do `.html` é do agente), **11** (senha ou referência a outro dossiê) — e **cada (C) que se aplique** (4 se modo não for claro). Itens **(O)** podem ficar em aberto com padrão do playbook (**publicar sempre**, salvo exceção no item 12), desde que o agente **declare** o que assumiu (incluindo o **nome final** do `.html` gerado).

Se o usuário só enviar um subconjunto, o agente **pergunta** tudo o que for **(E)** ou **(C)** aplicável em falta; não inventar.

#### Briefing só com nomes de creators ou artistas

Lista de nomes **não** substitui um briefing fechado. O repo já cobre **como** descobrir @ e redes ([`METODO_DESCOBERTA_PERFIS_CREATORS.md`](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) e a secção **Descoberta de perfis** mais abaixo neste arquivo), **como** montar o HTML (modo B), brand safety e síntese (4b). O que **ainda precisa** existir (por pergunta ao usuário ou por padrão explícito) para um dossiê **completo, profundo e bem estruturado**:

| Lacuna | Por que importa | Ação do agente |
|--------|-----------------|----------------|
| **(E) Cliente, objetivo, pasta de publicação, senha** | Sem isso não há critério de risco alinhado ao projeto, lugar de publicação nem hash do gate | **Perguntar** — itens 1, 2, 10 e **11** do modelo acima (nome do `.html` = agente, §2) |
| **Contexto para homônimos** | Nome comum ou vários talentos parecidos → risco de amarrar **perfil errado** | Pedir: nicho, obra/programa, cidade, agência, “é o mesmo do item X”, ou link de referência mínima |
| **O que significa “profundo” aqui** | “Profundo” sem definição vira achismo ou escopo infinito | Confirmar ou declarar: janela de tempo (imprensa/histórico), **lista de concorrentes** a cruzar, recorte político/polêmico; se o pedido for decisório, **perguntar** o que é inaceitável |
| **Critérios explícitos** | Brand safety depende do que a **marca** chama de risco | Se o briefing não listar (concorrência, política, polêmica), usar template padrão **e** resumir na entrega o que foi assumido |
| **Métricas “de painel”** | Social Blade, Upfluence e X costumam exigir **browser/login** ou arquivo do time | Preencher o que for **público + evidência**; marcar **lacunas** com data; não inventar números |
| **Modo A/B/C e referência visual** | Estrutura e profundidade mudam | Se só vier lista de nomes, **perguntar** modo ou “igual ao dossiê X” (item 4 **C**) |

**Limites que nenhum nome sozinho resolve:** conta privada, paywall, mídia só dentro do app, bloqueio da plataforma, ou falta de pegada digital — registrar no texto como **limitação da coleta** com data, sem preencher vazio com suposição.

### 2. Estrutura e convenções

#### Nomenclatura do arquivo `.html` (publicado)

**Quem define o nome:** o **agente**, ao publicar — **não** é necessário o usuário mandar o nome no briefing. Aplicar este padrão e **anunciar** o nome escolhido (resposta, mensagem de commit ou nota curta). **Exceção:** briefing que **exija** um nome de arquivo literal (raro).

**Como escolher o `<slug>` (corpo após `dossie-`):** curto, **minúsculas**, **ASCII**, **hífens**; preferir **cliente** + **tema/campanha** + **ano** ou **recorte** (ex.: `squad-always-on-loterias-2026`, `auditoria-personalidades-caixa-2026`). Evitar lista de 13 nomes no nome do arquivo; se for revisão do **mesmo** tema, mudar o **`YYYYMMDD`** ou acrescentar sufixo claro (`-rev2`, `-delta-8`).

Padrão obrigatório salvo **briefing explícito** em contrário:

| Parte | Regra | Exemplo |
|-------|--------|---------|
| **Prefixo de data** | `YYYYMMDD` — data de **entrega**, **revisão** ou fecho do conteúdo relevante (não uma data arbitrária). | `20260406` |
| **Corpo** | `dossie-` + **slug** em **minúsculas**, **ASCII**, **hífens** entre palavras, sem espaços. | `dossie-squad-always-on-loterias-2026` |
| **Extensão** | `.html` | — |

**Nome completo:** `YYYYMMDD-dossie-<slug>.html`  
Exemplos reais no repo (mesmo padrão de nome em **todos** os clientes):

- **Caixa (tema geral, sem ser Loterias):** `20260326-dossie-auditoria-personalidades-caixa-2026.html` em [`caixa/`](caixa/).
- **Caixa (linha Loterias / Always ON):** `20260401-dossie-squad-always-on-loterias-2026.html` (histórico na raiz de `caixa/`; novos → preferir [`caixa/loterias/`](caixa/loterias/) quando existir).
- **Embratur:** `20260323-dossie-auditoria-personalidades-embratur-2026.html` em [`embratur/`](embratur/).

**Evitar:** `relatorio-final.html`, `Dossie_Loterias.HTML`, underscores se o repositório já usa hífens no mesmo cliente, nomes sem data quando há várias revisões do mesmo tema (a data no nome desambigua URLs).

#### Pastas onde o HTML deve ficar (GitHub Pages)

Cada pasta na **raiz do repo** (irmã de `tools/`, `docs/`) corresponde a um **segmento de URL** em `https://<org>.github.io/calia-bi-reports/<pasta>/…`.

| Cliente / âmbito | Pasta de publicação | Exemplo no repo (referência) |
|------------------|---------------------|------------------------------|
| **Caixa — temas gerais** (auditorias, personalidades, produtos que **não** sejam a linha Loterias/Always ON) | **`caixa/`** (raiz desta pasta) | `20260326-dossie-auditoria-personalidades-caixa-2026.html` — ver [`caixa/README.md`](caixa/README.md). |
| **Caixa — linha Loterias / Always ON** (e campanhas equivalentes do mesmo “pacote”) | **`caixa/loterias/`** | Novos arquivos aqui (URL `…/caixa/loterias/<arquivo>.html`). No histórico: `20260401-dossie-squad-always-on-loterias-2026.html` ainda em `caixa/` na raiz. |
| **Embratur** | **`embratur/`** | `20260323-dossie-auditoria-personalidades-embratur-2026.html` — ver [`embratur/research/README.md`](embratur/research/README.md) para contexto. |
| **Cliente sem pasta ainda** | **Criar** `/<slug>/` na raiz | `slug` em minúsculas, sem espaços (hífen ok); adicionar **`README.md`** com URL base do Pages e lista de relatórios. |

**Resumo:** **Caixa “puro”** (outros temas) → **`caixa/`**. **Caixa + Loterias** (linha dedicada) → **`caixa/loterias/`** para entregas novas. **Embratur** → **`embratur/`** (nunca dentro de `caixa/`).

**Fonte editável (modo B)** continua na pasta do **projeto** (ex.: `loterias2026/data/`, `loterias2026-20260406/data/`) — não confundir com a pasta de **publicação**. O fluxo é: build → copiar o `.html` gerado para `caixa/`, `caixa/loterias/`, `embratur/` ou outra pasta de cliente → commit.

**Histórico:** alguns dossiês Loterias já publicados estão **diretamente** em `caixa/*.html`; **novos** da mesma linha devem preferir **`caixa/loterias/`**. Migrar arquivos antigos para a subpasta é **opcional** (exige atualizar links em `index.html` e referências).

**`index.html`:** recomendado em `caixa/`, em `caixa/loterias/` (quando existir) e em qualquer pasta com **vários** relatórios — listar links para cada `.html` (evita 404 por URL digitada errada). Ao acrescentar relatório novo, **atualizar** o `index.html` dessa pasta.

- Modo **B:** criar par `dossier_<slug>.md` + `dossier_<slug>_panels.yaml` — comandos e template na [documentação do modo B](loterias2026/README.md) e em [`new_creator_dossier.py`](loterias2026/scripts/new_creator_dossier.py) (referência atual; o tooling pode viver noutra pasta no futuro).

### 3. Pesquisa e registro

- Notas e evidências: `research/` da pasta do projeto, ou `.md` dedicado; seguir metodologia local quando existir (ex.: [metodologia brand safety](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md)).
- Manter rastreio do que foi consultado (queries, datas) para replicação.

### 4. Montagem e revisão

- Modo **A/C:** revisar HTML (acessibilidade básica, links, typos, senha).
- Modo **B:** `python3 scripts/build_dossier_completo.py` com `--md` / `--out` / `--variant` (executar dentro da pasta do lote; ver [README do modo B](loterias2026/README.md)).

### 5. Publicação

- Colocar o HTML na pasta servida pelo Pages; **testar URL** e gate de senha em HTTPS (**padrão:** sempre com senha).
- Commit com mensagem clara em português; **push ao remoto** conforme fluxo do branch em uso (**padrão:** sempre publicar), salvo o briefing pedir **explicitamente** o contrário.

## Mapa rápido do repositório

| Entrega | Pasta típica | Documentação extra |
|---------|--------------|-------------------|
| Pasta entrega A | [`embratur/`](embratur/) | [README research](embratur/research/README.md) |
| Pasta entrega B (HTML no ar) | [`caixa/`](caixa/) | [README da pasta](caixa/README.md) |
| Modo B — referência + segundo lote | [`loterias2026/`](loterias2026/), [`loterias2026-20260406/`](loterias2026-20260406/) | [README modo B](loterias2026/README.md) |
| Visão geral + URLs | raiz | [`README.md`](README.md) |
| Índice métodos → arquivos | raiz | [`docs/INDICE_METODOS.md`](docs/INDICE_METODOS.md) |
| Agentes / automação | raiz | [`AGENTS.md`](AGENTS.md) |

### Disaster check / brand safety — ferramentas (onde está no playbook)

**Sim, está coberto** — não como um único capítulo com esse nome, mas reunido nestes pontos:

| Necessidade no disaster check | Onde no playbook / repo |
|-------------------------------|-------------------------|
| **Quem é o perfil certo** (homônimos, @ em cada rede) | Secção **Descoberta de perfis** (neste arquivo, após a tabela Toolbox) + [METODO_DESCOBERTA_PERFIS_CREATORS.md](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) |
| **Métricas públicas** (IG/YT, TT, X ativo/teor) | Secção **Coleta de dados** (a seguir a Descoberta) — Social Blade, Upfluence, X manual |
| **Busca aberta, OSINT, fontes de evidência** | [Metodologia brand safety](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md), [lista de fontes](loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md), tabela OSINT em **Coleta de dados** |
| **Sinais de mercado** (engagement, bots, frameworks de vetting) | Secção **Mercado: metodologia típica** (mais acima neste arquivo) + tabela de ferramentas gratuitas/OSINT |
| **Arquivo / histórico** (Wayback, etc.) | Na seção **Mercado** (sinais típicos) |
| **Geo / proxy Trends** (quando o dossiê precisar) | Linha **Proxy Trends / Wikipedia** em **Coleta de dados** + [`embratur/scripts/`](embratur/scripts/) |
| **Qualidade do entregável** (estrutura `.md`, links quebrados) | Tabela **Toolbox** (imediatamente abaixo desta subseção) — `validate_dossier_source.py`, `check_dossier_links.py` |

**Limitação honesta:** não há integração automática tipo “API de brand safety” no fluxo; é **manual + planilhas + OSINT opcional**, alinhado ao que o repositório já usa. Ferramentas **pagas** de mercado ficam fora do toolbox — só referência na seção **Mercado**.

## Toolbox (raiz)

| Ferramenta | Comando | Função |
|------------|---------|--------|
| Nome do arquivo publicado | `python3 tools/dossier_html_filename.py --md <dossier_*.md>` | Imprime `YYYYMMDD-dossie-<slug>.html` a partir de `meta.title` (usa hoje se omitir `--date`). |
| Pipeline até a pasta Pages | `python3 tools/dossier_publish.py --md <…> --dest <pasta ou .html>` | Valida → links → `build_dossier_completo.py` → grava HTML em `DEST` → `check_client_html_leakage` na pasta cliente. `make dossie-entregar MD=… DEST=…` na raiz. |
| Validação estrutura + regra texto plano | `python3 tools/validate_dossier_source.py <caminho/dossier_*.md>` | Exige `##` perfis com `### Handles` e `### Síntese de risco`; avisa se `meta.title` (etc.) tiver `**` ou `#` colados do Markdown. `--strict` falha com avisos de texto plano. **`--hints`** imprime dicas semânticas (lacunas, painéis, URLs); **`--strict-hints`** falha (exit 3) se houver dica — opcional em CI. [Exemplo de `dossier_*.md`](loterias2026/data/dossier_loterias2026.md). |
| Checagem de links (opcional) | `python3 tools/check_dossier_links.py <arquivo.md>` | Testa URLs http(s) do arquivo (pode falhar por bloqueio de bot). |
| Makefile | `make help` / `make dossie-filename` / `make dossie-entregar` / `make validate-dossier-squad-13` / `make build-dossier-squad-13` | Atalhos na raiz; `squad-13` / `squad-8` = lotes de referência do modo B. |
| CI | `.github/workflows/dossier-validate.yml` | Em PR/push que tocam nos `.md`, corre o validador (com PyYAML). |

### Descoberta de perfis (nome ou nome + um @)

Quando a entrada for **só o nome do creator** ou **nome + um único user** de uma rede, seguir a metodologia passo a passo para achar **Instagram, TikTok, YouTube e X** com confirmação e desambiguação de homônimos:

**[Metodologia — descoberta de perfis](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md)**

### Coleta de dados (ferramentas já usadas no repo)

Não são os mesmos scripts que validam o `.md`; servem para **alimentar pesquisa** e **métricas** antes de escrever o dossiê. Respeitar ToS das redes e política de dados do cliente.

#### Inventário — o que o guia já contempla para pesquisa / disaster check

| Categoria | Ferramentas / métodos |
|-----------|------------------------|
| **Métricas em painel** | Social Blade (IG/YT, browser), Upfluence (TT, dados que envias), X manual (seguidores + ativo + teor) |
| **OSINT no repo** | Instaloader, yt-dlp, Sherlock — [`tools/requirements-osint.txt`](tools/requirements-osint.txt) (canônico; cópia espelhada em `loterias2026/research/osint_runs/`) |
| **Descoberta de @** | Metodologia em [METODO_DESCOBERTA_PERFIS_CREATORS.md](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) |
| **Narrativa / fontes** | [METODO_BRAND_SAFETY_LOTERIAS2026.md](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md), [FONTES_BRAND_SAFETY_LOTERIAS2026.md](loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md) |
| **Arquivo e mercado** | Wayback, tabela ampliada na seção **Mercado** (Sherlock, gallery-dl, Maigret, Google News/Alerts, etc.) |
| **Geo / tendências (proxy Trends + Wikipedia)** | [`tools/penetracao_mercados.py`](tools/penetracao_mercados.py) + JSON de entidades (ex.: [`embratur/research/penetracao_entities_embratur_2026.json`](embratur/research/penetracao_entities_embratur_2026.json)); *wrapper* [`embratur/scripts/penetracao_mercados.py`](embratur/scripts/penetracao_mercados.py) chama o de `tools/`. |

| Área | O quê | Onde / como |
|------|--------|-------------|
| **Métricas Instagram e YouTube** | **Social Blade** — consulta manual no site (navegador); copiar números para o painel do dossiê. | Preencher `instagram` e `youtube` em **`dossier_*_panels.yaml`** (estrutura como nos [dados de exemplo](loterias2026/data/)). Rodapés do HTML já citam “Social Blade” onde aplicável. |
| **Métricas TikTok** | **Upfluence (TikTok Audit)** — exportação ou captura que **você** faz; enviar os dados (CSV, print estruturado ou tabela) para **organizar no repositório** (inserção nas `rows` do bloco `tiktok` do `_panels.yaml`, alinhado aos cabeçalhos do template). | Coordenação humana + edição de `dossier_*_panels.yaml`; não há integração API automática no fluxo atual. |
| **Métricas X (Twitter)** | **Plataforma X**, consulta **manual** no perfil público (navegador ou app). O essencial para o painel: **número de seguidores** e se a conta está **ativa** — ou seja, se a pessoa **ainda usa** o X (posts recentes visíveis) ou se está **parada há muito tempo** (sem uso relevante / última atividade antiga). Não é preciso inventariar todo o conteúdo; basta o que sustenta essas duas leituras + uma **linha de teor recente** (resumo objetivo) na tabela, como nos dossiês já publicados. | Preencher o bloco `x` em **`dossier_*_panels.yaml`** (`headers` + `rows`: costuma haver colunas para seguidores, atividade Sim/Não e resumo do teor). Rodapé do HTML: checagem na data da coleta. |
| **OSINT open source** (suplemento narrativa) | Instaloader, yt-dlp, Sherlock (+ na seção **Mercado**: Maigret, Google News/Alerts, imagem inversa, archive.today, holehe se aplicável). Quando a imprensa não cobre o handle; logs em `research/osint_runs/`. | [Metodologia brand safety](loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md) (seção *Ferramentas open source e fluxo OSINT*), [lista de fontes](loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md), [`tools/requirements-osint.txt`](tools/requirements-osint.txt) |
| **Segundo lote (merge / CSV)** | CSVs, merge de baseline, notas de redes | [`merge_creators_baseline.py`](loterias2026-20260406/scripts/merge_creators_baseline.py), [`data/`](loterias2026-20260406/data/), [`research/`](loterias2026-20260406/research/) |
| **Proxy Trends / Wikipedia** | Penetração mercados (índices relativos; ver limites no README). | [`tools/penetracao_mercados.py`](tools/penetracao_mercados.py), deps em [`tools/requirements-penetracao.txt`](tools/requirements-penetracao.txt), modelo JSON em [`tools/penetracao_entities_example.json`](tools/penetracao_entities_example.json); [README research Embratur](embratur/research/README.md) para o lote de exemplo. |

**Resumo (modo B — qualquer campanha com esta fábrica):** HTML final = `dossier_*.md` + `_panels.yaml` + `build_dossier_completo.py`. **Apify não faz parte do fluxo operacional.** Métricas típicas neste modelo: **Social Blade** (IG/YT) + **Upfluence** (TT) + **X manual**. **OSINT** opcional para narrativa. Caminhos com nomes de produto no repo são **históricos** do primeiro uso deste pipeline.

### Regra: não copiar Markdown para campos errados

- **Onde pode `**` e links `[x](url)`:** parágrafos do briefing (`intro_paragraphs`, `criterios`), blocos `executive_summary` / `consolidated_narrative`, e no **corpo** do perfil: `### Narrativa`, eixos longos, `### Resumo tabela` e células da matriz — o gerador aplica **mini Markdown** (negrito, links).
- **Onde deve ser texto plano:** `meta.title`, `meta.subtitle`, `meta.client_line`, `meta.periodo`, nomes em `briefing.redes`, rótulos `methodology.columns[].label`, **tabelas de painéis** (`_panels.yaml`), e identificadores estruturais (`## Nome`, `- **Camada:**`, handles). Não colar linhas com `##` ou `**` vindas de outras seções para esses campos.
- **Defesa no código:** `tools/dossier_plain.strip_markdown_to_plain()` remove `**`, cabeçalhos `#` e converte links em “texto (URL)” nos campos que são só escape HTML, e normaliza nome/camada/handles ao ler o `.md`, para o HTML do cliente não mostrar lixo literal se alguém colar errado.

## Evolução do método

- **Novo tipo de dossiê** que vá se repetir: considere extrair **template HTML** ou **script de build** para a pasta do projeto (hoje muito do código partilhado já está em [`tools/`](tools/)) e acrescente uma linha na tabela acima.
- **Comandos finos** (variantes `squad_13` / `squad_8`, flags do build): ficam no [README do modo B](loterias2026/README.md); este playbook não substitui esses passos técnicos.
