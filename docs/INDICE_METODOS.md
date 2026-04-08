# Índice de métodos e documentação operacional

Mapa **pergunta → ficheiro**. O **`PLAYBOOK_DOSSIES.md`** na raiz é o **guia geral** para criar qualquer dossiê (modos A/B/C).

**Nota:** `loterias2026/` é a pasta onde o **modo B** (`.md` + gerador) está **implementado de exemplo** — não significa que todo dossiê novo seja “Loterias 2026”. Métodos em `loterias2026/research/` (descoberta de perfis, brand safety) são **reutilizáveis** para outros clientes.

| Se precisas de… | Abre |
|-----------------|------|
| **Guia geral** — modos A/B/C, publicação, toolbox | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) (raiz) |
| **Inventário de todos os blocos HTML** (sumário, pedido, mini-cards redes, eixos, tabelas…) — modo B | [`PLAYBOOK_DOSSIES.md`](../PLAYBOOK_DOSSIES.md) — *Estrutura do HTML final (modo B) — inventário completo* |
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
| Validação fonte `.md` (formato do gerador) | `tools/validate_dossier_source.py` |
| Legado Apify / `run_pipeline` | [`loterias2026/scripts/README_LEGADO.md`](../loterias2026/scripts/README_LEGADO.md) |
