# Skin Effect and Dielectric Loss

<!-- SUMMARY: Every real transmission line dissipates signal energy through two frequency-dependent mechanisms: skin effect resistance in the conductor and molecular polarization loss in the dielectric. This guide derives both loss mechanisms from their electromagnetic origins and shows how they combine to create the insertion loss profile that defines a channel's bandwidth limit. -->

<p><em>Prefer to read this seamlessly offline? <a href="../../../assets/docs/signal-integrity-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity eBook here.</a></em></p>

A copper transmission line is not a perfect conductor, and the dielectric material surrounding it is not a perfect insulator. Both the metal and the insulator introduce frequency-dependent losses that attenuate the signal as it propagates. The two dominant loss mechanisms in high-speed PCB design are the skin effect (conductor loss) and dielectric absorption (insulator loss). Together, they cause the transmission line to behave as a physical low-pass filter, selectively attenuating the high-frequency harmonics that construct fast signal edges while passing lower-frequency content with relatively little distortion.

Understanding the physics of each mechanism separately, and then understanding how they combine, is essential for predicting signal degradation, selecting laminate materials, specifying surface roughness requirements, and designing equalization strategies that compensate for the damage.

## Core Concepts

### Resistivity vs. Resistance

The distinction between resistivity and resistance is the foundation for understanding why the skin effect increases loss at high frequencies.

Resistivity ($\rho$) is a constant chemical property of the copper atomic lattice. It describes the innate opposition to electron flow provided by the material itself and does not change with geometry. Resistance ($R$) describes the total opposition to current flow for a specific physical piece of copper, and it depends directly on the geometry of the path:

$$R = \rho \cdot \frac{L}{A}$$

where $L$ is the length of the current path and $A$ is the cross-sectional area available to carry that current.

A wide ground plane carrying DC current has an enormous cross-sectional area. Every available parallel path through the copper is utilized simultaneously, driving $A$ in the denominator to its maximum value and minimizing the total resistance. Any mechanism that reduces the usable cross-sectional area increases the resistance proportionally. The skin effect is precisely such a mechanism: it forces high-frequency current out of the interior of the conductor and into a thin surface layer, drastically reducing the effective $A$ and increasing the AC resistance.

### The Skin Effect: Eddy Current Cancellation

The skin effect is driven entirely by internal magnetic fields and induced eddy currents within the conductor.

A primary signal current flowing through a copper trace generates a surrounding magnetic field. The Right-Hand Rule dictates that this field forms concentric circles around the current axis. A longitudinal cross-section through a cylindrical conductor reveals the magnetic field pointing in one direction on the top half of the wire and the opposite direction on the bottom half.

When the primary current changes rapidly (as with a high-frequency signal), these internal magnetic fields strengthen rapidly. Faraday's Law of Induction dictates that a changing magnetic field cutting through a solid conductor induces a localized voltage. Inside the bulk copper, this changing magnetic field induces microscopic, circular currents known as eddy currents.

Lenz's Law mandates that these induced eddy currents must flow in a direction that opposes the original change that created them. The physical geometry of these circular loops is where the cancellation mechanism originates.

Consider the top half of the wire, where the primary magnetic field is strengthening. Lenz's Law requires the copper to generate an opposing field in that region. Applying the Right-Hand Rule determines the direction of the induced eddy current loop. Tracing the physical path of this loop through the conductor reveals a critical asymmetry:

- The portion of the eddy current loop located deep inside the center of the wire flows in the **opposite direction** of the primary signal current, causing cancellation.
- The portion of the loop located at the outer surface flows in the **same direction** as the primary signal current, causing reinforcement.

Examining the bottom half of the wire produces the identical result through the same Faraday-Lenz-Right-Hand-Rule chain, with appropriately reversed field directions and loop orientations. The net effect is universal throughout the conductor volume: eddy currents subtract from the primary current at the core and add to it at the surface.

Each eddy current forms a perfectly closed circular loop. A closed loop traveling in a circle contributes exactly zero net current from one end of the wire to the other. The side flowing backward cancels the side flowing forward. The eddy currents do not create new net current, nor do they destroy existing net current. They act strictly as a physical redistribution mechanism, moving the active current density from the interior to the surface.

DC signals produce zero rate of change in the magnetic field, generate zero eddy currents, and utilize the entire copper cross-section. High-frequency signals generate intense eddy currents that banish the active current flow to the outermost microscopic skin of the metal.

### The Exponential Gradient

The cancellation is not binary. It manifests as a smooth, continuous exponential gradient across the conductor cross-section.

The internal magnetic field strength inside a solid conductor is not uniform. The field is essentially zero at the exact dead center and grows steadily stronger moving outward toward the surface. A stronger magnetic field at the outer radii generates proportionally stronger eddy currents. Trillions of these overlapping circular eddy currents exist simultaneously throughout the copper volume.

Summing the effects of all overlapping loops produces an exponential decay function for the current density:

$$J = J_0 \, e^{-d/\delta}$$

