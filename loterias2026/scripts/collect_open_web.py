#!/usr/bin/env python3
"""
Coleta complementar na web aberta — Brand Safety Loterias 2026.

Fontes (sem API key obrigatória):
- Wikipedia PT/EN: busca + trecho intro (API extracts)
- Google Notícias (RSS, hl=pt-BR)
- RSS de veículos BR (config/open_web.yaml), filtrados pelo nome
- Busca web (pacote ddgs)

Saída: data/raw/open_web.jsonl
"""
from __future__ import annotations

import html as html_lib
import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, quote_plus

import feedparser
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
INFLUENCERS_PATH = ROOT / "data" / "influencers.yaml"
OPEN_WEB_CONFIG = ROOT / "config" / "open_web.yaml"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Loterias2026-BrandSafety/1.0 (research; +https://github.com)",
        "Accept": "application/json",
    }
)


def norm_key(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def load_open_web_cfg() -> dict:
    if not OPEN_WEB_CONFIG.is_file():
        return {}
    with open(OPEN_WEB_CONFIG, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_profiles() -> list[dict]:
    with open(INFLUENCERS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return list(data.get("profiles") or [])


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def strip_html_snippet(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    return html_lib.unescape(s)


def wiki_search(lang: str, name: str, limit: int) -> list[dict]:
    api = f"https://{lang}.wikipedia.org/w/api.php"
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
        snippet = strip_html_snippet(h.get("snippet", "") or "")
        url = f"https://{lang}.wikipedia.org/wiki/{quote(title.replace(' ', '_'), safe='')}"
        out.append({"title": title, "snippet": snippet, "url": url, "lang": lang})
    return out


def wiki_extract_intro(lang: str, title: str, max_chars: int) -> str:
    api = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "exintro": True,
        "explaintext": True,
        "format": "json",
    }
    try:
        r = SESSION.get(api, params=params, timeout=30)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        p = next(iter(pages.values()), {})
        ex = (p.get("extract") or "").strip()
        if max_chars > 0 and len(ex) > max_chars:
            ex = ex[:max_chars].rsplit(" ", 1)[0] + "…"
        return ex
    except Exception:
        return ""


def google_news_rss(query: str, limit: int) -> list[dict]:
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
                "summary": strip_html_snippet(e.get("summary") or e.get("description") or ""),
                "url": e.get("link") or "",
                "published_at": e.get("published") or e.get("updated") or "",
            }
        )
    return out


def feed_entries_filtered(
    feed_url: str,
    name_key: str,
    max_entries: int,
    name_tokens: list[str],
    fetch_max_bytes: int,
) -> list[dict]:
    """Lê RSS e mantém só itens cujo título ou resumo menciona o nome (normalizado)."""
    if not name_key:
        return []
    try:
        r = SESSION.get(feed_url, timeout=20, stream=True)
        r.raise_for_status()
        max_b = max(50_000, fetch_max_bytes)
        chunks: list[bytes] = []
        total = 0
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                continue
            chunks.append(chunk)
            total += len(chunk)
            if total >= max_b:
                break
        parsed = feedparser.parse(b"".join(chunks))
    except Exception:
        return []
    # Nome de uma palavra só: exige token com limite de palavra (menos ruído tipo "davi" em substring)
    if len(name_tokens) == 1:
        tok = re.escape(name_tokens[0])
        name_pat = re.compile(rf"(?:^|[^a-z0-9áàâãéêíóôõúç]){tok}(?:$|[^a-z0-9áàâãéêíóôõúç])")
    elif len(name_tokens) >= 2:
        name_pat = re.compile(
            ".*" + "".join(rf"(?=.*{re.escape(t)})" for t in name_tokens),
            re.DOTALL,
        )
    else:
        name_pat = None
    out: list[dict] = []
    for e in getattr(parsed, "entries", []) or []:
        if len(out) >= max_entries:
            break
        title = e.get("title") or ""
        summary = strip_html_snippet(e.get("summary") or e.get("description") or "")
        blob = norm_key(f"{title} {summary}")
        ok = False
        if name_pat is not None:
            ok = bool(name_pat.search(blob))
        elif name_key in blob:
            ok = True
        if ok:
            out.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": e.get("link") or "",
                    "published_at": e.get("published") or e.get("updated") or "",
                }
            )
    return out


