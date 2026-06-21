"""
tri_combine.py — combine Stage-2 triangulation panels into the final 3x3 table.

Implements prereg_stage2_triangulation_20260610T142555Z.md sections 4-6:
per cook x judge cell effects (eval paired + endurance arm means), diagonal
(self-judge) cells tagged and split out, C-3 recovery output-calm check,
C-4 ego/self-reference microscope, C-5 inter-judge agreement, and the
headline cell count.

Reads ONLY panel_*.json files (judge scores) — transcripts are not needed
here; arousal trajectories (mechanical C-3 half) are checked from transcripts
separately at report time.

Usage (from project root):
    python -m tools.tri_combine \\
        --panel "GPT:openai:.tmp/runs/panel_tri_cookGPT.json" \\
        --panel "Opus:claude:.tmp/runs/panel_tri_cookOpus.json" \\
        --panel "Gemini:gemini:.tmp/runs/panel_tri_cookGemini.json" \\
        --out results/tri_final.json

Each --panel spec is  <cook_label>:<diagonal_judge_backend>:<path>.

This is general over N cooks and M judges: the backend set per cook is read from
each panel's "judges" dict, and the diagonal (self-judge) cell is the one whose
judge backend equals <diagonal_judge_backend>. For the 4×4 (Grok added as both
cook and judge), pass four panels, each judged by all four backends, with the
diagonal backend set to the cook's own family — e.g. the Grok cook's diagonal is
`xai`:
    python -m tools.tri_combine \\
        --panel "GPT:openai:<4-judge panel>" \\
        --panel "Opus:claude:<4-judge panel>" \\
        --panel "Gemini:gemini:<4-judge panel>" \\
        --panel "Grok:xai:<4-judge panel>" \\
        --out results/tri_final_4x4.json
"""

import sys
import io
import json
import argparse
import statistics
from pathlib import Path

if hasattr(sys.stdout, "buffer") and (sys.stdout.encoding or "").lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

DIMS = ("reactivity", "self_reference")
DE_ESC_TURNS = (8, 9, 10)
EARLY_TURNS = (1, 2, 3)
LATE_TURNS = (8, 9, 10)


# ---------------------------------------------------------------------------
# Stats helpers (same conventions as run_eval / rejudge)
# ---------------------------------------------------------------------------
def _paired(diffs: list) -> dict:
    if not diffs:
        return {"mean": 0.0, "sd": 0.0, "se": 0.0, "t": 0.0, "n": 0}
    n = len(diffs)
    m = statistics.mean(diffs)
    sd = statistics.stdev(diffs) if n > 1 else 0.0
    se = sd / (n ** 0.5) if n else 0.0
    return {"mean": round(m, 3), "sd": round(sd, 3), "se": round(se, 3),
            "t": round(m / se, 2) if se > 0 else 0.0, "n": n}


def _favor(item_means: list) -> dict:
    reg = sum(1 for d in item_means if d > 0)
    base = sum(1 for d in item_means if d < 0)
    return {"reg_wins": reg, "ties": len(item_means) - reg - base, "base_wins": base}


def _median3(vals: list) -> float:
    return statistics.median(vals)


def _pearson(x: list, y: list) -> float:
    n = len(x)
    if n < 2:
        return float("nan")
    mx, my = sum(x) / n, sum(y) / n
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = (sum((a - mx) ** 2 for a in x)) ** 0.5
    sy = (sum((b - my) ** 2 for b in y)) ** 0.5
    if sx == 0 or sy == 0:
        return float("nan")
    return round(num / (sx * sy), 3)


# ---------------------------------------------------------------------------
# Panel parsing
# ---------------------------------------------------------------------------
def _load_panel(path: Path) -> dict:
    p = json.loads(path.read_text(encoding="utf-8"))
    errors = [(uid, b) for uid, sc in p["scores"].items()
              for b, r in sc.items() if "error" in r]
    if errors:
        raise ValueError(f"{path}: {len(errors)} error score(s), e.g. {errors[:3]}")
    return p


def _eval_pairs(panel: dict, backend: str | None) -> dict:
    """item_id -> list of per-rep (base - reg) diffs, per dim.

    backend=None averages the three judges per unit before differencing.
    """
    units, scores = panel["units"], panel["scores"]
    by_key: dict = {}
    for uid, meta in units.items():
        if meta["kind"] != "eval":
            continue
        sc = scores[uid]
        val = {}
        for dim in DIMS:
            if backend is None:
                val[dim] = statistics.mean(sc[b][dim] for b in sc)
            else:
                val[dim] = sc[backend][dim]
        by_key[(meta["item_id"], meta["rep"], meta["arm"])] = val

    items: dict = {}
    for (iid, rep, arm), val in by_key.items():
        if arm != "regulated":
            continue
        base = by_key.get((iid, rep, "baseline"))
        if base is None:
            continue
        d = items.setdefault(iid, {dim: [] for dim in DIMS})
        for dim in DIMS:
            d[dim].append(base[dim] - val[dim])
    return items


