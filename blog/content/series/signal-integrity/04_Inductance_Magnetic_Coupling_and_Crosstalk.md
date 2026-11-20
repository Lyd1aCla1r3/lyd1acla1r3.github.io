# Inductance, Magnetic Coupling, and Crosstalk

<!-- SUMMARY: A changing current creates a magnetic field that induces voltage across adjacent conductors. Mutual inductance and mutual capacitance govern near-end (NEXT) and far-end (FEXT) crosstalk signatures, explaining why FEXT scales with coupled length while NEXT saturates once the coupled delay exceeds half the rise time. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>

[Chapter 3](03_Impedance_Reflections_and_Termination.md) treated inductance $L$ as a circuit parameter that gives conducting electrons magnetic flywheel inertia and reflects high-frequency signal edges at impedance discontinuities. Electromagnetic field theory explains how conductor geometry creates that inductance and how the expanding magnetic field of one trace induces unwanted voltages across neighboring traces.

[Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) established that a transmission line stores electric field energy in the dielectric capacitance $C$ between the trace and the ground plane. The same transmission line stores magnetic field energy in the current loop formed by the outbound trace and the return path, which defines the distributed loop inductance $L$. The ratio and product of those two per-unit-length parameters set the characteristic impedance $Z_0$ and the wave propagation velocity $v_p$.

Magnetic induction separates into two distinct physical mechanisms depending on which conductor experiences the changing magnetic flux. Self-inductance describes the opposing voltage that a conductor's own changing magnetic field induces against changes in its own current. Mutual inductance describes magnetic coupling between two conductors, where the changing magnetic field of one current path induces a voltage across a second path. Both mechanisms act simultaneously inside every PCB transmission line and across every pair of adjacent traces.

The sections below build the physics in sequence from Ampère's law and conductor field geometry to Faraday's and Lenz's laws, the two right-hand rules, the four physical cases of induction, total loop inductance, and coupled-line crosstalk.

## Core Concepts

### The Magnetic Field of a Current: Ampère's Law and the Generation Rule

Stationary electric charges produce only an electric field, whereas moving electric charges generate a circulating magnetic field in the surrounding space. The total magnetic field around any copper conductor is the vector superposition of the individual magnetic fields created by all moving electrons inside the metal.

A right-hand procedure, termed the **Generation Rule** throughout this series, gives the spatial direction of the magnetic field from a known current direction. Pointing the thumb of the right hand along the direction of conventional positive current causes the curled fingers of the right hand to point along the circulating magnetic field lines encircling the conductor.

Electromagnetics distinguishes two vector quantities at every point in space to separate the current-driven cause from the material-dependent result:

- **Magnetic field intensity $\vec{H}$ (in amperes per meter, $\text{A/m}$):** The geometric driving effort produced purely by the electric current $I$ and the path geometry, independent of the surrounding medium. Magnetic field intensity $\vec{H}$ pairs with the electric field $\vec{E}$ (in $\text{V/m}$) in the Poynting vector $\vec{S}$ of [Chapter 3](03_Impedance_Reflections_and_Termination.md).
- **Magnetic flux density $\vec{B}$ (in teslas, $\text{T}$, or milliteslas, where $1\text{ mT}$ equals $10^{-3}\text{ T}$):** The resulting concentration of magnetic field lines per unit area at a specific point after the surrounding material responds to $\vec{H}$. One tesla equals one weber per square meter ($\text{Wb/m}^2$) or one volt-second per square meter ($\text{V}\cdot\text{s/m}^2$).

The medium's total magnetic permeability $\mu$ from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) relates the local magnetic flux density $\vec{B}$ to the magnetic field intensity $\vec{H}$:

$$\vec{B} = \mu \vec{H} = \mu_0 \mu_r \vec{H}$$

Here $\mu_r$ is the dimensionless relative permeability of the material, and $\mu_0$ is the magnetic permeability of free space (expressed in henries per meter, $\text{H/m}$, or equivalently tesla-meters per ampere, $\text{T}\cdot\text{m/A}$):

$$\mu_0 = 4\pi \times 10^{-7}\text{ H/m} = 4\pi \times 10^{-7}\text{ T}\cdot\text{m/A}$$

Ferromagnetic materials such as iron or ferrite align their internal atomic domains with $\vec{H}$ to amplify the flux density by relative permeabilities $\mu_r$ of $10^2$ to $10^4$. Copper, air, vacuum, and PCB dielectrics such as FR4 are non-magnetic ($\mu_r$ equal to $1$), so $\vec{B}$ and $\vec{H}$ share the same spatial distribution everywhere on a circuit board and differ only by the constant $\mu_0$:

$$\vec{B} = \mu_0 \vec{H}$$

In its pure geometric form, Ampère's law states that the line integral of $\vec{H}$ around any closed loop equals the net conduction current $I_{\text{enc}}$ (in amperes, $\text{A}$) enclosed by that loop. Multiplying both sides by $\mu_0$ writes Ampère's law in terms of the magnetic flux density $\vec{B}$:

$$\oint \vec{H} \cdot d\vec{\ell} = I_{\text{enc}} \qquad \Longleftrightarrow \qquad \oint \vec{B} \cdot d\vec{\ell} = \mu_0 I_{\text{enc}}$$

#### External Magnetic Field of a Cylindrical Wire

Consider a long, straight cylindrical wire of radius $a$ carrying a steady current $I$. By circular symmetry around the wire axis, every point on a concentric circle of radius $r > a$ outside the wire experiences the same magnetic field magnitude $B(r)$ directed tangentially along the circle.

The vector $\vec{B}$ is everywhere parallel to the circular path and constant in magnitude at fixed radius $r$, so the line integral in Ampère's law simplifies to the field magnitude $B(r)$ multiplied by the circle circumference $2\pi r$. A circle outside the wire ($r > a$) encloses the entire wire cross-section, setting the enclosed current $I_{\text{enc}}$ equal to the full wire current $I$:

$$\oint \vec{B} \cdot d\vec{\ell} = B(r)\,(2\pi r) = \mu_0 I$$

Dividing both sides by the circumference $2\pi r$ gives the magnetic flux density outside a straight cylindrical wire ($r \ge a$):

$$B(r) = \frac{\mu_0 I}{2\pi r}$$

Moving farther away from the wire in the surrounding space does not change the enclosed current $I$, while the circular path length $2\pi r$ stretches proportionally with $r$. The external magnetic field therefore weakens in inverse proportion to the radial distance $r$.

#### Uniform Magnetic Field of a Wide Current Sheet

A wide, flat copper reference plane shapes the magnetic field into a completely different spatial pattern through vector superposition. Consider a horizontal copper plane of width $W_{\text{plane}}$ and vertical foil thickness $t_{\text{Cu}}$ carrying a uniform current $I$ across its two-dimensional cross-sectional area $A_{\text{plane}}$. Inside the copper foil, dividing current $I$ by $A_{\text{plane}}$ defines the cross-sectional current density $J$ (in amperes per square meter, $\text{A/m}^2$):

$$A_{\text{plane}} = W_{\text{plane}}\,t_{\text{Cu}}, \qquad J = \frac{I}{A_{\text{plane}}} = \frac{I}{W_{\text{plane}}\,t_{\text{Cu}}}$$

Above any observation point on the plane, narrow current strips located at equal horizontal distances to the left and right produce magnetic field vectors whose vertical components point in opposite directions and cancel, while their horizontal components parallel to the plane point in the same direction and add. Summing across the full width of the sheet eliminates the vertical field component and leaves a uniform horizontal magnetic field parallel to the copper surface, pointing in opposite directions above and below the plane.

To find the magnitude of that external horizontal field, apply Ampère's law around a rectangular loop of horizontal width $w$ whose top and bottom legs sit outside the copper foil, straddling the entire vertical thickness $t_{\text{Cu}}$. Multiplying the area current density $J$ by the enclosed copper cross-sectional area $A_{\text{enc}}$ of $w\,t_{\text{Cu}}$ cancels the foil thickness $t_{\text{Cu}}$:

$$I_{\text{enc}} = J\,A_{\text{enc}} = \left(\frac{I}{W_{\text{plane}}\,t_{\text{Cu}}}\right)(w\,t_{\text{Cu}}) = \left(\frac{I}{W_{\text{plane}}}\right)w$$

That cancellation occurs because any loop outside the copper plane encloses $100\%$ of the vertical thickness $t_{\text{Cu}}$, just as a circle outside a cylindrical wire ($r \ge a$) encloses $100\%$ of the wire radius $a$. Electromagnetics defines the product $J\,t_{\text{Cu}}$ as the **sheet (or linear) current density** $K$ (in amperes per meter of width, $\text{A/m}$):

$$K = J\,t_{\text{Cu}} = \frac{I}{W_{\text{plane}}}$$

Substituting the enclosed current $K\,w$ along the two horizontal path segments of length $w$ (above and below the plane) into Ampère's law gives:

$$B\,(2w) = \mu_0 I_{\text{enc}} = \mu_0 (K\,w)$$

Dividing both sides by $2w$ cancels the loop width $w$ and gives the magnetic flux density on either side of a wide current sheet:

$$B = \frac{\mu_0 K}{2} = \frac{\mu_0 I}{2 W_{\text{plane}}}$$

Individual moving electrons obey the same physical law in both conductors. Cross-sectional geometry determines which vector components cancel and which reinforce: a narrow wire concentrates magnetic field lines into tight circles that decay as $1/r$, whereas a wide ground plane spreads the field into a uniform sheet parallel to the copper surface.

### The Magnetic Field Inside and Outside a Solid Conductor

#### One Hollow Copper Ring: Cancellation Inside, Constructive Field Outside

To see how a solid wire builds its internal magnetic field, start with a single infinitely thin hollow copper ring of radius $\rho$ and wall thickness $d\rho$ carrying current straight out of the page ($\odot$). By the Generation Rule (right-hand thumb pointing out of the page), the current filament at $12\text{ o'clock}$ creates a counter-clockwise circular magnetic field that points to the **right** ($\rightarrow$) below $12\text{ o'clock}$ (inside the ring) and to the **left** ($\leftarrow$) above $12\text{ o'clock}$ (outside the ring). The opposite filament at $6\text{ o'clock}$ creates a counter-clockwise circular field that points to the **left** ($\leftarrow$) above $6\text{ o'clock}$ (inside the ring) and to the **right** ($\rightarrow$) below $6\text{ o'clock}$ (outside the ring).

Inside the hollow ring ($r < \rho$), every observation point $P$ sits between opposite walls whose magnetic fields point in opposite directions ($\rightarrow$ versus $\leftarrow$). Even when $P$ lies off-center, closer to the top wall at distance $d_1$ than to the bottom wall at distance $d_2$, drawing two opposite cones of narrow angle $d\theta$ through $P$ cuts a short near copper arc of length $d_1\,d\theta$ and a wide far copper arc of length $d_2\,d\theta$. The far arc is $d_2 / d_1$ times wider and carries $d_2 / d_1$ times more current, which cancels its greater distance in the wire field law ($\Delta I / d$) so that opposite arcs cancel pair by pair around all $360^\circ$:

$$dB_{\text{ring}}(r) = 0, \qquad \text{for } r < \rho$$

Outside the hollow ring ($r \ge \rho$), the magnetic field circle from the far side reaches across the ring diameter to the exterior observation point. Both the $12\text{ o'clock}$ and $6\text{ o'clock}$ filaments now lie on the same side of the observation point and push the magnetic field in the **same counter-clockwise direction**. The ring adds no current past its own radius $\rho$ in either surrounding air or surrounding outer copper; it contributes only the current $dI(\rho)$ flowing in its own circumference, and its field strength diminishes inversely with the observation radius $r$:

$$dB_{\text{ring}}(r) = \frac{\mu_0\,dI(\rho)}{2\pi r}, \qquad \text{for } r \ge \rho$$

#### Building a Solid Wire from Nested Concentric Rings

A solid cylindrical copper wire of outer radius $a$ is an infinite series of infinitely thin concentric copper rings of radius $\rho$ nested from the center axis (zero $\rho$) to the outer surface ($\rho$ equal to $a$). Under a steady DC current $I$ distributed uniformly across the total wire area $\pi a^2$, the constant current per unit area is the current density $J$ (in $\text{A/m}^2$):

$$J = \frac{I}{\pi a^2}$$

Each thin concentric ring at radius $\rho$ with thickness $d\rho$ has a copper strip area equal to its circumference $2\pi\rho$ multiplied by $d\rho$, so the current $dI(\rho)$ generated by that single ring is proportional to its circumference:

$$dI(\rho) = J\,(2\pi\rho\,d\rho)$$

At an interior observation radius $r < a$ inside the solid copper wire, every outer ring larger than $r$ ($r < \rho \le a$) surrounds the observation point and cancels itself to zero. Every inner ring smaller than $r$ ($0 \le \rho \le r$) sits inside the observation circle and sends its constructive magnetic field outward to radius $r$.

Each inner ring is counted **only once**, evaluated at the single observation radius $r$ where the field is measured. Summing the field contributions at observation radius $r$ from all inner rings (from zero $\rho$ to $r$) factors out the common observation-point denominator $2\pi r$ and integrates the inner ring circumferences $2\pi\rho\,d\rho$:

$$B(r) = \int_{\rho = 0}^{\rho = r} \frac{\mu_0\,dI(\rho)}{2\pi r} = \frac{\mu_0\,J}{2\pi r}\int_{\rho = 0}^{\rho = r} 2\pi\rho\,d\rho$$

Adding the circumferences $2\pi\rho\,d\rho$ of all concentric rings from zero $\rho$ to $r$ builds the circular cross-sectional area $\pi r^2$ of the interior disk, which encloses current $I_{\text{enc}}(r)$:

$$\int_{\rho = 0}^{\rho = r} 2\pi\rho\,d\rho = \pi r^2 \qquad \Longrightarrow \qquad I_{\text{enc}}(r) = J\,(\pi r^2) = \left(\frac{I}{\pi a^2}\right)(\pi r^2) = I\,\frac{r^2}{a^2}$$

Replacing the integral of the circumferences with the enclosed area $\pi r^2$ and enclosed current $I_{\text{enc}}(r)$ reproduces Ampère's law for a circular path of radius $r$:

$$B(r)\,(2\pi r) = \mu_0 I_{\text{enc}}(r) = \mu_0 I\,\frac{r^2}{a^2}$$

Dividing both sides by the observation circumference $2\pi r$ gives the internal magnetic flux density inside the solid wire ($0 \le r \le a$):

$$B(r) = \frac{\mu_0 I\, r}{2\pi a^2}$$

Evaluating this internal expression at the outer copper surface ($r$ equal to $a$) where the internal linear rise meets the external $1/r$ decay gives the peak surface magnetic flux density $B(a)$:

$$B(a) = \frac{\mu_0 I\, a}{2\pi a^2} = \frac{\mu_0 I}{2\pi a}$$

#### Comparing the Four Radial Zones Across Interior, Surface, and Exterior Radii

Two competing geometric factors (the enclosed current $I_{\text{enc}}(r)$ in the numerator and the observation circumference $2\pi r$ in the denominator) govern the field across the four radial zones:

- **At the center axis (zero $r$):** Zero concentric rings sit inside the center axis (zero $I_{\text{enc}}$), and all surrounding rings cancel at the center, leaving zero $B(0)$.
- **Inside the copper wire ($0 < r < a$):** Stepping outward adds new inner rings whose cumulative area $\pi r^2$ grows as $r^2$ while the observation circumference $2\pi r$ grows only as $r$. Area growth outpaces circumference stretching by the factor $r^2 / r$, so the internal magnetic field rises **linearly** with radius $r$.
- **At the copper surface ($r$ equal to $a$):** All concentric rings across the full radius $a$ contribute constructively ($I_{\text{enc}}$ equal to $I$) at the smallest radius containing the full wire, so the magnetic field reaches its **maximum strength** at the copper surface.
- **Outside the copper wire ($r > a$):** Stepping beyond the wire surface into the surrounding air adds **zero new rings** and zero new current ($I_{\text{enc}}$ stays fixed at $I$). Increasing the observation radius $r$ stretches the denominator $2\pi r$ around that constant current, so the external field decays **inversely** with distance ($1/r$).

This uniform DC current distribution holds for steady currents; at high frequencies, time-varying internal fields push current toward the outer skin ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)).

#### Numerical Walkthrough Across Interior, Surface, and Exterior Radii

Consider a solid copper wire of outer radius $a$ equal to $0.1\text{ mm}$ ($1.0 \times 10^{-4}\text{ m}$) carrying a steady current $I$ of $1.0\text{ A}$ in free space ($\mu_0$ of $4\pi \times 10^{-7}\text{ T}\cdot\text{m/A}$).

