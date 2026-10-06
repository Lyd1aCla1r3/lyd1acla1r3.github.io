# Smith Charts

<!-- SUMMARY: The Smith chart is the conformal map $\Gamma = (z - 1)/(z + 1)$ that places passive impedances inside a unit circle. This guide derives its constant-resistance circles and constant-reactance arcs, demonstrating how the $S_{11}$ reflection plane visually separates inductive and capacitive components. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Chapter 8](08_S_Parameters_and_VNA.md) established that $S_{11}$ measured at one frequency is the reflection coefficient $\Gamma$ of [Chapter 3](03_Impedance_Reflections_and_Termination.md), and that a VNA reports it as a complex number at every point of a frequency sweep. A complex number needs two coordinates, so a plot of magnitude in decibels or of phase in degrees against frequency shows only half of the information at a time. The complex plane of $\Gamma$ shows both halves together, with the real part on the horizontal axis and the imaginary part on the vertical axis, and the Smith chart is the same plane with a grid of impedance values printed on top of it.

The chart solves a problem of scale. The impedance that produces a given reflection ranges from zero (a short circuit) to infinity (an open circuit), and a Cartesian plot of impedance cannot place infinity on a finite sheet. The reflection coefficient of any passive impedance has a magnitude of at most 1, so the $\Gamma$ plane is bounded by the unit circle, and the Smith chart is the map from the unbounded impedance plane into that circle. This chapter derives the map and its two families of curves, explains the landmarks of the chart and the motion of a trace along a line and across frequency, introduces the admittance chart for shunt elements, and ends by completing the story that [Chapter 7](07_Time_Domain_Reflectometry.md) left open: how the complex $S_{11}$ separates an inductance from a capacitance that the time domain cannot separate.

## Core Concepts

### Normalization and the Universal Chart

The reflection coefficient of Chapter 3 depends on the load impedance $Z_L$ and on the reference impedance $Z_0$:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

A 100 Ω load gives different values of $\Gamma$ against a 50 Ω reference and against a 75 Ω reference, so a chart drawn in ohms would apply to one system only. Dividing the load impedance by the reference impedance gives the normalized impedance:

$$z = \frac{Z_L}{Z_0} = r + jx$$

The normalized resistance $r$ is nonnegative for a passive load, and the normalized reactance $x$ is positive for an inductor and negative for a capacitor (the sign convention of Chapter 3). Dividing the numerator and the denominator of $\Gamma$ by $Z_0$ removes the reference impedance from the equation:

$$\Gamma = \frac{z - 1}{z + 1}$$

A normalized impedance of $z = 1$ always gives $\Gamma = 0$, whether the system is 50 Ω, 75 Ω, or any other value, and a single printed chart therefore serves every transmission line system.

### The Reflection Coefficient as a Complex Number

The quotient of two complex numbers is a complex number, so $\Gamma$ has a real part $u$ and an imaginary part $v$:

$$\Gamma = u + jv$$

The two coordinates carry the two properties of a reflected wave: the magnitude $|\Gamma|$ gives its relative amplitude and the angle of $\Gamma$ gives its phase relative to the incident wave. The derivation starts from the substitution of $z = r + jx$:

$$\Gamma = \frac{(r - 1) + jx}{(r + 1) + jx}$$

Multiplying the numerator and the denominator by the complex conjugate of the denominator, $(r + 1) - jx$, makes the denominator real:

$$[(r + 1) + jx]\,[(r + 1) - jx] = (r + 1)^2 + x^2$$

The numerator expands to $(r-1)(r+1) + x^2 + jx[(r+1) - (r-1)]$, which simplifies to $r^2 - 1 + x^2 + 2jx$, so:

$$\Gamma = \frac{r^2 - 1 + x^2}{(r + 1)^2 + x^2} + j\,\frac{2x}{(r + 1)^2 + x^2}$$

The first term has no factor $j$ and is the real part, and the second is the imaginary part:

$$u = \frac{r^2 - 1 + x^2}{(r + 1)^2 + x^2}, \qquad v = \frac{2x}{(r + 1)^2 + x^2}$$

Every impedance $z = r + jx$ therefore maps to exactly one point $(u, v)$. The denominator of $v$ is positive, so the imaginary part of $\Gamma$ has the same sign as the reactance $x$: a positive reactance (inductive) lies above the horizontal axis and a negative reactance (capacitive) lies below it. This sign rule is the basis of the hemisphere reading at the end of the chapter.

### Passive Impedances Lie Inside the Unit Circle

The squared magnitude of $\Gamma$ follows from the magnitudes of its numerator and denominator:

$$|\Gamma|^2 = \frac{|z - 1|^2}{|z + 1|^2} = \frac{(r - 1)^2 + x^2}{(r + 1)^2 + x^2}$$

The difference between the denominator and the numerator is $(r + 1)^2 - (r - 1)^2 = 4r$. A passive load has $r \ge 0$, so the denominator is at least as large as the numerator and $|\Gamma| \le 1$. The equality $|\Gamma| = 1$ holds only for $r = 0$, a purely reactive load that absorbs no power. This is the energy conservation of Chapter 3 (the load absorbs the portion $1 - |\Gamma|^2$ of the incident power) shown in the algebra: the numerator and denominator differ by $4r$, which is proportional to the resistive part that dissipates the power.

### The Conformal Mapping

The map $\Gamma(z) = (z - 1)/(z + 1)$ is an analytic function of the complex variable $z$, and its derivative is:

$$\frac{d\Gamma}{dz} = \frac{(z + 1) - (z - 1)}{(z + 1)^2} = \frac{2}{(z + 1)^2}$$

The derivative is nonzero everywhere except at $z = -1$, which is not a passive impedance. An analytic map with a nonzero derivative preserves angles between curves (a standard result of complex analysis, stated here without proof), and a map with this property is called conformal. The rectangular grid of vertical lines of constant $r$ and horizontal lines of constant $x$ in the impedance plane meets at right angles, and the images of those lines meet at right angles on the $\Gamma$ plane. The lines do not remain straight, because a map of this form (a Möbius transformation) turns lines into circles, and the next section derives the circles. The right half of the impedance plane ($r \ge 0$) is the set of passive impedances, and it fills the disc $|\Gamma| \le 1$.

## Worked Examples

### Deriving the Constant Resistance Circles

The derivation starts from the inverse map of Chapter 3, written for normalized impedance:

$$z = \frac{1 + \Gamma}{1 - \Gamma}$$

Substituting $z = r + jx$ and $\Gamma = u + jv$:

$$r + jx = \frac{(1 + u) + jv}{(1 - u) - jv}$$

Multiplying the numerator and the denominator by the complex conjugate of the denominator, $(1 - u) + jv$, gives:

$$r + jx = \frac{1 - u^2 - v^2}{(1 - u)^2 + v^2} + j\,\frac{2v}{(1 - u)^2 + v^2}$$

Equating the real parts isolates the resistance:

$$r = \frac{1 - u^2 - v^2}{(1 - u)^2 + v^2}$$

Multiplying both sides by the denominator and expanding it:

$$r - 2ru + ru^2 + rv^2 = 1 - u^2 - v^2$$

Collecting the terms in $u^2$, $u$, and $v^2$ on the left:

$$u^2(r + 1) - 2ru + v^2(r + 1) = 1 - r$$

Dividing by $(r + 1)$:

$$u^2 - \frac{2r}{r + 1}\,u + v^2 = \frac{1 - r}{r + 1}$$

Completing the square in $u$ requires adding $\left(\frac{r}{r+1}\right)^2$ to both sides:

$$\left(u - \frac{r}{r+1}\right)^2 + v^2 = \frac{1 - r}{r + 1} + \frac{r^2}{(r+1)^2}$$

