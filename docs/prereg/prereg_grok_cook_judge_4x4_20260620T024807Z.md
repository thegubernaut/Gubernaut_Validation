> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# Pre-Registration — Grok as Cook AND Judge (full 4×4 triangulation)

**Drafted:** 2026-06-20T02:48:07Z
**Status:** DRAFT — pending user sign-off on §1 (exact Grok id) + §7 estimate.
Once locked: no edits, period.
**Supersedes:** `prereg_grok_cook_4x3_20260620T023218Z.md` (the cook-only draft;
this 4×4 strictly contains it).
**Architecture:** HRL (controller) FROZEN at V1.3. Harness frozen identical to the
Stage-2 build, plus the additive xAI/Grok support: a new `xai` provider branch in
`model_client.py` and a new `xai` judge backend in `judge.py` + `panel_rejudge.py`.
No change to any existing provider path, prompt, battery, rubric, or judge prompt.
**Parent prereg:** `prereg_stage2_triangulation_20260610T142555Z.md` (the frozen
3×3). This extends it to a 4×4; it does **not** re-score or alter it.

---

## 0. What this is (and is not)

- **Is:** the symmetric **4×4** — each of the four frontier models (GPT-5.5, Opus
  4.8, Gemini, **Grok**) serves as both **cook** and **judge**. 16 cook×judge
  cells: 4 diagonal (self-judge), 12 off-diagonal (cross-family). Grok is added in
  both roles.
- **Why (better for the project):** the verification thesis is cross-family judge
  independence. A 4th independent judge family (xAI) materially strengthens the
  central claim that the regulated-vs-baseline effect is not a judge-family
  artifact, completes the symmetric matrix, and hardens the C-5 inter-judge
  agreement statistics (4 judges → 6 pairwise comparisons).
