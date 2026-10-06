# Dual-Dirac Model and BER Extrapolation

<!-- SUMMARY: A compliance target such as a bit error ratio of 1e-12 describes edges so rare that they never populate a captured histogram, so the total jitter at that ratio must be projected from the tails that are visible. This guide derives the Gaussian distribution, the complementary error function and the Q-factor, shows how the Dual-Dirac model turns the convolution of deterministic and random jitter into two Gaussians whose tails give TJ = DJ + 2 Q RJ, constructs the bathtub curve, works a PCIe Gen 4 budget, and states the assumptions under which the projection is conservative and the cases in which it is not. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Chapter 10](10_Jitter_Decomposition_and_Measurement.md) decomposed the timing error of a received signal into random and deterministic components and ended with a histogram of time interval error values that is the convolution of the two. A specification does not ask for that histogram. It asks how wide a window of time around the ideal edge contains all but one edge in a trillion, and the answer lies in a part of the distribution that a measurement of a few hundred thousand edges never reaches.

The high-speed serial standards state compliance at bit error ratios such as $10^{-12}$. A direct measurement at that ratio is feasible only for a short time at a modest rate, and it becomes impractical at lower ratios, as the first worked example computes. An oscilloscope that captures a few hundred thousand edges therefore projects the timing behavior at the target ratio from the tails that its histogram does show. The projection rests on the shape of the Gaussian distribution and on a deliberately simple model of the deterministic part.

This chapter derives the mathematics in the order in which it is needed: the Gaussian distribution and its standard deviation, the tail area as a bit error ratio, the complementary error function and the Q-factor, the Dual-Dirac model and the formula for total jitter, the Q-scale fit that extracts the model parameters, and the bathtub curve that links a sampling position to an error ratio. The Edge Cases state the conditions under which the projection is conservative and the conditions under which it is not.

## Core Concepts

### The Gaussian Distribution

The **Gaussian** (normal) probability density of a variable $x$ with mean $\mu$ and parameter $\sigma$ is

$$g(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-(x-\mu)^2/2\sigma^2}$$

Three properties are needed, and each follows from a short calculation. The first is that the density has a total area of one, which is what makes the factor $1/(\sigma\sqrt{2\pi})$ correct. The calculation takes $\mu = 0$ and defines $I = \int_{-\infty}^{\infty} e^{-x^2/2\sigma^2}dx$ as the unnormalized area. The square of $I$ is a double integral over the plane, and converting to polar coordinates ($x^2 + y^2 = r^2$, area element $r\,dr\,d\theta$) gives:

$$I^2 = \int\!\!\int e^{-(x^2+y^2)/2\sigma^2}\,dx\,dy = \int_0^{2\pi}\!\!\int_0^{\infty} e^{-r^2/2\sigma^2}\,r\,dr\,d\theta = 2\pi\,\sigma^2$$

The radial integral equals $\sigma^2$ because $r\,e^{-r^2/2\sigma^2}$ is the derivative of $-\sigma^2 e^{-r^2/2\sigma^2}$. Therefore $I = \sigma\sqrt{2\pi}$, and $g(x)$ integrates to one.

The second property is that the parameter $\sigma$ is the standard deviation, the square root of the mean square distance from the mean. Integration by parts with $u = x$ and $dv = x\,e^{-x^2/2\sigma^2}dx$ (so $v = -\sigma^2 e^{-x^2/2\sigma^2}$) gives

$$\int_{-\infty}^{\infty} x^2 e^{-x^2/2\sigma^2}dx = \Bigl[-\sigma^2 x\,e^{-x^2/2\sigma^2}\Bigr]_{-\infty}^{\infty} + \sigma^2\int_{-\infty}^{\infty} e^{-x^2/2\sigma^2}dx = \sigma^2\cdot\sigma\sqrt{2\pi}$$

The boundary term vanishes at both limits because the exponential decays faster than any power of $x$ grows. Dividing by the normalization $\sigma\sqrt{2\pi}$ gives a variance of $\sigma^2$.

