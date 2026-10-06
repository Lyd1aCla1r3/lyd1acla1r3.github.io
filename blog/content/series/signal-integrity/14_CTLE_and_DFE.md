# Continuous Time Linear Equalization and Decision Feedback Equalization

<!-- SUMMARY: The receiver has two equalizers that act on different parts of the problem. The continuous time linear equalizer (CTLE) is a filter with one zero and two poles that restores the gain that the channel removed at high frequency, and it amplifies the noise in the same band. The decision feedback equalizer (DFE) removes the interference of earlier bits by subtracting a weighted sum of their decisions, so it cancels post-cursors without amplifying noise and has no effect on pre-cursors. This guide derives the CTLE transfer function and its circuit origin, models the DFE and quantifies its noise and error-propagation behavior, derives the least mean squares (LMS) update as a gradient descent and its convergence rate, describes the link training procedure that sets the transmitter and receiver equalizers together, and works the numbers on the 12 inch line of the earlier chapters. --> 

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) ends with the division of work among the three equalizers: the transmitter filter is open loop and can act on pre-cursors and post-cursors, the decision feedback equalizer cancels post-cursors only, and the linear equalizer at the receiver shapes the smooth part of the loss. This chapter describes the two receiver equalizers and the procedure that sets all three. It works with the same line as the earlier chapters, 12 inches of FR4 whose loss comes from [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) and whose insertion loss, a quantity defined in [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md), sets the amount of equalization required.

The two equalizers differ in what they observe. The CTLE sees the analog waveform before any decision, and it applies a gain that depends on frequency. The DFE sees the decisions of the slicer, and it subtracts a weighted sum of them from the waveform before the next decision. The first is a linear filter and shares the limits of every linear filter, which is that it cannot change the signal-to-noise ratio at any single frequency. The second is nonlinear because it contains the slicer, and the nonlinearity is the reason that it escapes one of those limits and acquires another: it does not enhance noise, and it can propagate a decision error.

Neither equalizer chooses its own parameters without help from an adaptation procedure. An adaptation engine estimates the tap weights from the received signal, and a negotiation with the transmitter sets the transmitter filter. The chapter derives the update rule of the adaptation engine, shows how fast it converges, and describes the negotiation. [PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md) then shows why these equalizers become more demanding when the number of voltage levels increases from two to four.

## Core Concepts

### Pulse Response and Impulse Response

Both equalizers act on samples of the pulse response, and the two terms need to be kept apart. [Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md) defines the **impulse response** $h(t)$ as the output of the channel for an infinitely short input of unit area, and the **pulse response** as the output for one bit, a pulse of unit amplitude and one unit interval (UI) in length. A pulse is a step followed one UI later by the opposite step, so the pulse response is the difference between the step response and its copy delayed by one UI. The impulse response is a mathematical object that no transmitter can launch. The pulse response is the quantity that a link produces for every bit.

The receiver samples the pulse response once per UI at its sampling instant. The samples are the **cursors**: the main cursor $A$ (in volts) at the sampling instant, the pre-cursors before it, and the post-cursors after it. Write the cursors in volts as $A h_k$, where $h_k$ are the normalized cursors of [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) with $h_0 = 1$, negative $k$ for pre-cursors, and positive $k$ for post-cursors. With the decided symbols $a_n = \pm 1$, the sample taken for bit $n$ is

$$y_n = A \sum_{k} h_k\, a_{n-k} + \nu_n$$

where $\nu_n$ is the noise at the sampling instant. The terms with $k \neq 0$ make up the intersymbol interference, and the peak-distortion result of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md) gives the worst-case eye height $2A(1 - \sum_{k \neq 0}|h_k|)$. The cursors are properties of the pulse response and not of the impulse response. The two are related by the convolution of that earlier chapter, and a statement such as "the DFE taps equal the impulse response" is correct only in the sense that each tap equals one sample of the pulse response at the cursor spacing.

The main cursor $A$ is smaller than the launch amplitude. The line of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) delivers 0.874 of the launch amplitude at the main cursor, because part of the energy of each bit has moved into the tail. The resistance of the copper at DC accounts for a small part of this: the 12 inches have $R_{DC} = 0.125 \times 12 = 1.5\ \Omega$ in the model of that chapter, and the conductor attenuation at low frequency is $R/(2Z_0) = 1.5/100 = 0.015$ Np, which is 0.13 dB or 1.5 percent of the voltage. The dielectric loss is proportional to frequency and has no DC component. The main cursor is therefore a measured quantity of the received pulse, and the receiver estimates it, as the Architecture section describes.

