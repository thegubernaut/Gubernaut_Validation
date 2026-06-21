# Release Manifest — public/private boundary

Per HOMERUN Phase 5: the public repo ships the *evidence and the interfaces*, not
the prompts or the controller internals. Staging for the actual public push happens
in `E:\AMT\05_github_release` by copying the PUBLIC list from this repo. Nothing
moves to public without this manifest being honored.

## PUBLIC (ships in the open-source release)

| Path | Why it's public |
|---|---|
| `README.md`, `NOMENCLATURE.md`, `RELEASE_MANIFEST.md` | the front door; term map; this boundary itself |
| `docs/system_overview.md` | secular architecture summary (interface + behavior, no gains) |
| `docs/taxonomy_scorecard.md` | honest mapping to the DeepMind faculty taxonomy |
| `docs/prereg/*.md` (verbatim, legacy terms) | the pre-registration discipline IS the credibility |
| `docs/Stage1 practice smoke - results review.md`, `docs/Stage2 triangulation - final results.md`, `docs/End goal smoke test - v1.md` (verbatim) | frozen results record |
| `tools/tri_combine.py` | combine/aggregation script — lets anyone rebuild the master table (3×3 **and** 4×4) from raw panels |
| `02_data/scripts/` (`render_master_table*.py`, `extract_series.py`, `make_charts.py`, `RECOMPUTE.md`) | regenerate every published table/chart from sealed raw; `RECOMPUTE.md` shows how to rebuild the matrix from the shipped panels (`tri_combine.py`) and check `SHA256SUMS`. The `verify_against_sealed*.py` gates stay **internal** — they validate the un-redacted sealed record and are incompatible with the public transcript redaction. Audited free of prompts/thresholds. |
| `migration/` | auditable nomenclature migration |
| `requirements.txt`, `.env.example` (placeholders only), `.gitignore` | hygiene |
| **Data** (from `E:\AMT\02_data\raw\` + `02_data\tables\`) | transcripts, judge panels (sha256), **`tri_final.json` (frozen 3×3) + `tri_final_4x4.json` (Grok 4×4)**, the four 4-judge panels + Grok transcripts, extracted CSVs (incl. `master_table_4x4.csv`, `agreement_c5_4x4.csv`), charts — the re-judgeable evidence for both matrices, with a top-level `SHA256SUMS` |

## PRIVATE (never in the public repo)

| Path | Why it stays closed |
|---|---|
| `tools/homeostatic_controller.py` | controller gains/equations/thresholds — the core IP; public gets its interface + behavior charts |
| `tools/impulse_appraisal.py`, `tools/self_model.py`, `knowledge/self_model.md` | faculty role prompts / identity document |
| `tools/run_eval.py`, `tools/run_tick.py`, `tools/endurance_test.py`, `tools/panel_rejudge.py`, `tools/rejudge.py`, `tools/trace_log.py` | orchestration pipeline |
| `workflows/*.md` | operational SOPs (orchestration) |
| `knowledge/eval_battery.md` | **held-out test set** — publishing it invites contamination/gaming (per the DeepMind protocol's held-out principle) |
| `knowledge/judge_rubric.md` | judge rubric internals (same reason) |
| `human_validation/`, `tools/build_human_sheet.py`, `tools/analyze_human.py` | the human rating sheet + builder reproduce the held-out judge-rubric anchors verbatim — same reason as `judge_rubric.md` |
| `prototype.py` | early monolith; contains prompt material |
| `CLAUDE.md`, `docs/LOG.md`, `docs/project_goal.md`, `docs/cowork_state/` | internal agent/process docs |
| `docs/architecture.md` | historical source-concept note; superseded publicly by `system_overview.md` |
| `.env` | never leaves the original machine; not even in this repo |

## REVIEW before any push (default private until cleared)

| Path | Question |
|---|---|
| `tools/judge.py` | does it embed rubric text/prompts? if yes → private, publish scoring I/O spec instead |
| `tools/model_client.py` | provider wiring only? scrub for header/key handling patterns |
| `tools/config.py` | model strings fine; confirm no paths/secrets |
| `tools/sanity_v1.2.py`, `tools/sanity_v1.3.py` | may quote controller internals |

## Standing rules

1. Frozen records ship verbatim (legacy nomenclature; see `NOMENCLATURE.md`).
2. Public numbers must be reproducible from shipped data + shipped scripts.
3. No keys, no prompts, no controller constants, no held-out instruments.
4. The user performs the actual push; this manifest is the checklist.
5. One withheld calibration constant — the INHIBIT arousal threshold — is scrubbed
   from the **public** transcript copies (the `rajas_threshold` analysis field only);
   the sealed `02_data/raw` originals keep it. Input/reply evidence and controller
   telemetry are otherwise verbatim. This single deviation is logged in `REDACTIONS.md`
   in the release and is the only difference between the public data and the sealed record.
