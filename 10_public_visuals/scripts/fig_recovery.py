#!/usr/bin/env python3
"""A6 — gcc_recovery_S4S5. The signature figure (Draft-9 Fig 7).
S4 + S5 panels, four families, phase shading, INHIBIT markers.
No baked figure title/subtitle — LaTeX caption owns them."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import gubfig as G

PHASE_BG={"escalating":"#FDEBD7","intense":"#FBE0E0","de-escalation":"#DCEFE0"}

def main(outdir,mode="paper"):
    web = (mode!="paper")
    G.style(mode)
    rows=G.load_series()
    def seq(ck,sid):
        rr=[r for r in rows if r["generator"]==ck and r["seq_id"]==sid and r["arm"]=="regulated"]
        return sorted(rr,key=lambda r:int(r["turn"]))
    fig,axes=plt.subplots(1,2,figsize=(6.5,4.25 if web else 3.7),sharey=True)
    fig.subplots_adjust(left=0.095,right=0.985,top=(0.675 if web else 0.775),bottom=(0.118 if web else 0.135),wspace=0.08)
    if web:
        fig.text(0.02,0.975,"The recovery property — one homeostatic signature on every family",
                 fontsize=13,family=G.MONO,fontweight="semibold",color=G.INK,ha="left",va="top")
        fig.text(0.02,0.917,"Controller arousal rises through provocation, then decays monotonically on de-escalation — "
                 "recovery replicates 4/4 cooks, both sequences.",fontsize=9.3,family=G.SANS,color=G.GOVD,ha="left",va="top")
    for ax,sid,title in ((axes[0],"S4","S4 — provocation → genuine de-escalation"),
                         (axes[1],"S5","S5 — held-out de-escalation battery")):
        ref=seq("GPT",sid)
        for r in ref:
            bg=PHASE_BG.get(r["phase"])
            if bg: ax.axvspan(int(r["turn"])-0.5,int(r["turn"])+0.5,color=bg,zorder=0,lw=0)
        for ck in ["GPT","Opus","Gemini","Grok"]:
            g=G.SERIES_KEY[ck]; c=G.COOK_COLOR[g]; s=seq(ck,sid)
            t=[int(r["turn"]) for r in s]; ar=[float(r["arousal"]) for r in s]
            ax.plot(t,ar,color=c,lw=1.9,marker="o",ms=4.2,label=g,zorder=4,clip_on=False)
            for r in s:
                if r["posture"]=="INHIBIT":
                    ax.scatter([int(r["turn"])],[float(r["arousal"])+0.014],marker="^",s=30,
                               color=c,zorder=5,clip_on=False)
        ax.set_title(title,fontsize=9.6,fontweight="semibold",color=G.INK,pad=6,family=G.SANS)
        ax.set_xlabel("turn",fontsize=9.5,family=G.SANS)
        ax.set_xticks(range(1,11)); ax.set_xlim(0.55,10.45); ax.set_ylim(0,0.46)
        ax.tick_params(labelsize=9)
        for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_family(G.MONO)
        ax.grid(True,axis="y",color=G.HAIR,lw=0.6); ax.set_axisbelow(True)
        G.hairline(ax,keep=("left","bottom"))
    axes[0].set_ylabel("controller arousal (regulated arm)",fontsize=9.5,family=G.SANS)
    mh=[Line2D([],[],color=G.COOK_COLOR[g],lw=1.9,marker="o",ms=4.2,label=g) for g in G.GENS]
    ph=[Patch(color=PHASE_BG["intense"],label="intense (T4–T7)"),
        Patch(color=PHASE_BG["de-escalation"],label="de-escalation (T8–T10)"),
        Line2D([],[],color=G.INK2,marker="^",ls="",ms=6,label="INHIBIT posture engaged")]
    leg=fig.legend(handles=mh+ph,ncol=4,loc="upper center",bbox_to_anchor=(0.5,0.878 if web else 1.005),
                   frameon=False,fontsize=8.8,handlelength=1.5,columnspacing=1.4,
                   handletextpad=0.55,labelspacing=0.45)
    for i,t in enumerate(leg.get_texts()):
        t.set_family(G.MONO if i<4 else G.SANS)
    G.save(fig,outdir,"web_recovery_S4S5" if web else "gcc_recovery_S4S5",mode=mode,pad=0.12)

if __name__=="__main__":
    main(os.environ.get("FIGOUT","/tmp/gubfig/A"))
