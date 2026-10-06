# Wideband Signal Analysis and EVM

<!-- SUMMARY: A coherent receiver's digital processor must remove fiber and laser impairments. This guide models chromatic dispersion ($\Delta\tau = D \cdot L \cdot \Delta\lambda$) and laser phase noise ($2\pi\Delta\nu\tau$), linking $\text{EVM} = \sqrt{\overline{|e|^2}}/\sqrt{\overline{|s_{\text{ref}}|^2}}$ to the optical signal-to-noise ratio. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Mach-Zehnder and IQ Modulators](20_Mach_Zehnder_IQ_Modulators.md) ended with eight photodiodes, four transimpedance amplifiers and four converters that deliver the in-phase and quadrature samples of two polarizations to a digital processor. The processor must undo what the fiber, the amplifiers and the two lasers did to the symbols, and an engineer who designs or qualifies a link needs a number that says how well it succeeded and a way to find the cause when it did not. This chapter supplies both, and the number is the error vector magnitude, which does for a constellation what the eye width of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md) does for a bit stream. The way to find the cause is the structure of the instrument that measures it, an optical modulation analyzer, which is a coherent receiver built to a measurement standard in the same way that [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md) describes an oscilloscope as a reference receiver.

## Core Concepts

### Chromatic Dispersion

The refractive index of silica depends slightly on the wavelength, so the waves of different frequencies in a modulated signal travel at different speeds. The propagation constant of the fiber, $\beta(\omega)$, is expanded around the carrier frequency $\omega_0$ in the offset $\Omega = \omega - \omega_0$:

$$\beta(\omega_0 + \Omega) = \beta_0 + \beta_1\Omega + \tfrac12\beta_2\Omega^2 + \dots$$

The first term is a constant phase, and the second term $\beta_1\Omega$ is a pure delay $\beta_1 L$ of the whole signal (the delay $L/v_g$ with the group velocity $v_g$). The term that distorts the signal is the third, $\tfrac12\beta_2\Omega^2$, whose coefficient $\beta_2$ is the **group velocity dispersion**. The group delay of a component at the offset $\Omega$ is the derivative of the accumulated phase, $\tau_g(\Omega) = d(\beta L)/d\Omega = \beta_1L + \beta_2 L\,\Omega$, so two components separated by the bandwidth $\Delta\omega$ arrive with the delay difference

$$\Delta\tau = \beta_2 L\,\Delta\omega$$

The fiber data sheets quote the **dispersion parameter** $D$ in ps/(nm km) instead of $\beta_2$. The conversion follows from $\Delta\omega = 2\pi c\,\Delta\lambda/\lambda^2$: the magnitude of $\Delta\tau$ is $\left(2\pi c\,|\beta_2|/\lambda^2\right) L\,\Delta\lambda$, and with $D = -2\pi c\,\beta_2/\lambda^2$ this becomes

$$\Delta\tau = |D|\,L\,\Delta\lambda$$

Standard single-mode fiber has $D \approx 17$ ps/(nm km) at 1550 nm (a typical value), which corresponds to $\beta_2 = -D\lambda^2/(2\pi c) = -21.7$ ps$^2$/km.

The distortion is a pure phase, because the factor $e^{-j\beta_2L\Omega^2/2}$ has magnitude 1 at every frequency, so the fiber is an **all-pass filter** with a quadratic phase, and it removes no power. A digital filter with the opposite phase, $H(\Omega) = e^{+j\beta_2L\Omega^2/2}$, cancels it exactly, and it amplifies no noise because its magnitude is also 1. This property separates chromatic dispersion from the copper channels of Part 1. The loss of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) attenuates the high frequencies, an equalizer must restore them, and [CTLE and DFE](14_CTLE_and_DFE.md) shows that restoring them amplifies the noise at those frequencies. The dispersion of a fiber loses nothing, and the compensation costs no signal-to-noise ratio, which is why a coherent receiver can compensate thousands of kilometers digitally.

### Polarization Mode Dispersion and Polarization Mixing

A real fiber is not exactly round or free of stress, so its two polarization modes have slightly different propagation constants. A signal that excites both modes spreads in time by the **differential group delay** (DGD) between them. The fiber is also bent, twisted, and heated along its length, so the DGD and the orientation of the modes change with position and with time, and the accumulated effect is random. The root-mean-square DGD grows as the square root of the length, $\Delta\tau_{rms} = D_{PMD}\sqrt{L}$, because the contributions of independent sections add in quadrature (the same rule as the independent jitter sources of Chapter 12). With the assumed coefficient $D_{PMD} = 0.1$ ps/$\sqrt{\text{km}}$ a 100 km link has $\Delta\tau_{rms} = 1$ ps, which is 5 percent of the 20 ps symbol of a 50 GBd signal.

