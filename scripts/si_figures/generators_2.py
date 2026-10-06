import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import os
from scipy.special import erfc

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

def save_fig(fig, filename):
    fig.savefig(os.path.join(OUT_DIR, filename), bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)

# Part 3: Jitter
def generate_part3():
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 2)
    
    # TIE Histogram
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.linspace(-30, 30, 200)
    # Dual Dirac
    y = 0.5 * np.exp(-((x - 10)**2)/(2*4**2)) + 0.5 * np.exp(-((x + 10)**2)/(2*4**2))
    ax1.fill_between(x, y, color=CYAN, alpha=0.5)
    ax1.plot(x, y, color=CYAN)
    ax1.set_title("TIE Histogram (Dual-Dirac)", color=TEXT_COLOR)
    ax1.grid(True)
    
    # Bathtub
    ax2 = fig.add_subplot(gs[1, 0])
    ui = np.linspace(-0.5, 0.5, 100)
    q = np.linspace(1, 15, 100)
    ber = 0.5 * erfc(q / np.sqrt(2))
    bathtub = np.concatenate((ber[::-1], ber))
    t = np.linspace(-0.5, 0.5, 200)
    ax2.plot(t, bathtub + 1e-18, color=COPPER, lw=2)
    ax2.set_yscale('log')
    ax2.set_ylim(1e-15, 1)
    ax2.set_title("Bathtub Curve", color=TEXT_COLOR)
    ax2.grid(True)
    
    # Spectrum
    ax3 = fig.add_subplot(gs[:, 1])
    f = np.linspace(0.1, 10, 500)
    noise = np.random.normal(0, 0.1, len(f)) - 100
    spurs = np.zeros_like(f)
    for i in [2, 4, 6]:
        idx = np.abs(f - i).argmin()
        spurs[idx] = 40
    ax3.plot(f, noise + spurs, color=CYAN, lw=1)
    ax3.set_ylim(-120, -50)
    ax3.set_title("Jitter Spectrum", color=TEXT_COLOR)
    ax3.grid(True)
    
    plt.tight_layout()
    save_fig(fig, "si_part3_jitter.jpg")

# Part 4: Equalization
def generate_part4():
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 3)
    
    # Closed Eye
    ax1 = fig.add_subplot(gs[0])
    t = np.linspace(-1, 1, 200)
    for _ in range(30):
        # Heavy ISI
        y = np.tanh(2*t) * np.random.uniform(0.1, 0.5) + np.random.normal(0, 0.1, len(t))
        ax1.plot(t, y, color=COPPER, alpha=0.3)
    ax1.set_title("Closed Eye (Lossy Channel)", color=TEXT_COLOR)
    ax1.grid(True)
    
    # Open Eye
    ax2 = fig.add_subplot(gs[1])
    for _ in range(50):
        y = np.tanh(10*t) * 0.8 + np.random.normal(0, 0.05, len(t))
        ax2.plot(t, y, color=CYAN, alpha=0.2)
        ax2.plot(t, -y, color=CYAN, alpha=0.2)
    ax2.set_title("Open Eye (CTLE + DFE)", color=TEXT_COLOR)
    ax2.grid(True)
    
    # Response
    ax3 = fig.add_subplot(gs[2])
    f = np.linspace(0.1, 20, 100)
    ch_loss = -1.2 * f
    ctle = 10 * np.log10(1 + (f/5)**2) - 10 * np.log10(1 + (f/15)**2)
    ax3.plot(f, ch_loss, color=COPPER, label="Channel Loss")
    ax3.plot(f, ctle, color=CYAN, label="CTLE Response")
    ax3.plot(f, ch_loss + ctle, color=TEXT_COLOR, ls='--', label="Net")
    ax3.legend(loc='lower left', frameon=False, labelcolor=TEXT_COLOR)
    ax3.set_title("Frequency Response", color=TEXT_COLOR)
    ax3.grid(True)
    
    plt.tight_layout()
    save_fig(fig, "si_part4_equalization.jpg")

