# SerDes Architecture and Eye Diagrams

<!-- SUMMARY: The serializer/deserializer (SerDes) is the fundamental architecture underlying every modern high-speed interface, resolving the speed mismatch between the physical channel and digital logic. This guide traces the complete signal path from parallel-to-serial conversion through the analog front end, and explains how real-time oscilloscopes, sampling oscilloscopes, and BERTs each construct eye diagrams through physically distinct measurement mechanisms. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

A serializer/deserializer (SerDes) link is the fundamental architecture underlying every modern high-speed interface: PCIe, Ethernet, USB, HDMI, and DisplayPort all transmit data as a continuous stream of serial bits across a single differential pair, then reconstruct the parallel data words inside the receiving chip. The entire system exists because of a speed mismatch between the physical channel and the digital logic. A copper trace or optical fiber can carry analog transitions at 112 Gbps, but no digital logic gate can switch at 112 GHz. The SerDes architecture resolves this contradiction by confining extreme-speed analog processing to a tiny, specialized front-end circuit and then gearing the data down to a clock rate that standard digital silicon can handle.

The eye diagram is the primary visual tool for evaluating whether the analog portion of that system is working. It represents the accumulated voltage and timing margin available to the receiver at the moment it commits to a bit decision. Three fundamentally different instruments produce eye diagrams through three different physical mechanisms: real-time oscilloscopes capture continuous waveforms and fold them mathematically, sampling oscilloscopes build dot-by-dot reconstructions using a hardware trigger, and bit error ratio testers (BERTs) sweep a decision threshold across a time-voltage grid and map the statistical boundary where errors begin. Understanding how each instrument constructs its eye, and what that eye physically represents, is essential for interpreting signal integrity measurements at any data rate.

## Core Concepts

### The SerDes Signal Path

The transmitter and receiver halves of a SerDes link divide naturally into analog and digital domains, with the boundary between them defining the critical interface where signal integrity measurements take place.

**Transmitter (TX).** The digital core generates parallel data words at a relatively low clock rate. A multiplexer (MUX) serializes those parallel words into a single high-speed bitstream. For NRZ signaling, the output stage is a current-mode differential driver that steers a constant current between two complementary outputs. To send a logic 1, the driver routes current so that D+ swings positive and D- swings negative, producing a positive differential voltage (for example, +300 mV). To send a logic 0, the driver reverses the current steering, producing a negative differential voltage (-300 mV). The current flows continuously; information is encoded in the direction of steering, not in the presence or absence of a signal. The differential receiver threshold sits at 0 V, the natural midpoint of this symmetric swing. Modern PAM4 transmitters replace the simple current-steering driver with a digital-to-analog converter (DAC) that produces four distinct voltage levels from a 2-bit input symbol, as described in [PAM4 Signaling and Gray Coding](../04_Equalization_and_Receiver_Architecture/15_PAM4_Signaling_and_Gray_Coding.md).

**Channel.** The differential pair (copper traces, cables, connectors, vias) carries the analog signal from transmitter to receiver. Channel loss from skin effect and dielectric absorption progressively degrades the signal, closing the eye diagram.

**Receiver (RX).** The receiver faces the inverse problem. A continuous stream of high-speed serial bits arrives with no accompanying clock signal. The receiver must recover the embedded clock, make binary decisions on each bit, and convert the serial stream back into parallel words that the digital core can process. This chain of operations proceeds through four functional stages:

1. **Clock and Data Recovery (CDR).** The first block the incoming signal encounters is the CDR, a phase-locked loop (PLL) circuit that locks onto the data transitions and generates a local clock aligned to the center of each bit period. The mechanics of the PLL, including loop bandwidth, damping, and jitter transfer, are covered in [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md).

2. **Slicer.** At each tick of the recovered clock, an analog voltage comparator (the slicer) examines the instantaneous differential voltage. If the voltage exceeds the threshold (0 V for NRZ), the slicer outputs a digital 1. If the voltage falls below the threshold, it outputs a digital 0. The slicer has no knowledge of the actual voltage magnitude. It reports only whether the signal crossed the boundary. This single-bit binary decision is the moment the analog world ends and the digital world begins.