The mixing of the two polarizations of Chapter 20, the rotation of the field orientation, is a slower and larger effect. The receiver models the channel as a $2\times2$ complex matrix that maps the transmitted X and Y components onto the received ones, and an adaptive $2\times2$ filter (four FIR filters in a butterfly arrangement) inverts it. The adaptation is the least-mean-squares update of [CTLE and DFE](14_CTLE_and_DFE.md), applied to complex taps, and it tracks the rotation as it changes. It needs a starting point, and a blind criterion that exploits a known property of the constellation (for example that a QPSK signal has a constant amplitude) provides it, because no known training sequence is required.

### Laser Phase Noise

A real laser does not emit a single frequency. Its frequency fluctuates, and the spectrum has a width $\Delta\nu$, the **linewidth**. Assume that the frequency noise is white, which is the origin of a Lorentzian line. The phase is the integral of the frequency, the same relation as the VCO of [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md), and the integral of white noise is a random walk: the phase changes over the time $\tau$ by a random amount whose variance grows linearly with $\tau$,

$$\sigma_\phi^2(\tau) = 2\pi\,\Delta\nu\,\tau$$

Both the transmitter laser and the LO contribute, so $\Delta\nu$ is the sum of the two linewidths. The numbers explain why the effect matters. For a sum of 200 kHz the variance during one 20 ps symbol is $2\pi(2\times10^{5})(2\times10^{-11}) = 2.5\times10^{-5}$ rad$^2$, an rms change of 5 mrad per symbol, which is invisible. The variance over 1 $\mu$s is $1.26$ rad$^2$ (an rms of 64 degrees), which exceeds the decision angle of every constellation by a large factor. The phase therefore wanders through the whole circle within a few microseconds, and the receiver must track it. The tracking loop cannot be too slow, or it falls behind the random walk, and it cannot be too fast, or it follows the additive noise of the individual symbols. The trade is the loop bandwidth trade of Chapter 17, applied to a carrier phase instead of a data clock.

Residual phase error enters the constellation as a tangential error. A symbol $s$ rotated by the small angle $\delta$ becomes $s\,e^{j\delta} \approx s(1 + j\delta)$, and the error vector $s\,j\delta$ has the magnitude $|s|\,\delta$, so the error divided by the symbol magnitude is exactly the angle. A residual phase error of rms $\sigma_\phi$ therefore contributes $\text{EVM} = \sigma_\phi$ in radians to the measure defined next, 1.75 percent for 1 degree rms.

### Error Vector Magnitude

The analyzer compares each received symbol $r_k$ with the ideal point $s_k$ that the transmitter intended. The **error vector** is $e_k = r_k - s_k$, a complex number whose real and imaginary parts are the errors along the I and Q axes. The rms error divided by the rms of the reference defines the **error vector magnitude**:

$$\text{EVM}_{rms} = \frac{\sqrt{\frac1N\sum_k |e_k|^2}}{\sqrt{\frac1N\sum_k |s_k|^2}}$$

The denominator is the mean power of the reference constellation. Other normalizations exist (the peak magnitude or the outermost symbol), and they give different numbers for the same signal, so a report must state which one it uses. Only the mean-power normalization makes QPSK and 16QAM comparable, and this chapter uses it.

EVM is the constellation counterpart of the eye measures of Part 3. With errors from additive noise alone, $\sum|e_k|^2/N$ is the noise power and $\sum|s_k|^2/N$ is the signal power, so

$$\text{SNR} = \frac{1}{\text{EVM}^2}, \qquad \text{EVM} = 10^{-\text{SNR}_{dB}/20}$$

The relation to the bit error ratio follows from the Q function of [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md). A symbol of a QPSK constellation sits at $(\pm a, \pm a)$ and has the mean power $2a^2$. The noise has the variance $\sigma^2 = 2a^2\,\text{EVM}^2$ per complex sample, half of it on each axis, so each axis sees a Gaussian with the standard deviation $\sigma/\sqrt2 = a\,\text{EVM}$. A bit is wrong when the noise exceeds the distance $a$ to the decision threshold of its axis:

$$\text{BER}_{QPSK} = Q\!\left(\frac{a}{a\,\text{EVM}}\right) = Q\!\left(\frac{1}{\text{EVM}}\right)$$

A 16QAM axis is a PAM4 signal ([PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md)). With the levels $\pm1$ and $\pm3$ the half-spacing between a level and its threshold is 1, the mean power is $10$, and the noise per axis is $\sigma_{axis} = \sqrt{10\,\text{EVM}^2/2} = \sqrt5\,\text{EVM}$. The Gray-coded PAM4 result of Chapter 15 ($\text{BER} = 0.75\,Q$) gives

