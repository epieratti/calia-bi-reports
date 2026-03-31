#!/usr/bin/env python3
"""
Classifica textos agregados (título + legenda + descrição) em três eixos:
concorrência, polêmicas, política — por correspondência com listas em keywords.yaml.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS_PATH = ROOT / "config" / "keywords.yaml"
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def load_keywords() -> dict[str, list[str]]:
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_hits(text: str, terms: list[str]) -> list[str]:
    t = normalize(text)
    hits: list[str] = []
    for term in terms:
        n = normalize(term)
        if not n.strip():
            continue
        if re.search(re.escape(n), t):
            hits.append(term)
    return hits


def aggregate_record(rec: dict) -> str:
    parts = [
        str(rec.get("title") or ""),
        str(rec.get("description") or ""),
        str(rec.get("caption") or ""),
        str(rec.get("text") or ""),
    ]
    return " \n ".join(p for p in parts if p.strip())


def main() -> None:
    kw = load_keywords()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    for path in sorted(RAW_DIR.glob("*.jsonl")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                # Ignora linhas só de diagnóstico (sem conteúdo de post)
                if rec.get("note") and not str(rec.get("url", "")).strip():
                    continue
                if rec.get("error") and not aggregate_record(rec).strip():
                    continue
                blob = aggregate_record(rec)
                if not blob.strip():
                    continue
                c1 = find_hits(blob, kw.get("concorrencia") or [])
                c2 = find_hits(blob, kw.get("polemicas") or [])
                c3 = find_hits(blob, kw.get("politica") or [])
                rows.append(
                    {
                        "source_file": path.name,
                        "platform": rec.get("platform", ""),
                        "profile": rec.get("profile_name", ""),
                        "handle": rec.get("handle", ""),
                        "url": rec.get("url", ""),
                        "published_at": rec.get("published_at", ""),
                        "risk_concorrencia": "sim" if c1 else "não",
                        "hits_concorrencia": "; ".join(c1),
                        "risk_polemicas": "sim" if c2 else "não",
                        "hits_polemicas": "; ".join(c2),
                        "risk_politica": "sim" if c3 else "não",
                        "hits_politica": "; ".join(c3),
                        "text_sample": (blob[:500] + "…") if len(blob) > 500 else blob,
                    }
                )

    csv_path = OUT_DIR / "classified_posts.csv"
    if rows:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    summary = {
        "total_rows": len(rows),
        "with_concorrencia": sum(1 for r in rows if r["risk_concorrencia"] == "sim"),
        "with_polemicas": sum(1 for r in rows if r["risk_polemicas"] == "sim"),
        "with_politica": sum(1 for r in rows if r["risk_politica"] == "sim"),
        "csv": str(csv_path.relative_to(ROOT)) if rows else None,
    }
    with open(OUT_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
