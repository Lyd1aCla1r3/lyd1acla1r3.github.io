# Wave Propagation and Transmission Lines

<!-- SUMMARY: Information in a high-speed digital system travels as an electromagnetic wave guided through the dielectric material of the PCB, not as electrons drifting through copper. This guide traces the physical mechanism from the CMOS switching event through the distributed geometry of a transmission line, derives the characteristic impedance and the propagation velocity from the Telegrapher's Equations, links the geometric and material forms of the velocity, and explains why a steady current of V/Z0 flows behind every propagating wavefront. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

Every high-speed digital system operates on a single physical principle: information travels as electromagnetic waves, not as electrons drifting through copper. The moment a transistor connects a trace to a voltage rail, a localized electric field boundary forms and propagates through the dielectric material at a significant fraction of the speed of light, while the electrons themselves barely move. Understanding this distinction is the foundation on which all signal integrity analysis rests, from characteristic impedance and TDR measurements to jitter budgeting and equalization design.

This guide traces the complete physical mechanism of wave propagation on a PCB transmission line: the distributed nature of trace geometry, the CMOS switching event that launches a wavefront, the segment-by-segment chain reaction that constitutes propagation, the relationship between signal voltage and current, and the Telegrapher's Equations, from which the characteristic impedance and the propagation velocity are derived.

## Core Concepts

### Distributed vs. Lumped Elements

A discrete resistor, capacitor, or inductor is a *lumped* element: a component localized at a single physical coordinate, designed to hold a specific value and small enough that the signal traverses it in effectively zero time. Ohm's law, Kirchhoff's voltage law, and the standard circuit equations all assume lumped behavior.

A transmission line is a *distributed* structure. Its physical dimensions are significant relative to the wavelength of the signal it carries. The capacitance and inductance are not localized hardware elements; they exist continuously along every microscopic fraction of the trace. A bare microstrip trace on a PCB is itself a capacitor, with no soldered ceramic component required: the trace is the top metal plate, the ground plane is the bottom metal plate, and the FR4 fiberglass laminate is the insulating dielectric between them. The capacitance is intrinsic to the geometry and distributed along the entire length.

The inductance is similarly geometric: any current flowing through a conductor generates a surrounding magnetic field that resists changes in current flow. The signal current travels forward on the trace while the return current travels backward on the ground plane directly below it, forming a current loop. The area enclosed by this loop stores energy in the magnetic field, producing a distributed series inductance per unit length.

These two parameters are geometrically coupled, so a change that raises one usually lowers the other. Widening a trace increases the surface area facing the ground plane, which increases capacitance. That same widening simultaneously provides a broader path for current, which decreases the loop area and lowers inductance. Moving the trace closer to the ground plane increases capacitance and decreases inductance. The ratio of distributed inductance to distributed capacitance per unit length determines the characteristic impedance of the line, derived from the Telegrapher's Equations at the end of this section:

$$Z_0 = \sqrt{\frac{L}{C}}$$

The boundary between lumped and distributed behavior is set by comparing the time the wave needs to cross the trace with the duration of the signal transition. A trace whose one-way propagation delay is a small fraction of the rise time charges almost uniformly during the edge, and a single lumped capacitor models it adequately. A trace whose delay is comparable to the rise time has one end changing voltage while the other end has not yet responded, and only the distributed model describes it. A widely used guideline treats a trace as lumped only when its length is less than about one sixth of the spatial length of the rising edge, which is the distance the edge travels during one rise time. Assume a driver with a 30 ps rise time on FR4, where the wave travels about 0.147 mm per picosecond (derived in the velocity section below). The rising edge spans about 4.4 mm of trace, so the lumped limit, called the critical length, is roughly 0.7 mm. Essentially every trace in a multi-gigabit link is longer than this and must be analyzed as a transmission line.

### Why Ohm's Law Fails at High Speed

Ohm's law ($V = IR$) assumes an immediate steady-state condition where electrons drift uniformly across the entire conductor and the voltage is identical at every point. This assumption requires the signal to have already finished propagating and settled into equilibrium.

