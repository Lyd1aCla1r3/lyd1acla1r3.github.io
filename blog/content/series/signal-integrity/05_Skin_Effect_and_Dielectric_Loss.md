# Skin Effect and Dielectric Loss

<!-- SUMMARY: Real transmission lines dissipate wave energy into heat through frequency-dependent conductor and dielectric mechanisms. Magnetic current crowding in copper scales attenuation with the square root of frequency, whereas polar molecular friction in the laminate scales attenuation linearly with frequency, rounding fast edges and stretching pulses into long post-cursor tails. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>

[Chapter 3](03_Impedance_Reflections_and_Termination.md) showed that matching a transmission line to a $50\ \Omega$ termination resistor eliminates boundary reflections, and [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) showed that spacing adjacent traces apart suppresses electromagnetic crosstalk. Even on an isolated, reflection-free $50\ \Omega$ board trace, a crisp $1.0\text{ V}$ pulse launched at $10\text{ Gbps}$ or $25\text{ Gbps}$ arrives at the far-end receiver shrunk in height, rounded along its edges, and trailing a long voltage tail across subsequent bit intervals.

The missing signal energy does not reflect or radiate away; real circuit board materials convert propagating wave energy ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)) irreversibly into heat. Both copper conductors and fiberglass-epoxy insulators burn far more wave energy at multi-gigahertz frequencies than at low frequencies, selectively stripping away the upper Fourier harmonics ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)) that give digital transitions their steepness.

Two independent physical mechanisms drain high-frequency wave energy along every PCB interconnect. Inside the copper metal, rapidly changing magnetic fields choke off current in the interior core and crowd alternating current into a microscopic surface layer (**skin effect**, amplified by **copper surface roughness**), raising conductor attenuation in proportion to $\sqrt{f}$. Inside the insulating laminate between the trace and the ground plane, rapidly reversing electric fields twist bound polar molecules back and forth against internal polymer drag (**dielectric polarization loss**), raising insulator attenuation linearly with frequency $f$.

The sections below build each mechanism step by step from physical cause to engineering design equation. First, bulk copper resistivity and magnetic current crowding establish skin depth, surface resistance, exponential wave decay, and surface roughness. Subsequent sections examine dielectric dipole friction, post-cursor Inter-Symbol Interference (ISI), and the crossover frequency that guides stackup remedies.

## Core Concepts

### Resistivity Versus Resistance

A handheld multimeter touching the ends of a $12\text{ in}$ stripline PCB trace measures roughly $1.5\ \Omega$ of direct-current resistance, a value small enough to ignore beside a $50\ \Omega$ transmission line. At $10\text{ GHz}$, that identical strip of copper presents nearly $40\ \Omega$ of series resistance on smooth foil (and over $70\ \Omega$ on standard rough foil or single-sided microstrip), draining a substantial share of the traveling wave. Clear separation between an intrinsic property of the copper crystal (**resistivity**) and a geometric property of the current path (**resistance**) explains how solid metal multiplies its resistance nearly thirtyfold to fiftyfold without altering a single copper atom.

#### Atomic Collisions and Bulk Resistivity

Mobile conduction electrons pushed through a metal crystal by an electric field collide continuously with vibrating copper ions and lattice imperfections, converting directed kinetic energy into random thermal vibration (heat). **Bulk resistivity** $\rho_r$ (measured in ohm-meters, $\Omega\cdot\text{m}$) is an intrinsic property of the metal crystal at a given temperature, completely independent of conductor length, width, or thickness. This series writes $\rho_r$ with subscript $r$ to keep bulk resistivity distinct from the cylindrical radial coordinate $\rho$ of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md).

The reciprocal of bulk resistivity defines a second geometry-independent material property: **electrical conductivity** $\sigma$ (lowercase sigma, measured in siemens per meter, $\text{S/m}$), which quantifies how readily conduction electrons drift under an applied electric field:

$$\sigma = \frac{1}{\rho_r}$$

Standard annealed copper at room temperature has $\rho_r$ of $1.72 \times 10^{-8}\ \Omega\cdot\text{m}$ and $\sigma$ of $5.8 \times 10^7\ \text{S/m}$. Neither parameter is universally constant across the entire electromagnetic spectrum: at multi-terahertz infrared frequencies, wave polarity reverses faster than copper's $25\text{ fs}$ ($2.5 \times 10^{-14}\text{ s}$) electron collision time and electron inertia alters $\sigma$. Across all PCB and millimeter-wave signal scales from DC past $100\text{ GHz}$ (wave period of $10{,}000\text{ fs}$ or longer), electrons undergo hundreds of lattice collisions every cycle, so $\rho_r$ and $\sigma$ remain effectively constant.

#### Usable Cross-Sectional Area and DC Trace Resistance

Bulk resistivity $\rho_r$ describes the copper material itself, whereas **resistance** $R$ (measured in ohms, $\Omega$) measures the end-to-end opposition encountered by current traveling through a specific conductor of length $\ell$ (in $\text{m}$) and **usable cross-sectional area** $A$ (in $\text{m}^2$). Twice the trace length $\ell$ places twice as many atomic collision zones in series and doubles $R$, whereas twice the usable cross-sectional area $A$ opens twice as many parallel electron lanes side by side and cuts $R$ in half:

$$R = \rho_r\,\frac{\ell}{A}$$

The denominator $A$ represents the cross-sectional area of copper that the flowing current occupies, not merely the outer silhouette of the metal strip on a layout drawing. Under a steady direct current (DC), magnetic fields around the wire do not change with time and induce zero opposing voltage inside the metal ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)). Steady current spreads evenly across the full horizontal trace width $w$ and full vertical copper foil thickness $t_{\text{Cu}}$, setting the usable DC cross-sectional area $A_{\text{DC}}$ to the entire copper rectangle:

$$A_{\text{DC}} = w\,t_{\text{Cu}}$$

Division of total segment resistance $R$ by trace length $\ell$ defines the **per-unit-length DC resistance** $R_{\text{DC}}$ (measured in ohms per meter, $\Omega/\text{m}$), matching the distributed series resistance parameter of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md):

$$R_{\text{DC}} = \frac{R}{\ell} = \frac{\rho_r}{A_{\text{DC}}} = \frac{\rho_r}{w\,t_{\text{Cu}}}$$

Constant atomic resistivity $\rho_r$ across gigahertz frequencies leaves only one physical way for a trace's resistance per meter to climb nearly thirtyfold to fiftyfold at $10\text{ GHz}$. High-frequency electromagnetic fields must evict current from nearly the entire copper interior, shrinking the usable cross-sectional area $A$ to a small fraction of $A_{\text{DC}}$.

### Why a Changing Current Cannot Stay Uniform

No physical barrier blocks the center of a solid copper wire; the interior core consists of the same high-conductivity copper crystal as the outer surface. What electromagnetic force locks alternating current out of the middle of the metal while leaving direct current untouched?

[Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) established the three electromagnetic principles that govern the interior of a current-carrying wire. Electric current generates concentric magnetic field circles (Ampère's law), a solid wire carrying current fills its own copper interior with magnetic flux from inner current rings, and any time-varying magnetic flux induces a backward electric push (**back-EMF**) that opposes the current change (Faraday's and Lenz's laws).

#### Outer Ring Versus Inner Ring: Why Backward Push Is Stronger in the Core

Start in two dimensions with a single thin copper filament lying horizontally and carrying a rising current toward the right ($\rightarrow$). That rising current creates two distinct spatial patterns around the filament:

- **Sideways magnetic field (reverses direction across the filament):** By the Generation Rule, the magnetic field points out of the page ($\odot$) above the filament and flips into the page ($\otimes$) below the filament.
- **Lengthwise backward electric push (same direction everywhere):** By Faraday's and Lenz's laws, rising rightward current creates an opposing electric push (**back-EMF**) pointing **to the left** ($\leftarrow$) on **every** side of the filament, strongest right beside the filament and weakening with distance.

Arrange many such filaments into a **hollow outer copper ring** of radius $a$ at the wire's surface, all carrying rising current to the right ($\rightarrow$). Between the top wall and bottom wall of that hollow ring, the top wall pushes magnetic field into the page ($\otimes$) while the bottom wall pushes magnetic field out of the page ($\odot$), canceling the magnetic field inside the hollow interior to zero ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)).

The backward electric push behaves completely differently inside that same hollow ring because it never flips direction across a filament. Both the top wall and the bottom wall carry current rising to the right ($\rightarrow$), so **both walls push backward to the left ($\leftarrow$) in the same direction** and add together. A step closer to the top wall strengthens its leftward push by the same amount that the greater distance from the bottom wall weakens its push, producing a **flat, uniform backward push** across the entire hollow interior that slows the center core and the outer surface **equally**.

Now place a **small inner copper ring** tightly around the wire's center core, also carrying rising current to the right ($\rightarrow$). Outside that small inner ring (toward the wire's surface at radius $a$), both its top wall and bottom wall sit on the same side of an observer, so their magnetic fields add constructively across the copper interior ($0 < r < a$). Recall from [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) the internal and external magnetic flux densities of a solid cylindrical wire of outer radius $a$:

$$B_{\text{internal}}(r, t) = \frac{\mu_0\,i(t)\,r}{2\pi a^2}, \qquad B_{\text{external}}(r, t) = \frac{\mu_0\,i(t)}{2\pi r}$$

Close up at the center core, every filament of that small inner ring sits nearby and exerts a **strong** backward electric push ($\leftarrow$). Out on the wire's outer surface at radius $a$, every point sits farther away from all filaments of the inner ring at once, so the inner ring's backward push **weakens with distance**. Superposition of the outer ring and the inner ring inside a solid wire breaks the tie: the outer ring pushes backward equally on core and surface, whereas the inner ring pushes backward **much harder on the center core than on the outer surface**.

#### Internal Inductance: Why the Center Core Is a Higher-Impedance Path

Closed-loop flux accounting from [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) expresses that unequal backward push directly in terms of inductance. Every parallel copper filament inside the wire completes its closed circuit through the distant return conductor.

A filament running along the **outer copper surface** (at radius $a$) is encircled solely by the external magnetic field circles outside the wire, so its circuit loop encloses only the external magnetic flux $\Phi_{\text{ext}}(t)$. A filament running down the **center axis** (at zero radius) is encircled by all of those external field circles **plus** every internal magnetic field circle inside the copper metal, enclosing the sum of external flux $\Phi_{\text{ext}}(t)$ and internal copper flux $\Phi_{\text{int}}(t)$:

$$\Phi_{\text{surface}}(t) = \Phi_{\text{ext}}(t), \qquad \Phi_{\text{center}}(t) = \Phi_{\text{ext}}(t) + \Phi_{\text{int}}(t)$$

Recall from [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) the definition of inductance $L$ and the Faraday-Lenz self-induced back-EMF $\mathcal{E}(t)$:

$$L = \frac{\Phi_B(t)}{i(t)}, \qquad \mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt} = -L\,\frac{di(t)}{dt}$$

Division of each filament's enclosed flux by current $i(t)$ shows that the center axis carries an extra **internal inductance** $L_{\text{int}}$ on top of the surface filament's external inductance $L_{\text{ext}}$:

$$L_{\text{surface}} = L_{\text{ext}}, \qquad L_{\text{center}} = L_{\text{ext}} + L_{\text{int}} > L_{\text{surface}}$$

An external voltage source connected to the ends of the wire drives the core filaments and surface filaments in parallel. Under steady DC (zero $\frac{di(t)}{dt}$), inductive back-EMF vanishes everywhere and current divides evenly across all filaments. Under multi-gigahertz alternating current (huge $\frac{di(t)}{dt}$), the extra internal inductance $L_{\text{int}}$ down the center generates a strong opposing back-EMF that chokes off interior flow and diverts alternating current onto the lower-inductance outer skin.

#### Internal Eddy Loops Inside the Solid Wire

A longitudinal slice down the center axis of that **same solid copper wire** reveals how changing internal flux $\Phi_{\text{int}}(t)$ drives closed **eddy current loops** inside the metal. Recall the right-hand geometric rule from [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md): the **straight thumb** always tracks whichever quantity moves in a **straight line**, and the **curled fingers** always track whichever quantity wraps in a **circle or closed loop**.

The shift from Orientation A to Orientation B below does **not** come from hollow versus solid geometry; both steps occur inside the same solid conductor. Step 1 tracks a **straight** primary current creating **circular** magnetic field rings around the wire (Orientation A). Step 3 inspects each flat half-window where $\vec{B}_{\text{induced}}$ pokes **straight** through the page to drive a **closed-loop** eddy current (Orientation B). For a primary current $i(t)$ flowing right ($\rightarrow$) and increasing with time, the center axis divides the longitudinal slice into an **upper copper window** and a **lower copper window**:

1. **Primary internal magnetic field (Generation Rule, Orientation A):** Straight primary current $i(t)$ points the right-hand **thumb** right ($\rightarrow$), curling the **fingers** in circles around the axis (**out of the page** $\odot$ across the upper window and **into the page** $\otimes$ across the lower window).
2. **Opposing magnetic field (Lenz's law):** Opposition to that growing internal flux requires an induced field $\vec{B}_{\text{induced}}$ pointing **into the page** ($\otimes$) across the upper window and **out of the page** ($\odot$) across the lower window.
3. **Closed eddy loops (Reaction Rule, Orientation B):** In the upper window, the **thumb** into the page ($\otimes$) curls the **fingers** **clockwise** ($\circlearrowright$). In the lower window, the **thumb** out of the page ($\odot$) curls the **fingers** **counter-clockwise** ($\circlearrowleft$).
4. **Core cancellation and skin reinforcement:** Both closed loops flow **to the left** ($\leftarrow$) along their shared inner edge on the center axis, subtracting from $i(t)$ in the core, and return **to the right** ($\rightarrow$) along the outer copper surface, reinforcing $i(t)$ in the skin.

Comparing the center core against the outer skin summarizes how enclosed magnetic flux and internal eddy loops govern high-frequency current distribution:

| Radial Location in Wire | Encircling Magnetic Flux | Filament Inductance | Eddy Flow During Rising $i(t)$ ($\rightarrow$) | Net High-Frequency Behavior |
|---|---|---|---|---|
| **Center Core ($r = 0$)** | $\Phi_{\text{ext}}(t) + \Phi_{\text{int}}(t)$ | Maximum ($L_{\text{ext}} + L_{\text{int}}$) | Leftward ($\leftarrow$), opposing $i(t)$ | Chokes off AC amplitude and delays phase. |
| **Outer Skin ($r = a$)** | $\Phi_{\text{ext}}(t)$ only | Minimum ($L_{\text{ext}}$) | Rightward ($\rightarrow$), reinforcing $i(t)$ | Concentrates AC flow into thin outer shell. |

Each internal eddy loop forms a closed ring inside the metal that crosses any wire cross-section once forward at the surface and once backward at the core, adding **zero net current** to the total terminal current $i(t)$ supplied by the driver. Eddy currents solely redistribute existing current out of the interior and onto the surface.

#### Why Back-EMF Superposition Delays Interior Current Peaks in Time

A sinusoidal signal is **one single wave** characterized at any point by two measurable quantities: the forward driving voltage $v(t)$ and the resulting electron current $i(t)$ ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)). Probed at the same spot on an oscilloscope, $v(t)$ and $i(t)$ both oscillate at frequency $f$, yet magnetic induction shifts **when** interior current hits its peak relative to driving voltage.

Across any short wire segment, the external source applies the same forward voltage $v(t)$ across **all copper depths simultaneously**. At any single copper filament of resistance $R$, electron flow responds instantaneously to the **superposed net voltage** formed by adding the forward driving voltage $v(t)$ and the induced back-EMF $\mathcal{E}(t)$ from all changing magnetic flux $\Phi_B(t)$ encircling that filament ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)):

$$i_{\text{filament}}(t) = \frac{v(t) + \mathcal{E}(t)}{R}, \qquad \mathcal{E}(t) = -\frac{d\Phi_B(t)}{dt}$$

Right on the **outer copper skin**, zero internal copper flux encircles the filament. Without internal back-EMF, skin current rises, peaks, and falls **in step** ($0^\circ$ internal lag) with the driving push.

Inside an **interior copper filament**, Lenz's law opposes every change in enclosed internal flux across the two halves of a sinusoidal peak:

- **Before the peak (upward half-cycle):** Upward flux expansion induces a **backward** push (negative $\mathcal{E}(t)$) that subtracts from $v(t)$, holding interior current down while $v(t)$ reaches its maximum.
- **After the peak (downward half-cycle):** Downward flux collapse flips Lenz's law into a **forward** push (positive $\mathcal{E}(t)$) that adds to $v(t)$, propping interior current up after $v(t)$ begins to fall.

Subtraction during the rise paired with forward reinforcement after the peak shifts the superposed net interior current peak **later in time** (**phase lag**).

Deeper layers are **not** triggered sequentially one after another; all depths are driven at once, and simultaneous **superposition** of all induced fields sets both amplitude and timing at each depth. A shallow filament encloses only the outermost skin flux, shifting its peak slightly late. A deeper filament is encircled both by more total copper flux and by intermediate layers whose own currents already peak late. Their delayed Lenz reactions shift the superposed net push inside the core **progressively later in phase** with depth.

### Skin Depth and Exponential Current Decay

Round wires rarely appear on circuit boards; real interconnects use flat rectangular copper strips routed over flat copper ground planes. A quantitative model of the active current layer on a PCB trace defines the trace's physical dimensions, balances copper resistance against internal inductance to find the **skin depth** $\delta$, and tracks how current decays inward from the surface.

#### Trace Dimensions Versus Inward Copper Depth

Four macroscopic dimensions define a rectangular PCB trace suspended above its return ground plane:

- **Trace length $\ell$ (in $\text{m}$):** Longitudinal distance along the wave propagation axis $z$ from transmitter to receiver.
- **Trace width $w$ (in $\text{m}$):** Horizontal side-to-side width of the copper strip across the board (typically $100\ \mu\text{m}$, roughly $4\text{ mil}$).
- **Copper foil thickness $t_{\text{Cu}}$ (in $\text{m}$):** Vertical thickness of the copper metal itself from its bottom face to its top face (typically $35\ \mu\text{m}$ for standard $1\text{ oz}$ copper foil).
- **Dielectric gap thickness $d_{\text{gap}}$ (in $\text{m}$):** Vertical thickness of the fiberglass-epoxy insulator separating the bottom copper face of the trace from the top copper face of the ground plane underneath (written $d_{\text{gap}}$ here for the dielectric height $h$ of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) and [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)).

To track how alternating current distributes inside the $35\ \mu\text{m}$ copper foil, measure **inward copper depth** $x$ (in $\text{m}$ or $\mu\text{m}$) starting at zero on the active copper face closest to the ground plane and stepping vertically inward into the metal away from the ground plane. Why does a flat rectangular trace crowd high-frequency current onto its bottom face rather than spreading current evenly across all horizontal layers of the $35\ \mu\text{m}$ foil?

Return current $-i(t)$ flows on the ground plane directly beneath the trace across the dielectric gap $d_{\text{gap}}$ ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)). A horizontal filament right on the bottom copper face of the trace (zero depth $x$) forms a closed loop of height $d_{\text{gap}}$ with the ground plane, enclosing **only** the magnetic flux inside the insulating gap. A horizontal filament deeper inside the copper foil at inward depth $x$ sits farther from the ground plane at total distance $d_{\text{gap}} + x$; its taller return loop encloses all of the gap flux **plus** the internal magnetic flux inside the copper between zero and $x$.

Higher enclosed flux at greater depth $x$ gives deeper horizontal layers higher loop inductance and stronger opposing back-EMF, choking off current in the upper interior of the foil and pulling microstrip current onto the bottom face closest to the ground plane. In a symmetric buried stripline sandwiched halfway between an upper ground plane and a lower ground plane, the middle of the foil ($t_{\text{Cu}} / 2$) sits farthest from both return planes and experiences maximum back-EMF, crowding high-frequency current equally onto **both** the top and bottom copper faces.

#### Why Skin Depth Cannot Shrink to Zero: Resistive Pushback Versus Inductive Choking

At first glance, minimum inductance right at the outer boundary suggests that $100\%$ of an alternating current should crowd into an infinitely thin atomic sheet of zero thickness on the copper surface. Why does current instead penetrate a finite **skin depth** $\delta$ into the metal?

Two opposing physical mechanisms fight each other across a surface current shell of length $\ell$, width $w$, and inward thickness $\delta$ at sinusoidal frequency $f$:

- **Copper resistance pushes current to spread inward:** Confinement into a thinner surface shell of thickness $\delta$ shrinks the cross-sectional area $w\,\delta$ and drives ohmic resistance $R_{\text{shell}}(\delta)$ upward, creating a resistive voltage drop along the surface that pushes electrons into the less-crowded copper underneath.
- **Internal inductance pushes current to crowd outward:** Magnetic field entering the shell tapers from maximum at the surface to zero at depth $\delta$, giving an average flux depth of $\delta / 2$ and an internal inductive reactance $X_{\text{int}}(\delta)$ that grows with $\delta$ and $f$ to block deeper flow.

Recall the geometric conductor resistance equation applied to a rectangular surface layer of length $\ell$, width $w$, and thickness $\delta$:

$$R_{\text{shell}}(\delta) = \rho_r\,\frac{\ell}{w\,\delta}$$

Recall from [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) the parallel-plate inductance formula and from [Chapter 3](03_Impedance_Reflections_and_Termination.md) the inductive reactance magnitude at frequency $f$, applied across the effective internal flux thickness $\delta / 2$ of non-magnetic copper ($\mu_0$):

$$L_{\text{int}}(\delta) = \mu_0\,\frac{(\delta / 2)\,\ell}{w} \qquad \Longrightarrow \qquad X_{\text{int}}(\delta) = 2\pi f\,L_{\text{int}}(\delta) = \pi f \mu_0\,\frac{\delta\,\ell}{w}$$

At depths much shallower than $\delta$, resistive crowding outweighs tiny inductive opposition and current spreads deeper; beyond $\delta$, growing inductive reactance overpowers resistance and chokes off interior flow. The natural penetration boundary **$\delta$ (the skin depth)** is the thickness where internal inductive reactance matches ohmic shell resistance:

$$X_{\text{int}}(\delta) = R_{\text{shell}}(\delta) \qquad \Longrightarrow \qquad \pi f \mu_0\,\frac{\delta\,\ell}{w} = \rho_r\,\frac{\ell}{w\,\delta}$$

Trace length $\ell$ and trace width $w$ cancel from both sides. Thickness $\delta$ sits in the numerator of inductive reactance (thicker layer encloses more flux) and in the denominator of resistance (thicker layer opens more parallel area), so cross-multiplying produces $\delta^2$:

$$\delta^2 = \frac{\rho_r}{\pi f \mu_0}$$

The positive square root defines the **skin depth** $\delta$ (measured in meters, $\text{m}$, or micrometers, $\mu\text{m}$) for non-magnetic conductors such as copper:

$$\delta = \sqrt{\frac{\rho_r}{\pi f \mu_0}}$$

Every variable inside that square root reflects a direct physical cause and effect:

- **Higher resistivity $\rho_r$ in the numerator makes $\delta$ larger:** A more resistive metal (such as brass or titanium) builds stronger resistive pushback at the surface while weakening internal eddy currents, forcing current to penetrate deeper into the metal.
- **Higher frequency $f$ in the denominator makes $\delta$ smaller:** Faster current oscillation accelerates magnetic flux changes per cycle and strengthens Faraday back-EMF; because of the square root, **quadrupling the signal frequency ($4\times f$) cuts the skin depth in half ($\delta / 2$)**.
- **Magnetic permeability $\mu_0$ in the denominator makes $\delta$ smaller:** Substitution of $\mu_0 \mu_r$ for $\mu_0$ in ferromagnetic metals such as nickel or steel ($\mu_r \gg 1$) amplifies internal flux density and squeezes current into an ultra-thin, high-resistance skin, which is why magnetic nickel barriers on RF connector pins inflate high-frequency loss.

#### Exponential Amplitude Decay With Depth

Current inside a thick copper foil does not stop abruptly at a sharp internal wall at depth $\delta$. Different depths carry different amounts of current, so local flow at depth $x$ is measured by the **current density** $J(x, t)$ (in amperes per square meter, $\text{A/m}^2$), defined as the current $\Delta i(x, t)$ flowing through a thin cross-sectional strip divided by its strip area $\Delta A$:

$$J(x, t) = \frac{\Delta i(x, t)}{\Delta A}$$

Slice a thick copper conductor ($t_{\text{Cu}} \gg \delta$) conceptually from the active surface inward into identical horizontal layers of thickness $\Delta x$. An inward step across the first layer (zero depth to $\Delta x$) encloses that layer's eddy-current flux, whose superposed back-EMF cancels a fixed percentage of the surface current amplitude $J_0$. Below depth $\Delta x$, the remaining thick copper has the same resistivity $\rho_r$, permeability $\mu_0$, and frequency $f$ as at the surface, scaled down in net current amplitude. By linearity of Maxwell's equations, superposed eddy flux across the second step $\Delta x$ cancels the **same percentage** of the remaining net current, and every subsequent step $\Delta x$ repeats that identical fractional reduction.

Equal fractional loss across every identical step of depth produces **exponential decay** scaled by the skin depth $\delta$:

