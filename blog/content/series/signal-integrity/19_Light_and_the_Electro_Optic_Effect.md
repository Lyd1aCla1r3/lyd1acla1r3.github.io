# Light as an Electromagnetic Wave and the Electro-Optic Effect

<!-- SUMMARY: The coherent optical links of Part 6 carry data on the amplitude and phase of a light wave, and that wave obeys the same field equations as the signals of Part 1. This guide derives the wave equation of light from Faraday's law and the Ampere-Maxwell law, which gives the speed $c/n$, the refractive index $n = \sqrt{\epsilon_r}$, the impedance of a medium, and the reflection at an interface with the reflection coefficient of Chapter 3. It then defines amplitude, phase and polarization (including why two orthogonal polarizations carry independent data without any rule that fields of different kinds do not interact), derives the phase accumulated in a medium, and explains how a voltage changes the refractive index of lithium niobate through the Pockels effect. The result is the phase shift per volt, the half-wave voltage, and the bandwidth limit that the velocity mismatch between the electrical wave and the optical wave imposes on the electrode. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Line Coding, FEC, and Protocol Framing](18_Line_Coding_FEC_and_Protocol_Framing.md) closed the electrical story of a serial link with a stream of corrected bits. A coherent optical link starts from the same bits, and it differs in the carrier: the symbols ride on the amplitude and phase of a light wave at about 193 THz, and the signal travels through glass instead of copper. The field equations that [Wave Propagation and Transmission Lines](01_Wave_Propagation_and_Transmission_Lines.md) used for a trace apply without change to that light wave, so the reader already owns most of the physics. This chapter shows the correspondence and then derives the one new ingredient, the electro-optic effect that lets a voltage control the phase of the wave.

## Core Concepts

### The Wave Equation of Light

[Wave Propagation and Transmission Lines](01_Wave_Propagation_and_Transmission_Lines.md) and [Inductance, Magnetic Coupling, and Crosstalk](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) name two laws: Faraday's law (a changing magnetic flux produces an electric field) and the Ampere-Maxwell law (a changing electric field produces a magnetic field). Together they produce a self-sustaining wave, and a short derivation shows its speed. Consider a wave that travels along $z$, with the electric field along $x$ and the magnetic field along $y$, in a region without charge or current. The two laws reduce to one equation each:

$$\frac{\partial E_x}{\partial z} = -\frac{\partial B_y}{\partial t}, \qquad -\frac{\partial B_y}{\partial z} = \mu_0\varepsilon_0\,\frac{\partial E_x}{\partial t}$$

Differentiate the first equation with respect to $z$, exchange the order of the derivatives, and insert the second equation:

$$\frac{\partial^2 E_x}{\partial z^2} = -\frac{\partial}{\partial t}\frac{\partial B_y}{\partial z} = \mu_0\varepsilon_0\,\frac{\partial^2 E_x}{\partial t^2}$$

This is a wave equation, and the function $E_x(z,t) = E_0\cos(kz - \omega t + \varphi)$ satisfies it when $k^2 = \mu_0\varepsilon_0\,\omega^2$. The speed of the pattern, $v = \omega/k$, is therefore $1/\sqrt{\mu_0\varepsilon_0} = 2.998 \times 10^{8}$ m/s, the speed of light $c$. In a dielectric with the permittivity $\varepsilon = \varepsilon_0\varepsilon_r$ the same steps give

$$v = \frac{1}{\sqrt{\mu_0\varepsilon_0\varepsilon_r}} = \frac{c}{\sqrt{\varepsilon_r}} = \frac{c}{n}, \qquad n = \sqrt{\varepsilon_r}$$

which is the velocity $c/\sqrt{\varepsilon_r}$ of Chapter 1 under the optical name **refractive index** $n$. The wave needs no conductor to guide it, because the two fields sustain each other and carry the energy between them.

The first equation also fixes the ratio of the two fields. Assume the fields $E_x = E_0\cos(kz-\omega t)$ and $B_y = B_0\cos(kz-\omega t)$, for which $\partial E_x/\partial z = -kE_0\sin(kz-\omega t)$ and $-\partial B_y/\partial t = -\omega B_0\sin(kz-\omega t)$, and equating the two gives $B_0 = kE_0/\omega = E_0/v$. The ratio of the electric to the magnetic field strength $H = B/\mu_0$ is the **wave impedance** of the medium:

$$\eta = \frac{E}{H} = \mu_0 v = \sqrt{\frac{\mu_0}{\varepsilon_0\varepsilon_r}} = \frac{\eta_0}{n}, \qquad \eta_0 = \sqrt{\frac{\mu_0}{\varepsilon_0}} = 376.7\ \Omega$$

The electric field plays the role of the voltage, the magnetic field strength plays the role of the current, and $\eta$ plays the role of $Z_0$. The correspondence has numerical consequences that the next sections use:

| Transmission line (Part 1) | Light in a dielectric |
|---|---|
| Voltage $V$, current $I$ | Electric field $E$, magnetic field strength $H$ |
| Characteristic impedance $Z_0$ | Wave impedance $\eta = \eta_0/n$ |
| Velocity $c/\sqrt{\varepsilon_r}$ | Phase velocity $c/n$ |
| Power $P = V^2/R$ | Intensity $I = E^2/\eta$ (time average $\tfrac12 n \varepsilon_0 c E_0^2$) |
| Reflection coefficient $\Gamma$ | Fresnel coefficient at normal incidence |
| Delay $\tau = \ell/v$ and phase $\theta = -360^\circ f\tau$ | Delay $\tau = nL/c$ and phase $\omega\tau$ |

### Amplitude, Phase, Frequency, and Wavelength

The wave $E_0\cos(kz - \omega t + \varphi)$ has four parameters, which the next sentences define in turn. The **amplitude** $E_0$ is the peak field strength, and the intensity is proportional to $E_0^2$ as the power of a voltage is proportional to $V^2$ ([S-Parameters and VNA](08_S_Parameters_and_VNA.md) derives that factor). The **phase** $\varphi$ places the wave in its cycle at a chosen point and time. The angular frequency $\omega = 2\pi f$ gives the number of oscillations per second, and the wavenumber $k = 2\pi/\lambda$ gives the number per meter. The telecommunication band near $\lambda_0 = 1550$ nm (the wavelength in vacuum) corresponds to

$$f = \frac{c}{\lambda_0} = 193.4\ \text{THz}, \qquad T = \frac{1}{f} = 5.17\ \text{fs}$$

so one optical cycle lasts 5.17 femtoseconds, and the data symbols of Chapter 20 (tens of picoseconds) span several thousand cycles each.

A wave that crosses the boundary between two media keeps its frequency. The field at the interface must be continuous at every instant, and two sinusoids on the two sides can match at all times only if they oscillate at the same frequency. The speed changes to $c/n$, so the relation $v = f\lambda$ forces the wavelength to shrink to $\lambda = \lambda_0/n$. In lithium niobate with $n = 2.14$ the 1550 nm light has a wavelength of 725 nm and travels at 0.468 $c$. The energy of a photon, $hf$, depends on the frequency alone, so it does not change either.

### Phase as Accumulated Delay

A wave that travels the length $L$ in a medium of index $n$ accumulates the phase

$$\phi = kL = \frac{2\pi n L}{\lambda_0} = \omega\,\frac{nL}{c} = \omega\tau$$

with the delay $\tau = nL/c$, which is the relation $\theta = -360^\circ f\tau$ of Chapter 8 in another notation, evaluated at a frequency $10^{4}$ times higher than a microwave measurement. The consequence is the central fact of optical modulation: a delay of half a cycle, $T/2 = 2.6$ fs, changes the phase by $180^\circ$, so a tiny change of the delay (the light travels 0.78 $\mu$m in that time in vacuum) controls the phase completely. A delay of one full period, 5.17 fs, changes the phase by $2\pi$ and is indistinguishable from no delay, so a delay change of a few femtoseconds covers the whole range of phases.

A steady phase offset leaves the frequency unchanged. A phase that changes with time does shift the instantaneous frequency by $\Delta f = (1/2\pi)\,d\phi/dt$. A phase ramp of $\pi$ in 10 ps corresponds to $\Delta f = (\pi/10\ \text{ps})/2\pi = 50$ GHz, which is the way in which a modulated carrier acquires the sidebands of the spectrum in [Frequency Content of Digital Signals](02_Frequency_Content_of_Digital_Signals.md): the electrical bandwidth of the data appears as optical bandwidth around the carrier.

### Reflection at an Interface