### The CTLE Transfer Function

[Impedance, Reflections, and Termination](03_Impedance_Reflections_and_Termination.md) derives the transfer function of a resistor and a capacitor, $H = 1/(1 + j\omega RC)$, whose magnitude is $1/\sqrt{1 + (f/f_{3\text{dB}})^2}$. The phasor rule of that chapter replaces the derivative with a multiplication by $j\omega$, and the transfer function of a circuit is therefore a ratio of polynomials in $s = j\omega$. Write the single-pole response with the pole frequency $\omega_p = 1/RC$:

$$H_{pole}(s) = \frac{1}{1 + s/\omega_p}$$

The magnitude is $1/\sqrt{1 + (f/f_p)^2}$, and it equals $0.707$ ($-3.01$ dB, the half-power point of [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md)) at $f = f_p$. For $f \gg f_p$ the magnitude approaches $f_p/f$, and a tenfold increase of frequency reduces it by a factor of 10, which is $-20$ dB per decade. A pole therefore marks the frequency above which the gain falls, and the gain of a single pole decreases at every frequency, faster above $f_p$ than below.

A **zero** is the same factor in the numerator, $1 + s/\omega_z$, and its magnitude $\sqrt{1 + (f/f_z)^2}$ is the reciprocal of the pole magnitude. The gain is $+3.01$ dB at $f_z$ and rises at $+20$ dB per decade above it. A zero alone would amplify without limit, and the pole that follows it limits the rise. The CTLE has one zero and two poles:

$$H(s) = A_{dc}\,\frac{1 + s/\omega_z}{\left(1 + s/\omega_{p1}\right)\left(1 + s/\omega_{p2}\right)}$$

The magnitude of a product is the product of the magnitudes, and the decibel values of [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md) add for a product of gains. The gain curve in decibels is therefore the sum of three simple curves: the zero rises from $f_z$, the first pole cancels the rise above $f_{p1}$, and the second pole causes the gain to fall above $f_{p2}$, which stops the amplification of noise at frequencies where there is no signal.

The **peaking** is the gain at the top of the curve relative to the gain at DC, expressed in decibels as a ratio (the decibel is a ratio and carries no physical unit, as that chapter explains). For $f_z \ll f_{p1}$ and $f_{p2}$ well above $f_{p1}$, the gain in the region $f_{p1} \ll f \ll f_{p2}$ is

$$|H| \approx A_{dc}\,\frac{f/f_z}{f/f_{p1}} = A_{dc}\,\frac{f_{p1}}{f_z} \qquad\Longrightarrow\qquad \text{peaking} \approx 20\log_{10}\frac{\omega_{p1}}{\omega_z}$$

The relation gives an upper estimate of the peaking. The poles are close to the zero and to each other in practical designs, so the curve rounds off before it reaches the plateau, and the Worked Examples section computes an exact curve and compares it with the estimate.

The channel loss of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) rises smoothly with frequency, as $\sqrt{f}$ for the conductor and as $f$ for the dielectric, and the CTLE reproduces the rising part of the curve with a zero and a pole. The match between the filter and the channel is approximate. A smooth curve with three parameters cannot follow the irregular structure of a real channel, which contains resonances from via stubs and reflections from discontinuities. The CTLE corrects the overall slope, and the cursors that remain are the work of the DFE.

### The DFE: Subtracting Decided Bits

The decision feedback equalizer subtracts from each sample a weighted sum of the decisions that precede it. A slicer compares the corrected sample with a threshold (zero for a differential NRZ signal) and outputs the decision $\hat{a}_n = \pm 1$. A logic 1 is represented as $+1$ and a logic 0 as $-1$, because high-speed differential links represent a logic 0 as a negative voltage. The slicer input for bit $n$ is

$$z_n = y_n - \sum_{k=1}^{K} w_k\, \hat{a}_{n-k}$$

where $w_k$ is the weight, in volts, of tap $k$, and $K$ is the number of taps. Tap $k$ reads the decision of bit $n-k$, so a $K$-tap equalizer uses the bits from $n-1$ down to $n-K$. Substitute the sample $y_n$ into this expression and assume that the decisions are correct, $\hat{a}_{n-k} = a_{n-k}$:

