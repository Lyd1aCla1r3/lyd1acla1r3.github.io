# Inductance, Magnetic Coupling, and Crosstalk

<!-- SUMMARY: A changing current in one conductor creates a changing magnetic field, and that field induces voltages in the same conductor and in every conductor nearby. This guide derives the field of a current from Ampere's law (outside and inside a wire), states Faraday's and Lenz's laws as three distinct statements, introduces the Generation Rule and the Reaction Rule for applying the right-hand rule, works through the four cases of induction, derives self, mutual, and loop inductance with the reciprocity theorem, and then derives the near-end and far-end crosstalk between adjacent traces, including why backward coupling is the sum of capacitive and inductive coupling while forward coupling is their difference. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Chapter 3](03_Impedance_Reflections_and_Termination.md) used the inductance $L$ as a given number: a 1 nH parasitic inductor reflects the edge, and a narrow trace behaves as a series inductance. This chapter explains where that number comes from, why it depends on geometry, and how the magnetic field of one conductor induces a voltage in another, which is the mechanism behind crosstalk between neighboring traces.

The electric field of a transmission line stores energy in the dielectric between the trace and the ground plane and defines the capacitance. The magnetic field stores energy in the current loop formed by the outbound trace and the return path and defines the inductance. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) showed that the ratio of the two per-unit-length quantities sets the characteristic impedance and that their product sets the propagation velocity, so controlling inductance is inseparable from controlling signal integrity.

The subject divides into two mechanisms that differ in which conductor receives the induced voltage. Self-inductance describes the opposition that a conductor's own changing field creates against changes in its own current. Mutual inductance describes the coupling between two separate conductors, in which the changing field of one induces a voltage in the other. Both act simultaneously in every transmission line, and the total loop inductance depends on the self-inductance of the outbound trace, the self-inductance of the return path, and the mutual inductance between them.

This guide develops the physics in order: the field of a current from Ampere's law, the field inside a conductor, Faraday's and Lenz's laws and the two rules for applying the right-hand rule, the four cases of induction, the definitions of self, mutual, and loop inductance, and finally the crosstalk that mutual coupling produces between adjacent traces.

## Core Concepts

### The Magnetic Field of a Current: Ampere's Law and the Generation Rule

Ampere's law states that the line integral of the magnetic field $\mathbf{B}$ around any closed path equals the permeability of free space $\mu_0$ times the current enclosed by the path:

$$\oint \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{enc}$$

Charges in motion produce the field, and the field of any conductor is the vector sum of the contributions of all its moving charges. This is the principle of superposition: the total field at a point is the addition, with direction, of the fields that each current element produces there.

The right-hand rule gives the direction of the field. This series calls the procedure the **Generation Rule**: point the thumb of the right hand along the current, and the fingers curl in the direction of the magnetic field circling the conductor. The Generation Rule answers the question of which way the field points when a current is known, and it is applied once, at the start of any analysis.

For a long straight wire, symmetry makes the field tangent to circles centered on the wire and constant in magnitude on each circle. Choosing a circle of radius $r$ outside the wire, the enclosed current is the full current $I$, and the integral reduces to the field times the circumference:

$$B \cdot 2\pi r = \mu_0 I \quad \Rightarrow \quad B(r) = \frac{\mu_0 I}{2\pi r}$$

The field falls in inverse proportion to the distance from the wire. A wide, flat conductor such as a ground plane shapes the field differently. Consider a very wide sheet carrying a current per unit width $K$. At a point above the sheet, the contributions of strips lying at equal distances to the left and to the right have equal magnitudes and point at mirror-image angles, so the components perpendicular to the sheet cancel while the components parallel to the sheet add. The resulting field is parallel to the sheet, and Ampere's law with a rectangular path that straddles the sheet (two sides parallel to the sheet at equal heights above and below, each of length $w$) gives:

$$B \cdot 2w = \mu_0 K w \quad \Rightarrow \quad B = \frac{\mu_0 K}{2}$$

