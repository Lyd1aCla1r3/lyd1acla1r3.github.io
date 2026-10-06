# Skin Effect and Dielectric Loss

<!-- SUMMARY: Real transmission lines dissipate signal energy through frequency-dependent mechanisms. This guide derives the square-root attenuation of the skin effect and the linear attenuation of dielectric loss, demonstrating how these losses disperse edge transitions and collapse the data eye. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Chapter 2](02_Frequency_Content_of_Digital_Signals.md) described the channel as a linear, time-invariant low-pass filter and showed that any loss which grows with frequency breaks the $1/f$ proportion of a step, rounds the edge, and spreads the pulse response into neighboring bits. This chapter supplies the physical origin of that low-pass behavior. [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) found that the magnetic field inside a conductor is zero at the center and grows in proportion to the radius when the current is uniform, and it deferred the question of what happens to that current distribution when the current changes quickly.

A copper transmission line is not a perfect conductor, and the dielectric around it is not a perfect insulator. The two dominant loss mechanisms in high-speed PCB design are the skin effect, which raises the resistance of the conductor with frequency, and dielectric absorption, which grows with the frequency of the electric field in the laminate. The two mechanisms have different causes, different frequency scaling, and different remedies, so the chapter develops each from its physics and then combines them into the insertion loss that determines how many gigahertz a channel can carry.

## Core Concepts

### Resistivity versus Resistance

The distinction between resistivity and resistance is the foundation for understanding why the skin effect increases loss at high frequencies.

Resistivity ($\rho_r$) is a property of the copper lattice. It describes the opposition to charge flow that the material itself provides and does not depend on geometry. This series writes $\rho_r$ for resistivity, to keep the symbol $\Gamma$ for reflection and to avoid confusion with other uses of $\rho$. Resistance ($R$) describes the opposition of one specific piece of copper, and it depends on the geometry of the current path:

$$R = \rho_r \cdot \frac{\ell}{A}$$

where $\ell$ is the length of the current path and $A$ is the cross-sectional area available to carry the current. Annealed copper has $\rho_r = 1.72 \times 10^{-8}\ \Omega\,\text{m}$, which corresponds to a conductivity $\sigma = 1/\rho_r = 5.8 \times 10^{7}\ \text{S/m}$.

A wide ground plane carrying DC current has a large cross-section, because every parallel path through the copper carries current at once. Any mechanism that reduces the usable cross-section raises the resistance in the same proportion. The skin effect is such a mechanism: it forces high-frequency current out of the interior of the conductor and into a thin layer at the surface, which reduces the effective $A$ and raises the AC resistance.

### Why a Changing Current Cannot Stay Uniform: The Eddy-Current Procedure

