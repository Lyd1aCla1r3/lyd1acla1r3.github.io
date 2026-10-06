# Inductance and Magnetic Coupling

<!-- SUMMARY: Current flowing through a conductor generates a magnetic field that stores energy and resists changes in current flow. This guide covers self-inductance, mutual inductance, and the crosstalk coupling mechanisms that transfer energy between adjacent signal traces on a PCB through shared magnetic and electric fields. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

Inductance governs the magnetic dimension of every high-speed transmission line. The electric field stores energy in the dielectric between the trace and the ground plane, defining capacitance. The magnetic field stores energy in the current loop formed by the outbound trace and the return path, defining inductance. The ratio of these two distributed parameters sets the characteristic impedance, and the product of them sets the propagation velocity. Controlling inductance is therefore inseparable from controlling signal integrity.

The concept divides naturally into two distinct mechanisms. Self-inductance describes the opposition that a single conductor's own magnetic field generates against changes in its own current. Mutual inductance describes the magnetic coupling between two separate conductors, where the changing field of one induces a voltage in the other. In a transmission line, both mechanisms act simultaneously. The total loop inductance of the system depends on the self-inductance of the outbound trace, the self-inductance of the return plane, and the mutual inductance bridging the gap between them. Engineers who understand how physical geometry controls each of these three quantities can predict and manage the inductive behavior of any PCB structure.

This guide develops the physics from the microscopic scale upward: the origin of macroscopic fields from individual electron contributions, the internal field gradient inside a solid conductor, the mathematical structure of self-inductance and mutual inductance, the Reciprocity Theorem that enforces symmetric coupling, and the total loop inductance equation that ties the entire system together.

## Core Concepts

### The Origin of Macroscopic Fields: Superposition

Every moving electron in a conductor generates its own microscopic magnetic field. These individual fields are tiny, perfectly circular loops (often visualized as "hula hoops") centered on each electron's trajectory. The macroscopic magnetic field that engineers measure with instruments is the vector sum of trillions of these microscopic contributions. This is the Principle of Superposition: the total field at any point in space is the mathematical addition of every individual electron's field at that point.

The shape of the physical conductor dictates the geometric arrangement of the moving electrons, and that arrangement determines how the microscopic fields combine.

Packing all the electrons into a tight cylindrical wire forces their individual hula hoops into close proximity. The fields add constructively, producing tight, dense concentric circles immediately outside the wire. Spreading the same electrons across a massive flat copper plane changes the superposition pattern. The horizontal components of adjacent hula hoops cancel each other, while the vertical components add together, transforming the macroscopic field into a wide, diffuse oval rather than a compact circle.

The microscopic physics of each electron remains identical in both cases. The geometry of the copper simply determines which components of the individual fields reinforce and which cancel. Compressing a conductor does not alter the fundamental behavior of any single electron; it packs the charge carriers into a tighter bundle, forcing their superimposed macroscopic field to occupy a much denser volume.

### Self-Inductance and the Effect of Trace Width

Self-inductance measures the magnetic opposition that a conductor's own field exerts against changes in its current. The physical mechanism is direct: a changing current generates a changing magnetic field, which (by Faraday's Law) induces a voltage that opposes the original current change. The magnitude of this opposition depends on how much magnetic flux the conductor's geometry allows it to generate per ampere of current.

Trace width has a pronounced effect on self-inductance. Ampere's Law dictates that magnetic field strength is inversely proportional to distance from the current source. In a wide trace, the current spreads across a large cross-section, producing a broad, diffuse magnetic field with significant internal cancellation between the left and right edges. A narrow trace forces the same total current through a small physical bottleneck. The magnetic field lines crowd extremely close to the concentrated charge flow, creating an intense, spatially compressed field that stores more magnetic energy per unit length. The result is a higher self-inductance for the narrow trace.

This relationship has a practical interpretation: a narrow trace acts like a series inductor. The dense magnetic field surrounding the bottleneck physically resists rapid changes in current. High-frequency signals, which carry an astronomically high rate of change ($dI/dt$), encounter a violent opposing voltage (back-EMF) that chokes off the fast edge content. Low-frequency signals, with a near-zero rate of change, pass through unaffected. The narrow trace therefore behaves as a geometric low-pass filter, rounding the edges of the propagating wavefront and degrading the signal at the receiver.

### The Internal B-Field Gradient