This uniform field points in opposite directions on the two sides of the sheet. The geometry of the copper therefore selects which components of the contributions of the individual current elements reinforce and which cancel: a compact wire produces tight circles around itself, and a wide sheet produces a broad, uniform field parallel to its surface. The behavior of each moving charge is identical in both cases.

[Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) added the Ampere-Maxwell term, which lets a changing electric field produce a magnetic field in the same way as a current. The remainder of this chapter concerns fields produced by conduction current, and the displacement-current contribution is not repeated here.

### The Field Inside a Conductor

Inside a solid wire of radius $a$ carrying a uniform current density $J = I/(\pi a^2)$, the same circular symmetry applies. A circle of radius $r < a$ encloses only the part of the current that flows through the area $\pi r^2$:

$$I_{enc} = J \pi r^2 = I \, \frac{r^2}{a^2}$$

Ampere's law gives the field at radius $r$:

$$B \cdot 2\pi r = \mu_0 I \, \frac{r^2}{a^2} \quad \Rightarrow \quad B(r) = \frac{\mu_0 I \, r}{2\pi a^2}$$

The field is zero at the center, where a circle of zero radius encloses no current, and grows in direct proportion to $r$, because the enclosed current grows with the area ($\propto r^2$) while the circumference grows only with the radius ($\propto r$). At the surface ($r = a$) the result equals the external expression $\mu_0 I/(2\pi a)$, and beyond the surface the field falls as $1/r$. Assume 1 A flows in a wire of radius 0.1 mm. The field is 1 mT halfway to the surface, reaches its maximum of 2 mT at the surface, and falls to 0.2 mT at a distance of 1 mm from the axis.

Ampere's law uses only the enclosed current, so the copper outside the circle contributes nothing at radius $r$. The same fact follows from a geometric argument about a hollow current-carrying pipe. Consider a point inside the cavity and a narrow cone of angle $d\theta$ that opens from the point and cuts the wall on both sides. The wall length cut by the cone is proportional to the distance from the point, so the nearer segment carries less current and the farther segment carries more current in direct proportion to its distance. A line current produces a field proportional to its current divided by its distance, so both segments produce fields of equal magnitude, and they point in opposite directions. Every cone cancels, and the field inside a hollow current-carrying cylinder is zero. A solid wire is a nest of such hollow tubes, so only the current inside radius $r$ produces the field at radius $r$.

The uniform current density assumed here holds at DC. At high frequency the changing field inside the conductor drives currents of its own, which push the current distribution toward the surface, and [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) analyzes that redistribution.

### Faraday's Law, Lenz's Law, and Ampere's Law as Three Distinct Statements

Three statements about electromagnetic induction are often blended, and keeping them separate removes most of the confusion about which direction is which.

1. **Ampere's law** describes the generation of a magnetic field by a current. A current is the cause and a field is the effect.
2. **Faraday's law** describes the generation of a voltage by a changing magnetic flux. The magnetic flux $\Phi$ through a surface is the integral of the perpendicular component of $\mathbf{B}$ over the surface, and a changing flux through a loop produces an electromotive force (EMF) around the loop: $\mathcal{E} = -d\Phi/dt$.
3. **Lenz's law** is the minus sign in Faraday's law. It states that the EMF drives a current whose own magnetic field opposes the change in flux that produced it.

Ampere's law concerns the field that a current creates, and Lenz's law concerns the reaction of a conductor to a change in the field that passes through it. A conductor that is not exposed to a changing field shows no Lenz effect, and a conductor carrying a steady current is surrounded by a steady field with no induced EMF.

### The Reaction Rule

Applying the right-hand rule to find the direction of an induced current requires a second procedure, distinct from the Generation Rule. This series calls it the **Reaction Rule**:

1. Use the Generation Rule to find the direction of the existing field and decide whether its magnitude is increasing or decreasing.
2. Write down the direction of the opposing field that Lenz's law demands: opposite to the existing field when the flux grows, and parallel to it when the flux shrinks.
3. Point the right-hand thumb along that opposing field, and read the direction of the induced current from the curl of the fingers around the thumb.