$$|J(x)| = J_0\,e^{-x/\delta}$$

Evaluation of $e^{-x/\delta}$ at integer multiples of $\delta$ shows how rapidly the interior copper empties out. At one skin depth ($x$ equal to $\delta$), current density falls to $e^{-1}$ (roughly $36.8\%$) of its surface value $J_0$. At three skin depths ($3\delta$), current density falls to $e^{-3}$ (roughly $5.0\%$), and by five skin depths ($5\delta$) less than $e^{-5}$ (roughly $0.7\%$) remains. Across any finite inward step $\Delta x$ into the metal, subtracting the surviving amplitude ratio from unity gives the canceled amplitude fraction:

$$\text{Fraction Canceled Across }\Delta x = 1 - \frac{|J(x + \Delta x)|}{|J(x)|} = 1 - e^{-\Delta x/\delta}$$

Across a single $1.0\ \mu\text{m}$ step into annealed copper, eddy-current cancellation climbs from $1.5\%$ at $1\text{ MHz}$ ($\delta$ of $66.0\ \mu\text{m}$) to $38.0\%$ at $1\text{ GHz}$ ($\delta$ of $2.09\ \mu\text{m}$) and $78.0\%$ at $10\text{ GHz}$ ($\delta$ of $0.66\ \mu\text{m}$).

#### Linear Phase Delay With Depth and Current Reversal

Amplitude decay is only half of what changes with inward depth $x$; peak timing shifts at the same spatial rate. Across any thin step $\Delta x$, induced back-EMF alters current in two ways at once: an **in-phase opposition** that shrinks peak height, and a **quarter-cycle Lenz shift** (subtracting before the peak, adding after) that delays peak timing.

Skin depth $\delta$ was derived earlier as the thickness where internal inductive reactance matches ohmic shell resistance. Equal inductive and resistive opposition splits each inward step $\Delta x / \delta$ equally between fractional amplitude loss and radian phase lag. Across one full skin depth ($x$ equal to $\delta$), the timing delay equals **one radian** (one $360^\circ$ cycle spans $2\pi$ or $6.283\text{ radians}$, so $1\text{ radian}$ equals $57.3^\circ$ or roughly one-sixth of a cycle):

$$\phi_{\text{lag}}(x) = \frac{x}{\delta}\ \text{radians}$$

Multiplication of the amplitude envelope $J_0\,e^{-x/\delta}$ by a unit cosine at angular frequency $\omega$ ($2\pi f$) delayed by $\phi_{\text{lag}}(x)$ writes the steady-state current density $J(x, t)$:

$$J(x, t) = J_0\,e^{-x/\delta}\cos\!\left(\omega t - \frac{x}{\delta}\right)$$

A **minus sign** inside $\cos(\omega t - x/\delta)$ represents a **later** arrival in time. A cosine hits its $+1$ peak where its interior angle equals zero, occurring at $t$ of $0$ on the outer surface ($x$ of $0$). At one skin depth inward ($x$ equal to $\delta$), $\omega t - 1$ reaches zero only after the clock advances further to $\omega t$ of $+1\text{ radian}$ ($t$ equal to $1 / \omega$ later).

Evaluation of both factors in $J(x, t)$ at inward depth $\pi\delta$ (roughly $3.14\,\delta$) shows what happens once phase lag reaches half a cycle ($\pi\text{ radians}$, or $180^\circ$, where $\cos(\omega t - \pi)$ flips sign to $-\cos(\omega t)$):

$$J(\pi\delta, t) = J_0\,e^{-\pi\delta / \delta}\cos\!\left(\omega t - \frac{\pi\delta}{\delta}\right) = J_0\,e^{-\pi}\cos(\omega t - \pi) = -0.043\,J_0\cos(\omega t)$$

At the instant surface current peaks forward ($+J_0$ to the right at $t$ of $0$), the remaining $4.3\%$ trickle at depth $\pi\delta$ ($e^{-\pi}$ of $0.043$) carries a **minus sign** and flows **backward to the left**. Under simultaneous superposition, the delayed Lenz reactions from overlying copper layers between $0$ and $\pi\delta$ momentarily outweigh the direct source push in the opposite direction. That backward trickle subtracts from net forward current delivered to the receiver while still burning resistive lattice heat, directly motivating the equivalent skin-shell model below.

### Equivalent Skin Layer, Surface Resistance, and AC Trace Resistance

Board designers sizing traces for a $25\text{ Gbps}$ channel need a direct geometric resistance formula rather than an exponential depth profile. A geometric link from that exponential distribution back to conductor cross-section answers two practical layout questions: why thicker copper foil fails to reduce gigahertz loss, and why wider traces succeed.

#### Measuring AC Heating With Root-Mean-Square Current

The geometric resistance formula ($R$ equal to $\rho_r\ell / A$) assumes current fills an area $A$ evenly, yet high-frequency current inside copper fades smoothly with depth and lags in timing. How does a circuit assign a single effective resistance $R_{\text{eff}}$ to a wire whose internal current is uneven?

First, **net current** $i(t)$ means the total forward current entering and leaving the ends of the wire once all horizontal copper layers are added together. For an alternating sine wave $i(t)$ swinging between $+I_{\text{peak}}$ and $-I_{\text{peak}}$, a plain average over one cycle equals zero because the positive and negative halves cancel. Heat does **not** cancel to zero: electrons crash into copper atoms during both forward flow ($+i$) and reverse flow ($-i$), because instantaneous heating power $p(t)$ depends on current **squared** ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)):

$$p(t) = \bigl[i(t)\bigr]^2\,R_{\text{eff}} = I_{\text{peak}}^2\cos^2(\omega t)\,R_{\text{eff}}$$

The square turns negative half-cycles positive. Over one full cycle, $\cos^2(\omega t)$ swings symmetrically between $0$ and $1$, placing its cycle average (mean) halfway between $0$ and $1$ at one-half ($1/2$). Average heating power $P_{\text{heat}}$ of a sinusoidal current is half that of a steady DC current equal to $I_{\text{peak}}$:

$$P_{\text{heat}} = \frac{1}{2}\,I_{\text{peak}}^2\,R_{\text{eff}}$$

To write AC heating in the same form as DC heating ($I^2 R$), circuits define the **root-mean-square (RMS) current** $I_{\text{rms}}$ as the steady DC current that burns the same average heat. The three words in root-mean-square apply in reverse order from right to left (**Square** the wave, take the cycle **Mean**, then take the square **Root**):

$$I_{\text{rms}} = \sqrt{\frac{1}{2}\,I_{\text{peak}}^2} = \frac{I_{\text{peak}}}{\sqrt{2}} \approx 0.707\,I_{\text{peak}}$$

A sine wave peaking at $10\text{ mA}$ has an $I_{\text{rms}}$ of $7.07\text{ mA}$ and heats the copper trace at the same wattage as $7.07\text{ mA}$ of steady DC. Substitution of $I_{\text{rms}}^2$ for $\frac{1}{2}\,I_{\text{peak}}^2$ defines effective resistance $R_{\text{eff}}$ (and **Joule heating** $P_{\text{heat}}$) directly from total heat burned divided by squared net RMS current:

$$P_{\text{heat}} = I_{\text{rms}}^2\,R_{\text{eff}} \qquad \Longrightarrow \qquad R_{\text{eff}} = \frac{P_{\text{heat}}}{I_{\text{rms}}^2}$$

#### The Equivalent Uniform Skin Shell

Applying that $P_{\text{heat}} / I_{\text{rms}}^2$ test identifies what uniform copper thickness matches the smooth skin curve $J(x, t)$. Comparing the real conductor against a reference **flat box of thickness $\delta$** carrying uniform, in-phase surface density from $x$ of $0$ to $\delta$ (zero deeper than $\delta$) relates heat $P_{\text{box}}$, net RMS current $I_{\text{box}}$, and shell resistance $R_{\text{shell}}(\delta)$:

$$R_{\text{shell}}(\delta) = \frac{P_{\text{box}}}{I_{\text{box}}^2} = \rho_r\,\frac{\ell}{w_{\text{eff}}\,\delta}$$

First consider exponential spreading alone, temporarily ignoring phase lag. Without phase lag, the total area under $J_0\,e^{-x/\delta}$ across all depths equals $J_0\,\delta$ (the tail past $\delta$ fills the missing upper corner inside $\delta$), matching the net current $I_{\text{box}}$ of the flat box. Why does spreading that same total current across more copper depth burn **less** heat? Heat scales with current **squared** ($I^2 R$): packing $2\text{ A}$ into a single $1\ \Omega$ copper lane burns $(2\text{ A})^2(1\ \Omega)$, or $4\text{ W}$. Equal division of that $2\text{ A}$ into $1\text{ A}$ per lane across two $1\ \Omega$ lanes burns $1\text{ W}$ plus $1\text{ W}$, or $2\text{ W}$ (half the heat).

In the same way, shifting current out of the crowded inner region ($0 < x < \delta$) into the low-density tail slashes $J^2$ everywhere. At depth $\delta$, current density is $0.37\,J_0$ while squared density is just $0.14\,J_0^2$, and at $2\delta$ squared density drops to $0.02\,J_0^2$. Algebraically, squaring $e^{-x/\delta}$ doubles the exponent, compressing the horizontal decay width from $\delta$ down to $\delta / 2$:

$$\bigl(e^{-x/\delta}\bigr)^2 = e^{-2x/\delta} = e^{-x / (\delta / 2)}$$

Horizontal compression of that exponential curve to half its width ($\delta / 2$ instead of $\delta$) at the same starting height cuts the area under the curve in half. Total heat summed across all depths therefore equals **one-half** of the flat box's heat ($P_{\text{heat}}$ equal to $\frac{1}{2}\,P_{\text{box}}$).

Next restore progressive phase lag ($\cos(\omega t - x/\delta)$). Timing delay does not change how much heat each individual copper layer burns, leaving $P_{\text{heat}}$ at $\frac{1}{2}\,P_{\text{box}}$. Summation of all layers into net wire current, by contrast, adds waves that never peak at the same instant. Two equal waves separated by phase angle $\Delta\phi$ reach their combined peak halfway between at $\frac{1}{2}\,\Delta\phi$; symmetric cosine roll-off places both waves at height $\cos(\frac{1}{2}\,\Delta\phi)$, retaining $100\%$ at $0^\circ$, $70.7\%$ at $90^\circ$, and $0\%$ at $180^\circ$.

Right at the outer surface ($x$ of $0$), zero overlying flux is enclosed, so surface driving voltage $V_{\text{surf}}$ sets $J_0$ directly. Inside the inductance-free flat box, Ohm's law relates $V_{\text{surf}}$ to $I_{\text{box}}$ and $R_{\text{shell}}(\delta)$, while the real conductor opposes current across $\delta$ with equal inductive reactance and shell resistance:

$$V_{\text{surf}} = I_{\text{box}}\,R_{\text{shell}}(\delta), \qquad X_{\text{int}}(\delta) = R_{\text{shell}}(\delta)$$

For net wire current $I_{\text{rms}}$, resistive voltage drop $I_{\text{rms}}\,R_{\text{shell}}(\delta)$ (peaking with current) and inductive Faraday drop $I_{\text{rms}}\,X_{\text{int}}(\delta)$ (peaking $90^\circ$ earlier, at steepest current slope) form two equal waves separated by $\Delta\phi$ of $90^\circ$. Application of the $\cos(45^\circ)$ ($1/\sqrt{2}$) rule sums those two drops to $V_{\text{surf}}$:

$$V_{\text{surf}} = 2\,I_{\text{rms}}\,R_{\text{shell}}(\delta)\cos(45^\circ) = \frac{2}{\sqrt{2}}\,I_{\text{rms}}\,R_{\text{shell}}(\delta) = \sqrt{2}\,I_{\text{rms}}\,R_{\text{shell}}(\delta)$$

Substitution of $I_{\text{box}}\,R_{\text{shell}}(\delta)$ for $V_{\text{surf}}$ cancels $R_{\text{shell}}(\delta)$ and proves that $90^\circ$ inductive-resistive opposition cuts net RMS current by $\sqrt{2}$ ($70.7\%$) and cuts **squared** net current in half:

$$\sqrt{2}\,I_{\text{rms}} = I_{\text{box}} \qquad \Longrightarrow \qquad I_{\text{rms}} = \frac{I_{\text{box}}}{\sqrt{2}} \approx 0.707\,I_{\text{box}} \qquad \Longrightarrow \qquad I_{\text{rms}}^2 = \frac{1}{2}\,I_{\text{box}}^2$$

Inductive reactance stores and returns magnetic energy each quarter-cycle without burning heat, so effective resistance still comes from dividing heat burned ($P_{\text{heat}}$) by squared net current ($I_{\text{rms}}^2$). Tail spreading cuts heat in half while phase lag cuts squared net current in half, canceling both factors of $1/2$:

