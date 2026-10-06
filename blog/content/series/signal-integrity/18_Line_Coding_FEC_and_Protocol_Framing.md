# Line Coding, FEC, and Protocol Framing

<!-- SUMMARY: The recovered clock and the slicer decisions of the previous chapters deliver a stream of bits that carries no structure, and three operations turn it into data. Line coding and scrambling bound the run length and the running disparity that the clock recovery loop and the coupling capacitor require, and this guide derives why 10 bits cannot hold a balanced 8-bit code, how running disparity stays at plus or minus one, how a self-synchronous scrambler works and why it multiplies errors by three, and why the sync header of 64b/66b and 128b/130b bounds the run length to 66 and 130 bits. Error detection and correction follow, with the CRC derived as polynomial division and the Reed-Solomon code derived from polynomial evaluation, which gives the minimum distance $n - k + 1$ and the correction capability $t = (n - k)/2$. The chapter then places the operations in the sublayer stack (PMA, PCS, MAC), explains word alignment, interleaving and clock compensation, and shows with numbers why a cycle slip cannot be repaired by the code. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) ended with a receiver that holds a recovered clock and a stream of slicer decisions, and with two requests of the data: the stream must contain transitions often enough for the loop to hold its phase, and the receiver must be able to find the word boundary again after a cycle slip. This chapter shows how the transmitter satisfies the first request and how the receiver satisfies the second. The decided bits are still not data. They have no word boundaries, they may contain a few errors, and they may be shifted by a bit relative to the transmitted stream, and three operations remove these problems before a processor sees a byte.

**Line coding** and **scrambling** shape the bit stream so that its run length and its running disparity stay bounded. **Error detection and correction** add redundancy that lets the receiver find a bit error and, for a correcting code, repair it without a retransmission. **Framing** places markers in the stream so that the receiver can find the boundaries of words, blocks, and lanes. The three operations also create the distinction between the rate at which symbols cross the channel and the rate at which user data arrives, a distinction that every measurement setup depends on, and the chapter begins with it.

## Core Concepts

### Data Rate, Transfer Rate, Symbol Rate, and Code Rate

[PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md) separates the data rate $R_b$ (bits per second delivered by the protocol) from the symbol rate $R_s$ (voltage symbols per second on the wire). A line code adds a third quantity. The **code rate** $k/n$ is the number of data bits $k$ in a block divided by the number of transmitted bits $n$ that carry them, and the rate on the wire is larger than the data rate by the factor $n/k$:

$$R_{line} = R_{data}\,\frac{n}{k}$$

The unit interval of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md) follows from the line rate and not from the data rate. The **transfer rate** in transfers per second (T/s) counts the symbols that cross the channel, so for NRZ it equals the line rate in bits per second and the symbol rate in baud, and for PAM4 the symbol rate in baud is half the line rate in bits per second. A PCIe lane at 8 GT/s sends 8 billion symbols per second, each of which carries one bit, and its unit interval is $1/(8\times 10^9) = 125$ ps. The oscilloscope, the transmission line, and the receiver circuits see only the line rate. They cannot distinguish a payload bit from a bit that a code added, so every transmitted symbol must survive the channel with the margin that the earlier chapters derived.

The data rate $R_{data} = R_{line}\,k/n$ is the quantity that the user sees, and the two numbers differ by the code overhead. The overhead has two common definitions that give different numbers for the same code. The fraction of the transmitted bits that carry no data is $(n-k)/n$, and the extra bandwidth relative to the payload is $(n-k)/k$. For 8b/10b these are 20 percent and 25 percent, and for 128b/130b they are $2/130 = 1.54$ percent and $2/128 = 1.56$ percent. This chapter quotes the first definition unless it says otherwise, and the 1.54 percent value replaces the two inconsistent figures (1.6 and 1.5 percent) that appear in many descriptions of 128b/130b.

### What the Channel Requires of the Bit Stream

Two earlier chapters set quantitative requirements on the stream, and a code is judged by how it meets them.

The first requirement is a bounded **run length**. [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) shows that a loop without transitions runs on its stored frequency, so that a residual error of $\epsilon = 200$ ppm moves the phase by $\epsilon N$ unit intervals during a run of $N$ identical bits. The drift of 0.001 UI over 5 bits and 0.0132 UI over 66 bits is small against the unit interval, because a full unit interval needs $1/\epsilon = 5{,}000$ bits without a transition, and the run length limits that the codes below achieve (5 and 66 bits) stay far below that number.

The second requirement is a bounded **running disparity**. [Return Path Dynamics and Parasitic Effects](06_Return_Path_Dynamics_and_Parasitic_Effects.md) derives that a series coupling capacitor with time constant $\tau$ develops the voltage $v_C = A\,D\,T_{UI}/\tau$, where $A$ is the signal amplitude, $T_{UI}$ is the unit interval and $D$ is the running disparity, the number of ones minus the number of zeros transmitted over the memory of the capacitor. A code that keeps $|D| \le D_{max}$ limits the baseline wander to $A\,D_{max}\,T_{UI}/\tau$.