The two rules are applied one after the other with a pause between them, and they are never chained into a single motion. The Generation Rule starts from a current and produces a field. The Reaction Rule starts from a changing field, produces an opposing field, and only then reads the current that would generate that opposing field. [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) uses the Reaction Rule inside a single conductor to explain the skin effect, and the crosstalk section below uses it between two conductors.

### The Four Cases of Induction

Four situations cover the cases in which a conductor and a magnetic field interact.

**Case 1: a constant current in an isolated conductor.** The field is steady, the flux is constant, and $d\Phi/dt = 0$. No EMF is induced and the conductor shows only its DC resistance.

**Case 2: a changing current in an isolated conductor.** The field changes in proportion to the current, and the changing flux induces an EMF that opposes the change in the conductor's own current. This opposition is the back-EMF of self-inductance. It acts on every part of the conductor, and the internal distribution of that opposition is the cause of the skin effect treated in Chapter 5.

**Case 3: a changing current near a second conductor.** The changing field of the first conductor passes through the loop of the second, and the induced EMF drives a current in the second conductor. This is mutual inductance, and it is the inductive part of crosstalk.

**Case 4: a conductor moving through a static field.** The force on the moving charges produces an EMF without any change in the field. This motional EMF is the principle of generators and has no role in the signal paths studied here, and it is included for completeness.

Case 2 occurs inside Case 3, because every conductor reacts to the changing field of its own current and to the changing fields of its neighbors at the same time, and the two effects add by linear superposition. A current already flowing in the second conductor does not alter the induced current from the first, because the induced contribution is simply added to it.

### Inductance Defined

Ampere's law shows that the field is proportional to the current that produces it, so the flux through a given loop is also proportional to that current. The constant of proportionality is the inductance of the loop:

$$\Phi = L\, I$$

The unit is the henry, equal to one weber per ampere or one volt-second per ampere. Faraday's law gives the EMF induced by a changing current, and the minus sign records the opposition of Lenz's law:

$$\mathcal{E} = -\frac{d\Phi}{dt} = -L\,\frac{dI}{dt}$$

A source that drives the current against this back-EMF must supply the opposite voltage across the inductor, which gives the circuit equation used in Chapter 3:

$$v = L\,\frac{dI}{dt}$$

The flux that a current $I_A$ in one loop produces through a second loop defines the mutual inductance in the same way, $\Phi_{BA} = M\, I_A$, and the EMF induced in the second loop is $-M\, dI_A/dt$.

## Architecture

### Self-Inductance and the Effect of Trace Width

Self-inductance measures how much magnetic flux a conductor's geometry produces per ampere of its own current. Trace width has a pronounced effect on it. The field of a current is stronger close to the current, so a narrow trace that concentrates the current in a small cross-section produces a field that is denser near the conductor and stores more magnetic energy per unit length than a wide trace carrying the same current. The narrow trace therefore has a higher inductance per unit length.

Chapter 1 showed that the inductance and capacitance per unit length change in opposite directions when the width changes, so a narrower trace over the same plane has a lower capacitance, a higher inductance, and a higher characteristic impedance. The inductance per unit length is tied to the impedance and the velocity by $L' = Z_0/v_p$, which follows from $Z_0 = \sqrt{L'/C'}$ and $v_p = 1/\sqrt{L'C'}$ (the symbols with a prime denote per-unit-length values).

A short narrow section acts as a series inductor. The back-EMF of the extra inductance is proportional to $dI/dt$, so it is small for the slow change of a low-frequency signal and large for the fast change of an edge. The section therefore behaves as a low-pass filter: it passes the low-frequency content, reflects part of the high-frequency content as derived in Chapter 3, and rounds the edge that continues to the receiver.

### Mutual Inductance and Geometry

Mutual inductance $M$ measures the efficiency of magnetic coupling between two current paths. The current in the outbound trace generates a field that spreads through space, and a fraction of the field lines pass through the loop of the second path. The mutual inductance is the flux through the second loop per ampere in the first.

Geometry alone determines how strongly the two paths couple. A thick dielectric between the trace and the ground plane lets the field spread over a wide region before it reaches the plane, so only a small fraction of the field links the return path, and the mutual inductance is low. Compressing the dielectric moves the plane close to the trace, so the plane intercepts a much larger fraction of the field lines and the mutual inductance rises.

