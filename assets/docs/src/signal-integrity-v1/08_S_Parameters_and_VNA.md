# S-Parameters and Vector Network Analysis

<!-- SUMMARY: S-parameters describe the complete frequency-dependent behavior of a multi-port network as ratios of incident and reflected voltage waves. This guide covers the mathematical framework of the scattering matrix, the physical architecture of the vector network analyzer (VNA) that measures it, and the interpretation of insertion loss, return loss, and crosstalk in high-speed channel characterization. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

Time domain reflectometry reveals what a transmission line looks like at a single moment: a fast voltage step propagates down the channel, and the instrument records each echo as a spatial impedance profile. This approach excels at localizing physical structures along the trace, but it cannot separate the frequency-dependent behavior of those structures. A via that appears as a simple capacitive dip on a TDR waveform actually presents a complex impedance that varies continuously with frequency. Characterizing this frequency-dependent behavior requires an instrument that operates natively in the frequency domain.

A Vector Network Analyzer (VNA) replaces the broadband voltage step with a precisely controlled, narrowband sine wave. The instrument sweeps this sine wave across a programmable frequency range, and at each frequency step, it measures the magnitude and phase of the waves that reflect back and the waves that transmit through the device under test. These measurements are organized into a matrix of complex ratios called scattering parameters (S-parameters), which completely describe the linear behavior of the network at every measured frequency.

S-parameters are the lingua franca of high-speed channel characterization. Compliance specifications for PCIe, USB, HDMI, and Ethernet all define pass/fail criteria in terms of S-parameter masks. Return loss limits, insertion loss budgets, crosstalk isolation requirements, and impedance matching tolerances are all expressed as S-parameter thresholds plotted against frequency. This guide covers the physical architecture of the VNA, the mathematical definition of scattering parameters, the decibel system used to represent them, multi-port measurement for differential and crosstalk characterization, and the IF bandwidth mechanism that controls dynamic range.

## Core Concepts

### What the VNA Measures: Incident and Scattered Waves

A VNA injects a known sine wave into one port of a device under test and simultaneously measures two quantities: the fraction of energy that reflects back out of the same port, and the fraction that transmits through to each other port. The instrument captures both the magnitude and the phase of each measured wave relative to its own internal reference oscillator.

Scattering parameters organize these measurements into a systematic matrix indexed by port number. The naming convention $S_{ij}$ means "the ratio of the wave leaving port $i$ to the wave entering port $j$." In a standard two-port measurement where Port 1 is the transmitter end and Port 2 is the receiver end:

- **$S_{11}$** is the signal injected into Port 1 that reflects back to Port 1. This quantity is called return loss. It measures the impedance match at the input.
- **$S_{21}$** is the signal injected into Port 1 that successfully transmits through to Port 2. This is insertion loss. It measures how much energy the channel delivers to the receiver.
- **$S_{12}$** is the signal injected into Port 2 that transmits backward to Port 1. This is the reverse transmission coefficient.
- **$S_{22}$** is the signal injected into Port 2 that reflects back to Port 2. This is the return loss at the output port.

Measuring from both directions is necessary to fully characterize the device. A simple passive copper trace is symmetric: $S_{21} = S_{12}$ and $S_{11} = S_{22}$. This symmetry is a direct consequence of the reciprocity theorem, which guarantees that the electromagnetic coupling between two ports of a passive linear network is identical regardless of direction. Active components like amplifiers or RF isolators break this symmetry, passing energy preferentially in one direction while attenuating the reverse path.

### S-Parameters as Complex Ratios

The VNA measures the incident wave ($a$) entering a port and the scattered wave ($b$) leaving a port. Each S-parameter is the ratio of a scattered wave to an incident wave:

$$S_{21} = \frac{b_2}{a_1}$$

