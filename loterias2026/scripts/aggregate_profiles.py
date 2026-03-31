#!/usr/bin/env python3
"""
Agrega `classified_posts.csv` por personalidade (nome do briefing).
Saída: profile_summary.json e profile_risk_matrix.csv
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
INFLUENCERS = ROOT / "data" / "influencers.yaml"


def load_profile_names() -> list[str]:
    with open(INFLUENCERS, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [str(p.get("name") or "").strip() for p in (data.get("profiles") or []) if p.get("name")]


def main() -> None:
    csv_path = PROCESSED / "classified_posts.csv"
    PROCESSED.mkdir(parents=True, exist_ok=True)
    names = load_profile_names()
    campaign = "Always ON Loterias 2026"
    with open(INFLUENCERS, encoding="utf-8") as f:
        inf = yaml.safe_load(f) or {}
        campaign = str(inf.get("campaign") or campaign)

    by_profile: dict[str, list[dict]] = defaultdict(list)
    note = None
    if not csv_path.is_file():
        note = "Sem classified_posts.csv — rode collect.py (com APIFY_TOKEN) e classify.py."
    else:
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                note = "CSV de classificação vazio ou inválido."
            else:
                for row in reader:
                    prof = str(row.get("profile") or "").strip()
                    if prof:
                        by_profile[prof].append(row)
        if not by_profile and note is None:
            note = "Nenhum post classificável na coleta atual (verifique token Apify e erros em data/raw/*.jsonl)."

    axes = ("concorrencia", "polemicas", "politica")
    profiles_out: list[dict] = []

    for name in names:
        rows = by_profile.get(name, [])
        per_platform: dict[str, int] = defaultdict(int)
        risk_any = {a: False for a in axes}
        hits_union: dict[str, set[str]] = {a: set() for a in axes}
        evidence: dict[str, list[dict]] = {a: [] for a in axes}

        for r in rows:
            plat = str(r.get("platform") or "?")
            per_platform[plat] += 1
            for a in axes:
                key_risk = f"risk_{a}"
                key_hits = f"hits_{a}"
                if r.get(key_risk) == "sim":
                    risk_any[a] = True
                    hs = str(r.get(key_hits) or "")
                    for h in [x.strip() for x in hs.split(";") if x.strip()]:
                        hits_union[a].add(h)
                    if len(evidence[a]) < 8:
                        evidence[a].append(
                            {
                                "platform": r.get("platform", ""),
                                "url": r.get("url", ""),
                                "published_at": r.get("published_at", ""),
                                "hits": hs,
                                "sample": (r.get("text_sample") or "")[:280],
                            }
                        )

        level = "baixo"
        if any(risk_any.values()):
            level = "médio"
        if sum(1 for v in risk_any.values() if v) >= 2:
            level = "alto (revisar)"

        profiles_out.append(
            {
                "name": name,
                "posts_classificados": len(rows),
                "posts_por_plataforma": dict(per_platform),
                "risco": {
                    "concorrencia": "sim" if risk_any["concorrencia"] else "não",
                    "polemicas": "sim" if risk_any["polemicas"] else "não",
                    "politica": "sim" if risk_any["politica"] else "não",
                },
                "nivel_heuristico": level,
                "termos_detectados": {a: sorted(hits_union[a]) for a in axes},
                "evidencias": evidence,
            }
        )

    summary = {
        "campaign": campaign,
        "total_perfis": len(profiles_out),
        "total_linhas_classificadas": sum(p["posts_classificados"] for p in profiles_out),
        "profiles": profiles_out,
    }
    if note:
        summary["note"] = note
    with open(PROCESSED / "profile_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    matrix_path = PROCESSED / "profile_risk_matrix.csv"
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "perfil",
                "posts",
                "risco_concorrencia",
                "risco_polemicas",
                "risco_politica",
                "nivel_heuristico",
            ]
        )
        for p in profiles_out:
            w.writerow(
                [
                    p["name"],
                    p["posts_classificados"],
                    p["risco"]["concorrencia"],
                    p["risco"]["polemicas"],
                    p["risco"]["politica"],
                    p["nivel_heuristico"],
                ]
            )

    print(json.dumps({"profile_summary": str(PROCESSED / "profile_summary.json"), "matrix": str(matrix_path)}, indent=2))


if __name__ == "__main__":
    main()
