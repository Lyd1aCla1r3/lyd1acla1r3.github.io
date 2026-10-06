# PAM4 Signaling and Gray Coding

<!-- SUMMARY: PAM4 encodes two digital bits into each voltage symbol by subdividing the transmitter swing into four amplitude levels, doubling the data rate at a constant symbol rate. This guide covers the signaling mechanism, the 9.5 dB SNR penalty from reduced eye height, three-threshold receiver design, and the Gray coding assignment that minimizes bit errors at adjacent voltage levels. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

Every high-speed serial link faces a physical ceiling: the analog bandwidth of the copper channel. Skin effect resistance and dielectric absorption attenuate high-frequency signal components progressively, and no amount of equalization can restore energy that has been permanently converted to heat. Raising the symbol rate to push more bits through the channel requires wider analog bandwidth, which the physical copper cannot provide at modern data rates.

PAM4 (Pulse Amplitude Modulation, 4-level) breaks through this ceiling by encoding two digital bits into a single voltage symbol. The transmitter subdivides the available voltage swing into four evenly spaced levels, each representing a unique two-bit combination. The symbol rate stays constant while the data rate doubles. A 64 Gb/s PAM4 link operates at the same 32 GBaud symbol rate, and requires the same 16 GHz analog bandwidth, as a 32 Gb/s NRZ link. The bandwidth problem is solved by packing more information into each voltage measurement rather than switching faster.

The cost is severe. Compressing four voltage levels into the same total swing that previously held two reduces each individual eye opening to one-third of the NRZ eye height, inflicting a 9.5 dB signal-to-noise ratio penalty. The receiver must evaluate the incoming waveform against three separate decision thresholds instead of one, and the voltage margin at each threshold is so small that even minor noise spikes can push the sampled voltage into the wrong level. Aggressive equalization and forward error correction become mandatory.

The mapping between voltage levels and digital bit patterns is itself a critical engineering decision. A naive sequential binary assignment places a two-bit boundary at the most noise-vulnerable threshold in the center of the signal, causing a single analog error to flip both digital bits simultaneously. Gray coding eliminates this vulnerability by constraining adjacent voltage levels to differ by exactly one bit, ensuring that the most common type of analog error produces only a single digital bit flip.

## Core Concepts

### NRZ Signaling and the Return-to-Zero Distinction

The term "non-return-to-zero" (NRZ) describes the temporal behavior of the waveform, not its physical voltage topology. Older signaling protocols used return-to-zero (RZ) encoding, which forced the voltage back to a neutral zero-volt baseline in the middle of every bit period to guarantee a clock transition. A sequence of three logic ones in an RZ scheme pulses high, drops to zero, pulses high, drops to zero, pulses high, and drops to zero.

An NRZ transmitter abandons this forced neutral state entirely. The transmitter holds the voltage at the designated logical level for the full duration of the bit period. A sequence of three logic ones produces a continuous high voltage for three complete bit times. The signal never returns to a neutral baseline between identical bits.

This design eliminates the transition overhead of RZ encoding but creates a specific timing challenge: long runs of identical bits contain no voltage transitions for the receiver to track. The clock and data recovery (CDR) circuit must infer the timing from the statistical properties of the data stream. Engineers commonly use the term "NRZ" interchangeably with "PAM2" to distinguish this two-level modulation from four-level PAM4 systems.

High-speed serial links use differential signaling. The physical link consists of two wires carrying equal and opposite voltages around a constant common-mode DC average. The common-mode voltage never swings. The receiver subtracts the negative trace from the positive trace to evaluate the differential signal, rejecting any noise that appears equally on both wires.

### Data Rate, Symbol Rate, and the Nyquist Frequency

Three distinct metrics describe the performance of a serial link, and confusing any two of them leads to incorrect bandwidth calculations.

**Data rate** measures the total number of digital bits transmitted per second. This is the throughput metric that protocols and applications consume.

**Symbol rate** (baud rate) measures the number of physical voltage changes on the wire per second. Each voltage transition constitutes one symbol. For NRZ (PAM2), one symbol carries one bit, so the data rate and symbol rate are numerically identical. For PAM4, one symbol carries two bits, so the data rate is exactly twice the symbol rate.

