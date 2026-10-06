# CDR and PLL Loop Dynamics

<!-- SUMMARY: High-speed serial links embed the clock in the data, and the receiver recovers its sampling clock from the data transitions with a phase-locked loop. This guide derives why the clock is embedded, the early/late (bang-bang) and baud-rate phase detectors, the linear phase model of a Type-I and a Type-II loop, the jitter transfer function with its bandwidth and peaking, and the error transfer function that the sampler sees, which reconciles the low-pass tracking of the clock with the high-pass jitter that remains in the measured timing. It then covers cycle slips and slew limits, the golden PLL that standards and instruments use to define how much jitter a receiver tracks, and the jitter tolerance curve. One numerical loop is carried through every worked example. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md) placed the clock and data recovery circuit (CDR) in parallel with the slicer. Its output is the clock that strobes the slicer, so it decides where in each unit interval the decision is made, and [CTLE and DFE](14_CTLE_and_DFE.md) noted that this instant is the one at which the main cursor is sampled. This chapter is the single home of embedded clocking, of the phase-locked loop (PLL) model that describes the CDR, of the jitter transfer function (JTF), and of the golden PLL by which standards define the clock that a measurement must use.

The CDR is a filter with chosen dynamics and not only a clock extractor. Slow timing variations of the data, such as drift from temperature or the small frequency difference between two crystals, must be followed so that the sampling instant stays in the eye. Fast variations must not be followed, because a clock that jumps with every edge displacement carries no stable timing reference. The boundary between the two behaviors is the loop bandwidth, and the shape of the response near that boundary decides whether the loop amplifies jitter at some frequency.

Two statements about the same loop appear contradictory at first. The recovered clock follows the slow components of the data timing, which makes the loop a low-pass filter for jitter. The timing error that the sampler experiences, the difference between the data edge and the recovered clock, contains only the components that the loop does not follow, which makes it a high-pass quantity. [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) stated this relation with a first-order model, and this chapter derives it for the first-order and second-order loops and shows that the two statements are complementary. One numerical loop, introduced in the Worked Examples, serves every calculation.

## Core Concepts

### Why the Clock Is Embedded

A separate clock trace next to the data trace must keep its phase relative to the data across manufacturing variation, temperature, and cable length. The unit interval at 16 Gb/s is 62.5 ps, and the FR4 delay of [Wave Propagation and Transmission Lines](01_Wave_Propagation_and_Transmission_Lines.md) is 170 ps per inch. A length mismatch of 0.37 inch between the clock and data traces therefore shifts the clock by a full unit interval, and a skew budget of 10 percent of the interval (6.25 ps) allows a mismatch of only 0.037 inch, which is 0.93 mm. The delay also changes with the material. The delay of a line is $t_d = \ell\sqrt{\varepsilon_r}/c$, so a relative change $\delta\varepsilon_r/\varepsilon_r$ of the permittivity changes the delay by half that fraction. A 1 percent change over 10 inches (1.7 ns) shifts the delay by 8.5 ps, which is more than a tenth of the interval.

Embedding the clock in the data removes the problem. The receiver derives its clock from the transitions of the data it must sample, so the clock and the data share the same drift by construction, and the skew between a separate clock and the data never arises. The price is the requirement of transitions. A stream with a long run of identical bits has no edges to align to. The loop then runs freely on the frequency that it has stored, and the drift during a run is the residual frequency error multiplied by the length of the run. Assume that the residual error is 200 ppm. The phase drifts by 0.001 UI during a run of 5 bits (the limit of 8b/10b) and by 0.0132 UI (0.83 ps) during a run of 66 bits, and a full unit interval accumulates only after $1/(200 \times 10^{-6}) = 5{,}000$ bits without any transition. The line codes of [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) bound the run length far below that number.

The transmitter and the receiver derive their clocks from separate crystal oscillators, commonly 100 MHz. A PLL multiplies the reference to the line rate (100 MHz multiplied by 160 gives 16 GHz). Two crystals with a tolerance of 100 ppm each differ by up to 200 ppm, and the data frequency at the receiver differs from the receiver's own clock by up to $16\ \text{GHz} \times 200\ \text{ppm} = 3.2$ MHz. The CDR must absorb this offset and recover the exact phase of the data on top of it.

### Phase, Frequency, and the Integrating Oscillator

A voltage-controlled oscillator (VCO) changes its frequency with a control voltage $v_c$. With a gain $K_{vco}$ in rad/s per volt (equal to $2\pi$ times the gain in Hz per volt), the frequency is $\omega_0 + K_{vco} v_c$. The phase accumulated relative to the free-running frequency $\omega_0$ is the integral of the frequency deviation:

$$\theta_{out}(t) = K_{vco}\int_0^t v_c(\tau)\,d\tau \qquad\Longleftrightarrow\qquad \Theta_{out}(s) = \frac{K_{vco}}{s}\,V_c(s)$$

The VCO is an integrator from voltage to phase. A change of phase therefore requires a temporary difference in frequency. Two identical clocks at 10 GHz, with aligned edges, differ in phase by 5 ps after one of them runs at 11 GHz for 50 ps and returns to 10 GHz (the extra 1 GHz over 50 ps adds $10^9 \times 50 \times 10^{-12} = 0.05$ cycle, which is 5 ps of a 100 ps period). The VCO has no separate phase control, and every phase correction is made by a brief change of frequency.

