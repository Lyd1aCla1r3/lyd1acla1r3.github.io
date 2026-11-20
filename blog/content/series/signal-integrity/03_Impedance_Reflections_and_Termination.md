# Impedance, Reflections, and Termination

<!-- SUMMARY: A wavefront meeting an impedance discontinuity splits into reflected and transmitted waves to satisfy Kirchhoff's continuity laws and conservation of energy. Complex reactance, reflection and transmission coefficients, and multi-bounce lattices govern how high-speed interconnects ring and settle to their DC steady state. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>

[Chapter 2](02_Frequency_Content_of_Digital_Signals.md) derived the frequency spectrum of a digital transition and showed that every physical structure along a link responds to that spectrum one frequency at a time. The first such structure is a change in impedance, which raises two fundamental questions: why does an electromagnetic wave reflect at an impedance boundary, and how do capacitors and inductors respond to each frequency component inside a rising edge?

Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) how distributed inductance $L$ and distributed capacitance $C$ determine the propagation velocity $v_p$ and characteristic impedance $Z_0$ of a lossless transmission line:

$$v_p = \frac{1}{\sqrt{LC}}, \qquad Z_0 = \sqrt{\frac{L}{C}}$$

Characteristic impedance $Z_0$ locks the ratio of voltage to current within the forward wave for as long as the trace geometry remains uniform. At any boundary where the downstream impedance $Z_L$ differs from $Z_0$, a single forward wave can no longer satisfy both voltage continuity and current continuity simultaneously. Nature resolves that boundary incompatibility by launching a second electromagnetic wave backward toward the source.

The reflection coefficient $\Gamma$ is the ratio of the reflected voltage wave to the incident voltage wave at the boundary. It follows directly from Kirchhoff's voltage and current laws and underlies every time-domain reflectometry (TDR) profile, every impedance-controlled stackup, every termination resistor, and every via optimization. Throughout this series, the symbol $\Gamma$ denotes reflection coefficient exclusively, whereas bulk material resistivity is written as $\rho_r$ so the two symbols never collide.

The sections below derive the complex impedance of capacitors and inductors, establish the reflection and transmission coefficients along with their power and energy balances, and invert the reflection equation to recover unknown impedances. Subsequent sections trace multi-bounce reflections between a real driver and load until the link settles into its steady-state DC voltage divider, compare series and parallel termination architectures, and derive the condition under which parasitic inductance and capacitance cancel each other's reflections.

## Core Concepts

### Impedance, Resistance, and Reactance

An electromagnetic signal propagating along a conductor is a single wave with two measurable aspects at every location: **voltage** $v(t)$ (scalar electrical pressure in Volts) and **current** $i(t)$ (flow rate of charge in Amps, or Coulombs per second). Two probes clipped to the same point on a trace display $v(t)$ and $i(t)$ versus time $t$ on an oscilloscope screen. Electrical opposition in Ohms ($\Omega$, or $\text{V/A}$) quantifies the physical counter-force that pushes back against moving charge to limit peak current $I_0$ under a peak voltage push $V_0$.

The fundamental physical quantity inside the conductor is **displaced charge** $Q(t)$ in Coulombs, which serves as the electrical equivalent of mechanical **position**. Successive time derivatives of $Q(t)$ yield charge **velocity** $i(t)$ (first derivative) and charge **acceleration** $\frac{di(t)}{dt}$ (second derivative):

$$i(t) = \frac{dQ(t)}{dt}, \qquad \frac{di(t)}{dt} = \frac{d^2 Q(t)}{dt^2}$$

A mechanical spring, friction damper, and heavy mass push back against position, velocity, and acceleration. Each passive electrical element generates back-voltage proportional to the zeroth, first, or second time derivative of charge $Q(t)$.

#### Capacitor, Resistor, and Inductor Back-Voltage Laws

A **capacitor** acts as an electrical spring against the zeroth derivative, charge position $Q(t)$. Two metal plates separated by an insulating dielectric gap form a broken wire where charge flows in the attached leads only during plate filling or emptying, and parked electrons repel newcomers in proportion to accumulated charge $Q(t)$:

$$v_C(t) = \frac{1}{C}\,Q(t) \qquad \Longrightarrow \qquad i(t) = \frac{dQ(t)}{dt} = C\,\frac{dv_C(t)}{dt}$$

A **resistor** acts as atomic friction against the first derivative, charge velocity $i(t)$. Conduction electrons collide with lattice atoms inside the resistive material and generate frictional back-pressure proportional to instantaneous current, keeping peak voltage and peak current aligned ($0^\circ$ phase shift) with constant resistance $R$ across frequency:

$$v_R(t) = R\,\frac{dQ(t)}{dt} = R\,i(t)$$

An **inductor** acts as magnetic flywheel inertia against the second derivative, charge acceleration $\frac{di(t)}{dt}$. Its unbroken coiled conductor lets steady direct current coast with $0\,\Omega$ opposition, while its magnetic field generates a Faraday counter-voltage proportional to the rate of current change:

$$v_L(t) = L\,\frac{d^2 Q(t)}{dt^2} = L\,\frac{di(t)}{dt}$$

#### Quarter-Cycle Phase Shift from a Time Derivative

Capacitors and inductors sit one derivative below and one derivative above current $i(t)$, producing a universal timing shift on any sinusoidal wave. On an oscilloscope, one full repeating cycle of duration $T$ maps to $360^\circ$ of cycle progress, so "$90^\circ$ apart" means a **quarter-cycle timing offset** along the horizontal time axis rather than spatial perpendicularity in a room.

Any sinusoid crosses zero height at $0^\circ$ at its steepest upward rate of change, then flattens to zero rate of change one quarter-cycle later at $90^\circ$ at its peak height. Relative to current $i(t)$, resistor voltage sits at the same derivative level ($0^\circ$ shift), inductor voltage sits one derivative higher ($+90^\circ$ ahead of current), and capacitor voltage sits one derivative lower ($-90^\circ$ behind current).

#### Frequency Scaling of Amplitude and Reactive Energy Exchange

A time derivative $\frac{d}{dt}$ also scales wave amplitude in proportion to frequency $f$ because $\frac{d}{dt}$ measures rate of change per second. Consider an elevator traveling between Floor 0 and Floor 10 across a fixed vertical swing $V_0$. Cycling between those ten floors ten times per second instead of once per hour forces the cabin to cover the same vertical distance in a tiny fraction of the time, multiplying speed in proportion to $f$.

Oscillating a sinusoidal wave of fixed amplitude $V_0$ at higher frequency $f$ forces the wave to climb from zero to $V_0$ across a shorter quarter-cycle window $\Delta t$, multiplying its peak rate of change by angular frequency $\omega$:

$$\Delta t = \frac{1}{4f}, \qquad \omega = 2\pi f$$

At the instant $v(t)$ hits its peak $V_0$, current $i(t)$ in a pure capacitor or inductor passes through $0\text{ A}$, so the instantaneous ratio $\frac{v(t)}{i(t)}$ varies continuously across the cycle. Alternating-current analysis characterizes opposition in Ohms by comparing the **peak voltage amplitude $V_0$ to the peak current amplitude $I_0$** ($\frac{V_0}{I_0}$) while tracking the quarter-cycle ($90^\circ$) timing offset as phase.

That $90^\circ$ timing offset governs energy flow through the instantaneous power product $p(t)$:

$$p(t) = v(t)\,i(t)$$

Instantaneous power $p(t)$ alternates positive across one quarter-cycle (absorbing circuit energy to build the electric or magnetic field) and negative across the next quarter-cycle (returning $100\%$ of that stored energy to the circuit). Opposition to alternating current that limits peak Amps by storing and returning field energy shifted $90^\circ$ in phase, rather than burning energy as heat, is called **reactance** ($X$). Complex **impedance** $Z(\omega)$ packages resistance $R$ and reactance $X$ into a single frequency-dependent hardware specification.

### Capacitor Impedance

An insulating gap separates the two capacitor plates, so a steady DC voltage $V_0$ fills the plates once to full charge $Q_{\text{full}}$ and current stops permanently at $0\text{ A}$ (infinite DC opposition):

$$Q_{\text{full}} = C\,V_0$$

Sustaining alternating current in the leads requires reversing the source voltage at frequency $f$ to slosh charge onto and off of the plates repeatedly. Tracking the plates from empty to full across one rising quarter-cycle explains why capacitor current peaks one quarter-cycle ($90^\circ$) ahead of voltage:

1. **Empty plates at the voltage zero-crossing ($0\text{ V}$):** Zero accumulated charge sits on the plates to repel incoming electrons. Unopposed by electrostatic back-pressure, charging current rushes onto the plates at its **maximum rate (peak current $I_0$)** right as $v(t)$ passes through $0\text{ V}$.
2. **Full plates at the voltage peak ($V_0$):** Source voltage reaches its crest $V_0$ one quarter-cycle ($90^\circ$) later and momentarily stops rising while electrostatic back-pressure from the crowded plates balances $V_0$. Charge inflow stops completely at $0\text{ A}$ right at the voltage peak $V_0$.

Those same tank-filling mechanics explain how capacitance $C$ and frequency $f$ control the peak current $I_0$ allowed by a peak voltage push $V_0$:

- **Plate capacity ($C$, bucket size):** A doubled capacitance $C$ doubles the Coulombs of full charge $Q_{\text{full}}$ that pile onto the plates before back-pressure reaches $V_0$. Twice the charge per cycle doubles peak current $I_0$ in proportion to $C$ and halves opposition in Ohms in proportion to $\frac{1}{C}$.
- **Reversal rate ($f$, sloshes per second):** A low frequency $f$ fills the plates early in the slow cycle so back-pressure blocks flow across most of the period. A high frequency $f$ reverses source polarity before much charge accumulates, pumping more Coulombs per second in proportion to $f$ and shrinking Ohms in proportion to $\frac{1}{f}$.

The calculus of the capacitor represents those physical relationships directly. Stored charge $Q(t)$ scales linearly with terminal voltage $v(t)$, and terminal current $i(t)$ equals the rate at which charge arrives on the plates:

$$Q(t) = C\,v(t), \qquad i(t) = \frac{dQ(t)}{dt} = C\,\frac{dv(t)}{dt}$$

Connecting a sinusoidal voltage source across the capacitor fixes terminal voltage $v(t)$ by Kirchhoff's voltage law. One full cycle spans $2\pi$ radians, so a wave repeating $f$ times per second sweeps through phase angle $\theta(t)$ at angular speed $\omega$ in radians per second:

$$\theta(t) = \omega t, \qquad \omega = 2\pi f, \qquad v(t) = V_0 \sin(2\pi f t) = V_0 \sin(\omega t)$$

Differentiation of $v(t)$ with respect to time multiplies vertical voltage swing $V_0$ by angular frequency $\omega$, reflecting the shorter time available to cover $V_0$ at higher frequency:

$$\frac{dv(t)}{dt} = \frac{d}{dt} \left[ V_0 \sin(\omega t) \right] = V_0 \cos(\omega t)\,\frac{d(\omega t)}{dt} = (\omega V_0) \cos(\omega t)$$

Substitution of the voltage rate of change $\frac{dv(t)}{dt}$ into the capacitor charging law gives the capacitor current waveform $i(t)$:

$$i(t) = (\omega C V_0) \cos(\omega t) = (\omega C V_0) \sin(\omega t + 90^\circ)$$

Over each cycle, $\cos(\omega t)$ oscillates between $-1$ and $+1$. At the instants where $\cos(\omega t)$ reaches $+1$ (right as $v(t)$ crosses $0\text{ V}$ at its steepest upward slope), current $i(t)$ hits its peak value $I_0$, equal to angular slosh rate $\omega$ times charge bucket $C\,V_0$:

$$I_0 = (\omega C V_0) \times 1 = \omega C V_0 = 2\pi f C V_0$$

Division of peak voltage push $V_0$ by peak current flow $I_0$ cancels $V_0$ and yields the magnitude of capacitive reactance $|X_C(\omega)|$ in Ohms:

$$|X_C(\omega)| = \frac{V_0}{I_0} = \frac{V_0}{\omega C V_0} = \frac{1}{\omega C} = \frac{1}{2\pi f C}$$

Trigonometry relates cosine directly to a quarter-cycle-advanced sine wave:

$$\cos(\omega t) = \sin(\omega t + 90^\circ)$$

Capacitor current reaches its peak $I_0$ one quarter-cycle ($90^\circ$) earlier than the voltage peak $V_0$: **current in a capacitor leads voltage by $90^\circ$**.

### Inductor Impedance

An inductor operates as the physical dual of a capacitor: its magnetic field endows conducting electrons with mechanical flywheel inertia. Voltage $v(t)$ acts as pushing force $F(t)$, inductance $L$ acts as mass $m$, and current $i(t)$ acts as mechanical velocity $u_{\text{mech}}(t)$:

$$v(t) = L\,\frac{di(t)}{dt} \qquad \longleftrightarrow \qquad F(t) = m\,\frac{du_{\text{mech}}(t)}{dt}$$

Tracking that magnetic flywheel across one forward-push half-cycle under sinusoidal driving voltage $v(t)$ explains why inductor current peaks one quarter-cycle ($90^\circ$) behind voltage (equivalently, inductor voltage peaks $90^\circ$ ahead of current):

1. **Maximum acceleration at the voltage peak ($V_0$):** At the crest of the voltage push ($90^\circ$ into the cycle), forward pushing force on the electrons reaches its maximum. Current accelerates upward at its steepest rate $\frac{di(t)}{dt}$ right as $i(t)$ passes through $0\text{ A}$.
2. **Top coasting speed at the end of the forward push ($0\text{ V}$):** Across the ensuing quarter-cycle, positive voltage continues pushing charge forward until dropping back to $0\text{ V}$ at $180^\circ$. Right at that turnaround instant before push reversal, the magnetic flywheel reaches its **fastest forward speed (peak current $I_0$)**.

Those flywheel mechanics explain how inductance $L$ and frequency $f$ determine the peak current $I_0$ reached under a peak voltage push $V_0$:

- **Magnetic inertia ($L$, flywheel mass):** A doubled coil inductance $L$ doubles magnetic inertia and cuts the current acceleration rate $\frac{V_0}{L}$ in half. Half the acceleration across the cycle halves peak current $I_0$ in proportion to $\frac{1}{L}$ and doubles opposition in Ohms in proportion to $L$.
- **Time before reversal ($f$, push duration):** A low frequency $f$ applies a forward push across a long interval before reversing, accelerating current to a large peak amplitude. A high frequency $f$ shrinks the effective push window $\frac{1}{2\pi f}$ so rapidly that the flywheel barely moves, throttling $I_0$ in proportion to $\frac{1}{f}$ and raising Ohms in proportion to $f$.

Faraday's law of induction ([Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md)) writes those two physical knobs as a differential equation:

$$v(t) = L\,\frac{di(t)}{dt}$$

Connecting the sinusoidal voltage source $V_0 \sin(\omega t)$ across the inductor terminals sets the current acceleration rate at every instant $t$ by Kirchhoff's voltage law:

$$\frac{di(t)}{dt} = \frac{v(t)}{L} = \frac{V_0}{L} \sin(\omega t)$$

