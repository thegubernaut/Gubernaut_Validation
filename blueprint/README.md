# Architectural blueprint — the token-free boundary, runnable

This folder holds a minimal **reference skeleton** of the architecture the paper
evaluates: a deterministic controller that regulates an LLM's response posture
from a meta level that **no text token can reach**.

```
python governor_skeleton.py        # stdlib only, no dependencies, no API calls
```

The demo runs a scripted 10-turn provocation → de-escalation sequence and prints
the controller state per turn. You will see the homeostatic shape the paper
measures across four model families: arousal integrates under attack, the
recovery window opens on a genuine change of valence, and the state decays back
under the veto threshold once the pressure ends. The demo closes by throwing a
prompt-injection string directly at the controller, which is rejected **by
type, before any logic runs**.

## The one idea

```
             OBJECT LEVEL (reads text)          META LEVEL (numbers only)
  user text ──► appraise()  ──[intensity, valence]──►  HomeostaticLoop
                                                        │ state: {equilibrium,
                                                        │         arousal,
                                                        │         perseveration}
  reply     ◄── arbitrate() ◄──[posture, temp bound]────┘
```

- `appraise()` (IGL) is the only sensing component that reads raw text, and all
  it may emit is two numbers.
- `HomeostaticLoop` (HRL) is a numeric state vector plus fixed transition
  rules: an array-driven state machine. Its API accepts finite floats only and
  raises on anything else, so injection resistance of the **controller** is a
  property of the wiring, not of a filter.
- `arbitrate()` (EAU) is the one text-exposed gatekeeper that writes the reply
  under the active posture. In the evaluated system its posture compliance is a
  **measured property** (see the paper's evaluation), never an assumption.

## What this is not

- **Not the evaluated system.** Every constant is illustrative and deliberately
  different from the evaluated configuration. The appraiser here is a toy
  keyword heuristic; the evaluated system uses a model-based appraiser.
- **Not a reproduction path for the paper's numbers.** Those are recomputed
  from the sealed transcripts and judge panels by `../02_data/scripts/` and
  `../figures/` (see `../02_data/scripts/RECOMPUTE.md`).
- **Not a safety guarantee.** The claim demonstrated here is scoped and
  structural: text cannot reach the deciding layer. Nothing more.

No consciousness, sentience, or subjective experience is claimed or implied.
The system is a control layer: monitored state, regulated output.
