# Wave Propagation and Transmission Lines

<!-- SUMMARY: Information in high-speed digital systems travels as electromagnetic waves through the PCB dielectric rather than as drifting electrons in copper. Trace geometry and Maxwell's coupled field loops feed the lossless and lossy Telegrapher's Equations to govern characteristic impedance, propagation velocity, and wave attenuation. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>

Every high-speed digital system operates on a single physical principle: information travels as electromagnetic waves through the insulating dielectric, not as individual electrons racing from transmitter to receiver through copper. At the instant a transistor switch connects a trace to a voltage rail, a localized electromagnetic field boundary forms at the driver. That boundary sweeps down the dielectric channel at more than half the speed of light, whereas conduction electrons inside the metal lattice drift at fractions of a millimeter per second. A clear grasp of this distinction provides the physical foundation for characteristic impedance, time-domain reflectometry, return-path design, jitter analysis, and equalization.

Six linked stages govern wave propagation on a printed circuit board (PCB) transmission line. Stages one through three cover the transition from lumped circuits to distributed transmission lines and the coupled three-dimensional loops of a transverse electromagnetic (TEM) wave, followed by first-principles derivations of capacitance, inductance, velocity, and characteristic impedance. Stages four through six develop the lossless Telegrapher's Equations, segment-by-segment charge delivery and return-path closure between driver and receiver, and the lossy frequency-domain Helmholtz wave equation.

## Core Concepts

### Distributed vs. Lumped Elements and Trace Geometry

A discrete resistor, capacitor, or inductor is a *lumped* element: a component localized at a single physical coordinate and small enough that an electromagnetic wave traverses its body in negligible time. Kirchhoff's nodal equations, elementary circuit analysis, and Ohm's law all assume lumped behavior, treating voltage $V$ as uniform across a wire of resistance $R$ carrying current $I$ at any frozen instant of time:

$$V = I R$$

Circuit behavior depends on two distinct dimensions: variation across time ($t$) at a single coordinate, and variation across space ($z$) at a single frozen clock instant. Standard $60\text{ Hz}$ household power cords vary continuously in time, yet their electromagnetic wavelength spans roughly $5{,}000\text{ km}$. A snapshot at any frozen microsecond reveals the same voltage at every point along a two-meter desk lamp cord, so the cord behaves as a single lumped node.

High-speed PCB traces operate in the *distributed* regime because the signal voltage changes faster than the wave can cross the board. At any frozen instant during a transition, the near end of the trace sits at $1.2\text{ V}$ while the far end still sits at $0\text{ V}$. Capacitance and inductance no longer act as isolated components; both properties exist continuously along every microscopic slice of the trace.

#### Distributed Capacitance from Electrostatic Geometry

A bare microstrip trace over a reference plane forms a distributed parallel-plate capacitor without any soldered ceramic component. The copper trace acts as the top plate of width $w$, the solid ground plane acts as the bottom plate at vertical distance $h$, and the FR4 fiberglass epoxy laminate forms the insulating dielectric between them. Two electrostatic mechanisms govern how trace width $w$ and dielectric height $h$ control the distributed capacitance per unit length ($C$):

- **Trace width ($w$) and lateral repulsion:** Like charges on the same metal surface repel one another horizontally. A wider trace provides greater surface area per unit length, allowing charges to spread out laterally with weaker mutual repulsion so the trace stores more charge at the same voltage.
- **Dielectric height ($h$) and vertical attraction:** Opposite charges on the trace ($+Q$) and the ground plane beneath it ($-Q$) attract one another vertically across the dielectric gap. A thinner dielectric brings those opposite charges closer together, strengthening vertical attraction and pulling more charge onto the plates for a given voltage.

Together, wider copper and thinner insulation scale capacitance per unit length in direct proportion to $w$ and inverse proportion to $h$:

$$C \propto w, \qquad C \propto \frac{1}{h}$$

#### Distributed Inductance from the Signal-Return Loop

Distributed series inductance per unit length ($L$, in $\text{H/m}$) emerges from the magnetic field of the signal-and-return current loop. Forward conduction current $I$ flows along the trace in the $+z$ direction while return current flows in the $-z$ direction on the ground plane directly beneath the trace, enclosing a vertical cross-sectional window of height $h$ between the conductors. In a non-magnetic PCB laminate of free-space magnetic permeability $\mu_0$ ($4\pi \times 10^{-7}\text{ H/m}$), spreading current $I$ across a wide sheet of width $w$ sets the horizontal magnetic flux density $B$ (in Teslas, $\text{T}$, or $\text{Wb/m}^2$) between the plates:

$$B = \frac{\mu_0 I}{w}$$

Two magnetostatic mechanisms govern how the same geometric dimensions $w$ and $h$ control the distributed inductance per unit length ($L$):

- **Trace width ($w$) and current-sheet spreading:** A wider trace at fixed dielectric height $h$ spreads the forward current $I$ and its underlying return current across a broader horizontal sheet. Current distributed across that wider sheet lowers the magnetic flux density $B$ between the plates and reduces the stored magnetic flux per amp.
- **Dielectric height ($h$) and magnetic cancellation:** A thinner dielectric shrinks the vertical cross-sectional window height $h$ through which magnetic flux passes. Closer spacing simultaneously brings the opposing forward and return currents into tighter proximity, so their opposite magnetic fields cancel more completely in the surrounding space.

Together, wider copper and thinner insulation scale inductance per unit length in inverse proportion to $w$ and direct proportion to $h$:

$$L \propto \frac{1}{w}, \qquad L \propto h$$

Capacitance and inductance move in opposite directions whenever trace geometry changes. A wider trace or a thinner dielectric raises $C$ and lowers $L$, reducing the characteristic impedance $Z_0$ of the transmission line, which the Telegrapher's Equations derive later in this chapter:

$$Z_0 = \sqrt{\frac{L}{C}}$$

### Rise Time, Rising-Edge Length, and the Critical Length Threshold

The boundary between lumped and distributed behavior depends on the ratio between the one-way propagation delay of the trace ($t_{pd}$) and the signal rise time ($t_r$, typically measured from $10\%$ to $90\%$ of the voltage step). A trace of physical length $\ell$ carrying a wave at propagation velocity $v_p$ has a one-way transit delay:

$$t_{pd} = \frac{\ell}{v_p}$$

Over the rise time $t_r$ required for the transmitter output to slew from $0\text{ V}$ to $1.2\text{ V}$, the leading toe of the wavefront advances into the dielectric at speed $v_p$. At the instant the transmitter reaches the top of its $1.2\text{ V}$ ramp, the physical span of trace occupied by the sloped transition is the spatial length of the rising edge:

$$\ell_{\text{edge}} = v_p\, t_r$$

A widely used engineering rule treats an interconnect as a lumped element only when its physical length $\ell$ is shorter than one-sixth of the spatial length of the rising edge:

$$\ell_{\text{critical}} = \frac{\ell_{\text{edge}}}{6} = \frac{v_p\, t_r}{6} \qquad \Longleftrightarrow \qquad t_{pd} < \frac{t_r}{6}$$

The factor of one-sixth comes from round-trip reflection timing. Any reflection generated at the far end of the trace must travel from the driver to the load and back again, requiring a round-trip time of $2 t_{pd}$. Keeping one-way transit delay $t_{pd}$ below one-sixth of $t_r$ confines the round-trip echo $2 t_{pd}$ to less than one-third of $t_r$. Returning within that window brings the echo back while the driver is still slewing, blending the reflection smoothly into the transition instead of ringing.

Consider a CMOS driver with rise time $t_r$ of $30\text{ ps}$ launching onto an FR4 stripline with propagation velocity $v_p$ of approximately $0.146\text{ mm/ps}$. Those parameters determine the spatial rising-edge length and the lumped critical length on the board:

$$\ell_{\text{edge}} = (0.146\text{ mm/ps})(30\text{ ps}) \approx 4.4\text{ mm}, \qquad \ell_{\text{critical}} = \frac{\ell_{\text{edge}}}{6} \approx \frac{4.4\text{ mm}}{6} \approx 0.73\text{ mm}$$

