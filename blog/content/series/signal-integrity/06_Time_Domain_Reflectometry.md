# Time Domain Reflectometry

<!-- SUMMARY: Time domain reflectometry (TDR) launches a fast electrical step into a transmission line and measures the reflected waveform to map impedance variations along the physical path. This guide covers the measurement physics, instrument architecture, and interpretation of TDR impedance profiles for PCB and connector characterization. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

A time domain reflectometer is an electromagnetic wave instrument. It launches a fast voltage step onto a transmission line and records the echoes that return from impedance discontinuities along the path. The measurement is conceptually identical to sonar or radar: a known pulse is transmitted, the system waits for reflections, and the arrival time and amplitude of each returning echo reveal the location and severity of every structural anomaly in the channel.

The physical foundation is wave propagation. The incident step travels through the dielectric material between the trace and the ground plane at a velocity governed by the dielectric constant ($v_p = c / \sqrt{\epsilon_r}$). When this wavefront encounters a change in characteristic impedance, a portion of the wave energy reflects backward while the remainder continues forward. The TDR instrument sitting at the source measures the total voltage at the connector over time, extracting the reflection coefficient from the difference between the measured voltage and the known incident step. The algebraic inversion of the reflection coefficient equation converts each measured voltage perturbation into a local impedance value, producing a continuous impedance profile of the entire channel from a single measurement event.

The result is a spatial map of the transmission line's impedance as a function of physical distance. Every via, connector, trace width change, reference plane gap, and termination discontinuity produces a distinct signature on the TDR display. This guide covers the complete instrument architecture, the physics of reflection and impedance translation, the mathematical derivation of spatial resolution limits, quantitative parasitic extraction from the TDR waveform, and the peeling algorithm that corrects for cumulative wavefront degradation.

## Core Concepts

### The TDR Architecture: Source, Sampler, and Termination

A TDR consists of three functional elements sharing a single physical node at the instrument connector: an internal voltage source (step generator), an internal series resistor, and a high-bandwidth sampling oscilloscope.

The industry standard for the internal source resistance ($R_S$) is exactly 50 ohms. Connecting the TDR to a PCB trace physically links this internal 50-ohm source to the transmission line's characteristic impedance ($Z_0$). For a properly designed 50-ohm trace, the entire system forms a simple voltage divider at the connector.

The internal source generates a clean 1V step. This 1V potential divides across two equal resistances in series: the internal 50-ohm resistor and the 50-ohm active impedance of the trace. Equal resistances split the voltage evenly. Exactly 0.5V drops across the internal TDR resistor as heat, and the remaining 0.5V launches onto the trace as an electromagnetic wave.

The TDR screen displays the voltage measured precisely at the connector. It shows an instantaneous jump to 0.5V. The screen remains perfectly flat at 0.5V while the wavefront is actively traveling down a uniform 50-ohm trace. The required ratio of voltage to current ($V/I = Z_0$) remains constant across the uniform copper geometry, producing zero reflections during propagation.

The internal 50-ohm resistor serves a second critical function beyond forming the voltage divider. When a reflection returns from a downstream discontinuity, the backward-traveling wave encounters this 50-ohm resistor at the source. The arriving wave perceives the resistor as a perfect physical continuation of the 50-ohm trace. Encountering zero change in impedance prevents any new reflections from occurring at the connector boundary. The electrical current of the returning wave flows directly into the physical resistor material, converting the electromagnetic energy into thermal heat. The entire reflection is absorbed, preventing it from bouncing forward again and contaminating the measurement of the rest of the trace.

### Velocity of Propagation and Distance Measurement

The electromagnetic wave propagates through the dielectric at a velocity determined by the dielectric constant:

$$v_p = \frac{c}{\sqrt{\epsilon_r}}$$

Standard FR4 has a dielectric constant of approximately 4.0, reducing the propagation velocity to roughly half the speed of light, or about six inches per nanosecond. Lower-loss laminates such as Megtron 6 have lower dielectric constants (around 3.6), permitting slightly faster propagation.

