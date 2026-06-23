#!/usr/bin/env python3
"""
Compara HTML publicado (caixa/, febraban/) com rebuild a partir das fontes .md.

Uso (na raiz):
  python3 tools/check_dossier_publish_sync.py --build

Exit 0 se os hashes coincidem; 1 se divergir ou arquivo publicado ausente.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "loterias2026/scripts/build_dossier_completo.py"

SYNC_TARGETS: list[dict[str, str]] = [
    {
        "label": "squad-13",
        "project_root": "loterias2026",
        "md": "loterias2026/data/dossier_loterias2026.md",
        "variant": "squad_13",
        "staging": "loterias2026/output/20260401-dossie-squad-always-on-loterias-2026.html",
        "published": "caixa/20260401-dossie-squad-always-on-loterias-2026.html",
    },
    {
        "label": "squad-8",
        "project_root": "loterias2026/lotes/20260406",
        "md": "loterias2026/lotes/20260406/data/dossier_loterias2026.md",
        "variant": "squad_8",
        "staging": "loterias2026/lotes/20260406/output/20260406-dossie-squad-always-on-loterias-2026.html",
        "published": "caixa/20260406-dossie-squad-always-on-loterias-2026.html",
    },
    {
        "label": "squad-20260504",
        "project_root": "loterias2026/lotes/20260504",
        "md": "loterias2026/lotes/20260504/data/dossier_loterias2026.md",
        "variant": "squad_8",
        "staging": "loterias2026/lotes/20260504/output/20260504-dossie-squad-always-on-loterias-2026.html",
        "published": "caixa/20260504-dossie-squad-always-on-loterias-2026.html",
    },
    {
        "label": "febraban",
        "project_root": "loterias2026",
        "md": "loterias2026/data/dossier_febraban_concorrencia_2026.md",
        "panels": "loterias2026/data/dossier_febraban_concorrencia_2026_panels.yaml",
        "variant": "squad_8",
        "out": "loterias2026/output/20260427-dossie-febraban-concorrencia-creators-2026.html",
        "published": "febraban/20260427-dossie-febraban-concorrencia-creators-2026.html",
    },
]


def _extract_document_date(html_text: str) -> str | None:
    m = re.search(r"Documento:\s*(\d{2}/\d{2}/\d{4})", html_text)
    return m.group(1) if m else None


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build(target: dict[str, str], out_path: Path, *, document_date: str | None) -> None:
    env = os.environ.copy()
    if document_date:
        env["DOSSIER_BUILD_DATE"] = document_date
    cmd = [
        sys.executable,
        str(BUILD_SCRIPT),
        "--project-root",
        str(ROOT / target["project_root"]),
        "--md",
        str(ROOT / target["md"]),
        "--out",
        str(out_path),
        "--variant",
        target["variant"],
    ]
    panels = target.get("panels")
    if panels:
        cmd.extend(["--panels", str(ROOT / panels)])
    subprocess.run(cmd, check=True, cwd=str(ROOT), env=env)


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica alinhamento publicado vs fonte .md")
    ap.add_argument(
        "--build",
        action="store_true",
        help="Regenerar HTML de staging antes de comparar",
    )
    args = ap.parse_args()

    if not BUILD_SCRIPT.is_file():
        print(f"ERRO: build não encontrado: {BUILD_SCRIPT}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for target in SYNC_TARGETS:
        label = target["label"]
        published = ROOT / target["published"]
        if not published.is_file():
            failures.append(f"{label}: publicado ausente — {published}")
            continue

        doc_date = _extract_document_date(published.read_text(encoding="utf-8", errors="replace"))

        if args.build:
            staging_path = target.get("staging") or target.get("out")
            if not staging_path:
                failures.append(f"{label}: sem caminho de staging/out para --build")
                continue
            built = ROOT / staging_path
            built.parent.mkdir(parents=True, exist_ok=True)
            _build(target, built, document_date=doc_date)
            compare = built
        else:
            staging = target.get("staging") or target.get("out")
            if staging and (ROOT / staging).is_file():
                compare = ROOT / staging
            else:
                with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
                    compare = Path(tmp.name)
                _build(target, compare, document_date=doc_date)

        pub_hash = _sha256(published)
        cmp_hash = _sha256(compare)
        if pub_hash != cmp_hash:
            failures.append(
                f"{label}: divergência entre publicado ({published}) e rebuild ({compare})"
            )
        else:
            print(f"OK: {label}")

    if failures:
        for msg in failures:
            print(f"ERRO: {msg}", file=sys.stderr)
        return 1

    print("OK: todos os publicados alinhados às fontes .md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