The incident and scattered waves are both measured in the same voltage units, so S-parameters are fundamentally dimensionless. They carry no inherent unit of measurement. Each S-parameter is a complex number containing both magnitude and phase, represented as $r\angle\theta$. The magnitude quantifies how much energy reflects or transmits. The phase quantifies the time delay that the signal accumulates in transit, expressed as degrees of rotation of the specific sine wave period at each measurement frequency.

### The Decibel System

S-parameter magnitudes span an enormous dynamic range. Insertion loss through a well-designed trace might be $-0.5$ dB (89% of the power reaching the receiver), while the crosstalk leaking between two adjacent lanes might be $-60$ dB (one millionth of the injected power). Comparing these values on a linear scale is impractical. The decibel compresses this range into manageable numbers using a logarithmic transformation.

The decibel is fundamentally a ratio between two quantities, not an absolute unit of physical measurement. It expresses how much larger or smaller a measured value is compared to a reference value. The mathematical definition depends on whether the underlying quantity is power or voltage.

For **power ratios**, the decibel is defined as:

$$\text{dB} = 10 \log_{10}\left(\frac{P_{out}}{P_{in}}\right)$$

For **voltage ratios**, the exponent rule of logarithms converts the squared relationship ($P \propto V^2$) into a factor of 20:

$$\text{dB} = 20 \log_{10}\left(\frac{V_{out}}{V_{in}}\right)$$

S-parameters are voltage ratios, so the 20-multiplier form applies. An $S_{21}$ of 0 dB indicates perfect unity: 100% of the signal power injected at Port 1 reached Port 2. The ratio is exactly 1, and $\log_{10}(1) = 0$. An $S_{21}$ of $-3$ dB indicates a 50% reduction in power (the voltage ratio is $1/\sqrt{2} \approx 0.707$). An $S_{11}$ of $-20$ dB indicates that only 1% of the injected power reflects back, denoting an excellent impedance match.

Several important reference benchmarks follow directly from the logarithm:

| Magnitude (linear) | dB Value | Physical Meaning |
|---|---|---|
| 1.0 | 0 dB | Perfect unity (zero loss, zero gain) |
| 0.707 | $-3$ dB | Half-power point |
| 0.1 | $-20$ dB | 1% power reflection / 99% transmission |
| 0.01 | $-40$ dB | 0.01% power |
| 0.001 | $-60$ dB | One-millionth of power |

### Absolute Power: dBm

Standard dB expresses a relative ratio between two values that may both be unknown. The unit dBm anchors this ratio to a fixed physical reference: 0 dBm equals exactly 1 milliwatt. The underlying mathematics remain identical. The ratio of 1 milliwatt divided by the 1-milliwatt reference evaluates to 1, and $10 \log_{10}(1) = 0$.

A critical distinction separates these two units. A relative dB gain or loss can be applied to an absolute dBm power level (a 10 dBm signal passing through a $-3$ dB attenuator produces a 7 dBm signal at the output), but converting between dB and dBm without knowing at least one absolute reference is mathematically undefined. The two units measure fundamentally different concepts: dB measures a ratio, and dBm measures an absolute power.

## Architecture

### The VNA Swept-Sine Architecture

The physical architecture of a VNA differs fundamentally from a TDR. A TDR launches a broadband voltage step containing energy across the entire spectrum simultaneously, then sorts out the frequency content by mathematics (FFT) after the fact. A VNA operates in the opposite direction. Its internal source generates a single, pure, continuous sine wave at one specific frequency. The instrument injects this sine wave into the device under test, measures the reflected and transmitted responses at that one frequency, then increments the source to the next frequency and repeats. The VNA builds the complete frequency-domain picture one data point at a time across the programmed sweep range.

This swept-sine approach carries a fundamental advantage in measurement precision. At each frequency step, the VNA knows exactly what frequency it injected and can tune its receiver to listen exclusively at that frequency. All energy arriving at any other frequency is rejected as noise. This narrow-band detection is the mechanism that gives VNAs their extraordinary dynamic range, often exceeding 100 dB.

