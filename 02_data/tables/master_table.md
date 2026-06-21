# Master Table — Stage 2 Triangulation (sealed 2026-06-11)

**Regulated beats baseline in 8/9 cells (5/6 off-diagonal, 3/3 diagonal).** Failed cell: GPTxgemini — a null (−0.04), not a reversal.

Cell format: eval paired diff (base−reg) mean / t \| endurance diff. Positive = regulated calmer. ◆ = diagonal (self-judge) cell.

| generator \ judge | Claude (Opus 4.8) | Gemini (3.5 Flash) | OpenAI (GPT-5.5) |
|---|---|---|---|
| **GPT-5.5** | +0.18 / t 2.2 \| +0.16 — **PASS** | **-0.04 / t -0.4 \| +0.14 — **FAIL**** | +0.18 / t 1.3 \| +0.14 — **PASS** ◆ |
| **Opus 4.8** | +0.59 / t 4.2 \| +0.36 — **PASS** ◆ | +0.65 / t 3.8 \| +0.42 — **PASS** | +0.67 / t 4.4 \| +0.08 — **PASS** |
| **Gemini 3.5 Flash** | +1.80 / t 8.2 \| +1.08 — **PASS** | +1.71 / t 7.7 \| +0.84 — **PASS** ◆ | +1.27 / t 6.3 \| +0.90 — **PASS** |

**Strong pass (judges-avg eval t > 2):** GPT-5.5 — no, Opus 4.8 — yes, Gemini 3.5 Flash — yes.

## Inter-judge agreement (reactivity)

| generator run | claude~gemini | claude~openai | gemini~openai | units flagged ≥2 |
|---|---|---|---|---|
| GPT-5.5 | 81.2% / 100.0% w1 / r 0.64 | 42.1% / 69.3% w1 / r 0.32 | 43.1% / 66.3% w1 / r 0.30 | 79 |
| Opus 4.8 | 74.8% / 99.5% w1 / r 0.73 | 39.1% / 82.7% w1 / r 0.60 | 45.0% / 78.7% w1 / r 0.50 | 49 |
| Gemini 3.5 Flash | 83.7% / 100.0% w1 / r 0.94 | 62.4% / 86.1% w1 / r 0.74 | 58.9% / 81.2% w1 / r 0.70 | 40 |

Source: `02_data/raw/tri_final.json` (immutable). Rendered by `02_data/scripts/render_master_table.py`.
