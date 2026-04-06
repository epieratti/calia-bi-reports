# Always ON Loterias 2026 — lote 06/04/2026

Novo dossiê no mesmo modelo de **`loterias2026/`**: Brand Safety / squad, com artefatos internos aqui até gerarmos o HTML e publicar em **`caixa/`** (como no dossiê `20260401-dossie-squad-always-on-loterias-2026.html`).

## Leitura dos dados (redes em falta)

**Ausência de perfil numa rede não é erro de levantamento:** quando um creator não aparece no Instagram, YouTube ou TikTok neste dossiê, significa que **não foi identificado perfil público nessa rede** (ou não existe canal/conta própria), salvo nota explícita em `research/` ou CSV. Não interpretar como falha de pesquisa sem cruzar com as notas de verificação.

**X (Twitter):** contas com **audiência muito baixa** ou **perfil protegido** não são tratadas como o creator (podem ser homónimos ou contas antigas). Ver `research/X_PERFIS.md`.

## Conteúdo desta pasta

| Caminho | Descrição |
|--------|-----------|
| `data/influencers.yaml` | Squad (8 perfis) — redes; YouTube em `research/YOUTUBE_CANAIS.md`; TikTok em `research/TIKTOK_PERFIS.md`; X em `research/X_PERFIS.md`. |
| `research/X_PERFIS.md` | Perfis no X — handles vs Instagram e colisões. |
| `data/x_handles_verificados.csv` | Handles X + URLs, última publicação visível e atividade (inativa / pouca atividade). |
| `research/TIKTOK_PERFIS.md` | Pesquisa de perfil TikTok por nome/handle (diferenças vs Instagram). |
| `data/tiktok_handles_verificados.csv` | Handles TikTok verificados + URLs e notas. |
| `data/upfluence_tiktok_audit.csv` | Métricas [Upfluence TikTok Audit](https://www.upfluence.com/tiktok-audit-tool) (colagem manual). |
| `research/YOUTUBE_CANAIS.md` | Pesquisa de canal próprio no YouTube por nome (handles e URLs). |
| `research/YOUTUBE_PESQUISA_NOME.md` | 2ª verificação: nome + handle, channel IDs e colisões (@juliaferraric, @ademara0, etc.). |
| `research/SOCIAL_BLADE_YOUTUBE.md` | Métricas Social Blade (YouTube) + status de indexação por canal. |
| `data/social_blade_youtube.csv` | CSV resumo SB YouTube (URLs e notas). |
| `data/social_blade_instagram.csv` | Tabela Social Blade (Instagram) para planilha / merge. |
| `data/youtube_handles_verificados.csv` | Handles YouTube + `channel_id` após 2ª verificação. |
| `research/SOCIAL_BLADE_INSTAGRAM.md` | Mesma tabela + notas de fonte e data de captura. |
| `research/BRAND_SAFETY_CAIXA.md` | Brand safety Loterias Caixa: apostas/loteria, marcas, política, polémicas (ronda 2026-04-06). |
| `research/SQUAD_FICHA_COMPLETA.md` | Ficha completa por creator: identidade, métricas, posicionamento, parcerias, riscos e referências URL. |
| `data/brand_safety_evidencias.csv` | Evidências por categoria (POLEMICA, POLITICA, ASSOCIACAO, etc.). |
| `data/apostas_loterias_historico.csv` | Histórico público bet/loteria concorrente + classificação. |
| `data/parcerias_marcas.csv` | Marcas e parcerias citadas em fontes públicas. |
| `data/creators_master.csv` | Baseline único (métricas IG/TikTok/YT/X + flags). |
| `data/creators_master_rebuild.csv` | Baseline gerado por [`scripts/merge_creators_baseline.py`](scripts/merge_creators_baseline.py) (reproduzível). |
| `data/youtube_rss_recent.csv` | RSS YouTube por **todos** os `channel_id` do lote (último vídeo / status). |
| `data/busca_loteria_complementar.csv` | 2.ª ronda: nome + Mega-Sena/Lotofácil (sem achado publi). |
| `data/busca_nome_bet.csv` | Registo de auditoria: **query literal nome + bet** por creator, data, classificação e URLs da SERP. |
| `scripts/merge_creators_baseline.py` | Merge IG + TikTok + YT + X + SB em CSV único. |
| `research/google_alerts_sugestoes.md` | Queries sugeridas para Google Alerts (configuração manual). |
| `research/fontes_referencia_gemini.md` | Índice rápido de URLs; detalhe narrativo em `SQUAD_FICHA_COMPLETA.md`. |
| `data/dossier_loterias2026.yaml` | Fonte do **HTML** do dossiê (8 perfis, painéis IG/TT/YT/X, textos Brand Safety). |
| `scripts/build_dossier_completo.py` | Gera `output/20260406-dossie-squad-always-on-loterias-2026.html` (mesmo modelo que `loterias2026/`). |
| `output/20260406-dossie-squad-always-on-loterias-2026.html` | Dossiê gerado; cópia publicada em `caixa/` com o mesmo nome. |

## HTML do dossiê (cliente)

Na **raiz do repositório** `calia-bi-reports`:

```bash
./loterias2026-20260406/scripts/publish_to_caixa.sh
```

(Equivale a `python3 scripts/build_dossier_completo.py` + cópia para `caixa/`.)

**Senha:** `caixa2026` (SHA-256 no YAML, igual ao dossiê 20260401).

## Próximos passos (quando for fechar o dossiê)

1. Redes em `data/influencers.yaml`: YouTube e TikTok conferidos nos `research/`; X ainda pode ser cruzado com bios oficiais.
2. Após editar `data/dossier_loterias2026.yaml`, voltar a gerar o HTML e copiar para `caixa/`.

## Referência

- Dossiê anterior (13 perfis): `loterias2026/README.md`
- Publicação Caixa: `caixa/README.md`