The right side over the common denominator $(r + 1)^2$ is $\frac{(1 - r)(r + 1) + r^2}{(r + 1)^2} = \frac{1 - r^2 + r^2}{(r + 1)^2} = \frac{1}{(r + 1)^2}$, so:

$$\left(u - \frac{r}{r+1}\right)^2 + v^2 = \left(\frac{1}{r+1}\right)^2$$

This is a circle with center $\left(\frac{r}{r+1},\, 0\right)$ and radius $\frac{1}{r+1}$. Every constant-resistance circle is centered on the horizontal axis. For $r = 0$ the center is the origin and the radius is 1, which is the outer boundary of the chart. For $r = 1$ the center is $(0.5, 0)$ and the radius is 0.5, so the circle passes through the center of the chart. For $r \to \infty$ the center approaches $(1, 0)$ and the radius approaches zero, so every circle passes through the point $(1, 0)$ and the family shrinks onto it.

### Deriving the Constant Reactance Arcs

The imaginary parts of the same expanded equation give the reactance:

$$x = \frac{2v}{(1 - u)^2 + v^2}$$

For $x = 0$ the equation reduces to $v = 0$, which is the horizontal axis, so the resistive axis is the zero-reactance line. For $x \ne 0$, multiplying by the denominator and expanding gives:

$$x - 2xu + xu^2 + xv^2 = 2v$$

Dividing every term by $x$ gives $1 - 2u + u^2 + v^2 = 2v/x$, and moving the terms into the form of a circle:

$$u^2 - 2u + v^2 - \frac{2v}{x} = -1$$

Completing the square adds 1 for $u$ and $1/x^2$ for $v$ to both sides:

$$(u - 1)^2 + \left(v - \frac{1}{x}\right)^2 = \frac{1}{x^2}$$

This circle has center $\left(1,\, \frac{1}{x}\right)$ and radius $\frac{1}{|x|}$. Every center lies on the vertical line $u = 1$, and every circle passes through the point $(1, 0)$, because the distance from the center to that point is $1/|x|$. Only the part of each circle that lies inside the unit circle corresponds to passive impedances, so the reactance curves appear as arcs. Larger values of $|x|$ move the center toward the horizontal axis and tighten the arc, and in the limit $|x| \to 0$ the radius grows without limit and the arc flattens into the horizontal axis. The sign rule of the previous section places the arcs for $x > 0$ in the upper half of the chart and the arcs for $x < 0$ in the lower half.

### Reading a Point on the Chart

Assume a load of $25 + j50$ Ω in a 50 Ω system. The normalized impedance is $z = 0.5 + j1.0$, which lies at the intersection of the $r = 0.5$ circle and the $x = +1$ arc. The coordinates follow from the equations for $u$ and $v$ with $r = 0.5$ and $x = 1$, where the denominator is $(1.5)^2 + 1 = 3.25$:

$$u = \frac{0.25 - 1 + 1}{3.25} = 0.0769, \qquad v = \frac{2}{3.25} = 0.6154$$

The distance from the center is $|\Gamma| = \sqrt{0.0769^2 + 0.6154^2} = 0.620$ and the angle is $\arctan(0.6154/0.0769) = 82.9^\circ$. The squared magnitude from the closed form is $|\Gamma|^2 = 1.25/3.25 = 0.385$, which confirms the coordinates. The return loss is $-20\log_{10}(0.620) = 4.15$ dB and the fraction of the power absorbed by the load is $1 - 0.385 = 0.615$. The point lies in the upper half of the chart, in agreement with the positive reactance.

## Architecture

### Landmarks and Navigation

The two families of curves form a coordinate system inside the unit circle, and each point on it corresponds to one normalized impedance.

The **center** of the chart, at $(u, v) = (0, 0)$, is the intersection of the $r = 1$ circle and the $x = 0$ axis. It represents $\Gamma = 0$, a load equal to the reference impedance with no reflection, and the aim of impedance matching is to bring a trace to this point.

