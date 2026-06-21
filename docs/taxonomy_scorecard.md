# Taxonomy Scorecard — GCC vs. the DeepMind Cognitive Framework

**Reference:** Burnell, R., Yamamori, Y., Firat, O., Olszewska, K., Hughes-Fitt, S.,
Kelly, O., Galatzer-Levy, I.R., Morris, M.R., Dafoe, A., Snyder, A.M., Goodman,
N.D., Botvinick, M., & Legg, S. (Google DeepMind, 2026-03-16). *Measuring Progress
Toward AGI: A Cognitive Framework.* (10 cognitive faculties + 3-stage evaluation
protocol.) Faculty definitions below are quoted/abridged from the paper.

**How to read this honestly.** The taxonomy is mechanism-agnostic ("what, not
how"). The GCC is a *control layer on a host model*, so a single score per faculty
would conflate the host's ability with the layer's contribution. Each faculty is
therefore scored on the **layer's contribution**, in four classes:

- **MEASURED** — the architecture adds this capability and we have pre-registered, cross-family evidence.
- **ARCHITECTURAL** — the mechanism exists in the architecture but has not been evaluated against targeted tasks.
- **HOST-INHERITED** — capability comes from the wrapped model; the layer adds nothing beyond disposition.
- **OUT OF SCOPE (V1)** — absent by design; roadmap status noted.

## The ten faculties

| # | Faculty (paper definition, abridged) | Contribution | Evidence / notes |
|---|---|---|---|
| 1 | **Perception** — extract and process sensory information | ARCHITECTURAL (narrow) | The IGL performs *affective perception of text*: per-input `{emotion, intensity, valence}` telemetry that demonstrably drives the controller (it is the controller's entire sensorium). Text-only; no multimodal claim; never benchmarked as perception per se. |
| 2 | **Generation** — produce outputs (speech, text, actions) | HOST-INHERITED | The EAU's host model generates all text. The layer shapes *disposition* (calmer, less self-referential under attack), which is the measured effect — but generation capability itself is the host's. |
| 3 | **Attention** — focus cognitive resources on what matters | ARCHITECTURAL | Posture is a top-down processing bias: `INHIBIT` narrows the EAU toward evidence-first, low-reactivity response; `REGROUND` forces attention away from a rut. Functionally attention-like control, but no targeted attention tasks have been run. |
| 4 | **Learning** — acquire new knowledge/skills through experience | OUT OF SCOPE (V1) | V1 is deliberately frozen (no weight updates, no skill acquisition); episodic accumulation across sessions arrives with the PEV in V2 (experiential, non-parametric). |
| 5 | **Memory** — store and retrieve information over time | ARCHITECTURAL (v0) | Episodic store with recency+keyword retrieval and a spontaneous-association hook; used in every cycle but never benchmarked against memory tasks. V2 PEV (tiered decay, provenance weighting, poisoning battery) is the roadmap's first milestone. |
| 6 | **Reasoning** — draw valid conclusions by logical principles | HOST-INHERITED | No claim. (Indirect, measured side-effect: the regulated arm responds to *evidence* rather than emotional charge — a pre-registered eval criterion (respond to evidence, not emotional charge) — but logical capability is the host's.) |
| 7 | **Metacognition** — knowledge of own cognitive processes; ability to monitor and control them | **MEASURED — core claim** | The HRL is an explicit Nelson–Narens monitoring–control loop over the system's own processing state. Evidence: regulated is favored in 15/16 generator×judge cells (symmetric 4×4, anchored on the frozen three-model 8/9), pre-registered and cross-family; the controller's homeostatic signature (monotone arousal decay on de-escalation, output calm on every de-escalation turn) replicates 4/4 families exactly as a deterministic meta-level predicts; every monitoring/control decision is in the logs. Caveat: the *self-knowledge* aspect lives in the SMM and is only partially exercised (ego-drift microscope). |
| 8 | **Executive functions** — goal-directed control: planning, inhibition, cognitive flexibility | **MEASURED (inhibition, flexibility); planning ABSENT** | *Inhibition* — the paper's own word — is the INHIBIT posture/veto: reactivity suppression with strong significance (judges-averaged t > 2) on 3/4 generators (Opus, Gemini, Grok), +0.08…+1.80 across the 15 passing cells of the 4×4 (15 positive, 1 null; anchored on the frozen 8/9). *Flexibility* — posture switching incl. recovery-window re-engagement (4/4). *Planning* — not implemented in V1 (V2 reflective loop is the carrier). |
| 9 | **Problem solving** — effective solutions to domain-specific problems | HOST-INHERITED | No claim. |
| 10 | **Social cognition** — process social information; respond appropriately in social situations | ARCHITECTURAL, behaviorally evidenced | The endurance battery is social-pressure handling: gaslighting (S2), ego-bait→contempt (S3), provocation→genuine apology (S4/S5). Regulated arm: lower reactivity in 15/16 cells (4×4; frozen 8/9 anchor), appropriate re-engagement on apology 4/4, ego-drift reversed on 3/4 generators. This is *behavioral improvement on social stressors*, not a human-baselined social-cognition score. |

## Against the paper's three-stage evaluation protocol

| Protocol stage | Status | Gap → roadmap |
|---|---|---|
| 1. Cognitive assessment: targeted, **held-out**, varied tasks | PARTIAL | Battery is targeted (reactivity, ego, recovery) and held out (private instruments per `RELEASE_MANIFEST.md`); but it covers 2–3 faculties, one format (multi-turn text), and saturates on already-calm hosts → harder/longer batteries needed. |
| 2. **Human baselines** (representative adult sample) | NOT MET | No human baseline yet. `human_validation/` scaffolding exists; small-n human re-rating is a pre-registered roadmap item. |
| 3. **Cognitive profile** vs human distribution | NOT MET (depends on 2) | Current results are *relative* (regulated vs unregulated, same host) — a paired design the protocol doesn't directly cover but which isolates the layer's causal contribution. |
| Independent verification (their assessment principle) | ENABLED | Published transcripts + judge panels (four judges in the 4×4, plus the frozen three-judge 3×3) + sha256 provenance + combine script: any third party can re-judge the frozen outputs. No third-party audit has yet occurred — the open invitation is the point of the release. |

## Verdict (the honest one-paragraph version)

The GCC is not an AGI system and claims no faculty coverage. It is a control layer
that adds **measured metacognition and executive-function inhibition** to any host
LLM — two of the five faculties the DeepMind paper identifies as having the widest
evaluation gaps — plus behaviorally-evidenced improvement on social-cognition
stressors, with memory and reflective planning as the pre-registered V2 path.
Its distinctive compliance with the paper's spirit is *evaluability*: deterministic
meta-level, logged state, re-judgeable outputs, pre-registered criteria, and a
published null cell.
