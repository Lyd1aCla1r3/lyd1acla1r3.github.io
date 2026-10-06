# Impedance, Reflections, and Termination

<!-- SUMMARY: A wavefront that meets a change in impedance splits into a reflected wave and a transmitted wave. This guide derives the impedance of capacitors and inductors from their defining equations (including the phasor notation and the half-power point of an RC filter), derives the reflection coefficient, transmission coefficient, and power fractions from Kirchhoff's laws, inverts the reflection coefficient to recover impedance, shows why the total voltage and current at a boundary no longer have the ratio $Z_0$, and follows the reflections between a driver and a load until the line settles to the DC divider voltage. Series and parallel termination, numerical examples of resistive and reactive mismatches, and the compensation of inductance by capacitance complete the chapter. -->

<p><em>Prefer to read offline? <a href="../../../assets/docs/signal-integrity-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete Signal Integrity (Advanced Edition) ebook.</a></em></p>

[Chapter 2](02_Frequency_Content_of_Digital_Signals.md) derived the spectrum of an edge and showed that every structure a wavefront meets responds to that spectrum one frequency at a time. This chapter treats the first such structure, a change in impedance, and answers two questions: how much of the incident wave reflects, and how do capacitors and inductors, whose opposition to current depends on frequency, respond to each frequency in the edge?

A transmission line carries electromagnetic energy forward as a propagating wave, and the characteristic impedance $Z_0$ sets the ratio of voltage to current within that wave as long as the geometry remains uniform. At a boundary where the impedance changes, the voltage and current on the two sides must still satisfy Kirchhoff's laws, and no single forward wave can satisfy both laws at once. A second wave, traveling backward, appears to make up the difference.

The reflection coefficient $\Gamma$ is the ratio of the reflected voltage to the incident voltage at the boundary. It follows directly from Kirchhoff's voltage and current laws, and it underlies every TDR measurement, every impedance-controlled stackup, every termination resistor, and every via optimization. The symbol $\Gamma$ is reserved for reflection throughout this series, and resistivity receives a separate subscripted symbol so that the two never share one.

This guide derives the impedance of the two reactive elements, derives the reflection and transmission coefficients and the power each carries, and inverts the reflection coefficient to recover impedance. It then follows the reflections between a driver and a load until the line settles into its DC state, compares the two basic termination strategies, and closes with numerical examples and the conditions under which inductance and capacitance cancel each other's reflections.

## Core Concepts

### Impedance, Resistance, and Reactance

The impedance of a two-terminal element at one frequency is the ratio of the voltage amplitude across it to the current amplitude through it, together with the phase difference between the two. A resistor obeys $v = iR$ at every instant, so its voltage and current rise and fall together and the ratio $R$ does not depend on frequency.

A capacitor and an inductor store energy instead of dissipating it, and the defining equation of each links voltage and current through a rate of change. The ratio of amplitudes therefore depends on how fast the signal varies, and the peaks of voltage and current no longer coincide. The frequency-dependent part of impedance is called reactance, and the next sections derive it for each element.

### Capacitor Impedance

A capacitor of capacitance $C$ holds a charge $Q = Cv$ at a voltage $v$. Current is the rate at which charge flows, so for a constant $C$:

$$i(t) = \frac{dQ}{dt} = C\,\frac{dv}{dt}$$

Assume a sinusoidal voltage with amplitude $V_0$ and angular frequency $\omega = 2\pi f$:

$$v(t) = V_0 \sin(\omega t)$$

The derivative of $\sin(u)$ with respect to $u$ is $\cos(u)$, and the inner function $u = \omega t$ has derivative $du/dt = \omega$. The chain rule multiplies the two, which moves the frequency from inside the sine to a factor in front:

$$\frac{d}{dt}\sin(\omega t) = \omega \cos(\omega t)$$

Substituting into the capacitor equation gives the current:

$$i(t) = \omega C V_0 \cos(\omega t)$$

The current amplitude is $I_0 = \omega C V_0$, so the ratio of voltage amplitude to current amplitude is:

$$\frac{V_0}{I_0} = \frac{1}{\omega C} = \frac{1}{2\pi f C}$$

The identity $\cos(\omega t) = \sin(\omega t + 90^\circ)$ shows that the current waveform is the voltage waveform shifted a quarter period earlier. The current of a capacitor leads its voltage by 90°.

### Inductor Impedance

An inductor of inductance $L$ produces a voltage proportional to the rate of change of the current through it. [Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) derives this relation from Faraday's law; here it serves as the defining equation:

$$v(t) = L\,\frac{di}{dt}$$

Assume the sinusoidal current $i(t) = I_0 \sin(\omega t)$ flows through the inductor, and apply the same chain rule to find the voltage:

$$v(t) = \omega L I_0 \cos(\omega t)$$

The ratio of voltage amplitude to current amplitude is:

$$\frac{V_0}{I_0} = \omega L = 2\pi f L$$

The voltage waveform is now the one that is shifted a quarter period earlier, so the voltage across an inductor leads its current by 90°. The two elements mirror each other: the capacitor current leads the voltage, the inductor voltage leads the current, and their magnitudes move in opposite directions with frequency.

### Phasor Notation and the Factor $j\omega$

Keeping track of amplitudes and 90° shifts for every network quickly becomes unwieldy. Complex numbers encode both quantities in one symbol. Euler's identity $e^{j\theta} = \cos\theta + j\sin\theta$ describes a point that rotates around the unit circle as $\theta$ increases, and a sinusoid of amplitude $V_0$ and phase $\varphi$ is the real part of a rotating point:

$$v(t) = V_0 \cos(\omega t + \varphi) = \mathrm{Re}\left\{\hat{V} e^{j\omega t}\right\}, \qquad \hat{V} = V_0 e^{j\varphi}$$

The complex number $\hat{V}$ is the phasor of the voltage. It stores the amplitude as its magnitude and the phase as its angle, and the rotation $e^{j\omega t}$ is common to every signal in a linear circuit at one frequency, so it can be carried along implicitly.

Differentiating the rotating point with respect to time brings down the factor $j\omega$ from the exponent:

$$\frac{d}{dt}\mathrm{Re}\left\{\hat{V} e^{j\omega t}\right\} = \mathrm{Re}\left\{j\omega\,\hat{V} e^{j\omega t}\right\}$$

The imaginary unit satisfies $j = e^{j 90^\circ}$, a rotation by a quarter turn. Multiplying a phasor by $j\omega$ therefore scales its amplitude by $\omega$ and advances its phase by 90°, which is exactly the change that the derivative of a sine wave produced in the previous two sections. In phasor form, a time derivative is a multiplication by $j\omega$.

Applying this rule to the capacitor equation $i = C\,dv/dt$ gives $\hat{I} = j\omega C\,\hat{V}$, and the impedance is the ratio of voltage phasor to current phasor:

$$Z_C = \frac{\hat{V}}{\hat{I}} = \frac{1}{j\omega C} = -\frac{j}{\omega C}$$

Applying it to $v = L\,di/dt$ gives $\hat{V} = j\omega L\,\hat{I}$:

$$Z_L = \frac{\hat{V}}{\hat{I}} = j\omega L$$

The real part of an impedance is its resistance, and the imaginary part is its reactance. The inductor has a positive reactance $X_L = \omega L$, and the capacitor has a negative reactance $X_C = -1/(\omega C)$. The magnitudes match the amplitude ratios found from the sine waves, and the sign of the imaginary part records the direction of the 90° shift. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) used the same rule to turn the Telegrapher's Equations into algebraic equations at one frequency.

### Reactance Scaling with Frequency

The two magnitudes scale in opposite directions, because the capacitive reactance falls in inverse proportion to frequency, and the inductive reactance rises in direct proportion to it. Assume a parasitic capacitance of 0.5 pF, a plausible value for a via, and a parasitic inductance of 1 nH:

- The capacitor presents $1/(2\pi \cdot 10^3 \cdot 0.5\times10^{-12}) \approx 318\ \text{M}\Omega$ at 1 kHz, about 318 kΩ at 1 MHz, about 318 Ω at 1 GHz, and about 32 Ω at 10 GHz. Each factor of ten in frequency lowers the magnitude by a factor of ten.
- The inductor presents $2\pi \cdot 10^9 \cdot 10^{-9} \approx 6.3\ \Omega$ at 1 GHz and about 63 Ω at 10 GHz.

At low frequencies the capacitor therefore looks like an open circuit and the inductor like a short circuit, and neither disturbs a 50 Ω line. Near 10 GHz the same two elements have magnitudes comparable to $Z_0$ and change the impedance the wave encounters.

The physical reason follows from the defining equations. A capacitor changes its voltage only by receiving or delivering charge, so a fast transition requires a large current and a slow one requires a small current. At DC the voltage does not change and no current flows. An inductor opposes a change in its current with a voltage proportional to the rate of change (the back EMF derived in Chapter 4), so a rapidly varying current requires a large voltage across the inductor for each ampere and a constant current requires none.

