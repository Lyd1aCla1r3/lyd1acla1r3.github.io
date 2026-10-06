import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
from scipy.special import erfc
import scipy.signal as signal
import os
import io
from PIL import Image

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
    "lines.linewidth": 1.5,
})

OUT_DIR = "/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/images"
os.makedirs(OUT_DIR, exist_ok=True)
generated_files = []

# For M3 Compositing
BG_IMAGE_PATH = os.path.join(OUT_DIR, "lab_bench_etched.jpg")

def composite_m3(fig, out_filename):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=BG_COLOR, edgecolor='none', dpi=150)
    buf.seek(0)
    plt.close(fig)
    
    plot_img = Image.open(buf).convert("RGBA")
    
    try:
        bg = Image.open(BG_IMAGE_PATH).convert("RGBA")
        # Dim background
        bg = bg.point(lambda p: p * 0.4)
        
        bg_w, bg_h = bg.size
        plot_w, plot_h = plot_img.size
        
        if plot_w > bg_w or plot_h > bg_h:
            scale = max(plot_w/bg_w, plot_h/bg_h)
            bg = bg.resize((int(bg_w*scale), int(bg_h*scale)), Image.LANCZOS)
            bg_w, bg_h = bg.size
            
        offset = ((bg_w - plot_w) // 2, (bg_h - plot_h) // 2)
        bg.paste(plot_img, offset, plot_img)
        final_img = bg.convert("RGB")
    except Exception as e:
        print(f"Failed M3 composite: {e}")
        final_img = plot_img.convert("RGB")
        
    out_path = os.path.join(OUT_DIR, out_filename)
    final_img.save(out_path, quality=95)
    generated_files.append(out_path)

def save_fig(fig, out_filename):
    out_path = os.path.join(OUT_DIR, out_filename)
    fig.savefig(out_path, bbox_inches='tight', facecolor=BG_COLOR, edgecolor='none', dpi=150)
    plt.close(fig)
    generated_files.append(out_path)

def generate_cover_eye():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    # Channel frequency response
    f = np.linspace(0.1, 20, 1000)
    loss_dB = 12 * (0.20 * np.sqrt(f/5) + 0.47 * (f/5)) # From Ch14 exact formula
    H_mag = 10 ** (-loss_dB / 20)
    
    np.random.seed(42)
    sps = 32
    bits = np.random.randint(0, 2, 2000)*2 - 1
    tx = np.repeat(bits, sps)
    
    # Simple lowpass to emulate dispersion (exact causal tail is complex, use butterworth for this specific visual)
    b, a = signal.butter(2, 0.1)
    rx = signal.lfilter(b, a, tx)
    rx += np.random.normal(0, 0.02, len(rx))
    
    for i in range(2, len(bits)-2):
        start = i * sps - sps//2
        end = i * sps + int(1.5*sps)
        t_plot = np.linspace(-0.5, 1.5, end-start)
        ax.plot(t_plot, rx[start:end], color=CYAN, alpha=0.05, linewidth=1.0)
        
    # Mask
    mask_poly = plt.Polygon([[-0.2, -0.4], [0.2, -0.4], [0.35, 0], [0.2, 0.4], [-0.2, 0.4], [-0.35, 0]], 
                            closed=True, fill=True, facecolor=GRATICULE, alpha=0.6, edgecolor=COPPER, linewidth=2)
    ax.add_patch(mask_poly)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title("NRZ EYE DIAGRAM", color=CYAN, loc='left')
    composite_m3(fig, "signal_integrity_cover.jpg")

def generate_part1():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    h, w = 2.0, 4.0
    ax.add_patch(patches.Rectangle((-5, -0.5), 10, 0.5, color=GRATICULE)) 
    ax.add_patch(patches.Rectangle((-5, 0), 10, h, color="#111a2a")) 
    ax.add_patch(patches.Rectangle((-w/2, h), w, 0.2, color=COPPER)) 
    
    x = np.linspace(-5, 5, 200)
    y = np.linspace(0.1, 5, 200)
    X, Y = np.meshgrid(x, y)
    Ex, Ey = np.zeros_like(X), np.zeros_like(X)
    Hx, Hy = np.zeros_like(X), np.zeros_like(X)
    
    qs = np.linspace(-w/2, w/2, 50)
    for qx in qs:
        dx1 = X - qx
        dy1 = Y - h
        r1_sq = dx1**2 + dy1**2 + 1e-6
        Ex += dx1 / r1_sq
        Ey += dy1 / r1_sq
        dy2 = Y + h
        r2_sq = dx1**2 + dy2**2 + 1e-6
        Ex -= dx1 / r2_sq
        Ey -= dy2 / r2_sq
        
        Hx -= dy1 / r1_sq
        Hy += dx1 / r1_sq
        Hx -= dy2 / r2_sq
        Hy += dx1 / r2_sq
        
    ax.streamplot(X, Y, Ex, Ey, color=CYAN, density=1.0, linewidth=1, arrowsize=1)
    ax.streamplot(X, Y, Hx, Hy, color=COPPER, density=0.8, linewidth=1, arrowsize=1)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-0.5, 5)
    ax.axis('off')
    composite_m3(fig, "si_part1_electromagnetic.jpg")

