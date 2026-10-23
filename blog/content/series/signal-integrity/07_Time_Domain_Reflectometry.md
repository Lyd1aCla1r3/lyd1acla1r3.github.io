# Time Domain Reflectometry

<!-- SUMMARY: Time domain reflectometry (TDR) launches a fast step into a transmission line to record impedance mismatches. The analysis derives the spatial resolution limit of the incident edge, the masking effect of multiple reflections, and the closed-form area extraction of series inductance and shunt capacitance. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Ebook here.</a></em></p>

[Chapter 3](03_Impedance_Reflections_and_Termination.md) derived the reflection coefficient $\Gamma$ and its inversion to impedance, and [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) derived how the capacitance and inductance of a via reflect a fast edge. A time domain reflectometer (TDR) measures those reflections in the laboratory. The instrument launches a voltage step with a short rise time onto a transmission line, records the voltage at its own connector as a function of time, and interprets every deviation from the launched level as a reflection from an impedance change somewhere along the path.

The measurement rests on the wave propagation of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md). The step travels through the dielectric between the trace and the reference plane at the velocity $v_p = c/\sqrt{\epsilon_r}$, a reflection returns at the same velocity, and the delay between the launch and the return of a reflection therefore locates the impedance change along the line. The amplitude of the reflection identifies the size of the change, and its polarity identifies whether the structure is predominantly capacitive or inductive. A single measurement thus produces an impedance profile of the whole channel, with distance replaced by time along the horizontal axis.

The sections below establish the complete TDR measurement framework: the instrument architecture, the conversion from measured port voltage to characteristic impedance, and the time-domain signatures of the reactive structures from [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md). Subsequent sections derive the spatial resolution limit set by the step rise time, the closed-form extraction of capacitance and inductance from reflection area, and the masking and dispersion effects that obscure features far from the launch connector.

## Core Concepts

### The TDR Architecture: Source, Sampler, and Termination

A TDR consists of three functional elements that share one physical node at the instrument connector: a step generator, a series source resistor $R_S$, and a high-bandwidth sampling voltmeter. The source resistance is made equal to the reference impedance of the measurement, which is 50 Ω for the instruments considered here, so that $R_S = Z_0$ for a 50 Ω line.

The step generator produces an open-circuit amplitude $V_S$. Assume $V_S = 1$ V, which keeps the arithmetic visible, although the amplitude differs between instruments. The source resistor and the line form the voltage divider of [Chapter 3](03_Impedance_Reflections_and_Termination.md), and the amplitude of the launched wave is:

$$V_{inc} = V_S\,\frac{Z_0}{R_S + Z_0} = 0.5\ \text{V}$$

The voltmeter reads the voltage at the connector. The line presents a resistance equal to $Z_0$ at the connector, because the ratio of voltage to current for a single wave in one direction equals $Z_0$ ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)), while the wavefront travels along a uniform 50 Ω line. The display therefore stays flat at 0.5 V until a reflection arrives.

The source resistor has a second function. A returning wave reaches the connector and meets $R_S$ with the step generator acting as a constant voltage, so the source reflection coefficient of Chapter 3 applies:

$$\Gamma_S = \frac{R_S - Z_0}{R_S + Z_0} = 0$$

A source matched to the line reflects nothing, and every returning wave is absorbed in $R_S$ as heat. Each reflection therefore appears at the display once, which keeps the later part of the waveform free of re-reflections from the connector.

The voltmeter is a sampling oscilloscope that works in equivalent time. The step generator repeats the step many times, and each repetition samples the voltage once, at a delay that is a small increment later than the previous sample. The waveform builds from many repetitions, so the device under test must repeat the same response for every step, which holds for a passive linear board. The sampling method is the reason a TDR can reach tens of gigahertz of bandwidth with a simple sampler.

### Velocity of Propagation and Distance Measurement

[Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) derived the velocity $v_p = c/\sqrt{\epsilon_r}$ and the resulting delay of FR4 ($\epsilon_r \approx 4.2$), which is about 6.8 ps per millimeter or 170 ps per inch. A TDR measures time, and the wave must travel to a discontinuity and back, so the distance to a feature at round-trip time $\Delta t$ is:

