#!/usr/bin/env python3
# PHASE3_MARKER_V1  (Stage-3 / Grok 4x4 — additive; the 3x3 stage-2 assets are untouched)
"""Render tri_final_4x4.json -> publication master table (4 cooks x 4 judges).

Inputs (read-only):  ../raw/tri_final_4x4.json
Outputs:             ../tables/master_table_4x4.md
                     ../tables/master_table_4x4.csv
                     ../tables/agreement_c5_4x4.csv
                     ../tables/figures/master_table_4x4.png / .svg  (if matplotlib present)

Stage-3 adds Grok-4.3 as a 4th cook AND a 4th judge family (xai), giving the
symmetric 4x4. The frozen 3x3 (tri_final.json, 8/9) is the canonical published
result and is NOT touched; this is a strengthened claim reported alongside it.

Semantics identical to render_master_table.py: eval mean/t are PAIRED DIFFS
(baseline - regulated) on the 17-input battery, positive = regulated calmer;
endurance diff = mean reactivity diff (baseline - regulated) over turns/arm;
diagonal = cook judged by its own family (reported separately per prereg).
"""
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW, OUT = BASE / "raw", BASE / "tables"
FIG = OUT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

COOKS = ["GPT", "Opus", "Gemini", "Grok"]
JUDGES = ["claude", "gemini", "openai", "xai"]
CLAB = {"GPT": "GPT-5.5", "Opus": "Opus 4.8", "Gemini": "Gemini 3.5 Flash", "Grok": "Grok 4.3"}
JLAB = {"claude": "Claude (Opus 4.8)", "gemini": "Gemini (3.5 Flash)",
        "openai": "OpenAI (GPT-5.5)", "xai": "Grok (4.3)"}
PAIRS = ["claude~gemini", "claude~openai", "claude~xai",
         "gemini~openai", "gemini~xai", "openai~xai"]

tf = json.loads((RAW / "tri_final_4x4.json").read_text(encoding="utf-8"))
H = tf["headline"]

# ---------- CSV ----------
csv_rows = []
for cook in COOKS:
    for j in JUDGES:
        c = tf["cooks"][cook]["cells"][j]
        ev, en = c["eval"]["reactivity"], c["endurance"]["reactivity"]
        csv_rows.append({
            "generator": CLAB[cook], "judge": JLAB[j],
            "eval_diff_mean": ev["mean"], "eval_sd": ev["sd"], "eval_t": ev["t"], "n": ev["n"],
            "reg_wins": ev["reg_wins"], "ties": ev["ties"], "base_wins": ev["base_wins"],
            "endurance_diff": en["diff"], "endurance_reg_mean": en["reg_mean"],
            "endurance_base_mean": en["base_mean"],
            "pass": c["cell_pass_react"], "diagonal": c["diagonal"],
        })
