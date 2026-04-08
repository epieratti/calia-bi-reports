# Playbook — dossiês de creators (linha de produção Calia)

Este documento consolida **como** produzir dossiês de brand safety / auditoria de creators de forma repetível, usando o que já funcionou nos lotes Loterias 2026 (13 e 8 perfis), `research/METODO_BRAND_SAFETY_LOTERIAS2026.md` e a entrega HTML com senha no cliente.

## Princípios (experiência acumulada)

1. **Separar narrativa de planilha** — Texto de pesquisa e achados vão no **`.md`** (fácil de escrever e revisar no Git). Números de painéis (Social Blade, Upfluence, etc.) vão no **`_panels.yaml`** (colar/atualizar exportações sem poluir a narrativa).
2. **Um fato, uma prova** — No corpo do perfil ou em `research/`, preferir **[rótulo](URL)** no Markdown; evitar afirmação forte sem link. Ver regras em `research/METODO_BRAND_SAFETY_LOTERIAS2026.md`.
3. **Desambiguação** — Nome + @ + contexto; registrar homônimos descartados na **Narrativa** ou no eixo relevante (ex.: “não é a Julia do O Tempo”).
4. **“Não consta”** — Significa “não achamos nas fontes deste trabalho”, não “não existe”. Deixar explícito no briefing quando necessário.
5. **Concorrência (bets/loterias)** — Separar publi/contrato de menção temática, humor, personagem, curso com “bet” no nome (ler a página).
6. **Snapshot** — `meta.periodo` e notas nos painéis com **data da coleta**; números envelhecem rápido.
7. **Entrega** — HTML em `caixa/` é o que o **GitHub Pages** serve; gerar com o script e **copiar** de `output/` (ou `publish_to_caixa.sh` apontando para o arquivo certo).

## Pipeline em 5 fases

### Fase 0 — Briefing fechado

- Cliente, campanha, **quantidade de nomes**, redes em escopo, **critérios** (concorrência / polêmica / política ou equivalente).
- **Camadas** (Tier 1, Mezzos, “Squad (8)”, etc.) e **ordem** em `briefing.tier_order` — a ordem do sumário e da tabela resumo segue isso.
- **Senha** do HTML: definir hash SHA-256 e colocar em `password_sha256_hex` no front matter (alinhado aos outros dossiês Caixa quando for o caso).

### Fase 1 — Estrutura nova (uma vez por entrega)

Na raiz do repositório:

```bash
python3 loterias2026/scripts/new_creator_dossier.py SEU_SLUG --output-dir loterias2026/data --variant squad_13
```

- Gera `dossier_SEU_SLUG.md` (a partir de `data/dossier_TEMPLATE.md`) e `dossier_SEU_SLUG_panels.yaml` (esqueleto com **mesmos cabeçalhos** do lote de referência e `rows` vazios).
- Para lote no estilo **8 perfis / sem coluna “Variação 14d” no IG**, use `--variant squad_8` e `--output-dir loterias2026-20260406/data` (ou copie depois).

Ajuste no `.md`: `meta.title`, `meta.subtitle`, `periodo`, parágrafos do briefing e blocos de leitura rápida / síntese.

### Fase 2 — Pesquisa (por perfil)

Para cada creator:

1. **Handles** oficiais (IG / TikTok / YouTube / X) — conferir colisões (notas em `research/` dos lotes anteriores como referência de rigor).
2. **Busca aberta** — notícias, TSE se política, termos do método em `METODO_BRAND_SAFETY_LOTERIAS2026.md`.
3. Preencher no `.md` o bloco `## Nome` com:
   - `### Síntese de risco` (texto do selo)
   - `### Resumo tabela` (três linhas: Concorrência / Polêmicas / Política — alimentam a matriz executiva)
   - Eixos longos (caixas coloridas)
4. Registrar URLs nos eixos; manter linguagem **adequada ao cliente** (sem citar ferramentas internas no HTML gerado — o template já é só conteúdo editorial).

### Fase 3 — Métricas

- Preencher `rows` em `dossier_*_panels.yaml` por rede (copiar estrutura das entregas anteriores).
- Ajustar `intro_note`, `coverage_note` e `footnote` por rede se a coleta mudar.

### Fase 4 — Build e publicação

```bash
cd loterias2026
python3 scripts/build_dossier_completo.py \
  --md data/dossier_SEU_SLUG.md \
  --panels data/dossier_SEU_SLUG_panels.yaml \
  --out output/2026MMDD-dossie-....html \
  --variant squad_13
cp output/2026MMDD-dossie-....html ../caixa/
```

- `--no-gate` para preview local sem senha.
- Depois: commit + push (artefatos em `caixa/` disparam o fluxo de Pages conforme regras do repo).

## Referências rápidas no repositório

| O quê | Onde |
|--------|------|
| Template narrativa + YAML inicial | `loterias2026/data/dossier_TEMPLATE.md` |
| Metodologia de pesquisa | `loterias2026/research/METODO_BRAND_SAFETY_LOTERIAS2026.md` |
| Exemplo completo 13 perfis | `loterias2026/data/dossier_loterias2026.md` + `_panels.yaml` |
| Exemplo completo 8 perfis | `loterias2026-20260406/data/dossier_loterias2026.md` + `_panels.yaml` |
| Migração YAML monolítico → md+painéis | `loterias2026/scripts/migrate_yaml_to_md_source.py` |

## Melhorias futuras (opcional)

- CSV intermediário para painéis + script “csv → rows do YAML”.
- Workflow que só valida links quebrados no `.md` antes do build.
- Um único pacote Python em `tools/dossier_kit/` para evitar duplicar `dossier_render.py` entre pastas de lote.