TDR operates on time of flight. The instrument launches the step, starts a timer, and waits for the echo. The wave must travel to the discontinuity and back, so the distance formula accounts for the round trip:

$$d = \frac{v_p \cdot \Delta t}{2}$$

The instrument does not know the dielectric constant of the board under test. The user interface provides a setting for velocity factor ($V_f$) or dielectric constant ($D_k$) that must be configured manually. Entering the wrong value has a specific consequence: the impedance readings on the vertical axis remain perfectly correct (the reflection coefficient depends only on the voltage ratio, which is measured directly), but the distance scale on the horizontal axis is warped. If the true dielectric constant is unknown, a practical calibration technique is available: measure a trace of physically known length, record the time delay, and calculate the exact $D_k$ of the fabricated board from the measured flight time.

Varying dielectrics along the signal path introduce cumulative distance error. A wavefront leaving an FR4 trace ($D_k = 4.0$) and passing through a coaxial connector (Teflon, $D_k = 2.1$) accelerates through the connector region. If the TDR assumes a constant velocity for the entire measurement, the spatial X-axis will be distorted after the first material transition. Standard TDR instruments accept this minor error for physically short transitions like vias or connectors, where the time error is measured in single-digit picoseconds. Transitioning to a long cable or substrate with a substantially different dielectric constant, however, will noticeably skew all downstream distance measurements.

### The Reflection Coefficient

When the incident step encounters an impedance mismatch, the fraction of voltage that reflects backward is governed by the reflection coefficient:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

$Z_0$ is the transmission line's characteristic impedance (the 50-ohm baseline), and $Z_L$ is the impedance of the discontinuity.

Three canonical cases define the extremes of TDR behavior:

**Perfectly matched load ($Z_L = 50\Omega$):** $\Gamma = \frac{50 - 50}{50 + 50} = 0$. No reflection occurs. The energy is entirely absorbed by the load. The TDR screen displays a flat 0.5V line extending indefinitely.

**Open circuit ($Z_L = \infty$):** $\Gamma = \frac{\infty - 50}{\infty + 50} = +1$. 100% of the voltage reflects with a positive sign. The TDR screen, which has been displaying a steady 0.5V, abruptly jumps to 1.0V at the moment the full positive reflection returns. The returning wave encounters the internal 50-ohm source termination and is completely absorbed. The system achieves steady state at 1.0V, holding the full internal source potential across the entire trace length.

**Short circuit ($Z_L = 0$):** $\Gamma = \frac{0 - 50}{0 + 50} = -1$. 100% of the voltage reflects with an inverted (negative) sign. The TDR screen drops from 0.5V to 0V.

Turning the TDR on without connecting any trace at all causes the connector itself to act as an open circuit. Zero current flows through the internal 50-ohm resistor, so zero voltage drops across it. The full 1V potential from the internal source appears immediately at the connector with no intermediate 0.5V stair, because the round-trip flight time is zero.

### From Measured Voltage to Impedance

The TDR oscilloscope is a voltmeter. It physically measures the total voltage on the line at its port:

$$V_{measured}(t) = V_{incident} + V_{reflected}(t)$$

The reflection coefficient at each point in time is isolated by subtracting the known incident voltage and normalizing:

$$\rho(t) = \frac{V_{measured}(t) - V_{incident}}{V_{incident}}$$

The TDR firmware then applies a standard algebraic inversion of the reflection coefficient formula to convert each $\rho(t)$ value into the local impedance. Starting from the definition $\rho = \frac{Z - Z_0}{Z + Z_0}$, multiplying both sides by $(Z + Z_0)$, distributing, grouping terms, and solving for $Z$ yields:

$$Z(t) = Z_0 \cdot \frac{1 + \rho(t)}{1 - \rho(t)}$$

This equation is the bridge between the raw voltage measurement and the impedance profile displayed on the screen.