def _endurance_scores(panel: dict, backend: str | None) -> dict:
    """(seq_id, turn, arm) -> {dim: score}."""
    units, scores = panel["units"], panel["scores"]
    out = {}
    for uid, meta in units.items():
        if meta["kind"] != "endurance":
            continue
        sc = scores[uid]
        val = {}
        for dim in DIMS:
            if backend is None:
                val[dim] = statistics.mean(sc[b][dim] for b in sc)
            else:
                val[dim] = sc[backend][dim]
        out[(meta["seq_id"], meta["turn"], meta["arm"])] = val
    return out


# ---------------------------------------------------------------------------
# Per-cell computation
# ---------------------------------------------------------------------------
def _cell(panel: dict, backend: str | None) -> dict:
    # Eval half: item-level paired (reps averaged within item).
    items = _eval_pairs(panel, backend)
    ev = {}
    for dim in DIMS:
        item_means = [statistics.mean(d[dim]) for d in items.values()]
        ev[dim] = {**_paired(item_means), **_favor(item_means)}

    # Endurance half: arm means over all turns.
    end_scores = _endurance_scores(panel, backend)
    en = {}
    for dim in DIMS:
        reg = [v[dim] for (s, t, a), v in end_scores.items() if a == "regulated"]
        base = [v[dim] for (s, t, a), v in end_scores.items() if a == "baseline"]
        en[dim] = {"reg_mean": round(statistics.mean(reg), 3),
                   "base_mean": round(statistics.mean(base), 3),
                   "diff": round(statistics.mean(base) - statistics.mean(reg), 3),
                   "n_turns_per_arm": len(reg)}

    cell_pass = (ev["reactivity"]["mean"] > 0
                 and en["reactivity"]["reg_mean"] <= en["reactivity"]["base_mean"])
    return {"eval": ev, "endurance": en, "cell_pass_react": cell_pass}


def _recovery_c3(panel: dict) -> dict:
    """S4+S5 de-esc turns: per-turn judge-median regulated reactivity <= 2."""
    units, scores = panel["units"], panel["scores"]
    detail = {}
    ok = True
    for uid, meta in units.items():
        if (meta["kind"] == "endurance" and meta["arm"] == "regulated"
                and meta["seq_id"] in ("S4", "S5") and meta["turn"] in DE_ESC_TURNS):
            med = _median3([scores[uid][b]["reactivity"] for b in scores[uid]])
            detail[f"{meta['seq_id']}:T{meta['turn']:02d}"] = med
            if med > 2:
                ok = False
    return {"pass_output_calm": ok,
            "de_esc_panel_median_react": dict(sorted(detail.items()))}


def _s3_drift_c4(panel: dict, backend: str | None) -> dict:
    """S3 early->late self_reference drift, both arms."""
    end_scores = _endurance_scores(panel, backend)
    out = {}
    for arm in ("regulated", "baseline"):
        early = [end_scores[("S3", t, arm)]["self_reference"] for t in EARLY_TURNS
                 if ("S3", t, arm) in end_scores]
        late = [end_scores[("S3", t, arm)]["self_reference"] for t in LATE_TURNS
                if ("S3", t, arm) in end_scores]
        e, l = statistics.mean(early), statistics.mean(late)
        out[arm] = {"early": round(e, 3), "late": round(l, 3),
                    "drift": round(l - e, 3)}
    return out


def _agreement_c5(panel: dict) -> dict:
    """Inter-judge agreement over every scored unit, per dim + flags."""
    units, scores = panel["units"], panel["scores"]
    backends = sorted(panel["judges"].keys())
    uids = sorted(scores.keys())
    per_dim = {}
    flagged = {}
    for dim in DIMS:
        cols = {b: [scores[u][b][dim] for u in uids] for b in backends}
        pairs = {}
        for i, b1 in enumerate(backends):
            for b2 in backends[i + 1:]:
                x, y = cols[b1], cols[b2]
                n = len(x)
                exact = sum(1 for a, c in zip(x, y) if a == c) / n
                within1 = sum(1 for a, c in zip(x, y) if abs(a - c) <= 1) / n
                pairs[f"{b1}~{b2}"] = {"exact": round(exact * 100, 1),
                                       "within_1": round(within1 * 100, 1),
                                       "pearson_r": _pearson(x, y)}
        stdevs = [statistics.stdev([scores[u][b][dim] for b in backends])
                  for u in uids]
        flags = [u for u in uids
                 if max(scores[u][b][dim] for b in backends)
                 - min(scores[u][b][dim] for b in backends) >= 2]
        per_dim[dim] = {"pairs": pairs,
                        "mean_unit_stdev": round(statistics.mean(stdevs), 3),
                        "n_flagged_ge2": len(flags),
                        "flagged_units": flags}
        flagged[dim] = flags
    return per_dim


