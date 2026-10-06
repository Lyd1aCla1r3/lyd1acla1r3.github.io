import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import os

BG_COLOR = "#0b1220"
CYAN = "#38d6ff"
COPPER = "#e8a07a"
GRATICULE = "#1e2a3a"
TEXT_COLOR = "#a0b0c0"

plt.rcParams.update({
    "figure.facecolor": BG_COLOR,
    "axes.facecolor": BG_COLOR,
    "axes.edgecolor": GRATICULE,
    "axes.labelcolor": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "grid.color": GRATICULE,
    "font.family": "sans-serif",
})

OUT_DIR = "../../assets/images"

def save_fig(fig, filename):
    fig.savefig(os.path.join(OUT_DIR, filename), bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)

def gen_qa01():
    fig, ax = plt.subplots(figsize=(6, 4))
    circle = patches.Circle((0, 0), 1, fill=False, color=COPPER, lw=2)
    ax.add_patch(circle)
    ax.text(0, 0.5, "Eddy\nLoop", color=CYAN, ha="center")
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    save_fig(fig, "fig_qa01_eddy.jpg")

def gen_qa05():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([0, 2], [0, 0], color=COPPER, lw=3)
    ax.plot([0, 2], [1, 1], color=CYAN, lw=3)
    ax.text(1, 0.5, "Desk Frame Case 2/3", color=TEXT_COLOR, ha="center")
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    save_fig(fig, "fig_qa05_desk.jpg")

def gen_tdr():
    fig, ax = plt.subplots(figsize=(6, 4))
    t = np.linspace(0, 10, 100)
    z = np.ones_like(t) * 50
    z[20:40] = 75
    z[60:80] = 25
    ax.plot(t, z, color=CYAN, lw=2)
    ax.set_title("TDR Staircase", color=TEXT_COLOR)
    ax.set_ylim(0, 100)
    ax.grid(True)
    save_fig(fig, "fig_tdr_staircase.jpg")

def gen_gibbs():
    fig, ax = plt.subplots(figsize=(6, 4))
    t = np.linspace(0, 1, 200)
    y = np.zeros_like(t)
    for n in range(1, 15, 2):
        y += (4/(np.pi*n)) * np.sin(2*np.pi*n*t)
    ax.plot(t, y, color=CYAN, lw=2)
    ax.set_title("Step Synthesis & Gibbs", color=TEXT_COLOR)
    ax.grid(True)
    save_fig(fig, "fig_gibbs.jpg")

def gen_sparam():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(patches.Rectangle((0, 0), 2, 1.5, color=GRATICULE, alpha=0.5))
    ax.text(1, 0.75, "DUT", color=TEXT_COLOR, ha="center", va="center")
    ax.annotate("a1", xy=(0, 1.2), xytext=(-1, 1.2), arrowprops=dict(arrowstyle="->", color=CYAN))
    ax.annotate("b1", xy=(-1, 0.3), xytext=(0, 0.3), arrowprops=dict(arrowstyle="<-", color=COPPER))
    ax.annotate("a2", xy=(2, 0.3), xytext=(3, 0.3), arrowprops=dict(arrowstyle="<-", color=CYAN))
    ax.annotate("b2", xy=(3, 1.2), xytext=(2, 1.2), arrowprops=dict(arrowstyle="->", color=COPPER))
    ax.set_xlim(-1.5, 3.5)
    ax.set_ylim(-0.5, 2)
    ax.axis('off')
    save_fig(fig, "fig_sparam_port.jpg")

def gen_next():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([0, 4], [1, 1], color=COPPER, lw=3, label="Aggressor")
    ax.plot([0, 4], [0, 0], color=CYAN, lw=3, label="Victim")
    ax.annotate("NEXT", xy=(0, 0), xytext=(-1, 0), arrowprops=dict(arrowstyle="<-", color=TEXT_COLOR))
    ax.annotate("FEXT", xy=(4, 0), xytext=(5, 0), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax.legend(frameon=False, labelcolor=TEXT_COLOR)
    ax.set_xlim(-1.5, 5.5)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    save_fig(fig, "fig_next_fext.jpg")

def gen_fir():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.add_patch(patches.Rectangle((0, 0), 1, 1, color=CYAN, alpha=0.3))
    ax.add_patch(patches.Rectangle((2, 0), 1, 1, color=COPPER, alpha=0.3))
    ax.text(0.5, 0.5, "Delay", color=TEXT_COLOR, ha="center")
    ax.text(2.5, 0.5, "Tap", color=TEXT_COLOR, ha="center")
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    ax.set_title("FIR Block Diagram", color=TEXT_COLOR)
    save_fig(fig, "fig_fir_block.jpg")

def generate_all():
    gen_qa01()
    gen_qa05()
    gen_tdr()
    gen_gibbs()
    gen_sparam()
    gen_next()
    gen_fir()
    # IQ constellation already in Part 6, but we can make a standalone
    fig, ax = plt.subplots(figsize=(4, 4))
    levels = [-3, -1, 1, 3]
    for i in levels:
        for q in levels:
            ax.scatter(i, q, color=CYAN)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, alpha=0.3)
    ax.set_title("IQ Constellation", color=TEXT_COLOR)
    save_fig(fig, "fig_iq_constellation.jpg")

if __name__ == '__main__':
    generate_all()
