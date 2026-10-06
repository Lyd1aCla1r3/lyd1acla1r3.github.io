# Wave Propagation and Transmission Lines

<!-- SUMMARY: Information in a high-speed digital system travels as electromagnetic waves propagating through the dielectric material of the PCB, not as electrons drifting through copper. This guide traces the complete physical mechanism from the CMOS switching event through distributed transmission line geometry to the Telegrapher's Equations. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

Every high-speed digital system operates on a single physical principle: information travels as electromagnetic waves, not as electrons drifting through copper. The moment a transistor connects a trace to a voltage rail, a localized electric field boundary forms and propagates through the dielectric material at a significant fraction of the speed of light. The electrons themselves barely move. Understanding this distinction is the foundation on which all signal integrity analysis rests, from characteristic impedance and TDR measurements to jitter budgeting and equalization design.

This guide traces the complete physical mechanism of wave propagation on a PCB transmission line: the distributed nature of trace geometry, the CMOS switching event that launches a wavefront, the segment-by-segment chain reaction that constitutes propagation, the relationship between signal voltage and current, and the Telegrapher's Equations that formalize the entire system mathematically.

## Core Concepts

### Distributed vs. Lumped Elements

A discrete resistor, capacitor, or inductor is a *lumped* element: a component localized at a single physical coordinate, designed to hold a specific value and small enough that the signal traverses it in effectively zero time. Ohm's law, Kirchhoff's voltage law, and the standard circuit equations all assume lumped behavior.

A transmission line is a *distributed* structure. Its physical dimensions are significant relative to the wavelength of the signal it carries. The capacitance and inductance are not localized hardware elements; they exist continuously along every microscopic fraction of the trace. A bare microstrip trace on a PCB is itself a capacitor: the trace is the top metal plate, the ground plane is the bottom metal plate, and the FR4 fiberglass laminate is the insulating dielectric between them. No soldered ceramic component is required. The capacitance is intrinsic to the geometry and distributed along the entire length.

The inductance is similarly geometric. Any current flowing through a conductor generates a surrounding magnetic field that resists changes in current flow. The signal current travels forward on the trace while the return current travels backward on the ground plane directly below it, forming a current loop. The area enclosed by this loop stores energy in the magnetic field, producing a distributed series inductance per unit length.

These two parameters are geometrically coupled. Widening a trace increases the surface area facing the ground plane, which increases capacitance. That same widening simultaneously provides a broader path for current, which decreases the loop area and lowers inductance. Moving the trace closer to the ground plane increases capacitance and decreases inductance. The ratio of distributed inductance to distributed capacitance per unit length determines the characteristic impedance of the line:

$$Z_0 = \sqrt{\frac{L}{C}}$$

### Why Ohm's Law Fails at High Speed

Ohm's law ($V = IR$) assumes an immediate steady-state condition where electrons drift uniformly across the entire conductor and the voltage is identical at every point. This assumption requires the signal to have already finished propagating and settled into equilibrium.

High-speed serial links operate in a regime where this equilibrium never exists during a signal transition. A CMOS driver transitions from low to high in picoseconds. The voltage at the near end of the trace changes before the wave has reached the far end. The wavefront sees the bare trace as an infinite chain of empty geometric capacitors it must fill with charge. The energy is consumed charging the local geometry, not overcoming the DC resistance of the copper.

The ratio of voltage to current within the traveling wave is determined by the trace geometry alone, expressed as the characteristic impedance $Z_0 = \sqrt{L/C}$, not the DC resistance of the conductor. Treating a high-speed transmission line as a lumped resistor produces physically incorrect results.

### Transverse Electromagnetic (TEM) Propagation

A static voltage applied by a disconnected battery creates a pure electric field with no associated magnetic field. A steady DC current creates a constant magnetic field with no changing electric field. Neither of these scenarios produces a propagating wave.

Propagation requires both fields to exist simultaneously and to vary in time. Maxwell's equations mandate that a changing electric field induces a changing magnetic field, and a changing magnetic field induces a changing electric field. These two fields couple into a self-sustaining transverse electromagnetic (TEM) wave that travels through the dielectric material between the trace and the ground plane.

The electromagnetic wave propagates exclusively through the dielectric material, not through the copper. The copper trace and the ground plane serve only as physical guide rails that confine and direct the wave. This is the fundamental reason that the properties of the PCB laminate material (dielectric constant, loss tangent) completely dominate high-speed signal integrity engineering.

### Propagation Velocity and the Dielectric Constant

The speed of the electromagnetic wave in a transmission line is governed by the dielectric constant ($\epsilon_r$, also called relative permittivity or $D_k$) of the insulating material surrounding the conductors:

$$v_p = \frac{c}{\sqrt{\epsilon_r}}$$

where $c$ is the speed of light in a vacuum ($\approx 3 \times 10^8$ m/s).

Standard FR4 has a dielectric constant of approximately 4.0 to 4.5, which reduces the propagation velocity to roughly half the speed of light. Lower-loss laminates such as Megtron 6 have lower dielectric constants (around 3.6), which allow slightly faster propagation.

The amplitude of the signal has no effect on propagation velocity. A higher voltage produces a stronger electric field (higher "electrical pressure"), but the velocity of an electromagnetic wave in a transmission line is determined entirely by the distributed inductance and capacitance of the physical geometry:

$$v_p = \frac{1}{\sqrt{LC}}$$

Neither $L$ nor $C$ changes when the voltage increases from 1V to 5V. The speed remains identical regardless of the signal amplitude.

## Architecture

### The CMOS Driver as a High-Speed Valve

The voltage rail (such as +1.2V) and the ground plane (0V) are two reservoirs of constant electrical potential. The power distribution network (PDN) works to keep these reservoirs stable and fully charged, regardless of what the surrounding logic circuits are doing.

At the beginning of a trace sits an output driver (transmitter). At the most basic level, this driver consists of two complementary transistors acting as switches. The pull-up transistor connects the trace to the voltage rail. The pull-down transistor connects the trace to ground. Information is not sent by asking the power supply to generate different voltage levels. Instead, information is encoded in *time*. To send a logic "1," the driver closes the pull-up switch and opens the pull-down switch, connecting the trace to the +1.2V reservoir. To send a logic "0," the driver does the reverse.

The power supply provides the constant potential energy. The transistor provides the timing. The laws of physics dictate that abrupt transitions in the time domain inherently contain broad frequency content in the frequency domain.

### The Wavefront Launch Event

Consider a trace currently sitting at 0V. At the exact picosecond the pull-up transistor switches on, the physical copper at the beginning of the trace is abruptly exposed to the +1.2V potential from the rail.

The entire length of the trace cannot instantly jump to 1.2V. The distributed parasitic capacitance requires time to charge, and the distributed series inductance resists sudden current flow. A sharp boundary forms right at the transmitter between the newly applied 1.2V region and the existing 0V region.

The massive difference in potential across this microscopic physical boundary creates a very intense, localized electric field. This field, accompanied by a magnetic field from the inrush current, is what launches down the trace as an electromagnetic wave.

### Frequency Content of the Transition

The high-frequency content carried by the signal does not come from different voltage levels output by the rail. It comes entirely from the speed of the transition between the two DC states.

Toggling the rail connection at a constant rate creates a square wave in the time domain. Fourier analysis shows that a perfect square wave is constructed by summing a fundamental sine wave with an infinite series of odd harmonics. A fast rise time (for example, 20 picoseconds) requires frequency harmonics extending well past 15 GHz to mathematically construct that steep vertical edge, regardless of how infrequently the transitions occur.

Two distinct frequency scales coexist on the same transmission line:

- **The data rate frequency** describes how often the driver chooses to change states. An alternating 10101010 pattern at 10 Gbps has a fundamental frequency of 5 GHz. A long run of identical bits (like 11111) drops to 0 Hz (DC) for that duration.
- **The edge bandwidth** describes the high-frequency harmonics required to construct the shape of each rising or falling transition. This bandwidth is dictated entirely by the transistor's switching speed, not by the bit pattern.

Both frequency scales propagate simultaneously on the same physical trace. Any mechanism that treats high frequencies differently from low frequencies (such as the skin effect, dielectric absorption, or dispersion) will cause the composite square wave to distort and smear as it propagates.

### Segment-by-Segment Propagation

The physical mechanism of propagation can be understood by mentally dividing the entire trace into millions of microscopic, contiguous segments. Each segment is a tiny piece of copper separated from the ground plane by an insulator, making each segment a tiny capacitor with a tiny series inductance.

**Time $t = 0$:** The transistor switches on, abruptly exposing the very first microscopic segment of the trace (at $d = 0$) to the 1.2V rail. To bring this first segment up to 1.2V, charge must be deposited onto it. A localized burst of electrons flows from the power supply into this segment. This physical movement of charge is the conduction current. As charge accumulates, an electric field rapidly builds across the dielectric, pointing from the trace down to the ground plane. Maxwell proved that a rapidly changing electric field behaves exactly like a current. This is the displacement current, and it bridges the physical gap of the insulator, completing the local circuit loop back through the ground plane to the source. At this moment, only the first microscopic segment is affected. The rest of the trace is entirely unaware that anything has happened.

