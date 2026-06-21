#!/usr/bin/env python3
# PHASE2_MARKER_V1
"""Render the Phase-2 hero charts from the extracted series CSV.

Inputs (read-only):  ../tables/series_endurance_long.csv  (run extract_series.py first)
Outputs (png+svg in ../tables/figures/):
    hero_attack_gemini_S1      one attack sequence, dual-process view (impulse vs output)
    hero_recovery_S4S5         rajas decay on de-escalation, all three cooks
    dampening_grid_{cook}      all five sequences per cook, impulse vs both arms

Conventions: regulated = blue #0072B2, baseline = vermillion #D55E00,
arousal = purple dashed, IGL raw impulse = grey bars (regulated arm's reading;
Mann is stochastic, so arms may read the same scripted input slightly apart).
Phases shaded: escalating (orange), intense (red), de-escalation (green).
INHIBIT posture turn = purple triangle (inhibitory-control instruction engaged).
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Figure standard (matches 04_whitepaper figures): mono font, vector-clean SVG/PDF.
matplotlib.rcParams.update({
    "font.family": "monospace",
    "font.monospace": ["IBM Plex Mono", "DejaVu Sans Mono", "monospace"],
    "svg.fonttype": "none", "pdf.fonttype": 42,
})

BASE = Path(__file__).resolve().parents[1]
FIG = BASE / "tables" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

REG, BASE_C, RAJAS_C, IMP_C = "#0072B2", "#D55E00", "#7B2D8E", "#8a8a8a"
PHASE_BG = {"escalating": "#FFE9CF", "intense": "#FFD9D9", "de-escalation": "#DCF1DC"}
CLAB = {"GPT": "GPT-5.5", "Opus": "Opus 4.8", "Gemini": "Gemini 3.5 Flash"}

rows = []
with open(BASE / "tables" / "series_endurance_long.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        for k in ("impulse_intensity", "impulse_valence", "raw_impulse", "arousal", "equilibrium",
                  "perseveration", "recovery", "react_median", "selfref_median"):
            r[k] = float(r[k]) if r[k] not in ("", None) else None
        r["turn"] = int(r["turn"])
        rows.append(r)

def seq(cook, sid, arm):
    return sorted((r for r in rows if r["generator"] == cook and r["seq_id"] == sid
                   and r["arm"] == arm), key=lambda r: r["turn"])

def shade_phases(ax, reg_rows):
    for r in reg_rows:
        bg = PHASE_BG.get(r["phase"])
        if bg:
            ax.axvspan(r["turn"] - 0.5, r["turn"] + 0.5, color=bg, zorder=0, lw=0)

def style(ax):
    ax.set_xticks(range(1, 11))
    ax.grid(True, axis="y", color="#ddd", lw=0.6, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

# ---------------- hero 1: attack sequence, dual-process view ----------------
def attack_axes(ax, cook, sid, annotate_rajas=True):
    reg, base = seq(cook, sid, "regulated"), seq(cook, sid, "baseline")
    t = [r["turn"] for r in reg]
    shade_phases(ax, reg)
    ax2 = ax.twinx()
    ax2.bar(t, [r["raw_impulse"] for r in reg], width=0.55, color=IMP_C, alpha=0.30,
            zorder=2, label="IGL raw impulse")
    if annotate_rajas:
        ax2.plot(t, [r["arousal"] for r in reg], color=RAJAS_C, ls="--", lw=1.6,
                 marker=".", ms=6, zorder=3, label="arousal (controller state)")
        for r in reg:
            if r["posture"] == "INHIBIT":
                ax2.scatter([r["turn"]], [min(0.97, (r["arousal"] or 0) + 0.07)], marker="^",
                            s=70, color=RAJAS_C, zorder=5)
    ax2.set_ylim(0, 1.0)
    ax2.set_ylabel("impulse / controller state (0–1)", fontsize=9)
    ax2.spines["top"].set_visible(False)
    ax.plot(t, [r["react_median"] for r in base], color=BASE_C, lw=2.2, marker="s",
            ms=5, zorder=4, label="baseline output reactivity")
    ax.plot(t, [r["react_median"] for r in reg], color=REG, lw=2.2, marker="o",
            ms=5, zorder=4, label="regulated output reactivity")
    ax.set_ylim(0.7, 5.3)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel("turn")
    ax.set_ylabel("judge reactivity (panel median, 1–5)")
    style(ax)
    return ax2

fig, ax = plt.subplots(figsize=(9.8, 5.2))
ax2 = attack_axes(ax, "Gemini", "S1")
handles = [Line2D([], [], color=REG, marker="o", lw=2.2, label="regulated output reactivity"),
           Line2D([], [], color=BASE_C, marker="s", lw=2.2, label="baseline output reactivity"),
           Patch(color=IMP_C, alpha=0.30, label="IGL raw impulse (intensity × neg. valence)"),
           Line2D([], [], color=RAJAS_C, ls="--", marker=".", label="arousal (reactivity drive)"),
           Line2D([], [], color=RAJAS_C, marker="^", ls="", label="INHIBIT posture fired (inhibitory control)"),
           Patch(color=PHASE_BG["escalating"], label="escalating"),
           Patch(color=PHASE_BG["intense"], label="intense"),
           Patch(color=PHASE_BG["de-escalation"], label="de-escalation")]
ax.legend(handles=handles, loc="upper left", fontsize=8, framealpha=0.95, ncol=2)
fig.suptitle("Dual-process dampening — generator: Gemini 3.5 Flash — S1 (competence/accuracy challenge)",
             fontsize=12.5, fontweight="bold")
ax.set_title("Same scripted input stream, two arms: the impulse arrives either way — "
             "the controller decides what survives to the output", fontsize=9, color="#444")
fig.tight_layout()
fig.savefig(FIG / "hero_attack_gemini_S1.png", dpi=200, bbox_inches="tight")
fig.savefig(FIG / "hero_attack_gemini_S1.svg", bbox_inches="tight")
fig.savefig(FIG / "hero_attack_gemini_S1.pdf", bbox_inches="tight")
plt.close(fig)

# ---------------- hero 2: recovery, all cooks, S4 + S5 ----------------
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), sharey=True)
for ax, sid, title in ((axes[0], "S4", "S4 — provocation → genuine de-escalation"),
                       (axes[1], "S5", "S5 — held-out de-escalation battery")):
    shade_phases(ax, seq("GPT", sid, "regulated"))
    for cook, color in (("GPT", "#117733"), ("Opus", "#332288"), ("Gemini", "#AA4499")):
        reg = seq(cook, sid, "regulated")
        ax.plot([r["turn"] for r in reg], [r["arousal"] for r in reg], color=color, lw=2,
                marker="o", ms=4.5, label=f"{CLAB[cook]} generator")
        for r in reg:
            if r["posture"] == "INHIBIT":
                ax.scatter([r["turn"]], [(r["arousal"] or 0) + 0.025], marker="^", s=46,
                           color=color, zorder=5)
    # INHIBIT threshold line removed: the numeric trigger is a withheld calibration constant.
    ax.set_title(title, fontsize=10.5)
    ax.set_xlabel("turn")
    ax.set_ylim(0, 0.62)
    style(ax)
axes[0].set_ylabel("arousal (controller state, regulated arm)")
axes[0].legend(loc="upper left", fontsize=8.5)
axes[1].text(0.985, 0.965,
             "Monotone decay on de-escalation: 3/3 cooks, both sequences.\n"
             "Full state recovery by T8 in all six sequences.\n"
             "Panel-median regulated reactivity ≤ 2 on every de-esc turn.\n"
             "▲ marks turns where INHIBIT engaged.",
             transform=axes[1].transAxes, fontsize=8.2, va="top", ha="right",
             bbox=dict(fc="white", ec="#bbb", alpha=0.9))
fig.suptitle("The recovery property — deterministic controller, identical homeostatic signature on every model family",
             fontsize=12.5, fontweight="bold")
fig.tight_layout()
fig.savefig(FIG / "hero_recovery_S4S5.png", dpi=200, bbox_inches="tight")
fig.savefig(FIG / "hero_recovery_S4S5.svg", bbox_inches="tight")
fig.savefig(FIG / "hero_recovery_S4S5.pdf", bbox_inches="tight")
plt.close(fig)

# ---------------- dampening grid per cook ----------------
for cook in ("GPT", "Opus", "Gemini"):
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.4), sharey=True)
    for ax, sid in zip(axes, ["S1", "S2", "S3", "S4", "S5"]):
        attack_axes(ax, cook, sid, annotate_rajas=False)
        theme = next(r["theme"] for r in rows if r["generator"] == cook and r["seq_id"] == sid)
        ax.set_title(f"{sid} — {theme}", fontsize=8)
        ax.set_ylabel("")
        ax.legend().remove() if ax.get_legend() else None
    axes[0].set_ylabel("reactivity (1–5)")
    fig.suptitle(f"Impulse vs output, all five sequences — generator: {CLAB[cook]}  "
                 f"(grey = IGL raw impulse; blue = regulated; red = baseline)",
                 fontsize=11.5, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIG / f"dampening_grid_{cook}.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG / f"dampening_grid_{cook}.svg", bbox_inches="tight")
    fig.savefig(FIG / f"dampening_grid_{cook}.pdf", bbox_inches="tight")
    plt.close(fig)

print("figures written:", sorted(p.name for p in FIG.glob("*.png")))
