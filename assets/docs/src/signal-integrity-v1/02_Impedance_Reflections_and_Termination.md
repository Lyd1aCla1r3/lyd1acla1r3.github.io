# Impedance, Reflections, and Termination

<!-- SUMMARY: When an electromagnetic wave encounters a boundary where the characteristic impedance changes, a portion of the wave reflects back toward the source. This guide derives the reflection coefficient from first principles, traces the physical mechanism of signal ringing, and explains the termination strategies that eliminate reflections on production PCBs. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

A transmission line carries electromagnetic energy forward as a propagating wave. The characteristic impedance $Z_0$ governs the ratio of voltage to current within that wave as long as the geometry remains uniform. The moment the wave encounters a boundary where the impedance changes, physics demands that a portion of the energy reflect backward.

The reflection coefficient $\rho$ quantifies exactly how much energy reflects and how much transmits through the boundary. It emerges directly from Kirchhoff's voltage and current laws applied at the impedance discontinuity, and it is the single most important quantity in signal integrity engineering. Every TDR measurement, every impedance-controlled PCB stackup, every termination resistor, and every via optimization strategy traces back to controlling $\rho$.

This guide derives the reflection coefficient from first principles, traces the physical mechanism of reflections propagating between source and load, explains how termination absorbs reflected energy, and describes the transient process by which a transmission line settles from its initial wave-propagation regime into a DC steady state.

## Core Concepts

### The Reflection Coefficient: Derivation from Kirchhoff's Laws

An incident wave travels down a transmission line with characteristic impedance $Z_0$ and strikes a boundary where the impedance abruptly changes to $Z_L$. At this boundary, the incident wave splits into two components: a reflected wave that bounces backward and a transmitted wave that continues forward into $Z_L$.

Three waves exist at the boundary:

1. **Incident wave:** voltage $V_{inc}$, current $I_{inc}$
2. **Reflected wave:** voltage $V_{ref}$, current $I_{ref}$
3. **Transmitted wave:** voltage $V_{trans}$, current $I_{trans}$

Physics imposes two constraints at the exact plane of the boundary.

**Kirchhoff's Voltage Law** requires voltage continuity. The total voltage on the left side of the boundary must equal the total voltage on the right:

$$V_{inc} + V_{ref} = V_{trans}$$

**Kirchhoff's Current Law** requires current continuity. Charge cannot accumulate or vanish at the boundary, so the total current flowing into the junction from the left must equal the current flowing out to the right:

$$I_{inc} + I_{ref} = I_{trans}$$

The relationship between voltage, current, and impedance ($I = V/Z$) links these three waves to the impedances on each side:

- Incident current: $I_{inc} = V_{inc} / Z_0$
- Transmitted current: $I_{trans} = V_{trans} / Z_L$
- Reflected current: $I_{ref} = -V_{ref} / Z_0$

The reflected current carries a negative sign. Voltage is a scalar quantity, but current is a vector with a physical direction. The reflected wave travels backward, so its current vector is opposite to the incident wave's current vector.

Substituting these current expressions into Kirchhoff's Current Law:

$$\frac{V_{inc}}{Z_0} - \frac{V_{ref}}{Z_0} = \frac{V_{trans}}{Z_L}$$

Replacing $V_{trans}$ with the voltage continuity equation ($V_{inc} + V_{ref}$):

$$\frac{V_{inc}}{Z_0} - \frac{V_{ref}}{Z_0} = \frac{V_{inc} + V_{ref}}{Z_L}$$

Cross-multiplying to clear the denominators:

$$Z_L(V_{inc} - V_{ref}) = Z_0(V_{inc} + V_{ref})$$

Distributing the impedances:

$$Z_L V_{inc} - Z_L V_{ref} = Z_0 V_{inc} + Z_0 V_{ref}$$

Collecting $V_{inc}$ terms on the left and $V_{ref}$ terms on the right:

$$V_{inc}(Z_L - Z_0) = V_{ref}(Z_L + Z_0)$$

