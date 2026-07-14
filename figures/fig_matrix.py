#!/usr/bin/env python3
"""A3 — gcc_matrix_4x4. The single in-text 4x4 representation (Draft-9 Fig 3).
No baked title/counts — the LaTeX caption owns the result statement."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
import gubfig as G

COL_MODEL={"Claude (Opus 4.8)":"Opus 4.8","Gemini (3.5 Flash)":"3.5 Flash",
           "OpenAI (GPT-5.5)":"GPT-5.5","Grok (4.3)":"Grok 4.3"}

def main(outdir,mode="paper"):
    web = (mode!="paper")
    G.style(mode)
    S=G.load_matrix_4x4()
    cell={(G.GENS.index(s["gen"]),G.JUDGES.index(s["judge"])):s for s in S}
    cmap=LinearSegmentedColormap.from_list("gov",[G.VERM,"#FBEDE3","#FFFFFF","#CFE6F2",G.GOV])
    norm=TwoSlopeNorm(vmin=-0.3,vcenter=0.0,vmax=1.8)

    fig=plt.figure(figsize=(6.5,5.38 if web else 4.81))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,100); ax.set_ylim(0,82.8 if web else 74); ax.axis("off")
    X0,YT,CW,CH=17,66,20,13

    def T(x,y,s,fs=9,mono=False,w="normal",c=G.INK,ha="center",va="center",rot=0):
        ax.text(x,y,s,fontsize=fs,color=c,ha=ha,va=va,rotation=rot,
                family=(G.MONO if mono else G.SANS),fontweight=w,zorder=6)

    # headers
    for j,J in enumerate(G.JUDGES):
        cx=X0+j*CW+CW/2
        T(cx,70.8,f"{G.JSHORT[J]} judge",10,w="semibold")
        T(cx,68.3,COL_MODEL[J],8.8,mono=True,c=G.INK2)
    for i,g in enumerate(G.GENS):
        cy=YT-i*CH-CH/2
        nm=g.split(" ")
        if g=="Gemini 3.5 Flash":
            T(15.5,cy+2.2,"Gemini",9.5,mono=True,w="semibold",ha="right")
            T(15.5,cy,"3.5 Flash",9.5,mono=True,w="semibold",ha="right")
            T(15.5,cy-2.4,"cook",8.7,c=G.INK2,ha="right")
        else:
            T(15.5,cy+1.1,g,9.5,mono=True,w="semibold",ha="right")
            T(15.5,cy-1.5,"cook",8.7,c=G.INK2,ha="right")
    T(1.8,YT-2*CH,"GENERATOR (cook)",9.2,w="semibold",rot=90)

    # cells
    for (i,j),s in cell.items():
        x,y=X0+j*CW,YT-(i+1)*CH
        ax.add_patch(Rectangle((x,y),CW,CH,fc=cmap(norm(s["m"])),ec=G.PAPER,lw=2.2,zorder=2))
        dark=s["m"]>0.95
        tc="#FFFFFF" if dark else G.INK
        t2="#E8EEF4" if dark else G.INK2
        null=not s["pas"]
        T(x+CW/2,y+CH-3.5,f"{s['m']:+.2f}",15,mono=True,w="semibold",c=tc)
        T(x+CW/2,y+CH-7.3,f"t {s['t']:+.1f} end {s['end']:+.2f}",8.7,mono=True,c=t2)
        cx,cy=x+CW/2,y+2.6
        word="null (n.s.)" if null else ("p<.05" if s["sig"] else "n.s.")
        wlen=len(word)*1.128
        mk=None if null else ("filled" if s["sig"] else "open")
        parts_w=(2.3 if mk else 0)+wlen+(2.3 if s["diag"] else 0)
        gx=cx-parts_w/2
        if mk:
            ax.scatter([gx+0.7],[cy],s=26,marker="o",
                       facecolor=(tc if mk=="filled" else "none"),edgecolor=tc,linewidths=1.1,zorder=6)
            gx+=2.3
        T(gx+wlen/2,cy,word,8.8,mono=True,w=("semibold" if null else "normal"),c=tc)
        gx+=wlen
        if s["diag"]:
            ax.scatter([gx+1.5],[cy],s=24,marker="D",facecolor=tc,edgecolor=tc,zorder=6)
        if null:
            ax.add_patch(Rectangle((x+0.55,y+0.55),CW-1.1,CH-1.1,fill=False,ec=G.INK,lw=1.6,zorder=5))
        elif not s["sig"]:
            ax.add_patch(Rectangle((x+0.55,y+0.55),CW-1.1,CH-1.1,fill=False,ec=G.INK2,lw=1.0,
                                   ls=(0,(4,3)),zorder=5))
    if web:
        h4=G.headline_4x4(); h3=G.headline_3x3()
        ax.text(2,80.6,"Triangulation matrix — 4×4",fontsize=13.5,family=G.MONO,
                fontweight="semibold",color=G.INK,ha="left",va="center")
        ax.text(2,77.3,f"Regulated beats baseline in {h4['cells_pass']} of {h4['cells_total']} cells "
                f"({h4['offdiag_pass']}/{h4['offdiag_total']} off-diagonal · {h4['diag_pass']}/{h4['diag_total']} self-judge) — "
                f"frozen 3×3 (provenance): {h3['cells_pass']}/{h3['cells_total']}.",
                fontsize=9.3,family=G.SANS,color=G.GOVD,ha="left",va="center")
    # key (three compact lines; the caption owns the headline result)
    T(X0,10.4,"cell: Δ eval reactivity (baseline − regulated) · positive = regulated calmer · t = paired t · end = Δ endurance",8.8,c=G.INK2,ha="left")
    ky=7.6
    ax.scatter([X0+0.7],[ky],s=26,marker="o",facecolor=G.INK2,edgecolor=G.INK2,linewidths=1.1,zorder=6)
    T(X0+2.1,ky,"p<.05",8.8,c=G.INK2,ha="left")
    ax.scatter([X0+13.2],[ky],s=26,marker="o",facecolor="none",edgecolor=G.INK2,linewidths=1.1,zorder=6)
    T(X0+14.6,ky,"sub-threshold (n.s.)",8.8,c=G.INK2,ha="left")
    ax.scatter([X0+40.2],[ky],s=24,marker="D",facecolor=G.INK2,edgecolor=G.INK2,zorder=6)
    T(X0+41.6,ky,"self-judge",8.8,c=G.INK2,ha="left")
    T(X0+57.5,ky,"solid box = the single null · dashed box = n.s.",8.8,c=G.INK2,ha="left")
    T(X0,4.8,"columns: judges · Grok 4.3 is the lineage-independent fourth family (xAI) · rows: generators (cooks)",8.8,c=G.INK2,ha="left")

    G.save(fig,outdir,"web_matrix_4x4" if web else "gcc_matrix_4x4",mode=mode)

if __name__=="__main__":
    main(os.environ.get("FIGOUT","/tmp/gubfig/A"))