$$z_n = A\,a_n + A\sum_{k<0} h_k\, a_{n-k} + \sum_{k=1}^{K}\left(A h_k - w_k\right) a_{n-k} + A\sum_{k>K} h_k\, a_{n-k} + \nu_n$$

The third term vanishes when $w_k = A h_k$ for every tap, and the equalizer then cancels exactly the post-cursors from $k = 1$ to $K$. Three useful properties follow directly from this equation.

**Only post-cursors are cancelled:** The pre-cursor terms $k < 0$ involve the bits $a_{n+1}, a_{n+2}, \dots$, which come after bit $n$ and have not been decided when the slicer evaluates bit $n$. The feedback structure can subtract only what it knows, and the later bits are unknown. A pre-cursor is the work of the transmitter filter or of the CTLE, which act on the waveform and not on decisions. The cursors beyond tap $K$ also remain.

**No noise enhancement:** The noise term $\nu_n$ passes through the equalizer unchanged. The subtracted quantity is a weighted sum of decisions, which are the values $\pm 1$ and carry no noise, so the noise at the slicer input has the variance $\sigma^2$ that it had before the equalizer. A linear equalizer that cancels the same post-cursors by filtering the whole waveform also filters the noise. Consider a channel with a single post-cursor, $y_n = A(a_n + h_1 a_{n-1}) + \nu_n$ with $h_1 = a$. The linear filter that removes the post-cursor is $1/(1 + a z^{-1}) = \sum_k (-a)^k z^{-k}$, and white noise of variance $\sigma^2$ passes through it with the variance $\sigma^2 \sum_k a^{2k} = \sigma^2/(1 - a^2)$, so the rms noise grows by the factor $1/\sqrt{1 - a^2}$:

| Post-cursor $a$ | Linear cancellation, noise rms gain | DFE noise rms gain |
|:---:|:---:|:---:|
| 0.0418 (first cursor of the 12 in line) | 1.0009 (+0.008 dB) | 1 |
| 0.3 | 1.048 (+0.41 dB) | 1 |
| 0.5 | 1.155 (+1.25 dB) | 1 |
| 0.8 | 1.667 (+4.44 dB) | 1 |

The values of $a$ other than the first are illustrative and not tied to a particular channel. The advantage of the DFE is small for the mild interference of the 12 inch line and grows without bound as $a$ approaches 1, which is the case of a large post-cursor that a linear filter could cancel only by amplifying noise.

**Signed arithmetic:** The decision of a logic 0 is $-1$, so the prediction for a logic 0 is the tap weight with a negative sign, and the subtraction adds voltage. The same multiplication handles both polarities, and there is no separate path for zeros and ones.

The nonlinearity gives the DFE its behavior. The equalizer removes interference by discarding the analog value of the previous bit and replacing it with its decision, and the decision has no noise. The price is that a wrong decision is also treated as correct, and the Edge Cases section quantifies the consequence.

## Architecture

### The Data Path and the Control Path

The circuit that performs the subtraction contains delay registers that hold the past decisions, one digital-to-analog converter (DAC) per tap that converts the weight $w_k$ into a current, switches that choose the sign of that current from the stored decision, and a summing node in front of the slicer. All of it operates at the full symbol rate. The tap currents steer into the summing node according to the past decisions: a decision of $+1$ closes one switch of a differential pair and sends $+I_k$ into the node, and a decision of $-1$ sends $-I_k$. By Kirchhoff's current law the currents add at the node, and the net current across the load resistance becomes the correction voltage. The weights come from a separate and much slower block, the adaptation engine, which writes them into registers that the DACs read. The data path runs at the gigahertz line rate, processing transitions in picoseconds. The control path updates the registers at a small fraction of that rate. The sub-sampled architecture is mathematically sound because the physical channel changes over milliseconds as temperature drifts, which is millions of times slower than the data rate. The high-speed data path continuously uses the static tap weights while the adaptation loop operates on its own slow clock to track the thermal drift.

The CTLE belongs to the data path as well. The order is CTLE, summing node, slicer, and the decisions return to the summing node through the tap registers. Clock recovery uses the same signal, and the sampling instant that [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) describes is the instant at which the main cursor is sampled.

### Where the CTLE Zero and Poles Come From