Every PCB trace in a multi-gigabit link exceeds a millimeter and must be designed as a distributed transmission line.

### Why Ohm's Law Fails During Wave Propagation

Steady-state Ohm's law describes a circuit in which charge carriers drift uniformly throughout the entire conductor loop and the potential gradient is established end to end. That steady-state condition exists only after all wavefront reflections have settled.

In a picosecond logic transition, the transmitter switches states long before the electromagnetic wave reaches the far-end receiver. At the launch instant, the wavefront cannot observe what load impedance sits centimeters away at the end of the trace; the wave interacts solely with the local distributed capacitance $C$ and inductance $L$ of the copper slice immediately ahead.

Source energy during the transition goes into building electric and magnetic fields inside each newly reached slice of dielectric rather than merely overcoming the DC resistance of the copper. Even though a multimeter measures less than $0.1\ \Omega$ of end-to-end DC resistance along the copper trace, the ratio of voltage to current in the forward-traveling wave is governed by the local geometric characteristic impedance $Z_0$ (typically $50\ \Omega$):

$$Z_0 = \sqrt{\frac{L}{C}}$$

### Transverse Electromagnetic (TEM) Propagation and the 3D Field Loops

Electromagnetic wave propagation down a PCB trace depends on dynamic coupling between electric and magnetic fields inside the insulating laminate. Distinguishing static charge, steady direct current, and a moving transition clarifies how a wave propels itself and how its three-dimensional field loops fit together.

#### Static, Steady-State, and Coupled Dynamic Field Regimes

On a disconnected battery or charged open trace, surface charges hold a constant voltage difference between the conductors and produce a static vertical electric field (nonzero $\vec{E}$). Zero current $I$ flows through the open conductor, so the magnetic field $\vec{B}$ vanishes everywhere:

$$I = 0, \qquad \vec{B} = 0$$

In a closed loop carrying steady direct current $I$ forward through the trace and back through the ground plane, a static magnetic field (nonzero $\vec{B}$) surrounds the conductors while the constant trace-to-ground voltage maintains a static vertical electric field (nonzero $\vec{E}$). Both time derivatives vanish in steady state, so the two static fields coexist independently without regenerating each other:

$$\frac{\partial \vec{E}}{\partial t} = 0, \qquad \frac{\partial \vec{B}}{\partial t} = 0$$

At a propagating wavefront between the charged and uncharged regions of a trace, both fields change rapidly in time:

$$\frac{\partial \vec{E}}{\partial t} \neq 0, \qquad \frac{\partial \vec{B}}{\partial t} \neq 0$$

Each changing field continuously generates the other slightly further down the line. The Ampère-Maxwell law states that a time-varying electric field ($\partial \vec{E} / \partial t$) across the dielectric generates a circulating magnetic field as Maxwell's displacement current. Faraday's law of induction ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)) states that a time-varying magnetic field ($\partial \vec{B} / \partial t$) generates a circulating electric field loop.

#### Unified Dielectric Wavefront and Clockwise Current Loop

A side view of the board places the transmitter on the left (at spatial origin $z$ equal to $0$) and the receiver on the right, with the signal trace on top and the ground plane on the bottom. During a positive $+1.2\text{ V}$ transition, one unified electromagnetic wavefront sweeps from left to right ($+z$) through the insulating dielectric corridor between the trace and the ground plane, where $80\%$ to $95\%$ of the field energy is concentrated. The top of that dielectric wavefront strips electrons from the bottom surface of the trace while the bottom of the same wavefront pushes electrons along the top surface of the ground plane directly below.

Rightward conduction current ($\rightarrow$) flows along the trace from the driver to the wavefront, while downward displacement current ($\downarrow$, driven by $\partial \vec{E} / \partial t$ as the vertical electric field builds) crosses the dielectric exclusively within the moving wavefront zone. Leftward return conduction current ($\leftarrow$) flows along the ground plane beneath the trace back to the source. All three legs form a single clockwise current loop, and by the right-hand rule all three legs reinforce one magnetic field ($\vec{B} \otimes$) pointing into the page between the trace and the ground plane.

#### Counter-Clockwise Faraday Loop and TEM Wave Geometry

At the leading edge of the wavefront, the into-the-page magnetic flux increases rapidly ($\partial \vec{B} / \partial t \otimes$). Faraday's law relates the curl of the induced electric field to that growing magnetic flux density:

$$\nabla \times \vec{E}_{\text{induced}} = -\frac{\partial \vec{B}}{\partial t}$$

Growing into-the-page magnetic flux induces a counter-clockwise electric field loop around the wavefront boundary. Its left vertical leg points downward ($\downarrow$) from trace to ground behind the wavefront to sustain the vertical TEM electric field. Its top horizontal leg points leftward ($\leftarrow$) inside the trace copper, producing the inductive back-EMF that momentarily opposes the forward current surge into the next segment.

Both the vertical electric field ($\vec{E} \downarrow$) and the horizontal into-the-page magnetic field ($\vec{B} \otimes$) lie entirely in the cross-sectional plane perpendicular to the $+z$ direction of travel. Perpendicular electric and magnetic field geometry defines a **Transverse Electromagnetic (TEM)** wave. Wave energy travels inside the dielectric space between the conductors while the copper surfaces serve as guide rails, so the permittivity and loss tangent of the PCB laminate govern signal speed and high-frequency attenuation.

### Propagation Velocity, Material Constants, and Parallel-Plate Derivations

The propagation velocity $v_p$ of a TEM wave in a uniform dielectric is set by the relative permittivity ($\varepsilon_r$, also called the dielectric constant or $D_k$) of the insulator:

$$v_p = \frac{c}{\sqrt{\varepsilon_r}}$$

Constant $c$ (approximately $3.00 \times 10^8\text{ m/s}$) is the speed of light in a vacuum. From the circuit perspective, the same propagation velocity is set by the distributed inductance $L$ and distributed capacitance $C$ per unit length:

$$v_p = \frac{1}{\sqrt{LC}}$$

Signal voltage amplitude appears in neither formula; doubling the launch swing from $1\text{ V}$ to $2\text{ V}$ doubles the electric field strength and doubles the charging current, leaving $L$, $C$, and $v_p$ unchanged.

The physical bridge between the material velocity expression $c / \sqrt{\varepsilon_r}$ and the circuit velocity expression $1 / \sqrt{LC}$ comes from Maxwell's vacuum relation for the speed of light:

$$c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} \qquad \Longleftrightarrow \qquad \frac{1}{c^2} = \mu_0 \varepsilon_0$$

Taking the reciprocal of the squared velocity links $LC$ directly to the fundamental electromagnetic constants of the medium:

$$\frac{1}{v_p^2} = LC = \frac{\varepsilon_r}{c^2} = \mu_0 \varepsilon_0 \varepsilon_r$$

#### Permittivity and Permeability of PCB Materials

Total electric permittivity $\varepsilon$ and total magnetic permeability $\mu$ scale their free-space baselines by dimensionless material constants:

$$\varepsilon = \varepsilon_0 \varepsilon_r, \qquad \mu = \mu_0 \mu_r$$

Free space has a baseline electric permittivity $\varepsilon_0$ of approximately $8.854 \times 10^{-12}\text{ F/m}$, while relative permittivity $\varepsilon_r$ measures how strongly an insulator polarizes under an applied electric field relative to vacuum (where $\varepsilon_r$ equals $1$). In standard FR4 epoxy-glass ($\varepsilon_r$ of approximately $4.2$), molecular dipoles stretch and rotate against the applied vertical electric field, partially counteracting the internal electric field so the copper plates store $4.2$ times more charge at the same voltage.

Free space has a baseline magnetic permeability $\mu_0$ of $4\pi \times 10^{-7}\text{ H/m}$, while relative permeability $\mu_r$ measures how strongly a material amplifies magnetic flux relative to vacuum. Ferromagnetic materials such as iron or ferrite contain magnetic domains that align with a magnetic field ($\mu_r$ from $10^2$ to $10^4$), whereas copper and PCB dielectrics are non-magnetic ($\mu_r$ equal to $1$), fixing the total permeability of every PCB transmission line at vacuum permeability:

$$\mu = \mu_0(1) = \mu_0$$

#### First-Principles Parallel-Plate Capacitance per Unit Length

First-principles derivations of $C$ and $L$ for a wide parallel-plate transmission line of trace width $w$, dielectric thickness $h$, and section length $\ell$ (neglecting edge fringing) prove why trace geometry cancels out of $LC$ while directly controlling $Z_0$. Total capacitance $C_{\text{total}}$ equals stored charge $Q$ divided by voltage $V$, and Gauss's law gives the uniform vertical electric field $E$ produced by charge $Q$ spread across rectangular plate area $A$ (equal to $w\ell$) in permittivity $\varepsilon_0 \varepsilon_r$:

$$C_{\text{total}} = \frac{Q}{V}, \qquad A = w\ell, \qquad E = \frac{Q}{\varepsilon_0 \varepsilon_r w \ell}$$

Multiplying that uniform vertical electric field by the plate separation $h$ gives the potential difference between the trace and ground plane:

$$V = E\, h = \frac{Q\, h}{\varepsilon_0 \varepsilon_r w \ell}$$

Substitution of $V$ into the total capacitance ratio and division by the section length $\ell$ yield the capacitance per unit length $C$ (in $\text{F/m}$):

$$C_{\text{total}} = \frac{Q}{\dfrac{Q\, h}{\varepsilon_0 \varepsilon_r w \ell}} = \frac{\varepsilon_0 \varepsilon_r w \ell}{h}$$

$$C = \frac{C_{\text{total}}}{\ell} = \frac{\varepsilon_0 \varepsilon_r w}{h}$$

#### First-Principles Parallel-Plate Inductance per Unit Length

Total inductance $L_{\text{total}}$ equals enclosed magnetic flux $\Phi_B$ divided by current $I$. Applying Ampère's circuital law around a forward current $I$ distributed across a sheet of width $w$ above an opposing return-current sheet produces a uniform horizontal magnetic flux density $B$ confined between the sheets and zero field outside:

$$L_{\text{total}} = \frac{\Phi_B}{I}, \qquad \oint \vec{B} \cdot d\vec{\ell} = \mu_0 I \qquad \Longrightarrow \qquad B = \frac{\mu_0 I}{w}$$

That magnetic field passes perpendicularly through the side cross-sectional window of height $h$, length $\ell$, and area $A_{\text{window}}$ (equal to $h\ell$), producing total magnetic flux $\Phi_B$:

$$A_{\text{window}} = h\ell, \qquad \Phi_B = B\, A_{\text{window}} = \left(\frac{\mu_0 I}{w}\right)(h\ell)$$

Substitution of $\Phi_B$ into the total inductance ratio and division by the section length $\ell$ yield the inductance per unit length $L$ (in $\text{H/m}$):

$$L_{\text{total}} = \frac{\Phi_B}{I} = \frac{\mu_0 h \ell}{w} \qquad \Longrightarrow \qquad L = \frac{L_{\text{total}}}{\ell} = \frac{\mu_0 h}{w}$$

#### Cancellation of Geometry in Velocity and Aspect-Ratio Control of Impedance

Multiplying $L$ and $C$ cancels both geometric dimensions $w$ and $h$ identically:

$$LC = \left(\frac{\mu_0 h}{w}\right) \left(\frac{\varepsilon_0 \varepsilon_r w}{h}\right) = \mu_0 \varepsilon_0 \varepsilon_r$$

$$v_p = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{\mu_0 \varepsilon_0}} \frac{1}{\sqrt{\varepsilon_r}} = \frac{c}{\sqrt{\varepsilon_r}}$$

Division of $L$ by $C$ inside the characteristic impedance square root inverts the denominator fraction and reinforces the geometric aspect ratio $h/w$:

$$Z_0 = \sqrt{\frac{L}{C}} = \sqrt{\frac{\dfrac{\mu_0 h}{w}}{\dfrac{\varepsilon_0 \varepsilon_r w}{h}}} = \sqrt{\frac{\mu_0 h}{w} \cdot \frac{h}{\varepsilon_0 \varepsilon_r w}}$$

$$Z_0 = \sqrt{\frac{h^2}{w^2} \frac{\mu_0}{\varepsilon_0 \varepsilon_r}} = \frac{h}{w} \sqrt{\frac{\mu_0}{\varepsilon_0 \varepsilon_r}}$$

A wider trace ($w \uparrow$) or a thinner dielectric ($h \downarrow$) lowers $L$ and raises $C$ by the same geometric factor $h/w$, reducing $Z_0$ while leaving $v_p$ unchanged.

### Buried Stripline vs. Surface Microstrip Propagation Speeds

Trace layer placement in the PCB stackup determines how much of the electric field resides inside the FR4 substrate versus the surrounding air, directly setting wave propagation speed.

#### Buried Stripline in a Homogeneous Dielectric

A stripline trace is routed on an internal PCB layer sandwiched symmetrically between an upper reference plane and a lower reference plane, completely encased in FR4 ($\varepsilon_r$ of approximately $4.2$). All electric field lines remain inside the FR4 dielectric, so every stripline trace experiences the full relative permittivity of $4.2$ and propagates at a uniform speed (equivalent to $14.6\text{ cm/ns}$, or a delay of $6.8\text{ ps/mm}$):

$$v_p = \frac{c}{\sqrt{4.2}} \approx 1.46 \times 10^8\text{ m/s}$$

#### Surface Microstrip in an Inhomogeneous Air-Plus-FR4 Dielectric

A microstrip trace sits on the top or bottom outer surface of the PCB, with FR4 ($\varepsilon_r$ of approximately $4.2$) beneath the copper and air ($\varepsilon_r$ of approximately $1.0$) above the copper. Most electric field lines pass directly downward through the FR4 to the ground plane, while the remaining lines fringe upward through the air before curving back down to the reference plane.

Field sharing across air and laminate exposes the wave to a weighted-average **effective dielectric constant** $\varepsilon_{\text{eff}}$ between $1.0$ and $\varepsilon_r$ (typically $3.0$ to $3.3$ on FR4). Reduced effective permittivity allows a surface microstrip signal to travel $15\%$ to $20\%$ faster (or a delay of $5.9\text{ ps/mm}$) than an inner-layer stripline on the same PCB:

$$v_p = \frac{c}{\sqrt{\varepsilon_{\text{eff}}}} \approx 1.70 \times 10^8\text{ m/s}$$

### The Lossless Telegrapher's Equations and Traveling-Wave Solution

Characteristic impedance $Z_0$ and propagation velocity $v_p$ emerge rigorously from Kirchhoff's voltage and current laws applied to an infinitesimal slice of lossless transmission line of length $\Delta z$ containing series inductance $L\,\Delta z$ and shunt capacitance $C\,\Delta z$. Let $v(z, t)$ and $i(z, t)$ denote the instantaneous voltage and current at spatial coordinate $z$ and time $t$; many textbooks omit $(z, t)$ as shorthand, but explicit arguments keep every spatial and temporal derivative unambiguous.

#### Differential Slice Balance and Coupled Partial Derivatives

Voltage $v(z, t)$ and current $i(z, t)$ depend on two independent variables ($z$ and $t$), so calculus uses the partial derivative symbol $\partial$:

- **Spatial partial derivative ($\partial / \partial z$):** Holds time $t$ frozen like a photograph and measures how rapidly voltage or current changes per meter along the copper trace at that single instant.
- **Temporal partial derivative ($\partial / \partial t$):** Holds position $z$ fixed at a single probe point and measures how rapidly voltage or current changes per second as the wave sweeps past that coordinate.

Kirchhoff's voltage law across the slice from $z$ to $z + \Delta z$ at frozen instant $t$ equates the spatial voltage drop to the inductive voltage across $L\,\Delta z$:

$$v(z, t) - v(z + \Delta z, t) = L\,\Delta z\,\frac{\partial i(z, t)}{\partial t}$$

Kirchhoff's current law at the slice node equates the spatial current lost along the trace to the displacement current diverted into the shunt capacitance $C\,\Delta z$:

$$i(z, t) - i(z + \Delta z, t) = C\,\Delta z\,\frac{\partial v(z, t)}{\partial t}$$

Taking the forward-difference limit as slice length $\Delta z$ shrinks to zero converts each difference quotient into a spatial partial derivative:

$$-\lim_{\Delta z \to 0} \frac{v(z + \Delta z, t) - v(z, t)}{\Delta z} = L\,\frac{\partial i(z, t)}{\partial t} \qquad \Longrightarrow \qquad -\frac{\partial v(z, t)}{\partial z} = L\,\frac{\partial i(z, t)}{\partial t}$$

$$-\lim_{\Delta z \to 0} \frac{i(z + \Delta z, t) - i(z, t)}{\Delta z} = C\,\frac{\partial v(z, t)}{\partial t} \qquad \Longrightarrow \qquad -\frac{\partial i(z, t)}{\partial z} = C\,\frac{\partial v(z, t)}{\partial t}$$

These two coupled partial differential equations are the **lossless Telegrapher's Equations**. The first states that a spatial voltage gradient along the trace requires a time-varying current through the distributed inductance $L$; the second states that a spatial decrease in trace current along the line feeds a time-varying voltage across the distributed capacitance $C$.

#### Traveling-Wave Substitution and Impedance Proof

On a lossless line (zero series resistance $R$ and zero shunt conductance $G$, so zero energy dissipates as heat) with frequency-independent $L$ and $C$ (zero dispersion, so all frequency components travel at speed $v_p$), a forward-traveling wave preserves its shape in $+z$. Reserving symbol $f$ for frequency in Hertz ($\text{Hz}$), let $v_w(\tau)$ and $i_w(\tau)$ denote the arbitrary forward-traveling voltage and current waveform shapes as functions of a single combined variable $\tau$, the **launch time**:

$$\tau = t - \frac{z}{v_p}$$

$$v(z, t) = v_w\!\left(t - \frac{z}{v_p}\right) = v_w(\tau), \qquad i(z, t) = i_w\!\left(t - \frac{z}{v_p}\right) = i_w(\tau)$$

Ratio $z / v_p$ is the transit time required for a feature on the wave to travel from the transmitter at coordinate $0$ to position $z$, so launch time $\tau$ is the clock time when the piece of the wave observed at $(z, t)$ originally left the driver. Functions $v_w(\tau)$ and $i_w(\tau)$ are not restricted to sine or cosine waves; they represent any pulse, step, or ramp profile launched onto the trace.

Consider a concrete numerical voltage ramp of slew rate $0.1\text{ V/ns}$ launched onto a trace with propagation velocity $v_p$ of $15\text{ cm/ns}$:

$$v_w(\tau) = (0.1\text{ V/ns})\,\tau$$

At the transmitter ($z$ of $0\text{ cm}$) at clock instant $t$ of $2\text{ ns}$, zero transit delay sets the launch time and driver voltage:

$$\tau = 2\text{ ns} - 0\text{ ns} = 2\text{ ns}, \qquad v(0, 2\text{ ns}) = (0.1\text{ V/ns})(2\text{ ns}) = 0.2\text{ V}$$

One nanosecond later ($t$ of $3\text{ ns}$) at a probe point $15\text{ cm}$ down the trace, the transit delay $z / v_p$ of $(15\text{ cm}) / (15\text{ cm/ns})$ equals $1\text{ ns}$, yielding the identical launch time and identical voltage:

$$\tau = 3\text{ ns} - 1\text{ ns} = 2\text{ ns}, \qquad v(15\text{ cm}, 3\text{ ns}) = (0.1\text{ V/ns})(2\text{ ns}) = 0.2\text{ V}$$

Differentiating the scalar launch-time argument $\tau$ partially with respect to $z$ and $t$ produces two constant factors:

$$\frac{\partial \tau}{\partial z} = -\frac{1}{v_p}, \qquad \frac{\partial \tau}{\partial t} = 1$$

Applying the chain rule relates the spatial and temporal partial derivatives directly to the ordinary waveform derivatives $dv_w(\tau)/d\tau$ and $di_w(\tau)/d\tau$:

$$\frac{\partial v(z, t)}{\partial z} = \frac{dv_w(\tau)}{d\tau} \frac{\partial \tau}{\partial z} = -\frac{1}{v_p} \frac{dv_w(\tau)}{d\tau}, \qquad \frac{\partial i(z, t)}{\partial t} = \frac{di_w(\tau)}{d\tau} \frac{\partial \tau}{\partial t} = \frac{di_w(\tau)}{d\tau}$$

$$\frac{\partial i(z, t)}{\partial z} = \frac{di_w(\tau)}{d\tau} \frac{\partial \tau}{\partial z} = -\frac{1}{v_p} \frac{di_w(\tau)}{d\tau}, \qquad \frac{\partial v(z, t)}{\partial t} = \frac{dv_w(\tau)}{d\tau} \frac{\partial \tau}{\partial t} = \frac{dv_w(\tau)}{d\tau}$$

Recalling the first lossless Telegrapher's Equation and substituting the first pair of chain-rule derivatives cancel the minus signs:

$$-\frac{\partial v(z, t)}{\partial z} = L\,\frac{\partial i(z, t)}{\partial t} \qquad \Longrightarrow \qquad \frac{1}{v_p} \frac{dv_w(\tau)}{d\tau} = L\,\frac{di_w(\tau)}{d\tau}$$

Integration of both sides with respect to $\tau$ from the uncharged baseline ahead of the wave (where both $v_w(\tau)$ and $i_w(\tau)$ vanish, fixing the integration constant at zero) gives the first algebraic relation between voltage and current:

$$v_w(\tau) = v_p\, L\, i_w(\tau)$$

Recalling the second lossless Telegrapher's Equation, substituting the second pair of chain-rule derivatives, and integrating with respect to $\tau$ give the companion relation:

$$-\frac{\partial i(z, t)}{\partial z} = C\,\frac{\partial v(z, t)}{\partial t} \qquad \Longrightarrow \qquad \frac{1}{v_p} \frac{di_w(\tau)}{d\tau} = C\,\frac{dv_w(\tau)}{d\tau}$$

$$i_w(\tau) = v_p\, C\, v_w(\tau)$$

Substituting that current expression $i_w(\tau)$ into the voltage relation eliminates the current waveform:

$$v_w(\tau) = v_p L \left(v_p C\, v_w(\tau)\right) = v_p^2 LC\, v_w(\tau)$$

Cancellation of the arbitrary nonzero waveform $v_w(\tau)$ from both sides proves the geometric propagation velocity formula:

$$v_p^2 LC = 1 \qquad \Longrightarrow \qquad v_p = \frac{1}{\sqrt{LC}}$$

Dividing the forward voltage waveform $v_w(\tau)$ by the forward current waveform $i_w(\tau)$ and substituting $1 / \sqrt{LC}$ for $v_p$ prove the characteristic impedance formula:

$$Z_0 = \frac{v_w(\tau)}{i_w(\tau)} = v_p\, L = \frac{L}{\sqrt{LC}} = \sqrt{\frac{L}{C}}$$

Neither $v_p$ nor $Z_0$ contains the waveform shape $v_w(\tau)$. Every edge, regardless of rise time or voltage swing, travels at the same speed $1 / \sqrt{LC}$ and maintains the voltage-to-current ratio $\sqrt{L/C}$ at every point along a lossless uniform line.

## Architecture

### The CMOS Driver as a High-Speed Valve

The positive power rail (such as $+1.2\text{ V}$) and the ground plane ($0\text{ V}$) act as two reservoirs of constant electrical potential maintained by the power distribution network (PDN). At the near end of the trace (spatial origin $z$ equal to $0$) sits a CMOS output driver composed of two complementary transistor switches. A pull-up PMOS switch connects the trace to the $+1.2\text{ V}$ rail, while a pull-down NMOS switch connects the trace to the $0\text{ V}$ ground plane.