$$P_{\text{heat}} = \frac{1}{2}\,P_{\text{box}}, \qquad I_{\text{rms}}^2 = \frac{1}{2}\,I_{\text{box}}^2$$

$$R_{\text{eff}} = \frac{\frac{1}{2}\,P_{\text{box}}}{\frac{1}{2}\,I_{\text{box}}^2} = \frac{P_{\text{box}}}{I_{\text{box}}^2} = R_{\text{shell}}(\delta)$$

**A thick conductor carrying an exponentially decaying, phase-lagging AC skin current exhibits the same electrical resistance as a uniform, in-phase current confined entirely within a rectangular surface shell of thickness $\delta$.**

Let $w_{\text{eff}}$ denote the **effective active perimeter width** of that skin shell:

- **Surface microstrip ($w \gg t_{\text{Cu}}$):** Return-loop proximity pulls nearly all high-frequency current onto the bottom horizontal face facing the ground plane, giving an active perimeter width $w_{\text{eff}}$ of approximately $w$.
- **Symmetric buried stripline ($w \gg t_{\text{Cu}}$):** Equal proximity to the upper and lower ground planes splits current evenly across both the top and bottom horizontal faces, doubling the active perimeter width $w_{\text{eff}}$ to approximately $2w$.

The product of active perimeter width $w_{\text{eff}}$ and one skin depth $\delta$ defines the **usable AC cross-sectional area** $A_{\text{AC}}$:

$$A_{\text{AC}} = w_{\text{eff}}\,\delta$$

Recall the geometric conductor resistance equation from the start of the chapter:

$$R = \rho_r\,\frac{\ell}{A}$$

Substitution of $A_{\text{AC}}$ for $A$ and division by trace length $\ell$ yield the **per-unit-length AC resistance** $R_{\text{AC}}$ (in $\Omega/\text{m}$):

$$R_{\text{AC}} = \frac{R}{\ell} = \frac{\rho_r}{A_{\text{AC}}} = \frac{\rho_r}{w_{\text{eff}}\,\delta}$$

#### Why Copper Foil Thickness Stops Helping While Trace Width Still Helps

Consider sending $10\text{ mA}$ of signal current down a $35\ \mu\text{m}$-thick microstrip trace. At DC, those $10\text{ mA}$ spread calmly across the full $35\ \mu\text{m}$ foil thickness. At $10\text{ GHz}$ ($\delta$ of $0.66\ \mu\text{m}$), internal back-EMF locks current out of the upper $98\%$ of the metal and jams all $10\text{ mA}$ into a bottom skin $0.66\ \mu\text{m}$ thick, just $1/53\text{rd}$ of the foil thickness.

Confinement of the same total current into $1/53\text{rd}$ of the copper area multiplies electron traffic density fifty-three-fold inside that thin skin. Resistive lattice heating per unit volume scales with the square of local current density. Fifty-three-fold higher density inside $1/53\text{rd}$ of the volume burns $53\times$ more heat per meter, raising trace resistance fifty-three-fold while $34.3\ \mu\text{m}$ of interior copper sits idle.

The two cross-sectional dimensions of the trace play opposite roles in the denominator of $R_{\text{AC}}$:

- **Copper foil thickness $t_{\text{Cu}}$ disappears from the denominator:** Fabrication with $2\text{ oz}$ copper ($70\ \mu\text{m}$) instead of $1\text{ oz}$ copper ($35\ \mu\text{m}$) adds $35\ \mu\text{m}$ of unused interior metal that gigahertz signals never enter, reducing high-frequency resistance by $0\%$.
- **Trace width $w$ sits directly in the denominator:** Twice the horizontal trace width $w$ stretches the active outer skin sideways ($w_{\text{eff}}$ doubles), opening twice as many parallel surface lanes and cutting high-frequency AC resistance in half.

#### Surface Resistance ("Ohms per Square") and Square-Root Frequency Scaling

Confinement of gigahertz current to a surface film of fixed thickness $\delta$ turns every thick copper surface into a two-dimensional resistive sheet. A square patch of any size cut from that copper surface has path length $\ell$ equal to active width $w_{\text{eff}}$. A tenfold larger square places ten times more copper length in series while simultaneously opening ten times more parallel width, canceling patch dimensions completely:

$$R = \rho_r\,\frac{\ell}{w_{\text{eff}}\,\delta} \qquad \Longrightarrow \qquad R_s = \frac{\rho_r}{\delta} \quad (\text{for } \ell = w_{\text{eff}})$$

That size-independent resistance of one square patch defines the **surface resistance** (or **sheet resistance**) $R_s$ (measured in $\Omega$, commonly spoken as **ohms per square**). Recall the copper skin depth equation derived in the previous section:

$$\delta = \sqrt{\frac{\rho_r}{\pi f \mu_0}}$$

Substitution of $\delta$ into $R_s$ moves $\rho_r$ inside the radical as $\rho_r^2$ and reveals the **square-root frequency scaling** of conductor skin resistance:

$$R_s = \frac{\rho_r}{\sqrt{\frac{\rho_r}{\pi f \mu_0}}} = \sqrt{\frac{\rho_r^2\,\pi f \mu_0}{\rho_r}} = \sqrt{\pi f \mu_0 \rho_r}$$

A fourfold jump in signal frequency ($4\times f$) strengthens magnetic induction enough to halve the skin depth ($\delta / 2$), halving the usable copper area and **doubling** ($2\times$) the surface resistance. Recall the per-unit-length AC resistance equation and replace $\rho_r / \delta$ with $R_s$ to count how many squares of width $w_{\text{eff}}$ fit in series along one meter of trace:

$$R_{\text{AC}} = \frac{\rho_r}{w_{\text{eff}}\,\delta} = \frac{R_s}{w_{\text{eff}}} = \frac{\sqrt{\pi f \mu_0 \rho_r}}{w_{\text{eff}}}$$

Evaluation of $\delta$ and $R_s$ for annealed copper ($\rho_r$ of $1.72 \times 10^{-8}\ \Omega\cdot\text{m}$, $\mu_0$ of $4\pi \times 10^{-7}\ \text{H/m}$) across six benchmark frequencies tracks how quickly the active copper shrinks:

| Frequency ($f$) | Copper Skin Depth ($\delta$) | Surface Resistance ($R_s$) | Active Share of a $35\ \mu\text{m}$ ($1\text{ oz}$) Microstrip Foil |
|---|---|---|---|
| $1\text{ MHz}$ | $66.0\ \mu\text{m}$ | $0.26\text{ m}\Omega$ | $100\%$ of foil active; skin depth exceeds the $35\ \mu\text{m}$ thickness. |
| $100\text{ MHz}$ | $6.60\ \mu\text{m}$ | $2.61\text{ m}\Omega$ | $19\%$ of foil active inside the bottom $6.6\ \mu\text{m}$ shell. |
| $1\text{ GHz}$ | $2.09\ \mu\text{m}$ | $8.24\text{ m}\Omega$ | $6.0\%$ of foil active inside the bottom $2.1\ \mu\text{m}$ shell. |
| $5\text{ GHz}$ | $0.93\ \mu\text{m}$ | $18.4\text{ m}\Omega$ | $2.7\%$ of foil active; $\delta$ drops below $1\ \mu\text{m}$ where surface teeth dominate. |
| $10\text{ GHz}$ | $0.66\ \mu\text{m}$ | $26.1\text{ m}\Omega$ | $1.9\%$ of foil active; a $100\times$ jump from $100\text{ MHz}$ raises $R_s$ tenfold. |
| $15\text{ GHz}$ | $0.54\ \mu\text{m}$ | $31.9\text{ m}\Omega$ | $1.5\%$ of foil active inside a sub-micron bottom film. |

### The Skin Effect as a Low-Pass Filter

Why does rising AC resistance distort the shape of digital bits rather than shrinking the entire waveform uniformly? [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) established that a digital data stream is a bundle of many sinusoidal frequencies traveling together: low frequencies sustain flat voltage rails during long runs of identical bits, whereas multi-gigahertz harmonics construct steep rising and falling edges and narrow single-bit pulses.

Inside the same copper trace, each frequency component encounters a different usable cross-sectional area. Low-frequency components spread across nearly the full $35\ \mu\text{m}$ foil, face minimal resistance, and reach the receiver almost intact. Multi-gigahertz edge harmonics squeeze themselves into a sub-micron skin, encounter high resistance proportional to $\sqrt{f}$, and convert much of their energy into copper heat. Without a single discrete capacitor or inductor on the board, a plain copper trace acts as a **continuous low-pass filter** that selectively strips fast edge harmonics out of the signal.

#### Why Constant Resistance per Meter Produces Exponential Wave Decay

A uniform trace has the same AC resistance $R_{\text{AC}}$ on its first inch and on its twelfth inch, yet wave voltage does not drop along a straight line. Unlike a DC current source that forces fixed current through series resistors, a traveling wave carries **its own finite energy supply** ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)). Heat dissipated in the first inch shrinks both the wave's voltage $V_{\text{rms}}(z)$ and current $I_{\text{rms}}(z)$ before the wave enters the second inch, so the weaker wave burns fewer absolute milliwatts in the second inch while always losing the **same fixed percentage** of whatever wave power remains.

Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) and [Chapter 3](03_Impedance_Reflections_and_Termination.md) how forward wave voltage $V_{\text{rms}}(z)$, wave current $I_{\text{rms}}(z)$, and cycle-averaged wave power $P(z)$ relate on a transmission line of characteristic impedance $Z_0$:

$$V_{\text{rms}}(z) = Z_0\,I_{\text{rms}}(z), \qquad P(z) = V_{\text{rms}}(z)\,I_{\text{rms}}(z) = I_{\text{rms}}^2(z)\,Z_0 = \frac{V_{\text{rms}}^2(z)}{Z_0}$$

Across a short trace slice $\Delta z$, series copper resistance per meter $R_{\text{AC}}$ carries wave current $I_{\text{rms}}(z)$ and dissipates current-driven heat. Parallel dielectric shunt conductance per meter $G$ (in siemens per meter, $\text{S/m}$, from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md), derived from dipole friction below) sits across wave voltage $V_{\text{rms}}(z)$ and dissipates voltage-driven heat:

$$\Delta P(z) = -\Bigl[I_{\text{rms}}^2(z)\,R_{\text{AC}} + V_{\text{rms}}^2(z)\,G\Bigr]\Delta z$$

Division of the copper term by $I_{\text{rms}}^2(z)\,Z_0$ and the dielectric term by $V_{\text{rms}}^2(z) / Z_0$ cancels the local wave amplitude and isolates the **fractional power lost per meter**:

$$\frac{\Delta P(z)}{P(z)} = -\left(\frac{R_{\text{AC}}}{Z_0} + G\,Z_0\right)\Delta z$$

Characteristic impedance $Z_0$ enters those two loss terms in opposite positions for direct physical reasons:

- **Copper loss divides by $Z_0$:** Copper heating ($I^2 R_{\text{AC}}$) is driven by series **current**. A higher-$Z_0$ line (such as $75\ \Omega$ cable-television coax versus $50\ \Omega$ coax) transmits the same wave power at higher voltage and *lower current*, cutting copper heat loss per meter.
- **Dielectric loss multiplies by $Z_0$:** Dielectric heating ($V^2 G$) is driven by transverse **voltage** across the insulator. A higher-$Z_0$ line transmits the same wave power at *higher voltage*, stressing the laminate harder and increasing dielectric heat loss per meter.

Loss of a constant percentage of energy per meter causes wave voltage amplitude to decay exponentially with distance $z$ according to the **attenuation constant** $\alpha$ (in **nepers per meter**, $\text{Np/m}$) from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md):

$$|V(z)| = |V(0)|\,e^{-\alpha z}$$

Wave power scales with voltage **squared**, so voltage decaying as $e^{-\alpha z}$ causes wave power to decay twice as fast as $e^{-2\alpha z}$ (a $1\%$ voltage drop per centimeter corresponds to a $2\%$ power drop per centimeter). Differentiating $P(z)$ with respect to $z$ gives the fractional power lost across a short slice $\Delta z$:

$$P(z) = P(0)\,e^{-2\alpha z} \qquad \Longrightarrow \qquad \frac{dP(z)}{dz} = -2\alpha\,P(z) \qquad \Longrightarrow \qquad \frac{\Delta P(z)}{P(z)} = -2\alpha\,\Delta z$$

Equivalence between the two fractional power-loss expressions divides by $2$ and separates $\alpha$ into **conductor attenuation** $\alpha_c$ and **dielectric attenuation** $\alpha_d$:

$$\alpha = \alpha_c + \alpha_d = \frac{R_{\text{AC}}}{2 Z_0} + \frac{G\,Z_0}{2}$$

