#!/usr/bin/env python3
"""
Gera o HTML do dossiê a partir da fonte Markdown + painéis YAML.

Uso (na raiz do repo):
  python3 loterias2026/scripts/build_dossier_completo.py --project-root loterias2026
  python3 loterias2026/scripts/build_dossier_completo.py --project-root loterias2026/lotes/20260406
  python3 loterias2026/scripts/build_dossier_completo.py \\
    --md loterias2026/data/dossier_febraban_concorrencia_2026.md \\
    --panels loterias2026/data/dossier_febraban_concorrencia_2026_panels.yaml \\
    --out loterias2026/output/20260427-dossie-febraban-concorrencia-creators-2026.html \\
    --variant squad_8

Legado: data/dossier_loterias2026.yaml (monolítico) — use migrate_yaml_to_md_source.py
para gerar .md + _panels.yaml a partir dele.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve()
_DEFAULT_PROJECT = _SCRIPT.parents[1]
_REPO_ROOT = _DEFAULT_PROJECT.parent
if str(_REPO_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "tools"))

from dossier_render import render_loterias_dossier_html
from md_dossier_source import load_dossier_bundle, panels_only_path_for_md

# Defaults por pasta de lote (nome do diretório --project-root ou loterias2026)
_PROJECT_DEFAULTS: dict[str, dict[str, str]] = {
    "loterias2026": {
        "md": "data/dossier_loterias2026.md",
        "out": "output/20260401-dossie-squad-always-on-loterias-2026.html",
        "variant": "squad_13",
    },
    "20260406": {
        "md": "data/dossier_loterias2026.md",
        "out": "output/20260406-dossie-squad-always-on-loterias-2026.html",
        "variant": "squad_8",
    },
    "20260504": {
        "md": "data/dossier_loterias2026.md",
        "out": "output/20260504-dossie-squad-always-on-loterias-2026.html",
        "variant": "squad_8",
    },
    "20260511": {
        "md": "data/dossier_loterias2026.md",
        "out": "output/20260511-dossie-squad-always-on-loterias-2026.html",
        "variant": "squad_8",
    },
}

# Pastas antigas na raiz do repo (redirecionamento)
_LEGACY_PROJECT_ALIASES = {
    "loterias2026-20260406": "20260406",
    "loterias2026-20260504": "20260504",
}


def _preset_key(project_root: Path) -> str:
    name = project_root.name
    if name in _LEGACY_PROJECT_ALIASES:
        return _LEGACY_PROJECT_ALIASES[name]
    if project_root.parent.name == "lotes" and project_root.parent.parent.name == "loterias2026":
        return name
    if name == "loterias2026" and project_root.parent == _REPO_ROOT:
        return "loterias2026"
    return name


def _defaults_for_project(project_root: Path) -> dict[str, str]:
    key = _preset_key(project_root)
    return _PROJECT_DEFAULTS.get(
        key,
        {"md": "data/dossier_loterias2026.md", "out": "", "variant": "squad_8"},
    )


def _resolve_project_root(arg: Path | None) -> Path:
    root = (arg or _DEFAULT_PROJECT).resolve()
    alias = _LEGACY_PROJECT_ALIASES.get(root.name)
    if alias:
        candidate = _REPO_ROOT / "loterias2026" / "lotes" / alias
        if candidate.is_dir():
            return candidate
    return root


def load_bundle(
    md_path: Path,
    panels_path: Path | None,
    *,
    legacy_yaml: Path,
    default_md: Path,
) -> dict:
    if md_path.is_file():
        return load_dossier_bundle(md_path, panels_path)
    if md_path.resolve() == default_md.resolve() and legacy_yaml.is_file():
        import yaml

        with open(legacy_yaml, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    raise SystemExit(f"Arquivo fonte não encontrado: {md_path}")


def build_dossier(
    *,
    project_root: Path,
    md_path: Path,
    panels_path: Path | None,
    out_path: Path,
    variant: str,
    no_gate: bool = False,
) -> None:
    defaults = _defaults_for_project(project_root)
    default_md = (project_root / defaults["md"]).resolve()
    legacy_yaml = project_root / "data" / "dossier_loterias2026.yaml"
    bundle = load_bundle(
        md_path,
        panels_path,
        legacy_yaml=legacy_yaml,
        default_md=default_md,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    render_loterias_dossier_html(
        bundle,
        variant=variant,
        out_path=out_path,
        no_gate=no_gate,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera dossiê HTML (fonte .md + painéis YAML).")
    ap.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Pasta do lote (ex.: loterias2026, loterias2026/lotes/20260406). Default: loterias2026/",
    )
    ap.add_argument(
        "--md",
        type=Path,
        default=None,
        help="Arquivo fonte .md (front matter + perfis).",
    )
    ap.add_argument(
        "--panels",
        type=Path,
        default=None,
        help="YAML dos painéis; default: <stem do --md>_panels.yaml",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Caminho do HTML gerado.",
    )
    ap.add_argument(
        "--variant",
        choices=("squad_13", "squad_8"),
        default=None,
        help="Layout IG/tabela resumo (squad_13 = tiers 13; squad_8 = lote 8 perfis).",
    )
    ap.add_argument(
        "--no-gate",
        action="store_true",
        help="Sem tela de senha (preview local).",
    )
    args = ap.parse_args()

    project_root = _resolve_project_root(args.project_root)
    preset = _defaults_for_project(project_root)

    md_path = args.md or (project_root / preset["md"])
    md_path = md_path.resolve() if md_path.is_absolute() else (project_root / md_path).resolve()

    out_rel = args.out or preset.get("out")
    if not out_rel:
        raise SystemExit("Defina --out ou use --project-root de um lote conhecido.")
    out_path = Path(out_rel)
    if not out_path.is_absolute():
        out_path = (project_root / out_path).resolve()

    variant = args.variant or preset["variant"]

    panels_path: Path | None = args.panels.resolve() if args.panels else None
    if panels_path is None and md_path.is_file():
        panels_path = panels_only_path_for_md(md_path)
        if not panels_path.is_file():
            panels_path = None

    build_dossier(
        project_root=project_root,
        md_path=md_path,
        panels_path=panels_path,
        out_path=out_path,
        variant=variant,
        no_gate=args.no_gate,
    )


if __name__ == "__main__":
    main()