The third property gives $\sigma$ a geometric meaning on the horizontal axis. The first derivative is $g'(x) = -\frac{x-\mu}{\sigma^2}g(x)$, and the second derivative follows from the product rule:

$$g''(x) = g(x)\,\frac{(x-\mu)^2 - \sigma^2}{\sigma^4}$$

The second derivative is zero at $x = \mu \pm \sigma$. The curve changes from concave down to concave up at these two **inflection points**, so $\sigma$ is the horizontal distance from the center of the peak to the inflection point, a distance measured in picoseconds when the variable is a timing error. The area within $\pm k\sigma$ of the mean is $\operatorname{erf}(k/\sqrt{2})$, and the area beyond $k\sigma$ on one side is the quantity $Q(k)$ defined below:

| Distance from the mean | Area within $\pm k\sigma$ | Area beyond $+k\sigma$ (one side) |
|:---:|:---:|:---:|
| $1\sigma$ | 68.27% | $1.59 \times 10^{-1}$ |
| $2\sigma$ | 95.45% | $2.28 \times 10^{-2}$ |
| $3\sigma$ | 99.73% | $1.35 \times 10^{-3}$ |
| $4\sigma$ | 99.9937% | $3.17 \times 10^{-5}$ |
| $5\sigma$ | 99.99994% | $2.87 \times 10^{-7}$ |

The 68.27 percent proportion is a property of the Gaussian function and holds for any $\sigma$, whether it is 0.5 ps or 50 ps. [Chapter 10](10_Jitter_Decomposition_and_Measurement.md) showed that the random jitter of a link is Gaussian with $\sigma = RJ_{\text{rms}}$, and the rest of this chapter uses that result.

### What a Measured Sigma Determines

A pure Gaussian distribution is fixed by two numbers, its mean and its $\sigma$. Assume that the histogram contains random jitter alone. The width of the central mass then gives $\sigma$, and the whole curve, including the tail at $7\sigma$ that no measurement reaches, follows from the same formula. That statement holds only for pure random jitter, and only if the random jitter is Gaussian all the way out. The second condition is an assumption about the physics, and the Edge Cases return to it.

A real histogram contains deterministic jitter, and the center of the distribution is then the convolution of the Gaussian with the deterministic clusters of [Chapter 10](10_Jitter_Decomposition_and_Measurement.md). Its width reflects the clusters as well as $\sigma$, so the central mass cannot be used to measure $\sigma$. The tails are the part of the histogram that deterministic jitter does not reach. No edge lies farther from the ideal time than the outermost deterministic extreme plus whatever the unbounded random component adds, so the outer tails are approximately Gaussian tails centered on the outermost deterministic positions. The standard deviation is taken from the tails alone, which resolves the apparent conflict between measuring $\sigma$ in the center and measuring it in the tails: the center is used only when no deterministic jitter is present.

### Bit Error Ratio as Tail Area

A bit error does not occur at one specific jitter value. It occurs when an edge arrives anywhere beyond the sampling instant of the receiver. Assume a receiver that samples at a time $s$ after the ideal edge and an edge whose arrival time $t$ has probability density $g(t)$. The probability that the edge arrives after $s$, and the bit is read incorrectly, is the sum of the density over every value from $s$ to infinity:

$$P(t > s) = \int_{s}^{\infty} g(t)\,dt$$

The density at the single coordinate $s$ would give only the probability of landing in one narrow bin, and the error ratio requires the integral. The bit error ratio of a jitter-limited link is therefore the area under the tail beyond the sampling boundary, up to a transition-density factor that the Edge Cases treat.

### The Complementary Error Function and the Q-Factor

The integral of a Gaussian cannot be written with elementary functions, so two named functions represent it. The **Q-function** is the tail area of the standard Gaussian (mean 0, $\sigma = 1$) beyond $z$:

$$Q(z) = \frac{1}{\sqrt{2\pi}}\int_z^{\infty} e^{-s^2/2}\,ds = P(Z > z)$$

where $Z$ denotes a standard Gaussian variable. The **complementary error function** is defined by