The CTLE structure follows from a standard circuit, a differential pair with a resistor $R_s$ and a capacitor $C_s$ connected in parallel between the two sources (source degeneration). Treat each half of the pair as an amplifier with transconductance $g_m$ and load resistance $R_L$. The two sources move in opposite directions, so the midpoint of $R_s$ is a virtual ground, and each half sees a degeneration impedance made of $R_s/2$ in parallel with $2C_s$ to ground:

$$Z_{deg} = \frac{R_s/2}{1 + s R_s C_s}$$

The gain of a transistor with a source impedance $Z_{deg}$ is $g_m R_L/(1 + g_m Z_{deg})$. Substitute the impedance:

$$G(s) = \frac{g_m R_L}{1 + \dfrac{g_m R_s/2}{1 + sR_sC_s}} = \frac{g_m R_L\,(1 + sR_sC_s)}{1 + g_m R_s/2 + sR_sC_s}$$

Divide the numerator and the denominator by $1 + g_mR_s/2$ and define $\omega_z = 1/(R_sC_s)$:

$$G(s) = \frac{g_m R_L}{1 + g_m R_s/2}\;\frac{1 + s/\omega_z}{1 + s/\omega_{p1}}, \qquad \omega_{p1} = \left(1 + \frac{g_m R_s}{2}\right)\omega_z$$

The DC gain is reduced by the degeneration, the gain at high frequency is $g_m R_L$ (the capacitor short-circuits the resistor), and the ratio of the two is $1 + g_mR_s/2 = \omega_{p1}/\omega_z$, which is the peaking of the estimate above. The load resistance with its capacitance $C_L$ adds the second pole $\omega_{p2} = 1/(R_LC_L)$. The relation $\omega_{p1}/\omega_z = 1 + g_mR_s/2$ shows how the designer sets the peaking: a larger degeneration resistance gives a lower DC gain and more peaking, and the capacitor sets the frequency $\omega_z$ at which the peaking begins. The noise of the stage is shaped by the same gain, and the Edge Cases section quantifies the result for the filter of the Worked Examples.

### The Error Signal and the Main-Cursor Target

An adaptation engine cannot find the tap weights from the data path alone, because the slicer produces only decisions. The receiver therefore has a second comparator, the **error slicer**, which compares the corrected sample $z_n$ with the expected level $A \hat{a}_n$ and records the difference

$$e_n = z_n - A\,\hat{a}_n$$

The expected level uses the main-cursor amplitude $A$, and the engine estimates $A$ from the data. A pseudo-random bit sequence (PRBS) is strictly used for initial link training, as [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) details. Live traffic adaptation relies entirely on decision-directed tracking. The receiver treats its own slicer output $\hat{a}_n$ as the perfect mathematical reference, assuming every decision is correct. The receiver correlates this instantaneous error from the error slicer with the bit history to find the gradient that updates the taps. A target equal to the launch amplitude would make the error include the loss of the channel at DC and the spread of the pulse, and the taps would try to correct a quantity that no equalizer can restore. The error is positive when the corrected sample lies above the expected level and negative when it lies below, and it contains the residual interference and the noise at the sampling instant and nothing else. The estimate of $A$ is adapted by the rule that follows in the next section.

### The LMS Update as Gradient Descent

The adaptation engine chooses the weights that minimize the mean squared error $J = E[e_n^2]$. The error depends on the weights through $z_n$, and $\partial e_n/\partial w_k = -\hat{a}_{n-k}$, so the gradient of the cost with respect to a tap is

$$\frac{\partial J}{\partial w_k} = 2\,E\!\left[e_n\,\frac{\partial e_n}{\partial w_k}\right] = -2\,E\!\left[e_n\,\hat{a}_{n-k}\right]$$

Steepest descent moves each weight a small step against the gradient, $w_k \leftarrow w_k - (\mu/2)\,\partial J/\partial w_k$, where $\mu$ is the step size (a dimensionless constant, because the error and the weight are both in volts and the decision has no unit):

$$w_k \leftarrow w_k + \mu\,E\!\left[e_n\,\hat{a}_{n-k}\right]$$

The expectation requires an average over many bits. The **least mean squares** (LMS) algorithm replaces the expectation by the value for the current bit, which costs one multiplication per tap and gives the update of the hardware:

$$w_k^{new} = w_k^{old} + \mu\, e_n\, \hat{a}_{n-k}$$

