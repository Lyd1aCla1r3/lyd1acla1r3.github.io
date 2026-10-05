# Smith Charts

<!-- SUMMARY: The Smith Chart is a conformal mapping that transforms complex impedance values onto a bounded circular plane, making impedance matching and transmission line analysis graphically tractable. This guide derives the mapping from the reflection coefficient, explains navigation through the constant-resistance and constant-reactance circles, and connects the graphical framework to VNA measurements. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

The reflection coefficient is the central quantity of transmission line analysis. Time domain reflectometry measures it as a real-valued voltage ratio at each point in time, producing an impedance profile along the physical length of a channel. The same reflection coefficient, however, is inherently a complex number: it carries both a magnitude (how much energy reflects) and a phase angle (the timing relationship between the incident and reflected waves). Capturing both dimensions simultaneously requires a representation in the complex plane, where the horizontal axis carries the real component and the vertical axis carries the imaginary component.

The fundamental challenge is one of scale. The complex impedance that produces a given reflection can range from zero (a short circuit) to infinity (an open circuit). Plotting impedance directly on a Cartesian grid is physically impossible when one axis must extend to infinity. The Smith Chart solves this problem through conformal mapping: a rigorous mathematical transformation that compresses the entire infinite impedance plane into a single finite circle of unit radius. Every passive impedance that could ever exist on a transmission line maps to a unique point inside this circle.

The internal structure of the chart consists of two families of curves overlaid on the reflection coefficient plane. Constant resistance circles and constant reactance arcs create a warped coordinate grid that allows an engineer to read impedance values directly from any plotted point. Vector network analyzers display measured S-parameter data on this chart, and the trajectory of a trace across frequency immediately reveals whether a device under test is resistive, capacitive, inductive, well-matched, or drifting toward a dangerous mismatch.

This guide develops the Smith Chart from first principles: the complex nature of the reflection coefficient, the normalization convention that makes the chart universal, the full algebraic derivation of both circle families via completing the square, the geometric interpretation of every major landmark on the chart, and the extension beyond the unit circle for active devices.

## Core Concepts

### Normalization and the Universal Chart

The reflection coefficient relating load impedance to characteristic impedance is:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

Absolute impedance values prevent the chart from being universal. A 100-ohm load produces a different reflection coefficient depending on whether the system impedance is 50 ohms or 75 ohms. Dividing the load impedance by the characteristic impedance produces a dimensionless normalized impedance:

$$z = \frac{Z_L}{Z_0} = r + jx$$

The variable $r$ represents normalized resistance (always non-negative for passive circuits) and $x$ represents normalized reactance (positive for inductors, negative for capacitors). Substituting this normalized impedance into the reflection coefficient equation eliminates the system impedance entirely:

$$\Gamma = \frac{z - 1}{z + 1}$$

A normalized impedance of $z = 1$ (a load matched to the system) always produces $\Gamma = 0$, regardless of whether the system is 50 ohms, 75 ohms, or any other value. This normalization is the mechanism that makes a single printed chart applicable to every transmission line system.

### The Reflection Coefficient as a Complex Number

The normalized impedance $z = r + jx$ is complex. Dividing one complex number by another always produces a third complex number. The reflection coefficient therefore possesses both a real component and an imaginary component, which are assigned the variables $u$ and $v$:

$$\Gamma = u + jv$$

This assignment is not arbitrary. It reflects the physical reality that a reflected wave carries both a magnitude and a phase shift relative to the incident wave, and representing both quantities simultaneously requires two independent coordinates.

The algebraic proof begins with the explicit substitution $z = r + jx$ into $\Gamma = (z - 1)/(z + 1)$:

$$\Gamma = \frac{(r - 1) + jx}{(r + 1) + jx}$$

Removing the imaginary number from the denominator requires multiplying both the numerator and denominator by the complex conjugate of the denominator, $(r + 1) - jx$. The denominator becomes purely real:

$$[(r + 1) + jx] \cdot [(r + 1) - jx] = (r + 1)^2 + x^2$$

