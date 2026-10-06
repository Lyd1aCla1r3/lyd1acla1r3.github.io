# Jitter Decomposition and Measurement

<!-- SUMMARY: Jitter is the deviation of a signal edge from its ideal position in time, and no single number for total jitter provides enough information to diagnose a failing link. This guide decomposes total jitter into random and deterministic components based on their statistical behavior and physical origins, transforming an opaque timing failure into actionable hardware diagnostics. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

Jitter is the deviation of a signal edge from its ideal position in time. At modern serial data rates, no single number for "total jitter" provides enough information to diagnose a failing link. A signal that misses its timing budget could be failing because of thermal noise in the silicon, because of impedance discontinuities on the PCB, because of switching power supply coupling, or because of asymmetric transistor drive strength in the transmitter. Each of these root causes produces a physically distinct timing perturbation, and each requires a different corrective action.

The jitter decomposition framework separates total jitter into categories based on the statistical behavior and physical origin of each component. Random Jitter arises from thermodynamic processes that are fundamentally unbounded and Gaussian. Deterministic Jitter arises from structural and environmental sources that are bounded and repeatable. Within Deterministic Jitter, further sub-classification isolates pattern-dependent effects (Intersymbol Interference, Duty Cycle Distortion) from pattern-independent periodic disturbances (power supply coupling, EMI, clock crosstalk). This taxonomy transforms an opaque timing failure into a set of actionable hardware diagnostics.

This guide covers the physical origins of each jitter component, the measurement infrastructure that captures them, and the statistical properties that make decomposition possible.

## Core Concepts

### The Decomposition Taxonomy

All jitter falls into two primary categories, distinguished by their probability distributions:

**Random Jitter (RJ)** is caused by fundamental thermodynamic processes: thermal noise (Johnson-Nyquist noise from resistive elements), shot noise (discrete charge carriers crossing semiconductor junctions), and flicker noise (1/f noise in active devices). These microscopic processes involve the aggregate behavior of billions of independent electrons. The Central Limit Theorem guarantees that the sum of billions of independent random events produces a macroscopic distribution that follows a Gaussian probability curve with mathematical precision.

The critical property of RJ is that it is unbounded. The Gaussian distribution has tails that extend to infinity in both directions. Measuring for a longer duration does not change the underlying distribution; it simply reveals increasingly rare events further out in the tails. A peak-to-peak measurement of RJ is therefore meaningless because the observed peak-to-peak value grows without limit as the sample size increases. RJ is quantified exclusively by its standard deviation, $RJ_{\text{rms}}$, which is a fixed physical constant determined by the temperature and material properties of the silicon.

**Deterministic Jitter (DJ)** is caused by predictable, systemic characteristics of the hardware, channel, and electromagnetic environment. DJ is bounded: it has strict physical minimum and maximum limits that do not grow with observation time. DJ is quantified as a peak-to-peak value, $DJ_{\text{p-p}}$.

DJ decomposes further into sub-categories that isolate specific hardware mechanisms:

- **Data Dependent Jitter (DDJ)** is correlated to the transmitted bit sequence. It encompasses Intersymbol Interference (ISI) and Duty Cycle Distortion (DCD).
- **Periodic Jitter (PJ)** is uncorrelated to the data but repeats at a fixed frequency driven by an external oscillating source.

### Random Jitter: Physics and Statistical Invariance

Thermal noise originates from the random thermal agitation of electrons colliding with atoms in the silicon lattice and copper interconnect. This is a voltage (amplitude) perturbation, not a timing perturbation. The physical mechanism that converts amplitude noise into timing jitter is the finite slew rate of the signal edge.

A high-speed signal edge is not a perfect vertical transition; it traverses from the low voltage rail to the high voltage rail over a finite time interval, producing a slope (dV/dt). When random voltage noise superimposes on the data signal during this transition, the combined voltage ($V_{\text{received}} = V_{\text{data}} + V_{\text{noise}}$) shifts the point at which the edge crosses the receiver's decision threshold. A negative noise spike during a rising edge pulls the combined voltage downward, forcing the signal to travel further along its slope before reaching the threshold. The crossing point shifts to the right in time. A positive noise spike accelerates the crossing to the left. This geometric relationship between voltage perturbation and timing shift is called amplitude-to-phase conversion.

