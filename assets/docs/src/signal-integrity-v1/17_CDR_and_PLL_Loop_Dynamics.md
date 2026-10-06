# CDR and PLL Loop Dynamics

<!-- SUMMARY: High-speed serial links embed the clock directly in the data stream, forcing the receiver to reconstruct a local sampling clock from incoming voltage transitions. This guide derives the PLL-based clock and data recovery (CDR) loop dynamics, covering loop bandwidth, jitter transfer and tolerance, charge pump architecture, and the distinction between analog VCO-based and DSP-based digital CDR receivers. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

High-speed serial links transmit no separate clock signal. PCIe, USB, Ethernet, and every modern protocol embed the clock directly into the data stream, forcing the receiver to reconstruct a local clock from the timing of the incoming voltage transitions. This reconstruction is the job of the Clock and Data Recovery (CDR) circuit, and its core mechanism is a Phase-Locked Loop (PLL): a feedback control system that continuously adjusts a local oscillator to track the incoming data edges.

The CDR is not simply a clock extractor. It is a filter with carefully chosen dynamics. Low-frequency timing drift (from temperature changes, supply voltage variation, or crystal oscillator tolerance) must be tracked so that the recovered clock moves with the data and the eye stays open. High-frequency timing noise (from random thermal events, crosstalk, or power supply transients) must be rejected so that the recovered clock holds steady and does not chase every stray edge displacement. The boundary between tracking and rejection is the loop bandwidth, and the shape of the frequency response near that boundary determines whether the loop amplifies jitter (peaking) or smoothly attenuates it. These dynamics are governed entirely by the physics of the analog components inside the loop filter: a charge pump, a resistor, a capacitor, and a voltage-controlled oscillator.

Two fundamentally different receiver architectures implement clock recovery. The traditional analog CDR uses a PLL with a voltage-controlled oscillator that physically speeds up and slows down to track the data. The DSP-based digital CDR, which dominates the 112G/224G era, runs a free-running ADC clock and uses mathematical interpolation to reconstruct the optimal sampling point from digitized samples. Both architectures solve the same problem (aligning a local sampling instant to the center of the incoming data eye), but they solve it through radically different physical mechanisms with distinct tradeoffs in noise performance, power consumption, and silicon area.

Understanding CDR loop dynamics is essential for two reasons. First, the loop bandwidth and peaking directly determine which jitter components close the eye and which are invisible to the receiver. Second, protocol compliance testing requires test equipment (oscilloscopes and BERTs) to emulate the exact CDR behavior specified by the standard's "Golden PLL," so that the measured eye diagram reflects what a real receiver would see.

## Core Concepts

### Why Embedded Clocking Requires CDR

Running an external clock at gigahertz frequencies introduces a fundamental synchronization problem. A millimeter of trace length difference or a fraction of a degree of temperature change causes the clock phase and data phase to drift apart. This skew shifts the sampling instant toward the edge of the eye, degrading bit error performance. At multi-gigahertz data rates, maintaining phase alignment between a separate clock trace and a data trace across manufacturing variation, thermal gradients, and cable lengths is physically impractical.

Embedding the clock into the data eliminates the synchronization problem entirely. The transmitter encodes information as voltage transitions on a single differential pair. The receiver extracts timing information from those same transitions and generates a local clock that is, by construction, aligned to the data it must sample. Skew and thermal wander are eliminated because the clock is derived from the data itself.

This approach requires guaranteed transitions in the data stream. A long unbroken run of identical bits produces no voltage transitions, leaving the CDR with nothing to track. Line coding schemes (8b/10b, 128b/130b, scrambling) prevent long runs and maintain transition density, as covered in [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md).

### The Phase-Locked Loop as a Feedback Control System

The CDR is built around a phase-locked loop consisting of four functional blocks arranged in a closed feedback path.

**Phase Detector.** The phase detector compares the timing of each incoming data transition against the edge of the locally generated clock. The comparison produces a signal proportional to the time gap between the two edges. A common hardware implementation is the Bang-Bang (Alexander) Phase Detector, which uses D-flip-flops and a transistor switch to control a charge pump. When a data edge arrives, a flip-flop turns on the switch and connects a precision current source to the loop filter. When the local clock edge arrives, a second flip-flop turns the switch off. If the clock is far behind the data, the switch stays closed longer and a large pulse of current flows. If the two edges arrive simultaneously, the switch barely opens and almost zero current flows. The output is a current pulse whose duration encodes the magnitude and polarity of the phase error. A data edge arriving before the clock produces an "UP" pulse; a data edge arriving after the clock produces a "DOWN" pulse.

