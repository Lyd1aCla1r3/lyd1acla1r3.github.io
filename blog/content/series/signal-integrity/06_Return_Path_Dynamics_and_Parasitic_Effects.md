# Return Path Dynamics and Parasitic Effects

<!-- SUMMARY: Every signal requires a closed return current path that governs the loop inductance of the circuit. Electromagnetic field boundary conditions dictate how high-frequency return current concentrates beneath a trace, how vias and split planes introduce reactive discontinuities, and how series AC-coupling capacitors cause baseline wander. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Ebook here.</a></em></p>

[Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) showed that at high frequency the current in the ground plane flows in a layer one skin depth thick on the surface that faces the trace, and left open where along that surface the current flows. [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) defined loop inductance as a property of the whole circuit, which includes the return conductor, and stated that the high-frequency return current gathers beneath the trace. Electromagnetic boundary conditions determine that surface distribution, explain why it depends on frequency, and govern the structures that interrupt the return current or add unintended capacitance and inductance to the signal path.

The trace and its return path are the two halves of one closed current loop. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) established that the loop closes at the wavefront through the displacement current in the dielectric, and that the characteristic impedance and the velocity of the line follow from the inductance and the capacitance per unit length of this loop. Every feature of a board that changes the geometry of the loop, such as a via, a gap in the plane, or a pad, changes the local inductance or capacitance and produces a reflection of the kind analyzed in [Chapter 3](03_Impedance_Reflections_and_Termination.md).

## Core Concepts

### The Current Loop

Current requires a closed loop to flow at all. A transmitter launching a step into a trace sends current forward along the trace and draws an equal current from the ground plane. The loop travels outward with the wavefront: the current flows along the trace to the wavefront, crosses the dielectric as displacement current at the wavefront, and returns along the plane to the source, as the three-zone description of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) explains. Behind the wavefront, a steady current $V/Z_0$ continues to flow in the trace and in the plane.

One physical description of displacement current applies throughout the loop. Displacement current is the term of the Ampere-Maxwell law that lets a changing electric field produce a magnetic field in the same way that a conduction current does. No charge crosses the dielectric, yet the current through the gap obeys Kirchhoff's current law at every node and produces the same magnetic field as an equal conduction current. This field continuity closes the returning current loop at the wavefront and across the dielectric anti-pad gap of a via.

### Where the Return Current Flows at High Frequency

A common explanation holds that the return current follows the trace because the electrons in the plane are attracted to the opposite charge on the trace. The explanation does not predict the observed distribution or its dependence on frequency, and the field description below does. The return current distributes itself to minimize the impedance of the loop, as stated in [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md), and at high frequency the impedance is dominated by the inductive reactance, so the distribution minimizes the loop inductance.

The distribution can be derived from the fields. At high frequency the plane is a good conductor with a skin depth much smaller than its thickness, and [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) showed that the eddy currents inside the metal cancel any penetrating field. The magnetic field is therefore zero inside the plane, and the field just above the surface is tangent to it.

The tangential field at the surface and the surface current density $K$ are related by Ampere's law applied to a thin rectangular path of width $w$ that crosses the surface, with one side in the dielectric and one inside the metal. The field exists only along the dielectric side, so $B_t\,w = \mu_0 K w$, which gives $K = B_t/\mu_0$.

The remaining problem is to find the field of a trace at height $h$ above a plane whose interior is field-free. The method of images supplies the field. Replace the plane by an image of the trace at depth $h$ below the surface, carrying the same current in the opposite direction. The field of the trace and its image has a tangential component at the surface and no normal component, which is the boundary condition of a conducting plane, because the vertical components of the two fields cancel and the horizontal components add. This image-current symmetry matches the cancellation argument that [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) used for the field of a wide sheet.

At a point on the plane a lateral distance $x$ from the point directly beneath the trace, the distance to the trace and to its image is $r = \sqrt{x^2 + h^2}$. Each line current produces a field of magnitude $\mu_0 I/(2\pi r)$ by Ampere's law, and the horizontal component of each is smaller by the factor $h/r$. The two horizontal components add:

$$B_t = 2 \cdot \frac{\mu_0 I}{2\pi r}\cdot\frac{h}{r} = \frac{\mu_0 I\, h}{\pi\,(x^2 + h^2)}$$