### The RC Half-Power Point

The impedance of the capacitor fixes the bandwidth of the RC filter that [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) used to relate rise time to bandwidth. A resistor $R$ in series with a capacitor $C$, with the output taken across the capacitor, forms a voltage divider whose transfer function is the ratio of the capacitor impedance to the total impedance:

$$H = \frac{\hat{V}_{out}}{\hat{V}_{in}} = \frac{Z_C}{R + Z_C} = \frac{1/(j\omega C)}{R + 1/(j\omega C)}$$

Multiplying the numerator and denominator by $j\omega C$ removes the nested fraction:

$$H = \frac{1}{1 + j\omega RC}$$

The magnitude of a complex denominator is the square root of the sum of the squares of its real and imaginary parts:

$$|H| = \frac{1}{\sqrt{1 + (\omega RC)^2}}$$

With the time constant $\tau = RC$ and the definition $f_{3\text{dB}} = 1/(2\pi\tau)$, the product $\omega RC = 2\pi f \tau$ equals $f/f_{3\text{dB}}$, and the magnitude becomes the single-pole expression used in Chapter 2:

$$|H| = \frac{1}{\sqrt{1 + (f/f_{3\text{dB}})^2}}$$

At $f = f_{3\text{dB}}$ the magnitude is $1/\sqrt{2} \approx 0.707$, which is half of the input power. This is also the frequency at which the capacitive reactance $1/(\omega C)$ equals $R$, because $\omega RC = 1$ there.

### The Reflection Coefficient: Derivation from Kirchhoff's Laws

An incident wave travels down a transmission line with characteristic impedance $Z_0$ and strikes a boundary where the impedance changes to $Z_L$. At this boundary, the incident wave splits into a reflected wave that travels backward and a transmitted wave that continues forward into $Z_L$. Three waves exist at the boundary:

1. **Incident wave:** carries the voltage $V_{inc}$ and the current $I_{inc}$ toward the boundary.
2. **Reflected wave:** carries the voltage $V_{ref}$ and the current $I_{ref}$ back toward the source.
3. **Transmitted wave:** carries the voltage $V_{trans}$ and the current $I_{trans}$ into the load.

Two constraints hold at the plane of the boundary.

**Kirchhoff's voltage law** requires the voltage to be continuous across the boundary. The voltage on the line side, which is the sum of the incident and reflected waves, must equal the voltage on the load side:

$$V_{inc} + V_{ref} = V_{trans}$$

**Kirchhoff's current law** requires the current to be continuous across the boundary. Charge cannot accumulate at the boundary, so the current arriving from the line must equal the current entering the load:

$$I_{inc} + I_{ref} = I_{trans}$$

Each wave carries a current set by the impedance of the medium it travels in. Chapter 1 showed that a forward wave on the line has $V/I = Z_0$. Take current as positive when it flows in the direction of the incident wave, toward the load. A wave moving backward carries current in the opposite direction for the same sign of voltage, so the three currents are:

- The incident wave carries the current $I_{inc} = V_{inc} / Z_0$.
- The reflected wave carries the current $I_{ref} = -V_{ref} / Z_0$.
- The transmitted wave carries the current $I_{trans} = V_{trans} / Z_L$.

The sign of $I_{ref}$ records the direction of travel, because the reflected wave moves backward and the current is a signed quantity that follows the direction of the wave. Substituting these currents into Kirchhoff's current law:

$$\frac{V_{inc}}{Z_0} - \frac{V_{ref}}{Z_0} = \frac{V_{trans}}{Z_L}$$

Replacing $V_{trans}$ with the voltage continuity equation:

$$\frac{V_{inc}}{Z_0} - \frac{V_{ref}}{Z_0} = \frac{V_{inc} + V_{ref}}{Z_L}$$

Cross-multiplying to clear the denominators:

$$Z_L(V_{inc} - V_{ref}) = Z_0(V_{inc} + V_{ref})$$

Distributing the impedances:

$$Z_L V_{inc} - Z_L V_{ref} = Z_0 V_{inc} + Z_0 V_{ref}$$

Collecting $V_{inc}$ terms on the left and $V_{ref}$ terms on the right:

$$V_{inc}(Z_L - Z_0) = V_{ref}(Z_L + Z_0)$$

Isolating the ratio of reflected voltage to incident voltage:

$$\frac{V_{ref}}{V_{inc}} = \frac{Z_L - Z_0}{Z_L + Z_0}$$