$$\operatorname{erfc}(x) = \frac{2}{\sqrt{\pi}}\int_x^{\infty} e^{-u^2}\,du$$

The two are related by the substitution $s = \sqrt{2}\,u$, which gives $ds = \sqrt{2}\,du$ and a lower limit $u = z/\sqrt{2}$:

$$Q(z) = \frac{1}{\sqrt{2\pi}}\cdot\sqrt{2}\int_{z/\sqrt{2}}^{\infty} e^{-u^2}du = \frac{1}{\sqrt{\pi}}\int_{z/\sqrt{2}}^{\infty} e^{-u^2}du = \frac{1}{2}\operatorname{erfc}\!\left(\frac{z}{\sqrt{2}}\right)$$

Rearranged, $\operatorname{erfc}(x) = 2\,Q(x\sqrt{2}) = 2\,P(Z > x\sqrt{2})$, which is the correct statement of the definition: erfc counts the tail beyond $x\sqrt{2}$ standard deviations, doubled, and not the tail beyond $x$ standard deviations. The bit error ratio for a Gaussian edge distribution whose mean is $Q$ standard deviations from the sampling instant is

$$\text{BER} = Q(Q_{\text{factor}}) = \frac{1}{2}\operatorname{erfc}\!\left(\frac{Q_{\text{factor}}}{\sqrt{2}}\right)$$

A specification fixes the ratio, and the quantity to find is the distance. The jitter analysis therefore needs the inverse of the tail function. The forward function takes a boundary coordinate and returns the tail area. The inverse takes a tail area and returns the boundary coordinate, in units of the standard deviation, and an inverse function is a reversal of inputs and outputs and not a reciprocal. The coordinate returned for the target ratio is the **Q-factor**:

$$Q_{\text{factor}} = Q^{-1}(\text{BER})$$

The standard Gaussian has no physical scale, so the Q-factor is a pure number that applies to any distribution once the distance is multiplied by the measured $\sigma$. The values for the common ratios are:

| Target BER | Q-factor | Multiplier $2Q$ |
|:---:|:---:|:---:|
| $10^{-6}$ | 4.753 | 9.51 |
| $10^{-9}$ | 5.998 | 12.00 |
| $10^{-12}$ | 7.034 | 14.07 |
| $10^{-15}$ | 7.941 | 15.88 |
| $10^{-18}$ | 8.757 | 17.51 |

The Q-factor grows slowly with the number of decades of error ratio, and a short argument shows why. In the tail, $s \ge z$, so $1 \le s/z$ and

$$Q(z) = \int_z^{\infty}\varphi(s)\,ds < \int_z^{\infty}\frac{s}{z}\,\varphi(s)\,ds = \frac{\varphi(z)}{z}, \qquad \varphi(s) = \frac{e^{-s^2/2}}{\sqrt{2\pi}}$$

where the last step uses the fact that $s\,\varphi(s)$ is the derivative of $-\varphi(s)$. At $z = 7.034$ the bound is $1.02 \times 10^{-12}$ against the exact $1.00 \times 10^{-12}$, so it is accurate to 2 percent there. The logarithm of the bound has the slope $-z$ with respect to $z$, so each factor of ten in the ratio requires an increase of about $\ln 10/z = 2.303/7 = 0.33$ in the Q-factor, in agreement with the table (from $10^{-9}$ to $10^{-12}$ the increase is 1.04 over three decades, or 0.35 per decade). The extrapolation to a much lower ratio therefore adds little distance.

[Chapter 15](15_PAM4_Signaling_and_Gray_Coding.md) uses the same mapping between a ratio and a Q-factor for amplitude noise.

### The Dual-Dirac Model

The histogram of [Chapter 10](10_Jitter_Decomposition_and_Measurement.md) is the convolution of the deterministic density $p_{DJ}$ with the Gaussian $g$ of the random jitter. The deterministic density has a complicated shape: two clusters for duty cycle distortion, a set of clusters for intersymbol interference, an arcsine shape for each periodic tone, and a continuous bounded shape for crosstalk. Deconvolving the Gaussian from a general shape is sensitive to noise.

