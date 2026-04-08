#!/usr/bin/env python3
"""
Valida fonte .md do dossiê: estrutura mínima de perfis e aviso em campos
que devem ser texto plano (sem **, ##, etc. copiados do Markdown).

Saída: 0 se ok, 1 se erro (estrutura), 2 se só avisos (--strict falha com avisos).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Repo root = parent de tools/
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.dossier_plain import strip_markdown_to_plain  # noqa: E402

try:
    import yaml
except ImportError:
    print("Instale PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

_FM = re.compile(r"^---\s*$", re.M)
_MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+", re.M)


def split_fm(text: str) -> tuple[dict, str]:
    parts = _FM.split(text, maxsplit=2)
    if len(parts) < 3:
        raise ValueError("Falta front matter YAML entre ---")
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return fm, body


def check_plain_field(path: str, value: object, warnings: list[str]) -> None:
    """Campos que no HTML viram texto escapado sem mini_md: não use **, ##, etc."""
    if not isinstance(value, str) or not value.strip():
        return
    has_noise = "**" in value or _MD_HEADING.search(value)
    if not has_noise:
        return
    cleaned = strip_markdown_to_plain(value)
    if cleaned != value:
        warnings.append(
            f"{path}: texto com sintaxe Markdown (** ou # …). "
            "Use texto plano neste campo; o gerador remove artefatos, mas a fonte deve ficar limpa."
        )
    elif "**" in value or _MD_HEADING.search(value):
        warnings.append(f"{path}: ainda contém ** ou # — revise.")


def check_front_matter_plain(fm: dict, warnings: list[str]) -> None:
    meta = fm.get("meta") or {}
    for key in ("title", "subtitle", "client_line", "periodo"):
        check_plain_field(f"meta.{key}", meta.get(key), warnings)
    briefing = fm.get("briefing") or {}
    for i, r in enumerate(briefing.get("redes") or []):
        check_plain_field(f"briefing.redes[{i}]", r, warnings)
    for i, col in enumerate((fm.get("methodology") or {}).get("columns") or []):
        if isinstance(col, dict):
            check_plain_field(f"methodology.columns[{i}].label", col.get("label"), warnings)


def validate_profiles(body: str, errors: list[str]) -> None:
    chunks = re.split(r"(?m)^##\s+(.+)$", body)
    if len(chunks) < 2:
        errors.append("Corpo: nenhum perfil encontrado (esperado ## Nome).")
        return
    for i in range(1, len(chunks), 2):
        name = chunks[i].strip()
        pbody = chunks[i + 1] if i + 1 < len(chunks) else ""
        if not name:
            errors.append("Perfil com ## sem nome.")
            continue
        required = (
            "### Handles",
            "### Síntese de risco",
        )
        for r in required:
            if r not in pbody:
                errors.append(f"Perfil «{name}»: falta seção {r}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Valida dossier_*.md")
    ap.add_argument("md", type=Path, help="Caminho do .md")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Tratar avisos de texto plano como erro (exit 2).",
    )
    args = ap.parse_args()
    md_path = args.md.resolve()
    if not md_path.is_file():
        print(f"Arquivo não encontrado: {md_path}", file=sys.stderr)
        return 1

    text = md_path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    try:
        fm, body = split_fm(text)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1

    check_front_matter_plain(fm, warnings)
    validate_profiles(body, errors)

    for w in warnings:
        print(f"Aviso: {w}")
    for e in errors:
        print(f"Erro: {e}", file=sys.stderr)

    if errors:
        return 1
    if args.strict and warnings:
        return 2
    if warnings:
        print("(Avisos não bloqueiam; use --strict para falhar.)")
    try:
        rel = md_path.relative_to(ROOT)
    except ValueError:
        rel = md_path
    print("OK:", rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
