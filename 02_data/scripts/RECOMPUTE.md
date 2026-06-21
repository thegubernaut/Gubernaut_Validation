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

## Note on transcript provenance
Per REDACTIONS.md, one withheld calibration constant was stripped from the public
endurance transcripts, so their sha256 differs from the value recorded inside the
panels' "sources" field. All inputs, replies, telemetry, panels, and combined
matrices are otherwise intact; SHA256SUMS covers the published files as shipped.