**Charge Pump and Loop Filter.** The UP or DOWN pulses from the phase detector turn on a current switch (the charge pump), which sends a burst of current into the loop filter. The loop filter converts these current pulses into a smoothly varying control voltage. The components of the loop filter (resistors and capacitors) determine whether the loop is first-order or second-order, and their values set the loop bandwidth, damping factor, and peaking behavior. The physics of the loop filter is the central subject of this guide.

**Voltage-Controlled Oscillator (VCO).** The VCO generates the local clock signal at a frequency determined by its input voltage. Inside the VCO, a specialized diode called a varactor acts as a voltage-variable capacitor. The varactor sits within an LC tank circuit whose resonant frequency is $f = 1 / (2\pi\sqrt{LC})$. Changing the voltage applied to the varactor physically expands or contracts the depletion region inside the silicon, changing its capacitance. That capacitance change shifts the resonant frequency of the LC tank, which changes the VCO output frequency. Every VCO has a hardware specification called VCO gain ($K_{\text{vco}}$), measured in hertz per volt. If a VCO has a gain of 100 MHz/V, applying 1 V to its input increases the output frequency by 100 MHz. The relationship is strictly linear over the operating range.

**Feedback Path.** The VCO's output clock is routed back to the phase detector, closing the loop. The phase detector compares this clock against the next incoming data transition, and the cycle repeats continuously.

### Frequency as a Consequence of Phase Alignment

A PLL has no concept of frequency. The phase detector only sees phase: the time difference between a data edge and a clock edge at one specific instant. Frequency matching is purely a mathematical consequence of the system finding equilibrium. From calculus, frequency is the derivative of phase with respect to time. If the phase difference between clock and data is constant (not growing, not shrinking), the frequencies must be identical. The loop does not measure frequency, does not compare frequencies, and has no frequency detector. It controls frequency indirectly by controlling phase, and the mathematical relationship between phase and frequency ensures that a stable phase lock implies a stable frequency lock.

This principle reveals the distinction between two quantities that the loop connects:

*   **Phase Difference** is a static measurement: the time gap (in picoseconds) between a data edge and a clock edge at one specific instant.
*   **Rate of Phase Change** is literally a frequency difference. If the phase difference is growing over time, the clock and data are running at two different frequencies. If the phase difference is constant, the frequencies match exactly.

The phase detector measures only the phase difference. It has no memory and performs no differentiation. Every time an edge arrives, it simply measures the instantaneous phase gap and outputs a voltage proportional to that distance. The loop uses this static phase difference to set the VCO frequency, which in turn dictates the rate of phase change. When the loop reaches equilibrium, the phase difference is constant and the rate of phase change is zero, meaning the frequencies have matched.

### Loop Bandwidth: The Boundary Between Tracking and Filtering

The CDR acts as a low-pass filter for jitter. The loop bandwidth is the cutoff frequency of that filter.

**Below the loop bandwidth.** Timing variations slower than the loop bandwidth are tracked by the recovered clock. If the data slowly wanders back and forth due to thermal drift or supply voltage variation, the recovered clock wanders with it. The relative timing between clock and data remains constant, the sampling instant stays centered in the eye, and these slow jitter components do not degrade the bit error ratio. The CDR "tracks them out."

**Above the loop bandwidth.** Timing variations faster than the loop bandwidth are too rapid for the feedback loop to follow. The recovered clock holds steady while the incoming data edges vibrate around it. These high-frequency jitter components shift the data transitions relative to the fixed sampling instant and close the eye. They appear directly in the measured jitter.

The loop bandwidth is not set arbitrarily. Making it too wide causes the clock to chase stray noise spikes (a cosmic ray hit, a crosstalk burst, a random thermal event that displaces a single edge by 100 picoseconds). An excessively wide bandwidth would cause the clock to violently track that noise, destroying the timing reference for subsequent bits. Making the loop bandwidth too narrow prevents the clock from tracking legitimate low-frequency drift, causing the sampling instant to slide away from the eye center. Protocol standards specify the loop bandwidth as a compromise between these two failure modes.

