# Playbook — camada curta para agentes (Calia BI Reports)

**Primeiro contato com o repo:** [`docs/tutorials/INICIO_AGENTE.md`](docs/tutorials/INICIO_AGENTE.md) (start do pipeline + texto para colar no chat).

Leia **este arquivo em seguida**; o guia completo está em **`PLAYBOOK_DOSSIES.md`**. Idioma: **pt-BR** (ver `AGENTS.md`). Checklist curto: [`docs/tutorials/PRIMEIRO_DIA.md`](docs/tutorials/PRIMEIRO_DIA.md). Prompts prontos para colar no chat: [`docs/reference/PROMPTS_IA_AGENTES.md`](docs/reference/PROMPTS_IA_AGENTES.md). Briefing via GitHub: **New issue → Briefing — novo dossiê** (senha: ver governança). **Governança / PDF / validação no ar:** [`docs/how-to/GOVERNANCA_ENTREGA.md`](docs/how-to/GOVERNANCA_ENTREGA.md). **Metodologia PDF (HTML → PDF, Chart.js):** [`docs/how-to/METODO_PDF_DOSSIE.md`](docs/how-to/METODO_PDF_DOSSIE.md). **Vários agentes no mesmo pedido:** [`docs/how-to/MULTI_AGENTES.md`](docs/how-to/MULTI_AGENTES.md) — briefing único, um integrador, contrato entre etapas.

## Regras primordiais

0. **Ao receber um briefing (texto do usuário):** **não** iniciar pesquisa pesada, **não** criar `dossier_*.md` substancial **nem** build até (1) checar **(E)/(C)** em `PLAYBOOK_DOSSIES.md` §1 — se faltar, **perguntar**; (2) devolver **modo A/B/C** + **plano em 5–7 bullets** com arquivos; (3) **só então** executar. O usuário pode reforçar com o bloco **CONTRATO** em [`docs/tutorials/INICIO_AGENTE.md`](docs/tutorials/INICIO_AGENTE.md) §7. **Proibido** inventar pasta, senha ou “atalho” que ignore o playbook.

1. **Dossiê entregue ao cliente** — todo o conteúdo visível em **pt-BR**, salvo o **usuário** pedir outro idioma explicitamente (`PLAYBOOK_DOSSIES.md` → *Idioma do dossiê*).
2. **Redação** — textos finais **humanizados**, **fáceis de entender**, **sucintos** e **completos** para **planejamento, atendimento e cliente** (quem lê costuma não ter feito a pesquisa): sem dúvida sobre conclusão, base e vigência (`PLAYBOOK_DOSSIES.md` → *Qualidade da redação*).
3. **Autocontido + links** — texto completo **sem** precisar abrir o link para entender; **e**, quando houver URL da fonte, **sempre** citar com **hyperlink** (evidência); ver *Documento autocontido e links* no playbook completo.
4. **Briefing incompleto** — perguntar o que faltar nos itens **(E)** e **(C)** do Pipeline §1 do playbook completo; não supor pasta ou modo. **Padrão:** **sempre** gate/senha + **sempre** publicar (commit + push), salvo pedido explícito em contrário — se faltar o **texto da senha** (ou “igual ao dossiê X”), **perguntar**. **Só uma lista de nomes** não basta: ver *Briefing só com nomes de creators ou artistas* em `PLAYBOOK_DOSSIES.md` (após o modelo de briefing).
5. **Anti-vazamento** — no HTML do cliente, **não** citar caminhos do repo (`projects/caixa/loterias/always-on-20260401/`, `engine/`, `.md`, `_panels.yaml`). Validar com `python3 engine/qa/check_html_leakage.py` antes de publicar.
6. **Multiagente** — se mais de um agente atuar no mesmo dossiê: **não** editar o mesmo `dossier_*.md` em paralelo sem acordo; **um** integrador junta notas → fonte canônica; ver [`docs/how-to/MULTI_AGENTES.md`](docs/how-to/MULTI_AGENTES.md).

