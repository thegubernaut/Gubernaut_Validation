#!/usr/bin/env python3
"""A2 sealed-record summary · A4 effect forest · A5 headroom bars · A7 faculty radial.
Print set — no baked figure numbers/titles (LaTeX captions own them)."""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import gubfig as G

# ---------------- A4: forest ----------------
def forest(outdir):
    G.style("paper")
    S=G.load_matrix_4x4()
    order=["Gemini 3.5 Flash","Opus 4.8","Grok 4.3","GPT-5.5"]
    flat=[next(x for x in S if x["gen"]==g and x["judge"]==j) for g in order for j in G.JUDGES]
    fig,ax=plt.subplots(figsize=(6.5,5.9))
    fig.subplots_adjust(left=0.185,right=0.975,top=0.975,bottom=0.105)
    ax.axvspan(-0.6,0,color=G.VERM,alpha=0.05,zorder=0)
    ax.axvline(0,color=G.INK,lw=1.1,zorder=2)
    y=len(flat); yt=[];ylab=[]
    for s in flat:
        y-=1; yt.append(y); ylab.append(f"{G.COOK_SHORT[s['gen']]} × {G.JSHORT[s['judge']]}")
        col=G.COOK_COLOR[s["gen"]]
        ax.plot([s["lo"],s["hi"]],[y,y],color=col,lw=2.2,solid_capstyle="round",
                alpha=1.0 if s["sig"] else 0.45,zorder=3)
        ax.plot([s["m"]],[y],marker="o",ms=7.5,color=(col if s["sig"] else G.PAPER),
                mec=col,mew=1.7,zorder=5)
        ax.text(s["hi"]+0.06,y,f"d_z {s['dz']:+.2f}{'' if s['sig'] else '  n.s.'}",
                va="center",fontsize=8.8,family=G.MONO,
                color=(G.INK if s["sig"] else G.INK2))
        if not s["pas"]:
            ax.text(s["lo"]-0.06,y,"null",va="center",ha="right",fontsize=8.8,
                    family=G.MONO,fontweight="semibold",color=G.INK)
    for k in (4,8,12):
        ax.axhline(len(flat)-k-0.5,color=G.HAIR,lw=0.8,zorder=1)
    ax.set_yticks(yt); ax.set_yticklabels(ylab,fontsize=9,family=G.MONO)
    ax.set_ylim(-0.7,len(flat)-0.3)
    ax.set_xlim(-0.62,2.78)
    ax.set_xlabel("Δ eval reactivity (baseline − regulated) · positive = regulated calmer",
                  fontsize=9.5,family=G.SANS)
    ax.tick_params(labelsize=9)
    for lab in ax.get_xticklabels(): lab.set_family(G.MONO)
    ax.grid(True,axis="x",color=G.HAIR,lw=0.6); ax.set_axisbelow(True)
    G.hairline(ax,keep=("bottom",))
    handles=[Line2D([],[],color=G.COOK_COLOR[g],lw=2.4,marker="o",ms=6.5,label=g) for g in order]
    handles.append(Line2D([],[],color=G.INK2,lw=2.2,marker="o",ms=6.5,mfc=G.PAPER,alpha=0.6,
                          label="open = sub-threshold (n.s.)"))
    leg=ax.legend(handles=handles,loc="lower right",fontsize=8.8,framealpha=0.97,edgecolor=G.HAIR)
    for i,t in enumerate(leg.get_texts()): t.set_family(G.MONO if i<4 else G.SANS)
    G.save(fig,outdir,"gcc_effect_forest",mode="paper",pad=0.1)