High-speed serial links operate in a regime where this equilibrium never exists during a signal transition. A CMOS driver transitions from low to high in picoseconds. The voltage at the near end of the trace changes before the wave has reached the far end. The wavefront sees the bare trace as an infinite chain of empty geometric capacitors it must fill with charge. The energy is consumed charging the local geometry, not overcoming the DC resistance of the copper.

The ratio of voltage to current within the traveling wave is determined by the trace geometry alone, expressed as the characteristic impedance $Z_0 = \sqrt{L/C}$, not the DC resistance of the conductor. Treating a high-speed transmission line as a lumped resistor produces physically incorrect results.

### Transverse Electromagnetic (TEM) Propagation

A static voltage applied by a disconnected battery creates a pure electric field with no associated magnetic field. A steady DC current creates a constant magnetic field with no changing electric field. Neither of these scenarios produces a propagating wave.

Propagation requires both fields to exist simultaneously and to vary in time, and two of Maxwell's equations supply the coupling between them. The Ampere-Maxwell law states that a changing electric field produces a magnetic field in the same way a conduction current does; this contribution is the displacement current that appears again in the propagation sequence below. Faraday's law states that a changing magnetic field produces an electric field, and [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) develops it in detail as the basis of inductance. Each changing field regenerates the other a short distance further along the line, and the pair travels as a self-sustaining transverse electromagnetic (TEM) wave through the dielectric material between the trace and the ground plane. The word transverse means that both fields point across the direction of travel: the electric field runs from the trace down to the plane, and the magnetic field circles the trace within the cross-section.

The electromagnetic wave propagates through the dielectric material, not through the copper. The copper trace and the ground plane serve as physical guide rails that confine and direct the wave. This is the fundamental reason that the properties of the PCB laminate material (dielectric constant, loss tangent) dominate high-speed signal integrity engineering.

### Propagation Velocity and the Dielectric Constant

The speed of the electromagnetic wave in a transmission line is governed by the dielectric constant ($\epsilon_r$, also called relative permittivity or $D_k$) of the insulating material surrounding the conductors:

$$v_p = \frac{c}{\sqrt{\epsilon_r}}$$

where $c$ is the speed of light in a vacuum ($\approx 3 \times 10^8$ m/s).

Standard FR4 has a dielectric constant of approximately 4.0 to 4.5, which reduces the propagation velocity to roughly half the speed of light. For $\epsilon_r = 4.2$, the velocity is about $1.46 \times 10^8$ m/s, a delay of about 6.8 ps per millimeter (about 170 ps per inch). Lower-loss laminates such as Megtron 6 have lower dielectric constants (around 3.6), which allow slightly faster propagation.

The amplitude of the signal has no effect on propagation velocity. A higher voltage produces a stronger electric field (higher "electrical pressure"), but the velocity of an electromagnetic wave in a transmission line is determined entirely by the distributed inductance and capacitance of the physical geometry:

$$v_p = \frac{1}{\sqrt{LC}}$$

Neither $L$ nor $C$ changes when the voltage increases from 1V to 5V. The speed remains identical regardless of the signal amplitude.

The two velocity formulas describe the same quantity, and the link between them shows why the geometry drops out of the velocity. Every TEM line in a uniform dielectric obeys:

$$LC = \mu_0 \epsilon_0 \epsilon_r$$

where $\mu_0$ is the permeability of free space and $\epsilon_0$ is the permittivity of free space. Copper and PCB laminates are nonmagnetic, so the permeability stays at $\mu_0$. A wide trace over a plane, with the fringing fields at its edges ignored, shows the cancellation directly. Assume a trace of width $w$ at height $h$ above the plane. The capacitance per unit length follows the parallel-plate formula:

$$C = \frac{\epsilon_0 \epsilon_r w}{h}$$

The inductance per unit length of the same geometry, a current sheet of width $w$ with its return sheet a distance $h$ below, is:

$$L = \frac{\mu_0 h}{w}$$

Multiplying the two cancels both the width and the height:

$$LC = \frac{\epsilon_0 \epsilon_r w}{h} \cdot \frac{\mu_0 h}{w} = \mu_0 \epsilon_0 \epsilon_r$$

Substituting this product into the geometric velocity formula:

$$v_p = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{\mu_0 \epsilon_0}} \cdot \frac{1}{\sqrt{\epsilon_r}} = \frac{c}{\sqrt{\epsilon_r}}$$

