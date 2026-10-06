# PAM4 Signaling and Gray Coding

<!-- SUMMARY: PAM4 encodes two bits per symbol by dividing the transmitter swing into four levels. This guide derives the $-9.54$ dB penalty in eye amplitude, links it to target error ratios, and explains the symbol error reductions achieved by Gray coding and three-slicer receivers. --> 

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[CTLE and DFE](14_CTLE_and_DFE.md) describes the receiver equalizers that restore the amplitude and the shape of a pulse after the channel. The equalizers cannot restore energy that the channel has converted to heat, and the loss grows with frequency as [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) derives. A higher symbol rate therefore costs insertion loss at a higher Nyquist frequency, and at some rate the loss exceeds what the transmitter and receiver can compensate.

PAM4 (pulse amplitude modulation with four levels) raises the data rate without raising the symbol rate. The transmitter divides the voltage swing into four evenly spaced levels, and each level represents a unique pair of bits. A 64 Gb/s PAM4 link operates at 32 Gbaud, and its Nyquist frequency of 16 GHz is the Nyquist frequency of a 32 Gb/s NRZ link. The channel loss at 16 GHz is much smaller than the loss at the 32 GHz that 64 Gb/s NRZ would need, and the Worked Examples section puts numbers on the difference.

The price of the extra levels is paid in voltage margin. Four levels share the swing that held two, so the distance between adjacent levels is one third of the NRZ distance, and the same noise causes more errors. This chapter derives the penalty and the conditions under which it applies, links it to the Q table of [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md), and derives the error ratios of the three-slicer receiver. It then shows how the assignment of bit pairs to levels, the Gray code, reduces the bit error ratio, and why timing recovery from a PAM4 waveform is harder than from an NRZ waveform.

## Core Concepts

### NRZ, PAM2, and Return to Zero

The term non-return-to-zero (NRZ) describes the temporal behavior of the waveform. Older signaling schemes used return-to-zero (RZ) encoding, which forces the voltage back to zero in the middle of every bit period so that every bit contains a transition. A sequence of three logic 1 bits in an RZ scheme rises, falls to zero, and rises again three times. An NRZ transmitter holds the voltage at the level of the bit for the whole bit period, and three consecutive logic 1 bits produce one continuous high voltage for three bit times.

NRZ removes the transition overhead of RZ and leaves long runs of identical bits without transitions, which the clock recovery circuit must handle ([CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) describes the circuit, and [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) describes the codes that limit the run length). NRZ is the same as two-level pulse amplitude modulation, PAM2, and the name PAM2 distinguishes it from PAM4. The voltages in this chapter are differential voltages: the physical link carries two wires with equal and opposite voltages, and [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md) describes differential signaling and the rejection of common-mode noise.

### Symbol Rate, Unit Interval, and the Nyquist Frequency

Three quantities describe the speed of a serial link, and they are easily confused. The **data rate** is the number of bits per second that the protocol delivers. The **symbol rate** $R_s$ (in baud) is the number of voltage symbols per second on the wire. The **unit interval** is the duration of one symbol, $UI = 1/R_s$, which is the definition of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md). A symbol that can take $M$ levels carries $\log_2 M$ bits, so

$$\text{data rate} = R_s\log_2 M$$

NRZ has $M = 2$ and one bit per symbol, so the data rate in bits per second equals the symbol rate in baud. PAM4 has $M = 4$ and two bits per symbol, so the data rate is twice the symbol rate, and the unit interval of a PAM4 link is the reciprocal of the symbol rate and not of the bit rate: a 64 Gb/s PAM4 link has $UI = 1/(32\ \text{GBd}) = 31.25$ ps, whereas a 64 Gb/s NRZ link would need $UI = 15.625$ ps.

[Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md) defines the Nyquist frequency as half the symbol rate, the fundamental frequency of the fastest alternating pattern. The definition applies without change to PAM4, because the fastest alternation of a multilevel signal is one in which the level changes at every symbol, for instance $+3, -3, +3, -3$, which completes one cycle every two symbols. A pattern that cycles through all four levels, $+3, +1, -1, -3$, repeats only every four symbols and has the lower fundamental $R_s/4$, so it is not the fastest pattern. The Nyquist frequency is $R_s/2$ for both signaling schemes, and the comparison that matters for the channel is the symbol rate:

| Link | Data rate | Symbol rate | Nyquist frequency |
|:---|:---:|:---:|:---:|
| NRZ | 32 Gb/s | 32 GBd | 16 GHz |
| NRZ | 64 Gb/s | 64 GBd | 32 GHz |
| PAM4 | 64 Gb/s | 32 GBd | 16 GHz |

The number of bits per symbol is bounded by the noise as well as by the bandwidth. The capacity of a channel of bandwidth $B$ is $B\log_2(1 + \mathrm{SNR})$ (the Shannon-Hartley theorem), so the maximum rate grows only logarithmically with the signal-to-noise ratio. PAM4 uses a smaller bandwidth by spending signal-to-noise ratio, and the next section derives the amount.

### PAM4 Levels and the Three Eyes

A linear PAM4 signal divides the peak-to-peak swing into three equal intervals. In normalized units the four levels are $+1$, $+1/3$, $-1/3$, and $-1$, and engineers label them $+3$, $+1$, $-1$, and $-3$ to emphasize the uniform spacing. A typical transmitter has a differential peak-to-peak swing of 800 mV, which gives the levels $+400$, $+133.3$, $-133.3$, and $-400$ mV.

The signal has three vertical eye openings, one between each pair of adjacent levels. **All three eyes are equal:** each spans $800/3 = 266.7$ mV, because the spacing between adjacent levels is the same at every position. The decision threshold of each eye sits at its center, at $+266.7$, $0$, and $-266.7$ mV. Every level lies $133.3$ mV from each threshold beside it, and an inner level has two such thresholds while an outer level has one. The Edge Cases section returns to the question of which threshold limits the error ratio, and the answer depends on the number of thresholds that a level has and not on the distance to them.

### The Penalty of Four Levels

The NRZ levels at a peak swing of 800 mV are $\pm 400$ mV, and the distance from each level to its threshold is 400 mV. A signal with $M$ equally spaced levels in the same peak swing has $M - 1$ intervals, and the distance from a level to the nearest threshold is the half-interval $A/(M-1)$, where $A$ is the peak amplitude. The distance relative to NRZ ($M = 2$, distance $A$) is $1/(M-1)$, and the change in decibels of a voltage ratio is the $20\log_{10}$ defined in [S-Parameters and Vector Network Analysis](08_S_Parameters_and_VNA.md):

$$\text{penalty} = 20\log_{10}\frac{1}{M-1}, \qquad M = 4:\quad 20\log_{10}\frac13 = -9.54\ \text{dB}$$

The penalty applies under two stated assumptions: the **peak swing** is the same for both signals (it is limited by the supply and the output stage of the transmitter), and the **noise** at the slicer has the same rms value for both. Values for other numbers of levels follow from the formula:

| Levels $M$ | Bits per symbol | Penalty at equal peak swing |
|:---:|:---:|:---:|
| 2 | 1 | 0 dB |
| 4 | 2 | $-9.54$ dB |
| 8 | 3 | $-16.90$ dB |

The assumption of equal peak swing is one choice. A transmitter limited by its average power, as in a power-limited link, gives a different number. The average power of the four levels $\pm 1, \pm 1/3$ is $(2 \times 1 + 2 \times 1/9)/4 = 5/9$ of the NRZ value, so a PAM4 signal at the same average power as an NRZ signal has its levels scaled up by $\sqrt{9/5}$, and the half-interval becomes $(1/3)\sqrt{9/5} = 0.447$ of the NRZ distance, which is $-6.99$ dB. The two figures differ by 2.55 dB, which is $10\log_{10}(9/5)$, the ratio of the peak power to the average power of the PAM4 levels. A link limited by swing is the usual case in electrical serial links, and the rest of the chapter uses $-9.54$ dB.

The decibel figure translates into an error ratio through the Q function of [Dual-Dirac Model and BER Extrapolation](11_Dual_Dirac_Model_and_BER_Extrapolation.md). Assume that the noise at the slicer is Gaussian with the standard deviation $\sigma$. A level that lies a distance $d$ from a threshold is misread across that threshold with the probability $Q(d/\sigma)$. An NRZ level has one threshold, so the bit error ratio is $Q(A/\sigma)$, and the distance in standard deviations for a target ratio is the Q-factor of that chapter: 4.753, 5.998, 7.034, 7.941, and 8.757 for $10^{-6}$, $10^{-9}$, $10^{-12}$, $10^{-15}$, and $10^{-18}$.

