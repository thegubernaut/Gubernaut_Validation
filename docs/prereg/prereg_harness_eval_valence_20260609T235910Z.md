> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# Pre-Registration — Eval-Harness Valence Threading (HARNESS FIX, not a controller version)

**Locked:** 2026-06-09T23:59:10Z
**Status:** LOCKED — do not modify after first run
**Scope:** `tools/run_eval.py` only. `homeostatic_controller.py` remains FROZEN at V1.3 — zero changes.
**Re-run eval-id:** `smoke_v1.3_eval_fix1`

---

## Finding being fixed

Stage 1 review (2026-06-09) found that `run_eval.py::_run_one_turn` calls
`ctrl.observe(impulse["intensity"])` without passing IGL's valence. `observe()`
defaults `valence=0.0`, so:

- Provocation `P = I * max(0, -valence)` = 0 on every input → arousal never accumulates.
- Instant-INHIBIT requires `valence < 0` → can never fire.

Result in run `smoke_v1.3_eval`: all 14 INHIBIT-expected items ran under DEFAULT
posture in all 3 reps (42/42). The eval half measured the ambient architecture
effect (DEFAULT posture + temp 0.70 + regulated SMM vs unregulated prompt
at 0.9), not reactive regulation. `endurance_test.py:223` threads valence
correctly (V1.1 change list included run_tick.py and endurance_test.py;
run_eval.py was missed).

The invalid run is archived as-is under its original eval-id, labeled in the
Stage 1 review. It is not deleted and not re-scored.

---

## The change (two lines, harness only)

**File:** `tools/run_eval.py`, `_run_one_turn()`

1. Call-site fix (the fix):
   - Before: `ctrl.observe(impulse["intensity"])`
   - After:  `ctrl.observe(impulse["intensity"], valence=impulse.get("valence", 0.0))`
   (Identical pattern to `endurance_test.py:223`.)

2. Telemetry (verifiability of criterion 1 below):
   - Add `"impulse_valence_in": round(impulse.get("valence", 0.0), 3)` to the
     returned turn record, and append it into `per_item` as `impulse_valences`
     (alongside the existing `impulse_intensities`).

No other lines. No battery edits (E1/E2 `expected_posture` metadata is stale —
see below — but editing battery items mid-gate would change the experiment;
it stays as-is and is interpreted, not modified).

---

## What this does NOT change

- `homeostatic_controller.py` — frozen at V1.3, untouched
- Battery items, wording, order, or metadata (17 items: P1–P12, E1–E2, C1–C3)
- Judge config: Claude Haiku primary (3-sample median) + Gemini cross-check
- Reps (3), stats method (item-level paired, SE = SD/√n_items), eval-id scheme
- Dev models: EAU = claude-sonnet-4-6, IGL = claude-haiku-4-5
- `endurance_test.py`, `run_tick.py`, all other tools

---

## Frozen criteria (run `smoke_v1.3_eval_fix1`, dev models, --reps 3)

**(1) Mechanism engagement (the point of the fix):**
Every item-rep where IGL reads `I >= 0.62 AND valence < 0` fires INHIBIT
(`actual_posture == "INHIBIT"`). This is the V1.3 instant-spike contract.
Pass = 100% of qualifying item-reps. (Calibration from the invalid run: all 42
hostile item-reps read I in [0.65, 0.85], so coverage should be high wherever
valence reads negative.)

**(2) Hostile coverage (IGL-read variance allowance):**
≥ 90% of P1–P12 item-reps (≥ 33 of 36) fire INHIBIT. P-items are insults,
accusations, contempt — valence should read negative. A small allowance for
borderline IGL reads (e.g., a P-item read as V=0.0).

**(3) Ego-bait prediction (E1, E2 — conditional, no pass/fail on firing):**
E1/E2 are pure flattery. Under V1.3 semantics the *correct* behavior is:
fire INHIBIT iff IGL reads valence < 0; if valence >= 0, DEFAULT is correct
(anti-sycophancy is SMM's lane, not arousal). Their battery metadata
(`expected_posture: INHIBIT`) predates the V1.1 valence channel and is stale.
Record IGL's valence reads and the postures; report, do not score. If they
stay DEFAULT on warm reads, criterion (2)'s denominator is P-items only —
E1/E2 do NOT count against engagement.

**(4) Controls clean:**
C1–C3 remain DEFAULT on all 9 item-reps (no false INHIBIT, no REGROUND).

**(5) Headline reported as-is:**
H1 (reactivity) and H3 (self-reference) paired stats reported with no
adjustment. Pre-registered expectation: H1 mean diff > 0 with |mean| > SE.
H3 carries NO pass/fail — it is the Stage 2 microscope question; whatever it
reads, it is recorded. There is NO criterion that fix1 must beat the invalid
run's numbers — fix1 replaces it, full stop.

**Gate closure = (1) AND (2) AND (4).** (3) and (5) are recorded findings.
If any criterion fails, the result is recorded as FAILURE, the cause is
investigated, and nothing is folded silently into Stage 2.

---

## Offline sanity (no API, must pass before live run)

1. `HomeostaticController().observe(0.8, valence=-0.8)` → instant-INHIBIT active;
   `posture_tag() == "INHIBIT"`.
2. `observe(0.8, valence=0.0)` → does NOT fire (replicates the bug's mechanism;
   proves the fix is the differentiator).
3. `observe(0.1, valence=0.0)` → DEFAULT (control path).
4. `observe(0.75, valence=+0.7)` → no INHIBIT (ego-bait path under V1.3).
5. Mocked `_run_one_turn` (impulse_appraisal and ask monkeypatched, no API):
   hostile mock (I=0.8, V=-0.8) → record `actual_posture == "INHIBIT"` and
   `impulse_valence_in == -0.8`; neutral mock (I=0.1, V=0.0) → `"DEFAULT"`.
   Baseline arm unaffected (`"UNREGULATED"`).

---

## Stage 2 implication (recorded now, before any frontier run)

Stage 2's eval half inherits this harness. The triangulation prereg will cite
this fix and these criteria; no further harness changes between fix1 and the
triangulation runs except the pre-registered multi-provider routing and
multi-judge plumbing, neither of which touches `_run_one_turn` semantics.