Integration of acceleration rate $\frac{di(t)}{dt}$ over time $t$ gives the current waveform $i(t)$ built up during the push. The time derivative of $-\cos(\omega t)$ equals $+\omega \sin(\omega t)$, so anti-differentiation divides by angular frequency $\omega$, reflecting the shorter effective push window $\frac{1}{\omega}$ at higher frequency:

$$i(t) = -\left( \frac{V_0}{\omega L} \right) \cos(\omega t) = \left( \frac{V_0}{\omega L} \right) \sin(\omega t - 90^\circ)$$

Over each cycle, $\sin(\omega t - 90^\circ)$ oscillates between $-1$ and $+1$ and reaches $+1$ at the positive current crest. Peak current $I_0$ equals peak acceleration rate $\frac{V_0}{L}$ multiplied by effective push time $\frac{1}{\omega}$ (or $\frac{1}{2\pi f}$), and differentiating $i(t)$ via Faraday's law recovers $(\omega L I_0)\sin(\omega t)$:

$$I_0 = \left( \frac{V_0}{\omega L} \right) \times 1 = \frac{V_0}{\omega L} = \frac{V_0}{2\pi f L} \qquad \Longleftrightarrow \qquad V_0 = \omega L I_0$$

Division of peak voltage push $V_0$ by peak current flow $I_0$ yields the magnitude of inductive reactance $|X_L(\omega)|$ in Ohms:

$$|X_L(\omega)| = \frac{V_0}{I_0} = \frac{V_0}{V_0 / (\omega L)} = \omega L = 2\pi f L$$

Under a shared driving voltage $V_0 \sin(\omega t)$, capacitor and inductor currents follow opposite cosine polarities:

$$+\cos(\omega t) = \sin(\omega t + 90^\circ), \qquad -\cos(\omega t) = \sin(\omega t - 90^\circ)$$

Capacitor current peaks $90^\circ$ *before* voltage, whereas inductor current peaks $90^\circ$ *after* voltage, meaning **voltage across an inductor leads current by $90^\circ$**.

### Phasor Notation and the Factor $j\omega$

Time-domain trigonometry becomes unwieldy as soon as resistive, inductive, and capacitive elements share a network and shift phase simultaneously. Phasor notation maps sinusoidal waves onto rotating arrows in the complex plane, turning time derivatives into algebraic multiplication by $j\omega$.

#### Why Phasors Exist: Perpendicular ($90^\circ$-Shifted) Waveform Components

In a single pure capacitor or inductor, voltage $v(t)$ and current $i(t)$ reach their peaks one quarter-cycle ($90^\circ$) apart in time. In a series chain containing resistance $R$, inductance $L$, and capacitance $C$ carrying a shared sinusoidal current $i(t)$, Kirchhoff's voltage law sums three component waveforms:

$$v_{\text{total}}(t) = v_R(t) + v_L(t) + v_C(t)$$

Those three voltage waveforms separate by phase relative to $i(t)$ into two perpendicular groups:

- **In-phase resistive voltage wave ($0^\circ$ relative to current):** Resistor voltage $v_R(t)$ peaks at the identical instant as current $i(t)$ with peak amplitude $V_R$.
- **Quarter-cycle-shifted reactive voltage waves ($\pm 90^\circ$ relative to current):** Inductor voltage $v_L(t)$ peaks $+90^\circ$ *ahead* of $i(t)$ at amplitude $V_L$, whereas capacitor voltage $v_C(t)$ peaks $-90^\circ$ *behind* $i(t)$ at amplitude $V_C$, leaving a net reactive wave $v_X(t)$ of amplitude $V_X$.

Component peak amplitudes and the net reactive voltage wave satisfy:

$$V_R = I_0 R, \qquad V_L = I_0 X_L, \qquad V_C = I_0 |X_C|, \qquad v_X(t) = v_L(t) + v_C(t), \qquad V_X = V_L - V_C$$

Consider a $3\,\Omega$ resistor $R$ in series with a $4\,\Omega$ inductive reactance $X_L$ driven by a $1\text{ A}$ peak current $I_0$, producing peak amplitudes $V_R$ of $3\text{ V}$ across the resistor and $V_L$ of $4\text{ V}$ across the inductor. The combined peak voltage across the pair is **not** the arithmetic sum $7\text{ V}$ ($3\text{ V}$ plus $4\text{ V}$): at the instant the resistor hits $3\text{ V}$, the inductor passes through $0\text{ V}$, and one quarter-cycle earlier at the $4\text{ V}$ inductor crest, the resistor passed through $0\text{ V}$. Separation of $\cos(\omega t)$ and $\sin(\omega t)$ by $90^\circ$ of cycle timing places $V_R$ and $V_X$ along the horizontal ($0^\circ$) and vertical ($90^\circ$) legs of a **voltage right triangle** whose hypotenuse gives the combined peak voltage:

$$V_{\text{total}} = \sqrt{V_R^2 + V_X^2} = \sqrt{(3\text{ V})^2 + (4\text{ V})^2} = 5\text{ V}$$

#### Physical Definition of a Phasor: A Strobe-Light Snapshot of Circular Motion

Addition of quarter-cycle-shifted waves without expanding trigonometric identities at every circuit node maps each sinusoid to uniform circular motion. A two-dimensional arrow of length $V_0$ spinning counterclockwise on a clock face at constant angular speed $\omega$ from initial angle $\varphi$ at time zero sweeps through instantaneous angle $\theta(t)$ linearly with time:

$$\theta(t) = \omega t + \varphi, \qquad \omega = 2\pi f$$

Orthogonal light beams project that spinning arrow onto two perpendicular coordinate axes:

- **Horizontal shadow ($x$-axis):** Overhead illumination casts the spinning arrow's horizontal projection $x(t)$ onto the $x$-axis.
- **Vertical shadow ($y$-axis):** Side illumination casts the spinning arrow's vertical projection $y(t)$ onto the $y$-axis.

Trigonometry gives both axis projections at every instant $t$:

$$x(t) = V_0 \cos(\omega t + \varphi), \qquad y(t) = V_0 \sin(\omega t + \varphi)$$

In a linear circuit driven at a single angular frequency $\omega$, every voltage and current arrow spins at that identical speed $\omega$, locking the relative timing angles between all arrows like hands welded to a single rotating shaft. Flashing a strobe light at time zero freezes the spinning assembly into static two-dimensional arrows: each arrow's **length** equals the wave's peak amplitude $V_0$, and its **direction** equals the initial timing angle $\varphi$. That frozen initial two-dimensional arrow is the **phasor** (short for *phase vector*).

#### Lifting $v(t)$ into the Complex Plane: What the Real and Imaginary Parts Do

The complex plane writes two-dimensional arrows algebraically by assigning the horizontal axis as the **Real axis** and the vertical axis as the **Imaginary axis**, labeled by the imaginary unit $j$. Euler's identity expresses both orthogonal components of any angle $\theta$ in a single complex exponential:

$$j = \sqrt{-1}, \qquad j^2 = -1, \qquad e^{j\theta} = \cos\theta + j\sin\theta$$

Evaluating Euler's identity for an arrow of length $V_0$ at instantaneous angle $\theta(t)$ packages both shadows into one expression:

$$V_0 e^{j(\omega t + \varphi)} = \underbrace{V_0 \cos(\omega t + \varphi)}_{\substack{\text{Real part }\mathrm{Re}\{\cdot\}\\\text{(horizontal shadow = }v(t)\text{)}}} + j\,\underbrace{V_0 \sin(\omega t + \varphi)}_{\substack{\text{Imaginary part }\mathrm{Im}\{\cdot\}\\\text{(vertical shadow, }90^\circ\text{ behind)}}}$$

The physical voltage waveform $v(t)$ on the copper trace is the horizontal shadow, given by the **Real part** ($\mathrm{Re}\{\cdot\}$) of the two-dimensional spinning arrow. Pairing that real horizontal shadow with its vertical imaginary companion $j V_0 \sin(\omega t + \varphi)$ inside $V_0 e^{j(\omega t + \varphi)}$ accomplishes two operations that one-dimensional trigonometry cannot perform.

First, real trigonometry traps initial angle $\varphi$ and time progression $\omega t$ together inside $\cos(\omega t + \varphi)$. In the complex exponential, the exponent addition law factors the frozen initial phasor $\hat{V}$ cleanly away from the common spinning rotor $e^{j\omega t}$:

$$e^{a+b} = e^a e^b, \qquad v(t) = V_0 \cos(\omega t + \varphi) = \mathrm{Re} \left\{ V_0 e^{j(\omega t + \varphi)} \right\} = \mathrm{Re} \left\{ \hat{V} e^{j\omega t} \right\}$$

$$\hat{V} = V_0 e^{j\varphi} = V_0 \cos\varphi + j V_0 \sin\varphi$$

Every voltage and current in the network shares that identical non-zero rotor $e^{j\omega t}$, allowing $e^{j\omega t}$ to cancel out of every circuit equation so only the static phasors $\hat{V}$ and $\hat{I}$ remain.

Second, rotating a two-dimensional arrow counterclockwise by $+90^\circ$ swings its vertical imaginary coordinate directly onto the horizontal real axis. Retaining the imaginary companion $j V_0 \sin(\omega t + \varphi)$ inside the complex arrow ensures that any $90^\circ$ capacitor or inductor phase shift rotates the vertical shadow straight into the new horizontal shadow:

$$j \cdot \left[ j\sin(\omega t) \right] = j^2 \sin(\omega t) = -\sin(\omega t) = \cos(\omega t + 90^\circ)$$

#### Turning Calculus into Ohm's Law: Why Phasors Differentiate $\hat{V} e^{j\omega t}$ and Multiply by $\pm j$

In a resistor, Ohm's law is ordinary algebra, allowing series chains, parallel branches, and voltage dividers to be solved by elementary multiplication and division. Capacitors and inductors follow differential component laws instead because both elements physically respond to a **rate of change** ($\frac{d}{dt}$).

Phasor analysis converts those differential laws into **algebraic Ohm's-law multipliers** at any angular frequency $\omega$:

$$\hat{V} = Z(\omega)\,\hat{I}$$

Performing that conversion requires substituting the spinning-arrow waveforms $\hat{V} e^{j\omega t}$ and $\hat{I} e^{j\omega t}$ into the time derivative $\frac{d}{dt}$ inside the capacitor and inductor equations. The frozen initial phasor $\hat{V}$ is constant with respect to time $t$, so differentiating $\hat{V} e^{j\omega t}$ applies the exponential chain rule to exponent $u(t)$:

$$\frac{d}{dt}\left[e^{u(t)}\right] = \frac{du(t)}{dt}\,e^{u(t)}, \qquad u(t) = j\omega t, \qquad \frac{du(t)}{dt} = j\omega$$

$$\frac{d}{dt} \left[ \hat{V} e^{j\omega t} \right] = \hat{V}\,\frac{d}{dt} \left[ e^{j\omega t} \right] = \hat{V} \left( j\omega\,e^{j\omega t} \right) = (j\omega)\,\hat{V} e^{j\omega t}$$

Taking the Real part (the horizontal shadow on the wire) of both sides shows how a time derivative acts on any sinusoidal waveform:

$$\frac{dv(t)}{dt} = \frac{d}{dt} \mathrm{Re} \left\{ \hat{V} e^{j\omega t} \right\} = \mathrm{Re} \left\{ (j\omega)\,\hat{V} e^{j\omega t} \right\}$$

The imaginary unit $j$ appears alongside $\omega$ during differentiation because taking the rate of change of a sinusoid both scales wave amplitude by $\omega$ and shifts the wave peak by one quarter-cycle ($\pm 90^\circ$ on the circular clock face). Evaluating Euler's exponential identity at $+90^\circ$ and $-90^\circ$ shows how the complex plane writes those quarter-cycle shifts:

$$e^{j 90^\circ} = \cos(90^\circ) + j\sin(90^\circ) = 0 + j(1) = +j$$

$$e^{-j 90^\circ} = \cos(-90^\circ) + j\sin(-90^\circ) = 0 + j(-1) = -j$$

Division by $j$ is algebraically identical to multiplication by $-j$, as shown by multiplying numerator and denominator of $\frac{1}{j}$ by $j$:

$$\frac{1}{j} = \frac{1 \cdot j}{j \cdot j} = \frac{j}{j^2} = \frac{j}{-1} = -j = e^{-j 90^\circ}$$

Multiplying a two-dimensional phasor arrow by $+j$ rotates it $+90^\circ$ counterclockwise (advancing its peak one quarter-cycle ahead in time), whereas multiplying by $-j$ (or dividing by $j$) rotates it $-90^\circ$ clockwise (delaying its peak one quarter-cycle behind in time). Every time derivative $\frac{d}{dt}$ inside a sinusoidal circuit equation becomes algebraic multiplication by $j\omega$.

#### Deriving the Stationary Hardware Impedance $Z(\omega)$

Substitution of the spinning voltage arrow $\hat{V} e^{j\omega t}$ and spinning current arrow $\hat{I} e^{j\omega t}$ into the resistor, inductor, and capacitor laws converts all three elements into Ohm's-law form. Dividing $\hat{V} e^{j\omega t}$ by $\hat{I} e^{j\omega t}$ cancels the common spinning rotor $e^{j\omega t}$:

$$\frac{\hat{V} e^{j\omega t}}{\hat{I} e^{j\omega t}} = \frac{\hat{V}}{\hat{I}} = Z(\omega)$$

Cancellation of $e^{j\omega t}$ shows that **impedance $Z(\omega)$ is not a time-varying waveform**; it is a **stationary hardware ratio** in Ohms.

For a **resistor** ($0^\circ$ shift, plotted on the Real axis), substituting $\hat{V}_R e^{j\omega t}$ and $\hat{I} e^{j\omega t}$ into Ohm's law and canceling $e^{j\omega t}$ yields resistor impedance $Z_R(\omega)$:

$$\hat{V}_R e^{j\omega t} = R \left( \hat{I} e^{j\omega t} \right) \qquad \Longrightarrow \qquad \hat{V}_R = R\,\hat{I} \qquad \Longrightarrow \qquad Z_R(\omega) = \frac{\hat{V}_R}{\hat{I}} = R$$

Resistance $R$ (equal to $\frac{V_R}{I_0}$) is a purely **real** number along the horizontal Real axis because a resistor scales voltage by $R$ with **$0^\circ$ timing shift**.

For an **inductor** ($+90^\circ$ shift, plotted on the positive Imaginary axis), substituting $\hat{V}_L e^{j\omega t}$ and $\hat{I} e^{j\omega t}$ into Faraday's law and applying the $j\omega$ derivative rule gives:

$$\hat{V}_L e^{j\omega t} = L\,\frac{d}{dt} \left[ \hat{I} e^{j\omega t} \right] = L \left( j\omega\,\hat{I} e^{j\omega t} \right) = (j\omega L)\,\hat{I} e^{j\omega t}$$

Dividing both sides by $e^{j\omega t}$ and $\hat{I}$ defines the complex **inductor impedance** $Z_{\text{ind}}(\omega)$ (written with subscript $\text{ind}$ so $Z_L$ remains reserved for load impedance):

$$\hat{V}_L = (j\omega L)\,\hat{I} \qquad \Longrightarrow \qquad Z_{\text{ind}}(\omega) = \frac{\hat{V}_L}{\hat{I}} = +j\omega L = +j X_L(\omega), \qquad X_L(\omega) = +\omega L$$