3. **Deserializer (DEMUX).** The recovered bits arrive at the full serial line rate, far too fast for digital logic to process individually. The DEMUX acts as a gearbox: it collects bits from the slicer and distributes them across multiple parallel output lanes, stepping the clock rate down proportionally. A 112 Gbps serial stream split across 128 parallel lanes requires only an 875 MHz clock on each lane, well within the capability of standard CMOS digital logic.

4. **Word alignment.** The DEMUX produces a continuous flow of parallel bits with no inherent framing. The digital logic scans for predetermined alignment markers embedded in the data stream (comma symbols in 8b/10b-encoded protocols like early PCIe generations, or sync headers in 64b/66b-encoded protocols like 100G+ Ethernet). Once the alignment marker is found, the logic locks the byte boundaries and hands structured data to the upper protocol layers. The encoding schemes and protocol framing details are covered in [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md).

### The PMA/PCS/MAC Sublayer Hierarchy

The silicon implementing this signal path is divided into strict functional domains. When hardware engineers refer to "the receiver," they almost always mean the analog circuitry at the chip's edge: the CDR, the slicer, and the DEMUX. This collection of analog circuits constitutes the Physical Medium Attachment (PMA) sublayer. Its responsibility is limited to getting bits off the wire and handing them to the digital core. The PMA has no knowledge of Ethernet frames, PCIe transactions, or any protocol semantics.

The digital core sits behind the PMA and processes the incoming parallel data through two additional sublayers. The Physical Coding Sublayer (PCS) performs word alignment, descrambling, and forward error correction (FEC). The Media Access Control (MAC) sublayer reconstructs the actual protocol data units (Ethernet frames, PCIe packets) and hands them to the system processor. While these sublayers process the received data, they are functionally and physically distinct from the analog receiver.

The significance of this boundary is practical: when an oscilloscope or BERT probes the link, it is analyzing the analog signal feeding into the PMA. If the eye diagram shows an unrecoverable closure, the PMA slicer will pass bit errors into the PCS, and the FEC must attempt to correct them mathematically. The eye diagram measures the margin available to the analog receiver, not the end-to-end error rate after FEC correction.

### Differential Signaling and Common-Mode Rejection

High-speed serial links universally use differential signaling. The transmitter drives two complementary traces (D+ and D-) with equal and opposite voltage swings. The receiver measures only the voltage difference between them.

The reason is noise immunity. An electromagnetic interference source couples equally into both traces of a tightly routed differential pair. If a noise spike adds +100 mV to both D+ and D-, the differential voltage is unchanged:

$$(D^+ + \text{noise}) - (D^- + \text{noise}) = D^+ - D^-$$

The noise cancels completely. This property, common-mode rejection, is the only mechanism that makes reliable data transmission at 112 Gbps across a piece of fiberglass physically possible.

Both oscilloscopes and BERTs exploit this property during measurement. When two SMA cables carry D+ and D- to a scope, the instrument performs the mathematical subtraction (Channel 1 minus Channel 2) and displays the resulting clean differential waveform as the eye diagram. A BERT performs the same subtraction internally before feeding the differential signal to both its CDR (for clock recovery) and its slicer (for bit decisions).

### The Analog Front-End vs. DSP Receiver Architectures

Two fundamentally different receiver architectures exist for processing the incoming analog signal, and the distinction determines both the equalization strategy and the test methodology.

**Architecture A: Analog front-end (AFE).** The degraded differential waveform passes through continuous-time linear equalization (CTLE), enters an analog summing node where the decision feedback equalizer (DFE) subtracts its echo estimate, and the slicer makes a binary decision directly on the analog voltage. No analog-to-digital converter exists in this signal path. This architecture is used in the majority of SerDes implementations through 56 Gbps NRZ and is also the architecture inside a BERT error detector. The equalization mechanics are covered in [CTLE and DFE](../04_Equalization_and_Receiver_Architecture/14_CTLE_and_DFE.md).

