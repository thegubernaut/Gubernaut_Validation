# Changelog

What changed in this repository, release by release. The sealed record under `02_data/` does not
change between releases: `SHA256SUMS`, its OpenTimestamps proof and the Zenodo DOI cover it, and
every entry below leaves it byte for byte as sealed.

## Unreleased

- **The seal passes on a fresh clone, on every platform.** A `.gitattributes` file restores the
  line endings the sealed files were written with, so `sha256sum -c SHA256SUMS` (RECOMPUTE.md
  step 3) passes 84 of 84 on Linux and macOS, where it had passed 21. Step 4's regenerated tables
  now match the checkout byte for byte as well. No stored file changed.
- **The recompute chain runs on every push.** `.github/workflows/verify.yml` runs RECOMPUTE.md
  steps 1 and 3 to 6, read-only.
- **`requirements.txt` lists only what the published scripts import,** pinned to the versions the
  chain was verified with: numpy, scipy and matplotlib. The model-API clients it used to list are
  imported by no script in this repository. `.python-version` pins Python 3.12.

## v1.0.2 · 2026-07-14

Internal staging artifacts removed, the citation identity fixed, and the paper shipped with the
record.

## v1.0.1 · 2026-07-13

Publish-state polish of the documentation and figures.

## v1.0.0 · 2026-07-10

The public recompute chain completed: the figures, the telemetry series and the statistics are
reproducible from the release tree.