First, evaluate the field at the copper surface ($r$ equal to $a$, or $1.0 \times 10^{-4}\text{ m}$), where all concentric rings contribute the full $1.0\text{ A}$ current at minimum circumference. Substituting $\mu_0$, $I$, and $a$ into the surface field equation gives the peak magnetic flux density in teslas and milliteslas:

$$B(a) = \frac{\mu_0 I}{2\pi a} = \frac{(4\pi \times 10^{-7}\text{ T}\cdot\text{m/A})(1.0\text{ A})}{2\pi (1.0 \times 10^{-4}\text{ m})}$$

$$B(a) = \frac{2.0 \times 10^{-7}\text{ T}\cdot\text{m}}{1.0 \times 10^{-4}\text{ m}} = 2.0 \times 10^{-3}\text{ T} = 2.0\text{ mT}$$

Second, evaluate the field inside the copper halfway from the center axis to the surface ($r$ of $0.05\text{ mm}$, equal to $0.5\,a$). The inner rings inside $0.5\,a$ span one-quarter of the cross-sectional area ($I_{\text{enc}}$ of $0.25\text{ A}$) along one-half of the surface circumference, yielding half of the surface peak:

$$B(0.05\text{ mm}) = \frac{\mu_0 I\, r}{2\pi a^2} = \left(\frac{\mu_0 I}{2\pi a}\right)\left(\frac{r}{a}\right) = (2.0\text{ mT})\left(\frac{0.05\text{ mm}}{0.10\text{ mm}}\right) = 1.0\text{ mT}$$

Third, evaluate the field outside the wire at a radius ten times the wire radius ($r$ of $1.0\text{ mm}$, equal to $10\,a$). Zero additional current enters beyond radius $a$ ($I_{\text{enc}}$ remains $1.0\text{ A}$) while the observation circumference is ten times larger than at the surface, reducing the magnetic flux density to one-tenth of its surface peak:

$$B(1.0\text{ mm}) = \frac{\mu_0 I}{2\pi r} = \left(\frac{\mu_0 I}{2\pi a}\right)\left(\frac{a}{r}\right) = (2.0\text{ mT})\left(\frac{0.10\text{ mm}}{1.0\text{ mm}}\right) = 0.2\text{ mT}$$

### Faraday's Law, Lenz's Law, and Ampère's Law as Three Distinct Principles

Electromagnetic induction involves three distinct physical laws that govern current, magnetic flux, and induced voltage. Keeping cause and effect separate in each law prevents directional sign errors.

#### Principle 1: Ampère's Law (Current Generates Magnetic Field)

Electric current is the physical cause, and a circulating magnetic field is the physical effect. Charge flowing along a conductor surrounds the current path with a magnetic flux density $\vec{B}$ whose direction follows the Generation Rule and whose magnitude obeys Ampère's law.

#### Principle 2: Faraday's Law (Changing Magnetic Flux Induces Voltage)

Magnetic flux density $\vec{B}$ (in $\text{T}$ or $\text{Wb/m}^2$) measures the local concentration of magnetic field lines **per unit area at a single point**. By contrast, **magnetic flux** $\Phi_B$ measures the **total amount of magnetic field** passing through an entire two-dimensional surface of area $A$, such as the rectangular dielectric window between a signal trace and its ground plane. Magnetic flux $\Phi_B$ is measured in **webers** ($\text{Wb}$, equal to $\text{T}\cdot\text{m}^2$ or volt-seconds, $\text{V}\cdot\text{s}$) and is found by integrating the normal component of $\vec{B}$ across the surface area $A$:

$$\Phi_B = \iint_A \vec{B} \cdot d\vec{A}$$

For a uniform magnetic flux density $B$ passing perpendicularly through a flat window of area $A$, that surface integral simplifies to the product of flux density and area:

$$\Phi_B = B\,A$$

Faraday's law states that a time-varying total magnetic flux $\Phi_B(t)$ enclosed by a loop is the physical cause, and an induced electromotive force $\mathcal{E}(t)$ (loop voltage, in volts) around that loop is the physical effect. A steady magnetic field whose enclosed flux $\Phi_B$ does not change with time induces zero voltage, regardless of how strong the static flux density $\vec{B}$ is.

#### Principle 3: Lenz's Law (Induced Polarity Opposes the Flux Change)

Conservation of energy requires that the voltage induced by a changing magnetic flux always takes the polarity that opposes the flux change that created it. Combining Faraday's rate-of-change magnitude with Lenz's opposing minus sign yields the Faraday-Lenz law of induction:

$$\mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt}$$

An increasing magnetic flux $\Phi_B(t)$ through a closed conducting loop induces an electromotive force $\mathcal{E}(t)$ that drives a secondary current whose own magnetic field points opposite to the primary field to resist the increase. A decreasing primary magnetic flux drives an induced current in the opposite direction to reinforce the primary field and resist the decay.

### The Reaction Rule

Finding the direction of an induced current from Lenz's law requires a three-step right-hand procedure that is distinct from the Generation Rule. This series calls this three-step sequence the **Reaction Rule**:

1. **Primary field evaluation:** Apply the Generation Rule to the primary current to identify the spatial direction of the existing magnetic field $\vec{B}_{\text{primary}}$ passing through the target loop, and identify an increasing versus decreasing flux magnitude over time.
2. **Opposing field alignment:** Establish the direction of the induced opposing magnetic field $\vec{B}_{\text{induced}}$ required by Lenz's law, pointing opposite to $\vec{B}_{\text{primary}}$ when the primary flux is growing and parallel to $\vec{B}_{\text{primary}}$ when the primary flux is shrinking.
3. **Induced current readout:** Around a **straight wire**, curl the right-hand **fingers** along the concentric circles of $\vec{B}_{\text{induced}}$ and read the straight induced current direction from the right-hand **thumb**. Inside a **single flat loop window** where $\vec{B}_{\text{induced}}$ points in one direction, point the **thumb** along $\vec{B}_{\text{induced}}$ and read the loop current from the **fingers**.

The Generation Rule and the Reaction Rule must never be blended into a single hand motion. The Generation Rule starts from a known current and finds the magnetic field it creates. The Reaction Rule starts from a changing magnetic flux, determines the opposing magnetic field required to fight that change, and reads out the induced current that generates that opposing field.

Why does Step 3 sometimes place the **thumb** along the induced current and other times along the opposing magnetic field? On a human hand, the **thumb is a straight line** and the **fingers curl in a circle**. In every electromagnetic geometry, whichever physical quantity travels in a **straight line** gets the **straight thumb**, and whichever physical quantity wraps in a **circle or closed loop** gets the **curled fingers**:

| Geometry Under Inspection | Quantity Moving in a Straight Line (**Straight Thumb**) | Quantity Wrapping in a Circle or Loop (**Curled Fingers**) | When to Use This Orientation |
|---|---|---|---|
| **Orientation A: Straight-Wire View** (a straight trace surrounded by concentric circles of $\vec{B}$) | **Current or back-EMF** along the straight wire ($\rightarrow$ or $\leftarrow$) | **Magnetic field $\vec{B}$** wrapping in concentric circles around the wire ($\odot$ on one side, $\otimes$ on the other) | Whenever inspecting a **straight wire or PCB trace** where $\vec{B}$ forms concentric circles around the conductor (`Case 2` self-inductance and straight-trace crosstalk). |
| **Orientation B: Closed-Loop Window View** (a rectangular loop or coil with $\vec{B}$ piercing the window) | **Magnetic field $\vec{B}$** poking straight through the loop window ($\otimes$ or $\odot$) | **Current or back-EMF** circulating around the closed loop perimeter ($\circlearrowright$ or $\circlearrowleft$) | Whenever inspecting a **single closed loop window** on one side of a wire where $\vec{B}$ points in one single straight direction through the window (`Case 3` loop view). |

On straight parallel PCB traces, both orientations always yield the same induced current direction along the copper trace, so either orientation can be used.

### The Four Physical Cases of Magnetic Induction

Four physical scenarios classify all interactions between currents, conductors, and magnetic fields:

| Case | Conductor and Field State | Flux Rate | Physical Mechanism and Signal Integrity Role |
|---|---|---|---|
| **Case 1: Steady isolated current** | Constant DC current in a single stationary conductor | $\frac{d\Phi_B}{dt} = 0$ | Static magnetic field induces zero voltage; conductor exhibits only DC resistance. |
| **Case 2: Changing isolated current** | Time-varying current $i(t)$ in a single conductor | $\frac{d\Phi_{\text{self}}}{dt} \neq 0$ | Changing self-flux induces a back-EMF that opposes current changes (self-inductance $L$) and drives the high-frequency skin effect ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)). |
| **Case 3: Changing current near a neighbor** | Time-varying current $i_1(t)$ in conductor 1 coupling into conductor 2 | $\frac{d\Phi_{21}}{dt} \neq 0$ | Changing magnetic field from the aggressor passes through the victim loop window and induces mutual voltage (mutual inductance $M$), producing inductive crosstalk. |
| **Case 4: Moving conductor in static field** | Conductor moving mechanically through a stationary magnetic field | Motional Lorentz force | Mechanical motion cuts field lines to generate motional EMF in motors and generators; absent in stationary PCB interconnects. |

Case 2 and Case 3 operate simultaneously whenever multiple conductors carry high-speed signals on a circuit board. Every conductor reacts to the changing magnetic field of its own current (Case 2) while simultaneously reacting to the changing magnetic fields of neighboring currents (Case 3). By the linearity of Maxwell's equations, the induced voltages superpose directly on top of any signal already traveling on the victim conductor.

### Self-Inductance and Mutual Inductance Defined

#### Deriving Flux-Current Linearity from Ampère's Law and the Flux Integral

To see where the linear relationship between magnetic flux $\Phi_B(t)$ and current $i(t)$ comes from, substitute the magnetic flux density $B(r, t)$ from Ampère's law directly into the surface flux integral across the two-dimensional dielectric window of area $A$ between an outbound conductor and its return path:

$$\Phi_B(t) = \iint_A \vec{B}(t) \cdot d\vec{A}$$

First, evaluate this integral for a cylindrical wire of radius $a$ and length $\ell$ whose return path sits at radial distance $d$. Outside the wire ($a \le r \le d$), Ampère's law gives a magnetic flux density $B(r, t)$ that is proportional to $i(t)$ and inversely proportional to radius $r$:

$$B(r, t) = \frac{\mu_0\,i(t)}{2\pi r}$$

The rectangular dielectric window from inner radius $a$ to outer radius $d$ has length $\ell$ along the wire, so each thin radial strip of width $dr$ and length $\ell$ has differential area $dA$ equal to $\ell\,dr$. Substituting $B(r, t)$ and $\ell\,dr$ into the flux integral allows the time-varying current $i(t)$ (which depends only on time $t$, not on radius $r$) to factor completely outside the spatial integral:

$$\Phi_B(t) = \int_{r = a}^{r = d} B(r, t)\,\ell\,dr = \int_{r = a}^{r = d} \left(\frac{\mu_0\,i(t)}{2\pi r}\right)\ell\,dr = \left(\frac{\mu_0\,\ell}{2\pi}\int_{r = a}^{r = d} \frac{dr}{r}\right)i(t)$$

Evaluating the spatial integral of $1/r$ from $a$ to $d$ yields $\ln(d/a)$, expressing the total enclosed flux $\Phi_B(t)$ as a purely geometric constant multiplied by the current $i(t)$:

$$\Phi_B(t) = \underbrace{\left[\frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{d}{a}\right)\right]}_{L}\,i(t)$$

Second, evaluate the same flux integral for a wide parallel-plate transmission line of trace width $w$, length $\ell$, and dielectric thickness $h$ ($w \gg h$). An outbound current $+i(t)$ on the top plate and an equal return current $-i(t)$ on the bottom plate each carry a surface current density $K(t)$ equal to $i(t)/w$. Between the plates, the two horizontal magnetic fields of magnitude $\frac{\mu_0 K(t)}{2}$ point in the same direction and add constructively to produce a uniform magnetic flux density $B(t)$ across the gap:

$$B(t) = \frac{\mu_0 K(t)}{2} + \frac{\mu_0 K(t)}{2} = \mu_0 K(t) = \frac{\mu_0\,i(t)}{w}$$

Integrating that uniform flux density across the rectangular dielectric window of height $h$ and length $\ell$ (area $A$ equal to $h\,\ell$) again factors the current $i(t)$ outside the geometry:

$$\Phi_B(t) = \int_{y = 0}^{y = h} B(t)\,\ell\,dy = B(t)\,(h\,\ell) = \underbrace{\left(\frac{\mu_0\,h\,\ell}{w}\right)}_{L}\,i(t)$$

In every linear, non-magnetic conductor geometry ($\mu_r$ equal to $1$), the current $i(t)$ factors out of the spatial surface integral in the same way. Doubling the current $i(t)$ doubles the local flux density $\vec{B}(t)$ at every point in the window, which doubles the total flux $\Phi_B(t)$. The ratio of total enclosed magnetic flux $\Phi_B(t)$ to current $i(t)$ is therefore a constant determined strictly by the permeability $\mu_0$ and the conductor loop geometry, defined as the **inductance** $L$:

$$\Phi_B(t) = L\,i(t) \qquad \Longleftrightarrow \qquad L = \frac{\Phi_B(t)}{i(t)}$$

Inductance $L$ is measured in **henries** ($\text{H}$, equal to webers per ampere, $\text{Wb/A}$, or volt-seconds per ampere, $\text{V}\cdot\text{s/A}$).

#### How the Cylindrical and Parallel-Plate Inductance Formulas Connect

The cylindrical inductance formula and the parallel-plate inductance formula look different at first glance, yet they are two geometric limits of the same law:

$$L_{\text{cyl}} = \frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{d}{a}\right), \qquad L_{\text{plate}} = \frac{\mu_0\,h\,\ell}{w}$$

To see how one transforms into the other, take the flat parallel-plate line of width $w$, length $\ell$, and thin dielectric gap $h$, and roll it into a coaxial cylinder of inner radius $a$ and outer return radius $d$:

1. **Trace width becomes cylinder circumference:** Rolling the flat strip of width $w$ into a closed circle of radius $a$ sets the circumference $2\pi a$ equal to the width $w$:

$$w = 2\pi a$$

2. **Dielectric thickness sets the outer radius:** The return plane sits a radial distance $h$ outside the inner conductor surface of radius $a$, setting the outer return radius $d$ to $a + h$:

$$d = a + h \qquad \Longrightarrow \qquad \frac{d}{a} = 1 + \frac{h}{a}$$

Substituting this radius ratio into the cylindrical inductance formula gives:

$$L_{\text{cyl}} = \frac{\mu_0\,\ell}{2\pi}\ln\!\left(1 + \frac{h}{a}\right)$$

For a dielectric gap $h$ that is much thinner than the cylinder radius $a$ ($h \ll a$), the circular magnetic path circumference $2\pi r$ barely changes between the inner radius $a$ and the outer radius $a + h$, so the $1/r$ variation of the magnetic field across the gap flattens into a nearly uniform field. Mathematically, the first-order Taylor series expansion of the natural logarithm for a small ratio $\frac{h}{a} \ll 1$ replaces $\ln\!\left(1 + \frac{h}{a}\right)$ with $\frac{h}{a}$:

$$\ln\!\left(1 + \frac{h}{a}\right) = \frac{h}{a} - \frac{1}{2}\left(\frac{h}{a}\right)^2 + \cdots \approx \frac{h}{a}, \qquad \text{for } h \ll a$$

Replacing $\ln\!\left(1 + \frac{h}{a}\right)$ with $\frac{h}{a}$ and substituting the trace width $w$ for the circumference $2\pi a$ reduces the cylindrical formula directly to the parallel-plate formula:

$$L_{\text{cyl}} \approx \frac{\mu_0\,\ell}{2\pi}\left(\frac{h}{a}\right) = \frac{\mu_0\,h\,\ell}{2\pi a} = \frac{\mu_0\,h\,\ell}{w} = L_{\text{plate}}$$

The natural logarithm $\ln(d/a)$ appears whenever the return path sits far enough away ($d$ comparable to or larger than $a$) that the magnetic path circumference $2\pi r$ expands appreciably across the dielectric window, causing $B(r)$ to decay as $1/r$. A dielectric thickness $h$ that is small compared to the conductor width $w$ keeps the magnetic path length constant at $w$ across the entire gap $h$, so the logarithmic integral collapses to the ratio $h/w$.

#### Self-Induced Voltage from Self-Inductance ($L$)

Recall the Faraday-Lenz law relating induced electromotive force $\mathcal{E}(t)$ to the time derivative of enclosed magnetic flux:

$$\mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt}$$

Replacing $\Phi_B(t)$ with $L\,i(t)$ for a stationary conductor geometry (where $L$ is constant in time) gives the self-induced back-EMF $\mathcal{E}_{\text{self}}(t)$:

$$\mathcal{E}_{\text{self}}(t) = -\frac{d}{dt}\bigl[L\,i(t)\bigr] = -L\,\frac{di(t)}{dt}$$