The **Dual-Dirac model** replaces the deterministic density with two Dirac impulses, each carrying half of the edges, at positions $\mu_L$ and $\mu_R$:

$$p_{DJ}(\tau) = \tfrac{1}{2}\,\delta(\tau - \mu_L) + \tfrac{1}{2}\,\delta(\tau - \mu_R)$$

The convolution with a Dirac impulse simply shifts the Gaussian to the position of the impulse, because $\int \delta(\tau - \mu)\,g(t-\tau)\,d\tau = g(t-\mu)$. The total density of the model is therefore the sum of two Gaussians with the same $\sigma$:

$$p_{TJ}(t) = \tfrac{1}{2}\,g(t - \mu_L) + \tfrac{1}{2}\,g(t - \mu_R), \qquad DJ_{\delta\delta} = \mu_R - \mu_L$$

The standard model uses equal weights of one half. The only deterministic parameter that enters the total jitter is the separation $DJ_{\delta\delta}$, called the **dual-Dirac deterministic jitter**, and it is a parameter of the fit, which is generally not equal to the peak-to-peak deterministic jitter that the instrument could measure directly. The positions $\mu_L$ and $\mu_R$ need not be symmetric about the ideal edge time; an offset of the pair shifts the center of the eye but does not change the separation.

### The Total Jitter Formula

The probability that an edge arrives later than a position $x$ in the model is

$$P_R(x) = \tfrac{1}{2}\,Q\!\left(\frac{x - \mu_L}{\sigma}\right) + \tfrac{1}{2}\,Q\!\left(\frac{x - \mu_R}{\sigma}\right)$$

For $x$ at or beyond $\mu_R$, the first term is negligible, because the left Gaussian is centered $DJ_{\delta\delta}$ away and its tail at that distance is far smaller, so only the right Gaussian contributes. The compliance convention takes the boundary $x_R$ at which the tail of the right impulse, counted at full weight, equals the target ratio:

$$Q\!\left(\frac{x_R - \mu_R}{\sigma}\right) = \text{BER} \quad\Rightarrow\quad x_R = \mu_R + Q_{\text{factor}}\,\sigma$$

By symmetry the left boundary is $x_L = \mu_L - Q_{\text{factor}}\,\sigma$. Total jitter at the target ratio is the width of the interval between the boundaries:

$$TJ(\text{BER}) = x_R - x_L = DJ_{\delta\delta} + 2\,Q_{\text{factor}}\,RJ_{\text{rms}}$$

The factor of two arises because an edge can be early or late, and each tail contributes a distance of $Q_{\text{factor}}\,\sigma$. The formula is additive because the width is the separation of the two deterministic positions plus the Gaussian reach on each outer side. The peak-to-peak random jitter at a ratio is the second term, $RJ_{\text{p-p}} = 2\,Q_{\text{factor}}\,RJ_{\text{rms}}$, a calculation and not a measurement, as [Chapter 10](10_Jitter_Decomposition_and_Measurement.md) stated. The convention counts each impulse at full weight and does not include the transition density of the data. The Edge Cases quantify what this omission costs.

### The Q-Scale Fit and the Single-Sigma Constraint

The model parameters are extracted from the histogram tails by a linear fit. Take the tail probability of a single Gaussian tail with mean $\mu$ and deviation $\sigma$, $P(x) = Q((x - \mu)/\sigma)$, and apply the inverse tail function to both sides:

$$Q^{-1}\bigl(P(x)\bigr) = \frac{x - \mu}{\sigma}$$

Plotted against $x$, the quantity $Q^{-1}(P)$ is a straight line with slope $1/\sigma$ that crosses zero at $x = \mu$. This is the **Q-scale**: a Gaussian tail becomes a line, and the standard deviation and the mean are the slope and the intercept of a linear regression. In the Dual-Dirac model the measured tail probability includes the weight of one half, so the quantity to transform is $2P(x)$, the tail probability conditioned on the impulse that produces it.