The last step uses the defining relationship of the speed of light, $c = 1/\sqrt{\mu_0 \epsilon_0}$. Widening the trace raises $C$ and lowers $L$ by the same factor, which is the geometric coupling described earlier expressed as an equation, so widening a trace changes its impedance while leaving its velocity unchanged. The same two expressions give the impedance of the wide trace, $Z_0 = \sqrt{L/C} = (h/w)\sqrt{\mu_0/(\epsilon_0 \epsilon_r)}$, which falls as the trace widens or moves closer to the plane. A microstrip departs from the uniform-dielectric case in degree: part of its field travels through the air above the trace, so the wave sees an effective dielectric constant between 1 and $\epsilon_r$ and travels slightly faster than a stripline buried in the same laminate.

### The Telegrapher's Equations: Deriving Z0 and Velocity

The characteristic impedance and the propagation velocity both follow from applying Kirchhoff's laws to one short slice of line. A slice of a lossless line, of length $\Delta z$, contains a series inductance $L\,\Delta z$ and a shunt capacitance $C\,\Delta z$, where $L$ and $C$ are the per-unit-length values. Let $v(z,t)$ and $i(z,t)$ be the voltage and current at position $z$ and time $t$.

Kirchhoff's voltage law states that the voltage lost across the slice equals the voltage across its series inductance:

$$v(z,t) - v(z+\Delta z,t) = L\,\Delta z\,\frac{\partial i}{\partial t}$$

Kirchhoff's current law states that the current lost along the slice is the current diverted through its shunt capacitance:

$$i(z,t) - i(z+\Delta z,t) = C\,\Delta z\,\frac{\partial v}{\partial t}$$

Dividing both equations by $\Delta z$ and letting the slice shrink to zero turns each left-hand difference into a spatial derivative. The results are the lossless Telegrapher's Equations:

$$-\frac{\partial v}{\partial z} = L\,\frac{\partial i}{\partial t}$$

$$-\frac{\partial i}{\partial z} = C\,\frac{\partial v}{\partial t}$$

The first equation states that a voltage falling along the line requires a current changing in time. The second states that a current falling along the line requires a voltage changing in time, because the current that disappears from the trace is charging the local capacitance.

A wave traveling in the $+z$ direction at speed $v_p$ keeps its shape, so its voltage and current depend only on the combination $t - z/v_p$. Writing the voltage waveform as $f$ and the current waveform as $g$:

$$v(z,t) = f\!\left(t - \frac{z}{v_p}\right), \qquad i(z,t) = g\!\left(t - \frac{z}{v_p}\right)$$

By the chain rule, a derivative with respect to $z$ brings out a factor of $-1/v_p$, while a derivative with respect to $t$ brings out a factor of 1:

$$\frac{\partial v}{\partial z} = -\frac{1}{v_p} f', \qquad \frac{\partial i}{\partial t} = g'$$

Here $f'$ and $g'$ are the derivatives of each waveform with respect to its argument. Substituting both into the first Telegrapher's Equation:

$$\frac{1}{v_p} f' = L\, g'$$

Integrating both sides gives the first relationship between voltage and current (the integration constant is zero because the line ahead of the wave is uncharged and carries no current):

$$f = v_p L\, g$$

The same steps applied to the second Telegrapher's Equation give the second relationship:

$$g = v_p C\, f$$

Substituting the second relationship into the first:

$$f = v_p L \cdot v_p C\, f = v_p^2 LC\, f$$

The waveform $f$ cancels from both sides, leaving the propagation velocity:

$$v_p = \frac{1}{\sqrt{LC}}$$

The characteristic impedance is the ratio of the voltage waveform to the current waveform. Taking the first relationship and substituting the velocity:

$$Z_0 = \frac{f}{g} = v_p L = \frac{L}{\sqrt{LC}} = \sqrt{\frac{L}{C}}$$

The waveform shape $f$ appears in neither result. Every edge, regardless of its rise time or amplitude, travels at the same velocity and carries current in the same proportion to its voltage, provided $L$ and $C$ do not depend on frequency. Losses introduce that frequency dependence, as the Edge Cases section shows.