This ratio is the reflection coefficient:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

$\Gamma$ is a ratio of voltages, not of energies. The fraction of the incident power that reflects is $\Gamma^2$, as shown below. For a load with reactance, $Z_L$ is complex, the same algebra holds for each frequency component, and $\Gamma$ is a complex number with a magnitude and a phase.

### The Transmission Coefficient and the Power Fractions

The voltage continuity equation gives the transmitted voltage directly. Dividing it by $V_{inc}$ defines the transmission coefficient $\tau$:

$$\tau = \frac{V_{trans}}{V_{inc}} = 1 + \frac{V_{ref}}{V_{inc}} = 1 + \Gamma$$

Substituting the expression for $\Gamma$ and combining over a common denominator:

$$\tau = \frac{(Z_L + Z_0) + (Z_L - Z_0)}{Z_L + Z_0} = \frac{2Z_L}{Z_L + Z_0}$$

The power carried by a wave of voltage $V$ in a medium of impedance $Z$ is proportional to $V^2/Z$, and the same constant applies on both sides of a resistive boundary, so power fractions follow from ratios. The reflected wave travels on the same line as the incident wave, so its power fraction is the square of the voltage ratio:

$$\frac{P_{ref}}{P_{inc}} = \frac{V_{ref}^2/Z_0}{V_{inc}^2/Z_0} = \Gamma^2$$

The transmitted wave travels in the load impedance, so its power fraction includes the impedance ratio:

$$\frac{P_{trans}}{P_{inc}} = \frac{\tau^2 V_{inc}^2/Z_L}{V_{inc}^2/Z_0} = \tau^2\,\frac{Z_0}{Z_L} = \frac{4 Z_0 Z_L}{(Z_L + Z_0)^2}$$

The identity $(Z_L + Z_0)^2 - (Z_L - Z_0)^2 = 4 Z_0 Z_L$ shows that this fraction equals $1 - \Gamma^2$:

$$1 - \Gamma^2 = \frac{(Z_L + Z_0)^2 - (Z_L - Z_0)^2}{(Z_L + Z_0)^2} = \frac{4 Z_0 Z_L}{(Z_L + Z_0)^2}$$

The reflected and transmitted powers therefore sum to the incident power, so the equations conserve energy. The transmission coefficient can exceed one, with $\tau = 2$ for an open circuit, without violating this conservation, because the transmitted wave enters a higher impedance and carries less current for the same power.

### Recovering Impedance from the Reflection Coefficient

A measurement instrument observes $\Gamma$ and must report the impedance that produced it. The inversion starts from the definition and clears the denominator:

$$\Gamma (Z_L + Z_0) = Z_L - Z_0$$

Distributing $\Gamma$:

$$\Gamma Z_L + \Gamma Z_0 = Z_L - Z_0$$

Collecting the $Z_L$ terms on one side and the $Z_0$ terms on the other:

$$Z_0 + \Gamma Z_0 = Z_L - \Gamma Z_L$$

Factoring each side and solving for $Z_L$:

$$Z_L = Z_0\,\frac{1 + \Gamma}{1 - \Gamma}$$

This pair of equations, $\Gamma(Z_L)$ and $Z_L(\Gamma)$, is the working relationship between what an instrument measures and the impedance it reports. [Chapter 7](07_Time_Domain_Reflectometry.md) applies it to a reflection measured in time, [Chapter 8](08_S_Parameters_and_VNA.md) applies it to a reflection measured in frequency, and [Chapter 9](09_Smith_Charts.md) draws it as a map of the complex plane.

### Three Canonical Terminations

The reflection coefficient formula produces three boundary cases that define the extremes of termination behavior, summarized here with the transmission coefficient and the power fractions.

**Matched termination ($Z_L = Z_0$):** The numerator vanishes, so $\Gamma = 0$ and $\tau = 1$. The entire wave enters the load, and the load absorbs all of the incident power. A 50 Ω trace terminated by a 50 Ω resistor produces no reflection.

**Open circuit ($Z_L \to \infty$):** The reflection coefficient approaches $\Gamma = +1$ and the transmission coefficient approaches $\tau = 2$. The reflected voltage has the same polarity as the incident voltage and adds to it, doubling the voltage at the boundary. No current flows into the open circuit, because the reflected current equals the incident current and flows the other way. All of the incident power returns on the reflected wave.