$$\text{BER}_{16QAM} = 0.75\,Q\!\left(\frac{1}{\sqrt5\,\text{EVM}}\right)$$

Both expressions assume noise that is white and Gaussian and a receiver that makes no other error.

### Optical Signal-to-Noise Ratio

An optical amplifier adds amplified spontaneous emission (ASE), a broadband noise that the receiver cannot distinguish from the signal. The industry measures it with the **optical signal-to-noise ratio** (OSNR): the signal power divided by the noise power in a reference bandwidth of 0.1 nm, which is 12.5 GHz at 1550 nm, with the noise of both polarizations counted. The noise power in the bandwidth of the symbol stream, $R_s$, is $R_s/12.5$ GHz times the reference noise, so

$$\text{SNR} = \text{OSNR}\,\frac{12.5\ \text{GHz}}{R_s}$$

where SNR is the ratio per symbol that sets the EVM above. A link of identical amplified spans adds the ASE of each span, and the contributions are independent, so they add in power (the rule of [S-Parameters and VNA](08_S_Parameters_and_VNA.md) for uncorrelated signals). The noise grows in proportion to the number of spans $N$, and the OSNR falls as $10\log_{10}N$: 3.01 dB for each doubling of the number of spans at a fixed launch power.

## Architecture

### The Analyzer as a Coherent Receiver

An **optical modulation analyzer** (OMA) is a coherent receiver of the kind that [Mach-Zehnder and IQ Modulators](20_Mach_Zehnder_IQ_Modulators.md) derived: a polarization beam splitter, a tunable LO laser, two 90-degree hybrids, eight photodiodes in four balanced pairs, four transimpedance amplifiers and four converters, followed by software that processes the samples. It is designed for measurement: wide and flat bandwidth, a low-noise LO, converters with a good effective number of bits, and a calibration of the skew and gain between the four channels. It is not a perfect receiver, and its own limits appear in every result: the LO has a linewidth, the amplifiers have noise, the converters quantize, and the four paths have residual skew and imbalance. The instrument reports the signal *through* these limits, and a measurement must account for them (see the budget below).

An instrument defines its receiver in software, and that definition affects the result in the same way that the golden PLL of Chapter 17 and the reference equalizer of Chapter 16 affect a jitter or eye measurement. The carrier recovery bandwidth, the number of taps of the equalizer and the adaptation step determine how much of an impairment the instrument removes before it computes the EVM, and a measurement reported without these settings is incomplete.

### The Processing Chain

The software applies the following steps to the four sample streams, in this order, and each step has a parameter that is itself a measurement:

1. **Front-end correction:** the instrument removes the DC offsets, the gain imbalance between the I and Q channels, and the skew between the four channels, using the calibration data.
2. **Resampling and chromatic dispersion compensation:** the all-pass filter $e^{+j\beta_2L\Omega^2/2}$ cancels the dispersion. The instrument finds $\beta_2L$ (or $DL$) by scanning it and maximizing a quality metric, so the best value of the parameter *is* the dispersion measurement.
3. **Polarization demultiplexing:** the adaptive $2\times2$ filter of the core concepts inverts the polarization mixing and the PMD. The converged taps give the DGD and the rotation.
4. **Carrier recovery:** a frequency estimate removes the offset between the lasers and a phase tracking loop removes the phase noise (Chapter 17 and Chapter 20 describe the loop and its $90^\circ$ ambiguity). The loop's residual and its estimated frequency offset are measurements.
5. **Decision and EVM:** the software decides each symbol, compares it with the ideal point and computes the EVM, the constellation, and the bit error ratio.

The order follows the physics of the channel. The dispersion filter acts first because chromatic dispersion is large (hundreds of symbol periods) and identical for both polarizations, and the polarization filter, which spans only a few symbols, must see symbols that are not smeared over that many neighbors. The phase tracking acts last because it must see the symbols after the filters have removed the deterministic distortion, and the blind constant-modulus criterion of the polarization filter does not depend on the carrier phase, so the filter converges while the phase is still rotating.

### Frequency-Domain Measurements

The analyzer also measures the optical spectrum. The software computes the discrete Fourier transform of a captured record by the FFT, with the resolution and the leakage of [Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md): a record of $N$ samples at the rate $f_s$ has the bin spacing $f_s/N$ and needs a window function to keep the strong carrier region from masking the neighboring channels. A pulse-shaped signal with a roll-off factor $\beta$ occupies the bandwidth $R_s(1 + \beta)$, 55 GHz for 50 GBd and $\beta = 0.1$. The spectrum shows whether the signal leaks power into the neighboring wavelength channel, which is a separate specification from the EVM.