The Gaussian distribution of the underlying voltage noise maps directly through this conversion into a Gaussian distribution of timing jitter. The shape of the distribution is preserved because the conversion is linear over the small perturbation range near the threshold crossing.

RJ is fundamentally uncorrelated and memoryless. The thermal agitation that shifts the current edge has no physical mechanism to influence the position of the next edge. Each edge crossing is an independent statistical trial drawn from the same Gaussian distribution. This is the defining contrast with ISI, where the timing of the current edge is strictly dictated by the history of preceding bits.

### $RJ_{\text{rms}}$ as a Physical Time Coordinate

$RJ_{\text{rms}}$ is not a count of edge crossings. It is a physical time distance on the horizontal axis of the TIE histogram, measured in picoseconds.

$RJ_{\text{rms}}$ equals exactly one standard deviation ($1\sigma$) of the Gaussian distribution. Geometrically, it defines the distance from the center peak of the Gaussian to the inflection point where the curve transitions from concave-down to concave-up. The mathematics of the Gaussian function dictate that 34.1% of all edge crossings will fall within one $\sigma$ on either side of the mean, totaling 68.2% within the $\pm 1\sigma$ window.

The stability of $RJ_{\text{rms}}$ as a measurement derives from a fundamental property of the Gaussian distribution: its variance converges. Variance is the expected value of the squared distance from the mean, weighted by the probability of landing at each distance. While the squared distance grows quadratically ($x^2$) as you move further from the center, the probability of landing at that distance decays exponentially ($e^{-x^2}$). Exponential decay dominates quadratic growth at every scale. By the time an outlier event occurs far out in the tail, its probability is so vanishingly small that multiplying it by the large squared distance contributes effectively zero to the total variance sum. The mathematical series converges, and the standard deviation reaches a fixed value determined by the physics of the noise source, not by how long the oscilloscope runs.

This convergence is what allows $RJ_{\text{rms}}$ to serve as the input to BER extrapolation. The static $RJ_{\text{rms}}$ constant is multiplied by a Q-factor (derived from the complementary error function for a target BER) to predict the peak-to-peak Random Jitter spread at any desired confidence level. For a BER of $10^{-12}$, the Q-factor is 7.03, and the total multiplier is $2Q \approx 14$, accounting for both the early and late tails of the distribution.

### Intersymbol Interference (ISI)

ISI is the dominant source of jitter in modern high-speed serial links. It arises because the physical channel (PCB traces, vias, cables, connectors) acts as a low-pass filter that attenuates high-frequency signal components more aggressively than low-frequency components.

Three physical mechanisms produce this frequency-dependent attenuation:

1. **Skin effect:** At high frequencies, eddy currents force the signal current to the extreme outer perimeter of the copper conductor. The usable cross-sectional area shrinks, and the effective resistance increases proportionally. The skin depth is inversely proportional to the square root of frequency, so a 10 GHz signal component encounters dramatically higher resistance than a 1 GHz component traveling the same trace.

2. **Dielectric loss:** The FR4 or advanced laminate material absorbs electromagnetic energy and dissipates it as heat. The absorption increases with frequency, further attenuating high-frequency components.

3. **Parasitic capacitance:** The copper trace above the ground plane forms a distributed capacitor that resists instantaneous voltage changes. Charging a capacitor instantaneously requires infinite current; the finite drive strength of the transmitter limits the achievable slew rate, governed by the local RC time constant.

The interaction between these mechanisms and the data pattern is what creates ISI:

A long run of identical bits (such as `00000`) acts as a near-DC signal. The channel's distributed capacitance has ample time to fully charge or discharge to the absolute voltage rail. The signal reaches maximum amplitude.

An alternating `10101` pattern represents the highest-frequency content the link carries (the Nyquist rate). The transmitter pulls the voltage upward, but before the parasitic capacitance can charge to full amplitude, the transmitter reverses direction and pulls the voltage back down. The peak-to-peak voltage swing of the alternating pattern is substantially attenuated compared to the low-frequency run.