where $J_0$ is the maximum current density at the absolute outer surface, $d$ is the physical depth into the conductor, and $\delta$ is the skin depth constant. At one skin depth ($d = \delta$), the current density has fallen to $1/e$ (approximately 37%) of its surface value. At five skin depths, the current is effectively zero.

The skin depth is inversely proportional to the square root of the frequency:

$$\delta \propto \frac{1}{\sqrt{f}}$$

A 10 GHz signal is forced into a microscopic outer ring of the copper trace. A 1 GHz signal penetrates deeper, utilizing more copper. A DC signal uses the entire cross-section with no restriction. The practical consequence is that high-frequency signal components encounter dramatically higher AC resistance ($R_{AC}$) than low-frequency components traveling on the same physical trace.

### The Low-Pass Filter Effect

The frequency-dependent resistance created by the skin effect causes the transmission line to function as a physical low-pass filter. Applying a voltage step to the trace launches a wavefront containing frequency harmonics spanning from DC to many gigahertz (the bandwidth determined by the rise time). The low-frequency components of that step propagate with minimal attenuation because they penetrate deep into the copper and encounter low resistance. The high-frequency components are squeezed into the thin surface layer, encounter massive AC resistance, and lose amplitude over distance.

The result is progressive degradation of the signal edge. The steep, sharp transition that left the transmitter arrives at the receiver with its high-frequency harmonics attenuated, producing a slower, rounded edge. The data rate and pattern have not changed, but the edge quality has been physically damaged by the conductor itself.

### Skin Effect and Loop Inductance

The skin effect also influences the return path geometry and the total loop inductance of the transmission line.

At high frequencies, the return current on the ground plane concentrates on the top skin of the metal, riding the surface closest to the signal trace. This bunching minimizes the vertical dielectric gap between the outbound and return currents, tightening the current loop. Inductance is proportional to the magnetic flux enclosed by the loop ($L = \Phi / I$), so a smaller geometric loop captures fewer field lines and reduces the total loop inductance.

Narrowing the active current distribution does increase the self-inductance of the return path slightly (the surrounding magnetic field becomes denser when current is concentrated in a smaller area). This penalty is real but small compared to the massive reduction in mutual loop area achieved by the tight bunching. The current distribution organically settles at the exact profile that minimizes total mathematical impedance, balancing the competing self-inductance and loop-inductance terms.

### Surface Roughness

The exponential current density profile places the highest current density at the absolute outer surface of the conductor. Any physical irregularity at that surface forces the current to travel a longer, more tortuous path around microscopic peaks and valleys of the copper grain structure. This additional path length increases the effective AC resistance beyond what the smooth-conductor skin depth formula predicts.

The Hammerstad-Jensen correction factor quantifies this roughness penalty by comparing the RMS surface roughness to the skin depth. When the roughness features are much smaller than the skin depth (at lower frequencies), the correction is negligible. When the roughness features approach or exceed the skin depth (at high frequencies, where the skin depth shrinks to micrometers), the correction becomes substantial. Low-loss PCB designs intended for multi-gigahertz operation specify smoother copper foil profiles (such as very-low-profile or hyper-low-profile copper) specifically to minimize this roughness-induced loss.

## Architecture

### Dielectric Loss: Molecular Rotation and Energy Absorption

The dielectric insulator surrounding the conductor introduces a second, independent loss mechanism. The dielectric material (FR4 fiberglass, or more advanced laminates) contains polar molecules with asymmetric charge distributions. These molecules respond physically to the electric field of the propagating electromagnetic wave.

When the wavefront passes through a section of dielectric, the intense electric field forces the polar molecules to rotate and align with the field direction. This alignment absorbs kinetic energy from the wave. The molecules do not simply snap into position; the rotation involves physical work against intermolecular forces, and a portion of the wave's energy is dissipated as heat in the process.

The loss tangent ($\tan \delta$, also called the dissipation factor or $D_f$) quantifies this energy absorption as the ratio of energy dissipated per cycle to energy stored per cycle. A higher loss tangent means the dielectric absorbs more of the wave's energy during each oscillation of the electric field. Standard FR4 has a relatively high loss tangent (approximately 0.02), making it unsuitable for multi-gigahertz serial links. Low-loss laminates such as Megtron 6 achieve loss tangents below 0.005 by using molecular structures that resist rotation more effectively.

The dielectric loss scales directly with frequency. Each cycle of the electric field forces the molecules through one full rotation-and-relaxation event, so higher-frequency signals force more absorption events per unit time. This frequency dependence makes dielectric loss, like the skin effect, a contributor to the transmission line's low-pass filter behavior.

### The Relaxation Asymmetry

A subtle but physically significant asymmetry exists in the dielectric response. The rising edge of a signal brings a massive, highly organized external force. The intense electric field of the wavefront acts on the polar molecules with the full driving power of the transmitter voltage, forcing them into strict alignment rapidly.

