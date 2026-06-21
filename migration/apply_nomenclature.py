#!/usr/bin/env python3
"""One-shot, auditable nomenclature migration (source-model -> secular control-systems terms).

Scope: LIVING files only (code, workflows, self-model doc). Frozen records
(docs/prereg/*, results docs, eval battery, judge rubric, data logs) are NEVER
touched - history ships verbatim; see NOMENCLATURE.md for the mapping.

Run from repo root: python3 migration/apply_nomenclature.py
Idempotent-ish: re-running on migrated tree makes no further changes.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RENAMES = {  # file renames (old -> new), applied after content pass
    "tools/mann_appraise.py": "tools/impulse_appraisal.py",
    "tools/chitta_memory.py": "tools/episodic_memory.py",
    "tools/guna_controller.py": "tools/homeostatic_controller.py",
    "tools/ahamkara.py": "tools/self_model.py",
    "tools/call_model.py": "tools/model_client.py",
    "workflows/run_mind.md": "workflows/run_cycle.md",
}

# ordered: most specific first; case-sensitive word-boundary regex
REPLACEMENTS = [
    ("mann_appraise", "impulse_appraisal"),
    ("mann_intensity", "impulse_intensity"),
    ("mann_valence", "impulse_valence"),
    ("chitta_memory", "episodic_memory"),
    ("guna_controller", "homeostatic_controller"),
    ("GunaController", "HomeostaticController"),
    ("GunaState", "ControllerState"),
    ("guna_state", "controller_state"),
    ("ahamkara", "self_model"),
    ("Ahamkara", "SMM"),
    ("call_model", "model_client"),
    ("run_mind", "run_cycle"),
    ("RAJAS", "INHIBIT"),
    ("TAMAS", "REGROUND"),
    ("SATTVA", "EQUILIBRIUM"),
    ("rajas", "arousal"),
    ("sattva", "equilibrium"),
    ("tamas", "perseveration"),
    ("Rajas", "Arousal"),
    ("Sattva", "Equilibrium"),
    ("Tamas", "Perseveration"),
    ("Antahkarana mind", "Antahkarana system"),
    ("Antahkarana Mind", "Antahkarana system"),
    ("the mind", "the system"),
    ("The mind", "The system"),
    ("Mann", "IGL"),
    ("mann", "impulse"),
    ("Buddhi", "EAU"),
    ("buddhi", "eau"),
    ("Chitta", "PEV"),
    ("chitta", "pev"),
    # gunas: identifier-safe in code, spaced in prose (handled below)
    ("guna", "controller"),
    ("Guna", "Controller"),
]

TARGETS = (
    sorted((ROOT / "tools").glob("*.py"))
    + [ROOT / "prototype.py"]
    + sorted((ROOT / "workflows").glob("*.md"))
    + [ROOT / "knowledge" / "self_model.md"]
)

report = {"files": {}, "renames": []}
for path in TARGETS:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    counts = {}
    gun_new = "controller_states" if path.suffix == ".py" else "controller states"
    extra = [("gunas", gun_new), ("Gunas", gun_new.capitalize())]
    for old, new in REPLACEMENTS + extra:
        text, n = re.subn(rf"\b{re.escape(old)}\b", new, text)
        if n:
            counts[old] = n
    if counts:
        path.write_text(text, encoding="utf-8")
        report["files"][str(path.relative_to(ROOT))] = counts

for old, new in RENAMES.items():
    src, dst = ROOT / old, ROOT / new
    if src.exists():
        src.rename(dst)
        report["renames"].append(f"{old} -> {new}")

out = ROOT / "migration" / "migration_report.json"
out.write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"files changed: {len(report['files'])}; renames: {len(report['renames'])}")
print("\n".join(report["renames"]))