Dividing by $\mu_0$ gives the surface current density of the return current:

$$K(x) = \frac{I}{\pi}\,\frac{h}{x^2 + h^2}$$

The integral of $K$ over all $x$ equals $I$, because $\int dx\, h/(x^2+h^2) = \pi$, confirming that the plane carries the full signal current in the opposite direction. The distribution is a bell-shaped curve, centered under the trace, with a width set by the height $h$ of the trace above the plane. The fraction of the current within a lateral distance $a$ of the center is $(2/\pi)\arctan(a/h)$: 50 percent lies within $\pm h$, 80 percent within $\pm 3h$, and 94 percent within $\pm 10h$. Reducing the dielectric thickness narrows the current band in proportion.

Among all surface distributions that carry the same total current $I$, this Cauchy distribution minimizes the stored magnetic field energy $\tfrac{1}{2}LI^2$. The energy stored in the field defines the inductance through $\tfrac{1}{2}LI^2$, so the flux-exclusion property of the plane and the minimum-inductance principle describe the same distribution, and one mechanism accounts for the behavior.

### Frequency-Dependent Return Path Selection

The impedance of a return path is $Z = R + j\omega L$, and the current divides among the available paths in inverse proportion to their impedances. The division of current among the paths changes smoothly with frequency.

At DC and at low frequency the reactive term $\omega L$ is negligible and the resistance $R = \rho_r\,\ell/A$ decides. Spreading across the whole width of the plane enlarges the cross-sectional area $A$, so the current takes the shortest geometric path from source to sink over the full width of the plane and ignores the route of the trace. A DC test current injected into a trace therefore returns by a broad, nearly straight path.

At high frequency the term $\omega L$ dominates the impedance. The current then takes the distribution that minimizes the loop inductance, which is the narrow band derived above, directly beneath the trace and following its routing however long or winding the route is. The narrow band has a higher resistance than the broad path, and the current accepts the higher resistance because the reduction in inductive reactance is larger. The skin effect of [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) confines the band to the surface facing the trace.

The transition between the two regimes occurs between 100 kHz and 1 MHz on typical boards, with the crossover point determined by the path geometry and trace length. Every high-speed digital edge operates far above this transition frequency, so the inductance-minimizing distribution governs all of them. At intermediate frequencies the current is partly concentrated and partly spread, and the distribution reflects the relative size of $R$ and $\omega L$ for each path.

### Loop Area and Loop Ballooning

The inductance of the loop is proportional to the magnetic flux that the loop encloses per unit of current, as [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) defined it ($\Phi = LI$). The cross-section of the loop of a trace and its return path is a long, thin rectangle whose area is the trace length multiplied by the dielectric thickness, the same rectangle that Chapter 4 identified as the closed loop of Wire B. A changing current in this rectangle encloses a changing flux, which sets the back-EMF that defines the inductance, and a smaller area encloses less flux.

The return current cannot cross a slot or a hole in the plane, because there is no copper to carry it. It detours around the obstacle, and the loop changes from a thin rectangle into a wide polygon whose width at the obstacle is the width of the detour instead of the dielectric thickness. The enclosed area grows, the loop inductance grows with it, and the impedance of the affected stretch of line rises. Engineers call this effect **loop ballooning**, and the Worked Examples section estimates its size.

The field geometry explains why the distribution derived above favors proximity. Around the narrow trace the field lines form tight circles, and around the broad plane they form wide, shallow arcs. The current band concentrates beneath the trace because the closer the return current lies to the outbound current, the more completely the two fields cancel outside the narrow gap, and the less flux the loop encloses.

## Architecture

### Parasitic Structures: Geometry That Behaves as a Circuit Element

A parasitic is a local change in the inductance or capacitance per unit length of the line, over a length short enough to behave as a lumped element. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) derived how widening a trace raises the capacitance and lowers the inductance per unit length, and [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) gave the reference values for a 50 Ω line on FR4, $L' = 342$ nH/m and $C' = 137$ pF/m.

Any feature that adds metal facing a plane adds capacitance, and any feature that lengthens or narrows the current path, or enlarges the loop, adds inductance. A parasitic capacitor behaves as a shunt element from the signal to the reference plane, and a parasitic inductor behaves as a series element in the signal path.