A third requirement is implicit in the first two. The spectrum of the stream should contain little energy near DC, where the coupling capacitor removes it, and the transition density should stay close to one half so that the loop gain of the phase detector ($K_{pd}$ is proportional to the transition density $\eta_T$ in Chapter 17) stays predictable. Every code below is a way to obtain these properties at the lowest cost in line rate.

### 8b/10b: A Deterministic Code

A counting argument shows why a balanced code needs more than 10 bits for 8 data bits. A code word with zero disparity has five ones and five zeros, and there are $\binom{10}{5} = 252$ such words. There are 256 different data bytes, so even a map that used every balanced word could not cover them, and a code that gives every byte a word of zero disparity does not exist at 10 bits. The code must also use words with six ones and four zeros, of which there are $\binom{10}{6} = 210$, and the equal number of words with four ones and six zeros. A word with an unequal number of ones and zeros has a **disparity** of $+2$ or $-2$ (the number of ones minus the number of zeros). The code therefore needs two variants for many bytes, one with disparity $+2$ and one with $-2$, and the transmitter has to choose between them.

The choice follows the **running disparity** (RD), the cumulative number of ones minus zeros that the transmitter has sent up to the end of the previous symbol. The rule has two cases, and these two cases determine the whole behavior of the code:

1. At a running disparity of $-1$, the transmitter selects a symbol of disparity 0 or $+2$. The running disparity after the symbol is $-1$ for disparity 0 and $+1$ for disparity $+2$.
2. At a running disparity of $+1$, the transmitter selects a symbol of disparity 0 or $-2$. The running disparity after the symbol is $+1$ for disparity 0 and $-1$ for disparity $-2$.

The rule starts from $-1$ by convention. By induction the running disparity at every symbol boundary is $-1$ or $+1$, because each case ends in one of those two values, and the number of ones in any stretch of whole symbols differs from the number of zeros by at most 2. The symbol disparity of a valid word is $0$, $+2$, or $-2$ (the disparity $\pm 1$ appears only as the *running* value, and the older statement that a symbol holds at most one extra bit is wrong, because six ones and four zeros differ by two). Inside a symbol the running count can depart from its boundary value by at most the length of the symbol, so $|D| \le 11$ bits is a safe bound for every point of the stream.

The practical code is built from two sub-blocks, a 5b/6b code for the five low-order bits and a 3b/4b code for the three high-order bits, because the two small tables are much simpler than one table of 256 entries. The 6-bit sub-block has $\binom{6}{3} = 20$ balanced words and $\binom{6}{4} = 15$ words of disparity $+2$, and the 4-bit sub-block has $\binom{4}{2} = 6$ balanced words and $\binom{4}{3} = 4$ words of disparity $+2$. The tables are designed so that a symbol never has the disparity $\pm 4$ that two sub-blocks of the same sign would give, and so that the longest run of identical bits, within a symbol and across a symbol boundary, is five. These two properties are facts of the table (Tier 2: the tables are not reproduced here), and they are the run length and disparity limits that the rest of the book quotes. The cost is 20 percent of the line rate.

8b/10b has a second use that a scrambler cannot provide. The 10-bit space contains words that carry no data byte, and the code reserves some of them as **control symbols** (K-codes). The most important control symbol, the comma, contains the seven-bit sequence 0011111 or 1100000. The table is constructed so that this sequence, with its run of five identical bits, never appears across the boundary of any valid data symbols, and the receiver can therefore find the symbol boundary by searching for it (see Word Alignment below).

### Scrambling and the 64b/66b and 128b/130b Block Codes

A table code costs 20 percent of the line rate, and the cost is too high at 25 Gb/s and above. The alternative is to leave the payload unchanged in meaning but to transform it with a **scrambler**, a deterministic operation that makes the stream statistically similar to random data, and to add only a short header that carries the framing. The 64b/66b code of Ethernet places a 2-bit **sync header** (01 for a data block, 10 for a control block) in front of 64 payload bits, and the 128b/130b code of PCIe Gen 3 and later places a 2-bit header (01 or 10) in front of 128 payload bits. The headers are not scrambled, and the code rates are $64/66 = 96.97$ percent and $128/130 = 98.46$ percent, and the overheads are 3.03 percent and 1.54 percent of the line rate.

The scrambler of 64b/66b is **self-synchronous**, which means that the transmitter forms each output bit $y_n$ from the input bit $x_n$ and two earlier output bits,

$$y_n = x_n \oplus y_{n-39} \oplus y_{n-58}, \qquad \text{that is,} \qquad Y(x) = \frac{X(x)}{G(x)}, \quad G(x) = 1 + x^{39} + x^{58}$$