### The Reciprocity Theorem

A narrow trace and a wide ground plane are very different shapes. The trace produces a dense, localized field, and the plane produces a broad, uniform one. It seems that the flux linking the plane because of a current in the trace should differ from the flux linking the trace because of the same current in the plane. The reciprocity theorem states that the two are equal:

$$M_{12} = M_{21}$$

The equality follows from the Neumann formula for the mutual inductance of two current paths $C_1$ and $C_2$:

$$M_{12} = \frac{\mu_0}{4\pi} \oint_{C_1} \oint_{C_2} \frac{d\mathbf{l}_1 \cdot d\mathbf{l}_2}{r}$$

where $r$ is the distance between the two line elements. The expression is unchanged when the labels 1 and 2 are exchanged, so $M_{12} = M_{21}$ for any pair of shapes. The derivation of the Neumann formula uses vector calculus beyond the scope of this guide, and it is stated here with every symbol defined. The physical content is that a concentrated source projecting onto a large receiver and a diffuse source projecting onto a small receiver couple the same total flux, and mutual inductance is a property of the pair of conductors and not of either one alone.

The symmetry is the reason the loop inductance equation below contains the term $2M$ and not the sum $M_{12} + M_{21}$ of two different values.

### The Total Loop Inductance Equation

A signal needs a return path, so the quantity that governs signal behavior is the inductance of the complete loop. Let a current $I$ flow along conductor 1 (the trace) and return along conductor 2 (the plane). Each conductor carries a partial self-inductance, $L_1$ and $L_2$, which describes the flux that conductor's own current produces through the loop, and the mutual inductance $M$ links them.

Take the reference direction of current along the trace, so the trace carries $+I$ and the plane carries $-I$ in that direction. The voltage along each conductor combines its own back-EMF and the EMF induced by the other conductor:

$$v_1 = L_1 \frac{dI}{dt} + M \frac{d(-I)}{dt} = (L_1 - M)\frac{dI}{dt}$$

$$v_2 = L_2 \frac{d(-I)}{dt} + M \frac{dI}{dt} = -(L_2 - M)\frac{dI}{dt}$$

The loop voltage is the drop along the outbound conductor minus the drop along the return conductor, because the loop traverses the return path in the opposite direction:

$$v_{loop} = v_1 - v_2 = (L_1 - M)\frac{dI}{dt} + (L_2 - M)\frac{dI}{dt}$$

Factoring out $dI/dt$ gives the total loop inductance:

$$L_{loop} = L_1 + L_2 - 2M$$

The minus sign on $M$ arises because the return current flows opposite to the outbound current, so the magnetic coupling between the two conductors cancels part of each self-inductance. Compressing the dielectric raises $M$ and lowers $L_{loop}$. The reduction has a floor, because the coupling cannot exceed the geometric mean of the two self-inductances, $M \le \sqrt{L_1 L_2}$. Substituting this bound gives the smallest possible loop inductance:

$$L_{loop} \ge L_1 + L_2 - 2\sqrt{L_1 L_2} = \left(\sqrt{L_1} - \sqrt{L_2}\right)^2$$

The loop inductance approaches zero only when the two conductors have equal self-inductances and perfect coupling. A trace and a wide plane have unequal self-inductances, so the floor is positive, and the loop inductance of a real structure remains finite however thin the dielectric becomes.

The quantities $L_1$, $L_2$, and $M$ in this equation are partial inductances, which describe the contribution of a segment of the loop and have no independent meaning for an isolated segment. The per-unit-length values $L'$ and $M'$ apply to a slice of line whose length $\Delta z$ is small compared with the shortest wavelength in the signal, and the values for a full trace follow from summing the slices along its length.

### Loop Inductance versus Self-Inductance

The self-inductance of a conductor considered alone, with no return path, answers a theoretical question about the flux of one wire in free space. Loop inductance describes the complete, closed circuit that exists in practice, and it includes the outbound conductor, the return conductor, and the coupling between them. No real signal exists without a return path, so the loop inductance is the quantity that determines signal behavior.