Isolating the ratio of reflected voltage to incident voltage:

$$\frac{V_{ref}}{V_{inc}} = \frac{Z_L - Z_0}{Z_L + Z_0}$$

Defining this ratio as the reflection coefficient $\rho$:

$$\rho = \frac{Z_L - Z_0}{Z_L + Z_0}$$

This equation is the absolute foundation of signal integrity measurement. Every impedance profile on a TDR screen, every S-parameter return loss plot, and every termination design decision derives from it.

### Three Canonical Terminations

The reflection coefficient formula produces three boundary cases that define the extremes of termination behavior.

**Matched termination ($Z_L = Z_0$):** The numerator becomes zero. $\rho = 0$. No energy reflects. The entire wave transmits into the load and is absorbed. This is the ideal condition for signal integrity. A 50-ohm trace terminated by a 50-ohm resistor produces zero reflections.

**Open circuit ($Z_L = \infty$):** The reflection coefficient approaches $\rho = +1$. The entire wave reflects with the same polarity as the incident wave. The reflected voltage adds constructively to the incident voltage, doubling it at the boundary. No current flows into the open circuit, and the reflected wave carries all of the incident energy backward.

**Short circuit ($Z_L = 0$):** The reflection coefficient equals $\rho = -1$. The entire wave reflects with inverted polarity. The reflected voltage subtracts from the incident voltage, forcing the boundary voltage to zero. The current doubles at the boundary, and the reflected wave again carries all incident energy backward.

### Impedance as a Property of the Medium

Electromagnetic waves do not possess their own independent impedance. Impedance is a strictly physical property of the copper geometry and the surrounding dielectric material.

The characteristic impedance of a trace dictates the strict mathematical ratio between voltage and current for any wave currently traveling on that specific geometry. A 50-ohm trace forces any propagating wave to maintain a ratio where voltage divided by current equals exactly 50 ohms. A reflected wave created by a localized defect immediately steps onto the trace heading backward. The trace takes complete physical control of that wave, locking its voltage and current into the 50-to-1 ratio demanded by the geometry.

The defect determines only the initial amplitude of the reflected wave. The reflection coefficient at the discontinuity dictates exactly how much voltage the defect rejects backward. Once launched, the reflected wave behaves exactly like a new signal traveling in the reverse direction. The physical geometry of the trace it currently occupies entirely defines its voltage-to-current relationship.

A reflected wave with a smaller voltage amplitude necessarily carries a proportionally smaller current. If a transmitter launches a 1-volt forward wave on a 50-ohm trace (producing 20 milliamps of forward current), and a parasitic via rejects 0.1 volts backward, the reflected wave's current is forced by the 50-ohm geometry to equal 2 milliamps ($0.1\text{V} / 50\Omega$). The reflected wave carries significantly less energy than the original forward wave.

## Architecture

### The Reflection as a Separate Electromagnetic Wave

A reflection is not the return current of the forward wave. A reflection is an entirely separate electromagnetic wave propagating in the backward direction.

The forward wavefront carries its own localized current loop: conduction current flows forward on the trace, displacement current bridges the dielectric at the wavefront location, and return current flows backward on the ground plane. This loop structure, described in the [Wave Propagation guide](01_Wave_Propagation_and_Transmission_Lines.md), closes at all times during forward propagation.

When the forward wavefront reaches an impedance discontinuity, the mismatch launches a new backward-traveling wave. This reflected wave possesses its own independent current loop: conduction current on the trace, displacement current through the dielectric at the reflected wavefront location, and return current on the ground plane. The reflected wave propagates backward toward the source, completely independent of the DC state established by the forward wave behind it.

### Ping-Pong Reflections and Energy Absorption

The reflected wave travels backward along the trace until it reaches the source. The driver transistor at the source possesses an internal resistance, typically between 10 and 30 ohms. The backward-traveling reflection encounters this internal source resistance as a physical boundary.