where $\oplus$ is the exclusive-or, the sum without carry that the CRC section below defines, and the polynomial form writes each bit stream as a polynomial in a delay variable $x$ (a bit delayed by $m$ positions is multiplied by $x^m$). The receiver applies the inverse operation and obtains

$$x_n = y_n \oplus y_{n-39} \oplus y_{n-58}, \qquad X(x) = Y(x)\,G(x)$$

and the two operations are inverse to each other, because $X = Y G = X G/G = X$. Two consequences follow directly from the structure.

The first consequence is **self-synchronization**, which follows from the fact that the descrambler output depends only on the last 58 received bits, so it recovers the correct data 58 bits after it starts, whatever state its delay line held at the start. A simulation of a random stream with a wrong initial state shows 27 of the first 58 bits in error and none after bit 58. No reset signal or seed exchange is needed.

The second consequence is **error multiplication**, and it follows from the same structure. Assume that the channel flips one bit of the stream, so that the received stream is $Y(x) + x^m$. The descrambler output is $(Y + x^m)G = X + x^m G(x) = X + x^m + x^{m+39} + x^{m+58}$, which differs from the transmitted data in three positions, spaced 39 and 58 bits from the first. The simulation confirms the positions 500, 539 and 558 for a flip at bit 500. The number of errors after descrambling is equal to the number of non-zero terms of $G(x)$, so a scrambled link multiplies the bit error ratio by up to three for isolated errors. The multiplication affects the choice of the order of operations, as the architecture section shows.

The transition density of a scrambled stream is a statistical statement. For independent random bits the probability that a given position starts a run of at least $L$ identical bits (preceded by a transition) is $\tfrac12 \cdot 2^{-(L-1)} = 2^{-L}$, so such a run occurs on average once in $2^L$ bits. At 16 Gb/s a run of 40 bits occurs once every 69 s, a run of 50 bits once every 19.5 hours, and a run of 64 bits once every $1.15 \times 10^9$ s, which is 36.6 years. The probability of a long run falls with the factor 2 per added bit, and the payload alone cannot be called a deterministic bound.

The header supplies the deterministic bound, because it never equals 00 or 11 and so holds a transition inside every block, and a run of identical bits cannot extend beyond the blocks around it. The worst case for 64b/66b is a header ending in 1, a payload of 64 ones, and a following header that starts with 1: the run is $1 + 64 + 1 = 66$ bits and ends at the next 0. The same argument gives $1 + 128 + 1 = 130$ bits for 128b/130b. These are the limits of 66 and 130 bits that Chapter 6 and Chapter 17 use, and they are the exact worst cases, not typical values.

### Error Detection: CRC as Polynomial Division

A **cyclic redundancy check** (CRC) detects errors at the level of a frame. The transmitter writes the $k$ data bits as a binary polynomial $D(x)$, multiplies it by $x^r$ (which appends $r$ zeros), and divides the result by a fixed **generator polynomial** $G(x)$ of degree $r$. The division uses arithmetic modulo 2, in which addition and subtraction are both the exclusive-or and there is no carry. The division gives a quotient $Q(x)$ and a remainder $R(x)$ of degree below $r$:

$$D(x)\,x^r = Q(x)\,G(x) + R(x)$$

The transmitter sends the $k + r$ bits of $C(x) = D(x)\,x^r + R(x)$. Addition is the exclusive-or, so $R + R = 0$ and $C(x) = Q(x)\,G(x) + R(x) + R(x) = Q(x)\,G(x)$. Every valid codeword is therefore a multiple of $G(x)$, and the receiver divides the received polynomial by $G(x)$ and accepts the frame when the remainder is zero.

The detection capability follows from the same algebra. Assume that the channel adds an error pattern $E(x)$, so that the received polynomial is $C(x) + E(x)$. The remainder of the received frame equals the remainder of $E(x)$, since $C$ leaves none. An error escapes detection only when $G(x)$ divides $E(x)$. Three properties follow:

- **Single-bit errors:** the error $E = x^i$ is not divisible by a generator that has a constant term 1 and at least one other term, so every single-bit error is detected.
- **Bursts up to $r$ bits:** a burst has the form $E = x^i B(x)$ with $B$ of degree below $r$. The generator does not divide $x^i$ (its constant term is 1) and cannot divide $B$ (its degree is higher), so every burst of length $r$ or less is detected.
- **Random errors:** a random error pattern is a multiple of $G$ with probability $2^{-r}$, so an $r$-bit CRC leaves an undetected fraction of $2^{-16} = 1.5 \times 10^{-5}$ for 16 bits and $2^{-32} = 2.3 \times 10^{-10}$ for 32 bits.

A CRC detects an error and cannot locate it. A mismatch makes the protocol ask for a retransmission, as the PCIe data link layer does with a 32-bit link CRC and an acknowledgment protocol, or as Ethernet does with the frame check sequence at the MAC layer that makes the higher layers discard the frame.