### Clock Architecture and Phase Interpolators

Transmitter and receiver typically share a common reference architecture. A stable, low-frequency crystal oscillator on the motherboard (commonly 100 MHz) provides the frequency reference. The transmitter multiplies this reference up to the line rate using a PLL (for example, 100 MHz multiplied by 160 to produce 16 GHz). The receiver multiplies its own 100 MHz crystal to the same approximate frequency using a separate PLL.

The CDR's task is then to take that locally generated clock and fine-tune its phase to align precisely with the incoming data transitions. Many modern implementations accomplish this fine-tuning through a Phase Interpolator rather than directly adjusting the VCO frequency. The Phase Interpolator takes the local clock and mathematically blends between adjacent phase taps to shift the sampling edge in precise fractional-UI increments, achieving the same alignment result through digital phase control rather than analog frequency manipulation.

### Type-I and Type-II Loop Classification

PLL loop dynamics literature describes loops as "first-order" or "second-order" based on the number of energy-storage elements in the loop filter, and as "Type-I" or "Type-II" based on the number of integrators in the open-loop transfer function. In the context of CDR design, a first-order loop with a resistor-only filter is a Type-I system (proportional control only), and a second-order loop with a resistor-capacitor filter is a Type-II system (proportional plus integral control). The Type-I and Type-II naming convention maps directly onto the first-order and second-order architectural distinction that governs the loop's steady-state behavior, its ability to eliminate phase error, and its susceptibility to overshoot and ringing.

## Architecture

### First-Order Loop: Proportional Control (Type-I)

The simplest loop filter is a single resistor. The charge pump outputs a current proportional to the phase error. Ohm's law converts that current to a voltage across the resistor ($V = I \times R$). This voltage directly controls the VCO frequency. The control voltage is strictly proportional to the instantaneous phase error: $V_{\text{control}} = K \times \text{Phase Error}$. A larger phase error produces a higher voltage; a smaller phase error produces a lower voltage; zero phase error produces zero voltage.

A first-order loop is unconditionally stable. Its frequency response is a smooth low-pass curve with zero peaking. It tracks low-frequency jitter with unity gain and rolls off monotonically above the loop bandwidth.

#### Static Phase Offset: The Catch-22

The fatal limitation of a Type-I loop is the steady-state phase error. The mechanism is a catch-22 rooted in the physics of the resistor.

Consider a transmitter crystal running at 101 MHz while the receiver's VCO naturally oscillates at 100 MHz when its control input sits at 0 V. The VCO needs a non-zero control voltage to speed up from its resting frequency to match the data. With a VCO gain of 100 MHz/V, matching the 1 MHz frequency offset requires exactly +10 mV. The resistor generates voltage only when current flows through it, and the charge pump generates current only when the phase detector measures a non-zero time gap between the data edge and the clock edge.

Here is what happens cycle by cycle:

1.  The data is arriving at 101 MHz while the VCO clock runs at 100 MHz. The clock is slower, so each successive clock edge falls further behind the corresponding data edge. The phase error is actively growing.
2.  As the phase error grows, the phase detector outputs wider UP pulses. The voltage across the resistor rises in proportion: at 5 degrees of phase error, the voltage is 1.1 V; at 10 degrees, it is 1.3 V; at 15 degrees, it is 1.5 V.
3.  The rising voltage pushes the VCO frequency upward: 100.1 MHz, 100.5 MHz, 100.9 MHz.
4.  At exactly 15 degrees of phase error and 1.5 V of control voltage, the VCO reaches 101 MHz. At this instant, the clock and data are running at the same speed.

The system now freezes. The clock edges stop falling further behind the data edges, so the phase error stops growing. The phase detector keeps measuring the same 15 degrees of separation edge after edge, and the resistor keeps producing the same 1.5 V. The VCO holds steady at 101 MHz.

