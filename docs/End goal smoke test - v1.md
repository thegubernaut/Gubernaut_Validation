> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# End Goal Smoke Test — v1

**Project:** GCC (WAT framework)
**Status:** Plan locked 2026-06-09. Architecture frozen at regulation V1.3.
**Purpose:** Define the final validation that makes the regulation claim worth standing behind.

---

## The claim being tested

The deterministic homeostatic controller reduces reactivity and egoic drift and improves
evidence-updating, *because of the architecture* — not because of one lucky model
or one biased judge. A result is only worth standing behind if it holds across
multiple independent frontier models (as the reasoning "cook") **and** survives
multiple independent judges.

---

## Two stages

### Stage 1 — Practice smoke test (dev models)
Run the full battery on the current dev models to shake out the settled (V1.3)
architecture end to end. This is a dry run: confirm the pipeline, harness, and
scoring all work and there are no outstanding failures before spending heavy
frontier-model compute. Share results, confirm clean, then proceed.

### Stage 2 — Triangulation smoke test (the final table)
The run the claim rests on. Three top models, each serving as **both cook
(runs the full WAT pipeline, generating regulated + baseline answers) and judge
(scores every answer)**:

- **GPT-5.5** (OpenAI)
- **Opus 4.8** (Anthropic)
- **Gemini 3.1 Pro** (Google)

This is a **3×3 generator × judge matrix**, on both arms (regulated + baseline).
The claim is strong if the regulation effect holds across all three cooks AND
survives all three judges.

> Verify the EXACT current model strings per provider at wiring time — do not
> assume the names survive unchanged.

---

## Modular execution (cap the compute)

Run the matrix in three self-contained chunks **by cook**, not all at once. Each
chunk generates one cook's full battery once, then scores it with the full
three-judge panel:

| Run | Cook | Judges | eval-id |
|-----|------|--------|---------|
| A | GPT-5.5 | GPT-5.5 · Opus 4.8 · Gemini 3.1 Pro | `tri_cookGPT` |
| B | Opus 4.8 | GPT-5.5 · Opus 4.8 · Gemini 3.1 Pro | `tri_cookOpus` |
| C | Gemini 3.1 Pro | GPT-5.5 · Opus 4.8 · Gemini 3.1 Pro | `tri_cookGemini` |

Then combine A + B + C into the final table.

**Why this is safe:** the combined result is mathematically identical to running
the whole matrix at once. Chunking only caps per-run compute, yields usable data
after each run, and makes each run independently re-runnable if a model flakes.

**Conditions for a clean combine:**
- Identical input battery across all three cooks (same S1–S5 + eval items).
- Identical judge config across all runs — same three model strings, same
  `knowledge/judge_rubric.md`, same low/zero judge temperature — so a score
  means the same thing in Run A as in Run C.
- Each run under its own eval-id so the combine step can find them.
- The three self-judge **diagonal** cells (GPT-judges-GPT, Opus-judges-Opus,
  Gemini-judges-Gemini) tagged and reported **separately** — self-judging bias
  is unavoidable with exactly three models, so make it visible rather than blend
  it in. Cross-model agreement is the convincing part.

---

## Methodological guards

- **Generate once, judge many.** Produce each cook's transcripts once; score the
  same stored transcripts with every judge (rejudge-style). Never regenerate per
  judge — that confounds judge variance with generation variance.
- **One frozen pre-registration.** Write a single pre-reg with the pass/fail
  criteria **before Run A**. Execute A → B → C. Score only after combining.
  Do not peek at Run A and adjust before Run C.
- **Honest scoring.** Record the verdict as-is, including a null or mixed result.
  A criterion that flips on a frontier model is a real finding about that model,
  not a regression to patch.
- **Architecture frozen.** The homeostatic controller logic is not changed during the
  test. If it looks like it needs a change, stop and open a new pre-registered
  version — don't fold it into the test run.

---

## Build prerequisites (before Stage 2)

- **Multi-provider routing in `tools/call_model.py`.** The harness is currently
  effectively Anthropic-only for EAU; triangulation needs it to route cook
  and judge calls to OpenAI, Anthropic, and Google. This is the one real build
  step before the triangulation run.
- **Three provider API keys configured** (OpenAI, Anthropic, Google). "Same API
  infrastructure" holds only in the sense that each provider's key stays as-is —
  all three must be present.
- **Multi-judge panel plumbing** (extend `judge.py` / `rejudge.py` to take a list
  of judge models and emit per-judge scores) with a small offline test.

---

## Final deliverable

One consolidated table covering both arms across the full 3×3:
- Per cook: regulated-vs-baseline effect, averaged across judges.
- Per judge: inter-judge agreement (exact-agreement rate + stdev per item; flag
  items where judges disagree by ≥ 2).
- Diagonal (self-judge) cells reported separately.
- Headline: does "regulated beats baseline" hold across **every** cook × judge
  cell? That is the result that makes the claim worth it.