High-frequency return current gathers directly beneath the trace to minimize the loop inductance. Concentrating the return current into a narrow band raises the self-inductance of the return path slightly, because a narrower current distribution produces a denser field, but the penalty is much smaller than the benefit: the loop area shrinks and the mutual inductance with the trace rises. The current settles into the distribution that minimizes the total impedance at each frequency, and [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) describes the resulting return-path behavior in detail.

### Loop Resistance and Why It Lacks Spatial Interaction

Resistance and inductance respond to conductor spacing differently at DC. The resistance of a conductor of length $\ell$ and cross-section $A$ is $R = \rho_r\, \ell / A$, where $\rho_r$ is the resistivity of copper. Spreading the return current across the full width of the ground plane enlarges $A$ and lowers the resistance. At DC the current is confined to the copper and distributes itself uniformly, so the spacing between the outbound and return paths has no effect on the total series resistance, and the term "loop resistance" carries no extra information beyond the sum of the two resistances. Magnetic fields project into the surrounding space, so the spacing changes the mutual inductance strongly, and "loop inductance" is a central design parameter.

The statement is exact only for uniform current. At high frequency the currents in neighboring conductors redistribute under each other's fields, an effect called the proximity effect, and the effective resistance then depends on spacing.

The frequency-dependent distribution of return current follows from the comparison between the two terms. At low frequencies the inductive reactance $\omega L$ is small, the DC resistance dominates the impedance, and the current spreads across the whole ground plane to minimize resistance. At high frequencies the reactance grows to dominate the impedance, and the current gathers under the trace to minimize the loop inductance, accepting a higher resistance as the price of the much larger reduction in the inductive term.

### Crosstalk: Coupling Between Neighboring Traces

Crosstalk is the transfer of energy from one trace, the aggressor, to a neighboring trace, the victim. Two mechanisms operate together in producing crosstalk. The **capacitive coupling** is the electric-field link: a mutual capacitance per unit length $C_m$ lets the changing voltage of the aggressor drive displacement current into the victim. The **inductive coupling** is Case 3 of the four cases: the changing current of the aggressor induces an EMF in the victim loop, characterized by a mutual inductance per unit length $L_m$.

Two locations on the victim define the measurements. The **near end** is the end of the victim next to the aggressor's transmitter, and the **far end** is the end next to the aggressor's receiver. The words refer to fixed positions on the board relative to the point where the aggressor launches its signal, and the direction of the victim's own traffic is irrelevant. **Near-end crosstalk (NEXT)** is the noise that appears at the victim's near end, which is carried by a wave traveling backward on the victim. **Far-end crosstalk (FEXT)** is the noise that appears at the victim's far end, carried by a wave traveling forward.

The directions follow from how each mechanism launches waves on the victim. A short segment of the aggressor with a rising edge passing through it couples two sources into the matching segment of the victim:

- The capacitive coupling injects a displacement current of $C_m\,\Delta z\,dV_a/dt$, where $V_a$ is the aggressor voltage. A current source in a transmission line launches equal currents away from the injection point in both directions, so half of the current travels toward each end, and both launched waves have the positive polarity of the injected current.
- The inductive coupling induces a series EMF of $L_m\,\Delta z\,dI_a/dt$ in the victim. By Lenz's law and the Reaction Rule, the induced current opposes the aggressor's current, so it flows against the direction of the aggressor's travel. A series voltage source launches a forward wave and a backward wave of opposite voltage polarity: the current is continuous through the source, so both waves carry current in the same direction along the line, and the backward wave travels the other way, which reverses the sign of its voltage relative to its current. The induced current in the victim flows backward, so the backward wave has positive polarity and the forward wave has negative polarity.

Both couplings therefore produce a positive wave toward the near end, and the two contributions add. Toward the far end, the capacitive contribution is positive and the inductive contribution is negative, and the two subtract. Backward coupling is the sum of capacitive and inductive coupling, and forward coupling is their difference.

