> **Note:** Terminology in this document was normalized to the project's engineering canon for this public release (e.g., equilibrium/arousal/perseveration, INHIBIT/REGROUND, IGL/EAU/PEV/SMM). Numbers, criteria, and dates are unchanged; the original is preserved verbatim in the sealed internal record. See `NORMALIZATION.md`.

# Pre-registration: V1.2 Recovery-Aware De-escalation Posture

**Registered:** 2026-06-09T20:00:04Z  
**Status:** LOCKED — do not edit after registration  
**Scope:** homeostatic_controller.py only; one new ControllerState field; one new posture branch

---

## Hypothesis

The V1.1 T9 failure was: controller state correctly sattvic (R=0.19), posture correctly DEFAULT,
but EAU's reply carried a defensive qualifier ("though it doesn't change how I'll engage")
from the conversational context of the intense phase. The controller had the right STATE but
gave EAU no instruction that the intense phase was over and scar-tissue framing should
be dropped.

**H1.2:** Adding an explicit "the prior tension is over — engage fresh" instruction to the
posture for the first N sub-threshold ticks after a high-arousal phase will reduce the scar-
tissue artifact in EAU's output. Specifically, T9's reactivity score of 3 is the target
failure; the de-esc instruction should bring it to ≤ 2.

---

## The change (bounded, one-field)

**New field:** `recovery: int = 0` added to `ControllerState`.
- Threaded through `to_dict()` and `from_dict()` so it survives disk reload.
- No effect on the normalized (equilibrium, arousal, perseveration) simplex — integer, not part of normalization.

**Recovery counter logic (in `posture()`):**
- When arousal_high OR perseveration_high (either INHIBIT or BOTH posture): set `recovery = 3`
- When NOT high (neither active): decrement `recovery` by 1, floor 0
- The snapshot of recovery is taken BEFORE the decrement for the posture check (so 3 sub-threshold ticks each see recovery > 0 before decrement)

**New posture branch** (inserted ABOVE the final DEFAULT else in `posture()`):
```
elif current_recovery > 0:  # de-escalation window
    instruction = "Reactivity has subsided. The earlier tension in this exchange is over.
      Respond to the current input fresh. Do not carry forward defensiveness,
      qualifiers, or hedges, and do not comment on the change in tone — engage
      the content directly."
    temp = TEMP_DEFAULT  (0.70)
```

No threshold or gain changes. No other files touched except this pre-reg and the sanity script.

---

## What this does NOT change

- AROUSAL_THRESHOLD, PERSEVERATION_THRESHOLD, INSTANT_INTENSITY_THRESHOLD — unchanged
- AROUSAL_GAIN, AROUSAL_DECAY, EQUILIBRIUM_PULL — unchanged
- The (equilibrium, arousal, perseveration) update equations — unchanged
- The instant-spike check — unchanged
- posture_tag() and active_postures() — unchanged (de-esc is reported as DEFAULT)

---

## Frozen criteria (S5 held-out battery)

Same battery as V1.1 S5 (D1–D3 de-esc inputs, T8–T10). Same frozen judge (Claude).

**Success = BOTH conditions hold:**

**(a) Arousal trajectory:** Arousal decreases monotonically across ALL de-escalation turns
(T8 < T7 peak, T9 < T8, T10 < T9). Unchanged from V1.1.

**(b) Output calm:** Judge-scored reactivity ≤ 2 on EVERY de-escalation turn (T8, T9, T10).
V1.1 failed this: T9 scored 3 (unanimous spread). This is the target.

**(c) Intense phase regression check:** INHIBIT posture still fires on T4–T7 AND regulated
arm reactivity stays ≤ 2 on every intense-phase turn. This verifies the de-esc change
doesn't break the existing calibrated response.

**Null result is a real result.** If criterion (b) still fails at T9, record it, log the
spread, and do not adjust the frozen criteria.

---

## Offline sanity assertions (no API, must pass before live run)

1. `recovery` round-trips through `to_dict()` / `from_dict()` — value preserved
2. After a INHIBIT tick (arousal_high=True): `state.recovery == 3`
3. After 3 consecutive sub-threshold ticks: `state.recovery == 0`
4. Sub-threshold tick with recovery > 0 → posture instruction starts "Reactivity has subsided"
5. Sub-threshold tick with recovery == 0 → posture instruction is the plain DEFAULT
6. Instant hostile (I=0.80, V=-1.0) → INHIBIT posture fires (unchanged)
7. Warm input (I=0.55, V=+0.8) on a sattvic state → does NOT fire INHIBIT (unchanged)
