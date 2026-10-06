# Mach-Zehnder and IQ Modulators

<!-- SUMMARY: A phase modulator moves the phase of a light wave and an interferometer turns a phase difference into an amplitude, and a nested arrangement of two interferometers reaches every point of the plane of amplitude and phase. This guide derives the field transfer of a Mach-Zehnder modulator, E_out = E_in cos(delta phi / 2), its bipolar behavior at the null bias point and its finite extinction ratio, and then the identity I cos wt + Q sin wt = A cos(wt - phi), with A = sqrt(I^2 + Q^2) and phi = atan(Q/I), that lets the in-phase and quadrature interferometers synthesize any amplitude and phase. The chapter counts the four degrees of freedom of a dual-polarization transmitter and the bits per symbol of QPSK and 16QAM, works out the arcsine drive that the sinusoidal transfer requires, and derives coherent detection with a 90-degree optical hybrid, a local oscillator and balanced photodiode pairs, where the multiplication of the received wave by a reference occurs in the optics and the photodiodes and not in the digital processor. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Light as an Electromagnetic Wave and the Electro-Optic Effect](19_Light_and_the_Electro_Optic_Effect.md) ended with a phase modulator, a crystal section that adds the phase $\Delta\phi = \pi V/V_\pi$ to the wave that passes through it. A phase modulator alone moves the phase and leaves the amplitude unchanged, and a transmitter that must place a symbol anywhere on the plane of amplitude and phase needs more. This chapter derives how an interferometer converts a phase difference into an amplitude, how two interferometers in quadrature produce any point of the plane, and how the receiver recovers the two components again. The chapter uses the trigonometry that [Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md) used for the Fourier series, and the receiver derivation uses the power relations of [S-Parameters and VNA](08_S_Parameters_and_VNA.md).

## Core Concepts

### The Mach-Zehnder Modulator

A **Mach-Zehnder modulator** (MZM) splits the input wave into two arms, applies a phase modulator to each arm, and recombines the two waves. Assume that the splitter and the combiner divide the power equally, so that each arm receives the field $E_{in}/\sqrt2$ and the combiner passes $1/\sqrt2$ of each arm field to the output. The arms add the phases $\phi_1$ and $\phi_2$, and the output field is

$$E_{out} = \frac{E_{in}}{2}\left(e^{j\phi_1} + e^{j\phi_2}\right)$$

Write the two phases as their mean $\bar\phi = (\phi_1 + \phi_2)/2$ and their difference $\Delta\phi = \phi_1 - \phi_2$, so that $\phi_{1,2} = \bar\phi \pm \Delta\phi/2$. Factor out the mean phase:

$$E_{out} = \frac{E_{in}}{2}\,e^{j\bar\phi}\left(e^{j\Delta\phi/2} + e^{-j\Delta\phi/2}\right) = E_{in}\,e^{j\bar\phi}\cos\frac{\Delta\phi}{2}$$

The cosine comes from Euler's formula for the sum of the two exponentials. In **push-pull** operation the two arms receive voltages of opposite sign, $\phi_1 = \pi v/(2V_\pi)$ and $\phi_2 = -\pi v/(2V_\pi)$, which gives $\bar\phi = 0$ and $\Delta\phi = \pi v/V_\pi$, and the output phase stays fixed while the amplitude varies:

$$E_{out} = E_{in}\cos\!\left(\frac{\pi v}{2V_\pi}\right), \qquad P_{out} = P_{in}\cos^2\!\left(\frac{\pi v}{2V_\pi}\right) = \frac{P_{in}}{2}\left(1 + \cos\frac{\pi v}{V_\pi}\right)$$

Here $V_\pi$ is the voltage difference between the point of full transmission ($v = 0$, $\Delta\phi = 0$) and the point of zero transmission ($v = V_\pi$, $\Delta\phi = \pi$, the arms in antiphase). A driver that applies the same voltage to one arm only ($\bar\phi \ne 0$) also changes the output phase, which is a **chirp**, and push-pull drive avoids it.