The skin effect follows from the three statements of [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) applied inside a single conductor: the current produces a field (Ampere's law), the changing field induces an EMF (Faraday's law), and the EMF drives a current that opposes the change (Lenz's law). This section applies the Generation Rule and the Reaction Rule step by step to find the direction of the induced currents, and the next section derives their magnitude.

Use the desk frame of Chapter 4. A straight wire lies on the desk with the page as the desk surface, the current $I$ flows to the right, and the cross-section drawn is the plane that contains the axis of the wire, so the viewer looks down on a lengthwise slice through the copper. Assume that the current is increasing at the moment of analysis.

1. **The Generation Rule gives the direction of the primary field.** Point the right-hand thumb to the right, along the current. The fingers curl out of the desk on the upper side of the axis and into the desk on the lower side. The field inside the upper half of the wire therefore points out of the desk, the field inside the lower half points into the desk, and both grow stronger as the current grows. The field is zero on the axis and strongest at the surface, as derived in Chapter 4.
2. **Lenz's law fixes the direction of the opposing field.** The induced currents must produce a field that opposes the growth of the primary field. In the upper half of the wire the primary field points out of the desk and is growing, so the opposing field points into the desk.
3. **The Reaction Rule gives the eddy loop.** Point the right-hand thumb along the opposing field, into the desk. The fingers curl clockwise as seen from above. An eddy current loop in the upper half of the wire therefore circulates clockwise: its upper arc, nearer the surface, flows to the right, and its lower arc, nearer the axis, flows to the left.
4. **Comparison with the primary current shows the effect.** The upper arc flows in the same direction as the primary current and adds to it near the surface. The lower arc flows opposite to the primary current and subtracts from it near the axis.
5. **The lower half follows the same steps.** The primary field points into the desk and is growing, so the opposing field points out of the desk, the thumb points toward the viewer, and the loop circulates counterclockwise. Its lower arc, nearer the lower surface, flows to the right and adds to the primary current, and its upper arc, nearer the axis, flows to the left and subtracts from it.

In the end-on view, with the primary current flowing toward the reader, the top and bottom halves of the lengthwise slice correspond to the 12 o'clock and 6 o'clock positions of the circular cross-section, and the same two-step check at each position gives the same result: eddy currents add to the primary current at the surface and subtract from it at the core.

Each eddy loop is a closed circuit. A loop crosses any transverse plane of the wire twice, once in each direction, so it contributes zero net current from one end of the wire to the other. The source fixes the total current, and the eddy loops only redistribute it, drawing current density out of the interior and adding it at the surface. A decreasing current reverses the procedure: the opposing field points in the same direction as the primary field, every loop reverses, and the eddy currents add to the current at the core and subtract at the surface. In both cases the eddy currents oppose the change at the core, so the interior current lags behind the surface current. A DC current produces no changing flux and no eddy currents, and it uses the full cross-section.

The procedure gives the direction of the redistribution. The magnitude and the depth over which the interior current is suppressed follow from combining Faraday's law with Ampere's law, which the next section does.

### The Diffusion of Current into a Conductor

Consider a flat conductor surface at depth $x = 0$ with copper filling $x > 0$. The current flows in the $z$ direction, the magnetic field points in the $y$ direction, and both depend only on the depth $x$. This planar model describes a wire or a trace whose thickness is much larger than the depth analyzed, and it contains the physics of the round wire without the extra geometry.

Faraday's law relates the spatial change of the electric field to the changing flux. For fields of this orientation it reduces to:

$$\frac{\partial E_z}{\partial x} = \frac{\partial B_y}{\partial t}$$

Ampere's law relates the spatial change of the magnetic field to the current density $J_z = \sigma E_z$. The displacement-current term of Chapter 1 is negligible inside copper, because the conduction current $\sigma E$ exceeds the displacement current $\varepsilon_0\,\partial E/\partial t$ by the factor $\sigma/(\omega \varepsilon_0)$, which is about $10^{8}$ at 10 GHz. Ampere's law therefore reads:

$$\frac{\partial B_y}{\partial x} = \mu_0 \sigma E_z$$

Differentiating the second equation with respect to $x$ and substituting the first gives a single equation for the magnetic field:

$$\frac{\partial^2 B_y}{\partial x^2} = \mu_0 \sigma \frac{\partial E_z}{\partial x} = \mu_0 \sigma \frac{\partial B_y}{\partial t}$$

This is a diffusion equation, the same mathematical form as the flow of heat into a solid. It states that a magnetic field penetrates a conductor slowly, by diffusion, at a rate set by the product $\mu_0 \sigma$. Consider a field that varies as a sine wave at angular frequency $\omega$ and write it as a phasor, so that the time derivative becomes multiplication by $j\omega$ (the notation of [Chapter 3](03_Impedance_Reflections_and_Termination.md)):

$$\frac{d^2 B}{dx^2} = j\omega\mu_0\sigma\, B$$

A decaying solution has the form $B = B_0\, e^{-\gamma_s x}$, and substituting it gives $\gamma_s^2 = j\omega\mu_0\sigma$. The complex number $j$ equals $\left((1+j)/\sqrt{2}\right)^2$, because squaring gives $(1 + 2j - 1)/2 = j$. The square root of the equation is therefore:

$$\gamma_s = (1+j)\sqrt{\frac{\omega\mu_0\sigma}{2}}$$

The real part and the imaginary part of $\gamma_s$ are equal. Define the **skin depth** $\delta$ as the reciprocal of that common value:

$$\delta = \sqrt{\frac{2}{\omega\mu_0\sigma}} = \sqrt{\frac{\rho_r}{\pi f \mu_0}}$$

where the second form substitutes $\omega = 2\pi f$ and $\sigma = 1/\rho_r$. The field therefore varies as $B = B_0\, e^{-x/\delta}\, e^{-jx/\delta}$ with depth. The current density is proportional to the spatial derivative of $B$ by Ampere's law, so it has the same dependence:

$$J(x) = J_0\, e^{-x/\delta}\, e^{-jx/\delta}$$

The first exponential is the decay of the amplitude: at one skin depth the current density has fallen to $1/e$, about 37 percent of its surface value, and at five skin depths it has fallen below 1 percent. The second exponential is a phase rotation of one radian per skin depth, which is the quantitative form of the statement from the eddy-current procedure that the interior current lags the surface current. The Chapter 4 value of the field inside a wire, which grows linearly with the radius, is the DC limit in which $\delta$ is much larger than the wire.

### Skin Depth and Surface Resistance

For copper, with $\rho_r = 1.72 \times 10^{-8}\ \Omega\,\text{m}$ and $\mu_0 = 4\pi \times 10^{-7}\ \text{H/m}$, the skin depth follows directly from the formula. It shrinks in inverse proportion to the square root of the frequency:

| Frequency | Skin depth $\delta$ | Surface resistance $R_s$ |
|---|---|---|
| 1 MHz | 66 µm | 0.26 mΩ |
| 100 MHz | 6.6 µm | 2.6 mΩ |
| 1 GHz | 2.1 µm | 8.2 mΩ |
| 5 GHz | 0.93 µm | 18 mΩ |
| 10 GHz | 0.66 µm | 26 mΩ |
| 15 GHz | 0.54 µm | 32 mΩ |

The surface resistance $R_s$ in the table is derived next. A typical 1 oz PCB trace is 35 µm thick, so the current is confined to a thin layer at every frequency above a few tens of megahertz.

The total current carried by a conductor of the planar model, per unit width of surface, is the integral of the current density over depth:

$$K = \int_0^\infty J_0\, e^{-(1+j)x/\delta}\, dx = \frac{J_0\,\delta}{1+j}$$

The electric field at the surface is $E_0 = J_0/\sigma = \rho_r J_0$. The ratio of the surface field to the total current per unit width is the **surface impedance**:

$$Z_s = \frac{E_0}{K} = \rho_r\,\frac{1+j}{\delta}$$

The real part is the surface resistance and it equals the resistance of a layer of copper one skin depth thick, carrying the current uniformly:

$$R_s = \frac{\rho_r}{\delta} = \sqrt{\pi f \mu_0 \rho_r}$$

The imaginary part, which is the internal inductive reactance of the conductor, has the same value as the resistance. Both terms grow in proportion to $\sqrt{f}$. The internal reactance is small beside the external reactance $\omega L$ of the loop, and the remainder of this chapter keeps only the resistance.

For a conductor whose current flows on a surface of effective width $w_{eff}$, the AC resistance per unit length is:

$$R'_{AC} = \frac{R_s}{w_{eff}} \propto \sqrt{f}$$

The skin effect therefore does not switch on at a particular frequency. It is a smooth law in which the AC resistance equals the DC resistance at low frequency, where $\delta$ exceeds half the thickness of the conductor, and then rises as $\sqrt{f}$.

### The Skin Effect as a Low-Pass Filter

A resistance that grows with frequency attenuates the high-frequency content of an edge more than the low-frequency content, so the conductor behaves as a low-pass filter. The attenuation per unit length follows from the propagation constant derived in [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md):

$$\gamma = \sqrt{(R + j\omega L)(G + j\omega C)}$$

On a typical PCB trace $R \ll \omega L$ and $G \ll \omega C$ at multi-gigahertz frequencies. Factor out $j\omega\sqrt{LC}$ and expand each square root of the form $\sqrt{1 + \epsilon} \approx 1 + \epsilon/2$:

$$\gamma = j\omega\sqrt{LC}\,\sqrt{1 + \frac{R}{j\omega L}}\,\sqrt{1 + \frac{G}{j\omega C}} \approx j\omega\sqrt{LC}\left(1 + \frac{R}{2j\omega L} + \frac{G}{2j\omega C}\right)$$

Multiplying through and using $Z_0 = \sqrt{L/C}$ gives:

$$\gamma \approx j\omega\sqrt{LC} + \frac{R}{2 Z_0} + \frac{G Z_0}{2}$$

The imaginary part is the phase constant of the lossless line. The real part is the attenuation constant $\alpha$ in nepers per unit length, with a conductor contribution $\alpha_c = R/(2Z_0)$ and a dielectric contribution $\alpha_d = G Z_0/2$. The voltage of a forward wave falls as $e^{-\alpha z}$, so a length $\ell$ attenuates the voltage by the factor $e^{-\alpha\ell}$. Chapter 8 defines the decibel from the power ratio, and the voltage form $20\log_{10}$ gives the loss in dB of the same factor:

$$\text{loss (dB)} = -20 \log_{10}\left(e^{-\alpha \ell}\right) = 20\,\alpha\ell\,\log_{10} e \approx 8.686\,\alpha\ell$$

The conductor loss is therefore $\alpha_c = R'_{AC}/(2Z_0)$, and since $R'_{AC}$ is proportional to $\sqrt{f}$, so is $\alpha_c$. This is the quantitative form of the statement in Chapter 2: the loss no longer matches the $1/f$ proportion of the step spectrum, so the high frequencies that form the edge are removed faster than the low frequencies that form the plateau.

### Skin Effect and the Return Path

The return current on the ground plane obeys the same physics. Its distribution is set by the competition between resistance and inductance, and at high frequency the current gathers directly under the trace in a layer one skin depth thick, on the surface facing the trace. [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) derived the loop inductance and the small self-inductance penalty that this crowding pays, and [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) follows the resulting return path through vias, slots, and plane splits.

### Surface Roughness

The current density is largest at the conductor surface, so any irregularity there forces the current along a longer path around the peaks and valleys of the copper grain structure. The extra path length raises the effective resistance above the smooth-surface value $R_s$.

The standard model, due to Hammerstad and Jensen, multiplies the smooth-surface resistance by a correction factor that depends on the RMS roughness $\Delta$ of the surface compared with the skin depth:

$$K_r = 1 + \frac{2}{\pi}\arctan\left[1.4\left(\frac{\Delta}{\delta}\right)^2\right]$$

This is an empirical fit, and the book states it without derivation because deriving it requires solving the field equations over a rough boundary. The formula has two limits that carry the physical content. The argument of the arctangent is small when the roughness is much smaller than the skin depth, so $K_r \approx 1$ and the surface behaves as a smooth one. The arctangent approaches $\pi/2$ when the roughness greatly exceeds the skin depth, so $K_r$ saturates at 2, and the resistance of a rough conductor at very high frequency is at most about twice the smooth value. Assume $\Delta = 1\ \mu\text{m}$ of RMS roughness, a value typical of standard foil. At 1 GHz ($\delta = 2.1\ \mu\text{m}$) the factor is 1.20, at 5 GHz it is 1.65, and at 10 GHz ($\delta = 0.66\ \mu\text{m}$) it is 1.81. Foils with an RMS roughness of 0.3 µm give 1.02, 1.09, and 1.18 at the same three frequencies. Low-loss designs intended for multi-gigahertz operation therefore specify very low profile or hyper very low profile copper foil.

## Architecture

### Dielectric Loss: Polarization That Lags the Field

The laminate surrounding the trace contains polar molecules, which are molecules with an asymmetric distribution of charge. The electric field of the propagating wave exerts a torque on each molecule and rotates it toward alignment with the field. The alternating field reverses direction every half cycle, and the molecules follow it with a delay, because the rotation does work against the forces that bind each molecule to its neighbors. The polarization of the material therefore lags the field by a small angle, and the work done during the lag is dissipated as heat.

The lag has a compact mathematical form. A lossless capacitor with a dielectric of permittivity $\varepsilon'$ has capacitance $C$ and carries a current $I = j\omega C V$, which leads the voltage by exactly 90°. The lag of the polarization is described by giving the permittivity an imaginary part, $\varepsilon = \varepsilon' - j\varepsilon''$, which multiplies the capacitance by $(1 - j\tan\delta)$, with the **loss tangent**:

$$\tan\delta = \frac{\varepsilon''}{\varepsilon'}$$

The current of the capacitor then has two parts:

$$I = j\omega C\,(1 - j\tan\delta)\,V = j\omega C V + \omega C \tan\delta\,V$$

The first term is the ordinary capacitive current, 90° ahead of the voltage. The second term is in phase with the voltage, so it behaves as a conductance, and it identifies the shunt conductance that [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) introduced:

$$G = \omega C \tan\delta$$

The average power dissipated in this conductance is $\tfrac{1}{2}G|V|^2$, and the reactive power exchanged with the field is $\tfrac{1}{2}\omega C|V|^2$. The loss tangent is therefore the ratio of the power dissipated to the reactive power, and the angle $\delta$ is the amount by which the current deviates from a pure 90° lead. The dissipation factor $D_f$ quoted in laminate datasheets is the same quantity.

The conductance is proportional to frequency, because the same fraction of the stored energy is lost on every cycle, and there are more cycles per second at higher frequency. The dielectric attenuation follows from the result of the previous section, $\alpha_d = G Z_0/2$. Substituting $G = \omega C\tan\delta$ and using $Z_0 C = \sqrt{L/C}\cdot C = \sqrt{LC} = 1/v_p$ gives:

$$\alpha_d = \frac{\omega \tan\delta}{2 v_p} = \frac{\pi f \sqrt{\varepsilon_r}\,\tan\delta}{c}$$

The velocity $v_p = c/\sqrt{\varepsilon_r}$ comes from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md). The dielectric attenuation grows linearly with frequency and does not depend on the width or the geometry of the trace.

Standard FR4 has $\tan\delta \approx 0.02$, which makes it unsuitable for multi-gigahertz serial links over long traces. Low-loss laminates such as Megtron 6 have loss tangents below 0.005, because their resin systems contain fewer polar groups that rotate and lag the field, so less energy is dissipated on each cycle. This chapter uses $\tan\delta = 0.004$ as a representative value for such materials and assumes that $\tan\delta$ is constant with frequency, a common first approximation, since the loss tangent of real laminates varies only slowly over the range of interest.

Assume the propagation delay of about 170 ps per inch from Chapter 1, which corresponds to $\sqrt{\varepsilon_r} \approx 2.04$. At 5 GHz the dielectric attenuation of FR4 is $\alpha_d = \pi \cdot 5\times10^9 \cdot 2.04 \cdot 0.02 / (3\times10^8) = 2.14$ Np/m, which is $18.6$ dB/m or $0.47$ dB per inch. The same expression for $\tan\delta = 0.004$ gives 0.094 dB per inch.

### The Loss Is Symmetric: Rising Edges and Falling Edges

The molecular picture above might suggest that the dielectric responds quickly to an applied field and relaxes slowly after the field is removed, and that this asymmetry produces the long trailing tail of a pulse. The picture is not correct for the signal levels of a PCB, and the correction matters for the equalization chapters.

A laminate driven with signals of a few hundred millivolts is a linear material: doubling the field doubles the polarization, and the response to a sum of fields is the sum of the responses. A linear system treats a falling edge as the exact negative of a rising edge. The polarization current that follows a rising edge and the polarization current that follows a falling edge have the same shape and opposite signs, and no part of the response is faster or slower in one direction. The trailing tail of a pulse arises in a different way, which the next section develops.

### The Causal Low-Pass Tail and Inter-Symbol Interference

A channel with attenuation that grows with frequency has two properties that together produce a tail in the time domain.

The first property is **causality**: the output cannot begin before the input. The magnitude and the phase of a causal channel are not independent, and a magnitude response that falls with frequency requires a phase response that varies with frequency, so that the sine waves composing an edge arrive with different delays. A pulse whose components are attenuated by different amounts and delayed by different amounts cannot reassemble into its original shape. The leading edge arrives rounded, and the energy that is delayed arrives after the main response.

The second property is the **shape of the attenuation**. The skin effect gives a useful exact case. Using the form $\gamma \approx j\omega\sqrt{LC} + R/(2Z_0)$ with the surface impedance $Z_s = R_s(1+j)$ in place of $R$, the voltage transfer function of a conductor-loss line of length $\ell$ is:

$$H(f) = e^{-j\omega\tau_d}\;\exp\!\left[-(1+j)\,a\sqrt{f}\right], \qquad a = \frac{\ell\, R_s}{2 Z_0\, w_{eff}\,\sqrt{f}}$$

where $\tau_d$ is the lossless delay and $a$ is a constant of the line, measured in $\text{s}^{1/2}$. Using $(1+j)\sqrt{f} = \sqrt{j\omega/\pi}$ the exponent becomes $-(a/\sqrt{\pi})\sqrt{j\omega}$, which has the form $e^{-k\sqrt{s}}$ with $s = j\omega$ and $k = a/\sqrt{\pi}$. The step response of this transfer function is a standard Laplace transform pair, which the book states without derivation:

$$s_r(t') = \operatorname{erfc}\!\left(\frac{a}{2\sqrt{\pi\, t'}}\right), \qquad t' = t - \tau_d$$