Inductive impedance is **positive imaginary** along the $+y$ Imaginary axis because Faraday's rate-of-change law shifts inductor voltage **$+90^\circ$ ahead** of current, represented by $+j$.

For a **capacitor** ($-90^\circ$ shift, plotted on the negative Imaginary axis), substituting $\hat{I} e^{j\omega t}$ and $\hat{V}_C e^{j\omega t}$ into the capacitor charging law and applying the $j\omega$ derivative rule gives:

$$\hat{I} e^{j\omega t} = C\,\frac{d}{dt} \left[ \hat{V}_C e^{j\omega t} \right] = C \left( j\omega\,\hat{V}_C e^{j\omega t} \right) = (j\omega C)\,\hat{V}_C e^{j\omega t}$$

Dividing out $e^{j\omega t}$, forming the voltage-to-current ratio $Z_C(\omega)$, and replacing $\frac{1}{j}$ with $-j$ define the complex **capacitor impedance** $Z_C(\omega)$:

$$Z_C(\omega) = \frac{\hat{V}_C}{\hat{I}} = \frac{1}{j\omega C} = \frac{1 \cdot j}{(j\omega C) \cdot j} = \frac{j}{j^2 \omega C} = -\frac{j}{\omega C} = +j X_C(\omega), \qquad X_C(\omega) = -\frac{1}{\omega C}$$

Capacitive impedance is **negative imaginary** along the $-y$ Imaginary axis because the capacitor charging law places capacitor voltage **$-90^\circ$ behind** current, represented by $-j$.

In a series $RLC$ chain carrying a common current phasor $\hat{I}$, Kirchhoff's voltage law adds the three component phasor voltages and factors out $\hat{I}$:

$$\hat{V}_{\text{total}} = \hat{V}_R + \hat{V}_L + \hat{V}_C = R\,\hat{I} + (j\omega L)\,\hat{I} + \left( -\frac{j}{\omega C} \right) \hat{I} = \left[ R + j\left( \omega L - \frac{1}{\omega C} \right) \right] \hat{I}$$

Division of both sides by $\hat{I}$ yields the **impedance triangle** $Z(\omega)$ and its Pythagorean magnitude $|Z(\omega)|$:

$$Z(\omega) = \frac{\hat{V}_{\text{total}}}{\hat{I}} = R + j\left( \omega L - \frac{1}{\omega C} \right) = R + j X(\omega), \qquad |Z(\omega)| = \frac{V_{\text{total}}}{I_0} = \sqrt{R^2 + X(\omega)^2}$$

Placing $0^\circ$ in-phase resistance $R$ on the horizontal Real axis and $\pm 90^\circ$ quarter-cycle-shifted net reactance $X(\omega)$ on the vertical Imaginary axis turns multi-element AC differential equations into ordinary complex-number algebra. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) applied that same transformation from $\frac{\partial}{\partial t}$ to $j\omega$ to turn the lossy Telegrapher's partial differential equations into the ordinary Helmholtz wave equation.

### Reactance Scaling with Frequency

Capacitive reactance magnitude $|X_C(f)|$ falls inversely with frequency $f$, whereas inductive reactance magnitude $|X_L(f)|$ rises linearly with frequency $f$:

$$|Z_C(f)| = |X_C(f)| = \frac{1}{2\pi f C}, \qquad |Z_{\text{ind}}(f)| = |X_L(f)| = 2\pi f L$$

Consider a typical PCB via or package pin with parasitic shunt capacitance $C$ of $0.5\text{ pF}$ and parasitic series inductance $L$ of $1.0\text{ nH}$:

- **Capacitive reactance scaling ($0.5\text{ pF}$ shunt capacitance $C$):** Magnitude $|Z_C(f)|$ equals $318\text{ M}\Omega$ at $1\text{ kHz}$, $318\text{ k}\Omega$ at $1\text{ MHz}$, $318\,\Omega$ at $1\text{ GHz}$, and $31.8\,\Omega$ at $10\text{ GHz}$, dropping by a factor of ten for every decade increase in frequency.
- **Inductive reactance scaling ($1.0\text{ nH}$ series inductance $L$):** Magnitude $|Z_{\text{ind}}(f)|$ equals $6.28\,\text{m}\Omega$ at $1\text{ MHz}$, $6.28\,\Omega$ at $1\text{ GHz}$, and $62.8\,\Omega$ at $10\text{ GHz}$, rising by a factor of ten for every decade increase in frequency.

At kilohertz and megahertz frequencies, the $0.5\text{ pF}$ capacitor behaves as an open circuit ($|Z_C(f)|$ far above $50\,\Omega$) and the $1.0\text{ nH}$ inductor behaves as a short circuit ($|Z_{\text{ind}}(f)|$ far below $50\,\Omega$), leaving a $50\,\Omega$ signal undisturbed. At $10\text{ GHz}$, both parasitic reactances reach magnitudes comparable to $50\,\Omega$ ($31.8\,\Omega$ and $62.8\,\Omega$), creating severe impedance discontinuities that reflect high-speed edges.

### Series and Parallel Combinations of $R$, $L$, and $C$, and the Voltage Divider

Representation of resistors, inductors, and capacitors as complex impedances $Z(\omega)$ unifies circuit network reduction across all passive components. Any pair of two-terminal impedances $Z_1$ and $Z_2$ combines through two universal connection geometries: series addition along a single current path and parallel reciprocal addition across a shared voltage pair.

#### Series Connection and the Voltage Divider Rule

Wiring $Z_1$ and $Z_2$ end-to-end along a single path with no branching node between them forces every electron passing through $Z_1$ to pass through $Z_2$ as well. Both elements carry the identical current phasor $\hat{I}$, and Kirchhoff's voltage law sums their individual voltage drops:

$$\hat{V}_{\text{total}} = \hat{V}_1 + \hat{V}_2 = Z_1\,\hat{I} + Z_2\,\hat{I} = (Z_1 + Z_2)\,\hat{I} \qquad \Longrightarrow \qquad Z_{\text{series}} = \frac{\hat{V}_{\text{total}}}{\hat{I}} = Z_1 + Z_2$$

Driving a series pair $Z_1$ and $Z_2$ with an input voltage $\hat{V}_{\text{in}}$ establishes a shared loop current $\hat{I}$ and produces the **voltage divider rule** across $Z_2$:

$$\hat{I} = \frac{\hat{V}_{\text{in}}}{Z_1 + Z_2} \qquad \Longrightarrow \qquad \hat{V}_{\text{out}} = Z_2\,\hat{I} = \hat{V}_{\text{in}}\,\frac{Z_2}{Z_1 + Z_2}$$

Elements in series divide the applied voltage in proportion to each element's share of total series impedance.

#### Parallel Connection and Reciprocal Addition

Wiring $Z_1$ and $Z_2$ side-by-side across the same pair of nodes applies the identical terminal voltage push $\hat{V}$ to both elements while opening a second parallel lane for current flow. Kirchhoff's current law sums the two branch currents:

$$\hat{I}_{\text{total}} = \hat{I}_1 + \hat{I}_2 = \frac{\hat{V}}{Z_1} + \frac{\hat{V}}{Z_2} = \hat{V} \left( \frac{1}{Z_1} + \frac{1}{Z_2} \right)$$

Division of $\hat{V}$ by $\hat{I}_{\text{total}}$ yields the universal parallel impedance rule:

$$\frac{1}{Z_{\text{parallel}}} = \frac{1}{Z_1} + \frac{1}{Z_2} \qquad \Longrightarrow \qquad Z_{\text{parallel}} = \frac{Z_1 Z_2}{Z_1 + Z_2}$$

Connecting a second $100\,\Omega$ resistor in parallel with an existing $100\,\Omega$ resistor opens a second identical path under the same voltage push, doubling total current flow and cutting combined resistance in half:

$$R_{\text{parallel}} = \frac{(100\,\Omega)(100\,\Omega)}{100\,\Omega + 100\,\Omega} = \frac{100\,\Omega}{2} = 50\,\Omega$$

#### Resistors and Inductors in Series and Parallel

Those universal series and parallel rules explain why inductors combine like resistors whereas capacitors follow the opposite pattern. In **resistors**, series connection lengthens the frictional path so resistances add directly, whereas parallel connection widens the conductive path so reciprocals add:

$$R_{\text{series}} = R_1 + R_2, \qquad \frac{1}{R_{\text{parallel}}} = \frac{1}{R_1} + \frac{1}{R_2}, \qquad R_{\text{parallel}} = \frac{R_1 R_2}{R_1 + R_2}$$

In **inductors**, inductance $L$ sits in the numerator of $j\omega L$ and represents magnetic flywheel inertia. Wiring two coils in series forces a single current to accelerate both magnetic flywheels in tandem like coupled train cars, whereas parallel wiring splits current acceleration across two branches. Substitution of $j\omega L_1$ and $j\omega L_2$ into the universal impedance rules and cancellation of $j\omega$ give:

$$L_{\text{series}} = L_1 + L_2, \qquad \frac{1}{L_{\text{parallel}}} = \frac{1}{L_1} + \frac{1}{L_2}, \qquad L_{\text{parallel}} = \frac{L_1 L_2}{L_1 + L_2}$$

#### Capacitors in Parallel and Series

Capacitors follow the flipped combination pattern because capacitance $C$ sits in the denominator of capacitive impedance $\frac{1}{j\omega C}$. A parallel-plate capacitor consists of two flat metal plates of surface area $A$ separated by an insulating dielectric gap of thickness $d_{\text{gap}}$, with one lead attached to the upper plate and one lead attached to the lower plate:

$$C = \frac{\varepsilon A}{d_{\text{gap}}} \qquad \Longleftrightarrow \qquad \frac{1}{C} = \frac{d_{\text{gap}}}{\varepsilon A}$$

Wiring two capacitors in **parallel** across a $+V$ supply rail and a $0\text{ V}$ ground rail connects both upper leads to $+V$ and both lower leads to $0\text{ V}$, while each capacitor retains its own gap thickness $d_{\text{gap}}$. Both capacitors experience the full voltage $V$ side-by-side, storing charges $Q_1$ on area $A_1$ and $Q_2$ on area $A_2$ like one wider capacitor of combined plate area $A_1 + A_2$:

$$Q_1 = C_1 V, \qquad Q_2 = C_2 V, \qquad Q_{\text{total}} = Q_1 + Q_2 = (C_1 + C_2)\,V, \qquad C_{\text{parallel}} = \frac{\varepsilon(A_1 + A_2)}{d_{\text{gap}}} = C_1 + C_2$$

Wiring two capacitors in **series** along a single path connects the $+V$ source to the upper plate of $C_1$, joins the lower plate of $C_1$ by a middle wire to the upper plate of $C_2$, and ties the lower plate of $C_2$ to $0\text{ V}$ ground. That middle wire forms an isolated metal island trapped between two insulating gaps where no external charge can enter or leave. Pushing $+Q$ onto the upper plate of $C_1$ electrostatically repels $+Q$ off the lower plate of $C_1$ onto the upper plate of $C_2$, leaving the identical shifted charge $Q$ on both capacitors across the combined dielectric gap $d_{\text{gap},1} + d_{\text{gap},2}$:

$$V_{\text{total}} = V_1 + V_2 = \frac{Q}{C_1} + \frac{Q}{C_2} = Q \left( \frac{1}{C_1} + \frac{1}{C_2} \right)$$

Division of $V_{\text{total}}$ by $Q$ (or substitution of $\frac{1}{j\omega C}$ into $Z_1 + Z_2$) yields the series capacitor formulas:

$$\frac{1}{C_{\text{series}}} = \frac{1}{C_1} + \frac{1}{C_2} = \frac{d_{\text{gap},1} + d_{\text{gap},2}}{\varepsilon A}, \qquad C_{\text{series}} = \frac{C_1 C_2}{C_1 + C_2}$$

### Putting Complex Impedance to Work: Solving for the RC Half-Power Point

In [Chapter 2](02_Frequency_Content_of_Digital_Signals.md), deriving the frequency response of a single-pole $RC$ low-pass filter required setting up and solving a time-domain differential equation. Complex capacitor impedance $Z_C(\omega)$ and the series voltage divider rule solve that same filter by elementary algebra to find the half-power frequency $f_{3\text{dB}}$:

$$Z_1 = R, \qquad Z_2 = Z_C(\omega) = \frac{1}{j\omega C}$$

A series resistor $Z_1$ driving a shunt capacitor $Z_2$, with output voltage measured across the capacitor, forms a complex voltage divider:

$$H(\omega) = \frac{\hat{V}_{\text{out}} (\omega)}{\hat{V}_{\text{in}} (\omega)} = \frac{Z_C(\omega)}{R + Z_C(\omega)} = \frac{\dfrac{1}{j\omega C}}{R + \dfrac{1}{j\omega C}}$$

Multiplication of both numerator and denominator by $j\omega C$ clears the internal fraction:

$$H(\omega) = \frac{1}{1 + j\omega RC}$$

Taking the Pythagorean magnitude $\sqrt{a^2 + b^2}$ of the complex denominator $1 + j(\omega RC)$ gives the voltage amplitude gain $|H(f)|$ at any frequency $f$:

$$|H(f)| = \frac{1}{\sqrt{1^2 + (\omega RC)^2}} = \frac{1}{\sqrt{1 + (2\pi f RC)^2}}$$

Electrical power delivered to a load scales with the square of voltage amplitude $|H(f)|^2$, so setting $|H(f_{3\text{dB}})|^2$ equal to $\frac{1}{2}$ defines the **half-power cutoff frequency** $f_{3\text{dB}}$:

$$|H(f_{3\text{dB}})|^2 = \frac{1}{1 + (2\pi f_{3\text{dB}} RC)^2} = \frac{1}{2}$$

Matching denominators occurs at the frequency where capacitive reactance magnitude $|X_C(f_{3\text{dB}})|$ equals series resistance $R$:

$$(2\pi f_{3\text{dB}} RC)^2 = 1, \qquad |X_C(f_{3\text{dB}})| = \frac{1}{2\pi f_{3\text{dB}} C} = R \qquad \Longrightarrow \qquad f_{3\text{dB}} = \frac{1}{2\pi RC}$$

At cutoff frequency $f_{3\text{dB}}$, power gain equals $\frac{1}{2}$ ($-3.01\text{ dB}$) and voltage gain drops to $\frac{1}{\sqrt{2}}$. Replacing $2\pi RC$ with $\frac{1}{f_{3\text{dB}}}$ writes the transfer magnitude in normalized form:

$$|H(f_{3\text{dB}})| = \frac{1}{\sqrt{2}} \approx 0.707, \qquad 2\pi f RC = \frac{f}{f_{3\text{dB}}}, \qquad |H(f)| = \frac{1}{\sqrt{1 + \left( \dfrac{f}{f_{3\text{dB}}} \right)^2}}$$

### Why Reflections Occur and the Derivation of $\Gamma$ from Kirchhoff's Laws

Finite wave speed forces an electromagnetic wave to reflect at any impedance change. In a steady-state DC circuit, connecting a second $100\,\Omega$ load in parallel with an existing $100\,\Omega$ load halves combined load resistance to $50\,\Omega$ and doubles steady battery current, yet the battery cannot detect that distant switch closure instantaneously. Information that downstream impedance changed travels from load back to source solely as an electromagnetic adjustment wavefront propagating through the dielectric at finite phase velocity $v_p$:

$$v_p = \frac{c}{\sqrt{\varepsilon_r}}$$

On a transmission line of characteristic impedance $Z_0$, the forward-traveling incident wave arrives at boundary coordinate $\ell$ with voltage $V_{\text{inc}}$ and current $I_{\text{inc}}$ locked in the geometric ratio $Z_0$:

$$\frac{V_{\text{inc}}}{I_{\text{inc}}} = Z_0 \qquad \Longrightarrow \qquad I_{\text{inc}} = +\frac{V_{\text{inc}}}{Z_0}$$

Across the boundary sits a load or second transmission line of impedance $Z_L$, which demands that the transmitted wave entering it obey the ratio $Z_L$:

$$\frac{V_{\text{trans}}}{I_{\text{trans}}} = Z_L \qquad \Longrightarrow \qquad I_{\text{trans}} = +\frac{V_{\text{trans}}}{Z_L}$$

At any boundary where $Z_L$ differs from $Z_0$, a single incident wave cannot satisfy both ratios simultaneously. Setting $V_{\text{trans}}$ equal to $V_{\text{inc}}$ breaks current continuity ($\frac{V_{\text{inc}}}{Z_L}$ differs from $\frac{V_{\text{inc}}}{Z_0}$), whereas setting $I_{\text{trans}}$ equal to $I_{\text{inc}}$ breaks voltage continuity ($I_{\text{inc}} Z_L$ differs from $I_{\text{inc}} Z_0$). The boundary resolves this conflict by splitting the incident wave into a **transmitted wave** ($V_{\text{trans}}, I_{\text{trans}}$) continuing forward into $Z_L$ and a **reflected wave** ($V_{\text{ref}}, I_{\text{ref}}$) traveling backward onto the $Z_0$ line toward the source.

#### Boundary Voltage Addition Versus Current Subtraction

Consider the side view of a horizontal signal trace running above a $0\text{ V}$ ground plane, with $+z$ pointing **rightward** (driver to load) and $-z$ pointing **leftward** (load to driver). Electric potential on the trace is a scalar vertical difference measured with respect to the underlying $0\text{ V}$ ground plane and carries no horizontal left-or-right sign. Positive wave voltage raises local copper potential above ground for both rightward ($+z$) and leftward ($-z$) waves, so Kirchhoff's voltage law at the boundary sums the two wave voltages directly:

$$V_{\text{inc}} + V_{\text{ref}} = V_{\text{trans}}$$

Trace current $I$, by contrast, is a directed horizontal charge flow with rightward ($+z$) defined as positive. In the **charge-flow picture**, a positive voltage wave advancing into an uncharged trace section deposits positive charge onto the trace capacitance ahead of it. A rightward forward wave ($+z$) of positive voltage $V_{\text{inc}}$ pushes positive charge **rightward ($+z$)**, whereas a leftward reflected wave ($-z$) of positive voltage $V_{\text{ref}}$ charges trace capacitance to the **left** of the boundary and pushes positive charge **leftward ($-z$)**.

Electromagnetic **field geometry** confirms the identical sign reversal through the Poynting energy-flux vector $\vec{S}$ and Ampère's right-hand grip rule:

$$\vec{S} = \vec{E} \times \vec{H}$$

Pointing the right-hand fingers along electric field $\vec{E}$ and curling them toward magnetic field $\vec{H}$ (or $\vec{B}$) aligns the outstretched thumb with propagation direction $\vec{S}$. Positive trace potential above the $0\text{ V}$ ground plane points electric field lines straight **downward** ($\downarrow$). For the **forward wave** (thumb **rightward** $\rightarrow$ and fingers **downward** $\downarrow$), the fingers curl **into the page** ($\otimes$), corresponding by Ampère's grip rule to conventional current flowing **rightward ($+z$)**:

$$I_{\text{inc}} = +\frac{V_{\text{inc}}}{Z_0}$$

For the **reflected wave** (thumb **leftward** $\leftarrow$ with positive $V_{\text{ref}}$ still pointing $\vec{E}$ **downward** $\downarrow$), pointing the fingers downward with the thumb leftward curls the fingers **out of the page** ($\odot$). Reversing propagation direction while keeping $\vec{E}$ downward reverses $\vec{B}$ out of the page ($\odot$) and drives conventional current **leftward ($-z$)**:

$$I_{\text{ref}} = -\frac{V_{\text{ref}}}{Z_0}$$

#### Algebraic Solution for the Reflection Coefficient

Kirchhoff's current law at the boundary equates net rightward current on the $Z_0$ side to rightward current entering $Z_L$:

$$I_{\text{inc}} + I_{\text{ref}} = I_{\text{trans}} \qquad \Longrightarrow \qquad \frac{V_{\text{inc}}}{Z_0} - \frac{V_{\text{ref}}}{Z_0} = \frac{V_{\text{trans}}}{Z_L}$$

Substitution of voltage continuity ($V_{\text{inc}} + V_{\text{ref}}$ for $V_{\text{trans}}$) into current continuity eliminates $V_{\text{trans}}$:

$$\frac{V_{\text{inc}} - V_{\text{ref}}}{Z_0} = \frac{V_{\text{inc}} + V_{\text{ref}}}{Z_L}$$

Cross-multiplication by $Z_0 Z_L$ and grouping of incident and reflected voltage terms give:

$$Z_L V_{\text{inc}} - Z_L V_{\text{ref}} = Z_0 V_{\text{inc}} + Z_0 V_{\text{ref}} \qquad \Longrightarrow \qquad V_{\text{inc}}(Z_L - Z_0) = V_{\text{ref}}(Z_L + Z_0)$$

The ratio of reflected voltage $V_{\text{ref}}$ to incident voltage $V_{\text{inc}}$ defines the **voltage reflection coefficient** $\Gamma$:

$$\Gamma = \frac{V_{\text{ref}}}{V_{\text{inc}}} = \frac{Z_L - Z_0}{Z_L + Z_0}$$

Division of leftward reflected current $I_{\text{ref}}$ by rightward incident current $I_{\text{inc}}$ gives the current reflection ratio the opposite algebraic sign:

$$\frac{I_{\text{ref}}}{I_{\text{inc}}} = -\frac{V_{\text{ref}}}{V_{\text{inc}}} = -\Gamma$$

#### Step-Down Discontinuities and Rightward Discharge Current

At a step-down discontinuity where $Z_L$ sits below $Z_0$ (such as a $50\,\Omega$ trace meeting a $25\,\Omega$ load formed by two $50\,\Omega$ branch traces in parallel), the lower-impedance load offers less opposition to current flow than the incoming trace. That lower-impedance load demands **more rightward current** ($I_{\text{trans}}$ above $I_{\text{inc}}$) at a **lower boundary voltage** ($V_{\text{trans}}$ below $V_{\text{inc}}$).

The lower-impedance load pulls that extra rightward current directly off the adjacent upstream $Z_0$ trace capacitance before the distant transmitter learns that the boundary exists. Draining positive charge off the upstream trace steps trace voltage *down* as a **negative-voltage discharge wave** (negative $V_{\text{ref}}$) sweeps leftward ($-z$) toward the source, while drained positive charge flows **rightward ($+z$)** (positive $I_{\text{ref}}$) across the boundary into $Z_L$.

The reflection equations capture both physical effects automatically: $Z_L$ below $Z_0$ makes $\Gamma$ and $V_{\text{ref}}$ negative, and substituting negative $V_{\text{ref}}$ into $-\frac{V_{\text{ref}}}{Z_0}$ yields positive (**rightward, $+z$**) reflected current $I_{\text{ref}}$. Suppose a $+1.00\text{ V}$ forward wave $V_{\text{inc}}$ on a $50\,\Omega$ trace $Z_0$ strikes a $25\,\Omega$ load $Z_L$.

First, the rightward ($+z$) incident wave arrives at the boundary carrying $+20.0\text{ mA}$:

$$V_{\text{inc}} = +1.00\text{ V}, \qquad I_{\text{inc}} = +\frac{1.00\text{ V}}{50\,\Omega} = +20.0\text{ mA} \quad (\text{current flowing rightward, }+z)$$

Second, the step-down boundary from $50\,\Omega$ to $25\,\Omega$ sets a negative reflection coefficient $\Gamma$:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0} = \frac{25\,\Omega - 50\,\Omega}{25\,\Omega + 50\,\Omega} = \frac{-25\,\Omega}{75\,\Omega} = -\frac{1}{3} \approx -0.333$$

Third, the reflected discharge wave propagates leftward ($-z$), stepping voltage down while pulling $+6.67\text{ mA}$ of extra positive charge rightward ($+z$):

$$V_{\text{ref}} = \Gamma\,V_{\text{inc}} = \left( -\frac{1}{3} \right) (+1.00\text{ V}) = -0.333\text{ V} \quad (\text{wavefront moving leftward, }-z)$$

$$I_{\text{ref}} = -\frac{V_{\text{ref}}}{Z_0} = -\frac{-0.333\text{ V}}{50\,\Omega} = +6.67\text{ mA} \quad (\text{current flowing rightward, }+z)$$

Fourth, summing incident and reflected waves at the boundary steps transmitted voltage down to $+0.667\text{ V}$ while boosting rightward current to $+26.67\text{ mA}$, matching the $25\,\Omega$ load ratio:

$$V_{\text{trans}} = V_{\text{inc}} + V_{\text{ref}} = +1.00\text{ V} + (-0.333\text{ V}) = +0.667\text{ V}$$

$$I_{\text{trans}} = I_{\text{inc}} + I_{\text{ref}} = +20.0\text{ mA} + 6.67\text{ mA} = +26.67\text{ mA} \quad (\text{current flowing rightward, }+z)$$

$$\frac{V_{\text{trans}}}{I_{\text{trans}}} = \frac{0.667\text{ V}}{0.02667\text{ A}} = 25\,\Omega = Z_L$$

### The Transmission Coefficient and Passive Power Conservation

An impedance boundary splits an arriving wave into two waves traveling in opposite directions, and link engineers track signal behavior at both ends of the channel. At the launch port, the **voltage reflection coefficient** $\Gamma$ measures the leftward ($-z$) echo returning onto the $Z_0$ line, governing upstream signal corruption, driver re-reflections, and return-loss measurements ([Chapter 7](07_Time_Domain_Reflectometry.md) and [Chapter 8](08_S_Parameters_and_VNA.md)).

At the far end of the trace (coordinate $\ell$), the digital receiver comparator senses the **transmitted voltage** $V_{\text{trans}}$ surviving across the boundary into $Z_L$. Division of the boundary voltage continuity equation by $V_{\text{inc}}$ defines the companion **voltage transmission coefficient** $T_V$ (denoted $T_V$ so $\tau$ remains reserved for time constants and $T$ for oscillation period):

$$T_V = \frac{V_{\text{trans}}}{V_{\text{inc}}} = \frac{V_{\text{inc}} + V_{\text{ref}}}{V_{\text{inc}}} = 1 + \frac{V_{\text{ref}}}{V_{\text{inc}}} = 1 + \Gamma$$

Substitution of the impedance formula for $\Gamma$ over the common denominator $Z_L + Z_0$ expresses $T_V$ directly in terms of $Z_L$ and $Z_0$:

$$T_V = 1 + \frac{Z_L - Z_0}{Z_L + Z_0} = \frac{(Z_L + Z_0) + (Z_L - Z_0)}{Z_L + Z_0} = \frac{2 Z_L}{Z_L + Z_0}$$

Reflection coefficient $\Gamma$ and transmission coefficient $T_V$ form companion descriptions of the same boundary split: $\Gamma$ measures the reflected voltage fraction, and $T_V$ scales $V_{\text{inc}}$ into the forward load voltage $V_{\text{trans}}$.

#### Passive Boundary Power Split and Voltage Step-Up Conservation

A passive copper boundary contains no internal battery or amplifier and cannot create or destroy energy. Every milliwatt of arriving incident power $P_{\text{inc}}$ must either bounce backward in reflected power $P_{\text{ref}}$ or enter the load in transmitted power $P_{\text{trans}}$.

Both the incident wave $V_{\text{inc}}$ and reflected wave $V_{\text{ref}}$ propagate on the same $Z_0$ transmission line, where wave power equals $\frac{V^2}{Z_0}$:

$$P_{\text{inc}} = \frac{V_{\text{inc}}^2}{Z_0}, \qquad P_{\text{ref}} = \frac{V_{\text{ref}}^2}{Z_0} = \frac{(\Gamma\,V_{\text{inc}})^2}{Z_0} = \Gamma^2 \left( \frac{V_{\text{inc}}^2}{Z_0} \right) = \Gamma^2\,P_{\text{inc}}$$

Division of $P_{\text{ref}}$ by $P_{\text{inc}}$ fixes the reflected power fraction at $\Gamma^2$, and energy conservation fixes the transmitted power fraction entering $Z_L$ at $1 - \Gamma^2$:

$$\frac{P_{\text{ref}}}{P_{\text{inc}}} = \Gamma^2, \qquad P_{\text{trans}} = P_{\text{inc}} - P_{\text{ref}} = (1 - \Gamma^2)\,P_{\text{inc}} \qquad \Longrightarrow \qquad \frac{P_{\text{trans}}}{P_{\text{inc}}} = 1 - \Gamma^2$$

Transmitted voltages $V_{\text{trans}}$ larger than $V_{\text{inc}}$ never violate energy conservation because **voltage measures electrical push $V$, whereas power measures voltage push multiplied by current flow:**

$$P = V \cdot I$$

The incident wave travels in impedance $Z_0$ while the transmitted wave enters $Z_L$, adjusting current opposite to voltage across both mismatch directions. At a **step-up boundary** ($Z_L$ above $Z_0$), higher load impedance restricts current flow and builds up a transmitted voltage *larger* than $V_{\text{inc}}$ ($T_V$ above $1$, reaching $2$ and $2 V_{\text{inc}}$ at an open circuit), conserving energy because $Z_L$ draws proportionally smaller current $I_{\text{trans}}$ than $I_{\text{inc}}$.

At a **step-down boundary** ($Z_L$ below $Z_0$), a $1.00\text{ V}$ incident wave on a $50\,\Omega$ trace $Z_0$ carries $20.0\text{ mW}$ of incident power, whereas sustaining that full $1.00\text{ V}$ across a $25\,\Omega$ load $Z_L$ would require $40.0\text{ mW}$ (twice the arriving power):

$$P_{\text{inc}} = \frac{V_{\text{inc}}^2}{Z_0} = \frac{(1.00\text{ V})^2}{50\,\Omega} = 20.0\text{ mW}, \qquad P_{\text{hypothetical}} = \frac{(1.00\text{ V})^2}{25\,\Omega} = 40.0\text{ mW}$$

The $25\,\Omega$ boundary prevents an energy deficit by stepping $T_V$ down to $\frac{2}{3}$ ($0.667\text{ V}$ transmitted voltage) while boosting current to $26.67\text{ mA}$.

Accounting for both the voltage ratio $T_V$ and the impedance ratio $\frac{Z_0}{Z_L}$ expresses the transmitted power fraction directly in terms of $T_V$:

$$\frac{P_{\text{trans}}}{P_{\text{inc}}} = \frac{\dfrac{V_{\text{trans}}^2}{Z_L}}{\dfrac{V_{\text{inc}}^2}{Z_0}} = \left( \frac{V_{\text{trans}}}{V_{\text{inc}}} \right)^2 \frac{Z_0}{Z_L} = T_V^2\,\frac{Z_0}{Z_L}$$

Substitution of the impedance formula for $T_V$ and cancellation of one factor of $Z_L$ yield:

$$\frac{P_{\text{trans}}}{P_{\text{inc}}} = \left( \frac{2 Z_L}{Z_L + Z_0} \right)^2 \frac{Z_0}{Z_L} = \frac{4 Z_L^2}{(Z_L + Z_0)^2} \cdot \frac{Z_0}{Z_L} = \frac{4 Z_0 Z_L}{(Z_L + Z_0)^2}$$

Expansion of $1 - \Gamma^2$ over the common denominator $(Z_L + Z_0)^2$ produces the identical fraction:

$$1 - \Gamma^2 = 1 - \left( \frac{Z_L - Z_0}{Z_L + Z_0} \right)^2 = \frac{(Z_L + Z_0)^2 - (Z_L - Z_0)^2}{(Z_L + Z_0)^2} = \frac{(Z_L^2 + 2 Z_0 Z_L + Z_0^2) - (Z_L^2 - 2 Z_0 Z_L + Z_0^2)}{(Z_L + Z_0)^2} = \frac{4 Z_0 Z_L}{(Z_L + Z_0)^2}$$

Every passive load $Z_L$ satisfies the complete boundary power balance:

$$\frac{P_{\text{trans}}}{P_{\text{inc}}} = T_V^2\,\frac{Z_0}{Z_L} = 1 - \Gamma^2 \qquad \Longrightarrow \qquad P_{\text{ref}} + P_{\text{trans}} = \Gamma^2\,P_{\text{inc}} + (1 - \Gamma^2)\,P_{\text{inc}} = P_{\text{inc}}$$

In the step-down transition from $50\,\Omega$ to $25\,\Omega$ ($\Gamma$ of $-\frac{1}{3}$ and $T_V$ of $\frac{2}{3}$), the reflected and transmitted power fractions sum to $100\%$ of the $20.0\text{ mW}$ incident wave:

$$\frac{P_{\text{ref}}}{P_{\text{inc}}} = \Gamma^2 = \left( -\frac{1}{3} \right)^2 = \frac{1}{9} \approx 11.1\% \quad (2.22\text{ mW})$$

$$\frac{P_{\text{trans}}}{P_{\text{inc}}} = T_V^2\,\frac{Z_0}{Z_L} = \left( \frac{2}{3} \right)^2 \frac{50\,\Omega}{25\,\Omega} = \frac{8}{9} \approx 88.9\% \quad (17.78\text{ mW})$$

### Recovering Impedance from the Reflection Coefficient

Internal vias, pads, and receiver terminations sit deep inside a fabricated PCB or IC package where a physical ohmmeter cannot reach them. Time-domain reflectometers ([Chapter 7](07_Time_Domain_Reflectometry.md)) and vector network analyzers ([Chapter 8](08_S_Parameters_and_VNA.md)) deduce those hidden impedances remotely from the launch port: the instrument sends a known incident wave $V_{\text{inc}}$ into the line, measures the returning wave $V_{\text{ref}}$ to determine $\Gamma$, and inverts the reflection relation for unknown impedance $Z_L$:

$$\Gamma = \frac{V_{\text{ref}}}{V_{\text{inc}}} = \frac{Z_L - Z_0}{Z_L + Z_0}$$

Multiplication of both sides by $Z_L + Z_0$ and collection of $Z_L$ terms on one side isolate $Z_L$:

$$\Gamma(Z_L + Z_0) = Z_L - Z_0 \quad \Longrightarrow \quad Z_0(1 + \Gamma) = Z_L(1 - \Gamma) \quad \Longrightarrow \quad Z_L = Z_0\,\frac{1 + \Gamma}{1 - \Gamma}$$

This bilinear transformation between $\Gamma$ and $Z_L$ forms the mathematical basis of TDR impedance profiling, S-parameter return-loss conversion, and the Smith chart ([Chapter 9](09_Smith_Charts.md)).

### Five Canonical Boundary Conditions and Their Field Energy Mechanics

Any passive load $Z_L$ terminating a $Z_0$ transmission line falls into one of five canonical boundary regimes spanning zero Ohms to an open circuit. Across every passive termination regime, the boundary wave equations hold **instant-by-instant** at boundary coordinate $\ell$ for every instant $t$:

$$v_{\text{ref}}(\ell, t) = \Gamma\,v_{\text{inc}}(\ell, t), \qquad v_{\text{trans}}(\ell, t) = T_V\,v_{\text{inc}}(\ell, t)$$

An arriving wave does **not** need to "complete a cycle" at the boundary. In digital time-domain analysis, the arriving signal is a **DC step wave** (a logic `0` to logic `1` transition launched at time zero, as in [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)), which has **no cycles at all**. Ahead of the moving step wavefront, the trace sits uncharged at $0\text{ V}$ and $0\text{ A}$; behind the wavefront, the trace sits at a flat plateau of $+V_{\text{inc}}$ and $+I_{\text{inc}}$.

#### Open-Circuit Charge Pile-Up and Inductive Braking

Consider a $+1.0\text{ V}$ step wave ($+20\text{ mA}$ forward current $I_{\text{inc}}$ on a $50\,\Omega$ trace $Z_0$) striking an **open circuit** at coordinate $\ell$ (infinite $Z_L$, reflection coefficient $\Gamma$ of $+1$, transmission coefficient $T_V$ of $2$). Along the middle of the uniform $50\,\Omega$ trace, each copper segment stays at $+1.0\text{ V}$ because $+20\text{ mA}$ entering from the left exits immediately into the next segment on the right. At an open dead-end tip, the copper trace ends in mid-air with no downstream segment, yet upstream trace inductance $L$ keeps shoving $+20\text{ mA}$ rightward onto the tip capacitance $C$.

Arrival of $+20\text{ mA}$ from the left with $0\text{ mA}$ exiting to the right piles positive charge $Q(t)$ onto tip capacitance $C$ like water rising against a closed dam, raising tip voltage $v_{\text{tip}}(t)$ above $+1.0\text{ V}$. Stopping $+20\text{ mA}$ on a $50\,\Omega$ trace requires $+1.0\text{ V}$ of extra electrostatic back-pressure on top of the initial $+1.0\text{ V}$, doubling boundary voltage $V_{\text{total}}$ to $+2.0\text{ V}$, bringing net current $I_{\text{total}}$ to $0\text{ A}$, and launching a $+1.0\text{ V}$ **charge-pile-up compression wave** leftward toward the source:

$$v_{\text{tip}}(t) = \frac{Q(t)}{C}, \qquad \Delta V_{\text{pile-up}} = (+20\text{ mA})(50\,\Omega) = +1.0\text{ V}$$

$$V_{\text{total}} = 2 V_{\text{inc}} = +2.0\text{ V}, \qquad I_{\text{total}} = 0\text{ A}$$

$$V_{\text{ref}} = +V_{\text{inc}} = +1.0\text{ V}, \qquad I_{\text{ref}} = -I_{\text{inc}} = -20\text{ mA}$$

A modest $+1.1\text{ V}$ tip potential cannot stop an incoming $+1.0\text{ V}$ wave because charges in the $+1.0\text{ V}$ trace are already coasting rightward at $+20\text{ mA}$ through trace inductance $L$ with magnetic flywheel momentum. Initial acceleration of each segment from $0\text{ mA}$ up to $+20\text{ mA}$ required a $+1.0\text{ V}$ forward push across $L$, so Faraday's law demands an equal and opposite $+1.0\text{ V}$ **backward braking difference** $\Delta V_{\text{braking}}$ above $+1.0\text{ V}$ to decelerate $+20\text{ mA}$ back to $0\text{ A}$:

$$v_L(t) = L\,\frac{di(t)}{dt}, \qquad \Delta V_{\text{braking}} = V_{\text{tip}} - 1.0\text{ V}, \qquad \Delta I_{\text{braking}} = \frac{0.1\text{ V}}{50\,\Omega} = 2\text{ mA}$$

At the instant $V_{\text{tip}}$ reaches $+1.1\text{ V}$, the $0.1\text{ V}$ backward push across $50\,\Omega$ slows current by only $2\text{ mA}$, leaving $+18\text{ mA}$ still coasting into the dead-end tip. Rightward current continues piling charge onto the tip until $V_{\text{tip}}$ reaches $+2.0\text{ V}$ (twice nominal charge), producing the full $+1.0\text{ V}$ braking push. In the DC steady state after all reflections between tip and driver ring out, the open-ended trace rests fully charged at supply voltage $V_S$ with $0\text{ A}$ steady-state current:

$$V_{\text{final}} = V_S, \qquad I_{\text{final}} = 0\text{ A}$$

#### Short-Circuit Charge Drain and Current Doubling

A **short circuit** at coordinate $\ell$ (zero load resistance $Z_L$, reflection coefficient $\Gamma$ of $-1$, transmission coefficient $T_V$ of $0$) is a solid vertical copper bridge tying the signal trace directly to the $0\text{ V}$ ground plane. Zero-ohm solid metal cannot sustain a vertical potential difference across itself, clamping boundary potential $v(\ell, t)$ to $0\text{ V}$ and draining arriving positive charge straight into ground. Upstream coordinates along the trace do not drop to $0\text{ V}$ instantaneously because distributed inductance $L$ per meter between launch and short limits wave propagation to finite speed $v_p$.

Arrival of the $+1.0\text{ V}$ step at one-way delay $t_{pd}$ exposes the charged trace capacitance beside coordinate $\ell$ to the $0\text{ V}$ drain, dumping stored positive charge rightward into the short. That rapid discharge clamps local voltage $V_{\text{total}}$ to $0\text{ V}$ and adds $+20\text{ mA}$ of rightward discharge current to the incoming $+20\text{ mA}$, doubling total rightward current $I_{\text{total}}$ to $+40\text{ mA}$ while a $-1.0\text{ V}$ **discharge wave** sweeps leftward:

$$V_{\text{ref}} = -V_{\text{inc}} = -1.0\text{ V}, \qquad I_{\text{ref}} = +I_{\text{inc}} = +20\text{ mA}, \qquad V_{\text{total}} = 0\text{ V}, \qquad I_{\text{total}} = 2 I_{\text{inc}} = +40\text{ mA}$$

Upstream of the returning leftward wavefront, the trace remains at $+1.0\text{ V}$ and $+20\text{ mA}$; downstream between the returning wavefront and the short, the trace sits drained at $0\text{ V}$ and $+40\text{ mA}$. Steady-state settling against a transmitter of supply $V_S$ and positive internal resistance $R_S$ leaves the entire lossless trace at $0\text{ V}$ carrying continuous DC current $I_{\text{final}}$ into ground, with $100\%$ of $V_S$ dropped across $R_S$:

$$V_{\text{final}} = 0\text{ V}, \qquad I_{\text{final}} = \frac{V_S}{R_S}$$

#### Capacitive Electric Energy and Inductive Magnetic Energy per Meter

Open-circuit and short-circuit reflections convert energy directly between magnetic and electric fields inside the overlap zone where incident and reflected waves coexist:

- **Open-circuit field conversion:** Zero net boundary current ($0\text{ A}$) collapses magnetic field $\vec{B}$ to zero and converts kinetic magnetic energy into electrostatic potential energy inside the doubled electric field ($2 V_{\text{inc}}$).
- **Short-circuit field conversion:** Zero net boundary potential ($0\text{ V}$) collapses electric field $\vec{E}$ to zero and converts capacitive electrostatic energy into magnetic energy inside the doubled magnetic field ($2 I_{\text{inc}}$).

Quantifying that conversion requires integrating energy delivered per meter into trace capacitance $C$ and trace inductance $L$. Instantaneous power $p(t)$ equals the energy delivery rate $\frac{dW}{dt}$ in Joules per second, so an infinitesimal time step $dt$ adds energy $dW$:

$$dW = p(t)\,dt = v(t)\,i(t)\,dt$$

Charging an initially empty capacitor ($0\text{ V}$ at time zero) up to final voltage $V$ and final charge $Q$ at time $t_1$ pushes the first electron onto an uncharged plate against $0\text{ V}$ and the last electron against full voltage $V$. Opposing plate potential $v(q)$ rises linearly with $q$ as $\frac{q}{C}$, so plotting voltage $v$ (height) against charge $q$ (base $C V$) forms a **right triangle** of electric energy $w_E$:

$$w_E = \frac{1}{2} \times \text{base} \times \text{height} = \frac{1}{2} (C V) V = \frac{1}{2} C V^2$$

Calculus confirms that triangle area directly. Substituting the capacitor charging law for $i(t)$ and pulling constant $C$ outside the integral give:

$$w_E = \int_{t=0}^{t=t_1} v(t)\,i(t)\,dt = \int_{t=0}^{t=t_1} v(t) \left( C\,\frac{dv(t)}{dt} \right) dt = C \int_{t=0}^{t=t_1} v(t) \left( \frac{dv(t)}{dt}\,dt \right)$$

Changing variables via $dv$ for $\frac{dv(t)}{dt}\,dt$ maps time limits $[0, t_1]$ to voltage limits $[0, V]$, and integrating $v\,dv$ by the power rule yields **electric field energy stored per meter of trace** (for distributed $C$ in $\text{F/m}$):

$$dv = \frac{dv(t)}{dt}\,dt, \qquad w_E = C \int_{v=0}^{v=V} v\,dv = C \left[ \frac{v^2}{2} \right]_{v=0}^{v=V} = C \left( \frac{V^2}{2} - \frac{0^2}{2} \right) = \frac{1}{2} C V^2$$

Ramping an inductor from $0\text{ A}$ at time zero to final current $I$ at time $t_1$ pushes against Faraday counter-voltage $L\,\frac{di(t)}{dt}$ across an average current of $\frac{1}{2}I$. Changing variables via $di$ for $\frac{di(t)}{dt}\,dt$ and integrating $i\,di$ from $0$ to $I$ yield **magnetic field energy stored per meter of trace** (for distributed $L$ in $\text{H/m}$):

$$di = \frac{di(t)}{dt}\,dt, \qquad w_B = \int_{t=0}^{t=t_1} \left( L\,\frac{di(t)}{dt} \right) i(t)\,dt = L \int_{i=0}^{i=I} i\,di = L \left[ \frac{i^2}{2} \right]_{i=0}^{i=I} = \frac{1}{2} L I^2$$

#### Wave Energy Parity and Overlap-Zone Quadrupling

In any single traveling wave ($V_{\text{inc}}, I_{\text{inc}}$) on a lossless trace of characteristic impedance $Z_0$, wave current is locked to wave voltage through $\sqrt{\frac{C}{L}}$:

$$Z_0 = \sqrt{\frac{L}{C}}, \qquad I_{\text{inc}} = \frac{V_{\text{inc}}}{Z_0} = V_{\text{inc}}\sqrt{\frac{C}{L}}$$