The power transfer is an even function of the voltage, and a direct-detection receiver that measures only power cannot see the sign of the field, whereas the field carries more information than the power. A bias at the null point, $\Delta\phi = \pi + \pi v/V_\pi$, gives

$$E_{out} = E_{in}\cos\!\left(\frac{\pi}{2} + \frac{\pi v}{2V_\pi}\right) = -E_{in}\sin\!\left(\frac{\pi v}{2V_\pi}\right)$$

so that the field is proportional to the drive near the origin, changes its sign when the drive changes its sign, and reaches $\pm E_{in}$ at $v = \pm V_\pi$. A positive and a negative drive produce fields that differ in phase by $\pi$. The MZM at the null bias is therefore a modulator of a **real-valued** field, which carries one dimension of the plane (a binary phase code, with levels $\pm 1$, or a multilevel code on the real axis). A single MZM cannot place a point off the real axis, which is why the older statement that a single modulator can only change the amplitude is incomplete: a phase modulator changes the phase, an MZM changes the real amplitude, and neither covers the plane.

The null is not perfect in a real device. Assume that the splitter divides the field unequally, so that the arm fields are $\tfrac12(1 + \varepsilon)E_{in}$ and $\tfrac12(1 - \varepsilon)E_{in}$. At $\Delta\phi = \pi$ the arms are in antiphase and the output amplitude is the difference, $\varepsilon E_{in}$, so the **extinction ratio** is $-20\log_{10}\varepsilon$ dB: a 1 percent imbalance gives 40 dB, 3 percent gives 30.5 dB, and 10 percent gives 20 dB. The residual field appears in the constellation as an offset from the intended point.

### The In-Phase and Quadrature Identity

The plane of amplitude and phase needs two real numbers per symbol, and two orthogonal waves of the same frequency supply them. The sum of a cosine and a sine of the same frequency is a single cosine with a shifted phase. Let the weights be $I$ and $Q$ and expand a cosine with amplitude $A$ and phase $\varphi$:

$$A\cos(\omega t - \varphi) = A\cos\varphi\,\cos\omega t + A\sin\varphi\,\sin\omega t$$

The right side has the form $I\cos\omega t + Q\sin\omega t$ with $I = A\cos\varphi$ and $Q = A\sin\varphi$. The two relations invert to the amplitude and the phase,

$$I\cos\omega t + Q\sin\omega t = A\cos(\omega t - \varphi), \qquad A = \sqrt{I^2 + Q^2}, \quad \varphi = \operatorname{atan2}(Q, I)$$

where atan2 chooses the quadrant of the angle (the plain arctangent $\operatorname{atan}(Q/I)$ cannot distinguish $(I, Q)$ from $(-I, -Q)$). This is the statement that [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) uses for a phase interpolator: a sum of a weighted cosine and a weighted sine of one frequency is one sinusoid of that frequency, with amplitude $\sqrt{w_1^2 + w_2^2}$ and phase $\operatorname{atan}(w_2/w_1)$. Two numbers $(I, Q)$ and the two numbers $(A, \varphi)$ are two descriptions of one point, and the point is written as the complex number $s = I + jQ = A e^{j\varphi}$, the complex envelope of the carrier, with $E(t) = \operatorname{Re}\{s\,e^{-j\omega t}\}$. The sign of the exponent is a convention of optics that differs from the $e^{j\omega t}$ of [Impedance, Reflections, and Termination](03_Impedance_Reflections_and_Termination.md), and the constellation point $(I, Q)$ is the same in both.

The weights can be recovered from the sum. Average the product of the sum with $\cos\omega t$ over one period, using $\langle\cos^2\rangle = \tfrac12$ and $\langle\sin\cos\rangle = 0$:

$$\left\langle (I\cos\omega t + Q\sin\omega t)\cos\omega t\right\rangle = \frac{I}{2}, \qquad \left\langle (I\cos\omega t + Q\sin\omega t)\sin\omega t\right\rangle = \frac{Q}{2}$$