### Error Correction: Reed-Solomon Codes

A **forward error correction** (FEC) code adds enough redundancy for the receiver to repair errors without asking for a retransmission, which at 100 Gb/s and above is the only practical choice because a retransmission request cannot be issued within the delay of the link. The code of Ethernet at 100 Gb/s and above is the **Reed-Solomon** (RS) code, and PCIe 6.0 uses a lighter correcting code on fixed-size units. The Reed-Solomon code works on **symbols** of $m$ bits (10 bits for the codes below) and not on single bits, and an RS$(n, k)$ code turns $k$ data symbols into a block of $n$ symbols by adding $n - k$ parity symbols.

The correction capability follows from an argument that needs only the properties of polynomials. Treat the $k$ data symbols as the coefficients of a polynomial $p(x)$ of degree below $k$ over a finite field with $2^m$ elements (a set of symbols in which addition and multiplication are defined and every non-zero element has an inverse), and transmit the values $p(\alpha_1), \dots, p(\alpha_n)$ at $n$ distinct field elements. Two different polynomials of degree below $k$ can agree at no more than $k - 1$ points, since their difference is a non-zero polynomial of degree below $k$ and has at most $k - 1$ roots. Two different codewords therefore differ in at least $n - (k - 1)$ positions, and the **minimum distance** of the code is

$$d_{min} = n - k + 1$$

A decoder that finds the closest codeword is guaranteed to be right when the number of symbol errors $t$ is small enough that the spheres of radius $t$ around the codewords do not overlap, which requires $2t + 1 \le d_{min}$:

$$t = \left\lfloor \frac{n - k}{2} \right\rfloor$$

Each corrected error costs two parity symbols, because the decoder must find both the position of the error and its value. An **erasure**, a symbol whose position is known (for example, a lane that lost lock), costs only one parity symbol, so a code can repair $n - k$ erasures. The decoding itself (computing syndromes, locating the errors with the Berlekamp-Massey algorithm, and finding their values) is stated here without derivation (Tier 2), because its mathematics goes beyond the book's scope, and the result of the argument above is what matters for link design: the correction capability counts **symbols**, so a burst of bit errors that falls inside one 10-bit symbol is a single error, and the same number of bit errors spread across ten symbols is ten.

The code is **systematic**, which means that the data symbols appear unchanged in the codeword followed by the parity symbols. A receiver that detects no error can pass the data on without decoding, and the decoder only needs to correct symbols when the syndrome is non-zero.

## Architecture

### The Sublayer Stack

The operations of this chapter sit at fixed positions in a stack of sublayers, and the stack is the place where the analog and digital parts of a link meet. The standards name the sublayers differently, but the order is the same:

| Sublayer | Task | Where it is treated |
|---|---|---|
| Physical medium dependent (PMD) | Drives and receives the channel medium (copper driver, optical modulator and detector) | Part 1 to Part 4, Part 6 |
| Physical medium attachment (PMA) | Serializer and deserializer, CTLE, DFE, clock recovery, slicer, lane multiplexing | [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md) and [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) |
| Forward error correction (FEC) | Reed-Solomon encoding and decoding, interleaving | This chapter |
| Physical coding sublayer (PCS) | Block encoding, scrambling, word and lane alignment, descrambling | This chapter |
| Media access control (MAC) | Frames, addresses, and the frame check sequence (CRC) | This chapter |

The PMA is the last analog stage. Its output is the stream of slicer decisions that Chapter 16 describes as a parallel word at a lower clock rate, and everything behind it is digital logic. The instruments of Part 3 and Part 4 act at the PMA input, so their eye diagrams describe the analog receiver only, while the PCS and the MAC deliver a corrected stream whose error ratio is a separate quantity. The final edge case of this chapter returns to the difference. The PCIe stack uses other names (a physical layer with an electrical and a logical sub-block, then a data link layer with the link CRC and the acknowledgment protocol, then a transaction layer), and the allocation of the tasks to them is the same.

### The Receive Pipeline and the Order of Operations

The receiver processes the stream in the reverse order of the transmitter, and the order is constrained by the properties derived above:

1. **Word and block alignment:** the slicer output is a stream of bits with no framing, and the logic must find the boundary of the symbol or block before any decoding makes sense.
2. **Lane alignment and deskew:** a multi-lane link spreads the data over several lanes whose delays differ, so each lane carries a periodic marker with a pattern unique to that lane, and the receiver identifies the lane and delays each lane to line up the markers.
3. **Forward error correction:** the decoder acts on the stream as it arrived from the channel.
4. **Descrambling and decoding:** the descrambler and the block or table decoder recover the data and strip the overhead.
5. **Frame handling and CRC:** the MAC checks the frame check sequence and delivers the frame.