**Architecture B: DSP-based receiver.** The analog waveform enters a high-speed ADC that measures the exact instantaneous voltage (for example, +212 mV) and converts it to a multi-bit digital word. A digital signal processor (DSP) then performs equalization, clock recovery, and bit-decision logic entirely in the digital domain. No analog slicer exists in this path. This architecture appears in ultra-high-speed implementations (112 Gbps PAM4 Ethernet and beyond) where the channel loss is so severe that analog equalization alone cannot open the eye sufficiently.

The critical distinction for test and measurement is that an oscilloscope operates on Architecture B principles (it uses an ADC to digitize the analog voltage and produces a visual representation of the waveform), while a BERT operates on Architecture A principles (it uses a slicer to make binary decisions and produces statistical error data). These are not interchangeable measurements. They answer fundamentally different questions about the link.

## Architecture

### Eye Diagram Construction: Three Instruments, Three Methods

The eye diagram is a composite image formed by overlaying many individual bit transitions on a common time axis. Every instrument that produces an eye diagram must solve two problems: capturing the analog voltage at a sufficient number of time-voltage coordinates, and establishing a timing reference that defines where each unit interval (UI) begins and ends. The three primary instruments solve these problems through radically different mechanisms.

**Real-time oscilloscope (RTO).** The RTO contains a massively fast ADC (for example, 256 billion samples per second on a modern Keysight UXR-Series) that digitizes the continuous analog voltage from the transmission line into an unbroken record stored in memory. Because the entire waveform is captured at once, no external clock or trigger is required to construct the eye. Instead, software algorithms implement a mathematical CDR: they analyze the stored waveform, calculate the data transition positions, determine the bit rate, and identify the clock frequency. The software then chops the continuous record into individual one-UI slices and mathematically overlays them on a common time axis. This folding operation produces the eye diagram entirely in post-processing.

The RTO display depends on how the software renders the stored data. In linear view, the captured record appears as a long trace of voltage over time. In persistence mode with the timebase set to one or two UI, the software overlays all slices and the characteristic eye shape emerges. If the timebase is zoomed out to show the entire PRBS pattern, the repeated overlay of the same pattern with slight noise and jitter variations produces a thick, glowing trace rather than a recognizable eye.

**Sampling oscilloscope (DCA).** A sampling scope builds the eye diagram dot by dot over millions of measurement cycles. Its ADC is far slower than an RTO's ADC (perhaps 1 million samples per second), but it achieves far greater analog bandwidth through an elegant trick. At the input sits an ultra-high-bandwidth analog track-and-hold circuit consisting of an electronic switch (typically a diode bridge) and a microscopic capacitor. When a hardware trigger fires, the switch closes for a few picoseconds, and the capacitor charges to the instantaneous voltage on the transmission line. The switch then snaps open, freezing the captured voltage. The slow ADC takes its time to measure the held voltage, and the scope plots exactly one dot at one (time, voltage) coordinate on the display.

The bandwidth of a sampling scope is not limited by the ADC speed. It is limited entirely by the aperture time of the analog switch. If the switch takes 10 picoseconds to open and close, and the signal being measured oscillates at 100 GHz, the voltage swings significantly during the capture window and the capacitor records a blurred average. Measuring a 100 GHz signal requires a sub-picosecond aperture, and building an analog switch with that speed is one of the most difficult challenges in test and measurement hardware.

A sampling scope cannot build an eye diagram without an external timing reference. High-speed serial links transmit no separate clock signal, so the DCA requires a hardware CDR (either built into the measurement module or provided as a standalone instrument) to extract the clock from the data stream. The data signal is split using pick-off tees (high-bandwidth microwave power splitters) or, in integrated DCA modules, tapped internally. One copy of the signal feeds the measurement channel. The other copy feeds the hardware CDR, which locks onto the data transitions and generates a physical clock signal routed to the DCA's trigger input. Each tick of that recovered clock fires the track-and-hold circuit once, capturing one dot.

**Bit Error Ratio Tester (BERT).** A BERT does not contain an ADC and does not measure analog voltage. Its "eye diagram" is constructed through a fundamentally statistical process. The BERT contains two subsystems: a pattern generator (PG) that transmits a known test pattern, and an error detector (ED) that receives data and checks it for errors. The ED uses a slicer identical in principle to the slicer inside a SerDes receiver chip: a purely analog comparator that outputs a single bit (1 or 0) based on whether the instantaneous voltage exceeds a programmable threshold.