The magnitudes follow from the equations above. Assume the two traces are identical, weakly coupled, and terminated in $Z_0$ at both ends, and let $C$ and $L$ be the self values per unit length of Chapter 1. The relations $Z_0 C' = L'/Z_0 = 1/v_p$ follow from $Z_0 = \sqrt{L'/C'}$ and $v_p = 1/\sqrt{L'C'}$. A wave of half the injected current times $Z_0$ gives the backward capacitive wave from a segment $\Delta z$:

$$\Delta V_{b,C} = \frac{Z_0}{2}\,C_m\,\Delta z\,\frac{dV_a}{dt} = \frac{1}{2}\,\frac{C_m}{C}\,\frac{\Delta z}{v_p}\,\frac{dV_a}{dt}$$

The inductive EMF with $dI_a/dt = (1/Z_0)\,dV_a/dt$ gives half of that EMF as the backward voltage wave:

$$\Delta V_{b,L} = \frac{1}{2}\,\frac{L_m}{Z_0}\,\Delta z\,\frac{dV_a}{dt} = \frac{1}{2}\,\frac{L_m}{L}\,\frac{\Delta z}{v_p}\,\frac{dV_a}{dt}$$

The edge reaches the segment at position $z$ at time $z/v_p$, and the backward wave from that segment reaches the near end after a further $z/v_p$, so the contribution from position $z$ arrives at the near end delayed by $2z/v_p$. Summing over a coupled length $\ell$ with the substitution $\tau = 2z/v_p$ (so that $\Delta z = v_p\,d\tau/2$) turns the integral of the aggressor slope into the difference of the aggressor voltage at two instants:

$$V_{NEXT}(t) = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\int_0^{2T_c} \frac{dV_a(t - \tau)}{dt}\, d\tau = K_b\,\bigl[V_a(t) - V_a(t - 2T_c)\bigr]$$

Here $T_c = \ell/v_p$ is the one-way delay of the coupled region and the backward coupling coefficient is:

$$K_b = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)$$

The bracket reaches the full aggressor swing when the round-trip delay $2T_c$ of the coupled region exceeds the rise time of the edge, and NEXT then forms a flat pulse of height $K_b V_a$ and duration about $2T_c$. The pulse height does not grow with additional coupled length once this condition holds.

Forward waves behave differently, because a forward wave on the victim travels at the same velocity as the aggressor's edge and stays aligned with it. The contribution from every segment reaches the far end at the same instant, $\ell/v_p$ after the edge launches, so the segments add directly instead of spreading out in time. With the capacitive part positive and the inductive part negative:

$$V_{FEXT}(t) = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\frac{\ell}{v_p}\,\frac{dV_a}{dt}\bigg|_{t - \ell/v_p}$$

FEXT is proportional to the slope of the aggressor edge and to the coupled length, so it grows with both. A stripline surrounded by a single uniform dielectric has $C_m/C = L_m/L$, and the forward terms cancel, so its FEXT is ideally zero. A microstrip has air above the trace and laminate below, so the field distribution differs between the electric and magnetic couplings, the inductive ratio $L_m/L$ exceeds $C_m/C$, and the forward crosstalk is nonzero with negative polarity. The two expressions are weak-coupling results for matched terminations and uniform parallel traces. Strong coupling, unmatched terminations that re-reflect the crosstalk, and nonparallel routing require the full coupled-line equations.

Both ratios $C_m/C$ and $L_m/L$ fall as the spacing between the traces grows relative to the height above the plane, because a thinner dielectric ties the fields of each trace to its own plane and reduces the fields that reach the neighbor. Reducing the dielectric height lowers crosstalk at a fixed spacing.

Crosstalk from several aggressors with uncorrelated data adds in power and not in voltage, a rule that [Chapter 8](08_S_Parameters_and_VNA.md) derives together with the decibel arithmetic. [Chapter 8](08_S_Parameters_and_VNA.md) also shows how a multiport VNA measures NEXT and FEXT, and [Chapter 10](10_Jitter_Decomposition_and_Measurement.md) classifies the timing disturbance that crosstalk causes on the victim as bounded uncorrelated jitter.

## Worked Examples

### Case 2 and Case 3 on the Desk

