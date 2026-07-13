#!/usr/bin/env python3
"""Verification harness — every number the public visuals plot, asserted
against the sealed record (02_data/raw). ALL PASS required before any asset
advances past RENDERED in REGISTRY.md."""
import csv, json, sys
from pathlib import Path
import gubfig as G

FAIL=[]
def check(name,cond,detail=""):
    print(("PASS " if cond else "FAIL ")+name+(f"  [{detail}]" if detail and not cond else ""))
    if not cond: FAIL.append(name)

# ---- 1. sealed matrix invariants (raw) ----
S=G.load_matrix_4x4()
check("16 cells",len(S)==16)
check("15/16 by sign",sum(1 for s in S if s["m"]>0)==15)
check("13/16 significant",sum(1 for s in S if s["sig"])==13)
nulls=[s for s in S if not s["pas"]]
check("single null is GPT x Gemini",len(nulls)==1 and nulls[0]["gen"]=="GPT-5.5" and G.JSHORT[nulls[0]["judge"]]=="Gemini")
check("null value -0.039 / end +0.14",abs(nulls[0]["m"]+0.039)<1e-9 and abs(nulls[0]["end"]-0.14)<1e-9)
subthr=[f"{G.COOK_SHORT[s['gen']]}x{G.JSHORT[s['judge']]}" for s in S if not s["sig"]]
check("3 sub-threshold, all on GPT cook",len(subthr)==3 and all(x.startswith("GPT") for x in subthr),str(subthr))
check("naming standard: judge labels model-first (locked 2026-07-10)",
      set(G.JSHORT.values())=={"Opus","Gemini","GPT","Grok"},str(sorted(G.JSHORT.values())))

# ---- 2. headlines ----
h4=G.headline_4x4()
check("headline 4x4 = 15/16, 11/12 offdiag, 4/4 diag",
      (h4["cells_pass"],h4["cells_total"],h4["offdiag_pass"],h4["offdiag_total"],h4["diag_pass"],h4["diag_total"])==(15,16,11,12,4,4))
h3=G.headline_3x3()
check("frozen 3×3 provenance 8/9 (5/6 offdiag, 3/3 diag)",
      (h3["cells_pass"],h3["cells_total"],h3["offdiag_pass"],h3["offdiag_total"],h3["diag_pass"],h3["diag_total"])==(8,9,5,6,3,3))
rec,rt=G.recovery_counts(); check("recovery 4/4",(rec,rt)==(4,4))

# ---- 3. cook summary (headroom bars / dose-response) ----
cs=G.cook_summary(S)
want={"Gemini 3.5 Flash":(1.48,4),"Opus 4.8":(0.61,4),"Grok 4.3":(0.47,4),"GPT-5.5":(0.10,1)}
for g,(m,k) in want.items():
    check(f"cook avg {G.COOK_SHORT[g]} = +{m:.2f}, {k}/4 sig",round(cs[g]["m"],2)==m and cs[g]["sig"]==k,
          f"got {cs[g]['m']:.3f},{cs[g]['sig']}")

# ---- 4. rendered tables agree with raw (master_table_4x4.csv) ----
rows={ (r["generator"],r["judge"]):r for r in csv.DictReader(open(G.TAB/"master_table_4x4.csv")) }
ok=True
for s in S:
    r=rows[(s["gen"],s["judge"])]
    ok&=abs(float(r["eval_diff_mean"])-s["m"])<1e-9
    ok&=abs(float(r["eval_t"])-s["t"])<1e-9
    ok&=abs(float(r["endurance_diff"])-s["end"])<1e-9
    ok&=(r["pass"]=="True")==s["pas"] and (r["diagonal"]=="True")==s["diag"]
check("master_table_4x4.csv byte-consistent with raw",ok)

# ---- 5. series CSV spot-checks vs raw endurance logs ----
ser=G.load_series()
def spot(cook,sid,turn,arm="regulated"):
    raw=json.load(open(G.RAW/f"endurance_endurance_tri_cook{cook}.json"))
    seq=next(s for s in raw["sequences"] if s["seq_id"]==sid)
    t=next(x for x in seq[arm] if x["turn"]==turn)
    ctl=t.get("guna") or t.get("controller") or {}
    a_raw=ctl.get("rajas",ctl.get("arousal"))
    row=next(r for r in ser if r["generator"]==cook and r["seq_id"]==sid
             and int(r["turn"])==turn and r["arm"]==arm)
    post_raw={"RAJAS":"INHIBIT","TAMAS":"REGROUND"}.get(t.get("posture"),t.get("posture"))
    if a_raw is None:   # baseline arm: governor absent -> no controller state
        return row["arousal"] in ("",None) and (row["posture"] or None)==post_raw
    return abs(float(row["arousal"])-a_raw)<1e-9 and row["posture"]==post_raw
check("series spot: Gemini S4 T7",spot("Gemini","S4",7))
check("series spot: Grok S5 T4",spot("Grok","S5",4))
check("series spot: GPT S4 T10 baseline",spot("GPT","S4",10,"baseline"))
check("series rows = 400",len(ser)==400)

# ---- 6. staged assets exist, vector + >=300dpi PNG ----
from PIL import Image
PV=G.PV
A=["gcc_architecture_schematic","gcc_sealed_record_summary","gcc_matrix_4x4","gcc_effect_forest",
   "gcc_headroom_by_cook","gcc_recovery_S4S5","gcc_faculty_contribution"]
B=["gcc_architecture_blueprint_dark","web_matrix_4x4","web_recovery_S4S5","web_headroom_by_cook",
   "web_dose_response","web_at_a_glance","web_dual_process","web_faculty_gapfill"]
MINW={"gcc_faculty_contribution":1380,"web_faculty_gapfill":1340}   # 4.6in layout width x 300dpi
ok=True; small=[]
for sub,names in (("A_whitepaper",A),("B_website",B)):
    for n in names:
        for ext in ("pdf","png","svg"):
            ok &= (PV/sub/f"{n}.{ext}").exists()
        im=Image.open(PV/sub/f"{n}.png")
        if im.width<MINW.get(n,1900): small.append(f"{n}:{im.width}px")
check("all 14 assets staged as PDF+PNG+SVG",ok)
check("all PNGs >= 300 dpi at layout width",not small,str(small))

# ---- 7. print set carries no baked figure numbering ----
import re
bad=[]
for f in ["fig_architecture.py","fig_matrix.py","fig_recovery.py","fig_batch.py"]:
    src=open(Path(__file__).parent/f).read()
    if re.search(r'"Figure\s*\d',src): bad.append(f)
check("no baked 'Figure N' strings in print-set sources",not bad,str(bad))

print()
print("ALL PASS" if not FAIL else f"{len(FAIL)} FAILURES: {FAIL}")
sys.exit(1 if FAIL else 0)
