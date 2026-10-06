# Line Coding, FEC, and Protocol Framing

<!-- SUMMARY: Between the physical voltage transitions on the wire and the usable data that reaches the processor sit three operations: line coding (DC balance and run length control), forward error correction (mathematical redundancy for error repair without retransmission), and protocol framing (structural markers for byte and packet boundaries). This guide traces the evolution from 8b/10b through 128b/130b to RS-FEC and explains the critical distinction between transfer rate (GT/s) and data rate (Gb/s). -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

A serial link is more than an analog channel. Between the physical voltage transitions on the wire and the usable data that reaches the processor sits a set of encoding, error correction, and framing operations that collectively transform raw bits into a reliable digital transport. Line coding guarantees the electrical properties the analog channel requires: DC balance to prevent baseline wander across AC coupling capacitors, bounded run length to maintain the transition density that clock and data recovery circuits depend on, and a controlled frequency spectrum that keeps energy within the channel's passband. Forward error correction injects mathematical redundancy that allows the receiver to detect and repair bit errors without retransmission, relaxing the analog margin requirements that would otherwise be physically impossible to meet at extreme data rates. Protocol framing provides the structural markers that allow the receiver to identify where bytes begin, distinguish data from control information, and hand complete packets to the upper layers of the protocol stack.

These operations also determine the relationship between two quantities that high-speed engineers must never conflate: the transfer rate (the physical signaling speed on the wire, measured in GT/s) and the data rate (the usable throughput after encoding overhead is removed, measured in Gb/s). Every measurement setup, from oscilloscope trigger configuration to BERT pattern generation, depends on this distinction.

## Core Concepts

### Transfer Rate, Data Rate, and Encoding Overhead

The transfer rate specifies the number of physical symbols transmitted per second, independent of what those symbols contain. The unit is transfers per second (T/s), typically expressed as gigatransfers per second (GT/s). The transfer rate is what the oscilloscope sees, what the transmission line carries, and what the Unit Interval (UI) is derived from:

$$\text{UI} = \frac{1}{\text{Transfer Rate}}$$

A 3.2 GT/s signal has a UI of exactly 312.5 picoseconds. The oscilloscope triggers and recovers the clock based on those transfers regardless of what the bits represent.

The data rate describes the usable throughput after encoding overhead is subtracted. PCIe Gen 1 runs at 2.5 GT/s, but the link uses 8b/10b encoding: for every 8 bits of actual data, 10 bits are transmitted on the wire. The raw transfer rate is 2.5 billion symbols per second, but the data throughput is only 2.0 Gb/s ($2.5 \times 8/10$). The two extra bits per symbol carry no user data. They exist solely to maintain DC balance and transition density.

The distinction matters for signal integrity measurement. The analog channel and physical layer test equipment do not differentiate between payload bits and overhead bits. Every symbol must survive the channel with adequate margin. Signal integrity engineers measure in GT/s because they are characterizing the physical transport, not the protocol throughput.

### Line Coding for DC Balance and Transition Density

AC coupling capacitors sit in series on the data path in PCIe, Ethernet, USB, and virtually every modern serial link. A capacitor blocks DC and passes AC. If the data stream contains a long unbroken run of identical bits, the capacitor sees what appears to be a static voltage and begins to charge, causing the baseline voltage at the receiver to drift. This baseline wander shifts the signal away from the decision threshold and causes bit errors. The physics of AC coupling and baseline wander are covered in [CTLE and DFE](../04_Equalization_and_Receiver_Architecture/14_CTLE_and_DFE.md).

Line coding prevents this failure by guaranteeing an approximately equal density of ones and zeros over time.

**8b/10b encoding.** Used by PCIe Gen 1 and Gen 2, Gigabit Ethernet, SATA, SAS, Fibre Channel, and USB 3.0. The encoder maps every 8-bit data byte to a 10-bit symbol selected from a lookup table. The table is constructed so that each 10-bit symbol contains either an equal number of ones and zeros (five of each) or at most one extra bit of either polarity. The encoder tracks a running disparity counter that records whether the cumulative transmitted bit stream has sent more ones or more zeros. If the running disparity is positive (more ones have been sent), the encoder selects the symbol variant that contains more zeros, and vice versa. This feedback mechanism keeps the long-term DC content of the signal at zero, holding the AC coupling capacitors at their neutral charge state.