The reflection coefficient at the source determines how much of the returning wave is absorbed and how much re-reflects forward. If the source impedance matches the trace impedance, the source absorbs the returning wave completely and no re-reflection occurs. If the source impedance differs from $Z_0$, a portion of the wave re-reflects forward toward the load, and the process repeats.

The wave literally bounces back and forth between the source termination and the load termination. Each time the wave strikes a termination, the resistive element absorbs a fraction of the wave's electromagnetic energy and converts it permanently into thermal heat. The current of the arriving wave flows directly into the physical resistor material, and the energy dissipation destroys a portion of the wave amplitude.

The reflections become progressively smaller with each successive bounce. The exponentially decaying amplitude eventually drops below any measurable threshold, and the ping-ponging ceases.

### Settling to Steady State

The transient ping-pong process is the physical mechanism that bridges the gap between wave-propagation physics and DC circuit analysis.

When a voltage is first applied, the wavefront travels down the line, strikes the termination, and reflects backward. These reflections superimpose on one another as they bounce back and forth. The transient voltages ring down as the termination resistors absorb energy at each boundary.

Only after this infinite series of reflections converges does the entire line reach a uniform equipotential state. At that exact moment, the transient $Z_0$ behavior ceases. The voltage is identical at every point along the trace. No voltage gradient exists to drive a propagating wave. The system has reached DC equilibrium, and Ohm's law ($V = IR$) now perfectly describes the circuit.

The DC source acts as a constant-pressure reservoir holding the line at its intended voltage. The initial wavefront establishes this baseline. The reflections act as transient pressure ripples bouncing on top of that baseline. Once the ripples dissipate entirely into heat, the transmission line reaches a quiet steady state, held firmly at the source voltage.

Energy is lost to the DC resistance of the copper at all times, producing a voltage drop along the trace and generating heat. During the picosecond transient phase, however, the vast majority of the source energy is actively consumed by building the electric and magnetic fields in the surrounding dielectric, not by resistive heating.

## Worked Examples

### Open Circuit Response on a TDR

A time domain reflectometer contains an internal voltage source and an internal series resistor. The industry standard for this internal source resistance is exactly 50 ohms.

Connecting the TDR to a 50-ohm trace creates a simple voltage divider at the connector. The internal source generates a 1V step. The 1V source sits in series with the internal 50-ohm resistor, followed by the 50-ohm characteristic impedance of the trace. Equal resistances split the voltage evenly: 0.5V drops across the internal resistor as heat, and the remaining 0.5V launches onto the trace as an electromagnetic wave.

The TDR screen displays the voltage measured at the connector. It shows an instantaneous jump to 0.5V and remains flat at that level while the wavefront is actively traveling down a uniform 50-ohm trace. The ratio of voltage to current ($V/I = Z_0$) remains constant across the uniform geometry, so no reflections are generated during propagation.

If the far end of the trace is completely disconnected (an open circuit), the 0.5V wavefront hits the open boundary and reflects completely ($\rho = +1$). A +0.5V reflection travels backward toward the source. The TDR screen continues to display the 0.5V baseline until the exact moment this reflection arrives back at the connector. The returning +0.5V wave superimposes on the existing 0.5V baseline, and the screen jumps to 1.0V.

The returning wave then encounters the internal 50-ohm source termination. The perfect impedance match ($50\Omega$ source to $50\Omega$ trace) completely absorbs the returning wave energy. No further bouncing occurs. The system achieves steady state, holding the full 1V potential across the entire trace.

Turning the TDR on without connecting any trace at all causes the connector itself to act as an open circuit with infinite impedance. Zero current flows, so zero voltage drops across the internal 50-ohm resistor. The full 1V potential appears immediately at the connector with no intermediate 0.5V stair. The round-trip flight time is zero, and the TDR screen shows a flat line at 0V followed by a single sharp edge jumping directly to 1V.