### Reading the Constellation

The shape of the scatter around the ideal points indicates the impairment, and the shapes follow from the derivations above:

| Signature | Cause |
|---|---|
| Round clouds of equal size at every point | Additive noise (ASE, receiver thermal noise) |
| Clouds stretched along the radius from the origin | Amplitude noise, or modulator compression near the corners (Chapter 20) |
| Clouds stretched along the circle (tangentially), growing with the distance from the origin | Phase noise (the error is $|s|\,\delta$) |
| Parallelogram instead of a square grid | Quadrature error or skew between I and Q |
| All points shifted in one direction | Carrier leakage or DC offset |
| Points on spirals or rotated rings | Unremoved frequency offset or carrier phase |

A single instrument setting can often separate two causes. The measurement repeated with a tighter carrier-recovery bandwidth turns tangential smear into a smaller cloud if the cause was the loop and leaves it unchanged if the cause was the transmitter.

## Worked Examples

### EVM of Four QPSK Symbols

The ideal points are $s = \pm1 \pm j$ with $|s|^2 = 2$ for every point. Four received values are $1.08 + 0.95j$, $-0.93 + 1.10j$, $-1.05 - 0.90j$ and $0.90 - 1.07j$. The error vectors have the magnitudes 0.0943, 0.1221, 0.1118 and 0.1221. The mean of $|e|^2$ is $0.0128$, and

$$\text{EVM} = \sqrt{\frac{0.0128}{2}} = 0.0800 = 8.0\ \text{percent}$$

The corresponding signal-to-noise ratio is $1/0.0064 = 156$, which is 21.9 dB.

### EVM Requirements for a Given Bit Error Ratio

The relations of the core concepts give the largest EVM that a format tolerates:

| Format | Raw BER | $Q$ argument | Maximum EVM | SNR (dB) |
|---|---|---|---|---|
| QPSK | $10^{-12}$ | 7.034 | 14.2 % | 16.9 |
| QPSK | $10^{-4}$ | 3.719 | 26.9 % | 11.4 |
| QPSK | $2.1\times10^{-4}$ | 3.527 | 28.4 % | 10.9 |
| 16QAM | $10^{-12}$ | 6.994 | 6.39 % | 23.9 |
| 16QAM | $10^{-4}$ | 3.646 | 12.3 % | 18.2 |
| 16QAM | $2.1\times10^{-4}$ | 3.450 | 13.0 % | 17.7 |

The $Q$ argument for 16QAM is the solution of $0.75\,Q = \text{BER}$, which is 6.994 at $10^{-12}$ and the same table as in Chapter 15 (the PAM4 axis). The raw ratio $2.1\times10^{-4}$ is the threshold that [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) found for the code RS(544,514), so a 16QAM channel protected by that code works with an EVM up to 13.0 percent, about twice the 6.39 percent that an uncoded link needs. The two EVM values differ by a factor of 2.03, which is 6.1 dB and matches the difference of the two SNR values in the table.

### From OSNR to EVM

A 50 GBd signal with an OSNR of 20 dB (a ratio of 100) has $\text{SNR} = 100 \times 12.5/50 = 25$, or 13.98 dB, and $\text{EVM} = 1/\sqrt{25} = 20$ percent. That is within the QPSK limit of 26.9 percent at $10^{-4}$ and far outside the 16QAM limit of 12.3 percent. The OSNR that 16QAM needs for $10^{-12}$ is the SNR of 23.88 dB plus the bandwidth ratio $10\log_{10}(50/12.5) = 6.02$ dB, which is 29.9 dB. Every doubling of the number of amplified spans costs 3.01 dB of OSNR, so a link with 29.9 dB after $N$ spans has 26.9 dB after $2N$ spans and can no longer carry uncoded 16QAM at $10^{-12}$.

### Chromatic Dispersion of a Link

A 50 GBd signal occupies about 50 GHz, which is $\Delta\lambda = \lambda^2\Delta f/c = (1.55\ \mu\text{m})^2(50\ \text{GHz})/c = 0.40$ nm. At 80 km the accumulated dispersion is $DL = 17 \times 80 = 1{,}360$ ps/nm, and the delay spread is $\Delta\tau = 1360 \times 0.40 = 545$ ps, which is 27 symbol periods of 20 ps. A converter that samples every 10 ps (twice per symbol) sees a response that spans 54 samples, so the compensating FIR filter needs about 54 taps. At 1,000 km the spread is 6.8 ns, which is 341 symbols, and the filter needs about 680 taps. A signal without compensation is unreadable, since each symbol overlaps dozens of its neighbors, and a filter of this size is routine for a digital receiver.