**Time $t > 0$:** Segment 1 is now charged to 1.2V, but segment 2 remains at 0V. The voltage difference causes segment 1 to act as the local power source for segment 2. Electrons shift from segment 1 into segment 2. The local series inductance briefly resists this sudden movement, but charge transfers. Segment 2 charges, and an electric field forms beneath it, creating a local displacement current through the dielectric and a local magnetic field around the copper. Segment 2 then acts as the source for segment 3. Segment 3 charges segment 4.

This continuous, sequential charging of microscopic segments is the physical mechanism of electromagnetic wave propagation on a transmission line.

### The Three Zones of a Propagating Wavefront

Freezing time while the wavefront is halfway down the board reveals three distinct zones:

1. **Behind the wavefront:** The trace is fully charged to 1.2V. A static electric field holds steady between the trace and the ground plane, but the voltage is not changing. The conduction current in the trace is zero. The displacement current through the dielectric is zero. The transmission line acts like a charged capacitor holding a DC state.

2. **Ahead of the wavefront:** The trace is still at 0V. The voltage is not changing. The conduction current is zero. The displacement current is zero.

3. **Exactly at the wavefront:** The voltage is actively transitioning from 0V to 1.2V. Electrons are shifting to charge the local segment (conduction current). The electric field is growing, passing energy through the dielectric (displacement current). The current flows in a highly localized loop: forward on the trace to the wavefront, vertically through the dielectric as displacement current, and backward through the ground plane to the source. This entire active loop physically slides down the transmission line at the propagation velocity, carrying the signal with it.

### The Role of the Power Supply During Propagation

A critical physical detail: segment 1 does not simply dump its stored charge into segment 2 and go dead. Segment 1 remains continuously connected to the 1.2V power supply through the closed transistor switch. The power supply acts as a continuous, high-pressure source that forces charge into the trace at $d = 0$ to feed the propagating wavefront. Every segment behind the wavefront stays firmly pinned at 1.2V.

The forward direction of energy flow is maintained by the permanent voltage gradient. The driver at $d = 0$ is forcefully held at 1.2V, representing high potential energy. The uncharged trace ahead of the wavefront sits at 0V. Charge always flows from higher potential to lower potential. The electrical pressure behind the wavefront is 1.2V, and the pressure in front is 0V. A forward segment cannot transfer charge backward to a previous segment because the previous segment is held at a higher electrical potential by the continuous supply.

When the transmitter decides to send a logic "0," it disconnects the 1.2V rail and connects the trace to 0V ground. The high-pressure source is removed, a low-resistance path to ground is provided, and the built-up charge rushes out of the trace, discharging it segment by segment until the local electric field collapses.

### Conventional Current vs. Electron Motion

Operating a standard positive voltage rail (+1.2V) means the power supply is performing the exact opposite of "pushing electrons into the trace." Electrons carry negative charge. The copper trace naturally contains an equal number of protons and electrons, giving it a neutral 0V baseline. Creating a +1.2V potential on the trace requires the power supply to *strip electrons away* from the copper atoms and deposit them into the ground plane.

This removal of electrons creates a localized electron deficiency (a net positive charge) at $d = 0$. The propagating wavefront requires the power supply to continuously pull more electrons out of the trace at $d = 0$ so that each newly encountered segment reaches that same +1.2V state of electron deficiency.

Operating a negative voltage rail (-1.2V) reverses this: the power supply literally forces surplus electrons into the trace, creating a state of electron overdensity.

Electrical engineers typically use "conventional current" and state that "the power supply pushes charge into the trace" for a positive voltage. This is a historical mathematical convention established by Benjamin Franklin before the electron was discovered. The physical reality of the subatomic motion is always reversed for positive voltages. The core mechanical principle remains identical regardless of polarity: the power supply actively does physical work at $d = 0$ to alter the electron density of the copper, and it must continuously perform that work to keep the entire length of the transmission line fully charged behind the wavefront.

## Worked Examples

### Electrons, Drift Velocity, and Signal Speed

Electrons move through copper at a drift velocity measured in millimeters per second. The signal arrives at the far end of a trace in under a nanosecond. The resolution to this apparent paradox lies in the distinction between particle transport and wave transport.

The mathematical definition of current is:

$$I = n \cdot A \cdot q \cdot v_d$$

