#!/usr/bin/env python3
"""
Pipeline: validar .md → (opcional) links → build HTML → cópia implícita no --out
→ verificar vazamento na pasta de publicação.

O build usa sempre `loterias2026/scripts/build_dossier_completo.py` (importa tools/),
com caminhos absolutos para --md e --out — funciona para qualquer `dossier_*.md` no repo.

Uso (na raiz):
  python3 tools/dossier_publish.py --md loterias2026/data/dossier_loterias2026.md \\
    --dest caixa/loterias

  python3 tools/dossier_publish.py --md path/to/dossier_x.md --dest embratur/ \\
    --date 20260408 --variant squad_8
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from dossier_html_filename import html_basename
from md_dossier_source import panels_only_path_for_md

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "loterias2026/scripts/build_dossier_completo.py"
PAGES_BASE = "https://epieratti.github.io/calia-bi-reports"


def _run(cmd: list[str], *, cwd: Path | None = None) -> None:
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def _resolve_dest(dest: Path, md: Path, *, yyyymmdd: str | None, suffix: str | None) -> Path:
    dest = dest.expanduser()
    if not dest.is_absolute():
        dest = (ROOT / dest).resolve()
    if dest.suffix.lower() == ".html":
        return dest
    name = html_basename(md_path=md, yyyymmdd=yyyymmdd, suffix=suffix)
    return dest / name


def _leakage_scan_dir_for_file(html_path: Path) -> Path:
    try:
        rel = html_path.resolve().relative_to(ROOT)
    except ValueError:
        return html_path.parent
    if len(rel.parts) <= 1:
        return html_path.parent
    return ROOT / rel.parts[0]


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Valida, gera HTML (modo B) e publica em pasta Pages com nome padrão."
    )
    ap.add_argument("--md", type=Path, required=True, help="dossier_*.md")
    ap.add_argument(
        "--dest",
        type=Path,
        required=True,
        help="Pasta de publicação (ex.: caixa/loterias) ou caminho completo .html",
    )
    ap.add_argument(
        "--date",
        metavar="YYYYMMDD",
        default=None,
        help="Prefixo de data no nome do arquivo (default: hoje)",
    )
    ap.add_argument("--suffix", default=None, help="Sufixo opcional no slug do nome")
    ap.add_argument(
        "--variant",
        choices=("squad_13", "squad_8"),
        default="squad_13",
        help="Layout do gerador (default: squad_13)",
    )
    ap.add_argument("--skip-validate", action="store_true")
    ap.add_argument(
        "--skip-links",
        action="store_true",
        help="Não rodar check_dossier_links (útil se URLs bloqueiam bot)",
    )
    ap.add_argument("--skip-leakage", action="store_true")
    ap.add_argument(
        "--no-gate",
        action="store_true",
        help="Preview sem senha (não usar para entrega cliente)",
    )
    ap.add_argument("--quiet-url", action="store_true", help="Não imprimir URL sugerida")
    args = ap.parse_args()

    md = args.md.resolve()
    if not md.is_file():
        print(f"Arquivo .md não encontrado: {md}", file=sys.stderr)
        return 1
    if not BUILD_SCRIPT.is_file():
        print(f"Script de build não encontrado: {BUILD_SCRIPT}", file=sys.stderr)
        return 1

    out_html = _resolve_dest(args.dest, md, yyyymmdd=args.date, suffix=args.suffix)
    out_html.parent.mkdir(parents=True, exist_ok=True)

    panels = panels_only_path_for_md(md)
    panels_arg: list[str] = []
    if panels.is_file():
        panels_arg = ["--panels", str(panels)]

    py = sys.executable

    if not args.skip_validate:
        _run([py, str(ROOT / "tools/validate_dossier_source.py"), str(md)])

    if not args.skip_links:
        _run(
            [py, str(ROOT / "tools/check_dossier_links.py"), str(md)],
            cwd=str(ROOT),
        )

    build_cmd = [
        py,
        str(BUILD_SCRIPT),
        "--md",
        str(md),
        *panels_arg,
        "--out",
        str(out_html),
        "--variant",
        args.variant,
    ]
    if args.no_gate:
        build_cmd.append("--no-gate")
    _run(build_cmd, cwd=str(ROOT / "loterias2026"))

    if not args.skip_leakage:
        scan_root = _leakage_scan_dir_for_file(out_html)
        try:
            rel_scan = scan_root.resolve().relative_to(ROOT)
            arg = str(rel_scan).replace("\\", "/")
        except ValueError:
            arg = str(scan_root)
        _run([py, str(ROOT / "tools/check_client_html_leakage.py"), arg])

    if not args.quiet_url:
        try:
            rel_url = out_html.resolve().relative_to(ROOT)
            url_path = "/".join(rel_url.parts)
            print(f"\nHTML: {out_html}")
            print(f"URL (GitHub Pages): {PAGES_BASE}/{url_path}")
        except ValueError:
            print(f"\nHTML: {out_html}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
