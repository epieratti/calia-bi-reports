# Índice de métodos e documentação operacional

Mapa **pergunta → arquivo**. O **`PLAYBOOK_DOSSIES.md`** na raiz é o **guia geral** para criar dossiês (modos A/B/C), com foco em **brand safety / vetting / disaster check** de creators; outros formatos usam o mesmo fluxo com adaptação. Texto deste índice em **pt-BR** (alinhado a `AGENTS.md`).

**Nota:** `loterias2026/` é a pasta onde o **modo B** (`.md` + gerador) está **implementado de exemplo** — não significa que todo dossiê novo seja “Loterias 2026”. Métodos em `loterias2026/research/` (descoberta de perfis, brand safety) são **reutilizáveis** para outros clientes.

| Se precisas de… | Abre |
|-----------------|------|
| **Guia curto para agentes** (ler primeiro) | [`PLAYBOOK_AGENTES.md`](../PLAYBOOK_AGENTES.md) (raiz) |
| **Guia completo** — modos A/B/C, publicação, toolbox | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) (raiz) |
| **Métodos** — atalhos (descoberta, brand safety, fontes) | [`docs/metodos/README.md`](metodos/README.md) |
| **Exemplo mínimo** modo B (1 perfil) | [`examples/minimo/README.md`](../examples/minimo/README.md) |
| **Idioma** — dossiê sempre **pt-BR** (exceto se o **usuário** pedir outro) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Idioma do dossiê* |
| **Disaster check — mapa de ferramentas** (onde está cada coisa no playbook) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Disaster check / brand safety — ferramentas* |
| **Inventário de pesquisa** + extras sem API (Maigret, News, imagem inversa…) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Coleta de dados* + *Mercado* |
| **Modelo de briefing** — (E)/(C)/(O) essencial/condicional/opcional + template | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Pipeline §1 — Perguntas / Modelo* |
| **Nome do `.html` + pasta** (`caixa/` geral, `caixa/loterias/`, `embratur/`, novo cliente) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Pipeline §2 — Nomenclatura / Pastas* |
| **Etapas para o agente** — 0→7 + **4b síntese crítica** após coleta | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Fluxo em etapas* + *Síntese crítica e arquitetura da entrega* |
| **Inventário de todos os blocos HTML** (sumário, pedido, mini-cards redes, eixos, tabelas…) — modo B | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Estrutura do HTML final (modo B) — inventário completo* |
| **Esquema de cores** — tokens Calia, neutros, risco, redes, gráficos | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Esquema de cores* |
| **Mercado** — metodologia típica BI/creator audit; ferramentas gratuitas/OSINT | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Mercado: metodologia típica* |
| **Tipos de gráfico** — qual usar em cada caso; Chart.js; panorama ECharts/Vega-Lite/D3; modo B sem charts | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Gráficos* |
| **Barra de progresso (%)** — quando usar (score, cobertura); não é Chart.js | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Barras de progresso* |
| Descobrir IG/TT/YT/X a partir de **só nome** ou **nome + um @** | [`loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md`](../loterias2026/research/METODO_DESCOBERTA_PERFIS_CREATORS.md) |
| Brand safety, busca aberta, OSINT (ex.: yt-dlp, Sherlock) | [`loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md`](../loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md) |
| Tabela de evidências e URLs (exemplo de entrega passada) | [`loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md`](../loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md) |
| **Implementação modo B** — `new_creator_dossier`, `build`, template, publish Caixa | [`loterias2026/README.md`](../loterias2026/README.md) |
| Segundo lote no **mesmo** modelo (8 perfis): inventário pesquisa + build | [`loterias2026-20260406/README.md`](../loterias2026-20260406/README.md) |
| HTML publicado Caixa, senhas, índice | [`caixa/README.md`](../caixa/README.md) |
| Embratur + script Trends/Wikipedia | [`embratur/research/README.md`](../embratur/research/README.md) |
| URLs do site e Pages | [`README.md`](../README.md) (raiz) |
| Instruções para agentes / git | [`AGENTS.md`](../AGENTS.md) |
| Motor HTML + parser `.md` (modo B) | `tools/dossier_render.py`, `tools/md_dossier_source.py` |
| **OSINT pip** (qualquer cliente) | [`tools/requirements-osint.txt`](../tools/requirements-osint.txt) |
| **Trends + Wikipedia** (qualquer cliente) | [`tools/penetracao_mercados.py`](../tools/penetracao_mercados.py), [`tools/requirements-penetracao.txt`](../tools/requirements-penetracao.txt) |
| Validação fonte `.md` (formato do gerador) | `tools/validate_dossier_source.py` |
| **QA** — validate + links + build + vazamento HTML | `make qa-dossier-squad-13` ou `make qa-dossier-squad-8` |
| **Vazamento** em HTML (caminhos repo no texto visível) | [`tools/check_client_html_leakage.py`](../tools/check_client_html_leakage.py) |
| Legado Apify / `run_pipeline` | [`loterias2026/scripts/README_LEGADO.md`](../loterias2026/scripts/README_LEGADO.md) |
