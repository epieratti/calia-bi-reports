#!/usr/bin/env python3
"""
Proxy de penetração EUA + Europa: Google Trends (interesse por país) e
pageviews Wikipedia EN (últimos ~90 dias). Não substitui painéis oficiais.
"""
from __future__ import annotations

import csv
import json
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

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

# (rótulo dossiê, termo Trends, título Wikipedia EN para pageviews — ajustado se search falhar)
ARTISTAS = [
    ("Tiago Iorc", "Tiago Iorc", "Tiago Iorc"),
    ("Marisa Monte", "Marisa Monte", "Marisa Monte"),
    ("Djavan", "Djavan", "Djavan"),
    ("Carlinhos Brown", "Carlinhos Brown", "Carlinhos Brown"),
    # Nome civil tende a volume zero no Trends; termo descritivo captura buscas reais.
    ("Júnior (futebol)", "Júnior comentarista Globo", "Júnior (footballer, born 1973)"),
    ("Samuel Rosa", "Samuel Rosa", "Samuel Rosa"),
    ("Bebel Gilberto", "Bebel Gilberto", "Bebel Gilberto"),
    ("Seu Jorge", "Seu Jorge", "Seu Jorge"),
    ("Liniker", "Liniker", "Liniker"),
    ("Zeca Pagodinho", "Zeca Pagodinho", "Zeca Pagodinho"),
]

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "CaliaBI-Research/1.0 (educational; contact@example.com)"})


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
        r = SESSION.get(url, params=params, timeout=30)
        r.raise_for_status()
        hits = r.json().get("query", {}).get("search", [])
        return hits[0]["title"].replace(" ", "_") if hits else None
    except Exception:
        return None


def wiki_pageviews_90d(title: str) -> int | None:
    """Soma pageviews diários últimos ~90 dias no EN wiki."""
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
        r = SESSION.get(url, timeout=30)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        items = r.json().get("items", [])
        return sum(x.get("views", 0) for x in items)
    except Exception:
        return None


def trends_by_country(term: str) -> dict[str, float]:
    pytrends = TrendReq(hl="pt-BR", tz=360, timeout=(10, 25))
    pytrends.build_payload([term], timeframe="today 12-m", geo="")
    df = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False)
    if df.empty or term not in df.columns:
        return {}
    col = term
    out = {}
    for _, name in PAISES.items():
        if name in df.index:
            out[name] = float(df.loc[name, col])
        else:
            out[name] = 0.0
    return out


def normalizar_slice(scores: dict[str, float], keys: list[str]) -> dict[str, float]:
    s = sum(max(0, scores.get(k, 0)) for k in keys)
    if s <= 0:
        return {k: 0.0 for k in keys}
    return {k: round(100 * max(0, scores.get(k, 0)) / s, 2) for k in keys}


def main():
    rows = []
    pytrends = TrendReq(hl="pt-BR", tz=360, timeout=(10, 25))

    for label, trend_term, wiki_guess in ARTISTAS:
        row = {"artista": label, "termo_trends": trend_term}

        # Wikipedia
        wt = wiki_search_title(wiki_guess.replace("_", " ")) or wiki_guess.replace(" ", "_")
        views = wiki_pageviews_90d(wt.replace("_", " "))
        row["wiki_en_titulo"] = wt.replace("_", " ")
        row["wiki_en_views_90d"] = views if views is not None else ""
        time.sleep(0.4)

        # Trends
        try:
            pytrends.build_payload([trend_term], timeframe="today 12-m", geo="")
            df = pytrends.interest_by_region(
                resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False
            )
            scores = {}
            if not df.empty and trend_term in df.columns:
                for _, nome in PAISES.items():
                    scores[nome] = float(df.loc[nome, trend_term]) if nome in df.index else 0.0
            else:
                scores = {n: 0.0 for n in PAISES.values()}

            mercado = [PAISES["us"], PAISES["uk"], PAISES["fr"], PAISES["de"], PAISES["it"], PAISES["es"], PAISES["pt"]]
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
        print(row.get("artista"), "OK" if "trends_erro" not in row else row.get("trends_erro"))
        time.sleep(3.5)  # evitar bloqueio Trends

    out_csv = "/workspace/embratur/research/penetracao_trends_wiki_2026.csv"
    out_json = "/workspace/embratur/research/penetracao_trends_wiki_2026.json"
    if rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
    print("Salvo:", out_csv)


if __name__ == "__main__":
    main()