The **left edge** of the horizontal axis, at $(-1, 0)$, is the short circuit ($z = 0$). The magnitude is 1 and the phase is 180°, so the load reflects the full wave with inverted voltage.

The **right edge** of the horizontal axis, at $(+1, 0)$, is the open circuit ($z \to \infty$). The magnitude is 1 and the phase is 0°. All the resistance circles and all the reactance arcs meet at this point.

The **horizontal axis** is the line of zero reactance, so every point on it is a pure resistance. The printed values rise from 0 at the left edge through 1 at the center to infinity at the right edge.

The **upper half** of the chart contains the impedances with positive reactance (inductive), and the **lower half** contains those with negative reactance (capacitive). The **outer circle** is the $r = 0$ circle, which holds the purely reactive loads.

The magnitude and the angle of a point are the polar reading of the same chart: the distance from the center is $|\Gamma|$, and the angle measured from the positive horizontal axis is the phase of the reflection. A VNA measures these two quantities directly, and the printed grid converts them into resistance and reactance.

### Rotation with Line Length and Frequency

A reflection coefficient that is measured at a distance $d$ from the load, looking toward the load along a line, is the load reflection delayed by the round trip of the wave. The reflected wave travels the extra distance $2d$ and attenuates and rotates over it, so with the propagation constant $\gamma = \alpha + j\beta$ of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md):

$$\Gamma(d) = \Gamma_L\,e^{-2\gamma d} = \Gamma_L\,e^{-2\alpha d}\,e^{-j2\beta d}$$

On a lossless line ($\alpha = 0$) the magnitude is unchanged and the phase decreases by $2\beta d$, so the point rotates clockwise around the center on a circle of constant $|\Gamma|$. The phase $2\beta d = 2\omega d/v_p$ equals $360^\circ f\,(2\tau_d)$ for the delay $\tau_d = d/v_p$ of the line, which is the rule $\theta = -360^\circ f\tau$ of Chapter 8 applied to the round-trip delay. A half wavelength of line ($\beta d = 180^\circ$) turns the point through a full circle. Increasing the frequency at fixed length rotates the point clockwise by the same rule, so a trace of $S_{11}(f)$ for any structure with delay moves clockwise as the sweep proceeds.

Assume an open stub of 1 inch of FR4 line, which has a delay of 170 ps ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)) and a round-trip delay of 340 ps. The open circuit starts at $\Gamma = 1$ (phase 0°). At 1 GHz the phase is $-360^\circ \times 10^9 \times 0.34\times10^{-9} = -122.4^\circ$, which places the point in the lower left of the chart, and the impedance is $z = -j\cot(2\pi f\tau_d) = -j0.550$, a capacitive reactance in the lower half. At $f = 1/(4\tau_d) = 1.47$ GHz the phase is $-180^\circ$ and the stub, a quarter wavelength long, appears as a short circuit at the left edge. At 2 GHz the phase is $-244.8^\circ$ (equivalent to $+115.2^\circ$), and the impedance is $z = +j0.635$, which is inductive and lies in the upper half. A single open stub is therefore capacitive below the quarter-wave frequency and inductive above it, and the trace passes from the lower to the upper half of the chart through the short-circuit point.

### The Admittance Chart

Shunt elements add their admittances, so the natural variable for a shunt element is the normalized admittance $y = 1/z = g + jb$, with the normalized conductance $g$ and the normalized susceptance $b$. The reflection coefficient in terms of $y$ follows from $z = 1/y$:

$$\Gamma = \frac{z - 1}{z + 1} = \frac{1/y - 1}{1/y + 1} = \frac{1 - y}{1 + y}$$