# ---------------- A5: headroom bars ----------------
def bars(outdir,mode="paper"):
    web = (mode!="paper")
    G.style(mode)
    S=G.load_matrix_4x4(); cs=G.cook_summary(S)
    order=sorted(G.GENS,key=lambda g:cs[g]["m"],reverse=True)
    fig,ax=plt.subplots(figsize=(6.5,4.3 if web else 3.75))
    fig.subplots_adjust(left=0.115,right=0.98,top=(0.82 if web else 0.96),bottom=(0.265 if web else 0.30))
    if web:
        fig.text(0.02,0.975,"The effect scales with the host's reactivity headroom",
                 fontsize=13,family=G.MONO,fontweight="semibold",color=G.INK,ha="left",va="top")
        fig.text(0.02,0.914,"Judges-averaged effect per cook. The hottest host gains most; the near-saturated "
                 "GPT host is already calm unregulated.",fontsize=9.3,family=G.SANS,color=G.GOVD,ha="left",va="top")
    xs=np.arange(len(order))
    for x,g in zip(xs,order):
        c=G.COOK_COLOR[g]; m=cs[g]["m"]
        ax.bar(x,m,width=0.6,color=c,zorder=3)
        ax.text(x,m+0.05,f"+{m:.2f}",ha="center",va="bottom",fontsize=13,
                fontweight="semibold",family=G.MONO,color=c)
        ax.text(x,m+0.21,f"{cs[g]['sig']}/4 judges p<.05",ha="center",va="bottom",
                fontsize=8.8,family=G.SANS,color=G.INK2)
    ax.set_xticks(xs)
    ax.set_xticklabels([g.replace(" ","\n",1) for g in order],fontsize=9.5)
    for lab in ax.get_xticklabels(): lab.set_family(G.MONO); lab.set_fontweight("semibold")
    ax.tick_params(axis="x",length=0,pad=8)
    for x,g in zip(xs,order):
        ax.text(x,-0.42,f"baseline reactivity {cs[g]['headroom']:.2f}",ha="center",va="top",
                fontsize=8.8,family=G.SANS,color=G.INK2,transform=ax.transData,clip_on=False)
    ax.set_ylim(0,1.85)
    ax.set_ylabel("judges-averaged Δ eval reactivity",fontsize=9.5,family=G.SANS)
    ax.tick_params(axis="y",labelsize=9)
    for lab in ax.get_yticklabels(): lab.set_family(G.MONO)
    ax.axhline(0,color=G.INK,lw=1.0)
    ax.grid(True,axis="y",color=G.HAIR,lw=0.6); ax.set_axisbelow(True)
    G.hairline(ax,keep=("bottom",))
    G.save(fig,outdir,"web_headroom_by_cook" if web else "gcc_headroom_by_cook",mode=mode,pad=0.1)

# ---------------- A7: faculty radial (gap-fill design) ----------------
def radial(outdir,mode="paper"):
    """Layer contribution class per faculty; the four areas Burnell et al.
    flag ("such as", their 4.1) as evaluation-coverage gaps shaded as wedges:
    metacognition, attention, learning, social cognition. One MEASURED spike
    (metacognition) lands in a shaded gap; executive functions is measured
    but is NOT a flagged gap (corrected 2026-07-12, checked against the
    arXiv HTML of 2605.28405).
    Radius stays ORDINAL (contribution class), stated in-figure."""
    web=(mode!="paper")
    G.style(mode)
    fac=["Perception","Generation","Attention","Learning","Memory","Reasoning",
         "Metacognition","Executive\nfunctions","Problem\nsolving","Social\ncognition"]
    cls=[2,1,2,0,2,1,3,3,1,2]
    gap=[0,0,1,1,0,0,1,0,0,1]
    N=len(fac); ang=np.linspace(0,2*np.pi,N,endpoint=False)
    a=np.concatenate([ang,ang[:1]]); v=np.array(cls+cls[:1])
    if web:
        BG=G.COCKPIT; LINE="#2FAF64"; FILL="#2FAF64"; TXT=G.CTEXT; TX2=G.CTEXT2
        GRID=G.CGRID; WEDGE="#14273B"; GAPLAB="#56B4E9"; RING=G.CTEXT2
    else:
        BG=G.PAPER; LINE=G.GOV; FILL=G.GOV; TXT=G.INK; TX2=G.INK2
        GRID=G.HAIR; WEDGE="#EBF3F8"; GAPLAB=G.GOVD; RING=G.INK2
    import matplotlib as mpl
    mpl.rcParams.update({"figure.facecolor":BG,"savefig.facecolor":BG})
    fig=plt.figure(figsize=(4.6,4.42))
    fig.patch.set_facecolor(BG)
    ax=fig.add_axes([0.115,0.075,0.77,0.83],polar=True)
    ax.set_facecolor(BG)
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
    ax.set_ylim(0,3.3)
    # gap wedges (behind everything)
    for k in range(N):
        if gap[k]:
            ax.bar(ang[k],3.3,width=2*np.pi/N,bottom=0,color=WEDGE,
                   edgecolor="none",zorder=0)
    ax.set_yticks([0,1,2,3])
    ax.set_yticklabels(["OUT-OF-SCOPE","HOST-INHERITED","ARCHITECTURAL","MEASURED"],
                       fontsize=8.5,color=RING,family=G.SANS)
    ax.set_rlabel_position(174)
    for i,t in enumerate(ax.get_yticklabels()):
        t.set_bbox(dict(boxstyle="round,pad=0.24",fc=BG,ec=GRID,lw=0.6,alpha=0.97))
        if i==3:
            t.set_color(LINE if web else G.GOVD); t.set_fontweight("bold")
    ax.set_xticks(ang)
    ax.set_xticklabels([f for f in fac],fontsize=8.8)
    for t,g in zip(ax.get_xticklabels(),gap):
        t.set_family(G.SANS)
        t.set_color((GAPLAB if g else TXT))
        t.set_fontweight("semibold" if g else "normal")
    ax.plot(a,v,color=LINE,lw=2.1,zorder=4)
    ax.fill(a,v,color=FILL,alpha=0.16 if web else 0.12,zorder=3)
    for k in range(N):
        if cls[k]==3:
            ax.plot(ang[k],3,marker="o",ms=7.5,color=LINE,zorder=5)
    ax.grid(color=GRID,lw=0.8)
    ax.spines["polar"].set_color(GRID)
    # ---- callout brackets at the two MEASURED spikes (figure coords) ----
    def bracket(theta,label,fx,fy):
        ax.annotate(label,xy=(theta,3.06),xytext=(fx,fy),
            textcoords="figure fraction",fontsize=8.2,family=G.MONO,fontweight="semibold",
            color=LINE,ha="left",va="center",
            bbox=dict(fc=BG,ec="none",pad=1.0),
            arrowprops=dict(arrowstyle="-",color=LINE,lw=0.9,
                            connectionstyle="angle3,angleA=0,angleB=80"),
            annotation_clip=False,zorder=6)
    bracket(ang[7],"SPIKE: EXECUTIVE FUNCTIONS",0.025,0.225)
    bracket(ang[6],"SPIKE: METACOGNITION",0.025,0.062)
    G.save(fig,outdir,"web_faculty_gapfill" if web else "gcc_faculty_contribution",mode=mode,pad=0.12)

