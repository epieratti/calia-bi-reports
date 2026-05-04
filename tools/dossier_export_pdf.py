#!/usr/bin/env python3
"""
Exporta o dossiê (HTML com gate) para PDF com aparência próxima da tela: fundos,
cards e tipografia Inter. Usa Playwright (Chromium) em contexto HTTP local para o
gate SHA-256 funcionar (crypto.subtle).

Na raiz do repo:
  pip install playwright && playwright install chromium
  python3 tools/dossier_export_pdf.py --html caixa/20260504-dossie-squad-always-on-loterias-2026-rev-nomes.html \\
    --password 'sua_senha' --out ~/Desktop/dossie.pdf

Senha também pode vir de variável de ambiente DOSSIER_PDF_PASSWORD (evita histórico de shell).
"""
from __future__ import annotations

import argparse
import os
import sys
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial

ROOT = Path(__file__).resolve().parents[1]


def _serve_file(html_path: Path) -> tuple[str, HTTPServer, threading.Thread]:
    html_path = html_path.resolve()
    if not html_path.is_file():
        raise FileNotFoundError(html_path)
    directory = str(html_path.parent)
    handler = partial(SimpleHTTPRequestHandler, directory=directory)
    server = HTTPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{port}/{html_path.name}"
    return url, server, thread


def main() -> int:
    ap = argparse.ArgumentParser(description="Gera PDF a partir do HTML do dossiê (com senha).")
    ap.add_argument("--html", type=Path, required=True, help="Arquivo .html (ex.: caixa/....html)")
    ap.add_argument("--out", type=Path, required=True, help="Caminho do .pdf de saída")
    ap.add_argument(
        "--password",
        default="",
        help="Senha do gate (ou use env DOSSIER_PDF_PASSWORD)",
    )
    ap.add_argument("--wait-ms", type=int, default=8000, help="Timeout para o conteúdo aparecer")
    args = ap.parse_args()

    pw = (args.password or os.environ.get("DOSSIER_PDF_PASSWORD") or "").strip()
    if not pw:
        print(
            "Defina --password ou a variável de ambiente DOSSIER_PDF_PASSWORD.",
            file=sys.stderr,
        )
        return 1

    html_path = args.html
    if not html_path.is_absolute():
        html_path = (ROOT / html_path).resolve()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Instale: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        return 1

    url, server, _thread = _serve_file(html_path)
    out_path = args.out.expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": 1200, "height": 1600})
            page.goto(url, wait_until="domcontentloaded", timeout=60_000)
            page.fill("#access-pw", pw)
            page.click("#access-form button[type='submit']")
            # Espera o root visível (remove classe hidden do Tailwind)
            try:
                page.wait_for_function(
                    "() => { const r = document.getElementById('dossier-root'); "
                    "return r && !r.classList.contains('hidden'); }",
                    timeout=args.wait_ms,
                )
            except Exception:
                err = page.locator("#access-err").inner_text(timeout=500).strip()
                browser.close()
                print(
                    f"Falha ao desbloquear o gate. Mensagem na página: {err or '(vazia)'}",
                    file=sys.stderr,
                )
                return 2
            time.sleep(0.8)
            page.emulate_media(media="print")
            page.pdf(
                path=str(out_path),
                format="A4",
                print_background=True,
                margin={"top": "12mm", "bottom": "14mm", "left": "12mm", "right": "12mm"},
            )
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
