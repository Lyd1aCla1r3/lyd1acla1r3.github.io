# Dual-Dirac Model and BER Extrapolation

<!-- SUMMARY: The Dual-Dirac model approximates the total jitter probability density function as two Gaussian distributions separated by the deterministic jitter component, enabling bit error ratio extrapolation to target rates as low as 1e-12 from feasible measurement sample sizes. This guide derives the model, its mathematical assumptions, and the bathtub curve construction that links timing margin to error probability. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

High-speed serial standards specify compliance at Bit Error Rates that are impossible to observe directly. PCIe Gen 4 requires $10^{-12}$, meaning only one bit in a trillion may arrive outside the timing window. At 16 GT/s, accumulating a trillion bits takes over 60 seconds of continuous transmission, and observing even a single error at that rate requires statistical patience that exceeds practical measurement timescales by orders of magnitude. The fundamental problem is not measurement speed; it is that the BER target describes an event so rare that the Gaussian tail governing its probability has never been directly populated in the captured histogram.

The Dual-Dirac model resolves this by exploiting a structural property of the Gaussian distribution: the shape of the unmeasured tail is mathematically determined by the measurable center. The model decomposes the total jitter histogram into two Gaussian populations anchored at the Deterministic Jitter boundaries, fits the visible tail slopes to extract a single Random Jitter standard deviation, and then uses the complementary error function to project that standard deviation outward to the target BER. The result is a Total Jitter number at $10^{-12}$ (or any other target) derived from a measurement of a few hundred thousand edges, not a trillion.

This guide covers the physical and mathematical machinery of the Dual-Dirac model: why the Gaussian tail shape is locked by the center mass, how the complementary error function maps between tail area and boundary position, how the Q-factor normalizes this mapping into a hardware-independent constant, how the constrained fitting algorithm enforces physical consistency, and how the complete framework produces a PCIe Gen 4 jitter budget from oscilloscope measurements.

## Core Concepts

### Why the Gaussian Tail Is Predictable from the Center

Inside the silicon and copper interconnect, thermal energy causes electrons to vibrate chaotically. Each vibration generates a microscopic voltage pulse. At any given picosecond during transmission, the total noise voltage on the wire is the sum of billions of these individual pulses.

Most of the time, roughly half the electrons experience a positive thermal perturbation and half experience a negative perturbation. Their voltage contributions cancel. This high physical likelihood of cancellation creates the massive peak at the center of the bell curve, representing near-zero net noise voltage. For a large voltage spike to occur, a massive majority of those billions of electrons must coincidentally vibrate in the same direction at the same instant. The laws of entropy dictate that this level of spontaneous coordination is extraordinarily improbable.

This physical reality produces the Gaussian shape. The center peak exists because cancellation is highly probable. The tails decay exponentially because large-scale coordination of billions of independent electrons is highly improbable. The critical insight is that the physics generating the dense center and the physics generating the sparse tails are identical. There is no change in mechanism at any point along the curve. A single continuous mathematical equation ($e^{-x^2/2\sigma^2}$) describes the entire spectrum from center to infinity.

Once the oscilloscope measures the visible central mass of the histogram and calculates the standard deviation ($\sigma$), all variables in that equation are locked. The shape of the unmeasured tail at $7\sigma$ or $10\sigma$ is not an extrapolation in the sense of projecting a trend; it is a consequence of the same thermodynamic process that produced the measured data. The tail's trajectory is mathematically bound to the center mass because both regions arise from the same physical source.

### Standard Deviation as a Geometric Coordinate

The standard deviation ($\sigma$) is not an abstract statistical summary. It is a physical distance on the horizontal axis of the TIE histogram, measured in picoseconds.

The Gaussian bell curve starts flat at its peak, accelerates steeply downward, and then begins to level out as it approaches the tail. The exact coordinate where the curve stops accelerating downward and begins to level out is the inflection point, the transition from concave-down to concave-up curvature. The horizontal distance from the center peak to this inflection point is exactly one standard deviation.