A fixed coordinate frame removes the ambiguity of "above" and "below". Imagine looking down at a flat desk. The $x$ axis points to the right, the $y$ axis points toward the top of the page, and the $z$ axis points up out of the desk toward the viewer.

**Case 2 (self-inductance):** Wire A lies on the desk along the $x$ axis, with its current flowing to the right and increasing. The Generation Rule (thumb to the right) gives a field that points out of the desk, in the $+z$ direction, at points on the $+y$ side of the wire and into the desk, in the $-z$ direction, on the $-y$ side. The field at every point grows in proportion to the current. The Reaction Rule demands an opposing field at each point. Where the original field points out of the desk, the opposing field points into the desk, and the right-hand thumb into the desk gives a clockwise circulation of induced current as seen from above. The induced current therefore reduces the net field, which is the back-EMF of self-inductance, and its distribution inside a single conductor is the subject of Chapter 5.

**Case 3 (mutual inductance):** Wire B lies on the desk parallel to Wire A on its $-y$ side, so Wire A is above Wire B in the picture, and the return path of Wire B lies farther toward $-y$. Wire B and its return path form a long rectangle, and the flux through that rectangle is the flux of Wire A's field at the rectangle. Wire A's field points into the desk at Wire B and grows with the current. The Reaction Rule demands an opposing field out of the desk, and the right-hand thumb out of the desk gives a counterclockwise circulation around the rectangle. Wire B is the edge of the rectangle nearest to Wire A, so a counterclockwise circulation carries the current in Wire B from right to left, opposite to the current in Wire A. This opposition is the property of inductive crosstalk used above, and the induced voltage is $-M\,dI_A/dt$.

The rectangle formed by Wire B and its return path is the closed loop whose enclosed changing flux sets the EMF, and it is the same loop area that governs loop inductance in [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md). Case 2 occurs inside Case 3 in this example. The total EMF in the rectangle is the sum of the EMF from Wire B's own changing current and the EMF from Wire A's changing current:

$$\mathcal{E}_B = -L_B\,\frac{dI_B}{dt} - M\,\frac{dI_A}{dt}$$

A current that already flows in Wire B contributes only through the first term, and the second term is independent of it.

### Loop Inductance of a 50 Ω Microstrip

Chapter 1 gave a velocity of $1.46\times10^8$ m/s for FR4. The relation $L' = Z_0/v_p$ then gives the loop inductance per unit length of a 50 Ω line:

$$L' = \frac{50}{1.46\times10^8} = 342\ \text{nH/m} \approx 8.7\ \text{nH/in}$$

The capacitance per unit length follows from $C' = 1/(Z_0 v_p) = 137$ pF/m, which is about 3.5 pF/in, and the two values reproduce $Z_0 = \sqrt{L'/C'} = 50\ \Omega$.

The loop inductance of one inch combines the partial inductances according to $L_{loop} = L_1 + L_2 - 2M$. Assume partial inductances $L_1 = 14$ nH for the trace and $L_2 = 2$ nH for the plane (illustrative values chosen to reproduce the 8.7 nH/in loop value). A mutual inductance of $M = 3.65$ nH gives $14 + 2 - 7.3 = 8.7$ nH, matching the figure above. Thinning the dielectric until $M = 4.5$ nH lowers the loop inductance to $16 - 9 = 7.0$ nH. The coupling bound is $M \le \sqrt{14 \cdot 2} = 5.29$ nH, so even perfect coupling leaves a floor of $(\sqrt{14} - \sqrt{2})^2 = 5.4$ nH. The reduction available from thinning the dielectric is therefore limited, and the loop inductance never approaches zero.

### A Narrow Neck as a Series Inductor

Assume a manufacturing defect narrows a 2 mm section of a 50 Ω trace so that its local impedance rises to 65 Ω (a value a field solver would supply), and assume the velocity is unchanged. The excess loop inductance of the neck follows from $L' = Z/v_p$:

$$\Delta L = \frac{65 - 50}{1.46\times10^8}\,(2\times10^{-3}) \approx 0.21\ \text{nH}$$

