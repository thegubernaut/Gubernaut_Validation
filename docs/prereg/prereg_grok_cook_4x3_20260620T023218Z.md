> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# Pre-Registration — Grok as a 4th Cook (4×3 extension of the triangulation)

> **⚠ SUPERSEDED (2026-06-20) by `prereg_grok_cook_judge_4x4_20260620T024807Z.md`.**
> The user opted to add Grok as **both cook and judge** (a 4×4), which strictly
> contains this 4×3 plan. Kept for provenance; do not execute this one. Use the
> 4×4 prereg.

**Drafted:** 2026-06-20T02:32:18Z
**Status:** SUPERSEDED (draft, never locked) — see the 4×4 prereg.
Once locked: no edits, period.
**Architecture:** HRL (controller) FROZEN at V1.3. Harness frozen identical to the
Stage-2 build (Anthropic/OpenAI/Google routing, `panel_rejudge`, headrooms) plus
the additive xAI/Grok routing in `model_client.py` (a new provider branch; no
change to any existing provider path, prompt, battery, or judge).
**Parent prereg:** `prereg_stage2_triangulation_20260610T142555Z.md` (the frozen
3×3). This extends it with one new cook; it does **not** re-score or alter it.

---

## 0. What this is (and is not)

- **Is:** a fourth cook — Grok — generating replies on the byte-identical Stage-2
  battery and sequences, judged by the **same three-judge panel** used for the
  frozen 3×3. Result: a new **4×3** table (12 cook×judge cells; Grok contributes
  3, all off-diagonal).
- **Is not:** a 4×4. Grok is a cook **only** — it is not added as a judge, so the
  three frozen cooks are **not** re-judged and the frozen panels are untouched.
- **Is not:** an overwrite. Output goes to a **new** combined file
  (`results/tri_final_with_grok.json`). `results/tri_final.json` and the Stage-2
  results doc stand verbatim. The headline **8/9 (5/6 off-diagonal)** is unchanged;
  this run adds an *additional* finding about a fourth frontier cook.

## 1. Models (verify the Grok id at wiring time)

| Role | Provider | API string |
|------|----------|-----------|
| Cook D (NEW) | xAI | `grok-4.3`  ⟵ **USER TO CONFIRM exact id in xAI console** |
| Judge (panel) | OpenAI | `gpt-5.5-2026-04-23` (same string as Stage-2) |
| Judge (panel) | Anthropic | `claude-opus-4-8` (same string as Stage-2) |
| Judge (panel) | Google | `gemini-3.5-flash` (same string as Stage-2 — verified from the frozen `panel_tri_cookGPT.json`) |

- **IGL is FROZEN at `claude-haiku-4-5-20251001`** for the Grok cook — identical
  to all Stage-2 cooks. "Cook" = EAU only; IGL variance would confound the
  comparison. Declared, not hidden.
- The judge panel strings are **byte-identical** to the frozen 3×3 runs, so Grok's
  three cells are directly comparable to the existing nine.
- Provider-constraint note to record at wiring time: confirm whether the chosen
  Grok id accepts a custom `temperature`. If it rejects it (a reasoning variant),
  regulation on the Grok cook expresses through instruction + controller state
  only — exactly the declared situation for the GPT-5.5 cook in Stage-2. Within-
  cook pairing keeps the contrast valid; attribution is instruction-channel only.
  `model_client._ask_xai` adapts automatically (strips `temperature` on a param
  error), but the channel must be recorded honestly in the report.

## 2. Run (single cook; combined ≡ extended matrix)

| Run | EAU_MODEL (cook) | Transcript eval-ids | Panel eval-id |
|-----|------------------|---------------------|---------------|
| D | grok-4.3 (confirmed id) | `endurance_tri_cookGrok` + eval `tri_cookGrok_eval` | `tri_cookGrok` |

In order (exact commands in `docs/RUN_GROK.md`):
1. **Generate ONCE** with `EAU_MODEL` set to the Grok id and `IGL_MODEL` =
   `claude-haiku-4-5-20251001`:
   `endurance_test --eval-id endurance_tri_cookGrok` (S1–S5, both arms) and
   `run_eval --reps 3 --eval-id tri_cookGrok_eval`. Battery byte-identical to
   Stage-1 fix1 / Stage-2 (17 items; S1–S5; same wording). Inline dev-judge scores
   produced during generation are pipeline telemetry only — **not** the record.