The mathematics of the Gaussian function lock the area between $-1\sigma$ and $+1\sigma$ at precisely 68.2689% of the total distribution. This is not an engineering approximation. It is a fundamental mathematical constant derived by integrating $e^{-x^2/2}$ between those inflection boundaries, in the same way that $\pi$ is derived from the geometry of a circle. The 68.2% proportion holds regardless of whether $\sigma$ is 0.5 picoseconds or 50 picoseconds. It is a property of the Gaussian function itself, not of any particular hardware.

This geometric rigidity is what makes the Q-factor framework possible. Measuring $\sigma$ at the inflection point fixes the entire curve. The area under the tail at $7\sigma$, at $10\sigma$, or at any other multiple is a calculable consequence of that single measured parameter.

### Bit Error Rate as Tail Area

A bit error does not occur at a single specific jitter coordinate. A bit error occurs when an edge shifts anywhere past the receiver's sampling threshold.

If the receiver samples data exactly 31.25 picoseconds after the ideal edge crossing (half the Unit Interval for PCIe Gen 4), then an edge delayed by 32 picoseconds causes a bit error. An edge delayed by 50 picoseconds also causes a bit error. The probability of a bit error is therefore the total probability that the edge arrives anywhere from 31.25 ps outward to infinity.

Reading the probability density at the 31.25 ps coordinate alone would report only the likelihood of landing in that specific infinitesimal time bin. The actual BER requires summing the probability across all bins from 31.25 ps to infinity. In calculus, summing a continuous curve over a range is an integral. The Bit Error Rate is mathematically identical to the area under the Gaussian tail beyond the sampling threshold.

### The Complementary Error Function (erfc) and Its Inverse

The Gaussian probability density is defined by the exponential function $e^{-x^2}$. Integrating this function from a boundary point $x$ out to infinity cannot be solved using elementary algebra. Mathematicians created the complementary error function (erfc) to represent this specific integral.

The erfc computes the area under the tail of a Gaussian distribution beyond a specified boundary. It answers the question: if a random variable is drawn from a Gaussian distribution, what is the probability that it falls beyond $x$ standard deviations from the mean?

In jitter analysis, the problem runs in the opposite direction. The standard (PCIe, IEEE, Fibre Channel) dictates the required BER. The area is known. What is unknown is how far the physical timing jitter must spread before the probability drops to that BER level. The problem is solving for the x-axis boundary, not the y-axis probability.

This requires the inverse erfc. An inverse function is not a reciprocal ($1/\text{function}$); it is a mathematical reversal of inputs and outputs. The forward erfc takes a boundary coordinate as input and outputs the tail area. The inverse erfc takes a tail area as input and outputs the boundary coordinate. The relationship mirrors basic geometry: the forward function $A = \pi r^2$ computes area from radius; the inverse function $r = \sqrt{A/\pi}$ computes radius from area.

The inverse erfc receives the target BER (such as $10^{-12}$) and returns the exact number of standard deviations from the mean where the tail area equals that probability. This number of standard deviations is the Q-factor.

### The Q-Factor

Every physical system has a different amount of thermal noise. One oscillator's Gaussian distribution might be very narrow (low noise), while another's is very wide (high noise). The erfc cannot output a result in picoseconds because it operates in dimensionless mathematical space, normalized to standard deviations.

The Q-factor is the output of the inverse erfc: the boundary coordinate measured in units of $\sigma$. For a target BER of $10^{-12}$, the inverse erfc returns $Q = 7.03$. This means that for any Gaussian distribution in the universe, regardless of its physical scale, the tail area beyond $7.03\sigma$ from the mean contains exactly $10^{-12}$ of the total probability.

Common Q-factor values across standard BER targets:

| Target BER | Q-Factor | Peak-to-Peak Multiplier ($2Q$) |
|:---:|:---:|:---:|
| $10^{-9}$ | 6.00 | 12.00 |
| $10^{-12}$ | 7.03 | 14.06 |
| $10^{-15}$ | 7.94 | 15.88 |

To convert the universal Q-factor into a physical time boundary for a specific piece of hardware, the Q-factor is multiplied by the measured $RJ_{\text{rms}}$ of that hardware:

$$\text{Physical Boundary (ps)} = Q \cdot RJ_{\text{rms}}$$