**Numerical example:** The TDR launches a 1V step ($V_{incident} = 1\text{V}$, producing a 0.5V launched wave into a matched line). At $t = 2\text{ ns}$, the scope measures 1.2V total at the connector. The incident wave was 1V (the full source amplitude as seen at the scope node), so $\rho = \frac{1.2 - 1.0}{1.0} = 0.2$. The local impedance is $Z = 50 \cdot \frac{1.2}{0.8} = 75\Omega$. The TDR displays a step from the 50-ohm baseline up to 75 ohms at the physical location corresponding to the 2 ns round-trip delay.

### The TDR Staircase: What the Screen Displays

Understanding the TDR display requires internalizing that the screen is not a camera looking sideways at the physical length of the trace. The TDR is a hyper-fast voltmeter permanently fixed at exactly one physical location: the connector. The horizontal X-axis represents time (or, equivalently, round-trip distance), and the vertical Y-axis represents either voltage or impedance.

Consider a 12-inch PCB trace with an open circuit at the far end:

1. **$t < 0$:** The screen displays a flat line at 0V.
2. **$t = 0$:** The internal source fires. The voltage at the connector immediately jumps. The screen draws a vertical line shooting from 0V to 0.5V.
3. **$0 < t < 4\text{ ns}$:** The wavefront actively travels down the 12-inch trace and reflects back. The electromagnetic wave in FR4 requires approximately 2 ns to travel 12 inches; the round trip is 4 ns. During this entire window, the active transmission line presents a 50-ohm load at the connector, holding the voltage at 0.5V via the voltage divider. The screen draws a flat horizontal line at 0.5V for 4 nanoseconds. This plateau is the literal time-of-flight of the wave through the board.
4. **$t = 4\text{ ns}$:** The reflection arrives back at the connector. The returning +0.5V wave superimposes on the existing 0.5V. The screen draws a second vertical step from 0.5V to 1.0V.
5. **$t > 4\text{ ns}$:** The matched internal source absorbs the reflection. The system achieves steady state. The screen extends a flat line at 1.0V indefinitely.

The resulting shape is a two-step staircase. The horizontal width of the 0.5V plateau is the exact round-trip flight time. Engineers use this width to physically calculate the length of the trace.

## Architecture

### Capacitive Dips and Inductive Bumps

Every localized impedance discontinuity produces a characteristic signature on the TDR display. The polarity of the reflection directly identifies the physical nature of the parasitic structure.

**Capacitive parasitic (impedance dip):** Excess capacitance arises from physical structures that add metallic surface area or bring conductors closer together. Test point pads, surface-mount device pads, and via barrels passing through internal ground planes act as parallel-plate capacitors connecting the signal path to the ground plane. When the propagating wavefront encounters this excess geometric capacitance, the wide region demands a sudden surge of current to charge the extra metal area. A surge in current for a given voltage means the instantaneous impedance drops ($Z = V/I$). The TDR records this momentary drop as a downward dip on the screen.

The physical mechanism of the negative reflection follows directly from the wavefront dynamics. The parasitic capacitor opens a new parallel path to the ground plane, allowing electrons to flow out of the signal path into ground more readily than the baseline geometry permits. This sudden opening of an additional escape route drops the local electrical pressure below the forward baseline. The localized pressure drop propagates backward as a negative voltage ripple, which the TDR instrument records as a negative dip.

The impedance of a capacitor is:

$$Z_C = \frac{1}{2\pi f C}$$

At DC or very low frequencies, this impedance is effectively infinite. The capacitor acts as an open circuit to ground, and low-frequency signal energy ignores the via entirely. At the high frequencies composing the sharp leading edge of the step function, the impedance drops dramatically. The via looks like a partial short circuit to ground, and the high-frequency wave energy reflects violently.