**Short circuit ($Z_L = 0$):** The reflection coefficient equals $\Gamma = -1$ and $\tau = 0$. The reflected voltage has the opposite polarity and cancels the incident voltage, so the boundary voltage is zero. The total current doubles, because the reflected current flows in the same direction as the incident current, and all of the incident power again returns.

### Impedance as a Property of the Medium

Electromagnetic waves do not possess an independent impedance. Impedance is a property of the copper geometry and the dielectric surrounding it, and it sets the ratio between voltage and current for any wave traveling on that geometry. A 50 Ω trace forces each propagating wave to maintain a voltage-to-current ratio of 50 Ω.

A reflected wave created by a localized defect steps onto the trace heading backward, and the geometry of the trace immediately fixes the ratio of its voltage to its current. The defect determines only the initial amplitude of the reflected wave, through $\Gamma$, and once launched the reflected wave behaves as a new signal traveling in the reverse direction.

A reflected wave with a smaller voltage amplitude therefore carries a proportionally smaller current. Assume a transmitter launches a 1 V forward wave on a 50 Ω trace, producing 20 mA of forward current, and a parasitic via rejects 0.1 V backward. The geometry forces the reflected current to equal $0.1\ \text{V} / 50\ \Omega = 2$ mA, and the reflected wave carries $\Gamma^2 = (0.1)^2 = 1\%$ of the incident power.

## Architecture

### The Reflection as a Separate Electromagnetic Wave

A reflection is an electromagnetic wave of its own, propagating in the backward direction, and it is distinct from the return current of the forward wave. The forward wavefront carries its own localized current loop: conduction current flows forward on the trace, displacement current bridges the dielectric at the wavefront, and return current flows backward on the ground plane. This loop structure, described in [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md), closes at all times during forward propagation.

At an impedance discontinuity, the mismatch launches a new backward-traveling wave with its own current loop: conduction current on the trace, displacement current through the dielectric at the reflected wavefront, and return current on the ground plane. The two waves coexist on the line wherever the reflected wavefront has already passed, and the fields add by superposition because Maxwell's equations in the dielectric are linear.

### What a Meter Sees: Total Voltage and Current with a Reflection

A voltmeter and a current probe at one point on the line observe the sum of the waves present there. Behind the reflected wavefront, the forward wave contributes voltage $V_{inc}$ and current $V_{inc}/Z_0$, and the reflected wave contributes voltage $V_{ref} = \Gamma V_{inc}$ and current $-\Gamma V_{inc}/Z_0$. The totals are:

$$V_{total} = V_{inc}(1 + \Gamma), \qquad I_{total} = \frac{V_{inc}}{Z_0}(1 - \Gamma)$$

Dividing the voltage by the current gives the ratio a meter reports:

$$\frac{V_{total}}{I_{total}} = Z_0\,\frac{1 + \Gamma}{1 - \Gamma}$$

The ratio equals $Z_0$ only when $\Gamma = 0$. With a reflected wave present, the ratio of total voltage to total current at a boundary equals the load impedance, as the inversion equation predicts, and the individual waves still obey $V/I = \pm Z_0$ separately. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) noted that $Z_0 = V/I$ holds for a single wave traveling in one direction, and this equation is the quantitative form of that restriction.

### The Launched Wave and the Driver Resistance

A driver is not an ideal voltage source. The output transistor has an internal resistance $R_S$, typically between 10 and 30 Ω, that forms a voltage divider with the line. During the first round-trip time after switching, no reflection has yet returned, so the line presents only its characteristic impedance to the driver, and the driver sees $Z_0$ as a resistive load. The launched voltage is the divider output for a source voltage $V_S$:

$$V_1 = V_S\,\frac{Z_0}{R_S + Z_0}$$

Assume a 1.2 V supply and $R_S = 10\ \Omega$ driving a 50 Ω line. The launched wave has $V_1 = 1.2 \cdot 50/60 = 1.0$ V and a current of $1.0/50 = 20$ mA, compared with the 24 mA drawn by the ideal 1.2 V switch of Chapter 1.

The same boundary analysis applies at the source end. A wave returning from the line meets the resistance $R_S$ with the source voltage acting as a constant, which contributes nothing to a wave that merely arrives. The source therefore has a reflection coefficient:

$$\Gamma_S = \frac{R_S - Z_0}{R_S + Z_0}$$

A driver resistance of $10\ \Omega$ on a 50 Ω line gives $\Gamma_S = -40/60 = -2/3$. The source reflects two thirds of a returning wave with inverted polarity, because a driver with a resistance below $Z_0$ behaves as a partial short circuit.

