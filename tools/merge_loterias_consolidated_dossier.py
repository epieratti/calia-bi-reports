#!/usr/bin/env python3
"""
Gera loterias2026/lotes/20260511/data/dossier_loterias2026.md a partir dos lotes
anteriores (13 + 8 + 3 perfis) + fragmento do lote 3 (mai/2026).

Uso (na raiz do repo):
  python3 tools/merge_loterias_consolidated_dossier.py
  python3 tools/merge_loterias_consolidated_dossier.py --check
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "loterias2026/lotes/20260511/data"
OUT_MD = OUT_DIR / "dossier_loterias2026.md"

SOURCES: list[tuple[str, Path]] = [
    ("squad-13", ROOT / "loterias2026/data/dossier_loterias2026.md"),
    ("squad-8", ROOT / "loterias2026/lotes/20260406/data/dossier_loterias2026.md"),
    ("squad-20260504", ROOT / "loterias2026/lotes/20260504/data/dossier_loterias2026.md"),
]

LOTE3_FRAGMENT = OUT_DIR / "lote3_profiles_fragment.md"

CONSOLIDATED_FRONT_MATTER = """---
meta:
  title: Squad Always ON Loterias 2026 — Brand Safety
  subtitle: Risco de imagem — consolidação dos lotes (abr.–mai./2026) + três novos nomes (lote 3).
  client_line: Agência Calia | Unidade de BI — Cliente CAIXA
  periodo: 'Consolidação 11/05/2026 · Referências de coleta por bloco em Métricas'
password_sha256_hex:
- 992743c627cb5ed96392d34989de45a8935c3df8faa62587e073b933004c1f1b
presentation:
  executive_dashboard: false
quality_calibration:
  data_corte_coleta: "11/05/2026 (conteúdo novo); demais blocos conforme entrega de origem"
  delta_vs_entrega_anterior: Consolidação de 20260401, 20260406, 20260504 + lote 3 (Raquel Real, Morgana Camila, Paulo Victor Freitas).
  definicoes_prova:
    concorrencia: Publi paga ou parceria declarada com apostas, cassino ou loteria concorrente; humor que gere associação indevida ≠ menção casual.
    polemicas: Episódio com risco de imagem documentado em imprensa ou padrão recorrente nas redes.
    politica: Filiação, candidatura ou proximidade com partido/figura com prova documentada.
briefing:
  perfis_institucionais:
  - Catraca Livre
  intro_paragraphs:
  - Este ficheiro **consolida** os perfis já entregues nos dossiês de **01/04/2026**, **06/04/2026** e **04/05/2026** e acrescenta o **lote 3** (três creators) com o mesmo quadro de **quatro eixos**. Para nomes herdados, a coluna **«Loterias 18+»** na tabela resumo explica que o sub-eixo **não foi reexecutado** nesta consolidação.
  - Levantamento de **brand safety** para o squad Always ON Loterias 2026 — **27 creators**. Eixos por perfil e método em **Como foi analisado**. "**Não encontramos**" = ausência nas **fontes públicas** da coleta de origem; pode haver informação fora do escopo.
  criterios:
  - 'Concorrência: publi ou parceria com apostas, cassino, loterias concorrentes — inclusive humor que gere associação indevida, mesmo sem publi paga.'
  - 'Polêmicas: falas ou episódios com risco de imagem documentado.'
  - 'Política: filiação, candidatura ou posicionamento político recorrente e explícito (PT, PL ou outros partidos), com prova.'
  - 'Loterias 18+: **menor de idade** em vídeo, capa ou série no **material público** do perfil.'
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
  - Squad (3)
  - Squad — lote 3 (mai/2026)