An external voltage source driving a changing current $i(t)$ through the inductor terminals must supply a forward terminal voltage $v_L(t)$ equal and opposite to $\mathcal{E}_{\text{self}}(t)$ to overcome this opposing back-EMF. Reversing the sign from internal back-EMF to applied terminal voltage gives the standard circuit voltage-current relation for an inductor used in [Chapter 3](03_Impedance_Reflections_and_Termination.md):

$$v_L(t) = -\mathcal{E}_{\text{self}}(t) = L\,\frac{di(t)}{dt}$$

#### Coupled Flux and Induced Voltage from Mutual Inductance ($M$)

Self-inductance $L$ tracks how a single loop reacts to its own magnetic field. **Mutual inductance** $M$ tracks the same four-step physical chain across **two neighboring loops**:

- **Loop 1 (source or aggressor loop):** Carries a time-varying current $i_1(t)$ and radiates a magnetic flux density $\vec{B}_1(r, t)$ into the surrounding space.
- **Loop 2 (neighboring or victim loop):** Sits nearby with its own rectangular dielectric window of surface area $A_2$.
- **Double-subscript convention ($21$):** Names the **target loop experiencing the effect** first ($2$) and the **source loop causing it** second ($1$), reading $\Phi_{21}(t)$ as *"magnetic flux in Loop 2 from Loop 1"* and $\mathcal{E}_{21}(t)$ as *"voltage induced in Loop 2 from Loop 1"*.

Walking through the four steps one equation at a time shows how $M$ and $\mathcal{E}_{21}(t)$ emerge directly from Ampère's law and Faraday's law:

1. **Current $i_1(t)$ in Loop 1 creates magnetic flux density $B_1(r, t)$ at Loop 2:** At any radial distance $r$ from Wire 1, Ampère's law gives the magnetic flux density produced by Loop 1's current:

$$B_1(r, t) = \frac{\mu_0\,i_1(t)}{2\pi r}$$

2. **Loop 2's window area $A_2$ intercepts part of that field as shared flux $\Phi_{21}(t)$:** Suppose window $A_2$ of length $\ell$ spans from radial distance $r_{\text{near}}$ to radial distance $r_{\text{far}}$ from Wire 1. Integrating Wire 1's field $B_1(r, t)$ across thin strips of differential area $dA_2$ equal to $\ell\,dr$ factors $i_1(t)$ outside the spatial integral:

$$\Phi_{21}(t) = \iint_{A_2} \vec{B}_1(r, t) \cdot d\vec{A}_2 = \int_{r = r_{\text{near}}}^{r = r_{\text{far}}} \left(\frac{\mu_0\,i_1(t)}{2\pi r}\right)\ell\,dr$$

$$\Phi_{21}(t) = \underbrace{\left[\frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{r_{\text{far}}}{r_{\text{near}}}\right)\right]}_{M}\,i_1(t)$$

3. **Factoring out $i_1(t)$ defines the mutual inductance $M$:** The bracketed spatial integral depends strictly on the permeability $\mu_0$ and the relative geometry of the two loops. Naming that geometric constant the **mutual inductance** $M$ (measured in henries, $\text{H}$, or $\text{Wb/A}$) relates the shared magnetic flux in Loop 2 to the current in Loop 1:

$$\Phi_{21}(t) = M\,i_1(t) \qquad \Longleftrightarrow \qquad M = \frac{\Phi_{21}(t)}{i_1(t)}$$

4. **Changing current $i_1(t)$ in Loop 1 induces voltage $\mathcal{E}_{21}(t)$ around Loop 2:** Recall the Faraday-Lenz law applied to the shared magnetic flux $\Phi_{21}(t)$ passing through Loop 2:

$$\mathcal{E}_{21}(t) = -\frac{d\Phi_{21}(t)}{dt}$$

Replacing $\Phi_{21}(t)$ with $M\,i_1(t)$ gives the open-circuit electromotive force $\mathcal{E}_{21}(t)$ induced around Loop 2 by a time-varying current in Loop 1:

$$\mathcal{E}_{21}(t) = -\frac{d}{dt}\bigl[M\,i_1(t)\bigr] = -M\,\frac{di_1(t)}{dt}$$

Comparing every symbol side by side highlights the one-to-one parallel between self-inductance and mutual inductance:

| Physical Quantity | Self-Inductance ($L$, Single Loop) | Mutual Inductance ($M$, Loop 1 into Loop 2) | SI Unit |
|---|---|---|---|
| **Driving current (cause)** | $i(t)$ in the loop | $i_1(t)$ in Loop 1 (source) | $\text{A}$ |
| **Magnetic flux density generated** | $\vec{B}(r, t)$ from $i(t)$ | $\vec{B}_1(r, t)$ from $i_1(t)$ | $\text{T}$ ($\text{Wb/m}^2$) |
| **Window area intercepting the field** | Own loop window $A$ | Neighboring Loop 2 window $A_2$ | $\text{m}^2$ |
| **Total enclosed magnetic flux** | $\Phi_B(t) = L\,i(t)$ | $\Phi_{21}(t) = M\,i_1(t)$ | $\text{Wb}$ ($\text{V}\cdot\text{s}$) |
| **Geometric inductance constant** | $L = \frac{\Phi_B(t)}{i(t)}$ | $M = \frac{\Phi_{21}(t)}{i_1(t)}$ | $\text{H}$ ($\text{Wb/A}$) |
| **Induced loop back-EMF (effect)** | $\mathcal{E}_{\text{self}}(t) = -L\,\frac{di(t)}{dt}$ | $\mathcal{E}_{21}(t) = -M\,\frac{di_1(t)}{dt}$ | $\text{V}$ |

## Architecture

### Self-Inductance and the Effect of Trace Width

#### Why Trace Width Controls Inductance ($L$) and Capacitance ($C$) in Opposite Directions

Changing the horizontal copper width $w$ of a PCB trace sitting at height $h$ above its reference plane pushes its distributed inductance per unit length $L$ (in $\text{H/m}$) and its distributed capacitance per unit length $C$ (in $\text{F/m}$) in opposite directions.

First, consider why **narrowing trace width $w$ increases inductance per unit length $L$**. Self-inductance measures how much magnetic flux a conductor stores per ampere of its own current, and the external magnetic field of a current filament is strongest right beside the filament (decaying as $1/r$). Squeezing the same total current $I$ into a narrower copper width $w$ packs the current filaments together so their near-field flux lines reinforce around the metal perimeter, whereas widening the trace spreads the filaments apart so adjacent vertical field components cancel. Dividing $L_{\text{plate}}$ by trace length $\ell$ gives the distributed inductance per unit length $L$ with $w$ in the denominator:

$$L_{\text{plate}} = \frac{\mu_0\,h\,\ell}{w} \qquad \Longrightarrow \qquad L = \frac{L_{\text{plate}}}{\ell} = \frac{\mu_0\,h}{w}$$

Second, consider why **narrowing trace width $w$ decreases capacitance per unit length $C$**. Capacitance $C$ measures opposite electric charge $+Q$ and $-Q$ stored per volt $V$ across the dielectric ($Q/V$). [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) established that a trace of width $w$ and length $\ell$ separated by dielectric thickness $h$ of permittivity $\varepsilon$ (the product $\varepsilon_0 \varepsilon_r$) from the ground plane forms a parallel-plate capacitor of facing area $w\,\ell$. Narrowing $w$ shrinks the facing surface area per meter of length, reducing stored charge and electric field lines across the gap:

$$C_{\text{total}} = \frac{\varepsilon\,w\,\ell}{h} \qquad \Longrightarrow \qquad C = \frac{C_{\text{total}}}{\ell} = \frac{\varepsilon\,w}{h}$$

#### How $L$ and $C$ Set Wave Velocity ($v_p$) and Characteristic Impedance ($Z_0$)

[Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) established how the per-unit-length inductance $L$ and capacitance $C$ govern the phase velocity $v_p$ and characteristic impedance $Z_0$ of a lossless transmission line:

$$v_p = \frac{1}{\sqrt{LC}}, \qquad Z_0 = \sqrt{\frac{L}{C}}$$

Substituting the geometric expressions for $L$ and $C$ into the product $L\,C$ cancels the geometric ratio $h/w$ against $w/h$:

$$L\,C = \left(\frac{\mu_0\,h}{w}\right)\left(\frac{\varepsilon\,w}{h}\right) = \mu_0 \varepsilon = \mu_0 \varepsilon_0 \varepsilon_r$$

Taking the inverse square root of $L\,C$ shows that the wave propagation velocity $v_p$ depends strictly on the dielectric material and remains constant when trace width $w$ changes:

$$v_p = \frac{1}{\sqrt{LC}} = \frac{1}{\sqrt{\mu_0 \varepsilon_0 \varepsilon_r}}$$

By contrast, substituting $L$ and $C$ into the ratio $L/C$ inside the characteristic impedance $Z_0$ compounds the two geometric changes:

$$Z_0 = \sqrt{\frac{L}{C}} = \sqrt{\frac{\mu_0\,h / w}{\varepsilon\,w / h}} = \sqrt{\frac{\mu_0}{\varepsilon}}\,\left(\frac{h}{w}\right)$$

Narrowing a PCB trace ($w \downarrow$) simultaneously raises the numerator $L$ and lowers the denominator $C$, driving the characteristic impedance $Z_0$ upward in inverse proportion to $w$.

Multiplying $Z_0$ by $1/v_p$ cancels $C$ to isolate $L$, and dividing $1/v_p$ by $Z_0$ cancels $L$ to isolate $C$:

$$\frac{Z_0}{v_p} = \sqrt{\frac{L}{C}}\,\sqrt{LC} = \sqrt{L^2} = L$$

$$\frac{1}{Z_0 v_p} = \sqrt{\frac{C}{L}}\,\sqrt{LC} = \sqrt{C^2} = C$$

Rearranging those two identities expresses the constant inverse phase velocity $1/v_p$ in terms of either $L/Z_0$ or $Z_0 C$:

$$\frac{1}{v_p} = \frac{L}{Z_0} = Z_0 C$$

#### Signal Integrity Consequences of a Narrow Trace Neck-Down

Routing a $50\,\Omega$ PCB trace through a dense BGA pin field, connector breakout, or via array often forces the layout to narrow the trace width $w$ over a short segment, a geometry known as a **neck-down** (similar to transitioning onto a narrow IC package lead or bondwire). Inside that narrowed segment, the smaller copper width $w$ packs current filaments together ($L_{\text{neck}}$ rises above the line's normal $L$) while shrinking the facing plate area over the ground plane ($C_{\text{neck}}$ falls below the line's normal $C$). The narrowed segment therefore introduces **localized excess series inductance** $L_{\text{excess}}$ without matching shunt capacitance, spiking its local characteristic impedance $Z_{\text{neck}}$ well above $50\,\Omega$:

$$Z_{\text{neck}} = \sqrt{\frac{L_{\text{neck}}}{C_{\text{neck}}}} > Z_0$$

Recall the inductor voltage-current relation across that excess series inductance $L_{\text{excess}}$ for a digital step whose current changes by $\Delta I$ over rise time $t_r$:

$$v_{\text{neck}}(t) = L_{\text{excess}}\,\frac{di(t)}{dt} \approx L_{\text{excess}}\,\frac{\Delta I}{t_r}$$

This slew-rate proportionality explains why the same physical neck-down is harmless at low speeds yet destructive to high-speed serial links across three distinct mechanisms:

- **Slew-rate selectivity between slow and steep edges:** A slowly varying low-frequency signal has a long rise time $t_r$ and a small slew rate $\frac{di(t)}{dt}$, producing negligible voltage drop $v_{\text{neck}}(t)$, whereas a $20\text{ ps}$ digital edge induces a large opposing back-EMF spike.
- **Positive boundary reflection toward the transmitter ($\Gamma > 0$):** [Chapter 3](03_Impedance_Reflections_and_Termination.md) showed that an incident wave on a $Z_0$ line hitting a higher-impedance segment ($Z_{\text{neck}} > Z_0$) encounters a positive reflection coefficient $\Gamma$ and reflects an upward voltage bump back toward the source.
- **Series low-pass filtering and eye closure at the receiver:** In the frequency domain ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md) and [Chapter 3](03_Impedance_Reflections_and_Termination.md)), inductive reactance $2\pi f L_{\text{excess}}$ grows linearly with $f$, reflecting upper Fourier harmonics to stretch $t_r$ and shrink the receiver eye opening.

$$\Gamma = \frac{Z_{\text{neck}} - Z_0}{Z_{\text{neck}} + Z_0} > 0$$

### Mutual Inductance and Dielectric Height

Placing a return ground plane at vertical distance $h$ below a signal trace of radius $a$ divides the trace's concentric circular magnetic field lines into two radial zones:

1. **Inner magnetic field circles inside the dielectric gap ($a < r < h$):** Field circles with radius smaller than $h$ pass through the dielectric window between the trace and the ground plane and close without reaching the plane. These inner circles wrap around **only** the outbound trace.
2. **Outer magnetic field circles extending beyond the ground plane ($r > h$):** Field circles with radius larger than $h$ expand past the ground plane and wrap around **both** the outbound trace and the return ground plane.

Those outer field circles ($r > h$) encircle both conductors in common and form the **shared magnetic flux** between the outbound trace and the return plane. Older textbooks say this flux "links" the second conductor, picturing a closed magnetic field ring interlocking a conductor ring like two loops of a chain. The **mutual inductance** $M$ between the outbound trace and the return plane is the amount of that shared outer magnetic flux ($r > h$) per ampere of current.

The return plane carries an equal and opposite return current ($-i(t)$) whose magnetic field in the outer region ($r > h$) opposes and cancels that shared outer flux $M$, leaving only the inner magnetic field circles ($a < r < h$) inside the dielectric gap:

- **Thick dielectric (large $h$):** Separating the trace far above the ground plane leaves a wide gap ($a < r < h$) where most magnetic field circles close before reaching the plane. Shared outer flux per ampere ($M$) stays **small**, little outer field is canceled by the return plane, and a large magnetic field remains stored around the loop.
- **Thin dielectric (small $h$):** Bringing the ground plane close underneath the trace shrinks the gap ($a < r < h$) so nearly all magnetic field circles extend past radius $h$ and wrap around both conductors ($M$ is **large**). The opposite return current cancels almost all of that outer field, leaving only a thin ribbon of flux inside the narrow gap $h$.

### The Reciprocity Theorem

A narrow copper signal trace of width $0.15\text{ mm}$ (Conductor 1) and a wide solid ground plane of width $50\text{ mm}$ (Conductor 2) have markedly different cross-sectional shapes. Driving $1\text{ A}$ through the narrow trace generates a concentrated circular magnetic field $\vec{B}_1(r, t)$ that sweeps across the wide plane at steep angles, whereas driving $1\text{ A}$ through the wide plane generates a broad horizontal magnetic field sheet $\vec{B}_2(r, t)$ around the trace. Despite that geometric asymmetry, $1\text{ A}$ in the narrow trace produces the same shared magnetic flux per ampere with the wide plane ($M_{21}$) as $1\text{ A}$ in the wide plane produces with the narrow trace ($M_{12}$).

#### Mutual Flux Symmetry Between Two Individual Filaments

Start with a single thin current filament representing the narrow signal trace (Filament 1) and a single thin current filament $k$ inside the ground plane, separated by straight-line radial distance $r_k$ inside an outer return boundary $r_{\text{far}}$. Recall the logarithmic shared magnetic flux equation derived in the mutual inductance section above:

$$\Phi_{k1}(t) = \left[\frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{r_{\text{far}}}{r_k}\right)\right]i_1(t) = M_{k1}\,i_1(t)$$

The filament-to-filament mutual inductance $M_{k1}$ depends strictly on the permeability $\mu_0$, the shared parallel length $\ell$, and the straight-line radial distance $r_k$ between the two filaments. Point-to-point distance $r_k$ measured from Filament 1 to Filament $k$ is identical to the distance measured from Filament $k$ back to Filament 1, so swapping the roles of the two filaments leaves the logarithmic geometry factor unchanged:

$$M_{k1} = M_{1k} = \frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{r_{\text{far}}}{r_k}\right)$$

#### Extending from One Filament to a Wide Ground Plane of $N$ Filaments

Slicing the wide ground plane into $N$ narrow equal-width parallel filaments ($k$ running from $1$ to $N$) places each filament $k$ at its own radial distance $r_k$ from the narrow signal trace. Under a uniform current distribution across those $N$ strips (and more generally for any shared current-weight distribution across frequency), evaluating the shared flux per ampere in both driving directions yields identical sums:

- **Narrow trace driving the wide plane ($M_{21}$):** Driving current $i_1(t)$ through the narrow trace sends magnetic flux $M_{k1}\,i_1(t)$ to each of the $N$ equal-weight filaments across the ground plane. Each filament carries weight $1/N$ of the parallel plane path, so the effective shared flux $\Phi_{21}(t)$ linking the plane as a whole is the average of the filament fluxes across all $N$ strips:

$$\Phi_{21}(t) = \left(\frac{1}{N}\sum_{k = 1}^{N} M_{k1}\right)i_1(t) \qquad \Longrightarrow \qquad M_{21} = \frac{\Phi_{21}(t)}{i_1(t)} = \frac{1}{N}\sum_{k = 1}^{N} M_{k1}$$

- **Wide plane driving the narrow trace ($M_{12}$):** Driving a uniform total current $i_2(t)$ through the wide ground plane divides the current equally into $i_2(t)/N$ per filament. Each filament $k$ sends a weak magnetic flux $M_{1k}\,i_2(t)/N$ back to the narrow trace, and superposing all $N$ filament contributions at the trace sums the individual fluxes:

$$\Phi_{12}(t) = \sum_{k = 1}^{N} M_{1k}\left(\frac{i_2(t)}{N}\right) = \left(\frac{1}{N}\sum_{k = 1}^{N} M_{1k}\right)i_2(t) \qquad \Longrightarrow \qquad M_{12} = \frac{\Phi_{12}(t)}{i_2(t)} = \frac{1}{N}\sum_{k = 1}^{N} M_{1k}$$

Pairwise distance symmetry ($M_{k1}$ equal to $M_{1k}$ for every strip $k$) makes the two sums identical term by term. That equality is the **reciprocity theorem** for mutual inductance:

$$M_{21} = M_{12} = M$$

No matter how asymmetric the two conductor cross-sections are, mutual inductance is a single shared geometric property $M$ of the conductor pair.

### Total Loop Inductance

#### Stage 1: Why Copper Alone Is Transparent to Magnetic Fields

Every high-speed signal travels around a closed current loop formed by an outbound signal conductor (Conductor 1, carrying current $i_1(t)$) and a return path (Conductor 2, carrying an equal and opposite current $i_2(t)$):

$$i_1(t) = +i(t), \qquad i_2(t) = -i(t)$$

What happens physically when the circular magnetic field lines $\vec{B}_1(x, y, t)$ of the outbound trace hit the copper of the return plane at an angle?

Copper by itself is non-magnetic, with relative permeability $\mu_r$ equal to $1$ ($\mu$ equal to $\mu_0$). A copper sheet carrying zero current is completely transparent to magnetic fields: the circular magnetic field lines from the trace pass straight through the copper atoms at any angle without bending or stopping, just as if the copper were air. Magnetic field lines are only deflected, reshaped, or canceled at a point $(x, y)$ in space when a **second magnetic field** $\vec{B}_2(x, y, t)$, generated by electric current flowing in the second conductor, adds to the first field at that same point by vector superposition:

$$\vec{B}_{\text{net}}(x, y, t) = \vec{B}_1(x, y, t) + \vec{B}_2(x, y, t)$$

#### Three-Region Right-Hand-Rule Superposition

Before examining angled vectors, trace the horizontal magnetic field directions along the vertical centerline passing through both conductors. The top outbound conductor carries current straight out of the page ($\odot$) and generates a counter-clockwise magnetic field by the Generation Rule, whereas the bottom return conductor carries current straight into the page ($\otimes$) and generates a clockwise magnetic field.

A common visual trap arises from comparing the magnetic field **above the top conductor** (where its counter-clockwise circle points **left**, $\leftarrow$) with the magnetic field **below the bottom conductor** (where its clockwise circle also points **left**, $\leftarrow$). Comparing those two leftward arrows makes it appear as though the outer magnetic fields point in the same direction and reinforce.

That comparison is a spatial trap because the space above the top conductor and the space below the bottom conductor are **two different locations**. Vector superposition adds $\vec{B}_1$ and $\vec{B}_2$ at the **same point in space**. Evaluating both conductors' magnetic field circles at the same observation point across the three vertical regions resolves the field directions immediately:

1. **Region 1 (Above both conductors):** A point above the trace sits above the top conductor ($\odot$ counter-clockwise top pointing **left**, $\leftarrow$) and also sits above the bottom conductor ($\otimes$ clockwise top pointing **right**, $\rightarrow$). The two fields point in **opposite directions and cancel** in the upper outer region.
2. **Region 2 (Inside dielectric gap $h$):** A point inside the dielectric gap sits below the top conductor ($\odot$ counter-clockwise bottom pointing **right**, $\rightarrow$) and above the bottom conductor ($\otimes$ clockwise top pointing **right**, $\rightarrow$). Both fields point in the **same rightward direction and add constructively** inside the dielectric gap.
3. **Region 3 (Below both conductors):** A point underneath the return path sits below the top conductor ($\odot$ counter-clockwise bottom pointing **right**, $\rightarrow$) and also sits below the bottom conductor ($\otimes$ clockwise bottom pointing **left**, $\leftarrow$). The two fields point in **opposite directions and cancel** in the lower outer region.

#### Stage 2: How Two Angled Field Vectors Superpose into a Flat Horizontal Field

Step off the vertical centerline to an observation point $P$ on the copper return surface slightly to the right of the outbound trace, where the trace's circular field line hits the copper at an angle. By the Generation Rule, the outbound trace ($\odot$) produces a counter-clockwise magnetic field vector $\vec{B}_1$ at point $P$ slanted **upward and to the right** ($\nearrow$). That slanted vector decomposes into a rightward horizontal component $B_{1,x}$ ($\rightarrow$) parallel to the copper surface and an upward vertical component $+B_{1,y}$ ($\uparrow$) poking perpendicularly through the copper surface:

$$\vec{B}_1 = B_{1,x}\,\hat{x} + B_{1,y}\,\hat{y}$$

Return current ($\otimes$) concentrated directly beneath the trace produces a clockwise magnetic field vector $\vec{B}_2$ at point $P$ slanted **downward and to the right** ($\searrow$). That second vector decomposes into a rightward horizontal component $B_{2,x}$ ($\rightarrow$) parallel to the copper surface and a downward vertical component $-B_{2,y}$ ($\downarrow$) pointing into the copper surface:

$$\vec{B}_2 = B_{2,x}\,\hat{x} - B_{2,y}\,\hat{y}$$

Adding $\vec{B}_1$ and $\vec{B}_2$ component by component at point $P$ when the vertical components have equal magnitude ($B_{2,y}$ equal to $B_{1,y}$) bends the net magnetic field flat along the copper plane:

$$B_{\text{net},x} = B_{1,x} + B_{2,x}, \qquad B_{\text{net},y} = B_{1,y} - B_{2,y} = 0$$

The opposing vertical components ($\uparrow$ and $\downarrow$) cancel to zero so the net magnetic field cannot poke through the copper surface, while the matching horizontal components ($\rightarrow$ and $\rightarrow$) reinforce so the net magnetic field skims flat and parallel inside the dielectric gap.

#### Deriving Total Loop Inductance from Partial Inductances

Partial inductance notation quantifies how each conductor's self-flux and their shared mutual flux combine around the complete signal loop:

- **Outbound trace partial self-inductance $L_1$ (in $\text{H}$):** The magnetic flux per ampere that Conductor 1's own current $i_1(t)$ generates around itself.
- **Return path partial self-inductance $L_2$ (in $\text{H}$):** The magnetic flux per ampere that Conductor 2's own current $i_2(t)$ generates around itself.
- **Mutual inductance $M$ (in $\text{H}$):** The shared outer magnetic flux per ampere ($r > h$) that wraps around both conductors in common.

Recall the self-induced terminal voltage relation and mutual-induced voltage relation established earlier in this chapter:

$$v_{\text{self}}(t) = L\,\frac{di(t)}{dt}, \qquad v_{\text{mutual}}(t) = M\,\frac{di_{\text{other}}(t)}{dt}$$

Both conductors carry time-varying currents simultaneously, so the total inductive voltage drop $v_1(t)$ along Conductor 1 in the $+z$ direction is the sum of its self-induced voltage drop from $i_1(t)$ and the mutual voltage induced by Conductor 2's current $i_2(t)$. Likewise, the total inductive voltage drop $v_2(t)$ along Conductor 2 referenced to the $+z$ direction is the sum of its self-induced voltage drop from $i_2(t)$ and the mutual voltage induced by Conductor 1's current $i_1(t)$:

$$v_1(t) = L_1\,\frac{di_1(t)}{dt} + M\,\frac{di_2(t)}{dt}$$

$$v_2(t) = L_2\,\frac{di_2(t)}{dt} + M\,\frac{di_1(t)}{dt}$$

Recall the antiparallel outbound and return loop currents:

$$i_1(t) = +i(t), \qquad i_2(t) = -i(t)$$

Substituting $+i(t)$ for $i_1(t)$ and $-i(t)$ for $i_2(t)$ into both conductor voltage equations shows how the opposing return current subtracts $M$ from each conductor's self-inductance:

$$v_1(t) = L_1\,\frac{di(t)}{dt} + M\,\frac{d\bigl[-i(t)\bigr]}{dt} = (L_1 - M)\,\frac{di(t)}{dt}$$

$$v_2(t) = L_2\,\frac{d\bigl[-i(t)\bigr]}{dt} + M\,\frac{di(t)}{dt} = -(L_2 - M)\,\frac{di(t)}{dt}$$

A signal source driving the closed loop pushes current forward ($+z$) along Conductor 1 and pulls it back ($-z$) along Conductor 2. Reversing the traversal direction along Conductor 2 from $+z$ to $-z$ flips the sign of $v_2(t)$, so the total voltage drop $v_{\text{loop}}(t)$ around the complete round-trip circuit subtracts $v_2(t)$ from $v_1(t)$:

$$v_{\text{loop}}(t) = v_1(t) - v_2(t) = (L_1 - M)\,\frac{di(t)}{dt} - \left[-(L_2 - M)\,\frac{di(t)}{dt}\right] = (L_1 + L_2 - 2M)\,\frac{di(t)}{dt}$$

Defining the **total loop inductance** $L_{\text{loop}}$ as the net inductance of the complete round-trip circuit relates $v_{\text{loop}}(t)$ to $\frac{di(t)}{dt}$:

$$v_{\text{loop}}(t) = L_{\text{loop}}\,\frac{di(t)}{dt} \qquad \Longrightarrow \qquad L_{\text{loop}} = L_1 + L_2 - 2M$$

The $-2M$ term captures the two-way outer field cancellation in Regions 1 and 3: one $-M$ comes from Conductor 2's return current canceling the outer flux of Conductor 1 ($L_1 - M$), and the second $-M$ comes from Conductor 1's outbound current canceling the outer flux of Conductor 2 ($L_2 - M$). Bringing the return plane closer to the trace increases $M$ and reduces $L_{\text{loop}}$ by twice the increase in $M$.

#### Motivating the Coupling Bound $M \le \sqrt{L_1 L_2}$ and the Loop Inductance Floor

How large can the mutual inductance $M$ become before reaching a physical limit? Current $i_1(t)$ in Conductor 1 generates a total self-flux $\Phi_{11}(t)$ equal to $L_1\,i_1(t)$. Even if Conductor 2 sits right against Conductor 1, Conductor 2 can intercept at most $100\%$ of the magnetic flux that Conductor 1 created, never more than $100\%$. Let $k_1$ (a dimensionless fraction between $0$ and $1$) represent the fraction of Conductor 1's self-flux that passes through Conductor 2:

$$\Phi_{11}(t) = L_1\,i_1(t), \qquad \Phi_{21}(t) = k_1\,\Phi_{11}(t), \qquad 0 \le k_1 \le 1$$

Replacing $\Phi_{21}(t)$ with $M\,i_1(t)$ and $\Phi_{11}(t)$ with $L_1\,i_1(t)$ and dividing both sides by $i_1(t)$ relates $M$ to $L_1$:

$$M = k_1\,L_1$$

By the same physical conservation of flux, Conductor 2 carrying current $i_2(t)$ generates self-flux $\Phi_{22}(t)$ equal to $L_2\,i_2(t)$, of which Conductor 1 intercepts at most a fraction $k_2$ (between $0$ and $1$), relating $M$ to $L_2$:

$$\Phi_{22}(t) = L_2\,i_2(t), \qquad \Phi_{12}(t) = k_2\,\Phi_{22}(t), \qquad 0 \le k_2 \le 1 \qquad \Longrightarrow \qquad M = k_2\,L_2$$

Multiplying those two expressions for $M$ together and taking the square root defines the dimensionless **magnetic coupling coefficient** $k$:

$$M^2 = (k_1\,L_1)(k_2\,L_2) \qquad \Longrightarrow \qquad M = k\sqrt{L_1 L_2}, \qquad k = \sqrt{k_1 k_2} \in [0, 1]$$

Neither fraction $k_1$ nor $k_2$ can exceed $1$, so the coupling coefficient $k$ is at most $1$, bounding the mutual inductance $M$ by the geometric mean of the two partial self-inductances:

$$M \le \sqrt{L_1 L_2}$$

Recall the total loop inductance equation derived above:

$$L_{\text{loop}} = L_1 + L_2 - 2M$$

Replacing $M$ with its upper bound $\sqrt{L_1 L_2}$ and factoring the perfect-square trinomial establishes the theoretical minimum floor on total loop inductance:

$$L_{\text{loop}} \ge L_1 - 2\sqrt{L_1 L_2} + L_2 = \left(\sqrt{L_1} - \sqrt{L_2}\right)^2$$

Total loop inductance $L_{\text{loop}}$ can approach zero only when both conductors have equal partial self-inductances ($L_1$ equal to $L_2$) and share $100\%$ of their magnetic flux ($k$ equal to $1$). A narrow PCB trace ($L_1$ large) paired with a wide ground plane ($L_2$ small) always has $L_1$ larger than $L_2$, leaving a positive inductance floor $\left(\sqrt{L_1} - \sqrt{L_2}\right)^2$ no matter how thin the dielectric laminate becomes.

### Loop Inductance and Return Current Distribution Across Frequency

On a circuit board, the outbound signal trace is a narrow copper strip of width $w$, whereas the return path is a continuous copper ground plane of much larger width $W_{\text{plane}}$. Return electrons inside the wide ground plane are free to distribute themselves across $W_{\text{plane}}$ along whichever path minimizes the total loop impedance $Z_{\text{loop}}(\omega)$. At angular frequency $\omega$ (equal to $2\pi f$), the total loop impedance combines the series loop resistance $R_{\text{loop}}$ (in $\Omega$) with the inductive reactance $j\omega L_{\text{loop}}$ (in $\Omega$) from [Chapter 3](03_Impedance_Reflections_and_Termination.md):

$$Z_{\text{loop}}(\omega) = R_{\text{loop}} + j\omega L_{\text{loop}}$$

Comparing steady DC ($\omega$ equal to $0$) with high-frequency AC ($\omega$ greater than $0$) explains why the trace's magnetic field passes straight through the copper ground plane at DC yet is blocked from penetrating the plane at high frequencies.

#### Stage 3 (Steady DC): Why the Trace's Field Passes Through the Uniform Ground Plane

Under a steady, unchanging DC current $I$, the angular frequency $\omega$ is zero and the magnetic flux $\Phi_B$ around the trace is constant in time:

$$\frac{d\Phi_B(t)}{dt} = 0$$

Recall the Faraday-Lenz law relating induced loop voltage $\mathcal{E}(t)$ to the time derivative of magnetic flux:

$$\mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt}$$

Substituting zero flux change shows that a static magnetic field induces zero opposing voltage ($\mathcal{E}$ equal to $0$) inside the copper ground plane, and the inductive reactance term $j\omega L_{\text{loop}}$ vanishes from the loop impedance:

$$Z_{\text{loop}}(0) = R_{\text{loop}} = R_{\text{trace}} + R_{\text{plane}}$$

With zero magnetic opposition acting on them, the return electrons spread uniformly across the entire two-dimensional cross-sectional area $A_{\text{plane}}$ ($W_{\text{plane}}\,t_{\text{Cu}}$) of the copper sheet (of width $W_{\text{plane}}$, vertical foil thickness $t_{\text{Cu}}$, and electrical resistivity $\rho_r$) to minimize the plane's DC resistance $R_{\text{plane}}$ from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md):

$$R_{\text{plane}} = \frac{\rho_r\,\ell}{A_{\text{plane}}} = \frac{\rho_r\,\ell}{W_{\text{plane}}\,t_{\text{Cu}}}$$

Inside the copper foil, the return current $I$ has a uniform cross-sectional area current density $J_{\text{DC}}$ (in $\text{A/m}^2$):

$$J_{\text{DC}} = \frac{I}{A_{\text{plane}}} = \frac{I}{W_{\text{plane}}\,t_{\text{Cu}}}$$