The tails of the histogram are fitted in a region that excludes the center and excludes the region too far out to contain data. A common choice is the region where $Q^{-1}$ lies between 3 and 5, which is the span of $3\sigma$ to $5\sigma$ from each mean. The lower limit is set by the deterministic contamination of the center, and the upper limit is set by the sparse population of the tail. The line is then extended to $Q^{-1} = Q_{\text{factor}}$, which gives $x_R$ without any assumption beyond the Gaussian shape of the tail.

The two tails have the same physical origin in the noise of one circuit, so the model requires them to share one standard deviation: $\sigma_L = \sigma_R$, which in the Q-scale means that the left line and the right line have slopes of equal magnitude. Fitting each tail alone gives slightly different values because of finite sample sizes and because rising and falling edges can have slightly different slopes at the threshold ($\sigma_t = \sigma_v/S$, [Chapter 10](10_Jitter_Decomposition_and_Measurement.md)). Oscilloscope jitter software, for example Keysight EZJIT, applies a constrained least-squares fit that forces equal slopes and returns one unified $RJ_{\text{rms}}$ together with the two means.

The probability density and the jitter spectrum are different descriptions, and the fit uses only the first. The deterministic density of a periodic tone is an arcsine shape and its spectrum is a single line, and the two impulses of the model describe where the deterministic mass sits in the histogram. They do not describe discrete spectral lines.

## Architecture

### The Bathtub Curve

The **bathtub curve** shows the bit error ratio as a function of the position at which the receiver samples the bit. It follows from the model by counting the two ways a bit can be misread. Let $s$ be the sampling position measured from the left bit boundary. The bit is misread if the left boundary edge arrives after $s$, so that the previous bit is still present, or if the right boundary edge, at $UI$ plus its own timing error, arrives before $s$. Random data has a transition at a given boundary with probability $\eta_T = 1/2$, which scales both events, so for the Dual-Dirac model with impulse positions $d \in \{\mu_L, \mu_R\}$:

$$\text{BER}(s) = \eta_T \sum_{d}\tfrac{1}{2}\left[\,Q\!\left(\frac{s - d}{\sigma}\right) + Q\!\left(\frac{UI + d - s}{\sigma}\right)\right]$$

On a plot of $\log\text{BER}$ against $s$, the first term produces the left wall and the second term the right wall. Each wall is the Gaussian tail of the corresponding edge, so on the logarithmic scale it falls with a curvature that increases with distance from the boundary. Between the walls the curve falls to a floor that is far below any measurable ratio. The horizontal width of the curve at a chosen ratio is the width of the eye at that ratio, and the convention of the previous section gives

$$W_{eye}(\text{BER}) = UI - TJ(\text{BER})$$

A bathtub built from measured tails and the Q-scale fit is the standard picture for reading margin: a wider floor at a given ratio is a wider horizontal eye. The curve describes timing only, and the vertical noise of the receiver is a separate limit, and a floor of $10^{-64}$ at the center of the example below is a statement about timing jitter, which other mechanisms would exceed long before.

### From Histogram to Compliance: the Pipeline

The jitter analysis software executes the following sequence, building on the first three steps (acquisition, histogram construction, and tail isolation) of the measurement flow in [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md):

4. **Fit the tails** in the Q-scale under the single-sigma constraint, solving for $RJ_{\text{rms}}$, $\mu_L$, and $\mu_R$.
5. **Compute the dual-Dirac deterministic jitter** as $DJ_{\delta\delta} = \mu_R - \mu_L$.
6. **Compute the Q-factor** for the target ratio from the inverse tail function.
7. **Apply the total jitter formula** and compare $TJ$ with the unit interval.

The pipeline converts a physical histogram into one picosecond value that is compared with the unit interval to give pass or fail. The terms of the formula have direct interpretations: $DJ_{\delta\delta}$ is the deterministic spread that the model assigns to hardware mechanisms, $RJ_{\text{rms}}$ is the Gaussian width of the unbounded noise, $Q_{\text{factor}}$ is the number of standard deviations required for the target ratio, and the factor of two covers both tails.