Recall the AC trace resistance equation derived above:

$$R_{\text{AC}} = \frac{R_s}{w_{\text{eff}}} = \frac{\sqrt{\pi f \mu_0 \rho_r}}{w_{\text{eff}}}$$

Substitution of $R_{\text{AC}}$ into $\alpha_c$ shows that smooth-copper attenuation per meter scales with $\sqrt{f}$:

$$\alpha_c(f) = \frac{R_{\text{AC}}}{2 Z_0} = \frac{R_s}{2 Z_0\,w_{\text{eff}}} = \frac{\sqrt{\pi \mu_0 \rho_r}}{2 Z_0\,w_{\text{eff}}}\,\sqrt{f}$$

#### Why Engineers Express Channel Loss in Decibels

Each segment along a real serial link (packages, vias, backplane traces, and connectors) multiplies the surviving voltage by another exponential fraction. Application of $-20\log_{10}$ to the voltage ratio across trace length $\ell$ converts repeated multiplication of fractions into **addition of decibels** ($\text{dB}$), matching how Vector Network Analyzers ([Chapter 8](08_S_Parameters_and_VNA.md)) and SerDes link budgets tally channel loss:

$$\text{Loss (dB)} = -20\log_{10}\!\left(\frac{|V(\ell)|}{|V(0)|}\right) = -20\log_{10}\!\left(e^{-\alpha\ell}\right) = \left(20\log_{10} e\right)\alpha\ell \approx 8.686\,\alpha\ell$$

One neper of attenuation (where $|V(\ell)|$ drops to $e^{-1}$, or $36.8\%$ of launch amplitude) equals $8.686\text{ dB}$, $6\text{ dB}$ cuts voltage amplitude roughly in half ($50\%$), and $20\text{ dB}$ shrinks voltage amplitude to one-tenth ($10\%$). Twice the trace length $\ell$ doubles the decibel loss, whereas a ninefold jump in frequency (from a $1\text{ GHz}$ tone to its $9\text{ GHz}$ ninth harmonic) **triples** copper decibel loss under $\sqrt{f}$ scaling.

### Skin Effect on the Ground Plane Return Path

Every transmission-line circuit includes both the outbound signal trace and the reference ground plane returning $-i(t)$ underneath. Two crowding mechanisms confine that ground-plane return current simultaneously at multi-gigahertz frequencies:

- **Horizontal crowding beneath the trace ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)):** Return current pulls out of the distant wings of the board into a narrow corridor roughly three trace widths ($3w$) wide directly beneath the signal trace to maximize mutual inductance $M$ and minimize total loop inductance.
- **Vertical crowding into the top copper skin:** Inside that narrow corridor, internal magnetic flux inside the ground foil chokes off interior flow and crowds the return current vertically into a surface layer one skin depth $\delta$ thick along the face of the plane closest to the signal trace.

The wider horizontal return corridor ($3w$ versus $w$) gives the ground plane roughly one-third the series skin resistance of the narrow trace above it, though field solvers sum both copper surfaces in accurate link budgets. Confinement to a sub-micron skin also means that a single $35\ \mu\text{m}$ ground plane sandwiched between two stripline layers carries **two completely isolated gigahertz return currents** on its top and bottom faces, separated by more than $30\ \mu\text{m}$ of field-free interior copper until a layer-transition via punctures the plane ([Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md)).

### Copper Surface Roughness and Multi-Gigahertz Foil Models

Smooth-copper skin formulas predict roughly half as much conductor loss at $10\text{ GHz}$ as lab instruments measure on standard FR4 boards. That discrepancy comes from intentional microscopic roughening of PCB copper foil.

#### Smooth Versus Rough Copper Regimes

Mirror-smooth copper foil would peel off epoxy fiberglass during soldering reflow because resin cannot grip a slick metal surface. Foil manufacturers intentionally grow microscopic copper nodules and teeth on the bonding face of the foil so cured resin interlocks mechanically around them. Surface roughness is characterized by the root-mean-square (RMS) tooth height $\Delta$ ($1.0\text{ to }2.0\ \mu\text{m}$ on standard electrodeposited (ED) foil versus $0.2\text{ to }0.3\ \mu\text{m}$ on ultra-low-profile HVLP smooth foil). That roughened bonding face sits directly against the dielectric gap, right on the active boundary where the skin effect forces $100\%$ of gigahertz current to flow.

The ratio of skin depth $\delta$ to RMS tooth height $\Delta$ separates conductor behavior into two physical regimes:

- **Low-frequency smooth regime ($\delta \gg \Delta$):** At $10\text{ MHz}$ ($\delta$ of $20.9\ \mu\text{m}$ versus $\Delta$ of $1.0\ \mu\text{m}$), surface teeth sit at the bottom of a deep $21\ \mu\text{m}$ current layer, so electrons flow straight above the valleys with minimal extra resistance.
- **High-frequency rough regime ($\delta \ll \Delta$):** Above $5\text{ GHz}$ ($\delta$ below $1.0\ \mu\text{m}$), internal back-EMF blocks current from cutting across tooth bases where magnetic flux would be enclosed. The sub-micron current sheet climbs every microscopic hillside and valley, nearly doubling copper resistance.

#### The Hammerstad-Jensen Roughness Multiplier

The widely used Hammerstad-Jensen model quantifies that smooth-to-rough transition by multiplying smooth-copper resistance by a dimensionless **roughness factor** $K_r$ built from the inverse tangent ($\arctan$) of the squared ratio $(\Delta / \delta)^2$:

$$K_r = 1 + \frac{2}{\pi}\arctan\!\left[1.4\left(\frac{\Delta}{\delta}\right)^2\right]$$

The two endpoints of $\arctan$ confirm how the empirical Hammerstad-Jensen groove model behaves across both regimes. For thick skin depths ($\Delta / \delta \ll 1$), $\arctan(0)$ equals zero and $K_r$ equals $1.0$, recovering smooth copper. For sub-micron skin depths much thinner than the teeth ($\Delta / \delta \gg 1$), $\arctan(\infty)$ approaches $\pi / 2$ and the 2D grooved Hammerstad-Jensen curve saturates at an upper ceiling of $2.0$:

$$K_{r,\text{max}} = 1 + \frac{2}{\pi}\left(\frac{\pi}{2}\right) = 2.0$$

Above $10\text{ to }15\text{ GHz}$ on dendritic copper treatments where three-dimensional copper nodules stack like microscopic spheres, eddy-current scattering around those spheres pushes measured roughness factors past $2.0$ (reaching $2.5$ to $3.5$ on $56\text{ to }112\text{ Gbps}$ channels). Electromagnetic field solvers capture that three-dimensional sphere scattering with the **Huray snowball model**.

Multiplication of smooth-copper resistance $R_{\text{AC}}$ and attenuation $\alpha_c(f)$ by $K_r$ defines the roughness-corrected conductor parameters and the line's lumped **conductor loss coefficient** $k_c$ (in $\text{Np}\cdot\text{m}^{-1}\cdot\text{Hz}^{-1/2}$):

$$R_{\text{AC,rough}} = K_r\,R_{\text{AC}}, \qquad \alpha_{c,\text{rough}}(f) = K_r\,\alpha_c(f) = k_c\sqrt{f}$$

$$k_c = \frac{K_r\sqrt{\pi \mu_0 \rho_r}}{2 Z_0\,w_{\text{eff}}}$$

A side-by-side comparison of standard ED copper foil ($\Delta$ of $1.0\ \mu\text{m}$) and ultra-low-profile HVLP smooth foil ($\Delta$ of $0.3\ \mu\text{m}$) quantifies the fractional copper loss reduction $1 - K_{r,\text{HVLP}} / K_{r,\text{ED}}$ achieved on multi-gigabit backplanes:

| Frequency ($f$) | Skin Depth ($\delta$) | Standard ED Foil ($\Delta = 1.0\ \mu\text{m}$) $K_r$ | Smooth HVLP Foil ($\Delta = 0.3\ \mu\text{m}$) $K_r$ | Total Copper Loss Saved by Smooth Foil |
|---|---|---|---|---|
| $1\text{ GHz}$ | $2.09\ \mu\text{m}$ | $1.20$ ($+20\%$ roughness penalty) | $1.02$ ($+2\%$ roughness penalty) | Cuts total copper loss by $15\%$ |
| $5\text{ GHz}$ | $0.93\ \mu\text{m}$ | $1.65$ ($+65\%$ roughness penalty) | $1.09$ ($+9\%$ roughness penalty) | Cuts total copper loss by $34\%$ |
| $10\text{ GHz}$ | $0.66\ \mu\text{m}$ | $1.81$ ($+81\%$ roughness penalty) | $1.18$ ($+18\%$ roughness penalty) | Cuts total copper loss by $35\%$ |
| $15\text{ GHz}$ | $0.54\ \mu\text{m}$ | $1.87$ ($+87\%$ roughness penalty) | $1.26$ ($+26\%$ roughness penalty) | Cuts total copper loss by $33\%$ |

## Architecture

### Dielectric Loss: Molecular Polarization Friction Inside the Laminate

Wide traces and ultra-smooth HVLP copper minimize conductor loss, yet above $1\text{ GHz}$ on standard FR4 fiberglass-epoxy, **more than half of the signal attenuation occurs outside the copper altogether**. That second, steeper loss mechanism takes place inside the insulating polymer resin separating the trace from the ground plane.

#### Polar Dipoles Twisting Against Polymer Friction

Fiberglass cloth and cured epoxy resin contain virtually zero free mobile electrons, so zero DC conduction current leaks from trace to ground. Instead, the long polymer chains of the epoxy resin contain **polar chemical groups** whose electron clouds sit asymmetrically between bonded atoms, leaving one end of each chemical group slightly negative ($-$) and the opposite end slightly positive ($+$) to form a bound **electric dipole**.

The propagating wave's vertical electric field $\vec{E}$ ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)) pulls the negative end of every polar group toward the positive conductor and pushes the positive end toward the negative conductor, twisting billions of dipoles toward vertical alignment. On an alternating wave of frequency $f$, the vertical electric field reverses polarity twice per cycle ($10\text{ billion}$ reversals per second at $5\text{ GHz}$), forcing every polar group to twist back and forth continuously. Each group is chemically cross-linked inside a dense solid polymer network, so rotation against neighboring chains encounters microscopic mechanical drag (**molecular friction**).

#### Reversible Storage Versus Linear-With-Frequency Frictional Loss

Comparison between an ideal frictionless insulator (such as vacuum or dry air) and a real polymer laminate over one sinusoidal cycle at angular frequency $\omega$ ($2\pi f$) explains why dielectric loss grows faster with frequency than copper skin loss.

In an ideal lossless dielectric of per-unit-length capacitance $C$ ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) and [Chapter 3](03_Impedance_Reflections_and_Termination.md)), electric charge flows onto the plates during the rising voltage half-cycle and returns $100\%$ of its stored electric field energy during the falling half-cycle. In phasor notation, that pure capacitive charging current $I_{\text{cap}}$ (in $\text{A/m}$) leads voltage $V$ by $+90^\circ$ (multiplication by $j$) and burns zero net power:

$$I_{\text{cap}} = j\omega C\,V$$

In a real epoxy laminate, viscous polymer drag delays the twisting dipoles so their alignment **lags slightly behind** the driving electric field. Delayed dipole motion prevents the insulator from returning $100\%$ of its stored electric energy during the second half-cycle; a nearly fixed fraction of the stored energy rubs away into random molecular vibration (heat) during **every back-and-forth cycle**.

A $1\text{ GHz}$ wave executes $1\text{ billion}$ rub cycles per second, whereas a $10\text{ GHz}$ wave executes **$10\text{ billion}$ rub cycles per second**. Ten times as many frictional cycles every second burn ten times as much wave power per meter, causing dielectric attenuation to climb **linearly with frequency $f$** rather than with $\sqrt{f}$.

#### Loss Tangent and Shunt Conductance

Inside the lossy transmission-line circuit of [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md), total vertical current per meter $I_{\text{shunt}}$ across voltage $V$ splits into two parallel branches. Reversible $+90^\circ$ capacitive current $I_{\text{cap}}$ stores electric energy, while in-phase frictional current $I_{\text{loss}}$ flows through parallel **shunt conductance** $G$ (in siemens per meter, $\text{S/m}$):

$$I_{\text{loss}} = G\,V, \qquad I_{\text{shunt}} = I_{\text{loss}} + I_{\text{cap}} = G\,V + j\omega C\,V$$

