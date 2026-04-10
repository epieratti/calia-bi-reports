---
# Copie para dossier_<projeto>.md. Painéis: dossier_<projeto>_panels.yaml (veja dossier_loterias2026_panels.yaml).
meta:
  title: Título do dossiê — Brand Safety
  subtitle: Uma linha sobre escopo e quantidade de nomes.
  client_line: Agência Calia | Unidade de BI — Cliente CAIXA
  periodo: Mês/ano da coleta
password_sha256_hex:
  - "0000000000000000000000000000000000000000000000000000000000000000"
# Opcional — aparência do HTML (ver PLAYBOOK_DOSSIES.md → *presentation* no modo B)
# presentation:
#   executive_dashboard: true
#   product_tagline: "Uso interno — brand safety / vetting"
#   footer_note: "Texto legal ou disclaimer curto (texto plano)."
briefing:
  intro_paragraphs:
    - Parágrafo 1 do pedido (**negrito**, [links](https://exemplo.com)).
  criterios:
    - Concorrência — o que foi buscado.
    - Polêmicas — o que foi buscado.
    - Política — o que foi buscado.
  redes:
    - Instagram
    - TikTok
    - YouTube
    - X
  tier_order:
    - Tier 1
    - Tier 2
    - Mezzos
    - Micros
    - Página
methodology:
  columns:
    - label: Coluna 1
      body: |
        Texto da metodologia. Parágrafos separados por linha em branco viram blocos no HTML.
executive_summary:
  tagline: Frase de abertura da leitura rápida.
  blocks:
    - title: Bloco A
      items:
        - Bullet com **markdown** curto.
consolidated_narrative:
  title: Síntese do squad
  subtitle: Data ou contexto.
  tagline: Linha de apoio à decisão.
  blocks:
    - title: Visão
      items:
        - Item 1.
---

> **Modelo de produção:** o corpo abaixo contém **somente perfis**. Cada pessoa = um `## Nome`. A linha `- **Camada:**` deve coincidir com um valor de `briefing.tier_order`. Novo lote: `python3 scripts/new_creator_dossier.py SEU_SLUG`. Build: `python3 scripts/build_dossier_completo.py --md data/dossier_SEU_SLUG.md --out output/arquivo.html`. Método geral do repo: **`PLAYBOOK_DOSSIES.md`** (raiz).

## Exemplo de perfil (substitua e duplique)

- **Camada:** Tier 1

### Síntese de risco

Baixo — texto do selo no card.

### Handles

- instagram: usuario
- tiktok: usuario
- youtube: usuario
- x: usuario

### Narrativa

Contexto do talento. [Link](https://exemplo.com).

### Resumo tabela

- **Concorrência:** Linha da matriz executiva.
- **Polêmicas:** Linha da matriz.
- **Política:** Linha da matriz.

### Concorrência (bets / loterias / jogos)

Detalhe do eixo (caixa grande em Perfis).

### Polêmicas e situações delicadas

Detalhe do eixo.

### Política e pautas sensíveis

Detalhe do eixo.