Parasitic resistance is usually negligible on a PCB. Assume a via barrel of 0.3 mm diameter and 1.57 mm length (a 62 mil board) with a plated wall 25 µm thick. The DC resistance of the barrel is $\rho_r \ell /(\pi d\, t) = 1.2$ mΩ. At 5 GHz the skin depth of 0.93 µm confines the current to a thinner layer and raises the resistance to about 31 mΩ, which gives a reflection coefficient of about $0.03/100 = 3\times10^{-4}$ in a 50 Ω line. The reactive impedance is the concern, because it scales in proportion to frequency, as [Chapter 3](03_Impedance_Reflections_and_Termination.md) showed for a 0.5 pF capacitance and a 1 nH inductance.

### The Via Anti-Pad as a Capacitor

A via is a plated vertical barrel that connects traces on different layers. The barrel must pass through every plane in the stack without touching it, so the manufacturer drills a clearance hole in each plane, called an **anti-pad**, which is larger than the barrel and filled with laminate. The barrel, the laminate in the annular gap, and the rim of the plane form two conductors separated by a dielectric, which is the definition of a capacitor.

The capacitance of one plane crossing follows from Gauss's law, treating the geometry as a coaxial capacitor of length $t$ (the thickness of the plane), inner radius $a = D_v/2$, and outer radius $b = D_a/2$. A charge per unit length $\lambda$ on the barrel produces a radial field $E(r) = \lambda/(2\pi\varepsilon\, r)$ in the gap, and integrating the field from the barrel to the rim gives the voltage:

$$V = \int_a^b E\, dr = \frac{\lambda}{2\pi\varepsilon}\ln\frac{b}{a}$$

The capacitance is the charge $\lambda t$ divided by the voltage:

$$C = \frac{2\pi\varepsilon\, t}{\ln(D_a/D_v)}$$

Assume a 35 µm plane, a barrel of $D_v = 0.3$ mm, an anti-pad of $D_a = 0.8$ mm, and $\varepsilon_r = 4.2$. The result is 8.3 fF per plane, which shows that the barrel-to-rim capacitance is small and falls as the anti-pad grows, in proportion to $1/\ln(D_a/D_v)$. The pads on each layer, which are wider than the barrel and face the planes above and below, add capacitance of comparable or larger size. A widely used empirical expression for the total capacitance of a via that crosses a ground plane gives:

$$C \approx 1.41\,\varepsilon_r\,\frac{T\,D_1}{D_2 - D_1} \ \text{pF}$$

where $T$ is the thickness of the board, $D_1$ is the diameter of the pad that surrounds the barrel, and $D_2$ is the diameter of the clearance hole in the plane, all in inches. This empirical formula is a curve fit to three-dimensional field-solver results across standard PCB via geometries. For $T = 62$ mil, $D_1 = 20$ mil, $D_2 = 40$ mil, and $\varepsilon_r = 4.2$ it gives 0.37 pF. The value falls as the anti-pad grows and rises as the pad grows, in agreement with the coaxial result.

### Displacement Current through the Anti-Pad

A signal that enters the barrel sees two paths. The first is the copper of the barrel, which carries the signal to the destination layer. The second is the capacitor: the rising voltage of the barrel changes the electric field across the laminate in the gap, and the changing field is a displacement current that leads to the plane. The description of the displacement current in the first section of this chapter applies: no charge crosses the gap, yet the current through the gap obeys Kirchhoff's current law and produces a magnetic field.

The capacitor current obeys $i = C\,dV/dt$, which establishes two governing rules for when via capacitance degrades a signal:

- **Steady-state invisibility:** The displacement current is zero whenever the trace holds a constant DC logic level ($dV/dt = 0$). A fully charged anti-pad gap draws no current and the via is electrically invisible; the capacitance acts as a low-impedance shunt only during voltage transitions.
- **Edge-rate dependence:** The magnitude of the diverted current scales with the voltage slew rate $dV/dt$ rather than the clock repetition rate. A driver that switches in 20 ps generates the same peak displacement current at 1 MHz as at 1 GHz; the repetition rate changes only how often the transition occurs. Via capacitance therefore penalizes links with fast rise times regardless of the underlying data rate.

### How a Shunt Capacitance Divides the Current of an Edge