The two instruments measure the same physical quantity. A time-domain TDR step response can be mathematically converted into a frequency-domain S-parameter response by applying a Fast Fourier Transform (FFT) to the measured step waveform. The inverse operation is equally valid: an IFFT applied to S-parameter data reconstructs the equivalent time-domain impulse response. The TDR excels at spatial localization of impedance structures. The VNA excels at isolating frequency-dependent behavior and separating reactive components that the TDR cannot distinguish on a flat baseline.

### Phase Measurement and Display

Each S-parameter carries a phase component alongside its magnitude. The VNA determines the phase by comparing the arrival time of the measured wave against its own internal reference oscillator. The result is expressed as degrees of rotation of that specific sine wave period. At low frequencies, a given physical delay produces a small phase shift. At high frequencies, the same physical delay produces many more degrees of rotation.

Phase is typically plotted on a secondary vertical axis (on the right side of the graph) against the same frequency horizontal axis used for the magnitude trace. Alternatively, phase appears on a completely separate rectangular graph beneath the magnitude plot. Both magnitude and phase can be combined onto a single polar Smith Chart, where the radial distance from the center represents magnitude and the angular position represents phase. The Smith Chart representation is identical to the one described in the companion guide: the impedance corresponding to each measured frequency appears as a point on the chart, and sweeping across frequency traces a trajectory that reveals the evolution of the impedance match.

### Multi-Port and Differential Measurement

A standard two-port VNA characterizes single-ended channels. Differential signaling, which dominates modern high-speed protocols (PCIe, USB, HDMI, Ethernet), requires simultaneous measurement of two coupled signal paths. A 4-port VNA handles this naturally. A single differential pair requires four ports: two at the transmitter end (corresponding to the D+ and D$-$ signals) and two at the receiver end. This configuration produces a 4x4 S-parameter matrix with 16 entries.

The raw single-ended S-parameters from the 4-port measurement are mathematically transformed into mixed-mode S-parameters that decompose the channel behavior into differential mode (the desired signal) and common mode (the noise mode). Differential insertion loss ($S_{dd21}$) measures how efficiently the differential signal propagates through the channel. Mode conversion parameters ($S_{cd21}$, $S_{dc21}$) measure how much energy converts between differential and common modes during transit, a phenomenon caused by asymmetries in the physical trace routing (length mismatch, unequal coupling to ground planes, or asymmetric via structures).

High port-count VNAs (8, 16, or 32 ports) extend this framework to characterize complex multi-lane buses. Crosstalk between adjacent lanes is measured by injecting a signal into one lane and recording the coupled energy appearing at the ports of neighboring lanes. Near-End Crosstalk (NEXT) measures the energy coupling backward to the aggressor's source end. Far-End Crosstalk (FEXT) measures the energy coupling forward to the victim's receiver end. Compliance specifications for multi-lane protocols define NEXT and FEXT isolation thresholds that must be met across the entire operating frequency range.

### IF Bandwidth and Dynamic Range

The precision of each frequency-domain measurement depends on how long the VNA dwells at each frequency step. The instrument controls this through its Intermediate Frequency (IF) bandwidth setting. The IF bandwidth defines the width of the detection filter centered on the measurement frequency.

A wider IF bandwidth allows the instrument to sweep quickly but admits more thermal noise into the measurement. Thermal noise is random, Gaussian, and zero-mean. The VNA test signal is a steady, deterministic sine wave. If the instrument measures for a very short duration, a random noise spike might superimpose on the signal, producing a false amplitude reading. Narrowing the IF bandwidth forces the analyzer to dwell longer at each frequency step, collecting more samples. The positive and negative random noise spikes mathematically cancel toward zero over longer averaging windows, while the deterministic sine wave remains constant. This noise cancellation lowers the measurement noise floor, allowing the analyzer to detect extremely faint signals buried deep in the noise.