$$d = \frac{v_p\,\Delta t}{2}$$

The instrument does not know the dielectric constant of the board. The user supplies a velocity factor $V_f = v_p/c$ or a dielectric constant $D_k$, and the instrument uses it to convert time to distance. An incorrect value changes the horizontal scale only. The vertical scale depends on the ratio of two voltages, which the instrument measures directly, so the impedance readings stay correct. A board of known length provides a calibration: the measured delay of a trace of known physical length gives $v_p$, and from it $\epsilon_r$, for that board.

The propagation velocity changes along a path that crosses different materials. A wave that leaves an FR4 trace ($D_k = 4.0$) and enters a PTFE coaxial connector ($D_k = 2.1$) travels faster by the factor $\sqrt{4.0/2.1} = 1.38$. An instrument configured for FR4 reports a connector region that is 1.38 times shorter than its physical length, so a 20 mm coaxial section appears as 14.5 mm, and every feature beyond it shifts earlier on the distance axis by the same offset.

For a short via or connector pad, the round-trip delay is on the order of picoseconds and the resulting distance offset is negligible. A long test cable with a different dielectric constant displaces all downstream board features by a large offset, requiring the instrument to de-embed or configure the cable and board velocity factors separately.

### The Reflection Coefficient on the TDR Display

[Chapter 3](03_Impedance_Reflections_and_Termination.md) derived $\Gamma = (Z_L - Z_0)/(Z_L + Z_0)$ and the three terminations that bound its range. The display shows each of them as a level of the total voltage, which is the sum of the incident wave and the reflected wave that has returned to the connector:

- **Matched load (`Γ = 0`):** The display stays at 0.5 V indefinitely because no reflected wave returns to the port.
- **Open circuit (`Γ = +1`):** The reflected wave matches the amplitude and polarity of the incident wave. The display steps from 0.5 V to 1.0 V at the round-trip time, and the source resistor $R_S$ absorbs the returning wave, leaving the line at the open-circuit voltage $V_S$ with zero current.
- **Short circuit (`Γ = -1`):** The reflected wave cancels the incident wave, and the display drops from 0.5 V to 0 V at the round-trip time, matching the zero-voltage boundary of the short.

A connector with nothing attached is an open circuit at zero distance. No current flows through $R_S$, the voltage across it is zero, and the display shows the full 1 V immediately, with no intermediate level at 0.5 V, because the round-trip time is zero.

The display shows voltage, and the reflection coefficient is a ratio of voltages, and the fraction of power that returns is $\Gamma^2$ ([Chapter 3](03_Impedance_Reflections_and_Termination.md)), so a reflection of 0.2 on the screen corresponds to 4 percent of the incident power.

### From Measured Voltage to Impedance

The instrument measures the total voltage on the line at its port, the sum of the incident and reflected voltages:

$$v(t) = V_{inc} + v_r(t)$$

The incident voltage $V_{inc}$ is the launched wave, which is 0.5 V for the divider above and not the 1 V of the open-circuit source, because $R_S$ and the line share the source voltage. Subtracting the launched wave and normalizing by it isolates the reflection coefficient at each instant:

$$\Gamma(t) = \frac{v(t) - V_{inc}}{V_{inc}}$$

The inversion of [Chapter 3](03_Impedance_Reflections_and_Termination.md) converts each value of $\Gamma(t)$ to the impedance that produced it:

$$Z(t) = Z_0\,\frac{1 + \Gamma(t)}{1 - \Gamma(t)}$$

The same result follows from the divider alone. Before any reflection from a later feature has returned, the line looks like an impedance $Z$ to the source, and the connector voltage is $v = V_S Z/(R_S + Z)$. Solving for $Z$ gives $Z = R_S\,v/(V_S - v)$, which equals $Z_0\,v/(V_S - v)$ for $R_S = Z_0$. Substituting $v = V_{inc}(1 + \Gamma) = V_S(1 + \Gamma)/2$ into this expression reproduces $Z_0(1 + \Gamma)/(1 - \Gamma)$.