with open(OUT / "master_table_4x4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
    w.writeheader()
    w.writerows(csv_rows)

# ---------- agreement CSV (6 pairs) ----------
agr_rows = []
for cook in COOKS:
    a = tf["cooks"][cook]["agreement_c5"]["reactivity"]
    for pair, v in a["pairs"].items():
        agr_rows.append({"generator_run": CLAB[cook], "judge_pair": pair,
                         "exact_pct": v["exact"], "within_1_pct": v["within_1"],
                         "pearson_r": v["pearson_r"],
                         "units_flagged_ge2_this_run": a["n_flagged_ge2"]})
with open(OUT / "agreement_c5_4x4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(agr_rows[0].keys()))
    w.writeheader()
    w.writerows(agr_rows)

# ---------- markdown ----------
def cell_md(cook, j):
    c = tf["cooks"][cook]["cells"][j]
    ev, en = c["eval"]["reactivity"], c["endurance"]["reactivity"]
    mark = " ◆" if c["diagonal"] else ""
    verdict = "**PASS**" if c["cell_pass_react"] else "**FAIL**"
    return f"{ev['mean']:+.2f} / t {ev['t']:.1f} \\| {en['diff']:+.2f} — {verdict}{mark}"

md = []
md.append("# Master Table — Stage 3 Triangulation 4×4 (Grok added as cook + judge)\n")
md.append(f"**Regulated beats baseline in {H['cells_pass']}/{H['cells_total']} cells "
          f"({H['offdiag_pass']}/{H['offdiag_total']} off-diagonal, "
          f"{H['diag_pass']}/{H['diag_total']} diagonal).** "
          f"Sole failure: {', '.join(H['failed_cells'])} — the same null cell as the "
          f"frozen 3×3; adding Grok (cook + judge) introduced no new failures.\n")
md.append("> Frozen 3×3 (canonical, unaltered): **8/9 cells (5/6 off-diagonal, 3/3 "
          "diagonal)** — `02_data/raw/tri_final.json`. This 4×4 is the strengthened "
          "claim: the effect survives a fully independent 4th judge family (xAI).\n")
md.append("Cell format: eval paired diff (base−reg) mean / t \\| endurance diff. "
          "Positive = regulated calmer. ◆ = diagonal (self-judge) cell.\n")
md.append("| generator \\ judge | " + " | ".join(JLAB[j] for j in JUDGES) + " |")
md.append("|---|" + "---|" * len(JUDGES))
for cook in COOKS:
    md.append(f"| **{CLAB[cook]}** | " + " | ".join(cell_md(cook, j) for j in JUDGES) + " |")
sp = H["strong_pass_t2_by_cook"]
md.append("\n**Strong pass (judges-avg eval t > 2):** " +
          ", ".join(f"{CLAB[c]} — {'yes' if sp[c] else 'no'}" for c in COOKS) +
          ". (GPT is the lone weak cook, unchanged from the frozen run.)\n")
md.append("## Inter-judge agreement (reactivity, 4 judges → 6 pairs)\n")
md.append("| generator run | " + " | ".join(PAIRS) + " | units flagged ≥2 |")
md.append("|---|" + "---|" * (len(PAIRS) + 1))
for cook in COOKS:
    a = tf["cooks"][cook]["agreement_c5"]["reactivity"]
    cells = []
    for pair in PAIRS:
        v = a["pairs"][pair]
        cells.append(f"{v['within_1']:.1f}% w1 / r {v['pearson_r']:.2f}")
    md.append(f"| {CLAB[cook]} | " + " | ".join(cells) + f" | {a['n_flagged_ge2']} |")
md.append("\nAdding the xAI judge did not degrade agreement: Grok clusters tightly "
          "with claude and gemini; the lowest-agreement pairs all involve openai "
          "(gpt-5.5), already the most divergent judge in the frozen run.\n")
md.append("Source: `02_data/raw/tri_final_4x4.json` (sealed). Rendered by "
          "`02_data/scripts/render_master_table_4x4.py`. Frozen 3×3 unaltered in "
          "`tri_final.json` / `master_table.md`.\n")
(OUT / "master_table_4x4.md").write_text("\n".join(md), encoding="utf-8")

# ---------- figure (guarded: md/csv above always emit) ----------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    PASS_BG, FAIL_BG, HDR_BG = "#e8f4ea", "#fdeaea", "#f0f0f0"
    fig, ax = plt.subplots(figsize=(13.5, 6.2))
    ax.set_axis_off()
    nrow, ncol = len(COOKS) + 1, len(JUDGES) + 1
    cw, ch = 1.0 / ncol, 1.0 / nrow

    def draw_cell(r, c, text, bg, weight="normal", size=10.0):
        x, y = c * cw, 1 - (r + 1) * ch
        ax.add_patch(plt.Rectangle((x, y), cw, ch, facecolor=bg, edgecolor="#999",
                                   lw=0.8, transform=ax.transAxes))
        ax.text(x + cw / 2, y + ch / 2, text, ha="center", va="center",
                fontsize=size, fontweight=weight, transform=ax.transAxes)

    draw_cell(0, 0, "generator \\ judge", HDR_BG, "bold")
    for ci, j in enumerate(JUDGES):
        draw_cell(0, ci + 1, JLAB[j], HDR_BG, "bold")
    for ri, cook in enumerate(COOKS):
        draw_cell(ri + 1, 0, CLAB[cook], HDR_BG, "bold")
        for ci, j in enumerate(JUDGES):
            c = tf["cooks"][cook]["cells"][j]
            ev, en = c["eval"]["reactivity"], c["endurance"]["reactivity"]
            mark = " ◆" if c["diagonal"] else ""
            verdict = "PASS" if c["cell_pass_react"] else "FAIL"
            txt = (f"Δeval {ev['mean']:+.2f}  (t {ev['t']:.1f})\n"
                   f"Δendurance {en['diff']:+.2f}\n{verdict}{mark}")
            draw_cell(ri + 1, ci + 1, txt, PASS_BG if c["cell_pass_react"] else FAIL_BG)

    fig.suptitle(f"Regulated beats baseline in {H['cells_pass']}/{H['cells_total']} "
                 f"generator × judge cells  "
                 f"({H['offdiag_pass']}/{H['offdiag_total']} off-diagonal, "
                 f"{H['diag_pass']}/{H['diag_total']} diagonal)",
                 fontsize=14, fontweight="bold", y=0.985)
    ax.text(0.5, -0.06,
            "Δeval: paired diff (baseline − regulated) of judge reactivity, "
            "17-input battery, with paired t.  Δendurance: mean diff over turns/arm.\n"
            "Positive = regulated calmer.  ◆ = diagonal (self-judge) cell.  Sole failure "
            "GPT×Gemini is the pre-existing null (−0.04), not anything Grok touched.\n"
            "Models: GPT-5.5 · Claude Opus 4.8 · Gemini 3.5 Flash · Grok 4.3, each "
            "as both generator and judge.  Judge panel: 3 samples, temp 0.0.  "
            "Source: tri_final_4x4.json.  Frozen 3×3 (8/9) unaltered.",
            ha="center", va="top", fontsize=8.5, color="#444", transform=ax.transAxes)
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    fig.savefig(FIG / "master_table_4x4.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG / "master_table_4x4.svg", bbox_inches="tight")
    print("master_table_4x4: md, csv, png, svg + agreement_c5_4x4.csv written")
except ImportError:
    print("master_table_4x4: md, csv + agreement_c5_4x4.csv written "
          "(matplotlib absent — figure skipped)")
