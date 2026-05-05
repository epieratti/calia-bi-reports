#!/usr/bin/env python3
"""
Fonte do dossiê em Markdown: front matter YAML + corpo com perfis (## Nome).
Painéis de métricas ficam em arquivo YAML à parte (ex.: dossier_loterias2026_panels.yaml).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.dossier_plain import strip_markdown_to_plain

_FM_BOUNDARY = re.compile(r"^---\s*$", re.M)


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Primeiro bloco --- ... --- é YAML; o restante é Markdown dos perfis."""
    parts = _FM_BOUNDARY.split(text, maxsplit=2)
    if len(parts) < 3 or not parts[1].strip():
        raise ValueError(
            "Arquivo deve começar com front matter YAML entre linhas --- (meta, briefing, etc.)."
        )
    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return meta, body


def _slug_handles_block(block: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # - instagram: foo OR instagram: foo
        line = re.sub(r"^[-*]\s*", "", line)
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        k = key.strip().lower().replace("**", "").strip()
        v = strip_markdown_to_plain(val.strip().strip("`\"'"))
        if k in ("instagram", "tiktok", "youtube", "x"):
            out[k] = v
    return out


def _field_line(body: str, label: str) -> str | None:
    """Ex.: - **Camada:** Tier 1 (dois-pontos costumam ficar dentro do ** no MD exportado)."""
    for pat in (
        rf"(?im)^[*-]?\s*\*\*{re.escape(label)}:\*\*\s*(.+)$",
        rf"(?im)^[*-]?\s*\*\*{re.escape(label)}\*\*\s*:\s*(.+)$",
    ):
        m = re.search(pat, body)
        if m:
            return m.group(1).strip()
    return None


def _subsection(body: str, title: str) -> str:
    """Conteúdo após ### Título até o próximo ### ou ##."""
    pat = rf"(?ms)^###\s*{re.escape(title)}\s*$(.*?)(?=^###\s|^##\s|\Z)"
    m = re.search(pat, body)
    return m.group(1).strip() if m else ""


def _resumo_from_body(body: str) -> dict[str, str]:
    block = _subsection(body, "Resumo tabela")
    if not block:
        return {
            "concorrencia": "",
            "polemicas": "",
            "politica": "",
            "loterias_18": "",
        }
    out = {
        "concorrencia": "",
        "polemicas": "",
        "politica": "",
        "loterias_18": "",
    }
    for line in block.splitlines():
        m = re.match(
            r"^[*-]?\s*\*\*(Concorrência|Polêmicas|Política|Loterias\s*18\+)\*\*\s*:\s*(.+)$",
            line.strip(),
            re.I,
        )
        if not m:
            continue
        k = m.group(1).lower()
        v = m.group(2).strip()
        if "concorr" in k:
            out["concorrencia"] = v
        elif "polêm" in k or "polem" in k:
            out["polemicas"] = v
        elif "polít" in k or "polit" in k:
            out["politica"] = v
        elif "loteria" in k or "18" in k:
            out["loterias_18"] = v
    return out


def parse_profiles_markdown(body: str) -> list[dict[str, Any]]:
    """Perfis: cada ## Nome ... até o próximo ##."""
    chunks = re.split(r"(?m)^##\s+(.+)$", body)
    if len(chunks) < 2:
        return []
    profiles: list[dict[str, Any]] = []
    # chunks[0] ignorado (texto antes do primeiro perfil)
    for i in range(1, len(chunks), 2):
        name = strip_markdown_to_plain(chunks[i].strip()).strip()
        pbody = chunks[i + 1] if i + 1 < len(chunks) else ""
        tier = strip_markdown_to_plain(
            _field_line(pbody, "Camada") or _field_line(pbody, "Tier") or ""
        ).strip()
        risco_block = _subsection(pbody, "Síntese de risco")
        if risco_block.strip():
            risco = strip_markdown_to_plain(risco_block.strip())
        else:
            risco = strip_markdown_to_plain(_field_line(pbody, "Síntese de risco") or "—")

        handles_block = _subsection(pbody, "Handles")
        handles = _slug_handles_block(handles_block)

        narr = _subsection(pbody, "Narrativa")
        resumo = _resumo_from_body(pbody)
        lot18 = _subsection(pbody, "Loterias 18+ (leitura qualitativa)") or _subsection(
            pbody, "Loterias 18+"
        )
        conc = _subsection(pbody, "Concorrência") or _subsection(
            pbody, "Concorrência (bets / loterias / jogos)"
        )
        pol = _subsection(pbody, "Polêmicas") or _subsection(
            pbody, "Polêmicas e situações delicadas"
        )
        poli = _subsection(pbody, "Política") or _subsection(
            pbody, "Política e pautas sensíveis"
        )

        def _rt(key: str, eixo_txt: str) -> str:
            v = (resumo.get(key) or "").strip()
            return v if v else (eixo_txt.strip() or "—")

        lot18_body = (lot18 or "").strip()
        lot18_axis = lot18_body if lot18_body else "—"

        prof: dict[str, Any] = {
            "name": name,
            "tier": tier,
            "risco_geral": risco or "—",
            "resumo_tabela": {
                "concorrencia": _rt("concorrencia", conc),
                "polemicas": _rt("polemicas", pol),
                "politica": _rt("politica", poli),
                "loterias_18": _rt("loterias_18", lot18_axis),
            },
            "handles": handles,
            "narrativa": narr or "—",
            "eixos": {
                "concorrencia": conc.strip() or "—",
                "polemicas": pol.strip() or "—",
                "politica": poli.strip() or "—",
                "loterias_18": lot18_axis,
            },
        }
        profiles.append(prof)
    return profiles


def load_dossier_bundle(
    md_path: Path,
    panels_path: Path | None = None,
) -> dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    profiles = parse_profiles_markdown(body)
    bundle = {**fm, "profiles": profiles}
    if panels_path and panels_path.is_file():
        with open(panels_path, encoding="utf-8") as f:
            panels_doc = yaml.safe_load(f) or {}
        bundle["panels"] = panels_doc.get("panels") or panels_doc
    elif "panels" in fm:
        bundle["panels"] = fm["panels"]
    return bundle


def panels_only_path_for_md(md_path: Path) -> Path:
    """dossier.md → dossier_panels.yaml ao lado."""
    return md_path.with_name(md_path.stem + "_panels.yaml")
