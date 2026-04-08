#!/usr/bin/env python3
"""
Cria um novo par fonte para dossiê de creators: dossier_<slug>.md + dossier_<slug>_panels.yaml.

Uso:
  python3 new_creator_dossier.py meu_lote_2026 --output-dir ../data --variant squad_13

O .md é copiado de data/dossier_TEMPLATE.md (ajuste meta no editor).
O _panels.yaml copia cabeçalhos/notas de um lote de referência e zera as linhas (rows).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
LOT_ROOT = SCRIPT_DIR.parent
TEMPLATE = LOT_ROOT / "data" / "dossier_TEMPLATE.md"
REF_PANELS = {
    "squad_13": LOT_ROOT / "data" / "dossier_loterias2026_panels.yaml",
    "squad_8": LOT_ROOT.parent / "loterias2026-20260406" / "data" / "dossier_loterias2026_panels.yaml",
}


def slugify(raw: str) -> str:
    s = raw.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "novo_lote"


def empty_panel_rows(doc: dict) -> dict:
    """Preserva intro_note, headers, footnote; zera rows em instagram/tiktok/youtube/x."""
    panels = dict(doc.get("panels") or doc)
    out = {}
    for k, v in panels.items():
        if isinstance(v, dict) and "rows" in v:
            vc = dict(v)
            vc["rows"] = []
            out[k] = vc
        else:
            out[k] = v
    return {"panels": out}


def main() -> None:
    ap = argparse.ArgumentParser(description="Novo dossiê: .md + _panels.yaml a partir do template.")
    ap.add_argument("slug", help="Identificador (ex.: loterias_cliente_2026_abr)")
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=LOT_ROOT / "data",
        help="Pasta data/ do lote (default: loterias2026/data)",
    )
    ap.add_argument(
        "--variant",
        choices=("squad_13", "squad_8"),
        default="squad_13",
        help="Qual painel de referência copiar (cabeçalhos IG/TT/YT/X).",
    )
    args = ap.parse_args()

    slug = slugify(args.slug)
    out_dir: Path = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not TEMPLATE.is_file():
        raise SystemExit(f"Template não encontrado: {TEMPLATE}")

    ref_path = REF_PANELS[args.variant]
    if not ref_path.is_file():
        raise SystemExit(f"YAML de referência não encontrado: {ref_path}")

    md_out = out_dir / f"dossier_{slug}.md"
    panels_out = out_dir / f"dossier_{slug}_panels.yaml"

    if md_out.exists() or panels_out.exists():
        raise SystemExit(f"Já existe: {md_out.name} ou {panels_out.name} — use outro slug ou apague antes.")

    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("dossier_<projeto>", f"dossier_{slug}")
    text = text.replace("dossier_TEMPLATE", f"dossier_{slug}")
    md_out.write_text(text, encoding="utf-8")

    with open(ref_path, encoding="utf-8") as f:
        ref_doc = yaml.safe_load(f) or {}
    emptied = empty_panel_rows(ref_doc)
    with open(panels_out, "w", encoding="utf-8") as f:
        yaml.dump(
            emptied,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            width=120,
        )

    print(f"OK: {md_out}")
    print(f"OK: {panels_out}")
    print()
    print("Próximo passo: edite meta/briefing no .md e preencha rows nos painéis.")
    print("Build (exemplo):")
    try:
        md_rel = md_out.relative_to(LOT_ROOT)
        pan_rel = panels_out.relative_to(LOT_ROOT)
        print(
            f"  cd {LOT_ROOT} && python3 scripts/build_dossier_completo.py "
            f"--md {md_rel} --panels {pan_rel} "
            f"--out output/SEU_ARQUIVO.html --variant {args.variant}"
        )
    except ValueError:
        print(
            f"  cd {LOT_ROOT} && python3 scripts/build_dossier_completo.py "
            f"--md {md_out} --panels {panels_out} "
            f"--out output/SEU_ARQUIVO.html --variant {args.variant}"
        )


if __name__ == "__main__":
    main()