methodology:
  columns:
  - label: Imprensa e buscas
    body: Google e DuckDuckGo com nome entre aspas + termos de risco. Cada afirmação sensível tem fonte com link no corpo do dossiê.
  - label: Redes sociais
    body: Perfis públicos no Instagram, TikTok, YouTube e X; datas de coleta por bloco em Métricas (última atualização do conteúdo novo 11/05/2026).
  - label: Tamanho de público (painéis)
    body: Social Blade (Instagram e YouTube) e Upfluence (TikTok). Dados usados só para audiência e engajamento — não são prova de risco.
  - label: Política e eleições (2026)
    body: Buscas abertas por filiação partidária e candidatura; verificação via imprensa e declarações públicas indexadas.
  loterias_18_note: |
    **Coleta:** bio, amostra de feed e notícias com **link**; foco em **menor de idade em cena** no conteúdo público.

    **Demografia / idade de audiência:** as redes costumam mostrar esse recorte **só** para quem **administra** o perfil. **Não** há acesso a isso neste relatório **sem** esses dados **compartilhados** pelo titular ou pela agência.
executive_summary:
  tagline: 'Brand safety — **27 creators** (consolidação abr.–mai./2026). Detalhe em **Perfis** e **tabela resumo**.'
  blocks:
  - title: Concorrência (bets / loterias)
    items:
    - Perfis herdados mantêm a leitura das entregas anteriores; lote 3 sem publi de aposta nas fontes consultadas.
  - title: Polêmicas
    items:
    - Sem episódio novo de risco documentado no lote 3 além do que consta nos perfis.
  - title: Política
    items:
    - "**Sem** filiação partidária documentada no lote 3; ano eleitoral de 2026 — rever sensibilidade institucional."
  - title: Loterias 18+
    items:
    - Lote 3 com leitura qualitativa por perfil; nomes herdados com coluna «Loterias 18+» explicando limite da consolidação.
---
"""


def _split_front_matter(text: str) -> tuple[str, str]:
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        raise ValueError("Fonte sem front matter YAML")
    return parts[1], parts[2].lstrip("\n")


def _extract_profile_sections(body: str) -> list[str]:
    chunks = re.split(r"(?m)^##\s+(.+)$", body)
    if len(chunks) < 2:
        return []
    sections: list[str] = []
    for i in range(1, len(chunks), 2):
        name = chunks[i].strip()
        pbody = chunks[i + 1] if i + 1 < len(chunks) else ""
        sections.append(f"## {name}\n{pbody.rstrip()}\n")
    return sections


def build_consolidated_md() -> str:
    profiles: list[str] = []
    for _label, path in SOURCES:
        if not path.is_file():
            raise SystemExit(f"Fonte ausente: {path}")
        _fm, body = _split_front_matter(path.read_text(encoding="utf-8"))
        profiles.extend(_extract_profile_sections(body))

    if not LOTE3_FRAGMENT.is_file():
        raise SystemExit(f"Fragmento lote 3 ausente: {LOTE3_FRAGMENT}")
    _fm3, lote3_body = _split_front_matter(LOTE3_FRAGMENT.read_text(encoding="utf-8"))
    profiles.extend(_extract_profile_sections(lote3_body))

    header = (
        "<!-- Gerado por tools/merge_loterias_consolidated_dossier.py — não editar manualmente "
        "sem atualizar as fontes dos lotes ou lote3_profiles_fragment.md -->\n\n"
    )
    return CONSOLIDATED_FRONT_MATTER + header + "\n".join(profiles)


def main() -> int:
    ap = argparse.ArgumentParser(description="Merge fontes .md do consolidado 20260511")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Só verificar se o .md gerado coincide com o arquivo em disco",
    )
    args = ap.parse_args()

    generated = build_consolidated_md()
    if args.check:
        if not OUT_MD.is_file():
            print(f"ERRO: {OUT_MD} ausente — rode sem --check para gerar")
            return 1
        existing = OUT_MD.read_text(encoding="utf-8")
        if existing != generated:
            print(f"ERRO: {OUT_MD} desatualizado — rode merge_loterias_consolidated_dossier.py")
            return 1
        print(f"OK: {OUT_MD} alinhado às fontes")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(generated, encoding="utf-8")
    n_profiles = len(re.findall(r"(?m)^##\s+", generated))
    print(f"OK: {OUT_MD} ({n_profiles} perfis)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