## Architecture

### The CMOS Driver as a High-Speed Valve

The voltage rail (such as +1.2V) and the ground plane (0V) are two reservoirs of constant electrical potential. The power distribution network (PDN) works to keep these reservoirs stable and fully charged, regardless of what the surrounding logic circuits are doing.

At the beginning of a trace sits an output driver (transmitter). At the most basic level, this driver consists of two complementary transistors acting as switches. The pull-up transistor connects the trace to the voltage rail. The pull-down transistor connects the trace to ground. The power supply is never asked to generate different voltage levels, and the information is encoded in *time*, in the moments at which the switches change state. To send a logic "1," the driver closes the pull-up switch and opens the pull-down switch, connecting the trace to the +1.2V reservoir. To send a logic "0," the driver does the reverse.

The power supply provides the constant potential energy, and the transistor decides when that energy is applied to the trace. Abrupt transitions in the time domain contain broad frequency content in the frequency domain, and [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) quantifies that content and its dependence on the transition speed.

### The Wavefront Launch Event

Consider a trace currently sitting at 0V. At the exact picosecond the pull-up transistor switches on, the physical copper at the beginning of the trace is abruptly exposed to the +1.2V potential from the rail.

The entire length of the trace cannot instantly jump to 1.2V. The distributed parasitic capacitance requires time to charge, and the distributed series inductance resists sudden current flow. A sharp boundary forms right at the transmitter between the newly applied 1.2V region and the existing 0V region.

The 1.2V difference concentrated across this narrow boundary creates an intense, localized change in the electric field. This field, accompanied by a magnetic field from the inrush current, is what launches down the trace as an electromagnetic wave. The spatial width of the boundary equals the rise time multiplied by the propagation velocity, about 4.4 mm for a 30 ps edge on FR4.

### Segment-by-Segment Propagation

The physical mechanism of propagation can be understood by mentally dividing the entire trace into millions of microscopic, contiguous segments. Each segment is a tiny piece of copper separated from the ground plane by an insulator, making each segment a tiny capacitor with a tiny series inductance.

**Time $t = 0$:** The transistor switches on, abruptly exposing the very first microscopic segment of the trace (at $d = 0$) to the 1.2V rail. To bring this first segment up to 1.2V, charge must be deposited onto it. A localized burst of conventional current flows from the power supply into this segment (physically, electrons are pulled out of the copper, as the section on conventional current below explains). This movement of charge is the conduction current. The accumulating charge rapidly builds an electric field across the dielectric, pointing from the trace down to the ground plane. Maxwell showed that a changing electric field produces a magnetic field exactly as a current does. This displacement current bridges the physical gap of the insulator, completing the local circuit loop back through the ground plane to the source. At this moment, only the first microscopic segment is affected, and the rest of the trace has not yet received any signal.

**Time $t > 0$:** Segment 1 is now charged to 1.2V, but segment 2 remains at 0V. The voltage difference causes segment 1 to act as the local power source for segment 2. Charge shifts from segment 1 into segment 2. The local series inductance briefly resists this sudden movement, but charge transfers. Segment 2 charges, and an electric field forms beneath it, creating a local displacement current through the dielectric and a local magnetic field around the copper. Segment 2 then acts as the source for segment 3, which in turn charges segment 4.

This continuous, sequential charging of microscopic segments is the physical mechanism of electromagnetic wave propagation on a transmission line.

### The Three Zones of a Propagating Wavefront

Freezing time while the wavefront is halfway down the board reveals three distinct zones:

1. **Behind the wavefront:** The trace is fully charged to 1.2V. A static electric field holds steady between the trace and the ground plane, and because the voltage is not changing, no displacement current flows here. The conduction current is steady and nonzero: a current of $V/Z_0$ flows along the trace from the driver to the wavefront and returns along the ground plane beneath it, surrounding the trace with a static magnetic field. This current delivers the charge that the wavefront deposits on each newly reached segment, as the next section quantifies.

2. **Ahead of the wavefront:** The trace is still at 0V, its voltage is not changing, and neither conduction current nor displacement current flows.

