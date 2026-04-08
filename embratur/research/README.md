# Pesquisa de penetração (proxy)

## O que foi gerado

- `penetracao_trends_wiki_2026.csv` / `.json` — saída do script genérico [`tools/penetracao_mercados.py`](../../tools/penetracao_mercados.py) (entidades em `penetracao_entities_embratur_2026.json`). O ficheiro `embratur/scripts/penetracao_mercados.py` é *wrapper* que chama o de `tools/`.

## Metodologia (resumo)

1. **Google Trends** (`pytrends`): interesse por país, janela **últimos 12 meses**, idioma **pt-BR**. Valores são **índices relativos** do Trends, não audiência real.
2. **Colunas derivadas** (entre EUA + UK + FR + DE + IT + ES + PT, normalizados para somar 100%):
   - `trends_proxy_pct_US` — share relativa **EUA** nesse conjunto.
   - `trends_proxy_pct_Europa_6` — soma dos outros seis países europeus no mesmo conjunto.
3. **Wikipedia EN**: pageviews **últimos ~90 dias** no artigo encontrado por busca na API (título em `wiki_en_titulo`).

## Limitações

- Trends pode devolver **0** ou volumes estranhos para nomes curtos ou ambíguos; o termo de busca precisa ser **calibrado** (ex.: Júnior usa query descritiva).
- **Djavan** e **Zeca** podem aparecer com **Brasil baixo** no relatório mundial quando o volume absoluto é baixo ou a normalização do Google se comporta de forma opaca — **interpretar com cautela**.
- **Júnior**: o termo que gera volume no Trends (**“Júnior comentarista Globo”**) concentra interesse no **Brasil**; os países EU/Europa listados podem sair **0** — o Trends **não substitui** narrativa de carreira na Itália para esse caso.
- Não substitui Spotify for Artists, YouTube Studio ou dados de mídia paga.

## Como rodar de novo

```bash
# Na raiz do repositório (recomendado — válido para qualquer cliente):
pip install -r tools/requirements-penetracao.txt
python3 tools/penetracao_mercados.py \
  --entities-json embratur/research/penetracao_entities_embratur_2026.json \
  --output-prefix embratur/research/penetracao_trends_wiki_2026

# Atalho (mesmo resultado — delega para tools/):
python3 embratur/scripts/penetracao_mercados.py
```

Para **outro dossiê**, copiar [`tools/penetracao_entities_example.json`](../../tools/penetracao_entities_example.json), preencher `label`, `trend_term`, `wiki_title` e passar `--entities-json` / `--output-prefix` adequados.

Data da última execução no ambiente de desenvolvimento: ver commit / timestamp do arquivo.