This equilibrium is self-arresting. The loop cannot correct the 15-degree phase error because doing so would destroy the voltage required to maintain the frequency match. If the clock attempted to catch up to the data (reducing the phase error toward zero), the voltage across the resistor would drop. As the voltage dropped, the VCO frequency would fall below 101 MHz, the clock would start falling behind again, and the phase error would grow back to 15 degrees. The system is trapped: the phase error is stuck at a permanent, non-zero offset because that offset is the only mechanism available for generating the control voltage the VCO requires. This permanent offset is called **static phase offset**.

The hardware cannot escape this trap because the Type-I loop filter has no memory. The voltage exists only as long as the current flows, and the current flows only as long as there is an error. The loop uses phase difference to control frequency, but it cannot drive phase difference to zero while simultaneously maintaining the voltage that keeps the frequency matched.

### Second-Order Loop: Proportional Plus Integral Control (Type-II)

Adding a capacitor in series with the resistor transforms the loop filter into a proportional-integral (PI) controller. The total control voltage delivered to the VCO is the sum of two components:

$$V_{\text{total}} = V_{\text{resistor}} + V_{\text{capacitor}} = I \times R + \frac{1}{C}\int I \, dt$$

The resistor provides an instantaneous voltage proportional to the current (proportional control). The capacitor accumulates charge over time, producing a voltage that integrates the history of all past error currents (integral control).

The series arrangement is critical. In a parallel configuration, the capacitor would absorb and smooth out the fast voltage transients from the resistor, eliminating the proportional response. In series, the VCO receives the instant "kick" from the resistor (to react to sudden phase jumps) plus the slow, steady memory of the capacitor (to correct permanent frequency offsets). The resistor and capacitor values jointly determine the loop bandwidth and damping factor.

**Eliminating steady-state phase error.** When the transmitter runs at 101 MHz and the VCO rests at 100 MHz, the phase detector generates a persistent trickle of error current. This current charges the capacitor, and its voltage slowly rises: 1 mV, 5 mV, 9 mV. The VCO speeds up progressively. As the frequency gap closes, the phase error shrinks and the error current diminishes. At the moment the clock achieves perfect phase alignment, the charge pump stops outputting current. Unlike the resistor, which drops to zero voltage immediately, the capacitor holds its accumulated charge. It stores the +10 mV like a battery, continuously feeding it to the VCO. The loop has reached perfect equilibrium: the phase error is zero, the current is zero, and the VCO is held at exactly 101 MHz by the capacitor's stored charge. The integrator drives the steady-state phase error to absolute zero regardless of the frequency offset between transmitter and receiver crystals.

In real silicon, the capacitor slowly leaks charge through parasitic resistance. At gigabit data rates, however, data transitions arrive so frequently that the phase detector sends continuous micro-pulses of correction current to maintain the stored voltage at the correct level. The leakage is negligible in practice.

Virtually all high-speed standards (PCIe, USB, Ethernet) mandate second-order CDRs because every physical link involves two independent crystal oscillators with parts-per-million (PPM) frequency tolerances that cannot be bridged without integral control.

#### The Overshoot Mechanism: How Type-II Eliminates Phase Error

The capacitor does not simply accumulate charge to the correct voltage and stop. The physical mechanism by which the Type-II loop drives phase error to zero requires a temporary frequency overshoot.

Phase cannot be changed without a difference in frequency. Phase is the integral of frequency over time, so the only way for the clock to catch up to the data is if the clock temporarily runs *faster* than the data. This is the fundamental constraint that separates the Type-II from the Type-I.

Scenario: Data is 101 MHz, VCO rests at 100 MHz.

1.  **The Lag.** The VCO is slower than the data, so the data pulls ahead. A large phase error accumulates as the clock edges fall further and further behind.
2.  **The Charge.** The phase detector sees this growing error and pumps current into the capacitor. The voltage rises, and the VCO frequency rises with it.
3.  **The Crossing Point.** The VCO reaches 101.0 MHz. At this instant, the frequencies match. The phase error stops growing. But a massive phase error remains from the entire time the capacitor was charging up and the clock was running slower than the data.
4.  **The Overshoot.** That large residual phase error still drives the phase detector to output UP pulses. The charge pump keeps pushing current into the capacitor. The voltage continues to rise, pushing the VCO frequency past 101.0 MHz to, say, 101.2 MHz.
5.  **Closing the Gap.** The VCO is now running faster than the data (101.2 MHz vs. 101.0 MHz). Because the clock is faster, it begins to catch up to the data. The phase error shrinks.
6.  **The Settling.** As the phase error shrinks toward zero, the phase detector stops pumping excess current. The control voltage settles back down. The loop reaches equilibrium at the exact moment the phase error hits zero and the VCO frequency returns precisely to 101.0 MHz. The capacitor holds the correct voltage indefinitely.

