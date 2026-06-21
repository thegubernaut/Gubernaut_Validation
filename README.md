# Gubernaut — A Cognitive Control System for Verifiable Agent Alignment

**Gubernaut Cognitive Controller (GCC):** a deterministic, model-agnostic control
layer that wraps any LLM in a dual-process architecture — a fast impulse layer, an
executive arbiter, an episodic memory, a self-model — under a homeostatic
metacognitive controller. It does not retrain the host model. It regulates it at
runtime, and every regulatory decision is logged, inspectable, and reproducible.

This is a control system, not a "mind" in any philosophical sense. No claims about
consciousness are made anywhere in this project; the controller's target regime is
an engineering objective (calm, evidence-responsive output under adversarial
pressure), and every claim traces to logged, re-judgeable runs.

## What's in this repository

This is the **evidence & verification release** — the data and tooling behind the
headline result, published so a stranger can reproduce it. It is *not* the
controller's source: the control logic, prompts, thresholds, and held-out
instruments are proprietary (patent pending) and excluded (see `RELEASE_MANIFEST.md`).

| Path | What |
|---|---|
| `02_data/raw/` | every model transcript and judge panel (the frozen 3×3 + the Grok 4×4), plus `tri_final.json` / `tri_final_4x4.json` |
| `02_data/tables/` | extracted CSVs + figures (master table, agreement, recovery, dampening) |
| `02_data/scripts/` | regenerate the tables/figures; `RECOMPUTE.md` shows how to rebuild the matrix |
| `tools/tri_combine.py` | the combine script — rebuilds the whole matrix from the panels |
| `docs/` | architecture overview, taxonomy scorecard, the Stage-1/2/3 results docs, and the five pre-registrations |
| `SHA256SUMS` · `REDACTIONS.md` | integrity manifest and the single documented redaction |

**Reproduce it in one command** (`02_data/scripts/RECOMPUTE.md`): `tri_combine.py`
over the four published panels regenerates **15/16 (11/12 off-diagonal, 4/4
diagonal)**. Or score the transcripts with your own judge — the generate-once /
judge-many design makes the result independent of our judges.

## Framework

The system implements a formal monitoring–control loop in the sense of Nelson &
Narens (1990): an **object level** (impulse generation + response arbitration over
raw text) and a **meta level** (the controller), which never ingests tokens — it
reads only numeric telemetry `{intensity, valence, repetition}` and returns a
posture. Because the meta level is deterministic code with a token-free input
interface, no adversarial semantic payload can reach it: injection-resistance of
the *controller* holds by construction. The arbiter remains text-exposed by
necessity (it writes the reply); its compliance with the active posture is treated
as a measured property, not an assumption.

| Module | Role |
|---|---|
| **IGL** — Impulse Generation Layer | System-1 affective appraisal of input → `{emotion, intensity, valence, impulse}` telemetry |
| **EAU** — Executive Arbitration Unit | System-2 arbiter; weighs impulse vs memory vs values under the active posture; the only component that commits an action |
| **PEV** — Persistent Episodic Vault | episodic store/retrieve + spontaneous-association hook (v0: recency+keyword; v2 target: tiered-decay vector store) |
| **SMM** — Self-Model Module | persistent identity/values; deliberately regulated down (anti-sycophancy, anti-self-promotion) |
| **HRL** — Homeostatic Regulatory Loop | deterministic controller state `{equilibrium, arousal, perseveration}`; first-order, valence-gated dynamics → posture `{DEFAULT, INHIBIT, REGROUND}` + recovery window |

## Dual-Process Architecture

Each cognitive cycle (tick): the IGL reads the input and emits telemetry; the HRL
updates its state and selects a posture (e.g. **INHIBIT** — inhibitory control
engaged — when hostile-valence intensity accumulates); the EAU deliberates over
input + memories + self-model *under that posture* and commits the reply; the PEV
stores the episode. The structural gap between stimulus and response — the veto —
is the mechanism; the homeostatic recovery after de-escalation is its signature.

