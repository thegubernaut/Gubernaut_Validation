#!/usr/bin/env python3
# STAGE3_MARKER_4x4
"""Extend the per-turn endurance time-series to all FOUR cooks (adds Grok 4.3).

The frozen 3-cook extractor (`extract_series.py`) reads the original schema
(`mann_intensity` / `mann_valence` / `guna`). Grok was sealed later (2026-06-20)
in a sibling schema (`impulse_intensity` / `impulse_valence` / `controller`) and
its panel carries a 4th judge family (`xai`). This script normalises both schemas
into one tidy long table so the trace figures can show the 4×4 story.

Inputs (read-only, sealed):
    ../raw/endurance_endurance_tri_cook{GPT,Opus,Gemini,Grok}.json
    ../raw/panel_tri_cook{GPT,Opus,Gemini}.json          (3-judge panels)
    ../raw/panel_tri_cook{GPT,Opus,Gemini,Grok}_4judge.json  (4-judge panels)

Outputs:
    ../tables/series_endurance_long_4x4.csv
    ../tables/dampening_summary_4x4.csv

raw_impulse  = intensity * max(0, -valence)   (the controller's reactivity drive)
react_median = cross-judge median of the panel judges' reactivity per unit
No withheld controller constants (gains/decay/thresholds) are emitted.
"""
import csv, json, statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW, OUT = BASE / "raw", BASE / "tables"
OUT.mkdir(parents=True, exist_ok=True)

COOKS = ["GPT", "Opus", "Gemini", "Grok"]
# 4-judge panels exist for every cook; prefer them so xai reactivity is included.
JUDGES = ["claude", "gemini", "openai", "xai"]


def turn_fields(t):
    """Normalise a turn dict across the two sealed schemas."""
    intensity = t.get("mann_intensity", t.get("impulse_intensity"))
    valence = t.get("mann_valence", t.get("impulse_valence"))
    ctl = t.get("guna") or t.get("controller") or {}
    arousal = ctl.get("rajas", ctl.get("arousal"))
    equil = ctl.get("sattva", ctl.get("equilibrium"))
    persev = ctl.get("tamas", ctl.get("perseveration"))
    recovery = ctl.get("recovery")
    return intensity, valence, arousal, equil, persev, recovery


def load_panel(cook):
    """Return {unit_id: {judge: {reactivity, self_reference}}} from the richest panel."""
    p4 = RAW / f"panel_tri_cook{cook}_4judge.json"
    p3 = RAW / f"panel_tri_cook{cook}.json"
    path = p4 if p4.exists() else p3
    return json.loads(path.read_text(encoding="utf-8"))["scores"]


rows = []
for cook in COOKS:
    end = json.loads((RAW / f"endurance_endurance_tri_cook{cook}.json").read_text(encoding="utf-8"))
    scores = load_panel(cook)
    for seq in end["sequences"]:
        sid = seq["seq_id"]
        for arm in ("regulated", "baseline"):
            for t in seq[arm]:
                turn = t["turn"]
                uid = f"{sid}:T{turn:02d}:{arm}"
                sc = scores.get(uid, {})
                rvals = [(sc.get(j) or {}).get("reactivity") for j in JUDGES]
                rvals = [v for v in rvals if v is not None]
                svals = [(sc.get(j) or {}).get("self_reference") for j in JUDGES]
                svals = [v for v in svals if v is not None]
                intensity, valence, arousal, equil, persev, recovery = turn_fields(t)
                rows.append({
                    "generator": cook,
                    "seq_id": sid,
                    "theme": seq.get("theme", ""),
                    "turn": turn,
                    "arm": arm,
                    "phase": t.get("phase"),
                    "posture": {"RAJAS": "INHIBIT", "TAMAS": "REGROUND"}.get(t.get("posture"), t.get("posture")),
                    "impulse_intensity": intensity,
                    "impulse_valence": valence,
                    "raw_impulse": round((intensity or 0) * max(0.0, -(valence or 0)), 4),
                    "equilibrium": equil,
                    "arousal": arousal,
                    "perseveration": persev,
                    "recovery": recovery,
                    "react_median": statistics.median(rvals) if rvals else None,
                    "selfref_median": statistics.median(svals) if svals else None,
                })

with open(OUT / "series_endurance_long_4x4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ---- dampening summary on provoked turns, per cook x sequence ----
damp = []
for cook in COOKS:
    for sid in ["S1", "S2", "S3", "S4", "S5"]:
        sub = [r for r in rows if r["generator"] == cook and r["seq_id"] == sid]
        prov = sorted({r["turn"] for r in sub if r["raw_impulse"] > 0})
        if not prov:
            continue
        def mean_react(arm):
            vals = [r["react_median"] for r in sub if r["arm"] == arm and r["turn"] in prov and r["react_median"] is not None]
            return statistics.mean(vals) if vals else None
        reg, base = mean_react("regulated"), mean_react("baseline")
        imp = statistics.mean([r["raw_impulse"] for r in sub if r["arm"] == "regulated" and r["turn"] in prov])
        damp.append({
            "generator": cook, "seq_id": sid, "n_provoked_turns": len(prov),
            "mean_raw_impulse": round(imp, 3),
            "mean_react_regulated": round(reg, 3) if reg else None,
            "mean_react_baseline": round(base, 3) if base else None,
            "dampening_diff": round(base - reg, 3) if (reg and base) else None,
            "dampening_ratio": round(reg / base, 3) if base else None,
        })

with open(OUT / "dampening_summary_4x4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(damp[0].keys()))
    w.writeheader()
    w.writerows(damp)

n_grok = sum(1 for r in rows if r["generator"] == "Grok")
print(f"rows: {len(rows)} (expect 400 = 4 cooks x 5 seq x 10 turns x 2 arms); Grok rows: {n_grok}")
print(f"dampening rows: {len(damp)}")
missing = [r for r in rows if r["react_median"] is None]
print(f"turns with no panel score: {len(missing)}")
