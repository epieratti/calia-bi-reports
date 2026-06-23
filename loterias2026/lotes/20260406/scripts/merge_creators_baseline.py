#!/usr/bin/env python3
"""
Reconstrói uma tabela única a partir dos CSVs do lote (stdlib apenas).
Uso: python3 scripts/merge_creators_baseline.py
Saída: data/creators_master_rebuild.csv (não sobrescreve creators_master.csv manual).
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_ig() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open(DATA / "social_blade_instagram.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["handle"]] = row
    return out


def load_tiktok() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open(DATA / "tiktok_handles_verificados.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["instagram_handle"]] = row
    return out


def load_yt() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open(DATA / "youtube_handles_verificados.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["nome_instagram"]] = row
    return out


def load_sb_yt() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open(DATA / "social_blade_youtube.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["instagram_handle"]] = row
    return out


def load_x() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with open(DATA / "x_handles_verificados.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["instagram_handle"]] = row
    return out


def main() -> None:
    ig = load_ig()
    tt = load_tiktok()
    yt = load_yt()
    sb = load_sb_yt()
    x = load_x()

    # Instagram handles from influencers — parse yaml simple
    yaml_path = DATA / "influencers.yaml"
    handles: list[str] = []
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("instagram:"):
            handles.append(line.split(":", 1)[1].strip())

    fields = [
        "instagram_handle",
        "ig_seguidores",
        "ig_taxa_engaj_pct",
        "tiktok_handle",
        "youtube_channel_id",
        "youtube_sb_match",
        "x_handle_oficial",
        "x_perfil_confirmado",
    ]
    rows = []
    for h in handles:
        r = {"instagram_handle": h}
        r["ig_seguidores"] = ig.get(h, {}).get("seguidores", "")
        r["ig_taxa_engaj_pct"] = ig.get(h, {}).get("taxa_engaj_pct", "")
        r["tiktok_handle"] = tt.get(h, {}).get("tiktok_handle", "")
        r["youtube_channel_id"] = yt.get(h, {}).get("channel_id", "")
        r["youtube_sb_match"] = sb.get(h, {}).get("sb_match", "")
        r["x_handle_oficial"] = x.get(h, {}).get("x_handle_oficial", "")
        r["x_perfil_confirmado"] = x.get(h, {}).get("perfil_confirmado", "")
        rows.append(r)

    out_path = DATA / "creators_master_rebuild.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})
    print(f"Wrote {out_path} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