The impedance correspondence gives the reflection at a boundary with the same expression as [Impedance, Reflections, and Termination](03_Impedance_Reflections_and_Termination.md). For normal incidence, with the impedances $\eta_1 = \eta_0/n_1$ and $\eta_2 = \eta_0/n_2$,

$$\Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1} = \frac{n_1 - n_2}{n_1 + n_2}$$

and the power reflected is $\Gamma^2$, as in Chapter 3. The boundary from glass of index 1.444 (fiber) to lithium niobate (2.14) has $\Gamma = -0.194$ and reflects 3.75 percent of the power, a return loss of 14.3 dB, and the boundary from air to lithium niobate has $\Gamma = -0.363$ and reflects 13.2 percent (8.8 dB). The negative sign is the phase flip of a wave that enters a medium of lower impedance, the same sign as the reflection from a trace that meets a lower impedance. Index matching layers and angled facets are the optical counterparts of termination and of the impedance taper.

### Polarization

The electric field of the wave oscillates along a direction in the plane perpendicular to the travel direction, and that direction is the **polarization**. A wave polarized along $x$ and a wave polarized along $y$ travel in the same direction through the same glass core. A general field is the sum of the two components with complex amplitudes $E_x$ and $E_y$, and the intensity is the sum of the two intensities,

$$I \propto |E_x|^2 + |E_y|^2$$

with no cross term, because the dot product of two perpendicular field directions is zero. The two polarizations therefore add in power and do not interfere, which makes them two independent channels. The wave of each channel has its own magnetic field, along $y$ for the $x$-polarized wave and along $-x$ for the $y$-polarized wave, and the two pairs of fields exist at the same points in the fiber.

The old rule that electric fields interact only with electric fields and magnetic fields only with magnetic fields does not describe this system. The fields obey the *linear superposition* of Maxwell's equations: the total electric field at a point is the vector sum of all the electric fields present, and each polarization component propagates through an isotropic medium as if the other were absent. The channels are independent because the glass does not couple them, so the cause is a property of the medium and not a rule about field types. A medium that does couple them, such as a fiber with a bend or a birefringent crystal, mixes the two components, and [Wideband Signal Analysis and EVM](21_Wideband_Signal_Analysis.md) shows how the receiver separates them again.

## Architecture

### Dual-Polarization Transmitter Layout

A coherent transmitter uses both polarizations to double the capacity, and the layout follows from the independence above. The laser emits one steady polarized beam, and a **power splitter** (not a polarization beam splitter) divides it into two beams of half the power. A polarization beam splitter divides light according to its polarization, so it would send a polarized input entirely to one port unless the input is aligned at 45 degrees. Each beam enters its own modulator array, which Chapter 20 describes, and carries its own data stream. The beam of the second branch passes a **polarization rotator** that turns its field by 90 degrees, so the two branches become orthogonal. A **polarization beam combiner** merges them into the single beam that enters the fiber. The same component, run in the opposite direction, serves as the polarization beam splitter at the receiver, where it separates the two components again.

### The Electro-Optic Modulator Crystal

A modulator needs a material whose refractive index depends on an applied electric field. Lithium niobate has this property, and it is the material of most coherent modulators. The electric field of the electrode pulls the electron clouds and the ions of the crystal lattice slightly out of their positions, and the change of the lattice changes the polarizability and thus $\varepsilon_r$ and $n$. The effect that is *linear* in the field is the **Pockels effect**, which exists only in crystals without a center of symmetry, because a center of symmetry would require the index change to be the same for $+E$ and $-E$, which excludes a term linear in $E$.

The index change is defined through the **impermeability** $1/n^2$, which the field changes linearly with the electro-optic coefficient $r$ (Tier 2: the coefficient is a tensor, and the value of the relevant component $r_{33}$ comes from a measurement or a lattice calculation):

$$\Delta\!\left(\frac{1}{n^2}\right) = r\,E$$

Differentiating $1/n^2$ with respect to $n$ gives $\Delta(1/n^2) = -2\Delta n/n^3$, and so

$$\Delta n = -\tfrac12\,n^3\,r\,E$$

For light polarized along the crystal axis of largest coefficient, $n = n_e = 2.14$ and $r_{33} = 30.8$ pm/V at 1550 nm (typical literature values, which differ between crystal grades). An electrode pair with the gap $g$ and a voltage $V$ produces the field $E = V/g$. The extra phase of light that travels the length $L$ in this field is