To construct a BER contour (also called a statistical eye), the BERT sweeps its slicer across a two-dimensional grid of time delay and voltage threshold. At each grid coordinate, the BERT samples millions of bits and records the bit error ratio. At the center of the eye, where the voltage and timing margins are largest, the BER is zero. As the slicer moves toward the edges (higher voltage thresholds or earlier/later sampling instants), it begins intersecting the signal transitions and the BER increases. The BERT maps the BER at every coordinate and renders the result as a heat map. The dark, open region at the center is where errors are absent. The colored contour lines at the boundary represent specific BER thresholds (for example, $10^{-6}$, $10^{-9}$, $10^{-12}$).

A scope eye diagram shows what the signal looks like. A BERT BER contour shows how much margin a real silicon receiver has before it starts making errors. The two measurements are complementary, not redundant.

### How the BERT Error Detector Achieves Pattern Synchronization

The ED exploits the deterministic nature of PRBS (pseudo-random binary sequence) test patterns. A PRBS pattern is generated by a linear feedback shift register (LFSR) driven by a mathematical polynomial. The sequence appears random but is entirely predictable once the LFSR state is known.

The ED contains its own internal PRBS generator implementing the same polynomial. When data begins flowing, the ED examines a short segment of the incoming bitstream and uses it to synchronize its internal generator's state. Once pattern synchronization is achieved, the ED can predict every subsequent bit indefinitely. From that point, operation reduces to a simple comparison: the physical slicer output (the received bit) is compared against the mathematically predicted bit. A mismatch increments the error counter.

The ED has no concept of what voltage is arriving. It does not know whether the signal swing is 50 mV or 500 mV. The engineer configures the nominal slicer threshold (0 V for standard differential NRZ), and the slicer reports only whether the voltage is above or below that threshold at the instant the recovered clock triggers. The BER contour sweep deliberately moves this threshold away from the optimal center to map the boundaries of the eye.

### TX Testing vs. RX Testing

The physical asymmetry between the transmitter and receiver pins creates two distinct testing paradigms that require different instruments.

**Transmitter testing** uses an oscilloscope. The chip under test generates a continuous test pattern (such as PRBS-31) from its TX pins. The signal travels through the channel to the measurement point, and the scope captures the eye diagram and measures jitter, rise time, and voltage swing. The scope is a passive listener that characterizes the quality of the transmitted signal.

**Receiver testing** uses a BERT. Data does not "come out" of the RX pins. The RX pins are strictly inputs, and once a signal enters the chip, it proceeds directly into the internal analog front-end and digital core with no external observation point. Testing a receiver therefore requires stressing it to the boundaries of its specification and determining whether it can still recover data correctly.

The BERT pattern generator acts as a controlled-impairment transmitter. It injects calibrated amounts of jitter, noise, and signal attenuation to degrade the eye diagram to the exact limits specified by the protocol compliance standard. This degraded signal is driven into the chip's RX pins. Two mechanisms verify whether the receiver survived:

**Loopback mode.** The chip is placed in a special test configuration where the received bits, after passing through the RX analog front-end and digital core, are routed internally to the TX block and retransmitted. The BERT error detector receives the loopback signal and compares it against the original transmitted pattern. Any mismatch indicates that the receiver made a bit error.

**Internal error counters.** The chip's digital protocol layer is configured to expect a specific PRBS pattern. When the analog receiver passes an incorrect bit into the digital core, the logic detects the discrepancy and increments an error counter accessible through a management interface (such as a JTAG or I2C debug port). The engineer reads the accumulated error count to determine the receiver's bit error ratio under stress.

The scope tests the transmitter by listening. The BERT tests the receiver by attacking it.

## Worked Examples

### Constructing an Eye Diagram from a Linear Capture

An RTO captures a continuous 10 Gbps NRZ differential signal for 1 microsecond. At 256 GSa/s, the memory contains 256,000 voltage samples covering 10,000 bit periods.