Step 3 stands before step 4 because of the error multiplication that the scrambler section derives. A self-synchronous descrambler turns one channel error into up to three errors, and a decoder placed behind it would see three times the error rate with the errors in symbols it cannot tell apart from random ones. A transmitter therefore scrambles first and encodes the result, so that the decoder acts directly on the channel errors and the descrambler works on the already corrected stream. This is a design consideration that follows from the algebra, and the exact order of the sublayers inside a given standard varies with the standard.

### Word Alignment and Frame Lock

An **8b/10b receiver** searches the stream for the comma. The symbol boundary can lie at any of 10 bit positions, and the comma, which cannot occur in valid data across any boundary, fixes the position at its first occurrence. Link training sends commas continuously for this purpose.

A **64b/66b receiver** has no comma, so it tests the hypothesis that a header starts at position $s$ by checking that the two bits at $s$ and at every following multiple of 66 form 01 or 10. In scrambled random data a wrong hypothesis passes one check with probability $1/2$, since two of the four two-bit patterns are valid, and it fails after on average 2 blocks (the mean of a geometric distribution with $p = 1/2$). The receiver declares lock after $N$ consecutive valid headers, and a wrong alignment passes all of them with probability $2^{-N}$. The 10 Gb/s Ethernet state machine uses $N = 64$, so the probability of a false lock is $2^{-64} = 5.4 \times 10^{-20}$. The search over the 65 wrong positions costs at most about $65 \times 2$ blocks (8,580 bits), and the confirmation of the right position costs 64 blocks (4,224 bits), together about 12,800 bits, or 1.24 microseconds at 10.3125 Gb/s. This is an upper estimate, and the real search stops at the first correct position.

A **multi-lane link** adds an alignment marker that is repeated periodically on each lane. The markers have two uses: they identify the lane (so that a swapped pair of lanes can be reordered) and they give the relative skew between lanes (so that the faster lanes can be delayed until the slowest has arrived). The period and pattern of the markers are defined by each standard.

### Interleaving and Burst Errors

The error mechanisms of the earlier chapters produce bursts, not isolated errors. [CTLE and DFE](14_CTLE_and_DFE.md) shows that one wrong decision of a DFE feeds a wrong value into the next decisions, so a burst follows. A burst of $b$ consecutive bits touches at most $\lceil (b-1)/10 \rceil + 1$ symbols of 10 bits, so a 30-bit burst corrupts at most 4 symbols, and it corrupts only 3 symbols when it is aligned with the symbol boundaries. A code with $t = 7$ repairs it easily, but a longer burst exceeds $t$ in one codeword.

**Interleaving** distributes a burst over several codewords. The transmitter sends the symbols of $I$ codewords in a round-robin order, so that $I$ consecutive symbols on the wire belong to $I$ different codewords. A burst of $B$ consecutive symbols then puts at most $\lceil B/I \rceil$ symbols into any one codeword, and the code repairs the burst when $\lceil B/I \rceil \le t$, that is, for any burst up to $I\,t$ symbols. With depth $I = 4$ and $t = 7$ this is 28 symbols, or 280 bits. Interleaving costs latency and memory, because the receiver must collect the symbols of all $I$ codewords before it can decode the first, and it does not improve the capability against independent random errors.

### Clock Compensation and Forwarded Clocks

The transmitter and the receiver of a link have independent reference oscillators. Two crystals with an offset of up to 100 ppm each can differ by 200 ppm (the worst case that [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) also uses), so the receiver consumes symbols at a rate that departs from the arrival rate by that fraction. The mismatch gains or loses one symbol in $1/(200 \times 10^{-6}) = 5{,}000$ symbols, and a **clock compensation** mechanism absorbs it. The transmitter periodically inserts a filler symbol (an idle or a skip ordered set) that carries no data, and an elastic buffer in the receiver deletes or repeats these fillers to match the rates. The frequency of the fillers must be high enough that the buffer neither empties nor overflows within the interval between them.

Memory interfaces use the opposite clocking architecture. A DDR bus has a physical clock wire (CK) next to the data wires (DQ), and the memory controller places a new data symbol on each rising and each falling edge of the clock, so the data rate in transfers per second is twice the clock frequency:

$$1.6\ \text{GHz} \times 2 = 3.2\ \text{GT/s}$$

The Nyquist frequency of the data wires is half the transfer rate, 1.6 GHz, and it equals the clock frequency because one clock cycle carries two transfers. A standard non-ECC DDR4 channel is 64 bits wide, so its throughput is $3.2\ \text{GT/s} \times 64 = 204.8$ Gb/s (25.6 GB/s). The forwarded clock removes the clock recovery circuit, and it moves the cost to the board: the clock and data traces must be length matched so that their skew stays well below the unit interval, and the matching becomes impractical as the frequency rises. [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) shows why the highest-speed interfaces embed the clock instead.

