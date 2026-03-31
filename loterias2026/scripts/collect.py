#!/usr/bin/env python3
"""
Coleta inicial para Brand Safety — Always ON Loterias 2026.

- YouTube: RSS público (feedparser) + resolução de @handle via yt-dlp quando necessário.
- Instagram / TikTok / X: chamadas opcionais à API Apify (APIFY_TOKEN + IDs dos Actors).
- X alternativo: API oficial v2 com TWITTER_BEARER_TOKEN (limitado por plano).

Saída: data/raw/*.jsonl (um arquivo por plataforma), linhas JSON por post.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import feedparser
import requests
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
INFLUENCERS_PATH = ROOT / "data" / "influencers.yaml"

load_dotenv(ROOT / ".env")

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Loterias2026-BrandSafety/1.0 (research; +https://github.com)",
        "Accept": "application/json",
    }
)


def load_profiles() -> list[dict]:
    with open(INFLUENCERS_PATH, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return list(data.get("profiles") or [])


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def youtube_channel_id_from_handle(handle: str) -> str | None:
    """Resolve @handle ou URL para channel_id usando yt-dlp (sem API key)."""
    h = handle.strip().lstrip("@")
    url = f"https://www.youtube.com/@{h}"
    try:
        out = subprocess.run(
            [
                sys.executable,
                "-m",
                "yt_dlp",
                "--print",
                "%(channel_id)s",
                "--playlist-end",
                "0",
                "--no-warnings",
                "--quiet",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(ROOT),
        )
        cid = (out.stdout or "").strip()
        if cid.startswith("UC") and len(cid) >= 10:
            return cid
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def fetch_youtube_rss(channel_id: str, limit: int = 15) -> list[dict]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={quote(channel_id, safe='')}"
    parsed = feedparser.parse(url)
    out: list[dict] = []
    for i, e in enumerate(getattr(parsed, "entries", []) or []):
        if i >= limit:
            break
        vid = None
        if e.get("yt_videoid"):
            vid = e["yt_videoid"]
        elif e.get("id"):
            # often tag:youtube.com,2008:video:VIDEOID
            parts = str(e["id"]).split(":")
            if parts:
                vid = parts[-1]
        link = e.get("link") or (f"https://www.youtube.com/watch?v={vid}" if vid else "")
        out.append(
            {
                "title": e.get("title") or "",
                "description": e.get("summary") or e.get("description") or "",
                "published_at": e.get("published") or e.get("updated") or "",
                "url": link,
                "video_id": vid or "",
            }
        )
    return out


def apify_actor_path(actor_id: str) -> str:
    """Apify espera username~actorName na URL (barra vira til)."""
    return actor_id.strip().replace("/", "~")


def run_apify_actor(actor_id: str, run_input: dict, token: str) -> dict | None:
    """Inicia run e aguarda dataset (simplificado)."""
    base = "https://api.apify.com/v2"
    aid = apify_actor_path(actor_id)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = SESSION.post(
        f"{base}/acts/{aid}/runs",
        headers=headers,
        json=run_input,
        timeout=60,
    )
    if not r.ok:
        return None
    run = r.json().get("data") or {}
    rid = run.get("id")
    if not rid:
        return None
    for _ in range(120):
        s = SESSION.get(f"{base}/actor-runs/{rid}", headers=headers, timeout=60)
        if not s.ok:
            return None
        st = (s.json().get("data") or {}).get("status")
        if st in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        time.sleep(2)
    d = SESSION.get(f"{base}/actor-runs/{rid}/dataset/items", headers=headers, timeout=120)
    if not d.ok:
        return None
    return {"items": d.json(), "run_id": rid}


def collect_youtube(profiles: list[dict]) -> Path:
    path = DATA_RAW / "youtube.jsonl"
    if path.exists():
        path.unlink()
    for p in profiles:
        name = p.get("name", "")
        yt = str(p.get("youtube") or "").strip()
        if not yt:
            continue
        cid = yt if yt.startswith("UC") else youtube_channel_id_from_handle(yt)
        if not cid:
            append_jsonl(
                path,
                {
                    "platform": "youtube",
                    "profile_name": name,
                    "handle": yt,
                    "error": "channel_id não resolvido",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            continue
        for item in fetch_youtube_rss(cid, limit=20):
            append_jsonl(
                path,
                {
                    "platform": "youtube",
                    "profile_name": name,
                    "handle": yt,
                    "channel_id": cid,
                    "title": item["title"],
                    "description": item["description"],
                    "caption": "",
                    "url": item["url"],
                    "published_at": item["published_at"],
                    "video_id": item["video_id"],
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            )
        time.sleep(0.5)
    return path


def collect_apify_placeholder(
    platform: str,
    actor_env: str,
    profiles: list[dict],
    build_input,
) -> Path:
    path = DATA_RAW / f"{platform}.jsonl"
    if path.exists():
        path.unlink()
    token = os.environ.get("APIFY_TOKEN", "").strip()
    actor_id = os.environ.get(actor_env, "").strip()
    if not token or not actor_id:
        append_jsonl(
            path,
            {
                "platform": platform,
                "note": f"Configure APIFY_TOKEN e {actor_env} no .env para coleta Apify.",
                "collected_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        return path
    for p in profiles:
        inp = build_input(p)
        res = run_apify_actor(actor_id, inp, token)
        if not res:
            append_jsonl(
                path,
                {
                    "platform": platform,
                    "profile_name": p.get("name"),
                    "error": "Apify run falhou ou sem itens",
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            continue
        for item in res.get("items") or []:
            rec = {
                "platform": platform,
                "profile_name": p.get("name"),
                "handle": inp.get("username") or inp.get("usernames") or "",
                "raw": item,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
            # Normalização mínima (Actors variam no schema)
            if isinstance(item, dict):
                rec["url"] = item.get("url") or item.get("webVideoUrl") or item.get("postUrl") or ""
                rec["title"] = item.get("title") or item.get("text") or ""
                rec["caption"] = item.get("caption") or item.get("description") or rec["title"]
                rec["description"] = item.get("description") or ""
                rec["published_at"] = str(
                    item.get("timestamp")
                    or item.get("date")
                    or item.get("createdAt")
                    or ""
                )
            append_jsonl(path, rec)
        time.sleep(1)
    return path


def collect_x_tweepy(profiles: list[dict]) -> None:
    path = DATA_RAW / "x.jsonl"
    bearer = os.environ.get("TWITTER_BEARER_TOKEN", "").strip()
    if not bearer:
        return
    try:
        import tweepy
    except ImportError:
        return
    if path.exists():
        path.unlink()
    client = tweepy.Client(bearer_token=bearer)
    for p in profiles:
        x = str(p.get("x") or "").strip().lstrip("@")
        if not x:
            continue
        try:
            # Requer acesso de busca no plano; pode falhar em tier gratuito.
            resp = client.search_recent_tweets(
                query=f"from:{x} -is:retweet",
                max_results=10,
                tweet_fields=["created_at", "text"],
            )
            tweets = resp.data or []
            for tw in tweets:
                append_jsonl(
                    path,
                    {
                        "platform": "x",
                        "profile_name": p.get("name"),
                        "handle": x,
                        "title": "",
                        "description": "",
                        "caption": "",
                        "text": tw.text,
                        "url": f"https://twitter.com/{x}/status/{tw.id}",
                        "published_at": tw.created_at.isoformat() if tw.created_at else "",
                        "collected_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
        except tweepy.TweepyException as e:
            append_jsonl(
                path,
                {
                    "platform": "x",
                    "profile_name": p.get("name"),
                    "handle": x,
                    "error": str(e),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                },
            )
        time.sleep(1)


def main() -> None:
    profiles = load_profiles()
    collect_youtube(profiles)

    collect_apify_placeholder(
        "instagram",
        "APIFY_INSTAGRAM_ACTOR_ID",
        profiles,
        lambda p: {"username": [str(p.get("instagram") or "").replace("@", "")], "resultsLimit": 15},
    )
    collect_apify_placeholder(
        "tiktok",
        "APIFY_TIKTOK_ACTOR_ID",
        profiles,
        lambda p: {"profiles": [str(p.get("tiktok") or "").replace("@", "")], "resultsPerPage": 15},
    )
    collect_apify_placeholder(
        "x",
        "APIFY_X_ACTOR_ID",
        profiles,
        lambda p: {"searchTerms": [str(p.get("x") or "").replace("@", "")], "maxTweets": 15},
    )

    collect_x_tweepy(profiles)

    print("Coleta gravada em", DATA_RAW)


if __name__ == "__main__":
    main()
