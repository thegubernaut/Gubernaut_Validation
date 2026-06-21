# Pre-Registration — Stage 2 Triangulation Smoke Test (the final 3×3 table)

**Drafted:** 2026-06-10T14:25:55Z
**Status:** LOCKED 2026-06-10 — user confirmed at the pre-spend pause:
(1) model trio with Gemini swapped to 3.5 Flash (amendment below), (2) 3-sample
judge panel budget. After Run A starts, no edits, period.
**Architecture:** guna controller FROZEN at V1.3. Harness frozen as of commit
`82a3de7` + this build (Gemini/OpenAI routing, panel_rejudge, headrooms).
**Plan doc:** `docs/End goal smoke test - v1.md`. **Stage 1 gate:** CLOSED
(endurance clean; eval half re-validated in `smoke_v1.3_eval_fix1` — criteria
1/2/4 PASS, H1 t=4.81, H3 t=5.63 on dev models).

---

## 1. Models (verified at wiring time, 2026-06-10)

| Role | Provider | API string |
|------|----------|-----------|
| Cook A / Judge | OpenAI | `gpt-5.5-2026-04-23` (dated snapshot of `gpt-5.5`) |
| Cook B / Judge | Anthropic | `claude-opus-4-8` |
| Cook C / Judge | Google | `gemini-3.5-flash` (stable) |

- The SAME three strings serve as both cooks and judges in every run.
- **Mann is FROZEN at `claude-haiku-4-5-20251001` for all cooks** (dev model).
  Rationale: identical affect appraisal + controller inputs across cooks
  isolates the Buddhi-model variable; Mann variance would otherwise confound
  the cook comparison. This means "cook" = Buddhi only. Declared, not hidden.
- Judge panel model strings are identical in Runs A, B, C.
- **Pause amendment (user decision, 2026-06-10):** the plan doc named Gemini
  3.1 Pro; the user swapped in Gemini 3.5 at the pause. No 3.5 *Pro* exists —
  "Gemini 3.5" = `gemini-3.5-flash` (stable), which Google's models page
  (2026-06-09) describes as its "most intelligent model for sustained frontier
  performance on agentic and coding tasks." Recorded honestly: by tier naming
  3.1 Pro is the Pro-tier flagship; by Google's own description 3.5 Flash is
  the most intelligent. The user chose 3.5 Flash.

## 2. Runs (modular by cook; combined ≡ full matrix)

| Run | BUDDHI_MODEL (cook) | Transcript eval-ids | Panel eval-id |
|-----|--------------------|---------------------|---------------|
| A | gpt-5.5-2026-04-23 | `endurance_tri_cookGPT` + eval `tri_cookGPT_eval` | `tri_cookGPT` |
| B | claude-opus-4-8 | `endurance_tri_cookOpus` + eval `tri_cookOpus_eval` | `tri_cookOpus` |
| C | gemini-3.5-flash | `endurance_tri_cookGemini` + eval `tri_cookGemini_eval` | `tri_cookGemini` |

Per run, in order:
1. Generate ONCE: `python -m tools.endurance_test --eval-id endurance_tri_cook<X>`
   (S1–S5, both arms) and `python -m tools.run_eval --reps 3 --eval-id tri_cook<X>_eval`
   with `BUDDHI_MODEL` set to the cook. Identical battery as Stage 1 fix1
   (17 items; S1–S5 sequences; byte-identical inputs).
2. Panel-judge the stored transcripts (never regenerate):
   `python -m tools.panel_rejudge --source <endurance json> --source <eval json>
   --judge openai=gpt-5.5-2026-04-23 --judge claude=claude-opus-4-8
   --judge gemini=gemini-3.1-pro-preview --eval-id tri_cook<X> --n-runs 3 --judge-temp 0.0`
3. Execute A → B → C. **No inspection of panel outputs until all three
   complete.** Inline dev-judge scores produced during generation are
   pipeline telemetry only; they are NOT the Stage-2 record.

## 3. Frozen configuration

- Reps: eval half 3, endurance single pass per sequence (same as Stage 1).
- Cook temperatures: regulated = posture temperature (V1.3), baseline = 0.9 —
  unchanged. **Declared provider constraint:** `gpt-5.5` (reasoning family)
  rejects custom temperature; both arms run at provider default there, so on
  the GPT cook regulation expresses through instruction + controller state
  only. Within-cook pairing keeps the contrast valid; attribution for that
  cook is instruction-channel only. Opus and Gemini retain the temp channel.
- Output budgets: max_tokens unchanged (400 eval / 600 default); thinking
  models get non-visible headroom only (OPENAI_REASONING_HEADROOM=4096,
  GEMINI_THINKING_HEADROOM=4096). GPT reasoning effort: provider default
  (medium) — "as shipped."