## Worked Examples

### Encoding Overhead Across PCIe Generations

The data rate per lane is the transfer rate multiplied by the code rate $k/n$:

| Generation | Transfer rate (GT/s) | Code | Code rate | Data rate (Gb/s) |
|---|---|---|---|---|
| Gen 1 | 2.5 | 8b/10b | 0.8000 | 2.000 |
| Gen 2 | 5 | 8b/10b | 0.8000 | 4.000 |
| Gen 3 | 8 | 128b/130b | 0.9846 | 7.877 |
| Gen 4 | 16 | 128b/130b | 0.9846 | 15.754 |
| Gen 5 | 32 | 128b/130b | 0.9846 | 31.508 |

The change of code at Gen 3 reduced the overhead from 20 percent to 1.54 percent, and the 1.6 times higher transfer rate (from 5 to 8 GT/s) together with the 1.23 times better code rate gives a data rate per lane of 7.877 Gb/s instead of 4.0 Gb/s, a factor of 1.97 and not the factor of 2 that the nominal "doubling" suggests. PCIe 6.0 changes the signaling (PAM4 at 32 GBd with a lightweight FEC and CRC on fixed-size units) and does not use 128b/130b.

### Ethernet Line Rates and the 100G and 400G Rate Chains

The 10 Gb/s Ethernet lane uses 64b/66b, so the line rate is $10 \times 66/64 = 10.3125$ Gb/s and the unit interval is $1/10.3125\ \text{GHz} = 96.97$ ps. The 25 Gb/s lane has the line rate $25 \times 66/64 = 25.78125$ Gb/s, and four such lanes give the aggregate $4 \times 25.78125 = 103.125$ Gb/s of a 100 Gb/s link.

The same aggregate follows from the chain that includes FEC. The 66-bit blocks are converted to 257-bit blocks (the 256 payload bits of four 66-bit blocks and one flag bit form one 257-bit block, so the eight header bits are replaced by one bit, a code rate of $256/257$), and the Reed-Solomon code RS(528,514) with 10-bit symbols adds $14$ parity symbols to $514$:

$$100 \times \frac{257}{256} \times \frac{528}{514} = 103.125\ \text{Gb/s}$$

The RS(528,514) code has $t = (528 - 514)/2 = 7$, a minimum distance of 15, a codeword of 5,280 bits, and an overhead of $14/514 = 2.72$ percent. The 400 Gb/s chain uses RS(544,514) ($t = 15$, minimum distance 31, 5,440 bits, overhead 5.84 percent) and gives

$$400 \times \frac{257}{256} \times \frac{544}{514} = 425.0\ \text{Gb/s}$$

for the aggregate of the lanes, for example 53.125 Gb/s per lane over 8 lanes with PAM4 at 26.5625 GBd. The code parameters in these examples are those of the named standards. The derivations above do not depend on them, and the clause numbers are not quoted here.

### Running Disparity Walk

Start with $RD = -1$ and send five symbols whose allowed disparities are shown. At $RD = -1$ the transmitter may choose disparity 0 or $+2$, and at $RD = +1$ it may choose 0 or $-2$:

| Symbol | RD before | Disparity chosen | RD after |
|---|---|---|---|
| 1 | $-1$ | $+2$ | $+1$ |
| 2 | $+1$ | 0 | $+1$ |
| 3 | $+1$ | $-2$ | $-1$ |
| 4 | $-1$ | 0 | $-1$ |
| 5 | $-1$ | $+2$ | $+1$ |

The cumulative sum never leaves the pair $\{-1, +1\}$ at a boundary. With the bound $|D| \le 11$ bits, a 10 Gb/s link ($T_{UI} = 100$ ps) with the 100 nF coupling capacitor and 50 ohm termination of Chapter 6 ($\tau = 5\ \mu\text{s}$) has a baseline wander of at most $11 \times 100\ \text{ps}/5\ \mu\text{s} = 2.2 \times 10^{-4}$ of the amplitude. At the symbol boundaries, where $|D| = 1$, the value is $2 \times 10^{-5}$.

### Baseline Wander of a Scrambled Stream

A scrambled stream behaves like random bits $a_k = \pm 1$. The capacitor voltage $v_k = (A\,T_{UI}/\tau)\sum_j a_{k-j}\,e^{-jT_{UI}/\tau}$ has the variance

$$\sigma_v^2 = \left(\frac{A T_{UI}}{\tau}\right)^2 \sum_{j=0}^{\infty} e^{-2jT_{UI}/\tau} \approx \left(\frac{A T_{UI}}{\tau}\right)^2 \frac{\tau}{2T_{UI}} = \frac{A^2 T_{UI}}{2\tau}$$