## Ordem de trabalho (0→7, com 4b)

| # | O quê |
|---|--------|
| 0 | Definir modo **A** (HTML manual), **B** (`.md` + gerador) ou **C** (pesquisa → HTML na mão) a partir do briefing. |
| 1 | Briefing fechado — modelo e checklist em `PLAYBOOK_DOSSIES.md` §1. |
| 2 | Identidade / @ — [METODO descoberta](methods/discovery/METODO_DESCOBERTA_PERFIS.md) (atalhos em [`methods/README.md`](methods/README.md)). |
| 3 | **B:** par `dossier_*.md` + `dossier_*_panels.yaml` — [`projects/caixa/loterias/always-on-20260401/README.md`](projects/caixa/loterias/always-on-20260401/README.md), [`projects/_template/`](projects/_template/) como modelo mínimo. **A/C:** clonar HTML de referência. |
| 4 | Pesquisa e métricas — [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) (*Coleta de dados*, *Mercado*). |
| 4b | **Síntese crítica** — após a coleta: o que entra, hierarquia, gráficos (se houver), credibilidade; plano em bullets **antes** do build. Ver *Síntese crítica e arquitetura da entrega* no playbook completo. |
| 5 | Build ou edição HTML. |
| 6 | QA — `engine/qa/validate_source.py` (modo B; `--hints` para calibragem/vagueza); opcional `engine/qa/check_links.py`; passo **advogado do diabo** por perfil de risco (`docs/explanation/CALIBRAGEM_QUALIDADE.md`); **`make qa-dossier-squad-13`** ou `qa-dossier-squad-8`. |
| 7 | Publicar na pasta correta (`caixa/`, `caixa/loterias/`, `embratur/`, …); **nome do `.html`** = padrão `YYYYMMDD-dossie-<slug>.html` (Pipeline §2) — **definido pelo agente**; git conforme `AGENTS.md`. |

## Limites do que o agente faz

- **Não** substitui login humano em Social Blade, Upfluence ou redes fechadas; **não** contorna paywall nem viola ToS em massa.
- Se a plataforma **bloquear** ou os dados não existirem, registrar no dossiê (**“não consta”** / limitação da coleta) com data.
- **OSINT** (Instaloader, etc.) é **opcional** e documentado; falhas de API/redes são esperadas — não inventar números.

## Links rápidos

| Precisa de… | Abrir |
|-------------|--------|
| Índice pergunta → arquivo | [`docs/reference/INDICE_METODOS.md`](docs/reference/INDICE_METODOS.md) |
| Métodos reutilizáveis | [`methods/README.md`](methods/README.md) |
| **Exemplos de briefing** (e-mail / texto bruto) | [`docs/how-to/EXEMPLOS_BRIEFINGS.md`](docs/how-to/EXEMPLOS_BRIEFINGS.md) |
| Playbook completo (cores, gráficos, briefing E/C/O, pastas) | [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) |
| Instruções git / estrutura repo | [`AGENTS.md`](AGENTS.md) |
| OSINT pip | `pip install -r engine/requirements/osint.txt` |
| QA pós-build (referência squad) | `make qa-dossier-squad-13` ou `make qa-dossier-squad-8` |
| Nome `.html` + entrega num comando | `make dossie-filename MD=…` / `make dossie-entregar MD=… DEST=…` (ver `make help`) |
| Vazamento em HTML publicado | `python3 engine/qa/check_html_leakage.py` |
| Vários agentes sem conflito | [`docs/how-to/MULTI_AGENTES.md`](docs/how-to/MULTI_AGENTES.md) |
| PDF após gate | [`docs/how-to/METODO_PDF_DOSSIE.md`](docs/how-to/METODO_PDF_DOSSIE.md) · `make dossie-pdf` · [`docs/how-to/GOVERNANCA_ENTREGA.md`](docs/how-to/GOVERNANCA_ENTREGA.md) |