The Type-I loop physically cannot execute this overshoot. In a Type-I system, the control voltage is tied to the instantaneous phase error. To overshoot the frequency to 101.2 MHz, the phase error would have to grow to the value that generates enough voltage for 101.2 MHz. But the moment the clock speeds up and the phase error starts shrinking, the voltage instantly drops, immediately pulling the frequency back down before the phase can ever reach zero. The Type-I system lacks the component (the capacitor) that would allow it to hold excess voltage while the phase error is being corrected.

The capacitor is the physical memory device that makes the overshoot possible. It stores the baseline voltage required for 101 MHz while the phase detector temporarily pushes it higher to close the phase gap. Once the gap is closed, the excess charge drains and the voltage settles to the baseline.

#### Ringing: The Time-Domain Cost of Overshoot

The overshoot does not stop cleanly on the first pass. The Type-II loop exhibits ringing (decaying oscillation) before it settles, and this is a direct consequence of second-order control theory.

When the phase error reaches zero, the capacitor still holds the excess voltage that pushed the VCO past 101.0 MHz. The clock is still running faster than the data, so the clock edge physically passes the data edge. The phase error immediately becomes non-zero in the opposite direction (the clock is now early instead of late). The phase detector switches from sending UP pulses to sending DOWN pulses. The DOWN pulses extract electrons from the capacitor, lowering the voltage. The frequency drops.

If the loop filter were a pure capacitor with no resistor, this overshoot and correction cycle would repeat indefinitely with constant amplitude, exactly like a frictionless pendulum swinging through the center point. The system would never settle.

The resistor in the loop filter acts as electrical damping. It provides a proportional voltage component that reacts instantaneously to the current error, counteracting the stored energy in the capacitor. Each successive overshoot is smaller than the previous one. The control voltage and phase error oscillate with decreasing amplitude until the system parks at exactly zero phase error and exactly the correct frequency. Hardware designers tune the ratio of the resistor and capacitor values to control the damping factor. A critically damped or slightly overdamped response flattens the oscillation and settles quickly. An underdamped response rings longer but may converge faster on the initial approach. Protocol compliance specifications constrain the maximum peaking (typically 1 dB or 2 dB), which is the frequency-domain manifestation of the time-domain ringing.

### Digital CDR: Free-Running Clock and Mathematical Phase Recovery

Ultra-high-speed DSP-based receivers (112G+ Ethernet, 224G development) replace the analog PLL with a fully digital clock recovery architecture. There is no voltage-controlled oscillator, no charge pump, and no analog feedback loop.

**The free-running clock.** On the receiver board, a local crystal oscillator drives the ADC at a fixed, stable frequency. This clock is not controlled by a feedback loop; it runs freely. The ADC takes snapshots of the incoming waveform strictly at this rate. The transmitter on the opposite end of the link has its own crystal oscillator, running at a frequency that differs by a few parts per million. This slight frequency mismatch causes the ADC sampling point to drift slowly across the data eye over time.

**Mueller-Muller phase detection.** The DSP examines the digitized amplitude of the signal during bit transitions to determine the sampling phase offset. The algorithm compares the voltage of the current sample against the voltage of the previous sample at a data transition. If the ADC is sampling at the dead center of the eye, the voltages on either side of a transition are symmetrical: a 0-to-1 transition produces a sample at $-0.5$ V followed by a sample at $+0.5$ V, with equal magnitudes. If the ADC clock is drifting late, the sample during the 0 is taken as the voltage is already rising toward the transition and might measure $-0.2$ V, while the sample during the 1 is taken further up the flat top of the pulse and might measure $+0.6$ V. The asymmetry between these two amplitudes tells the DSP exactly which direction the clock is drifting, and the magnitude of the imbalance is mathematically proportional to the time offset.