The power supply never generates time-varying analog waveforms to encode bits; information is encoded in the instants at which the switches change state. A logic `1` transition closes the pull-up switch and opens the pull-down switch, exposing the near end of the trace to $+1.2\text{ V}$. A logic `0` transition opens the pull-up switch and closes the pull-down switch, shorting the near end of the trace to the $0\text{ V}$ ground plane. Abrupt time-domain transitions generate broad frequency spectra, which [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) derives from Fourier analysis.

### The Wavefront Launch Event

Consider an uncharged trace of total length $\ell$ sitting at $0\text{ V}$ from its near end to its far end. At initial instant $t$ equal to $0$, the pull-up transistor switches on and exposes the near-end copper at the driver to the $+1.2\text{ V}$ supply rail.

The entire length of the trace cannot jump to $1.2\text{ V}$ instantaneously because each downstream slice of distributed capacitance $C\,\Delta z$ requires charge and each slice of series inductance $L\,\Delta z$ opposes an instantaneous current jump. A steep spatial boundary of rising-edge width $\ell_{\text{edge}}$ (equal to $v_p t_r$, or roughly $4.4\text{ mm}$ for a $30\text{ ps}$ edge on FR4) forms at the transmitter between the newly charged $1.2\text{ V}$ region and the uncharged $0\text{ V}$ copper ahead.

### Segment-by-Segment Propagation and Local Inductive Back-EMF

A chain of contiguous microscopic segments of length $\Delta z$, each containing series inductance $L\,\Delta z$ and shunt capacitance $C\,\Delta z$, reveals the chronological chain reaction of wave propagation.

#### Stage 1: Initial Launch and Displacement Current in Segment 1

Activation of the pull-up switch at time $0$ exposes Segment 1 at the driver to the $+1.2\text{ V}$ rail. Conduction current flows from the supply into Segment 1, stripping electrons from the copper to deposit positive charge and building a downward vertical electric field $\vec{E} \downarrow$ across the dielectric to the ground plane. That rapidly growing vertical electric field ($\partial \vec{E} / \partial t$) creates downward displacement current $I_D$ across the insulator, closing the initial current loop while Segments 2, 3, and beyond remain at $0\text{ V}$:

$$I_D = C\,\Delta z\,\frac{\partial v(z, t)}{\partial t}$$

#### Stage 2: Current Surge and Direct Faraday Induction into Segment 2

Segment 1 rises toward $1.2\text{ V}$ while Segment 2 sits at $0\text{ V}$, and the horizontal voltage drop pushes conduction current rightward into Segment 2. Rising forward current generates a growing into-the-page magnetic field ($\partial \vec{B} / \partial t \otimes$) in the dielectric window beneath the junction, governed by Faraday's law:

$$\nabla \times \vec{E}_{\text{induced}} = -\frac{\partial \vec{B}}{\partial t}$$

Growing into-the-page magnetic flux directly induces a leftward horizontal electric field ($\vec{E}_{\text{induced}} \leftarrow$) inside the trace copper. An out-of-the-page right-hand thumb ($\odot$) serves solely as the right-hand-rule mnemonic for the minus sign in Faraday's law, not as a second opposing magnetic field.

#### Stage 3: Inductive Pacing and Downstream Cascade

The leftward induced electric field ($\vec{E}_{\text{induced}} \leftarrow$) opposes the incoming charge and produces the series inductance voltage drop $v_L(z, t)$ across the slice:

$$v_L(z, t) = L\,\Delta z\,\frac{\partial i(z, t)}{\partial t}$$

Inductive back-EMF paces the current ramp so charge transfers into Segment 2 at the finite velocity $v_p$ of $1 / \sqrt{LC}$. Segment 2 then charges its own capacitance $C\,\Delta z$ through vertical displacement current and feeds Segment 3 in a continuous cascade down the line.

### The Three Zones of a Propagating Wavefront and Return Current in a 0V Plane

A snapshot in time halfway through a transition along a trace of length $\ell$ divides the interconnect into three distinct spatial zones relative to the wavefront coordinate $z_{\text{front}}$.

#### Charged Region Behind the Wavefront

Across the energized span from $0$ to $z_{\text{front}}$ behind the transition, every segment sits at a constant $+1.2\text{ V}$ with a static vertical electric field $E$ of $V / h$ between the $+Q$ trace charge and $-Q$ ground-plane charge. Unchanging local voltage sets the temporal voltage derivative and dielectric displacement current $I_D$ to zero:

$$\frac{\partial v(z, t)}{\partial t} = 0, \qquad I_D = 0$$

Inside the copper, the horizontal electric field drives a steady conduction current $I$ rightward from the driver to deliver charge to the wavefront while an equal return current flows leftward in the ground plane:

$$I = \frac{V}{Z_0}$$

That steady current loop surrounds the trace behind the wavefront with a static into-the-page magnetic field ($\vec{B} \otimes$) storing magnetic energy $\frac{1}{2}L I^2$ per meter.

#### Active Transition Zone at the Wavefront

Within the moving transition zone around $z_{\text{front}}$ (of spatial width $\ell_{\text{edge}}$ equal to $v_p t_r$), both local trace voltage $v(z, t)$ and current $i(z, t)$ actively slew upward with positive time derivatives. Forward conduction current arrives from the trace behind the wavefront, turns downward across the dielectric as displacement current $I_D$ while the vertical electric field builds, and turns leftward onto the ground plane as return conduction current:

$$I_D = C\,\Delta z\,\frac{\partial v(z, t)}{\partial t}$$

That vertical displacement-current bridge slides rightward at speed $v_p$, continuously elongating the energized current loop behind it.

#### Uncharged Region Ahead of the Wavefront

Ahead of the advancing boundary between $z_{\text{front}}$ and far end $\ell$, the electromagnetic wave has not yet arrived. Both the trace and the ground plane remain at $0\text{ V}$ with zero electric field, zero magnetic field, zero conduction current, and zero displacement current.

#### Return Current Flow Through a 0 V Reference Plane

A natural question arises in the behind-the-wavefront zone: how can return conduction current flow leftward through a ground plane labeled "$0\text{ V}$" everywhere? The label "$0\text{ V}$" does not indicate zero charge or an inability to conduct current; it denotes the arbitrary reference potential assigned to the negative terminal of the power supply.

In an ideal lossless copper ground plane (zero sheet resistance $R_{\text{plane}}$), mobile electrons experience zero lattice friction and coast from the wavefront footprint back to the source terminal with zero voltage drop:

$$\Delta V = I\, R_{\text{plane}} = 0\text{ V}$$

In a real copper ground plane with a small sheet resistance $R_{\text{plane}}$ of $1\text{ m}\Omega$, a $24\text{ mA}$ return current produces a microvolt-scale longitudinal potential gradient:

$$\Delta V = (24\text{ mA})(1\text{ m}\Omega) = 24\,\mu\text{V}$$

That $24\,\mu\text{V}$ gradient between the wavefront footprint ($+0.000024\text{ V}$) and the supply ground terminal ($0.000000\text{ V}$) drives the return current home while keeping the plane within microvolts of the $0\text{ V}$ reference.

### The Closed-Loop Power Supply Pump, Probing, and the Falling Edge

Sustaining a traveling step wave requires continuous charge delivery from the local power distribution network, two-contact differential probing, and proper far-end termination. Tracing a complete pulse from supply injection through load arrival and logic-zero discharge connects every part of the transmission-line loop.

#### Continuous Supply Current and Local Decoupling

Segment 1 at the driver never dumps its stored charge into Segment 2 and drops back to $0\text{ V}$; Segment 1 remains clamped to $+1.2\text{ V}$ through the closed pull-up switch while the power supply continuously feeds charge into the trace. In each second of travel, the wavefront advances a distance $v_p$ and charges a new capacitance $C v_p$ to voltage $V$, requiring a steady supply current:

$$I = \frac{\Delta Q}{\Delta t} = C\, v_p\, V = \frac{C}{\sqrt{LC}}\, V = \sqrt{\frac{C}{L}}\, V = \frac{V}{Z_0}$$

An ideal $1.2\text{ V}$ switch launching into a $50\ \Omega$ trace draws a constant wave current throughout transit (a real driver has a small internal source resistance $R_S$ that forms a voltage divider with $Z_0$, covered in [Chapter 3](03_Impedance_Reflections_and_Termination.md)):

$$I = \frac{1.2\text{ V}}{50\ \Omega} = 24\text{ mA}$$

At the driver end of the board, the local decoupling capacitor ($C_{\text{decap}}$) next to the transmitter pins and the board voltage regulator module (VRM) connect directly between the $+1.2\text{ V}$ rail and the $0\text{ V}$ ground plane. Together they act as a closed-loop charge pump: $C_{\text{decap}}$ supplies the initial picosecond current surge before the distant VRM responds, and the VRM replenishes $C_{\text{decap}}$ to sustain steady-state current. Returning conventional current exits the left edge of the $0\text{ V}$ ground plane at the same $24\text{ mA}$ rate that charge enters the trace, preventing charge accumulation and holding the plane at $0\text{ V}$.

#### Two-Contact Voltage Probing and Ground-Loop Inductance

Measurement of that $1.2\text{ V}$ signal with a multimeter or a high-bandwidth oscilloscope probe always requires **two** physical contacts because voltage is strictly a potential difference between two locations. Touching the probe tip to the signal trace ($+1.2\text{ V}$) while seating a coaxial ground spring on the adjacent PCB ground plane ($0\text{ V}$) reports the true signal swing, whereas placing both contacts on the same $1.2\text{ V}$ trace reports zero:

$$V_{\text{probe}} = 1.2\text{ V} - 0\text{ V} = 1.2\text{ V}, \qquad V_{\text{same-trace}} = 1.2\text{ V} - 1.2\text{ V} = 0\text{ V}$$

Using a long clip-on ground wire instead of a short coaxial ground spring forces the probe return current around a large physical loop of parasitic inductance $L_{\text{loop}}$. Fast edge currents through $L_{\text{loop}}$ add a false inductive voltage spike $V_{\text{error}}$ that masquerades as signal ringing on the oscilloscope screen:

$$V_{\text{error}} = L_{\text{loop}}\,\frac{di(t)}{dt}$$

#### Far-End Receiver Termination States

Far-end receiver termination ([Chapter 3](03_Impedance_Reflections_and_Termination.md)) determines the steady-state fields once the rising wavefront reaches distance $\ell$. With a **parallel-terminated load** matched to the line impedance, wavefront arrival leaves the entire trace charged to $1.2\text{ V}$ and stops dielectric displacement current everywhere ($I_D$ of $0\text{ A}$). Termination resistor $R_T$ bridges the far end of the trace to the ground plane and takes over from the displacement current to close the loop, sustaining a steady DC conduction current $I_C$ alongside both the static vertical electric field and the static into-the-page magnetic field:

$$R_T = Z_0 = 50\ \Omega \qquad \Longrightarrow \qquad I_C = \frac{1.2\text{ V}}{50\ \Omega} = 24\text{ mA}$$

With an **open circuit or high-impedance CMOS gate** (infinite load resistance $R_L$), no DC path to ground exists at distance $\ell$, so current cannot exit the far end of the trace. Decay of the reflection transient reduces displacement current $I_D$ and conduction current $I_C$ to zero, collapses the magnetic field $\vec{B}$, and leaves only the static vertical electric field $E$ across the charged trace capacitance:

$$I_D = 0, \qquad I_C = 0, \qquad \vec{B} = 0, \qquad E = \frac{1.2\text{ V}}{h}$$

#### Falling-Edge Discharge Wavefront

Transmission of a logic `0` (a falling transition from $+1.2\text{ V}$ back to $0\text{ V}$) begins at the driver. The CMOS output stage opens the top PMOS pull-up switch to disconnect the $+1.2\text{ V}$ supply and closes the bottom NMOS pull-down switch, creating a low-resistance bridge directly between the near end of the trace and the $0\text{ V}$ ground plane beneath it. Segment 1 at the driver immediately drains its stored positive charge downward through the closed NMOS switch into the ground plane and drops to $0\text{ V}$, while Segment 2 still sits at $+1.2\text{ V}$.

The resulting potential difference causes Segment 2 to discharge leftward ($\leftarrow$) into Segment 1 and down through the NMOS switch to ground, dropping Segment 2 to $0\text{ V}$ and pulling charge from Segment 3. At the moving **discharge wavefront**, falling local voltage produces a negative temporal derivative $\partial v(z, t) / \partial t$ and drives an upward displacement current ($\uparrow$) that closes a counter-clockwise loop:

$$I_D = C\,\Delta z\,\frac{\partial v(z, t)}{\partial t} < 0$$

Stored positive charge drains leftward ($\leftarrow$) along the trace into the NMOS ground switch while the discharge boundary sweeps rightward ($\rightarrow$) at velocity $v_p$. By superposition, closing the pull-down switch launches a $-1.2\text{ V}$ wave in $+z$ that cancels the $+1.2\text{ V}$ state segment by segment.

### Conventional Current vs. Electron Motion

Positive-rail operation ($+1.2\text{ V}$) requires the power supply to perform the physical opposite of pushing electrons into the signal trace. Electrons carry negative charge ($-q$), and an uncharged $0\text{ V}$ copper trace contains equal numbers of protons and electrons. Raising the trace to $+1.2\text{ V}$ requires the power supply to *pull electrons out* of the trace at the driver end and pump them into the ground plane.

Removal of electrons from Segment 1 leaves behind a net positive charge deficiency ($+1.2\text{ V}$) on the trace and a net electron surplus on the ground plane beneath it. Propagation of the rising wavefront rightward ($+z$) causes free electrons in each newly reached trace segment to drift slightly leftward ($-z$) toward the driver while electrons in the ground plane drift slightly rightward ($+z$) beneath the wavefront.

Electrical engineering follows Benjamin Franklin's historical **conventional current** convention, defining current direction as the flow of positive charge (opposite to electron drift). Every field direction, right-hand rule, and circuit equation produces identical physical results under either convention; the rest of this series tracks current in the conventional direction.

## Worked Examples

### Electrons, Drift Velocity, and Signal Speed

Conduction electrons inside a copper trace drift at fractions of a millimeter per second, yet a digital edge crosses a circuit board in less than a nanosecond. Separating mechanical particle drift inside the metal lattice from electromagnetic wave propagation inside the dielectric resolves this apparent paradox.

Conduction current $I$ in a conductor of cross-sectional area $A$ obeys the microscopic carrier transport equation:

$$I = n \cdot A \cdot q \cdot v_d$$

Four physical quantities govern this transport relation:

- **Free-electron carrier density ($n$):** Copper's atomic lattice donates roughly one free conduction electron per atom, fixing carrier concentration $n$ at approximately $8.5 \times 10^{28}\text{ electrons/m}^3$. Kirchhoff's current law ensures that every electron pulled out of the trace is injected into the ground plane, keeping $n$ constant at all times.
- **Conductor cross-sectional area ($A$):** Trace width $w$ multiplied by copper thickness $t_{\text{cu}}$ defines the conducting cross-section through which charge carriers drift.
- **Elementary charge ($q$):** Each conduction electron carries a fixed charge magnitude $q$ of approximately $1.602 \times 10^{-19}\text{ C}$.
- **Electron drift velocity ($v_d$):** The internal longitudinal electric field $E_{\text{wire}}$ drives electrons through the copper lattice at an average net speed proportional to electron mobility $\mu_e$.

Conducting cross-section $A$ and average drift speed $v_d$ follow directly from trace dimensions and copper mobility:

$$A = w\, t_{\text{cu}}, \qquad v_d = \mu_e\, E_{\text{wire}}$$

