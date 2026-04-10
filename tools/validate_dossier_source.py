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
from tools.md_dossier_source import panels_only_path_for_md, parse_profiles_markdown  # noqa: E402

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


def _plain_len(s: str) -> int:
    return len((s or "").strip())


def _has_url(s: str) -> bool:
    return bool(re.search(r"https?://", s or ""))


def collect_semantic_hints(md_path: Path, body: str) -> list[str]:
    """Avisos de lacunas comuns (heurística). Não bloqueiam salvo --strict-hints."""
    hints: list[str] = []
    profiles = parse_profiles_markdown(body)
    names_in_panels: set[str] = set()

    panels_path = panels_only_path_for_md(md_path)
    if panels_path.is_file():
        try:
            doc = yaml.safe_load(panels_path.read_text(encoding="utf-8")) or {}
            panels = doc.get("panels") or doc
            ig = (panels.get("instagram") or {}).get("rows") or []
            for row in ig:
                if row and len(row) > 0:
                    cell0 = str(row[0]).strip()
                    base = re.split(r"\s*[—–-]\s*", cell0, maxsplit=1)[0].strip().lower()
                    if base:
                        names_in_panels.add(base)
        except Exception:
            hints.append(
                f"Dica: não foi possível ler {panels_path.name} para cruzar nomes com os painéis."
            )

    for pc in profiles:
        name = (pc.get("name") or "").strip() or "?"
        slug = name.lower()
        handles = pc.get("handles") or {}
        if not any((handles.get(k) or "").strip() for k in ("instagram", "tiktok", "youtube", "x")):
            hints.append(
                f"«{name}»: nenhum handle em ### Handles — confirmar se é intencional (ex.: página só site)."
            )

        risco = (pc.get("risco_geral") or "").strip()
        if risco in ("", "—", "-"):
            hints.append(f"«{name}»: ### Síntese de risco vazia ou só traço.")

        narr = (pc.get("narrativa") or "").strip()
        if _plain_len(narr) < 50:
            hints.append(
                f"«{name}»: narrativa muito curta — o playbook pede texto autocontido; expandir se possível."
            )

        eixos = pc.get("eixos") or {}
        for axis, label in (
            ("concorrencia", "Concorrência"),
            ("polemicas", "Polêmicas"),
            ("politica", "Política"),
        ):
            txt = (eixos.get(axis) or "").strip()
            if txt in ("", "—", "-") or _plain_len(txt) < 12:
                hints.append(
                    f"«{name}»: eixo «{label}» muito vazio — preencher ou explicitar «não consta» com contexto."
                )
            elif (
                axis == "polemicas"
                and not _has_url(txt)
                and _plain_len(txt) > 40
                and not re.search(
                    r"imprensa|matéria|materia|veículo|veiculo|http|reddit|youtube\.com|instagram\.com",
                    txt,
                    re.I,
                )
            ):
                hints.append(
                    f"«{name}»: Polêmicas sem URL — se existir matéria/post estável, incluir link (playbook)."
                )

        if names_in_panels:
            matched = slug in names_in_panels or any(
                slug in n or n.startswith(slug) for n in names_in_panels
            )
            if not matched:
                hints.append(
                    f"«{name}»: nome não bate com a 1ª coluna do painel Instagram — conferir _panels.yaml."
                )

    return hints


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
    ap.add_argument(
        "--hints",
        action="store_true",
        help="Mostrar dicas semânticas (lacunas, links, painéis).",
    )
    ap.add_argument(
        "--strict-hints",
        action="store_true",
        help="Com --hints: exit 3 se houver qualquer dica (CI opcional).",
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

    hint_list: list[str] = []
    if args.hints or args.strict_hints:
        hint_list = collect_semantic_hints(md_path, body)

    for w in warnings:
        print(f"Aviso: {w}")
    for e in errors:
        print(f"Erro: {e}", file=sys.stderr)
    for h in hint_list:
        print(f"Dica: {h}")

    if errors:
        return 1
    if args.strict and warnings:
        return 2
    if args.strict_hints and hint_list:
        return 3
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
