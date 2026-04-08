# Always ON Loterias 2026 — Brand Safety

## Linha de produção (novos dossiês de creators)

1. Leia o playbook geral na raiz do repo: **`PLAYBOOK_DOSSIES.md`** (vale para qualquer cliente; aqui só os passos técnicos Loterias).
2. Crie fonte nova: `python3 scripts/new_creator_dossier.py SEU_SLUG --variant squad_13` (ou `squad_8` para layout do lote de 8 perfis).
3. Edite `dossier_SEU_SLUG.md` e `dossier_SEU_SLUG_panels.yaml`.
4. Gere HTML: `python3 scripts/build_dossier_completo.py --md data/dossier_SEU_SLUG.md --out output/....html --variant squad_13`
5. Na raiz do repo: `python3 tools/validate_dossier_source.py loterias2026/data/dossier_SEU_SLUG.md` (ou `make validate-dossier-13` para o ficheiro atual). Ver regras de Markdown em **`PLAYBOOK_DOSSIES.md`** → Toolbox.

## Dossiê HTML (página do cliente)

- O HTML publicado **não** menciona repositório, `.md`, `.yaml` nem ferramentas internas — só o pedido da campanha, os três critérios, leitura clara e métricas como contexto.
- **Ordem das seções no HTML:** após metodologia, vem **Perfis por camada**; depois **Síntese**; em seguida **Tabela resumo** (matriz executiva); por último **Métricas** (tabelas por rede).

### Fonte da verdade (conteúdo + narrativa)

- **`data/dossier_loterias2026.md`** — front matter YAML (meta, briefing, metodologia, sínteses) + **corpo em Markdown** com um bloco `## Nome` por perfil (handles, narrativa, eixos, resumo da tabela). Formato pensado para **anotar pesquisa** sem editar YAML profundo.
- **`data/dossier_loterias2026_panels.yaml`** — só as **tabelas de métricas** (Instagram, TikTok, YouTube, X) e notas de cobertura. Colar/atualizar exportações aqui.
- **`data/dossier_TEMPLATE.md`** — modelo para **novos dossiês** (copiar e renomear; ajustar `build_dossier_completo.py` se usar outro stem).
- **`data/dossier_loterias2026.yaml`** — snapshot **legado** (monolítico). O build usa **primeiro** o `.md` se existir; sem o `.md`, cai no YAML. Para regenerar `.md` + `_panels.yaml` a partir do YAML: `python3 scripts/migrate_yaml_to_md_source.py`.

### Pesquisa e referências

- **Evidências com URLs:** `research/FONTES_BRAND_SAFETY_LOTERIAS2026.md`
- **Metodologia:** `research/METODO_BRAND_SAFETY_LOTERIAS2026.md`
- **Handles do squad:** `data/influencers.yaml`

**Gerar o HTML:**

```bash
cd loterias2026
python3 scripts/build_dossier_completo.py
```

Saída: `output/20260401-dossie-squad-always-on-loterias-2026.html`

**No ar (GitHub Pages, pasta `caixa/`):** após o deploy em `main`, use  
https://epieratti.github.io/calia-bi-reports/caixa/20260401-dossie-squad-always-on-loterias-2026.html  
(senha **apenas** `caixa2026`). Copie o HTML de `output/` para `caixa/` com o mesmo nome ao publicar.

**Acesso:** proteção client-side — somente **`caixa2026`** (SHA-256 no script), alinhado ao box do dossiê 20260326, sem alias.

Fluxo recomendado: editar **`dossier_loterias2026.md`** (texto) e **`dossier_loterias2026_panels.yaml`** (números) → rodar o build → copiar o HTML para **`caixa/`**.

## Pipeline opcional (Apify)

Ver `requirements.txt` e `.github/workflows/loterias2026-brand-safety.yml` — exige `APIFY_TOKEN`; gera outro HTML heurístico em `output/dossie-brand-safety-loterias-2026.html`.