The sign of the update is correct. A positive error with $\hat{a}_{n-k} = +1$ means that the sample is too high because too little of the contribution of bit $n-k$ was subtracted, and the weight increases. The same gradient argument applies to the main-cursor estimate, because $\partial e_n/\partial A = -\hat{a}_n$, and it gives $A \leftarrow A + \mu\,e_n\hat{a}_n$.

The behavior of the update follows from the expected value. Assume that the decisions are correct and that the bits are independent with zero mean, so that $E[a_ia_j] = 0$ for $i \neq j$ and $E[a_i^2] = 1$. The error is $e_n = \sum_{k \ge 1}(Ah_k - w_k)\,a_{n-k} + (\text{terms with other bits}) + \nu_n$, and the average of its product with $a_{n-j}$ keeps only the term of the same bit:

$$E\!\left[e_n\,a_{n-j}\right] = A h_j - w_j$$

The update therefore moves each weight toward the cursor that it should cancel, and the average step is proportional to the remaining distance:

$$w_j^{(m+1)} - A h_j = (1 - \mu)\left(w_j^{(m)} - A h_j\right)$$

The distance falls by the factor $(1 - \mu)$ per update, so it decays exponentially with the time constant $1/\mu$ updates. Each tap converges to its own cursor because the bits are independent: the pre-cursor terms and the terms of other taps average to zero in the product with $a_{n-j}$, and only the cursor of that tap survives. A tap that corresponds to a cursor of zero converges to zero. [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) shows that a pseudo-random pattern supplies the independence that this result requires.

The step size sets a compromise between speed and accuracy. The weight fluctuates around its mean because each update contains the part of the error that is uncorrelated with $a_{n-j}$, which has a variance $\sigma_\varepsilon^2$ (the noise and the residual of the other taps). Define the distance from the target as $u = w_j - Ah_j$. Then $u_{m+1} = (1 - \mu)u_m + \mu\,\varepsilon_m$ with $\varepsilon_m$ of variance $\sigma_\varepsilon^2$, and in the steady state

$$\mathrm{var}(u) = \frac{\mu^2\sigma_\varepsilon^2}{1 - (1-\mu)^2} = \frac{\mu}{2 - \mu}\,\sigma_\varepsilon^2$$

A larger $\mu$ converges faster and leaves a larger fluctuation of the weights. The assumption that decisions are correct fails during normal operation, because noise inevitably causes raw slicer errors. The adaptation loop survives these errors solely through the law of large numbers and the tiny step size ($\mu$). The incorrect updates average to zero over millions of samples. The adaptation loop cannot use bits corrected by forward error correction, because the decoding latency of the pipeline detailed in [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) is far too massive for picosecond feedback. The physical survival of the analog loop relies purely on statistics, while the digital survival of the payload relies on the code. The Worked Examples section gives the numbers. The error shrinks as the taps converge, so the production hardware keeps the loop running, which lets the taps follow the slow changes of temperature and supply voltage.

### Link Training

The transmitter filter, the CTLE setting, and the DFE taps depend on each other. The optimum transmitter taps depend on how hard the receiver equalizes, and the optimum receiver settings depend on the residual that the transmitter leaves. The Worked Examples section shows the dependence with numbers: the best transmitter tap on the 12 inch line is $-0.040$ without a DFE and zero with one. A setting measured in the laboratory serves only as a starting value, since the channel differs from board to board and the silicon differs from lot to lot.

Modern standards therefore set the transmitter taps through a negotiation at every start-up, wake-up, and cable insertion. The structure is common to the protocols that use training, and the paragraph in [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) states its request semantics:

1. **Starting point:** The transmitter begins with a preset, a predefined combination of taps that is safe for a wide range of channels.
2. **Receiver adaptation:** The transmitter holds its taps, and the receiver adapts its CTLE and DFE to the received training pattern with the LMS update above and measures a figure of merit of the result, such as the eye height or the error count.
3. **Request:** The receiver sends a request to the transmitter on a low-speed return path. The request is an instruction to increase, decrease, or hold a transmitter tap, or a request for a specific preset.
4. **Update:** The transmitter changes the tap within the limits of its normalization (the sum of the magnitudes of the taps is 1) and reports that the change took effect, and the receiver measures the figure of merit again.
5. **Convergence:** The receiver repeats steps 2 to 4 until the figure of merit stops improving, then declares the link trained and the data transfer begins.