When the data transitions from a long run of zeros to a one (`000001`), the voltage must climb from a deeply discharged state. It has a longer voltage distance to travel to reach the receiver's decision threshold compared to a transition following an alternating pattern, which started from a shallower voltage. The transmitter's slew rate is fixed by the silicon, so traversing a longer voltage distance requires more time. The edge crosses the threshold later than it would in the alternating-pattern case. This pattern-dependent timing shift is ISI jitter.

### Duty Cycle Distortion (DCD)

DCD occurs when the duration of a logic "1" does not equal the duration of a logic "0." Two distinct physical mechanisms produce DCD:

**Transmitter slew rate asymmetry:** If the P-channel pull-up transistor in the CMOS output driver has different drive strength than the N-channel pull-down transistor, rising edges will slew at a different rate than falling edges. The faster edge crosses the threshold earlier; the slower edge crosses later. The resulting jitter histogram shows a systematic offset between rising-edge and falling-edge crossing times.

**Receiver threshold offset:** Even if the transmitter generates a perfectly symmetrical waveform, a DC offset in the receiver's decision threshold voltage will create apparent DCD. If the threshold is shifted upward from the true center of the waveform, the receiver intersects the rising edge later (higher on its slope) and the falling edge earlier (higher on its slope). The receiver interprets the logic "1" as shorter in duration and the logic "0" as longer. The hardware is flawless; the measurement reference point is wrong.

### Periodic Jitter (PJ)

Periodic Jitter is uncorrelated to the data pattern but repeats at a fixed, identifiable frequency. It is caused by external oscillating sources coupling into the signal path:

- Switching power supply noise at the regulator's switching frequency
- Electromagnetic interference from nearby circuits or external sources
- Crosstalk from an adjacent clock signal routed on the PCB
- A PLL that has not achieved stable phase lock, causing the recovered clock to oscillate around its target frequency

PJ appears in the frequency domain as sharp spectral spikes at the interfering source's frequency, rising distinctly above the broadband noise floor of RJ.

### RJ Symmetry vs. DJ Asymmetry

The decomposition taxonomy rests on a fundamental physical asymmetry between the two primary categories.

Random Jitter is guaranteed to follow a perfectly symmetric Gaussian curve. The microscopic thermodynamic processes that generate it possess no directional bias. An electron is exactly as likely to experience a positive thermal perturbation as a negative one. The resulting timing distribution is centered on the ideal crossing time with identical tails on both sides.

Deterministic Jitter can be profoundly asymmetric. DCD from a stronger pull-up transistor will concentrate rising-edge crossings early and falling-edge crossings late, producing a lopsided histogram. ISI from a specific via reflection may interfere strongly with one bit transition pattern (`001`) while leaving the complementary pattern (`110`) unaffected, creating a heavy concentration of delayed edges on one side of the distribution.

This physical asymmetry is precisely why measurement algorithms cannot assume a simple symmetric distribution for total jitter. The Dual-Dirac model, covered in detail in [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md), addresses this by placing two independent impulses that need not be equidistant from the ideal crossing, nor carry equal populations of hits.

## Worked Examples

### Time Interval Error (TIE) Measurement

The measurement infrastructure for jitter decomposition begins with Time Interval Error.

The oscilloscope digitizes the incoming voltage waveform at high sample rates and mathematically interpolates the precise moment each edge crosses the differential zero-volt threshold (or the single-ended decision threshold). Simultaneously, the instrument runs a software Phase-Locked Loop on the captured data to generate a perfect, ideal recovered clock.

For each edge, the instrument subtracts the ideal clock time from the actual edge crossing time. The resulting difference is the TIE for that specific transition. A positive TIE means the edge arrived late (lagging the ideal clock). A negative TIE means the edge arrived early (leading the ideal clock). The zero point on the TIE axis is not absolute zero time; it is the relative reference defined by the ideal recovered clock.