## Worked Examples

### How Long a Direct Measurement Takes

Assume a link running at 16 GT/s. One trillion bits take $10^{12}/(16 \times 10^9) = 62.5$ s to transmit, but observing no error in that many bits does not prove that the ratio is $10^{-12}$ or better. The true ratio is $p$, and the probability of seeing no error in $N$ independent bits is $(1-p)^N \approx e^{-Np}$. A measurement with no errors therefore supports the claim that the ratio is below $p_0$ with a confidence

$$C = 1 - e^{-N p_0} \quad\Rightarrow\quad N = \frac{-\ln(1 - C)}{p_0}$$

For a 95 percent confidence, $-\ln 0.05 = 2.996$, so $N \approx 3.0/p_0$ bits. The times at 16 GT/s are:

| Target BER | Bits required | Time at 16 GT/s |
|:---:|:---:|:---:|
| $10^{-12}$ | $3.0 \times 10^{12}$ | 187 s (3.1 minutes) |
| $10^{-15}$ | $3.0 \times 10^{15}$ | 52 hours (2.2 days) |
| $10^{-18}$ | $3.0 \times 10^{18}$ | 5.9 years |

A ratio of $10^{-12}$ can therefore be verified directly with a bit error ratio tester in a few minutes at this rate. A ratio of $10^{-15}$ or lower, a capture of a limited record by an oscilloscope, and any measurement that must also identify the cause of the errors need the projection from the tails.

### PCIe Gen 4 Jitter Budget

Consider a link at 16 GT/s, so that $UI = 1/(16 \times 10^9) = 62.5$ ps. Assume that the tail fit returns $DJ_{\delta\delta} = 12.0$ ps and $RJ_{\text{rms}} = 1.5$ ps. For a target ratio of $10^{-12}$ the Q-factor is 7.034, and the calculation proceeds in four steps:

$$RJ_{\text{p-p}} = 2 \times 7.034 \times 1.5\ \text{ps} = 21.10\ \text{ps}$$

$$TJ = DJ_{\delta\delta} + RJ_{\text{p-p}} = 12.0 + 21.10 = 33.10\ \text{ps}$$

$$W_{eye} = UI - TJ = 62.5 - 33.10 = 29.40\ \text{ps}$$

The total jitter consumes 53 percent of the unit interval, and the horizontal opening is 47 percent. The same fit at other targets gives:

| Target BER | Q-factor | $RJ_{\text{p-p}}$ (ps) | $TJ$ (ps) | Eye width (ps) | Eye width (% of UI) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| $10^{-9}$ | 5.998 | 17.99 | 29.99 | 32.51 | 52.0 |
| $10^{-12}$ | 7.034 | 21.10 | 33.10 | 29.40 | 47.0 |
| $10^{-15}$ | 7.941 | 23.82 | 35.82 | 26.68 | 42.7 |

Each added three decades of ratio cost 2.7 to 3.1 ps of eye width, which is the slow growth of the Q-factor stated above.

### Extracting the Parameters in the Q-Scale

Use the model of the previous example, with the right impulse at $\mu_R = +6.0$ ps, the left at $-6.0$ ps, and $\sigma = 1.5$ ps. The tail probability beyond three positions on the right side, multiplied by two to condition on the right impulse, and transformed by the inverse tail function, is:

| $x$ (ps) | $2\,P(t > x)$ | $Q^{-1}(2P)$ |
|:---:|:---:|:---:|
| 10.5 | $1.350 \times 10^{-3}$ | 3.0 |
| 12.0 | $3.167 \times 10^{-5}$ | 4.0 |
| 13.5 | $2.867 \times 10^{-7}$ | 5.0 |

