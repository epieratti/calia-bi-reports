"""
Normaliza texto que veio de Markdown colado por engano em campos que o gerador
trata como texto puro (escape HTML), sem interpretar ** ou ##.

Uso: importado por dossier_render e por validate_dossier_source.
"""
from __future__ import annotations

import re


def strip_markdown_to_plain(s: object) -> str:
    """
    Remove artefatos comuns de MD que não devem aparecer literais no HTML:
    - **negrito** e __sublinhado__
    - cabeçalhos ATX (# …) no início de linha
    - links [texto](https://…) → texto (URL)

    Não interpreta listas ou blocos de código; só limpa o que costuma ser
    copiado por engano do corpo do MD para o front matter YAML.
    """
    t = str(s or "")
    if not t.strip():
        return t

    lines = [re.sub(r"^\s{0,3}#{1,6}\s+", "", line) for line in t.splitlines()]
    t = "\n".join(lines)

    for _ in range(5):
        n = re.sub(r"\*\*(.+?)\*\*", r"\1", t, flags=re.DOTALL)
        if n == t:
            break
        t = n
    for _ in range(5):
        n = re.sub(r"__(.+?)__", r"\1", t, flags=re.DOTALL)
        if n == t:
            break
        t = n

    t = re.sub(r"\[(.+?)\]\((https?://[^)\s]+)\)", r"\1 (\2)", t)
    return t