The loop measures a figure of merit after the receiver has adapted, so each trial requires the receiver adaptation to settle first, and the time per trial is set by the convergence time derived above. The number of trials that fit in the time that a protocol allows for training is therefore finite, which limits the size of the search. The training pattern is pseudo-random for the reason that the previous section uses.

### Implementation Note: the First Tap and Speculation

The decision of bit $n-1$ must reach the summing node before the slicer evaluates bit $n$, so the first tap closes a feedback loop whose delay must be shorter than one UI. At 32 Gbaud the UI is 31.25 ps, and the loop contains the slicer, the register, the switch, and the summing node. A common solution is to speculate: the receiver evaluates $\mathrm{sgn}(y_n - w_1)$ and $\mathrm{sgn}(y_n + w_1)$ in parallel for the two possible values of $\hat{a}_{n-1}$ and selects one with a multiplexer controlled by the previous decision, so that the loop delay is the delay of the multiplexer only. The result is the same as the equation above, and the cost is a second slicer.

The same equations describe an equalizer whose decisions are computed digitally after an analog-to-digital converter, in which the taps are binary multiplications in logic. [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md) compares the analog front end with the converter-based receiver, and only the implementation differs from this chapter.

## Worked Examples

### A CTLE for the 12 Inch Line

Over 12 inches, the line of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) has the insertion loss $IL(f) = 12\,(0.20\sqrt{f/5} + 0.47\,f/5)$ dB with $f$ in GHz. This gives 8.04 dB at 5 GHz (the 8.1 dB of [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md) with the rounded constants), which is the Nyquist frequency of a 10 Gb/s link. Choose a CTLE with $f_z = 1.5$ GHz, $f_{p1} = 6$ GHz, $f_{p2} = 15$ GHz, and $A_{dc} = 1$. The circuit of the previous section needs $g_mR_s/2 = f_{p1}/f_z - 1 = 3$ for this ratio. The gain follows from the three factors:

$$|H(f)| = \frac{\sqrt{1 + (f/1.5)^2}}{\sqrt{1 + (f/6)^2}\,\sqrt{1 + (f/15)^2}}$$

The asymptotic estimate of the peaking is $20\log_{10}(6/1.5) = 12.04$ dB. The exact curve peaks at 9.23 dB near 9.2 GHz, because the second pole and the proximity of the first pole round off the plateau. The table compares the filter with the channel:

| $f$ (GHz) | Channel loss (dB) | CTLE gain (dB) | Net (dB) |
|:---:|:---:|:---:|:---:|
| 0.5 | 1.32 | 0.42 | $-0.90$ |
| 1 | 2.20 | 1.46 | $-0.74$ |
| 1.5 | 3.01 | 2.70 | $-0.30$ |
| 2.5 | 4.52 | 4.96 | $+0.44$ |
| 5 | 8.04 | 8.08 | $+0.04$ |
| 7.5 | 11.40 | 9.09 | $-2.31$ |
| 10 | 14.67 | 9.21 | $-5.47$ |

The net response is within 0.9 dB of flat from 0.5 GHz to the Nyquist frequency, and the Nyquist tone, which the channel reduces to 0.396 of its amplitude, leaves the filter at 1.005. Above the Nyquist frequency the net response falls to $-5.47$ dB at 10 GHz. The data pattern has no fundamental above 5 GHz, so the shortfall affects only the edge content, and the cursors that result from it are part of what the DFE removes. The zero sits at the frequency at which the channel loss reaches 3 dB (1.5 GHz in the table). The estimate of 12.04 dB exceeds the 8.08 dB that the filter delivers at the Nyquist frequency by 4 dB, which is the reason that the exact calculation is needed.

### Cancelling the Cursors of the 12 Inch Line

Take the pulse response of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) at 10 Gb/s and the receiver values of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md), a main cursor of $A = 200$ mV. The first seven normalized post-cursors are 0.0418, 0.0186, 0.0111, 0.0076, 0.0056, 0.0044, and 0.0035, so the weights of the DFE in volts are $w_k = A h_k = 8.37$, 3.72, 2.22, 1.52, 1.12, 0.87, and 0.70 mV.

For a bit $n$ with the previous three decisions $(+1, -1, +1)$ the sample is $200 + 8.37(+1) + 3.72(-1) + 2.22(+1) = 206.87$ mV for $a_n = +1$. The DFE subtracts $8.37(+1) + 3.72(-1) + 2.22(+1) = 6.87$ mV and the slicer sees 200.00 mV. The subtraction follows the history of the bits, so the same cancellation applies to every pattern, and the interference of this history is removed whether it adds to the sample or subtracts from it.