The points lie on a straight line with slope $1/\sigma = 1/1.5 = 0.667$ per ps, which crosses zero at 6.0 ps. The regression therefore returns $\mu_R = 6.0$ ps and $\sigma = 1.5$ ps, and the mirrored left tail returns $\mu_L = -6.0$ ps, so $DJ_{\delta\delta} = 12.0$ ps. Extending the line to $Q^{-1} = 7.034$ gives $x_R = 6.0 + 7.034 \times 1.5 = 16.55$ ps and $TJ = 2 \times 16.55 = 33.10$ ps, the same total as before.

### The Bathtub of the Example

Evaluate the bathtub formula with $UI = 62.5$ ps, $\mu = \pm 6$ ps, $\sigma = 1.5$ ps, and $\eta_T = 1/2$:

| Sampling position $s$ (ps) | Position as fraction of UI | BER |
|:---:|:---:|:---:|
| 5.0 | 0.08 | $1.9 \times 10^{-1}$ |
| 10.0 | 0.16 | $9.6 \times 10^{-4}$ |
| 15.0 | 0.24 | $2.5 \times 10^{-10}$ |
| 20.0 | 0.32 | $1.3 \times 10^{-21}$ |
| 25.0 | 0.40 | $1.1 \times 10^{-37}$ |
| 31.25 | 0.50 | $3.5 \times 10^{-64}$ |

The left wall falls by more than six decades between 10 ps and 15 ps. The curve reaches $10^{-12}$ at $s = 16.26$ ps and, by symmetry, at $62.5 - 16.26 = 46.24$ ps, so the horizontal opening at $10^{-12}$ is 29.98 ps. The compliance convention gave 29.40 ps for the same ratio, and the difference is explained in the Edge Cases.

### Fitting a Distribution That Is Not Two Points

The Dual-Dirac fit applies to a deterministic jitter that is not two points, but the fitted $DJ_{\delta\delta}$ is then a parameter and not a measured width. Take three cases with the same random jitter ($\sigma = 1.5$ ps) and a deterministic jitter of 12 ps peak to peak. The Q-scale fit is made in the region between $Q^{-1} = 3$ and $Q^{-1} = 5$, and the result is compared with the total jitter computed directly from the density at $10^{-12}$ under the same convention:

| Deterministic jitter | Fitted $DJ_{\delta\delta}$ (ps) | Fitted $\sigma$ (ps) | $TJ$ from fit (ps) | True $TJ$ (ps) | Difference (ps) |
|---|:---:|:---:|:---:|:---:|:---:|
| Two impulses at $\pm 6$ ps | 12.00 | 1.500 | 33.10 | 33.10 | 0.00 |
| Uniform over $\pm 6$ ps | 8.51 | 1.672 | 32.03 | 31.67 | +0.36 |
| Arcsine (sinusoid, $A = 6$ ps) | 9.98 | 1.602 | 32.51 | 32.30 | +0.22 |

In both extended cases the fitted $DJ_{\delta\delta}$ is smaller than the 12 ps peak-to-peak value, and the fitted $\sigma$ is larger than the true 1.5 ps, because part of the width of the deterministic distribution is absorbed into the apparent noise. The projected total jitter is slightly above the true value. Using the peak-to-peak value in the formula, $12 + 21.10 = 33.10$ ps, overestimates the true values of 31.67 ps and 32.30 ps by 1.4 ps and 0.8 ps.

## Edge Cases

### The Projection Is Usually Conservative but Not Guaranteed

The comparison above shows the typical outcome: the fitted total jitter is equal to or slightly above the true total jitter, so hardware that passes the projected limit usually meets the target. The model carries no guarantee, and the result depends on the shape of the deterministic distribution, on the region chosen for the fit, and on the assumption that the random jitter is Gaussian beyond the region that the data reaches.

A concrete failure of the last assumption shows the size of the possible error. Assume that one edge in $10^5$ carries random jitter with a standard deviation of 3 ps instead of 1.5 ps, for example because of an occasional supply glitch, and that the rest follow the model above. The tail fit in the $3\sigma$ to $5\sigma$ region sees almost only the narrow population and returns $DJ_{\delta\delta} = 11.86$ ps and $\sigma = 1.52$ ps, which projects $TJ = 33.25$ ps at $10^{-12}$. The wide population dominates the density far out, and the true value at $10^{-12}$ is 43.20 ps. The projection under-predicts by 9.95 ps, which is 16 percent of the unit interval at 16 GT/s. The model is conservative when its assumptions hold and it can under-predict when they do not, and a measurement that must be trusted at a very low ratio needs a check of the tail shape or a direct measurement.