### Ping-Pong Reflections

The launched wave reaches the load and reflects with $\Gamma_L$. The reflected wave returns to the source and reflects with $\Gamma_S$, and the process repeats. Each wave has been multiplied by the product $\Gamma_S \Gamma_L$ after one complete round trip.

Let $T$ be the one-way delay of the line. The load voltage after the first arrival at time $T$ is the incident wave plus its reflection, $V_1(1 + \Gamma_L)$. The wave that returns to the source and reflects arrives at the load again at time $3T$, with amplitude $V_1 \Gamma_L \Gamma_S$, and it adds $V_1 \Gamma_L \Gamma_S (1 + \Gamma_L)$ to the load voltage. Each later arrival repeats this step with a further factor $\Gamma_S \Gamma_L$.

Each time a wave strikes a resistive termination, the resistance absorbs the fraction $1 - \Gamma^2$ of the arriving power and converts it to heat. The remaining power returns on the reflected wave with a smaller amplitude, so the reflections shrink with each bounce, and the ping-pong ends when the amplitudes fall below any measurable threshold. A reactive termination does not absorb power, and its reflection depends on frequency, as the Edge Cases section shows.

### Settling to Steady State

The ping-pong process is the mechanism that connects wave propagation to ordinary DC circuit analysis. The load voltage after all the bounces is the sum of the series above, which is geometric because each term is the previous one multiplied by the constant $\Gamma_S \Gamma_L$:

$$V_{final} = V_1(1 + \Gamma_L)\left[1 + \Gamma_S\Gamma_L + (\Gamma_S\Gamma_L)^2 + \cdots\right] = \frac{V_1(1 + \Gamma_L)}{1 - \Gamma_S\Gamma_L}$$

The sum converges whenever $|\Gamma_S\Gamma_L| < 1$, which holds for any source resistance above zero. Writing each factor in terms of the resistances, and noting that $1 + \Gamma_L = 2R_L/(R_L + Z_0)$, the denominator becomes:

$$1 - \Gamma_S\Gamma_L = \frac{(R_S + Z_0)(R_L + Z_0) - (R_S - Z_0)(R_L - Z_0)}{(R_S + Z_0)(R_L + Z_0)} = \frac{2Z_0(R_S + R_L)}{(R_S + Z_0)(R_L + Z_0)}$$

Substituting $V_1 = V_S Z_0/(R_S + Z_0)$ and simplifying, the factors containing $Z_0$ cancel:

$$V_{final} = V_S\,\frac{Z_0}{R_S + Z_0}\cdot\frac{2R_L}{R_L + Z_0}\cdot\frac{(R_S + Z_0)(R_L + Z_0)}{2Z_0(R_S + R_L)} = V_S\,\frac{R_L}{R_S + R_L}$$

The result is the DC voltage divider, with no trace of $Z_0$. The characteristic impedance governs how the line approaches its final state and has no influence on the state it reaches. The voltage is then uniform along the trace, no gradient remains to drive a propagating wave, and Ohm's law ($V = IR$) describes the circuit completely.

The wave solution and the DC solution are the same solution observed at different times. The series converges only asymptotically, so the practical settling time is the number of round trips needed for the remaining amplitude to fall below the noise or timing margin of the receiver. A well-matched link settles in the first arrival, and a poorly matched one rings for many round trips. Copper resistance dissipates a small part of the energy throughout, and the loss mechanisms are the subject of [Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md).

### Termination Strategies

The ping-pong series ends after at most one reflection when either $\Gamma_S$ or $\Gamma_L$ is zero, because the product $\Gamma_S\Gamma_L$ then vanishes and nothing returns for a second trip. This observation defines the two basic termination strategies.

**Series (source) termination** adds a resistor $R_T$ at the driver so that $R_S + R_T = Z_0$ and $\Gamma_S = 0$. The launched voltage is $V_S/2$, which reaches an open load and doubles to the full $V_S$. The reflection returns to the source and is absorbed completely, so the line settles after one round trip. No DC current flows with a high-impedance receiver, which makes the method power-efficient. The line voltage between the driver and the load equals only $V_S/2$ until the reflection passes, so every receiver must sit at the far end, and the method suits point-to-point links.