Assume the display reads 0.6 V at some instant. The reflection coefficient is $(0.6 - 0.5)/0.5 = 0.2$, the impedance is $50 \cdot 1.2/0.8 = 75\ \Omega$, and the divider form gives $50 \cdot 0.6/(1 - 0.6) = 75\ \Omega$ as well. The display therefore shows a step from the 0.5 V baseline to 0.6 V when the line changes from 50 Ω to 75 Ω.

The vertical accuracy of the impedance readout depends on the accuracy of the voltage readout. Differentiating $Z = Z_0\,v/(V_S - v)$ and evaluating at $v = V_S/2$ gives $\Delta Z/Z = 2\,\Delta v/v$, so a 1 percent error in the voltage at the 50 Ω level produces a 2 percent error in the impedance. The factor 2 explains why the instrument is calibrated against a reference of known impedance.

The impedance profile $Z(t)$ is an apparent impedance. It treats the wave at every point as if it had the full launched amplitude, which holds until an earlier reflection has depleted the wave. The Edge Cases section quantifies the error.

### The TDR Staircase: What the Screen Displays

The screen does not show a side view of the board. The TDR is a voltmeter fixed at one physical location, the connector, and its horizontal axis is time, which maps to round-trip distance through $d = v_p\Delta t/2$. Consider a 12 inch FR4 trace with an open circuit at the far end. The one-way delay is $12 \cdot 170 = 2.04$ ns and the round trip is 4.08 ns.

1. **$t < 0$:** The display shows a flat line at 0 V.
2. **$t = 0$:** The step generator fires, and the voltage at the connector rises to 0.5 V, the divider level.
3. **$0 < t < 4.08$ ns:** The wavefront travels to the open end and the reflection returns. The line presents 50 Ω to the source throughout this interval, so the display stays at 0.5 V. The width of this plateau is the round-trip time of the trace.
4. **$t = 4.08$ ns:** The reflection of $+0.5$ V arrives and adds to the existing 0.5 V, and the display steps to 1.0 V.
5. **$t > 4.08$ ns:** The source absorbs the reflection, and the display stays at 1.0 V.

The staircase has two steps, and the width of the first plateau gives the electrical length of the trace: $d = v_p \cdot 4.08\ \text{ns}/2 = 12$ in.

## Architecture

### Capacitive Dips and Inductive Bumps

A structure with a small reactive impedance reflects only the part of the edge that changes in time, and the display records the reflection with a polarity that identifies the type of the structure. [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) derived the result for each type, for an incident edge $u(t)$ that is slow compared with the time constant of the structure:

$$v_r \approx -\tau_C\,\dot u \ \ \text{(shunt capacitance, } \tau_C = Z_0 C/2\text{)}, \qquad v_r \approx +\tau_L\,\dot u \ \ \text{(series inductance, } \tau_L = L/(2Z_0)\text{)}$$

A shunt capacitance reflects a negative pulse and produces a downward dip on the display, corresponding to a local impedance below $Z_0$. The uncharged capacitor draws current from the arriving transition as a transient short circuit, with a current magnitude proportional to the voltage slew rate $du/dt$.

A series inductance reflects a positive pulse and produces an upward bump on the display, corresponding to a local impedance above $Z_0$. The inductance opposes the change in line current with a back-EMF of $L\,di/dt$, which returns toward the source as a positive voltage reflection. Both reflection amplitudes scale directly with the slope of the incident edge: a slow step with a long rise time produces a small reflection, whereas a fast step produces a large peak, matching the high-frequency reflection behavior $\Gamma(f)$ derived in [Chapter 3](03_Impedance_Reflections_and_Termination.md).

The numbers of Chapter 6 give the size of each feature on the display. The 0.37 pF anti-pad of a 62 mil via, probed by a 30 ps edge, produces a dip of $-0.30$, which is an impedance of 27 Ω at the minimum. Its 1.33 nH barrel produces a bump of $+0.40$, an impedance of 116 Ω at the maximum. The 0.21 nH neck of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md), probed by a 15 ps edge, has $\tau_L = 0.21\ \text{nH}/100\ \Omega = 2.1$ ps and produces a bump of $(2.1/15)(1 - e^{-15/2.1}) = +0.14$, an impedance of 66 Ω. The neck also removes capacitance, so the measured bump is smaller than this inductance-only estimate.