The cursors of this model decay as $t^{-3/2}$ because they come from the erfc step response of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md), and the sum of the post-cursors beyond tap $K$ is $(1 - s((K+1)\,UI))/h_{main}$ with the step response $s$ normalized to its final value 1. The first seven cursors of the earlier chapters sum to 9.26 percent, and the sum of all post-cursors is 14.35 percent, because the tail beyond the seventh cursor holds the other 5.09 percent. The residual after $K$ taps and the resulting eye height $2A(1 - R(K))$ are:

| Taps $K$ | Residual $R(K)$ | Eye height (mV) |
|:---:|:---:|:---:|
| 0 | 14.35% | 342.6 |
| 1 | 10.17% | 359.3 |
| 3 | 7.20% | 371.2 |
| 7 | 5.09% | 379.6 |
| 15 | 3.60% | 385.6 |
| 31 | 2.55% | 389.8 |

The eye heights of 363 mV and 364 mV in [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) and [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md) count only the first seven cursors, and the 342.6 mV of the first row counts all of them. The residual falls as $1/\sqrt{K}$, so a long tail needs many taps for a small gain: going from 7 to 31 taps halves the residual (5.09 to 2.55 percent) and adds 10 mV of eye height. The ideal conditions of the table are correct decisions, no noise, and no reflections.

### LMS Convergence

Take the update $w_k \leftarrow w_k + \mu e_n \hat{a}_{n-k}$ with the weights starting from zero. The distance to the cursor falls by the factor $(1-\mu)^m$ after $m$ updates, and it reaches 1 percent when $m = \ln(100)/(-\ln(1 - \mu))$. The steady-state fluctuation follows from the variance formula with $\sigma_\varepsilon = 10$ mV:

| $\mu$ | Updates to reach 1 percent | Fluctuation of a weight (rms) |
|:---:|:---:|:---:|
| 0.1 | 44 | 2.29 mV |
| 0.01 | 458 | 0.71 mV |
| 0.001 | 4,603 | 0.22 mV |

The first tap of the example has the weight 8.37 mV, so a fluctuation of 0.71 mV is 8.5 percent of that tap, and a smaller step size is required for the later taps, whose weights are about 1 mV or below. A practical engine starts with a large step and reduces it as the error falls. Each update uses one product per tap, so the cost scales with the number of taps and not with the length of the channel.

### The Optimum Transmitter Tap Depends on the Receiver

Apply the transmitter filter of [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) with a post-cursor tap $c_1$ only ($c_0 = 1 - |c_1|$) to the 12 inch line and compute the eye height for a receiver with no DFE, with a one-tap DFE, and with a seven-tap DFE. The eye is $2A(1 - |c_1|)(1 - R)$, where $R$ is the sum of the magnitudes of the post-cursors of the combined response that the DFE does not cancel. The values use all the cursors of the model and ideal decisions:

| $\lvert c_1\rvert$ | No DFE (mV) | One tap (mV) | Seven taps (mV) |
|:---:|:---:|:---:|:---:|
| 0 | 342.6 | 359.3 | 379.6 |
| 0.040 | 347.2 | 347.2 | 365.2 |
| 0.100 | 304.2 | 329.1 | 343.8 |
| 0.200 | 232.3 | 298.9 | 308.1 |
| 0.303 | 158.3 | 267.8 | 271.2 |

Without a DFE the best tap is $|c_1| = 0.040$, the tap that zeroes the first post-cursor, and it gives 347.2 mV. With any DFE of one tap or more the best tap is zero, because the DFE cancels the post-cursors without the amplitude cost of the transmitter filter. A link that starts from the 8.1 dB preset at $|c_1| = 0.303$ and requests decreases of the tap improves at every step until $|c_1| = 0.040$ when the receiver has no DFE, and until $|c_1| = 0$ when it has one, so the point at which the training stops depends on what the receiver can do. The channel of the example is mild. A long channel still needs the transmitter filter with a DFE, because the filter reduces the size of the cursors that the DFE has to cancel, and the error propagation result of the next section shows that large cursors raise the probability of a burst.

## Edge Cases

### Error Propagation in the DFE