The cosine and the sine are **mathematically orthogonal**: their product averages to zero, so each average isolates one weight and ignores the other. This is a different property from the **physical orthogonality** of two polarizations in [Light as an Electromagnetic Wave and the Electro-Optic Effect](19_Light_and_the_Electro_Optic_Effect.md). Two polarizations are separate field components that never add into one vector direction, and the receiver separates them with a polarization beam splitter. The in-phase and quadrature waves have the *same* polarization and add into one wave, and only the multiplication and averaging above separate them.

### Degrees of Freedom and Bits per Symbol

A transmitter that controls $I$ and $Q$ on each of the two polarizations has four independent real numbers per symbol, which are the four degrees of freedom (XI, XQ, YI, and YQ). Assume that each real number takes $m$ equally spaced levels, so that each polarization carries $m^2$ distinct points and $\log_2 m^2$ bits, so a **constellation** of $M$ points carries $\log_2 M$ bits per symbol:

| Format | Levels per axis | Points $M$ | Bits per polarization | Bits per symbol, both polarizations |
|---|---|---|---|---|
| QPSK | 2 | 4 | 2 | 4 |
| 16QAM | 4 | 16 | 4 | 8 |

The older description of eight bits per optical clock cycle confuses the units. The symbols follow each other at the **symbol rate** (tens of gigabaud), and one optical cycle lasts 5.17 fs, so a symbol spans thousands of optical cycles. The eight bits per symbol of dual-polarization 16QAM follow from the table. With the levels $\pm1$ and $\pm3$ on each axis (the unit of the table is arbitrary) a 16QAM constellation has the mean power $\langle I^2 + Q^2\rangle = 10$ and the peak power 18 at the corners, a peak-to-average ratio of 2.55 dB, whereas every QPSK point has the same power.

## Architecture

### The Nested IQ Modulator

An IQ modulator nests two MZMs inside a third interferometer. The outer splitter divides the field into two arms of $E_{in}/\sqrt2$, and each arm contains a child MZM, one for $I$ and one for $Q$. The child field transfers are the real numbers $m_I, m_Q \in [-1, 1]$ of the null-biased expression above, each multiplied by the child's own field factor, so each child passes $E_{in}\,m/\sqrt2$. A phase section in the $Q$ arm adds a fixed $90^\circ$ at the carrier (a quarter of an optical *cycle*, 1.29 fs of delay at 1550 nm, set by a bias voltage on a phase modulator and not by a physical path of a quarter wavelength). The outer combiner passes $1/\sqrt2$ of each arm, so

$$E_{out} = \frac{E_{in}}{2}\left(m_I + j\,m_Q\right)$$

with $m_I$ and $m_Q$ set by the two data drives. The combination of the two orthogonal waves produces one wave with amplitude $A = \tfrac12\sqrt{m_I^2 + m_Q^2}\,|E_{in}|$ and phase $\operatorname{atan2}(m_Q, m_I)$, as the identity above states, so the complex number $m_I + j m_Q$ sets the constellation point. The factor $1/2$ in this field costs optical power. At a corner of the constellation ($m_I = m_Q = 1$) the output power is $\tfrac14(1 + 1) = \tfrac12$ of the input (3.01 dB loss), and on an axis ($m_I = 1$, $m_Q = 0$) it is $\tfrac14$ (6.02 dB loss), because the output combiner passes the factor $1/\sqrt2$ of each arm field and the remaining power leaves through the unused port or radiates into the substrate.

### Dual-Polarization Transmitter

The dual-polarization transmitter of Chapter 19 places one such IQ modulator in each polarization branch. The laser feeds a power splitter, the two IQ modulators carry independent data, a polarization rotator turns the second branch by $90^\circ$, and the polarization beam combiner merges the branches. The array contains four child MZMs, each with two phase-modulating arms, which makes eight arms in all. The four child MZMs receive four independent electrical streams: XI, XQ, YI, and YQ. The optical power budget follows from the factors above. For a 16QAM constellation driven to $m \in \{\pm\tfrac13, \pm1\}$ the mean of $m^2$ is $\tfrac12(\tfrac19 + 1) = 0.556$, so each IQ modulator has the mean output power $\tfrac14(2)(0.556) = 0.278$ of its input, and the whole transmitter delivers $0.278$ of the laser power (a loss of 5.56 dB) before the excess loss of the waveguides.