The same signatures appear for distributed features. A section of trace that is wider than the rest has more capacitance per unit length and a lower impedance, and it appears as a plateau below the baseline. A narrower section appears as a plateau above the baseline. The lumped dip or bump is the limit in which the section is shorter than the edge, so that the plateau does not reach its full height. The next two sections describe the plateau and its limit.

### Returning to the Baseline After a Defect

A defect has a finite length, so the display returns to the baseline after it. Consider a section of impedance $Z_1$ and one-way delay $T_d$ in an otherwise uniform 50 Ω line. The wavefront reaches the entry of the section and generates a reflection with coefficient $\Gamma_1 = (Z_1 - Z_0)/(Z_1 + Z_0)$ that returns to the connector. The wavefront then travels through the section to the exit, where the impedance returns to $Z_0$ and the reflection coefficient for a wave arriving from the section is:

$$\Gamma_{exit} = \frac{Z_0 - Z_1}{Z_0 + Z_1} = -\Gamma_1$$

The exit reflection has the opposite sign and arrives at the connector $2T_d$ later than the entry reflection. The display therefore stays at the level of the entry reflection for a time $2T_d$ and then returns toward the baseline, because the second reflection cancels the first. The width of the plateau gives the length of the section:

$$\text{Length} = v_p\,\frac{\Delta t}{2}$$

The uniform 50 Ω line beyond the section generates no reflection and the display stays at the baseline. The TDR plots voltage, which is the sum of the incident wave and the reflections that have returned, so the return to the baseline is the end of the reflected voltage and not the end of a stored quantity. The section generates a reflection only while the edge crosses its two boundaries. The Worked Examples section computes the plateau of a 75 Ω section and shows that a section shorter than the edge produces a lower, shorter bump.

### The Impedance Cancellation Principle

[Chapter 3](03_Impedance_Reflections_and_Termination.md) showed that a discontinuity that adds inductance and capacitance in the proportion $\Delta L'/\Delta C' = Z_0^2$ leaves the impedance unchanged, and [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) derived the lumped condition $L = Z_0^2 C$ in the time domain as the equality of the time constants $\tau_L = \tau_C$. The display of such a structure is flat, because no reflection occurs, but the structure is slower than the surrounding line, so the flat region is displaced later by the extra delay. A flat trace therefore does not prove that the geometry is uniform, and the equal areas of the dip and the bump in the next sections reveal the cancellation.

## Worked Examples

### Spatial Resolution: Why Rise Time Limits What the TDR Can See

The step of a TDR has a finite rise time $t_r$, the 10 to 90 percent transition time, and this rise time sets the smallest separation of two features that the display distinguishes. The incident edge occupies a length of line:

$$l_{edge} = v_p\,t_r$$

An edge of 30 ps on FR4 ($v_p = 1/(6.8\ \text{ps/mm})$ from Chapter 1) occupies 4.4 mm. Consider two discontinuities, Point A and Point B, separated by a distance $d$. The tip of the edge reaches Point A at $t = 0$, and Point A begins to reflect. The reflection from Point A needs $t_r$ to reach its full value, because the incident edge needs $t_r$ to reach its full amplitude. The edge continues to Point B, which takes $d/v_p$, and the reflection from Point B travels back across the same distance. The second reflection therefore arrives behind the first by:

$$\Delta t = \frac{2d}{v_p}$$

The display shows two separate features only if the first has completed its transition before the second begins, which requires $2d/v_p > t_r$. Solving for the separation gives:

$$d > \frac{v_p\,t_r}{2} = \frac{l_{edge}}{2}$$

Two discontinuities are resolved when their separation exceeds half the length of the edge. A closer pair produces overlapping echoes that merge into one feature. The criterion is a rule of thumb, because the visibility of the two features also depends on their relative heights and on the noise.

[Chapter 2](02_Frequency_Content_of_Digital_Signals.md) derived the relation $t_r \approx 0.35/f_{3dB}$ between rise time and the bandwidth of a single-pole system, and noted that instruments with a sharp-cutoff response have $t_r \approx 0.45/f_{max}$. Using the single-pole value, the resolution in terms of the instrument bandwidth is $d_{min} = 0.175\,v_p/f_{3dB}$.

