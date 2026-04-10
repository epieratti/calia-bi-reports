# Vários agentes de IA no mesmo dossiê (sem dar merda)

Objetivo: **paralelizar ou especializar** tarefas **sem** dois modelos sobrescrevendo a mesma coisa, **sem** briefing contraditório e **sem** HTML com vazamento de repo.

---

## Regras que **não** são opcionais

1. **Briefing único e congelado** — Uma issue (**Briefing — novo dossiê**) ou mensagem **fechada** com (E) preenchidos. Se outro agente “reinterpretar” o pedido, para tudo e **alinha com o humano**.
2. **Uma fonte canônica no modo B** — Só existem **`dossier_*.md`** + **`dossier_*_panels.yaml`** como entrada do build. Notas soltas ficam em **`research/`** (ou arquivo por perfil) e **não** substituem o `.md` até alguém **integrar**.
3. **Um integrador** — Idealmente **um** agente (ou você) faz o **merge** das notas no `.md` / painéis e o **commit** final. Vários agentes **escrevendo no mesmo par de arquivos ao mesmo tempo** = conflito e trechos perdidos.
4. **Contrato entre etapas** — Cada agente recebe **entrada explícita** (arquivo, trecho, lista de nomes) e devolve **saída explícita** (novo arquivo ou seção nomeada). Prompt vagão (“melhora o dossiê”) gera retrabalho.
5. **Quem publica** — Só o passo final roda **`dossie-entregar`** / `build` + **`check_client_html_leakage`** + push. Não publicar HTML pela metade.
6. **Anti-vazamento** — Qualquer agente que toque em HTML para cliente: **não** citar `loterias2026/`, `tools/`, `.md`, `_panels.yaml` no texto visível.

---

## Papéis sugeridos (pode colapsar em menos agentes)

| Papel | Foco | Entrada | Saída | Evita |
|-------|------|---------|-------|--------|
| **Coordenador** | Modo A/B/C, plano em bullets, quem faz o quê | Briefing | Plano + lista de arquivos | Dois agentes no mesmo arquivo |
| **Pesquisa / identidade** | @, homônimos, notas, URLs | Nomes + briefing | `research/*.md` ou notas por perfil | Narrativa final no cliente sem passar pelo `.md` |
| **Autor fonte** | Narrativa, eixos, resumo tabela | Notas + método | Atualiza **`dossier_*.md`** (+ painéis se couber) | Editar o mesmo `## Nome` em paralelo com outro agente |
| **Métricas** | `_panels.yaml`, SB/Upfluence/X | Handles confirmados | **`_panels.yaml`** só | Misturar narrativa longa no YAML |
| **QA** | Validador, hints, links, leakage | `.md` pronto + HTML gerado | Relatório de correções; **não** reescrever tudo | “Só confiar” sem rodar `validate` |

Ordem típica: **Coordenador → Pesquisa → Autor (+ Métricas pode ser paralelo se arquivos diferentes) → build → QA → publicação**.

---

## Paralelo **seguro**

- **Por perfil:** cada agente trabalha **só** em `research/NOME.md` ou num **único** bloco `## Nome` acordado — o **Autor** junta depois.
- **Pesquisa vs métricas:** notas em `research/` **enquanto** outro preenche `_panels.yaml` — **desde que** o Autor una tudo antes do build.
- **Não fazer:** dois chats editando o **mesmo** `dossier_*.md` sem turnos.

---

## Prompt mínimo de “passagem de bastão”

Cole no próximo agente:

```
Briefing: [link issue ou resumo fixo]
Modo: B. Arquivos canônicos: [caminho dossier_*.md] + [*_panels.yaml].
O agente anterior deixou em: [research/... ou seções já prontas].
Não alteres [lista do que está fechado]. Tua tarefa só: [uma frase].
Segue AGENTS.md + PLAYBOOK_AGENTES.md. Não commites se outro agente for integrar.
```

Mais modelos em [`PROMPTS_IA_AGENTES.md`](PROMPTS_IA_AGENTES.md).

---

## Quando **não** vale multiagente

- Dossiê **curto** (1–3 perfis) — um fluxo só costuma ser mais rápido.
- Briefing **ainda em aberto** — primeiro fecha (E), depois divide trabalho.

---

## Automação que já ajuda (não é “agente”, mas reduz risco)

- `python3 tools/validate_dossier_source.py --hints <dossier.md>`
- `make dossie-entregar` / `check_client_html_leakage.py`
- CI em `dossier_*.md` no GitHub

Isto **não substitui** o integrador humano ou o agente que fecha o `.md`.