Laminate datasheets report a material's intrinsic molecular friction as the ratio of **in-phase frictional loss current magnitude** ($G\,|V|$) to **reactive storage current magnitude** ($\omega C\,|V|$). In the complex plane, $I_{\text{loss}}$ (real axis) and $I_{\text{cap}}$ ($+j$ axis) form the opposite and adjacent legs of a right triangle. Their ratio equals the tangent of the small phase angle by which total current tilts away from an ideal $90^\circ$ capacitor, called the **dielectric loss tangent** $\tan\delta$ (or **dissipation factor** $D_f$):

$$\tan\delta = D_f = \frac{|I_{\text{loss}}|}{|I_{\text{cap}}|} = \frac{G\,|V|}{\omega C\,|V|} = \frac{G}{\omega C}$$

Electrical engineering writes $\tan\delta$ as a single inseparable symbol for dielectric loss tangent (dimensionless), distinct from the standalone symbol $\delta$ for copper skin depth (in meters). Electromagnetic textbooks package both parallel branches into a complex permittivity $\varepsilon(\omega)$ with real storage part $\varepsilon'$ and imaginary loss part $\varepsilon''$, where $j^2$ equal to $-1$ produces the positive in-phase conductance $G$:

$$\varepsilon(\omega) = \varepsilon' - j\varepsilon'', \qquad j\omega(\varepsilon' - j\varepsilon'') = \omega\varepsilon'' + j\omega\varepsilon', \qquad \tan\delta = \frac{\varepsilon''}{\varepsilon'}$$

Multiplication of both sides of the loss-tangent ratio by $\omega C$ ($2\pi f C$) expresses per-unit-length shunt conductance $G$ directly from datasheet parameters:

$$G = \omega C \tan\delta = 2\pi f C \tan\delta$$

#### Dielectric Attenuation and Why Trace Width Cannot Fix It

Recall the dielectric voltage attenuation relation and shunt conductance equation established above:

$$\alpha_d = \frac{G\,Z_0}{2}, \qquad G = 2\pi f C \tan\delta$$

Substitution of $G$ groups per-unit-length capacitance $C$ next to characteristic impedance $Z_0$:

$$\alpha_d = \frac{(2\pi f C \tan\delta)\,Z_0}{2} = \pi f\,(C\,Z_0)\,\tan\delta$$

Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) and [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) how the product $C\,Z_0$ relates to wave propagation velocity $v_p$, vacuum light speed $c$ ($3.0 \times 10^8\ \text{m/s}$), and effective relative permittivity $\varepsilon_{\text{eff}}$:

$$Z_0 = \sqrt{\frac{L}{C}}, \qquad v_p = \frac{1}{\sqrt{LC}} = \frac{c}{\sqrt{\varepsilon_{\text{eff}}}}$$

$$C\,Z_0 = C\sqrt{\frac{L}{C}} = \sqrt{LC} = \frac{1}{v_p} = \frac{\sqrt{\varepsilon_{\text{eff}}}}{c}$$

Substitution of $\sqrt{\varepsilon_{\text{eff}}} / c$ for $C\,Z_0$ yields the **dielectric attenuation constant** $\alpha_d(f)$ (in $\text{Np/m}$) and defines the line's lumped **dielectric loss coefficient** $k_d$ (in $\text{Np}\cdot\text{m}^{-1}\cdot\text{Hz}^{-1}$):

$$\alpha_d(f) = \frac{\pi f\,\tan\delta}{v_p} = \frac{\pi f \sqrt{\varepsilon_{\text{eff}}}\,\tan\delta}{c} = k_d\,f$$

$$k_d = \frac{\pi\sqrt{\varepsilon_{\text{eff}}}\,\tan\delta}{c}$$

Inside a homogeneous dielectric, neither trace width $w$ nor dielectric gap thickness $d_{\text{gap}}$ appears anywhere in $\alpha_d(f)$. Twice the trace width $w$ doubles parallel-plate capacitance $C$ (putting twice as many polar molecules into motion beneath the trace) while simultaneously halving characteristic impedance $Z_0$ (lowering voltage stress for a given wave power), leaving the product $C\,Z_0$ completely unchanged.

Wider PCB traces therefore provide **zero reduction in homogeneous dielectric loss**. Reduction of $\alpha_d(f)$ per inch requires replacing polar standard FR4 epoxy ($\tan\delta$ near $0.020$) with low-polarity polyphenylene ether (PPE), hydrocarbon, or fluoropolymer resin systems whose polymer chains contain far fewer polar groups. Commercial high-speed laminates in those low-polarity classes include Megtron 6 ($\tan\delta$ near $0.004$) and Megtron 8 ($\tan\delta$ near $0.0015$).

### Why Loss Is Linear and Symmetric on Rising and Falling Edges

An oscilloscope capture of an isolated `1` pulse (`0 -> 1 -> 0`) at the receiver end of a long FR4 trace shows a steep leading rise followed by a long positive voltage tail dragging behind the falling edge. That asymmetric pulse shape often prompts a plausible-sounding misconception: that an applied electric field snaps polar dipoles into alignment rapidly on a rising `0 -> 1` edge, whereas removing the field leaves dipoles to drift back slowly by random thermal motion on a falling `1 -> 0` edge.

A $1.0\text{ V}$ digital signal across a $100\ \mu\text{m}$ dielectric gap applies an electric field of $10^4\text{ V/m}$, tens of thousands of times weaker than the internal atomic fields binding the epoxy network. Each polar group twists by a tiny fraction of a degree well inside its **linear** elastic regime: returning from $+1.0\text{ V}$ back to $0\text{ V}$ is driven by the identical linear bond-restoring stiffness and polymer drag as twisting from $0\text{ V}$ up to $+1.0\text{ V}$.

An oscilloscope test of an isolated `0` pulse (`1 -> 0 -> 1`) or a side-by-side comparison of a lone rising step (`00001111...`) and a lone falling step (`11110000...`) proves that symmetry directly. Both step transitions exhibit **identical mirror-image curves**, jumping rapidly through roughly $85\%$ of their swing and creeping slowly across the remaining $15\%$. Single pulses look lopsided in time not because molecules relax nonlinearly, but because **causality** runs one way in time: delayed wave energy cannot arrive before the wavefront, so all dispersed energy trails behind the pulse.

### Dispersion, the Long Post-Cursor Tail, and Inter-Symbol Interference

At $10\text{ Gbps}$, a transmitter launches a new bit every $T_{\text{UI}}$ of $100\text{ ps}$. A clear time-domain link from frequency-dependent attenuation to pulse stretching across dozens of later bit slots bridges electromagnetic board physics directly to SerDes equalization ([Chapter 13](13_Transmitter_FFE.md) and [Chapter 14](14_CTLE_and_DFE.md)).

#### Why Low Frequencies Travel Slower and Arrive as a Late Tail

[Chapter 2](02_Frequency_Content_of_Digital_Signals.md) showed that a crisp $0\text{ V}$ to $1.0\text{ V}$ voltage step stacks sine waves of all frequencies together: multi-gigahertz harmonics build the fast initial jump, megahertz harmonics fill in the shoulder immediately after the edge, and low frequencies hold the steady $1.0\text{ V}$ rail. Propagation down a lossy trace of length $\ell$ alters that sine-wave bundle through three coupled frequency-dependent mechanisms:

1. **Selective high-frequency attenuation:** Copper skin loss (scaling with $\sqrt{f}$) and dielectric polarization loss (scaling linearly with $f$) strip away multi-gigahertz harmonics, rounding off the sharp initial corner of the step.
2. **Causal copper velocity dispersion:** Low-frequency waves penetrate deep into the copper foil and enclose extra internal inductance $L_{\text{int}}(f)$, whereas gigahertz waves skim along the outer skin with $L_{\text{ext}}$ alone. Higher low-frequency inductance $L(f)$ slows low-frequency phase velocity $v_p(f)$.
3. **Causal dielectric velocity dispersion:** Inside any polar laminate with non-zero $\tan\delta$, causality (modeled across multi-decade bands by wideband **Debye** or **Djordjevic-Sarkar** relaxation) requires relative permittivity $\varepsilon_r(f)$ to decrease gently with $\ln f$ as sluggish dipoles lag rapid field reversals. Higher low-frequency capacitance $C(f)$ reinforces $L(f)$ to slow $v_p(f)$ into a late-arriving tail.

#### Characteristic Skin-Dispersion Time and the Inverse-Square-Root Step Tail

Contrasting a lumped single-pole resistor-capacitor ($RC$) filter ([Chapter 3](03_Impedance_Reflections_and_Termination.md)) against a skin-effect transmission line highlights why skin tails linger. A lumped $RC$ filter has one time constant $\tau_{RC}$, so its exponential step response finishes $99.3\%$ of its climb within $5\,\tau_{RC}$. A skin-effect trace has **no single time constant** because every frequency penetrates a different depth $\delta(f)$ into the copper.

Let $t'$ denote elapsed time at the receiver after the fastest wavefront arrives at one-way flight delay $\tau_d$ ($\ell / v_p$):

$$t' = t - \tau_d, \qquad \tau_d = \frac{\ell}{v_p}$$

Recall that total conductor attenuation across trace length $\ell$ scales with $\sqrt{f}$:

$$\alpha_{c,\text{rough}}(f)\,\ell = k_c\,\ell\,\sqrt{f}$$

Low frequencies near DC experience nearly zero attenuation, meaning $100\%$ of a unit $1.0\text{ V}$ step must reach the receiver eventually; the missing top portion of the edge is **delayed**, not destroyed. In the complementary-error-function diffusion solution of a causal skin-effect line, spectral components near $1 / t'$ ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)) govern late-time settling and combine $k_c\,\ell$ and $\pi$ into the **characteristic skin-dispersion time** $\tau_{\text{skin}}$ (in seconds or picoseconds):

$$\tau_{\text{skin}} = \left(\frac{k_c\,\ell}{\pi}\right)^2$$

During the first few picoseconds near wavefront arrival ($t'$ comparable to $\tau_{\text{skin}}$), heavy skin attenuation of upper multi-gigahertz harmonics rounds the initial toe smoothly upward from $0\text{ V}$. Across all bit-sampling times well past that initial picosecond toe ($t' \gg \tau_{\text{skin}}$), the received unit step response $s_r(t')$ follows an **inverse-square-root creeping tail**:

$$s_r(t') \approx 1 - \sqrt{\frac{\tau_{\text{skin}}}{t'}}, \qquad \text{for } t' \gg \tau_{\text{skin}}$$

The inverse-square-root factor $\sqrt{\tau_{\text{skin}} / t'}$ settles far more slowly than an exponential curve. A $50\%$ reduction in the remaining voltage deficit requires waiting **four times** as long ($4\times t'$), and shrinking a $12.6\%$ deficit at $1\text{ UI}$ down to $1.26\%$ requires waiting **$100\text{ UI}$**.

#### Single-Bit Pulse Superposition and Post-Cursor ISI

A single isolated `1` bit of duration equal to one **unit interval** $T_{\text{UI}}$ (`...0001000...`) equals a positive unit rising step launched at zero time plus a negative unit falling step launched one bit period later at $T_{\text{UI}}$ ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)). By linearity, the received **single-bit pulse response** $p_r(t')$ is the step response $s_r(t')$ minus a copy of itself delayed by $T_{\text{UI}}$:

$$p_r(t') = s_r(t') - s_r(t' - T_{\text{UI}})$$

Receiver clock ticks spaced one unit interval $T_{\text{UI}}$ apart around the main sampling instant $t'_0$ divide $p_r(t')$ into three **cursor** regions:

- **Pre-cursor ($v_{-1}$):** Early voltage sampled at $t'_0 - T_{\text{UI}}$ one unit interval *before* the main cursor. Heavy high-frequency loss delays the dispersed pulse peak past $T_{\text{UI}}$ ($t'_0 > T_{\text{UI}}$), placing $t'_0 - T_{\text{UI}}$ on the rounded rising toe after wavefront arrival. For short skin-dispersion times ($\tau_{\text{skin}} \ll T_{\text{UI}}$) where $t'_0$ sits near $T_{\text{UI}}$, $v_{-1}$ approaches zero.
- **Main cursor ($v_0$):** Primary signal peak sampled at $t'_0$ (evaluated at $T_{\text{UI}}$ in the thin-skin hand model where the delayed falling step is still zero, giving $s_r(T_{\text{UI}})$), attenuated below $1.0$ because the slow step tail has not finished climbing within a single bit slot.
- **Post-cursors ($v_1, v_2, v_3, \dots$):** Residual positive voltages sampled $1, 2, 3, \dots$ unit intervals *after* the main cursor ($t'_0 + T_{\text{UI}}, t'_0 + 2 T_{\text{UI}}, \dots$), left behind because the earlier rising step $s_r(t')$ remains slightly higher than the delayed falling step $s_r(t' - T_{\text{UI}})$ as both creep upward.

Addition of all post-cursors from $v_1$ out to infinity produces a telescoping cancellation where every intermediate step term cancels against its neighbor:

$$\sum_{m = 1}^{\infty} v_m = \bigl[s_r(2 T_{\text{UI}}) - s_r(T_{\text{UI}})\bigr] + \bigl[s_r(3 T_{\text{UI}}) - s_r(2 T_{\text{UI}})\bigr] + \cdots = s_r(\infty) - s_r(T_{\text{UI}}) = 1 - v_0$$

Every millivolt missing from the main cursor peak ($1 - v_0$) reappears spread across the post-cursor tail. A long run of `1` bits before a lone `0` bit (`1111111...0`) stacks all preceding post-cursor tails onto that `0`, lifting the `0` rail while a lone `1` (`0000000...1`) reaches only $v_0$. That voltage spillover across bit boundaries is **Inter-Symbol Interference (ISI)**, and subtracting those post-cursor taps is the primary job of Transmitter Feed-Forward Equalizers ([Chapter 13](13_Transmitter_FFE.md)) and Receiver Decision Feedback Equalizers ([Chapter 14](14_CTLE_and_DFE.md)).

### Combined Insertion Loss and the Crossover Frequency

Suppose a prototype multi-gigabit board fails eye-diagram compliance in the lab. Should the engineering team widen the copper traces and specify smooth HVLP foil, or pay for a low-loss dielectric laminate? Wider traces lower conductor loss while leaving dielectric loss unchanged, whereas low-loss resin lowers dielectric loss while leaving conductor loss unchanged. The right physical fix depends on which mechanism dominates at the link's Nyquist frequency ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)).

Recall the roughness-corrected conductor attenuation $\alpha_{c,\text{rough}}(f)$ and dielectric attenuation $\alpha_d(f)$ derived earlier:

$$\alpha_{c,\text{rough}}(f) = k_c\sqrt{f}, \qquad \alpha_d(f) = k_d\,f$$

$$k_c = \frac{K_r\sqrt{\pi \mu_0 \rho_r}}{2 Z_0\,w_{\text{eff}}}, \qquad k_d = \frac{\pi\sqrt{\varepsilon_{\text{eff}}}\,\tan\delta}{c}$$

Both mechanisms act simultaneously along every centimeter of trace, so total channel attenuation per meter $\alpha(f)$ (in $\text{Np/m}$) is their sum:

$$\alpha(f) = \alpha_{c,\text{rough}}(f) + \alpha_d(f) = k_c\sqrt{f} + k_d\,f$$

Near DC and low megahertz frequencies, $\sqrt{f}$ climbs much steeper than a straight line $f$, putting conductor skin loss on top. At multi-gigahertz frequencies, $\sqrt{f}$ bends over while the linear dielectric curve $k_d\,f$ keeps climbing steadily until it overtakes copper loss. Equality between the two terms defines the **crossover frequency** $f_x$ (in $\text{Hz}$) where conductor loss and dielectric loss match:

$$k_c\sqrt{f_x} = k_d\,f_x \qquad \Longrightarrow \qquad \sqrt{f_x} = \frac{k_c}{k_d} \qquad \Longrightarrow \qquad f_x = \left(\frac{k_c}{k_d}\right)^2$$

Comparison of a signal's spectral frequencies against $f_x$ divides board optimization into two clear regimes:

- **Below the crossover frequency ($f < f_x$):** Square-root copper loss exceeds linear dielectric loss; wider traces ($w \uparrow$) or smoother HVLP foil ($K_r \downarrow$) deliver the largest insertion-loss reduction.
- **Above the crossover frequency ($f > f_x$):** Linear dielectric loss overtakes copper loss; a lower-$\tan\delta$ laminate shrinks $k_d$, shifts $f_x$ upward with the **square** of the $\tan\delta$ improvement, and delivers the largest eye-opening gain.

## Worked Examples

### Worked Example 1: DC Versus 1 GHz AC Resistance of a Stripline Trace

Consider a smooth symmetric copper stripline trace ($K_r$ of $1.0$, $\rho_r$ of $1.72 \times 10^{-8}\ \Omega\cdot\text{m}$, $\mu_0$ of $4\pi \times 10^{-7}\ \text{H/m}$, and homogeneous FR4 permittivity $\varepsilon_{\text{eff}}$ of $4.16$) designed for characteristic impedance $Z_0$ of $50\ \Omega$. The trace has horizontal width $w$ of $0.10\text{ mm}$ ($1.0 \times 10^{-4}\text{ m}$, roughly $4\text{ mil}$) and standard $1\text{ oz}$ copper foil thickness $t_{\text{Cu}}$ of $35\ \mu\text{m}$ ($3.5 \times 10^{-5}\text{ m}$). In the signal-strip perimeter model (neglecting sidewall edge crowding and ground-plane return resistance), equal spacing between upper and lower reference planes splits high-frequency skin current evenly across top and bottom faces, doubling the effective active perimeter width $w_{\text{eff}}$:

$$w_{\text{eff}} = 2w = 0.20\text{ mm} = 2.0 \times 10^{-4}\text{ m}$$

#### Step 1: Per-Unit-Length DC Resistance

Recall the per-unit-length DC resistance equation:

$$R_{\text{DC}} = \frac{\rho_r}{w\,t_{\text{Cu}}}$$

Substitution of $\rho_r$, $w$, and $t_{\text{Cu}}$ yields the DC resistance per meter and per inch ($0.0254\text{ m/in}$):

$$R_{\text{DC}} = \frac{1.72 \times 10^{-8}\ \Omega\cdot\text{m}}{(1.0 \times 10^{-4}\text{ m})(3.5 \times 10^{-5}\text{ m})} = 4.91\ \Omega/\text{m} \approx 0.125\ \Omega/\text{in}$$

Across a $12\text{ in}$ trace, a DC multimeter reads just $1.50\ \Omega$ end to end.

#### Step 2: Skin Depth, Surface Resistance, and AC Resistance at 1 GHz

Recall the copper skin depth equation:

$$\delta = \sqrt{\frac{\rho_r}{\pi f \mu_0}}$$

Evaluation of $\delta$ at frequency $f$ of $1.0\text{ GHz}$ ($1.0 \times 10^9\text{ Hz}$) gives:

$$\delta = \sqrt{\frac{1.72 \times 10^{-8}\ \Omega\cdot\text{m}}{\pi\,(1.0 \times 10^9\text{ Hz})(4\pi \times 10^{-7}\text{ H/m})}} = \sqrt{4.36 \times 10^{-12}\text{ m}^2} \approx 2.09 \times 10^{-6}\text{ m} = 2.09\ \mu\text{m}$$

Two $2.09\ \mu\text{m}$ skins on the top and bottom faces occupy $4.18\ \mu\text{m}$ out of the $35\ \mu\text{m}$ foil ($12\%$ of the copper), confirming that the thick-foil skin model holds. Recall the surface resistance equation and substitute $\rho_r$ and $\delta$:

$$R_s = \frac{\rho_r}{\delta} = \frac{1.72 \times 10^{-8}\ \Omega\cdot\text{m}}{2.087 \times 10^{-6}\text{ m}} = 8.24 \times 10^{-3}\ \Omega = 8.24\text{ m}\Omega$$

Recall the per-unit-length AC resistance equation and divide $R_s$ by $w_{\text{eff}}$:

$$R_{\text{AC}} = \frac{R_s}{w_{\text{eff}}} = \frac{8.24 \times 10^{-3}\ \Omega}{2.0 \times 10^{-4}\text{ m}} = 41.2\ \Omega/\text{m} \approx 1.05\ \Omega/\text{in}$$

Even at a modest $1.0\text{ GHz}$, magnetic current crowding raises trace resistance to **$8.4\times$ its DC value** ($12.6\ \Omega$ across $12\text{ in}$).

#### Step 3: Conductor Attenuation at 1 GHz and Low-Loss Verification

Recall the conductor attenuation equation and substitute $R_{\text{AC}}$ and $Z_0$:

$$\alpha_c = \frac{R_{\text{AC}}}{2 Z_0} = \frac{41.2\ \Omega/\text{m}}{2(50\ \Omega)} = 0.412\text{ Np/m}$$

Recall the decibel conversion equation across length $\ell$:

$$\text{Loss (dB)} = 8.686\,\alpha\ell$$

Multiplication of $0.412\text{ Np/m}$ by $8.686\text{ dB/Np}$ (and by $0.0254\text{ m/in}$) converts copper loss into decibels per meter and per inch:

$$\text{Conductor Loss at } 1\text{ GHz} = (8.686)(0.412\text{ Np/m}) = 3.58\text{ dB/m} \approx 0.091\text{ dB/in}$$

Verification of the low-loss transmission-line assumption ($R_{\text{AC}} \ll 2\pi f L$) uses the stripline distributed inductance $L$ of $340\text{ nH/m}$ from $Z_0\sqrt{\varepsilon_{\text{eff}}} / c$ (matching the $342\text{ nH/m}$ FR4 microstrip benchmark of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)). Comparing $R_{\text{AC}}$ against $2\pi f L$ confirms that $41.2\ \Omega/\text{m}$ is under $2\%$ of the inductive reactance at $1.0\text{ GHz}$:

$$L = \frac{Z_0\sqrt{\varepsilon_{\text{eff}}}}{c} = \frac{(50\ \Omega)(2.04)}{3.0 \times 10^8\text{ m/s}} = 340\text{ nH/m}$$

$$2\pi f L = 2\pi(1.0 \times 10^9\text{ Hz})(340 \times 10^{-9}\text{ H/m}) = 2136\ \Omega/\text{m}$$

### Worked Example 2: Harmonic Loss Budget and Crossover Frequency on a 12-Inch Stripline

Transmit a $10\text{ Gbps}$ Non-Return-to-Zero (NRZ) repeating `101010...` pattern ($T_{\text{UI}}$ of $100\text{ ps}$) across an $\ell$ of $12\text{ in}$ ($0.3048\text{ m}$) stripline using the trace geometry of Worked Example 1 on standard FR4 ($\varepsilon_{\text{eff}}$ of $4.16$, so $\sqrt{\varepsilon_{\text{eff}}}$ equals $2.04$, and $\tan\delta$ equals $0.020$). From [Chapter 2](02_Frequency_Content_of_Digital_Signals.md), the `101010...` square wave has fundamental (Nyquist) frequency $f_1$ and third edge harmonic $f_3$ (launched at one-third of the fundamental amplitude):

$$f_1 = \frac{1}{2 T_{\text{UI}}} = 5.0\text{ GHz}, \qquad f_3 = 3 f_1 = 15.0\text{ GHz}$$

#### Step 1: Conductor and Dielectric Loss Rates at 5 GHz and 15 GHz

Square-root frequency scaling of the $1.0\text{ GHz}$ smooth-copper rate ($0.091\text{ dB/in}$) gives conductor loss per inch at $5\text{ GHz}$ and $15\text{ GHz}$:

$$\text{Conductor Loss at } 5\text{ GHz} = (0.091\text{ dB/in})\sqrt{\frac{5.0\text{ GHz}}{1.0\text{ GHz}}} = (0.091\text{ dB/in})(2.236) = 0.203\text{ dB/in}$$

$$\text{Conductor Loss at } 15\text{ GHz} = (0.091\text{ dB/in})\sqrt{\frac{15.0\text{ GHz}}{1.0\text{ GHz}}} = (0.091\text{ dB/in})(3.873) = 0.352\text{ dB/in}$$

Recall the dielectric attenuation equation:

$$\alpha_d(f) = \frac{\pi f \sqrt{\varepsilon_{\text{eff}}}\,\tan\delta}{c}$$

Substitution of $f_1$ of $5.0 \times 10^9\text{ Hz}$, $\sqrt{\varepsilon_{\text{eff}}}$ of $2.04$, $\tan\delta$ of $0.020$, and $c$ of $3.0 \times 10^8\text{ m/s}$ gives $\alpha_d$ at $5.0\text{ GHz}$, followed by conversion to decibels per inch:

$$\alpha_d(5\text{ GHz}) = \frac{\pi\,(5.0 \times 10^9\text{ Hz})(2.04)(0.020)}{3.0 \times 10^8\text{ m/s}} = 2.136\text{ Np/m}$$

$$\text{Dielectric Loss at } 5\text{ GHz} = (8.686)(2.136\text{ Np/m})(0.0254\text{ m/in}) = 0.471\text{ dB/in}$$

Linear frequency scaling of dielectric loss triples that rate at $15\text{ GHz}$ to $1.413\text{ dB/in}$ and divides it by $5$ at $1.0\text{ GHz}$ to $0.094\text{ dB/in}$.

#### Step 2: 12-Inch Channel Survival and Square-Wave Rounding

Inversion of the decibel definition recovers the fraction of launched voltage amplitude surviving at the receiver after total decibel loss $L_{\text{dB}}$:

$$\frac{|V(\ell)|}{|V(0)|} = 10^{-L_{\text{dB}} / 20}$$

Summation of conductor and dielectric rates across $12\text{ in}$ compares how much of the fundamental and third harmonic reach the receiver:

| Spectral Component | Copper Rate | Dielectric Rate | Total Rate | $12\text{ in}$ Loss ($L_{\text{dB}}$) | Surviving Voltage Ratio $\lvert V(\ell)\rvert / \lvert V(0)\rvert$ |
|---|---|---|---|---|---|
| **Fundamental ($5\text{ GHz}$)** | $0.203\text{ dB/in}$ | $0.471\text{ dB/in}$ | $0.674\text{ dB/in}$ | $8.09\text{ dB}$ | $0.394$ ($39.4\%$ survives) |
| **Third Harmonic ($15\text{ GHz}$)** | $0.352\text{ dB/in}$ | $1.413\text{ dB/in}$ | $1.765\text{ dB/in}$ | $21.18\text{ dB}$ | $0.087$ ($8.7\%$ survives) |

At the transmitter pins, the $15\text{ GHz}$ third harmonic starts at $33.3\%$ ($1/3$) of the $5\text{ GHz}$ fundamental amplitude to build crisp square edges. At the end of $12\text{ in}$ of FR4, differential attenuation collapses that third-to-fundamental amplitude ratio to $7.4\%$, rounding the square wave into a shrunken, nearly pure $5\text{ GHz}$ sine wave:

$$\frac{|V_3(\ell)|}{|V_1(\ell)|} = \frac{1}{3}\left(\frac{0.087}{0.394}\right) \approx 0.074 = 7.4\%$$

#### Step 3: Crossover Frequency on Standard FR4 Versus Low-Loss Laminate

Recall the crossover frequency equation:

$$f_x = \left(\frac{k_c}{k_d}\right)^2$$

At $1.0\text{ GHz}$, the copper loss rate ($0.091\text{ dB/in}$) and FR4 dielectric loss rate ($0.094\text{ dB/in}$) directly measure $k_c$ and $k_d$ scaled to $1.0\text{ GHz}$:

$$f_{x,\text{FR4}} = \left(\frac{0.091\text{ dB/in}}{0.094\text{ dB/in}}\right)^2(1.0\text{ GHz}) = 0.94\text{ GHz}$$

An upgrade from standard FR4 ($\tan\delta$ of $0.020$) to a low-loss laminate ($\tan\delta$ of $0.004$) cuts the $1.0\text{ GHz}$ dielectric rate fivefold to $0.0188\text{ dB/in}$ and raises the squared crossover ratio twenty-five-fold:

$$f_{x,\text{low-loss}} = \left(\frac{0.091\text{ dB/in}}{0.0188\text{ dB/in}}\right)^2(1.0\text{ GHz}) = 23.4\text{ GHz}$$

Standard FR4 is dielectric-dominated everywhere above $0.94\text{ GHz}$, whereas on the low-loss laminate conductor skin loss dominates all the way to $23.4\text{ GHz}$, making wider traces and smooth HVLP foil the primary optimization levers at $10\text{ to }15\text{ GHz}$.

### Worked Example 3: Creeping Step Tail and Post-Cursor ISI on the 12-Inch Stripline

Isolate the smooth-copper skin loss of the $12\text{ in}$ stripline from Worked Example 2 at $10\text{ Gbps}$ ($T_{\text{UI}}$ of $100\text{ ps}$) to see how the inverse-square-root step tail creates post-cursor ISI even before dielectric loss is added.

#### Step 1: Characteristic Skin-Dispersion Time $\tau_{\text{skin}}$

Across $12\text{ in}$, multiply the $5.0\text{ GHz}$ copper loss rate ($0.203\text{ dB/in}$) by trace length and divide by $8.686\text{ dB/Np}$ to obtain total conductor attenuation in nepers:

$$L_{\text{dB,Cu}} = (12\text{ in})(0.203\text{ dB/in}) = 2.44\text{ dB} \qquad \Longrightarrow \qquad \alpha_c(5\text{ GHz})\,\ell = \frac{2.44\text{ dB}}{8.686\text{ dB/Np}} = 0.281\text{ Np}$$

Recall the total conductor attenuation relation and solve for $k_c\,\ell$:

$$\alpha_c(f)\,\ell = k_c\,\ell\,\sqrt{f} \qquad \Longrightarrow \qquad k_c\,\ell = \frac{0.281}{\sqrt{5.0 \times 10^9\text{ Hz}}} = 3.97 \times 10^{-6}\text{ s}^{1/2}$$

Recall the characteristic skin-dispersion time equation and substitute $k_c\,\ell$:

$$\tau_{\text{skin}} = \left(\frac{k_c\,\ell}{\pi}\right)^2 = \left(\frac{3.97 \times 10^{-6}\text{ s}^{1/2}}{\pi}\right)^2 = 1.60 \times 10^{-12}\text{ s} = 1.60\text{ ps}$$

#### Step 2: Computing the Main Cursor and Post-Cursor ISI Taps

Every $100\text{ ps}$ bit-sampling instant satisfies $t' \gg 1.60\text{ ps}$, so recall the inverse-square-root step tail equation and single-bit pulse superposition equation:

$$s_r(t') \approx 1 - \sqrt{\frac{\tau_{\text{skin}}}{t'}}, \qquad p_r(t') = s_r(t') - s_r(t' - T_{\text{UI}})$$

Evaluate the first two bit intervals explicitly to verify the arithmetic. At $t'$ of $100\text{ ps}$ ($1\text{ UI}$, where the delayed step at $0\text{ ps}$ has not started), the step response sets the main cursor $v_0$:

$$v_0 = s_r(100\text{ ps}) \approx 1 - \sqrt{\frac{1.60\text{ ps}}{100\text{ ps}}} = 1 - 0.1265 \approx 0.874$$

At $t'$ of $200\text{ ps}$ ($2\text{ UI}$), subtracting the delayed step $s_r(100\text{ ps})$ from $s_r(200\text{ ps})$ gives the first post-cursor tap $v_1$:

$$s_r(200\text{ ps}) \approx 1 - \sqrt{\frac{1.60\text{ ps}}{200\text{ ps}}} = 1 - 0.0894 \approx 0.911 \qquad \Longrightarrow \qquad v_1 = 0.911 - 0.874 = 0.037$$

Application of that pocket-calculator square root across later bit slots maps out the slow diffusive tail:

| Elapsed Time ($t'$) | Step Response $s_r(t')$ | Delayed Step $s_r(t' - 100\text{ ps})$ | Pulse Sample $p_r(t')$ | Cursor Role and Share of Main Cursor $v_0$ |
|---|---|---|---|---|
| $100\text{ ps}$ ($1\text{ UI}$) | $0.874$ | $0.000$ | $v_0 = 0.874$ | **Main cursor:** Reaches $87.4\%$ of launch swing; $12.6\%$ delayed. |
| $200\text{ ps}$ ($2\text{ UI}$) | $0.911$ | $0.874$ | $v_1 = 0.037$ | **First post-cursor:** $4.2\%$ of main cursor height. |
| $300\text{ ps}$ ($3\text{ UI}$) | $0.927$ | $0.911$ | $v_2 = 0.016$ | **Second post-cursor:** $1.8\%$ of main cursor height. |
| $400\text{ ps}$ ($4\text{ UI}$) | $0.937$ | $0.927$ | $v_3 = 0.010$ | **Third post-cursor:** $1.1\%$ of main cursor height. |
| $1000\text{ ps}$ ($10\text{ UI}$) | $0.960$ | $0.958$ | $v_9 = 0.002$ | **Ninth post-cursor:** Step remains $4.0\%$ below $1.0$ after $10$ bits. |
| $10000\text{ ps}$ ($100\text{ UI}$) | $0.98735$ | $0.98729$ | $v_{99} = 0.00006$ | **Ninety-ninth post-cursor:** Step remains $1.3\%$ below $1.0$ after $100$ bits. |

By telescoping cancellation, the sum of the first seven post-cursors ($v_1$ through $v_7$) equals the step difference between $800\text{ ps}$ and $100\text{ ps}$:

$$\sum_{m = 1}^{7} v_m = s_r(800\text{ ps}) - s_r(100\text{ ps}) = 0.955 - 0.874 = 0.081$$

Seven consecutive `1` bits before a lone `0` bit (`11111110`) lift the `0` rail to $+0.081$ while a lone `1` bit (`00000001`) peaks at $0.874$, shrinking the vertical eye opening to $0.793$ (more than $20\%$ eye closure from smooth-copper skin dispersion alone):

$$\text{Vertical Eye Opening} = v_0 - \sum_{m = 1}^{7} v_m = 0.874 - 0.081 = 0.793$$

## Edge Cases

### Hammerstad Saturation Versus Skin-Depth Scaling and Huray Scattering

Engineers occasionally misread the Hammerstad-Jensen ceiling ($K_r$ approaching $2.0$) as implying that skin depth $\delta$ hits a floor at the copper tooth height $\Delta$ or that conductor resistance flattens out above $15\text{ GHz}$. Recall the skin depth equation and roughness-corrected AC resistance equation:

$$\delta = \sqrt{\frac{\rho_r}{\pi f \mu_0}}, \qquad R_{\text{AC,rough}} = K_r\,\frac{\rho_r}{w_{\text{eff}}\,\delta}$$

Skin depth $\delta$ has no microwave floor and continues shrinking in inverse proportion to $\sqrt{f}$. Saturation of the Hammerstad-Jensen multiplier near $2.0$ reflects a two-dimensional grooved contour limit in which $R_{\text{AC,rough}}$ continues climbing with $\sqrt{f}$ at twice the smooth-copper slope. On three-dimensional nodular copper foils above $15\text{ GHz}$, Huray snowball scattering drives $K_r$ above $2.0$ and steepens conductor loss even further.

### The Low-Frequency Transition Where Skin Layers Overlap Inside Thin Foil

The high-frequency surface resistance formula for $R_{\text{AC}}$ assumes that skin depth $\delta$ is much thinner than the copper foil so opposing skins on the top and bottom faces never meet in the center. Recall the skin depth equation and solve for the transition frequency $f_{\text{skin}}$ where $\delta$ equals half the thickness of a $1\text{ oz}$ copper trace ($17.5\ \mu\text{m}$ out of $35\ \mu\text{m}$):

$$\delta = \sqrt{\frac{\rho_r}{\pi f_{\text{skin}} \mu_0}} \qquad \Longrightarrow \qquad f_{\text{skin}} = \frac{\rho_r}{\pi \mu_0\,\delta^2}$$

$$f_{\text{skin}} = \frac{1.72 \times 10^{-8}\ \Omega\cdot\text{m}}{\pi\,(4\pi \times 10^{-7}\text{ H/m})(1.75 \times 10^{-5}\text{ m})^2} \approx 14.2\text{ MHz}$$

Below roughly $14\text{ MHz}$, top and bottom skin layers merge across the full $35\ \mu\text{m}$ foil and trace resistance flattens onto its horizontal DC floor $R_{\text{DC}}$. Between $10\text{ MHz}$ and $100\text{ MHz}$, resistance transitions smoothly from flat $R_{\text{DC}}$ onto the $\sqrt{f}$ asymptote, creating low-frequency amplitude mismatch (**baseline wander**) during long runs of identical bits ([Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) and [Chapter 12](12_Test_Patterns_and_Jitter_Isolation.md)).

### Physical Board Remedies Matched to the Dominant Loss Regime

Different physical scaling laws for conductor loss and dielectric loss require matching any stackup change to the active frequency regime while holding characteristic impedance $Z_0$ fixed at $50\ \Omega$:

- **Low-loss dielectric laminate (cuts $k_d$ above $f_x$):** A resin with lower $\tan\delta$ directly slashes linear dielectric attenuation $\alpha_d(f)$ across multi-gigahertz Nyquist bands without altering copper skin resistance.
- **Smooth VLP or HVLP copper foil (cuts $K_r$ across multi-GHz):** Smaller RMS tooth height $\Delta$ drives the roughness multiplier $K_r$ back toward $1.0$, cutting copper loss by up to $35\%$ without changing trace width or board thickness.
- **Wider copper traces paired with thicker dielectric gaps (cuts $k_c$ at fixed $Z_0$):** Greater trace width $w$ cuts conductor loss in inverse proportion to $w$. Constant $50\ \Omega$ impedance requires increasing dielectric gap thickness $d_{\text{gap}}$ in the same proportion ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)), trading lower copper loss against a thicker PCB stackup.

With the wave and loss foundations of Part 1 complete, [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) opens Part 2 in Volume 2 by examining how high-frequency return currents navigate reference planes, layer-transition vias, plane splits, and AC-coupling capacitors.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>