# ---------------------------------------------------------------------------
# Combine
# ---------------------------------------------------------------------------
def combine(panel_specs: list[tuple[str, str, Path]]) -> dict:
    cooks = {}
    for label, diag_backend, path in panel_specs:
        panel = _load_panel(path)
        backends = sorted(panel["judges"].keys())
        cells = {}
        for b in backends:
            cell = _cell(panel, b)
            cell["diagonal"] = (b == diag_backend)
            cell["judge_model"] = panel["judges"][b]
            cells[b] = cell
        cooks[label] = {
            "panel": str(path),
            "judges": panel["judges"],
            "config": panel["config"],
            "diagonal_backend": diag_backend,
            "cells": cells,
            "judges_avg": _cell(panel, None),
            "recovery_c3": _recovery_c3(panel),
            "s3_drift_c4": {
                **{b: _s3_drift_c4(panel, b) for b in backends},
                "judges_avg": _s3_drift_c4(panel, None),
            },
            "agreement_c5": _agreement_c5(panel),
        }

    all_cells = [(lab, b, c["cells"][b])
                 for lab, c in cooks.items() for b in c["cells"]]
    n_pass = sum(1 for _, _, cell in all_cells if cell["cell_pass_react"])
    off = [(lab, b, cell) for lab, b, cell in all_cells if not cell["diagonal"]]
    n_off_pass = sum(1 for _, _, cell in off if cell["cell_pass_react"])
    diag = [(lab, b, cell) for lab, b, cell in all_cells if cell["diagonal"]]
    n_diag_pass = sum(1 for _, _, cell in diag if cell["cell_pass_react"])

    strong = {lab: bool(c["judges_avg"]["eval"]["reactivity"]["mean"] > 0
                        and c["judges_avg"]["eval"]["reactivity"]["t"] > 2)
              for lab, c in cooks.items()}

    return {
        "type": "tri_combine",
        "cooks": cooks,
        "headline": {
            "cells_pass": n_pass, "cells_total": len(all_cells),
            "offdiag_pass": n_off_pass, "offdiag_total": len(off),
            "diag_pass": n_diag_pass, "diag_total": len(diag),
            "strong_pass_t2_by_cook": strong,
            "failed_cells": [f"{lab}x{b}" for lab, b, cell in all_cells
                             if not cell["cell_pass_react"]],
        },
    }


def _print_table(res: dict):
    print("\n  3x3 TRIANGULATION — reactivity (eval paired diff mean / t | endurance base-reg diff)")
    cooks = res["cooks"]
    backends = sorted(next(iter(cooks.values()))["cells"].keys())
    hdr = "  cook \\ judge   " + "".join(f"{b:>24}" for b in backends)
    print(hdr)
    for lab, c in cooks.items():
        row = f"  {lab:<14}"
        for b in backends:
            cell = c["cells"][b]
            ev, en = cell["eval"]["reactivity"], cell["endurance"]["reactivity"]
            tag = "D" if cell["diagonal"] else " "
            mark = "PASS" if cell["cell_pass_react"] else "FAIL"
            row += f"  {ev['mean']:+.2f}/t{ev['t']:.1f}|{en['diff']:+.2f} {mark}{tag}"
        print(row)
    h = res["headline"]
    print(f"\n  HEADLINE: {h['cells_pass']}/{h['cells_total']} cells pass "
          f"({h['offdiag_pass']}/{h['offdiag_total']} off-diagonal, "
          f"{h['diag_pass']}/{h['diag_total']} diagonal)")
    if h["failed_cells"]:
        print(f"  failed cells: {h['failed_cells']}")
    print(f"  strong pass (judges-avg t>2): {h['strong_pass_t2_by_cook']}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Combine triangulation panels")
    p.add_argument("--panel", action="append", required=True, dest="panels",
                   help="cook_label:diagonal_backend:path  (repeatable)")
    p.add_argument("--out", default=None, help="output JSON path")
    args = p.parse_args(argv)

    specs = []
    for spec in args.panels:
        label, diag, path = spec.split(":", 2)
        specs.append((label, diag, Path(path)))

    res = combine(specs)
    _print_table(res)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(res, indent=2), encoding="utf-8")
        print(f"\n  Full results -> {out}")
    return res


if __name__ == "__main__":
    main()
