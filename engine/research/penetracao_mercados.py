#!/usr/bin/env python3
"""
Proxy de penetração (Google Trends por país + pageviews Wikipedia EN ~90d).
Uso genérico: lista de entidades num JSON — não acoplado a um cliente.

Exemplo:
  pip install -r tools/requirements-penetracao.txt
  python3 tools/penetracao_mercados.py \\
    --entities-json embratur/research/penetracao_entities_embratur_2026.json \\
    --output-prefix embratur/research/penetracao_trends_wiki_2026

Saída: <prefix>.csv e <prefix>.json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from pytrends.request import TrendReq

# Países-alvo como retornados pelo Trends com hl='pt-BR'
PAISES = {
    "br": "Brasil",
    "us": "Estados Unidos",
    "uk": "Reino Unido",
    "fr": "França",
    "de": "Alemanha",
    "it": "Itália",
    "es": "Espanha",
    "pt": "Portugal",
}

_SESSION = requests.Session()
_SESSION.headers.update(
    {"User-Agent": "CaliaBI-Research/1.0 (research; adjust contact in fork)"}
)


def wiki_search_title(query: str) -> str | None:
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 1,
    }
    try:
        r = _SESSION.get(url, params=params, timeout=30)
        r.raise_for_status()
        hits = r.json().get("query", {}).get("search", [])
        return hits[0]["title"].replace(" ", "_") if hits else None
    except Exception:
        return None


def wiki_pageviews_90d(title: str) -> int | None:
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=90)
    enc = urllib.parse.quote(title.replace(" ", "_"), safe="()%2C")
    a = start.strftime("%Y%m%d")
    b = end.strftime("%Y%m%d")
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia.org/all-access/user/{enc}/daily/{a}00/{b}00"
    )
    try:
        r = _SESSION.get(url, timeout=30)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        items = r.json().get("items", [])
        return sum(x.get("views", 0) for x in items)
    except Exception:
        return None


def normalizar_slice(scores: dict[str, float], keys: list[str]) -> dict[str, float]:
    s = sum(max(0, scores.get(k, 0)) for k in keys)
    if s <= 0:
        return {k: 0.0 for k in keys}
    return {k: round(100 * max(0, scores.get(k, 0)) / s, 2) for k in keys}


def load_entities(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise SystemExit(f"JSON deve ser uma lista não vazia: {path}")
    out = []
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            raise SystemExit(f"Item {i} não é objeto JSON: {path}")
        label = row.get("label")
        trend_term = row.get("trend_term")
        wiki_title = row.get("wiki_title")
        if not label or not trend_term or not wiki_title:
            raise SystemExit(
                f"Item {i} precisa de label, trend_term, wiki_title (strings): {path}"
            )
        out.append(
            {
                "label": str(label),
                "trend_term": str(trend_term),
                "wiki_title": str(wiki_title),
            }
        )
    return out


def run(entities: list[dict[str, str]]) -> list[dict]:
    rows = []
    pytrends = TrendReq(hl="pt-BR", tz=360, timeout=(10, 25))
    mercado = [
        PAISES["us"],
        PAISES["uk"],
        PAISES["fr"],
        PAISES["de"],
        PAISES["it"],
        PAISES["es"],
        PAISES["pt"],
    ]

    for ent in entities:
        label = ent["label"]
        trend_term = ent["trend_term"]
        wiki_guess = ent["wiki_title"]
        row: dict = {"artista": label, "termo_trends": trend_term}

        wt = wiki_search_title(wiki_guess.replace("_", " ")) or wiki_guess.replace(" ", "_")
        views = wiki_pageviews_90d(wt.replace("_", " "))
        row["wiki_en_titulo"] = wt.replace("_", " ")
        row["wiki_en_views_90d"] = views if views is not None else ""
        time.sleep(0.4)

        try:
            pytrends.build_payload([trend_term], timeframe="today 12-m", geo="")
            df = pytrends.interest_by_region(
                resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False
            )
            scores: dict[str, float] = {}
            if not df.empty and trend_term in df.columns:
                for _, nome in PAISES.items():
                    scores[nome] = (
                        float(df.loc[nome, trend_term]) if nome in df.index else 0.0
                    )
            else:
                scores = {n: 0.0 for n in PAISES.values()}

            norm_mercado = normalizar_slice(scores, mercado)
            norm_br_eua = normalizar_slice(scores, [PAISES["br"], PAISES["us"]])

            for k, v in scores.items():
                row[f"trends_{k}"] = v
            row["trends_proxy_pct_US"] = norm_mercado[PAISES["us"]]
            row["trends_proxy_pct_Europa_6"] = round(
                sum(norm_mercado[k] for k in mercado if k != PAISES["us"]), 2
            )
            row["trends_proxy_pct_BR_vs_US_BR"] = norm_br_eua.get(PAISES["br"], 0)
            row["trends_proxy_pct_US_vs_BR_US"] = norm_br_eua.get(PAISES["us"], 0)
        except Exception as e:
            row["trends_erro"] = str(e)[:120]

        rows.append(row)
        print(
            row.get("artista"),
            "OK" if "trends_erro" not in row else row.get("trends_erro"),
            file=sys.stderr,
        )
        time.sleep(3.5)

    return rows


def main() -> None:
    root = Path(__file__).resolve().parent
    default_entities = root / "penetracao_entities_example.json"

    ap = argparse.ArgumentParser(description="Trends + Wikipedia pageviews (proxy).")
    ap.add_argument(
        "--entities-json",
        type=Path,
        default=default_entities,
        help=f"Lista JSON: [{{label, trend_term, wiki_title}}, ...] (default: {default_entities.name})",
    )
    ap.add_argument(
        "--output-prefix",
        type=Path,
        required=True,
        help="Prefixo dos ficheiros de saída (sem extensão): gera .csv e .json",
    )
    args = ap.parse_args()

    path = args.entities_json.resolve()
    if not path.is_file():
        raise SystemExit(f"Ficheiro não encontrado: {path}")

    entities = load_entities(path)
    rows = run(entities)

    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    out_csv = prefix.with_suffix(".csv")
    out_json = prefix.with_suffix(".json")

    if rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
    print("Salvo:", out_csv, out_json, file=sys.stderr)


if __name__ == "__main__":
    main()