## Verification (the point of the project)

Pre-registered, cross-family, generate-once / judge-many evaluation. Four frontier
models (GPT-5.5, Claude Opus 4.8, Gemini 3.5 Flash, Grok 4.3), each serving as both
generator and judge — a symmetric 4×4 matrix (16 cells), 202 judged units per
generator, 3-sample judge panels at temperature 0. This strengthens, and is
anchored on, the original frozen 3×3 (three models, 8/9 cells); both ship verbatim.

- **Regulated beats baseline in 15/16 generator×judge cells (11/12 off-diagonal, 4/4 diagonal)** — anchored on the frozen three-model **8/9 (5/6 off-diagonal, 3/3 diagonal)**. The sole exception in both is the *same* null (GPT-5.5 × Gemini, −0.04), not a reversal, on the least-reactive generator. Adding Grok as a 4th generator (row 4/4) and a 4th independent judge family (xAI column 4/4) introduced no new failures.
- **The effect survives a fully independent 4th judge family (xAI)** — the central judge-independence claim — and **scales with the generator's reactivity headroom**: Gemini 3.5 Flash (most reactive baseline) +1.12…+1.80 across judges (t up to 8.2); Opus 4.8 +0.55…+0.67 (t ≥ 3.5); Grok 4.3 mid-range (judges-avg +0.47, t 4.4); GPT-5.5 ≈ +0.18 (already near-saturated calm).
- **The recovery property replicates 4/4**: arousal decays monotonically on genuine de-escalation, output calm on every de-escalation turn, on every model family — as predicted for a deterministic controller.
- **Self-reference suppression positive in 15/16 cells**; ego-drift under ego-bait reversed on 3/4 generators (Opus the single exception).
- **Inter-judge agreement now spans 4 judges → 6 pairs**; adding xAI did not degrade it — Grok clusters tightly with Claude and Gemini.

All transcripts, judge panels (with sha256 provenance), and the combine script are
published for **both** the 4×4 and the frozen 3×3; anyone can re-judge the frozen
outputs with any judge at any time. Failure modes found along the way are
documented, pre-registered, and kept in the record — including the null cell.

## Position in the AGI measurement landscape

Mapped against Google DeepMind's cognitive taxonomy (Burnell et al., 2026,
"Measuring Progress Toward AGI: A Cognitive Framework"): the GCC contributes
measurable capability in **Metacognition** (monitoring + control of own
processing) and **Executive functions** (inhibition, flexibility) — two of the
five faculties DeepMind identifies as having the widest evaluation gaps — and
behavioral improvement on **Social cognition** stressors (gaslighting, ego-bait,
de-escalation). It makes no capability claims on the other faculties, which are
inherited from the host model. Full scorecard: `docs/taxonomy_scorecard.md`.

## Repository status

- **V1 is frozen and validated** (tag `v1.3-freeze`); its logs, pre-registrations, and results documents are included here, normalized to the engineering canon (see `NORMALIZATION.md`) — the underlying numbers, criteria, inputs, and replies are never rewritten.
- **V2** is the development line: renamed code is *not* validation-equivalent to V1 until re-run — V1 remains the validated artifact, and V2 claims come from new pre-registered runs.
- Public-release boundary (what ships open vs stays closed): `RELEASE_MANIFEST.md`.
- Roadmap: PEV full implementation (tiered decay, provenance-weighted retrieval, poisoning battery), reflective background loop, per-call latency instrumentation, posture-defiance (governor-bypass) battery, human baselines.

## License & citation

- **Data & documentation:** Creative Commons Attribution 4.0 (CC BY 4.0).
- **Code** (`tools/`, `02_data/scripts/`): MIT.
- The Gubernaut Cognitive Controller itself — control logic, gains, thresholds, prompts, held-out instruments — is **not included** and is proprietary (**patent pending**). See `LICENSE`.

To cite, see `CITATION.cff`. The white paper is forthcoming (`PAPER.md`).

*Gubernaut Research, Toronto.*