The relationship between field strength and distance from the current takes on a distinctive character inside a solid conductor. Outside the wire, the field decreases with distance, matching the common intuition that fields weaken as you move away from the source. Inside the wire, the gradient runs in the opposite direction.

Ampere's Law states that the magnetic field strength along a circular boundary is proportional to the total current physically enclosed within that boundary. Applying this rule at different radii inside the conductor reveals a systematic gradient:

At the exact center, a measuring circle of zero radius encloses zero current. The magnetic field is exactly zero. Moving outward, the measuring circle captures progressively more cross-sectional area and therefore more current. The field strength grows steadily. At the surface, the measuring circle encompasses the entire cross-section and encloses 100 percent of the current, producing the maximum internal field strength.

The field increases linearly from zero at the center to its maximum at the surface. This linear behavior arises from a geometric ratio: the enclosed current grows with the area of the measuring circle ($\propto r^2$), while the boundary length grows only with its circumference ($\propto r$). Dividing the enclosed current by the circumference leaves a field strength proportional to the radius.

Stepping outside the wire, the enclosed current stops growing (all of it is already inside the boundary), and the field begins to fall off with distance.

### The Shell Theorem Analog: Why Outer Current Cancels

The zero-contribution of current outside the measuring radius is not an approximation; it is a rigorous consequence of cylindrical symmetry, analogous to the gravitational shell theorem in mechanics.

A solid conductor can be conceptually decomposed into a solid inner core of radius $r$ and a hollow outer pipe surrounding it. The question is: what magnetic field does the current in the outer pipe generate at a point inside its cavity?

At any point inside the hollow pipe, competing magnetic forces act from every direction. The current in the pipe wall closest to the point generates a strong, localized field. The current on the far side of the pipe, being more distant, generates a weaker field pointing in the opposite direction. Geometry dictates that there is more copper (and more total current) spanning the wide arc on the far side than on the narrow arc nearby. The larger magnitude of distant current perfectly offsets the stronger influence of the close current. Integrating the field contributions from every degree of the circular pipe wall reveals exact, uniform cancellation. The net magnetic field anywhere inside the cavity of a hollow current-carrying cylinder is precisely zero.

A solid wire is an infinite series of concentric hollow tubes nested together. At any internal radius $r$, all the copper outside that radius behaves as a collection of these hollow tubes, each contributing zero net field to the interior. The only current capable of generating a measurable magnetic field at radius $r$ is the current flowing physically inside radius $r$.

The copper medium does not change across the boundary, and the electrons do not behave differently depending on where an imaginary line is drawn. The boundary simply divides the uniform electron population into two geometric groups: electrons located farther from the center than the measurement point surround it symmetrically, forcing their individual field vectors to cancel at that coordinate; electrons located closer to the center fail to surround the point, so their field vectors add constructively and produce the measurable field.

### Mutual Inductance and Geometry

Mutual inductance ($M$) measures the efficiency of magnetic coupling between two separate current paths. Current flowing through the outbound trace generates a magnetic field that expands into three-dimensional space. A portion of those field lines physically intersect the return plane. Mutual inductance quantifies exactly how much of that flux successfully couples to the second conductor.

This coupling efficiency is entirely dictated by physical geometry. A thick dielectric separating the trace from the ground plane allows a large fraction of the magnetic field to dissipate into the surrounding material before reaching the return path. The resulting poor magnetic coupling yields a low mutual inductance. Compressing the dielectric gap moves the ground plane closer to the trace, allowing it to intercept a much larger fraction of the expanding field lines and drastically increasing the mutual inductance.

### The Reciprocity Theorem ($M_{12} = M_{21}$)

A narrow trace and a wide ground plane are physically very different shapes. The trace generates a dense, localized magnetic field; the plane generates a broad, diffuse one. It seems counter-intuitive that these two conductors would share the same mutual inductance value.

The Reciprocity Theorem resolves this apparent asymmetry. Mutual inductance is a shared geometric property of the entire two-conductor system, not an attribute of either conductor individually. The theorem guarantees that the magnetic coupling between any two arbitrary shapes is perfectly symmetric, regardless of their individual physical profiles.

The underlying mechanism is a precise geometric balance. A highly concentrated magnetic source (the narrow trace) projects its field onto a massive receiving area (the wide plane). The field weakens over distance, but the enormous surface area of the plane acts as a giant net, intercepting the weaker, expanding field lines. The total intercepted flux reaches some definite value.