The encoding also enforces a maximum run length of five identical consecutive bits. This bounded run length ensures that voltage transitions occur frequently enough for the CDR to maintain phase lock. The overhead cost is 20%: two out of every ten transmitted bits carry no user data.

**128b/130b encoding.** Used by PCIe Gen 3 and later. The encoder groups 128 data bits into a block and prepends a 2-bit sync header. The sync header is always either `01` or `10`, guaranteeing at least one transition at every block boundary. The 128-bit payload is scrambled using a linear feedback shift register (LFSR) that produces a pseudo-random bit pattern with statistically balanced ones and zeros. The overhead drops from 20% (8b/10b) to approximately 1.6% ($2/130$), a massive efficiency improvement. The tradeoff is that scrambling provides statistical DC balance rather than the deterministic per-symbol guarantee of 8b/10b. Over any sufficiently long window, the scrambled stream converges to equal density, but short-term deviations are possible.

**64b/66b encoding.** Used by 10G+ Ethernet (IEEE 802.3). Structurally identical in principle to 128b/130b: a 2-bit sync header followed by a scrambled payload block. The sync header values (`01` for data blocks, `10` for control blocks) provide both framing and transition density at the block boundary.

### Embedded Clocks vs. Forwarded Clocks

High-speed serial links (PCIe, Ethernet, USB) transmit no separate clock signal. The clock is embedded in the data transitions. The receiver uses a CDR circuit to extract timing information from the voltage edges and generate a local sampling clock. The mechanics of CDR, including PLL loop bandwidth, damping, peaking, and jitter transfer, are covered in [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md).

The absence of a physical clock wire eliminates the term "clock cycle" from the serial link vocabulary. Hardware engineers instead use the term symbol (or Unit Interval). For NRZ signaling, one symbol carries one bit. For PAM4, one symbol carries two bits. The relationship between symbol rate, Nyquist frequency, and multi-level modulation is covered in [PAM4 Signaling and Gray Coding](../04_Equalization_and_Receiver_Architecture/15_PAM4_Signaling_and_Gray_Coding.md).

If the baud rate is 32 GT/s (32 billion symbols per second), the Nyquist frequency is exactly half: 16 GHz, because the fastest possible toggle pattern (101010...) takes two symbols to complete one full wave. For NRZ at 32 GT/s, that 16 GHz channel carries 32 Gb/s. For PAM4 at 32 GT/s, the same 16 GHz channel carries 64 Gb/s because each symbol encodes two bits.

**DDR memory uses the opposite architecture.** DDR is a parallel bus with a dedicated physical clock wire (CK) running alongside the data wires (DQ). The clock wire transmits a continuous, perfect alternating pattern. The data wires carry standard NRZ data. "Double Data Rate" means the memory controller outputs a new NRZ data symbol on each rising edge and each falling edge of the clock, achieving two transfers per clock cycle:

$$1.6 \text{ GHz clock} \times 2 \text{ edges} = 3.2 \text{ GT/s}$$

The Nyquist frequency of the data wires is half the transfer rate: 1.6 GHz. The physical clock frequency is also 1.6 GHz. These two values align exactly because one full clock cycle (rising edge plus falling edge) triggers exactly two data transfers.

Total bandwidth for a DDR channel uses the bus width. A standard non-ECC DDR4 channel is 64 bits wide:

$$3.2 \text{ GT/s} \times 64 \text{ bits} = 204.8 \text{ Gb/s} \quad (25.6 \text{ GB/s})$$

The forwarded-clock architecture avoids the complexity of CDR entirely. The receiver does not need to extract timing from data transitions because it receives an explicit clock reference. The cost is the dedicated clock wire, the strict trace-length matching required to keep the clock and data signals phase-aligned across the PCB, and the physical limitation that skew control becomes impractical as frequencies increase. This is why the highest-speed interfaces (PCIe Gen 5/6, 100G+ Ethernet) are all serial with embedded clocking.

## Architecture

### Protocol Stack Processing