The division of current at a via follows from a short calculation. Consider a step of amplitude $V_+$ traveling on a line of impedance $Z_0$ that meets a shunt capacitance $C$ and continues on an identical line. The line on the source side is equivalent to a source of $2V_+$ in series with $Z_0$, which is the doubling at an open circuit from Chapter 3, and the line on the far side is a load $Z_0$. The Thevenin equivalent seen by the capacitor has open-circuit voltage $2V_+ Z_0/(Z_0 + Z_0) = V_+$ and resistance $Z_0 \parallel Z_0 = Z_0/2$. The capacitor charges with the time constant:

$$\tau_C = \frac{Z_0\, C}{2}$$

The node voltage is $v_j(t) = V_+\left(1 - e^{-t/\tau_C}\right)$ and the capacitor current is $i_C = C\,dv_j/dt = (2V_+/Z_0)\,e^{-t/\tau_C}$. At $t = 0$ the capacitor is uncharged and acts as a short circuit, so it takes twice the incident current $I_+ = V_+/Z_0$. The current falls to zero as the capacitor charges, and the total charge drawn is $\int i_C\,dt = CV_+$, which is the charge of the fully charged capacitor.

Kirchhoff's current law at the node fixes the split. The reflected wave $v_r$ travels back toward the source, so the net current arriving from the source side is $(V_+ - v_r)/Z_0$. The node voltage is $v_j = V_+ + v_r$, and the current continuing forward is $v_j/Z_0$. The remainder flows into the capacitor:

$$\frac{V_+ - v_r}{Z_0} = \frac{V_+ + v_r}{Z_0} + i_C \quad \Rightarrow \quad i_C = -\frac{2 v_r}{Z_0}$$

The reflection is therefore negative, and the current taken by the capacitor is proportional to its size. The return currents in the plane follow the same accounting: the plane carries, at each instant, a current equal to the sum of the forward trace current and the capacitor current, which equals the incident current minus the reflected current, so the total return current at the source matches the current delivered by the transmitter at every instant.

The result for an edge of finite duration follows from the same equations. Writing $v_j = u + v_r$, where $u(t)$ is the incident edge, the node equation $\tau_C\, \dot v_j + v_j = u$ becomes:

$$\tau_C\,\dot v_r + v_r = -\tau_C\,\dot u$$

For an edge slow compared with $\tau_C$ the first term is negligible and $v_r \approx -\tau_C\,\dot u$: the reflected voltage is proportional to the rate of change of the incident edge. For a linear ramp of duration $t_r$ and amplitude $V_+$, $\dot u = V_+/t_r$ and the solution is:

$$v_r(t) = -\frac{\tau_C V_+}{t_r}\left(1 - e^{-t/\tau_C}\right) \quad (0 \le t \le t_r)$$

The reflection reaches its largest magnitude at the end of the ramp. The Worked Examples section evaluates it for a via.

### The Via Barrel as an Inductance

The current in the barrel flows vertically, and the return current in the planes must close the loop. The loop is larger when the return path is farther from the barrel, and the inductance is proportional to the enclosed flux. An empirical expression, widely used as a first estimate, gives the inductance of a barrel of length $h$ and diameter $d$ in inches:

$$L \approx 5.08\,h\left[\ln\frac{4h}{d} + 1\right] \ \text{nH}$$

This empirical formula comes from circular-loop filament approximations for a vertical cylinder of length $h$ and diameter $d$. For $h = 0.062$ in and $d = 0.010$ in, the expression gives $L = 1.33$ nH. A series inductance reflects an edge in the same way that a shunt capacitance does but with the opposite sign. The two lines on either side of a series inductance $L$ share the current $i$, and the voltage across the inductor is $L\,di/dt$. Writing the node voltages on the two sides in terms of the incident edge $u$ and the reflected wave $v_r$ gives $2v_r = L\,di/dt$ with $i = (u - v_r)/Z_0$, and therefore:

$$\tau_L\,\dot v_r + v_r = +\tau_L\,\dot u, \qquad \tau_L = \frac{L}{2 Z_0}$$

The equation has the same form as the equation of the capacitor with the sign reversed. A shunt capacitance reflects a negative pulse of size $\tau_C\dot u$ and a series inductance reflects a positive pulse of size $\tau_L\dot u$.

### Matching the Via: Capacitance That Cancels Inductance

The opposite signs of the two reflections allow them to cancel, which is the compensation that [Chapter 3](03_Impedance_Reflections_and_Termination.md) derived for a lumped network. The two reflected pulses are equal in size when $\tau_L = \tau_C$:

$$\frac{L}{2Z_0} = \frac{Z_0 C}{2} \quad \Rightarrow \quad L = Z_0^2\, C$$

This equality reproduces the lumped matching condition of [Chapter 3](03_Impedance_Reflections_and_Termination.md) directly in the time domain. A barrel with $L = 1.33$ nH is matched in a 50 Ω line when its capacitance equals $C = L/Z_0^2 = 0.53$ pF, and the empirical capacitance formula yields the required anti-pad clearance diameter: $D_2 = D_1\left(1 + 1.41\,\varepsilon_r T/C\right) = 34$ mil for $D_1 = 20$ mil and $T = 0.062$ in. Enlarging the anti-pad beyond 34 mil lowers the capacitance below the matched target and leaves the via net inductive, whereas shrinking the anti-pad leaves the via net capacitive. Board designers adjust anti-pad diameters during stackup optimization to balance these two reactances.

The cancellation has limits that depend on the size of the structure. The lumped treatment holds only for structures shorter than about one sixth of the spatial length of the edge, which is 0.73 mm for a 30 ps edge on FR4 (the critical length of Chapter 1). A 1.57 mm barrel is longer than this guideline, so the lumped values are a first estimate, and a field solver or a measurement with the techniques of [Chapter 7](07_Time_Domain_Reflectometry.md) and [Chapter 8](08_S_Parameters_and_VNA.md) gives the final answer. A time domain reflectometer displays a capacitive parasitic as a dip in impedance and an inductive parasitic as a bump, and Chapter 7 treats the signatures in detail.

### The Series Capacitor and Baseline Wander

An intentionally placed series capacitor, the AC coupling capacitor of a high-speed serial link, uses the same capacitor physics in a controlled way. It blocks the DC level so that the transmitter and the receiver can use different common-mode voltages. Together with the termination resistance $R$ at the receiver it forms a high-pass filter with the time constant $\tau = RC$.

Let $v_C$ denote the voltage across the capacitor and $v_{in}$ the signal applied to the series combination. The current through the capacitor and the resistor is $i = C\,dv_C/dt$, and the receiver sees $v_{out} = v_{in} - v_C = iR$. Eliminating $i$ gives:

$$\frac{dv_C}{dt} = \frac{v_{in} - v_C}{\tau}$$

For times short compared with $\tau$ the capacitor voltage remains small beside the signal, so $v_C \approx (1/\tau)\int v_{in}\,dt$. Take $v_{in} = \pm A$ for the two logic levels and let $D$ be the excess of ones over zeros accumulated since the capacitor was last at its reference level, counted in bit intervals. The integral gives:

$$v_C \approx \frac{A\, D\, T_{UI}}{\tau}$$

where $T_{UI}$ is the unit interval of the data. This one expression describes both of the problems that follow. A long run of $N$ identical bits has $D = N$ and produces a droop that is proportional to the run length: the receiver level decays toward zero along the exponential $e^{-t/\tau}$ for as long as the run lasts. A sequence with an unequal proportion of ones and zeros has an average level different from zero, and the capacitor voltage follows the average, so the received levels shift by the amount $\langle v_{in}\rangle$ and the decision threshold no longer sits in the middle of the eye. The slow shift of the received baseline is **baseline wander**.

The remedy is a DC-balanced signal, in which the running disparity $D$ stays bounded to a few bits at all times. The line codes of [Chapter 18](18_Line_Coding_FEC_and_Protocol_Framing.md) bound the disparity by construction, as 8b/10b does, or keep it statistically small by scrambling, as 64b/66b does, and the capacitor voltage then stays within $A\,D_{max}\,T_{UI}/\tau$ of its reference level. The capacitor does not reset when the polarity reverses. The balance holds the average input level at the bias point, and the capacitor voltage remains close to it.

## Worked Examples

### Return Current Distribution under a Microstrip

Assume a trace $h = 0.1$ mm above a plane, a typical dielectric thickness for a 50 Ω microstrip. The distribution $K(x) = (I/\pi)\,h/(x^2 + h^2)$ places 50 percent of the return current within $\pm 0.1$ mm of the trace center, 80 percent within $\pm 0.3$ mm, and 94 percent within $\pm 1$ mm.