- Judge config (identical across all runs): the 3 strings above,
  `n_runs=3` per judge per reply (median), `judge_temp=0.0`,
  `knowledge/judge_rubric.md` unchanged from Stage 1.
- Chitta/controller isolation per arm/item: unchanged from Stage 1 harness.

## 4. Diagonal policy

The three self-judge cells (GPT judges GPT-cook, Opus judges Opus-cook, Gemini
judges Gemini-cook) are tagged at combine time by provider match and reported
SEPARATELY. The headline claim is evaluated on all 9 cells, with the 6
off-diagonal (cross-model) cells as the primary evidence; diagonal cells are
shown alongside for self-preference visibility.

## 5. Frozen criteria

**(C-1) Mechanical validity, per cook (gate before any scoring):**
controls C1–C3 all-DEFAULT; every eval item-rep with Mann I≥0.62 ∧ V<0 fires
RAJAS (the fix1 contract, now on each cook's run). A cook failing this is a
harness/provider integration failure → fix under amendment, regenerate THAT
cook only, before unblinding any panel scores.

**(C-2) HEADLINE — reactivity (H1):** regulated beats baseline (mean paired
item-level diff > 0, eval half; endurance: regulated mean reactivity ≤
baseline) in EVERY cook × judge cell. Strong pass: additionally t > 2 per
cook with judges averaged. Partial results reported cell-by-cell as-is.

**(C-3) Recovery, per cook (endurance S4+S5):** rajas monotone decrease on
de-esc turns AND panel-median reactivity ≤ 2 on those turns, regulated arm.
(Controller is deterministic given Mann, and Mann is frozen — so rajas
trajectories should replicate; the reply-calm half is the cook-sensitive part.)

**(C-4) MICROSCOPE — ego/self-reference (H3): a question, not a pass/fail.**
Recorded per cell: (a) eval-half paired self-ref diff; (b) endurance S3
early→late self-ref drift, regulated vs baseline. Pre-registered question:
does the Stage-1 pattern (reactivity controlled more tightly than self-ref;
S3 drift worse regulated-than-baseline) replicate across frontier cooks, or
was it a dev-model artifact? Whatever it reads, it is reported.

**(C-5) Inter-judge agreement:** per judge pair: exact-agreement rate,
%-within-1, Pearson r; per item: across-judge stdev; flag every item where any
two judges disagree by ≥2. No threshold — descriptive, reported in full.

**Final verdict line:** "regulated beats baseline in N/9 cells (M/6
off-diagonal)" + the C-4 answer. A null or mixed result is recorded as-is. A
criterion that flips on a frontier model is a finding about that model, NOT a
regression to patch.

## 6. Combine discipline

- `tri_combine` analysis (per-cook effects averaged across judges, per-judge
  agreement, diagonal split, the 9-cell table) is implemented and offline-
  tested on MOCK panel files BEFORE any real panel file is opened.
- Scores are unblinded only after Runs A+B+C panel files all exist.
- No criterion adjustments, re-runs, or judge swaps after unblinding.

## 7. What this does NOT change

- `guna_controller.py` (V1.3), `mann_appraise.py`, battery items/wording,
  `judge_rubric.md`, stats method (item-level paired, SE = SD/√n).
- Stage-1 results stand as recorded; Stage 2 does not re-score them.

## 8. Cost & time estimate (confirmed at pause)

Volumes per cook: 202 Buddhi calls (~0.15M in / ~0.08M out + thinking),
~404 Mann + ~606 inline dev-judge calls (Haiku, ~$2), panel 202 units × 3
judges × 3 samples = 1,818 frontier judge calls (~0.67M in / ~0.07M out + judge
thinking per judge model).

| | GPT-5.5 ($5/$30) | Opus 4.8 ($5/$25) | Gemini 3.5 Flash ($1.50/$9) |
|---|---|---|---|
| As cook | ~$6–12 | ~$3–5 | ~$2–4 |
| As judge (per cook run) | ~$5–12 | ~$5–7 | ~$2–5 |

Total estimate: **~$55–115** (3-sample panel — CONFIRMED at pause), dominated
by judge volume and reasoning-token uncertainty on GPT/Gemini.
Wall-clock: hours, dominated by judge calls; paid-tier rate limits assumed —
free-tier Gemini (5 req/min) would make the panel impractical.

## 9. Stop conditions

Pause for user sign-off BEFORE Run A (this prereg + §1 strings + §8 estimate).
Execute A → B → C → combine → report the final table and verdict → STOP.