where the sum of the geometric series uses $T_{UI} \ll \tau$. For the 5 $\mu$s time constant at 10 Gb/s this gives $\sigma_v = A\sqrt{100\ \text{ps}/(2 \times 5\ \mu\text{s})} = 3.2 \times 10^{-3} A$, and at the 7.03 sigma of a $10^{-12}$ tail the shift is $2.2 \times 10^{-2} A$. The deterministic code bound above is 100 times smaller than this tail. A 1 nF capacitor with the same 50 ohm termination has $\tau = 50$ ns and gives $\sigma_v = 0.032 A$ and a $10^{-12}$ tail shift of 0.22 $A$ for the scrambled stream, while the 8b/10b bound is $11 \times 100\ \text{ps}/50\ \text{ns} = 0.022 A$, ten times smaller. The scrambled link therefore needs a larger coupling capacitor, or a receiver that corrects the baseline, to reach the same margin.

### Self-Synchronous Scrambler

A simulation of the scrambler $G(x) = 1 + x^{39} + x^{58}$ confirms the derivation. A random stream of 2,000 bits is scrambled from a random state and descrambled from the all-zero state: the first 58 output bits contain 27 errors, and the remaining 1,942 bits contain none. One channel flip at bit 500 produces three data errors at bits 500, 539 and 558. A bit error ratio of $10^{-12}$ in the channel therefore becomes $3 \times 10^{-12}$ after descrambling, and the three errors fall in different 10-bit symbols of a code that acts after the descrambler, so the code would see three symbol errors for one channel error, one reason for the order of the receive pipeline.

### CRC by Hand

Take the data $D = 1101011011$ (10 bits) and the generator $G = x^4 + x + 1$, written 10011, so that $r = 4$. Appending four zeros to the data gives the dividend 11010110110000. The long division by the exclusive-or of 10011 at each leading one leaves the remainder $R = 1110$. The transmitted frame is 11010110111110, and dividing it by 10011 leaves the remainder 0000. Flipping any one of its 14 bits gives a non-zero remainder, so every single-bit error is detected, in agreement with the argument above. The error pattern equal to the generator shifted three positions, 00000010011000, is a multiple of $G$ and changes the frame to 11010100100110, which also leaves the remainder 0000. This is a burst of 5 bits, longer than $r = 4$, and it shows the limit of the guarantee.

### Reed-Solomon Capability and the Raw Error Ratio

Assume independent bit errors at the raw ratio $p$. A 10-bit symbol is wrong with probability $p_s = 1 - (1 - p)^{10}$, which is about $10p$ for small $p$. A codeword is uncorrectable when more than $t$ of its $n$ symbols are wrong, with the probability $P_{cw} = \sum_{j > t}\binom{n}{j}p_s^{\,j}(1-p_s)^{n-j}$. The table lists the model values:

| Code | $t$ | Raw $p$ | $P_{cw}$ |
|---|---|---|---|
| RS(528,514) | 7 | $1 \times 10^{-5}$ | $1.4 \times 10^{-15}$ |
| RS(528,514) | 7 | $1 \times 10^{-4}$ | $8.9 \times 10^{-8}$ |
| RS(528,514) | 7 | $5 \times 10^{-4}$ | $5.6 \times 10^{-3}$ |
| RS(544,514) | 15 | $1 \times 10^{-4}$ | $1.4 \times 10^{-18}$ |
| RS(544,514) | 15 | $2 \times 10^{-4}$ | $5.4 \times 10^{-14}$ |
| RS(544,514) | 15 | $5 \times 10^{-4}$ | $2.8 \times 10^{-8}$ |

The raw ratio that gives $P_{cw} = 10^{-13}$ is $1.7 \times 10^{-5}$ for RS(528,514) and $2.1 \times 10^{-4}$ for RS(544,514). The codeword probability falls steeply, by ten orders of magnitude between $5 \times 10^{-4}$ and $10^{-4}$ for the second code, because the error count must exceed $t$, so the code has a **threshold** behavior: the post-correction ratio is negligible below the threshold and rises quickly above it.

The threshold translates into an analog margin through [PAM4 Signaling and Gray Coding](15_PAM4_Signaling_and_Gray_Coding.md). A Gray-coded PAM4 link has the bit error ratio $0.75\,Q(d/\sigma)$, so the raw ratio $2.1 \times 10^{-4}$ needs $d/\sigma = 3.45$, against 6.99 at $10^{-12}$. The noise can be larger by $20\log_{10}(6.994/3.452) = 6.13$ dB for RS(544,514), and by 4.69 dB for the weaker RS(528,514) code. The 5.66 dB of the table in Chapter 15 corresponds to an assumed raw ratio of $10^{-4}$, between these two values. The code buys 6 dB of analog noise tolerance at the cost of 5.84 percent line rate and latency. A codeword of 5,440 bits needs at least $5{,}440/425\ \text{Gb/s} = 12.8$ ns to arrive, and the 5,280 bits of RS(528,514) need 51.2 ns at 103.125 Gb/s, which is the minimum added delay of a decoder that waits for the complete block.

