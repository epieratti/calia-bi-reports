# Brand safety — Loterias Caixa (squad 06/04/2026)

**Metodologia:** fontes públicas (busca web + dados já consolidados no lote). **Data desta ronda:** 2026-04-06.  
**Não substitui** due diligence jurídica nem declaração de exclusividade da agência/creator.  
**Ficha narrativa completa por perfil** (parcerias, riscos, política, referências): [`SQUAD_FICHA_COMPLETA.md`](SQUAD_FICHA_COMPLETA.md).

## Complemento (2026-04-06 — 2.ª passagem)

- **YouTube RSS:** todos os `channel_id` úteis em [`data/youtube_handles_verificados.csv`](../data/youtube_handles_verificados.csv) foram consultados via feed público (inclui `@julia_ferrari`, `@juliaferraric`, canais sem vídeo recente no feed aparecem como `feed sem entry` ou último vídeo antigo). Ver [`data/youtube_rss_recent.csv`](../data/youtube_rss_recent.csv).
- **Busca loteria concorrente (Mega-Sena / Lotofácil + nome):** ronda adicional — [`data/busca_loteria_complementar.csv`](../data/busca_loteria_complementar.csv).
- **Nome + bet (auditoria):** uma linha por creator com **query literal**, data e resultado — [`data/busca_nome_bet.csv`](../data/busca_nome_bet.csv).
- **Merge tabular:** script [`scripts/merge_creators_baseline.py`](../scripts/merge_creators_baseline.py) gera [`data/creators_master_rebuild.csv`](../data/creators_master_rebuild.csv) a partir dos CSVs (reproduzível).
- **2.º recorte Social Blade / Upfluence (delta temporal):** não executado — comparar manualmente com capturas futuras usando as mesmas tabelas.

## Resumo executivo

| Perfil | Aposta / loteria concorrente (evidência pública) | Política / exposição | Política partidária (filiação) |
|--------|--------------------------------------------------|----------------------|--------------------------------|
| **julia_ferrari** | Não encontrada publi bet | Não encontrada | Não encontrada |
| **joaovitormello** | Não encontrada publi bet | Não encontrada | Não encontrada |
| **rufislore** | Não encontrada | Não encontrada | Não encontrada |
| **barbaracoura** | Sem publi bet; **esquetes humor** com tema “tia que aposta” (sátira) — ver `apostas_loterias_historico.csv` | Não encontrada | Não encontrada |
| **raphaelvicente** | Não encontrada | **Exposição:** relato em mídia sobre **operação policial na Maré** (2023) — defesa comunitária; ver evidências | Não encontrada |
| **rafaelsaraiva28** | Sketch **"Bet Kids"** (Porta dos Fundos) — **humor**, não publi de casa de apostas; pode ser sensível ao cliente. | Declaração na imprensa sobre **não** se alinhar à **extrema-direita** (Veja) | Não encontrada |
| **pedroottoni_** | Não encontrada | **Não confundir** com **Otoni de Paula** (notícias PSD 2026) | Não atribuir ao ator |
| **ademara** | Não encontrada | **Encontro** com **Lula** / influenciadores (2023) — evento de governo; **não** é filiação partidária | Não encontrada |

## Matriz (eixos)

| Eixo | Conteúdo | Associação | Notícias | Identidade |
|------|----------|------------|----------|------------|
| **Leitura** | Apostas/loteria: Bárbara (sátira “tia que aposta”); Rafael (sketch “Bet Kids”) — ambos humor, não publi bet | Collabs de marcas: ver `parcerias_marcas.csv` | Polêmicas: Raphael (Maré); Rafael (assaltos); Rafael (entrevista) | Handles em `TIKTOK_PERFIS.md` / `X_PERFIS.md` |

## Risco de associação (rede)

- **X:** maior parte dos perfis **não confirmada** ou **inativa** — ver `X_PERFIS.md`.
- **TikTok:** métricas Upfluence em `upfluence_tiktok_audit.csv`.

## Recomendações para o cliente

1. **Ademara:** avaliar **sensibilidade** de campanha institucional se o cliente quiser **neutralidade política** estrita (encontro com governo é **fato público**, não filiação).
2. **Rafael Saraiva:** posicionamento **ideológico** em entrevista — alinhar com guideline de **imparcialidade** da marca.
3. **Pedro Ottoni:** manter **separação** de homónimos políticos nas buscas.

## Artefatos

- [`data/apostas_loterias_historico.csv`](../data/apostas_loterias_historico.csv)
- [`data/parcerias_marcas.csv`](../data/parcerias_marcas.csv)
- [`data/brand_safety_evidencias.csv`](../data/brand_safety_evidencias.csv)
- [`data/creators_master.csv`](../data/creators_master.csv)
- [`data/youtube_rss_recent.csv`](../data/youtube_rss_recent.csv) (RSS completo por UC)
- [`data/busca_loteria_complementar.csv`](../data/busca_loteria_complementar.csv)
- [`data/busca_nome_bet.csv`](../data/busca_nome_bet.csv)
- [`data/creators_master_rebuild.csv`](../data/creators_master_rebuild.csv)
- [`scripts/merge_creators_baseline.py`](../scripts/merge_creators_baseline.py)
- [`research/google_alerts_sugestoes.md`](google_alerts_sugestoes.md)
- [`research/fontes_referencia_gemini.md`](fontes_referencia_gemini.md)
- [`research/SQUAD_FICHA_COMPLETA.md`](SQUAD_FICHA_COMPLETA.md)