3. **Exactly at the wavefront:** The voltage is actively transitioning from 0V to 1.2V. Charge is shifting to charge the local segment (conduction current). The electric field is growing, passing energy through the dielectric (displacement current). The current flows in a loop: forward on the trace from the driver to the wavefront, vertically through the dielectric as displacement current, and backward through the ground plane to the source. The vertical leg of this loop, the only place where the fields are changing, slides down the transmission line at the propagation velocity, so the loop lengthens as the signal travels.

### The Role of the Power Supply During Propagation

A critical physical detail: segment 1 does not simply dump its stored charge into segment 2 and go dead. Segment 1 remains continuously connected to the 1.2V power supply through the closed transistor switch. The power supply acts as a continuous, high-pressure source that forces charge into the trace at $d = 0$ to feed the propagating wavefront. Every segment behind the wavefront stays firmly pinned at 1.2V.

The rate at which the supply must deliver charge follows from the geometry. In each second, the wavefront advances a distance $v_p$ and charges that length of line, whose capacitance is $C v_p$, to the voltage $V$. The charge delivered per second is the current:

$$I = C\, v_p\, V = \frac{C}{\sqrt{LC}}\, V = \sqrt{\frac{C}{L}}\, V = \frac{V}{Z_0}$$

An ideal 1.2V switch launching into a 50Ω line therefore draws a steady 24 mA from the supply for as long as the wavefront is still traveling toward the far end. A real driver has some output resistance, which forms a voltage divider with $Z_0$ and lowers the launched voltage; [Chapter 3](03_Impedance_Reflections_and_Termination.md) treats that divider. The ratio $Z_0 = V/I$ obtained here from charge bookkeeping alone is the same one the Telegrapher's Equations produced.

The forward direction of energy flow is maintained by the permanent voltage gradient. The driver at $d = 0$ is forcefully held at 1.2V, representing high potential energy. The uncharged trace ahead of the wavefront sits at 0V. Charge always flows from higher potential to lower potential. The electrical pressure behind the wavefront is 1.2V, and the pressure in front is 0V. A forward segment cannot transfer charge backward to a previous segment because the previous segment is held at a higher electrical potential by the continuous supply.

The transmitter sends a logic "0" by disconnecting the 1.2V rail and connecting the trace to 0V ground. The high-pressure source is removed, a low-resistance path to ground is provided, and the stored charge flows out of the trace through the driver, discharging the line segment by segment as a falling wavefront travels toward the far end.

### Conventional Current vs. Electron Motion

Operating a standard positive voltage rail (+1.2V) means the power supply is performing the exact opposite of "pushing electrons into the trace." Electrons carry negative charge, and the copper trace naturally contains an equal number of protons and electrons, giving it a neutral 0V baseline. Creating a +1.2V potential on the trace requires the power supply to *strip electrons away* from the copper atoms and deposit them into the ground plane.

This removal of electrons creates a localized electron deficiency (a net positive charge) at $d = 0$. The propagating wavefront requires the power supply to continuously pull more electrons out of the trace at $d = 0$ so that each newly encountered segment reaches that same +1.2V state of electron deficiency.

Operating a negative voltage rail (-1.2V) reverses this: the power supply forces surplus electrons into the trace, creating a state of electron overdensity.

Electrical engineers typically use "conventional current" and state that "the power supply pushes charge into the trace" for a positive voltage. This is a historical mathematical convention established by Benjamin Franklin before the electron was discovered. The physical reality of the subatomic motion is always reversed for positive voltages. The core mechanical principle remains identical regardless of polarity: the power supply actively does physical work at $d = 0$ to alter the electron density of the copper, and it must continuously perform that work to keep the entire length of the transmission line fully charged behind the wavefront. The rest of this series describes current in the conventional direction.

## Worked Examples

### Electrons, Drift Velocity, and Signal Speed

Electrons move through copper at a drift velocity measured in millimeters per second. The signal arrives at the far end of a trace in under a nanosecond. The resolution to this apparent paradox lies in the distinction between particle transport and wave transport.

The mathematical definition of current is:

$$I = n \cdot A \cdot q \cdot v_d$$