Reversing the experiment, the wide plane generates a weak, diffuse field spread across its entire surface. The narrow trace presents a tiny cross-sectional area, acting as a very small net. Intercepting a weak field with a small net seems destined to produce negligible flux. However, every microscopic slice of current distributed across the vast width of the plane contributes a tiny field vector that reaches up and touches the trace. Integrating all of these contributions from the full width of the plane reveals an exact mathematical balance: the total flux coupled to the narrow trace equals the total flux coupled to the wide plane. The physical shapes dictate the shape of each conductor's magnetic field, but the integrated coupling ratio remains a perfectly symmetric geometric constant.

This symmetry is why the total loop inductance equation contains the term $2M$ rather than $M_{12} + M_{21}$: the two values are identical by physical law.

## Architecture

### The Total Loop Inductance Equation

The magnetic behavior of a complete transmission line circuit is captured by the total loop inductance:

$$L_{loop} = L_1 + L_2 - 2M$$

where $L_1$ is the self-inductance of the outbound trace, $L_2$ is the self-inductance of the return plane, and $M$ is the mutual inductance between them.

This formula derives directly from Faraday's Law and the voltage drops within the current loop. Inductance translates a changing current into a voltage: $V = L(dI/dt)$. The total voltage drop around the loop is the sum of four contributions:

1. The outbound trace produces a self-induced voltage of $L_1(dI/dt)$.
2. The return plane produces a self-induced voltage of $L_2(dI/dt)$.
3. The outbound trace's magnetic field cuts through the return plane. The return current flows in the opposite direction ($-dI/dt$), so this mutually induced voltage is $-M(dI/dt)$.
4. Symmetrically, the return plane's magnetic field cuts through the outbound trace, inducing another $-M(dI/dt)$.

Adding all four components and factoring out the current change yields the total loop inductance. The engineering consequence is immediate: physically compressing the dielectric gap maximizes $M$, which mathematically cancels the self-inductance contributions and drives the total loop inductance toward zero.

The quantities $L_1$ and $L_2$ are not assigned to the entire length of the trace and plane at once. They describe an infinitesimally small geometric slice of the transmission line (typically modeled as one millimeter long). The per-unit-length parameters are integrated along the full trace length to model the complete board.

### Loop Inductance vs. Self-Inductance

Self-inductance in isolation measures the magnetic opposition generated by a single conductor suspended in an infinite vacuum, disconnected from any return path. It answers a purely theoretical question about one wire's intrinsic magnetic storage.

Loop inductance measures the total magnetic opposition of the complete, closed circuit that exists in reality. It incorporates the outbound conductor, the return conductor, and the mutual magnetic interaction bridging the space between them. The distinction matters because no real signal exists without a return path. The self-inductance of an isolated trace is a mathematical abstraction; the loop inductance is the physical quantity that determines signal behavior.

High-frequency current crowds tightly underneath the trace precisely to minimize loop inductance. The self-inductance of the return path increases slightly as the current concentrates into a narrow band, but this penalty is overwhelmed by the massive reduction in loop area and the corresponding increase in mutual inductance. The current organically settles into the exact spatial distribution that minimizes total impedance at each frequency.

### Loop Resistance and Why It Lacks Spatial Interaction

Resistance and inductance respond to conductor spacing in fundamentally different ways.

The geometric resistance of a conductor is $R = \rho \cdot (L_{trace} / A)$, where $\rho$ is the copper resistivity, $L_{trace}$ is the trace length, and $A$ is the cross-sectional area of the current path. Maximizing $A$ by spreading the return current across the full width of the ground plane places a large number in the denominator, driving resistance to its minimum.

Magnetic fields project outward into three-dimensional space. The physical distance separating the outbound and return paths drastically alters the mutual inductance. Resistance, by contrast, remains entirely confined within the physical boundaries of the copper. Moving a return trace closer to an outbound trace produces zero change in total series resistance. The spacing does not affect the pure addition of the two resistive values. The concept of an interacting "loop" is physically irrelevant for resistance calculations, which is why the term "loop resistance" rarely appears in engineering literature, while "loop inductance" is a core design parameter.

This asymmetry explains the frequency-dependent behavior of return current distribution. At low frequencies, inductive reactance ($X_L = 2\pi f L$) vanishes, leaving DC resistance as the dominant impediment. The current spreads across the full ground plane to maximize cross-sectional area and minimize resistance. At high frequencies, the inductive reactance grows to dominate the impedance budget. The current crowds under the trace to minimize loop area and loop inductance, accepting a higher resistance penalty as the cost of reducing the overwhelmingly larger inductive term.

