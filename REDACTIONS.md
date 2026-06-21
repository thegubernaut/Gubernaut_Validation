# Redactions in this public release

This release is intended to be independently re-computable and re-judgeable. For
full transparency, this file records every deviation between the data published
here and the sealed internal record.

## The only redaction

To keep the controller's calibration constants proprietary, the per-sequence
**recovery-verdict analysis block** was removed from the published endurance
transcripts. This block is appended *analysis*, not primary evidence: it restated
the INHIBIT arousal threshold and the post-de-escalation arousal trajectory. It
was removed from all sequences of:

  - 02_data/raw/endurance_endurance_tri_cookGPT.json
  - 02_data/raw/endurance_endurance_tri_cookOpus.json
  - 02_data/raw/endurance_endurance_tri_cookGemini.json
  - 02_data/raw/endurance_endurance_tri_cookGrok.json

## What is NOT affected

- All user inputs and model replies (the evidence used for re-judging) are verbatim.
- The combined matrices (tri_final.json, tri_final_4x4.json) — including the C-3
  recovery result (4/4) — all judge panels, and all extracted tables are unaffected.
  Recovery is recomputed from the judge PANELS, not from this block, so every
  published number reproduces exactly via tools/tri_combine.py.
- SHA256SUMS is computed over the published files, so this release is internally
  integrity-checkable exactly as shipped.

## Note on provenance & telemetry
Because the transcripts were edited, their sha256 differs from the value recorded
inside the panels' "sources" field; integrity for this release is via SHA256SUMS
plus the tri_combine recompute (see 02_data/scripts/RECOMPUTE.md). The published
per-turn controller state {equilibrium, arousal, perseveration} is real telemetry,
included so the regulation is inspectable; the controller's exact thresholds,
gains, and update law are proprietary (patent pending) and are not published.
