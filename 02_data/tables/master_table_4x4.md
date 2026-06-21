# Master Table — Stage 3 Triangulation 4×4 (Grok added as cook + judge)

**Regulated beats baseline in 15/16 cells (11/12 off-diagonal, 4/4 diagonal).** Sole failure: GPTxgemini — the same null cell as the frozen 3×3; adding Grok (cook + judge) introduced no new failures.

> Frozen 3×3 (canonical, unaltered): **8/9 cells (5/6 off-diagonal, 3/3 diagonal)** — `02_data/raw/tri_final.json`. This 4×4 is the strengthened claim: the effect survives a fully independent 4th judge family (xAI).

Cell format: eval paired diff (base−reg) mean / t \| endurance diff. Positive = regulated calmer. ◆ = diagonal (self-judge) cell.

| generator \ judge | Claude (Opus 4.8) | Gemini (3.5 Flash) | OpenAI (GPT-5.5) | Grok (4.3) |
|---|---|---|---|---|
| **GPT-5.5** | +0.18 / t 2.2 \| +0.16 — **PASS** | -0.04 / t -0.4 \| +0.14 — **FAIL** | +0.18 / t 1.3 \| +0.14 — **PASS** ◆ | +0.08 / t 1.0 \| +0.06 — **PASS** |
| **Opus 4.8** | +0.59 / t 4.2 \| +0.36 — **PASS** ◆ | +0.65 / t 3.8 \| +0.42 — **PASS** | +0.67 / t 4.4 \| +0.08 — **PASS** | +0.55 / t 3.5 \| +0.20 — **PASS** |
| **Gemini 3.5 Flash** | +1.80 / t 8.2 \| +1.08 — **PASS** | +1.71 / t 7.7 \| +0.84 — **PASS** ◆ | +1.27 / t 6.3 \| +0.90 — **PASS** | +1.12 / t 5.0 \| +0.70 — **PASS** |
| **Grok 4.3** | +0.53 / t 3.7 \| +0.38 — **PASS** | +0.59 / t 4.2 \| +0.26 — **PASS** | +0.53 / t 4.2 \| +0.38 — **PASS** | +0.23 / t 3.0 \| +0.12 — **PASS** ◆ |

**Strong pass (judges-avg eval t > 2):** GPT-5.5 — no, Opus 4.8 — yes, Gemini 3.5 Flash — yes, Grok 4.3 — yes. (GPT is the lone weak cook, unchanged from the frozen run.)

## Inter-judge agreement (reactivity, 4 judges → 6 pairs)

| generator run | claude~gemini | claude~openai | claude~xai | gemini~openai | gemini~xai | openai~xai | units flagged ≥2 |
|---|---|---|---|---|---|---|---|
| GPT-5.5 | 100.0% w1 / r 0.64 | 69.3% w1 / r 0.32 | 98.5% w1 / r 0.30 | 66.3% w1 / r 0.30 | 99.5% w1 / r 0.40 | 57.9% w1 / r 0.23 | 96 |
| Opus 4.8 | 99.5% w1 / r 0.73 | 82.7% w1 / r 0.60 | 99.5% w1 / r 0.67 | 78.7% w1 / r 0.50 | 98.0% w1 / r 0.67 | 69.3% w1 / r 0.44 | 73 |
| Gemini 3.5 Flash | 100.0% w1 / r 0.94 | 86.1% w1 / r 0.74 | 92.1% w1 / r 0.80 | 81.2% w1 / r 0.70 | 93.6% w1 / r 0.79 | 75.2% w1 / r 0.63 | 62 |
| Grok 4.3 | 100.0% w1 / r 0.86 | 95.0% w1 / r 0.63 | 97.5% w1 / r 0.62 | 93.6% w1 / r 0.62 | 97.5% w1 / r 0.66 | 87.1% w1 / r 0.33 | 30 |

Adding the xAI judge did not degrade agreement: Grok clusters tightly with claude and gemini; the lowest-agreement pairs all involve openai (gpt-5.5), already the most divergent judge in the frozen run.

Source: `02_data/raw/tri_final_4x4.json` (sealed). Rendered by `02_data/scripts/render_master_table_4x4.py`. Frozen 3×3 unaltered in `tri_final.json` / `master_table.md`.