The copper lattice and trace cross-section fix $n$, $A$, and $q$, so a larger current $I$ (driven by a larger voltage and stronger $E_{\text{wire}}$) proportionally increases the mechanical drift speed $v_d$. That variable particle drift speed $v_d$ inside the copper is completely distinct from the electromagnetic wave velocity $v_p$ ($c / \sqrt{\varepsilon_r}$, or $1 / \sqrt{LC}$) inside the dielectric, which depends solely on the laminate constants and never varies with voltage or current.

Consider the $24\text{ mA}$ wavefront current on a $50\ \Omega$ trace of width $w$ equal to $100\,\mu\text{m}$ and copper thickness $t_{\text{cu}}$ equal to $35\,\mu\text{m}$:

$$A = \left(100 \times 10^{-6}\text{ m}\right) \times \left(35 \times 10^{-6}\text{ m}\right) = 3.5 \times 10^{-9}\text{ m}^2$$

Rearrangement of the carrier transport equation for the drift velocity $v_d$ gives:

$$v_d = \frac{I}{n\, A\, q} = \frac{0.024\text{ A}}{\left(8.5 \times 10^{28}\text{ m}^{-3}\right) \left(3.5 \times 10^{-9}\text{ m}^2\right) \left(1.602 \times 10^{-19}\text{ C}\right)} \approx 5.0 \times 10^{-4}\text{ m/s}$$

Conduction electrons drift at $0.5\text{ mm/s}$, whereas the electromagnetic wavefront in the dielectric travels at $1.46 \times 10^8\text{ m/s}$, faster by a factor of nearly $300\text{ billion}$. Copper's lattice is already packed with $8.5 \times 10^{28}\text{ electrons/m}^3$, so electrons at the driver end only shift by nanometers for the electromagnetic field disturbance in the dielectric to propagate at $v_p$ and set local electrons in motion at each downstream segment.

### Signal, Voltage, and Characteristic Impedance

The electromagnetic wave is the signal, the transverse voltage $V$ is the electrical potential difference driving the wave, and the current $I$ is the resulting rate of charge flow. Within a single forward-traveling wave on a lossless line, voltage and current are locked in the constant ratio of the characteristic impedance:

$$Z_0 = \frac{V}{I}$$

On a $50\ \Omega$ trace, a $1.2\text{ V}$ wavefront carries $24\text{ mA}$ and a $0.6\text{ V}$ wavefront carries $12\text{ mA}$, and both wavefronts propagate at the same speed $v_p$. That single-wave ratio $V / I$ equals $Z_0$ strictly for a lone wave traveling in one direction. Superposition of a backward-traveling reflection over the same copper shifts the ratio of total voltage to total current away from $Z_0$, as [Chapter 3](03_Impedance_Reflections_and_Termination.md) proves.

### How Information Reaches the Receiver

Digital receivers recover data from the arrival times of wavefront transitions rather than by computing a Fourier transform of each incoming edge. At the far end of the link, the receiver acts as a clocked voltage comparator timed by a clock and data recovery (CDR) loop ([Chapter 17](17_CDR_and_PLL_Loop_Dynamics.md)).

Arrival of a rising wavefront steps the receiver voltage from $0\text{ V}$ to $1.2\text{ V}$, and the comparator samples the line at the center of the bit period (unit interval) to record a logic `1`. A closed pull-up switch held across a second consecutive bit period launches no new wavefront and keeps the line at $1.2\text{ V}$. The next clock sample then records a second logic `1` until a falling wavefront arrives to discharge the line to $0\text{ V}$.

The high-frequency harmonics inside each edge ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)) keep the rising and falling wavefronts steep in time. Loss of those high-frequency harmonics rounds and stretches the transition, shifting the instant at which the waveform crosses the comparator threshold and introducing timing jitter and bit errors.

## Edge Cases

### The Telegrapher's Equations with Losses and the Helmholtz Wave Equation

Real PCB traces have finite copper conductivity and imperfect dielectric insulation characterized by dielectric loss tangent $\tan\delta$. A complete transmission-line model adds series resistance $R$ (in $\Omega/\text{m}$) and parallel shunt conductance $G$ (in $\text{S/m}$) to each infinitesimal slice $\Delta z$ alongside $L$ and $C$:

| Parameter | Circuit Placement | Physical Origin | Frequency Dependence |
|---|---|---|---|
| **$R$** (series resistance, $\Omega/\text{m}$) | In series along the trace and return path | Lattice scattering of conduction electrons in copper | Holds constant at DC and rises as $\sqrt{f}$ at high frequencies via the skin effect ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)) |
| **$L$** (series inductance, $\text{H/m}$) | In series along the trace and return path | Magnetic energy stored in the trace-to-plane window | Remains nearly constant across high-speed signal bandwidths |
| **$G$** (shunt conductance, $\text{S/m}$) | In parallel across the dielectric | Dielectric dipole polarization friction (distinct from $1/R$) | Stays negligible at DC and rises linearly with frequency as $\omega C \tan\delta$ ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)) |
| **$C$** (shunt capacitance, $\text{F/m}$) | In parallel across the dielectric | Electric field energy stored between trace and ground plane | Remains nearly constant across gigahertz bandwidths |

#### Distributed Loss Mechanisms and the Lossy Telegrapher's Equations

The physical origin of parallel shunt conductance $G$ (measured in Siemens per meter, $\text{S/m}$, or $\Omega^{-1}/\text{m}$, and completely unrelated to horizontal copper resistance $R$) lies in molecular dipole polarization. Virtually zero free electrons leak DC current across fiberglass epoxy, yet a time-varying vertical electric field forces the polar epoxy molecules inside the FR4 laminate to twist back and forth billions of times per second.

Friction between those twisting molecular dipoles and their neighboring polymer chains dissipates electromagnetic energy into heat at a rate proportional to the square of the transverse voltage $V^2$. In circuit theory, any mechanism across two parallel plates that dissipates heat proportional to $V^2$ acts as an effective vertical resistance $R_{\text{polarization}}$ in parallel with capacitance $C$, defined alongside its reciprocal conductance $G$:

$$P_{\text{loss}} = \frac{V^2}{R_{\text{polarization}}} = G\, V^2, \qquad G = \frac{1}{R_{\text{polarization}}}$$

Reciprocal conductance $G$ eliminates fractions when summing the two parallel vertical currents crossing the dielectric slice $\Delta z$. Total shunt current leaving the trace across $\Delta z$ is the sum of the in-phase loss current $G\,\Delta z\,v(z, t)$ and the capacitive displacement current $C\,\Delta z\,\partial v(z, t) / \partial t$:

$$i(z, t) - i(z + \Delta z, t) = G\,\Delta z\,v(z, t) + C\,\Delta z\,\frac{\partial v(z, t)}{\partial t}$$

Similarly, the total series voltage drop along the copper slice $\Delta z$ is the sum of the resistive drop $R\,\Delta z\,i(z, t)$ and the inductive drop $L\,\Delta z\,\partial i(z, t) / \partial t$:

$$v(z, t) - v(z + \Delta z, t) = R\,\Delta z\,i(z, t) + L\,\Delta z\,\frac{\partial i(z, t)}{\partial t}$$

Division of both slice equations by $\Delta z$ as slice length $\Delta z$ shrinks to zero yields the general **lossy Telegrapher's Equations**:

$$-\frac{\partial v(z, t)}{\partial z} = R\,i(z, t) + L\,\frac{\partial i(z, t)}{\partial t}$$

$$-\frac{\partial i(z, t)}{\partial z} = G\,v(z, t) + C\,\frac{\partial v(z, t)}{\partial t}$$

#### Complex Phasor Reduction and the Helmholtz Wave Equation

Frequency-dependent losses $R(f)$ and $G(f)$ attenuate high frequencies more strongly than low frequencies, so an arbitrary digital pulse distorts along the line. Lossy transmission lines are solved one sinusoidal frequency $f$ at a time using complex phasors ([Chapter 3](03_Impedance_Reflections_and_Termination.md)) at angular frequency $\omega$:

$$\omega = 2\pi f$$

The time derivative of a sinusoidal wave $\cos(\omega t)$ scales its amplitude by $\omega$ and shifts its phase forward by $+90^\circ$ ($\pi/2\text{ radians}$) because the steepest upward slope of a cosine wave occurs at its upward zero-crossing, a quarter-cycle earlier in time than its peak:

$$\frac{d}{dt} \cos(\omega t) = -\omega\sin(\omega t) = \omega\cos(\omega t + 90^\circ)$$

Euler's formula packages both the $\omega$ amplitude scaling and the $+90^\circ$ counter-clockwise complex-plane rotation of the imaginary unit $j$ into a single algebraic operation:

$$e^{j\theta} = \cos\theta + j\sin\theta, \qquad j = \sqrt{-1}, \qquad e^{j 90^\circ} = j$$

Sinusoidal voltage and current at angular frequency $\omega$ take complex exponential form with position-dependent complex phasor amplitudes $V(z)$ and $I(z)$:

$$v(z, t) = V(z)e^{j\omega t}, \qquad i(z, t) = I(z)e^{j\omega t}$$

Differentiating those complex exponentials turns every time derivative $\partial / \partial t$ into multiplication by $j\omega$:

$$\frac{\partial v(z, t)}{\partial t} = \frac{\partial}{\partial t} \left[V(z)e^{j\omega t}\right] = j\omega\, V(z)e^{j\omega t}, \qquad \frac{\partial i(z, t)}{\partial t} = j\omega\, I(z)e^{j\omega t}$$

Substitution of these phasor expressions into the lossy Telegrapher's Equations and cancellation of the common nonzero time factor $e^{j\omega t}$ convert the partial differential equations into coupled ordinary differential equations in $z$:

$$-\frac{dV(z)}{dz} = (R + j\omega L)\, I(z)$$

$$-\frac{dI(z)}{dz} = (G + j\omega C)\, V(z)$$

Isolation of $V(z)$ from this coupled system begins with the spatial derivative $d/dz$ of the first equation, where $(R + j\omega L)$ is constant with respect to position $z$ at a fixed frequency $\omega$:

$$-\frac{d^2 V(z)}{dz^2} = (R + j\omega L)\,\frac{dI(z)}{dz}$$

Substituting $-(G + j\omega C)V(z)$ for $dI(z)/dz$ from the second equation eliminates $I(z)$ and produces the second-order **Helmholtz wave equation** for a lossy transmission line:

$$\frac{d^2 V(z)}{dz^2} = (R + j\omega L)(G + j\omega C)\, V(z) = \gamma^2\, V(z)$$

Complex propagation constant $\gamma$ combines series impedance and shunt admittance per meter into real and imaginary parts:

$$\gamma = \sqrt{(R + j\omega L)(G + j\omega C)} = \alpha + j\beta$$

#### Attenuation Constant, Phase Constant, and Lossy Characteristic Impedance

The Helmholtz equation states that differentiating $V(z)$ twice with respect to $z$ returns the constant $\gamma^2$ multiplied by the original function $V(z)$. An exponential function is the only mathematical function whose derivative is a constant multiple of itself, so a wave traveling in the $+z$ direction takes the exponential form:

$$V(z) = V^+ e^{-\gamma z}, \qquad I(z) = I^+ e^{-\gamma z}$$

Two spatial differentiations verify this solution directly:

$$\frac{dV(z)}{dz} = -\gamma V^+ e^{-\gamma z}, \qquad \frac{d^2 V(z)}{dz^2} = (-\gamma)^2 V^+ e^{-\gamma z} = \gamma^2\, V(z)$$

Restoring the time factor $e^{j\omega t}$ and decomposing $\gamma$ into its real part $\alpha$ and imaginary part $\beta$ reveal the physical meaning of both components:

$$v(z, t) = V^+ e^{-(\alpha + j\beta)z}\, e^{j\omega t} = \underbrace{V^+ e^{-\alpha z}}_{\text{amplitude decay}}\, \underbrace{e^{j(\omega t - \beta z)}}_{\text{traveling phase}}$$

Real and imaginary parts of $\gamma$ define the attenuation constant $\alpha$, phase constant $\beta$, and sinusoidal phase velocity $v_p$:

$$\alpha = \mathrm{Re}\{\gamma\}, \qquad \beta = \mathrm{Im}\{\gamma\} = \frac{\omega}{v_p}, \qquad v_p = \frac{\omega}{\beta}$$

Two propagation behaviors follow directly from those two components:

- **Attenuation constant ($\alpha$, in Nepers per meter, $\text{Np/m}$):** Governs the real exponential amplitude decay $e^{-\alpha z}$ as resistive and dielectric losses convert wave energy into heat along the trace.
- **Phase constant ($\beta$, in $\text{rad/m}$):** Governs the spatial phase shift $e^{-j\beta z}$ per meter of travel, setting the phase velocity $v_p$ at angular frequency $\omega$.

Substituting the forward-traveling phasors $V(z)$ and $I(z)$ back into the first coupled phasor equation relates the wave amplitudes $V^+$ and $I^+$:

$$-\frac{dV(z)}{dz} = \gamma V^+ e^{-\gamma z} = (R + j\omega L)\,I^+ e^{-\gamma z}$$

Solving for the ratio $V^+ / I^+$ yields Oliver Heaviside's general **characteristic impedance** of a lossy transmission line:

$$Z_0 = \frac{V(z)}{I(z)} = \frac{V^+}{I^+} = \frac{R + j\omega L}{\gamma} = \frac{R + j\omega L}{\sqrt{(R + j\omega L)(G + j\omega C)}} = \sqrt{\frac{R + j\omega L}{G + j\omega C}}$$

Zero-loss values of $R$ and $G$ recover the lossless results immediately:

$$\gamma = \sqrt{(j\omega L)(j\omega C)} = j\omega\sqrt{LC} \qquad \Longrightarrow \qquad \alpha = 0, \qquad \beta = \omega\sqrt{LC}$$

$$v_p = \frac{\omega}{\beta} = \frac{1}{\sqrt{LC}}, \qquad Z_0 = \sqrt{\frac{j\omega L}{j\omega C}} = \sqrt{\frac{L}{C}}$$

At multi-gigahertz SerDes frequencies on a PCB trace, reactive terms dominate resistive and conductive losses:

$$\omega L \gg R, \qquad \omega C \gg G$$

In that low-loss high-frequency regime, $Z_0$ remains close to $\sqrt{L/C}$ while copper skin-effect resistance $R(f)$ and dielectric loss $G(f)$ appear primarily in the attenuation constant $\alpha(f)$. Conductor series impedance $R + j\omega L$ also governs how return current distributes itself across reference planes across frequency, as [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) develops.

### Static Fields Between Transitions

Between logic transitions, no wavefront sweeps along the trace and no high-frequency energy propagates. Throughout the transit of a rising wavefront toward the receiver, the region behind the wavefront holds both a static vertical electric field ($V / h$) and a steady conduction current ($V / Z_0$) surrounded by its static magnetic field ($\vec{B} \otimes$).

Wavefront arrival at the far end and decay of all boundary reflections ([Chapter 3](03_Impedance_Reflections_and_Termination.md)) leave the entire line in a steady DC state dictated by the far-end load. An unterminated high-impedance CMOS receiver draws zero steady-state current $I_C$, so the magnetic field vanishes everywhere and the trace holds only a static vertical electric field like a charged capacitor. A parallel termination resistor $R_T$ to ground sustains a continuous DC current $I_C$ and a static magnetic field alongside the static electric field until the next wavefront arrives:

$$I_C = 0 \quad (\text{open load}), \qquad I_C = \frac{V}{R_T} \quad (\text{parallel termination})$$

High-frequency electromagnetic activity is confined to the rising and falling edges. [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) quantifies the frequency spectrum carried by each edge and derives how rise time dictates the required bandwidth of the interconnect and measurement instrumentation.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>
