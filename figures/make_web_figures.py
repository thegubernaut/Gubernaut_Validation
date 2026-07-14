#!/usr/bin/env python3
"""B set — website/outreach visuals (light brand theme; one dark blueprint).
B1 blueprint (fig_blueprint.py) · B2 matrix · B3 recovery · B4 headroom bars ·
B5 dose-response (no trend claim) · B6 at-a-glance · B7 dual-process."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Patch
from matplotlib.lines import Line2D
import gubfig as G
import fig_blueprint, fig_matrix, fig_recovery, fig_batch

def head(fig,title,sub):
    fig.text(0.02,0.975,title,fontsize=13,family=G.MONO,fontweight="semibold",
             color=G.INK,ha="left",va="top")
    fig.text(0.02,0.912,sub,fontsize=9.3,family=G.SANS,color=G.GOVD,ha="left",va="top")

# ---------------- B5: dose-response (descriptive only) ----------------
def dose(outdir):
    G.style("web")
    S=G.load_matrix_4x4(); cs=G.cook_summary(S)
    fig,ax=plt.subplots(figsize=(6.5,4.6))
    fig.subplots_adjust(left=0.105,right=0.97,top=0.82,bottom=0.13)
    head(fig,"A hotter host has more to regulate",
         "Each point is one cook (n = 4) — descriptive, not inferential. "
         "Baseline reactivity is the unregulated host on provoked turns.")
    for g in G.GENS:
        c=G.COOK_COLOR[g]
        ax.scatter([cs[g]["headroom"]],[cs[g]["m"]],s=200,color=c,zorder=4,edgecolor="white",lw=1.4)
        ax.annotate(G.COOK_SHORT[g],(cs[g]["headroom"],cs[g]["m"]),textcoords="offset points",
                    xytext=(11,7),fontsize=10.5,fontweight="semibold",family=G.MONO,color=c)
    ax.set_xlabel("host baseline reactivity on provoked turns (1–5)",fontsize=9.5,family=G.SANS)
    ax.set_ylabel("judges-averaged Δ eval reactivity",fontsize=9.5,family=G.SANS)
    ax.set_xlim(1.25,2.9); ax.set_ylim(-0.05,1.65)
    ax.tick_params(labelsize=9)
    for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_family(G.MONO)
    ax.grid(True,color=G.HAIR,lw=0.6); ax.set_axisbelow(True); G.hairline(ax,keep=("left","bottom"))
    G.save(fig,outdir,"web_dose_response",mode="web",pad=0.12)

# ---------------- B6: at-a-glance hero ----------------
def glance(outdir):
    G.style("web")
    S=G.load_matrix_4x4(); h4=G.headline_4x4(); h3=G.headline_3x3(); rec,rt=G.recovery_counts()
    null=next(s for s in S if not s["pas"])
    fig=plt.figure(figsize=(12.0,5.4))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,120); ax.set_ylim(0,54); ax.axis("off")
    ax.text(4,49.5,"Gubernaut Cognitive Layer — what the sealed record shows",
            fontsize=17,family=G.MONO,fontweight="semibold",color=G.INK,va="center")
    ax.text(4,44.8,"Triangulated head-to-head: each model is both generator (cook) and judge; "
            "the deterministic governor is toggled on vs off.",fontsize=10,family=G.SANS,color=G.INK2,va="center")
    cards=[(f"{h4['cells_pass']}/{h4['cells_total']}","cells favor regulated","4×4 matrix · sign test",G.GOV),
           (f"{h4['offdiag_pass']}/{h4['offdiag_total']}","off-diagonal cells","cross-family, no self-judge",G.GOVD),
           (f"{rec}/{rt}","recovery replicates","arousal resets by T8, every cook",G.GREEN),
           (f"{h3['cells_pass']}/{h3['cells_total']}","frozen 3×3 · provenance","sealed 2026-06-11 · unaltered",G.INK),
           ("1","null cell, reported",f"GPT × Gemini, {null['m']:+.2f}\nnot a reversal",G.VERM)]
    x=3.5; w=21.6; gap=1.55
    for big,lab,sub,col in cards:
        ax.add_patch(FancyBboxPatch((x,8.5),w,30,boxstyle="round,pad=0.4,rounding_size=1.6",
                     fc=G.SURFACE,ec=G.HAIR,lw=1.2))
        ax.text(x+w/2,31.5,big,ha="center",va="center",fontsize=21,family=G.MONO,
                fontweight="semibold",color=col)
        ax.text(x+w/2,22.8,lab,ha="center",va="center",fontsize=10,family=G.SANS,color=G.INK)
        ax.text(x+w/2,17.0,sub,ha="center",va="center",fontsize=8.2,family=G.MONO,color=G.INK2,linespacing=1.5)
        x+=w+gap
    ax.text(4,4.0,"effect scales with the host's reactivity headroom · inter-judge agreement held when the "
            "xAI family was added · numbers reproducible from the sealed record · recorded-run evidence — "
            "no consciousness claim",fontsize=8.6,family=G.SANS,color=G.INK2,va="center")
    G.save(fig,outdir,"web_at_a_glance",mode="web",pad=0.0)

# ---------------- B7: dual-process hero ----------------
def dual(outdir):
    G.style("web")
    rows=G.load_series()
    PHASE_BG={"escalating":"#FDEBD7","intense":"#FBE0E0","de-escalation":"#DCEFE0"}
    def seq(ck,sid,arm):
        rr=[r for r in rows if r["generator"]==ck and r["seq_id"]==sid and r["arm"]==arm]
        return sorted(rr,key=lambda r:int(r["turn"]))
    reg,base=seq("Gemini","S1","regulated"),seq("Gemini","S1","baseline")
    t=[int(r["turn"]) for r in reg]
    fig,ax=plt.subplots(figsize=(9.4,5.0))
    fig.subplots_adjust(left=0.075,right=0.925,top=0.80,bottom=0.115)
    head(fig,"Dual-process dampening — Gemini 3.5 Flash, S1 (competence probe)",
         "Same scripted input, two arms. The impulse arrives either way; the controller decides what survives. "
         "The regulated arm stays flat while the baseline tracks the provocation.")
    for r in reg:
        bg=PHASE_BG.get(r["phase"])
        if bg: ax.axvspan(int(r["turn"])-0.5,int(r["turn"])+0.5,color=bg,zorder=0,lw=0)
    ax2=ax.twinx()
    ax2.bar(t,[float(r["raw_impulse"]) for r in reg],width=0.55,color="#9AA0A6",alpha=0.32,zorder=2)
    ax2.plot(t,[float(r["arousal"]) for r in reg],color=G.VIO,ls="--",lw=1.8,marker=".",ms=7,zorder=3)
    for r in reg:
        if r["posture"]=="INHIBIT":
            ax2.scatter([int(r["turn"])],[min(0.97,float(r["arousal"])+0.055)],marker="^",s=52,color=G.VIO,zorder=5)
    ax2.set_ylim(0,1.0); ax2.set_ylabel("impulse / controller state (0–1)",fontsize=9.3,family=G.SANS,color=G.INK2)
    ax2.spines["top"].set_visible(False); ax2.tick_params(colors=G.INK2,labelsize=8.8)
    for lab in ax2.get_yticklabels(): lab.set_family(G.MONO)
    ax.plot(t,[float(r["react_median"]) for r in base],color=G.VERM,lw=2.3,marker="s",ms=5.4,zorder=4)
    ax.plot(t,[float(r["react_median"]) for r in reg],color=G.GOV,lw=2.3,marker="o",ms=5.4,zorder=4)
    ax.set_ylim(0.7,5.3); ax.set_yticks([1,2,3,4,5]); ax.set_xticks(range(1,11))
    ax.set_xlabel("turn",fontsize=9.3,family=G.SANS)
    ax.set_ylabel("judge reactivity (panel median, 1–5)",fontsize=9.3,family=G.SANS)
    ax.tick_params(labelsize=9)
    for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_family(G.MONO)
    ax.grid(True,axis="y",color=G.HAIR,lw=0.6); ax.set_axisbelow(True); G.hairline(ax,keep=("left","bottom"))
    handles=[Line2D([],[],color=G.GOV,marker="o",lw=2.3,label="regulated output"),
             Line2D([],[],color=G.VERM,marker="s",lw=2.3,label="baseline output"),
             Patch(color="#9AA0A6",alpha=0.32,label="raw impulse"),
             Line2D([],[],color=G.VIO,ls="--",marker=".",label="arousal (controller state)"),
             Line2D([],[],color=G.VIO,marker="^",ls="",label="INHIBIT engaged"),
             Patch(color=PHASE_BG["escalating"],label="escalating"),
             Patch(color=PHASE_BG["intense"],label="intense"),
             Patch(color=PHASE_BG["de-escalation"],label="de-escalation")]
    ax.legend(handles=handles,loc="upper left",fontsize=8.7,framealpha=0.97,edgecolor=G.HAIR,ncol=2,
              borderpad=0.5,labelspacing=0.4)
    G.save(fig,outdir,"web_dual_process",mode="web",pad=0.12)

if __name__=="__main__":
    out=os.environ.get("FIGOUT","/tmp/gubfig/B")
    fig_blueprint.main(out)
    fig_matrix.main(out,mode="web")
    fig_recovery.main(out,mode="web")
    fig_batch.bars(out,mode="web")
    dose(out); glance(out); dual(out)
    print("B set complete")