def duckduckgo_text(query: str, max_results: int) -> list[dict]:
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
    cfg = load_open_web_cfg()
    delays = cfg.get("delays_seconds") or {}
    lim = cfg.get("limits") or {}
    dw = float(delays.get("wikipedia", 0.35))
    dn = float(delays.get("google_news", 0.55))
    ds = float(delays.get("web_search", 0.85))
    df = float(delays.get("feed", 0.45))

    wiki_hits = int(lim.get("wiki_search_hits", 1))
    wiki_chars = int(lim.get("wiki_extract_max_chars", 1200))
    gn_limit = int(lim.get("google_news_per_query", 8))
    ws_max = int(lim.get("web_search_max_results", 6))
    feed_max = int(lim.get("feed_entries_per_source", 15))
    feed_bytes = int(lim.get("feed_fetch_max_bytes", 1_500_000))
    use_en = bool(cfg.get("wikipedia_en", True))
    en_limit = int(cfg.get("wikipedia_en_limit", 1))

    feeds_br = cfg.get("feeds_br") or []

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
        name_key = norm_key(name)
        parts = [tok for tok in re.split(r"\s+", name_key) if len(tok) > 2]
        name_for_feed = name_key if name_key else ""

        # --- Wikipedia PT ---
        for w in wiki_search("pt", name, limit=wiki_hits):
            intro = wiki_extract_intro("pt", w["title"], wiki_chars) if w["title"] else ""
            desc = intro if intro else w["snippet"]
            text = f"{w['title']}\n{desc}"
            append_jsonl(
                path,
                {
                    "platform": "wikipedia",
                    "profile_name": name,
                    "handle": ig,
                    "title": w["title"],
                    "description": desc,
                    "caption": "",
                    "text": text,
                    "url": w["url"],
                    "published_at": "",
                    "collected_at": now,
                    "source_detail": "pt.wikipedia intro" if intro else "pt.wikipedia search",
                },
            )
        time.sleep(dw)

        # --- Wikipedia EN (se ativo e nome parece pessoa) ---
        if use_en and len(parts) >= 2:
            for w in wiki_search("en", name, limit=en_limit):
                intro = wiki_extract_intro("en", w["title"], wiki_chars) if w["title"] else ""
                desc = intro if intro else w["snippet"]
                text = f"{w['title']}\n{desc}"
                append_jsonl(
                    path,
                    {
                        "platform": "wikipedia",
                        "profile_name": name,
                        "handle": ig,
                        "title": w["title"],
                        "description": desc,
                        "caption": "",
                        "text": text,
                        "url": w["url"],
                        "published_at": "",
                        "collected_at": now,
                        "source_detail": "en.wikipedia intro" if intro else "en.wikipedia search",
                    },
                )
            time.sleep(dw)

        # --- RSS veículos BR ---
        for feed in feeds_br:
            url = str(feed.get("url") or "").strip()
            label = str(feed.get("label") or "feed")
            if not url:
                continue
            for item in feed_entries_filtered(
                url, name_for_feed, feed_max, parts, feed_bytes
            ):
                blob = f"{item['title']} {item['summary']}"
                append_jsonl(
                    path,
                    {
                        "platform": "news_portal",
                        "profile_name": name,
                        "handle": ig,
                        "title": item["title"],
                        "description": item["summary"],
                        "caption": "",
                        "text": blob,
                        "url": item["url"],
                        "published_at": item["published_at"],
                        "collected_at": now,
                        "source_detail": label,
                    },
                )
            time.sleep(df)

        # --- Google Notícias ---
        news_q = f'"{name}"'
        if ig:
            news_q = f'"{name}" OR @{ig}'
        for item in google_news_rss(news_q, limit=gn_limit):
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
        time.sleep(dn)

        # --- Busca web (uma consulta combinada) ---
        q_web = f'{name} ("{name}" polêmica OR "{name}" aposta OR "{name}" loteria)'
        for d in duckduckgo_text(q_web, max_results=ws_max):
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
        time.sleep(ds)

    print("Open web gravado em", path)


if __name__ == "__main__":
    main()