**Phase interpolation.** The DSP maintains a digital phase offset register tracking exactly how far off-center the ADC is currently sampling. A digital FIR interpolation filter uses this offset to compute the voltage that the waveform would have had at the exact center of the eye, even though the ADC never physically sampled that instant. The interpolator examines the sample taken slightly before the ideal point and the sample taken slightly after, then calculates the intermediate value using the known signal shape. The DSP continuously updates the phase register and applies this mathematical correction to every incoming sample.

The Mueller-Muller phase detector has a critical advantage over the Bang-Bang (Alexander) phase detector used in analog CDRs. The Bang-Bang detector is an edge-based detector: it examines only the polarity of the data transition and produces a binary early/late decision. The Mueller-Muller detector is a baud-rate detector: it operates on the amplitude of the signal at the sampling point itself, extracting phase information without requiring a separate sample at the data edge. This allows the ADC to operate at exactly the symbol rate (one sample per UI) rather than at twice the symbol rate, halving the ADC's required sampling speed and power consumption.

### Cycle Slipping

The free-running ADC clock and the transmitter clock are not phase-locked. Their slight frequency mismatch causes the phase offset to accumulate continuously. If the transmitter is slightly faster than the receiver's ADC clock, each successive sample drifts a little later relative to the data eye. Eventually, the accumulated phase offset reaches 360 degrees (one full bit period), and the DSP resets the phase counter to zero. This event is called a **cycle slip**.

**Dropped bits (data faster than the ADC clock).** The data bits arrive slightly faster than the ADC can sample them. Each sample drifts progressively later in the data eye. After thousands or millions of bits, a data bit slides entirely past the ADC between two consecutive samples. The receiver physically misses that bit. The phase offset register reaches 360 degrees and resets.

**Duplicated bits (ADC clock faster than the data).** The ADC samples arrive slightly faster than the data transitions. Each sample drifts progressively earlier in the data eye. Eventually, the ADC samples twice while the same data bit is present on the wire. The receiver records two copies of a single bit. The phase offset register reaches $-360$ degrees and resets.

A cycle slip is not a catastrophic failure. The digital CDR immediately resumes normal tracking after the phase counter reset. The system does not lose synchronization or require retraining. The single dropped or duplicated bit is a localized error that Forward Error Correction (FEC) is designed to absorb. DSP-based SerDes architectures depend on robust FEC (Reed-Solomon codes at the physical layer) specifically because cycle slips are an expected, periodic consequence of running without a phase-locked oscillator. The FEC algorithm identifies the missing or duplicated bit in the received sequence and mathematically reconstructs the correct data, allowing the system to run indefinitely without a physical PLL.

### Peaking: The Cost of the Integrator

The capacitor that eliminates steady-state phase error introduces a time delay into the feedback path. A capacitor cannot change its voltage instantaneously; it requires time to accumulate charge. In AC circuit analysis, this charging time manifests as a phase shift (up to 90 degrees) between the current entering the capacitor and the voltage appearing across it.

This delayed correction interacts destructively with jitter at frequencies near the loop bandwidth.

**Low-frequency jitter.** The capacitor's charging delay is negligible relative to the slow jitter period. The VCO tracks the data accurately.

**High-frequency jitter.** The jitter oscillates so rapidly that the capacitor averages out to a flat DC voltage. The tracking stops, and the low-pass filter does its job.

**Jitter near the loop bandwidth.** At this crossover frequency, the jitter oscillates at the exact rate where the capacitor's delay is maximally destructive. By the time the capacitor charges up and delivers a correction voltage telling the VCO to slow down, the incoming jitter has already reversed direction and the VCO should be speeding up. The delayed correction adds to the existing error rather than subtracting from it. This constructive interference causes the VCO to swing further out of alignment than the original jitter. The feedback loop is chasing its tail: each correction arrives at the wrong moment and amplifies the oscillation rather than damping it.

On a Bode plot of the Jitter Transfer Function (JTF), this amplification appears as a bulge above 0 dB just before the rolloff frequency. A first-order filter shows a flat 0 dB line (unity gain, perfect 1:1 tracking) that smoothly curves downward at the cutoff. A second-order filter with peaking shows the same flat 0 dB line, but the curve bulges upward (for example, to +1.5 dB or +2 dB) just before the cutoff, then drops steeply. That physical bulge is the peaking.