A wrong decision enters the feedback sum as if it were correct. Suppose that the decision of bit $n-1$ is wrong and that the tap weight is $w_1 = A h_1$. The subtraction is then wrong by $2 A h_1$ (the difference between $+1$ and $-1$ times the weight). The sample of the next bit lies at $\pm A$ from the threshold with the error in the direction that depends on its value, so the margin of that bit is $A(1 - 2h_1)$ in one case and $A(1 + 2h_1)$ in the other. Write $z = A/\sigma$ for the margin in standard deviations, which [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md) relates to the error ratio by the Q function. The probability that the next bit is wrong, given the first error, is

$$P_2 = \tfrac12\left[Q\big((1 - 2h_1)z\big) + Q\big((1 + 2h_1)z\big)\right]$$

For a link whose margin is $z = 7.034$ (the Q-factor for $10^{-12}$ in the table of that chapter), the first cursor of the 12 inch line, $h_1 = 0.0418$, gives $P_2 = 2.9 \times 10^{-11}$, which is 29 times the nominal error ratio. A channel with a first cursor of $h_1 = 0.3$ gives $(1 - 0.6)z = 2.81$ and $P_2 = 1.2 \times 10^{-3}$, nine orders of magnitude above the nominal value. Errors therefore arrive in short bursts, and the burst length depends on the size of the cursors that the DFE cancels. A large first tap is a weakness in this respect, which is another reason to share the equalization with the transmitter filter and the CTLE, and the forward error correction of [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) exists in part to correct bursts. A precoding step at the transmitter, which shapes the data so that a burst shortens, is a known remedy that this chapter does not derive.

### CTLE Noise Amplification

A linear filter that follows the point where the noise is added has the same signal-to-noise ratio at every frequency as the signal that enters it, because it multiplies the signal and the noise at each frequency by the same factor. The CTLE therefore cannot improve the signal-to-noise ratio of any tone, and what it changes is the weighting between frequencies. The filter of the Worked Examples section restores the Nyquist tone from 0.396 to 1.005, a gain of 8.08 dB (2.54 times), and the noise at that frequency receives the same gain. For noise that is white over a bandwidth $B$, the rms gain is $\sqrt{\frac{1}{B}\int_0^B |H|^2\,df}$, which gives 1.82 (5.20 dB) for $B = 5$ GHz and 2.36 (7.48 dB) for $B = 10$ GHz. A receiver whose front end is wider than the signal needs adds noise at frequencies where the signal has no energy, and the second pole $f_{p2}$ exists to stop this.

The cost is largest for a channel that is not lossy. The same filter on a short channel boosts the noise by the factor above and restores nothing, so the optimum peaking depends on the loss and the link training searches for it. The comparison with the table of the DFE section explains the division of labor: the CTLE takes the smooth part of the loss, and the DFE takes the long tail, which a linear filter could remove only at the price of amplified noise.

### Reflections and the Span of the Taps

A reflection is a post-cursor located at the round-trip delay of its discontinuity, which [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md) also states. A $K$-tap DFE cancels reflections whose round trip is shorter than $K$ UI and leaves the others, and no CTLE setting removes a reflection, because a smooth filter with three parameters has no response that matches a delayed echo. A reflection at a delay of 1 ns is the tenth cursor for a UI of 100 ps, and it needs a DFE of at least ten taps. The pulse response measured by the receiver contains it, and the LMS update places a tap at that position without any knowledge of the cause.

### Baseline Wander and the Long Tail

The coupling capacitor of the link adds a very small and very long negative tail to the pulse response, with the time constant of its high-pass response. No tap of the DFE reaches this tail. The effect and the disparity bound that limits it belong to [Return Path Dynamics and Parasitic Effects](06_Return_Path_Dynamics_and_Parasitic_Effects.md), in the section The Series Capacitor and Baseline Wander, and the line codes of [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) limit it by construction.

### Training Search and Local Minima

The training procedure searches a space with several dimensions: the transmitter taps, the CTLE peaking, and the number of DFE taps in use. The figure of merit that the receiver measures at each point is the result after its own adaptation, so it is noisy and its dependence on the parameters need not be a single smooth hill. A step in the wrong direction can look like an improvement, and the search can stop at a combination that is better than its neighbors and worse than the best. The designer reduces the risk through the starting presets and the step sizes of the state machine. The search fails whatever its algorithm when the equalization that the silicon provides is smaller than the loss of the channel.
