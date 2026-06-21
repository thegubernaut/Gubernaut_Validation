# Nomenclature normalization in this public release

This release uses the project's engineering vocabulary throughout: the faculties
IGL (impulse layer), EAU (executive arbiter), PEV (episodic vault), and SMM
(self-model); the controller state variables equilibrium / arousal / perseveration;
and the postures DEFAULT / INHIBIT / REGROUND.

An earlier internal development line used different working labels for these same
components. For a consistent public record, the materials here were **normalized to
the engineering canon** — specifically:

- transcript field names and posture values (controller-state keys, posture strings),
- the pre-registrations (`docs/prereg/`), and
- the frozen results documents (`docs/Stage*`).

This is a **label-only** transformation:

- No number, score, criterion, threshold value, input, model reply, date, or
  judgment was changed.
- The judge panels and the combined matrices (`tri_final.json`, `tri_final_4x4.json`)
  are unaffected; every published result reproduces from the panels via
  `tools/tri_combine.py` (see `02_data/scripts/RECOMPUTE.md`).
- `SHA256SUMS` is computed over the published (normalized) files, so the release is
  internally integrity-checkable exactly as shipped.
- The sealed internal record preserves the original working labels verbatim.

## One honest exception
A small number of model **replies** quote a harness field label in their own text
(the model echoed a prompt label into its answer). These are left **verbatim as
model output** — altering a transcript reply would falsify the evidence this
release exists to make verifiable.