$$\Delta\phi = \frac{2\pi}{\lambda_0}\,\Delta n\,L = -\frac{\pi\,n^3 r_{33}\,V\,L}{\lambda_0\,g}$$

The minus sign shows that the phase decreases as the index decreases and is only a convention for the direction of the voltage. The voltage that gives a phase magnitude of $\pi$ is the **half-wave voltage**:

$$V_\pi = \frac{\lambda_0\,g}{n^3 r_{33}\,L}$$

so the product $V_\pi L$ is a property of the crystal and the electrode geometry. The relation shows the design trade: a narrow gap raises the field per volt, a long electrode accumulates more phase, and both improve $V_\pi$ at a price (optical loss from the nearby metal for the narrow gap, and electrical bandwidth for the long electrode, as the next section shows).

### Traveling-Wave Electrodes and the Bandwidth Limit

A lumped electrode of length $L$ would be a capacitor, and its bandwidth would be set by the RC product of Chapter 3. Practical modulators use a **traveling-wave electrode**, a transmission line along the optical waveguide, so that the electrical signal travels in the same direction as the light. [Wave Propagation and Transmission Lines](01_Wave_Propagation_and_Transmission_Lines.md) gives the electrical wave the velocity $c/n_m$ with the effective microwave index $n_m$, and the light travels at $c/n_o$. A mismatch $\Delta n = n_m - n_o$ makes the electrical wave move relative to the optical wave, and the optical wave samples a drive voltage that changes along its path.

Consider a sinusoidal drive at the frequency $f$. The drive voltage $\cos[2\pi f(t - z\,n_m/c)]$ travels with the microwave index $n_m$, and a slice of light that enters at time $t_0$ is at the position $z = (c/n_o)(t - t_0)$ at time $t$, and it sees the drive phase $2\pi f t_0 - 2\pi f z\,\Delta n/c$ there, so the drive that the slice sees drifts with its position by $2\pi f z\,\Delta n/c$. The phase that the slice accumulates is proportional to the integral of this drive over the electrode, and the magnitude of the integral relative to its value for a matched wave is

$$\left|\frac{1}{L}\int_0^L e^{-j2\pi f\,\Delta n\,z/c}\,dz\right| = \left|\frac{\sin x}{x}\right|, \qquad x = \frac{\pi f\,\Delta n\,L}{c}$$

This is the same sinc response as the aperture of a sampling oscilloscope in [SerDes Architecture and Eye Diagrams](16_SerDes_Architecture_and_Eye_Diagrams.md), and its $-3$ dB point (the amplitude factor $1/\sqrt2$) lies at $x = 1.392$:

$$f_{3\text{dB}} = \frac{1.392\,c}{\pi\,\Delta n\,L} \approx \frac{0.44\,c}{\Delta n\,L}$$

The bandwidth falls in proportion to the length and the velocity mismatch, and the product of $V_\pi$ and bandwidth cannot be improved by lengthening the electrode: doubling $L$ halves $V_\pi$ and halves $f_{3dB}$. The formula assumes a lossless line terminated in its characteristic impedance. The conductor and dielectric losses of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) reduce the bandwidth further, and an electrode that is not terminated reflects the drive as in Chapter 3.

## Worked Examples

### Frequency and Wavelength at 1550 nm

The vacuum wavelength 1550 nm gives $f = 299{,}792{,}458/1.55\times10^{-6} = 193.41$ THz and a period of 5.170 fs, and the wavenumber is $2\pi/\lambda_0 = 4.054\times10^{6}$ rad/m. Inside lithium niobate the wavelength is $1550/2.138 = 725$ nm, the speed is 0.468 $c$, and the wave impedance is $376.7/2.138 = 176.2\ \Omega$.

### Reflection at the Fiber and Crystal Facets

The boundary from fiber ($n = 1.444$) to lithium niobate ($n = 2.138$) gives $\Gamma = (1.444 - 2.138)/(1.444 + 2.138) = -0.194$. The reflected power is $\Gamma^2 = 3.75$ percent, which is a return loss of 14.3 dB and an insertion loss of $-10\log_{10}(1 - 0.0375) = 0.17$ dB per facet from the reflection alone. The boundary from air to lithium niobate reflects 13.2 percent ($\Gamma = -0.363$, 8.8 dB). An uncoated facet in air therefore loses 0.6 dB, and the reflected light returns to the laser, where it can disturb the source.