Expanding the numerator and grouping real and imaginary terms yields:

$$\Gamma = \frac{r^2 - 1 + x^2}{(r + 1)^2 + x^2} + j\frac{2x}{(r + 1)^2 + x^2}$$

The first fraction contains no $j$ operator and is a purely real number. This is $u$. The second fraction multiplies $j$ and is purely imaginary. This is $v$:

$$u = \frac{r^2 - 1 + x^2}{(r + 1)^2 + x^2}$$

$$v = \frac{2x}{(r + 1)^2 + x^2}$$

These two quantities serve as the horizontal and vertical plotting coordinates on the Smith Chart. Every complex impedance $z = r + jx$ maps to exactly one point $(u, v)$ inside the unit circle.

### The Conformal Mapping: Infinite Plane to Finite Circle

The Smith Chart is the visual result of a conformal mapping. The word "conformal" means angle-preserving: orthogonal intersections in the impedance plane remain orthogonal after transformation. The rectangular grid of constant-$r$ vertical lines and constant-$x$ horizontal lines in the impedance plane warps into families of circles and arcs on the $\Gamma$ plane, but the perpendicular crossing angles are maintained.

Passive circuits guarantee that the magnitude of the reflection coefficient can never exceed 1. No passive load can reflect more energy than it receives. This physical constraint means all possible positive resistance and reactance values map to points inside a circle of radius 1 centered at the origin of the $(u, v)$ plane. The conformal mapping compresses an infinite Cartesian coordinate system into this finite circular domain.

## Worked Examples

### Deriving the Constant Resistance Circles

The mathematical derivation begins with the fundamental relationship between normalized impedance and the reflection coefficient. Starting from the inverse mapping:

$$z = \frac{1 + \Gamma}{1 - \Gamma}$$

Substituting $z = r + jx$ and $\Gamma = u + jv$:

$$r + jx = \frac{(1 + u) + jv}{(1 - u) - jv}$$

Multiplying numerator and denominator by the complex conjugate of the denominator, $(1 - u) + jv$, produces:

$$r + jx = \frac{1 - u^2 - v^2}{(1 - u)^2 + v^2} + j\frac{2v}{(1 - u)^2 + v^2}$$

Equating real parts isolates the resistance equation:

$$r = \frac{1 - u^2 - v^2}{(1 - u)^2 + v^2}$$

Multiplying both sides by the denominator and expanding:

$$r - 2ru + ru^2 + rv^2 = 1 - u^2 - v^2$$

Grouping the $u$ and $v$ terms on the left side:

$$u^2(r + 1) - 2ru + v^2(r + 1) = 1 - r$$

Dividing the entire equation by $(r + 1)$:

$$u^2 - \frac{2r}{r + 1}u + v^2 = \frac{1 - r}{r + 1}$$

Completing the square for $u$ requires adding $\left(\frac{r}{r+1}\right)^2$ to both sides:

$$\left(u - \frac{r}{r+1}\right)^2 + v^2 = \frac{1 - r}{r + 1} + \frac{r^2}{(r+1)^2}$$

Simplifying the right side by combining fractions over the common denominator $(r+1)^2$:

$$\frac{(1 - r)(r + 1) + r^2}{(r + 1)^2} = \frac{1 - r^2 + r^2}{(r + 1)^2} = \frac{1}{(r + 1)^2}$$

The final result is the equation of a circle:

$$\left(u - \frac{r}{r+1}\right)^2 + v^2 = \left(\frac{1}{r+1}\right)^2$$

This circle has its center at coordinates $\left(\frac{r}{r+1},\, 0\right)$ on the horizontal axis and radius $\frac{1}{r+1}$.

The geometric interpretation is immediate. All constant resistance circles are centered on the horizontal axis ($v = 0$). As $r$ increases, the center shifts rightward toward $u = 1$ and the radius shrinks toward zero. At $r = 0$, the circle has center $(0, 0)$ and radius 1, tracing the outer boundary of the entire chart. At $r = 1$, the circle has center $(0.5, 0)$ and radius 0.5, passing exactly through the chart center. As $r \to \infty$, both the center and the circle converge to the single point $(1, 0)$ on the far right edge.

