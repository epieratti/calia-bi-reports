#!/usr/bin/env python3
"""Gera HTML do dossiê a partir de fonte .md + painéis YAML (modo B)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_CORE = REPO_ROOT / "engine" / "core"
if str(ENGINE_CORE) not in sys.path:
    sys.path.insert(0, str(ENGINE_CORE))

from dossier_render import render_loterias_dossier_html  # noqa: E402
from md_dossier_source import load_dossier_bundle, panels_only_path_for_md  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def _load_manifest(project_dir: Path) -> dict:
    manifest_path = project_dir / "manifest.yaml"
    if not manifest_path.is_file():
        raise SystemExit(f"manifest.yaml não encontrado em {project_dir}")
    if yaml is None:
        raise SystemExit("Instale PyYAML: pip install pyyaml")
    with open(manifest_path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _resolve_from_project(project: str) -> tuple[Path, Path, Path, str]:
    project_dir = (REPO_ROOT / "projects" / project).resolve()
    if not project_dir.is_dir():
        raise SystemExit(f"Projeto não encontrado: {project_dir}")
    manifest = _load_manifest(project_dir)
    source = manifest.get("source") or {}
    md_rel = source.get("md")
    if not md_rel:
        raise SystemExit(f"manifest sem source.md: {project_dir / 'manifest.yaml'}")
    md_path = (project_dir / md_rel).resolve()
    panels_rel = source.get("panels")
    panels_path = (project_dir / panels_rel).resolve() if panels_rel else panels_only_path_for_md(md_path)
    variant = manifest.get("variant") or "squad_13"
    build_dir = project_dir / ".build"
    build_dir.mkdir(parents=True, exist_ok=True)
    published = manifest.get("html_published")
    if published:
        out_name = Path(published).name
    else:
        out_name = "preview.html"
    out_path = build_dir / out_name
    return md_path, panels_path, out_path, variant


def load_bundle(md_path: Path, panels_path: Path | None) -> dict:
    if md_path.is_file():
        return load_dossier_bundle(md_path, panels_path)
    raise SystemExit(f"Arquivo fonte não encontrado: {md_path}")


def main(
    *,
    md_path: Path,
    panels_path: Path | None,
    out_path: Path,
    variant: str,
    no_gate: bool = False,
) -> None:
    bundle = load_bundle(md_path, panels_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    render_loterias_dossier_html(
        bundle,
        variant=variant,
        out_path=out_path,
        no_gate=no_gate,
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Gera dossiê HTML (fonte .md + painéis YAML).")
    ap.add_argument("--project", type=str, default=None, help="Caminho sob projects/, ex.: caixa/loterias/always-on-20260401")
    ap.add_argument("--md", type=Path, default=None, help="Arquivo fonte .md")
    ap.add_argument("--panels", type=Path, default=None, help="YAML dos painéis")
    ap.add_argument("--out", type=Path, default=None, help="Caminho do HTML gerado")
    ap.add_argument(
        "--variant",
        choices=("squad_13", "squad_8"),
        default=None,
        help="Layout (default: manifest ou squad_13)",
    )
    ap.add_argument("--no-gate", action="store_true", help="Sem tela de senha (preview)")
    args = ap.parse_args()

    if args.project:
        md_path, panels_path, out_path, variant = _resolve_from_project(args.project)
        if args.md:
            md_path = args.md.resolve()
        if args.panels:
            panels_path = args.panels.resolve()
        if args.out:
            out_path = args.out.resolve()
        if args.variant:
            variant = args.variant
    else:
        if not args.md:
            raise SystemExit("Informe --project ou --md")
        md_path = args.md.resolve()
        panels_path = args.panels.resolve() if args.panels else panels_only_path_for_md(md_path)
        if panels_path and not panels_path.is_file():
            panels_path = None
        variant = args.variant or "squad_13"
        out_path = args.out.resolve() if args.out else md_path.parent / "preview.html"

    main(
        md_path=md_path,
        panels_path=panels_path,
        out_path=out_path,
        variant=variant,
        no_gate=args.no_gate,
    )