**Parallel (end) termination** places a resistor equal to $Z_0$ from the load end to a reference voltage, so that $\Gamma_L = 0$. The load absorbs the wave and no reflection forms, regardless of the source resistance. The resistor draws a steady current whenever the line is held high, which costs static power. In the 10 Ω example above, a 50 Ω end termination draws $1.2/60 = 20$ mA, dissipating 20 mW in the termination while the line is high, and the steady-state swing is reduced to the divider voltage of 1.0 V. High-speed receivers commonly place this resistor on the die, where it is called on-die termination, to remove the stub that a discrete resistor would add.

## Worked Examples

### A 75 Ω Section on a 50 Ω Line

Assume a 1 V wave on a 50 Ω line reaches a boundary with a 75 Ω load. The reflection coefficient is:

$$\Gamma = \frac{75 - 50}{75 + 50} = 0.2$$

The reflected voltage is $0.2$ V, the transmitted voltage is $\tau V_{inc} = 1.2$ V, and the currents follow from the impedance of each medium. The incident current is $1/50 = 20$ mA, the reflected current is $-0.2/50 = -4$ mA, and the transmitted current is $1.2/75 = 16$ mA. The three currents satisfy Kirchhoff's current law, because $20 - 4 = 16$ mA.

The reflected power fraction is $\Gamma^2 = 0.04$, so 4% of the incident power returns and 96% enters the load. The total voltage at the boundary is 1.2 V and the total current is 16 mA, so a meter at the boundary reads $1.2/0.016 = 75\ \Omega$, the load impedance, and not $Z_0$.

### An Open Receiver Behind a 10 Ω Driver

Assume the 1.2 V, 10 Ω driver from the Architecture section drives a 50 Ω line that ends in a CMOS receiver whose input is effectively an open circuit. The reflection coefficients are $\Gamma_S = -2/3$ and $\Gamma_L = +1$, and the launched wave has $V_1 = 1.0$ V.

The voltage at the load at each arrival follows from the series above. The first arrival at time $T$ doubles the wave to 2.0 V. Each later arrival adds twice the incident amplitude, which is multiplied by $\Gamma_S\Gamma_L = -2/3$ per round trip:

- At time $T$ the load voltage is 2.0 V.
- At time $3T$ the load voltage is $2.0 + 2(1.0)(-2/3) = 0.667$ V.
- At time $5T$ the load voltage is $0.667 + 2(0.444) = 1.556$ V.
- At time $7T$ the load voltage is $1.556 + 2(-0.296) = 0.963$ V.
- At time $9T$ the load voltage is $0.963 + 2(0.198) = 1.358$ V.

The sequence oscillates around the final value $V_S R_L/(R_S + R_L) = 1.2$ V, and the departures from 1.2 V shrink by a factor of $2/3$ each round trip: +0.8 V, -0.53 V, +0.36 V, -0.24 V, +0.16 V. The first overshoot reaches 2.0 V, well above the 1.2 V supply, and can exceed the voltage rating of the receiver. The period of this oscillation is the round-trip delay $2T$, which depends only on trace length and velocity. The Gibbs ringing of [Chapter 2](02_Frequency_Content_of_Digital_Signals.md) has a different origin, because its period depends on the bandwidth of the system and not on the length of the line.

Adding a 40 Ω series resistor at the driver makes $R_S + R_T = 50\ \Omega$ and $\Gamma_S = 0$. The launched wave becomes $V_1 = 1.2 \cdot 50/100 = 0.6$ V, the load doubles it to the full 1.2 V at time $T$, the reflection returns and is absorbed, and no further bounce occurs. The receiver sees a single clean transition.

### Reactive Discontinuities on a 50 Ω Line

Two reactive structures appear throughout the later chapters: a parasitic capacitance that shunts the line to the reference plane, and a parasitic inductance in series with the line. Each can be treated as a load impedance in front of the remainder of the line, which behaves as a matched 50 Ω load.

For the shunt capacitance, the impedance seen at the discontinuity is the parallel combination of $Z_C$ and $Z_0$. Define the dimensionless quantity $x = \omega C Z_0$ to shorten the algebra, and write the parallel combination as:

$$Z_{in} = \frac{Z_0 \cdot \dfrac{1}{j\omega C}}{Z_0 + \dfrac{1}{j\omega C}} = \frac{Z_0}{1 + j x}$$

Substituting into the reflection coefficient:

$$\Gamma = \frac{Z_{in} - Z_0}{Z_{in} + Z_0} = \frac{1 - (1 + jx)}{1 + (1 + jx)} = \frac{-jx}{2 + jx}, \qquad |\Gamma| = \frac{x}{\sqrt{4 + x^2}}$$