A TDR with a 15 ps edge has $l_{edge} = 2.2$ mm and resolves features separated by 1.1 mm. A 30 ps edge resolves 2.2 mm. A 20 GHz instrument has $t_r \approx 17.5$ ps and resolves 1.3 mm on FR4. The criterion reappears in the next example, where the same condition decides whether a short section reaches its full impedance on the display.

### A 75 Ω Section on the Display

Assume a 1 V source and a 50 Ω source resistor, so that $V_{inc} = 0.5$ V, and a section of 75 Ω trace of one-way delay $T_d$ in a 50 Ω line that ends in a matched load. The entry reflection coefficient is:

$$\Gamma_1 = \frac{75 - 50}{75 + 50} = 0.2$$

The reflected wave at the entry is $0.2 \cdot 0.5 = 0.1$ V, so the display steps to $0.5 + 0.1 = 0.6$ V across a long section, corresponding to $Z = 50 \cdot 0.6/(1 - 0.6) = 75\ \Omega$. Meanwhile, a transmitted wave of amplitude $\tau V_{inc} = 1.2 \cdot 0.5 = 0.6$ V continues into the 75 Ω section. At the exit boundary back to 50 Ω, the reflection coefficient is $-0.2$, launching a $-0.12$ V wave backward toward the entry.

Crossing the entry boundary from the 75 Ω side into the 50 Ω line multiplies that wave by the transmission coefficient $1 + (-0.2) = 0.8$, delivering $-0.12 \cdot 0.8 = -0.096$ V to the connector at time $2T_d$ after the first step. The display drops to $0.6 - 0.096 = 0.504$ V rather than returning all the way to 0.5 V, because a portion of the backward wave reflects off the entry boundary from the inside and reverberates within the 75 Ω section. Each subsequent internal round trip scales the escaping wave by $(-0.2)^2 = 0.04$, stepping the display through 0.504 V, 0.50016 V, and 0.500006 V toward 0.5 V. Immediately after the 75 Ω section, the matched 50 Ω line reads an apparent impedance of $50 \cdot 0.504/(1 - 0.504) = 50.8\ \Omega$, illustrating the upstream masking effect analyzed in the Edge Cases section.

A section shorter than the edge behaves differently. To first order in $\Gamma$, the reflected voltage is the incident edge, scaled by $\Gamma_1$, minus a copy of the same edge delayed by $2T_d$, scaled by $\Gamma_1$ as well:

$$v_r(t) \approx \Gamma_1 V_{inc}\,[\,u(t) - u(t - 2T_d)\,]$$

In this expression $u(t)$ denotes the normalized edge. For a section of one-way delay 7.5 ps (1.1 mm of FR4) and a 30 ps linear ramp, the largest difference between the ramp and its delayed copy is $15/30 = 0.5$, which occurs for $2T_d = 15$ ps. The reflection reaches half its long-section value, so $\Gamma = 0.1$ and the apparent impedance is $50 \cdot 1.1/0.9 = 61\ \Omega$. A section whose round-trip delay exceeds the rise time ($2T_d \geq t_r$) reaches the full 75 Ω, which is the resolution criterion of the previous example.

### Quantitative Parasitic Extraction: The Area Under the Curve

The waveform contains enough information to extract the capacitance or the inductance of a lumped discontinuity. Chapter 6 derived the equations of the two structures without any approximation of small reflection. For a series inductance, with an edge $u(t)$ that rises to $V_{inc}$ and a reflected wave $v_r(t)$:

$$\tau_L\,\dot v_r + v_r = \tau_L\,\dot u, \qquad \tau_L = \frac{L}{2Z_0}$$

Integrating both sides over the whole duration of the reflection, from before the edge to long after it, replaces each term by its accumulated value:

$$\tau_L\,[v_r]_{0}^{\infty} + \int_0^{\infty} v_r\,dt = \tau_L\,[u]_{0}^{\infty}$$

The reflection vanishes before the edge arrives and after the reflection has ended, because the inductor is a short circuit for steady currents, so $[v_r]_0^\infty = 0$. The edge rises from 0 to $V_{inc}$, so $[u]_0^\infty = V_{inc}$. Dividing by $V_{inc}$ and using $\Gamma(t) = v_r(t)/V_{inc}$:

$$\int_0^{\infty} \Gamma(t)\,dt = \tau_L = \frac{L}{2Z_0} \quad \Rightarrow \quad L = 2Z_0 \int \Gamma(t)\,dt$$

The shunt capacitance follows from its equation, $\tau_C\,\dot v_r + v_r = -\tau_C\,\dot u$, by the same steps, with the sign of the right-hand side reversed:

$$\int_0^{\infty} \Gamma(t)\,dt = -\tau_C = -\frac{Z_0 C}{2} \quad \Rightarrow \quad C = \frac{2}{Z_0}\int \bigl(-\Gamma(t)\bigr)\,dt$$

The area is taken on the $\Gamma(t)$ axis, in seconds, and not on the impedance axis, because the conversion to impedance is nonlinear. The derivation requires only that the element is lumped (shorter than the edge), isolated from other features, and preceded by a line that delivers the full incident amplitude.

The area does not depend on the rise time of the edge, because the edge entered the integral only through its total change $V_{inc}$. A faster edge produces a taller and narrower reflection, and a slower edge produces a lower and wider one with the same area. For the 0.37 pF anti-pad, $\tau_C = 9.25$ ps, and the ramp solution of Chapter 6 gives the peak of the dip for three edges:

| Edge Rise Time (`t_r`) | Peak Reflection (`Γ`) | Minimum Impedance |
|---|---|---|
| `15 ps` | `-0.49` | `17 Ω` |
| `30 ps` | `-0.30` | `27 Ω` |
| `100 ps` | `-0.09` | `42 Ω` |

The three dips exhibit markedly different peak depths, yet each encloses the identical area $\tau_C = 9.25$ ps, yielding $C = 2 \cdot 9.25\ \text{ps}/50\ \Omega = 0.37$ pF. The physical capacitance does not change between the three measurements; a slower edge reduces only the peak depth on the display, making peak impedance an unreliable metric for a lumped parasitic unless the test rise time is specified alongside it.

Any low-pass filter in the instrument, test cable, or trace preserves the integrated area as long as its DC gain equals unity, because the integral of a convolution equals the product of the individual integrals. Area extraction therefore remains accurate even when the measurement path slows the displayed reflection below the launched rise time.

The measurement works in reverse for the neck of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md). A measured bump with area 2.1 ps on the $\Gamma(t)$ axis gives $L = 2 \cdot 50 \cdot 2.1\ \text{ps} = 0.21$ nH.

### The Order of a Bump and a Dip

The display shows the features in the order the edge meets them. Consider a series inductance $L = 1.33$ nH and a shunt capacitance $C = 0.37$ pF placed next to each other on a 50 Ω line, probed by a 30 ps linear ramp. The equations of both elements, solved numerically for the two orders, give the following display:

| Order Along the Line | First Feature | Second Feature |
|---|---|---|
| **Inductance first** | Bump of `+0.29` at `22 ps` | Dip of `-0.12` at `58 ps` |
| **Capacitance first** | Dip of `-0.20` at `14 ps` | Bump of `+0.25` at `50 ps` |

The times are measured from the instant the edge begins to arrive at the structure. The peaks differ from the isolated values of the previous example ($+0.40$ and $-0.30$), because the edge reaching the second element has already been modified by the first, and because the two reflections overlap in time. The net area is the same for both orders and equals $\tau_L - \tau_C = 13.3 - 9.25 = 4.05$ ps, which the numerical integral confirms. The area of a pair that overlaps in time is the difference of the two time constants, and it vanishes for $L = Z_0^2 C$, the cancellation condition of Chapter 3.

The order identifies the sequence along the signal path. A dip followed by a bump indicates a capacitive feature in front of an inductive one, and the reverse indicates the opposite order. A via modeled as a pad capacitance followed by a barrel inductance therefore shows the dip first.

## Edge Cases

### Rise Time Degradation and the Need for a Rising Edge