The reduced capacitance of the narrow neck partly compensates this inductance, as the cancellation condition of Chapter 3 describes, so the net behavior is smaller than that of the inductance alone. Using the inductance alone as an upper estimate and the series-inductor reflection of Chapter 3, $|\Gamma| = \omega \Delta L / |2Z_0 + j\omega \Delta L|$ gives 0.013 at 1 GHz and 0.128 at 10 GHz. The neck is nearly invisible to a slow edge and reflects about 13% of the voltage at the highest frequencies of a fast one, which rounds the edge at the receiver as described above. On a TDR display, which [Chapter 7](07_Time_Domain_Reflectometry.md) treats, the neck appears as a positive impedance bump.

### Crosstalk Numbers: Microstrip versus Stripline

Assume two closely spaced traces with a 1 V aggressor edge of 100 ps rise time, a coupled length of 1 inch (25.4 mm), and a velocity of $1.46\times10^8$ m/s, which gives $T_c = 174$ ps and a round-trip delay of $2T_c = 348$ ps. The round-trip delay exceeds the rise time, so NEXT reaches its full plateau.

For a microstrip, assume $C_m/C = 0.04$ and $L_m/L = 0.08$ (illustrative values for closely spaced traces). The backward coefficient is $K_b = \tfrac{1}{4}(0.04 + 0.08) = 0.03$, so NEXT is a 30 mV pulse lasting about 350 ps. The forward result is $V_{FEXT} = \tfrac{1}{2}(0.04 - 0.08)(174\ \text{ps})(1\ \text{V}/100\ \text{ps}) = -35$ mV, a negative pulse with the duration of the edge.

For a stripline with the same total coupling, assume $C_m/C = L_m/L = 0.06$. The backward coefficient is again $K_b = 0.03$, and NEXT is the same 30 mV. The forward terms cancel, and FEXT is zero.

NEXT depends on the sum of the two couplings and FEXT on their difference, so identical NEXT can accompany very different FEXT. Both quantities fall with greater spacing or with a thinner dielectric, which ties the fields of each trace to its own reference plane.

## Edge Cases

### Two Geometries, One Inductance Increase

Trace width and loop area both raise inductance, through different mechanisms, and confusing the two is a common source of error.

A narrow trace width increases the self-inductance of the trace by concentrating the field into a denser region around the conductor. A wide loop area, meaning a large vertical separation between the trace and the return plane, increases the loop inductance by allowing the field to occupy a larger volume, so more field lines pass through the loop and more flux links it per ampere.

The two mechanisms are geometrically independent of each other. A designer can choose a wide trace, which has a low self-inductance, on a thick dielectric, which has a high loop inductance, or a narrow trace on a thin dielectric. Good design minimizes both contributions: a trace width matched to the target impedance avoids unnecessary field concentration, and a thin dielectric raises the mutual coupling and lowers the loop inductance toward its floor.

### Short Coupled Lengths and Unmatched Victims

The NEXT expression $K_b[V_a(t) - V_a(t - 2T_c)]$ applies for any coupled length. The pulse height is approximately $K_b V_a\,(2T_c/t_r)$ when the round-trip delay is shorter than the rise time, because the bracket no longer reaches the full swing. Assume a coupled length of 5 mm with the 100 ps edge of the previous example. The round-trip delay is 68 ps, and the NEXT amplitude falls to about 21 mV instead of 30 mV.

The derivation assumed that both ends of the victim are terminated in $Z_0$. An unmatched victim end reflects the arriving crosstalk wave with the reflection coefficient $\Gamma$ of [Chapter 3](03_Impedance_Reflections_and_Termination.md), so a high-impedance receiver at the far end of the victim doubles the arriving FEXT, and a low-impedance driver at the near end of the victim reflects part of the backward wave toward the far end. The crosstalk observed at an unmatched victim is therefore the sum of the coupling terms above and their reflections.

The next chapter applies the Reaction Rule inside a single conductor, where the changing field of the current itself drives eddy currents that push the current toward the surface, and it examines the loss in the dielectric. The two mechanisms together set the frequency-dependent attenuation that rounds the edges whose spectrum Chapter 2 quantified.
