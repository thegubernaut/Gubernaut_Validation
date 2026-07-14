#!/usr/bin/env python3
"""A1 — gcc_architecture_schematic. Patent-style monitoring-control schematic.
Canvas 100 x 96 units at 6.5 x 6.24 in -> 1 unit = 4.68 pt. All text >= ~8.4pt,
information text >= 9pt equivalent. No baked-in figure number."""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import gubfig as G

INK,INK2=None,None

def main(outdir):
    G.style("paper")
    ink,g2=G.INK,G.INK2
    fig=plt.figure(figsize=(6.5,6.24))
    ax=fig.add_axes([0,0,1,1])
    ax.set_xlim(0,100); ax.set_ylim(0,96); ax.axis("off")

    def T(x,y,s,fs=9,mono=False,w="normal",c=ink,ha="left",va="center",rot=0,bbox=False,style="normal"):
        kw=dict(fontsize=fs,color=c,ha=ha,va=va,rotation=rot,fontstyle=style,
                family=(G.MONO if mono else G.SANS),fontweight=w,zorder=6)
        if bbox: kw["bbox"]=dict(fc="white",ec="none",pad=1.1)
        ax.text(x,y,s,**kw)

    def rect(x,y,w,h,lw=0.9,ls="-",double=False):
        ax.add_patch(Rectangle((x,y),w,h,fill=False,ec=ink,lw=lw,ls=ls,zorder=3))
        if double:
            ax.add_patch(Rectangle((x+0.75,y+0.6),w-1.5,h-1.2,fill=False,ec=ink,lw=0.55,zorder=3))

    def seg(pts,lw=1.0,ls="-"):
        for a,b in zip(pts[:-1],pts[1:]):
            ax.plot([a[0],b[0]],[a[1],b[1]],color=ink,lw=lw,ls=ls,solid_capstyle="projecting",zorder=4)

    def head(a,b,lw=1.0,filled=True,ls="-",ms=9):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle=("-|>" if filled else "->"),
            mutation_scale=ms,lw=lw,linestyle=ls,color=ink,shrinkA=0,shrinkB=0,zorder=5))

    def arrow(pts,lw=1.0,filled=True,ls="-",ms=9):
        if len(pts)>2: seg(pts[:-1],lw=lw,ls=ls)
        head(pts[-2],pts[-1],lw=lw,filled=filled,ls=ls,ms=ms)

    # ================= OBJECT BAND =================
    rect(3,63,94,31,lw=0.75)
    T(4.6,91.8,"OBJECT LEVEL",9.5,w="bold")
    T(20.2,91.8,"·  text-exposed",9,c=g2)

    # modules
    def module(x,w,title,s1=None,s2=None,tfs=10.5):
        rect(x,74,w,11)
        cy = 81.4 if s1 else 79.5
        T(x+w/2,cy,title,tfs,mono=True,w="semibold",ha="center")
        if s1: T(x+w/2,78.2,s1,8.5,mono=True,c=g2,ha="center")
        if s2: T(x+w/2,76.2,s2,8.5,mono=True,c=g2,ha="center")
    module(5,15,"INPUT","turn t")
    module(25,18,"IGL","appraisal →","telemetry only")
    module(51,22,"EAU","arbitration →","committed reply")
    module(79,16,"REPLY","committed")
    arrow([(20,79.5),(25,79.5)]); arrow([(43,79.5),(51,79.5)]); arrow([(73,79.5),(79,79.5)])

    # raw-text bypass over the top (INPUT -> EAU); IGL gets raw text via the main flow
    arrow([(12.5,85),(12.5,88.2),(62,88.2),(62,85)],lw=0.8)
    T(37.3,89.7,"raw, unsanitized text · reaches IGL and EAU",8.8,c=g2,ha="center",style="italic")

    # satellite memories (title-only, dashed)
    rect(52,64.8,8.5,5,ls=(0,(3,2)),lw=0.8); T(56.25,67.3,"PEV",9.2,mono=True,w="semibold",ha="center")
    rect(62,64.8,8.5,5,ls=(0,(3,2)),lw=0.8); T(66.25,67.3,"SMM",9.2,mono=True,w="semibold",ha="center")
    arrow([(55.4,69.8),(55.4,74)],lw=0.8,ms=7); arrow([(57.1,74),(57.1,69.8)],lw=0.8,ms=7)
    arrow([(66.25,69.8),(66.25,74)],lw=0.8,ms=7)

    # ================= META BAND =================
    rect(3,8,94,27,lw=0.75)
    T(4.6,32.8,"META LEVEL",9.5,w="bold",bbox=True)
    T(4.6,30.7,"token-free · deterministic",8.8,c=g2,bbox=True)

    # HRL controller (double border)
    rect(22.5,15,57,14,lw=1.1,double=True)
    T(51,26.4,"HRL — HOMEOSTATIC REGULATORY LOOP",10,mono=True,w="semibold",ha="center")
    T(51,23.7,"state {equilibrium, arousal, perseveration}",8.8,mono=True,ha="center")
    T(51,21.4,"posture: DEFAULT / INHIBIT / REGROUND",8.8,mono=True,ha="center")
    T(51,19.1,"+ RECOVERY window (timed sub-mode, §4)",8.6,mono=True,c=g2,ha="center")
    T(51,16.8,"deterministic: no sampling, no learned parameters",8.6,c=g2,ha="center",style="italic")

    # legend (two rows, inside meta band, below HRL)
    lx=5.5
    def key_node(x,y,kind):
        if kind=="obj": rect(x,y-0.85,3.2,1.9,lw=0.9)
        elif kind=="meta": rect(x,y-0.85,3.2,1.9,lw=0.9,double=False); ax.add_patch(Rectangle((x+0.4,y-0.5),2.4,1.2,fill=False,ec=ink,lw=0.5,zorder=3))
        elif kind=="sat": rect(x,y-0.85,3.2,1.9,lw=0.8,ls=(0,(3,2)))
    T(lx,13.3,"KEY",8.7,w="bold")
    key_node(11,13.3,"obj");  T(15.3,13.3,"object module",8.7)
    key_node(31,13.3,"meta"); T(35.3,13.3,"meta controller",8.7)
    key_node(52.5,13.3,"sat"); T(56.8,13.3,"satellite memory",8.7)
    arrow([(11,10.6),(14.2,10.6)],lw=1.0,filled=False,ms=8); T(15.3,10.6,"monitoring flow",8.7)
    arrow([(32.5,10.6),(35.7,10.6)],lw=1.0,filled=True,ms=8); T(36.8,10.6,"control flow",8.7)
    seg([(52.5,10.6),(55.7,10.6)],lw=0.9,ls=(0,(3,2))); T(56.8,10.6,"deterministic statistic",8.7)

    # ================= THE GAP =================
    ax.plot([3,97],[49,49],ls=(0,(7,4)),color=ink,lw=0.9,zorder=1)
    T(50,52.6,"THE STRUCTURAL GAP",9.5,w="bold",ha="center",bbox=True)
    T(50,46.8,"no text crosses",8.8,c=g2,ha="center",style="italic")
    T(52,44.6,"numbers ascend · a posture descends",8.8,c=g2,ha="center",style="italic")

    # ---- monitoring lane (x=34): IGL bottom -> HRL top ----
    arrow([(34,74),(34,29)],lw=1.1,filled=False)
    T(32.6,52.5,"telemetry {intensity, valence}",8.8,mono=True,rot=90,ha="center",bbox=True)
    # ---- control lane (x=72): HRL top -> EAU bottom ----
    arrow([(72,29),(72,74)],lw=1.1,filled=True)
    T(73.6,53.2,"posture {instruction, temperature}",8.8,mono=True,rot=90,ha="center",bbox=True)

    # lane tags + callouts (stacked rows, all between x35.5..70.5)
    T(35.8,42.5,"MONITORING · object → meta",8.7,w="bold")
    T(35.8,40.2,"zero-token numeric channel",8.7,c=g2,style="italic")
    T(70.4,37.9,"CONTROL · meta → object",8.7,w="bold",ha="right")
    T(70.4,35.6,"temperature clamp: not text-negotiable",8.7,c=g2,style="italic",ha="right")

    # ---- repetition statistic (INPUT -> HRL left side), dashed ----
    arrow([(9,74),(9,25),(22.5,25)],lw=0.9,ls=(0,(3,2)),filled=False)
    T(11,57.5,"repetition",8.7)
    T(11,55.4,"statistic",8.7)
    T(11,53.2,"(deterministic)",8.7,c=g2)

    # ================= MARGIN + TITLE BLOCK =================
    T(3,6.2,"baseline arm = governor removed",8.6,c=g2)
    T(3,4.2,"(IGL, HRL, and posture absent)",8.6,c=g2)
    T(3,1.9,"monitoring–control topology after Nelson & Narens (1990)",8.6,c=g2)

    tx,ty,tw,th=54,0.8,43,6.9
    rect(tx,ty,tw,th,lw=0.9)
    for yy in (ty+2.3,ty+4.6): ax.plot([tx,tx+tw],[yy,yy],color=ink,lw=0.5,zorder=4)
    T(tx+1,ty+5.75,"GCC ARCHITECTURE",8.8,mono=True,w="semibold")
    T(tx+tw-1,ty+5.75,"V1.3",8.8,mono=True,ha="right")
    T(tx+1,ty+3.45,"MONITORING–CONTROL LOOP",8.8,mono=True)
    T(tx+1,ty+1.15,"GUBERNAUT RESEARCH",8.6,mono=True)

    G.save(fig,outdir,"gcc_architecture_schematic",mode="paper")

if __name__=="__main__":
    main(os.environ.get("FIGOUT","/tmp/gubfig/A"))