An inner PAM4 level has a threshold on each side and an outer level has one. Take the four symbols as equally likely and count the errors to adjacent levels, the dominant error. Each of the three thresholds is crossed by two symbols, one from each side, with probability $Q(d/\sigma)$ each, where $d = A/3$ is the half-interval. The probability per symbol that a given threshold is crossed is therefore $2 \times \tfrac14\,Q(d/\sigma) = \tfrac12 Q(d/\sigma)$, and the symbol error ratio is the sum over the three thresholds:

$$\mathrm{SER} = 3 \times \tfrac12\,Q\!\left(\frac{d}{\sigma}\right) = 1.5\,Q\!\left(\frac{A}{3\sigma}\right)$$

The inner symbols have two neighbors and an error ratio of $2Q$ each, the outer symbols have one neighbor and an error ratio of $Q$ each, and the average over four symbols is $(2 \times 2Q + 2 \times Q)/4 = 1.5Q$, which agrees. The number of bit errors per symbol error depends on the code and is derived in the next sections. With Gray coding each adjacent-level error flips one of the two bits, and the bit error ratio is $\mathrm{BER} = \mathrm{SER}/2 = 0.75\,Q(A/(3\sigma))$.

The required noise follows from this expression. For a target $p$ the half-interval must be $z_p$ standard deviations, with $0.75\,Q(z_p) = p$. The values below use the Q function of that chapter, and the NRZ column is its table. They assume the same peak swing and the same Gaussian noise for both signals:

| Target BER | NRZ distance (σ units) | PAM4 distance (σ units) | SNR penalty of PAM4 |
|:---:|:---:|:---:|:---:|
| $10^{-12}$ | 7.034 | 6.994 | 9.49 dB |
| $10^{-9}$ | 5.998 | 5.951 | 9.47 dB |
| $10^{-6}$ | 4.753 | 4.695 | 9.44 dB |
| $10^{-4}$ | 3.719 | 3.646 | 9.37 dB |

The penalty at a fixed error ratio is 9.4 to 9.5 dB and not exactly 9.54 dB, because the factor $0.75$ lets the PAM4 receiver operate at a slightly smaller distance in standard deviations. The decibel figure of $-9.54$ dB is the exact change of the eye amplitude at equal swing, and it is the simple estimate of the loss of signal-to-noise ratio.

### The Three Slicers and Thermometer Code

The receiver uses three slicers, one for each eye. Each slicer is a comparator that outputs a logic 1 when the input exceeds its threshold and a logic 0 when it does not, and it produces no analog value. The thresholds sit at $+266.7$, $0$, and $-266.7$ mV for the levels of the example above. The outputs of the three slicers, read together, form a **thermometer code**, because the ones fill from the bottom as the voltage rises, like the mercury in a thermometer:

| Input level | Code (top, middle, bottom) | Meaning |
|:---:|:---:|:---|
| $+400$ mV (level $+3$) | 1-1-1 | Above all three thresholds |
| $+133.3$ mV (level $+1$) | 0-1-1 | Above the middle and bottom thresholds |
| $-133.3$ mV (level $-1$) | 0-0-1 | Above the bottom threshold only |
| $-400$ mV (level $-3$) | 0-0-0 | Below all three thresholds |

A fixed logic table converts the four codes into the two data bits. The mapping that this table implements is a design choice with consequences for the error ratio, which the next section analyzes.

### Gray Coding and the Hamming Distance

The mapping between the four levels and the four bit pairs determines how many bit errors one symbol error causes. The **Hamming distance** of two bit patterns is the number of positions in which they differ.

**Natural binary mapping:** Counting in binary, $00$, $01$, $10$, $11$, and assigning the values to the levels from the bottom to the top places the pair $01$ and $10$ on the two inner levels, which are separated by the middle threshold. A noise error across that threshold changes both bits, a Hamming distance of 2. The errors across the outer thresholds change one bit. The thresholds are crossed with equal probability $\tfrac12 Q$ per symbol, as derived above, so the number of bit errors per symbol is

$$\tfrac12 Q \times 2 + \tfrac12 Q \times 1 + \tfrac12 Q \times 1 = 2Q, \qquad \mathrm{BER}_{natural} = \frac{2Q}{2} = Q$$

**Gray mapping:** A Gray code is a sequence in which every neighbor differs in exactly one position, a Hamming distance of 1. The standard PAM4 assignment is:

| Level | Thermometer code | Bit pair |
|:---:|:---:|:---:|
| $+3$ | 1-1-1 | 1-0 |
| $+1$ | 0-1-1 | 1-1 |
| $-1$ | 0-0-1 | 0-1 |
| $-3$ | 0-0-0 | 0-0 |

Every adjacent-level error changes one bit, and the number of bit errors per symbol is $\tfrac12 Q \times 3 = 1.5Q$, so $\mathrm{BER}_{Gray} = 1.5Q/2 = 0.75Q$. Gray coding lowers the bit error ratio by one quarter compared with natural binary mapping, a factor of $4/3$. The reduction is a measurable gain and a modest one, and it comes from the middle threshold alone, which causes two bit errors with natural binary and one with Gray.

The assignment also divides the errors between the two bits. The first (most significant) bit is 1 for the top two levels and 0 for the bottom two, and it changes only across the middle threshold. The second (least significant) bit is 0 for the two outer levels and 1 for the inner levels, and it changes across the upper and the lower threshold. A middle-threshold error occurs with the probability $\tfrac12 Q$ per symbol and an outer-threshold error with $2 \times \tfrac12 Q = Q$, so the second bit has twice the error ratio of the first. The average, $(0.5Q + Q)/2 = 0.75Q$, agrees with the total. The benefit of Gray coding for forward error correction depends on how the code counts errors, which [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) describes.

## Architecture

### The Gray Decoder

The conversion from the thermometer code to the Gray bit pair needs very little hardware. The first bit is 1 for the top two levels and 0 for the bottom two, which is the output of the middle slicer, so a wire connects the middle slicer to the first bit and no gate is used. The second bit is 0 for the two outer levels and 1 for the two inner levels, which is the output of an exclusive-OR gate with the top and bottom slicers as inputs. The gate outputs 1 when its inputs differ:

- Level $+3$: top slicer 1, bottom slicer 1, the inputs match, output 0.
- Level $+1$: top slicer 0, bottom slicer 1, the inputs differ, output 1.
- Level $-1$: top slicer 0, bottom slicer 1, the inputs differ, output 1.
- Level $-3$: top slicer 0, bottom slicer 0, the inputs match, output 0.

The decoder is one wire and one gate, and the delay it adds is that of one gate. The standards fix the mapping so that every transmitter and receiver agree on it.

### The Demand on the Equalizers

The smaller distance between levels makes every part of the equalization chain more demanding, and the numbers of the earlier chapters show how. [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) shows that a filter with a post-cursor tap only is limited by the signal amplitude that remains after it equalizes, and that 21.2 dB of loss leaves 8.7 percent of the peak swing. The transmitter filter therefore has a limit that is closer for PAM4, whose levels sit at one third of the NRZ distance before any loss is applied. The factor of $1/3$ that gives the $-9.54$ dB penalty of this chapter equals the DC gain of the symmetric filter $(-1/6, 2/3, -1/6)$ of that chapter by coincidence, and the two are unrelated: one is the ratio of the level spacing, and the other is a ratio of the filter gains at two frequencies.

[CTLE and DFE](14_CTLE_and_DFE.md) quantifies the cost of a linear equalizer: it amplifies the noise in its boost band by the factor that it amplifies the signal, and noise already reduces the distance in standard deviations. A larger share of the equalization must come from the decision feedback equalizer, which does not amplify noise but propagates errors, and the burst probability of that chapter rises as the margin in standard deviations falls.

Forward error correction closes the remaining gap. The table of the previous section shows how much: at a target of $10^{-12}$ the PAM4 half-interval must be 6.994 standard deviations, and at a raw target of $10^{-4}$ it must be 3.646, which allows the noise to be larger by $20\log_{10}(6.994/3.646) = 5.66$ dB. A PAM4 link therefore runs at a raw error ratio far above the application requirement and relies on the code to correct the errors, and the code recovers more than half of the 9.5 dB that the extra levels cost.

## Worked Examples

### A Noise Spike at the Middle Threshold

An inner positive symbol arrives at $+133.3$ mV. A negative noise excursion of 150 mV at the sampling instant moves the sample to $-16.7$ mV, and the middle slicer outputs 0, so the receiver decides that the symbol is the inner negative level.

**Natural binary mapping:** the inner positive level is $10$ and the inner negative level is $01$ when the pairs are counted from the bottom, and both bits are wrong. One analog error produces two bit errors.