The falling edge simply removes this external force. The transmitter does not actively push the molecules back into their original random arrangement; it stops holding them in place. The molecules must rely entirely on ambient thermal energy to return to their neutral state. Random thermal jostling is an extremely weak and slow physical process compared to a directed electromagnetic force.

The polarization (alignment) is fast because it is actively driven. The relaxation (return to random orientation) is slow because it is passively thermal. This speed difference creates a temporal asymmetry in the dielectric response: the molecules release their stored energy gradually over a period that extends well beyond the duration of the original pulse.

### The Trailing Wake and Inter-Symbol Interference

The slow relaxation creates a physical effect analogous to the trailing wake behind a moving boat. The leading edge of a pulse creates a sharp, immediate disturbance as the molecules snap into alignment. After the pulse passes and the transmitter drops the voltage, the molecules slowly drift back to their resting state, gradually releasing their stored energy back into the copper trace.

This gradual energy release produces a lingering voltage tail that trails behind the pulse. The next data pulse arriving at the receiver rides on top of this decaying tail from the previous pulse. The receiver measures the total combined voltage at the sampling instant, and the residual energy from the old pulse physically adds to (or subtracts from) the new pulse voltage. This corruption of the receiver threshold voltage is trailing inter-symbol interference (ISI).

The asymmetry between the fast leading disturbance and the slow trailing wake is the physical reason why transmitter pre-emphasis (FFE) typically requires much stronger post-cursor correction taps than pre-cursor taps. The pre-cursor tap only needs to sharpen the immediate leading edge. The post-cursor taps must subtract voltage aggressively to flatten out the long, persistent trailing wake created by the dielectric relaxation.

## Worked Examples

### Frequency-Dependent Attenuation on a PCB Trace

Consider a 10 Gbps NRZ signal with a 30-picosecond rise time propagating on a 12-inch FR4 microstrip trace. The alternating 1010 pattern has a fundamental frequency of 5 GHz, but the 30 ps rise time requires harmonic content extending past 10 GHz to construct the edge shape.

The 5 GHz fundamental experiences moderate skin effect loss and moderate dielectric absorption. It arrives at the receiver attenuated but still with significant amplitude. The 10 GHz third harmonic encounters a skin depth that has shrunk by a factor of $\sqrt{2}$ compared to the 5 GHz case, roughly doubling the AC resistance contribution. The dielectric absorption at 10 GHz is also double that at 5 GHz, since dielectric loss scales linearly with frequency.

The combined effect is that the high-frequency harmonics responsible for the steep edges are attenuated far more heavily than the fundamental. The received signal retains its 5 GHz repetition rate but arrives with rounded, slower transitions. The eye diagram closes vertically (reduced voltage margin) and horizontally (increased timing uncertainty at the decision threshold).

### DC vs. High-Frequency Return Path Geometry

A DC test current injected into a trace spreads broadly across the ground plane, utilizing the maximum available copper cross-section. The current takes the shortest geometric path from source to sink, ignoring the trace routing entirely, because the inductance term in the impedance equation ($j\omega L$) vanishes at zero frequency. Only DC resistance matters, and spreading maximizes $A$ to minimize $R$.

The same trace carrying a 10 GHz signal produces a dramatically different return path. The massive frequency multiplier ($\omega$) causes the inductive reactance ($j\omega L$) to dominate the impedance equation completely. The return current ignores the vast expanse of available copper and crowds into a tight, narrow band directly underneath the signal trace, perfectly shadowing its physical routing. The current voluntarily accepts a higher DC resistance penalty to achieve the lowest possible loop inductance. The skin effect further confines this return current to the top surface of the ground plane (the side facing the trace), minimizing the vertical separation and tightening the loop to its physical minimum.

## Edge Cases

### Combined Loss Budget

In practice, the total insertion loss of a transmission line channel is the sum of conductor loss (skin effect plus surface roughness) and dielectric loss. At lower frequencies (below approximately 1 GHz on standard FR4), conductor loss dominates. At higher frequencies, dielectric loss grows linearly while conductor loss grows as the square root of frequency, so dielectric loss eventually overtakes conductor loss and dominates the total budget.

This crossover frequency depends on the specific laminate material and copper roughness profile. Upgrading from standard FR4 to a low-loss laminate dramatically reduces the dielectric loss contribution but does nothing for conductor loss. Specifying smoother copper foil reduces the roughness contribution but does nothing for dielectric loss. Achieving acceptable total loss at multi-gigahertz data rates typically requires addressing both mechanisms simultaneously: low-loss laminate paired with low-roughness copper.

### The Skin Depth Floor

The skin depth formula predicts that the active current layer becomes arbitrarily thin at sufficiently high frequencies. In practice, the copper surface roughness imposes a floor. Once the skin depth shrinks to the same scale as the RMS surface roughness (typically a few micrometers), the current can no longer be treated as flowing in a smooth, well-defined layer. The rough surface topology scatters the current, and the simple exponential decay model breaks down. Electromagnetic simulation tools that account for the three-dimensional roughness profile (rather than applying a scalar correction factor) provide more accurate loss predictions in this regime.