This multiplication scales the dimensionless mathematical model to the physical reality of the silicon. The result is the distance from the center of the RJ distribution to the point where the tail probability equals the target BER.

The factor of 2 in the Total Jitter formula arises because an edge can shift either too early (the left tail) or too late (the right tail). $Q \cdot RJ_{\text{rms}}$ measures the distance from center to one boundary. The total span of possible arrival times destroyed by random jitter is twice that distance:

$$RJ_{\text{p-p}} = 2 \cdot Q \cdot RJ_{\text{rms}}$$

### The Dual-Dirac Model Structure

The measured TIE histogram is the convolution of the Deterministic Jitter distribution with the Random Jitter Gaussian. The actual DJ distribution is complex: it contains discrete spectral lines for PJ and DCD, and bounded multi-modal shapes for ISI. Deconvolving the pure RJ Gaussian from this entangled composite is computationally intensive and highly susceptible to noise.

The Dual-Dirac model replaces the complex DJ distribution with two Dirac delta impulses separated by a distance $DJ_{\delta\delta}$. The total jitter histogram is then modeled as the convolution of these two deltas with a single Gaussian, producing a bimodal distribution: two overlapping bell curves, one anchored at the left DJ boundary ($\mu_L$) and one anchored at the right DJ boundary ($\mu_R$).

This is a worst-case simplifying assumption adopted by industry standards. Concentrating all DJ energy at two extreme points produces the widest possible convolution with the RJ Gaussian, yielding a conservative (overestimating) total jitter number. The mathematical convenience lies in reducing the DJ description from an arbitrary complex shape to two scalar parameters: the separation distance ($DJ_{\delta\delta}$) and the population split between the two impulses.

### Asymmetric Delta Placement and Population Weighting

The two Dirac deltas do not need to be equidistant from the ideal zero-crossing, and they do not need to carry equal populations of hits.

Random Jitter is guaranteed to follow a perfectly symmetric Gaussian. The thermodynamic processes that generate it possess no directional bias. An electron is exactly as likely to experience a positive perturbation as a negative one.

Deterministic Jitter, by contrast, can be profoundly asymmetric. DCD from a stronger pull-up transistor concentrates rising-edge crossings early and falling-edge crossings late. ISI from a specific via reflection may interfere aggressively with one bit pattern while leaving the complementary pattern unaffected. These hardware-specific directional biases create lopsided timing distributions.

The Dual-Dirac model accommodates this asymmetry by allowing the left and right impulses to sit at unequal distances from center and to carry unequal fractions of the total population. If DCD causes 80% of edges to cross early and 20% to cross late, the left Gaussian population contains 800,000 hits out of a million, and the right Gaussian contains 200,000. The left curve appears four times taller, but both curves share the same horizontal width ($\sigma$). The height difference reflects the population weighting multiplier (0.8 vs. 0.2), not a difference in noise magnitude.

The 68.2% rule applies locally to each sub-population. Of the 800,000 edges in the left group, exactly 68.2% fall within $\pm 1\sigma$ of the left mean. Of the 200,000 edges in the right group, exactly 68.2% fall within $\pm 1\sigma$ of the right mean.

### The Single-Sigma Constraint

Random Jitter originates from thermal noise in the silicon. The silicon possesses a single temperature and a single fundamental noise floor. The thermodynamic variance of the noise is identical for all edges, regardless of whether DCD or ISI has shifted the mean crossing time of a particular sub-population.

The Dual-Dirac model enforces this physical reality by requiring both Gaussian curves to share the same standard deviation. The model does not use two different Gaussians with independent widths. It uses the same Gaussian, duplicated and anchored at two different mean positions. The vertical amplitudes (population weights) may differ substantially, but the horizontal shapes ($\sigma$) are mathematically identical.

In practice, independently fitting the left tail and the right tail will yield slightly different $\sigma$ values due to finite sample sizes, instrument noise, or differing slew rates between rising and falling edges (which slightly alter the amplitude-to-phase conversion ratio). Oscilloscope algorithms such as Keysight EZJIT resolve this discrepancy through a constrained least-squares fit. The software applies a mathematical constraint that $\sigma_{\text{left}}$ must equal $\sigma_{\text{right}}$ and processes both tails simultaneously to find the single unified $RJ_{\text{rms}}$ that minimizes the total fitting error across the entire histogram.

