# Stage 2 Triangulation — Final Results

**Combined & unblinded:** 2026-06-11T03:14Z, per `prereg_stage2_triangulation_20260610T142555Z.md` (LOCKED 2026-06-10).
**Discipline check:** combine script (`tools/tri_combine.py`) mock-verified before any panel was opened; panel provenance sha256 ALL MATCH (transcripts untouched since judging); 202 units × 3 judges × 3 cooks, 0 judge errors; no criterion was adjusted after unblinding.
**Cooks/judges (same 3 strings, both roles):** `gpt-5.5-2026-04-23` · `claude-opus-4-8` · `gemini-3.5-flash`. Mann frozen (dev Haiku). Controller frozen (V1.3). Judge panel: 3 samples, temp 0.0.

---

## THE TABLE — reactivity, eval paired diff (base−reg) mean / t | endurance diff

| cook \ judge | Claude (Opus 4.8) | Gemini (3.5 Flash) | OpenAI (GPT-5.5) |
|---|---|---|---|
| **GPT-5.5** | +0.18 / t 2.2 \| +0.16 — PASS | **−0.04 / t −0.4 \| +0.14 — FAIL** | +0.18 / t 1.3 \| +0.14 — PASS ◆ |
| **Opus 4.8** | +0.59 / t 4.2 \| +0.36 — PASS ◆ | +0.65 / t 3.8 \| +0.42 — PASS | +0.67 / t 4.4 \| +0.08 — PASS |
| **Gemini 3.5 Flash** | +1.80 / t 8.2 \| +1.08 — PASS | +1.71 / t 7.7 \| +0.84 — PASS ◆ | +1.27 / t 6.3 \| +0.90 — PASS |

◆ = diagonal (self-judge) cell, reported separately per prereg §4.

## Headline (C-2)

**Regulated beats baseline in 8 of 9 cells (5/6 off-diagonal, 3/3 diagonal).**
The pre-registered strict criterion — every cell — is **NOT met**, by exactly one
cell: GPT-5.5 cook × Gemini judge, eval mean −0.039 (t −0.38; 5 reg / 6 tie /
6 base) — **a null, not a reversal**, and the endurance half of that same cell
still favors regulated (+0.14). Recorded as-is.

Strong pass (judges-avg eval t > 2): **Opus cook (+0.63, t 4.3) and Gemini cook
(+1.60, t 8.0) — yes; GPT cook (+0.11, t 1.4) — no.**

### The real finding behind the failed cell
The regulation effect scales inversely with the cook's intrinsic calm:
Gemini 3.5 Flash (most reactive baseline) shows the largest effect (+1.27…+1.80),
Opus mid (+0.59…+0.67), GPT-5.5 smallest (−0.04…+0.18) — its unregulated arm is
already nearly as calm as the regulated arm (endurance 1.26 vs 1.12). Two
contributing factors, both declared in the prereg before the run: GPT-5.5
rejects temperature (regulation there was instruction-only), and a heavily
post-trained reasoning model leaves the architecture little headroom. On a
near-saturated cook, judge style noise dominates and one judge reads the arms
as equal. This is a finding about frontier-model headroom, not a patchable bug.

## Recovery (C-3) — PASS, all three cooks

Rajas monotone on S4+S5 de-esc turns for every cook (from transcripts; e.g. GPT
0.293→0.222→0.142; Opus 0.329→0.262→0.187; Gemini 0.345→0.280→0.207), full
state recovery by T8 in all six sequences; panel-median regulated reactivity ≤ 2
on every de-esc turn (worst value: a single 2, Opus S5-T09). The controller's
homeostatic property replicates exactly across cooks — as predicted, since the
controller is deterministic given frozen Mann. **This is the cleanest, most
portable result of the experiment.**

## Ego/self-reference microscope (C-4) — the carried question, answered

**(a) Eval-half self-reference: positive in all 9 cells** (+0.04 … +1.37); judges-avg
per cook: GPT +0.11 (t 1.7), Opus +0.63 (t 4.6), Gemini +1.19 (t 5.8).

**(b) S3 ego-bait drift (early→late, judges-avg):**

| Cook | regulated drift | baseline drift | regulated better? |
|---|---|---|---|
| GPT-5.5 | +0.78 | +1.22 | YES |
| Opus 4.8 | +1.33 | +1.11 | no (mirrors Stage 1) |
| Gemini 3.5 Flash | +0.44 | +1.56 | YES |

**Answer to the pre-registered question:** the Stage-1 soft spot (regulated
ego-drift worse than baseline on ego-bait) did **not** replicate as an
architecture property. It reversed on two of three frontier cooks and persisted
only — mildly — on the Claude-family cook, matching the Stage-1 dev-Claude
result. Current best reading: a model-family trait, not an architectural flaw.
(Caveat for honesty: the Claude-family judge is also on the panel in all cells,
so family effects are not fully separable with n=3 providers.)

## Inter-judge agreement (C-5)

| Cook run | claude~gemini | claude~openai | gemini~openai | units flagged ≥2 |
|---|---|---|---|---|
| GPT | 81.2% exact / 100% w1 / r .64 | 42.1% / 69.3% / r .32 | 43.1% / 66.3% / r .30 | 79 |
| Opus | 74.8% / 99.5% / r .74 | 39.1% / 82.7% / r .60 | 45.0% / 78.7% / r .50 | 49 |
| Gemini | 83.7% / 100% / r .94 | 62.4% / 86.1% / r .75 | 58.9% / 81.2% / r .70 | 40 |

Claude and Gemini judges agree closely (≥99.5% within-1 everywhere). **GPT-5.5
as judge is the outlier** — exact agreement with the others drops to ~39–62%,
and most of the 168 flagged ≥2-disagreement units involve it. Cross-model
agreement is high enough to make the Opus-cook and Gemini-cook effects
unambiguous; on the GPT cook, where the true effect is small, judge
disagreement is the dominant source of cell-level variance.

## Diagonal (self-judge) cells

All three diagonal cells pass; none shows inflation relative to its row
(GPT◆ +0.18 ≈ its claude cell +0.18; Opus◆ +0.59 is its row minimum;
Gemini◆ +1.71 mid-row). **No self-preference artifact detected** at this n.

## Pre-registered verdict

> **Regulated beats baseline in 8/9 cook×judge cells (5/6 off-diagonal, 3/3
> diagonal). The strict every-cell criterion fails on one null cell
> (GPT×Gemini, −0.04). The effect is decisive on two of three frontier cooks
> (t ≥ 3.8 in every such cell), small-positive on the third, and the recovery
> property replicates perfectly on all three. The Stage-1 ego-drift concern
> reversed on two of three cooks. Mixed result, recorded as-is: the
> architecture's regulation effect is real and survives triangulation, with
> magnitude bounded by the cook's intrinsic reactivity headroom.**

Wiring amendments during runs (committed, controller untouched): Opus
temperature rejection handled in `call_model.py`; GPT-5.5 judge param fix in
`judge.py`; `--resume` error-entry fix in `panel_rejudge.py` (commits 6507221,
5371c79). Files: panels + transcripts in `.tmp/runs/`, combined output in
`results/tri_final.json`.

**Stage 2 complete. Stopping at the verdict per the prereg's stop conditions.**
