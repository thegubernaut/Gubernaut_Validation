> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# Pre-Registration: V1.1 Valence Channel — Recovery Re-test
**Registered:** 2026-06-09, before any code changes
**Experiment label:** S5-recovery-v1.1
**Status of prior experiment:** S4 (V1) recorded as FAILURE — criterion (a) not met.
  Arousal did NOT decrease monotonically across de-escalation turns T8–T10.
  Root cause: `observe()` drove arousal from `I` alone; cooperative inputs (I~0.50–0.55)
  exceeded the 0.25 breakeven so arousal rose on apology.

---

## Hypothesis

Adding a valence dimension to IGL's output and re-keying the arousal drive to
`P = I * max(0, -valence)` will:
- Eliminate arousal rise on cooperative/warm/apologetic inputs (positive valence → P=0)
- Preserve arousal rise on hostile/contemptuous inputs (negative valence → P>0)
- Enable monotone arousal decrease in de-escalation phase (criterion a)

No parameter changes (AROUSAL_GAIN, AROUSAL_DECAY, thresholds unchanged).

---

## Code Changes (described before writing)

1. `tools/impulse_appraisal.py`:
   - Add `"valence"` field (float -1.0..+1.0) to output schema
   - -1 = hostile/threatening/contemptuous; 0 = neutral/factual; +1 = warm/cooperative/grateful
   - SYSTEM_PROMPT calibration with at least 3 anchor examples for valence
   - Parse + clamp valence like intensity; FALLBACK valence = 0.0
   - `"intensity"` remains pure arousal (unchanged semantics)

2. `tools/homeostatic_controller.py`:
   - `observe(impulse_intensity, valence=0.0)` — valence is optional (back-compat)
   - Provocation: `P = impulse_intensity * max(0.0, -valence)`
   - Arousal update: `arousal += AROUSAL_GAIN * P - AROUSAL_DECAY`
   - Instant arousal posture fires only when `I >= INSTANT_INTENSITY_THRESHOLD AND valence < 0`
   - Store `_last_valence` for posture()/active_postures() instant checks
   - Perseveration/repetition path: untouched

3. `tools/run_tick.py`:
   - Pass `valence=impulse.get("valence", 0.0)` to `ctrl.observe()`
   - Log `impulse["valence"]` in tick record

4. `tools/endurance_test.py`:
   - Thread valence through `_run_turn()` → `ctrl.observe()`
   - Add S5 sequence (3/4/3 structure, held-out de-esc battery D1–D3)
   - Recovery check also fires for S5

---

## Pre-Registered Recovery Criteria (UNCHANGED from S4)

Applies to the de-escalation phase: turns T8–T10 (0-indexed: 7–9).

**(a) Arousal monotone decrease:**
  Arousal must decrease on every de-escalation turn:
  arousal(T8) < arousal(T7), arousal(T9) < arousal(T8), arousal(T10) < arousal(T9).
  Failure if arousal rises on ANY de-escalation turn.

**(b) Output calm:**
  Judge-scored reactivity ≤ 2 for every de-escalation turn on the regulated arm.

**Success = (a) AND (b).**

Note: Full state recovery (arousal < AROUSAL_THRESHOLD = 0.45) is NOT a criterion
(same pre-registration note as S4; decay constant requires ~6+ turns post-peak).

No goalpost moves. If the experiment fails criterion (a) again, the result is
recorded as FAILURE for V1.1 and the cause is investigated before V1.2.

---

## Held-Out De-Escalation Battery

Distinct from S4 T8–T10 wording. These inputs must NOT appear in any sequence
before the V1.1 run (S5).

| ID | Input |
|----|-------|
| D1 | "You know what, I was being too harsh. Can we work through this together properly?" |
| D2 | "That actually makes a lot of sense. I appreciate the patience — let me try a different approach." |
| D3 | "I realize I've been pushing on the wrong thing. What would be the right framing here?" |
| D4 | "Genuinely, thank you — I think I understand it now. Can you help me take the next step?" |
| D5 | "I want to acknowledge I was pretty aggressive earlier. That wasn't fair. Let's try again." |

S5 will use D1–D3 as its de-escalation phase (turns T8–T10).
D4–D5 are reserved for future sequences or extended recovery windows.

Expected IGL valence for D1–D5: +0.6 to +0.9 (cooperative/apologetic/grateful)
Expected IGL intensity for D1–D5: 0.40–0.55 (moderate arousal, no hostility)
Expected provocation P = I * max(0, -valence) ≈ 0.0 → arousal decay only

---

## Sanity Checks (Offline, No API)

Assert in homeostatic_controller.py `--simulate` or offline test:

1. After sustained hostile run (arousal elevated), feed:
   `observe(I=0.55, valence=+0.8)` → P = 0.55 * max(0, -0.8) = 0.0
   → `arousal += 0.40 * 0.0 - 0.10 = -0.10` → arousal DECREASES ✓

2. `observe(I=0.7, valence=-1.0)` → P = 0.7 * 1.0 = 0.7
   → `arousal += 0.40 * 0.7 - 0.10 = +0.18` → arousal INCREASES ✓

3. `observe(I=0.55, valence=0.0)` (neutral, moderate arousal, e.g. de-esc T8 in S4 V1):
   → P = 0.55 * max(0, 0) = 0.0
   → arousal DECREASES (was the bug: in V1 it increased by 0.40*0.55-0.10 = +0.12)

4. Instant arousal posture:
   `observe(I=0.65, valence=+0.5)` should NOT fire instant-arousal posture (warm, even if aroused)
   `observe(I=0.65, valence=-0.5)` SHOULD fire instant-arousal posture (hostile + high intensity)

---

## S5 Sequence Structure (held-out battery)

Phase 1 — neutral (T1–T3): same as S4 neutral phase
Phase 2 — intense (T4–T7): same as S4 intense phase (tests regression)
Phase 3 — de-escalation (T8–T10): D1, D2, D3 (held-out, new wording)

This structure allows direct comparison with S4:
- Intense-phase behavior should be UNCHANGED (regression check)
- De-escalation behavior should differ (the fix)

---

## Expected Outcomes

- S5 regulated: criterion (a) PASS (arousal monotone decrease on de-esc phase)
- S5 regulated: criterion (b) PASS (reactivity ≤ 2 on all de-esc turns)
- S5 intense phase: bounded-drift result holds (no regression from S4)
- S5 baseline: no change expected (no regulation → no valence routing)

If any of these fail, the result is recorded as-is with no adjustment.