**Gray mapping:** the inner positive level is $11$ and the inner negative level is $01$. The first bit changes from 1 to 0 and the second bit remains 1. One analog error produces one bit error.

The noise event is the same in both cases, and the mapping alone determines whether the error counts once or twice. Over many symbols the averages are the ones derived above: $\mathrm{BER} = Q$ for natural binary and $0.75\,Q$ for Gray.

### NRZ and PAM4 on the 12 Inch Line at 64 Gb/s

A link must carry 64 Gb/s over the 12 inches of FR4 trace that [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) analyzes. The insertion loss follows the model that [CTLE and DFE](14_CTLE_and_DFE.md) uses, $IL(f) = 12\,(0.20\sqrt{f/5} + 0.47\,f/5)$ dB with $f$ in GHz, which the earlier chapters verified against 5 and 15 GHz. The model extends beyond those frequencies with the same scaling laws, for smooth copper and a loss tangent of 0.02, and it is an estimate there because roughness raises the real loss.

**NRZ:** one bit per symbol needs 64 GBd. The Nyquist frequency is 32 GHz, and the insertion loss is $12\,(0.20\sqrt{6.4} + 0.47 \times 6.4) = 42.2$ dB. The signal arrives at 0.8 percent of its amplitude, and the equalizers cannot restore it.

**PAM4:** two bits per symbol need 32 GBd. The Nyquist frequency is 16 GHz and the insertion loss is $12\,(0.20\sqrt{3.2} + 0.47 \times 3.2) = 22.3$ dB. The loss is 19.8 dB smaller than for NRZ, and it is a loss that a transmitter filter and a receiver equalizer can share, as the 21.2 dB case of [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md) shows.

The net advantage at the Nyquist frequency is $19.8 - 9.5 = 10.3$ dB in favor of PAM4: the channel removes 19.8 dB less amplitude, and the extra levels cost 9.5 dB of signal-to-noise ratio. This difference is the engineering reason for the change from NRZ to PAM4 at rates in the range of 56 Gb/s and above per lane. A channel with a lower loss than this one, or a lower data rate, reverses the balance, because the loss at the NRZ Nyquist frequency is then small enough that the penalty of the extra levels exceeds the gain.

### A Noise Budget at the Slicer

Take the NRZ levels of $\pm 400$ mV and a target of $10^{-12}$. The distance of 400 mV must be 7.034 standard deviations, so the rms noise at the slicer must not exceed $400/7.034 = 56.9$ mV. The same noise on the PAM4 levels of the 800 mV swing gives the half-interval $133.3/56.9 = 2.34$ standard deviations, and the bit error ratio is $0.75\,Q(2.34) = 7.1 \times 10^{-3}$, which is about ten orders of magnitude above the target.

To reach $10^{-12}$ at the PAM4 distance of 6.994 standard deviations the noise must fall to $133.3/6.994 = 19.1$ mV, a factor of 2.98 (9.49 dB) below the NRZ limit. A code that corrects a raw ratio of $10^{-4}$ works at the distance of 3.646 standard deviations, which allows $133.3/3.646 = 36.6$ mV, and that is 5.66 dB more noise than the uncoded PAM4 link tolerates. The two numbers show how much of the penalty the code recovers, and the code adds redundancy that raises the symbol rate, which [Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) quantifies.

## Edge Cases

### Which Threshold Limits the Error Ratio

The three eyes have the same height of 266.7 mV, and the three thresholds lie at the same distance of 133.3 mV from the levels beside them. With symmetric noise each threshold is crossed with the same probability $\tfrac12 Q$ per symbol, as derived above, so no threshold dominates the symbol error ratio by its geometry. A statement that the middle eye is half as tall as the outer eyes is incorrect for a linear signal. The inner symbols are more exposed than the outer symbols because each has two thresholds beside it, and the errors of the inner symbols are twice as likely as those of the outer ones.

