#!/usr/bin/env python3
"""A set — white-paper print figures (Draft-9 slots). Renders into ../A_whitepaper.
Usage: python make_paper_figures.py [architecture|matrix|recovery|forest|bars|radial|summary|all]"""
import os, sys
from pathlib import Path
import fig_architecture, fig_matrix, fig_recovery, fig_batch

OUT = os.environ.get("FIGOUT", str(Path(__file__).resolve().parents[1] / "A_whitepaper"))
JOBS = {"architecture": lambda: fig_architecture.main(OUT),
        "matrix":       lambda: fig_matrix.main(OUT, mode="paper"),
        "recovery":     lambda: fig_recovery.main(OUT, mode="paper"),
        "forest":       lambda: fig_batch.forest(OUT),
        "bars":         lambda: fig_batch.bars(OUT, mode="paper"),
        "radial":       lambda: fig_batch.radial(OUT),
        "summary":      lambda: fig_batch.summary(OUT)}
which = sys.argv[1] if len(sys.argv) > 1 else "all"
for name, job in JOBS.items():
    if which in ("all", name): job()
print("A set ->", OUT)
