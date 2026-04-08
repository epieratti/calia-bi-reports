#!/usr/bin/env python3
"""
Migra dossier_loterias2026.yaml → dossier_loterias2026.md + dossier_loterias2026_panels.yaml.
Uso: python migrate_yaml_to_md_source.py [--yaml PATH]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_YAML = SCRIPT_DIR.parent / "data" / "dossier_loterias2026.yaml"


def profile_to_markdown(p: dict) -> str:
    name = p.get("name", "")
    tier = p.get("tier", "")
    risco = p.get("risco_geral", "")
    h = p.get("handles") or {}
    rt = p.get("resumo_tabela") or {}
    eix = p.get("eixos") or {}
    lines = [
        f"## {name}",
        "",
        f"- **Camada:** {tier}",
        "",
        "### Síntese de risco",
        "",
        str(risco or "—"),
        "",
        "### Handles",
        "",
        f"- instagram: {h.get('instagram', '')}",
        f"- tiktok: {h.get('tiktok', '')}",
        f"- youtube: {h.get('youtube', '')}",
        f"- x: {h.get('x', '')}",
        "",
        "### Narrativa",
        "",
        str(p.get("narrativa") or "—"),
        "",
        "### Resumo tabela",
        "",
        f"- **Concorrência:** {rt.get('concorrencia', '—')}",
        f"- **Polêmicas:** {rt.get('polemicas', '—')}",
        f"- **Política:** {rt.get('politica', '—')}",
        "",
        "### Concorrência (bets / loterias / jogos)",
        "",
        str(eix.get("concorrencia") or "—"),
        "",
        "### Polêmicas e situações delicadas",
        "",
        str(eix.get("polemicas") or "—"),
        "",
        "### Política e pautas sensíveis",
        "",
        str(eix.get("politica") or "—"),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yaml", type=Path, default=DEFAULT_YAML)
    args = ap.parse_args()
    ypath: Path = args.yaml
    with open(ypath, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    panels = data.pop("panels", None)
    profiles = data.pop("profiles", [])

    stem = ypath.stem  # dossier_loterias2026
    out_dir = ypath.parent
    panels_path = out_dir / f"{stem}_panels.yaml"
    md_path = out_dir / f"{stem}.md"

    if panels is not None:
        with open(panels_path, "w", encoding="utf-8") as f:
            yaml.dump(
                {"panels": panels},
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                width=120,
            )

    fm = yaml.dump(
        data,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=100,
    )
    body = "\n\n".join(profile_to_markdown(p) for p in profiles)
    md_path.write_text(f"---\n{fm}---\n\n{body}\n", encoding="utf-8")
    print("Wrote", md_path.relative_to(ypath.parent.parent))
    if panels is not None:
        print("Wrote", panels_path.relative_to(ypath.parent.parent))


if __name__ == "__main__":
    main()
