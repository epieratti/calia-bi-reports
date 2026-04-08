#!/usr/bin/env python3
"""
Legado: delega para o script genérico em tools/ (mesma lógica para qualquer cliente).

  python3 embratur/scripts/penetracao_mercados.py

Equivale a:
  python3 tools/penetracao_mercados.py \\
    --entities-json embratur/research/penetracao_entities_embratur_2026.json \\
    --output-prefix embratur/research/penetracao_trends_wiki_2026
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    script = _ROOT / "tools" / "penetracao_mercados.py"
    entities = _ROOT / "embratur" / "research" / "penetracao_entities_embratur_2026.json"
    out = _ROOT / "embratur" / "research" / "penetracao_trends_wiki_2026"
    cmd = [
        sys.executable,
        str(script),
        "--entities-json",
        str(entities),
        "--output-prefix",
        str(out),
    ]
    raise SystemExit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