### Unit Interval of DDR4-3200

DDR4-3200 operates at 3.2 GT/s, so the unit interval is $1/(3.2 \times 10^{9}) = 312.5$ ps, and the clock frequency is 1.6 GHz. An oscilloscope that draws an eye diagram on a DQ wire folds the capture modulo this 312.5 ps, in the construction of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md).

## Edge Cases

### Comma Symbols and K-Codes

The 8b/10b table contains control symbols that cannot be confused with data. The comma sequence 0011111 or 1100000 appears only in the K28.5 symbol (0011111010 or 1100000101) and in the reserved symbols K28.1 and K28.7, and it cannot be formed by any two adjacent data symbols. This uniqueness is what makes the alignment reliable in a continuous stream, but it also means that a bit error can create a false comma: a single flipped bit in a data stream can produce a comma-like pattern at a wrong boundary, and a receiver that realigns on every comma would lose its word boundary. Real receivers align once during training and re-align only after a sustained loss of valid symbols, and a received symbol that is not in the table is flagged as a **code violation**, which gives the receiver an error indication without any added redundancy. The check works because a corrupted symbol often lands on a word that is not in the table, or on a word whose disparity is wrong for the current running disparity.

### Scrambling Does Not Guarantee Transitions

The scrambler provides statistical balance, and some inputs defeat it. The all-zero input with the all-zero delay-line state produces the all-zero output, because each output bit is the exclusive-or of zeros: the simulation gives no ones at all in 100 bits. A real transmitter does not stay in this state, since the sync header, which is not scrambled, injects ones at every block, and the headers bound the run at 66 bits as derived above. A deliberately chosen input can also drive a self-synchronous scrambler into a long run, because the scrambler is linear and an attacker who knows the polynomial can compute an input that produces a chosen output. Standards that use the scrambler for short-run assurance therefore count on the header for the deterministic bound and on the statistics for the typical behavior. [Test Patterns and Jitter Isolation](12_Test_Patterns_and_Jitter_Isolation.md) uses PRBS-15 and PRBS-31 for the validation of scrambled links for this reason: a long pattern exercises long runs that a 5-bit run limit would never produce.

### Errors Beyond the Correction Limit

A codeword with more than $t$ symbol errors can end in two ways. The decoder may recognize that the syndrome does not match any pattern of $t$ or fewer errors and flag the codeword as uncorrectable, and the system counts a failed codeword and discards the frame. The decoder may also find a valid codeword at distance $t$ or less from the corrupted word, which is a different codeword from the one that was sent, and it then delivers wrong data with no flag (a **miscorrection**). The probability of a miscorrection is small for a code with a large $t$, because the spheres of radius $t$ cover a small fraction of the space, and the frame check sequence of the MAC catches the wrong data at the next level. The design therefore relies on the layers together: the code reduces the raw ratio to a low value, the CRC detects what remains, and the protocol retransmits what the CRC rejects.

### A Cycle Slip Is Not a Symbol Error

[CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) states that forward error correction cannot repair a cycle slip, and the code structure gives the quantitative reason. A slip moves the bit stream by one position. A 10-bit symbol after the slip equals the symbol at the same position before the slip only if the 11 bits that cover both are all equal, which has the probability $2^{-10}$, so about $528 \times (1 - 2^{-10}) = 527$ of the 528 symbols of a codeword are wrong. The capability of RS(528,514) is 7 symbols. The number of errors exceeds the limit by a factor of 75, so the codeword is lost, and every following codeword is lost until the receiver finds the alignment again. The recovery uses the markers of the stream: the 64b/66b receiver sees invalid headers at about half the blocks (the probability that a shifted header is valid is one half), drops the lock after the number of invalid headers that its state machine allows, and repeats the search of the word alignment section, which costs about 1.2 microseconds at 10.3125 Gb/s. The loop design of Chapter 17 must therefore keep slips rare enough that this recovery time, multiplied by their rate, stays negligible in the error budget.

### Eye Margin and the Post-Correction Ratio

A collapsed eye at the PMA input does not prove that the link fails, and an open eye does not prove that it works. The eye describes the margin at the slicer, and a code with the threshold behavior of the worked example tolerates a raw ratio of $10^{-4}$ to $10^{-5}$ while it delivers an error-free stream. Conversely, a link whose raw ratio sits just above the threshold of the code produces a stream of uncorrectable codewords even though the eye looks open at the $10^{-12}$ extrapolation of [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md), and the extrapolation does not apply to the bursts that a DFE generates. A validation plan therefore measures both: the raw ratio by a BERT or the eye contour of Chapter 16, and the post-correction codeword failure count by the error counters of the PCS. The next chapter begins Part 6, where the same questions of bandwidth, noise, and margin appear for a signal that travels on a light wave instead of a copper trace.