Substitution of $I_{\text{inc}}$ into magnetic energy density $w_{B,\text{inc}}$ proves **50/50 wave energy parity**, showing that every single traveling electromagnetic wave carries equal magnetic and electric energy per meter:

$$w_{B,\text{inc}} = \frac{1}{2} L I_{\text{inc}}^2 = \frac{1}{2} L \left( V_{\text{inc}} \sqrt{\frac{C}{L}} \right)^2 = \frac{1}{2} L \left( V_{\text{inc}}^2\,\frac{C}{L} \right) = \frac{1}{2} C V_{\text{inc}}^2 = w_{E,\text{inc}}$$

Let $w_0$ denote one share of field energy per meter:

$$w_0 = \frac{1}{2} C V_{\text{inc}}^2 = \frac{1}{2} L I_{\text{inc}}^2$$

Each traveling wave carries **two shares of energy per meter** ($1\,w_0$ electric plus $1\,w_0$ magnetic, totaling $2\,w_0$). At an open or short circuit where $100\%$ of the wave reflects (unit $|\Gamma|$), the incident wave ($2\,w_0$) and reflected wave ($2\,w_0$) coexist inside the overlap zone, so energy conservation requires each meter of the overlap zone to hold **four shares of energy** ($4\,w_0$). Field energy scales with $V^2$ and $I^2$, so doubling the surviving field at an open or short circuit **quadruples** ($4\times$) its energy density to hold all four shares.

At an **open circuit** ($2 V_{\text{inc}}$ total voltage and $0\text{ A}$ total current), all four shares ($2\,w_0$ originally electric plus $2\,w_0$ converted from the collapsed magnetic field) reside in the doubled electric field:

$$w_{E,\text{total}} = \frac{1}{2} C (2 V_{\text{inc}})^2 = 4 \left( \frac{1}{2} C V_{\text{inc}}^2 \right) = 4\,w_0, \qquad w_{B,\text{total}} = 0 \qquad \Longrightarrow \qquad w_{\text{total}} = 4\,w_0$$

At a **short circuit** ($0\text{ V}$ total voltage and $2 I_{\text{inc}}$ total current), all four shares ($2\,w_0$ originally magnetic plus $2\,w_0$ converted from the collapsed electric field) reside in the doubled magnetic field:

$$w_{B,\text{total}} = \frac{1}{2} L (2 I_{\text{inc}})^2 = 4 \left( \frac{1}{2} L I_{\text{inc}}^2 \right) = 4\,w_0, \qquad w_{E,\text{total}} = 0 \qquad \Longrightarrow \qquad w_{\text{total}} = 4\,w_0$$

#### Summary of the Five Canonical Boundary Regimes

Five canonical passive load regimes govern boundary wave reflection, transmission, and field energy partitioning at coordinate $\ell$:

| Boundary Regime | Load ($Z_L$) | $\Gamma$ and $T_V$ | Boundary Voltage and Current | Power Balance |
|---|---|---|---|---|
| **Matched load** | $Z_L = Z_0$ | $\Gamma = 0$, $T_V = 1$ | $V_{\text{total}} = V_{\text{inc}}$, $I_{\text{total}} = I_{\text{inc}}$ | $100\%$ absorbed ($P_{\text{ref}} = 0$) |
| **Step-down** | $0 < Z_L < Z_0$ | $-1 < \Gamma < 0$, $0 < T_V < 1$ | $V_{\text{total}} < V_{\text{inc}}$, $I_{\text{total}} > I_{\text{inc}}$ | $\Gamma^2$ reflected, $1 - \Gamma^2$ transmitted |
| **Step-up** | $Z_0 < Z_L < \infty$ | $0 < \Gamma < +1$, $1 < T_V < 2$ | $V_{\text{total}} > V_{\text{inc}}$, $I_{\text{total}} < I_{\text{inc}}$ | $\Gamma^2$ reflected, $1 - \Gamma^2$ transmitted |
| **Open circuit** | $Z_L \to \infty$ | $\Gamma = +1$, $T_V = 2$ | $V_{\text{total}} = 2 V_{\text{inc}}$, $I_{\text{total}} = 0$ | $100\%$ reflected ($E$-field energy $4\times$) |
| **Short circuit** | $Z_L = 0$ | $\Gamma = -1$, $T_V = 0$ | $V_{\text{total}} = 0\text{ V}$, $I_{\text{total}} = 2 I_{\text{inc}}$ | $100\%$ reflected ($B$-field energy $4\times$) |

### Impedance as a Property of the Medium

Electromagnetic waves do not carry an intrinsic impedance of their own; characteristic impedance is strictly a geometric property of the copper cross-section and surrounding dielectric medium. A $50\,\Omega$ trace forces any single wave propagating along it to maintain a voltage-to-current magnitude ratio of $50\,\Omega$.

At a localized defect (such as a capacitive pad or inductive via), the defect's reflection coefficient $\Gamma$ sets the initial reflected voltage amplitude $V_{\text{ref}}$ rejected backward onto the $50\,\Omega$ trace. Stepping back onto the $50\,\Omega$ trace immediately locks reflected current $I_{\text{ref}}$ to the $50\,\Omega$ line geometry:

$$V_{\text{ref}} = \Gamma\,V_{\text{inc}}, \qquad I_{\text{ref}} = -\frac{V_{\text{ref}}}{50\,\Omega}$$

Consider a $1.0\text{ V}$ forward wave ($20\text{ mA}$ incident current $I_{\text{inc}}$ and $20\text{ mW}$ incident power $P_{\text{inc}}$) on a $50\,\Omega$ trace striking a discontinuity with $\Gamma$ of $+0.10$, launching a $+0.10\text{ V}$ reflected wave $V_{\text{ref}}$. The $50\,\Omega$ trace locks reflected current and reflected power fraction to:

$$I_{\text{ref}} = -\frac{0.10\text{ V}}{50\,\Omega} = -2.0\text{ mA}, \qquad \frac{P_{\text{ref}}}{P_{\text{inc}}} = \Gamma^2 = (0.10)^2 = 0.01 \quad (1\%, \text{ or } 0.20\text{ mW})$$

## Architecture

### The Reflection as a Separate Electromagnetic Wave

A reflected wave is a complete, backward-traveling electromagnetic wave with its own moving displacement-current wavefront, completely distinct from the ground-plane return current of the forward wave. [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) established that the forward wave already closes its own clockwise current loop at every instant (rightward conduction current on the trace, downward displacement current at the forward wavefront, and leftward return current on the ground plane).

Arrival of the forward wavefront at an impedance discontinuity at coordinate $\ell$ launches a new electromagnetic wavefront propagating leftward ($-z$) through the dielectric at velocity $v_p$. Linearity of Maxwell's equations in the dielectric guarantees superposition, so the forward wave and reflected wave coexist on the trace wherever the reflected wavefront has passed, adding their voltages and currents algebraically at every coordinate $z$.

### What a Meter Sees: Total Voltage and Current with a Reflection

An oscilloscope probe or current sensor placed on the trace measures the local superposition of whichever waves have reached that coordinate. Upstream of the leftward-moving reflected wavefront (ahead of $z_{\text{ref}}$), the reflection has not yet arrived and the trace sits in the single forward-wave state $V_{\text{inc}}$ and $I_{\text{inc}}$.

Inside the overlap zone between $z_{\text{ref}}$ and $\ell$, both the forward wave and leftward reflected wave coexist simultaneously and obey the single-wave relations on the $Z_0$ line:

$$V_{\text{ref}} = \Gamma\,V_{\text{inc}}, \qquad I_{\text{inc}} = +\frac{V_{\text{inc}}}{Z_0}, \qquad I_{\text{ref}} = -\frac{V_{\text{ref}}}{Z_0}$$

Summing the two waves gives total voltage $V_{\text{total}}$ and total rightward current $I_{\text{total}}$ across the overlap zone:

$$V_{\text{total}} = V_{\text{inc}} + V_{\text{ref}} = V_{\text{inc}}(1 + \Gamma), \qquad I_{\text{total}} = I_{\text{inc}} + I_{\text{ref}} = \frac{V_{\text{inc}}}{Z_0}(1 - \Gamma)$$

Division of $V_{\text{total}}$ by $I_{\text{total}}$ cancels $V_{\text{inc}}$ and recovers the bilinear impedance expression for $Z_L$ derived earlier:

$$\frac{V_{\text{total}}}{I_{\text{total}}} = Z_0\,\frac{1 + \Gamma}{1 - \Gamma} = Z_L$$

Measured ratio $\frac{V_{\text{total}}}{I_{\text{total}}}$ equals $Z_0$ solely for zero $\Gamma$ (a single forward wave with no reflection). Superposition of a reflected wave onto the forward wave leaves each individual wave obeying magnitude ratio $Z_0$ on the trace, yet forces total voltage divided by total current to equal $Z_L$.

### The Launched Wave and the Driver Source Resistance

A physical CMOS transmitter is not an ideal zero-ohm voltage switch. Inside the transmitter chip, the conducting pull-up transistor channel carries an internal **source resistance** $R_S$ (typically $10\,\Omega$ to $30\,\Omega$ in uncalibrated logic, or $50\,\Omega$ in source-terminated SerDes drivers) wired in series between the on-chip DC power supply $V_S$ and the PCB trace launch pin at coordinate $0$.

At time zero, before any wave reaches the far end of the board, the uncharged transmission line presents characteristic impedance $Z_0$ at the launch pin. Closing the transistor switch sends current from supply rail $V_S$ through source resistor $R_S$ into line entrance $Z_0$ along a single unbranched path, where series impedances add and divide the supply voltage in proportion to impedance:

$$Z_{\text{series}} = Z_1 + Z_2, \qquad V_{\text{out}} = V_{\text{in}}\,\frac{Z_2}{Z_1 + Z_2}$$

Substituting $R_S$ for $Z_1$, $Z_0$ for $Z_2$, and $V_S$ for $V_{\text{in}}$ gives initial launched current $I_1$ and initial forward wave voltage $V_1$:

$$Z_{\text{series}} = R_S + Z_0, \qquad I_1 = \frac{V_S}{R_S + Z_0}, \qquad V_1 = I_1 Z_0 = V_S\,\frac{Z_0}{R_S + Z_0}$$

In [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md), the transmitter was modeled as an idealized $0\,\Omega$ switch $R_S$ connected to a $1.2\text{ V}$ supply $V_S$ driving a $50\,\Omega$ trace $Z_0$, stepping the full $1.2\text{ V}$ onto the trace and drawing $24\text{ mA}$:

$$I_{\text{ideal}} = \frac{V_S}{0\,\Omega + Z_0} = \frac{1.2\text{ V}}{50\,\Omega} = 24\text{ mA}$$

A real CMOS driver with a $10\,\Omega$ internal resistance $R_S$ connecting that same $1.2\text{ V}$ supply $V_S$ to the $50\,\Omega$ trace $Z_0$ raises total launch series resistance $R_S + Z_0$ from $50\,\Omega$ to $60\,\Omega$, reducing launched current $I_1$ to $20\text{ mA}$:

$$I_1 = \frac{V_S}{R_S + Z_0} = \frac{1.2\text{ V}}{10\,\Omega + 50\,\Omega} = \frac{1.2\text{ V}}{60\,\Omega} = 20\text{ mA}$$

Passing $20\text{ mA}$ through the internal $10\,\Omega$ channel drops $0.2\text{ V}$ ($I_1 R_S$) inside the driver chip, leaving an initial $1.0\text{ V}$ forward wave $V_1$ launched onto the trace:

$$V_1 = V_S\,\frac{Z_0}{R_S + Z_0} = 1.2\text{ V} \cdot \frac{50\,\Omega}{10\,\Omega + 50\,\Omega} = 1.0\text{ V}$$

At round-trip time $2 t_{pd}$, any reflected wave returning leftward to coordinate $0$ encounters internal driver resistance $R_S$ tied to the constant $1.2\text{ V}$ DC supply rail $V_S$. An ideal DC voltage source holds fixed potential $V_S$ with $0\,\Omega$ dynamic opposition to current changes, so the returning wave sees a boundary impedance of $R_S$ alone. Recalling the voltage reflection coefficient and substituting $R_S$ for $Z_L$ define the **source reflection coefficient** $\Gamma_S$:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

$$\Gamma_S = \frac{R_S - Z_0}{R_S + Z_0} = \frac{10\,\Omega - 50\,\Omega}{10\,\Omega + 50\,\Omega} = \frac{-40\,\Omega}{60\,\Omega} = -\frac{2}{3}$$

For a $10\,\Omega$ driver $R_S$ on a $50\,\Omega$ line $Z_0$, the low-impedance transmitter reflects two-thirds of any returning wave back toward the receiver with inverted polarity.

### Ping-Pong Reflections and Multi-Bounce Lattice Settling

In a lumped DC circuit with zero propagation delay, connecting a driver of source resistance $R_S$ to a receiver of load resistance $R_L$ establishes steady-state DC voltage immediately. On a physical PCB trace of one-way propagation delay $t_{pd}$, **the driver at coordinate $0$ and the receiver at coordinate $\ell$ cannot see each other instantaneously**. At time zero, the driver sees only $Z_0$, and at first arrival time $t_{pd}$, the wave reaching the receiver has no direct connection to $R_S$.

Two resistors separated by a transmission line with non-zero $\Gamma_S$ and non-zero $\Gamma_L$ discover each other's values and reach equilibrium by **bouncing reflection echoes back and forth across the line** in a **ping-pong** sequence.

#### Bounce Multiplication Versus Load Transmission Steps

Calculating voltage at each stage of a ping-pong sequence requires distinguishing between the wave bouncing back onto the trace and the total voltage step sensed across the load. Only the *reflected* portion of an arriving wave reverses direction to travel back across the channel: each load bounce multiplies the traveling wave by $\Gamma_L$, and each source bounce multiplies the returning wave by $\Gamma_S$. One complete round trip from load to source and back to load (duration $2 t_{pd}$) multiplies the next arriving wave by the **round-trip bounce factor** $\Gamma_S \Gamma_L$.

A receiver comparator or oscilloscope probe at coordinate $\ell$, by contrast, does not measure the reflected wave in isolation; it senses the *total transmitted voltage* formed by adding the arriving forward wave and the newly generated load reflection. Finding the voltage increment $\Delta V_L$ added to the receiver on any arrival applies the load's **voltage transmission coefficient** $T_{V,L}$:

$$T_{V,L} = 1 + \Gamma_L, \qquad \Delta V_L = T_{V,L}\,V_{\text{arriving}} = (1 + \Gamma_L)\,V_{\text{arriving}}$$

#### Step-by-Step Round-Trip Wave Tracking

Applying bounce multiplication and load transmission across successive propagation delays $t_{pd}$ traces the full multi-bounce trajectory. At **initial launch** (time zero at coordinate $0$), the driver launches the first forward wave $V_1$ onto the trace:

$$V_{\text{forward},1} = V_1 = V_S\,\frac{Z_0}{R_S + Z_0}$$

At **first load arrival** (time $t_{pd}$ at coordinate $\ell$), forward wave $V_1$ strikes load $R_L$. Multiplication by $T_{V,L}$ gives the first receiver voltage step $V_L(t_{pd})$, and multiplication by $\Gamma_L$ launches the first leftward reflection $V_{\text{backward},1}$ toward the driver:

$$V_L(t_{pd}) = (1 + \Gamma_L)\,V_1, \qquad V_{\text{backward},1} = \Gamma_L\,V_1$$

At **first source re-reflection** (time $2 t_{pd}$ at coordinate $0$), leftward wave $V_{\text{backward},1}$ reaches the driver and reflects off $R_S$, multiplying by $\Gamma_S$ to launch a second forward wave $V_{\text{forward},2}$ toward the receiver:

$$V_{\text{forward},2} = \Gamma_S\,V_{\text{backward},1} = (\Gamma_S \Gamma_L)\,V_1$$

At **second load arrival** (time $3 t_{pd}$ at coordinate $\ell$), forward wave $V_{\text{forward},2}$ strikes $R_L$ and multiplies by $T_{V,L}$ to add a second voltage increment $\Delta V_{L,2}$ on top of $V_L(t_{pd})$:

$$\Delta V_{L,2} = (1 + \Gamma_L)\,V_{\text{forward},2} = (1 + \Gamma_L)(\Gamma_S \Gamma_L)\,V_1$$

$$V_L(3 t_{pd}) = V_L(t_{pd}) + \Delta V_{L,2} = (1 + \Gamma_L)\,V_1 + (1 + \Gamma_L)(\Gamma_S \Gamma_L)\,V_1$$

Each subsequent round trip of duration $2 t_{pd}$ multiplies the previous voltage increment by another factor of $\Gamma_S \Gamma_L$. At every resistive bounce, the resistor absorbs power fraction $1 - \Gamma^2$ as heat, shrinking successive wave increments toward zero.

### Settling to the Steady-State DC Voltage Divider

Summing all load voltage increments across odd arrival multiples $t_{pd}, 3 t_{pd}, 5 t_{pd}, \dots$ in the steady-state limit gives final load voltage $V_{\text{final}}$. Factoring the common initial step $(1 + \Gamma_L)\,V_1$ out of every arrival leaves an infinite geometric series in powers of the round-trip ratio $r$ (defined as $\Gamma_S \Gamma_L$):

$$V_{\text{final}} = (1 + \Gamma_L)\,V_1 \left[ 1 + (\Gamma_S \Gamma_L) + (\Gamma_S \Gamma_L)^2 + (\Gamma_S \Gamma_L)^3 + \cdots \right]$$

For any positive resistances $R_S$ and $R_L$, both reflection coefficients have magnitude strictly below $1$, keeping $|r|$ strictly below $1$. Closed-form summation of the geometric series expresses $V_{\text{final}}$ in terms of the **wave variables** $V_1$, $\Gamma_L$, and $\Gamma_S$:

$$r = \Gamma_S \Gamma_L, \qquad 1 + r + r^2 + r^3 + \cdots = \frac{1}{1 - r} \qquad \Longrightarrow \qquad V_{\text{final}} = \frac{V_1(1 + \Gamma_L)}{1 - \Gamma_S \Gamma_L}$$

Parameters $V_1$, $\Gamma_L$, and $\Gamma_S$ inside that wave-domain sum all depend implicitly on trace impedance $Z_0$. Replacing each wave parameter with its circuit-impedance definition reveals how $R_S$ and $R_L$ govern final DC voltage and how $Z_0$ cancels out once reflections subside.

First, recall the launch voltage divider for $V_1$ and the load transmission expression for $1 + \Gamma_L$:

$$V_1 = V_S\,\frac{Z_0}{R_S + Z_0}, \qquad 1 + \Gamma_L = T_{V,L} = \frac{2 R_L}{R_L + Z_0}$$

Second, recall the source and load reflection definitions and place $1 - \Gamma_S \Gamma_L$ over the common denominator $(R_S + Z_0)(R_L + Z_0)$:

$$\Gamma_S = \frac{R_S - Z_0}{R_S + Z_0}, \qquad \Gamma_L = \frac{R_L - Z_0}{R_L + Z_0}$$

$$1 - \Gamma_S \Gamma_L = 1 - \left( \frac{R_S - Z_0}{R_S + Z_0} \right) \left( \frac{R_L - Z_0}{R_L + Z_0} \right) = \frac{(R_S + Z_0)(R_L + Z_0) - (R_S - Z_0)(R_L - Z_0)}{(R_S + Z_0)(R_L + Z_0)}$$

Expansion of both parenthesized products in the numerator cancels the $R_S R_L$ and $Z_0^2$ terms:

$$(R_S R_L + Z_0 R_S + Z_0 R_L + Z_0^2) - (R_S R_L - Z_0 R_S - Z_0 R_L + Z_0^2) = 2 Z_0 (R_S + R_L)$$

$$1 - \Gamma_S \Gamma_L = \frac{2 Z_0 (R_S + R_L)}{(R_S + Z_0)(R_L + Z_0)}$$

Third, multiplying $V_1$ by $1 + \Gamma_L$ and dividing by $1 - \Gamma_S \Gamma_L$ (multiplying by its reciprocal) cancels $(R_S + Z_0)$, $(R_L + Z_0)$, and $2 Z_0$ completely:

$$V_{\text{final}} = \left( V_S\,\frac{Z_0}{R_S + Z_0} \right) \left( \frac{2 R_L}{R_L + Z_0} \right) \left( \frac{(R_S + Z_0)(R_L + Z_0)}{2 Z_0 (R_S + R_L)} \right) = V_S\,\frac{R_L}{R_S + R_L}$$

Every factor containing trace impedance $Z_0$ cancels out of the steady-state voltage, leaving the elementary DC voltage divider between $R_S$ and $R_L$. Characteristic impedance $Z_0$ governs the transient wave trajectory across the picoseconds and nanoseconds required to reach equilibrium, whereas $R_S$ and $R_L$ govern the final DC state after all reflections die out.

### Termination Strategies

Multi-bounce ringing occurs solely when both ends of the link reflect (non-zero $\Gamma_S \Gamma_L$). Eliminating multi-bounce ringing forces the round-trip bounce product $\Gamma_S \Gamma_L$ to zero by matching either source impedance (zero $\Gamma_S$) or load impedance (zero $\Gamma_L$).

#### Series (Source) Termination

**Series termination** places a resistor $R_T$ in series with the driver output so total source resistance matches $Z_0$, while the far-end CMOS receiver gate remains an open circuit:

$$R_S + R_T = Z_0, \qquad \Gamma_S = 0, \qquad \Gamma_L = +1, \qquad T_{V,L} = 2$$

At time zero, the equal-value divider between $R_S + R_T$ and trace impedance $Z_0$ launches a half-amplitude forward wave $V_1$ onto the line:

$$V_1 = V_S\,\frac{Z_0}{Z_0 + Z_0} = \frac{V_S}{2}$$

At one-way delay $t_{pd}$, that half-amplitude wave strikes the open-circuit receiver and doubles on arrival, stepping the receiver cleanly to the full supply rail $V_S$ in a single transition:

$$V_L(t_{pd}) = (1 + \Gamma_L)\,V_1 = 2 \left( \frac{V_S}{2} \right) = V_S$$

The reflected $+\frac{V_S}{2}$ wave returns to the transmitter at $2 t_{pd}$, where the matched source impedance absorbs $100\%$ of the returning wave with zero re-reflection and zero steady-state DC current. Mid-span points along the trace sit at $\frac{V_S}{2}$ until the returning reflection passes back over them, restricting series termination to point-to-point links where only the far-end receiver samples the signal.

#### Parallel (Far-End) Termination and On-Die Termination

**Parallel termination** wires a resistor $R_T$ equal to $Z_0$ from the receiver input to ground (or a termination rail), matching the load directly to the trace:

$$R_L = R_T = Z_0, \qquad \Gamma_L = 0, \qquad T_{V,L} = 1$$

The arriving forward wave $V_1$ is $100\%$ absorbed at the receiver upon first arrival at $t_{pd}$ with zero reflection regardless of $\Gamma_S$, delivering a clean single step at every coordinate along the trace. Sustaining a steady high logic level draws continuous DC current $I_{\text{DC}}$ through $R_S$ and $Z_0$ in series:

$$I_{\text{DC}} = \frac{V_S}{R_S + Z_0}$$

High-speed SerDes receivers integrate that parallel resistor directly onto the silicon die as **On-Die Termination (ODT)** so the arriving wave never encounters an unterminated package-pin stub.

## Worked Examples

### A 75 Ω Section on a 50 Ω Line

Consider a $1.0\text{ V}$ incident forward wave $V_{\text{inc}}$ on a $50\,\Omega$ trace $Z_0$ ($20\text{ mA}$ incident current $I_{\text{inc}}$ and $20\text{ mW}$ incident power $P_{\text{inc}}$) striking a boundary with a $75\,\Omega$ trace $Z_L$.

Evaluating voltage reflection coefficient $\Gamma$ and voltage transmission coefficient $T_V$ across the step-up boundary from $50\,\Omega$ to $75\,\Omega$ gives the reflected and transmitted voltages:

$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0} = \frac{75\,\Omega - 50\,\Omega}{75\,\Omega + 50\,\Omega} = \frac{25\,\Omega}{125\,\Omega} = +0.20, \qquad T_V = 1 + \Gamma = 1.20$$

$$V_{\text{ref}} = \Gamma\,V_{\text{inc}} = +0.20\text{ V}, \qquad V_{\text{trans}} = T_V\,V_{\text{inc}} = 1.20\text{ V}$$

Each individual wave obeys the characteristic impedance of the trace section it occupies, with positive current for rightward ($+z$) propagation and negative current for leftward ($-z$) reflection:

$$\begin{aligned}
I_{\text{inc}} &= +\frac{V_{\text{inc}}}{Z_0} = \frac{1.0\text{ V}}{50\,\Omega} = +20\text{ mA}, & I_{\text{ref}} &= -\frac{V_{\text{ref}}}{Z_0} = -\frac{0.20\text{ V}}{50\,\Omega} = -4\text{ mA} \\
I_{\text{trans}} &= +\frac{V_{\text{trans}}}{Z_L} = \frac{1.20\text{ V}}{75\,\Omega} = +16\text{ mA}
\end{aligned}$$

$$I_{\text{inc}} + I_{\text{ref}} = 20\text{ mA} - 4\text{ mA} = 16\text{ mA} = I_{\text{trans}}$$

Evaluating reflected power $P_{\text{ref}}$ and transmitted power $P_{\text{trans}}$ confirms that $100\%$ of the $20\text{ mW}$ incident power is conserved and that the total voltage-to-current ratio equals $Z_L$:

$$P_{\text{ref}} = \Gamma^2\,P_{\text{inc}} = (0.20)^2 (20\text{ mW}) = 0.80\text{ mW} \quad (4\%), \qquad P_{\text{trans}} = \frac{V_{\text{trans}}^2}{Z_L} = \frac{(1.20\text{ V})^2}{75\,\Omega} = 19.20\text{ mW} \quad (96\%)$$

$$\frac{V_{\text{total}}}{I_{\text{total}}} = \frac{1.20\text{ V}}{0.016\text{ A}} = 75\,\Omega = Z_L$$

### An Open Receiver Behind a 10 Ω Driver

Consider a $1.2\text{ V}$ transmitter supply $V_S$ with $10\,\Omega$ source resistance $R_S$ launching into an unterminated $50\,\Omega$ trace $Z_0$ connected to an open-circuit CMOS receiver gate (infinite $R_L$). Recalling the launch voltage divider and source/load reflection equations and substituting the hardware values yield the initial wave and boundary coefficients:

$$V_1 = V_S\,\frac{Z_0}{R_S + Z_0} = 1.2\text{ V} \cdot \frac{50\,\Omega}{10\,\Omega + 50\,\Omega} = 1.0\text{ V}$$

$$\Gamma_S = \frac{R_S - Z_0}{R_S + Z_0} = \frac{10\,\Omega - 50\,\Omega}{10\,\Omega + 50\,\Omega} = -\frac{2}{3}, \qquad \Gamma_L = +1, \qquad T_{V,L} = 1 + \Gamma_L = 2$$

On round-trip index $k$ ($0, 1, 2, \dots$), arriving at odd delay multiple $(2k + 1)\,t_{pd}$, forward wave $V_{\text{forward},k+1}$ adds transmitted voltage increment $\Delta V_{L,k+1}$ at the open receiver:

$$V_{\text{forward},k+1} = (\Gamma_S \Gamma_L)^k\,V_1, \qquad \Delta V_{L,k+1} = T_{V,L}\,V_{\text{forward},k+1} = 2 V_1 (\Gamma_S \Gamma_L)^k$$

Evaluating cumulative receiver voltage across the first five arrivals produces an alternating overshoot-and-undershoot sequence:

$$V_L(t_{pd}) = 2(1.0\text{ V}) = 2.000\text{ V}$$

$$V_L(3 t_{pd}) = 2.000\text{ V} + 2(1.0\text{ V})\left(-\frac{2}{3}\right) = 0.667\text{ V}$$

$$V_L(5 t_{pd}) = 0.667\text{ V} + 2(1.0\text{ V})\left(-\frac{2}{3}\right)^2 = 1.556\text{ V}$$

$$V_L(7 t_{pd}) = 1.556\text{ V} + 2(1.0\text{ V})\left(-\frac{2}{3}\right)^3 = 0.963\text{ V}$$

$$V_L(9 t_{pd}) = 0.963\text{ V} + 2(1.0\text{ V})\left(-\frac{2}{3}\right)^4 = 1.358\text{ V}$$

Each odd multiple of $t_{pd}$ marks a distinct step toward the $1.2\text{ V}$ rail:

1. **First arrival ($t_{pd}$, bounce $0$):** The open-circuit boundary doubles the $1.0\text{ V}$ incident wave and steps the receiver to $2.000\text{ V}$ ($+0.800\text{ V}$ overshoot above the $1.2\text{ V}$ rail).
2. **Second arrival ($3 t_{pd}$, bounce $1$):** The first round-trip reflection scales the step by $-\frac{2}{3}$ and pulls the receiver down to $0.667\text{ V}$ ($-0.533\text{ V}$ undershoot below $1.2\text{ V}$).
3. **Third arrival ($5 t_{pd}$, bounce $2$):** The second round-trip reflection pushes the receiver back up to $1.556\text{ V}$ ($+0.356\text{ V}$ overshoot).
4. **Fourth arrival ($7 t_{pd}$, bounce $3$):** The third round-trip reflection pulls the receiver down to $0.963\text{ V}$ ($-0.237\text{ V}$ undershoot).
5. **Fifth arrival ($9 t_{pd}$, bounce $4$):** The fourth round-trip reflection brings the receiver to $1.358\text{ V}$ ($+0.158\text{ V}$ overshoot).

Receiver voltage rings around the $1.2\text{ V}$ steady-state DC open-circuit value $V_{\text{final}}$ with an oscillation period of $4 t_{pd}$ (two round trips per full cycle), shrinking in error magnitude by $\frac{2}{3}$ ($|\Gamma_S \Gamma_L|$) on every bounce. Adding a $40\,\Omega$ series termination resistor $R_T$ at the driver matches total source resistance to $50\,\Omega$, zeroing $\Gamma_S$:

$$R_S + R_T = 10\,\Omega + 40\,\Omega = 50\,\Omega = Z_0, \qquad \Gamma_S = 0, \qquad V_1 = 0.6\text{ V}, \qquad V_L(t_{pd}) = 1.2\text{ V}$$

That $0.6\text{ V}$ half-amplitude launch doubles cleanly to $1.2\text{ V}$ at the open receiver at $t_{pd}$, and the matched driver absorbs the returning $+0.6\text{ V}$ reflection completely at $2 t_{pd}$.

### Reactive Discontinuities on a 50 Ω Line

A localized parasitic structure embedded along the middle of a $50\,\Omega$ trace $Z_0$ sits immediately ahead of the remaining downstream $50\,\Omega$ trace. Finding the reflection from that mid-trace defect combines the defect's complex impedance ($Z_C(\omega)$ or $Z_{\text{ind}}(\omega)$) with the downstream $Z_0$ continuation to form effective input impedance $Z_{\text{in}}(\omega)$, then substitutes $Z_{\text{in}}(\omega)$ into $\Gamma(\omega)$:

$$Z_C(\omega) = \frac{1}{j\omega C}, \qquad Z_{\text{ind}}(\omega) = j\omega L, \qquad \Gamma(\omega) = \frac{Z_{\text{in}}(\omega) - Z_0}{Z_{\text{in}}(\omega) + Z_0}$$

#### Shunt Capacitive Pad in Parallel with the Downstream Trace

A wide component pad adds excess shunt capacitance $C$ from the trace to the underlying ground plane. Arriving current at the pad node splits into two side-by-side paths (part charging pad impedance $Z_C(\omega)$ to ground and part entering the downstream $Z_0$ trace), so the pad and downstream line share the identical node voltage and combine in parallel:

$$Z_{\text{parallel}} = \frac{Z_1 Z_2}{Z_1 + Z_2}$$

Defining normalized susceptance $x$ and substituting $Z_0$ and $Z_C(\omega)$ give $Z_{\text{in}}(\omega)$:

$$x = \omega C Z_0 = 2\pi f C Z_0, \qquad Z_{\text{in}}(\omega) = \frac{Z_0\,Z_C(\omega)}{Z_0 + Z_C(\omega)} = \frac{Z_0 \cdot \dfrac{1}{j\omega C}}{Z_0 + \dfrac{1}{j\omega C}} = \frac{Z_0}{1 + j\omega C Z_0} = \frac{Z_0}{1 + jx}$$

Substitution of $Z_{\text{in}}(\omega)$ into $\Gamma(\omega)$ and multiplication of numerator and denominator by $1 + jx$ yield the complex reflection coefficient and its Pythagorean magnitude $|\Gamma(\omega)|$:

$$\Gamma(\omega) = \frac{Z_{\text{in}}(\omega) - Z_0}{Z_{\text{in}}(\omega) + Z_0} = \frac{\dfrac{Z_0}{1 + jx} - Z_0}{\dfrac{Z_0}{1 + jx} + Z_0} = \frac{1 - (1 + jx)}{1 + (1 + jx)} = \frac{-jx}{2 + jx}$$

$$|\Gamma(\omega)| = \frac{x}{\sqrt{4 + x^2}}$$

For a $0.5\text{ pF}$ pad $C$ on a $50\,\Omega$ line $Z_0$, normalized susceptance $x$ equals $0.157$ at $1\text{ GHz}$, $0.785$ at $5\text{ GHz}$, and $1.571$ at $10\text{ GHz}$. Those susceptances produce reflection magnitudes $|\Gamma(\omega)|$ of $0.078$ ($0.6\%$ reflected power from $\Gamma^2$) at $1\text{ GHz}$, $0.366$ ($13.4\%$ reflected power) at $5\text{ GHz}$, and $0.618$ ($38.2\%$ reflected power) at $10\text{ GHz}$.

#### Series Inductive Bondwire or Neck Ahead of the Downstream Trace

A bondwire or narrow trace neck inserts excess inductance $L$ inline along the single conductor path ahead of the downstream $Z_0$ trace. Every electron passes through $L$ before entering the downstream $Z_0$ trace, so the inductor and downstream line carry identical current and add in series:

$$Z_{\text{ind}}(\omega) = j\omega L, \qquad Z_{\text{in}}(\omega) = Z_0 + Z_{\text{ind}}(\omega) = Z_0 + j\omega L$$

Substitution of $Z_{\text{in}}(\omega)$ into $\Gamma(\omega)$ yields the inductive reflection coefficient and its Pythagorean magnitude $|\Gamma(\omega)|$:

$$\Gamma(\omega) = \frac{(Z_0 + j\omega L) - Z_0}{(Z_0 + j\omega L) + Z_0} = \frac{j\omega L}{2 Z_0 + j\omega L}, \qquad |\Gamma(\omega)| = \frac{\omega L}{\sqrt{4 Z_0^2 + (\omega L)^2}}$$

For a $1.0\text{ nH}$ discontinuity $L$ on a $50\,\Omega$ line, inductive reactance $\omega L$ equals $6.28\,\Omega$ at $1\text{ GHz}$, $31.4\,\Omega$ at $5\text{ GHz}$, and $62.8\,\Omega$ at $10\text{ GHz}$. Those reactances produce reflection magnitudes $|\Gamma(\omega)|$ of $0.063$ ($0.4\%$ reflected power) at $1\text{ GHz}$, $0.300$ ($9.0\%$ reflected power) at $5\text{ GHz}$, and $0.532$ ($28.3\%$ reflected power) at $10\text{ GHz}$. Both reactive reflections scale linearly with frequency at low frequencies, explaining why fast edges rich in multi-gigahertz harmonics ([Chapter 2](02_Frequency_Content_of_Digital_Signals.md)) suffer far larger reflections from vias and pads than slow edges.

## Edge Cases

### Inductance and Capacitance That Cancel

Every millimeter of a uniform trace contains distributed inductance $L$ and distributed capacitance $C$ in the fixed ratio $Z_0^2$. A localized transition that adds excess inductance $\Delta L$ and excess capacitance $\Delta C$ in that identical $Z_0^2$ ratio leaves characteristic impedance unchanged:

$$Z = \sqrt{\frac{L + \Delta L}{C + \Delta C}} = \sqrt{\frac{L}{C}} = Z_0 \qquad \text{when} \qquad \frac{\Delta L}{\Delta C} = \frac{L}{C} = Z_0^2$$

A short lumped structure containing excess shunt capacitance $C_{\text{pad}}$ (such as a $0.5\text{ pF}$ connector pad on a $50\,\Omega$ line) can likewise be compensated by placing a narrow, high-inductance trace neck of excess series inductance $L_{\text{neck}}$ right beside the pad:

$$L_{\text{neck}} = Z_0^2\,C_{\text{pad}} = (50\,\Omega)^2 (0.5\text{ pF}) = 1.25\text{ nH}, \qquad f_{\text{cutoff}} = \frac{1}{\pi\sqrt{L_{\text{neck}}\,C_{\text{pad}}}} \approx 12.7\text{ GHz}$$

Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) the lumped critical length $\ell_{\text{critical}}$ for rise time $t_r$:

$$\ell_{\text{critical}} = \frac{v_p t_r}{6}$$

Keeping the physical length of the combined pad-and-neck structure shorter than $\ell_{\text{critical}}$ (operating well below the $12.7\text{ GHz}$ cutoff $f_{\text{cutoff}}$) lets the inductive bump and capacitive dip cancel each other to preserve a matched $50\,\Omega$ launch ([Chapter 6](06_Return_Path_Dynamics_and_Parasitic_Effects.md)).

### Reactive Terminations Reflect All Incident Power

A purely reactive termination $Z_L(\omega)$ (an ideal capacitor or inductor with zero resistance $R$) contains no resistive friction mechanism to dissipate electrical energy as heat. Every Joule of wave energy entering its electric or magnetic field during one quarter-cycle returns to the line during the next, so **a purely reactive load reflects $100\%$ of incident power back toward the source**, altering solely the reflected phase angle:

$$R = 0, \qquad Z_L(\omega) = jX(\omega), \qquad P_{\text{ref}} = P_{\text{inc}}, \qquad |\Gamma(\omega)| = 1$$

Recalling $\Gamma(\omega)$ and substituting $jX(\omega)$ for $Z_L(\omega)$ confirm energy conservation algebraically, because numerator $-Z_0 + jX(\omega)$ and denominator $+Z_0 + jX(\omega)$ share identical Pythagorean magnitudes:

$$\Gamma(\omega) = \frac{Z_L(\omega) - Z_0}{Z_L(\omega) + Z_0}$$

$$|\Gamma(\omega)| = \frac{|jX(\omega) - Z_0|}{|jX(\omega) + Z_0|} = \frac{\sqrt{(-Z_0)^2 + X(\omega)^2}}{\sqrt{(+Z_0)^2 + X(\omega)^2}} = 1$$

Unit reflection magnitude $|\Gamma(\omega)|$ across all frequencies places every purely reactive load on the outer unit-circle boundary of the Smith chart ([Chapter 9](09_Smith_Charts.md)).

#### Capacitive Step Response from Initial Short Circuit to Steady Open Circuit

**A capacitor conducts current on both leads whenever its terminal voltage changes, acting as an open circuit only after its plates finish charging to a constant DC voltage.**

A shunt load capacitor $C$ (such as a receiver's input gate capacitance) connects its upper plate to the trace end at coordinate $\ell$ and its lower plate directly to the $0\text{ V}$ ground plane. Arrival of positive charge $+\Delta Q$ on the upper plate sends an electric field across the thin dielectric gap that **electrostatically repels an equal positive charge $+\Delta Q$ off the lower plate** into the $0\text{ V}$ ground plane. Throughout charging or discharging (non-zero $\frac{dv_C(t)}{dt}$), identical current $i_C(t)$ enters the upper plate from the trace and exits the lower plate into ground without any electrons crossing the insulator:

$$i_C(t) = C\,\frac{dv_C(t)}{dt}$$

That plate-filling mechanism sweeps an initially uncharged shunt capacitor $C$ at the end of a $Z_0$ line from a **short circuit** upon step arrival at time zero to an **open circuit** in the steady-state limit. Prior to step arrival, the plates hold $0\text{ C}$ of charge $Q(0)$. Finite trace current $I$ cannot deposit finite charge $I\,\Delta t$ in zero elapsed time $\Delta t$, so at time zero the empty plates exert **zero electrostatic back-pressure** ($0\text{ V}$ initial potential $v_C(0)$) and conduct unimpeded on both sides like a **$0\text{ V}$ short circuit**:

$$Q(0) = 0\text{ C}, \qquad v_C(0) = 0\text{ V}, \qquad v_{\text{ref}}(0) = -V_{\text{inc}}, \qquad \Gamma(0) = -1$$

For positive time $t$, arriving current pours positive charge onto the upper plate and repels positive charge off the lower plate, building stored charge $Q(t)$ and a rising back-pressure potential $v_C(t)$ that gradually throttles flow on both leads:

$$v_C(t) = \frac{Q(t)}{C}$$

Under a flat $+V_{\text{inc}}$ step wave, plate back-pressure rises until matching the $2 V_{\text{inc}}$ open-circuit trace push ($+2.0\text{ V}$ for a $+1.0\text{ V}$ step) across the dielectric gap above the $0\text{ V}$ ground plate. Charge accumulation stops ($\frac{dQ}{dt}$ reaches zero), halting displacement and conduction on both sides like an **open circuit**:

$$v_C(\infty) = 2 V_{\text{inc}}, \qquad i_C(\infty) = 0\text{ A}, \qquad v_{\text{ref}}(\infty) = +V_{\text{inc}}, \qquad \Gamma(\infty) = +1$$

#### Exponential Charging Waveform and Reflected Step Trajectory

Combining Kirchhoff's boundary continuity laws, the directional wave impedance relations, and the capacitor charging law yields the closed-form time-domain waveforms $v_C(t)$ and $v_{\text{ref}}(t)$. At the capacitor boundary, terminal voltage $v_C(t)$ equals the sum of incident step $V_{\text{inc}}$ and reflected wave $v_{\text{ref}}(t)$:

$$v_C(t) = V_{\text{inc}} + v_{\text{ref}}(t) \qquad \Longrightarrow \qquad v_{\text{ref}}(t) = v_C(t) - V_{\text{inc}}$$

Applying the directional wave current relations on the $Z_0$ line expresses net rightward capacitor current $i_C(t)$ in terms of $V_{\text{inc}}$ and $v_{\text{ref}}(t)$:

$$I_{\text{inc}} = +\frac{V_{\text{inc}}}{Z_0}, \qquad i_{\text{ref}}(t) = -\frac{v_{\text{ref}}(t)}{Z_0}, \qquad i_C(t) = I_{\text{inc}} + i_{\text{ref}}(t) = \frac{V_{\text{inc}} - v_{\text{ref}}(t)}{Z_0}$$

Substitution of $v_C(t) - V_{\text{inc}}$ for $v_{\text{ref}}(t)$ eliminates the reflected wave from the current numerator:

$$i_C(t) = \frac{V_{\text{inc}} - \left( v_C(t) - V_{\text{inc}} \right)}{Z_0} = \frac{2 V_{\text{inc}} - v_C(t)}{Z_0}$$

That relation shows that the $Z_0$ transmission line feeds shunt capacitor $C$ like a Thévenin open-circuit source of $2 V_{\text{inc}}$ driving through series resistance $Z_0$. Equating that line current to the capacitor charging law $C\,\frac{dv_C(t)}{dt}$ and multiplying through by $Z_0$ produce a first-order $RC$ differential equation with time constant $\tau_{RC}$ ($25\text{ ps}$ for a $0.5\text{ pF}$ load $C$ on a $50\,\Omega$ line $Z_0$):

$$\tau_{RC} = Z_0 C, \qquad Z_0 C\,\frac{dv_C(t)}{dt} + v_C(t) = 2 V_{\text{inc}}$$

Starting from $0\text{ V}$ on empty plates at time zero and charging exponentially toward $2 V_{\text{inc}}$ with time constant $Z_0 C$ gives capacitor voltage $v_C(t)$:

$$v_C(t) = 2 V_{\text{inc}}\!\left( 1 - e^{-t/(Z_0 C)} \right)$$

Substituting $v_C(t)$ back into $v_C(t) - V_{\text{inc}}$ gives the reflected wave $v_{\text{ref}}(t)$ and shows the instantaneous reflection ratio sweeping smoothly from $-1$ at time zero ($e^0$ equal to $1$, short circuit) to $+1$ in the steady-state limit ($e^{-\infty}$ equal to $0$, open circuit):

$$v_{\text{ref}}(t) = 2 V_{\text{inc}}\!\left( 1 - e^{-t/(Z_0 C)} \right) - V_{\text{inc}} = V_{\text{inc}}\!\left( 1 - 2 e^{-t/(Z_0 C)} \right)$$

$$\frac{v_{\text{ref}}(t)}{V_{\text{inc}}} = 1 - 2 e^{-t/(Z_0 C)}$$

[Chapter 4](04_Inductance_Magnetic_Coupling_and_Crosstalk.md) derives the physical origin of inductance from Ampère's and Faraday's laws and shows how the magnetic and electric fields of one trace couple into adjacent traces to produce forward and backward crosstalk.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>
