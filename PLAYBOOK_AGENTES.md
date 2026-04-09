# Playbook — camada curta para agentes (Calia BI Reports)

Leia **este arquivo primeiro**; o guia completo está em **`PLAYBOOK_DOSSIES.md`**. Idioma: **pt-BR** (ver `AGENTS.md`).

## Regras primordiais

1. **Dossiê entregue ao cliente** — todo o conteúdo visível em **pt-BR**, salvo o **usuário** pedir outro idioma explicitamente (`PLAYBOOK_DOSSIES.md` → *Idioma do dossiê*).
2. **Redação** — textos finais **humanizados**, **fáceis de entender**, **sucintos** e **completos** para **planejamento, atendimento e cliente** (quem lê costuma não ter feito a pesquisa): sem dúvida sobre conclusão, base e vigência (`PLAYBOOK_DOSSIES.md` → *Qualidade da redação*).
3. **Autocontido + links** — texto completo **sem** precisar abrir o link para entender; **e**, quando houver URL da fonte, **sempre** citar com **hyperlink** (evidência); ver *Documento autocontido e links* no playbook completo.
4. **Briefing incompleto** — perguntar o que faltar nos itens **(E)** e **(C)** do Pipeline §1 do playbook completo; não supor pasta ou modo. **Padrão:** **sempre** gate/senha + **sempre** publicar (commit + push), salvo pedido explícito em contrário — se faltar o **texto da senha** (ou “igual ao dossiê X”), **perguntar**. **Só uma lista de nomes** não basta: ver *Briefing só com nomes de creators ou artistas* em `PLAYBOOK_DOSSIES.md` (após o modelo de briefing).
5. **Anti-vazamento** — no HTML do cliente, **não** citar caminhos do repo (`loterias2026/`, `tools/`, `.md`, `_panels.yaml`). Validar com `python3 tools/check_client_html_leakage.py` antes de publicar.

## Ordem de trabalho (0→7, com 4b)

| # | O quê |
|---|--------|
| 0 | Definir modo **A** (HTML manual), **B** (`.md` + gerador) ou **C** (pesquisa → HTML na mão) a partir do briefing. |
| 1 | Briefing fechado — modelo e checklist em `PLAYBOOK_DOSSIES.md` §1. |
| 2 | Identidade / @ — [METODO descoberta](loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) (atalhos em [`docs/metodos/README.md`](docs/metodos/README.md)). |
| 3 | **B:** par `dossier_*.md` + `dossier_*_panels.yaml` — [`loterias2026/README.md`](loterias2026/README.md), [`examples/minimo/`](examples/minimo/) como modelo mínimo. **A/C:** clonar HTML de referência. |
| 4 | Pesquisa e métricas — [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) (*Coleta de dados*, *Mercado*). |
| 4b | **Síntese crítica** — após a coleta: o que entra, hierarquia, gráficos (se houver), credibilidade; plano em bullets **antes** do build. Ver *Síntese crítica e arquitetura da entrega* no playbook completo. |
| 5 | Build ou edição HTML. |
| 6 | QA — `validate_dossier_source.py` (modo B); opcional `check_dossier_links.py`; **`make qa-dossier-squad-13`** ou `qa-dossier-squad-8`. |
| 7 | Publicar na pasta correta (`caixa/`, `caixa/loterias/`, `embratur/`, …); **nome do `.html`** = padrão `YYYYMMDD-dossie-<slug>.html` (Pipeline §2) — **definido pelo agente**; git conforme `AGENTS.md`. |

## Limites do que o agente faz

- **Não** substitui login humano em Social Blade, Upfluence ou redes fechadas; **não** contorna paywall nem viola ToS em massa.
- Se a plataforma **bloquear** ou os dados não existirem, registrar no dossiê (**“não consta”** / limitação da coleta) com data.
- **OSINT** (Instaloader, etc.) é **opcional** e documentado; falhas de API/redes são esperadas — não inventar números.

## Links rápidos

| Precisa de… | Abrir |
|-------------|--------|
| Índice pergunta → arquivo | [`docs/INDICE_METODOS.md`](docs/INDICE_METODOS.md) |
| Métodos (atalhos na pasta `docs/metodos/`) | [`docs/metodos/README.md`](docs/metodos/README.md) |
| **Exemplos de briefing** (e-mail / texto bruto) | [`docs/EXEMPLOS_BRIEFINGS.md`](docs/EXEMPLOS_BRIEFINGS.md) |
| Playbook completo (cores, gráficos, briefing E/C/O, pastas) | [`PLAYBOOK_DOSSIES.md`](PLAYBOOK_DOSSIES.md) |
| Instruções git / estrutura repo | [`AGENTS.md`](AGENTS.md) |
| OSINT pip | `pip install -r tools/requirements-osint.txt` |
| QA pós-build (referência squad) | `make qa-dossier-squad-13` ou `make qa-dossier-squad-8` |
| Vazamento em HTML publicado | `python3 tools/check_client_html_leakage.py` |