### Drive Levels and the Arcsine Predistortion

The field transfer $m = \sin(\pi v/2V_\pi)$ is not linear. A drive that spaces the voltages uniformly does not space the fields uniformly. To place the four amplitude levels at the field values $-1, -\tfrac13, +\tfrac13, +1$ (equal spacing), the drive must be the inverse function

$$\frac{v}{V_\pi} = \frac{2}{\pi}\arcsin m$$

which gives $v/V_\pi = \pm0.2163$ for $m = \pm\tfrac13$ and $\pm1$ for $m = \pm1$. The inner levels need a smaller voltage than the linear value of $\pm\tfrac13$, because the sine is steeper near the origin than the straight line to the corners. The transmitter applies this correction in the digital-to-analog converter ahead of the driver, so the **predistortion** table is part of the signal path, and the electrical drive reaches the full swing of $\pm V_\pi$ only at the outer levels.

### Bias Control

The relations above assume that the child MZMs are biased at their nulls and that the $Q$ arm is $90^\circ$ from the $I$ arm. The bias points drift with temperature and with the charge motion mentioned in Chapter 19, so each IQ modulator needs three bias voltages: one for the null of the $I$ child, one for the null of the $Q$ child, and one for the quadrature phase section. A dual-polarization transmitter therefore has six bias loops. A control loop adds a small dither tone to a bias voltage, detects the corresponding tone in a tap of the output power, and moves the bias until the detected tone reaches the value that marks the null or the quadrature point. The detection multiplies the tap by the known tone and averages the product, which is the same use of averaging that [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) applies to a repeating pattern.

### Coherent Reception

The receiver reverses the process, and the detection principle needs a derivation because no photodiode follows the optical phase at 193 THz. A photodiode responds to the power of the sum of the fields that fall on it, with the responsivity $R$ (amperes per watt, typically 0.8 to 1.0). Assume a signal field $E_s$ and a **local oscillator** (LO) field $E_{LO}$ of a laser at nearly the same frequency, with the powers $P_s = |E_s|^2$ and $P_{LO} = |E_{LO}|^2$. The current of a photodiode that receives $E_s + E_{LO}$ is

$$i = R\,|E_s + E_{LO}|^2 = R\left(P_s + P_{LO} + 2\operatorname{Re}\{E_s E_{LO}^*\}\right)$$

The last term is the **beat** of the two waves. It contains the product of the signal and the LO, which is the multiplication that the older description assigned to the digital processor (at 193 THz no processor and no converter can perform it). The photodiode performs the multiplication, because its response is proportional to the square of the field, and it also averages away the terms at twice the optical frequency.

A **balanced pair** of photodiodes receives the fields $E_s + E_{LO}$ and $E_s - E_{LO}$ (with the factor $\tfrac12$ of the splitting) and the current is the difference. The squares of the magnitudes differ by $4\operatorname{Re}\{E_s E_{LO}^*\}$ and the terms $P_s$ and $P_{LO}$ cancel, so the pair outputs only the beat. A **90-degree optical hybrid** is a passive coupler that forms four combinations of the two inputs: $E_s \pm E_{LO}$ and $E_s \pm jE_{LO}$ (each with the factor $\tfrac12$). The first pair gives the in-phase current and the second pair gives the quadrature current:

$$i_I = R\sqrt{P_sP_{LO}}\,\cos\theta, \qquad i_Q = R\sqrt{P_sP_{LO}}\,\sin\theta$$