**Inductive parasitic (impedance bump):** Excess inductance arises from physical structures that restrict the current path or force the return current to take a wider detour. Neck-downs, wirebonds, sharp corners, and gaps in the reference plane force the electromagnetic loop to expand. The elevated local inductance generates a violent opposing back-EMF against the high-frequency wavefront ($V = L \cdot dI/dt$). This opposition establishes a local impedance above the 50-ohm baseline. A positive reflection propagates backward, and the TDR displays an upward bump.

The impedance of an inductor is:

$$Z_L = 2\pi f L$$

At low frequencies, this impedance is negligible, and the restriction is invisible. At high frequencies, the impedance climbs, producing a strong positive reflection.

**Diagnostic power:** Both parasitics degrade high-frequency edge content and produce a rounded transition at the receiver. The distinction matters for diagnosis. On the TDR display, the capacitive parasitic appears as a negative dip (local impedance below $Z_0$), while the inductive parasitic appears as a positive bump (local impedance above $Z_0$). The physical difference lies in the mechanism: the capacitive parasitic shunts energy out of the signal path through a parallel escape route, while the inductive parasitic blocks energy from passing through the signal path with a series barrier.

### Returning to the Baseline After a Defect

A localized parasitic structure (a narrow trace measuring only a few millimeters, a via, a connector pad) has finite physical length. The forward-traveling wavefront hits the start of the anomalous section and immediately begins generating a reflection backward. The wavefront requires only a few picoseconds to traverse those millimeters. Exiting the defect returns the wavefront to the properly designed 50-ohm trace geometry, which generates zero reflections.

The TDR screen plots reflected energy arriving at the instrument against time. Receiving a short burst of reflected energy followed immediately by zero new reflected energy causes the screen to draw a bump (or dip) and then return to the flat 0.5V baseline. The time duration of the feature on the screen directly corresponds to the physical width of the discontinuity:

$$\text{Length} = v_p \cdot \frac{\Delta t}{2}$$

### The Impedance Cancellation Principle

If a discontinuity introduces additional inductance and additional capacitance in the exact proportions required to maintain $Z_0 = \sqrt{L/C}$, the impedance remains matched. The TDR trace displays a flat line with no reflection, even though the physical geometry changed. Engineers exploit this phenomenon to optimize signal links. Deliberately routing a narrow, highly inductive trace segment adjacent to a wide, highly capacitive connector pad can maintain a uniform 50-ohm impedance profile through a region where either element alone would produce a severe mismatch.

## Worked Examples

### Spatial Resolution: Why Rise Time Limits What the TDR Can See

The voltage step generated by the TDR is not instantaneous. It has a finite rise time ($t_r$), typically defined as the 10% to 90% transition time. This rise time sets a fundamental limit on the instrument's ability to distinguish between two impedance discontinuities that are physically close together.

**The physical length of the rising edge:** While the step function propagates down the trace, the transition from 0V to full voltage is not concentrated at a mathematical point. The rising edge is physically spread across a length of trace:

$$l_{edge} = v_p \cdot t_r$$

A 30-picosecond rise time at 6 inches per nanosecond produces a rising edge physically spread over 0.18 inches of the PCB.

**Deriving the resolution limit:** Consider two discontinuities, Point A and Point B, separated by physical distance $d$.

At $t = 0$, the leading tip of the rising edge hits Point A. Point A immediately begins generating a reflection that travels backward toward the TDR. This reflection requires $t_r$ seconds to finish, because the incident edge itself takes that long to reach full amplitude.

The forward wave continues past Point A and travels distance $d$ to reach Point B. This takes time $t_{forward} = d / v_p$. The edge hits Point B and generates a second reflection, which travels distance $d$ back to Point A. The total delay between the start of the first reflection and the arrival of the second reflection at Point A is:

$$\Delta t = \frac{2d}{v_p}$$

For the TDR to display two distinctly separate features, the first reflection must completely finish before the second reflection begins to arrive. The first reflection takes exactly $t_r$ seconds to finish rising. The condition for resolving the two features is:

$$\frac{2d}{v_p} > t_r$$

Solving for the minimum resolvable distance:

$$d > \frac{v_p \cdot t_r}{2} = \frac{l_{edge}}{2}$$

**Two discontinuities are resolvable on a TDR screen only if their physical separation exceeds half the physical length of the rising edge.** If they are closer, the second echo arrives before the first is finished, and they superimpose into a single, unresolved lump.

**Practical numbers:** A Keysight TDR with a 15 ps rise time operating on FR4 ($v_p \approx 6 \text{ in/ns}$) produces $l_{edge} = 6 \times 0.015 = 0.09 \text{ inches}$. The minimum resolvable separation is 0.045 inches, roughly 1.1 mm. A 30 ps system resolves only down to 2.3 mm.

### Quantitative Parasitic Extraction: The Area Under the Curve

The TDR waveform contains enough information to extract the actual physical capacitance or inductance of a localized discontinuity. The key is the mathematical integral of the reflection coefficient over time.

**The inductor formula:** The fundamental equation for an inductor is $V = L \cdot dI/dt$. Integrating both sides over the entire time duration of the defect converts the instantaneous rate of change into total accumulated values. The integral of voltage over time represents the total magnetic flux change. The integral of $dI/dt$ simply equals the total current change $\Delta I$.

Applying boundary conditions from transmission line theory (the maximum current through the defect equals $V_{inc}/Z_0$, and the reflected voltage equals half the total voltage generated across a small series element under the small-reflection approximation) yields, after substituting the reflection coefficient $\rho(t) = V_{reflected}/V_{incident}$:

$$L = 2Z_0 \int \rho(t)\, dt$$

The total inductance of the defect equals twice the baseline impedance multiplied by the area under the positive impedance bump on the $\rho(t)$ curve.

**The capacitor formula:** The fundamental equation for a capacitor is $I = C \cdot dV/dt$. The same integration process, applied to a parallel shunt element with the appropriate sign convention for the negative reflection, yields:

$$C = \frac{2}{Z_0} \int -\rho(t)\, dt$$

The total capacitance equals twice the reciprocal of the baseline impedance multiplied by the area enclosed within the negative impedance dip.

**Why the area stays constant regardless of rise time:** The capacitance of a via is a fixed physical property of the board. It is determined by the drilled hole geometry and the distance to the ground planes. The integral $\int -\rho(t)\, dt$ must therefore be a constant for a given structure. What changes is the shape of the curve. A fast incident edge produces a short interaction time ($dt$ is small), which forces the reflection amplitude ($\rho$) to spike high, producing a deep, narrow dip. A degraded, slow edge produces a long interaction time, which forces the amplitude down to maintain the same total area, producing a wide, shallow dip. The underlying physical capacitance has not changed, but the instrument's ability to measure the true peak impedance has been destroyed by the degraded rise time.

### Distinguishing $Z_0$ from Reactive Components

The TDR identifies the characteristic impedance $Z_0$ by reading the longest flat baseline region on the screen. On this flat line, the distributed inductance and capacitance are perfectly balanced in the ratio $Z_0 = \sqrt{L/C}$, producing zero net reflection. The TDR cannot separate the baseline inductance and capacitance on that flat line because their effects cancel.

Isolating the reactive components of individual discontinuities (the excess $L$ or $C$ above the balanced baseline) requires either the area-integral technique described above (for electrically small defects) or a transition to the frequency domain. A Vector Network Analyzer (VNA) measures S-parameters as a function of frequency, providing both magnitude and phase of the complex reflection coefficient. The Smith Chart plots this complex data: the center horizontal line represents pure resistance, points in the upper half indicate excess inductance, and points in the lower half indicate excess capacitance. Mathematically, a time-domain TDR step response can be converted into a frequency-domain S-parameter response by applying a Fast Fourier Transform to the measured step waveform.

## Edge Cases

### Rise Time Degradation and the Need for the Rising Edge