The phase detector sees only phase, because it measures the time between a data edge and a clock edge at one instant and has no memory. Frequency matching is a consequence of the loop settling. The frequency is the derivative of the phase, so a constant phase difference between the data and the clock means $d\theta_{in}/dt = d\theta_{out}/dt$, and the two frequencies are equal. A loop with only a phase detector acquires lock when the initial frequency difference lies within its pull-in range, which is limited. A larger offset makes the phase error slip through many cycles, the sign of the detector output alternates, and its average correction vanishes. CDRs therefore either add a frequency detector or begin from a local reference clock whose frequency differs from the data by only parts per million, as in the clock architecture above, and for that case the phase detector alone is sufficient. The common statement that a PLL has no frequency detector describes the basic loop and not every receiver.

### The Phase Detector: Early and Late Decisions

The phase detector most widely used in CDRs is the **Alexander** detector, also called the early/late or bang-bang detector. It samples the data three times around each transition: at the center of the bit before the transition ($D_{n-1}$), at the nominal crossing between the two bits ($E_n$, the edge sample), and at the center of the next bit ($D_n$), and the comparison of the three samples has three outcomes.

- Equal data samples ($D_{n-1} = D_n$) mean that there is no transition, and the samples carry no timing information, so the output is zero.
- Different data samples with an edge sample equal to the earlier bit ($E_n = D_{n-1}$) mean that the edge sample was taken before the data crossing, so the clock is early and the loop must delay it.
- Different data samples with an edge sample equal to the later bit ($E_n = D_n$) mean that the sample was taken after the crossing, so the clock is late and the loop must advance it.

Two exclusive-OR gates produce the flags, $\text{early} = E_n \oplus D_n$ and $\text{late} = E_n \oplus D_{n-1}$. Both gates give the same value when there is no transition, and the net output is zero. The detector output is **binary**, because it reports the sign of the phase error and not its size. A clock that is 1 ps early and one that is 20 ps early produce the same output. A charge pump turns the flag into a current of $+I_{cp}$ or $-I_{cp}$ into the loop filter.

A binary detector looks nonlinear, and it is, but the timing noise on the data linearizes it on average. Assume that the phase error of the clock relative to the edge is $\varphi$ and that the edge position carries Gaussian jitter of standard deviation $\sigma_\varphi$ (in radians). The detector reports "late" when $\varphi + n > 0$ and "early" otherwise, with $n$ Gaussian. The expected output of the detector is

$$E[\text{output}] = P(n > -\varphi) - P(n < -\varphi) = 1 - 2Q\!\left(\frac{\varphi}{\sigma_\varphi}\right) = \operatorname{erf}\!\left(\frac{\varphi}{\sigma_\varphi\sqrt{2}}\right)$$

with the Q function of [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md). For small $\varphi$ the error function is $\operatorname{erf}(u) \approx 2u/\sqrt{\pi}$, so the expected output is $\varphi\sqrt{2/\pi}/\sigma_\varphi$. Only a fraction $\eta_T$ of the bit boundaries carry a transition ($\eta_T = 1/2$ for random NRZ data, the transition density of [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md)). The average current per radian of phase error is therefore the effective phase detector gain

$$K_{pd} = \eta_T\,I_{cp}\,\frac{\sqrt{2/\pi}}{\sigma_\varphi}$$

The gain **decreases as the jitter grows**, and so does the loop bandwidth. The loop of a bang-bang CDR is a linear loop whose gain is set by the amount of timing noise at its input, and the linear model of the following sections holds for jitter frequencies far below the symbol rate, where the averaging over many edges is valid.

A **baud-rate** detector uses one sample per unit interval. The Mueller-Muller detector forms $e_n = y_n \hat{a}_{n-1} - y_{n-1}\hat{a}_n$ from the sample $y_n$ and the decision $\hat{a}_n$. Write $y_n = A\sum_k h_k a_{n-k}$ with the cursors $h_k$ of [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) ($h_0 = 1$, post-cursors for $k > 0$). For independent data with $a_n = \pm 1$ and correct decisions, $E[y_n a_{n-1}] = A h_1$ and $E[y_{n-1} a_n] = A h_{-1}$, because only the term with the matching bit survives the averaging. The expected value of the timing error is

$$E[e_n] = A\,(h_1 - h_{-1})$$

The loop settles where the post-cursor equals the pre-cursor. A pulse with a long causal tail has $h_1 > h_{-1}$ at its peak, so the loop moves the sampling instant later than the peak of the pulse. The detector needs no edge sample and only one sample per unit interval, which halves the sampling rate of a converter compared with an edge-based detector. The equalizer changes the cursors, and the tap adaptation of [CTLE and DFE](14_CTLE_and_DFE.md) and the timing loop therefore interact.

### The Loop Filter and the Linear Phase Model

The loop closes through four elements: the phase detector produces a current $i = K_{pd}(\theta_{in} - \theta_{out})$, the loop filter with the impedance $Z(s)$ converts the current to the control voltage $V_c = Z(s)\,I$, the VCO integrates the voltage into phase as above, and the VCO phase returns to the detector. The open-loop transfer function of this chain is

$$L(s) = \frac{K_{pd}\,Z(s)\,K_{vco}}{s}$$