where $\theta$ is the phase of the signal relative to the LO. The hybrid supplies the 90-degree reference optically, and the digital processor never multiplies at optical frequency. The currents are the real and imaginary parts of the complex envelope of the symbol. Each polarization needs its own hybrid and four photodiodes, so the dual-polarization receiver splits the signal with a polarization beam splitter, splits the LO in power, and uses **eight photodiodes** in four balanced pairs. A transimpedance amplifier follows each pair and converts the current to a voltage, and an analog-to-digital converter samples the voltage. The analog path does not end at the photodiode. It continues through the transimpedance amplifier, the filters and the converter, and only then do the samples reach the digital processor.

The beat has two practical consequences for the design of the receiver. The amplitude of the current grows with $\sqrt{P_{LO}}$, so a strong LO amplifies a weak signal: for $P_s = -10$ dBm ($0.1$ mW), $P_{LO} = 10$ dBm ($10$ mW) and $R = 0.9$ A/W, the beat current is $0.9\sqrt{(10^{-4})(10^{-2})} = 0.9$ mA, whereas direct detection of the signal gives $0.09$ mA, a gain of $\sqrt{P_{LO}/P_s} = 10$, or 20 dB in amplitude. The second consequence is that the angle $\theta$ is not constant. The two lasers have a frequency offset $\Delta f$ and a phase drift, so $\theta$ rotates as $2\pi\Delta f\,t$ plus the symbol phase and the laser noise, and the processor must remove the rotation. It tracks the carrier phase with a loop of the type of [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md), and [Wideband Signal Analysis and EVM](21_Wideband_Signal_Analysis.md) treats the other impairments that the processor removes.

## Worked Examples

### Mach-Zehnder Transfer Numbers

Take $V_\pi = 3$ V and push-pull drive, which gives the transmission $\cos^2 0 = 1$ at $v = 0$. At $v = V_\pi/2 = 1.5$ V the phase difference is $\pi/2$, and the power transmission is $\cos^2(\pi/4) = 0.5$ (3.01 dB). At $v = V_\pi = 3$ V the transmission is zero. With the null bias, a drive of $\pm1.5$ V gives the field $\mp\sin(\pi/4) = \mp0.707$ (power $0.5$), and $\pm3$ V gives $\mp1$. A splitting error of $\varepsilon = 0.03$ leaves the field $0.03\,E_{in}$ at the null, a power of $9\times10^{-4}$ and an extinction ratio of 30.5 dB.

### Synthesizing a Constellation Point

The 16QAM point with $I = 3$ and $Q = 1$ has the amplitude $A = \sqrt{10} = 3.162$ and the phase $\varphi = \operatorname{atan2}(1, 3) = 18.43^\circ$. The wave $3\cos\omega t + 1\sin\omega t$ and the wave $3.162\cos(\omega t - 18.43^\circ)$ agree at every instant: at $\omega t = 0$ both equal 3.000, and at $\omega t = 90^\circ$ both equal 1.000. The receiver averages with the cosine and the sine and finds $I/2 = 1.5$ and $Q/2 = 0.5$, which restores the point after the factor 2 is applied.

### Arcsine Drive and the Penalty of a Linear Drive

The four fields of 16QAM per axis are $-1, -\tfrac13, +\tfrac13, +1$, with equal spacings of $\tfrac23$ and the three eye openings equal. A drive that applied the voltages $\pm\tfrac13 V_\pi$ and $\pm V_\pi$ without correction would produce the fields $\sin(\pi/6) = 0.5$ and $\sin(\pi/2) = 1$, that is, $-1, -0.5, +0.5, +1$, so the spacings become $0.5, 1.0, 0.5$. The two outer eyes shrink to $0.5/0.667 = 0.75$ of the intended opening, which is a loss of $20\log_{10}0.75 = 2.5$ dB of margin in the outer eyes, while the middle eye grows to 1.5 times its intended opening. With the arcsine drive all three equal $\tfrac23$. The comparison is the optical counterpart of the equal PAM4 eyes of [PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md), where the transmitter must also place the levels at equal spacing.

### Symbol Rate and Bandwidth of a 400 Gb/s Channel