A constant voltage contains no time marker, so a DC level reveals only the total resistance of the path. The instrument measures distance by timing a change, and the rising edge is the marker that starts the clock. The sharpness of the edge matters as well. A step has a continuous spectrum, not a set of harmonics ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)), and the rise time sets the frequency up to which the spectrum has significant content. A 10 ps transition has a bandwidth of about $0.35/10\ \text{ps} = 35$ GHz. The reflections of Chapter 6 are proportional to the slope of the edge, so a slow edge passes over a small parasitic and reflects little.

The instrument limits the achievable rise time. A TDR with a 20 GHz bandwidth has $t_r \approx 0.35/20\ \text{GHz} = 17.5$ ps. An edge with zero rise time would need an infinite bandwidth, which no instrument provides.

### Masking: Upstream Discontinuities Reduce the Incident Wave

Each reflection takes energy from the forward wave, so the wave that reaches a downstream feature is smaller than the launched wave, and the reflection returns through the same upstream mismatch. Consider a mismatch with reflection coefficient $\Gamma_1$ at the entry of a section. The wave transmitted into the section has amplitude $(1 + \Gamma_1)V_{inc}$. A downstream feature with local reflection coefficient $\Gamma_2$, referenced to the impedance of the section, returns $\Gamma_2(1 + \Gamma_1)V_{inc}$. This wave crosses the same boundary in the opposite direction, where the reflection coefficient is $-\Gamma_1$ and the transmission coefficient is $1 - \Gamma_1$. The amplitude at the connector is:

$$v_{2} = V_{inc}\,\Gamma_2\,(1 + \Gamma_1)(1 - \Gamma_1) = V_{inc}\,\Gamma_2\,(1 - \Gamma_1^2)$$

The factor $1 - \Gamma_1^2$ scales every reflection from beyond the mismatch:

| Upstream Reflection (`Γ_1`) | Transmission Factor (`1 - Γ_1^2`) | Apparent Reflection of `+0.20` Feature | Apparent Impedance |
|---|---|---|---|
| `0.2` | `0.96` | `0.192` | `73.8 Ω` |
| `0.5` | `0.75` | `0.150` | `67.6 Ω` |
| `0.9` | `0.19` | `0.038` | `54.0 Ω` |

The instrument computes the impedance of every downstream feature under the assumption that the incident wave arrives with the full launched amplitude $V_{inc}$. A downstream 75 Ω discontinuity ($\Gamma_2 = 0.20$) preceded by an upstream mismatch of $\Gamma_1 = 0.5$ returns an attenuated reflection of $0.20 \cdot 0.75 = 0.15$, which the instrument displays as an apparent impedance of 68 Ω. Behind a severe upstream mismatch of $\Gamma_1 = 0.9$, the same 75 Ω feature returns only $0.20 \cdot 0.19 = 0.038$, reading as 54 Ω and disappearing into the baseline.

Accurate TDR diagnosis therefore requires identifying and accounting for the first large mismatch before interpreting any readings beyond it. Distributed series and shunt losses along the trace produce a similar compression by attenuating both the forward step and the returning echo.

### Spreading: Loss and Reactive Discontinuities Slow the Edge

The edge that reaches a downstream feature is slower than the launched edge, so the feature appears wider and shallower than an identical feature near the connector. Two mechanisms slow the edge, and a shunt capacitance acts as a single-pole low-pass element: [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) showed that an ideal step passing the 0.37 pF anti-pad emerges with a 10 to 90 percent rise time of $2.2\,\tau_C = 20$ ps. A series inductance slows the edge in the same way with $\tau_L$.

The line itself slows the edge through the frequency-dependent loss of [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md). The loss constants of that chapter for FR4 (conductor 0.20 dB per inch and dielectric 0.47 dB per inch at 5 GHz, scaling as $\sqrt f$ and $f$) define a transfer function, and a causal (minimum-phase) response with that magnitude applied to a 20 ps edge gives the following rise times, computed numerically:

| Path Distance Traveled | 10% to 90% Rise Time (`t_r`) |
|---|---|
| `0 in` | `20 ps` |
| `1 in` | `29 ps` |
| `3 in` | `69 ps` |
| `6 in` | `149 ps` |
| `12 in` | `342 ps` |
| `24 in` | `768 ps` |

