# Stage 3 — Grok 4×4 Triangulation: Final Results

**Run completed:** 2026-06-20. **Status:** sealed. New artifact only —
`02_data/raw/tri_final_4x4.json` (16 cells). The frozen 3×3
(`02_data/raw/tri_final.json`, `00_handoff/Stage2 triangulation - final results.md`)
is **unaltered** and remains the canonical published result.

**What changed vs Stage 2:** Grok-4.3 added as **both a 4th cook and a 4th judge
family (xai)** → the symmetric **4×4**. Pre-registered in
`docs/prereg/prereg_grok_cook_judge_4x4_20260620T024807Z.md`. Generate-once held:
the three frozen cooks' transcripts were reused; only the new Grok judge column
was added to them (via copy + `panel_rejudge --resume`). IGL frozen at
`claude-haiku-4-5-20251001`; judges at temp 0.0, 3-sample panels.

Models (each as both cook and judge): `gpt-5.5-2026-04-23`, `claude-opus-4-8`,
`gemini-3.5-flash`, `grok-4.3`.

---

## Headline — C-2 reactivity

**Regulated beats baseline in 15/16 generator × judge cells (11/12 off-diagonal,
4/4 diagonal).** The sole failure is **GPT × Gemini** (eval mean −0.04, t −0.4;
endurance still +0.14) — the *identical* cell that fails in the frozen 3×3.
Adding Grok as a 4th cook (row passes 4/4) and a 4th judge (xai column passes
4/4) introduced **no new failures**, and is reported as-is, not patched.

> Frozen 3×3, quoted unchanged: **8/9 cells (5/6 off-diagonal, 3/3 diagonal)**,
> sole failure GPT×Gemini. Canonical in `tri_final.json`.

### 4×4 cells — eval paired diff mean / t  |  endurance base−reg diff  (◆ = diagonal self-judge)

| cook \ judge | Claude (Opus 4.8) | Gemini (3.5 Flash) | OpenAI (GPT-5.5) | Grok (4.3) |
|---|---|---|---|---|
| **GPT-5.5** | +0.18 / t2.2 \| +0.16 ✅ | −0.04 / t−0.4 \| +0.14 ❌ | +0.18 / t1.3 \| +0.14 ✅◆ | +0.08 / t1.0 \| +0.06 ✅ |
| **Opus 4.8** | +0.59 / t4.2 \| +0.36 ✅◆ | +0.65 / t3.8 \| +0.42 ✅ | +0.67 / t4.4 \| +0.08 ✅ | +0.55 / t3.5 \| +0.20 ✅ |
| **Gemini 3.5 Flash** | +1.80 / t8.2 \| +1.08 ✅ | +1.71 / t7.7 \| +0.84 ✅◆ | +1.27 / t6.3 \| +0.90 ✅ | +1.12 / t5.0 \| +0.70 ✅ |
| **Grok 4.3** | +0.53 / t3.7 \| +0.38 ✅ | +0.59 / t4.2 \| +0.26 ✅ | +0.53 / t4.2 \| +0.38 ✅ | +0.23 / t3.0 \| +0.12 ✅◆ |

Positive = regulated calmer. **Strong pass (judges-avg eval t > 2):** Opus ✅,
Gemini ✅, Grok ✅, GPT ✗ — GPT is the lone weak cook, unchanged from the frozen
run. The effect continues to scale with the host's reactivity headroom (Gemini
largest, GPT smallest); Grok sits in the mid-range (judges-avg react +0.47, t4.4).

---

## C-3 — Recovery (S4 + S5 de-escalation, 4-judge panel-median regulated reactivity, criterion ≤ 2)

**All four cooks PASS.** Every de-escalation turn is calm. Max de-esc panel
median: GPT 1.0, Gemini 1.0, Grok 1.0, Opus 2.0 (the single 2 at Opus S5:T09,
unchanged from the frozen run). The deterministic controller's recovery signature
replicates on the Grok cook and under the xai judge column.

---

## C-4 — Self-reference (the microscope question: does the pattern hold with a 4th cook + 4th judge?)