# Part 5: SerDes
def generate_part5():
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2)
    
    # Block Diagram
    ax1 = fig.add_subplot(gs[0])
    ax1.add_patch(patches.Rectangle((0.1, 0.4), 0.2, 0.2, color=CYAN, alpha=0.3))
    ax1.text(0.2, 0.5, "PD", ha="center", va="center", color=TEXT_COLOR)
    
    ax1.add_patch(patches.Rectangle((0.4, 0.4), 0.2, 0.2, color=COPPER, alpha=0.3))
    ax1.text(0.5, 0.5, "LF", ha="center", va="center", color=TEXT_COLOR)
    
    ax1.add_patch(patches.Rectangle((0.7, 0.4), 0.2, 0.2, color=CYAN, alpha=0.3))
    ax1.text(0.8, 0.5, "VCO", ha="center", va="center", color=TEXT_COLOR)
    
    # Lines
    ax1.annotate("", xy=(0.4, 0.5), xytext=(0.3, 0.5), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.annotate("", xy=(0.7, 0.5), xytext=(0.6, 0.5), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.annotate("", xy=(0.8, 0.6), xytext=(0.8, 0.8), arrowprops=dict(arrowstyle="-", color=TEXT_COLOR))
    ax1.annotate("", xy=(0.2, 0.8), xytext=(0.8, 0.8), arrowprops=dict(arrowstyle="-", color=TEXT_COLOR))
    ax1.annotate("", xy=(0.2, 0.6), xytext=(0.2, 0.8), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.set_axis_off()
    ax1.set_title("CDR / PLL Block Diagram", color=TEXT_COLOR)
    
    # JTF Bode
    ax2 = fig.add_subplot(gs[1])
    f = np.logspace(4, 8, 100)
    w = 2 * np.pi * f
    wn = 2 * np.pi * 2e6
    zeta = 1.0
    # JTF Type II
    s = 1j * w
    jtf = (2*zeta*wn*s + wn**2) / (s**2 + 2*zeta*wn*s + wn**2)
    jtf_db = 20 * np.log10(np.abs(jtf))
    ax2.semilogx(f, jtf_db, color=CYAN, lw=2, label="Jitter Transfer")
    
    # Mask (tolerance)
    mask = np.where(f < 2e6, 20*np.log10((2e6/f)), 0)
    ax2.semilogx(f, mask, color=COPPER, ls='--', lw=2, label="Tolerance Mask")
    
    ax2.set_ylim(-20, 10)
    ax2.set_xlim(1e4, 1e8)
    ax2.grid(True, which="both")
    ax2.legend(loc='lower left', frameon=False, labelcolor=TEXT_COLOR)
    ax2.set_title("Jitter Transfer & Tolerance", color=TEXT_COLOR)
    
    plt.tight_layout()
    save_fig(fig, "si_part5_serdes.jpg")

# Part 6: Coherent Optics
def generate_part6():
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2)
    
    # 16-QAM
    ax1 = fig.add_subplot(gs[0])
    levels = [-3, -1, 1, 3]
    for i in levels:
        for q in levels:
            noise_i = np.random.normal(0, 0.15, 100)
            noise_q = np.random.normal(0, 0.15, 100)
            ax1.scatter(i + noise_i, q + noise_q, s=2, color=CYAN, alpha=0.5)
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.grid(True, alpha=0.3)
    ax1.set_title("16-QAM Constellation", color=TEXT_COLOR)
    ax1.text(-3.8, 3.5, "EVM: 6.4%", color=COPPER, fontsize=12)
    
    # MZM
    ax2 = fig.add_subplot(gs[1])
    # split
    ax2.plot([0, 1], [0, 0], color=TEXT_COLOR)
    ax2.plot([1, 2], [0, 1], color=TEXT_COLOR)
    ax2.plot([1, 2], [0, -1], color=TEXT_COLOR)
    
    # arm I
    ax2.add_patch(patches.Rectangle((2, 0.8), 2, 0.4, color=CYAN, alpha=0.3))
    ax2.text(3, 1, "MZM I", ha="center", va="center", color=TEXT_COLOR)
    
    # arm Q
    ax2.add_patch(patches.Rectangle((2, -1.2), 2, 0.4, color=COPPER, alpha=0.3))
    ax2.text(3, -1, "MZM Q", ha="center", va="center", color=TEXT_COLOR)
    
    # 90 deg
    ax2.plot([4, 5], [-1, -1], color=TEXT_COLOR)
    ax2.add_patch(patches.Rectangle((5, -1.2), 0.5, 0.4, color=TEXT_COLOR, alpha=0.3))
    ax2.text(5.25, -1, "90°", ha="center", va="center", color=TEXT_COLOR)
    
    # combine
    ax2.plot([4, 6], [1, 1], color=TEXT_COLOR)
    ax2.plot([5.5, 6], [-1, 1], color=TEXT_COLOR)
    ax2.plot([6, 7], [1, 1], color=TEXT_COLOR)
    
    ax2.set_xlim(-0.5, 7.5)
    ax2.set_ylim(-2, 2)
    ax2.axis('off')
    ax2.set_title("Nested IQ Modulator", color=TEXT_COLOR)
    
    plt.tight_layout()
    save_fig(fig, "si_part6_optics.jpg")

def generate_all():
    generate_part3()
    generate_part4()
    generate_part5()
    generate_part6()

if __name__ == '__main__':
    generate_all()