def generate_part2():
    fig = plt.figure(figsize=(12, 6), dpi=150)
    gs = gridspec.GridSpec(1, 3)
    
    ax1 = fig.add_subplot(gs[0])
    f = np.linspace(0.1, 20, 200)
    s21_db = -(12 * (0.20 * np.sqrt(f/5) + 0.47 * (f/5)))
    ax1.plot(f, s21_db, color=CYAN, lw=2)
    ax1.set_title("S21 Insertion Loss")
    
    ax2 = fig.add_subplot(gs[1])
    ax2.add_patch(patches.Circle((0, 0), 1, fill=False, color=GRATICULE))
    for r in [0.2, 0.5, 1.0, 2.0]:
        ax2.add_patch(patches.Circle((r/(1+r), 0), 1/(1+r), fill=False, color=GRATICULE, alpha=0.5))
    f_smith = np.linspace(0.1, 15, 200)
    Z_C = 1 / (1j * 2 * np.pi * f_smith * 1e9 * 0.37e-12)
    Z_L = 1j * 2 * np.pi * f_smith * 1e9 * 1.33e-9
    Z_in = 50 + Z_L + 1/(1/50 + 1/Z_C)
    Gamma = (Z_in - 50) / (Z_in + 50)
    ax2.plot(np.real(Gamma), np.imag(Gamma), color=COPPER, lw=2)
    ax2.axis('off')
    ax2.set_title("S11 Smith Chart")
    
    ax3 = fig.add_subplot(gs[2])
    t = np.linspace(0, 10, 500)
    v_dip = -0.30 * (1 - np.exp(-(t-2)/0.2)) * (t > 2) * np.exp(-(t-2)/0.8)
    v_bump = +0.40 * (1 - np.exp(-(t-5)/0.3)) * (t > 5) * np.exp(-(t-5)/0.9)
    v_total = v_dip + v_bump
    Z_tdr = 50 * (0.5 + v_total) / (0.5 - v_total)
    ax3.plot(t, Z_tdr, color=CYAN, lw=2)
    ax3.set_ylim(20, 80)
    ax3.set_title("TDR Impedance")
    composite_m3(fig, "si_part2_measurement.jpg")

def generate_part3():
    fig = plt.figure(figsize=(12, 8), dpi=150)
    gs = gridspec.GridSpec(2, 2)
    
    ax1 = fig.add_subplot(gs[0, 0])
    x = np.linspace(-30, 30, 200)
    DJ, RJ = 12.0, 1.5
    y = 0.5/(RJ*np.sqrt(2*np.pi)) * np.exp(-((x - DJ/2)**2)/(2*RJ**2)) + \
        0.5/(RJ*np.sqrt(2*np.pi)) * np.exp(-((x + DJ/2)**2)/(2*RJ**2))
    ax1.fill_between(x, y, color=CYAN, alpha=0.5)
    ax1.set_title("TIE Histogram")
    
    ax2 = fig.add_subplot(gs[1, 0])
    q = np.linspace(0, 15, 100)
    ber = 0.5 * erfc(q / np.sqrt(2))
    tj_right = DJ/2 + q * RJ
    tj_left = -DJ/2 - q * RJ
    ax2.plot(tj_right, ber + 1e-20, color=COPPER)
    ax2.plot(tj_left, ber + 1e-20, color=COPPER)
    ax2.set_yscale('log')
    ax2.set_ylim(1e-15, 1)
    ax2.set_title("Bathtub Curve")
    
    ax3 = fig.add_subplot(gs[:, 1])
    f = np.linspace(0.1, 10, 500)
    noise = np.random.normal(0, 1.5, len(f)) - 100
    spurs = np.zeros_like(f)
    spurs[100], spurs[200], spurs[300] = 40, 30, 20
    ax3.plot(f, noise + spurs, color=CYAN, lw=1)
    ax3.set_ylim(-120, -50)
    ax3.set_title("Jitter Spectrum")
    composite_m3(fig, "si_part3_jitter.jpg")