The steepness of that edge is limited by the instrument's bandwidth. A perfectly vertical edge would require zero rise time, which mathematically demands summing sine waves extending to infinite frequencies. A high-end TDR with 20 GHz bandwidth can only generate harmonics up to that limit, so the edge takes a finite time (perhaps 20 picoseconds) to climb from 0V to 1V. The slight slope of the transition is a direct consequence of the instrument's finite frequency content.

### Impedance Bump and Return to Baseline

A localized impedance discontinuity, such as a narrow trace segment measuring only a few millimeters, demonstrates how the TDR maps physical structure to reflections.

A positive impedance bump (impedance higher than $Z_0$) produces a positive reflection coefficient. The reflected wave adds to the baseline, creating a voltage bump on the screen. A negative impedance dip (impedance lower than $Z_0$) produces a negative reflection coefficient. The reflected wave subtracts from the baseline, creating a voltage dip.

The voltage returns to the baseline after the defect for a straightforward reason: the defect has a finite physical length. The forward wavefront hits the start of the narrow section and begins generating a positive reflection backward. The wavefront requires only a few picoseconds to traverse the two-millimeter defect. Exiting the narrow section returns the wavefront to the properly designed 50-ohm trace, which generates zero reflections. The defect physically stopped producing reflected energy the exact moment the wavefront cleared the bottleneck. The TDR screen, which plots reflected energy arriving at the instrument against time, draws a bump and then returns to the flat 0.5V baseline.

## Edge Cases

### Masking and Spreading of Downstream Discontinuities

Multiple impedance discontinuities along a trace do not appear independently on a TDR measurement. The first discontinuity physically alters the interrogating wavefront, degrading the instrument's ability to characterize everything downstream.

A parasitic inductor early in the trace severely strips the high-frequency content from the forward-traveling wave. The inductor generates a back-EMF proportional to the rate of current change ($V = L \cdot dI/dt$). A fast, steep edge produces a large rate of change, triggering a strong inductive response that removes energy from the highest-frequency harmonics. The surviving wavefront continuing past the inductor possesses a much slower, rounded rising edge.

This degraded wavefront becomes the new interrogating signal for the remainder of the trace. Striking a second parasitic inductor further down the line with a slow, rounded edge produces a drastically different response. The slow edge possesses a small rate of change, so the second inductor generates only a weak opposing voltage. The TDR records this weak response as a small bump on the screen. The first discontinuity physically masks the true severity of all subsequent discontinuities.

The spatial resolution also degrades. A perfectly sharp voltage step hits a parasitic inductor instantaneously, and the inductor reacts with a massive, concentrated back-EMF spike. The TDR records this rapid event as a sharp, narrow feature. A degraded, rounded wavefront hits the same inductor gradually, producing a weak voltage spread out over a longer time interval. The TDR plots a wide, flattened mound on the screen instead of a sharp needle. The degraded rise time stretches out the physical duration of the interaction, smearing the feature and reducing the instrument's ability to pinpoint the defect's exact location.

This masking and spreading effect is one of the fundamental limitations of time domain reflectometry. A massive impedance error at the far end of a board might appear as a tiny perturbation on the TDR screen simply because the interrogating wavefront lost its high-frequency energy to discontinuities encountered earlier in the path.

### Parasitic Inductance and Capacitance Cancellation

Every millimeter of a trace possesses both capacitance and inductance simultaneously. Their continuous ratio defines the baseline characteristic impedance of the line. At a structural discontinuity, one parameter typically dominates the local geometry: a via introduces both extra metal area (capacitance) and vertical travel distance (inductance), but the proportions may not match the baseline ratio.

If a discontinuity introduces additional inductance and additional capacitance in the exact proportions required to maintain $Z_0 = \sqrt{L/C}$, the impedance remains matched. The TDR trace displays a flat line with no reflection, even though the physical geometry changed. Engineers exploit this phenomenon to optimize signal links. Deliberately routing a narrow, highly inductive trace segment adjacent to a wide, highly capacitive connector pad can maintain a uniform 50-ohm impedance profile through a region where either element alone would produce a severe mismatch.