Once the analog front end has made its bit decisions and the DEMUX has spread the serial stream into parallel lanes at a slower clock speed, the data enters the digital protocol stack. Processing proceeds through three stages:

**Word alignment.** The parallel lanes arrive as an undifferentiated stream of bits with no inherent framing. Digital logic scans for predetermined alignment markers: comma symbols (specific reserved 10-bit patterns) in 8b/10b-encoded protocols, or sync headers (`01`/`10`) in 64b/66b and 128b/130b-encoded protocols. Once the alignment marker is found, the logic locks the byte or block boundaries and establishes the framing that all subsequent processing depends on.

**Descrambling and decoding.** For 8b/10b protocols, the decoder reverses the lookup table, converting each 10-bit symbol back to its 8-bit data value and stripping the encoding overhead. For 128b/130b and 64b/66b protocols, the descrambler reverses the LFSR transformation to recover the original data. The transmitter scrambles data to prevent long runs of identical bits that would compromise CDR lock and AC coupling stability. The receiver must precisely reverse this operation.

**Forward error correction.** At 100G+ data rates, the raw bit error rate after analog equalization frequently exceeds the target (for example, $10^{-12}$). FEC provides a mathematical safety net that corrects residual errors, including burst errors caused by DFE error propagation or transient noise events.

The Physical Coding Sublayer (PCS) performs word alignment, descrambling, and FEC. The Media Access Control (MAC) sublayer reconstructs the actual protocol data units (Ethernet frames, PCIe packets) and hands them to the system processor. The complete PMA-PCS-MAC sublayer hierarchy and the distinction between analog eye measurement and post-FEC error rate are covered in [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md).

### CRC: Error Detection by Polynomial Division

Cyclic Redundancy Check (CRC) provides error detection at the frame level. The mathematical mechanism exploits a property of modulo-2 polynomial arithmetic.

The transmitter treats the data payload as a binary polynomial and divides it by a standardized generator polynomial. The division uses modulo-2 arithmetic, where addition and subtraction are both identical to the XOR operation. The transmitter appends the remainder of this division (the CRC bits) to the end of the payload before transmission.

Appending the exact remainder to the original data forces the entire newly formed package to become a perfect multiple of the generator polynomial. The mathematical principle is identical to base-10 arithmetic: dividing 17 by 5 yields a remainder of 2; subtracting that remainder produces 15, which is perfectly divisible by 5. In modulo-2 arithmetic, subtraction and addition are the same operation (XOR), so appending the remainder is mathematically equivalent to subtracting it.

The receiver divides the entire received package (data plus appended CRC bits) by the same generator polynomial. Dividing a perfect multiple by its generator mathematically guarantees a remainder of exactly zero. A non-zero remainder proves that at least one bit flipped during transmission.

CRC detects errors but cannot locate or correct them. When the CRC check fails, the protocol must request retransmission (as in TCP/IP error recovery) or rely on FEC to have already corrected the error at a lower layer.

### FEC: Error Correction by Reed-Solomon Coding

Forward error correction extends the polynomial mathematics of CRC from detection to actual correction. The most common algorithm in high-speed protocols (Ethernet IEEE 802.3, PCIe Gen 6) is Reed-Solomon coding.

The transmitter groups incoming data bits into discrete blocks and treats each block as a single algebraic polynomial. It divides this polynomial by a standardized generator polynomial and appends the parity bits (the mathematical remainder) to the block. The structure parallels CRC, but the generator polynomial and field arithmetic are chosen so that the remainder carries enough information to locate and repair errors, not merely detect them.

The receiver divides the entire received block (data plus parity) by the same generator polynomial. A remainder of zero confirms error-free transmission. A non-zero remainder is called the syndrome. The syndrome is not merely a flag; its specific numerical value acts as a coordinate map that identifies the exact positions of the corrupted bits within the block and their correct values. The receiver hardware inverts the corrupted bits on the fly, eliminating the latency penalty of halting the link to request retransmission.

Every Reed-Solomon code has a strict mathematical limit on how many symbol errors it can correct per block. A parameter $t$ defines this limit: the code can correct up to $t$ symbol errors per codeword. If a burst of errors exceeds $t$, the block is uncorrectable.