def generate_part4():
    fig = plt.figure(figsize=(12, 6), dpi=150)
    gs = gridspec.GridSpec(1, 3)
    
    sps = 32
    t = np.linspace(-0.5, 1.5, int(2.0*sps))
    
    np.random.seed(42)
    bits = np.random.randint(0, 2, 500)*2 - 1
    tx = np.repeat(bits, sps)
    b, a = signal.butter(1, 0.05)
    rx_closed = signal.lfilter(b, a, tx)
    
    ax1 = fig.add_subplot(gs[0])
    for i in range(2, len(bits)-2):
        start = i * sps - sps//2
        end = i * sps + int(1.5*sps)
        ax1.plot(t, rx_closed[start:end], color=COPPER, alpha=0.1)
    ax1.set_title("Closed Eye")
    
    rx_open = rx_closed - 0.7 * np.concatenate([[0]*sps, rx_closed[:-sps]])
    ax2 = fig.add_subplot(gs[1])
    for i in range(2, len(bits)-2):
        start = i * sps - sps//2
        end = i * sps + int(1.5*sps)
        ax2.plot(t, rx_open[start:end], color=CYAN, alpha=0.1)
    ax2.set_title("Open Eye (CTLE + DFE)")
    
    ax3 = fig.add_subplot(gs[2])
    f = np.linspace(0.1, 15, 100)
    ch_loss = -(12 * (0.20 * np.sqrt(f/5) + 0.47 * (f/5)))
    ctle = 12.04 * np.log10(1 + (f/6)**2) - 12.04 * np.log10(1 + (f/15)**2)
    ax3.plot(f, ch_loss, color=COPPER, label="Channel")
    ax3.plot(f, ctle, color=CYAN, label="CTLE")
    ax3.plot(f, ch_loss + ctle, color=TEXT_COLOR, ls='--', label="Net")
    ax3.set_title("CTLE Response")
    composite_m3(fig, "si_part4_equalization.jpg")