# ---------------- A2: sealed-record summary (research-grade) ----------------
def summary(outdir):
    G.style("paper")
    S=G.load_matrix_4x4(); h4=G.headline_4x4(); rec,rt=G.recovery_counts()
    null=next(s for s in S if not s["pas"])
    nsig=sum(1 for s in S if s["sig"])
    rows=[(f"{h4['cells_pass']}/{h4['cells_total']}","cells favor the regulated arm","4×4 matrix · sign of the paired difference"),
          (f"{nsig}/{h4['cells_total']}","reach p < .05","paired t, df = 16, per cell"),
          (f"{h4['offdiag_pass']}/{h4['offdiag_total']}","off-diagonal (cross-family) cells","no self-judge in numerator"),
          (f"{rec}/{rt}","recovery replicates","arousal resets by T8, every cook, S4 + S5"),
          ("1","null cell, reported",f"GPT × Gemini, {null['m']:+.2f} (n.s.) · not a reversal")]
    fig=plt.figure(figsize=(6.5,2.7))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,41.5); ax.axis("off")
    def T(x,y,s,fs=9,mono=False,w="normal",c=G.INK,ha="left"):
        ax.text(x,y,s,fontsize=fs,color=c,ha=ha,va="center",
                family=(G.MONO if mono else G.SANS),fontweight=w)
    top=39.2
    ax.plot([2,98],[top,top],color=G.INK,lw=1.1)
    T(13,top-2.6,"COUNT",8.7,mono=True,c=G.INK2,ha="right")
    T(16,top-2.6,"FINDING",8.7,mono=True,c=G.INK2)
    T(55,top-2.6,"PROVENANCE",8.7,mono=True,c=G.INK2)
    ax.plot([2,98],[top-5.0,top-5.0],color=G.HAIR,lw=0.8)
    y=top-9.0
    for big,lab,src in rows:
        T(13,y,big,12.5,mono=True,w="semibold",ha="right")
        T(16,y,lab,9.5)
        T(55,y,src,8.8,mono=True,c=G.INK2)
        y-=5.5
    ax.plot([2,98],[y+2.6,y+2.6],color=G.INK,lw=1.1)
    T(2,y-0.6,"each model serves as both generator (cook) and judge · deterministic governor on vs off · "
      "counts derive from the sealed record",8.8,c=G.INK2)
    G.save(fig,outdir,"gcc_sealed_record_summary",mode="paper",pad=0.12)

if __name__=="__main__":
    out=os.environ.get("FIGOUT","/tmp/gubfig/A")
    forest(out); bars(out); radial(out); summary(out)