**Nyquist frequency** is the fundamental analog frequency of the fastest possible physical transition pattern. A continuous alternating sequence (101010 in NRZ, or cycling through all four levels in PAM4) completes one full analog cycle every two symbol periods. The Nyquist frequency is therefore exactly half the symbol rate. The physical channel must possess adequate analog bandwidth at this frequency to deliver an open eye diagram to the receiver.

A 32 Gb/s NRZ data stream switches at 32 GBaud. The Nyquist frequency is 16 GHz. Moving to 64 Gb/s PAM4 keeps the symbol rate at 32 GBaud and the Nyquist frequency at 16 GHz. The system doubles the digital throughput without demanding any additional analog bandwidth from the copper channel.

The Shannon-Hartley theorem formalizes the absolute boundary governing this tradeoff. The maximum theoretical data rate scales directly with the available analog bandwidth and logarithmically with the signal-to-noise ratio. PAM4 trades vertical voltage margin for horizontal bandwidth efficiency: the data rate doubles, but the noise tolerance drops by 9.5 dB. Modern standards such as PCIe Gen 6 and IEEE 802.3ck operate on channels that often lack sufficient analog bandwidth to perfectly preserve the Nyquist frequency even at the PAM4 symbol rate. The silicon must reconstruct the original data using complex equalization algorithms alongside forward error correction to compensate for the missing bandwidth.

### PAM4 Voltage Levels and the 9.5 dB Penalty

A perfectly linear PAM4 signal divides the maximum differential voltage swing into three equal intervals, producing four evenly spaced levels. Using the normalized representation, these levels sit at $+1$, $+1/3$, $-1/3$, and $-1$. Engineers typically refer to the four states using the integer labels $+3$, $+1$, $-1$, and $-3$ to denote their uniform spacing.

The physical voltages on the wire are much smaller than these normalized values. A typical high-speed transmitter outputs a total peak-to-peak differential swing of 800 mV. The four levels distribute as:

- Peak positive: $+400$ mV
- Inner positive: $+133$ mV
- Inner negative: $-133$ mV
- Peak negative: $-400$ mV

This four-level architecture creates three distinct vertical eye openings stacked between adjacent voltage levels, replacing the single large eye of an NRZ signal. Each individual eye spans only one-third of the total voltage swing. The reduction in vertical eye height from the full NRZ swing to one-third of that swing imposes a signal-to-noise ratio penalty of $20 \cdot \log_{10}(1/3) \approx 9.5$ dB.

The practical consequence is that the receiver must evaluate incoming voltages with three times the precision it needed for NRZ. A noise spike that would have been harmless in an NRZ system can easily push a PAM4 voltage across an adjacent threshold. The equalization chain (FFE, CTLE, DFE) must not only restore the frequency balance of the incoming waveform but must do so with enough residual voltage margin that the three compressed eyes remain open and distinguishable.

### The Triple Slicer and Thermometer Code

The receiver deploys three separate voltage slicers to evaluate the three PAM4 eyes. Each slicer is a high-speed digital comparator that outputs a pure logic 1 when the incoming analog voltage exceeds its threshold and a pure logic 0 when the voltage falls below it. No slicer produces an analog value or a fractional voltage.

The three thresholds sit at the midpoints between adjacent voltage levels:

- Top threshold: $+266$ mV (between $+400$ and $+133$ mV)
- Middle threshold: $0$ V (between $+133$ and $-133$ mV)
- Bottom threshold: $-266$ mV (between $-133$ and $-400$ mV)

The receiver reads the three binary outputs concurrently as a logic array. The digital ones fill from the bottom upward, producing a pattern known as thermometer code (analogous to mercury rising in a glass thermometer):

| Incoming Voltage | Thermometer Code (Top, Mid, Bot) | Interpretation |
|:---:|:---:|:---|
| $+400$ mV (level $+3$) | 1-1-1 | Above all three thresholds |
| $+133$ mV (level $+1$) | 0-1-1 | Below top, above middle and bottom |
| $-133$ mV (level $-1$) | 0-0-1 | Below top and middle, above bottom |
| $-400$ mV (level $-3$) | 0-0-0 | Below all three thresholds |