### Phase per Volt

Take $g = 10\ \mu$m and $V = 1$ V, which gives the field $E = V/g = 10^{5}$ V/m. With $n^3 r_{33} = 2.138^3 \times 30.8\ \text{pm/V} = 3.01\times10^{-10}$ m/V the index change is $\Delta n = \tfrac12 (3.01\times10^{-10})(10^{5}) = 1.51\times10^{-5}$. Over 1 cm the phase is $2\pi(1.51\times10^{-5})(0.01)/(1.55\times10^{-6}) = 0.610$ rad, or 35.0 degrees, and the delay is $\Delta n L/c = 0.50$ fs, which is 0.097 of one optical period. The ideal product is $V_\pi L = \lambda_0 g/(n^3 r_{33}) = 5.15$ V cm. The optical field does not fill the gap uniformly, and an assumed overlap factor of 0.5 doubles the product to 10.3 V cm, so a 4 cm electrode has $V_\pi = 2.6$ V (a value that illustrates the order of magnitude and depends on the actual geometry).

### Electrode Bandwidth from Velocity Mismatch

An assumed electrode of $L = 4$ cm with a mismatch $\Delta n = 2.0$ has $f_{3dB} = 1.392 \times 2.998\times10^{8}/(\pi \times 0.04 \times 2.0) = 1.66$ GHz. A design that reduces the mismatch to $\Delta n = 0.5$ and shortens the electrode to 2 cm reaches 13.3 GHz, and with $\Delta n = 0.2$ it reaches 33.2 GHz. The numbers are illustrations of the scaling. The shorter electrode needs a higher $V_\pi$ (twice the 2.6 V in the 4 cm example, 5.2 V), so the two requirements push in opposite directions, and the reduction of $\Delta n$ (by buffer layers and electrode shape) is the way out.

### Loss of Fiber and Copper

A fiber loses about 0.2 dB/km at 1550 nm (a typical value for standard single-mode fiber). A link of 100 km therefore loses 20 dB. The 12 inch FR4 line of [Skin Effect and Dielectric Loss](05_Skin_Effect_and_Dielectric_Loss.md) loses 0.67 dB per inch at 5 GHz, so 20 dB of loss accumulates in $20/0.67 = 30$ inches, 0.76 m. The glass carries the signal 130,000 times farther than the copper trace for the same loss, and its attenuation varies little over the bandwidth of one channel, which is the reason that optical links need no equalizer for attenuation. The impairments of the fiber are of a different kind (Chapter 21).

## Edge Cases

### Only One Polarization Is Modulated

The coefficient $r_{33}$ applies to the polarization along the crystal axis, and the coefficient for the perpendicular polarization is much smaller ($r_{13}$ is about 8.6 pm/V, less than one third of $r_{33}$). A modulator therefore works properly only for light that is polarized along its preferred axis, and the light must be aligned to that axis before it enters, with polarization-maintaining fiber or an integrated launch. Misaligned light has a component along the weak axis that receives little phase shift, and that component reaches the output as a carrier leak.

### The Index Change Is Small

The relative index change $\Delta n/n$ of $7\times10^{-6}$ per volt for the 10 $\mu$m gap in the example is tiny, which is why the interaction needs centimeter lengths: the phase of 0.61 rad accumulates over $10^{4}$ wavelengths. The Pockels coefficient is a first-order description, and the quadratic (Kerr) term is negligible at these fields. The material also responds to the applied field within femtoseconds, so the response of the crystal is not a limit and the electrode structure sets the bandwidth, as derived above.

### Slow Drift of the Operating Point

A voltage applied for a long time can drift in a lithium niobate modulator, because charges that move in the crystal and in the buffer layers screen part of the field. The bias point of a modulator then moves over minutes to hours, and the transmitter measures it and corrects it with a control loop. Chapter 20 describes the loops that hold the bias points.

### Wave and Photon Descriptions

The statements of this chapter use the wave description, which is sufficient for modulation and interference. The photon description gives the same average power and adds the shot noise of the detection process, and it explains why the energy of a quantum depends on the frequency alone. A reader needs the photon only to understand noise in the receiver, which Chapter 20 and Chapter 21 treat as an additive noise power.