This single unified $RJ_{\text{rms}}$ represents the true thermal baseline of the hardware. It is this number that the Q-factor scales to produce the Total Jitter budget.

## Worked Examples

### PCIe Gen 4 Jitter Budget

Consider a PCIe Gen 4 link operating at 16 GT/s, measured with a Keysight Infiniium oscilloscope and EZJIT+ analysis software.

**Step 1: Establish the time budget.**

At 16 GT/s, the Unit Interval (UI) is the physical time duration of a single bit:

$$UI = \frac{1}{16 \times 10^9} = 62.5 \text{ ps}$$

**Step 2: Capture and extract the Dual-Dirac parameters.**

The oscilloscope captures several hundred thousand edge crossings and generates a TIE histogram. The EZJIT+ algorithm isolates the extreme tails, fits Gaussian curves using the single-sigma constraint, and extracts:

- $DJ_{\delta\delta} = 12.0$ ps (the separation between the two Gaussian means)
- $RJ_{\text{rms}} = 1.5$ ps (the unified standard deviation from the constrained fit)

**Step 3: Define the compliance target.**

The PCI Express specification mandates compliance at $BER = 10^{-12}$. The corresponding Q-factor is 7.03.

**Step 4: Calculate peak-to-peak Random Jitter.**

$$RJ_{\text{p-p}} = 2 \cdot Q \cdot RJ_{\text{rms}} = 2 \times 7.03 \times 1.5 \text{ ps} = 21.09 \text{ ps}$$

**Step 5: Calculate Total Jitter at $10^{-12}$ BER.**

$$TJ = DJ_{\delta\delta} + RJ_{\text{p-p}} = 12.0 \text{ ps} + 21.09 \text{ ps} = 33.09 \text{ ps}$$

**Step 6: Evaluate the timing margin.**

The total jitter consumes 33.09 ps out of the 62.5 ps Unit Interval, approximately 53% of the available bit period. The remaining 29.41 ps (47% of the UI) is the horizontal eye opening, the time window within which the receiver must successfully sample the data.

### Gaussian Tail Fitting: The 3σ-to-5σ Region

The Dual-Dirac algorithm does not fit a Gaussian to the entire histogram. It fits exclusively to the far tails, typically in the region between $3\sigma$ and $5\sigma$ from each Gaussian mean.

The rationale is physical. DJ is bounded, so it has absolute maximum limits. Every edge that lands beyond the DJ boundary arrived there solely because unbounded Random Jitter pushed it there. The tails beyond $3\sigma$ are well outside the DJ contamination zone and reflect pure RJ behavior.

The practical challenge is that events in this region are rare. A $4\sigma$ event occurs roughly 6 times per 100,000 bits transmitted. To populate the fitting region with enough data points for a stable regression, the oscilloscope must capture a large total sample. Modern Dual-Dirac implementations typically require 100,000 to 1,000,000 edge crossings. The algorithm sacrifices the overwhelming majority of data points (those in the center, where DJ and RJ are entangled) and builds the entire extrapolation from the sparse but physically clean tail region.

Once the curve is fit to the visible tail edges between $3\sigma$ and $5\sigma$, the Gaussian equation extends the curve to $7\sigma$, $10\sigma$, or any other multiple with mathematical certainty, because the curve shape beyond $5\sigma$ is fully determined by the $\sigma$ measured within the visible portion.

## Architecture

### The TJ Extrapolation Formula

The complete Total Jitter extrapolation formula encapsulates the entire Dual-Dirac framework:

$$TJ(BER) = DJ_{\delta\delta} + 2 \cdot Q(BER) \cdot RJ_{\text{rms}}$$

Each term has a direct physical interpretation:

- $DJ_{\delta\delta}$ is the deterministic floor: the irreducible timing spread caused by bounded hardware mechanisms (ISI, DCD, PJ), modeled as the separation between two Dirac delta impulses.
- $RJ_{\text{rms}}$ is the thermal baseline: the standard deviation of the Gaussian noise contribution, measured as a single unified value across both tails via constrained least-squares fitting.
- $Q(BER)$ is the statistical amplifier: the number of standard deviations required to reach the target error probability, computed as the inverse of the complementary error function.
- The factor of 2 accounts for both the early and late tails of the distribution.

The formula is additive because it combines a bounded deterministic component with the peak-to-peak extent of the unbounded Gaussian at the target confidence level. It produces a single number in picoseconds that can be compared directly against the Unit Interval to determine pass/fail compliance.

### From Histogram to Compliance: The Algorithmic Pipeline

The EZJIT+ software executes the following sequence to produce a TJ number at the target BER:

1. **Acquire TIE values** for several hundred thousand edges (input from the measurement infrastructure described in [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md)).
2. **Construct the histogram** and normalize to a probability density function.
3. **Identify the tail regions** beyond the DJ bounds on both the left and right extremes.
4. **Fit Gaussian curves** to both tails simultaneously under the single-sigma constraint ($\sigma_L = \sigma_R$), solving for the unified $RJ_{\text{rms}}$ and the two mean positions ($\mu_L$, $\mu_R$).
5. **Compute $DJ_{\delta\delta}$** as $\mu_R - \mu_L$.
6. **Look up or compute the Q-factor** for the target BER using the inverse erfc.
7. **Apply the TJ formula** to produce the final compliance number.

The entire pipeline transforms a physical histogram into a single picosecond value that determines whether the link meets its specification.

## Edge Cases

### The Overestimation Tendency of Dual-Dirac

The Dual-Dirac model concentrates all DJ energy at exactly two points, creating the widest possible convolution footprint with the RJ Gaussian. In physical hardware, the DJ distribution is typically spread across many intermediate values (ISI creates a range of delays for different bit patterns, not just two extremes). The actual DJ distribution, when convolved with RJ, produces a total jitter that is narrower than the Dual-Dirac prediction.

This makes the Dual-Dirac model inherently conservative. It will report a TJ number that equals or exceeds the true total jitter, providing a safety margin. Standards bodies adopted this model precisely because its overestimation tendency means that hardware passing the Dual-Dirac compliance test is guaranteed to meet the BER target under real operating conditions.

The conservatism becomes problematic only when the overestimation is so large that functional hardware fails the specification. In practice, this is rare: the separation between the Dual-Dirac TJ and the true TJ is typically a few picoseconds, well within the design margin of links that are close to the performance boundary.

### The Single-Temperature Assumption

The single-sigma constraint assumes that the silicon operates at a uniform temperature, producing a single noise floor for all edges. In practice, power dissipation creates thermal gradients across the die. Regions near high-activity logic may run hotter than quiet regions, producing locally elevated noise. If the transmitter's output stage experiences significant temperature variation during a measurement window (as might occur during thermal transients at power-up), the left and right tails of the histogram could genuinely have slightly different intrinsic $\sigma$ values.

The constrained fit averages this variation into a single number, which remains a good approximation as long as the thermal gradient is small relative to the overall noise floor. For links where thermal transient effects are suspected, capturing data after thermal equilibrium is established eliminates this concern.

### Sample Size and Tail Population

The accuracy of the Dual-Dirac extraction depends entirely on populating the $3\sigma$-to-$5\sigma$ tail region with enough data points to constrain the Gaussian fit. With too few points, the regression is underdetermined and the extracted $\sigma$ is noisy.

In a system with only Random Jitter, a few thousand edges would suffice to determine $\sigma$ accurately, because the central mass directly reveals the standard deviation. In a real system contaminated with DJ, the algorithm cannot use the central mass (it is corrupted by the DJ distribution) and must rely exclusively on the sparse tail population. This is why the sample size requirement jumps from thousands to hundreds of thousands: the vast majority of captured edges are discarded by the algorithm, and only the rare tail events contribute to the fit.

Insufficient sample size manifests as measurement-to-measurement variation in the reported $RJ_{\text{rms}}$ and $TJ$ values. If repeated acquisitions produce inconsistent results, the first diagnostic step is to increase the capture depth.