### Phase Noise and Its Contribution to EVM

For a laser pair with a summed linewidth of 200 kHz the phase variance over 1 $\mu$s is $2\pi(2\times10^{5})(10^{-6}) = 1.26$ rad$^2$ (64 degrees rms), so the loop must track it. Assume that the loop leaves a residual phase error of 1 degree rms. The residual contributes $\text{EVM} = 0.0175$ (1.75 percent), and the contribution is the same for every symbol of a QPSK constellation (all have the same magnitude) and larger in size for the outer points of 16QAM, while its ratio to the symbol magnitude stays equal to the angle.

### Instrument Floor and the EVM Budget

The converters quantize, and the relation of [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md), $\text{SNR} = 6.02N + 1.76$ dB, gives the contribution. An ideal 8 bit converter has 49.9 dB and an EVM of 0.32 percent. A real converter with an effective number of bits of 5 has $6.02 \times 5 + 1.76 = 31.9$ dB and an EVM of 2.55 percent, so the quantization of a real instrument is not negligible. Independent contributions add in power, hence in quadrature in EVM, the rule that Chapter 8 and Chapter 12 used for uncorrelated sources:

$$\text{EVM}_{total} = \sqrt{\text{EVM}_1^2 + \text{EVM}_2^2 + \dots}$$

An assumed instrument noise floor of 3 percent, the quantization of 2.55 percent and the phase contribution of 1.75 percent give $\sqrt{3^2 + 2.55^2 + 1.75^2} = 4.28$ percent. The inverse operation removes a known floor from a measurement. A reading of 8.0 percent on an instrument with a 3.0 percent floor corresponds to $\sqrt{8.0^2 - 3.0^2} = 7.42$ percent for the signal itself, a correction of 7 percent in the result, and the floor itself needs a measurement on a clean reference signal.

## Edge Cases

### Different Normalizations Give Different Numbers

An EVM normalized to the mean power of the constellation and an EVM normalized to its outermost point differ by the ratio of the two magnitudes. For 16QAM the mean power is 10 and the corner power is 18, so the corner-normalized value is smaller by $\sqrt{10/18} = 0.745$ (a factor that makes the same signal look 25 percent better). A comparison between two reports is meaningless without the definition, and the Q mapping of the core concepts holds only for the mean-power normalization.

### Decisions Made at High EVM

The analyzer must decide which ideal point each received symbol belongs to, and it decides by the nearest point. A large noise puts some symbols closer to a neighbor than to the transmitted point, and the error vector is measured against the neighbor. The measured EVM then falls below the true value. For 16QAM the per-axis symbol error probability is $1.5\,Q(1/\sigma_{axis})$ with $\sigma_{axis} = \sqrt5\,\text{EVM}$, which is 1.9 percent for a true EVM of 20 percent and 19.8 percent for 40 percent, so the bias is small near the operating range of a working link and large for a link that has failed. A known transmitted sequence removes the bias, and the instrument uses it when the pattern is available.

### The Equalizer Hides How Close It Is to Its Limit

The EVM is computed after the processing chain. A signal with a residual EVM of 4 percent can come from a channel that the filters handle comfortably or from one at the edge of their capability (the dispersion near the number of taps, the PMD near the memory of the butterfly filter, or the phase noise near the bandwidth of the tracking loop), and the EVM does not distinguish them. The parameters of the chain give the margin: the dispersion estimate against the taps, the DGD estimate against the filter length, and the residual phase error against the loop bandwidth.

### Carrier Slips Appear as Bursts

A cycle slip of the carrier loop (Chapter 17 and Chapter 20) rotates the constellation by $90^\circ$ and makes every symbol wrong until the loop or a pilot symbol corrects it. An EVM averaged over a long record hides the event, because a short burst of errors of the size of the symbol spacing adds little to the mean. A per-symbol plot of $|e_k|$ against time shows the bursts, in the same way that the time-ordered TIE of Chapter 12 shows jitter that a histogram hides.

### Closing the Series

The question of Chapter 1 was how a wave travels along a trace and how much of it reaches the end. The same question closes here for a wave of light in glass: the amplitude and phase that arrive carry the data, the channel distorts them in ways that can be modeled, and a measurement quantifies how much margin remains. The tools carry over from the copper trace to the fiber because the physics is the same, the field equations, the impedance and reflection, the spectrum of a modulated signal, the Gaussian noise tail, and the limits of equalization that each chapter derived from them.
