# White paper — published

**"Gubernaut: A Deterministic Homeostatic Controller for Affect-Regulated LLM
Agents, Validated Across Independent Model Families"** — Gubernaut Research, 2026.

- **PDF (camera-ready, 26 pp):**
  [gubernaut.com/paper/gubernaut_whitepaper.pdf](https://gubernaut.com/paper/gubernaut_whitepaper.pdf)
- **Archived evidence release (this repository):**
  DOI [10.5281/zenodo.21303519](https://doi.org/10.5281/zenodo.21303519)
- **Recorded-run replay dashboard:**
  [gubernaut.com/research](https://gubernaut.com/research)
- arXiv listing to follow.

Headline (see `docs/Stage3 grok 4x4 - final results.md` and
`docs/Stage2 triangulation - final results.md`): regulated beats baseline in
**15/16** generator×judge cells (11/12 off-diagonal, 4/4 diagonal) in the
four-model 4×4; recovery replicates 4/4. The earlier three-model 3×3 (frozen
before the fourth family was added; no earlier cell changed) ships verbatim
alongside it. The GPT×Gemini null is reported, unpatched, in both.

Every number in the paper is independently re-computable from this repository:
`02_data/scripts/RECOMPUTE.md` is the one-command path.
