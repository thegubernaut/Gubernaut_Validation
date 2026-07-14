# Recompute & verify this release

Every published number is derived from the shipped judge panels by a small,
dependency-free script (Python stdlib only). You can reproduce it yourself.

## 1. Rebuild the 4x4 matrix from the shipped panels
From the repository root:

    python tools/tri_combine.py \
      --panel "GPT:openai:02_data/raw/panel_tri_cookGPT_4judge.json" \
      --panel "Opus:claude:02_data/raw/panel_tri_cookOpus_4judge.json" \
      --panel "Gemini:gemini:02_data/raw/panel_tri_cookGemini_4judge.json" \
      --panel "Grok:xai:02_data/raw/panel_tri_cookGrok.json" \
      --out /tmp/my_4x4.json

Expected: "15/16 cells pass (11/12 off-diagonal, 4/4 diagonal)", sole failure
GPTxgemini. The output matches the shipped 02_data/raw/tri_final_4x4.json.
(Frozen 3x3: the same command with the three original panels reproduces
02_data/raw/tri_final.json -> 8/9.)

## 2. Re-judge with your own judge (generate-once / judge-many)
The transcripts (02_data/raw/endurance_*.json, 02_data/raw/eval_*.json) carry
every user input and model reply. Score them with ANY judge and rebuild the
panels: the result is independent of our judge family. That independence is the
whole point of the 4x4 (four judge families; the effect survives all of them).

## 3. Verify file integrity

    sha256sum -c SHA256SUMS        # from the repository root

## 4. Regenerate the telemetry series and dampening tables

    cd 02_data/scripts && python extract_series_4x4.py

Rebuilds `02_data/tables/series_endurance_long_4x4.csv` and
`dampening_summary_4x4.csv` from the published transcripts + panels. Verified at
release time: the regenerated files are **byte-identical** to the shipped ones,
i.e. the documented transcript redaction removed appended analysis only, never
telemetry or evidence.

## 5. Verify every figure value against the shipped record

    cd figures && python verify_figure_numbers.py

Asserts every value plotted in the paper's figures against `tri_final_4x4.json`,
`tri_final.json`, `master_table_4x4.csv`, and the series CSV. Expected: **ALL PASS**
(20 checks). Regenerate the figures themselves with:

    cd figures && python make_paper_figures.py all     # -> figures/out/A_whitepaper

Needs `matplotlib`, `numpy` (requirements.txt).

The figures are printed in the paper, so this release ships the *scripts that
produce them*, not the renders. The IBM Plex font binaries are likewise not
redistributed: without them matplotlib falls back to DejaVu and the typography
differs, while **every plotted value is identical** — which is what the harness
above checks. Set `PV_FONTS` to a directory of IBM Plex `.ttf` files to reproduce
the paper's exact typography.

## 6. Recompute the paper's §6.6 statistics sentences

    cd 02_data/scripts && python stats_checks.py

Reconstructs the 17 per-item paired differences per cell from the shipped judge
panels, hard-validates them against the shipped cell summaries, then prints the
Bonferroni (11/16 survive; marginals GPT×Opus and Grok×Grok) and Wilcoxon
signed-rank (agrees with the paired t in 15/16 cells) results quoted in §6.6.
Expected: ALL VALIDATIONS PASS. Needs `scipy`.

## Note on transcript provenance
Per REDACTIONS.md, one withheld calibration constant was stripped from the public
endurance transcripts, so their sha256 differs from the value recorded inside the
panels' "sources" field. All inputs, replies, telemetry, panels, and combined
matrices are otherwise intact; SHA256SUMS covers the published files as shipped.
(The project's two internal-record verifiers, `verify_against_sealed*.py`, assert
those pre-redaction hashes and therefore run only against the internal sealed
record; the public equivalents are steps 1–6 above.)