Outside the ground plane (in the dielectric above the plane or the air below the plane), any Ampère loop straddles the full vertical thickness $t_{\text{Cu}}$ of the copper foil. Multiplying the area current density $J_{\text{DC}}$ by the foil thickness $t_{\text{Cu}}$ cancels $t_{\text{Cu}}$ and leaves the constant DC sheet current density $K_{\text{DC}}$ (in $\text{A/m}$) per unit width across the board:

$$K_{\text{DC}} = J_{\text{DC}}\,t_{\text{Cu}} = \left(\frac{I}{W_{\text{plane}}\,t_{\text{Cu}}}\right)t_{\text{Cu}} = \frac{I}{W_{\text{plane}}}$$

Recall the magnetic field of a uniform current sheet derived at the start of this chapter. Around any observation point on a uniform sheet, parallel current filaments located at equal distances to the left and right carry identical currents, so their upward ($\uparrow$) and downward ($\downarrow$) vertical magnetic field components cancel completely ($B_{\text{plane},y}$ equal to $0$). The uniform ground plane generates only a weak horizontal magnetic field $B_{\text{plane},x}$ parallel to the copper surface:

$$B_{\text{plane},y} = 0, \qquad B_{\text{plane},x} = \frac{\mu_0 K_{\text{DC}}}{2} = \frac{\mu_0 I}{2 W_{\text{plane}}}$$

Meanwhile, the narrow signal trace at height $h$ above the plane generates a strong circular magnetic field $\vec{B}_{\text{trace}}$ that hits the copper plane at an angle with both a strong horizontal component $B_{\text{trace},x}$ and a strong vertical component $B_{\text{trace},y}$. Superposing the trace field and the uniform DC plane field reveals two physical consequences:

- **Zero vertical opposition at the copper surface:** The uniform ground plane produces zero vertical magnetic field ($B_{\text{plane},y}$ equal to $0$) anywhere across its width. Nothing opposes $B_{\text{trace},y}$, so the trace's vertical magnetic field lines pass unopposed straight through the non-magnetic copper plane ($\mu_r$ equal to $1$).
- **Weak horizontal partial cancellation underneath the plane:** Directly below the ground plane (Region 3, at radial distance $r > h$ from the trace), the trace's rightward horizontal field has magnitude $\frac{\mu_0 I}{2\pi r}$, whereas the plane's opposing leftward horizontal field is diluted across the full board width $W_{\text{plane}}$:

$$B_{\text{net},x}\big|_{\text{below plane}} = \frac{\mu_0 I}{2\pi r} - \frac{\mu_0 I}{2 W_{\text{plane}}} > 0$$

How does this spread-out DC return current affect the mutual inductance $M_{\text{DC}}$ and the total DC loop inductance $L_{\text{loop,DC}}$? Recall the filament average for mutual inductance between the narrow trace and the $N$ parallel return filaments across the ground plane:

$$M_{\text{DC}} = \frac{1}{N}\sum_{k = 1}^{N} \frac{\mu_0\,\ell}{2\pi}\ln\!\left(\frac{r_{\text{far}}}{r_k}\right)$$

At steady DC, most of the return current flows in distant wing filaments where the radial distance $r_k$ from the trace is large. For any distant return filament at large $r_k$, almost all of the trace's circular magnetic field lines ($a < r < r_k$) close in the space between the trace and filament $k$ without ever reaching filament $k$. Only the largest, weakest outer field circles ($r > r_k$) wrap around both the trace and that distant filament, making $\ln(r_{\text{far}}/r_k)$ small and keeping the average mutual inductance $M_{\text{DC}}$ **small**.

Substituting that small $M_{\text{DC}}$ into the total loop inductance equation links $M_{\text{DC}}$ directly to the surviving net magnetic flux $\Phi_{\text{net,DC}}$ per ampere:

$$L_{\text{loop,DC}} = L_1 + L_2 - 2M_{\text{DC}} = \frac{\Phi_{\text{net,DC}}}{I}$$

Diluting the return current far out in the wings makes its opposing magnetic field near the trace tiny, which keeps the $-2M_{\text{DC}}$ field-cancellation term small. With almost no opposing field from the plane to cancel them, the trace's magnetic field lines survive unopposed across a wide region above, through, and underneath the ground plane, storing a large net magnetic flux $\Phi_{\text{net,DC}}$ per ampere and making the DC loop inductance $L_{\text{loop,DC}}$ **large**.

#### Stage 4 (High-Frequency AC): How Lenz Crowding Breaks Sheet Symmetry to Cancel Vertical and Outer Fields

Under a rapidly changing high-frequency current or a steep digital edge, the inductive reactance $\omega L_{\text{loop}}$ in the loop impedance equation dominates the resistance $R_{\text{loop}}$ by orders of magnitude:

$$Z_{\text{loop}}(\omega) = R_{\text{loop}} + j\omega L_{\text{loop}} \approx j\omega L_{\text{loop}}$$

Ramping up the trace current $i(t)$ causes its expanding circular magnetic field lines to push **changing vertical magnetic flux** through the copper ground plane directly beneath the trace. Recall the Faraday-Lenz law inside the conducting copper sheet:

$$\mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt}$$

The trace's circular magnetic field is strongest directly underneath the trace (at shortest radial distance $h$) and weakens with horizontal distance $x$ out into the wings. That spatial concentration makes the rate of change of magnetic flux most intense in the copper strip directly below the trace. By Lenz's law and the Reaction Rule, that local flux change induces the strongest opposing electromotive force right beneath the trace. The induced opposing voltage pulls the antiparallel return current ($-i(t)$) out of the wide outer wings of the plane and crowds it into a narrow, high-density corridor directly under the trace.

How does crowding the return current into a narrow corridor under the trace allow a flat copper plane to cancel the trace's **vertical** magnetic field component $B_{\text{trace},y}$? **Current crowding breaks the left-right uniformity of the ground plane.**

At an observation point $P$ on the copper plane surface slightly to the right of the trace, the outbound trace ($\odot$, counter-clockwise field) produces a slanted field vector $\vec{B}_{\text{trace}}$ with a rightward horizontal component ($\rightarrow$) and an **upward** vertical component $+B_{\text{trace},y}$ ($\uparrow$). Return filaments ($\otimes$, clockwise field) on the two sides of point $P$ contribute unequal vertical fields:

- **Inner plane filaments to the left of $P$ (directly under the trace):** These inner filaments carry the crowded, high-density peak of the return current ($\otimes$). Point $P$ lies to the right of these clockwise filaments, so their magnetic field circles push strongly **downward** ($\downarrow$) at point $P$.
- **Outer plane filaments to the right of $P$ (out in the wing of the plane):** These outer filaments carry only a sparse, weak tail of the return current ($\otimes$). Point $P$ lies to the left of these clockwise filaments, so their magnetic field circles push **upward** ($\uparrow$) at point $P$ only weakly.

The dense inner filaments under the trace overpower the sparse outer filaments in the wing, so the plane's upward and downward vertical contributions **no longer cancel each other**. Instead, the plane produces a net **downward** vertical magnetic field component $-B_{\text{plane},y}$ ($\downarrow$) on the right of the trace (and, by mirror symmetry, a net **upward** vertical component $\uparrow$ on the left of the trace) that matches and cancels the trace's vertical field across the copper surface:

$$B_{\text{net},y}\big|_{\text{copper surface}} = B_{\text{trace},y} - B_{\text{plane},y} = 0$$

Simultaneously, concentrating the return current $-i(t)$ directly beneath the trace raises the plane's local horizontal field component $B_{\text{plane},x}$ to match the trace's horizontal field magnitude $B_{\text{trace},x}$. Inside the dielectric gap (Region 2), the two rightward horizontal fields add constructively ($\rightarrow + \rightarrow$). Underneath the ground plane (Region 3), the trace's rightward horizontal field and the crowded plane's strong leftward horizontal field cancel to zero:

$$B_{\text{net},x}\big|_{\text{below plane}} = B_{\text{trace},x} - B_{\text{plane},x} \approx 0$$

Recall the total loop inductance equation to see the net effect on inductance:

$$L_{\text{loop}} = L_1 + L_2 - 2M$$

Pinching the return current into a narrow corridor under the trace slightly increases the partial self-inductance $L_2$ of the return path, just as narrowing a trace increases its self-inductance. At the same time, placing all the return current filaments at the minimum distance $h$ directly beneath the outbound trace maximizes the shared outer flux per ampere, driving the mutual inductance $M$ up by a much larger amount. The large $-2M$ reduction outweighs the small rise in $L_2$, driving the high-frequency loop inductance $L_{\text{loop,AC}}$ down to its minimum floor and confining the magnetic field cleanly inside the dielectric gap ([Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md)).

### Crosstalk: Electromagnetic Coupling Between Neighboring Traces

#### What Is the Victim Trace? (Victim Trace vs. Ground Plane vs. Differential Pair)

Up to this point in the chapter, every circuit had **two** pieces of copper: one narrow signal trace on top and one wide copper ground plane underneath. That single-wire-over-ground arrangement is called a **single-ended transmission line**. On a real circuit board (such as a computer memory bus), dozens of **separate, independent single-ended signal traces** run side by side over the **same shared ground plane**. **Trace 1** might carry Bit 0 of a data bus while **Trace 2** right next to it carries Bit 1.

Both the ground plane underneath and Trace 2 next door are passive copper conductors sitting within reach of Trace 1's expanding electric and magnetic fields, so a signal switching on Trace 1 induces currents in **both** of them. Why is current induced in the ground plane helpful, whereas current induced in Trace 2 is a serious problem?

- **The Ground Plane (intended return path):** Neither end of the ground plane connects to a receiver chip's data decision input. Current induced in the ground plane returns Trace 1's own signal current back to its source without disturbing any receiver threshold.
- **Trace 2, the Victim Trace (adjacent single-ended channel):** Trace 2 connects its own transmitter at the near end (zero $z$) to its own receiver at the far end (coordinate $\ell$), both measuring voltage relative to the ground plane. Unwanted voltage induced onto a quiet $0\text{ V}$ Trace 2 by Trace 1's fields enters Trace 2's receiver and can trigger a false logic `1` (**crosstalk**).
- **Differential-pair contrast (intentional odd-mode coupling):** A **differential pair** ([Chapter 8](08_S_Parameters_and_VNA.md) and [Chapter 16](16_SerDes_Architecture_and_Eye_Diagrams.md)) routes two coupled traces as paired conductors carrying equal and opposite signals ($+v(t)$ and $-v(t)$) into one differential receiver. Crosstalk instead couples two independent single-ended channels carrying unrelated data, analyzed by holding the victim quiet at $0\text{ V}$ while the aggressor steps from $0\text{ V}$ to $+V_a$.

#### Self vs. Mutual Capacitance ($C_m / C$) and Self vs. Mutual Inductance ($L_m / L$)

In a cross-section of the board, **Trace 1 (aggressor)** sits next to **Trace 2 (victim, at $0\text{ V}$)** above the **shared ground plane (also at $0\text{ V}$)**. Ramping the aggressor trace toward $+V_a$ and $+I_a$ sends most of its electric and magnetic fields to the ground plane underneath, while a smaller share spills sideways onto the victim trace:

- **Self-capacitance per unit length ($C$, in $\text{F/m}$):** Pushing positive charge onto the aggressor trace sends electric field lines ($\vec{E}$) outward toward $0\text{ V}$ copper. **Most** go straight down to the ground plane, and $C$ counts the **total** electric field lines leaving the aggressor trace per volt.
- **Mutual capacitance per unit length ($C_m$, in $\text{F/m}$) and the fraction $\frac{C_m}{C}$:** A smaller share of the aggressor's electric field lines curves sideways across the spacing gap and lands on the victim trace (which is also at $0\text{ V}$). The ratio $\frac{C_m}{C}$ is a fraction between $0$ and $1$ measuring **what share of the aggressor's electric field lines land sideways on the victim trace**.
- **Self-inductance per unit length ($L$, in $\text{H/m}$):** Driving current along the aggressor trace wraps circular magnetic flux loops ($\vec{B}$) around the aggressor. The line's self-inductance $L$ counts the total magnetic flux per ampere wrapping through the aggressor's own dielectric window to the ground plane.
- **Mutual inductance per unit length ($L_m$, in $\text{H/m}$) and the fraction $\frac{L_m}{L}$:** Wider magnetic flux loops from the aggressor reach sideways and thread between the victim trace and the ground plane, measured by $L_m$. The ratio $\frac{L_m}{L}$ is the matching magnetic fraction measuring **what share of the aggressor's magnetic flux loops reach sideways through the victim's loop window**.

#### Where Coupling Happens: Only Inside the Moving Rising Edge

Where along the coupled length $\ell$ (from zero $z$ on the left to $\ell$ on the right) do those sideways fields induce voltage and current on the victim trace?

- **Behind the rising edge (to the left):** The aggressor has already finished rising to a steady voltage $+V_a$ and a steady current $I_a$. Static electric and magnetic fields (zero $\frac{\partial v_a}{\partial t}$ and zero $\frac{\partial i_a}{\partial t}$) induce zero current and zero voltage in the victim.
- **Ahead of the rising edge (to the right):** The aggressor wave has not arrived yet, so the aggressor sits at $0\text{ V}$ and $0\text{ A}$ with zero fields.
- **Inside the moving rising edge (active transition zone):** The aggressor voltage and current actively ramp upward within the moving spatial window of length $\ell_{\text{edge}}$ (equal to $v_p\,t_r$), creating time-varying electric and magnetic fields $\vec{E}(z, t)$ and $\vec{B}(z, t)$.

$$\ell_{\text{edge}} = v_p\,t_r$$

Sliding from left (zero $z$) to right (coordinate $\ell$) at wave velocity $v_p$, that rising edge sweeps past each short copper slice $\Delta z$ and launches tiny coupled voltage waves (**wavelets**) onto the victim trace in both directions:

- **Near-End Crosstalk (NEXT, measured at zero $z$):** Unwanted noise voltage $v_{\text{NEXT}}(t)$ arriving at the left end of the victim trace (next to the aggressor's transmitter), carried by wavelets traveling **backward** ($-z$) opposite to the aggressor wave.
- **Far-End Crosstalk (FEXT, measured at coordinate $\ell$):** Unwanted noise voltage $v_{\text{FEXT}}(t)$ arriving at the right end of the victim trace (next to the aggressor's receiver), carried by wavelets traveling **forward** ($+z$) in the same direction as the aggressor wave.

#### Zero Electrons Cross the Gap: The 3D Geometry of the Fields

Before looking at the equations for a single slice $\Delta z$, clear up two foundational physical questions: **Do electrons ever jump across the gap from the aggressor wire to the victim wire?** And **which way do the electric and magnetic fields point in 3D space?**

First, **zero electrons ever cross the gap** between the aggressor trace and the victim trace. Fiberglass and air between the two traces are electrical insulators. Instead, the victim trace is already a solid copper wire filled with its own mobile conduction electrons ($-$) and fixed positive copper ions ($+$), initially balanced everywhere ($0\text{ V}$). Both capacitive and inductive crosstalk work purely by **fields reaching across the insulator and pushing the existing mobile charges already inside the victim wire**.

Second, trace the 3D directions of the fields around the aggressor trace as a rising step ($+V_a$, $+I_a$) travels **from left to right ($\rightarrow$, forward)**:

- **The aggressor's electrostatic field ($\vec{E}_{\text{cap}}$, from positive charge $+Q$):** Positive charge on the aggressor shoots straight electric field lines **radially outward like spokes on a wheel**, pointing perpendicular to the wire (straight down to the ground plane and **sideways across the gap** toward the victim trace).
- **The aggressor's magnetic field ($\vec{B}_{\text{agg}}$, from forward current $i_a$):** Pointing the right thumb to the right ($\rightarrow$) shows that $\vec{B}_{\text{agg}}$ wraps around the wire in **concentric circles** perpendicular to the $\vec{E}_{\text{cap}}$ spokes. Those circles come **out of the page ($\odot$) above the trace** and dive **into the page ($\otimes$) below the trace**.
- **The induced electric field ($\vec{E}_{\text{ind}}$, back-EMF) and opposing magnetic field ($\vec{B}_{\text{ind}}$):** By **Faraday's law**, the growing magnetic field ($\otimes$) creates a **lengthwise induced electric field $\vec{E}_{\text{ind}}$ pointing along the victim wire from right to left ($\leftarrow$)**. That $\vec{E}_{\text{ind}}$ pushes victim current $i_{\text{ind}}$ from right to left ($\leftarrow$), generating the **opposing magnetic field $\vec{B}_{\text{ind}}$ out of the page ($\odot$)**.

#### Capacitive Coupling at a Single Slice: A Sideways Electric Field Repelling Positive Current Both Ways

Consider how the aggressor's **sideways electrostatic field ($\vec{E}_{\text{cap}}$)** acts on the existing charges inside a single short slice $\Delta z$ of the victim wire at position $z$. Inside slice $\Delta z$, the rising aggressor voltage ($+V_a$) holds concentrated positive charge ($+$), shooting $\vec{E}_{\text{cap}}$ sideways across the insulating gap onto slice $\Delta z$ of the victim wire.

By Coulomb's law (**opposite charges attract, like charges repel**), that positive electric field reaching from the side attracts negative electrons ($-$) toward the facing surface of slice $\Delta z$ while **repelling positive conventional current ($\Delta i_C$) away from slice $\Delta z$ along the victim wire**.

Pushing on slice $\Delta z$ **from the side** (perpendicular to the length of the victim wire), $\vec{E}_{\text{cap}}$ has zero preference for left versus right. Seeing the same characteristic impedance $Z_0$ looking left (backward, $-z$) and looking right (forward, $+z$), the repelled positive current splits $50/50$ outward in **both directions**:

- Half of the repelled positive current ($\frac{1}{2}\Delta i_C$) flows **left (backward, $-z$)** toward the Near End, launching a **positive** capacitive voltage bump ($\Delta v_{b,C}$ positive).
- Half of the repelled positive current ($\frac{1}{2}\Delta i_C$) flows **right (forward, $+z$)** toward the Far End, launching an identical **positive** capacitive voltage bump ($\Delta v_{f,C}$ positive).

Three physical factors set the voltage height of those two positive capacitive bumps:

1. **The $\frac{1}{2}$ left-right split:** Half of the repelled positive current goes backward ($-z$) and half goes forward ($+z$).
2. **The electric-field sharing fraction $\frac{C_m}{C}$:** The fraction of the aggressor's electric field lines that land sideways on the victim trace ($C_m$) rather than the ground plane ($C$).
3. **The aggressor voltage change during the slice transit time $\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$:** Traveling at speed $v_p$, the aggressor wavefront spends transit time $\frac{\Delta z}{v_p}$ crossing slice $\Delta z$ while ramping at rate $\frac{\partial v_a(z, t)}{\partial t}$.

Circuit equations reproduce this product of three physical factors directly. Recall the capacitor current-voltage relation from [Chapter 3](03_Impedance_Reflections_and_Termination.md) and apply it to the slice coupling capacitance $C_{\text{cap}}$ of $C_m\,\Delta z$:

$$C_{\text{cap}} = C_m\,\Delta z, \qquad i_C(t) = C_{\text{cap}}\,\frac{dv(t)}{dt} \qquad \Longrightarrow \qquad \Delta i_C(z, t) = (C_m\,\Delta z)\,\frac{\partial v_a(z, t)}{\partial t}$$

Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) how a current wave $i_{\text{wave}}$ traveling into characteristic impedance $Z_0$ produces a voltage wave $v_{\text{wave}}$, and apply that relation to each half-current $\frac{1}{2}\Delta i_C(z, t)$:

$$v_{\text{wave}} = Z_0\,i_{\text{wave}}$$

$$\Delta v_{b,C}(z, t) = \Delta v_{f,C}(z, t) = Z_0\left[\frac{1}{2}\Delta i_C(z, t)\right] = \frac{1}{2}\,Z_0\,C_m\,\Delta z\,\frac{\partial v_a(z, t)}{\partial t}$$

To express circuit impedance $Z_0$ in terms of the line's self-capacitance $C$ and wave velocity $v_p$, recall the transmission-line identity derived earlier in this chapter:

$$Z_0 = \frac{1}{v_p\,C}$$

Replacing $Z_0$ with $\frac{1}{v_p\,C}$ confirms the three physical factors (the $\frac{1}{2}$ split, the capacitive sharing fraction $\frac{C_m}{C}$, and the slice transit time $\frac{\Delta z}{v_p}$ times the voltage slew rate):

$$\Delta v_{b,C}(z, t) = \Delta v_{f,C}(z, t) = \frac{1}{2}\,\frac{C_m}{C}\,\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$$

#### Inductive Coupling at a Single Slice: A Lengthwise Induced Electric Field (Back-EMF) Shoving Charge Backward

Contrasting that sideways capacitive push against the aggressor's expanding **magnetic field ($\vec{B}_{\text{agg}}$)** explains what magnetic coupling does to the charges inside that same victim slice $\Delta z$. Why does magnetic coupling launch a **positive** wave going backward ($-z$) and a **negative** wave going forward ($+z$)?

Follow the four-step Faraday and Lenz chain inside slice $\Delta z$ as the aggressor current $i_a(z, t)$ ramps up from **left to right ($\rightarrow$, forward)**:

1. **Growing magnetic field into the page ($\otimes$):** Below the wires inside the dielectric loop window, the aggressor's magnetic field $\vec{B}_{\text{agg}}$ points **into the page ($\otimes$)** and grows stronger with time (while coming **out of the page $\odot$** above the wire).
2. **Opposing magnetic field out of the page ($\odot$) below the wire:** By Lenz's law, the victim loop opposes that increase by generating an **induced magnetic field $\vec{B}_{\text{ind}}$** that comes **out of the page ($\odot$) below the wire** (and goes **into the page $\otimes$ above the wire**).
3. **Victim current direction from right to left ($\leftarrow$):** Pointing the right thumb **from right to left ($\leftarrow$)** along the victim wire curls the fingers into the page ($\otimes$) above and out of the page ($\odot$) below, producing $\vec{B}_{\text{ind}}$.
4. **Lengthwise induced electric field ($\vec{E}_{\text{ind}}$, back-EMF) pushing from right to left ($\leftarrow$):** Faraday's law creates a **lengthwise induced electric field $\vec{E}_{\text{ind}}$ pointing horizontally along the victim wire from right to left ($\leftarrow$)**, driving that leftward victim current.

Unlike the capacitive field $\vec{E}_{\text{cap}}$ (which pushed from the **side** and repelled positive charge equally left and right), the inductive back-EMF field $\vec{E}_{\text{ind}}$ pushes **lengthwise along the wire from right to left ($\leftarrow$)**, shoving positive charge from the right end of segment $\Delta z$ to the left end of segment $\Delta z$:

- **Near-End charge surplus on the left side ($+$):** Shoving positive charge into the left end creates a positive charge surplus on the left side. That surplus launches a **positive** inductive voltage wave ($\Delta v_{b,L}$ positive) traveling **backward** ($-z$) toward the near end (zero $z$).
- **Far-End charge deficit on the right side ($-$):** Pulling that positive charge out of the right end leaves behind a charge deficit (a negative voltage dip) on the right side. That deficit launches an equal-magnitude **negative** inductive voltage wave ($\Delta v_{f,L}$ negative) traveling **forward** ($+z$) toward the far end (coordinate $\ell$).

Why does inductive coupling also have a **$\frac{1}{2}$ factor** on each side (instead of sending the full amount to the left and making the leftward inductive current twice as large as the leftward capacitive current)?

To push current $i_{\text{ind}}$ from right to left ($\leftarrow$) through segment $\Delta z$, the inductive voltage $\Delta v_L$ cannot create charge out of nothing. Every bit of current pushed into the left half of the wire (impedance $Z_0$) must be pulled out of the right half (also impedance $Z_0$). Fighting both halves of the wire in **series** ($2Z_0$ total) cuts the inductive current in **half**:

$$Z_{\text{total}} = Z_0 + Z_0 = 2Z_0 \qquad \Longrightarrow \qquad i_{\text{ind}} = \frac{\Delta v_L}{Z_0 + Z_0} = \frac{1}{2}\,\frac{\Delta v_L}{Z_0}$$

Half of the total inductive voltage $\Delta v_L$ is spent pushing the left side up above $0\text{ V}$ ($+\frac{1}{2}\Delta v_L$), and the other half is spent pulling the right side down below $0\text{ V}$ ($-\frac{1}{2}\Delta v_L$). Parallel to capacitive coupling, three physical factors set the amplitude of those two opposite-sign inductive waves:

1. **The $\pm\frac{1}{2}$ series split:** Fighting $Z_0$ on the right and $Z_0$ on the left in series divides $\Delta v_L$ equally into $+\frac{1}{2}$ on the left and $-\frac{1}{2}$ on the right.
2. **The magnetic-flux sharing fraction $\frac{L_m}{L}$:** The fraction of the aggressor's magnetic flux loops that thread the victim's loop window ($L_m$) compared to the aggressor's own loop window ($L$).
3. **The aggressor voltage change during the slice transit time $\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$:** The transit time $\frac{\Delta z}{v_p}$ spent crossing slice $\Delta z$ multiplied by the aggressor's voltage slew rate.

Circuit equations confirm this result directly. Recall the mutual-induction voltage magnitude relation across the slice mutual inductance $M$ of $L_m\,\Delta z$:

$$M = L_m\,\Delta z, \qquad |\mathcal{E}_{21}(t)| = M\,\frac{di_1(t)}{dt} \qquad \Longrightarrow \qquad \Delta v_L(z, t) = (L_m\,\Delta z)\,\frac{\partial i_a(z, t)}{\partial t}$$

Dividing that inline voltage $\Delta v_L(z, t)$ equally between the backward victim impedance $Z_0$ ($+\frac{1}{2}\Delta v_L$ on the left) and forward victim impedance $Z_0$ ($-\frac{1}{2}\Delta v_L$ on the right) gives:

$$\Delta v_{b,L}(z, t) = +\frac{1}{2}\,L_m\,\Delta z\,\frac{\partial i_a(z, t)}{\partial t}, \qquad \Delta v_{f,L}(z, t) = -\frac{1}{2}\,L_m\,\Delta z\,\frac{\partial i_a(z, t)}{\partial t}$$

To express the aggressor's current slew rate $\frac{\partial i_a(z, t)}{\partial t}$ in terms of its voltage slew rate $\frac{\partial v_a(z, t)}{\partial t}$ and self-inductance $L$, recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) how a forward current wave relates to the voltage wave on a line of impedance $Z_0$, and recall the inductance identity derived earlier in this chapter:

$$i_a(z, t) = \frac{v_a(z, t)}{Z_0} \qquad \Longrightarrow \qquad \frac{\partial i_a(z, t)}{\partial t} = \frac{1}{Z_0}\,\frac{\partial v_a(z, t)}{\partial t}, \qquad \frac{1}{Z_0} = \frac{1}{v_p\,L}$$

Replacing $\frac{\partial i_a(z, t)}{\partial t}$ with $\frac{1}{v_p\,L}\,\frac{\partial v_a(z, t)}{\partial t}$ confirms the three physical factors (the $\pm\frac{1}{2}$ split, the magnetic sharing fraction $\frac{L_m}{L}$, and the slice transit time $\frac{\Delta z}{v_p}$ times the voltage slew rate):

$$\Delta v_{b,L}(z, t) = +\frac{1}{2}\,\frac{L_m}{L}\,\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$$

$$\Delta v_{f,L}(z, t) = -\frac{1}{2}\,\frac{L_m}{L}\,\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$$

#### Combining Both Mechanisms at Each Slice: The Four-Halves Accounting and Why FEXT Survives in Microstrip

Count the **four half-waves** generated at slice $\Delta z$ by both mechanisms combined: two halves from capacitance ($+\frac{1}{2}\frac{C_m}{C}$ going left and $+\frac{1}{2}\frac{C_m}{C}$ going right) plus two halves from inductance ($+\frac{1}{2}\frac{L_m}{L}$ going left and $-\frac{1}{2}\frac{L_m}{L}$ going right):

- **Going backward toward the Near End ($-z$, two halves add):** On the left side, both halves push positive charge left ($\leftarrow$), so the backward wavelet $\Delta v_b(z, t)$ is **$50\%$ ($\frac{1}{2}$) of the combined induced sum** $\left(\frac{C_m}{C} + \frac{L_m}{L}\right)$:

$$\Delta v_b(z, t) = \Delta v_{b,C}(z, t) + \Delta v_{b,L}(z, t) = \frac{1}{2}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$$

- **Going forward toward the Far End ($+z$, two halves subtract):** On the right side, the positive capacitive half ($+\frac{1}{2}\frac{C_m}{C}$) and the negative inductive half ($-\frac{1}{2}\frac{L_m}{L}$) oppose each other, so the forward wavelet $\Delta v_f(z, t)$ is **$50\%$ ($\frac{1}{2}$) of their difference**:

$$\Delta v_f(z, t) = \Delta v_{f,C}(z, t) + \Delta v_{f,L}(z, t) = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\frac{\Delta z}{v_p}\,\frac{\partial v_a(z, t)}{\partial t}$$

Opposing signs between the two forward halves raise two immediate physical questions: how any FEXT pulse survives to reach the Far End, and what a negative percentage such as $-2\%$ physically represents on the victim wire. The polarity and survival of FEXT depend on the balance between $\frac{C_m}{C}$ and $\frac{L_m}{L}$:

- **Uniform buried medium (stripline, $\frac{C_m}{C}$ equal to $\frac{L_m}{L}$, zero FEXT):** Burying both traces inside uniform fiberglass makes the capacitive and inductive fractions equal (such as $10\%$ each). On the right side, the $+5\%$ capacitive half and $-5\%$ inductive half cancel to **$0\%$** at every slice, so **zero FEXT arrives at the Far End**.
- **Bare outer surface in air (microstrip, $\frac{C_m}{C}$ smaller than $\frac{L_m}{L}$, negative FEXT):** Routing traces on the top surface puts fiberglass ($\varepsilon_r$ near $4$) below and **air** ($\varepsilon_r$ equal to $1$) above. Magnetic flux keeps $\frac{L_m}{L}$ at $10\%$ (forward half $-5\%$), whereas air weakens $\frac{C_m}{C}$ to $6\%$ (forward half $+3\%$), leaving an **uncanceled $-2\%$ negative pulse** traveling right at every slice.
- **High-permittivity overlay or capacitive tabs ($\frac{C_m}{C}$ larger than $\frac{L_m}{L}$, positive FEXT):** Coating the gap between the traces with a higher-permittivity dielectric overlay or adding small interdigitated copper fingers (capacitive compensation tabs) boosts $\frac{C_m}{C}$ above $\frac{L_m}{L}$ (such as $14\%$ versus $10\%$). The $+7\%$ capacitive half then exceeds the $-5\%$ inductive half, leaving a **$+2\%$ positive pulse** traveling right.

What does an uncanceled **$-2\%$ forward pulse** in bare microstrip physically mean and look like on the wire? On the right end of slice $\Delta z$, capacitance pushes $3\text{ units}$ of positive charge to the right ($\rightarrow$) while inductance pulls $5\text{ units}$ of positive charge to the left ($\leftarrow$), so a **net $2\text{ units}$ ($2\%$) of positive charge are pulled out of the right side**.

Pulling positive charge out of a neutral $0\text{ V}$ wire leaves behind an excess of negative electrons, dropping the local voltage **below $0\text{ V}$** (for a $+1000\text{ mV}$ aggressor step, $-2\%$ forms a **$-20\text{ mV}$ voltage trough below ground**). That $-20\text{ mV}$ local potential depression draws positive charge leftward from the next copper slice ahead of it while returning electrons flow on the reference plane underneath, propagating the **negative voltage trough forward ($\rightarrow$)** at velocity $v_p$ as a standard electromagnetic wave on the victim transmission line.

#### Why FEXT Is a Tall Narrow Spike and NEXT Is a Wide Flat Plateau: A Four-Section Timeline

Why do the wavelets arriving at the Far End (coordinate $\ell$, FEXT) form a **single narrow, tall spike** that grows taller with wire length? And why do the wavelets arriving at the Near End (zero $z$, NEXT) form a **wide, flat-topped plateau** whose ceiling height never grows past saturation?

Divide the coupled wire from left (zero $z$) to right (coordinate $\ell$) into **4 equal sections** (`Section 1`, `Section 2`, `Section 3`, `Section 4`), where a wave takes **$1\text{ ns}$** to cross each section (total one-way flight time $T_c$ equal to $4\text{ ns}$). Traveling from left to right at $1\text{ section per ns}$, the aggressor's rising edge triggers a coupled pulse in `Section 1` at $0\text{ ns}$, in `Section 2` at $1\text{ ns}$, in `Section 3` at $2\text{ ns}$, and in `Section 4` at $3\text{ ns}$.

First, follow the **forward pulses (FEXT, moving right toward the Far End)** across those 4 sections:

1. **In `Section 1` at $0\text{ ns}$:** The aggressor rising edge enters `Section 1` and creates forward `Pulse 1` on the victim wire. Both the aggressor edge and `Pulse 1` travel right at the **same speed** ($1\text{ section per ns}$), so they reach `Section 2` **at the same moment ($1\text{ ns}$)**.
2. **In `Section 2` at $1\text{ ns}$:** Right as `Pulse 1` arrives at `Section 2`, the aggressor edge creates `Pulse 2` in `Section 2`, stacking `Pulse 2` **directly on top of `Pulse 1`** (wave height `2 pulses`).
3. **In `Section 3` ($2\text{ ns}$) and `Section 4` ($3\text{ ns}$):** Both waves continue moving right together; `Pulse 3` lands directly on top of them at $2\text{ ns}$ (height `3 pulses`), and `Pulse 4` lands directly on top of them at $3\text{ ns}$ (height `4 pulses`).
4. **In the Far-End receiver at $4\text{ ns}$ ($T_c$):** All 4 pulses (`Pulse 1 + Pulse 2 + Pulse 3 + Pulse 4`) hit the Far-End receiver **at the same instant ($4\text{ ns}$)**. Stacked **vertically on top of each other**, they form a **single narrow, tall spike** of width $t_r$ whose height grows in direct proportion to wire length $\ell$.

Second, follow the **backward pulses (NEXT, moving left toward the Near End)** from those same 4 sections for a $4\text{ ns}$ rise time $t_r$ and a $+8\%$ single-slice sum $\frac{1}{2}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)$. Each $1\text{ ns}$ section experiences one-fourth ($\frac{1\text{ ns}}{4\text{ ns}}$) of the $4\text{ ns}$ voltage ramp at any instant, radiating a backward wave of height **$+2\%$** ($\frac{1}{4}$ of $+8\%$) that stays **on across the $4\text{ ns}$ rise time** and turns **off** once the section reaches steady $+V_a$:

1. **From `Section 1` ($0\text{ ns}$ away):** Backward wave arrives at the Near End starting at **$0\text{ ns}$**, stays on from $0\text{ ns}$ to $4\text{ ns}$, and **turns off at $4\text{ ns}$**.
2. **From `Section 2` ($1\text{ ns}$ away):** Out-and-back travel adds a **$2\text{ ns}$ round trip** ($1\text{ ns}$ out plus $1\text{ ns}$ back), so the wave stays on at the Near End from **$2\text{ ns}$ to $6\text{ ns}$** and **turns off at $6\text{ ns}$**.
3. **From `Section 3` ($2\text{ ns}$ away):** Out-and-back travel adds a **$4\text{ ns}$ round trip** ($2\text{ ns}$ out plus $2\text{ ns}$ back), so the wave stays on at the Near End from **$4\text{ ns}$ to $8\text{ ns}$**, turning on at $4\text{ ns}$ **right as `Section 1` turns off**.
4. **From `Section 4` ($3\text{ ns}$ away):** Out-and-back travel adds a **$6\text{ ns}$ round trip** ($3\text{ ns}$ out plus $3\text{ ns}$ back), so the wave stays on at the Near End from **$6\text{ ns}$ to $10\text{ ns}$**, turning on at $6\text{ ns}$ **right as `Section 2` turns off**.

Contrasting that arrival schedule against FEXT explains why Near-End crosstalk saturates. Propagation delay never shrinks the voltage of any individual lossless wave; every section's backward wave arrives with its full **$+2\%$** height. Instead, Near-End amplitude depends on **how many sections overlap at the Near End at the same time**:

- **Half-window ceiling ($+4\%$ rather than $+8\%$):** Overlapping all 4 sections simultaneously would produce $+8\%$ ($4$ sections at $+2\%$ each). The $2\text{ ns}$ round trip delays `Section 3` until $4\text{ ns}$, right as `Section 1` finishes its $4\text{ ns}$ rise time and turns off, so **only 2 sections (half of 4)** overlap at once ($+4\%$).
- **Flat-topped plateau across round-trip duration $2T_c$:** Holding 2 overlapping sections active at a time locks the Near-End voltage at a flat $+4\%$ ceiling across the $8\text{ ns}$ round-trip duration $2T_c$.
- **Length-independent ceiling past saturation:** Extending the wire (`Section 5`, `Section 6`, and beyond) adds later echoes at $8\text{ ns}$ and $10\text{ ns}$ right as earlier sections turn off, widening the flat plateau in time without raising its voltage ceiling.

#### Turning the Four-Section Schedule into Two Board-Design Formulas: `(Overlapping Slices) x (Voltage per Slice)`

Why turn the 4-section schedule above into two compact equations? In printed circuit board layout (as demonstrated immediately below in `Worked Example 4`), a designer needs to calculate in seconds how many millivolts of crosstalk noise will hit a receiver pin so that traces can be spaced apart before the board is fabricated. No calculus or differentiation is needed; the peak voltage at either end of the victim trace is **`(Number of Slices Overlapping at Once)` multiplied by `(Voltage from 1 Slice)`**.

First, find the **voltage from 1 slice** of flight time $\Delta t_{\text{slice}}$. Recall the single-slice backward and forward voltage equations:

$$\Delta t_{\text{slice}} = \frac{\Delta z}{v_p}$$

$$\Delta v_b = \frac{1}{2}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\Delta t_{\text{slice}}\,\frac{\partial v_a}{\partial t}$$

$$\Delta v_f = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\Delta t_{\text{slice}}\,\frac{\partial v_a}{\partial t}$$

For a digital step ramping from $0\text{ V}$ to $V_a$ over rise time $t_r$, the ramp rate $\frac{\partial v_a}{\partial t}$ is constant across the rising edge:

$$\frac{\partial v_a}{\partial t} = \frac{V_a}{t_r}$$

Substituting that constant ramp rate shows that one slice experiences the fraction $\frac{\Delta t_{\text{slice}}}{t_r}$ of the voltage ramp (in the 4-section timeline where $\Delta t_{\text{slice}}$ is $1\text{ ns}$ and $t_r$ is $4\text{ ns}$, each section experienced $\frac{1}{4}$ of the ramp):

$$\Delta v_b\text{ (from 1 slice)} = \frac{1}{2}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\left(\frac{\Delta t_{\text{slice}}}{t_r}\right)V_a$$

$$\Delta v_f\text{ (from 1 slice)} = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\left(\frac{\Delta t_{\text{slice}}}{t_r}\right)V_a$$

Multiplying the single-slice voltage by the number of slices overlapping simultaneously at each receiver yields the two board-design formulas.

First, find the **NEXT Ceiling Formula ($V_{\text{NEXT,peak}}$ at the Near End, zero $z$)**. Each slice stays active across $t_r$, while the out-and-back round trip delays each consecutive slice by $2\,\Delta t_{\text{slice}}$ ($\Delta t_{\text{slice}}$ out plus $\Delta t_{\text{slice}}$ back). Dividing the active duration $t_r$ by the round-trip spacing $2\,\Delta t_{\text{slice}}$ gives the number of slices overlapping at the Near End at the same time (2 slices in the 4-section timeline):

$$N_{\text{overlap,NEXT}} = \frac{t_r}{2\,\Delta t_{\text{slice}}}$$

Multiplying $N_{\text{overlap,NEXT}}$ by the single-slice backward voltage cancels both $\Delta t_{\text{slice}}$ and $t_r$. Combining the $\frac{1}{2}$ directional split with the $\frac{1}{2}$ round-trip overlap factor defines the dimensionless **backward coupling coefficient** $k_b$:

$$V_{\text{NEXT,peak}} = \left(\frac{t_r}{2\,\Delta t_{\text{slice}}}\right)\left[\frac{1}{2}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)\left(\frac{\Delta t_{\text{slice}}}{t_r}\right)V_a\right]$$

$$V_{\text{NEXT,peak}} = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)V_a$$

$$k_b = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right) \qquad \Longrightarrow \qquad V_{\text{NEXT,peak}} = k_b\,V_a, \qquad \text{for } 2T_c \ge t_r$$

How does this plateau behave as a function of time $t$ from start to finish? Write the aggressor input waveform as a digital step $v_w(t)$ that sits at $0\text{ V}$ before time zero, ramps linearly from $0\text{ V}$ to $+V_a$ over the rise time ($0 < t < t_r$), and stays flat at $+V_a$ thereafter ($t \ge t_r$). Subtracting a copy of that same step delayed by the full-wire round-trip time $2T_c$ writes the complete Near-End waveform in one line:

$$2T_c = \frac{2\ell}{v_p} \qquad \Longrightarrow \qquad v_{\text{NEXT}}(t) = k_b\,\Bigl[v_w(t) - v_w(t - 2T_c)\Bigr]$$

Why is $v_{\text{NEXT}}(t)$ non-zero across the middle window when subtracting $v_w(t - 2T_c)$ from $v_w(t)$, and at what instant does it return to $0\text{ V}$? Any causal step waveform is $0\text{ V}$ whenever the time argument inside its parentheses is zero or negative (before that wave arrives). Until $t$ reaches the round-trip time $2T_c$ ($8\text{ ns}$ in the 4-section timeline), the far-end echo has not returned to the Near End yet, so the delayed term $v_w(t - 2T_c)$ remains **$0\text{ V}$**. Past $2T_c$, the delayed term $v_w(t - 2T_c)$ ramps from $0\text{ V}$ to $+V_a$ (between $2T_c$ and $2T_c + t_r$), subtracting from $+V_a$ to bring the plateau back down to $0\text{ V}$:

| Time Window ($t_r = 4\text{ ns}, 2T_c = 8\text{ ns}$) | First Term $v_w(t)$ (Immediate Step) | Second Term $v_w(t - 2T_c)$ (Delayed Echo) | Resulting Near-End Voltage $v_{\text{NEXT}}(t) = k_b\,[v_w(t) - v_w(t - 2T_c)]$ |
|---|---|---|---|
| **1. Pre-step quiet state ($t \le 0$)** | Holds at $0\text{ V}$ | Holds at $0\text{ V}$ | **Holds at $0\text{ V}$** (quiet wire before switching) |
| **2. Rising front edge ($0 < t < t_r$, $0\text{ to }4\text{ ns}$)** | Ramps up from $0\text{ V}$ to $+V_a$ | Holds at $0\text{ V}$ ($t - 2T_c < 0$; far-end echo has not returned) | **Ramps up** from $0\text{ V}$ to ceiling $+k_b\,V_a$ |
| **3. Flat ceiling plateau ($t_r \le t \le 2T_c$, $4\text{ to }8\text{ ns}$)** | Holds flat at $+V_a$ | Holds at $0\text{ V}$ ($v_w(0) = 0\text{ V}$ at $t = 2T_c$) | **Holds flat** at $+k_b\,V_a$ ($k_b\,[V_a - 0] = +k_b\,V_a$) |
| **4. Falling back edge ($2T_c < t < 2T_c + t_r$, $8\text{ to }12\text{ ns}$)** | Holds flat at $+V_a$ | Ramps up from $0\text{ V}$ to $+V_a$ starting at $t = 2T_c$ | **Ramps down** from $+k_b\,V_a$ to $0\text{ V}$ as the delayed ramp subtracts |
| **5. Post-echo steady state ($t \ge 2T_c + t_r$, $\ge 12\text{ ns}$)** | Holds flat at $+V_a$ | Holds flat at $+V_a$ | **Returns to $0\text{ V}$** ($k_b\,[V_a - V_a] = 0\text{ V}$) |

Second, find the **FEXT Spike Formula ($V_{\text{FEXT,peak}}$ at the Far End, coordinate $\ell$)**. Forward wavelets travel right at the same speed $v_p$ as the aggressor edge, so zero round-trip wait occurs; **every slice along the entire wire** arrives at the Far End at the same instant $T_c$. Dividing the total one-way flight time $T_c$ by the single-slice time $\Delta t_{\text{slice}}$ gives the total number of slices stacking together at the Far End (all 4 slices in the 4-section timeline):

$$T_c = \frac{\ell}{v_p} \qquad \Longrightarrow \qquad N_{\text{overlap,FEXT}} = \frac{T_c}{\Delta t_{\text{slice}}}$$

Multiplying $N_{\text{overlap,FEXT}}$ by $\Delta v_f\text{ (from 1 slice)}$ cancels $\Delta t_{\text{slice}}$ and defines the dimensionless **forward coupling coefficient** $k_f$ (with factor $\frac{1}{2}$):

$$V_{\text{FEXT,peak}} = \left(\frac{T_c}{\Delta t_{\text{slice}}}\right)\left[\frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\left(\frac{\Delta t_{\text{slice}}}{t_r}\right)V_a\right]$$

$$V_{\text{FEXT,peak}} = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)\left(\frac{T_c}{t_r}\right)V_a$$

$$k_f = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right) \qquad \Longrightarrow \qquad V_{\text{FEXT,peak}} = k_f\,V_a\,\left(\frac{T_c}{t_r}\right) = k_f\,V_a\,\left(\frac{\ell}{v_p\,t_r}\right)$$

Comparing NEXT and FEXT side by side summarizes their physical mechanisms and board-design formulas:

| Crosstalk Property | Near-End Crosstalk (NEXT, at $z = 0$) | Far-End Crosstalk (FEXT, at $z = \ell$) |
|---|---|---|
| **Propagation direction on victim** | Backward ($-z$), opposite to aggressor wave | Forward ($+z$), co-propagating with aggressor wave |
| **Capacitive and inductive wavelet signs** | Both positive; add constructively ($\frac{C_m}{C} + \frac{L_m}{L}$) | Opposite signs; subtract ($\frac{C_m}{C} - \frac{L_m}{L}$) |
| **Number of slices overlapping at once** | Half of the rise-time window ($N_{\text{overlap}} = \frac{t_r}{2\,\Delta t_{\text{slice}}}$) due to round-trip delay | All slices along the entire wire ($N_{\text{overlap}} = \frac{T_c}{\Delta t_{\text{slice}}}$) arriving together at $t = T_c$ |
| **Coupling coefficient** | $k_b = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right)$ | $k_f = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)$ |
| **Peak voltage design formula** | $V_{\text{NEXT,peak}} = k_b\,V_a$ (for $2T_c \ge t_r$) | $V_{\text{FEXT,peak}} = k_f\,V_a\,\left(\frac{T_c}{t_r}\right)$ |
| **Waveform shape and duration** | Wide flat plateau ($v_{\text{NEXT}}(t) = k_b\,[v_w(t) - v_w(t - 2T_c)]$) | Narrow spike of duration $t_r$ arriving at $t = T_c$ |
| **Scaling with coupled length $\ell$** | Ceiling saturates at $k_b\,V_a$ once $2T_c \ge t_r$ | Spike height grows linearly with $\ell$ ($T_c = \frac{\ell}{v_p}$) |

## Worked Examples

### Worked Example 1: Case 2 and Case 3 on a Desktop Coordinate Grid

Fix a Cartesian coordinate system on a flat horizontal desk where the $+x$ axis points to the right, the $+y$ axis points toward the top of the desk, and the $+z$ axis points vertically upward out of the desk toward the viewer.

#### Case 2 (Self-Inductance on Wire A)

Wire A lies along the $x$ axis carrying a rightward ($+x$) current $i_A(t)$ that is increasing with time ($\frac{di_A(t)}{dt}$ positive). Pointing the right-hand thumb in the $+x$ direction under the Generation Rule curls the fingers upward out of the desk ($+z$) in the upper half-plane ($y$ positive) and downward into the desk ($-z$) in the lower half-plane ($y$ negative). Rising current $i_A(t)$ causes the magnetic flux density to grow in magnitude everywhere around Wire A.

Applying the Reaction Rule around Wire A requires concentric circles of induced magnetic field that oppose that growth, pointing into the desk ($-z$) in the upper half-plane ($y$ positive) and out of the desk ($+z$) in the lower half-plane ($y$ negative). Curling the right-hand **fingers** along those opposing concentric circles (into the desk above the $x$ axis and out of the desk below the $x$ axis) points the right-hand **thumb** leftward ($-x$) along the copper of Wire A, producing the self-induced back-EMF $\mathcal{E}_{\text{self}}(t)$ that resists the current rise:

$$\mathcal{E}_{\text{self}}(t) = -L_A\,\frac{di_A(t)}{dt}$$

#### Case 3 (Mutual Inductance from Wire A into Victim Loop B)

Place a parallel victim conductor, Wire B, in the lower half-plane ($y$ negative) with its own return path located farther in the $-y$ direction so that Wire B and its return path enclose a single rectangular loop window in the lower half-plane. Across that lower half-plane, the primary magnetic field from Wire A points downward into the desk ($-z$) and grows stronger as $i_A(t)$ rises.

Step 2 of the Reaction Rule requires an opposing induced magnetic field inside Victim Loop B pointing upward out of the desk ($+z$). Inside that lower-half-plane rectangle, pointing the right-hand **thumb** upward ($+z$) curls the **fingers** counter-clockwise around the perimeter of Victim Loop B as viewed from above.

Along the top edge of Loop B (Wire B, closest to Wire A), counter-clockwise circulation drives induced current from right to left ($-x$). That matches the straight-wire readout around Wire B, where curling the fingers into the desk above Wire B and out of the desk below Wire B points the thumb along $-x$. Summing the self-induced EMF from Wire B's own current $i_B(t)$ and the mutual EMF from Wire A's current $i_A(t)$ gives the total induced EMF around Loop B:

$$\mathcal{E}_B(t) = -L_B\,\frac{di_B(t)}{dt} - M\,\frac{di_A(t)}{dt}$$

### Worked Example 2: Loop Inductance of a 50 Ohm FR4 Microstrip

A standard microstrip trace on FR4 laminate has characteristic impedance $Z_0$ of $50\,\Omega$ and propagation velocity $v_p$ of $1.46 \times 10^8\text{ m/s}$ from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md). Recall the identities expressing distributed loop inductance $L$ and distributed capacitance $C$ per unit length in terms of $Z_0$ and $v_p$:

$$L = \frac{Z_0}{v_p}, \qquad C = \frac{1}{Z_0 v_p}$$

Substituting the $50\,\Omega$ impedance and $1.46 \times 10^8\text{ m/s}$ velocity into both equations yields the per-meter and per-inch line parameters ($1\text{ in}$ equals $0.0254\text{ m}$):

$$L = \frac{50\,\Omega}{1.46 \times 10^8\text{ m/s}} = 342\text{ nH/m} \approx 8.7\text{ nH/in}$$

$$C = \frac{1}{(50\,\Omega)(1.46 \times 10^8\text{ m/s})} = 137\text{ pF/m} \approx 3.5\text{ pF/in}$$

Recall the characteristic impedance relation and substitute $L$ and $C$ to verify self-consistency:

$$Z_0 = \sqrt{\frac{L}{C}} = \sqrt{\frac{342 \times 10^{-9}\text{ H/m}}{137 \times 10^{-12}\text{ F/m}}} = 50\,\Omega$$

Consider a $1\text{ in}$ ($25.4\text{ mm}$) section of this microstrip where the outbound trace has partial self-inductance $L_1$ of $14.0\text{ nH}$, the wide ground plane has partial self-inductance $L_2$ of $2.0\text{ nH}$, and the dielectric spacing establishes a mutual inductance $M$ of $3.65\text{ nH}$. Recall the total loop inductance equation:

$$L_{\text{loop}} = L_1 + L_2 - 2M$$

Substituting the three partial inductances reproduces the $8.7\text{ nH}$ loop inductance of the $1\text{ in}$ segment:

$$L_{\text{loop}} = 14.0\text{ nH} + 2.0\text{ nH} - 2(3.65\text{ nH}) = 16.0\text{ nH} - 7.3\text{ nH} = 8.7\text{ nH}$$

Thinning the dielectric laminate increases the mutual coupling $M$ to $4.5\text{ nH}$, which lowers the $1\text{ in}$ loop inductance to $7.0\text{ nH}$:

$$L_{\text{loop}} = 14.0\text{ nH} + 2.0\text{ nH} - 2(4.5\text{ nH}) = 16.0\text{ nH} - 9.0\text{ nH} = 7.0\text{ nH}$$

Recall the geometric-mean upper bound on mutual inductance:

$$M_{\text{max}} = \sqrt{L_1 L_2}$$

Substituting $L_1$ of $14.0\text{ nH}$ and $L_2$ of $2.0\text{ nH}$ limits the maximum physically achievable mutual inductance for this trace-and-plane pair:

$$M_{\text{max}} = \sqrt{(14.0\text{ nH})(2.0\text{ nH})} = \sqrt{28.0}\text{ nH} \approx 5.29\text{ nH}$$

Recall the theoretical loop inductance floor equation and substitute $M_{\text{max}}$ of $5.29\text{ nH}$ to find the minimum loop inductance achievable by thinning the dielectric alone:

$$L_{\text{loop,min}} = \left(\sqrt{L_1} - \sqrt{L_2}\right)^2 = L_1 + L_2 - 2\sqrt{L_1 L_2}$$

$$L_{\text{loop,min}} = 16.0\text{ nH} - 2(5.29\text{ nH}) \approx 5.42\text{ nH}$$

### Worked Example 3: A Narrow Trace Neck as a Lumped Series Inductor

Suppose an etching defect narrows a short segment of length $\Delta \ell$ equal to $2.0\text{ mm}$ ($2.0 \times 10^{-3}\text{ m}$) along a $50\,\Omega$ trace ($v_p$ of $1.46 \times 10^8\text{ m/s}$), raising the local characteristic impedance within the neck $Z_{\text{neck}}$ to $65\,\Omega$. Recall the identity relating distributed inductance per unit length $L$ to characteristic impedance and phase velocity:

$$L = \frac{Z_0}{v_p}$$

Multiplying the increase in distributed inductance inside the neck by the neck length $\Delta \ell$ gives the lumped excess series inductance $\Delta L_{\text{neck}}$:

$$\Delta L_{\text{neck}} = \left(\frac{Z_{\text{neck}} - Z_0}{v_p}\right)\Delta \ell$$

Substituting $Z_{\text{neck}}$ of $65\,\Omega$, $Z_0$ of $50\,\Omega$, velocity $v_p$, and length $\Delta \ell$ yields the lumped excess inductance:

$$\Delta L_{\text{neck}} = \left(\frac{65\,\Omega - 50\,\Omega}{1.46 \times 10^8\text{ m/s}}\right)(2.0 \times 10^{-3}\text{ m}) \approx 0.21\text{ nH}$$

Inserting that lumped series inductor $\Delta L_{\text{neck}}$ of $0.21\text{ nH}$ ahead of the continuing $50\,\Omega$ line sets the effective load impedance $Z_L(\omega)$ at the neck entrance to the series sum of $j\omega \Delta L_{\text{neck}}$ and $Z_0$:

$$Z_L(\omega) = Z_0 + j\omega \Delta L_{\text{neck}}$$

Recall the reflection coefficient equation from [Chapter 3](03_Impedance_Reflections_and_Termination.md):

$$\Gamma(\omega) = \frac{Z_L(\omega) - Z_0}{Z_L(\omega) + Z_0}$$

Substituting the series load impedance $Z_L(\omega)$ cancels $Z_0$ in the numerator and adds $2Z_0$ in the denominator:

$$\Gamma(\omega) = \frac{(Z_0 + j\omega \Delta L_{\text{neck}}) - Z_0}{(Z_0 + j\omega \Delta L_{\text{neck}}) + Z_0} = \frac{j\omega \Delta L_{\text{neck}}}{2Z_0 + j\omega \Delta L_{\text{neck}}}$$

Taking the complex magnitude of the numerator and the complex magnitude of the denominator gives the reflection magnitude $|\Gamma(\omega)|$ at angular frequency $\omega$ ($2\pi f$):

$$|j\omega \Delta L_{\text{neck}}| = \omega \Delta L_{\text{neck}}, \qquad |2Z_0 + j\omega \Delta L_{\text{neck}}| = \sqrt{(2Z_0)^2 + (\omega \Delta L_{\text{neck}})^2}$$

$$|\Gamma(\omega)| = \frac{\omega \Delta L_{\text{neck}}}{\sqrt{(2Z_0)^2 + (\omega \Delta L_{\text{neck}})^2}}$$

At frequency $f$ of $1\text{ GHz}$, the inductive reactance $\omega \Delta L_{\text{neck}}$ is $1.32\,\Omega$, producing a small reflection magnitude of $0.013$ ($1.3\%$):

$$\omega \Delta L_{\text{neck}}\big|_{1\text{ GHz}} = 2\pi(10^9\text{ Hz})(0.21 \times 10^{-9}\text{ H}) \approx 1.32\,\Omega$$

$$|\Gamma(1\text{ GHz})| = \frac{1.32\,\Omega}{\sqrt{(100\,\Omega)^2 + (1.32\,\Omega)^2}} \approx 0.013$$

At frequency $f$ of $10\text{ GHz}$, the inductive reactance rises tenfold to $13.2\,\Omega$, raising the reflection magnitude to $0.131$ ($13.1\%$):

$$\omega \Delta L_{\text{neck}}\big|_{10\text{ GHz}} = 2\pi(10^{10}\text{ Hz})(0.21 \times 10^{-9}\text{ H}) \approx 13.2\,\Omega$$

$$|\Gamma(10\text{ GHz})| = \frac{13.2\,\Omega}{\sqrt{(100\,\Omega)^2 + (13.2\,\Omega)^2}} \approx 0.131$$

### Worked Example 4: NEXT and FEXT in Microstrip versus Stripline

Consider two parallel $50\,\Omega$ traces coupled over a length $\ell$ of $1.0\text{ in}$ ($0.0254\text{ m}$) with propagation velocity $v_p$ of $1.46 \times 10^8\text{ m/s}$. The aggressor launches a step transition of amplitude $V_a$ equal to $1.0\text{ V}$ and rise time $t_r$ of $100\text{ ps}$. Recall the one-way coupled flight time equation and evaluate $T_c$ and the round-trip delay $2T_c$:

$$T_c = \frac{\ell}{v_p} = \frac{0.0254\text{ m}}{1.46 \times 10^8\text{ m/s}} \approx 174\text{ ps}, \qquad 2T_c \approx 348\text{ ps}$$

The round-trip delay $2T_c$ of $348\text{ ps}$ exceeds the aggressor rise time $t_r$ of $100\text{ ps}$, so the near-end crosstalk reaches its full saturated plateau height.

#### Case A: Surface Microstrip

For closely spaced surface microstrip traces where air above the board reduces capacitive coupling relative to inductive coupling, take a capacitive coupling ratio of $0.04$ and an inductive coupling ratio of $0.08$:

$$\frac{C_m}{C} = 0.04, \qquad \frac{L_m}{L} = 0.08$$

Recall the backward coupling coefficient equation and substitute both ratios:

$$k_b = \frac{1}{4}\left(\frac{C_m}{C} + \frac{L_m}{L}\right) = \frac{1}{4}(0.04 + 0.08) = 0.03$$

Recall the saturated NEXT peak equation and multiply $k_b$ by the aggressor swing $V_a$ of $1.0\text{ V}$:

$$V_{\text{NEXT,peak}} = k_b\,V_a = (0.03)(1.0\text{ V}) = +30\text{ mV}$$

Recall the peak FEXT pulse equation for a linear transition slope $V_a / t_r$:

$$V_{\text{FEXT,peak}} = \frac{1}{2}\left(\frac{C_m}{C} - \frac{L_m}{L}\right)T_c\,\left(\frac{V_a}{t_r}\right)$$

Substituting the microstrip ratios, $T_c$ of $174\text{ ps}$, $V_a$ of $1.0\text{ V}$, and $t_r$ of $100\text{ ps}$ yields a negative FEXT pulse of duration $100\text{ ps}$:

$$V_{\text{FEXT,peak}} = \frac{1}{2}(0.04 - 0.08)(174\text{ ps})\left(\frac{1.0\text{ V}}{100\text{ ps}}\right) = (-0.02)(1.74)\text{ V} \approx -34.8\text{ mV}$$

#### Case B: Homogeneous Stripline

Burying the traces inside a uniform stripline dielectric equalizes the capacitive and inductive coupling ratios at $0.06$:

$$\frac{C_m}{C} = \frac{L_m}{L} = 0.06$$

Substituting equal coupling ratios into the NEXT and FEXT equations above gives:

$$k_b = \frac{1}{4}(0.06 + 0.06) = 0.03 \qquad \Longrightarrow \qquad V_{\text{NEXT,peak}} = (0.03)(1.0\text{ V}) = +30\text{ mV}$$

$$V_{\text{FEXT,peak}} = \frac{1}{2}(0.06 - 0.06)(174\text{ ps})\left(\frac{1.0\text{ V}}{100\text{ ps}}\right) = 0\text{ mV}$$

Routing sensitive parallel buses on internal stripline layers eliminates far-end crosstalk while leaving near-end crosstalk unchanged for the same total coupling strength.

## Edge Cases

### Two Independent Geometries That Increase Inductance

Trace width $w$ and dielectric loop height $h$ both control inductance, but they act through distinct physical mechanisms that must not be conflated.

Narrowing the trace width $w$ increases the partial self-inductance $L_1$ of the trace by crowding the outbound current filaments into a smaller cross-section, which intensifies the local magnetic flux density around the wire. Increasing the dielectric height $h$ between the trace and the ground plane increases the total loop inductance $L_{\text{loop}}$ by separating the antiparallel return current farther from the outbound current, which reduces their mutual inductance $M$ and leaves a wider dielectric window of unshared magnetic flux.

A layout engineer can vary $w$ and $h$ independently. Keeping $L_{\text{loop}}$ low while holding characteristic impedance $Z_0$ at $50\,\Omega$ requires pairing a thin dielectric substrate $h$ (to maximize mutual coupling $M$) with a correspondingly narrow trace width $w$.

### Short Coupled Lengths and Unmatched Victim Terminations

#### Short Coupled Lengths ($2T_c < t_r$)

What happens physically to Near-End Crosstalk when the coupled trace section $\ell$ is so short that its round-trip propagation delay $2T_c$ is shorter than the aggressor rise time $t_r$?

In the overlapping-slices picture, reaching the full NEXT ceiling $+k_b\,V_a$ requires enough wire length for all $N_{\text{overlap,NEXT}}$ slices to overlap at the Near End at the same time (2 sections for a $4\text{ ns}$ rise time). Shortening the wire so that $2T_c < t_r$ (such as 1 section of $1\text{ ns}$ one-way flight time and $2\text{ ns}$ round-trip delay) leaves only the fraction $\frac{2T_c}{t_r}$ of the slices needed for full overlap. Equivalently, in the time-domain subtraction below, the delayed echo $v_w(t - 2T_c)$ begins subtracting at time $2T_c$ **before** the immediate step $v_w(t)$ finishes rising to $+V_a$ at time $t_r$, truncating the upward ramp at the fraction $\frac{2T_c}{t_r}$ of the full ceiling $k_b\,V_a$:

$$v_{\text{NEXT}}(t) = k_b\,\Bigl[v_w(t) - v_w(t - 2T_c)\Bigr]$$

During the overlap window ($2T_c \le t \le t_r$), both ramps rise with the same constant slope $V_a / t_r$:

$$v_w(t) = \left(\frac{V_a}{t_r}\right)t, \qquad v_w(t - 2T_c) = \left(\frac{V_a}{t_r}\right)(t - 2T_c)$$

Substituting both ramp expressions into the NEXT equation cancels the time variable $t$ and confirms that the peak NEXT voltage scales down by the ratio $2T_c / t_r$:

$$V_{\text{NEXT,short}} = k_b\left[\left(\frac{V_a}{t_r}\right)t - \left(\frac{V_a}{t_r}\right)(t - 2T_c)\right] = k_b\,V_a\,\left(\frac{2T_c}{t_r}\right), \qquad \text{for } 2T_c < t_r$$

Shortening the coupled microstrip section in Worked Example 4 from $25.4\text{ mm}$ to $5.0\text{ mm}$ reduces the round-trip delay $2T_c$ to $68.49\text{ ps}$, shorter than the $100\text{ ps}$ rise time $t_r$. Substituting $2T_c$ of $68.49\text{ ps}$ and $t_r$ of $100\text{ ps}$ into the short-line equation lowers the peak NEXT amplitude from $30\text{ mV}$ to $20.5\text{ mV}$:

$$2T_c = \frac{2(0.005\text{ m})}{1.46 \times 10^8\text{ m/s}} \approx 68.49\text{ ps}, \qquad V_{\text{NEXT,short}} = (30\text{ mV})\left(\frac{68.49\text{ ps}}{100\text{ ps}}\right) \approx 20.5\text{ mV}$$

#### Unmatched Victim Terminations

The crosstalk derivations above assume that both ends of the victim trace are terminated in matched resistors $Z_0$. An unmatched victim termination of impedance $Z_{\text{term}}$ reflects the arriving crosstalk wave according to the voltage reflection coefficient $\Gamma$ and voltage transmission coefficient $T_V$ from [Chapter 3](03_Impedance_Reflections_and_Termination.md):

$$\Gamma = \frac{Z_{\text{term}} - Z_0}{Z_{\text{term}} + Z_0}, \qquad T_V = 1 + \Gamma = \frac{2Z_{\text{term}}}{Z_{\text{term}} + Z_0}$$

An unterminated, high-impedance CMOS receiver at the far end of the victim trace (infinite $Z_{\text{term}}$) produces full positive reflection and voltage doubling at the receiver input pads:

$$\Gamma = +1, \qquad T_V = 1 + \Gamma = 2$$

Conversely, a low-impedance active driver at the near end of the victim trace ($Z_{\text{term}} < Z_0$) presents a negative reflection coefficient ($\Gamma < 0$), reflecting an inverted copy of the backward NEXT plateau and sending it traveling forward down the victim line toward the far-end receiver.

[Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md) applies the Reaction Rule inside the cross-section of a single conductor to show how internal magnetic flux forces high-frequency current onto the outer copper skin, and combines conductor loss with dielectric polarization damping to model frequency-dependent channel attenuation.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>