The thresholds differ from each other in other respects as well. Gray coding makes the most significant bit vulnerable at only one threshold (the middle), while the least significant bit is vulnerable at two thresholds (the outer), which gives the least significant bit a higher error ratio. The thresholds also experience different amounts of intersymbol interference, which is determined by a physical counting exercise. The four levels produce 12 possible ordered transitions between different voltage states. Any transition from the bottom two levels ($-3, -1$) to the top two levels ($+1, +3$) crosses the middle threshold, which gives $2 \times 2 = 4$ rising transitions. The symmetry provides 4 falling transitions, so 8 of the 12 transitions cross the middle threshold. A crossing of the top threshold requires the level $+3$ as an endpoint, which provides 3 rising transitions from the levels below it and 3 falling transitions to the levels below it, so 6 transitions cross the top threshold. The same count applies to the bottom threshold. This 8/6 distribution concentrates interference in the center eye. The eyes also differ in real transmitters, because the output stage compresses the outer levels at large swing, and the spacing between levels is then unequal. The transmitter specifications for PAM4 include a measure of the mismatch of the level spacing for this reason, and a smaller outer spacing lowers the distance of the outer thresholds below the 133.3 mV of the linear case.

### Timing Recovery from Several Trajectories

An NRZ waveform has one kind of transition, from $-1$ to $+1$ or back, and every transition crosses the threshold at the middle of its edge. A PAM4 waveform has 12 kinds of transition between two different levels, and the edges that cross a threshold differ in their start and end levels, and therefore in the time at which they cross it.

Model each edge as a linear ramp of duration $T_r$ between two levels. A transition from level $a$ to level $b$ crosses zero at the fraction $-a/(b-a)$ of the ramp. The eight transitions that cross the middle threshold, in both directions, give three fractions in units of $T_r$: 0.25 (for example $-1 \to +3$ and $+1 \to -3$), 0.5 (for example $-1 \to +1$ and $-3 \to +3$), and 0.75 (for example $-3 \to +1$ and $+3 \to -1$). The crossings are spread over $0.5\,T_r$ even without noise, and the spread depends on the data pattern, so it is deterministic jitter. Assume a ramp of $T_r = 0.4\,UI$ at 32 GBd, which is 12.5 ps. The crossing times then spread over 6.25 ps, a fifth of the unit interval, and the clock recovery circuit sees this spread as data-dependent jitter that an NRZ signal does not have.

The amplitude noise adds to the effect. The conversion of [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md), $\delta t = -\delta v/S$, depends on the slope $S$ at the crossing. A full-swing transition ($-1 \to +1$) has the amplitude 2 in the normalized units, and an inner transition ($-1/3 \to +1/3$) has the amplitude $2/3$. Over the same ramp the slope of the inner transition is one third of the slope of the full-swing transition and of the NRZ edge, and the same amplitude noise gives three times the timing jitter, which is $20\log_{10}3 = 9.54$ dB. The recovered clock of a PAM4 link has a larger jitter than that of an NRZ link at the same symbol rate for these two reasons, and the jitter budget of the link is correspondingly smaller. [CDR and PLL Loop Dynamics](17_CDR_and_PLL_Loop_Dynamics.md) describes how the phase detector uses the crossings.

### Interference Costs Three Times More Margin

The interference of the channel reduces the distance between a level and a threshold in the same way as noise does, and the relative cost is larger for PAM4. The worst-case interference on a sample comes from neighbors at the outer levels, $\pm A$, which contribute up to $A\sum_{k \neq 0}|h_k|$ in the notation of [Transmitter Feed-Forward Equalization](13_Transmitter_FFE.md). The NRZ margin is $A$, so the interference removes the fraction $\sum|h_k|$ of it, and the worst-case eye height is $2A(1 - \sum|h_k|)$ as in [Jitter Decomposition and Measurement](10_Jitter_Decomposition_and_Measurement.md). The PAM4 margin is $A/3$ while the neighbors can still be at $\pm A$, so the interference removes the fraction $3\sum|h_k|$ of it, and each eye has the height $(2A/3)(1 - 3\sum|h_k|)$. For $M$ levels the fraction is $(M-1)\sum|h_k|$, and the eye closes when that product reaches 1.

The numbers of the 12 inch line show the effect. Take $A = 200$ mV and the cursor sum of 9.26 percent for the first seven cursors. The NRZ eye height is $400 \times 0.9074 = 363$ mV, and 9.26 percent of the margin is gone. Each PAM4 eye has the height $(400/3)(1 - 3 \times 0.0926) = 96.3$ mV in place of 133.3 mV, so 27.8 percent of the margin is gone. The NRZ eye closes at a cursor sum of 1, and the PAM4 eyes close at a cursor sum of 1/3. The receiver therefore needs to cancel interference much more completely than for NRZ, and this requirement is the reason that the equalization of [CTLE and DFE](14_CTLE_and_DFE.md) is applied to its full extent in PAM4 links.
