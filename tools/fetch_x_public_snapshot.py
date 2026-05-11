#!/usr/bin/env python3
"""Snapshot público do X (sem login): seguidores + heurística de atividade via Playwright.

Uso: python3 tools/fetch_x_public_snapshot.py
Saída: JSON em stdout (uma linha por handle).
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, asdict

from playwright.sync_api import sync_playwright

# Handles públicos a auditar (sem @). Ordem: lote 3 + squad 8 (CSV) + tier 1 (tabela X do dossiê).
HANDLES: list[str] = [
    "raquelrealofc",
    "morganacamila",
    "seufreitaz",
    "lorerufis",
    "raphaelviicente",
    "ademaravilha",
    "giovannapitel",
    "RafaGratta",
    "indiobehn",
    "cleane_sampaio",
    "ivanbaron",
    "cristianwariu",
    "CatracaLivre",
    "linnykealves",
    "felipehatori",
    "julimara",
]


@dataclass
class Row:
    handle: str
    url: str
    ok: bool
    followers_raw: str | None
    followers_display: str | None
    posts_count_raw: str | None
    error: str | None
    activity_note: str | None


def parse_followers_pt(text: str) -> tuple[str | None, str | None]:
    """Extrai linha tipo '105,9 mil Seguidores' ou '70,2 mil Seguidores'."""
    m = re.search(
        r"([\d.,]+)\s*mil\s*Seguidores",
        text,
        re.I,
    )
    if m:
        raw = m.group(0)
        num = m.group(1).replace(".", "").replace(",", ".")
        try:
            val = float(num) * 1000
            if val >= 1_000_000:
                disp = f"{val/1_000_000:.1f}M".replace(".", ",")
            elif val >= 1000:
                disp = f"{val/1000:.1f}K".replace(".", ",")
            else:
                disp = str(int(val))
        except ValueError:
            disp = m.group(1) + " mil"
        return raw, disp
    m2 = re.search(r"([\d.,]+)\s*Seguidores", text)
    if m2:
        return m2.group(0), m2.group(1)
    return None, None


def parse_posts_mil(text: str) -> str | None:
    m = re.search(r"([\d.,]+)\s*mil\s*posts", text, re.I)
    return m.group(0) if m else None


def activity_heuristic(text: str) -> str:
    """Datas visíveis no corpo (pt): se aparece 2026 ou meses recentes em 2025, tende ativo."""
    if re.search(r"\b2026\b", text):
        return "ativa — datas 2026 visíveis na amostra pública da timeline"
    if re.search(
        r"(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\s+de\s+2025",
        text,
        re.I,
    ):
        return "ativa — posts de 2025 visíveis na amostra pública"
    if re.search(r"\b2025\b", text):
        return "atividade em 2025 visível na amostra; confirmar recência na data da campanha"
    if re.search(r"Sem posts recentes|sem posts", text, re.I):
        return "sem sinal de posts recentes no texto renderizado"
    if re.search(r"\b2024\b", text):
        return "última amostra dominada por 2024 — tratar como baixa atividade recente no X"
    return "incerta — poucas datas na amostra; confirmar no perfil vivo"


def fetch_one(page, handle: str) -> Row:
    url = f"https://x.com/{handle}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=55000)
        time.sleep(4.2)
        body = page.inner_text("body")
        if "Esta conta não existe" in body or "Account suspended" in body or "Conta suspensa" in body:
            return Row(handle, url, False, None, None, None, "conta inexistente ou suspensa", None)
        if "Algo deu errado" in body and "Seguidores" not in body:
            return Row(handle, url, False, None, None, None, "página sem dados de perfil (bloqueio/geo)", None)
        raw_f, disp = parse_followers_pt(body)
        posts_raw = parse_posts_mil(body)
        note = activity_heuristic(body)
        return Row(
            handle,
            url,
            True,
            raw_f,
            disp,
            posts_raw,
            None,
            note,
        )
    except Exception as e:
        return Row(handle, url, False, None, None, None, repr(e)[:200], None)


def main() -> None:
    out: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
            locale="pt-BR",
        )
        page = ctx.new_page()
        for h in HANDLES:
            if not h:
                continue
            row = fetch_one(page, h)
            out.append(asdict(row))
            time.sleep(2.0)
        browser.close()
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