A hardcoded digital logic table maps these four unique thermometer arrays directly to the final two-bit data payload. The hardware extracts the voltage state and the corresponding data bits simultaneously without performing any mathematical addition or analog measurement.

### Gray Coding and the Hamming Distance Constraint

The mapping between the four thermometer codes and the two-bit data payload determines how much damage a single analog noise event inflicts on the digital data stream.

**The sequential binary vulnerability.** Standard binary counts sequentially: $00$, $01$, $10$, $11$. Mapping these values directly to the four voltage levels from bottom to top (or top to bottom) places the $01 \rightarrow 10$ boundary at the zero-volt middle threshold. This is the most noise-vulnerable location in the entire signal, where the two inner voltage levels sit closest together and thermal noise has the highest probability of pushing a sample across the threshold.

A noise spike at the zero-volt boundary causes the receiver to misidentify the inner positive level as the inner negative level (or the reverse). Under sequential binary mapping, the inner positive level decodes as $01$ and the inner negative level decodes as $10$. Both bits flip simultaneously from a single analog error. The bit error rate artificially doubles for the most common type of receiver mistake, and the resulting two-bit burst error is more difficult for FEC to correct than a single-bit error.

The direction of the sequential counting (bottom-to-top or top-to-bottom) does not eliminate this flaw. The transition between the decimal values 1 and 2 always forces the binary shift between $01$ and $10$, and aligning this two-bit boundary with the middle threshold guarantees double-bit errors at the most vulnerable location regardless of which end of the voltage scale starts at $00$.

**The Gray code solution.** Gray code is a binary sequence constructed so that every adjacent pair of values differs in exactly one bit position. This property is described formally as a Hamming distance of 1 between all neighboring entries. The standard PAM4 Gray code mapping assigns:

| Voltage Level | Thermometer Code | Gray Code Payload |
|:---:|:---:|:---:|
| $+400$ mV ($+3$) | 1-1-1 | 1-0 |
| $+133$ mV ($+1$) | 0-1-1 | 1-1 |
| $-133$ mV ($-1$) | 0-0-1 | 0-1 |
| $-400$ mV ($-3$) | 0-0-0 | 0-0 |

A noise spike at the zero-volt threshold now causes the receiver to misread $11$ as $01$ (or the reverse). Only a single digital bit changes. The FEC algorithm handles single-bit errors routinely, while multi-bit cascade errors often overwhelm the mathematical parity checks and cause dropped packets. Every adjacent-level error at every threshold in the PAM4 signal produces at most one bit flip under Gray coding.

## Worked Examples

### Noise Spike at the Zero-Volt Threshold

An incoming signal at the inner positive level should arrive at $+133$ mV. A negative thermal noise spike of 150 mV hits at the exact sampling instant, dragging the sampled voltage to $-17$ mV. The receiver sees a voltage below the zero-volt middle threshold and categorizes it as the inner negative level.

**Under sequential binary mapping:** The inner positive level decodes as $01$. The inner negative level decodes as $10$. Both the left bit and the right bit flipped. One analog mistake produced two digital errors.

**Under Gray code mapping:** The inner positive level decodes as $11$. The inner negative level decodes as $01$. The left bit flipped from 1 to 0. The right bit remained 1. One analog mistake produced exactly one digital error.

The physical noise event was identical in both scenarios. The encoding scheme determined whether that single analog mistake propagated into one digital error or two.

### NRZ vs. PAM4 Bandwidth Calculation

A system architect needs to transport 64 Gb/s of data through a copper channel whose insertion loss profile supports adequate signal quality up to approximately 16 GHz.

**NRZ approach:** At one bit per symbol, 64 Gb/s requires 64 GBaud. The Nyquist frequency is 32 GHz. The channel cannot support this bandwidth. The link fails.

**PAM4 approach:** At two bits per symbol, 64 Gb/s requires only 32 GBaud. The Nyquist frequency is 16 GHz. The channel supports this bandwidth. The link is physically viable, but the 9.5 dB SNR penalty requires aggressive equalization and FEC to achieve acceptable error rates.

This calculation is the fundamental engineering motivation behind the industry transition from NRZ to PAM4 at data rates above approximately 56 Gb/s per lane.

## Architecture

### Gray Code Hardware Implementation