### Deriving the Constant Reactance Arcs

Equating imaginary parts from the same expanded equation isolates the reactance:

$$x = \frac{2v}{(1 - u)^2 + v^2}$$

Multiplying by the denominator and distributing:

$$x - 2xu + xu^2 + xv^2 = 2v$$

Dividing the entire equation by $x$ and rearranging:

$$u^2 - 2u + v^2 - \frac{2v}{x} = -1$$

Completing the square for $u$ (adding 1) and for $v$ (adding $\frac{1}{x^2}$):

$$(u - 1)^2 + \left(v - \frac{1}{x}\right)^2 = \left(\frac{1}{x}\right)^2$$

This circle has its center at coordinates $\left(1,\, \frac{1}{x}\right)$ and radius $\frac{1}{|x|}$.

All constant reactance circles are centered on the vertical line $u = 1$ (the right edge of the chart). They appear as arcs rather than full circles because only the portion falling inside the unit circle corresponds to physical passive impedances. As $|x|$ increases, the center approaches the horizontal axis and the radius shrinks, producing tighter arcs near the right edge. As $|x| \to 0$, the radius approaches infinity, and the arc flattens into the horizontal line $v = 0$ (the pure resistance axis). Positive reactance arcs ($x > 0$) curve through the upper half of the chart, representing inductive behavior. Negative reactance arcs ($x < 0$) curve through the lower half, representing capacitive behavior.

## Architecture

### Reading the Chart: Landmarks and Navigation

The overlaid grid of constant resistance circles and constant reactance arcs defines a complete coordinate system inside the unit circle. Every point on the chart corresponds to a unique normalized impedance, and every normalized impedance maps to a unique point.

**The center point** is the single most important location. It lies at the intersection of the $r = 1$ resistance circle and the $x = 0$ reactance line, at coordinates $(u, v) = (0, 0)$ on the reflection coefficient plane. This point represents $\Gamma = 0$: a perfect impedance match with zero reflection. The goal of impedance matching network design is to transform the load impedance toward this center point.

**The far left edge** of the horizontal axis, at $(u, v) = (-1, 0)$, represents a short circuit. The resistance is zero and the reactance is zero. The reflection coefficient magnitude is 1, and the phase is 180 degrees. The signal encounters a direct path to ground, reflecting all energy with an inverted voltage.

**The far right edge** of the horizontal axis, at $(u, v) = (1, 0)$, represents an open circuit. The resistance is infinite. The reflection coefficient magnitude is 1, and the phase is zero. All constant resistance circles and all constant reactance arcs converge at this single point.

**The horizontal axis** ($v = 0$, the line cutting straight through the center) represents zero reactance. Every point on this line is a purely resistive impedance. The printed resistance values along this axis begin at zero on the far left, pass through 1 at the center, and reach infinity at the far right.

**The upper half** of the chart ($v > 0$) contains all impedances with positive reactance (inductive behavior). **The lower half** ($v < 0$) contains all impedances with negative reactance (capacitive behavior). The outer circumference of the chart corresponds to the boundary where $r = 0$: purely reactive components with no resistive energy dissipation.

**Reading a specific impedance:** Locating the intersection of the $r = 0.5$ resistance circle with the $x = +1.0$ reactance arc defines the normalized impedance $z = 0.5 + j1.0$. In a 50-ohm system, this denormalizes to $Z_L = 25 + j50$ ohms. The physical distance from the chart center to this intersection point is the magnitude of the reflection coefficient. The angle of this point relative to the positive horizontal axis is the phase of the reflection.

### Coordinate Systems and Measurement

The Smith Chart exists simultaneously in two coordinate systems that serve complementary purposes.