The practical consequence is direct: if incoming data carries a jitter component at exactly the peaking frequency with an amplitude of 10 picoseconds, and the JTF gain at that frequency is +2 dB (a voltage ratio of approximately 1.26), the recovered clock oscillates by approximately 12.6 picoseconds. The clock is shaking more violently than the data. The relative timing displacement between clock and data at this frequency is worse than if the CDR were absent, closing the eye and spiking the bit error ratio.

### VCO Phase Adjustment Through Temporary Frequency Change

The VCO has only one control input, and that input controls frequency. It has no separate phase control. Yet the CDR must correct both frequency offsets and phase errors.

A change in frequency inherently produces a change in phase. Consider two identical square waves running at 10 GHz with their rising edges perfectly aligned. To shift the second wave's phase so that its edges arrive 5 picoseconds earlier, the VCO control voltage is temporarily increased, speeding the oscillator to 11 GHz for a brief interval. The faster oscillation causes the edges to accumulate a phase lead. Once the edges have walked exactly 5 picoseconds forward, the control voltage drops back, returning the VCO to 10 GHz. The two waves now run at the same frequency, but the second is permanently shifted 5 picoseconds ahead. By transiently manipulating frequency, the VCO achieves a permanent phase correction.

### The Jitter Transfer Function

The Jitter Transfer Function (JTF) quantifies the CDR's filtering behavior. It is not a voltage measurement. It is a ratio of time quantities:

$$\text{JTF}(f) = 20 \log_{10}\left(\frac{\text{Jitter Amplitude Out}}{\text{Jitter Amplitude In}}\right)$$

At 0 dB (a ratio of 1), the recovered clock vibrates by exactly the same amount as the incoming data. The clock and data move together, and the eye stays open. At -20 dB (a ratio of 0.1), the recovered clock vibrates by only one-tenth of the input jitter amplitude. The clock is stable while the data moves, and that relative motion closes the eye. At +2 dB (a ratio of approximately 1.26), the recovered clock vibrates more than the data, and the amplified relative motion closes the eye even further.

The critical distinction between clock frequency and jitter frequency causes persistent confusion. The clock frequency (for example, 16 GHz) describes how fast the bits arrive on the wire. The jitter frequency (for example, 5 MHz) describes how fast the phase error oscillates back and forth. Peaking occurs at the jitter frequency where the loop's reaction delay causes constructive interference, typically in the single-digit to tens-of-megahertz range. It has no direct relationship to the multi-gigahertz bit rate.

## Worked Examples

### Steady-State Phase Error in a Type-I Loop

A receiver's VCO has a natural resting frequency of 100 MHz at 0 V input and a VCO gain of 10 MHz/V. The incoming data arrives at 101 MHz. The phase detector gain produces a control voltage strictly proportional to the phase error.

**Step 1: Initial state.** The VCO is running at 100 MHz. The data is arriving at 101 MHz. The clock is slower, so the phase error begins to grow.

**Step 2: Voltage rises with phase error.** At 5 degrees of phase error, the phase detector produces 1.1 V, pushing the VCO to approximately 100.1 MHz. At 10 degrees, it produces 1.3 V. At 15 degrees, it produces 1.5 V. At exactly 1.5 V, the VCO reaches 101 MHz.

**Step 3: The freeze.** The clock and data are now running at the same speed. The clock edges stop falling further behind. The phase detector measures 15 degrees on the next edge, and the next, and the next. It outputs 1.5 V every time. The voltage "stops rising" simply because the phase detector keeps measuring the same 15-degree distance.

**Step 4: Equilibrium.** The system is locked with the clock edge permanently 15 degrees behind the data edge. This offset generates the exact 1.5 V the VCO needs to hold 101 MHz. The frequencies match, but the clock samples off-center in the eye.

**Step 5: Attempting higher gain.** Increasing the phase detector gain would reduce the steady-state error (the same 1.5 V could be produced by a smaller phase offset). Excessively high gain makes the feedback loop violently unstable: any microscopic phase perturbation produces an enormous voltage spike that drives the VCO frequency wildly out of control. Hardware designers accept a moderate steady-state error as the stability cost of a first-order loop, or they add a capacitor to eliminate the error entirely.

### Peaking Amplification at the Loop Bandwidth

