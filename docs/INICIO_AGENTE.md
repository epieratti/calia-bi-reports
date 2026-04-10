# Início rápido — novo agente neste repositório

Use este arquivo quando **abrir um agente novo** no **calia-bi-reports**. Idioma de trabalho com o humano: **pt-BR**.

---

## 1. Ordem de leitura (máx. 5 minutos)

| Ordem | Arquivo | Para quê |
|-------|---------|----------|
| 1 | **[`PLAYBOOK_AGENTES.md`](../PLAYBOOK_AGENTES.md)** | Regras, fluxo 0→7, links |
| 2 | **[`docs/PRIMEIRO_DIA.md`](PRIMEIRO_DIA.md)** | Checklist modo B ponta a ponta |
| 3 | Se o pedido for solto | **[`docs/PROMPTS_IA_AGENTES.md`](PROMPTS_IA_AGENTES.md)** §1 |

**Não precisa ler tudo antes de agir:** leia o **PLAYBOOK_AGENTES** e **pergunte** o que faltar no briefing (itens **E** em `PLAYBOOK_DOSSIES.md` §1).

---

## 2. Como “dar start” no pipeline (primeira mensagem)

Cole **adaptando** o bloco abaixo na conversa com o agente (ou peça ao humano para colar):

```text
Repositório: calia-bi-reports. Segue PLAYBOOK_AGENTES.md e AGENTS.md (pt-BR).

[BRIEFING OU PEDIDO DO HUMANO — colar aqui]

Tarefas:
1. Dizer se o briefing está completo nos itens (E)/(C); se faltar, perguntar antes de pesquisar pesado.
2. Propor modo A, B ou C e o plano em 5–7 bullets (arquivos que vai tocar).
3. Só depois executar: descoberta de @ se preciso → fonte .md + _panels.yaml (modo B) → validar → build → publicação conforme AGENTS.md.

Para blindagem forte, use também o bloco **CONTRATO** da seção 7 deste arquivo.
```

Se **não houver briefing**, o agente deve **pedir** cliente, objetivo, lista de perfis, pasta de publicação e **referência de senha** (não inventar) — ver issue template **Briefing — novo dossiê** no GitHub.

---

## 3. Atalhos por tipo de pedido

| Situação | O que fazer |
|----------|-------------|
| **Novo dossiê modo B** | `docs/PRIMEIRO_DIA.md` + `loterias2026/scripts/new_creator_dossier.py` ou copiar `dossier_TEMPLATE.md` |
| **Só texto bruto do cliente** | Prompt §1 em `PROMPTS_IA_AGENTES.md` |
| **Vários agentes** | `docs/MULTI_AGENTES.md` — um integrador, briefing único |
| **Senha / PDF / validar no ar** | `docs/GOVERNANCA_ENTREGA.md` |
| **Qualidade / prova por eixo** | `docs/CALIBRAGEM_QUALIDADE.md` + `quality_calibration` no front matter |
| **Entrega automatizada** | `make dossie-entregar MD=… DEST=…` (ver `make help`) |

---

## 4. Comandos que o agente costuma rodar (raiz do repo)

```bash
make help
python3 tools/validate_dossier_source.py --hints caminho/dossier_*.md
make dossie-entregar MD=... DEST=caixa/loterias   # exemplo
python3 tools/check_client_html_leakage.py caixa embratur
```

---

## 5. Onde está o “cérebro” longo

- Referência completa: **[`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md)**
- Índice pergunta → arquivo: **[`docs/INDICE_METODOS.md`](INDICE_METODOS.md)**
- Git e estrutura: **[`AGENTS.md`](../AGENTS.md)**

**Resumo de uma linha:** abra **`PLAYBOOK_AGENTES.md`**, cole o briefing com o template da seção 2, e siga o plano que o agente devolver antes de build pesado.

---

## 6. Briefing sozinho: o agente “starta” o pipeline?

**Sim**, desde que o briefing venha **acompanhado do contrato** (seção 7 ou 2). Sem isso, o modelo pode **pular** checagem de (E)/(C) ou ir direto para pesquisa/HTML.

**Blindagem (o que funciona de verdade):**

| Medida | Efeito |
|--------|--------|
| **Colar o bloco CONTRATO** (abaixo) **antes ou depois** do briefing em toda mensagem de pedido | O agente tem instrução explícita de **fases** e **proibições** até fechar o plano. |
| **Duas mensagens** (opcional) | 1ª: briefing + contrato → o agente só devolve **lacunas + plano**. 2ª: *“Executa o plano.”* → aí sim edita arquivos / pesquisa pesada. |
| **Regra no `AGENTS.md` / `PLAYBOOK_AGENTES.md`** | Agentes do Cursor costumam ler — reforça o mesmo contrato. |

Não existe garantia **técnica** 100% (LLM pode desobedecer); o contrato + duas mensagens reduz muito o desvio.

---

## 7. CONTRATO DE EXECUÇÃO — colar junto ao briefing (modo estrito)

Cole **este bloco inteiro** imediatamente antes ou depois do texto do briefing:

```text
=== CONTRATO calia-bi-reports (obrigatório) ===
Repositório: calia-bi-reports. Idioma com o usuário: pt-BR.
Seguir nesta ORDEM. Não pular fases. Não substituir o playbook por “atalho” próprio.

FASE 1 — Abrir mentalmente: docs/INICIO_AGENTE.md + PLAYBOOK_AGENTES.md.
FASE 2 — Briefing: checar itens (E) e (C) de PLAYBOOK_DOSSIES.md §1. Se faltar algo essencial, LISTAR perguntas e PARAR (sem pesquisa pesada, sem criar dossier_*.md novo substancial, sem build).
FASE 3 — Na MESMA conversa, PRIMEIRO output visível: (a) “Briefing: fechado OU lacunas: …” (b) Modo A/B/C (c) Plano em 5–7 bullets com caminhos de arquivo previstos.
FASE 4 — Só depois do bloco (a)(b)(c): executar pesquisa, descoberta de @, edição de .md / _panels.yaml, validate, build, leakage, git conforme AGENTS.md.

PROIBIDO antes de entregar (a)(b)(c): inventar pasta de publicação ou senha; publicar HTML sem plano visível; migrar tudo para YAML monolítico; ignorar validate_dossier_source no modo B.

Se o usuário escrever só “executa” numa segunda mensagem, retomar a partir da FASE 4 usando o plano já acordado.
=== fim do contrato ===
```

**Briefing do cliente:** (cole abaixo do contrato)