The **Cartesian coordinates** $(u, v)$ span from $-1$ to $+1$ on both axes and define the physical drawing space. The overlaid resistance circles and reactance arcs constitute the impedance grid projected onto this drawing space.

The **polar coordinates** (magnitude and angle) describe the measurement. The radial distance from the center to any plotted point is the magnitude $|\Gamma|$ of the reflection coefficient. The angle from the positive horizontal axis to that point is the phase of the reflected wave. Measurement equipment captures magnitude and phase natively, and the chart provides the visual translation from these polar quantities back to Cartesian resistance and reactance.

### VNA Trace Interpretation

Plotting S-parameter data from a vector network analyzer onto the Smith Chart provides immediate visual insight into channel behavior across frequency.

A well-matched component appears as a tight cluster of points near the chart center. The closer the trace stays to the center, the smaller the reflection coefficient across the measured frequency range. A trace circling tightly around the center as frequency sweeps indicates a broadband impedance match with minor frequency-dependent variation.

A trace residing entirely in the upper hemisphere reveals a predominantly inductive load. A trace confined to the lower hemisphere indicates a predominantly capacitive load. The trajectory of the trace across frequency shows how the impedance evolves: a spiral moving inward toward the center as frequency increases indicates that the match improves at higher frequencies, while a spiral moving outward indicates deteriorating performance.

The Smith Chart transforms abstract complex algebra into a direct visual map that connects the time-domain reflection coefficient measured by TDR instruments to the frequency-domain S-parameter data captured by network analyzers. Both instruments measure the same physical quantity. TDR presents it as a real-valued impedance profile along the spatial length of the trace. The VNA presents it as a complex-valued trajectory sweeping across frequency on the Smith Chart.

## Edge Cases

### The Passive Constraint and the Unit Circle Boundary

The unit circle boundary on the Smith Chart is not an arbitrary choice of scale. It is a direct consequence of energy conservation. A passive network contains no internal energy source. It can absorb energy, store and release energy, or reflect energy, but it cannot create energy. The maximum possible reflection occurs when no energy is absorbed: $|\Gamma| = 1$. This physical limit confines all passive impedances to points at or inside the unit circle.

Points exactly on the boundary ($|\Gamma| = 1$) represent purely reactive loads with zero resistance. An ideal lossless inductor or an ideal lossless capacitor reflects all incident energy with zero absorption. The $r = 0$ circle traces this boundary exactly.

Points inside the boundary ($|\Gamma| < 1$) represent loads with nonzero resistance. Some energy is dissipated as heat in the resistive component, and less than 100% reflects.

### The Extended Smith Chart

Active circuits containing transistor amplifiers or negative-resistance oscillators can generate reflection coefficients with magnitudes exceeding 1. A device that adds energy to the reflected wave produces $|\Gamma| > 1$, and its impedance maps to a point outside the unit circle.

The polar coordinate system underlying the Smith Chart is not bounded by the unit circle. Polar coordinates define the entire infinite plane using a radial distance from the origin and an angular rotation from a reference axis. The radial distance can extend from zero to infinity. The extended Smith Chart expands the printed region beyond the standard boundary to accommodate these active-device measurements, preserving the same families of resistance circles and reactance arcs extrapolated into the region where $|\Gamma| > 1$.

### Conformal Mapping Preserves Angles but Distorts Distances

The mapping from the impedance plane to the reflection coefficient plane is conformal (angle-preserving) but not isometric (distance-preserving). Equal increments of resistance in the impedance plane do not correspond to equal distances on the chart. The region near the center (around $r = 1$) is expanded relative to the extremes. Impedance values near the matched condition occupy a large visual area, providing high resolution exactly where engineers need it most. Impedance values near short or open circuits are compressed into narrow regions near the chart boundary, reflecting the physical reality that extreme mismatches are easy to detect but difficult to differentiate with precision.

This nonuniform spatial scaling is an inherent feature of the conformal mapping, not a limitation. It concentrates visual resolution on the impedance range where matching network adjustments are most sensitive.