**Step 1: Software CDR.** The instrument software analyzes the stored waveform and identifies the data transitions (rising and falling edges). From the transition positions, the software calculates the average bit period: 100 ps (corresponding to 10 Gbps).

**Step 2: Folding.** The software partitions the 1 microsecond capture into 10,000 individual slices, each exactly one UI (100 ps) wide. Every slice contains approximately 25.6 voltage samples.

**Step 3: Overlay.** All 10,000 slices are superimposed on a common 0-to-100-ps time axis. The rising edges from all slices cluster together, the falling edges cluster together, and the flat regions between transitions overlap. The characteristic diamond-shaped opening of the eye emerges from the composite overlay. Noise and jitter cause slight variations in the transition positions and settled voltage levels, which appear as thickness in the overlaid traces. A wider spread indicates more jitter or noise; a tighter bundle indicates a cleaner signal.

### BER Contour Sweep at a Single Grid Coordinate

A BERT error detector is configured to test a 28 Gbps NRZ link at one specific coordinate: a voltage threshold of +50 mV and a timing offset of +5 ps from the recovered clock edge.

**Step 1: Configuration.** The engineer programs the slicer threshold to +50 mV (above the nominal 0 V center) and adds a +5 ps delay to the sampling clock. The PRBS-31 pattern generator is running continuously.

**Step 2: Acquisition.** The ED samples 10 billion bits at this (time, voltage) coordinate and detects 3 bit errors. The BER at this coordinate is $3 \times 10^{-10}$.

**Step 3: Sweep.** The BERT increments the voltage threshold to +55 mV and repeats. Then +60 mV, +65 mV, and so on, recording the BER at each point. As the threshold approaches the signal's settled high level, the BER increases rapidly toward 0.5 (random guessing). The BERT then resets the voltage to +50 mV and sweeps the timing offset to +10 ps, +15 ps, and beyond. Over the full two-dimensional sweep, the accumulated BER values form a contour map of the eye.

**Interpreting the contour.** The open center of the eye (where BER is zero or immeasurably small) represents the margin available to the receiver. The contour line at $10^{-12}$ shows the boundary where the receiver would experience one error per trillion bits. Protocol compliance specifications typically require the eye to remain open at specific BER thresholds, and the BER contour directly measures whether that requirement is met.

## Edge Cases

### The Hardware CDR Configuration Trap

When an engineer configures a CDR loop bandwidth and peaking on a DCA or BERT, that configuration applies to the test equipment's CDR, not to the silicon chip's internal CDR. The test equipment CDR serves only to provide a timing reference for the measurement instrument. Protocol compliance standards (such as PCI-SIG or IEEE 802.3) define a mathematical "Golden PLL" with specific loop bandwidth and peaking parameters. The test equipment CDR must be configured to match the Golden PLL so that the measurement reflects what a compliant receiver would see. Misconfiguring the test equipment CDR (for example, setting the loop bandwidth too wide so that the CDR tracks jitter that a real receiver would not track) produces an artificially optimistic eye measurement that does not represent the true link margin.

### The DCA Bandwidth Bottleneck

A sampling scope's bandwidth is constrained entirely by the aperture time of its track-and-hold switch, not by the speed of its ADC. A DCA with a 70 GHz bandwidth rating and a 1 MSa/s ADC can measure signals that a 20 GHz real-time scope with a 256 GSa/s ADC cannot resolve. The bandwidth limitation is analog, not digital. As data rates push toward 112 Gbaud PAM4, the required aperture times drop below 1 picosecond, and the physical construction of analog switches fast enough to achieve these apertures represents a fundamental engineering constraint on measurement capability.

### Signal Splitting and Impedance Considerations

Splitting the data signal using pick-off tees introduces a 6 dB power loss at each split point (half the signal energy goes to each output port). On marginal links where the eye is already near closure, this additional loss can alter the measurement. Integrated DCA modules that tap the signal internally minimize this effect by using high-impedance sensing rather than resistive power splitting. When using external pick-off tees, the engineer must account for the insertion loss and verify that the splitter's bandwidth exceeds the signal bandwidth.
