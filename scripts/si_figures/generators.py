import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import os

# Palette
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
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
})

OUT_DIR = "../../assets/images"
os.makedirs(OUT_DIR, exist_ok=True)

def setup_fig(figsize=(10, 6)):
    fig = plt.figure(figsize=figsize, dpi=150)
    return fig

def save_fig(fig, filename):
    fig.savefig(os.path.join(OUT_DIR, filename), bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)

# M2 Eye Diagram for Cover
def generate_cover_eye():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    
    t = np.linspace(-1, 1, 500)
    for _ in range(100):
        # Simulate eye traces
        jitter = np.random.normal(0, 0.05)
        noise = np.random.normal(0, 0.02, len(t))
        
        # simple tanh for transition
        trace_up = np.tanh(10 * (t - jitter + 0.5)) - np.tanh(10 * (t - jitter - 0.5)) - 1 + noise
        trace_down = -trace_up + np.random.normal(0, 0.02, len(t))
        
        ax.plot(t, trace_up, color=CYAN, alpha=0.1, linewidth=1.5)
        ax.plot(t, trace_down, color=CYAN, alpha=0.1, linewidth=1.5)
        
    # Mask
    mask_poly = plt.Polygon([[-0.25, -0.5], [0.25, -0.5], [0.4, 0], [0.25, 0.5], [-0.25, 0.5], [-0.4, 0]], 
                            closed=True, fill=True, color=GRATICULE, alpha=0.5, edgecolor=COPPER, linewidth=2)
    ax.add_patch(mask_poly)
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("EYE DIAGRAM", color=CYAN, loc='left')
    save_fig(fig, "cover_eye_m2.png")

# Part 1: Foundations
def generate_part1():
    fig, ax = plt.subplots(figsize=(10, 6))
    # E-field lines (cyan), H-field loops (copper)
    # Ground plane
    ax.add_patch(patches.Rectangle((-5, -1), 10, 0.5, color=GRATICULE))
    # Dielectric
    ax.add_patch(patches.Rectangle((-5, -0.5), 10, 1.5, color="#111a2a"))
    # Trace
    ax.add_patch(patches.Rectangle((-1, 1), 2, 0.2, color=COPPER))
    
    # Field lines
    for x in np.linspace(-0.8, 0.8, 7):
        ax.annotate("", xy=(x*1.5, -0.5), xytext=(x, 1),
                    arrowprops=dict(arrowstyle="->", color=CYAN, alpha=0.7, lw=2, connectionstyle=f"arc3,rad={x*0.2}"))
        
    for r in [1, 2, 3]:
        circle = patches.Ellipse((0, 1.1), width=r*1.5, height=r*1.2, fill=False, color=COPPER, ls='--', lw=1.5, alpha=0.6)
        ax.add_patch(circle)
        
    ax.set_xlim(-5, 5)
    ax.set_ylim(-2, 4)
    ax.axis('off')
    save_fig(fig, "si_part1_foundations.jpg")

# Part 2: Measurement
def generate_part2():
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])
    
    # S21
    ax1 = fig.add_subplot(gs[0])
    f = np.linspace(0, 20, 100)
    s21 = -0.5 * f - 0.1 * np.sqrt(f)
    ax1.plot(f, s21, color=CYAN, lw=2)
    ax1.set_title("S21 Insertion Loss", color=TEXT_COLOR)
    ax1.set_xlabel("GHz")
    ax1.set_ylabel("dB")
    ax1.grid(True)
    
    # Smith Chart mockup
    ax2 = fig.add_subplot(gs[1])
    circle = patches.Circle((0, 0), 1, fill=False, color=GRATICULE)
    ax2.add_patch(circle)
    # R circles
    for r in [0.2, 0.5, 1.0]:
        c = patches.Circle((r/(1+r), 0), 1/(1+r), fill=False, color=GRATICULE, alpha=0.5)
        ax2.add_patch(c)
    # Spiraling trace
    theta = np.linspace(0, 4*np.pi, 200)
    r_spiral = np.linspace(0.8, 0, 200)
    ax2.plot(r_spiral*np.cos(theta), r_spiral*np.sin(theta), color=COPPER, lw=2)
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax2.axis('off')
    ax2.set_title("S11 Smith Chart", color=TEXT_COLOR)
    
    # TDR
    ax3 = fig.add_subplot(gs[2])
    t = np.linspace(0, 10, 200)
    z = 50 * np.ones_like(t)
    z[40:60] = 40  # dip
    z[120:140] = 60 # bump
    # smooth
    z = np.convolve(z, np.ones(5)/5, mode='same')
    ax3.plot(t, z, color=CYAN, lw=2)
    ax3.set_ylim(20, 80)
    ax3.set_title("TDR Impedance", color=TEXT_COLOR)
    ax3.grid(True)
    
    plt.tight_layout()
    save_fig(fig, "si_part2_measurement.jpg")

# We will generate Part 3 to 6 similarly...

def generate_all():
    generate_cover_eye()
    generate_part1()
    generate_part2()

if __name__ == '__main__':
    generate_all()