and the phase of the clock relative to the phase of the data follows from $\Theta_{out} = L\,(\Theta_{in} - \Theta_{out})$:

$$T(s) = \frac{\Theta_{out}}{\Theta_{in}} = \frac{L(s)}{1 + L(s)}, \qquad E(s) = \frac{\Theta_{in} - \Theta_{out}}{\Theta_{in}} = 1 - T(s) = \frac{1}{1 + L(s)}$$

$T$ is the **jitter transfer function** and $E$ is the **error transfer function**. Phase in radians and jitter in picoseconds are proportional, $\theta = 2\pi\,t_j/UI$, so both functions apply to either unit.

Two classifications describe the dynamics of a loop, and the **type** is the number of poles of $L(s)$ at the origin, which is the number of integrators in the open loop (the VCO contributes one). The **order** is the degree of the denominator of $T(s)$, the number of poles of the closed loop. The two differ from the older description in terms of the energy-storage elements of the loop filter. A resistor-only filter gives a Type-I loop of first order, because the only energy storage in the loop is the phase of the VCO. A resistor in series with a capacitor adds an integrator, which gives a Type-II loop of second order. A second small capacitor in parallel, used to smooth the control voltage, adds a third pole and makes the loop third order while it remains Type II.

### Type-I Loop: Proportional Control

The filter is a resistor, $Z = R$, and the open loop is $L(s) = \omega_L/s$ with $\omega_L = K_{pd} R K_{vco}$. The closed loop of this filter is

$$T(s) = \frac{\omega_L}{s + \omega_L} = \frac{1}{1 + s/\omega_L}$$

which is the single-pole low-pass of [Impedance, Reflections, and Termination](03_Impedance_Reflections_and_Termination.md) with the corner frequency $f_L = \omega_L/2\pi$. The loop is unconditionally stable, and the magnitude $1/\sqrt{1 + (f/f_L)^2}$ shows no peaking. The error transfer function is $E = (s/\omega_L)/(1 + s/\omega_L)$, which has the magnitude

$$|E(f)| = \frac{f/f_L}{\sqrt{1 + (f/f_L)^2}}$$

and reproduces the first-order expression of [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) with $f_c = f_L$.

The limitation of a Type-I loop is a static phase error. Assume that the data frequency exceeds the free-running VCO frequency by $\Delta\omega$. The phase of the data then ramps as $\theta_{in} = \Delta\omega\,t$, with the transform $\Delta\omega/s^2$. The final value theorem gives the steady-state phase error

$$\theta_e(\infty) = \lim_{s\to 0} s\,E(s)\,\frac{\Delta\omega}{s^2} = \lim_{s\to 0}\frac{\Delta\omega}{s + \omega_L} = \frac{\Delta\omega}{\omega_L}$$

The error is permanent because the VCO needs a control voltage $v_c = \Delta\omega/K_{vco}$ to hold the frequency offset. The resistor produces a voltage only while current flows, and the detector produces current only while the phase error is nonzero, so the phase error cannot return to zero without removing the voltage that holds the frequency. The same result follows from the group delay of [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md). The low-frequency group delay of $T(s)$ is $1/\omega_L$, so the recovered clock lags the data by that time, and a frequency offset $\Delta f$ with a lag of $1/\omega_L$ accumulates the phase error $\Delta f/f_L$ cycles. Raising the loop gain reduces the error in proportion, but the gain is limited by the delay around the loop and by the noise that a wide loop passes. A loop filter with a capacitor removes the error.

### Type-II Loop: Proportional Plus Integral Control

A capacitor in series with the resistor gives $Z(s) = R + 1/(sC)$. The control voltage is the sum of the proportional part $IR$ and the integral part $\frac{1}{C}\int I\,dt$. The series arrangement is essential, because a capacitor in parallel with the resistor would smooth away the fast voltage that the resistor provides and would remove the proportional response. In series, the VCO receives an immediate correction from the resistor for sudden phase jumps and a stored voltage from the capacitor that holds a frequency offset. The open loop of the Type-II filter is

$$L(s) = K_{pd}K_{vco}\,\frac{R + 1/(sC)}{s} = \frac{K s + K\omega_z}{s^2}, \qquad K = K_{pd}K_{vco}R, \quad \omega_z = \frac{1}{RC}$$

The closed loop is $T = L/(1+L)$:

$$T(s) = \frac{K s + K\omega_z}{s^2 + K s + K\omega_z} = \frac{2\zeta\omega_n s + \omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

with the natural frequency and damping factor

$$\omega_n = \sqrt{K\omega_z} = \sqrt{\frac{K_{pd}K_{vco}}{C}}, \qquad \zeta = \frac{K}{2\omega_n} = \frac{R}{2}\sqrt{K_{pd}K_{vco}C}$$

The zero of $T$ is at $\omega_z = \omega_n/(2\zeta)$. The error transfer function of this loop is

$$E(s) = 1 - T(s) = \frac{s^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

It has a double zero at $s = 0$, so a frequency offset ($\Delta\omega/s^2$) leaves the error $\lim_{s\to0} s\cdot E\cdot\Delta\omega/s^2 = 0$. The integrator drives the static phase error of a frequency offset to zero, and this is the reason that every standard that uses two independent crystals specifies a second-order CDR. At low frequency $T \approx 1 - s^2/\omega_n^2$, which has no linear term in $s$, so the group delay of the loop is zero at DC and the loop follows a phase ramp without lag.

The approach to zero error needs an overshoot of the frequency. The phase error changes only through a frequency difference, so the clock can catch up to a late data edge only by running faster than the data for a time. The VCO frequency therefore rises past the data frequency, closes the phase gap, and settles back as the capacitor discharges.

A charge pump driving a pure capacitor creates a perfect integrator, and the VCO provides a second perfect integrator. Phase is the position of the clock, and frequency is its speed. A system with two perfect integrators oscillates endlessly because the VCO frequency reaches its absolute maximum precisely when the phase error reaches zero, which guarantees continuous overshoot. The series resistor provides a proportional voltage spike while current flows to correct the phase. When the phase error reaches zero and the charge pump current stops, this proportional voltage instantly vanishes. The sudden drop in voltage abruptly decelerates the VCO to prevent the overshoot, providing the necessary damping. In the time domain the response of the clock phase to a unit phase step has the transform $T(s)/s$. For $\zeta = 1$ the result of the inverse transform is

$$\theta_{out}(t) = 1 - (1 - \omega_n t)\,e^{-\omega_n t}$$

which reaches its maximum at $\omega_n t = 2$ with the value $1 + e^{-2} = 1.135$. A critically damped Type-II loop still overshoots by 13.5 percent, because the proportional path (the zero) pushes the phase beyond the target before the integral path settles. The ratio $R/C$ chooses the damping.

### The Jitter Transfer Function and Its Peaking

The JTF is the magnitude of $T(j\omega)$ expressed in decibels, with the definition for amplitude ratios of [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md):

$$\text{JTF}(f) = 20\log_{10}|T(j2\pi f)|$$

It is a ratio of timing quantities (output jitter amplitude over input jitter amplitude at one jitter frequency) and not a voltage measurement. At 0 dB the clock moves exactly as much as the data, and a jitter frequency far above the loop bandwidth gives a large negative value.

Set $x = \omega/\omega_n$ in $T(j\omega)$, and the squared magnitude of the result is

$$|T|^2 = \frac{1 + 4\zeta^2 x^2}{(1 - x^2)^2 + 4\zeta^2 x^2}$$

Write $y = x^2$ and $a = 4\zeta^2$, so that $|T|^2 = (1 + a y)/(1 + (a - 2)y + y^2)$. The maximum satisfies $N'D - ND' = 0$, with $N$ the numerator and $D$ the denominator:

$$a\,[1 + (a-2)y + y^2] - (1 + ay)\,[(a-2) + 2y] = 2 - 2y - a y^2 = 0$$

The positive root is $y_{pk} = (\sqrt{1 + 2a} - 1)/a$, so the peak occurs at

$$\frac{\omega_{pk}}{\omega_n} = \sqrt{\frac{\sqrt{1 + 8\zeta^2} - 1}{4\zeta^2}}$$

For $\zeta = 1$ the peak is at $0.707\,\omega_n$ with $|T|^2 = 4/3$, which is **1.25 dB** of peaking. Setting $|T|^2 = 1/2$ gives $y^2 - (a+2)y - 1 = 0$ and the $-3$ dB bandwidth

$$\omega_{-3\text{dB}} = \omega_n\sqrt{1 + 2\zeta^2 + \sqrt{(1 + 2\zeta^2)^2 + 1}}$$

| $\zeta$ | Peaking (dB) | Peak at ($\omega_n$) | $\omega_{-3\text{dB}}/\omega_n$ |
|---|---|---|---|
| 0.5 | 3.33 | 0.856 | 1.82 |
| 0.707 | 2.09 | 0.786 | 2.06 |
| 1 | 1.25 | 0.707 | 2.48 |
| 2 | 0.40 | 0.545 | 4.25 |
| 4 | 0.12 | 0.402 | 8.12 |

The peaking comes from the zero of the loop. A second-order low-pass without a zero peaks only when $\zeta < 0.707$. The numerator $1 + 2\zeta s/\omega_n$ of a Type-II loop adds gain that rises at 20 dB per decade above $\omega_z$, so every Type-II loop peaks, and a larger $\zeta$ moves the zero to a lower frequency relative to $\omega_n$ and reduces the peaking. The mechanism of the peaking in terms of delay is the one that the capacitor introduces. The integral path corrects with a lag of up to 90 degrees. Near the loop bandwidth the correction arrives after the jitter has already reversed direction, so it adds to the motion of the clock, and the clock moves by more than the data.

The jitter frequency and the clock frequency are separate quantities. The clock frequency (16 GHz) is how fast the bits arrive. The jitter frequency (here 1.4 MHz at the peak) is how fast the phase error oscillates. The two differ by four orders of magnitude, and the peaking has no relation to the bit rate.

Peaking matters where the clock output is used again. A retimer recovers the clock and sends fresh data with that clock, so its output jitter is $T$ times the input jitter. A chain of $N$ retimers multiplies a jitter component at the peak frequency by the peaking ratio raised to the power $N$, and the standards limit the peaking for this reason. The Worked Examples give the numbers for a chain of retimers.

### The Jitter the Sampler Sees: The Error Transfer Function

The timing error that matters for a bit decision is the difference between the data edge and the recovered clock, and its transfer function is $E = 1 - T$. The complement of a low-pass function is a high-pass function, but the two magnitudes are not complementary in decibels, because the subtraction is complex. Near the loop bandwidth $T$ has a phase lag, so $|E|$ depends on the phase of $T$ as well as on its magnitude and cannot be derived from $|T|$ alone. The magnitude of $E$ for the Type-II loop is

$$|E(x)| = \frac{x^2}{\sqrt{(1 - x^2)^2 + 4\zeta^2 x^2}}$$

At low frequency $|E| \approx x^2$, which rises at 40 dB per decade, and at high frequency $|E| \to 1$, so the sampler sees the full jitter. For $\zeta \geq 0.707$ the function increases monotonically and never exceeds one. For $\zeta < 0.707$ it exceeds one over a band of frequencies, and the sampler then sees more jitter than the data contains. The Type-I loop of the previous section has a 20 dB per decade rise.

This resolves the contradiction of the introduction. The JTF describes the clock: $T$ is the fraction of the data timing that the clock reproduces, and it is low-pass. The jitter that remains in the timing of the data relative to the clock is $E\,\Theta_{in}$, and it is high-pass. A timing measurement made against a recovered clock, as in [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md), reports $E\,\Theta_{in}$. A receiver with the same loop sees the same quantity, so a slow component of the jitter that the loop follows does not reduce the margin of the receiver. The period jitter of that chapter is a different high-pass operation, with the factor $2\sin(\pi f\,UI)$ from differencing two successive edges, and it acts on the data timing and not through the loop.

The first-order model in the recovered-clock section of [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) is the Type-I special case and gives the same shape. For the loop of the Worked Examples with $f_c = 4$ MHz it gives $|E| = 0.243$ at 1 MHz, which turns 3 ps of jitter into 0.73 ps. The Type-II loop with $f_n = 2$ MHz and $\zeta = 1$ has $|E| = 0.2$ at 1 MHz and turns the same 3 ps into 0.60 ps. Both are high-pass, and the Type-II response rises faster at low frequency.

The loop has a second input, because the VCO adds its own phase noise $\Theta_v$ at its output, and the output of the loop is then

$$\Theta_{out} = T\,\Theta_{in} + E\,\Theta_v$$

The loop passes the input jitter below its bandwidth and suppresses the VCO noise below the same bandwidth. A wide loop follows the input closely and removes the noise of the VCO but passes the jitter of the data, and a narrow loop filters the input jitter and leaves the VCO noise at high offsets from the carrier. The loop bandwidth is a compromise between the two noise sources, and a standard specifies it for that reason. A spur on the control line of the VCO at some frequency appears as sinusoidal jitter of the recovered clock at that frequency, and above the loop bandwidth, where $E \approx 1$, the sampler sees it fully. This is the periodic jitter of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md).

## Architecture

### Charge Pump, Loop Filter, and VCO

The topologies of the Type-I and Type-II loops differ in their physical signal flow. A Type-I loop passes a voltage signal in series through a resistor to the VCO. A Type-II loop drives current into a T-junction. The main wire leads to the VCO, which acts as a high-impedance pressure gauge at the dead end of the wire. The charge pump forces the current to shunt down to ground through the loop filter components to build voltage pressure on the main wire.

The charge pump is a current source that physically forces electrons into the capacitor. A standard laboratory voltage source sets a potential and allows the circuit to determine the current, while a current source dictates the electron flow regardless of the resulting potential. The capacitor acts as a bucket, generating its own voltage from the accumulated charge ($V = Q/C$) without requiring any resistor. The series resistor and capacitor of the filter provide the proportional and integral voltage of the Type-II loop. The averaged model of the earlier sections treats the charge pump pulses as a continuous current, which holds for jitter frequencies far below the rate of the pulses.

The VCO contains an LC tank whose resonant frequency is $f = 1/(2\pi\sqrt{LC})$. A varactor, a diode whose depletion width and capacitance change with the reverse voltage, is part of the capacitance. The derivative $df/dC = -f/(2C)$ of the resonant frequency gives the gain

$$K_{vco} = \frac{df}{dv_c} = -\frac{f}{2C}\,\frac{dC}{dv_c}$$

A varactor that changes the tank capacitance by 10 percent per volt at 16 GHz gives $0.5 \times 0.10 \times 16\ \text{GHz} = 800$ MHz per volt. The tuning curve is not a straight line. The slope $K_{vco}$ is that of the operating point and varies with the control voltage, temperature, and process, and the linear model holds near the operating point only.

Many receivers adjust the phase of a fixed oscillator with a **phase interpolator** instead of the frequency of a VCO. The interpolator blends two clock phases that differ by a quarter period with weights $w_1$ and $w_2$. The sum $w_1\cos\omega t + w_2\sin\omega t$ is a sine of the amplitude $\sqrt{w_1^2 + w_2^2}$ and the phase $\tan^{-1}(w_2/w_1)$, which is the phase-shift identity that [Mach-Zehnder and IQ Modulators](20_Mach_Zehnder_IQ_Modulators.md) uses for modulators. A digital code selects the weights of the two phases. With 256 steps over one clock period the phase step is $62.5/256 = 0.244$ ps for a 62.5 ps period. The loop filter is then digital, with a proportional path that adds a fixed phase step for each early or late decision and an integral path that accumulates the decisions and holds the frequency offset. These are the $R$ path and the $1/(sC)$ path of the analog loop, and the model of the previous sections applies with the gains of the digital steps.

### Digital CDR with Converter Samples

A converter-based receiver ([SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md)) has no analog phase detector on edges. A digital phase detector, commonly the Mueller-Muller detector above, works on the samples at one sample per unit interval. The loop adjusts the phase of the sampling clock of the converter, with a phase interpolator or a digitally controlled oscillator, and the loop filter is the digital proportional-integral filter. A receiver may also run the converter from a fixed clock at a rate above the symbol rate and compute the samples at the optimum instant by digital interpolation, which costs a higher conversion rate. In both cases the timing loop is a PLL with the same transfer functions $T$ and $E$.

### Cycle Slips

The phase detector characteristic repeats with the period of one unit interval, and the loop locks onto one of the equivalent points. Assume that a large jitter excursion or a frequency step drives the phase error beyond half a unit interval. The loop then moves to the neighboring lock point, and this event is a **cycle slip**. The recovered clock gains or loses one cycle relative to the data, so the receiver records one bit twice or misses one bit.

A cycle slip is not an isolated bit error that forward error correction removes. The deserializer lost one bit, so every subsequent bit sits one position away from the word boundary that the alignment logic found, and the whole stream is misaligned until the alignment markers are detected again. Reed-Solomon decoding corrects symbols at known positions, and a shift of the bit stream changes many symbols at once, which exceeds the correction capacity. A slip is a synchronization error, and [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) describes the recovery through the markers. The design must keep the slips rare, and the Edge Cases give the limit of a digital loop.

### The Golden PLL and the Clock Recovery of Instruments

A measurement of jitter needs a reference clock, and the choice of the clock determines the result. The measured timing is $E\,\Theta_{in}$ for the loop that recovers the clock, so a wider loop reports less jitter than a narrower one. A compliance test must report what a compliant receiver sees. Protocol standards therefore define a reference clock recovery with a specified bandwidth and peaking, the **golden PLL**, and they require the measurement to use a clock recovered with that response. The error detector of a BERT and the software clock recovery of a real-time oscilloscope contain a CDR with configurable bandwidth and peaking for this purpose. Set them to the values of the standard, which differ between standards and between generations, and the eye shows the margin of a receiver that follows the golden PLL. The settings apply to the instrument and not to the chip under test.

The effect of a wrong setting follows from $E$. The Worked Examples show that an instrument loop twice as wide as the golden PLL reports the jitter of a 1 MHz component at less than one third of the correct value, which makes the link look better than it is.

The same function defines the **jitter tolerance** (JTOL) of a receiver. A BERT injects sinusoidal jitter of amplitude $A$ at a swept frequency, and the amplitude at which the receiver reaches the specified error ratio is recorded, and the sampler sees the amplitude $|E(f)|\,A$. Let $J_{max}$ be the residual jitter that the receiver can tolerate at its sampler, which depends on the eye and the other jitter. The jitter tolerance of the receiver is therefore given by

$$\text{JTOL}(f) = \frac{J_{max}}{|E(f)|}$$

At high jitter frequency $|E| \to 1$ and the tolerance equals $J_{max}$. Below the loop bandwidth the tolerance rises at 40 dB per decade, because the loop follows the jitter. The tolerance mask of a standard is a requirement on this curve.

## Worked Examples

The examples share one loop, whose data rate is 16 Gb/s with a unit interval of 62.5 ps and a clock of 16 GHz ($100\ \text{MHz} \times 160$). The transmitter and receiver crystals differ by 100 ppm, so the data frequency offset is $\Delta f = 1.6$ MHz. The VCO gain is 800 MHz per volt ($K_{vco} = 2\pi \times 800 \times 10^6$ rad/s per volt). The rms jitter on the data edges is 1.5 ps, the value used in [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md), which is $\sigma_\varphi = 2\pi \times 1.5/62.5 = 0.1508$ rad. The transition density is $\eta_T = 1/2$ and the charge pump current is $I_{cp} = 2\ \mu\text{A}$. All values are assumptions chosen to give round results, and no standard is implied.

### The Detector Gain and the Loop Design

The effective detector gain is $K_{pd} = 0.5 \times 2\ \mu\text{A} \times 0.7979/0.1508 = 5.29\ \mu\text{A}$ per radian. Choose the resistor so that the loop gain is $K_{pd}R = 5$ mV per radian, which gives $R = 945\ \Omega$. The Type-I loop of this resistor has $\omega_L = K_{pd}RK_{vco} = 0.005 \times 5.027 \times 10^9 = 2.513 \times 10^7$ rad/s, which is $f_L = 4$ MHz, the corner of the first-order model of [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md).

Add the capacitor to make the Type-II loop with the same $K = \omega_L$. The relation $2\zeta\omega_n = K$ holds for this loop, and the choice $\zeta = 1$ gives $\omega_n = 1.257 \times 10^7$ rad/s, $f_n = 2$ MHz, and a zero at $f_z = f_n/(2\zeta) = 1$ MHz. The capacitor follows from $\omega_z = 1/(RC)$:

$$C = \frac{1}{R\,\omega_z} = \frac{1}{945 \times 6.283 \times 10^6} = 168\ \text{pF}$$

The check $\omega_n^2 = K_{pd}K_{vco}/C$ gives $1.579 \times 10^{14}$, as it must. The component values are illustrative, and a digital loop filter has the same two paths.

### The Static Phase Error of the Type-I Loop

The frequency offset of 1.6 MHz needs a control voltage of $1.6\ \text{MHz}/800\ \text{MHz per V} = 2$ mV. The resistor produces this voltage only with the phase error

$$\theta_e = \frac{\Delta f}{f_L} = \frac{1.6}{4} = 0.40\ \text{rad} = 22.9^\circ = 0.0637\ \text{UI} = 3.98\ \text{ps}$$

The check $2\ \text{mV}/(5\ \text{mV/rad}) = 0.4$ rad gives the same result. The same number follows from the group delay: the lag is $1/\omega_L = 39.8$ ns, and $1.6\ \text{MHz} \times 39.8\ \text{ns} = 0.0637$ cycle. The clock samples 3.98 ps away from the point it would choose without the offset. Doubling the gain halves the error, and no finite gain removes it.

### The Type-II Loop Removes the Error

With the capacitor the static error of the frequency offset is zero. The capacitor stores the 2 mV after the transient. The transient of the error follows from $E(s)\,\Delta\omega/s^2 = \Delta\omega/(s^2 + 2\zeta\omega_n s + \omega_n^2)$. For $\zeta = 1$ the time function is $\theta_e(t) = \Delta\omega\,t\,e^{-\omega_n t}$, which has its maximum at $t = 1/\omega_n = 79.6$ ns:

$$\theta_{e,max} = \frac{\Delta\omega}{\omega_n e} = \frac{2\pi \times 1.6 \times 10^6}{1.257 \times 10^7 \times 2.718} = 0.294\ \text{rad} = 2.93\ \text{ps}$$

The Type-I error of 3.98 ps stays forever, and the Type-II error reaches a maximum of 2.93 ps and then decays to zero. A step in the phase of the data overshoots by 13.5 percent at $t = 2/\omega_n = 159$ ns, from the expression of the Core Concepts.

### The JTF, the Error Transfer Function, and the Tolerance

The loop has $f_n = 2$ MHz and $\zeta = 1$. The $-3$ dB bandwidth is $2.482 \times 2 = 4.96$ MHz, and the peaking of 1.25 dB (a ratio of 1.155) occurs at $0.707 \times 2 = 1.41$ MHz. The table gives the response and the tolerance for the assumption $J_{max} = 0.3$ UI.

| Frequency (MHz) | JTF (dB) | $\lvert T\rvert$ | $\lvert E\rvert$ | JTOL (UI) |
|---|---|---|---|---|
| 0.1 | 0.02 | 1.002 | 0.0025 | 120 |
| 0.5 | 0.44 | 1.052 | 0.059 | 5.1 |
| 1 | 1.07 | 1.131 | 0.200 | 1.5 |
| 1.41 | 1.25 | 1.155 | 0.333 | 0.90 |
| 2 | 0.97 | 1.118 | 0.500 | 0.60 |
| 4.96 | $-3.01$ | 0.707 | 0.860 | 0.35 |
| 10 | $-8.26$ | 0.387 | 0.962 | 0.31 |
| 40 | $-20.0$ | 0.100 | 0.998 | 0.30 |

Assume sinusoidal jitter of 10 ps peak to peak at the peaking frequency of 1.41 MHz. The recovered clock moves by $10 \times 1.155 = 11.5$ ps, more than the data. The sampler sees only $10 \times 0.333 = 3.33$ ps, because the clock moves almost in step with the data. At 1 MHz the clock moves by 11.3 ps and the sampler sees 2.0 ps. Peaking of the clock jitter therefore does not mean that the eye closes more. The peaking matters for jitter passed to the next stage, as the next example shows. The JTF and $E$ are not complementary in decibels: at 1 MHz the JTF is $+1.07$ dB, and $|E|$ is $-14.0$ dB.

### Peaking in a Chain of Retimers

A retimer recovers the clock and transmits new data with it, so its output carries $T$ times the input jitter. A jitter component at the peak frequency grows by the peaking ratio of 1.155 at each stage. The amplitude after $N = 1, 3, 5, 10$ retimers is multiplied by 1.155, 1.54, 2.05, and 4.21, which is 1.25, 3.75, 6.25, and 12.5 dB. A 2 ps component at 1.41 MHz becomes 8.4 ps after 10 stages. This accumulation is the reason that standards limit the peaking of the loop to a small value.

### A Wrong Loop Bandwidth in an Instrument

A component of sinusoidal jitter of 10 ps at 1 MHz is measured with three clock recoveries of the same $\zeta = 1$ shape. The golden loop ($f_n = 2$ MHz) leaves 2.0 ps in the timing. An instrument loop with twice the bandwidth ($f_n = 4$ MHz) gives $x = 0.25$ and $|E| = 0.0588$, so it reports 0.59 ps. This is 0.29 times the correct value, 10.6 dB too small, and the eye is too optimistic. An instrument loop with half the bandwidth ($f_n = 1$ MHz) gives $x = 1$ and $|E| = 0.5$, so it reports 5.0 ps, 2.5 times the correct value.

## Edge Cases

### The VCO Gain Is Not Constant

The linear model assumes a fixed $K_{vco}$, and the real gain varies with the control voltage, temperature, and process. Both $\omega_n$ and $\zeta$ scale as $\sqrt{K_{vco}}$ for the Type-II loop. A gain 20 percent below the nominal value gives $\zeta = 0.894$, $f_n = 1.79$ MHz, a peaking of 1.48 dB, and a $-3$ dB bandwidth of 4.15 MHz. A gain 20 percent above gives $\zeta = 1.095$, $f_n = 2.19$ MHz, a peaking of 1.08 dB, and a bandwidth of 5.77 MHz. The specification of the golden PLL covers a range of such values, and a design must meet the peaking and the bandwidth over the range of the gain. The phase detector gain varies in the same way with the amount of jitter, as the derivation of $K_{pd}$ showed.

### Leakage of the Loop Filter Capacitor

The capacitor of the Type-II loop holds its charge only if no leakage path exists. Assume a leakage resistance $R_L = 1\ \text{M}\Omega$ across the capacitor. The filter impedance at low frequency becomes $R_L$ and the loop acts as a Type-I loop of the larger gain $K_{pd}R_LK_{vco}$, so the static error is reduced from 0.4 rad by the ratio $R/R_L = 945/10^6$. The result is $3.8 \times 10^{-4}$ rad, or 0.0038 ps. The same value follows from the leakage current $2\ \text{mV}/1\ \text{M}\Omega = 2$ nA divided by the detector gain of 5.29 $\mu$A per radian. The detector delivers a small continuing current that replaces the leakage, and the cost is a static phase error far below any other jitter term. A real capacitor with a lower leakage resistance, or a loop with a long period between transitions, needs the same calculation.

### The Bandwidth Compromise

A loop bandwidth of infinity makes $T = 1$ and $E = 0$. The clock would reproduce the displacement of every edge, including the displacements that amplitude noise causes at the crossing ([Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md)) and that do not move the center of the bit where the decision is made. The sampling instant would then move with that noise, and a noisy early or late decision would pass directly into the clock for the following bits. A finite bandwidth lets the clock average the detector noise over many edges. The loop therefore follows the slow motion that is common to the whole bit, and the standard fixes the bandwidth that balances this averaging against the VCO noise term of the output $\Theta_{out} = T\Theta_{in} + E\Theta_v$.

### Slew Limit and Cycle Slips of a Digital Loop

A loop with a binary decision has a maximum rate at which it can move the phase. Assume the phase interpolator moves by $\delta = 1/256$ UI for each early or late decision and a transition occurs at the density $\eta_T = 1/2$. The phase can change by at most $\eta_T\delta = 0.00195$ UI per unit interval, which is a tracked frequency offset of 1,953 ppm. The offset of the example (100 ppm, or 200 ppm for the worst-case pair of crystals) is well within this limit. The slew rate in time is $\eta_T\delta R = 3.125 \times 10^7$ UI per second at 16 Gb/s.

A sinusoidal jitter of amplitude $A$ at frequency $f$ needs the slew rate $2\pi f A$, so the largest amplitude that the loop can follow is $A_{max} = \eta_T\delta R/(2\pi f)$. At 1 MHz this is 4.97 UI, which exceeds the 1.5 UI of the linear tolerance in the table, so the linear value applies. At 0.1 MHz it is 49.7 UI, which is less than the linear value of 120 UI, so the tolerance is limited by the slew rate and falls at 20 dB per decade. The two limits cross near 240 kHz, where both are about 20 UI. Above that frequency the tolerance follows $J_{max}/|E|$, and below it the slew rate sets the limit. A jitter or a frequency step that exceeds the slew limit produces a phase error that grows beyond 0.5 UI, and the loop slips a cycle.

### Timing Recovery from PAM4 Crossings

[PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md) derived where a linear ramp of duration $T_r$ crosses the middle threshold for each transition type, and the loop of this chapter inherits those numbers. Two, four, and two of the eight middle-threshold transitions cross at 0.25, 0.5, and 0.75 of the ramp, so the mean crossing lies at the middle of the ramp. Assume $T_r = 0.4$ UI at 32 Gbaud, which is 12.5 ps. The crossing time then has the rms deviation $0.1768\,T_r = 2.21$ ps around its mean, and the full range is the 6.25 ps of that chapter. A phase detector that uses every middle-threshold crossing receives this range as data-dependent jitter. The averaging of the loop places the clock at the mean crossing, and the part of the spread above the loop bandwidth reaches the sampler through $E \approx 1$ as deterministic jitter.

The slope result of the same chapter adds a second effect. The inner transitions have a third of the slope of the full-swing transitions, so equal amplitude noise moves their crossings by three times as much time (9.54 dB). A detector can avoid both effects by using only the full-swing transitions ($-3 \leftrightarrow +3$), whose crossings sit at the middle of the ramp with the full slope. These are 2 of the 16 equally probable symbol pairs, which gives a transition density of $1/8$ in place of $1/2$. The detector gain $K_{pd}$ is proportional to the density and falls by a factor of 4, and the charge pump current or the loop filter must compensate to keep the bandwidth. Both options reduce to the linear model of this chapter with the corresponding $K_{pd}$.

### The Detector Always Dithers

A binary detector cannot output zero while a transition is present. In lock the early and late decisions alternate, and the phase hunts around the lock point with an amplitude of a few phase steps. This dither is a small jitter added to the recovered clock, set by the phase step of the interpolator ($0.244$ ps in the example) and by the proportional gain, and it is one reason that the proportional step is made small.
