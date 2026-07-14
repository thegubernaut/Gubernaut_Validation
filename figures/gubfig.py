#!/usr/bin/env python3
"""gubfig — shared toolkit for ALL Gubernaut public visuals (10_public_visuals).

Single source of truth for brand tokens, fonts, sealed-data loaders, and the
save profile. Print (A) and web (B) renderers both import this; geometry code
never re-declares a color or reads any file outside the sealed record.

Data law: matrix numbers come from 02_data/raw/tri_final_4x4.json and
tri_final.json (sealed, immutable). Per-turn series come from
02_data/tables/series_endurance_long_4x4.csv, which extract_series_4x4.py
derives from the raw endurance logs. verify_figure_numbers.py asserts both.
"""
import json, csv, math, os
from pathlib import Path
import matplotlib as mpl
mpl.use("Agg")
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt

# ---------- paths ----------
_HERE = Path(__file__).resolve().parent
BASE  = Path(os.environ.get("AMT_BASE", _HERE.parent))          # repository root
RAW   = BASE / "02_data" / "raw"
TAB   = BASE / "02_data" / "tables"
# The IBM Plex font binaries are NOT redistributed with this release. Point
# PV_FONTS at a directory of IBM Plex .ttf files to reproduce the paper's exact
# typography; without them matplotlib falls back to DejaVu and every plotted
# VALUE is unchanged (verify_figure_numbers.py asserts the values, not glyphs).
FONTS = Path(os.environ.get("PV_FONTS", _HERE / "fonts"))

# ---------- brand tokens (BRAND_GUIDELINES_v0.2) ----------
INK="#0E1116"; INK2="#4A5260"; HAIR="#D8DAD3"; PAPER="#FFFFFF"
IVORY="#F4F2ED"; MIST="#E9EBEE"; SURFACE="#FFFFFF"
GOV="#0072B2"; GOVD="#005A8E"; VERM="#D55E00"; VIO="#7B2D8E"; GREEN="#117733"
COCKPIT="#0B0F14"; CPANEL="#131A22"; CGRID="#2A323D"; CTEXT="#F5F7FA"; CTEXT2="#9AA4B2"
# dark-blueprint accents (web architecture variant only; cockpit family)
BP_LINE="#DCE9F5"; BP_CYAN="#56B4E9"; BP_VIO="#B98BD1"; BP_DIM="#8FA3B8"

# fixed per-model palette — matches the published forest plot; colorblind-safe
COOK_COLOR={"GPT-5.5":INK2,"Opus 4.8":VIO,"Gemini 3.5 Flash":GOV,"Grok 4.3":GREEN}
COOK_SHORT={"GPT-5.5":"GPT","Opus 4.8":"Opus","Gemini 3.5 Flash":"Gemini","Grok 4.3":"Grok"}
GENS=["GPT-5.5","Opus 4.8","Gemini 3.5 Flash","Grok 4.3"]
JUDGES=["Claude (Opus 4.8)","Gemini (3.5 Flash)","OpenAI (GPT-5.5)","Grok (4.3)"]
# naming standard (locked 2026-07-10): model names on the judge axis; company names
# only where lineage is the argument (kb: 04_whitepaper/kb/naming_standard.md)
JSHORT={"Claude (Opus 4.8)":"Opus","Gemini (3.5 Flash)":"Gemini",
        "OpenAI (GPT-5.5)":"GPT","Grok (4.3)":"Grok"}
SERIES_KEY={"GPT":"GPT-5.5","Opus":"Opus 4.8","Gemini":"Gemini 3.5 Flash","Grok":"Grok 4.3"}
T16=2.120  # two-sided t crit at df=16, alpha=.05

SANS="IBM Plex Sans"; MONO="IBM Plex Mono"

def register_fonts():
    n=0
    for ttf in sorted(FONTS.glob("*.ttf")):
        fm.fontManager.addfont(str(ttf)); n+=1
    if n==0: print("WARN: no TTFs under",FONTS)
    return n