The expression equals the earlier map with $y$ in place of $z$ and a change of sign, which means that the point for the admittance $y$ lies at $-\Gamma$ of the point for the impedance $z = y$. The admittance chart is therefore the impedance chart rotated by 180° around the center. The constant-conductance circles are the images of the constant-resistance circles and pass through the left edge, and the constant-susceptance arcs mirror the reactance arcs. A combined impedance and admittance chart prints both grids, and each point carries both readings.

The two elements of Chapter 3 take a simple form in the two variables. A shunt capacitance on a matched line adds a susceptance $b = \omega C Z_0 = x$ (the dimensionless quantity of Chapter 3) to the matched admittance $y = 1$. A series inductance adds a reactance $x_L = \omega L/Z_0$ to the matched impedance $z = 1$. Assume $f = 5$ GHz and $Z_0 = 50$ Ω:

- A shunt capacitance of 0.5 pF gives $y = 1 + j0.785$ and $z = 1/y = 0.618 - j0.486$, and the equations for $u$ and $v$ place the point at $\Gamma = -0.134 - j0.340$ ($|\Gamma| = 0.366$, angle $-111.4^\circ$), in the lower half.
- A series inductance of 1 nH gives $z = 1 + j0.628$, and the point is at $\Gamma = 0.090 + j0.286$ ($|\Gamma| = 0.300$, angle $72.6^\circ$), in the upper half.

These magnitudes agree with the values of Chapter 3 (0.366 and 0.300), and the chart adds the information of the position: the capacitance lies below the horizontal axis and the inductance lies above it.

### Reading S11 Traces Across Frequency

A VNA plots $S_{11}(f)$ on the chart as a trajectory of points, one for each measured frequency. The position and the direction of the trajectory carry the following information.

- A trace that stays near the center has a small reflection at all frequencies, and the distance from the center is $|S_{11}|$, from which the return loss follows.
- A trace in the upper half has a net inductive reactance and a trace in the lower half has a net capacitive reactance, by the sign rule derived above.
- A trace rotates clockwise as the frequency rises, because the electrical length of the structure grows in proportion to frequency.
- A trace that spirals inward as it rotates indicates loss. The magnitude of $\Gamma(d)$ decays as $e^{-2\alpha d}$, and $\alpha$ grows with frequency ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)), so a poorly terminated lossy line spirals toward the center even though the termination itself has not improved. A spiral into the center is not evidence of a better match.

The chart is the display for the quantity that both instruments measure. A TDR presents it as a real voltage along the length of the trace, and a VNA presents it as a complex trajectory along frequency, and [Chapter 8](08_S_Parameters_and_VNA.md) gives the conversion between the two.

## Edge Cases

### The Passive Boundary and the Interior

The unit circle is the limit of the energy conservation derived in the Core section, and its interior has a physical meaning. A point on the boundary is a purely reactive load ($r = 0$) that reflects all of the power, such as an ideal lossless capacitor or inductor. A point inside the boundary has a nonzero resistance, which absorbs a fraction $1 - |\Gamma|^2$ of the incident power as heat and reflects the remainder.

### The Extended Chart

An active circuit that contains a transistor amplifier or a negative-resistance oscillator can reflect more power than it receives. The formula for $|\Gamma|^2$ gives the condition directly: its denominator exceeds its numerator by $4r$, so a negative normalized resistance $r < 0$ makes the numerator larger and gives $|\Gamma| > 1$, a point outside the unit circle. The extended Smith chart prints the continuation of the same circle and arc families into this region, with circles of negative resistance, so that the measurements of active devices can be read in the same way as those of passive ones.

### Conformal Mapping Preserves Angles but Distorts Distances

The mapping preserves angles and does not preserve distances. The sensitivity of the impedance to a small change in $\Gamma$ follows from the derivative of $z = (1 + \Gamma)/(1 - \Gamma)$:

$$\frac{dz}{d\Gamma} = \frac{(1 - \Gamma) + (1 + \Gamma)}{(1 - \Gamma)^2} = \frac{2}{(1 - \Gamma)^2}$$

