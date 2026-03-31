#!/usr/bin/env python3
"""
Coleta complementar na web aberta — Brand Safety Loterias 2026.

Fontes (sem API key obrigatória):
- Wikipedia PT (API MediaWiki: busca + snippet)
- Google Notícias (RSS público, hl=pt-BR)
- DuckDuckGo (busca HTML via duckduckgo-search)

Saída: data/raw/open_web.jsonl (platform: wikipedia | google_news | web_search)
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, quote_plus

import feedparser
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
INFLUENCERS_PATH = ROOT / "data" / "influencers.yaml"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Loterias2026-BrandSafety/1.0 (research; +https://github.com)",
        "Accept": "application/json",
    }
)

WIKI_DELAY = 0.35
NEWS_DELAY = 0.5
DDG_DELAY = 0.8


def load_profiles() -> list[dict]:
    with open(INFLUENCERS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return list(data.get("profiles") or [])


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def wiki_pt_search(name: str, limit: int = 3) -> list[dict]:
    """Busca na Wikipédia em português; devolve título, resumo e URL."""
    api = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": name,
        "format": "json",
        "srlimit": limit,
        "srprop": "snippet",
    }
    try:
        r = SESSION.get(api, params=params, timeout=30)
        r.raise_for_status()
        hits = r.json().get("query", {}).get("search", [])
    except Exception:
        return []
    out: list[dict] = []
    for h in hits:
        title = h.get("title") or ""
        snippet = h.get("snippet", "") or ""
        # snippet vem com marcação HTML simples da API
        snippet = snippet.replace("<span class=\"searchmatch\">", "").replace("</span>", "")
        url = f"https://pt.wikipedia.org/wiki/{quote(title.replace(' ', '_'), safe='')}"
        out.append({"title": title, "snippet": snippet, "url": url})
    return out


def google_news_rss(query: str, limit: int = 10) -> list[dict]:
    q = quote_plus(query)
    url = f"https://news.google.com/rss/search?q={q}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    try:
        parsed = feedparser.parse(url)
    except Exception:
        return []
    out: list[dict] = []
    for i, e in enumerate(getattr(parsed, "entries", []) or []):
        if i >= limit:
            break
        out.append(
            {
                "title": e.get("title") or "",
                "summary": e.get("summary") or e.get("description") or "",
                "url": e.get("link") or "",
                "published_at": e.get("published") or e.get("updated") or "",
            }
        )
    return out


def duckduckgo_text(query: str, max_results: int = 6) -> list[dict]:
    """Tenta pacote `ddgs`; fallback para `duckduckgo_search` legado."""
    out: list[dict] = []
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            gen = ddgs.text(query, region="br-pt", max_results=max_results)
            for r in gen or []:
                out.append(
                    {
                        "title": r.get("title") or "",
                        "body": r.get("body") or "",
                        "url": r.get("href") or "",
                    }
                )
        return out
    except ImportError:
        pass
    except Exception:
        return out
    try:
        from duckduckgo_search import DDGS as DDGSLegacy

        with DDGSLegacy() as ddgs:
            gen = ddgs.text(query, region="br-pt", max_results=max_results)
            for r in gen or []:
                out.append(
                    {
                        "title": r.get("title") or "",
                        "body": r.get("body") or "",
                        "url": r.get("href") or "",
                    }
                )
    except Exception:
        return []
    return out


def main() -> None:
    path = DATA_RAW / "open_web.jsonl"
    if path.exists():
        path.unlink()

    profiles = load_profiles()
    now = datetime.now(timezone.utc).isoformat()

    for p in profiles:
        name = str(p.get("name") or "").strip()
        if not name:
            continue
        ig = str(p.get("instagram") or "").strip().lstrip("@")

        # --- Wikipedia ---
        for w in wiki_pt_search(name, limit=3):
            append_jsonl(
                path,
                {
                    "platform": "wikipedia",
                    "profile_name": name,
                    "handle": ig,
                    "title": w["title"],
                    "description": w["snippet"],
                    "caption": "",
                    "text": w["snippet"],
                    "url": w["url"],
                    "published_at": "",
                    "collected_at": now,
                },
            )
        time.sleep(WIKI_DELAY)

        # --- Google Notícias (RSS) — consulta pelo nome (+ @ opcional para desambiguar) ---
        news_q = f'"{name}"'
        if ig:
            news_q = f'"{name}" OR @{ig}'
        for item in google_news_rss(news_q, limit=10):
            blob = f"{item['title']} {item['summary']}"
            append_jsonl(
                path,
                {
                    "platform": "google_news",
                    "profile_name": name,
                    "handle": ig,
                    "title": item["title"],
                    "description": item["summary"],
                    "caption": "",
                    "text": blob,
                    "url": item["url"],
                    "published_at": item["published_at"],
                    "collected_at": now,
                },
            )
        time.sleep(NEWS_DELAY)

        # --- Busca web (DuckDuckGo) — uma consulta neutra + uma focada em risco leve ---
        for q in (name, f"{name} polêmica OR {name} aposta OR {name} loteria"):
            for d in duckduckgo_text(q, max_results=5 if q == name else 4):
                append_jsonl(
                    path,
                    {
                        "platform": "web_search",
                        "profile_name": name,
                        "handle": ig,
                        "title": d["title"],
                        "description": d["body"],
                        "caption": "",
                        "text": f"{d['title']} {d['body']}",
                        "url": d["url"],
                        "published_at": "",
                        "collected_at": now,
                    },
                )
            time.sleep(DDG_DELAY)

    print("Open web gravado em", path)


if __name__ == "__main__":
    main()