where $n$ is the electron density (number of free electrons per unit volume), $A$ is the cross-sectional area of the conductor, $q$ is the charge of one electron, and $v_d$ is the drift velocity. The electron density $n$ is a fixed physical property of the copper lattice (approximately $8.5 \times 10^{28}$ electrons per cubic meter). To increase current, the drift velocity $v_d$ increases. The drift velocity remains extremely slow, but the number of free electrons is so large that a tiny collective drift moves a large number of coulombs past any cross-section each second.

Assume the 24 mA wavefront current from the previous section flows in a trace 100 µm wide and 35 µm thick, a cross-section of $3.5 \times 10^{-9}$ m². Solving the current equation for the drift velocity:

$$v_d = \frac{I}{n A q} = \frac{0.024}{(8.5 \times 10^{28})(3.5 \times 10^{-9})(1.6 \times 10^{-19})} \approx 5 \times 10^{-4} \text{ m/s}$$

The electrons drift at about half a millimeter per second, while the wavefront they support travels at about $1.5 \times 10^8$ m/s, a ratio of roughly 300 billion.

The copper trace is already packed completely full of free electrons. Applying the 1.2V potential at the driver exerts a force on the electrons at $d = 0$, which drift a short distance toward the driver. Their neighbors drift to fill the vacancy, and the next neighbors follow, creating a cascading wave of charge-density change along the line. An electron at $d = 0$ only needs to move a fraction of a micrometer for the disturbance to pass to its neighbor, which passes it to the next neighbor in line.

The signal is the electromagnetic wave traveling through the dielectric. The current is the localized shuffling of electrons facilitating that wave. The electrons leaving the transmitter are not the same electrons arriving at the receiver when the bit flips. The wave propagates through the dielectric at a fraction of the speed of light, locally perturbing the electron sea as it passes.

### Signal, Voltage, and Characteristic Impedance

The "signal" is the electromagnetic wave, and its driving force is the voltage (potential difference). The current is the resulting flow of charge. The relationship linking voltage to current in a traveling wave is the characteristic impedance:

$$Z_0 = \frac{V}{I}$$

A higher voltage pushes more current through a given transmission line geometry. On a 50Ω line, a 1.2V wavefront carries 24 mA and a 0.6V wavefront carries 12 mA, and both travel at the same velocity. This relationship holds strictly for the traveling wave; it does not describe the DC resistance of the copper. It also holds only for a single wave traveling in one direction. A reflected wave traveling back over the same segment adds its own voltage and current, and the ratio of the totals at that point is no longer $Z_0$, as [Chapter 3](03_Impedance_Reflections_and_Termination.md) shows.

### How Information Reaches the Receiver

Information is carried by the arrival time of wavefronts, not by the receiver interpreting the frequency content of each edge.

The receiver at the far end of the trace is essentially a voltmeter that samples the line at instants set by a recovered clock ([Chapter 17](17_CDR_and_PLL_Loop_Dynamics.md) explains how the receiver extracts that clock from the data itself). A rising-edge wavefront arrives, the receiver's local voltage jumps from 0V to 1.2V, and at the next clock tick the receiver reads 1.2V and records a "1." At the following tick the trace is still fully charged, since the transmitter kept the pull-up transistor closed and no falling edge has arrived, so the receiver records a second "1." A falling-edge wavefront then arrives and discharges the trace to 0V, and the receiver records a "0" at the next tick.

The data is encoded purely in the time duration between wavefronts. The high-frequency content of each edge, quantified in [Chapter 2](02_Frequency_Content_of_Digital_Signals.md), is the physical mechanism that makes those edges steep and sharp. An edge lacking that content would be slow and sloped, and the receiver would struggle to identify the exact moment the transition crossed the threshold, leading to jitter and bit errors.

## Edge Cases

### The Telegrapher's Equations with Losses

The derivation in Core Concepts assumes perfect copper and a perfect insulator. A real line adds two more distributed parameters, so each infinitesimal slice contains four:

- **$R$** (series resistance): the resistance per unit length of the conductor and its return path, which rises with frequency because of the skin effect ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)).
- **$L$** (series inductance): the self-inductance of the current loop formed by the trace and its return path on the ground plane.
- **$G$** (shunt conductance): the conductance per unit length through the dielectric between the trace and the ground plane. $G$ is a separate parameter, not the reciprocal of $R$. DC leakage through a good laminate is negligible; at high frequencies $G$ is dominated by dielectric loss and is approximately $\omega C \tan\delta$, where $\tan\delta$ is the loss tangent of the laminate ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)).
- **$C$** (shunt capacitance): the parallel capacitance between the trace and the ground plane.