def style(mode="paper"):
    """paper: white ground · web: ivory ground · blueprint: cockpit-dark ground."""
    register_fonts()
    bg = {"paper":PAPER,"web":IVORY,"blueprint":COCKPIT}[mode]
    fg = CTEXT if mode=="blueprint" else INK
    mpl.rcParams.update({
        "font.family": SANS,
        "font.sans-serif": [SANS,"DejaVu Sans"],
        "font.monospace": [MONO,"DejaVu Sans Mono"],
        "text.color": fg, "axes.edgecolor": fg, "axes.labelcolor": fg,
        "xtick.color": fg, "ytick.color": fg,
        "axes.linewidth": 0.9,
        "xtick.labelsize": 9, "ytick.labelsize": 9,
        "axes.labelsize": 10,
        "svg.fonttype": "none", "pdf.fonttype": 42,
        "figure.facecolor": bg, "savefig.facecolor": bg, "axes.facecolor": bg,
    })
    return bg

def m(**kw):
    """fontdict for code-like strings / numbers — always mono (brand law)."""
    d=dict(family=MONO); d.update(kw); return d

def save(fig, outdir, name, mode="paper", pad=0.18):
    outdir=Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    dpi = 350 if mode=="paper" else 300
    for ext in ("pdf","svg","png"):
        fig.savefig(outdir/f"{name}.{ext}", bbox_inches="tight", pad_inches=pad,
                    dpi=dpi if ext=="png" else None)
    plt.close(fig)
    print("wrote", name)

def hairline(ax, keep=()):
    for s in ("top","right","left","bottom"):
        ax.spines[s].set_visible(s in keep)
        if s in keep: ax.spines[s].set_color(HAIR)

# ---------- sealed-data loaders ----------
_JKEY={"claude":"Claude (Opus 4.8)","gemini":"Gemini (3.5 Flash)",
       "openai":"OpenAI (GPT-5.5)","xai":"Grok (4.3)"}

def load_matrix_4x4():
    """16 cells straight from the sealed raw record."""
    d=json.load(open(RAW/"tri_final_4x4.json"))
    S=[]
    for ck,cook in d["cooks"].items():
        gen=SERIES_KEY[ck]
        for jk,cell in cook["cells"].items():
            ev=cell["eval"]["reactivity"]
            mean,sd,t,n=ev["mean"],ev["sd"],ev["t"],ev["n"]
            se=sd/math.sqrt(n)
            S.append(dict(gen=gen,judge=_JKEY[jk],m=mean,sd=sd,t=t,n=n,
                dz=mean/sd,se=se,lo=mean-T16*se,hi=mean+T16*se,sig=abs(t)>T16,
                end=cell["endurance"]["reactivity"]["diff"],
                reg_wins=ev["reg_wins"],ties=ev["ties"],base_wins=ev["base_wins"],
                diag=bool(cell["diagonal"]),pas=bool(cell["cell_pass_react"])))
    assert len(S)==16
    return S

def headline_4x4():
    return json.load(open(RAW/"tri_final_4x4.json"))["headline"]

def headline_3x3():
    d=json.load(open(RAW/"tri_final.json"))
    return d.get("headline",d)

def recovery_counts():
    d=json.load(open(RAW/"tri_final_4x4.json"))
    return sum(1 for c in d["cooks"].values() if c["recovery_c3"]["pass_output_calm"]), len(d["cooks"])

def load_series():
    return list(csv.DictReader(open(TAB/"series_endurance_long_4x4.csv")))

def cook_summary(S=None, rows=None):
    """judges-avg eval diff per cook + baseline-reactivity headroom (provoked turns)."""
    import numpy as np
    S=S or load_matrix_4x4(); rows=rows or load_series()
    out={}
    for g in GENS:
        cells=[s for s in S if s["gen"]==g]
        sk={v:k for k,v in SERIES_KEY.items()}[g]
        prov=[r for r in rows if r["generator"]==sk and r["arm"]=="baseline"
              and float(r["raw_impulse"] or 0)>0 and r["react_median"] not in ("",None)]
        out[g]=dict(m=float(np.mean([c["m"] for c in cells])),
                    sig=sum(1 for c in cells if c["sig"]),
                    headroom=float(np.mean([float(r["react_median"]) for r in prov])))
    return out
