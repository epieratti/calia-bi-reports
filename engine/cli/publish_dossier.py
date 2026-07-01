#!/usr/bin/env python3
"""
Pipeline: validar .md → (opcional) links → build HTML → verificar vazamento na pasta de publicação.

Uso (na raiz):
  python3 engine/cli/publish_dossier.py --md projects/caixa/loterias/always-on-20260401/data/dossier_loterias2026.md \\
    --dest caixa/loterias

  python3 engine/cli/publish_dossier.py --project caixa/loterias/always-on-20260401
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_CORE = REPO_ROOT / "engine" / "core"
ENGINE_CLI = REPO_ROOT / "engine" / "cli"
for p in (ENGINE_CORE, ENGINE_CLI):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from html_filename import html_basename  # noqa: E402
from md_dossier_source import panels_only_path_for_md  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

PAGES_BASE = "https://epieratti.github.io/calia-bi-reports"
BUILD_SCRIPT = REPO_ROOT / "engine/cli/build_dossier.py"


def _run(cmd: list[str], *, cwd: Path | None = None) -> None:
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def _load_manifest(project_dir: Path) -> dict:
    path = project_dir / "manifest.yaml"
    if not path.is_file() or yaml is None:
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _resolve_dest(dest: Path, md: Path, *, yyyymmdd: str | None, suffix: str | None) -> Path:
    dest = dest.expanduser()
    if not dest.is_absolute():
        dest = (REPO_ROOT / dest).resolve()
    if dest.suffix.lower() == ".html":
        return dest
    name = html_basename(md_path=md, yyyymmdd=yyyymmdd, suffix=suffix)
    return dest / name


def _leakage_scan_dir_for_file(html_path: Path) -> Path:
    try:
        rel = html_path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return html_path.parent
    if len(rel.parts) <= 1:
        return html_path.parent
    return REPO_ROOT / rel.parts[0]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Valida, gera HTML (modo B) e publica em pasta Pages com nome padrão."
    )
    ap.add_argument("--project", type=str, default=None, help="Caminho sob projects/")
    ap.add_argument("--md", type=Path, default=None, help="dossier_*.md")
    ap.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Pasta de publicação ou caminho .html (default: manifest publish.dest)",
    )
    ap.add_argument("--date", metavar="YYYYMMDD", default=None)
    ap.add_argument("--suffix", default=None)
    ap.add_argument("--variant", choices=("squad_13", "squad_8"), default=None)
    ap.add_argument("--skip-validate", action="store_true")
    ap.add_argument("--skip-links", action="store_true")
    ap.add_argument("--skip-leakage", action="store_true")
    ap.add_argument("--no-gate", action="store_true")
    ap.add_argument("--quiet-url", action="store_true")
    args = ap.parse_args()

    variant = args.variant or "squad_13"
    dest_arg = args.dest

    if args.project:
        project_dir = (REPO_ROOT / "projects" / args.project).resolve()
        manifest = _load_manifest(project_dir)
        source = manifest.get("source") or {}
        md_rel = source.get("md")
        if not md_rel:
            print(f"manifest sem source.md: {project_dir}", file=sys.stderr)
            return 1
        md = (project_dir / md_rel).resolve()
        variant = args.variant or manifest.get("variant") or variant
        publish = manifest.get("publish") or {}
        if dest_arg is None:
            dest_arg = Path(publish.get("dest") or "caixa")
    else:
        if not args.md:
            print("Informe --project ou --md", file=sys.stderr)
            return 1
        md = args.md.resolve()

    if dest_arg is None:
        print("Informe --dest ou --project com manifest", file=sys.stderr)
        return 1

    if not md.is_file():
        print(f"Arquivo .md não encontrado: {md}", file=sys.stderr)
        return 1
    if not BUILD_SCRIPT.is_file():
        print(f"Script de build não encontrado: {BUILD_SCRIPT}", file=sys.stderr)
        return 1

    out_html = _resolve_dest(dest_arg, md, yyyymmdd=args.date, suffix=args.suffix)
    out_html.parent.mkdir(parents=True, exist_ok=True)

    panels = panels_only_path_for_md(md)
    panels_arg: list[str] = []
    if panels.is_file():
        panels_arg = ["--panels", str(panels)]

    py = sys.executable

    if not args.skip_validate:
        _run([py, str(REPO_ROOT / "engine/qa/validate_source.py"), str(md)])

    if not args.skip_links:
        _run([py, str(REPO_ROOT / "engine/qa/check_links.py"), str(md)], cwd=str(REPO_ROOT))

    build_cmd = [
        py,
        str(BUILD_SCRIPT),
        "--md",
        str(md),
        *panels_arg,
        "--out",
        str(out_html),
        "--variant",
        variant,
    ]
    if args.no_gate:
        build_cmd.append("--no-gate")
    _run(build_cmd, cwd=str(REPO_ROOT))

    if not args.skip_leakage:
        scan_root = _leakage_scan_dir_for_file(out_html)
        try:
            rel_scan = scan_root.resolve().relative_to(REPO_ROOT)
            arg = str(rel_scan).replace("\\", "/")
        except ValueError:
            arg = str(scan_root)
        _run([py, str(REPO_ROOT / "engine/qa/check_html_leakage.py"), arg])

    if not args.quiet_url:
        try:
            rel_url = out_html.resolve().relative_to(REPO_ROOT)
            url_path = "/".join(rel_url.parts)
            print(f"\nHTML: {out_html}")
            print(f"URL (GitHub Pages): {PAGES_BASE}/{url_path}")
        except ValueError:
            print(f"\nHTML: {out_html}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