The oscilloscope accumulates millions of TIE values and bins them into a histogram. The horizontal axis is time (divided into femtosecond or picosecond bins), and the vertical axis is the count of edge crossings that landed in each bin.

### Normalizing to a Probability Density Function

To perform mathematical operations on the histogram, the oscilloscope normalizes the raw hit counts into a Probability Density Function (PDF).

Each bin's hit count is divided by the total number of edges captured in the entire measurement run. The vertical axis transforms from integer counts to probability density. The total area under the normalized curve equals exactly 1.0, representing the certainty that every edge must land somewhere on the time axis.

The resulting PDF is the convolution of the DJ distribution with the RJ Gaussian distribution. The full measured histogram reflects the combined effect of all jitter sources acting simultaneously on every edge crossing.

### Extracting $RJ_{\text{rms}}$ from the Histogram Tails

The extraction of Random Jitter exploits the bounded nature of Deterministic Jitter.

DJ has absolute physical limits. No matter how many edges are captured, no DJ mechanism can push an edge beyond its maximum displacement. Therefore, the extreme left and right tails of the TIE histogram are entirely free of DJ influence. Every edge crossing that lands far enough from center arrived there solely because of unbounded Random Jitter.

The oscilloscope algorithm isolates these far tails and fits a standard Gaussian function to each one using least-squares regression. The fit solves for the standard deviation $\sigma$, which is $RJ_{\text{rms}}$, and the mean of each fitted Gaussian, whose separation defines $DJ_{\delta\delta}$ in the Dual-Dirac framework. The algorithm deliberately ignores the complex, multi-modal center of the histogram where DJ and RJ contributions are entangled.

### TJ Extrapolation

With $RJ_{\text{rms}}$ and $DJ_{\delta\delta}$ extracted, the oscilloscope calculates Total Jitter at any target BER without requiring hours of measurement to observe trillions of bits directly:

$$TJ(BER) = DJ_{\delta\delta} + 2 \cdot Q \cdot RJ_{\text{rms}}$$

For a BER of $10^{-12}$, $Q \approx 7.03$, giving $2Q \approx 14$. The total jitter at $10^{-12}$ BER is $DJ_{\delta\delta} + 14 \cdot RJ_{\text{rms}}$.

This formula reflects the physical reality that a bit error occurs when an edge shifts past the receiver's sampling threshold. The probability of that event is the area under the Gaussian tail beyond the threshold coordinate. The Q-factor, derived from the complementary error function (erfc), is the number of standard deviations required to leave exactly the target BER's worth of area in the tail. The detailed derivation of the Q-factor and erfc is covered in [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md).

## Architecture

### The Jitter Tree

The full decomposition hierarchy forms a tree that maps every timing perturbation to a measurable root cause:

```
Total Jitter (TJ)
├── Random Jitter (RJ)
│   └── Gaussian, unbounded, quantified by RJ_rms
│       Sources: thermal noise, shot noise, flicker noise
│
└── Deterministic Jitter (DJ)
    ├── Data Dependent Jitter (DDJ)
    │   ├── Intersymbol Interference (ISI)
    │   │   └── Channel low-pass filtering, reflections
    │   └── Duty Cycle Distortion (DCD)
    │       └── Slew rate asymmetry, threshold offset
    │
    └── Periodic Jitter (PJ)
        └── Power supply, EMI, clock crosstalk, PLL instability
```

Each leaf of the tree corresponds to a distinct physical mechanism and a distinct corrective action. ISI is addressed through channel design improvements or equalization. DCD is addressed through transmitter calibration or receiver threshold adjustment. PJ is addressed by identifying and decoupling the interfering oscillating source. RJ is addressed only by reducing the operating temperature or changing the semiconductor process, neither of which is typically practical, so RJ is treated as a fixed noise floor in the jitter budget.

### Measurement Flow: From TIE to Root Cause

The oscilloscope decomposes total jitter through a layered measurement process:

1. **Capture TIE values** for every edge crossing in the measurement window.
2. **Construct the TIE histogram** and normalize to a probability density function.
3. **Fit Gaussians to the extreme tails** to extract $RJ_{\text{rms}}$ and $DJ_{\delta\delta}$.
4. **Record the TIE Track** (chronological TIE values vs. time) to preserve temporal ordering.
5. **Apply synchronous pattern averaging** on the TIE Track over many repetitions of a known test pattern (such as PRBS-7) to isolate DDJ. Uncorrelated components (RJ and PJ) average to zero; only the pattern-correlated ISI and DCD survive.
6. **Subtract DDJ from the TIE Track** to produce the uncorrelated jitter residual.
7. **Apply FFT to the residual** to separate PJ (sharp spectral spikes at specific frequencies) from RJ (flat broadband noise floor).

The full detail of steps 4 through 7, including test pattern selection (PRBS-7/15/31), pattern averaging mathematics, and FFT spectral analysis, is covered in [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md).

### Differential Noise Cancellation

Differential signaling provides a natural defense against common-mode interference. If electromagnetic noise couples equally onto both the D+ and D- traces of a differential pair, it appears as common-mode noise. The differential receiver measures only the difference between the two traces ($V_{D+} - V_{D-}$). Equal noise on both lines cancels exactly, leaving the data signal undisturbed.

An analogous mechanism operates in source-synchronous architectures such as DDR memory. If low-frequency jitter affects both the data line and the forwarded clock identically, the receiver's sampling clock shifts in perfect lockstep with the data drift. The phase relationship between data and clock remains constant, and the jitter is effectively neutralized. This cancellation fails when the jitter source affects data and clock differently, as occurs when high-frequency jitter exceeds the bandwidth of the forwarded clock path.

## Edge Cases

### ISI and the Closed Eye

In a functioning link, ISI shifts the threshold crossing by a fraction of the Unit Interval. The signal still reaches the decision threshold within the allotted bit period, but it arrives late (or early), contributing deterministic jitter to the timing budget.

If channel attenuation is severe enough, the signal may fail to reach the threshold entirely. The voltage begins climbing from a deeply discharged state after a long run of opposite bits, the bit period expires, and the transmitter reverses direction before the voltage crosses the threshold. The receiver samples a value on the wrong side of the decision boundary and records a bit error. On an oscilloscope, the eye diagram is physically closed: the voltage trajectories overlap and no open region remains for the receiver to sample cleanly.

This failure mode is the direct motivation for transmitter pre-emphasis (Feed-Forward Equalization) and receiver equalization (CTLE and DFE). Equalizers artificially boost high-frequency transition energy to guarantee threshold crossing regardless of the preceding bit history. Equalization is covered in [Transmitter FFE](../04_Equalization_and_Receiver_Architecture/13_Transmitter_FFE.md) and [CTLE and DFE](../04_Equalization_and_Receiver_Architecture/14_CTLE_and_DFE.md).

### Peak-to-Peak RJ: A Defined Quantity, Not a Measured One

A common source of confusion is the notion that Random Jitter should have a measurable peak-to-peak value. The Gaussian distribution extends to infinity; there is no maximum displacement. Any peak-to-peak RJ number reported by an instrument is not a direct measurement but a statistical calculation: $RJ_{\text{p-p}} = 2Q \cdot RJ_{\text{rms}}$, where $Q$ is chosen for a specific target BER. Changing the target BER changes the reported peak-to-peak value, even though the underlying physical noise source has not changed. The $RJ_{\text{rms}}$ constant is the only measurement that reflects the true physics; the peak-to-peak value is a derived statistical projection.

### The Dual-Dirac Approximation and Its Limits

The Dual-Dirac model simplifies the entire complex DJ distribution into two Dirac delta impulses separated by $DJ_{\delta\delta}$. This is a worst-case simplification: it concentrates all DJ energy at two extreme points, producing the widest possible convolution with the RJ Gaussian. The model is mathematically convenient and adopted by industry standards (PCIe, Fibre Channel), but it can overestimate total jitter when the actual DJ distribution is spread across many smaller values rather than concentrated at two extremes. The full treatment of Dual-Dirac model mechanics, including asymmetric delta placement, constrained fitting, and Q-factor normalization, is in [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md).