Near the center ($\Gamma \approx 0$) the derivative is 2, so an uncertainty of 0.01 in $\Gamma$ corresponds to 0.02 in the normalized impedance, which is 1 Ω in a 50 Ω system. Near the open circuit, with $\Gamma = 0.9$, the derivative is $2/0.01 = 200$, and the same uncertainty of 0.01 corresponds to 2 in normalized impedance, which is 100 Ω. The region near the center is expanded, so a small mismatch occupies a large area on the chart and is read with good resolution. The regions near the short and open circuits are compressed into the narrow rim of the chart. A measurement of a nearly total reflection is therefore sensitive to noise and calibration error, and the result is large changes in the computed impedance for small changes in the measured $\Gamma$.

### Reading Reactance from S11: Separating Inductance and Capacitance

[Chapter 7](07_Time_Domain_Reflectometry.md) ended with a limit: a TDR reports only the net area $\tau_L - \tau_C$ of an inductance and a capacitance that overlap within the resolution of the edge, and it cannot recover the two values. The complex $S_{11}$ carries more information, and this section shows what the information is and what it does not include.

**The magnitude alone does not separate them.** The shunt capacitance and the series inductance of Chapter 3 have the reflection coefficients $\Gamma_C = -jx/(2 + jx)$ with $x = \omega C Z_0$, and $\Gamma_L = jy/(2 + jy)$ with $y = \omega L/Z_0$. The two expressions have the same form, so they have equal magnitudes whenever $y = x$, which requires $L/Z_0 = C Z_0$, that is $L = Z_0^2 C$ (the compensation condition of Chapter 3). For $C = 0.5$ pF the matching inductance is $L = 1.25$ nH, and the two reflections satisfy $\Gamma_L = -\Gamma_C$ at every frequency. At 5 GHz both have $|S_{11}| = 0.366$, which is $-8.7$ dB, and a plot of $|S_{11}|$ in decibels cannot tell the two elements apart, because both rise in proportion to frequency while they are small ($\pi f C Z_0$ for the capacitance and $\pi f L/Z_0$ for the inductance). The phase differs by 180°: $\Gamma_C$ has an angle of $-111.4^\circ$ and $\Gamma_L$ has an angle of $+68.6^\circ$.

**The hemisphere of the point separates the two elements in the complex plane.** The two points lie on opposite sides of the center of the chart, and the sign rule of the imaginary part identifies them: the capacitance is in the lower half and the inductance is in the upper half. A magnitude plot discards the sign of the reactance, and the complex plot retains it.

**The impedance plot gives the values of the elements.** The software converts $S_{11}$ to impedance with $Z = Z_0(1 + S_{11})/(1 - S_{11})$ (Chapter 3) and plots the real and imaginary parts against frequency, and the plot differs between two physical situations.

For a component that is measured as a one-port, with the component as the termination of the cable, the impedance is the reactance of the element itself. An inductor has $X_L = \omega L$, a straight line that rises in proportion to frequency (6.3, 31.4, and 62.8 Ω at 1, 5, and 10 GHz for 1 nH). A capacitor has $X_C = -1/(\omega C)$, a curve whose magnitude falls as $1/f$ (−318, −63.7, and −31.8 Ω for 0.5 pF). A lossless element reflects all of the power, so $|S_{11}| = 1$ at every frequency and the decibel plot is a flat line at 0 dB, and all of the information is in the phase. The capacitor has the angles $-17.9^\circ$, $-76.3^\circ$, and $-115.0^\circ$ at the three frequencies, and the inductor has $165.7^\circ$, $115.7^\circ$, and $77.0^\circ$. Both trajectories move clockwise along the rim of the chart as the frequency rises, the inductor from near the short circuit toward the open circuit and the capacitor from near the open circuit toward the short circuit.