where $n$ is the electron density (number of free electrons per unit volume), $A$ is the cross-sectional area of the conductor, $q$ is the charge of one electron, and $v_d$ is the drift velocity. The electron density $n$ is a fixed physical property of the copper lattice (approximately $8.5 \times 10^{28}$ electrons per cubic meter). To increase current, the drift velocity $v_d$ increases. While this velocity remains extremely slow, copper contains an astronomical number of free electrons. A microscopic increase in collective drift velocity results in a massive increase in total coulombs passing a physical cross-section per second.

The copper trace is already packed completely full of free electrons. Applying the 1.2V potential at the driver exerts an electromotive force on the electrons at $d = 0$. These electrons physically drift into the neighboring segment, creating a cascading compression wave of charge density. An electron at $d = 0$ only needs to move a fraction of a micrometer to displace its neighbor, which displaces the next neighbor in line.

The signal is the electromagnetic wave traveling through the dielectric. The current is the localized shuffling of electrons facilitating that wave. The electrons leaving the transmitter are not the same electrons arriving at the receiver when the bit flips. The wave propagates through the dielectric at a fraction of the speed of light, locally perturbing the electron sea as it passes.

### Signal, Voltage, and Characteristic Impedance

The "signal" is the electromagnetic wave, and its driving force is the voltage (potential difference). The current is the resulting flow of charge. The relationship linking voltage to current in a traveling wave is the characteristic impedance:

$$Z_0 = \frac{V}{I}$$

A higher voltage pushes more current through a given transmission line geometry. This relationship holds strictly for the traveling wave; it does not describe the DC resistance of the copper.

### How Information Reaches the Receiver

Information is carried by the arrival time of wavefronts, not by the receiver interpreting the frequency content of each edge.

The receiver at the far end of the trace is essentially a voltmeter connected to a very fast, highly synchronized clock recovery circuit. A rising edge wavefront arrives, and the receiver's local voltage jumps from 0V to 1.2V. The clock ticks. The voltage is 1.2V. The receiver records a "1." The clock ticks again. The trace is still fully charged (the transmitter kept the pull-up transistor closed, so no falling edge has arrived). The voltage is still 1.2V. The receiver records a second "1." A falling edge wavefront arrives, discharging the trace back to 0V. The clock ticks. The voltage is 0V. The receiver records a "0."

The data is encoded purely in the time duration between wavefronts. The extreme high-frequency bandwidth discussed earlier is the physical mechanism required to make those wavefront edges steep and sharp. If the edges lacked that high-frequency content, they would be slow and sloped, and the receiver would struggle to identify the exact moment the transition crossed the threshold, leading to jitter and bit errors.

## Edge Cases

### The Telegrapher's Equations and the Full Impedance Model

The simplified characteristic impedance formula $Z_0 = \sqrt{L/C}$ assumes a lossless transmission line. The complete model, derived by Oliver Heaviside from the Telegrapher's Equations, accounts for losses in both the conductor and the dielectric:

$$Z_0 = \sqrt{\frac{R + j\omega L}{G + j\omega C}}$$

In this formulation, each infinitesimal slice of the transmission line contains four distributed parameters:

- **$R$** (series resistance): the DC and AC resistance of the conductor, including skin effect losses at high frequencies.
- **$L$** (series inductance): the self-inductance of the current loop formed by the trace and its return path on the ground plane.
- **$G$** (shunt conductance): the microscopic leakage current that flows through the dielectric insulator from the signal trace to the ground plane. $G$ is the exact mathematical inverse of resistance and accounts for dielectric loss.
- **$C$** (shunt capacitance): the parallel capacitance between the trace and the ground plane.

The series elements ($R$ and $L$) are in-line with the current path. They dictate the impedance that the physical current encounters while traveling along the conductor. The shunt elements ($G$ and $C$) are in parallel between the trace and the ground plane. They determine how much current leaks across the dielectric at each point along the line.

The formula $Z = R + j\omega L$ describes only the series impedance of a single conductor. It answers the question of which path the physical current will choose when multiple return paths are available (for example, when a signal crosses between reference planes). The ratio of all four distributed parameters ($R$, $L$, $G$, $C$) determines the characteristic impedance the propagating wave experiences as it travels down the line.

### Static Fields Between Transitions

Between edge transitions, no new frequency content propagates along the trace. The section of the trace that the wavefront has already passed acts like a charged capacitor holding a DC state. A static electric field exists between the trace and the ground plane (maintaining the 1.2V potential), but the voltage is not changing, so no displacement current flows, the magnetic field has collapsed, and no propagating electromagnetic wave exists at that location.

The trace remains in this static, charged state until the next wavefront arrives to discharge it. The high-frequency energy content of the signal is concentrated entirely within the rising and falling edges. The flat portions between edges carry only DC energy.