A DC current in the same board spreads across the width of the plane. Assume that the plane is 50 mm wide and that the current spreads uniformly, so that the share within $\pm 1$ mm is $2/50 = 4$ percent. The band at 10 GHz is therefore more than twenty times more concentrated than the DC distribution inside the same $\pm 1$ mm window, and an intermediate frequency such as 100 kHz has an intermediate distribution that depends on $R$ and $\omega L$ of each path.

### A Via with 0.37 pF and 1.3 nH

Assume a 62 mil via with $C = 0.37$ pF and $L = 1.33$ nH on a 50 Ω line, driven by a 1 V edge that ramps linearly over 30 ps. The incident current is therefore $I_+ = 1/50 = 20$ mA.

The capacitive reflection has the time constant $\tau_C = Z_0 C/2 = 9.25$ ps, and the ramp solution of the previous section gives a peak at $t = t_r$:

$$v_r = -\frac{9.25}{30}\,(1 - e^{-30/9.25})\,\text{V} = -0.296\ \text{V}$$

The reflection is 30 percent of the edge amplitude, and the impedance at the minimum of the dip is $Z_0(1 + \Gamma)/(1 - \Gamma) = 27\ \Omega$, using the inversion of [Chapter 3](03_Impedance_Reflections_and_Termination.md) with $\Gamma = -0.296$. The capacitor current at the peak is $i_C = -2v_r/Z_0 = 11.9$ mA, which is 59 percent of the incident current, and the current that continues forward is 14.1 mA at that instant.

The diversion is large during the edge, because 30 ps is short compared with the 100 ps unit interval of a 10 Gbps signal and the capacitor changes its charge during that time. The capacitor then holds $CV_+ = 0.37$ pC and stops conducting, and the forward current recovers to the steady $V/Z_0$. The 50 percent point of an ideal step emerges delayed by about $0.69\,\tau_C = 6.4$ ps, and its 10 to 90 percent rise time becomes $2.2\,\tau_C = 20$ ps.

The inductive reflection has $\tau_L = L/(2Z_0) = 13.3$ ps and a peak of $+(13.3/30)(1 - e^{-30/13.3}) = +0.40$, which corresponds to an impedance of 116 Ω at the maximum of the bump. The two time constants differ, 13.3 ps against 9.25 ps, so the cancellation is incomplete, and the via shows a bump of +0.40 and a dip of -0.30 that are separated in time by the delay between the two structures. Raising the capacitance to the matched value of 0.53 pF equalizes the two time constants and the two peaks.

### Baseline Wander with a 100 nF Capacitor

Assume a coupling capacitor $C = 100$ nF and a termination resistance $R = 50\ \Omega$, yielding a time constant $\tau = 5\ \mu\text{s}$ and a high-pass corner frequency of $1/(2\pi\tau) = 32$ kHz. At 10 Gbps the unit interval is 100 ps. A run of 66 identical bits, the longest run permitted within a 64b/66b frame and its synchronization header, lasts 6.6 ns and droops by $1 - e^{-6.6\text{ ns}/5\,\mu\text{s}} = 0.13$ percent of the swing. A run of 130 bits droops by 0.26 percent. Single-run droop is therefore negligible with a 100 nF capacitor, and the primary risk comes from cumulative DC imbalance over thousands of unit intervals.

Consider an uncoded data pattern that contains 60 percent ones ($p = 0.6$). The mean input voltage is $(2p - 1)A = 0.2A$, and the coupling capacitor charges to that offset over several time constants. The received levels shift to $+0.8A$ and $-1.2A$ relative to the receiver threshold, closing the upper eye opening by 20 percent. Applying a line code that bounds the running disparity to $D_{max} = 3$ bits restricts the capacitor voltage drift to $A \cdot 3 \cdot 100\ \text{ps}/5\ \mu\text{s} = 6\times10^{-5}\,A$, eliminating baseline wander.

### Return Path Detour at a Slot

Assume a trace crosses a slot in its reference plane that forces the return current to detour over a length of 2 mm, with the return path displaced to a distance $D = 1$ mm from the trace. Modeling a flat strip of width $w = 0.18$ mm as an equivalent cylindrical wire of radius $a = w/4 = 0.045$ mm allows direct comparison between two classical transmission-line geometries: a wire at height $h$ over a solid plane, which has $L' = (\mu_0/2\pi)\ln(2h/a)$ by the method of images, and two parallel wires separated by center-to-center distance $D$, which have $L' = (\mu_0/\pi)\ln(D/a)$.