def generate_part5():
    fig = plt.figure(figsize=(12, 6), dpi=150)
    gs = gridspec.GridSpec(1, 2)
    
    ax1 = fig.add_subplot(gs[0])
    ax1.add_patch(patches.Rectangle((0.1, 0.4), 0.2, 0.2, color=CYAN, alpha=0.3))
    ax1.text(0.2, 0.5, "PD", ha="center", va="center", color=TEXT_COLOR)
    ax1.add_patch(patches.Rectangle((0.4, 0.4), 0.2, 0.2, color=COPPER, alpha=0.3))
    ax1.text(0.5, 0.5, "LF", ha="center", va="center", color=TEXT_COLOR)
    ax1.add_patch(patches.Rectangle((0.7, 0.4), 0.2, 0.2, color=CYAN, alpha=0.3))
    ax1.text(0.8, 0.5, "VCO", ha="center", va="center", color=TEXT_COLOR)
    ax1.annotate("", xy=(0.4, 0.5), xytext=(0.3, 0.5), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.annotate("", xy=(0.7, 0.5), xytext=(0.6, 0.5), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.plot([0.8, 0.8], [0.5, 0.2], color=TEXT_COLOR)
    ax1.plot([0.8, 0.15], [0.2, 0.2], color=TEXT_COLOR)
    ax1.annotate("", xy=(0.15, 0.4), xytext=(0.15, 0.2), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax1.set_axis_off()
    ax1.set_title("CDR / PLL Block Diagram")
    
    ax2 = fig.add_subplot(gs[1])
    f = np.logspace(4, 8, 100)
    s = 1j * 2 * np.pi * f
    wn = 2 * np.pi * 2e6
    zeta = 1.0
    jtf = (2*zeta*wn*s + wn**2) / (s**2 + 2*zeta*wn*s + wn**2)
    ax2.semilogx(f, 20 * np.log10(np.abs(jtf)), color=CYAN, lw=2)
    ax2.semilogx(f, np.where(f < 2e6, 20*np.log10((2e6/f)), 0), color=COPPER, ls='--', lw=2)
    ax2.set_ylim(-20, 10)
    ax2.set_title("Jitter Transfer")
    composite_m3(fig, "si_part5_serdes.jpg")

def generate_part6():
    fig = plt.figure(figsize=(12, 6), dpi=150)
    gs = gridspec.GridSpec(1, 2)
    
    ax1 = fig.add_subplot(gs[0])
    levels = [-3, -1, 1, 3]
    for i in levels:
        for q in levels:
            ax1.scatter(i + np.random.normal(0, 0.15, 50), q + np.random.normal(0, 0.15, 50), s=2, color=CYAN, alpha=0.5)
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_title("16-QAM Constellation")
    
    ax2 = fig.add_subplot(gs[1])
    ax2.add_patch(patches.Rectangle((2, 0.8), 2, 0.4, color=CYAN, alpha=0.3))
    ax2.text(3, 1, "MZM I", ha="center", va="center", color=TEXT_COLOR)
    ax2.add_patch(patches.Rectangle((2, -1.2), 2, 0.4, color=COPPER, alpha=0.3))
    ax2.text(3, -1, "MZM Q", ha="center", va="center", color=TEXT_COLOR)
    ax2.add_patch(patches.Rectangle((5, -1.2), 0.5, 0.4, color=TEXT_COLOR, alpha=0.3))
    ax2.text(5.25, -1, "90°", ha="center", va="center", color=TEXT_COLOR)
    ax2.axis('off')
    ax2.set_title("Nested IQ Modulator")
    composite_m3(fig, "si_part6_coherent_optics.jpg")

def gen_qa01():
    fig, ax = plt.subplots(figsize=(6, 4))
    circle = patches.Circle((0, 0), 1, fill=False, color=COPPER, lw=2)
    ax.add_patch(circle)
    ax.text(0, 0.5, "Eddy\nLoop", color=CYAN, ha="center")
    ax.annotate("Primary B", xy=(0, 0), xytext=(0, 0.2), arrowprops=dict(arrowstyle="->", color=TEXT_COLOR))
    ax.annotate("Induced E", xy=(1, 0), xytext=(1, 0.2), arrowprops=dict(arrowstyle="->", color=CYAN))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    save_fig(fig, "fig_qa01_eddy.jpg")

def gen_qa05():
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([0, 4], [1, 1], color=COPPER, lw=3, label="Wire A (Aggressor)")
    ax.plot([0, 4], [0, 0], color=CYAN, lw=3, label="Wire B (Victim)")
    ax.plot([-0.5, 4.5], [-0.5, -0.5], color=GRATICULE, lw=1)
    ax.text(2, -0.7, "Desk (Ground)", color=TEXT_COLOR, ha="center")
    ax.legend(frameon=False, labelcolor=TEXT_COLOR)
    ax.set_xlim(-1, 5)
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
    save_fig(fig, "fig_tdr_staircase.jpg")

def gen_gibbs():
    fig, ax = plt.subplots(figsize=(6, 4))
    t = np.linspace(0, 1, 200)
    y = np.zeros_like(t)
    for n in range(1, 15, 2):
        y += (4/(np.pi*n)) * np.sin(2*np.pi*n*t)
    ax.plot(t, y, color=CYAN, lw=2)
    ax.set_title("Step Synthesis & Gibbs", color=TEXT_COLOR)
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

def gen_iq():
    fig, ax = plt.subplots(figsize=(4, 4))
    levels = [-3, -1, 1, 3]
    for i in levels:
        for q in levels:
            ax.scatter(i, q, color=CYAN)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.set_title("IQ Constellation", color=TEXT_COLOR)
    save_fig(fig, "fig_iq_constellation.jpg")

def make_contact_sheet():
    cols = 4
    rows = (len(generated_files) + cols - 1) // cols
    fig = plt.figure(figsize=(16, 4*rows))
    for i, path in enumerate(generated_files):
        img = Image.open(path)
        ax = fig.add_subplot(rows, cols, i+1)
        ax.imshow(img)
        ax.axis('off')
        ax.set_title(os.path.basename(path), color=TEXT_COLOR)
    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "contact_sheet.jpg"), facecolor=BG_COLOR)
    plt.close(fig)

if __name__ == '__main__':
    generate_cover_eye()
    generate_part1()
    generate_part2()
    generate_part3()
    generate_part4()
    generate_part5()
    generate_part6()
    
    gen_qa01()
    gen_qa05()
    gen_tdr()
    gen_gibbs()
    gen_sparam()
    gen_next()
    gen_fir()
    gen_iq()
    
    make_contact_sheet()
    print("Done")