For a small discontinuity that is embedded in a line terminated by $Z_0$, as in Chapters 3, 6, and 7, the magnitude $|S_{11}|$ rises with frequency, and the roll-off $1/(2\pi f C)$ does not appear in $S_{11}$ itself. A shunt capacitance gives the input impedance $Z_{in} = Z_0/(1 + jx)$, whose magnitude falls with frequency, and this fall appears only after the conversion from $S_{11}$ to impedance. The admittance $Y_{in} = 1/Z_{in} = (1 + jx)/Z_0$ shows the capacitance directly, because its imaginary part $\omega C$ is a straight line that rises with frequency. A series inductance gives $Z_{in} - Z_0 = j\omega L$, which is also a straight line. The slopes of these lines are the values of $C$ and $L$.

**A cluster of both is read from one complex measurement.** Assume the via of Chapter 6 with $L = 1.33$ nH in series and $C = 0.37$ pF to ground, seen from the line with a $Z_0$ load behind it. The input impedance is:

$$Z_{in} = j\omega L + \frac{Z_0}{1 + jx}, \qquad x = \omega C Z_0$$

At low frequency the expansion of the second term, $Z_0(1 - jx - x^2 + \cdots)$, gives:

$$Z_{in} - Z_0 \approx j\omega\left(L - Z_0^2 C\right) - Z_0 x^2, \qquad S_{11} \approx \frac{j\omega\,(L - Z_0^2 C)}{2Z_0} = j\omega\,(\tau_L - \tau_C)$$

The first-order term is the net quantity $L - Z_0^2 C = 0.405$ nH, which is the same net area $\tau_L - \tau_C$ that Chapter 7 measures from the TDR display, so the two instruments agree at low frequency and carry the same limit there. The second-order term is real, equals $-Z_0 x^2$, and depends on the capacitance alone. At 1 GHz the exact impedance is $Z_{in} = 49.33 + j2.62$ Ω. The real part gives $x^2 = Z_0/\operatorname{Re}(Z_{in}) - 1 = 0.0135$, so $x = 0.116$ and $C = x/(\omega Z_0) = 0.370$ pF. The imaginary part then gives $\omega L = \operatorname{Im}(Z_{in}) + Z_0 x/(1 + x^2) = 2.62 + 5.74 = 8.36$ Ω, so $L = 1.33$ nH. One complex number at one frequency therefore determines both elements, where the time domain with an overlapping pair determines only their difference. The real part differs from $Z_0$ by only 0.67 Ω at 1 GHz, and the difference grows as $x^2$ (it is 12.6 Ω at 5 GHz), so the accuracy of the calibration of Chapter 8 and the use of many frequency points determine the quality of the result.

**The limits of the extracted values come from the assumed model.** The extraction assumes a model of the structure, here an inductance followed by a capacitance, and it returns the values of that model. Reversing the order of the two elements changes the phase of $S_{11}$ and leaves the magnitude unchanged (at 1 GHz the angle is $102.8^\circ$ for the series inductance first and $61.0^\circ$ for the shunt capacitance first, and the magnitude is 0.0272 for both), because reversing the order is looking into the network from the other port, and a lossless network has $|S_{22}| = |S_{11}|$. The measurement identifies the net frequency signature of the cluster and permits a lumped model to be fitted to it. It does not locate the individual elements along the line more finely than the time resolution set by its own bandwidth, which is $d > v_p\,(0.45/f_{max})/2 = 1.6$ mm for a 20 GHz sweep on FR4 (the same limit as in Chapter 7), and two elements that are closer than this appear as one cluster. The frequency domain removes the ambiguity between the signs of the reactances and supplies the data for a fit of both elements, and the choice of model must come from knowledge of the physical structure.

The channel that this chapter and the previous three chapters characterize is a frequency-dependent filter, and its effect on the timing of a digital signal is a separate question. [Chapter 10](10_Jitter_Decomposition_and_Measurement.md) begins Part 3 with that question and decomposes the timing error of a received signal into its sources.