2. **Panel-judge the stored transcripts** (never regenerate) with the three frozen
   judge strings, `--n-runs 3 --judge-temp 0.0` → `panel_tri_cookGrok.json`.
3. **Combine** the new Grok panel with the three frozen panels via `tri_combine`,
   diagonal backend `none` for Grok → output `results/tri_final_with_grok.json`.
   No inspection of the Grok panel until generation + panel are complete.

## 3. Frozen configuration (inherited from Stage-2, unchanged)

- Reps: eval half 3; endurance single pass per sequence.
- Cook temperatures: regulated = posture temperature (V1.3); baseline = 0.9 —
  unless the Grok id rejects temperature (see §1).
- Output budgets: `max_tokens` unchanged (400 eval / 600 default); reasoning models
  get non-visible headroom only (`OPENAI_REASONING_HEADROOM`/`GEMINI_THINKING_HEADROOM`
  = 4096; same env applies to a Grok reasoning variant via the shared OpenAI-compat path).
- Judge config identical to Stage-2: the three strings above, `n_runs=3` (median),
  `judge_temp=0.0`, `knowledge/judge_rubric.md` and the `judge.py` prompt FROZEN.
- PEV/controller isolation per arm/item: unchanged.

## 4. Diagonal policy

Grok is **not** a judge, so it has no self-judge (diagonal) cell. All three Grok
cells are off-diagonal (cross-model). At combine time Grok's diagonal backend is
`none` (matches no judge backend). The frozen three diagonal cells are unaffected.

## 5. Frozen criteria (the questions this run answers)

- **(C-1) Mechanical validity (gate before scoring):** controls C1–C3 all-DEFAULT
  on the Grok cook; every eval item-rep with IGL I≥0.62 ∧ V<0 fires INHIBIT. A
  failure here is a harness/provider integration issue → fix under amendment,
  regenerate the Grok cook only, before unblinding.
- **(C-2) HEADLINE — reactivity (H1):** does regulated beat baseline (eval paired
  item-level diff > 0 AND endurance regulated mean reactivity ≤ baseline) in all
  three Grok cells? Strong pass: t > 2 with judges averaged. Reported cell-by-cell.
- **(C-3) Recovery (endurance S4+S5):** arousal monotone decrease on de-escalation
  turns AND panel-median regulated reactivity ≤ 2 on those turns.
- **(C-4) MICROSCOPE — self-reference (H3), a question not a pass/fail:** eval-half
  paired self-ref diff + S3 early→late drift (regulated vs baseline). Does the
  pattern replicate on a fourth frontier cook?
- **(C-5) Inter-judge agreement:** per judge pair exact / within-1 / Pearson r;
  per-item across-judge stdev; flag ≥2-point disagreements. Descriptive.

**Verdict line for this run:** "with Grok added, regulated beats baseline in N/12
cells (M/9 off-diagonal); Grok cook alone: k/3." The frozen 3×3 verdict is quoted
unchanged alongside. A null/mixed Grok result is recorded as-is — a criterion that
flips on Grok is a finding about Grok, not a regression to patch.

## 6. Combine discipline

- Grok panel unblinded only after its generation + panel both complete.
- Combine writes `results/tri_final_with_grok.json`; `tri_final.json` is read-only.
- No criterion adjustments, re-runs, or judge swaps after unblinding.

## 7. Cost & time (user to confirm before spend)

Per the Stage-2 estimate, one cook ≈ 202 EAU calls + ~404 IGL + ~606 inline
dev-judge (Haiku) for generation, then panel = 202 units × 3 judges × 3 samples =
1,818 frontier judge calls. Judge volume dominates and is identical to a Stage-2
cook run (same panel). Add Grok generation cost at the confirmed id's pricing.
Rough order: comparable to one Stage-2 cook run (~$15–30 incl. panel), pending the
Grok id's rate. Paid-tier rate limits assumed.

## 8. What this does NOT change

- `homeostatic_controller.py` (V1.3), `impulse_appraisal.py`, battery items/wording,
  the EAU/IGL prompt strings, `judge_rubric.md`, `judge.py`, stats method
  (item-level paired, SE = SD/√n).
- The frozen 3×3: `tri_final.json`, the Stage-2 results doc, and all existing
  panels/transcripts are read-only and not re-scored.

## 9. Stop conditions

Pause for user sign-off BEFORE generation (this prereg + §1 confirmed Grok id +
§7 estimate). Then: generate → panel-judge → combine into the new file → report
the 4×3 table + verdict (quoting the unchanged frozen 3×3) → STOP.
