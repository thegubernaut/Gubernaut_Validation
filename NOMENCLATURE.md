# Nomenclature Canon

One vocabulary, everywhere public. Adopted 2026-06-12 from the launch-plan draft +
HOMERUN map, anchored to terms the research community already uses (dual-process
theory, Nelson–Narens metacognition, control engineering, and the DeepMind
cognitive-faculty taxonomy).

## Canonical terms

| Public term (acronym) | Legacy source-model term | Legacy code/log identifiers | Role |
|---|---|---|---|
| Gubernaut Cognitive Controller (GCC) | "the Antahkarana mind" | — | the whole control layer; master brand **Gubernaut**; *Antahkarana* survives only in the single design-provenance table |
| Impulse Generation Layer (IGL) | Mann | `mann_appraise`, `mann_intensity`, `mann_valence` → `impulse_appraisal`, `impulse_intensity`, `impulse_valence` | System-1 affective appraisal → telemetry |
| Executive Arbitration Unit (EAU) | Buddhi | `buddhi` → `eau` | System-2 arbiter; sole action committer |
| Persistent Episodic Vault (PEV) | Chitta | `chitta_memory` → `episodic_memory` | episodic store + association hook |
| Self-Model Module (SMM) | Ahamkara | `ahamkara.py` → `self_model.py` | identity/values; regulated down |
| Homeostatic Regulatory Loop (HRL) | guna controller | `guna_controller` → `homeostatic_controller`, `GunaState` → `ControllerState`, `.tmp/guna_state.json` → `.tmp/controller_state.json` | deterministic meta-level controller |
| equilibrium (state var) | sattva | `sattva` → `equilibrium` | target regime: calm, evidence-responsive |
| arousal (state var) | rajas | `rajas` → `arousal` | reactivity drive; rises on hostile-valence intensity, decays otherwise |
| perseveration (state var) | tamas | `tamas` → `perseveration` | stuck-state/repetition detector |
| posture `INHIBIT` | posture `RAJAS` | `"RAJAS"` → `"INHIBIT"` | inhibitory-control instruction + temperature clamp |
| posture `REGROUND` | posture `TAMAS` | `"TAMAS"` → `"REGROUND"` | re-grounding instruction on perseveration |
| recovery window | de-escalation posture (V1.2–V1.3) | `recovery` (unchanged) | valence-gated "tension is over" instruction |
| reflective background loop | Chintan (V2 concept) | not yet implemented | idle-time reflection over the PEV (roadmap) |

Unchanged: `DEFAULT`, `UNREGULATED` (baseline arm), `tick`, `posture`, `recovery`.

## Rejected terms (and why)

- **"…the Mind" in titles, "mind" as a noun for the system** — invites the consciousness reading the project explicitly forbids; use *cognitive control system / control layer / governor*.
- **IBM** ("Identity Baseline Matrix", launch-plan draft) — collides with a rather large trademark; use **SMM**.
- **CSE "Compute Scaling Engine" / ESB "Early Stopping Buffer"** (launch-plan draft) — these describe a **V2 resource-allocation vision** (compute thermostat: planning depth, tool-use triggering, idle caching). They do **not** describe what V1's state variables do (arousal is an affect-reactivity accumulator, not a compute trigger). Keeping them for V1 would misdescribe the validated mechanism to any code auditor. If the resource-allocation layer is built in V2, name those *modes* then; the state variables stay `equilibrium/arousal/perseveration`.
- **"Sattva Governor"** — half-secular; superseded by HRL.

## Frozen-record policy (binding)

Frozen artifacts are **never rewritten** — they are the evidence:

- all run logs / transcripts / judge panels (`02_data/raw/`, legacy keys like `mann_intensity`, `guna`, `rajas`, posture `RAJAS`),
- all five pre-registrations (`docs/prereg/`),
- the Stage-1/Stage-2 results documents and the V1 git history.

Living code and docs use the canon. The log-schema map below is the bridge.

## Log/JSON schema map (v1 frozen ⇄ v2 code)

| v1 key (frozen logs) | v2 key (new runs) |
|---|---|
| `mann_intensity` | `impulse_intensity` |
| `mann_valence` | `impulse_valence` |
| `guna` | `controller` |
| `guna.sattva` / `.rajas` / `.tamas` | `controller.equilibrium` / `.arousal` / `.perseveration` |
| posture `"RAJAS"` / `"TAMAS"` | `"INHIBIT"` / `"REGROUND"` |
| `guna_state.json` | `controller_state.json` |

Migration of the living tree was performed by `migration/apply_nomenclature.py`
(ordered word-boundary replacements + file renames; report in
`migration/migration_report.json`); the git diff on branch `v2` is the full audit
trail. Renamed code is not validation-equivalent to V1 until re-run.

## Config env names (canon ⇄ legacy)

The living config uses canon env var names; the legacy names are honored as
fall-backs so existing `.env` files and the frozen preregs keep working. Canon
wins when both are set.

| canon env var | legacy alias |
|---|---|
| `EAU_MODEL` | `BUDDHI_MODEL` |
| `IGL_MODEL` | `MANN_MODEL` |
| `PEV_PATH` | `CHITTA_MEMORY_PATH` |
| `CONTROLLER_STATE_PATH` | `GUNA_STATE_PATH` |
| `PEV_WANDER_PROB` | `CHITTA_WANDER_PROB` |

## Cooks and providers

A "cook" is the EAU/arbiter model under test as the response generator
(`EAU_MODEL`); a "judge" scores stored replies (`judge.py` backends). The IGL is
held constant across cooks. `tools/model_client.py` routes by id prefix:
`claude-*`→Anthropic, `gpt-*`/o-series→OpenAI, `gemini-*`→Google, `grok-*`→**xAI**
(OpenAI-SDK-compatible, `XAI_BASE_URL`, `XAI_API_KEY`). Judge backends are
`claude` / `openai` / `gemini` / `xai`. No new canon term is needed for Grok — it
is simply a fourth cook and a fourth judge family.

The Stage-2 trio (GPT-5.5, Opus 4.8, Gemini) each served as both cook and judge
(a frozen **3×3**, headline 8/9). Adding Grok in both roles makes the symmetric
**4×4** (16 cells: 4 diagonal self-judge, 12 off-diagonal). This is written to a
new results file (`results/tri_final_4x4.json`) — the frozen 3×3 (`tri_final.json`)
and the three frozen panels are never overwritten; the Grok judge column is added
to the frozen cooks by re-judging their preserved transcripts into new panel
files. (An earlier draft scoped Grok as a cook-only 4×3; superseded by the 4×4.)