**Interleaving.** Physical noise bursts on a serial link tend to corrupt consecutive symbols. A localized noise event might flip 10 adjacent bits, exceeding the correction capability of a single FEC block. Interleaving defeats this failure mode. The transmitter distributes consecutive data symbols sequentially across several independent FEC blocks before transmission. A localized burst then affects only a few scattered symbols in each block rather than concentrating all errors in one. Each block easily repairs its few distributed errors within the mathematical correction limit.

## Worked Examples

### PCIe Encoding Overhead Across Generations

PCIe Gen 1 runs at 2.5 GT/s with 8b/10b encoding. The data throughput is:

$$2.5 \text{ GT/s} \times \frac{8}{10} = 2.0 \text{ Gb/s per lane}$$

PCIe Gen 3 runs at 8.0 GT/s with 128b/130b encoding. The data throughput is:

$$8.0 \text{ GT/s} \times \frac{128}{130} \approx 7.877 \text{ Gb/s per lane}$$

The encoding overhead dropped from 20% to 1.5%, and the transfer rate increased by a factor of 3.2. The combined effect is a nearly four-fold increase in per-lane data throughput.

### UI Calculation for DDR4-3200

DDR4-3200 operates at 3.2 GT/s (3.2 billion transfers per second). The Unit Interval is:

$$\text{UI} = \frac{1}{3.2 \times 10^9} = 312.5 \text{ ps}$$

The physical clock frequency is 1.6 GHz (half the transfer rate, because each clock cycle triggers two transfers). An oscilloscope measuring jitter or drawing an eye diagram on the DQ data wire uses 312.5 ps as the UI for time-base alignment.

### CRC Verification

A transmitter sends a data payload treated as polynomial $D(x)$ and divides by generator $G(x)$, obtaining remainder $R(x)$. The transmitted package is $D(x) \cdot x^r + R(x)$, where $r$ is the degree of the generator (the number of CRC bits). The receiver divides the entire received package by $G(x)$:

$$\frac{D(x) \cdot x^r + R(x)}{G(x)}$$

The first term $D(x) \cdot x^r / G(x)$ produces quotient $Q(x)$ with remainder $R(x)$. Adding $R(x)$ to $R(x)$ in modulo-2 arithmetic yields zero (any value XORed with itself is zero). The receiver obtains a remainder of exactly zero, confirming no bit errors.

## Edge Cases

### Running Disparity and Special Symbols in 8b/10b

The 8b/10b code table contains two variants (positive and negative disparity) for most data symbols. The encoder selects the variant that steers the cumulative DC balance toward zero. Some symbols have only one variant and are inherently disparity-neutral. The code also reserves specific patterns as control symbols (K-codes) that can never appear in valid encoded data. These K-codes serve as unambiguous markers for comma detection, ordered set signaling, and link training. Their uniqueness within the code space is what makes reliable word alignment possible even in a continuous, unsynchronized bit stream.

### Scrambling vs. Deterministic Encoding

8b/10b encoding provides a deterministic, per-symbol guarantee of DC balance and bounded run length. Every transmitted symbol is individually constrained. 128b/130b and 64b/66b encoding rely on scrambling, which provides statistical balance: over any sufficiently long window, the density of ones and zeros converges to 50%, but short sequences within the stream can be temporarily unbalanced. The LFSR scrambler is designed so that pathological input patterns (such as all zeros or all ones) still produce output with adequate transition density. The 2-bit sync header at every block boundary provides a guaranteed transition regardless of the scrambled payload content, ensuring the CDR always receives periodic edges.

### FEC Correction Threshold and Residual Errors

An FEC code with correction capability $t$ can repair up to $t$ symbol errors per codeword. If the raw error rate is high enough that bursts occasionally exceed $t$ (even after interleaving), those blocks are uncorrectable and produce post-FEC errors. Protocol specifications define target post-FEC bit error rates (typically $10^{-15}$ or better) and select FEC parameters ($t$, block size, interleaving depth) to achieve that target given the expected pre-FEC raw error rate from the analog channel. The pre-FEC BER floor and the FEC correction threshold together determine the minimum analog eye opening that the equalization chain must achieve.