## Worked Examples

### Proving Reciprocity: Narrow Trace Driving a Wide Plane

The mutual inductance formula $M = \Phi / I$ provides a concrete framework for verifying that $M_{AB} = M_{BA}$.

**Setup:** Trace A is a narrow, focused copper wire. Trace B is a massive, wide copper plane. They are positioned parallel to each other, separated by a vertical distance $D$.

**$M_{AB}$ (Trace drives Plane):** Injecting exactly 1 Ampere into the narrow Trace A generates a dense, concentrated magnetic field radiating outward in tight concentric circles. The field weakens over the distance $D$, but the vast surface area of the wide plane below acts as a large net, intercepting the weakening field lines across its full extent. Summing all intercepted flux yields $\Phi_B = 50$ Webers (hypothetical value). The mutual inductance is $M_{AB} = 50 / 1 = 50$ Henrys.

**$M_{BA}$ (Plane drives Trace):** Reversing the experiment, 1 Ampere flows through the wide plane, generating a weak, diffuse field at any localized point above it. The narrow trace presents a tiny cross-sectional area. Intercepting a weak field with a small net appears destined to produce negligible flux. However, every microscopic current element across the full width of the plane contributes a tiny field vector reaching up to the trace. Integrating these contributions from the entire width yields $\Phi_A = 50$ Webers. The mutual inductance is $M_{BA} = 50 / 1 = 50$ Henrys.

The geometric balance is exact. A concentrated source projecting onto a large receiver produces the same total flux as a diffuse source projecting onto a small receiver. The coupling ratio is a symmetric geometric constant.

### Narrow Trace Bottleneck as a Series Inductor

Consider a 50-ohm microstrip trace with a manufacturing defect that narrows a short section of the trace. The properly designed section spreads the signal current across a calculated width, producing a diffuse magnetic field with significant internal cancellation between the left and right edges.

At the narrow bottleneck, the same current is forced through a reduced cross-section. The magnetic field lines compress into a dense ring surrounding the bottleneck, storing more magnetic energy per unit length and locally increasing the self-inductance.

The effect is frequency-dependent. A high-frequency wavefront carries a rapid $dI/dt$, which, when combined with the elevated local inductance, generates a large opposing back-EMF. This back-EMF partially blocks the high-frequency content of the edge, reflecting energy backward. A low-frequency signal has a near-zero $dI/dt$; the dense magnetic field remains static and generates no opposition, so the low-frequency content passes through encountering only a trivial increase in DC resistance.

The net effect at the receiver is a signal with its high-frequency building blocks stripped away: a rounded, sloped transition instead of a sharp edge. On a TDR display, the instrument records the localized impedance increase as a positive bump, pinpointing the exact physical location of the bottleneck.

## Edge Cases

### Two Geometries, One Inductance Increase

Trace width and loop area both affect inductance, but through different physical mechanisms. Confusing the two is a common source of error.

A *narrow trace width* increases self-inductance by concentrating the magnetic field. All of the current flows through a small cross-section, eliminating the parallel cancellation that exists in a wide trace. The field density rises, and more magnetic energy is stored per unit length.

A *wide loop area* (large vertical separation between the trace and the return plane) increases loop inductance by allowing the magnetic field to occupy a larger physical volume. More field lines are enclosed by the loop geometry, yielding more total flux per ampere.

Both mechanisms increase inductance, but they are geometrically independent. A designer can have a wide trace (low self-inductance) on a thick dielectric (high loop inductance), or a narrow trace (high self-inductance) on a thin dielectric (low loop inductance). Optimal design minimizes both: a correctly calculated trace width avoids unnecessary field concentration, and a thin dielectric maximizes mutual coupling to drive the loop inductance term toward zero.

### The Parasitic Via Capacitor vs. the Parasitic Narrow Trace

Both parasitic capacitance and parasitic inductance degrade high-frequency edge content, but through opposite mechanisms. A parasitic via capacitor provides a parallel escape route, shunting high-frequency energy into the ground plane and draining it from the signal path. A parasitic narrow trace acts as a series barrier, generating inductive back-EMF that blocks high-frequency energy and reflects it backward toward the source.

The measured result at the receiver is identical in both cases: a transition missing its high-frequency harmonics, producing a slower, more rounded edge. The distinction matters for diagnosis. On a TDR display, the capacitive parasitic appears as a negative dip (local impedance decrease), while the inductive parasitic appears as a positive bump (local impedance increase).