A DC voltage has no concept of time. Applying a flat 1V DC level charges the entire trace to 1V, and only the total resistance can be measured. To measure distance, the instrument needs a time marker. The rising edge is the physical event that starts the stopwatch, acting as a localized wavefront marker traveling down the line.

The sharpness of that edge is equally critical. A fast rising edge contains extremely high-frequency content (Fourier analysis of a 10-picosecond transition shows harmonics extending past 35 GHz). Impedance mismatches caused by tiny parasitic capacitances and inductances only react to high frequencies. If the edge is slow and contains only low-frequency content, it rolls right over these structures without generating a detectable reflection.

The finite bandwidth of the TDR instrument itself determines the steepest possible edge. A high-end TDR with 20 GHz bandwidth can generate harmonics only up to that frequency, limiting the rise time to approximately $t_r \approx 0.35/BW \approx 17.5\text{ ps}$. A perfectly vertical (zero rise time) edge would require infinite bandwidth, which no physical instrument can produce.

### Masking: Upstream Discontinuities Blind the Instrument

Every time the forward wave hits a mismatch, some energy reflects backward. The forward-traveling incident wave shrinks with each reflection. If the wave hits a massive mismatch (a near-open or near-short), almost all the energy reflects, and the forward wave drops to near zero. The TDR becomes blind to everything downstream.

This is the masking effect. The practical rule for signal integrity debugging is absolute: fix the first major mismatch in a trace before trusting what the TDR reports about the rest of the trace.

The masking effect also distorts the quantitative impedance readings. The TDR firmware calculates downstream impedance by assuming the incident wave retains its full original amplitude. If upstream reflections have depleted the wave to 80% of its original value, the firmware applies the full-amplitude calibration to a reduced signal, reporting incorrect impedance values for all downstream structures.

### Spreading: Frequency-Dependent Attenuation Smears Downstream Features

The first parasitic inductor strips high-frequency content from the forward-traveling wave. The surviving wavefront continuing past the inductor possesses a much slower, rounded rising edge. This degraded wavefront becomes the new interrogating signal for the remainder of the trace.

Striking a second parasitic inductor with a slow, rounded edge produces a drastically different response. The inductor generates back-EMF proportional to the rate of current change ($V = L \cdot dI/dt$). A slow, rounded edge has a small rate of change, producing only a weak opposing voltage. The TDR records this weak response as a small bump. Two physically identical inductors will look different on the screen: the first appears as a sharp, deep feature, while the second, hit by the degraded wavefront, appears as a wider, shallower, blurrier feature.

The spatial resolution literally degrades the further down the trace the TDR looks. The channel attenuation mechanisms described in the skin effect and dielectric loss guide (conductor loss scaling as $\sqrt{f}$, dielectric absorption scaling linearly with frequency) compound the problem. Even on a perfectly uniform trace with no discrete discontinuities, these distributed losses continuously filter the highest-frequency harmonics from the propagating step. A pristine 20-picosecond edge at the source can degrade to a sluggish 100-picosecond edge by the time it reaches the far end of a long board.

### The Peeling Algorithm

The peeling algorithm (also called impedance profile deconvolution, implemented in Keysight Physical Layer Test System software) is a purely mathematical correction that runs entirely in software. It does not alter the physical voltage on the board.

The algorithm analyzes the first reflection, calculates exactly how much energy was lost from the forward wave, and dynamically recalibrates the mathematics for the second reflection. It then strips the effect of the first discontinuity from the waveform and repeats the process for each subsequent feature, peeling away the cumulative errors layer by layer.

The recalibration accounts for three distinct error sources at each layer: the amplitude depletion of the forward wave (masking), the rise time degradation of the forward edge (spreading), and the secondary reflections generated when energy bouncing between two discontinuities creates phantom features on the screen. The result is a de-embedded impedance profile that represents the true local impedance at each point along the trace, as if each discontinuity had been measured in isolation with a pristine incident edge.
