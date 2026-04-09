#!/usr/bin/env python3
"""
Gera o nome do arquivo HTML publicado no padrão do playbook:
  YYYYMMDD-dossie-<slug>.html

O <slug> deriva de meta.title do front matter (ASCII, minúsculas, hífens).
"""
from __future__ import annotations

import argparse
import re
import unicodedata
from datetime import date
from pathlib import Path

from md_dossier_source import split_front_matter


def primary_title_phrase(title: str) -> str:
    """Remove subtítulo após em dash / travessão (comum em meta.title)."""
    t = title.strip()
    for sep in (" — ", " – ", " - "):
        if sep in t:
            head, tail = t.split(sep, 1)
            if tail.strip():
                t = head.strip()
            break
    return t


def slugify_title(title: str, *, max_len: int = 80) -> str:
    """Título → fragmento seguro para nome de arquivo (sem prefixo dossie-)."""
    t = unicodedata.normalize("NFKD", primary_title_phrase(title))
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    t = re.sub(r"-{2,}", "-", t).strip("-")
    # Evita "dossie-dossie-..." quando o título começa com "Dossiê …"
    if t.startswith("dossie-") and len(t) > 7:
        t = t[7:]
    if len(t) > max_len:
        t = t[:max_len].rstrip("-")
    return t or "relatorio"


def thematic_slug_from_md(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    fm, _ = split_front_matter(text)
    meta = fm.get("meta") or {}
    title = (meta.get("title") or "").strip()
    if not title:
        return slugify_title(md_path.stem.replace("dossier_", "").replace("_", " "))
    return slugify_title(title)


def html_basename(
    *,
    md_path: Path,
    yyyymmdd: str | None = None,
    suffix: str | None = None,
) -> str:
    """Nome completo do arquivo .html."""
    if yyyymmdd is None:
        yyyymmdd = date.today().strftime("%Y%m%d")
    if not re.fullmatch(r"\d{8}", yyyymmdd):
        raise ValueError(f"Data inválida (use YYYYMMDD): {yyyymmdd!r}")
    base = thematic_slug_from_md(md_path)
    if suffix:
        suf = slugify_title(suffix, max_len=32)
        if suf:
            base = f"{base}-{suf}"
    return f"{yyyymmdd}-dossie-{base}.html"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Sugere nome YYYYMMDD-dossie-<slug>.html a partir do .md (meta.title)."
    )
    ap.add_argument("--md", type=Path, required=True, help="Caminho do dossier_*.md")
    ap.add_argument(
        "--date",
        metavar="YYYYMMDD",
        default=None,
        help="Prefixo de data (default: hoje no fuso local)",
    )
    ap.add_argument(
        "--suffix",
        default=None,
        help="Sufixo opcional ao slug (ex.: rev2, delta-8)",
    )
    ap.add_argument(
        "--print-path",
        metavar="DEST",
        default=None,
        help="Se definido, imprime DEST/basename (DEST relativo ou absoluto)",
    )
    args = ap.parse_args()
    md = args.md.resolve()
    if not md.is_file():
        import sys

        print(f"Arquivo não encontrado: {md}", file=sys.stderr)
        return 1
    name = html_basename(md_path=md, yyyymmdd=args.date, suffix=args.suffix)
    if args.print_path:
        dest = Path(args.print_path)
        print(dest / name)
    else:
        print(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