The series elements ($R$ and $L$) are in-line with the current path. They dictate the impedance that the physical current encounters while traveling along the conductor. The shunt elements ($G$ and $C$) are in parallel between the trace and the ground plane. They determine how much current leaks across the dielectric at each point along the line.

Adding $R$ to the voltage equation and $G$ to the current equation gives the full Telegrapher's Equations:

$$-\frac{\partial v}{\partial z} = R\,i + L\,\frac{\partial i}{\partial t}$$

$$-\frac{\partial i}{\partial z} = G\,v + C\,\frac{\partial v}{\partial t}$$

With losses present, an edge no longer keeps its shape, because each frequency inside it is attenuated and delayed by a different amount. The analysis therefore proceeds one sine-wave frequency at a time. For a sine wave at angular frequency $\omega = 2\pi f$, each time derivative becomes a multiplication by $j\omega$, the notation for a 90° phase shift that [Chapter 3](03_Impedance_Reflections_and_Termination.md) derives in its treatment of reactive impedance. Writing $V$ and $I$ for the complex amplitudes of the voltage and current at one frequency, the equations become:

$$-\frac{dV}{dz} = (R + j\omega L)\, I$$

$$-\frac{dI}{dz} = (G + j\omega C)\, V$$

A forward-traveling solution has the form $V = V^+ e^{-\gamma z}$ and $I = I^+ e^{-\gamma z}$, where $\gamma$ is the propagation constant. Its real part sets the attenuation per unit length, and its imaginary part sets the phase shift per unit length. Differentiating each exponential brings down a factor of $-\gamma$, so the two equations become:

$$\gamma\, V^+ = (R + j\omega L)\, I^+$$

$$\gamma\, I^+ = (G + j\omega C)\, V^+$$

Multiplying the two equations together and canceling the common factor $V^+ I^+$ gives the propagation constant:

$$\gamma = \sqrt{(R + j\omega L)(G + j\omega C)}$$

Dividing the first equation by $I^+$ and substituting $\gamma$ gives the characteristic impedance, first written in this form by Oliver Heaviside:

$$Z_0 = \frac{V^+}{I^+} = \frac{R + j\omega L}{\gamma} = \sqrt{\frac{R + j\omega L}{G + j\omega C}}$$

Setting $R = G = 0$ recovers $Z_0 = \sqrt{L/C}$ and a purely imaginary $\gamma = j\omega\sqrt{LC}$, whose phase shift per unit length corresponds to the velocity $v_p = 1/\sqrt{LC}$ found earlier. At multi-gigahertz frequencies, $\omega L$ greatly exceeds $R$ and $\omega C$ greatly exceeds $G$ on a typical PCB trace, so $Z_0$ stays close to $\sqrt{L/C}$ even on a lossy line. The losses appear mainly in the real part of $\gamma$, as an attenuation that grows with frequency.

The series impedance $R + j\omega L$ also governs how return current distributes itself when several return paths are available, a topic [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) develops.

### Static Fields Between Transitions

Between edge transitions, no new frequency content propagates along the trace. The section behind a wavefront that is still traveling holds a static electric field and carries the steady current $V/Z_0$ with its static magnetic field, as described in the three-zone picture. The wavefront then reaches the far end, and the reflections described in [Chapter 3](03_Impedance_Reflections_and_Termination.md) travel back and forth until the line settles into a DC state set by the load. A high-impedance CMOS receiver draws essentially no current, so only the static electric field remains and the magnetic field disappears. A resistive termination $R_T$ keeps a DC current $V/R_T$ flowing, together with its static magnetic field.

The trace remains in this static state until the next wavefront arrives to change it. The changing fields, and therefore the high-frequency content of the signal, are confined to the rising and falling edges, while the flat portions between edges hold only static fields.

The next chapter determines how much high-frequency content a single edge carries, which sets the bandwidth that every later structure in the channel, and every instrument that measures it, must support.