For small $x$ the magnitude is approximately $x/2 = \pi f C Z_0$. With $C = 0.5$ pF, the value of $x$ is 0.157 at 1 GHz, 0.785 at 5 GHz, and 1.571 at 10 GHz, which gives $|\Gamma| = 0.078$, 0.366, and 0.618. The corresponding reflected power fractions are 0.6%, 13%, and 38%. The same capacitor that is invisible at 1 GHz reflects more than a third of the incident power at 10 GHz.

For the series inductance, the impedance seen at the discontinuity is $Z_{in} = Z_0 + j\omega L$, and the reflection coefficient simplifies to:

$$\Gamma = \frac{j\omega L}{2 Z_0 + j\omega L}$$

For $L = 1$ nH the reactance is 6.3 Ω at 1 GHz, 31.4 Ω at 5 GHz, and 62.8 Ω at 10 GHz, giving $|\Gamma| = 0.063$, 0.300, and 0.532, and reflected power fractions of 0.4%, 9%, and 28%.

Both reflections grow in proportion to frequency while the product $\omega C Z_0$ or $\omega L/Z_0$ is small, so a fast edge, which contains more high-frequency content ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)), is reflected more strongly than a slow one by the same structure. [Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md) traces where these parasitics come from in real geometry, [Chapter 7](07_Time_Domain_Reflectometry.md) shows how they appear as a dip and a bump on a TDR trace, and [Chapter 8](08_S_Parameters_and_VNA.md) shows how the same $\Gamma(f)$ is measured directly.

## Edge Cases

### Inductance and Capacitance That Cancel

Every millimeter of a trace has both capacitance and inductance, and their ratio sets the characteristic impedance. A discontinuity that adds inductance and capacitance together in the proportions of the line leaves the impedance unchanged. A uniform section of line with per-unit-length values $L' + \Delta L'$ and $C' + \Delta C'$ has the impedance:

$$Z = \sqrt{\frac{L' + \Delta L'}{C' + \Delta C'}} = \sqrt{\frac{L'}{C'}} = Z_0 \quad \text{when} \quad \frac{\Delta L'}{\Delta C'} = \frac{L'}{C'} = Z_0^2$$

The section is slower than the surrounding line, because the product $LC$ increased and the velocity $1/\sqrt{LC}$ fell, but it produces no reflection, and a TDR trace shows a flat impedance profile even though the geometry changed.

A short lumped network of a series inductor and a shunt capacitor imitates a short section of line when $L/C = Z_0^2$. Assume a pad adds 0.5 pF to a 50 Ω line. A neck of narrow trace with $L = Z_0^2 C = 2500 \cdot 0.5\times10^{-12} = 1.25$ nH next to the pad forms a matched section. The imitation holds for edge content well below $1/(\pi\sqrt{LC})$, which is about 12.7 GHz for these values, and the match degrades as the frequency approaches that limit. A discontinuity shorter than the critical length of Chapter 1 behaves as such a lumped element, which is why a via is modeled as a capacitance and an inductance. Engineers exploit this cancellation in connector launches and via designs ([Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md)).

### Reactive Terminations Reflect All of the Power

A load that is purely reactive, $Z_L = jX$, has no resistance to dissipate power. The magnitudes of the numerator and denominator of the reflection coefficient are equal, because $|jX - Z_0| = |jX + Z_0| = \sqrt{X^2 + Z_0^2}$, so $|\Gamma| = 1$ at every frequency. All of the incident power returns, and only the phase of the reflection changes with frequency. This unit magnitude is why purely reactive loads lie on the outer boundary of the Smith chart in [Chapter 9](09_Smith_Charts.md).

In the time domain, a capacitor $C$ at the end of a line initially holds no charge and acts as a short circuit, so the first reflection has $\Gamma = -1$. The capacitor then charges through the line impedance. An incident step of amplitude $V$ drives the load voltage as $2V$ through an effective source resistance $Z_0$, so $v_L(t) = 2V(1 - e^{-t/(Z_0 C)})$, and the instantaneous reflection coefficient $v_L/V - 1$ moves from $-1$ toward $+1$ with the time constant $Z_0 C$. A 0.5 pF capacitor on a 50 Ω line has $Z_0 C = 25$ ps, so it is a short circuit for edges much faster than 25 ps and an open circuit for edges much slower.

The inductance that appears in every example of this chapter has so far been a given quantity. The next chapter derives it from the laws of Ampere and Faraday, shows how the magnetic field of one trace induces a voltage in its neighbors, and answers the question of how much energy a neighboring trace receives, which is the problem of crosstalk.