The practical consequence is a direct tradeoff between sweep speed and dynamic range. A wide IF bandwidth produces a fast sweep with a shallow noise floor, adequate for measuring insertion loss on low-loss channels. A narrow IF bandwidth produces a slow sweep with a deep noise floor, necessary for measuring weak crosstalk signals or verifying the isolation of high-quality shielding.

## Worked Examples

### Reading an S-Parameter Plot

Consider a 12-inch PCB differential pair measured with a 4-port VNA from 10 MHz to 20 GHz. The $S_{dd21}$ (differential insertion loss) trace begins near 0 dB at low frequencies, indicating that nearly all the signal power reaches the receiver. As frequency increases, dielectric absorption and skin effect losses progressively attenuate the signal. The trace slopes downward, reaching $-3$ dB at approximately 8 GHz (the half-power frequency for this trace length) and $-15$ dB at 20 GHz. The compliance specification for the protocol requires that $S_{dd21}$ remain above the specification mask at every frequency point within the operating band.

The $S_{dd11}$ (differential return loss) trace begins at a large negative value (for example, $-30$ dB at low frequencies, indicating excellent matching). As frequency increases, parasitic resonances from vias and connectors create peaks where the return loss degrades. A spike reaching $-10$ dB at 12 GHz indicates that 10% of the injected power reflects back at that frequency, signaling a localized impedance mismatch that worsens at that specific resonant frequency.

### Converting Between Domains: FFT and IFFT

The mathematical connection between TDR and VNA measurements is the Fourier transform. A Fast Fourier Transform (FFT) decomposes a time-domain signal into its constituent frequency components. A sharp time-domain step function consists of an infinite sum of continuous sine waves, and the FFT calculates the exact magnitude and phase of each sine wave required to construct that step.

Applied to TDR data, the FFT converts the measured step response into an equivalent $S_{11}$ frequency-domain trace. The Inverse Fast Fourier Transform (IFFT) performs the reverse operation: it takes VNA S-parameter data and reconstructs the equivalent time-domain waveform. This bidirectional conversion allows engineers to view the same physical channel through either the spatial lens of TDR or the spectral lens of the VNA, choosing whichever representation best illuminates the specific defect under investigation.

## Edge Cases

### Passive Reciprocity and Its Violations

The reciprocity property ($S_{21} = S_{12}$) holds strictly for any passive, linear, time-invariant network. A copper trace, a connector, a via, a passive filter, or any combination of these elements will always exhibit identical forward and reverse transmission. Violating reciprocity requires an active element (a transistor amplifier providing gain in one direction), a nonlinear element (a diode whose impedance changes with signal amplitude), or a non-reciprocal component (a ferrite circulator or isolator that exploits magnetic bias to break symmetry).

Verifying reciprocity in measured data serves as a built-in sanity check. If a VNA measurement of a passive PCB trace shows $S_{21} \neq S_{12}$ beyond the instrument's measurement uncertainty, the discrepancy indicates a calibration error, a connector problem, or a systematic measurement artifact rather than a genuine physical asymmetry.

### The Tradeoff: Sweep Speed vs. Noise Floor

Narrowing the IF bandwidth improves dynamic range but proportionally increases the total sweep time. A 10 Hz IF bandwidth provides approximately 40 dB more dynamic range than a 10 kHz IF bandwidth, but the sweep takes 1000 times longer. Production environments performing high-volume compliance testing optimize this tradeoff by using a wide IF bandwidth for quick pass/fail screening and switching to a narrow IF bandwidth only when investigating marginal failures or measuring weak crosstalk signals that approach the noise floor.

### What S-Parameters Cannot Capture

S-parameters describe only the linear, time-invariant behavior of a network. They cannot represent phenomena that depend on signal amplitude (compression in active devices, dielectric nonlinearity at extreme voltages) or phenomena that change over time (thermal drift during a long measurement, aging of connector contacts). Systems that exhibit any of these behaviors require either large-signal measurement techniques or time-stamped repeated sweeps to track the variation.