where $\operatorname{erfc}$ is the complementary error function, which Chapter 11 defines and uses. The result is a step response that rises from zero and approaches its final value with a tail that falls as $1/\sqrt{t'}$, a much slower approach than the exponential of a single-pole filter. A step response of this shape never settles in a few unit intervals, so the voltage left over from a past bit still affects bits that arrive many unit intervals later.

The dielectric adds a second long tail. A material whose loss tangent is nearly constant over many decades of frequency, as FR4 is, contains polarization mechanisms with relaxation times spread across those decades. The time-domain polarization of such a material decays as a power law in time, not as a single exponential, and the polarization current continues to flow long after a step. The mechanism is linear and symmetric, and it adds to the conductor tail.

The pulse response of Chapter 2 is the step response minus a copy of itself delayed by one unit interval, so a long step-response tail is a long post-cursor tail. The tail has a signature that follows from the causal low-pass nature of the channel: a main cursor that is lower than the input pulse, a very small pre-cursor (a causal channel produces little response before the main arrival), and a larger series of post-cursors that decay slowly. A receiver sampling at the center of one bit therefore sees the sum of the main cursor and the decaying contributions of all earlier bits, and this sum is inter-symbol interference. The size of the first post-cursor relative to the pre-cursor is the reason that the transmitter equalization of [Chapter 13](13_Transmitter_FFE.md) needs more post-cursor correction than pre-cursor correction.

### Combined Insertion Loss

The total attenuation is the sum of the two contributions, $\alpha = \alpha_c + \alpha_d$, and the loss in decibels is proportional to the length. The two terms scale differently:

$$\alpha_c = k_c\sqrt{f}, \qquad \alpha_d = k_d\, f$$

where $k_c = R_s/(2 Z_0 w_{eff}\sqrt{f})$ and $k_d = \pi\sqrt{\varepsilon_r}\tan\delta / c$ are constants of the line. The two contributions are equal at the **crossover frequency**:

$$k_c\sqrt{f_x} = k_d\, f_x \quad \Rightarrow \quad f_x = \left(\frac{k_c}{k_d}\right)^2$$

Below $f_x$ the conductor dominates, and above it the dielectric dominates. The crossover frequency rises as the dielectric loss falls, so a low-loss laminate pushes the dielectric-dominated region to a higher frequency, and it falls as the conductor loss falls, so smooth copper has the opposite effect. The Worked Examples section computes both cases for a specific line.

The exact attenuation of a real line includes further effects: the roughness factor $K_r$ multiplies $\alpha_c$, the loss tangent of real laminates varies slowly with frequency, and the current distribution across a trace is not uniform. These effects are modeled by field solvers and measured with the VNA techniques of [Chapter 8](08_S_Parameters_and_VNA.md), and the equations above give the trend and the order of magnitude that a designer needs for a first estimate.

## Worked Examples

### Skin Depth and AC Resistance of a Stripline Trace

Assume a stripline trace 0.1 mm wide (about 4 mil) and 35 µm thick, with copper on both faces carrying current, so that the effective width of the current layer is $w_{eff} = 0.2$ mm. This is a simplified model that ignores the current on the edges and the non-uniform distribution across the width.

The DC resistance per meter is the resistivity divided by the cross-sectional area:

$$R'_{DC} = \frac{\rho_r}{w t} = \frac{1.72\times10^{-8}}{(0.1\times10^{-3})(35\times10^{-6})} = 4.9\ \Omega/\text{m} \quad (0.125\ \Omega/\text{in})$$

At 1 GHz the skin depth is 2.1 µm, which is much smaller than the 35 µm thickness, so the skin-effect model applies. The surface resistance is $R_s = \rho_r/\delta = 8.2\ \text{m}\Omega$, and the AC resistance per meter is:

$$R'_{AC} = \frac{R_s}{w_{eff}} = \frac{8.2\times10^{-3}}{0.2\times10^{-3}} = 41\ \Omega/\text{m} \quad (1.05\ \Omega/\text{in})$$

The AC resistance is 8.4 times the DC resistance at 1 GHz. The conductor attenuation on a 50 Ω line is $\alpha_c = R'_{AC}/(2Z_0) = 0.41$ Np/m, which is $0.091$ dB per inch. The 41 Ω/m is small compared with $\omega L' = 2\pi\,(10^9)(342\ \text{nH/m}) = 2150\ \Omega/\text{m}$, which uses the $L'$ of Chapter 4, so the approximation $R \ll \omega L$ used for $\gamma$ holds.

### Loss Budget of a 12 Inch FR4 Stripline

Consider a 10 Gbps NRZ signal with a 30 ps rise time on a 12 inch FR4 stripline with the trace of the previous example and $\tan\delta = 0.02$. The 1010 pattern has a fundamental of 5 GHz, the Nyquist frequency of [Chapter 2](02_Frequency_Content_of_Digital_Signals.md). The rise time corresponds to an edge bandwidth of $0.35/30\ \text{ps} = 11.7$ GHz, so the edge carries content above the fundamental. The square-wave series of Chapter 2 places the next component of the 1010 pattern at the third harmonic, 15 GHz, with one third of the fundamental amplitude.

The attenuation of each component follows from the equations above:

| Frequency | Conductor (dB/in) | Dielectric (dB/in) | Total (dB/in) | 12 in total (dB) | Voltage factor |
|---|---|---|---|---|---|
| 5 GHz | 0.20 | 0.47 | 0.67 | 8.1 | 0.39 |
| 15 GHz | 0.35 | 1.41 | 1.76 | 21.2 | 0.087 |

The conductor loss grows by a factor of $\sqrt{3} = 1.73$ between 5 GHz and 15 GHz, and the dielectric loss grows by a factor of 3. The skin depth shrinks by the same factor $\sqrt{3}$ and the resistance rises by it. The fundamental arrives at 39 percent of its input amplitude, and the third harmonic arrives at 8.7 percent. The ratio of the third harmonic to the fundamental, which was one third at the transmitter, becomes $(1/3)(0.087/0.39) = 0.074$ at the receiver. The harmonic that sharpens the edge has fallen from 33 percent of the fundamental to 7 percent, and the received waveform keeps its 5 GHz repetition rate with a rounded edge. The consequences for the eye diagram are the subject of [Chapter 10](10_Jitter_Decomposition_and_Measurement.md).

The two crossover frequencies follow from the constants of the line. The conductor and dielectric attenuations at 1 GHz are 0.091 dB per inch and 0.094 dB per inch for $\tan\delta = 0.02$, so $k_c/k_d = \sqrt{f_x}$ gives $f_x = 0.93$ GHz, which agrees with the statement that conductor loss dominates below about 1 GHz on FR4. For $\tan\delta = 0.004$ the dielectric attenuation at 1 GHz is 0.019 dB per inch, and the crossover moves to 23 GHz. A low-loss laminate therefore changes the dominant mechanism at 10 to 15 GHz from the dielectric to the conductor, and at that point only the conductor can be improved, by smoother copper.

### Pulse Response of a Skin-Effect Channel

Use only the conductor loss of the 12 inch line above. The attenuation at 5 GHz is $\alpha_c \ell = 0.28$ Np (2.4 dB), which gives $a = 0.28/\sqrt{5\times10^9} = 3.97\times10^{-6}\ \text{s}^{1/2}$. The step response $\operatorname{erfc}\!\left[a/(2\sqrt{\pi t'})\right]$ at the unit interval of 100 ps has the following values:

| Time after arrival $t'$ | Step response |
|---|---|
| 10 ps | 0.62 |
| 100 ps (1 UI) | 0.874 |
| 200 ps | 0.911 |
| 300 ps | 0.927 |
| 1 ns (10 UI) | 0.960 |
| 10 ns (100 UI) | 0.987 |

The line has delivered 87 percent of the final voltage after one unit interval, and 4 percent is still missing after ten unit intervals. The pulse response at the sampling instants is the step response minus the step response one unit interval earlier. The main cursor equals the step response at one unit interval, 0.874. The first post-cursor is $0.911 - 0.874 = 0.037$, which is 4.2 percent of the main cursor. The next ones are 0.016 (1.9 percent), 0.0097 (1.1 percent), and 0.0067 (0.8 percent). The sum of the first seven post-cursors is 9 percent of the main cursor. In the worst case, when all seven preceding bits have the opposite value, a receiver sampling a bit sees an interference of about 9 percent of the bit amplitude, before any dielectric loss is added.

## Edge Cases

### The Roughness Factor Saturates, and the Skin Depth Does Not

The skin depth formula $\delta = \sqrt{\rho_r/(\pi f \mu_0)}$ has no floor. It continues to fall as $1/\sqrt{f}$ at every frequency for which the copper behaves as a classical conductor, and no roughness changes that. Roughness changes the resistance of the conductor. A skin depth smaller than the RMS roughness means that the correction factor $K_r$ of the Hammerstad model has reached its limit of about 2, the current follows the contour of the surface, and the resistance continues to rise as $\sqrt{f}$ at twice the smooth value. The Hammerstad model is a scalar correction and neglects the three-dimensional shape of the grain, so models that resolve the roughness profile give more accurate loss predictions when the skin depth is below the roughness.

### The Transition from DC Resistance to Skin Resistance

The $\sqrt{f}$ law applies once the skin depth is much smaller than the thickness of the conductor. A 35 µm trace has $\delta = 17.5$ µm, half its thickness, at 14 MHz, and the AC resistance equals the DC resistance well below that frequency. Between roughly 10 and 100 MHz the resistance transitions smoothly from the DC value to the skin-effect value. The transition has no consequence for signals whose spectrum lies above 100 MHz, but it matters for low-frequency effects such as the settling of the DC level and the baseline wander of [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md).

### Which Loss Mechanism to Improve

The crossover frequency determines which remedy helps. Replacing standard FR4 with a low-loss laminate reduces $k_d$ and has no effect on $k_c$, and specifying smoother copper reduces $K_r$ and has no effect on $k_d$. A link at 5 GHz on FR4 is dominated by the dielectric (0.47 dB per inch against 0.20 dB per inch), so the laminate is the first choice. The same link on a low-loss laminate is dominated by the conductor (0.20 dB per inch against 0.094 dB per inch at 5 GHz), so the next improvement comes from copper profile and trace width. Wider traces lower $R'_{AC}$ in proportion to $w_{eff}$, which lowers $\alpha_c$ and also changes the impedance, so the width is chosen together with the dielectric thickness to hold $Z_0$ at its target.

[Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) examines the other half of the current loop: where the return current flows, and how vias, slots, and plane splits disturb it.
