#!/usr/bin/env python3
"""stats_checks.py — computes, from the SEALED record only, the two statistical
sentences the publishing draft adds in §6.6 (punch list 2.3 / 2.4):

  A. Multiplicity: Bonferroni correction across the 16 per-cell reactivity tests
     (threshold p = .05/16), from the sealed per-cell t values (df = 16).
  B. Non-parametric check: paired Wilcoxon signed-rank per cell on per-item
     differences RECONSTRUCTED from the sealed judge panels, hard-validated
     against the sealed cell summaries (mean, t, win/tie counts) before use.
  C. The 16th self-reference cell (punch list 2.6), named from the sealed record.

Read-only over E:\\AMT\\02_data. Exit 1 if any validation fails.
The paper quotes THIS script's output; never hand-derive these numbers.
"""
import json, math, sys
from pathlib import Path
from statistics import median, mean
from scipy import stats

RAW = Path(__file__).resolve().parents[2] / "02_data" / "raw"
DF = 16
ALPHA = 0.05
M = 16  # tests
BONF = ALPHA / M

COOKS = {"GPT": "panel_tri_cookGPT_4judge.json",
         "Opus": "panel_tri_cookOpus_4judge.json",
         "Gemini": "panel_tri_cookGemini_4judge.json",
         "Grok": "panel_tri_cookGrok.json"}
JUDGES = ["claude", "gemini", "openai", "xai"]
JLAB = {"claude": "Opus", "gemini": "Gemini", "openai": "GPT", "xai": "Grok"}

sealed = json.load(open(RAW / "tri_final_4x4.json"))
fail = []

def cellname(ck, jk):
    return f"{ck}×{JLAB[jk]}"

# ---------- A. Bonferroni over the sealed t values ----------
print("== A. multiplicity (Bonferroni .05/16 = %.6f, df=16) ==" % BONF)
tcrit = stats.t.ppf(1 - BONF / 2, DF)
print(f"two-sided critical |t| at Bonferroni threshold: {tcrit:.3f}")
rows = []
for ck, cook in sealed["cooks"].items():
    for jk, cell in cook["cells"].items():
        t = cell["eval"]["reactivity"]["t"]
        p = 2 * stats.t.sf(abs(t), DF)
        rows.append((cellname(ck, jk), t, p, p < ALPHA, p < BONF))
surv = [r for r in rows if r[4]]
nom = [r for r in rows if r[3]]
lost = [r for r in rows if r[3] and not r[4]]
print(f"nominal p<.05: {len(nom)}/16   surviving Bonferroni: {len(surv)}/16")
print("cells significant at .05 but NOT under Bonferroni (the correction-marginal cells):")
for name, t, p, *_ in sorted(lost, key=lambda r: r[2]):
    print(f"  {name:14s} t {t:+.2f}  p {p:.4f}")
print("all 16 (sorted by p):")
for name, t, p, s05, sB in sorted(rows, key=lambda r: r[2]):
    print(f"  {name:14s} t {t:+.2f}  p {p:.6f}  p<.05:{'Y' if s05 else 'n'}  bonf:{'Y' if sB else 'n'}")

# ---------- B. Wilcoxon on reconstructed per-item differences ----------
print("\n== B. paired Wilcoxon signed-rank per cell (reconstructed from sealed panels) ==")
def item_diffs(panel, judge):
    """17 per-item paired differences (baseline - regulated) for one judge.
    Unit score = the panel median already recorded per unit; item score per arm
    = mean over the 3 reps; validated against the sealed summaries below."""
    per = {}
    for uid, info in panel["units"].items():
        if info["kind"] != "eval":
            continue
        sc = panel["scores"][uid][judge]["reactivity"]
        per.setdefault(info["item_id"], {}).setdefault(info["arm"], []).append(sc)
    diffs = []
    for item, arms in sorted(per.items()):
        assert len(arms["regulated"]) == 3 and len(arms["baseline"]) == 3, item
        diffs.append(mean(arms["baseline"]) - mean(arms["regulated"]))
    assert len(diffs) == 17, len(diffs)
    return diffs

agree = True
for ck, fname in COOKS.items():
    panel = json.load(open(RAW / fname))
    for jk in JUDGES:
        d = item_diffs(panel, jk)
        ev = sealed["cooks"][ck]["cells"][jk]["eval"]["reactivity"]
        m_, sd_ = mean(d), (sum((x - mean(d)) ** 2 for x in d) / 16) ** 0.5
        t_ = m_ / (sd_ / math.sqrt(17)) if sd_ > 0 else 0.0
        wins = sum(1 for x in d if x > 1e-12); ties = sum(1 for x in d if abs(x) <= 1e-12)
        ok = (abs(m_ - ev["mean"]) < 5e-4 and abs(t_ - ev["t"]) < 0.06
              and wins == ev["reg_wins"] and ties == ev["ties"])
        if not ok:
            fail.append(f"validation {cellname(ck,jk)}: recon mean {m_:+.4f} t {t_:+.2f} "
                        f"w/t {wins}/{ties} vs sealed {ev['mean']:+.4f} t {ev['t']:+.2f} "
                        f"w/t {ev['reg_wins']}/{ev['ties']}")
            continue
        nz = [x for x in d if abs(x) > 1e-12]
        if nz:
            w = stats.wilcoxon(nz, alternative="two-sided", mode="exact" if len(nz) < 26 else "auto")
            wp = w.pvalue
        else:
            wp = 1.0
        t_sig = abs(ev["t"]) > 2.120
        w_sig = wp < ALPHA
        mark = "AGREE" if t_sig == w_sig else "DISAGREE"
        if t_sig != w_sig:
            agree = False
        print(f"  {cellname(ck,jk):14s} recon-validated | wilcoxon p {wp:.4f} "
              f"({'sig' if w_sig else 'n.s.'}) vs t-test ({'sig' if t_sig else 'n.s.'}) -> {mark}")
print("WILCOXON/T-TEST AGREEMENT ON ALL 16 CELLS:", "YES" if agree and not fail else "NO")

# ---------- C. the 16th self-reference cell ----------
print("\n== C. self-reference: the one cell not favoring regulated ==")
for ck, cook in sealed["cooks"].items():
    for jk, cell in cook["cells"].items():
        sr = cell["eval"]["self_reference"]
        if sr["mean"] <= 0:
            print(f"  {cellname(ck,jk)}: mean {sr['mean']:+.3f}, t {sr['t']:+.2f} "
                  f"(exact tie, not a reversal; on the GPT host)" if sr["mean"] == 0
                  else f"  {cellname(ck,jk)}: mean {sr['mean']:+.3f} (REVERSAL)")

if fail:
    print("\nVALIDATION FAILURES:")
    [print(" ", f) for f in fail]
    sys.exit(1)
print("\nALL VALIDATIONS PASS")