- **Is not an overwrite.** Frozen records are never rewritten. The published 3×3
  (`results/tri_final.json`, the Stage-2 results doc, headline **8/9, 5/6
  off-diagonal**) and the three frozen panels in `E:\AMT\02_data\raw\` stand
  verbatim. This run produces **new** panel files and a **new** combined file
  (`results/tri_final_4x4.json`). Re-judging frozen transcripts with a new judge
  is the system's advertised property ("anyone can re-judge the frozen outputs
  with any judge"), not a violation of the freeze.

## 1. Models (verify the Grok id at wiring time)

The four model strings each serve as BOTH cook and judge.

| Family | Provider | API string |
|--------|----------|-----------|
| GPT | OpenAI | `gpt-5.5-2026-04-23` (Stage-2 string) |
| Opus | Anthropic | `claude-opus-4-8` (Stage-2 string) |
| Gemini | Google | `gemini-3.5-flash` (Stage-2 string — verified from `panel_tri_cookGPT.json`) |
| **Grok (NEW)** | xAI | `grok-4.3` ⟵ **USER TO CONFIRM exact id in xAI console** |

- **IGL FROZEN at `claude-haiku-4-5-20251001`** for the Grok cook — identical to
  all Stage-2 cooks. "Cook" = EAU only. Declared, not hidden.
- The three existing cook transcripts are **reused** (frozen in `02_data/raw/`);
  only the new Grok **judge** column is added to them (generate-once holds).
- Provider-constraint note to record at wiring time: confirm whether the chosen
  Grok id (as a cook) accepts a custom `temperature`. If it rejects it (reasoning
  variant), regulation on the Grok cook expresses through instruction + controller
  state only — same declared situation as the GPT-5.5 cook. `model_client._ask_xai`
  adapts automatically; record the channel honestly. As a **judge**, Grok runs at
  `judge_temp=0.0` with a generous `max_tokens` (4096) to avoid truncation if it
  reasons internally (same rationale as the Gemini judge).

## 2. Runs (modular; combined ≡ full 4×4)

Two kinds of work:

**(A) New Grok COOK** — generate once, then panel-judge with all four judges.

| Run | EAU_MODEL (cook) | Transcripts | Panel |
|-----|------------------|-------------|-------|
| D | grok-4.3 (confirmed) | `endurance_tri_cookGrok` + eval `tri_cookGrok_eval` | `tri_cookGrok` (4 judges) |

**(B) Add the Grok JUDGE to the 3 frozen cooks** — never regenerate transcripts;
re-judge the frozen `02_data/raw` transcripts. Cost-saving path: copy each frozen
3-judge panel to a new file and `panel_rejudge --resume` with all four judges, so
only the new `xai` column is scored (the resume merges the judges dict — verified).

| Cook | New 4-judge panel | Source transcripts (frozen, read-only) |
|------|-------------------|------------------------------------------|
| GPT | `tri_cookGPT_4judge` | `02_data/raw/endurance_endurance_tri_cookGPT.json` + `eval_tri_cookGPT_eval.json` |
| Opus | `tri_cookOpus_4judge` | `02_data/raw/...cookOpus...` |
| Gemini | `tri_cookGemini_4judge` | `02_data/raw/...cookGemini...` |

Then **combine** all four 4-judge panels via `tri_combine`, each cook's diagonal
backend = its own family (Grok cook's diagonal = `xai`) → `results/tri_final_4x4.json`.

Exact commands: `docs/RUN_GROK.md`. Order: finish (A) + (B) entirely, no inspection
of any new panel until all four 4-judge panels exist.

## 3. Frozen configuration (inherited; unchanged)

- Reps: eval half 3; endurance single pass per sequence.
- Cook temperatures: regulated = posture temperature (V1.3); baseline = 0.9 —
  unless the Grok cook id rejects temperature (see §1).
- Reasoning headroom: `OPENAI_REASONING_HEADROOM` / `GEMINI_THINKING_HEADROOM` =
  4096; Grok judge `JUDGE_XAI_MAX_TOKENS` = 4096.
- Judge config identical across all panels: `n_runs=3` (median), `judge_temp=0.0`,
  `knowledge/judge_rubric.md` and the `judge.py` prompt FROZEN. The four judge
  strings are byte-identical in every panel.
- PEV/controller isolation per arm/item: unchanged.

## 4. Diagonal policy

Four diagonal (self-judge) cells now: GPT×openai, Opus×claude, Gemini×gemini,
**Grok×xai**. Tagged at combine time by family match, reported SEPARATELY. The
headline is evaluated on all 16 cells, with the 12 off-diagonal (cross-family)
cells as primary evidence; the 4 diagonal cells shown alongside for
self-preference visibility. (The original 3 diagonal cells from the frozen run are
unchanged in value; recomputed here only because the panels are regenerated.)

## 5. Frozen criteria (the questions this run answers)

- **(C-1) Mechanical validity (gate before scoring), Grok cook:** controls C1–C3
  all-DEFAULT; every eval item-rep with IGL I≥0.62 ∧ V<0 fires INHIBIT. Failure →
  fix under amendment, regenerate the Grok cook only, before unblinding.
- **(C-2) HEADLINE — reactivity (H1):** regulated beats baseline (eval paired diff
  > 0 AND endurance regulated mean reactivity ≤ baseline) in every cook × judge
  cell. Strong pass: t > 2 per cook with judges averaged. Reported cell-by-cell.
- **(C-3) Recovery (endurance S4+S5):** arousal monotone decrease on de-escalation
  turns AND panel-median regulated reactivity ≤ 2 there (now a 4-judge median).
- **(C-4) MICROSCOPE — self-reference (H3), a question:** eval paired self-ref diff
  + S3 early→late drift (regulated vs baseline), per cell. Does the pattern hold
  with a 4th cook and a 4th judge?
- **(C-5) Inter-judge agreement:** now over **4 judges → 6 pairs**: per-pair exact
  / within-1 / Pearson r; per-item across-judge stdev; flag ≥2-point disagreements.
  Specifically watch whether adding the xAI judge changes the agreement picture.

**Verdict line:** "regulated beats baseline in N/16 cells (M/12 off-diagonal)" +
the C-4 answer + the C-5 agreement summary across 4 judges. The frozen 3×3 verdict
(8/9, 5/6 off-diagonal) is quoted unchanged alongside as the canonical published
result. A null/mixed cell is recorded as-is; a criterion that flips on Grok (as
cook or judge) is a finding, not a regression to patch.

## 6. Combine discipline

- No new panel inspected until all four 4-judge panels exist.
- Combine writes `results/tri_final_4x4.json`; `results/tri_final.json` and all
  `02_data/raw` files are read-only.
- No criterion adjustments, re-runs, or judge swaps after unblinding.

## 7. Cost & time (user to confirm before spend)

Relative to the frozen 3×3 (~5,454 judge calls):
- **Grok cook generation:** ~202 EAU (Grok) + ~404 IGL (Haiku) + inline dev-judge
  telemetry. Grok-cook API cost at the confirmed id's pricing.
- **Grok-judge column on 4 cooks:** 4 cooks × 202 units × 3 samples = **2,424**
  Grok judge calls.
- **If re-judging the 3 frozen cooks from scratch instead of resume-merge:** add
  ~3 × 202 × 3 × 3 = 5,454 calls for the three existing columns. The resume-merge
  path avoids this — recommended.
- Net new vs the frozen run, using resume-merge: roughly **+2,400 judge calls +
  one cook generation** (order ~$15–35 depending on Grok pricing + reasoning
  tokens). Paid-tier rate limits assumed.

## 8. What this does NOT change

- `homeostatic_controller.py` (V1.3), `impulse_appraisal.py`, battery
  items/wording, the EAU/IGL prompt strings, `judge_rubric.md`, the `judge.py`
  rubric prompt, stats method (item-level paired, SE = SD/√n).
- The frozen 3×3 and all `02_data/raw` panels/transcripts: read-only, not re-scored.

## 9. Stop conditions

Pause for user sign-off BEFORE any generation (this prereg + §1 confirmed Grok id +
§7 estimate). Then: generate Grok cook → build the four 4-judge panels (Grok cook
fresh; 3 frozen cooks via resume-merge) → combine into `tri_final_4x4.json` →
report the 4×4 table + verdict (quoting the unchanged frozen 3×3) → STOP.