**Yes.** Eval self-reference paired diff (judges-avg, + = regulated less
self-serving): GPT +0.08 (t1.7, weak), Opus +0.59 (t4.4), Gemini +1.16 (t6.0),
Grok +0.43 (t4.4). S3 ego-bait drift (early→late, lower = less drift): baseline
drifts up more than regulated for **Gemini** (+1.33 vs +0.42), **Grok** (+0.58 vs
+0.25) and **GPT** (+0.92 vs +0.67); **Opus** is the exception (reg +1.17 > base
+0.75) — the same single-cook exception seen in the frozen run. Direction holds
for the Grok cook and the xai judge column.

---

## C-5 — Inter-judge agreement (now 4 judges → 6 pairs; reactivity, averaged across cooks)

| pair | within-1 | mean r | | pair | within-1 | mean r |
|---|---|---|---|---|---|---|
| claude~gemini | 99.9% | 0.79 | | claude~xai | 96.9% | 0.60 |
| claude~openai | 83.3% | 0.57 | | gemini~xai | 97.2% | 0.63 |
| gemini~openai | 80.0% | 0.53 | | openai~xai | 72.4% | 0.41 |

**Adding the xAI judge did not degrade agreement.** Grok clusters tightly with
claude (96.9%) and gemini (97.2%). The lowest-agreement pairs all involve openai
(gpt-5.5) — already the most divergent judge in the frozen run; openai~xai
(72.4%) is the new low. Per-cook ≥2-pt-disagreement flags rise with the 4th judge
(more judges → wider spread): GPT 96, Opus 73, Gemini 62, **Grok 30** — the
Grok-cook panel is the *tightest* of all (mean unit stdev 0.230 vs GPT's 0.549).

---

## Two operational notes (no rules bent)

1. **`.env` wiring fix (gitignored, not a protected file):** the xAI key was under
   `X_AI_API`; renamed to `XAI_API_KEY` (the var the code reads; value unchanged)
   and set `EAU_MODEL`/`JUDGE_XAI_MODEL=grok-4.3`,
   `IGL_MODEL=claude-haiku-4-5-20251001`. All four providers verified live before
   spend.
2. **OpenAI judge truncation, self-resolved:** 4 of the Grok-cook openai
   judge-units first errored (gpt-5.5 reasoning exhausted the judge's hard-coded
   300-token budget — a latent headroom gap vs. the prereg's declared 4096). A
   plain `--resume` cleared all 4 at the existing budget, so `judge.py` was never
   edited during the run and the rubric/prompt stayed frozen. Final panels: **0
   errors.** The latent gap has since been fixed in `judge.py` (OpenAI judge now
   uses `OPENAI_REASONING_HEADROOM`, like the gemini/xai judges) for future runs;
   the completed 4×4 panels are unaffected.

---

## Reproducibility

- Sealed inputs in `02_data/raw/`: Grok transcripts
  (`endurance_endurance_tri_cookGrok*.json`, `eval_tri_cookGrok_eval.json`), the
  four 4-judge panels (`panel_tri_cookGrok.json`,
  `panel_tri_cook{GPT,Opus,Gemini}_4judge.json`), and `tri_final_4x4.json`.
- Rendered assets: `02_data/tables/master_table_4x4.{md,csv}`,
  `agreement_c5_4x4.csv`, `figures/master_table_4x4.{png,svg}` — by
  `02_data/scripts/render_master_table_4x4.py`.
- Integrity gate: `02_data/scripts/verify_against_sealed_4x4.py` — **ALL CHECKS
  PASSED** (16 cells, judges-avg, recovery, S3 drift, agreement flags, and
  sha256 provenance of all four 4-judge panels against the sealed transcripts).
- The frozen 3×3 gate `verify_against_sealed.py` is unchanged and still passes.

## Bottom line

The regulated-vs-baseline effect survives a fully independent 4th judge family
(xAI) and a 4th cook (Grok): **15/16 cells (11/12 off-diagonal)**, with the one
null cell being the pre-existing GPT×Gemini — not anything Grok touched. The
claim is strengthened, not stretched; the frozen 8/9 stands as the canonical
record.