A second-order CDR has a loop bandwidth of 10 MHz and 2 dB of peaking. The incoming data carries a periodic jitter component at 10 MHz with an amplitude of 10 ps peak-to-peak.

**Step 1: JTF gain at 10 MHz.** The peaking specification indicates +2 dB gain at the loop bandwidth frequency. Converting to a linear ratio: $10^{2/20} \approx 1.26$.

**Step 2: Recovered clock jitter.** The clock oscillates by $10\text{ ps} \times 1.26 = 12.6\text{ ps}$ peak-to-peak. The clock is moving 2.6 ps more than the data at this frequency.

**Step 3: Eye closure.** The relative jitter between clock and data at 10 MHz is 2.6 ps peak-to-peak. This additional timing displacement reduces the eye opening and increases the probability of a slicer error. The effect is concentrated at the peaking frequency; jitter at lower or higher frequencies experiences unity gain or attenuation, respectively.

## Edge Cases

### CDRs in Test Equipment and the Golden PLL

The error detector (ED) inside a BERT faces the same clock recovery challenge as a silicon receiver: it receives a serial stream with no separate clock and must recover timing to sample the incoming bits for error comparison. The BERT therefore contains a high-performance CDR with precisely configurable loop bandwidth and peaking.

The configurability exists because test equipment must not be "too good." If a BERT's CDR tracks jitter perfectly and recovers data that a standard silicon receiver would fail on, the compliance test is invalid. Protocol standards (PCI-SIG for PCIe, IEEE 802.3 for Ethernet) define a mathematical reference receiver model called the Golden PLL, which specifies the exact loop bandwidth and maximum peaking. The BERT's CDR must be configured to match this specification so that its error detection reflects the performance a real receiver would achieve.

The same principle applies to oscilloscopes. When a real-time oscilloscope draws an eye diagram, its software CDR recovers the clock and folds the waveform. If the software CDR bandwidth is set too low, the scope will not track low-frequency jitter that a real receiver would track, and the eye will appear artificially closed. If the bandwidth is set too wide, the scope will track jitter that a real receiver cannot follow, and the eye will appear artificially open. The CDR bandwidth must match the Golden PLL specification defined by the protocol standard.

### Infinite Bandwidth and the Noise Rejection Tradeoff

Setting the CDR loop bandwidth to infinity would cause the clock to track every timing displacement, including single-event transients (crosstalk bursts, power supply glitches, cosmic ray hits). A stray noise spike that displaces one data edge by 100 ps would cause the recovered clock to jump 100 ps, destroying the timing reference for the next several bits. The finite loop bandwidth gives the flywheel inertia: the clock tracks the slow, real drift of the system but ignores fast, random noise. The loop bandwidth is the engineering compromise between drift tracking and noise rejection, and the protocol specification mandates its exact value.

### Capacitor Leakage in the Loop Filter

The integrator capacitor in a second-order loop filter theoretically holds its charge indefinitely, maintaining the control voltage that keeps the VCO at the correct frequency even when the phase error is zero. In real silicon, parasitic resistance across the capacitor causes slow charge leakage. At the data rates of modern serial links (multi-gigahertz), data transitions arrive so frequently that the phase detector delivers continuous micro-pulses of correction current faster than the leakage drains charge. The net effect of parasitic leakage is negligible in practical CDR implementations.

## References

**Source Extractions:**
- [extraction_784dbc1a_dsp_pll_cdr_deep_dive.md](../../source_extractions/extraction_784dbc1a_dsp_pll_cdr_deep_dive.md): Blocks 1 (CDR portion), 3, 4, 5, 6, 7, 8, 9, 10
- [extraction_77862985_cdr_pll.md](../../source_extractions/extraction_77862985_cdr_pll.md): Blocks 3-10
- [extraction_647ef085_serdes_eye_diagrams.md](../../source_extractions/extraction_647ef085_serdes_eye_diagrams.md): Block 8

**Related Guides:**
- [CTLE and DFE](../04_Equalization_and_Receiver_Architecture/14_CTLE_and_DFE.md): Receiver-side equalization architecture, analog vs. DSP DFE
- [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md): System-level signal path, hardware vs. software CDR
- [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md): Transition density, FEC for cycle slip tolerance
