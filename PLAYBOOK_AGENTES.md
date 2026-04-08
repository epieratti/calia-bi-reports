# Playbook — camada curta para agentes (Calia BI Reports)

Leia **este arquivo primeiro**; o guia completo está em **`PLAYBOOK_DOSSIES.md`**. Idioma: **pt-BR** (ver `AGENTS.md`).

## Regras primordiais

1. **Dossiê entregue ao cliente** — todo o conteúdo visível em **pt-BR**, salvo o **usuário** pedir outro idioma explicitamente (`PLAYBOOK_DOSSIES.md` → *Idioma do dossiê*).
2. **Briefing incompleto** — perguntar o que faltar nos itens **(E)** e **(C)** do Pipeline §1 do playbook completo; não supor pasta, senha ou push.
3. **Anti-vazamento** — no HTML do cliente, **não** citar caminhos do repo (`loterias2026/`, `tools/`, `.md`, `_panels.yaml`). Validar com `python3 tools/check_client_html_leakage.py` antes de publicar.

## Ordem de trabalho (0→7)

| # | O quê |
|---|--------|
| 0 | Definir modo **A** (HTML manual), **B** (`.md` + gerador) ou **C** (pesquisa → HTML na mão) a partir do briefing. |
| 1 | Briefing fechado — modelo e checklist em `PLAYBOOK_DOSSIES.md` §1. |
| 2 | Identidade / @ — [METODO descoberta](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) (atalhos em [`docs/metodos/README.md`](docs/metodos/README.md)). |
| 3 | **B:** par `dossier_*.md` + `dossier_*_panels.yaml` — [`loterias2026/README.md`](loterias2026/README.md), [`examples/minimo/`](examples/minimo/) como modelo mínimo. **A/C:** clonar HTML de referência. |
| 4 | Pesquisa e métricas — [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) (*Coleta de dados*, *Mercado*). |
| 5 | Build ou edição HTML. |
| 6 | QA — `validate_dossier_source.py` (modo B); opcional `check_dossier_links.py`; **`make qa-dossier-squad-13`** ou `qa-dossier-squad-8`. |
| 7 | Publicar na pasta correta (`caixa/`, `caixa/loterias/`, `embratur/`, …) — ver Pipeline §2 do playbook completo; git conforme `AGENTS.md`. |

## Limites do que o agente faz

- **Não** substitui login humano em Social Blade, Upfluence ou redes fechadas; **não** contorna paywall nem viola ToS em massa.
- Se a plataforma **bloquear** ou os dados não existirem, registrar no dossiê (**“não consta”** / limitação da coleta) com data.
- **OSINT** (Instaloader, etc.) é **opcional** e documentado; falhas de API/redes são esperadas — não inventar números.

## Links rápidos

| Precisa de… | Abrir |
|-------------|--------|
| Índice pergunta → arquivo | [`docs/INDICE_METODOS.md`](docs/INDICE_METODOS.md) |
| Métodos (atalhos na pasta `docs/metodos/`) | [`docs/metodos/README.md`](docs/metodos/README.md) |
| Playbook completo (cores, gráficos, briefing E/C/O, pastas) | [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) |
| Instruções git / estrutura repo | [`AGENTS.md`](AGENTS.md) |
| OSINT pip | `pip install -r tools/requirements-osint.txt` |
| QA pós-build (referência squad) | `make qa-dossier-squad-13` ou `make qa-dossier-squad-8` |
| Vazamento em HTML publicado | `python3 tools/check_client_html_leakage.py` |