Over the intact plane ($h = 0.1$ mm), the cylindrical approximation gives $L' = (\mu_0/2\pi)\ln(2h/a) = 298$ nH/m, close to the 342 nH/m full-strip value of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md). Across the slot, where the plane is absent and the return current detours at $D = 1$ mm, the two-wire loop inductance jumps to $L' = (\mu_0/\pi)\ln(D/a) = 1240$ nH/m, roughly four times larger.

Over the 2 mm detour, the slot adds an excess series inductance of $(1240 - 342)\ \text{nH/m} \times 2\ \text{mm} \approx 1.8$ nH. That lumped discontinuity exceeds the barrel inductance of a typical through-hole via, and the series-inductor formula of [Chapter 3](03_Impedance_Reflections_and_Termination.md) quantifies the resulting reflection: $|\Gamma| = \omega L/|2Z_0 + j\omega L|$ reaches 0.11 at 1 GHz, 0.49 at 5 GHz, and 0.75 at 10 GHz. Even a narrow gap in the reference plane reflects a large fraction of a multi-gigahertz edge. The cylindrical model provides a rapid order-of-magnitude estimate, and a three-dimensional field solver computes the full inductance for arbitrary slot geometries.

## Edge Cases

### Reference Plane Discontinuities

The most damaging layout error in a high-speed board is an interruption of the reference plane under a trace. A slot cut for routing, a split between power domains, and a poorly placed mounting hole all leave a region without copper that the high-frequency return current cannot cross. The return current detours around the obstacle, and the loop inflates, as the example above estimates.

Detouring the high-frequency return current around a reference-plane gap degrades the link through three simultaneous mechanisms:

- **Impedance discontinuity:** The enlarged loop raises the local series inductance and produces an inductive impedance bump on a TDR trace.
- **Electromagnetic radiation:** The expanded current loop acts as an efficient magnetic loop antenna, radiating high-frequency energy as electromagnetic interference (EMI).
- **Elevated crosstalk:** The inflated magnetic field spreads laterally into adjacent routing channels and couples strongly into neighboring victim loops ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)).

The severity of all three effects grows with frequency: whereas DC return current spreads smoothly around a slot with negligible penalty, multi-gigahertz return current is locked beneath the trace and suffers a sharp inductive spike across even a narrow split.

### Layer Transitions and Return Vias

A trace that changes layers through a via may change its reference plane (such as transitioning from a top microstrip referenced to Layer 2 to a bottom microstrip referenced to Layer 7). The signal current passes through the barrel, but the return current in the first plane must reach the second plane, and the two planes are connected only through the dielectric between them or through other vias.

The displacement current of the plane pair can carry the return current, because the changing field between the planes is a displacement current that closes the loop, but the capacitance of a plane pair is small at the location of one via and the path has a high impedance at the frequencies of interest.

A ground via placed next to the signal via gives the return current a conductive path from one plane to the other. The spacing $s$ of the return via from the signal via sets the loop area of the barrel pair. The two-wire expression $L' = (\mu_0/\pi)\ln(s/a)$ from the slot example applies to the pair of barrels. With $a = 0.15$ mm and a barrel length of 1.57 mm, a spacing of 1 mm gives a barrel-pair inductance of 1.2 nH, and a spacing of 5 mm gives 2.2 nH, which is an 80 percent increase. The return via should therefore lie as close to the signal via as the manufacturing rules permit.

### When the Lumped Via Model Fails

The lumped treatment of a via in this chapter assumes a barrel shorter than one sixth of the length of the edge. A barrel that is long compared with this guideline, or a stub that extends past the layer where the signal leaves the barrel, behaves as a short transmission line instead of a lumped capacitor and inductor, and its response includes resonances that the lumped values cannot predict. The lumped expressions then give the correct trend for the effect of the anti-pad and the return via spacing, and the actual values come from a three-dimensional field solver or from a measurement.

[Chapter 7](07_Time_Domain_Reflectometry.md) shows how to locate and measure such parasitics in the time domain, using the reflection of a fast edge from each feature of the board.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Ebook here.</a></em></p>
