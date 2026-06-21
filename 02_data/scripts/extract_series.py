#!/usr/bin/env python3
# PHASE2_MARKER_V1
"""Extract per-turn endurance time-series from the immutable raw record.

Inputs (read-only):  ../raw/endurance_endurance_tri_cook{GPT,Opus,Gemini}.json
                     ../raw/panel_tri_cook{GPT,Opus,Gemini}.json
Outputs:             ../tables/series_endurance_long.csv   (tidy long format)
                     ../tables/dampening_summary.csv       (per cook x sequence)

Definitions
-----------
raw_impulse      = mann_intensity * max(0, -mann_valence)   (the controller's P drive)
react_median     = cross-judge median of the 3 panel judges' reactivity (each judge
                   value is itself the median of 3 samples at temp 0.0, as stored)
provoked turn    = raw_impulse > 0 (hostile-valence input)
dampening_diff   = mean(baseline react) - mean(regulated react) on provoked turns
dampening_ratio  = mean(regulated react) / mean(baseline react) on provoked turns
"""
import csv
import json
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW, OUT = BASE / "raw", BASE / "tables"
OUT.mkdir(parents=True, exist_ok=True)

COOKS = ["GPT", "Opus", "Gemini"]
JUDGES = ["claude", "gemini", "openai"]

rows = []
postures, phases = set(), set()
mann_mismatches = 0

for cook in COOKS:
    end = json.loads((RAW / f"endurance_endurance_tri_cook{cook}.json").read_text(encoding="utf-8"))
    panel = json.loads((RAW / f"panel_tri_cook{cook}.json").read_text(encoding="utf-8"))
    scores = panel["scores"]
    for seq in end["sequences"]:
        sid = seq["seq_id"]
        # sanity: Mann readings should be identical across arms (same scripted input)
        for reg_t, base_t in zip(seq["regulated"], seq["baseline"]):
            if (reg_t["mann_intensity"], reg_t["mann_valence"]) != (base_t["mann_intensity"], base_t["mann_valence"]):
                mann_mismatches += 1
        for arm in ("regulated", "baseline"):
            for t in seq[arm]:
                turn = t["turn"]
                uid = f"{sid}:T{turn:02d}:{arm}"
                sc = scores.get(uid, {})
                reacts = {j: (sc.get(j) or {}).get("reactivity") for j in JUDGES}
                selfs = {j: (sc.get(j) or {}).get("self_reference") for j in JUDGES}
                rvals = [v for v in reacts.values() if v is not None]
                svals = [v for v in selfs.values() if v is not None]
                guna = t.get("guna") or {}
                postures.add(t["posture"])
                phases.add(t.get("phase"))
                rows.append({
                    "generator": cook,
                    "seq_id": sid,
                    "theme": seq["theme"],
                    "turn": turn,
                    "arm": arm,
                    "phase": t.get("phase"),
                    "posture": {"RAJAS": "INHIBIT", "TAMAS": "REGROUND"}.get(t["posture"], t["posture"]),
                    "impulse_intensity": t["mann_intensity"],
                    "impulse_valence": t["mann_valence"],
                    "raw_impulse": round(t["mann_intensity"] * max(0.0, -t["mann_valence"]), 4),
                    "equilibrium": guna.get("sattva"),
                    "arousal": guna.get("rajas"),
                    "perseveration": guna.get("tamas"),
                    "recovery": guna.get("recovery"),
                    "react_claude": reacts["claude"],
                    "react_gemini": reacts["gemini"],
                    "react_openai": reacts["openai"],
                    "react_median": statistics.median(rvals) if rvals else None,
                    "selfref_median": statistics.median(svals) if svals else None,
                })

with open(OUT / "series_endurance_long.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# ---- dampening summary: per cook x sequence over provoked turns ----
damp = []
for cook in COOKS:
    for sid in ["S1", "S2", "S3", "S4", "S5"]:
        sub = [r for r in rows if r["generator"] == cook and r["seq_id"] == sid]
        prov_turns = sorted({r["turn"] for r in sub if r["raw_impulse"] > 0})
        if not prov_turns:
            continue
        def mean_react(arm):
            vals = [r["react_median"] for r in sub if r["arm"] == arm and r["turn"] in prov_turns]
            return statistics.mean(vals)
        reg, base = mean_react("regulated"), mean_react("baseline")
        imp = statistics.mean([r["raw_impulse"] for r in sub if r["arm"] == "regulated" and r["turn"] in prov_turns])
        damp.append({
            "generator": cook, "seq_id": sid, "n_provoked_turns": len(prov_turns),
            "mean_raw_impulse": round(imp, 3),
            "mean_react_regulated": round(reg, 3),
            "mean_react_baseline": round(base, 3),
            "dampening_diff": round(base - reg, 3),
            "dampening_ratio": round(reg / base, 3) if base else None,
        })

with open(OUT / "dampening_summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(damp[0].keys()))
    w.writeheader()
    w.writerows(damp)

print(f"rows written: {len(rows)} (expect 300 = 3 cooks x 5 seq x 10 turns x 2 arms)")
print(f"impulse cross-arm mismatches (IGL is stochastic): {mann_mismatches} (expect 0)")
print(f"postures seen: {sorted(postures)}")
print(f"phases seen:   {sorted(p for p in phases if p)}")
print(f"dampening rows: {len(damp)}")
missing = [r for r in rows if r["react_median"] is None]
print(f"turns with no panel score: {len(missing)} (expect 0)")
