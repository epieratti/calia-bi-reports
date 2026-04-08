#!/usr/bin/env python3
"""
Extrai URLs http(s) de um dossier_*.md e verifica HEAD/GET (timeout curto).
Uso opcional na toolbox; pode falhar por rate limit ou bloqueio de bot.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s\)\]\"'<>]+", re.I)


def check_url(url: str, timeout: float) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "CaliaDossierLinkCheck/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code = getattr(r, "status", None) or r.getcode()
            if code and int(code) < 400:
                return True, str(code)
    except urllib.error.HTTPError as e:
        if e.code in (405, 501, 403):
            return check_url_get(url, timeout)
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:120]
    return True, "ok"


def check_url_get(url: str, timeout: float) -> tuple[bool, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CaliaDossierLinkCheck/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            code = getattr(r, "status", None) or r.getcode()
            if code and int(code) < 400:
                return True, str(code)
    except Exception as e:
        return False, str(e)[:120]
    return True, "ok"


def main() -> int:
    ap = argparse.ArgumentParser(description="Checa links em dossier .md")
    ap.add_argument("md", type=Path)
    ap.add_argument("--timeout", type=float, default=12.0)
    args = ap.parse_args()
    p = args.md.resolve()
    if not p.is_file():
        print(f"Não encontrado: {p}", file=sys.stderr)
        return 1
    text = p.read_text(encoding="utf-8")
    urls = sorted(set(URL_RE.findall(text)))
    bad = 0
    for u in urls:
        u = u.rstrip(").,;]")
        ok, msg = check_url(u, args.timeout)
        if ok:
            print(f"OK {msg:12} {u}")
        else:
            print(f"FALHA {msg:12} {u}", file=sys.stderr)
            bad += 1
    if bad:
        print(f"\n{bad} URL(s) com problema (rede, 404 ou bloqueio).", file=sys.stderr)
        return 1
    print(f"Verificadas {len(urls)} URL(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
