# Índice de métodos e documentação operacional

Mapa **pergunta → arquivo**. O **`PLAYBOOK_DOSSIES.md`** na raiz é o **guia geral** para criar dossiês (modos A/B/C), com foco em **brand safety / vetting / disaster check** de creators; outros formatos usam o mesmo fluxo com adaptação. Texto deste índice em **pt-BR** (alinhado a `AGENTS.md`).

**Nota:** `loterias2026/` é a pasta onde o **modo B** (`.md` + gerador) está **implementado de exemplo** — não significa que todo dossiê novo seja “Loterias 2026”. Métodos em `loterias2026/research/` (descoberta de perfis, brand safety) são **reutilizáveis** para outros clientes.

| Se você precisa de… | Abre |
|-----------------|------|
| **Início / start do pipeline** + **CONTRATO** (blindagem com briefing) | [`docs/tutorials/INICIO_AGENTE.md`](INICIO_AGENTE.md) |
| **Guia curto para agentes** (ler em seguida) | [`PLAYBOOK_AGENTES.md`](../PLAYBOOK_AGENTES.md) (raiz) |
| **Primeiro dia** — checklist modo B | [`docs/tutorials/PRIMEIRO_DIA.md`](PRIMEIRO_DIA.md) |
| **Prompts** para agentes de IA | [`docs/PROMPTS_IA_AGENTES.md`](PROMPTS_IA_AGENTES.md) |
| **Vários agentes** — papéis, paralelo seguro, anti-merda | [`docs/how-to/MULTI_AGENTES.md`](MULTI_AGENTES.md) |
| **Governança** — senha, validar vendo no Pages, PDF, escalação | [`docs/how-to/GOVERNANCA_ENTREGA.md`](GOVERNANCA_ENTREGA.md) |
| **Inventário** — dossiês publicados (modo A/B, fonte, URL) | [`docs/reference/INVENTARIO_DOSSIES.md`](INVENTARIO_DOSSIES.md) |
| **Calibragem de qualidade** — prova por eixo, confiança, delta, institucional | [`docs/explanation/CALIBRAGEM_QUALIDADE.md`](CALIBRAGEM_QUALIDADE.md) |
| **PDF do dossiê** — metodologia (Playwright, Chart.js, QA) | [`docs/how-to/METODO_PDF_DOSSIE.md`](METODO_PDF_DOSSIE.md) |
| **PDF** — script e flags | [`engine/cli/export_pdf.py`](../engine/cli/export_pdf.py), `make dossie-pdf` |
| **Template GitHub** — issue de briefing | [`.github/ISSUE_TEMPLATE/dossier-briefing.yml`](../.github/ISSUE_TEMPLATE/dossier-briefing.yml) |
| **Guia completo** — modos A/B/C, publicação, toolbox | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) (raiz) |
| **Métodos** — atalhos (descoberta, brand safety, fontes) | [`methods/README.md`](metodos/README.md) |
| **Exemplo mínimo** modo B (1 perfil) | [`projects/_template/README.md`](../projects/_template/README.md) |
| **Idioma** — dossiê sempre **pt-BR** (exceto se o **usuário** pedir outro) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Idioma do dossiê* |
| **Redação** — humanizado, claro, sucinto, completo (público: planejamento, atendimento, cliente) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Qualidade da redação* |
| **Links** — autocontido + **hyperlink obrigatório** quando houver URL da fonte | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Documento autocontido e links* |
| **Disaster check — mapa de ferramentas** (onde está cada coisa no playbook) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Disaster check / brand safety — ferramentas* |
| **Inventário de pesquisa** + extras sem API (Maigret, News, imagem inversa…) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Coleta de dados* + *Mercado* |
| **Modelo de briefing** — (E)/(C)/(O) essencial/condicional/opcional + template | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Pipeline §1 — Perguntas / Modelo* |
| **Padrão Calia** — **sempre** senha no gate + **sempre** commit/push (Pages); só perguntar o **valor** da senha se faltar | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Para o agente de IA* (lacunas) + *Acesso (senha)* / *Publicação (git)* na tabela §1 |
| **Só nomes na lista** — o que ainda falta além de descobrir @ (cliente, profundidade, métricas, homônimos) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Briefing só com nomes de creators ou artistas* |
| **Exemplos de briefing reais** (padrões squad, delta, casting, Docs, mínimo) | [`EXEMPLOS_BRIEFINGS.md`](EXEMPLOS_BRIEFINGS.md) |
| **Pasta** de publicação + **padrão de nome** do `.html` (`YYYYMMDD-dossie-<slug>.html`, nome definido pelo agente) | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Pipeline §2 — Nomenclatura / Pastas* |
| **Etapas para o agente** — 0→7 + **4b síntese crítica** após coleta | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Fluxo em etapas* + *Síntese crítica e arquitetura da entrega* |
| **Inventário de todos os blocos HTML** (sumário, pedido, mini-cards redes, eixos, tabelas…) — modo B | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Estrutura do HTML final (modo B) — inventário completo* |
| **Esquema de cores** — tokens Calia, neutros, risco, redes, gráficos | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Esquema de cores* |
| **Mercado** — metodologia típica BI/creator audit; ferramentas gratuitas/OSINT | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Mercado: metodologia típica* |
| **Tipos de gráfico** — qual usar em cada caso; Chart.js; panorama ECharts/Vega-Lite/D3; modo B sem charts | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Gráficos* |
| **Barra de progresso (%)** — quando usar (score, cobertura); não é Chart.js | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Barras de progresso* |
| Descobrir IG/TT/YT/X a partir de **só nome** ou **nome + um @** | [`methods/discovery/METODO_DESCOBERTA_PERFIS.md`](../methods/discovery/METODO_DESCOBERTA_PERFIS.md) |
| Brand safety, busca aberta, OSINT (ex.: yt-dlp, Sherlock) | [`methods/brand-safety/METODO_BRAND_SAFETY.md`](../methods/brand-safety/METODO_BRAND_SAFETY.md) |
| Tabela de evidências e URLs (exemplo de entrega passada) | [`loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md`](../loterias2026/research/FONTES_BRAND_SAFETY_LOTERIAS2026.md) |
| **Implementação modo B** — `new_creator_dossier`, `build`, template, publish Caixa | [`projects/caixa/loterias/always-on-20260401/README.md`](../projects/caixa/loterias/always-on-20260401/README.md) |
| Segundo lote no **mesmo** modelo (8 perfis): inventário pesquisa + build | [`projects/caixa/loterias/always-on-20260406/README.md`](../projects/caixa/loterias/always-on-20260406/README.md) |
| HTML publicado Caixa, senhas, índice | [`caixa/README.md`](../caixa/README.md) |
| Embratur + script Trends/Wikipedia | [`embratur/research/README.md`](../embratur/research/README.md) |
| URLs do site e Pages | [`README.md`](../README.md) (raiz) |
| Instruções para agentes / git | [`AGENTS.md`](../AGENTS.md) |
| Motor HTML + parser `.md` (modo B) | `tools/dossier_render.py`, `tools/md_dossier_source.py` |
| **OSINT pip** (qualquer cliente) | [`engine/requirements/osint.txt`](../engine/requirements/osint.txt) |
| **Trends + Wikipedia** (qualquer cliente) | [`engine/research/penetracao_mercados.py`](../engine/research/penetracao_mercados.py), [`tools/requirements-penetracao.txt`](../tools/requirements-penetracao.txt) |
| Validação fonte `.md` (formato do gerador) | `engine/qa/validate_source.py` |
| **Dicas semânticas** (lacunas, painéis, links) — `--hints` / `--strict-hints` | `python3 engine/qa/validate_source.py --hints <dossier.md>` |
| **QA** — validate + links + build + vazamento HTML | `make qa-dossier-squad-13` ou `make qa-dossier-squad-8` |
| **Vazamento** em HTML (caminhos repo no texto visível) | [`engine/qa/check_html_leakage.py`](../engine/qa/check_html_leakage.py) |
| **Nome automático** `YYYYMMDD-dossie-<slug>.html` + **pipeline** validar→build→pasta Pages | [`engine/cli/html_filename.py`](../engine/cli/html_filename.py), [`engine/cli/publish_dossier.py`](../engine/cli/publish_dossier.py), `make dossie-filename` / `make dossie-entregar` |
| Legado Apify / `run_pipeline` | [`loterias2026/scripts/legado/README_LEGADO.md`](../loterias2026/scripts/legado/README_LEGADO.md) |