The conversion from a three-bit thermometer array to a two-bit Gray code payload is implemented in physical silicon using combinatorial logic gates. The IEEE standards for high-speed Ethernet and PCIe dictate the specific truth table to guarantee uniform Gray coding across the industry.

The mapping yields a remarkably efficient hardware realization. Examining the truth table reveals that the first data bit equals 1 for the top two voltage levels and 0 for the bottom two levels. The middle slicer output exhibits exactly this behavior: it outputs 1 whenever the voltage exceeds zero and 0 whenever the voltage falls below zero. The hardware simply wires the middle slicer output directly to the first data bit. No logic gates are required.

The second data bit equals 0 for the peak positive level, 1 for both inner levels, and 0 for the peak negative level. This pattern matches the output of an exclusive-OR (XOR) gate fed by the top and bottom slicers. The XOR gate outputs 1 when its two inputs differ and 0 when they match:

- Peak positive ($+3$): Top slicer = 1, Bottom slicer = 1. Inputs match. XOR output = 0.
- Inner positive ($+1$): Top slicer = 0, Bottom slicer = 1. Inputs differ. XOR output = 1.
- Inner negative ($-1$): Top slicer = 0, Bottom slicer = 1. Inputs differ. XOR output = 1.
- Peak negative ($-3$): Top slicer = 0, Bottom slicer = 0. Inputs match. XOR output = 0.

The entire Gray code decoder consists of a single direct wire and a single XOR gate. The protocol committee chose this specific truth table assignment, and the silicon engineer discovered that the assignment translates into the simplest possible physical circuit. The conversion executes instantaneously with negligible propagation delay and zero power overhead beyond the gate itself.

### The Equalization Mandate

The 9.5 dB SNR penalty transforms the equalization chain from a performance optimization into an absolute necessity. An NRZ receiver with a full-height eye opening can tolerate moderate residual ISI and still make correct decisions. A PAM4 receiver with one-third the vertical margin cannot.

The transmitter FFE must pre-compensate for channel loss with greater precision, because any residual loss that closes the already-compressed eyes risks merging adjacent voltage levels into an indistinguishable blur. The receiver CTLE must amplify the high-frequency edge content without amplifying noise into the narrow voltage margins. The DFE must cancel ISI echoes that would be tolerable in NRZ but are catastrophic when the decision boundaries are spaced only 266 mV apart.

Forward error correction provides the final safety net. At PAM4 data rates, the raw bit error rate after equalization is typically orders of magnitude worse than what the application layer requires. The FEC encoder adds mathematical redundancy (typically Reed-Solomon codes) that allows the receiver to detect and correct a bounded number of bit errors per block. The combination of equalization and FEC operates as a system: equalization reduces the raw BER to a level the FEC can handle, and FEC closes the remaining gap to the application's target error rate.

## Edge Cases

### The Zero-Volt Threshold as the Dominant Error Source

The three PAM4 decision thresholds do not contribute equally to the total bit error rate. The middle threshold at zero volts separates the two inner voltage levels ($+133$ mV and $-133$ mV), which are spaced only 266 mV apart. The upper and lower thresholds each separate an inner level from a peak level ($+133$ to $+400$ mV, or $-133$ to $-400$ mV), with 534 mV of spacing.

The inner levels are twice as close to each other as they are to the outer levels. Thermal noise and residual ISI are far more likely to push a sample across the tightly spaced middle boundary than across either of the wider outer boundaries. The zero-volt threshold dominates the error statistics, which is precisely why Gray coding's protection at this boundary is so critical.

### CDR Challenges with PAM4

The clock and data recovery circuit in a PAM4 receiver must extract timing information from a signal with three stacked eyes rather than one. The transition density visible to the CDR depends on which voltage levels are transitioning. A transition between the two inner levels ($+1$ to $-1$) crosses the zero-volt threshold cleanly. A transition between an inner level and the adjacent peak level ($+1$ to $+3$) never crosses zero at all.

The CDR must track transitions across all three eyes simultaneously, and the timing extraction algorithms are more complex than their NRZ counterparts. The reduced voltage margin at each eye also means that the timing uncertainty (jitter) of the recovered clock is larger for PAM4 than for NRZ at the same symbol rate, further tightening the system's jitter budget.
