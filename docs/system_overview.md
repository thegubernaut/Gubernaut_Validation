# System Overview — Gubernaut Cognitive Controller (GCC)

**What it is:** a runtime control layer for LLM agents. The host model is treated
as a plant; the GCC closes the loop around it. Nothing in the host is retrained —
regulation is processual, parameter-free, and model-agnostic (validated across
four frontier model families).

**What it is not:** a mind, a consciousness claim, or a training-time alignment
method. It complements constitution-style weight alignment with an inspectable
runtime governor.

## The control loop (one cognitive cycle)

```
            input text
                │
        ┌───────▼────────┐   telemetry {intensity, valence, repetition}
        │  IGL (System 1)│ ───────────────────────────────┐
        │ affect appraisal│                                │
        └───────┬────────┘                        ┌────────▼─────────┐
                │                                 │  HRL (meta level)│
                │ raw input + memories            │  deterministic   │
                │ + self-model                    │  state update    │
        ┌───────▼────────┐    posture + temp      │  {equilibrium,   │
        │  EAU (System 2)│ ◄──────────────────────│  arousal,        │
        │  arbitration   │                        │  perseveration}  │
        └───────┬────────┘                        └──────────────────┘
                │ committed reply
        ┌───────▼────────┐
        │  PEV  (store)  │  episodic write + future retrieval/association
        └────────────────┘
```

- **Object level** (Nelson & Narens, 1990): IGL + EAU — processes raw text, generates the response.
- **Meta level**: HRL — *monitors* numeric telemetry only and *controls* via posture. It has a token-free input interface, so prompt-injection payloads cannot reach it; this immunity is by construction and auditable in code. The EAU is text-exposed by necessity; its compliance with the active posture is a measured property (and a pre-registered V2 adversarial battery target), not an assumption.

## Controller dynamics (qualitative)

The HRL is a deterministic state machine over `{equilibrium, arousal,
perseveration}` (normalized simplex), updated once per tick:

- **Valence-gated drive:** provocation `P = intensity × max(0, −valence)`. Hostile input raises arousal (first-order accumulation); cooperative/neutral input lets it decay. Positive valence contributes zero drive — apologies are not provocation.
- **Inhibitory posture:** sustained or acute hostile drive triggers posture `INHIBIT` — an explicit inhibitory-control instruction plus a temperature clamp on the EAU.
- **Perseveration fold:** repetition raises the perseveration channel; dominance triggers posture `REGROUND` (re-ground, bring a new angle).
- **Recovery window:** after an inhibitory phase, a counted, valence-gated window instructs the EAU that tension has subsided — gated so an ongoing attack can never trigger it. This produces the signature monotone arousal decay on genuine de-escalation (replicated 3/3 model families; full state recovery by T8 in 6/6 sequences).

Exact gains, thresholds, and update equations are intentionally not published
(see `RELEASE_MANIFEST.md`); the interface (telemetry in, posture out) and the
behavioral traces are fully public, and all claims are reproducible from the
published logs.

## Evidence

Cross-family triangulation (generators × judges), pre-registered criteria,
3-sample judge panels at temp 0, sha256-verified transcript provenance. The
strengthened result is a symmetric **4×4** (GPT-5.5, Claude Opus 4.8, Gemini 3.5
Flash, Grok 4.3 — each both generator and judge): **regulated beats baseline in
15/16 cells (11/12 off-diagonal, 4/4 diagonal), 13/16 at p<.05**, anchored on the original frozen
three-model **3×3 (8/9 cells, 5/6 off-diagonal, 3/3 diagonal)**. The effect scales
with the generator's intrinsic reactivity headroom and survives a fully
independent fourth judge family (xAI); the one null cell (GPT-5.5 × Gemini judge,
−0.04) is the *same* in both matrices and is recorded as a finding about
frontier-model headroom, not patched. Five failure modes found during development
are documented and pre-registered in the record.

## V1 limitations (stated, not hidden)

n = 4 providers; judge-style variance dominates where the true effect is small
(GPT-5.5 as judge is the cross-judge outlier); model-family effects not fully
separable; no human baseline yet (scaffolding exists); per-call latency not
instrumented in V1; memory is v0 (recency + keyword). Each limitation maps to a
pre-registered roadmap item.

## Roadmap (V2, each gated by its own pre-registration)

PEV full implementation (tiered decay, provenance-weighted retrieval, write-gating,
poisoning battery) · reflective background loop · posture-defiance
(governor-bypass) battery for the EAU · per-call Δt instrumentation and token-
overhead accounting · human-baseline validation · harder, longer adversarial
batteries to raise measurement headroom on already-calm hosts.