A 400 Gb/s dual-polarization 16QAM channel carries 8 bits per symbol. Assume that the forward error correction and framing of [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) add 15 percent (an assumed value for a strong code, larger than the 5.84 percent of the code in that chapter). The line rate is $400 \times 1.15 = 460$ Gb/s and the symbol rate is $460/8 = 57.5$ GBd. A raised-cosine pulse with a Nyquist frequency of $R_s/2$ ([Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md)) needs an electrical bandwidth of about 28.75 GHz on each of the four drive paths, and the receiver converters sample at twice the symbol rate or more, so at least 115 GSa/s on each of four channels. A dual-polarization QPSK channel at 100 Gb/s with the same overhead runs at $115/4 = 28.75$ GBd, which is half of the symbol rate of the 400 Gb/s channel and therefore needs half of its electrical bandwidth and sample rate.

### Optical Power Budget of the Transmitter

For the 16QAM drive of the architecture section the transmitter delivers 27.8 percent of the laser power, or $-5.56$ dB, before the excess loss of the waveguides, the facets (Chapter 19: 0.17 dB for each fiber facet) and the combiners. A laser of 16 dBm therefore yields about 10 dBm at the modulator output in the ideal case, and several decibels less in a real device. The same transmitter driven with QPSK (all four points at $m_I, m_Q = \pm1$) delivers half of the laser power, $-3.01$ dB overall, which is 2.55 dB more than the 16QAM drive. The difference equals the peak-to-average ratio of 16QAM, because the peak drive is the same and the mean power is lower. The lower mean power is the price of the higher number of bits per symbol, and the receiver must recover it with a higher signal-to-noise ratio.

## Edge Cases

### Quadrature Error and Carrier Leakage

A bias error in the $90^\circ$ section leaves the $I$ and $Q$ waves at $90^\circ + \delta$ instead of $90^\circ$. The two axes are no longer orthogonal, each average of the receiver picks up a fraction $\sin\delta$ of the other component, and the constellation becomes a parallelogram. A bias error at an MZM null leaves a residual field that adds a fixed offset to the point of that axis (the carrier leakage), with the size of the extinction ratio calculation above. Both errors are static in the model and are removed by the bias loops of the architecture section, and the part that remains appears as the constellation distortion that [Wideband Signal Analysis and EVM](21_Wideband_Signal_Analysis.md) measures.

### Overdrive and the Limit of the Sine

The transfer $m = \sin(\pi v/2V_\pi)$ reaches its maximum at $v = V_\pi$ and falls again beyond it. A drive that exceeds $V_\pi$ does not clip. The field decreases, and the outer levels fold back toward the inner levels, which can map a symbol to the wrong decision region. A transmitter limits the peak drive to the range $\pm V_\pi$, and it accepts the loss of efficiency that the compression near the corners costs.

### Phase Ambiguity of the Carrier Recovery

The constellations of QPSK and 16QAM are symmetric under rotation by $90^\circ$, so a carrier phase loop can lock to any of four phases without a change in its error signal. The receiver then decodes every symbol rotated by a multiple of $90^\circ$. Differential encoding of the phase transitions removes the ambiguity, because the data are carried by the change of the phase between symbols and not by its value relative to the carrier. Differential decoding doubles the symbol error probability of isolated errors (one wrong symbol corrupts two transitions), a multiplication of the same kind as the error tripling of the descrambler in Chapter 18. A cycle slip of the carrier loop, the event of Chapter 17, produces the same rotation by $90^\circ$ in the middle of a stream, and pilot symbols with known values let the processor detect it.

### Polarization Rotation in the Fiber

The fiber does not preserve the orientation of the polarization. The two components that leave the transmitter as XI/XQ and YI/YQ arrive as mixtures of each other, with a mixing that changes with temperature and with mechanical disturbance. The receiver therefore cannot assign one polarization beam splitter output to one transmitted polarization. The digital processor undoes the mixing with a $2 \times 2$ adaptive filter, as [Wideband Signal Analysis and EVM](21_Wideband_Signal_Analysis.md) shows, and the transmitter and the receiver need no alignment of their polarization axes.