The numbers use $\tan\delta = 0.02$ and smooth copper, and they provide the reference benchmark across this series for the degradation of an edge on FR4. The distance in the table is the total path of the edge, so a feature 3 in downstream is observed after the edge has traveled 6 in, out and back, and its echo has the 149 ps rise time of the 6 in row. The resolution of that echo is $0.147\ \text{mm/ps} \cdot 149\ \text{ps}/2 = 11$ mm, about ten times coarser than the 1.1 mm resolution at the connector.

The same inductance appears different when probed by different edges. A 1 nH inductance has $\tau_L = 10$ ps. A 30 ps edge reflects a peak of $(10/30)(1 - e^{-3}) = +0.32$, and a 100 ps edge reflects $(10/100)(1 - e^{-10}) = +0.10$. The area of both reflections is the same $\tau_L = 10$ ps, which is the reason the extraction of the previous section stays valid, as long as the slower edge is accounted for by integrating the whole reflection and not by reading its peak.

### The Peeling Algorithm

The peeling algorithm, also called layer peeling or impedance profile deconvolution, is a numerical method that corrects the masking of the previous sections. It runs on the measured waveform and does not change anything on the board. Several analysis tools implement it, including the physical-layer test software of instrument vendors, and the algorithm is a generic inverse scattering method that does not belong to a single product.

Consider a line that consists of successive sections, each with a delay equal to a time step of the measurement. The first sample of the reflection, taken at the first interface, is the reflection coefficient $\Gamma_1$ of that interface and is already correct, because the wave has crossed nothing before it. The second sample comes from the next interface and has crossed the first interface twice, so its true coefficient follows from the masking factor above:

$$\Gamma_2 = \frac{r_2}{1 - \Gamma_1^2}$$

The same step applies to every later sample. The reading $r_k$ is first corrected for the multiple reflections that the sections already identified would generate at that time, and the result is divided by the product of the factors $1 - \Gamma_j^2$ of all earlier interfaces, which restores the amplitude of the wave that reached the interface:

$$\Gamma_k = \frac{r_k^{\,\prime}}{\prod_{j<k}\bigl(1 - \Gamma_j^2\bigr)}$$

The method therefore removes the cumulative amplitude loss and the phantom features that result from reflections bouncing between two interfaces. It cannot restore resolution that the instrument bandwidth has removed. A lossy line requires a loss model, and the division by a product of factors that decreases with distance amplifies the noise of the later samples. The result is the impedance profile that each section would show if it were measured alone, subject to those limits.

### Where the Time Domain Stops: Separating Inductance and Capacitance

The TDR identifies $Z_0$ from the longest flat region of the display. On that region the distributed inductance and capacitance are in the ratio $Z_0^2 = L'/C'$ and produce no reflection, so the display shows only the ratio and not the two quantities separately. The delay of the region gives their product ($LC = 1/v_p^2$ per unit length), so the pair is fixed by the two readings.

The extraction of a discrete $L$ and $C$ is limited by the resolution of the instrument. A dip and a bump that are separated in time by more than the resolution show two areas, one for $C$ and one for $L$. A pair that overlaps within the resolution, as in the previous example, reports only the net area $\tau_L - \tau_C$, from which the individual values cannot be recovered, and a pair with $L = Z_0^2 C$ shows no area at all. The time domain measures the net signature of a cluster of structures within the resolution of the edge and does not separate their parts in space.

The frequency domain resolves this overlap ambiguity because a complex reflection coefficient measured across frequency distinguishes series inductance from shunt capacitance by phase angle. [Chapter 8](08_S_Parameters_and_VNA.md) defines the vector network analyzer measurement of $S_{11} = \Gamma(f)$ and derives the mathematical transformation from a TDR step response to $S_{11}$: differentiating the step response yields the impulse response, and the Fourier transform of that impulse response produces $S_{11}(f)$.

[Chapter 9](09_Smith_Charts.md) then maps $S_{11}(f)$ onto the Smith chart, separating inductive and capacitive reflections into opposite hemispheres. Together, those two chapters show how measuring reflection directly in the frequency domain overcomes the spatial resolution ceiling of a time-domain step.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Ebook here.</a></em></p>
