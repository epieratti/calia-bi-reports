# Exemplos de briefings reais (padrões para o agente)

Textos abaixo são **resumos** de pedidos que já chegaram — servem para reconhecer **formato**, **o que costuma faltar** e **qual modo** usar. **Não** copiar parágrafos do cliente para dentro do HTML final sem humanizar; **não** expor links internos do Google Docs no dossiê sem permissão do fluxo de publicação.

---

## Tipo A — Squad com tiers + critérios padrão (brand safety)

**Forma típica:** “Realizar análise de perfil e verificação de histórico…” + três critérios (concorrência, polêmicas, política) + redes IG/TT/YT/X + lista de nomes com **@** agrupados (Big names, Mezzos, Micros, Página).

**O que já vem fechado:** objetivo, critérios, redes, elenco com handles (às vezes com **espaço** no meio do @ — normalizar para o `.md`, ex.: `@indio.behn`).

**O que o agente ainda deve confirmar (se não vier):** cliente/pasta de publicação, senha, push ou não, data do snapshot; se “P - 54 conteúdos” entra no HTML ou só contexto interno.

**Modo:** em geral **B** (`dossier_*.md` + `_panels.yaml`) quando há muitos perfis e o mesmo layout.

---

## Tipo B — Atualização / delta (“novos nomes”)

**Forma típica:** mesmo texto de critérios e redes + bloco **“Novos nomes:”** com lista adicional.

**Leitura:** manter **coerência** com o lote anterior (mesmos critérios, mesma campanha); ou criar **novo** dossiê só com os novos perfis — conforme combinado com o usuário.

**Atenção:** perguntar se é **substituição**, **acréscimo** ao squad existente ou **lote novo** com arquivo/HTML separado.

---

## Tipo C — Viabilidade técnica / dados de casting (menos “eixos de risco”)

**Forma típica:** “Analisar potencial digital e perfil de audiência…” + lista de **atores** (às vezes **só nome**, sem @) + bloco **dados necessários:** alcance, demografia, performance, conteúdo qualitativo.

**Diferença do tipo A:** ênfase em **métricas e demografia**, não só concorrência/polêmica/política — pode exigir **seções ou tabelas** extras, gráficos, ou modo **A** (HTML manual) se o template B não cobrir.

**O que perguntar:** definição de “marca concorrente” para esse cliente (se aplicável); de onde virá demografia (export, estimativa, “não disponível”); formato de entrega (dossiê único por ator vs tabela comparativa).

---

## Tipo D — Briefing + documento externo (Google Docs, PDF)

**Forma típica:** link para **documento** com várias ações; pedido focado em **uma ação** (ex.: levantar **nomes** que atendem perfis e critérios).

**Riscos:** o agente pode **não** ter acesso ao conteúdo do link; o texto do e-mail pode ser só um recorte.

**Fluxo sugerido:** pedir ao usuário **colar no chat** os trechos relevantes da ação **ou** exportar/copy; registrar no `research/` o que foi usado; **não** tratar o link como fonte única sem ler o conteúdo.

**Entrega:** pode ser **lista + fichas** (modo B parcial), **pesquisa estruturada** em Markdown, ou dossiê HTML quando houver perfis fechados para auditar.

---

## Tipo E — Briefing mínimo (só nomes + campanha)

**Forma típica:** uma linha de campanha + bullet com **poucos nomes** (às vezes sem @).

**O que falta quase sempre:** critérios explícitos, redes, pasta, senha, formato — aplicar checklist **(E)/(C)** do `PLAYBOOK_DOSSIES.md` §1.

**Modo:** descoberta de @ pesada ([`METODO_DESCOBERTA_PERFIS_CREATORS.md`](../loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md)); depois A, B ou C conforme quantidade de perfis e profundidade.

---

## Tabela rápida: o que mapear do texto bruto

| Sinal no briefing | Ação do agente |
|-------------------|----------------|
| @ com espaço ou typo | Normalizar handle; confirmar perfil certo |
| “Página digital” / marca | Tratar como perfil **institucional**; métricas e risco podem diferir de pessoa física |
| Só nome de artista | Rodar descoberta de redes antes de prometer painéis |
| Demografia / “audiência EUA” | Declarar fonte ou limitação; não inventar percentuais |
| Link Google Docs | Garantir leitura do trecho; pedir colagem se não houver acesso |
| Mesmos critérios em dois e-mails | Provável **continuação** — alinhar com entrega anterior |

---

## Relação com o modelo formal de briefing

O template com itens **1–16** em `PLAYBOOK_DOSSIES.md` (Pipeline §1) **completa** o que esses e-mails costumam trazer pela metade. Use estes exemplos para **preencher mentalmente** o template e **perguntar** só o que ainda faltar.