### Weights, Transition Density, and the Conservative Convention

The total jitter convention equates the tail probability of one impulse, counted at full weight, with the bit error ratio. The exact bathtub includes two factors that the convention omits: each impulse carries a weight of one half, and random data has a transition density of one half. At the boundary of the convention, $x_R = 16.55$ ps, the exact ratio is $\eta_T \times \tfrac{1}{2} \times 10^{-12} = 2.5 \times 10^{-13}$, a factor of four below the target. The exact $10^{-12}$ boundary is found where $\tfrac{1}{4}Q(a) = 10^{-12}$, so $Q(a) = 4 \times 10^{-12}$ and $a = 6.84$ in place of 7.03. The exact total jitter is $12 + 2 \times 6.84 \times 1.5 = 32.52$ ps against the convention's 33.10 ps, and the convention therefore overstates the width by 0.59 ps in the example.

The weights are one half in the standard model. A general model may use unequal weights $w_L$ and $w_R$ with $w_L + w_R = 1$, which scales each tail by its weight and shifts the exact boundary by a fraction of a standard deviation, but it does not alter the form of the Q-scale line. Asymmetric deterministic jitter, such as duty cycle distortion, appears in the standard model as a shift of the pair or as unequal positions relative to the ideal edge, and the separation $DJ_{\delta\delta}$ is unchanged by either.

### The Single-Sigma Assumption

The constraint $\sigma_L = \sigma_R$ assumes that the noise level is the same for all edges. Slightly different slopes of rising and falling edges give slightly different values of $\sigma_t = \sigma_v/S$, and temperature gradients across the transmitter output stage change $\sigma_v$ during a thermal transient. The constrained fit averages these differences into one value, which remains a good description when they are small. A measurement made after thermal equilibrium removes the transient contribution.

### Sample Size and Tail Population

The fit needs data in the tail region, and the data are sparse. Assume 300,000 edges, so that each impulse holds 150,000 of them. The expected number of edges beyond $3\sigma$ above one impulse mean is $150{,}000 \times 1.35 \times 10^{-3} = 202$, beyond $4\sigma$ it is $150{,}000 \times 3.17 \times 10^{-5} = 4.75$, and beyond $5\sigma$ it is $150{,}000 \times 2.87 \times 10^{-7} = 0.043$. The practical upper edge of the fit region for this record is near $4\sigma$, and reaching five expected edges at $5\sigma$ needs about $3.5 \times 10^7$ edges. A record in which only noise-free random jitter is present could determine $\sigma$ from a few thousand edges, because the central mass reveals it. With deterministic jitter present the algorithm cannot use the center, and the sample requirement rises to hundreds of thousands or more because most edges contribute nothing to the fit. Measurement-to-measurement variation of the reported $RJ_{\text{rms}}$ and $TJ$ is the sign of an insufficient record, and increasing the capture depth is the first remedy.

### The Gaussian Assumption in the Far Tail

The central limit theorem explains why a sum of many small independent noise contributions is close to Gaussian near its center, and it gives the weakest guarantee in the far tails. A single large disturbance, a nonlinear conversion from voltage to time near the rails ([Chapter 10](10_Jitter_Decomposition_and_Measurement.md)), or a rare mechanism with a different noise level changes the tail without changing the center. The Q-scale line exposes such a change as a bend: a measured tail that departs from a straight line in the fit region indicates that the extrapolation should not be trusted beyond that region.

The projection tells the designer how much timing margin remains at the target ratio, and it needs the random and deterministic components to be known separately and accurately. [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) shows how pattern averaging and spectral analysis separate the data-dependent, periodic, and random contributions that this chapter treated as two parameters.
