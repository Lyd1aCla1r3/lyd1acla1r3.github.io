# Frequency Content of Digital Signals

<!-- SUMMARY: A digital edge is simultaneously a time-domain transition and a frequency-domain spectrum. Fourier series and step integrals establish the inverse relationship between rise time and knee bandwidth alongside the Nyquist limit, linear channel filtering, aliasing, and the Gibbs phenomenon. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>

[Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) showed that a digital signal is an electromagnetic wavefront launched when a transistor switches a trace between two DC levels, and that the transmitted information lies in the timing of those edges. Every high-speed link depends on the spectral counterpart of that timing: which frequencies reside inside a switching edge, and how much bandwidth must a channel or an instrument provide to preserve it?

A physical puzzle motivates this question. Nothing on a digital board visibly oscillates like a sine wave when a CMOS driver flips from $0\text{ V}$ to $1\text{ V}$, yet specification sheets for PCB laminates, connectors, equalizers, and oscilloscopes are written almost entirely in Hertz. Why does signal integrity decompose square waves and voltage steps into sine waves rather than triangles, ramps, or polynomials?

The answer comes from the physical laws of the transmission line itself. Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) that both the capacitive displacement current $i_C(z, t)$ and the inductive Faraday counter-voltage $v_L(z, t)$ depend on time derivatives:

$$i_C(z, t) = C\,\frac{\partial v(z, t)}{\partial t}, \qquad v_L(z, t) = L\,\frac{\partial i(z, t)}{\partial t}$$

Differentiating almost any geometric shape alters its form completely: the derivative of a parabola ($t^2$) is a linear ramp ($2t$), the derivative of a linear ramp ($t$) is a flat step ($1$), and the derivative of a flat plateau is zero. A square wave or trapezoidal edge launched into a lossy trace cannot hold its shape during propagation, and tracking how an arbitrary curve mutates at every millimeter of copper is mathematically intractable.

A sinusoid is the sole oscillating waveform in nature whose time derivative has the identical waveform shape at the identical frequency $f$:

$$\frac{d}{dt}\sin(2\pi f t) = 2\pi f \cos(2\pi f t) = 2\pi f \sin\!\left(2\pi f t + \frac{\pi}{2}\right)$$

Differentiating a sine wave of frequency $f$ creates no new frequencies; the operation only scales the wave's amplitude by $2\pi f$ and shifts its phase by a quarter cycle ($+\pi/2\text{ rad}$, or $+90^\circ$). In physics, a function that passes through a linear differential equation with its shape unchanged is called an **eigenfunction** (characteristic function) of that system. Maxwell's equations and the Telegrapher's equations are linear differential equations, making pure sinusoids the natural eigenfunctions of every linear transmission line. A pure $5\text{ GHz}$ sine wave entering a lossy PCB trace, via, or connector always emerges at the receiver as a pure $5\text{ GHz}$ sine wave, altered only in amplitude and shifted in phase.

The French physicist Jean-Baptiste Joseph Fourier discovered this principle in 1807 while analyzing a sharp temperature step under the heat diffusion equation, which shares the mathematical form of a lossy $RC$ cable:

$$\frac{\partial u(z, t)}{\partial t} = \alpha\,\frac{\partial^2 u(z, t)}{\partial z^2}$$

Solving that partial differential equation directly for a sharp step was impossible, whereas solving it for a pure sine wave was elementary because the sine wave kept its shape while decaying exponentially. Fourier realized that any physical waveform, including a sharp digital step or square wave, can be expressed as a unique sum of sine and cosine waves. Every linear channel problem then reduces to three steps: decompose the input waveform into sine waves, scale and phase-shift each sine wave across the channel, and sum the modified sine waves at the receiver.

## Core Concepts

### Fourier Analysis as Correlation

On a physical copper trace, all sinusoidal components add together into a single composite voltage $x(t)$ at every instant $t$. Extracting the amplitude and arrival time of one specific frequency from $x(t)$ without contamination from any other frequency relies on time-domain correlation across one period.

#### Starting with the Complete Periodic Equation

Consider a waveform $x(t)$ that repeats with period $T$. Its fundamental frequency $f_0$ and $n$-th harmonic frequency $f_n$ scale inversely with $T$:

$$f_0 = \frac{1}{T}, \qquad f_n = n f_0 = \frac{n}{T}$$

Each harmonic $n$ can have its own peak amplitude $A_n$ (how tall the wave is, in Volts) and its own phase angle $\phi_n$ (when its peak arrives relative to time zero, in radians):

$$x_n(t) = A_n \cos\!\left(\frac{2\pi n t}{T} + \phi_n\right)$$

The unknown phase $\phi_n$ sits inside the cosine argument. Applying the trigonometric angle-addition identity pulls $\phi_n$ out by splitting the shifted wave into an unshifted cosine wave and an unshifted sine wave at the same frequency:

$$\cos(\alpha + \beta) = \cos\alpha\cos\beta - \sin\alpha\sin\beta, \qquad \alpha = \frac{2\pi n t}{T}, \quad \beta = \phi_n$$

$$A_n \cos\!\left(\frac{2\pi n t}{T} + \phi_n\right) = \underbrace{(A_n \cos\phi_n)}_{a_n}\cos\!\left(\frac{2\pi n t}{T}\right) + \underbrace{(-A_n \sin\phi_n)}_{b_n}\sin\!\left(\frac{2\pi n t}{T}\right)$$

Every possible phase shift $\phi_n$ at frequency $f_n$ reduces to a linear combination of two basis waves at that frequency with constant amplitudes $a_n$ and $b_n$:

$$a_n = A_n\cos\phi_n, \qquad b_n = -A_n\sin\phi_n$$

Summing the constant DC offset $a_0$ and all positive integer harmonics $n$ ($1, 2, 3, \dots$) produces the complete trigonometric Fourier series:

$$\underbrace{x(t)}_{\text{Known waveform}} = \underbrace{a_0 + \sum_{n=1}^{\infty} \left[ a_n \cos\!\left(\frac{2\pi n t}{T}\right) + b_n \sin\!\left(\frac{2\pi n t}{T}\right) \right]}_{\text{Unknown coefficients } a_0,\, a_n,\, b_n}$$

The signal $x(t)$ on the left-hand side is known from a circuit definition or from oscilloscope voltage samples, whereas the coefficients $a_0$, $a_n$, and $b_n$ on the right-hand side are the unknown amplitudes to be isolated.

#### Solving for the DC Offset $a_0$

Integrating both sides of the trigonometric Fourier series over one full period $[0, T]$ isolates $a_0$:

$$\int_0^T x(t)\, dt = \int_0^T a_0\, dt + \sum_{n=1}^{\infty} \left[ a_n \int_0^T \cos\!\left(\frac{2\pi n t}{T}\right) dt + b_n \int_0^T \sin\!\left(\frac{2\pi n t}{T}\right) dt \right]$$

Every cosine and sine wave completes $n$ full cycles over $[0, T]$, spending half of each cycle positive and half negative by equal amounts. Its net area over a full period is zero:

$$\int_0^T \cos\!\left(\frac{2\pi n t}{T}\right) dt = \left[\frac{T}{2\pi n}\sin\!\left(\frac{2\pi n t}{T}\right)\right]_{t=0}^{t=T} = \frac{T}{2\pi n}\big(\sin(2\pi n) - \sin(0)\big) = 0$$

Every oscillating harmonic term on the right-hand side vanishes, leaving only the integrated DC term:

$$\int_0^T x(t)\, dt = \int_0^T a_0\, dt = a_0 T$$

Division of both sides by $T$ yields the DC average:

$$a_0 = \frac{1}{T}\int_0^T x(t)\, dt$$

#### Solving for the Cosine Coefficient $a_k$ (The Frequency Sieve)

Direct integration over $[0, T]$ eliminated every harmonic coefficient $a_n$ because each cosine wave flips between positive and negative half-cycles and cancels its own area. Isolating one specific cosine coefficient $a_k$ at harmonic index $k$ requires preventing the cosine factor next to $a_k$ from flipping sign while leaving every other wave oscillating symmetrically around zero.

Squaring that $k$-th cosine wave accomplishes the goal because the square of any real number is never negative:

$$\cos^2\!\left(\frac{2\pi k t}{T}\right) \ge 0$$

Multiplying both sides of the trigonometric Fourier series by the cosine test wave at harmonic index $k$ and integrating across $[0, T]$ squares the matching $k$-th cosine term:

$$\begin{aligned}
\int_0^T x(t)\cos\!\left(\frac{2\pi k t}{T}\right) dt &= \int_0^T a_0\cos\!\left(\frac{2\pi k t}{T}\right) dt + \sum_{n=1}^{\infty} a_n \int_0^T \cos\!\left(\frac{2\pi n t}{T}\right)\cos\!\left(\frac{2\pi k t}{T}\right) dt \\
&\quad + \sum_{n=1}^{\infty} b_n \int_0^T \sin\!\left(\frac{2\pi n t}{T}\right)\cos\!\left(\frac{2\pi k t}{T}\right) dt
\end{aligned}$$

Three distinct integral families appear on the right-hand side of that correlation integral. First, consider **mismatched cosine frequencies** where harmonic index $n$ differs from $k$. Adding the cosine angle-subtraction and angle-addition identities and dividing by $2$ gives the product-to-sum identity:

$$\cos\alpha\cos\beta = \frac{1}{2}\cos(\alpha - \beta) + \frac{1}{2}\cos(\alpha + \beta)$$

Assigning $\alpha$ and $\beta$ to the $n$-th and $k$-th harmonic angles rewrites the product of two distinct harmonics as a difference frequency plus a sum frequency:

$$\cos\!\left(\frac{2\pi n t}{T}\right)\cos\!\left(\frac{2\pi k t}{T}\right) = \frac{1}{2}\cos\!\left(\frac{2\pi(n - k)t}{T}\right) + \frac{1}{2}\cos\!\left(\frac{2\pi(n + k)t}{T}\right)$$

For any harmonic index $n$ distinct from $k$, both $(n - k)$ and $(n + k)$ are non-zero integers. Both cosine waves oscillate symmetrically above and below zero over $[0, T]$, so their antiderivatives vanish:

$$\int_0^T \cos\!\left(\frac{2\pi n t}{T}\right)\cos\!\left(\frac{2\pi k t}{T}\right) dt = 0 \qquad (\text{for all } n \neq k)$$

Second, consider **all sine-times-cosine cross terms** ($b_n$) across every $n$. Even at the matching harmonic index $k$, a sine wave and a cosine wave sit a quarter period ($90^\circ$) apart. Applying the double-angle sine identity turns their product into a double-frequency sine wave that spends equal time positive and negative:

$$\sin(2\theta) = 2\sin\theta\cos\theta$$

$$\begin{aligned}
\int_0^T \sin\!\left(\frac{2\pi k t}{T}\right)\cos\!\left(\frac{2\pi k t}{T}\right) dt &= \frac{1}{2}\int_0^T \sin\!\left(\frac{4\pi k t}{T}\right) dt \\
&= \left[-\frac{T}{8\pi k}\cos\!\left(\frac{4\pi k t}{T}\right)\right]_{t=0}^{t=T} = -\frac{T}{8\pi k}(1 - 1) = 0
\end{aligned}$$

The identical zero result holds for every mismatched harmonic index $n$ distinct from $k$, so every $b_n$ term on the right-hand side is multiplied by $0$ and disappears.

Third, consider **the single matching cosine frequency** where $n$ matches $k$. Zero frequency difference turns the constant half-angle term in the product-to-sum identity into $0.5$:

$$a_k \int_0^T \cos^2\!\left(\frac{2\pi k t}{T}\right) dt = a_k \int_0^T \left[\frac{1}{2} + \frac{1}{2}\cos\!\left(\frac{4\pi k t}{T}\right)\right] dt = a_k\left[\frac{T}{2} + 0\right] = a_k \cdot \frac{T}{2}$$

Physically, a signal component and test wave sharing the same frequency and phase are both positive during the first half-cycle and both negative during the second half-cycle:

$$(+) \times (+) = (+), \qquad (-) \times (-) = (+)$$

Their squared product never dips below zero, oscillating between $0$ and $1$ around an average height of $0.5$ across duration $T$ to accumulate an area of $T/2$. Substituting those evaluated integrals back into the cosine correlation expansion eliminates every unknown except $a_k$, and multiplying by $2/T$ isolates the cosine amplitude:

$$\int_0^T x(t)\cos\!\left(\frac{2\pi k t}{T}\right) dt = a_k \cdot \frac{T}{2}$$

$$a_k = \frac{2}{T}\int_0^T x(t)\cos\!\left(\frac{2\pi k t}{T}\right) dt = A_k \cos\phi_k$$

#### Solving for the Sine Coefficient $b_k$

A single cosine test wave cannot measure the signal alone. A pure sine wave at frequency $f_k$ (arriving with phase shift $\phi_k$ of $-90^\circ$) sets the cosine projection $a_k$ to zero and misses the wave completely:

$$a_k = A_k\cos(-90^\circ) = 0$$

Capturing the sine component $b_k$ requires multiplying both sides of the trigonometric Fourier series by the sine test wave at harmonic index $k$ and integrating over $[0, T]$:

$$\begin{aligned}
\int_0^T x(t)\sin\!\left(\frac{2\pi k t}{T}\right) dt &= \int_0^T a_0\sin\!\left(\frac{2\pi k t}{T}\right) dt + \sum_{n=1}^{\infty} a_n \int_0^T \cos\!\left(\frac{2\pi n t}{T}\right)\sin\!\left(\frac{2\pi k t}{T}\right) dt \\
&\quad + \sum_{n=1}^{\infty} b_n \int_0^T \sin\!\left(\frac{2\pi n t}{T}\right)\sin\!\left(\frac{2\pi k t}{T}\right) dt
\end{aligned}$$

On the right-hand side of the sine correlation expansion, the $a_0$ integral, every $a_n$ cosine-times-sine integral, and every mismatched $b_n$ integral (for $n$ distinct from $k$) evaluate to $0$. Only the matching $k$-th sine term survives, accumulating half the period:

$$\int_0^T \sin^2\!\left(\frac{2\pi k t}{T}\right) dt = \frac{T}{2}$$

Multiplying both sides by $2/T$ isolates $b_k$:

$$b_k = \frac{2}{T}\int_0^T x(t)\sin\!\left(\frac{2\pi k t}{T}\right) dt = -A_k \sin\phi_k$$

#### Geometric Meaning: Orthogonality as a Dot Product for Waveforms

In vector geometry, the dot product of two $N$-component vectors $\vec{x}$ and $\vec{y}$ multiplies their values at each index $i$ and sums the products, vanishing whenever the two vectors are **orthogonal** (perpendicular, $90^\circ$ apart):

$$\vec{x}\cdot\vec{y} = \sum_{i=1}^N x_i y_i, \qquad \vec{x}\cdot\vec{y} = 0 \quad (\text{orthogonal})$$

Orthogonality guarantees that projecting a vector onto one coordinate axis is never contaminated by components along the other axes. Sampling two continuous waveforms $x(t)$ and $y(t)$ at $N$ instants spaced by $\Delta t$ ($T/N$) forms two $N$-dimensional vectors whose time-weighted dot product converges in the continuous limit (as $N$ grows without bound and $\Delta t$ shrinks to $dt$) to the correlation integral:

$$\lim_{N \to \infty} \sum_{i=1}^N x(t_i)y(t_i)\,\Delta t = \int_0^T x(t)y(t)\, dt$$

The correlation integral between any two distinct frequencies $f_n$ and $f_k$ is zero, so the harmonics $f_1, f_2, \dots, f_N$ form a mutually orthogonal coordinate system. Within each individual frequency $f_k$, the cosine and sine basis waves are also orthogonal to each other, forming a 2D plane that captures both total amplitude $A_k$ and phase $\phi_k$.

By the Pythagorean theorem, the cosine projection $a_k$ and negative sine projection $-b_k$ form the adjacent and opposite legs of a right triangle with hypotenuse $A_k$. Squaring and adding them eliminates $\phi_k$ via the trigonometric Pythagorean identity:

$$\cos^2\phi_k + \sin^2\phi_k = 1$$

$$\sqrt{a_k^2 + (-b_k)^2} = \sqrt{(A_k\cos\phi_k)^2 + (A_k\sin\phi_k)^2} = A_k\sqrt{\cos^2\phi_k + \sin^2\phi_k} = A_k$$

Dividing the opposite leg by the adjacent leg cancels $A_k$ to recover the phase angle $\phi_k$, which converts directly into a physical arrival time shift $\Delta t_k$ on the wire (one $2\pi\text{ rad}$ cycle spans $1/f_k$ seconds):

$$\tan\phi_k = \frac{A_k\sin\phi_k}{A_k\cos\phi_k} = \frac{-b_k}{a_k} \implies \phi_k = \text{atan2}(-b_k,\, a_k), \qquad \Delta t_k = -\frac{\phi_k}{2\pi f_k}$$

#### Combining Cosine and Sine Projections via Euler's Formula

Packaging the cosine projection $a_k$ and sine projection $b_k$ into one expression without collapsing them into a single real scalar (which would lose the ability to solve for two unknowns $A_k$ and $\phi_k$) uses the imaginary unit $j$ ($\sqrt{-1}$). Recalling both Fourier coefficient integrals and Euler's complex exponential identity:

$$a_k = \frac{2}{T}\int_0^T x(t)\cos\!\left(\frac{2\pi k t}{T}\right) dt, \qquad b_k = \frac{2}{T}\int_0^T x(t)\sin\!\left(\frac{2\pi k t}{T}\right) dt$$

$$e^{-j\theta} = \cos\theta - j\sin\theta$$

Multiplying $b_k$ by $-j$ and adding it to $a_k$ merges the two real integrals into one complex correlation integral:

$$a_k - j b_k = \frac{2}{T}\int_0^T x(t)\left[\cos\!\left(\frac{2\pi k t}{T}\right) - j\sin\!\left(\frac{2\pi k t}{T}\right)\right] dt = \frac{2}{T}\int_0^T x(t)\, e^{-j 2\pi k t / T}\, dt$$

Substituting $A_k\cos\phi_k$ for $a_k$ and $-A_k\sin\phi_k$ for $b_k$ cancels the two minus signs on the imaginary term, placing $+A_k\cos\phi_k$ in the real part and $+A_k\sin\phi_k$ in the imaginary part:

$$a_k - j b_k = A_k\cos\phi_k - j(-A_k\sin\phi_k) = A_k\cos\phi_k + j A_k\sin\phi_k$$

#### Infinite-Period Limit: The Continuous Fourier Transform and Inverse Transform

A waveform that occurs only once and never repeats (such as a single digital pulse or step) has an unbounded repetition period $T$. Three changes govern that complex correlation integral in the infinite-period limit:

1. The integration window stretches from one period $[-T/2, T/2]$ to all time $(-\infty, +\infty)$.
2. Adjacent harmonic spacing $\Delta f$ ($1/T$) shrinks toward differential width $df$, merging the discrete harmonic frequencies $f_k$ ($k/T$) into the continuous frequency variable $f$.
3. Period normalization $1/T$ ($\Delta f$) moves out of the forward integral and into the reconstruction integral as differential frequency width $df$, preventing a finite pulse integral divided by an unbounded period $T$ from collapsing to zero.

The forward **Fourier Transform** computes the **spectral amplitude density** $X(f)$ (measured in volt-seconds, or $\text{V/Hz}$):

$$X(f) = \int_{-\infty}^{\infty} x(t)\, e^{-j 2\pi f t}\, dt = \underbrace{\int_{-\infty}^{\infty} x(t)\cos(2\pi f t)\, dt}_{\text{Re}\{X(f)\}} - j\underbrace{\int_{-\infty}^{\infty} x(t)\sin(2\pi f t)\, dt}_{-\text{Im}\{X(f)\}}$$

The complex magnitude $|X(f)|$ gives the amplitude density at frequency $f$, and the angle $\angle X(f)$ gives the phase relative to time zero:

$$|X(f)| = \sqrt{\big(\text{Re}\{X(f)\}\big)^2 + \big(\text{Im}\{X(f)\}\big)^2}, \qquad \angle X(f) = \text{atan2}\big(\text{Im}\{X(f)\},\, \text{Re}\{X(f)\}\big)$$

The **Inverse Fourier Transform** (Fourier synthesis) multiplies the spectral density $X(f)$ (in $\text{V/Hz}$) by $e^{+j2\pi f t}$ and integrates over $df$ (in $\text{Hz}$) to rebuild the real voltage waveform $x(t)$ (in Volts):

$$x(t) = \int_{-\infty}^{\infty} X(f)\, e^{+j 2\pi f t}\, df$$

Two algebraic properties explain why this complex integral reconstructs a purely real physical voltage $x(t)$. First, flipping the exponent sign to $+j2\pi f t$ multiplies the forward transform's complex phase factor by $e^{+j2\pi f t}$, where $j^2$ ($-1$) restores the angle-addition minus sign between the cosine and sine products:

$$\text{Re}\!\left\{(A\cos\phi + j A\sin\phi)(\cos 2\pi f t + j\sin 2\pi f t)\right\} = (A\cos\phi)\cos(2\pi f t) - (A\sin\phi)\sin(2\pi f t) = A\cos(2\pi f t + \phi)$$

Second, for any real signal $x(t)$, evaluating $X(f)$ at $-f$ leaves the even cosine integral unchanged while flipping the sign of the odd sine integral:

$$\cos(-2\pi f t) = \cos(2\pi f t), \qquad \sin(-2\pi f t) = -\sin(2\pi f t), \qquad X(-f) = X^*(f)$$

Integrating across both $-f$ and $+f$ cancels the opposite imaginary parts to zero and sums the two equal real halves ($0.5 + 0.5$), accounting for the factor of $2$ in the one-sided $2/T$ harmonic normalization.

#### Sampled Waveforms and the Discrete Fourier Transform (DFT)

An oscilloscope's analog-to-digital converter (ADC) cannot record a continuous voltage curve across all time. Instead, the instrument records $N$ individual voltage measurements $x[n]$ (indexed from $0$ through $N - 1$) spaced by sample interval $\Delta t$ across a finite capture window $T$ at sampling rate $f_s$:

$$f_s = \frac{1}{\Delta t}, \qquad t_n = n\,\Delta t, \qquad T = N\,\Delta t$$

Across capture duration $T$ (fundamental frequency $f_0$ of $1/T$), the $N$ discrete harmonic **frequency bins** (indexed by $k$ from $0$ through $N - 1$) that complete $k$ full cycles inside $T$ sit at integer multiples of $f_s / N$:

$$f_k = \frac{k}{T} = \frac{k}{N\,\Delta t} = k\,\frac{f_s}{N}$$

Instead of integrating over continuous time, the oscilloscope evaluates the Euler test wave at the $N$ sample timestamps $t_n$, multiplies each sample $x[n]$ by its corresponding test-wave value, and sums the $N$ products. Substituting $f_k$ and $t_n$ into the Euler exponent cancels $\Delta t$:

$$-j 2\pi f_k t_n = -j 2\pi \left(\frac{k}{N\,\Delta t}\right)(n\,\Delta t) = -j\frac{2\pi k n}{N}$$

Summing the $N$ products yields the **Discrete Fourier Transform (DFT)** $X[k]$ and its **Inverse DFT (IDFT)**:

$$X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j 2\pi k n / N}, \qquad x[n] = \frac{1}{N}\sum_{k=0}^{N-1} X[k]\, e^{+j 2\pi k n / N}$$

Evaluating the DFT directly from scratch is computationally expensive for two reasons:

- **Single-bin cost:** Evaluation of one frequency bin $X[k]$ multiplies all $N$ voltage samples by their Euler phase factors, requiring $N$ complex multiplications per bin.
- **Full-spectrum cost:** Independent evaluation across all $N$ frequency bins repeats that work $N$ times, scaling total multiplications quadratically with record length:

$$\text{Direct DFT Multiplications} = N \times N = N^2$$

For an oscilloscope capture of $1\text{ million}$ voltage samples ($N$), direct evaluation across all $1\text{ million}$ bins requires $10^{12}$ ($1\text{ trillion}$) multiplications:

$$(1{,}000{,}000)^2 = 10^{12}$$

#### Fast Fourier Transform Step 1: Even and Odd Sample Halving

Direct DFT evaluation wastes effort because the Euler phase factor steps repeatedly around the unit circle, revisiting identical angles across different combinations of $n$ and $k$:

$$e^{-j2\pi k n / N} = \cos\!\left(\frac{2\pi k n}{N}\right) - j\sin\!\left(\frac{2\pi k n}{N}\right)$$

The **Fast Fourier Transform (FFT)** exploits that periodicity by splitting the $N$ samples into $N/2$ **even-indexed timestamps** ($2m$) and $N/2$ **odd-indexed timestamps** ($2m + 1$), where $m$ runs from $0$ to $N/2 - 1$:

$$X[k] = \sum_{m=0}^{N/2 - 1} x[2m]\, e^{-j 2\pi k (2m) / N} + \sum_{m=0}^{N/2 - 1} x[2m+1]\, e^{-j 2\pi k (2m+1) / N}$$

Dividing numerator and denominator by $2$ rewrites $2m/N$ as $m/(N/2)$, and factoring the $m$-independent single-step rotation $e^{-j2\pi k/N}$ out of the odd sum exposes two half-length DFTs:

$$e^{-j2\pi k(2m+1)/N} = e^{-j2\pi k/N}\,e^{-j2\pi k m/(N/2)}$$

$$X[k] = \underbrace{\sum_{m=0}^{N/2 - 1} x[2m]\, e^{-j 2\pi k m / (N/2)}}_{E[k]\text{ (DFT of } N/2\text{ even samples)}} + e^{-j 2\pi k / N}\underbrace{\sum_{m=0}^{N/2 - 1} x[2m+1]\, e^{-j 2\pi k m / (N/2)}}_{O[k]\text{ (DFT of } N/2\text{ odd samples)}}$$

Both $E[k]$ and $O[k]$ share the identical algebraic form of the original DFT with $N/2$ in place of $N$, splitting one $N$-sample DFT into **two $(N/2)$-sample DFTs**.

#### Fast Fourier Transform Step 2: Reusing Half-Sized Sums Across the Spectrum

Each frequency bin $k$ in the first half of the spectrum ($0$ through $N/2 - 1$) pairs directly with bin $k + N/2$ in the second half. Inside $E[k]$ and $O[k]$, shifting $k$ by $N/2$ adds $m$ full $360^\circ$ rotations ($2\pi m$) to the exponent angle, leaving both half-sized sums unchanged:

$$\frac{2\pi(N/2)m}{N/2} = 2\pi m, \qquad e^{-j2\pi m} = 1$$

$$E\!\left[k + \frac{N}{2}\right] = E[k], \qquad O\!\left[k + \frac{N}{2}\right] = O[k]$$

In the twiddle multiplier $e^{-j2\pi k / N}$ sitting in front of $O[k]$, shifting $k$ by $N/2$ adds half a rotation ($\pi\text{ rad}$, or $180^\circ$) and flips the multiplier's sign:

$$e^{-j\pi} = \cos\pi - j\sin\pi = -1, \qquad e^{-j 2\pi (k + N/2) / N} = e^{-j 2\pi k / N}\cdot e^{-j\pi} = -\,e^{-j 2\pi k / N}$$

Both spectral halves follow from the same two half-sized sums $E[k]$ and $O[k]$ via one addition and one subtraction:

$$X[k] = E[k] + e^{-j 2\pi k / N}\,O[k], \qquad X\!\left[k + \frac{N}{2}\right] = E[k] - e^{-j 2\pi k / N}\,O[k]$$

Halving the $N$-sample DFT once replaces one $N^2$ calculation with two $(N/2)^2$ calculations, cutting the quadratic work in half:

$$\left(\frac{N}{2}\right)^2 + \left(\frac{N}{2}\right)^2 = \frac{N^2}{4} + \frac{N^2}{4} = \frac{N^2}{2}$$

#### Fast Fourier Transform Step 3: Recursive Halving to $N \log_2 N$ Complexity

Each $(N/2)$-sample DFT ($E[k]$ and $O[k]$) is itself an even-length DFT, so the algorithm continues halving into four $(N/4)$-sample DFTs and eight $(N/8)$-sample DFTs down to $1$-sample sums. A $1$-sample DFT equals the sample value $x[0]$ itself ($x[0]\,e^0$) and requires zero multiplications.

Dividing $N$ samples in half $s$ times until a single sample remains sets the number of halving stages to $\log_2 N$:

$$\frac{N}{2^s} = 1 \quad \implies \quad 2^s = N \quad \implies \quad s = \log_2 N$$

An $8$-sample record ($2^3$) takes $3$ stages, whereas a $1{,}000{,}000$-sample record (roughly $2^{20}$) takes $20$ stages. Every stage combines even and odd sub-sums across $N$ butterfly outputs, yielding $N \log_2 N$ total operations:

$$\text{Total Operations} = \underbrace{N}_{\text{operations per stage}} \times \underbrace{\log_2 N}_{\text{number of halving stages}} = N \log_2 N$$

For $8$ samples, the FFT performs $24$ operations ($8 \times 3$) instead of $64$ ($8^2$). Across a $1\text{ million}$-point oscilloscope capture, the FFT performs $20\text{ million}$ operations instead of $1\text{ trillion}$, achieving a $50{,}000\times$ speedup that updates a live spectrum display in milliseconds.

### Discrete Spectra vs. Continuous Spectra

Repeating waveforms and single non-repeating events produce fundamentally different spectra because of the boundary condition imposed by repetition. A repeating clock signal or square wave with period $T$ must return to the identical voltage and slope every $T$ seconds. Only sinusoids that complete an integer number of full cycles $k$ inside $T$ repeat with period $T$:

$$f_k = \frac{k}{T} \qquad (k = 1, 2, 3, \dots)$$

Any fractional multiple (such as $1.3 f_0$) lands at a shifted phase in the next period and cancels out over many cycles. A $1\text{ GHz}$ square wave (period $T$ of $1\text{ ns}$) contains energy exclusively at discrete odd harmonics ($1\text{ GHz}$, $3\text{ GHz}$, $5\text{ GHz}$, and higher odd multiples). Those harmonics appear on a spectrum analyzer or FFT plot as isolated vertical spikes separated by empty gaps of silence.

A single, non-repeating voltage step never returns to its starting state, stretching its repetition period $T$ without bound and shrinking the frequency spacing $\Delta f$ ($1/T$) to zero. Energy appears at $1\text{ GHz}$, at $1.000001\text{ GHz}$, at $1.000002\text{ GHz}$, and across an unbroken continuum starting at $0\text{ Hz}$ (DC). The word **harmonic** applies strictly to the discrete periodic case as an integer multiple of a fundamental frequency $f_0$ ($1/T$), whereas a non-repeating step has no fundamental period and carries a continuous spectral density.

### The Fourier Series of a Square Wave

Evaluating the DC, cosine, and sine Fourier coefficient integrals on a concrete square wave shows how correlation converts a known time-domain waveform into explicit numerical harmonic amplitudes. Consider a periodic square wave $x_T(t)$ of period $T$ that switches upward at time zero, holding $1\text{ V}$ across the first half-period and $0\text{ V}$ across the second half-period:

$$x_T(t) = \begin{cases} 1\text{ V} & 0 \le t < T/2 \\[4pt] 0\text{ V} & T/2 \le t < T \end{cases}$$

#### Evaluating the DC, Cosine, and Sine Integrals

Recalling the DC average and cosine projection integrals over period $T$:

$$a_0 = \frac{1}{T}\int_0^T x_T(t)\, dt, \qquad a_k = \frac{2}{T}\int_0^T x_T(t)\cos\!\left(\frac{2\pi k t}{T}\right) dt$$

Substituting the piecewise square wave $x_T(t)$ yields a $0.5\text{ V}$ average DC offset $a_0$ and zero for every cosine coefficient $a_k$:

$$a_0 = \frac{1}{T}\left[\int_0^{T/2} 1\, dt + \int_{T/2}^T 0\, dt\right] = \frac{1}{T}\left(\frac{T}{2}\right) = 0.5\text{ V}$$

$$a_k = \frac{2}{T}\int_0^{T/2} 1 \cdot \cos\!\left(\frac{2\pi k t}{T}\right) dt = \frac{2}{T}\left[\frac{T}{2\pi k}\sin\!\left(\frac{2\pi k t}{T}\right)\right]_{t=0}^{t=T/2} = \frac{1}{\pi k}\big(\sin(\pi k) - \sin(0)\big) = 0\text{ V}$$

Every cosine term vanishes because each cosine basis wave is even-symmetric around time zero, whereas the square wave jumps upward across time zero. Recalling the sine projection integral and substituting $x_T(t)$ across $[0, T/2]$ produce a closed-form formula for every harmonic index $k$:

$$b_k = \frac{2}{T}\int_0^T x_T(t)\sin\!\left(\frac{2\pi k t}{T}\right) dt$$

$$b_k = \frac{2}{T}\int_0^{T/2} 1 \cdot \sin\!\left(\frac{2\pi k t}{T}\right) dt = \frac{2}{T}\left[-\frac{T}{2\pi k}\cos\!\left(\frac{2\pi k t}{T}\right)\right]_{t=0}^{t=T/2} = \frac{1}{\pi k}\big(1 - \cos(\pi k)\big)$$

The factor $\cos(\pi k)$ alternates between $-1$ at odd $k$ and $+1$ at even $k$, making $(1 - \cos(\pi k))$ equal to $2$ for odd harmonics and $0$ for even harmonics:

$$\cos(\pi k) = (-1)^k, \qquad b_k = \begin{cases} \dfrac{2}{\pi k} & k \text{ odd } (1, 3, 5, \dots) \\[6pt] 0 & k \text{ even } (2, 4, 6, \dots) \end{cases}$$

For a general square wave swinging by $\pm a$ around its midpoint (peak-to-peak swing $2a$ rather than $1\text{ V}$), scaling by $2a$ sets odd harmonic amplitudes to $4a / (\pi k)$. Recalling the trigonometric Fourier series and substituting the $0\text{ V}$-to-$1\text{ V}$ coefficients ($a_0$ of $1/2$, $a_k$ of $0$, and odd $b_k$ of $2/(\pi k)$) yield the complete square-wave series:

$$x_T(t) = a_0 + \sum_{k=1}^{\infty} \left[ a_k \cos\!\left(\frac{2\pi k t}{T}\right) + b_k \sin\!\left(\frac{2\pi k t}{T}\right) \right]$$

$$x_T(t) = \frac{1}{2} + \sum_{k=1, 3, 5, \dots}^{\infty} \frac{2}{\pi k}\sin\!\left(\frac{2\pi k t}{T}\right)$$

#### Half-Wave Symmetry and Vanishing Even Harmonics

Measured relative to its $0.5\text{ V}$ midpoint, the second half of the square wave's period ($-0.5\text{ V}$) is an inverted copy of the first half ($+0.5\text{ V}$), a property called **half-wave symmetry**. Any odd harmonic ($1, 3, 5, \dots$) completes an odd number of half-cycles in $T/2$ and inverts sign in the second half-period alongside the square wave, so their product stays positive across both halves and adds constructively.

Any even harmonic ($2, 4, 6, \dots$) completes a whole number of full cycles inside $T/2$ and repeats with the identical sign during the second half-period while the square wave flips negative. Integration across the second half-period cancels the first half-period to zero, eliminating all even harmonics whenever a waveform has a $50\%$ duty cycle.

#### Building a Flat Plateau from Curved Sine Waves

Alternating peak polarities across the odd harmonics flatten rounded sine crests into a horizontal $1.0\text{ V}$ plateau. At the center of the high half-period ($T/4$), the fundamental ($b_1$) rides atop the $0.5\text{ V}$ DC offset and overshoots $1.0\text{ V}$, while higher odd harmonics alternate sign at $T/4$:

$$b_1 = \frac{2}{\pi} \approx 0.637\text{ V}, \qquad b_3 = \frac{2}{3\pi} \approx 0.212\text{ V}, \qquad b_5 = \frac{2}{5\pi} \approx 0.127\text{ V}, \qquad b_7 = \frac{2}{7\pi} \approx 0.091\text{ V}$$

Alone on top of $0.5\text{ V}$ DC, the fundamental peaks at $1.137\text{ V}$ ($0.5\text{ V}$ plus $0.637\text{ V}$). At that identical instant $T/4$, the 3rd harmonic hits its negative peak and subtracts $0.212\text{ V}$ to pull the center down, the 5th harmonic adds $0.127\text{ V}$, and the 7th harmonic subtracts $0.091\text{ V}$. By the Leibniz alternating series, the infinite sum at $T/4$ converges to $1.0\text{ V}$, flattening the curved peaks into a horizontal plateau:

$$1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \cdots = \frac{\pi}{4}, \qquad x_T\!\left(\frac{T}{4}\right) = \frac{1}{2} + \frac{2}{\pi}\left(\frac{\pi}{4}\right) = 1.0\text{ V}$$

#### Phase-Locked Zero Crossings and Periodic Sharp Edges

Every odd harmonic frequency $f_k$ ($k f_0$) is an odd integer multiple of the fundamental. Across one half-period $T/2$ of the fundamental, the $k$-th harmonic completes $k$ half-cycles, forcing all odd harmonics to cross zero in lockstep and reverse slope together at every integer multiple of $T/2$.

### The Fourier Integral of a Step

A single rising step $u(t)$ jumps from $0\text{ V}$ before time zero to $1\text{ V}$ after time zero. Physically, $u(t)$ is the infinite-period limit of the $0\text{ V}$-to-$1\text{ V}$ square wave $x_T(t)$ with its upward transition anchored at time zero. Letting period $T$ grow without bound pushes the preceding transition at $-T/2$ to $-\infty$ and the following transition at $+T/2$ to $+\infty$, leaving one permanent step at the origin.

#### Deriving the Continuous Step Integral

Recalling the periodic $0\text{ V}$-to-$1\text{ V}$ square-wave series shows that only odd harmonics appear, with each odd harmonic $k$ sitting at frequency $f_k$ ($k/T$):

$$x_T(t) = \frac{1}{2} + \sum_{k=1, 3, 5, \dots}^{\infty} \frac{2}{\pi k}\sin\!\left(\frac{2\pi k t}{T}\right)$$

Consecutive odd harmonics ($k$ and $k + 2$) are separated by a frequency spacing $\Delta f_{\text{odd}}$ of $2/T$:

$$f_k = \frac{k}{T} \implies \frac{1}{k} = \frac{1}{f_k T}, \qquad \Delta f_{\text{odd}} = f_{k+2} - f_k = \frac{k + 2}{T} - \frac{k}{T} = \frac{2}{T}$$

Rewriting the harmonic amplitude $2/(\pi k)$ in terms of $f_k$ and $\Delta f_{\text{odd}}$ casts the square-wave series as a Riemann sum over frequency:

$$\frac{2}{\pi k} = \frac{1}{\pi f_k}\left(\frac{2}{T}\right) = \frac{1}{\pi f_k}\,\Delta f_{\text{odd}}$$

$$x_T(t) = \frac{1}{2} + \sum_{k=1, 3, 5, \dots}^{\infty} \frac{1}{\pi f_k}\sin(2\pi f_k t)\,\Delta f_{\text{odd}}$$

Letting period $T$ grow without bound shrinks $\Delta f_{\text{odd}}$ into the differential $df$ and turns that Riemann sum into a continuous integral over all positive frequencies $f$. Expressing the integral in either cyclic frequency $f$ or angular frequency $\omega$ ($2\pi f$, where $df/f$ equals $d\omega/\omega$) yields the Fourier step integral:

$$u(t) = \frac{1}{2} + \frac{1}{\pi}\int_0^{\infty} \frac{\sin(2\pi f t)}{f}\, df = \frac{1}{2} + \frac{1}{\pi}\int_0^{\infty} \frac{\sin(\omega t)}{\omega}\, d\omega$$

#### Physical Roles of the DC Offset, Spectral Weight, and Dirichlet Plateau

Every term in the continuous step integral inherits a direct physical role from the periodic square wave. First, the $0.5\text{ V}$ DC offset comes directly from $a_0$. Every sine wave averages to zero over time, so the sine continuum alone steps antisymmetrically from $-0.5\text{ V}$ to $+0.5\text{ V}$. Adding the $0\text{ Hz}$ DC term shifts both plateaus upward by $+0.5\text{ V}$ to sit at $0\text{ V}$ before time zero and $1\text{ V}$ after time zero.

Second, the factor $1/(\pi f)$ in front of $\sin(2\pi f t)\,df$ (in $\text{V/Hz}$) weights each sine wave in inverse proportion to frequency $f$. Multiplying frequency by $10$ (one **decade**, such as $100\text{ MHz}$ to $1\text{ GHz}$) shrinks amplitude to one-tenth of its prior height ($-20\text{ dB/decade}$), whereas dividing frequency by $10$ ($100\text{ MHz}$ down to $10\text{ MHz}$) makes the wave $10\times$ taller:

$$20\log_{10}(0.1) = -20\text{ dB/decade}$$

Third, substituting $x$ for $\omega t$ at any positive time $t$ reduces the integral to the constant Dirichlet value $+\pi/2$, whereas odd sine symmetry at any negative time $t$ flips the integral to $-\pi/2$:

$$\int_0^\infty \frac{\sin(\omega t)}{\omega}\, d\omega = \begin{cases} +\dfrac{\pi}{2} & t > 0 \\[6pt] -\dfrac{\pi}{2} & t < 0 \end{cases} \quad \implies \quad u(t) = \begin{cases} \dfrac{1}{2} + \dfrac{1}{2} = 1\text{ V} & t > 0 \\[6pt] \dfrac{1}{2} - \dfrac{1}{2} = 0\text{ V} & t < 0 \end{cases}$$

#### High-Frequency Cancellation Versus Low-Frequency Plateau Support

Continuous frequency coverage allows oscillating sine waves to hold that $1.0\text{ V}$ plateau flat across all positive time. In a periodic square wave, only discrete multiples of $f_0$ exist, so **all** harmonics cross zero together at every multiple of $T/2$. In the continuous step integral, every intermediate frequency is present as well; individual pairs of frequencies still cross zero simultaneously, yet **the entire continuous spectrum never crosses zero in unison again after time zero**.

A continuous **relay race** from fast sine waves to progressively slower sine waves sustains the plateau across positive time $t$, partitioned at any observation instant $t$ by the crossover frequency $f_{\text{crossover}}$ whose half-period equals $t$:

$$f_{\text{crossover}} = \frac{1}{2t}$$

- **Faster frequencies (above $f_{\text{crossover}}$):** Waves above $f_{\text{crossover}}$ have already completed one or more half-cycles by time $t$, placing $+1$ crests beside $-1$ troughs across neighboring frequencies so they cancel one another out.
- **Slower frequencies (below $f_{\text{crossover}}$):** Waves between $0\text{ Hz}$ and $f_{\text{crossover}}$ have half-periods longer than $t$ and have never crossed zero since time zero, staying inside their first positive arch to hold $+0.5\text{ V}$ above the $0.5\text{ V}$ DC midpoint.

#### How Inverse-Frequency Weighting Prevents Plateau Droop

At $1\text{ ns}$, slow waves between $0\text{ Hz}$ and $500\text{ MHz}$ support the step plateau, whereas $10\times$ later at $10\text{ ns}$ only waves below $50\text{ MHz}$ remain in their first positive arch. Between $1\text{ ns}$ and $10\text{ ns}$, the $50\text{ MHz}$-to-$500\text{ MHz}$ waves complete their first positive arch and drop into the fast cancelling group, handing support to the $10\times$ narrower band between $0\text{ Hz}$ and $50\text{ MHz}$.

The plateau never sags because the $1/(\pi f)$ spectral weight makes those $10\times$ lower frequencies ($0\text{ Hz}$ to $50\text{ MHz}$) **$10\times$ taller in amplitude** than the $0\text{ Hz}$-to-$500\text{ MHz}$ band, keeping the product of active bandwidth $f_{\text{crossover}}$ and spectral density $1/(\pi f_{\text{crossover}})$ invariant for all positive $t$:

$$f_{\text{crossover}} = \frac{1}{2t}, \qquad \frac{1}{\pi f_{\text{crossover}}} = \frac{2t}{\pi} \qquad \Longrightarrow \qquad f_{\text{crossover}} \times \left(\frac{1}{\pi f_{\text{crossover}}}\right) = \frac{1}{\pi}$$

That relay balance explains two immediate hardware behaviors. An AC-coupling capacitor that blocks low frequencies removes the slow relay runners needed at large $t$, causing a long step plateau to droop back toward $0\text{ V}$. Conversely, a lossy PCB trace that attenuates high frequencies removes the fast relay runners needed right after time zero, rounding and slowing the rising edge.

### Rise Time and Bandwidth

An ideal mathematical step switches in zero rise time ($0\text{ s}$) and carries a $1/f$ spectrum that extends forever. Every physical transistor, PCB trace, connector, and oscilloscope front-end requires a finite **rise time** $t_r$ (measured from $10\%$ to $90\%$ of the voltage step) to complete a transition. Every real driver and interconnect contains series resistance $R$ (transistor channel and copper trace) and shunt capacitance $C$ (signal conductor, pad, and reference plane), where raising capacitor voltage by $\Delta V$ requires delivering charge $\Delta Q$ through resistance-limited current $i(t)$ over characteristic time constant $\tau$:

$$\Delta Q = C\,\Delta V, \qquad i(t) = \frac{v_{\text{supply}} - v(t)}{R}, \qquad \tau = R C$$

#### Time-Domain RC Charging and the 10%-to-90% Rise Time

Applying a $1\text{ V}$ step to an initially uncharged $RC$ circuit at time zero drops the full $1\text{ V}$ across $R$ initially, driving maximum charging current into $C$. Charge accumulation on $C$ raises $v(t)$ toward $1\text{ V}$ and shrinks the remaining voltage drop across $R$ exponentially:

$$v(t) = 1 - e^{-t/\tau}$$

Solving the exponential charging curve at the $10\%$ threshold ($0.1\text{ V}$ at $t_{10}$) and the $90\%$ threshold ($0.9\text{ V}$ at $t_{90}$) isolates both threshold timestamps in multiples of $\tau$:

$$0.1 = 1 - e^{-t_{10}/\tau} \implies e^{-t_{10}/\tau} = 0.9 \implies t_{10} = -\tau\ln(0.9) = \tau\ln\!\left(\frac{1}{0.9}\right)$$

$$0.9 = 1 - e^{-t_{90}/\tau} \implies e^{-t_{90}/\tau} = 0.1 \implies t_{90} = -\tau\ln(0.1) = \tau\ln\!\left(\frac{1}{0.1}\right)$$

Subtracting $t_{10}$ from $t_{90}$ and applying the quotient rule of logarithms expresses the $10\%$-to-$90\%$ rise time $t_r$ directly in terms of $\tau$:

$$t_r = t_{90} - t_{10} = \tau\left(\ln\frac{1}{0.1} - \ln\frac{1}{0.9}\right) = \tau\ln\!\left(\frac{0.9}{0.1}\right) = \tau\ln 9 \approx 2.197\,\tau$$

#### Series Charge Conservation and Frequency-Dependent Resistor Drop

That same $RC$ charging bottleneck filters each individual sine wave of frequency $f$ through series charge conservation. Electric charge cannot accumulate inside the wire node between $R$ and $C$, so every coulomb arriving on the capacitor plate per second must flow through the series resistor during that same second:

$$i_R(t) = i_C(t) = i(t) = \frac{dQ(t)}{dt} = C\,\frac{dv_C(t)}{dt}, \qquad v_R(t) = R\,i(t) = R C\,\frac{dv_C(t)}{dt} = \tau\,\frac{dv_C(t)}{dt}$$

Kirchhoff's voltage law sets total input voltage $v_{\text{in}}(t)$ at every instant equal to the sum of capacitor voltage and resistor drop:

$$v_{\text{in}}(t) = \underbrace{v_C(t)}_{\text{Capacitor voltage}} + \underbrace{\tau\,\frac{dv_C(t)}{dt}}_{\text{Resistor voltage}}$$

Pure sinusoids preserve their shape under differentiation, so both $v_{\text{in}}(t)$ and $v_C(t)$ oscillate at frequency $f$. Choosing time zero where $v_C(t)$ crosses $0\text{ V}$ heading positive writes capacitor voltage as $V_{\text{out}}\sin(2\pi f t)$. Physically, reaching $+V_{\text{out}}$ requires moving a fixed charge packet $\Delta Q$ ($C\,V_{\text{out}}$); a $10\times$ higher frequency moves that packet in one-tenth the time $\Delta t$, demanding $10\times$ more current ($\Delta Q / \Delta t$) and $10\times$ more resistor drop across $R$:

$$\frac{dv_C(t)}{dt} = \frac{d}{dt}\big[V_{\text{out}}\sin(2\pi f t)\big] = (2\pi f)\,V_{\text{out}}\cos(2\pi f t), \qquad v_R(t) = (2\pi f \tau)\,V_{\text{out}}\cos(2\pi f t)$$

$$v_{\text{in}}(t) = V_{\text{out}}\sin(2\pi f t) + (2\pi f \tau)\,V_{\text{out}}\cos(2\pi f t)$$

#### Quadrature Voltage Addition and the Half-Power Cutoff Frequency

At $0^\circ$, the uncharged capacitor ($0\text{ V}$) exerts zero back-voltage while $\sin(2\pi f t)$ crosses zero at maximum slope, driving peak current and peak resistor voltage $v_R(t)$. Between $0^\circ$ and $90^\circ$, rising capacitor voltage opposes inflow while the sine slope flattens; at the $90^\circ$ crest ($+V_{\text{out}}$), zero slope halts current and drops $v_R(t)$ to $0\text{ V}$. The cosine resistor wave peaks at $0^\circ$ while the sine capacitor wave peaks $90^\circ$ later, so their perpendicular peak amplitudes combine as legs of a right triangle with hypotenuse $V_{\text{in}}$:

$$V_{\text{in}} = \sqrt{V_{\text{out}}^2 + \big((2\pi f \tau)\,V_{\text{out}}\big)^2} = V_{\text{out}}\sqrt{1 + (2\pi f \tau)^2}$$

Dividing $V_{\text{out}}$ by $V_{\text{in}}$ defines the **channel transfer magnitude** $|H(f)|$, the fraction of input sine-wave amplitude reaching the capacitor at frequency $f$:

$$|H(f)| = \frac{V_{\text{out}}}{V_{\text{in}}} = \frac{1}{\sqrt{1^2 + (2\pi f \tau)^2}}$$

At low frequencies where $2\pi f \tau$ sits well below unity, resistor drop is negligible and nearly the full input swing reaches $C$. At high frequencies where $2\pi f \tau$ far exceeds unity, resistor drop dominates and capacitor amplitude rolls off inversely with frequency:

$$|H(f)| \approx 1 \quad (2\pi f \tau \ll 1), \qquad |H(f)| \approx \frac{1}{2\pi f \tau} \propto \frac{1}{f} \quad (2\pi f \tau \gg 1)$$

Equal resistor and capacitor voltage amplitudes ($2\pi f_{3\text{dB}}\tau$ equal to $1$) mark the **half-power bandwidth** $f_{3\text{dB}}$:

$$f_{3\text{dB}} = \frac{1}{2\pi\tau} = \frac{1}{2\pi R C}, \qquad |H(f_{3\text{dB}})| = \frac{1}{\sqrt{1^2 + 1^2}} = \frac{1}{\sqrt{2}} \approx 0.707$$

At $f_{3\text{dB}}$, both capacitor and resistor waves carry peak amplitude $0.707\,V_{\text{in}}$ spaced $90^\circ$ apart. At $45^\circ$ (where $\sin 45^\circ$ and $\cos 45^\circ$ both equal $0.707$), each instantaneous wave reaches $0.50\,V_{\text{in}}$ and sums to the $1.00\,V_{\text{in}}$ input peak. At $0^\circ$ and $90^\circ$, one wave hits $0.707\,V_{\text{in}}$ while the other crosses $0\text{ V}$. Electrical power scales with voltage squared ($V^2 / R$), delivering $50\%$ of the signal power to the capacitor and dissipating $50\%$ in the resistor ($-3\text{ dB}$, derived in [Chapter 8](08_S_Parameters_and_VNA.md)):

$$P \propto V^2 \implies (0.707)^2 = 0.50, \qquad 10\log_{10}(0.50) \approx -3.01\text{ dB}$$

#### Linking Single-Pole Rise Time and Half-Power Bandwidth

Both the time-domain rise time ($\tau\ln 9$) and the frequency-domain cutoff ($1 / (2\pi\tau)$) are governed by the **same physical time constant $\tau$**. Eliminating $\tau$ between the two expressions locks rise time and single-pole bandwidth together:

$$\tau = \frac{1}{2\pi f_{3\text{dB}}} \quad \implies \quad t_r = \frac{\ln 9}{2\pi f_{3\text{dB}}} \approx \frac{0.35}{f_{3\text{dB}}} \quad \Longleftrightarrow \quad f_{3\text{dB}} \approx \frac{0.35}{t_r}$$

Rise time and bandwidth are the time-domain and frequency-domain measurements of the same physical charging speed. One $RC$ charging bottleneck forms a **single-pole** (first-order) filter that introduces one factor of $1/f$ roll-off above $f_{3\text{dB}}$: a $1\text{ ns}$ step response corresponds to $350\text{ MHz}$ bandwidth, whereas a $20\text{ ps}$ step response corresponds to $17.5\text{ GHz}$ ($0.35 / 20\text{ ps}$). Instruments with **multi-pole** front-end filters cascade several stages for a steeper roll-off and exhibit a numerator constant between $0.40$ and $0.45$ rather than $0.35$.

#### Finite-Ramp Averaging and the Spectral Corner Frequency

Ramping an edge linearly over duration $t_r$ instead of jumping instantaneously reshapes the signal spectrum itself above a corner frequency set by $t_r$. In an ideal zero-rise-time step, cancelling positive and negative half-cycles leave one uncancelled lobe of width $1/(2f)$ whose integral scales inversely with frequency, giving the $-20\text{ dB/decade}$ ideal step spectrum $A_{\text{step}}(f)$:

$$\int \sin(2\pi f t)\,dt = -\frac{\cos(2\pi f t)}{2\pi f}, \qquad A_{\text{step}}(f) = \frac{1}{\pi f}$$

A linear ramp of duration $t_r$ spreads the $1\text{ V}$ jump into a uniform stream of miniature steps across $[-t_r/2, +t_r/2]$, multiplying the ideal step amplitude $1/(\pi f)$ by the ramp-window average of $\cos(2\pi f t)$:

$$\text{Ramp Factor} = \frac{1}{t_r}\int_{-t_r/2}^{+t_r/2} \cos(2\pi f t)\,dt = \frac{\sin(\pi f t_r)}{\pi f t_r}$$

At low frequencies well below the **spectral corner frequency** $f_{\text{corner}}$, the wave period $1/f$ far exceeds $t_r$. A $100\text{ MHz}$ wave ($10{,}000\text{ ps}$ period) advances through just $0.2\%$ ($20\text{ ps} / 10{,}000\text{ ps}$) of one cycle during a $20\text{ ps}$ ramp, keeping all miniature steps in phase near unity ramp factor and preserving the $-20\text{ dB/decade}$ slope. Above $f_{\text{corner}}$ (where the high-frequency sinc envelope $1/(\pi f t_r)$ crosses unity), fast waves oscillate through opposing half-cycles *during* the ramp itself; a $50\text{ GHz}$ wave completes one full $20\text{ ps}$ cycle inside a $20\text{ ps}$ ramp and steepens the roll-off to $1/f^2$ ($-40\text{ dB/decade}$):

$$f_{\text{corner}} = \frac{1}{\pi t_r} \approx \frac{0.32}{t_r}, \qquad A_{\text{ramp}}(f) = \left(\frac{1}{\pi f}\right) \times \left(\frac{1}{\pi f t_r}\right) = \frac{1}{\pi^2 t_r \, f^2} \propto \frac{1}{f^2}$$

#### Practical Knee Frequency and Interconnect Bandwidth Budgeting

A channel whose half-power cutoff $f_{3\text{dB}}$ merely equals $0.35 / t_r$ is too narrow to pass an existing $t_r$ edge without stretching it. That $0.35 / t_r$ bandwidth describes an $RC$ stage that turns an *ideal $0\text{ ps}$ step* into a $20\text{ ps}$ edge. Feeding an *existing* $20\text{ ps}$ driver edge $t_{r,\text{driver}}$ into a $17.5\text{ GHz}$ channel (channel rise time $t_{r,\text{channel}}$ of $20\text{ ps}$) cascades two charging bottlenecks via root-sum-square:

$$t_{r,\text{out}} \approx \sqrt{t_{r,\text{driver}}^2 + t_{r,\text{channel}}^2} = \sqrt{(20\text{ ps})^2 + (20\text{ ps})^2} \approx 28.3\text{ ps} \quad (41\%\text{ slower})$$

Setting one sine-wave half-cycle $1/(2f)$ equal to $t_r$ defines the **practical knee frequency** $f_{\text{knee}}$ ($25\text{ GHz}$ for a $20\text{ ps}$ edge):

$$f_{\text{knee}} = \frac{1}{2 t_r} = \frac{0.50}{t_r}$$

Every component above $f_{\text{knee}}$ completes more than one half-cycle during the $t_r$ climb (pulling back against its own upward push during the same transition) and already sits past the $1/f^2$ corner at $0.32 / t_r$. Removing all frequencies above $f_{\text{knee}}$ slows the $10\%$-to-$90\%$ rise time by less than $10\%$ (versus $41\%$ at $0.35 / t_r$), making $0.50 / t_r$ a conservative upper bound for **interconnect budgeting** across PCB traces, vias, connectors, and probes without overpaying for unused bandwidth.

Three rise-time-to-frequency expressions appear across signal integrity specifications, and each answers a distinct physical question:

| Expression | Named Quantity | Physical Meaning and Engineering Application |
|---|---|---|
| $f_{\text{corner}} = \frac{1}{\pi t_r} \approx \frac{0.32}{t_r}$ | **Spectral envelope corner** | Marks the frequency where a finite ramp begins oscillating through multiple half-cycles during $t_r$, steepening roll-off from $-20\text{ dB/decade}$ ($1/f$) to $-40\text{ dB/decade}$ ($1/f^2$); equals $15.9\text{ GHz}$ for a $20\text{ ps}$ edge. |
| $f_{3\text{dB}} \approx \frac{0.35}{t_r}$ | **Single-pole $-3\text{ dB}$ bandwidth** | Defines the half-power ($0.707$ voltage) bandwidth of a first-order $RC$ system whose step response has a $10\%$ to $90\%$ rise time of $t_r$; equals $17.5\text{ GHz}$ for a $20\text{ ps}$ edge. |
| $f_{\text{knee}} = \frac{0.50}{t_r}$ | **Practical knee frequency** | Provides a conservative upper frequency bound below which the vast majority of edge energy resides for channel and interconnect budgeting; equals $25.0\text{ GHz}$ for a $20\text{ ps}$ edge. |

### Data Rate, Nyquist Frequency, and Edge Bandwidth

Two separate frequency scales coexist on every digital transmission line, and confusing them is a common pitfall in hardware design.

#### Data-Rate Frequency and the Nyquist Fundamental

The first frequency scale measures **how often the switch flips** and is set by bit rate $R_{\text{bit}}$ (or symbol rate) and the transmitted bit pattern. In non-return-to-zero (NRZ) signaling, each bit occupies one unit interval $\text{UI}$, and the fastest repeating pattern (`10101010`) requires two bits (one `1` and one `0`) to complete one full square-wave cycle at the **Nyquist frequency** $f_{\text{Nyquist}}$:

$$\text{UI} = \frac{1}{R_{\text{bit}}}, \qquad f_{\text{Nyquist}} = \frac{R_{\text{bit}}}{2} = \frac{1}{2\,\text{UI}}$$

On a $10\text{ Gbps}$ NRZ link ($100\text{ ps}$ unit interval $\text{UI}$), an alternating `10101010` pattern has a $5\text{ GHz}$ Nyquist fundamental, whereas a long run of identical bits (`11111111`) drops to $0\text{ Hz}$ (DC) across the run. Industry standards (PCIe, Ethernet, and USB) specify channel insertion loss in decibels at $f_{\text{Nyquist}}$ because heavy attenuation of the `1010` fundamental closes the eye before higher harmonics even enter the picture. Note the terminology distinction: the **Nyquist frequency** is half the symbol or sampling rate, whereas the **Nyquist rate** in sampling theory is twice the signal's highest frequency.

#### Edge Bandwidth Independence from Repetition Rate

The second frequency scale measures **how fast the voltage climbs during each flip** and is governed solely by driver rise time $t_r$ through $0.35 / t_r$, independent of how often the bit flips. A transistor with a $20\text{ ps}$ rise time $t_r$ launches spectral energy past $17.5\text{ GHz}$ both during a $100\text{ ps}$ clock (`10 Gbps`) and during a once-per-second manual pushbutton trigger.

Together, bit pattern and rise time fix the complete wire spectrum. Pattern periodicity sets *where* odd harmonics ($f_0$, $3f_0$, and $5f_0$) sit along the frequency axis, while rise time $t_r$ sets the two-slope envelope ($1/f$ up to $f_{\text{corner}}$, then $1/f^2$) that weights their amplitudes.

### All Frequencies Travel Simultaneously

Fourier decomposition reveals a key physical reality about propagation on a trace: a digital bitstream does not switch its frequency from low to high moment by moment as the bit pattern changes. Instead, all frequency components travel along the copper trace simultaneously, superimposed in the same space at the same time.

Low-frequency components sustain the flat voltage plateaus during consecutive identical bits (`11110000`), and high-frequency components interfere constructively at every transition instant to build the steep vertical edges while cancelling each other across the plateaus. Frequency-dependent loss mechanisms such as the skin effect and dielectric absorption ([Chapter 5](05_Skin_Effect_and_Dielectric_Loss.md)) do not turn on only when an edge arrives; they continuously attenuate the high-frequency components and delay their phases relative to the low-frequency components along the entire trace. The waveform arriving at the receiver is distorted because its high-frequency sine waves arrive smaller and out of step with the low-frequency sine waves that hold the plateaus.

## Architecture

### Physical Reality vs. Mathematical Decomposition

Describing a voltage step as a sum of sine waves can create a misleading mental picture if taken literally at the transmitter: a SerDes driver or TDR step generator does **not** contain thousands of miniature sine-wave oscillators inside the silicon die.

Physically, the transmitter is just a DC power rail and a fast transistor switch. Prior to switching, the transistor holds the trace at $0\text{ V}$; at time zero, the transistor connects the trace to the $1\text{ V}$ supply rail, launching a single electromagnetic wavefront down the line ([Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md)).

Fourier analysis is a mathematical prism applied to that physical wavefront. A beam of white sunlight is a single electromagnetic wave that separates into a continuous rainbow of wavelengths when passed through a glass prism, even though the sun did not assemble white light by aligning millions of colored lasers. Similarly, a sharp voltage step on a copper trace is a single electromagnetic transition whose geometry intrinsically contains a continuous spectrum of frequencies. Copper skin loss and dielectric polarization respond differently to fast field reversals than to slow ones, so the transmission line itself acts like the glass prism, attenuating and delaying the high-frequency components of the wavefront during propagation.

### The Channel as a Linear, Time-Invariant Filter

Fourier analysis becomes a predictive engineering tool because passive interconnects (PCB traces, vias, packages, and connectors) behave as **Linear, Time-Invariant (LTI)** systems:

- **Linearity (Superposition):** A scaled input voltage scales the output voltage by the identical factor, and two signals applied together produce the sum of their individual responses.
- **Time-Invariance:** A bit launched at $1\text{ ns}$ experiences the identical channel behavior as a bit launched at time zero, shifted later in time by $1\text{ ns}$.

Pure sine waves are the eigenfunctions of any LTI channel: a sine wave of frequency $f$ entering the trace emerges at the receiver at the identical frequency $f$, scaled in amplitude by $|H(f)|$ and shifted in phase by $\angle H(f)$. Combining both effects into a complex **transfer function** $H(f)$ lets superposition evaluate each input frequency component $X(f)$ by direct multiplication:

$$H(f) = |H(f)|\,e^{j\angle H(f)}, \qquad Y(f) = H(f)\, X(f)$$

#### Impulse Response and Spectral Uniformity

In the time domain, frequency-domain multiplication corresponds to exciting the channel with an impulsive tap and summing the resulting ringing wakes. An infinitely brief, unit-area spike at time zero defines the **unit impulse** $\delta(t)$, obtained by recalling the unit step integral $u(t)$ and differentiating with respect to $t$:

$$u(t) = \frac{1}{2} + \frac{1}{\pi}\int_0^{\infty} \frac{\sin(2\pi f t)}{f}\, df$$

$$\delta(t) = \frac{du(t)}{dt} = \int_0^{\infty} \frac{1}{\pi f}\big(2\pi f\cos(2\pi f t)\big)\,df = 2\int_0^{\infty} \cos(2\pi f t)\,df$$

Higher frequencies in a step carry smaller $1/(\pi f)$ amplitudes yet steeper $2\pi f$ slopes at time zero. Multiplying those two factors gives a constant weight of $2$ across all positive frequencies while every cosine wave peaks at $+1$ at time zero (unit spectral density $X(f)$ across the two-sided frequency axis):

$$2\pi f \times \frac{1}{\pi f} = 2, \qquad X(f) = 1 \quad \implies \quad Y(f) = H(f) \cdot 1 = H(f)$$

Exciting an LTI channel with $\delta(t)$ yields output spectrum $H(f)$, whose inverse Fourier transform defines the channel's time-domain **impulse response** $h(t)$.

#### Time-Domain Convolution as Superposition of Wakes

Any arbitrary input waveform $x(t)$ decomposes into a continuous sequence of narrow vertical slices of height $x(\tau)$ and width $d\tau$, each acting as a miniature impulse launched at time $\tau$. At observation time $t$, the slice launched at $\tau$ has been ringing for elapsed duration $(t - \tau)$ and contributes a weighted wake to the receiver, forming the **convolution integral**:

$$y(t) = \int_{-\infty}^{\infty} x(\tau)\, h(t - \tau)\, d\tau$$

Frequency-domain multiplication of $H(f)$ by $X(f)$ and time-domain convolution of $x(t)$ with $h(t)$ are two mathematical descriptions of the identical physical process.

#### Step Response and Time-Domain Reflectometry

A unit step $u(t)$ stays high permanently after time zero as the running time integral of $\delta(t)$, so the channel's **step response** $s(t)$ equals the running accumulation of its impulse response $h(t)$:

$$s(t) = \int_{-\infty}^t h(\tau)\,d\tau$$

A Time-Domain Reflectometer (TDR, [Chapter 7](07_Time_Domain_Reflectometry.md)) launches a fast step into an interconnect and displays this step response directly.

#### Single-Bit Pulse Response and Intersymbol Interference

A single transmitted `1` bit of duration $\text{UI}$ (surrounded by `0` bits) equals a rising step $u(t)$ at time zero followed by a falling step $-u(t - \text{UI})$ one unit interval later. By linearity, the channel's single-bit **pulse response** $p(t)$ is the step response minus a copy delayed by $\text{UI}$:

$$p(t) = s(t) - s(t - \text{UI})$$

In an ideal infinite-bandwidth channel, $p(t)$ stays confined within its $1\text{-UI}$ slot. High-frequency channel loss slows and smears the edges so $p(t)$ spreads across multiple unit intervals, surrounding the **main cursor** with **pre-cursors** and **post-cursors** in adjacent bit slots. That residual tail spillage defines **Intersymbol Interference (ISI)**, corrected by transmitter FFE ([Chapter 13](13_Transmitter_FFE.md)) and receiver CTLE/DFE ([Chapter 14](14_CTLE_and_DFE.md)).

### Bandwidth and Time-Domain Resolution

A time-domain instrument such as a TDR or oscilloscope can spatially resolve two closely spaced impedance discontinuities (such as two vias or connector pins) only when the launched edge finishes rising before the reflection from the second discontinuity arrives. Recall from [Chapter 1](01_Wave_Propagation_and_Transmission_Lines.md) that an edge of rise time $t_r$ traveling at propagation velocity $v_p$ spans a physical spatial length $\ell_{\text{edge}}$ along the trace:

$$\ell_{\text{edge}} = v_p t_r \approx \frac{0.35\,v_p}{f_{3\text{dB}}}$$

High-frequency loss attenuates the upper spectrum of a step traveling down a long board trace, reducing $f_{3\text{dB}}$, lengthening $t_r$, and stretching $\ell_{\text{edge}}$ so that small physical features far from the launch port blur together ([Chapter 7](07_Time_Domain_Reflectometry.md)).

## Worked Examples

### Fourier Transform Pairs Used in Signal Integrity

Earlier sections established the pure sine wave, the symmetric square wave, and the unit impulse $\delta(t)$. Two additional pulse shapes arise directly when $\delta(t)$ passes through either an abrupt "brick-wall" frequency cutoff or a smooth bell-curve roll-off.

#### Brick-Wall Cutoff and the Sinc Pulse

Passing the unit impulse $\delta(t)$ through an ideal filter that transmits all frequencies up to a sharp cutoff $f_c$ and blocks everything above $f_c$ replaces the upper integration limit $\infty$ with $f_c$. Integrating $\cos(2\pi f t)$ with respect to $f$ while holding $t$ fixed produces the **sinc pulse**:

$$h_{\text{brick-wall}}(t) = 2\int_0^{f_c} \cos(2\pi f t)\,df = 2\left[\frac{\sin(2\pi f t)}{2\pi t}\right]_{f=0}^{f=f_c} = \frac{\sin(2\pi f_c t)}{\pi t}$$

At time zero, all surviving cosine waves from $0\text{ Hz}$ to $f_c$ align at $+1$ ($\cos 0$) to build a central peak of height $2f_c$. Away from time zero, abrupt removal of frequencies above $f_c$ leaves waves just below $f_c$ uncancelled: $\sin(2\pi f_c t)$ oscillates between $+1$ and $-1$ at rate $f_c$ while $1/(\pi t)$ decays slowly, creating artificial pre-cursor and post-cursor ringing ripples on both sides of the peak.

#### Smooth Bell-Curve Roll-Off and the Gaussian Pulse

Eliminating cutoff ringing requires tapering high frequencies smoothly instead of chopping them off at a hard wall. A **Gaussian bell-curve** spectrum $X(f)$ transforms into a self-reciprocal Gaussian bell curve $x(t)$ in the time domain:

$$X(f) = e^{-\pi (f/\sigma_f)^2}, \qquad x(t) = \int_{-\infty}^{\infty} e^{-\pi (f/\sigma_f)^2} e^{j 2\pi f t}\,df = \sigma_f\,e^{-\pi (\sigma_f t)^2}$$

Every point on $x(t)$ is strictly positive with no $\sin$ or $\cos$ oscillation factor, giving a Gaussian pulse (or Gaussian oscilloscope front-end filter) zero overshoot and zero side-lobe ringing. Placing bandwidth parameter $\sigma_f$ in the denominator of $(f/\sigma_f)^2$ and the numerator of $(\sigma_f t)^2$ shows that wider frequency bandwidth $\sigma_f$ produces a proportionally narrower pulse duration ($1/\sigma_f$).

#### Summary of Canonical Transform Pairs

Five canonical waveform-and-spectrum pairs recur throughout channel modeling, VNA/TDR conversion, and oscilloscope characterization:

| Time-Domain Waveform | Frequency-Domain Spectrum | Signal Integrity Significance |
|---|---|---|
| **Pure sine wave** | Single discrete spectral line at oscillation frequency $f_0$ | Serves as the shape-preserving eigenfunction of linear, time-invariant (LTI) channels during VNA frequency sweeps. |
| **Symmetric square wave** | Discrete spikes at fundamental $f_0$ and odd harmonics ($3f_0, 5f_0, \dots$) decaying as $1/k$; zero even harmonics | Models alternating `1010` clock and data patterns on high-speed links. |
| **Unit impulse** ($\delta(t)$) | Flat horizontal spectrum with equal amplitude density across all frequencies from $0\text{ Hz}$ to $\infty$ | Excites every frequency equally so the output spectrum equals the channel transfer function $H(f)$ directly. |
| **Sinc pulse** ($\frac{\sin(2\pi f_c t)}{\pi t}$) | Brick-wall low-pass spectrum flat up to cutoff $f_c$ and zero above $f_c$ | Exhibits oscillatory pre-cursor and post-cursor lobes extending before $t = 0$, showing that an abrupt brick-wall cutoff causes ringing. |
| **Gaussian pulse** ($\sigma_f e^{-\pi(\sigma_f t)^2}$) | Gaussian spectrum ($e^{-\pi(f/\sigma_f)^2}$) whose frequency width $\sigma_f$ scales inversely with pulse duration | Forms a self-reciprocal transform pair with zero overshoot and zero side-lobe ringing in both time and frequency domains. |

### Building a Step with a Finite Bandwidth

No real oscilloscope, VNA measurement, or channel simulation captures frequencies out to $\infty$; every measurement or filter stops at some maximum cutoff frequency $f_{\text{max}}$. Recalling the ideal $0\text{ V}$-to-$1\text{ V}$ step integral and passing it through a sharp brick-wall low-pass filter of cutoff $f_{\text{max}}$ truncate the upper integration limit from $\infty$ to $f_{\text{max}}$:

$$u(t) = \frac{1}{2} + \frac{1}{\pi}\int_0^{\infty} \frac{\sin(2\pi f t)}{f}\, df$$

$$u_{f_{\text{max}}}(t) = \frac{1}{2} + \frac{1}{\pi}\int_0^{f_{\text{max}}} \frac{\sin(2\pi f t)}{f}\, df$$

Differentiating $u_{f_{\text{max}}}(t)$ with respect to $t$ shows that the instantaneous **slope** of this band-limited step is the sinc pulse derived above:

$$\text{Slope}(t) = \frac{du_{f_{\text{max}}}(t)}{dt} = 2\int_0^{f_{\text{max}}} \cos(2\pi f t)\,df = \frac{\sin(2\pi f_{\text{max}} t)}{\pi t}$$

#### Midpoint Slope and Finite Rise Time

Evaluating the sinc slope of a $V_{\text{step}}$ ($1.0\text{ V}$) transition at the midpoint of the rising edge (in the limit as $t$ approaches $0$) via the small-angle sine approximation cancels $\pi t$ and fixes the peak edge slope at $2 f_{\text{max}} V_{\text{step}}$ (in $\text{V/s}$):

$$\text{Slope}(0) = V_{\text{step}} \lim_{t \to 0}\frac{\sin(2\pi f_{\text{max}} t)}{\pi t} = V_{\text{step}} \lim_{t \to 0}\frac{2\pi f_{\text{max}} t}{\pi t} = 2 f_{\text{max}} V_{\text{step}}$$

Spanning the $0.8\text{ V}$ window $\Delta V$ between $0.1\text{ V}$ ($10\%$) and $0.9\text{ V}$ ($90\%$) at that peak slope of $(2 f_{\text{max}})(1.0\text{ V})$ would take $0.40 / f_{\text{max}}$, and gentle sinc rounding near the $10\%$ and $90\%$ thresholds lengthens $t_r$ by roughly $11\%$:

$$\Delta V = 0.9\text{ V} - 0.1\text{ V} = 0.8\text{ V}, \qquad \frac{\Delta V}{2 f_{\text{max}} V_{\text{step}}} = \frac{0.40}{f_{\text{max}}}, \qquad t_r \approx \frac{0.45}{f_{\text{max}}}$$

For a $20\text{ GHz}$ brick-wall cutoff $f_{\text{max}}$, the step takes $22.5\text{ ps}$ ($0.45 / 20\text{ GHz}$) to climb from $0.1\text{ V}$ to $0.9\text{ V}$:

$$t_r \approx \frac{0.45}{20\text{ GHz}} = 22.5\text{ ps}$$

#### Truncation Overshoot and Ringing

The band-limited step keeps climbing while its sinc slope remains positive and hits its first peak at positive time $t_{\text{peak}}$ where the sinc numerator first reaches zero after time zero (at angle $\pi$, or $180^\circ$):

$$\sin(2\pi f_{\text{max}} t_{\text{peak}}) = 0 \implies 2\pi f_{\text{max}} t_{\text{peak}} = \pi \implies t_{\text{peak}} = \frac{1}{2 f_{\text{max}}}$$

The band-limited step peaks at half a cycle of $f_{\text{max}}$ rather than at the quarter-cycle ($90^\circ$) crest of $f_{\text{max}}$ alone because slower waves across the lower spectrum continue rising past that quarter-cycle mark. At a quarter cycle of $f_{\text{max}}$, every frequency component below $f_{\text{max}}$ sits between $0^\circ$ and $90^\circ$ with positive slope. Only at $t_{\text{peak}}$ does the downward slope of the upper half-band ($0.5\,f_{\text{max}}$ to $f_{\text{max}}$) balance the upward slope of the lower half-band ($0\text{ Hz}$ to $0.5\,f_{\text{max}}$).

Evaluating the truncated step integral at $t_{\text{peak}}$ reveals why the voltage overshoots $1.0\text{ V}$:

$$u_{f_{\text{max}}}(t_{\text{peak}}) = 0.5\text{ V} + \int_0^{f_{\text{max}}} \frac{1}{\pi f}\sin\!\left(\pi\frac{f}{f_{\text{max}}}\right)df \approx 0.5\text{ V} + 0.589\text{ V} = 1.089\text{ V}$$

At $t_{\text{peak}}$, every surviving wave up to $f_{\text{max}}$ has positive sine phase ($0^\circ$ to $180^\circ$) summing to $+0.589\text{ V}$. An infinite-bandwidth step also retains the band from $f_{\text{max}}$ to $2f_{\text{max}}$ ($180^\circ$ to $360^\circ$, negative sine), pulling $+0.589\text{ V}$ down by $-0.089\text{ V}$ to $+0.500\text{ V}$ ($1.000\text{ V}$ total). Truncating above $f_{\text{max}}$ removes that pullback group and creates an **$8.9\%$ (roughly $9\%$) overshoot** plus decaying ringing of period $1/f_{\text{max}}$; raising $f_{\text{max}}$ by $10\times$ shifts $t_{\text{peak}}$ earlier by $10\times$ without altering the $9\%$ overshoot height.

### Superposition and Phase: Why an Infinite Sum of Sine Waves Is Not Zero

A natural intuitive question is why adding infinitely many oscillating sine waves together produces a sharp step rather than averaging out to zero everywhere. The answer lies in **phase alignment**.

Summing thousands of sine waves whose phases $\phi(f)$ are chosen randomly causes their positive and negative peaks to collide at random instants, producing flat white noise with an average of zero and no coherent edges.

In the continuous step integral, the phases are not random: every single sine wave $\sin(2\pi f t)$ has zero initial phase $\phi(f)$ at time zero. That deterministic phase lock forces every frequency component across the spectrum to cross zero going upward at the identical instant (time zero). All of their positive slopes add together into a single step transition, while their differing periods cause them to cancel smoothly to $\pm 0.5\text{ V}$ at every other instant. Fourier synthesis reconstructs waveforms faithfully because the forward transform preserves both the amplitude $|X(f)|$ and the phase $\angle X(f)$ of every frequency component.

### How Many Harmonics Survive a Channel

Recalling the periodic square-wave series shows directly how channel bandwidth shapes a repeating digital pattern:

$$x_T(t) = \frac{1}{2} + \sum_{k=1, 3, 5, \dots}^{\infty} \frac{2}{\pi k}\sin(2\pi k f_0 t)$$

For an alternating `10101010` NRZ pattern at bit rate $R_{\text{bit}}$, the fundamental frequency $f_0$ equals $f_{\text{Nyquist}}$ and odd harmonics sit at odd integer multiples $k\,f_0$, so dividing channel bandwidth $BW$ by $f_0$ identifies the highest unattenuated odd harmonic $k_{\text{max}}$:

$$f_0 = f_{\text{Nyquist}} = \frac{R_{\text{bit}}}{2}, \qquad f_k = k\, f_0 \quad (k = 1, 3, 5, 7, \dots), \qquad k_{\text{max}} = \left\lfloor \frac{BW}{f_0} \right\rfloor_{\text{odd}}$$

Consider a $10\text{ Gbps}$ NRZ link (unit interval $\text{UI}$ of $100\text{ ps}$, fundamental $f_0$ of $5\text{ GHz}$) passing through a single-pole low-pass channel with $18\text{ GHz}$ half-power bandwidth $f_{3\text{dB}}$. Dividing $18\text{ GHz}$ by $5\text{ GHz}$ gives $3.6$, placing the $5\text{ GHz}$ fundamental and $15\text{ GHz}$ 3rd harmonic inside $f_{3\text{dB}}$ while attenuating higher harmonics gradually according to the single-pole magnitude curve:

$$|H(f)| = \frac{1}{\sqrt{1 + (f/f_{3\text{dB}})^2}}$$

$$\begin{aligned}
|H(5\text{ GHz})| &= \frac{1}{\sqrt{1 + (5/18)^2}} \approx 0.96, & |H(15\text{ GHz})| &= \frac{1}{\sqrt{1 + (15/18)^2}} \approx 0.77 \\
|H(25\text{ GHz})| &= \frac{1}{\sqrt{1 + (25/18)^2}} \approx 0.58, & |H(35\text{ GHz})| &= \frac{1}{\sqrt{1 + (35/18)^2}} \approx 0.46
\end{aligned}$$

Each surviving odd harmonic reshapes the received eye in a distinct geometric stage:

- **1st harmonic ($5\text{ GHz}$):** Keeps $96\%$ of its launched amplitude; alone, the fundamental forms a pure sine wave with rounded peaks and no flat plateau.
- **3rd harmonic ($15\text{ GHz}$):** Preserves $77\%$ of its launched amplitude, steepening the transition slopes and depressing the sine crest into a rounded trapezoid with roughly $23\text{ ps}$ rise time ($0.35 / 15\text{ GHz}$).
- **5th harmonic ($25\text{ GHz}$):** Passes $58\%$ of its launched amplitude, sharpening the plateau corners and tightening unobstructed rise time toward $14\text{ ps}$ ($0.35 / 25\text{ GHz}$).
- **7th harmonic ($35\text{ GHz}$):** Transmits $46\%$ of its modest $2/(7\pi)$ launched amplitude, adding fine corner definition.

Practical high-speed interconnect and oscilloscope designs typically target passing the 3rd to 5th harmonic of the Nyquist frequency. Passing the 1st harmonic alone leaves a sine wave, passing the 3rd harmonic forms a recognizable digital eye with a flat center, and passing the 5th harmonic produces crisp trapezoidal corners.

## Edge Cases

### The Gibbs Phenomenon

Truncating a Fourier series or integral abruptly at a sharp frequency cutoff $f_{\text{max}}$ produces an $8.9\%$ (roughly $9\%$) overshoot peak at $t_{\text{peak}}$ ($1 / (2f_{\text{max}})$) and decaying oscillatory ringing adjacent to every sharp transition, as derived in the finite-bandwidth step example above. This truncation artifact is called the **Gibbs phenomenon**.

In laboratory measurements, the Gibbs phenomenon has a direct physical consequence. An oscilloscope, anti-aliasing filter, or de-embedding algorithm whose frequency response cuts off steeply like a brick wall displays artificial $9\%$ overshoot and ringing on a fast step edge, even when the physical voltage on the PCB trace has zero overshoot. Conversely, an oscilloscope or channel with a gradual, Gaussian-like high-frequency roll-off tapers the higher harmonics smoothly instead of chopping them off abruptly, avoiding truncation overshoot. Signal integrity engineers must distinguish this **bandwidth-truncation ringing** (whose ringing period scales with instrument cutoff as $1 / f_{\text{max}}$) from **physical reflection ringing** caused by impedance mismatches and parasitic inductance ([Chapter 3](03_Impedance_Reflections_and_Termination.md)).

### Sampling, Aliasing, and Spectral Leakage

Digitizing a waveform on an oscilloscope at sampling rate $f_s$ and computing an FFT across an $N$-sample record of duration $T$ introduces two fundamental sampling boundaries:

$$f_s = \frac{1}{\Delta t}, \qquad T = N\,\Delta t$$

#### Aliasing from a Finite Sampling Rate

An **Analog-to-Digital Converter (ADC)** takes one discrete voltage snapshot $x[n]$ every $\Delta t$ seconds at sample timestamps $n / f_s$ without observing the wire between snapshots. Detecting an oscillating sinusoid requires at least **two samples per cycle** (one positive half-cycle sample and one negative half-cycle sample), setting the sampler's **Nyquist limit** at $f_s / 2$. A tone right at $f_s$ is sampled once every $360^\circ$ at identical voltage and mimics $0\text{ Hz}$ DC.

Any input frequency $f$ above $f_s / 2$ masquerades as a slower wave at the **alias frequency** $f_{\text{alias}}$. Shifting $f$ by an integer multiple $k f_s$ changes sample angle $n$ by $2\pi k n$ (full $360^\circ$ turns), while even cosine symmetry folds negative frequencies onto positive ones:

$$x[n] = \cos\!\left(2\pi\frac{f}{f_s}n\right) = \cos\!\left(2\pi\frac{|f - k f_s|}{f_s}n\right) \quad \implies \quad f_{\text{alias}} = |f - k f_s|$$

On a $10\text{ GHz}$ sampler ($5\text{ GHz}$ Nyquist limit), a $5.001\text{ GHz}$ tone advances $180.036^\circ$ per sample and aliases to $4.999\text{ GHz}$, while a $9\text{ GHz}$ tone advances $324^\circ$ per sample and aliases to $1\text{ GHz}$:

$$f_{\text{alias}}(5.001\text{ GHz}) = |5.001 - 10| = 4.999\text{ GHz}, \qquad f_{\text{alias}}(9\text{ GHz}) = |9 - 10| = 1\text{ GHz}$$

The Nyquist limit $f_s / 2$ acts like a **folding crease** that mirrors $f_s / 2 + \Delta f$ onto $f_s / 2 - \Delta f$, where post-ADC software can never separate aliased energy from true baseband signals. Real-time oscilloscopes place a physical analog anti-aliasing low-pass filter ahead of the ADC and sample well above $2 f_{3\text{dB}}$ so the analog filter rolls off cleanly below $f_s / 2$.

#### Spectral Leakage from a Non-Periodic Capture Window

The DFT evaluates integer harmonics $k / T$ of record duration $T$, inherently treating the captured $N$-sample window as one period of an infinitely repeating loop. A sine wave completing an integer number of cycles inside $T$ joins smoothly end-to-end and concentrates all energy into a single FFT bin $k$. Ending mid-cycle (such as $1.25$ cycles from $0\text{ V}$ at start to $+1.0\text{ V}$ at $T$) pastes mismatched endpoints into a sharp seam, forcing high-frequency bins to synthesize the discontinuity (**spectral leakage**).

How rapidly leaked energy decays across distant bins depends on boundary smoothness, because each time derivative of $\sin(2\pi f t)$ pulls out an additional power of $2\pi f$:

$$\frac{d}{dt}\sin(2\pi f t) = (2\pi f)\cos(2\pi f t), \qquad \frac{d^2}{dt^2}\sin(2\pi f t) = -(2\pi f)^2\sin(2\pi f t), \qquad \frac{d^3}{dt^3}\sin(2\pi f t) = -(2\pi f)^3\cos(2\pi f t)$$

- **Voltage Jump ($1/f$ Leakage, $-20\text{ dB/decade}$):** A vertical endpoint mismatch $\Delta V$ between $v(T)$ and $v(0)$ introduces a zeroth-derivative seam whose required high-frequency amplitudes decay slowly as $1/f$ ($0.1\times$ at $10\times$ frequency).
- **Slope Jump ($1/f^2$ Leakage, $-40\text{ dB/decade}$):** A V-shaped slope kink at matched endpoint voltages, where $\frac{dv(t)}{dt}$ at $T$ differs from $\frac{dv(t)}{dt}$ at $0$ (as in a $1.5$-cycle capture), shifts the seam to the first derivative and decays leaked amplitudes as $1/f^2$ ($0.01\times$ at $10\times$ frequency).
- **Curvature Jump ($1/f^3$ Leakage, $-60\text{ dB/decade}$):** A smooth endpoint join with matched voltage and matched slope leaves only a second-derivative curvature seam, shrinking leaked amplitudes rapidly as $1/f^3$ ($0.001\times$ at $10\times$ frequency).

#### Suppressing Leakage with Smooth Window Functions

Oscilloscopes suppress spectral leakage without knowing $v(0)$ or $v(T)$ in advance by multiplying the captured record $v(t)$ point-by-point by a smooth **window function** $w_{\text{win}}(t)$ (subscripted so bare $w$ remains reserved for trace width), such as a Blackman-Harris window or the Hann cosine-arch window:

$$w_{\text{win}}(t) = \frac{1}{2}\left(1 - \cos\frac{2\pi t}{T}\right)$$

The window acts like a volume fader that rises from $0\%$ at time zero to $100\%$ at midpoint $T/2$ and fades back to $0\%$ at $T$. Zero window height and zero window slope at both endpoints force both the windowed waveform $v(t)\,w_{\text{win}}(t)$ and its first time derivative to vanish at $0$ and $T$ via the product rule, eliminating $1/f$ and $1/f^2$ leakage so side lobes fall at $1/f^3$ ([Chapter 12](12_Test_Patterns_and_Jitter_Isolation.md)):

$$w_{\text{win}}(0) = w_{\text{win}}(T) = 0, \qquad \left.\frac{dw_{\text{win}}(t)}{dt}\right|_{t=0, T} = 0$$

$$\left.\frac{d}{dt}\big[v(t)\,w_{\text{win}}(t)\big]\right|_{t=0, T} = \left.\left(\frac{dv(t)}{dt}\,w_{\text{win}}(t) + v(t)\,\frac{dw_{\text{win}}(t)}{dt}\right)\right|_{t=0, T} = 0$$

### The DC Component and Amplitude Independence

In any linear, time-invariant (LTI) channel, the normalized spectral shape of an edge depends on its transition time $t_r$ and waveform geometry, not on voltage swing. Stepping from $0\text{ V}$ to $0.5\text{ V}$, from $0\text{ V}$ to $1.0\text{ V}$, or from $0\text{ V}$ to $3.3\text{ V}$ with the identical $20\text{ ps}$ rise time merely scales the DC offset $a_0$ and multiplies every frequency component by the same constant voltage factor. An LTI channel scales its output spectrum $Y(f)$ by that identical factor, so a $17.5\text{ GHz}$ channel is required to preserve a $20\text{ ps}$ edge across both a $400\text{ mV}$ low-swing SerDes link and a $3.3\text{ V}$ logic swing.

### When Fourier Analysis Breaks Down

Frequency-by-frequency multiplication of $H(f)$ by $X(f)$ relies strictly on channel **linearity** so superposition holds and distinct frequencies never exchange energy. In a linear channel (passive copper traces, dielectric substrates, resistors, and capacitors at normal signaling voltages), a pure input cosine wave at $f_1$ emerges scaled by $|H(f_1)|$ and phase-shifted by $\angle H(f_1)$ with zero new frequencies created:

$$v_{\text{out}}(t) = |H(f_1)|\cos\!\big(2\pi f_1 t + \angle H(f_1)\big)$$

Active or nonlinear elements violate superposition; common examples include CMOS output transistors compressing near the supply rails, ESD protection diodes clamping above $0.7\text{ V}$, saturating magnetic cores, and decision-feedback equalizers (DFEs) making thresholded bit decisions. Bending or clipping the transfer curve adds squared, cubed, and higher-power distortion terms to the output:

$$v_{\text{out}}(t) = \underbrace{a_1\,v_{\text{in}}(t)}_{\text{Linear term}} + \underbrace{a_2\,v_{\text{in}}^2(t) + a_3\,v_{\text{in}}^3(t) + \dots}_{\text{Nonlinear distortion terms}}$$

#### Symmetrical Peak Clipping and Odd Harmonics

Equal compression of both the positive peak ($90^\circ$) and negative trough ($270^\circ$) of a fundamental sine wave $f_1$ flattens both extremes toward a square wave. Across the $0.5$-cycle separation between $90^\circ$ and $270^\circ$ of $f_1$, an odd harmonic such as $3f_1$ completes $1.5$ cycles (flipping sign) to push the top peak down and the bottom trough up symmetrically, emerging algebraically from the cubic distortion term via double-angle and product-to-sum identities:

$$\cos^2\theta = \frac{1}{2} + \frac{1}{2}\cos(2\theta), \qquad \cos(2\theta)\cos\theta = \frac{1}{2}\cos\theta + \frac{1}{2}\cos(3\theta)$$

$$v_{\text{in}}^3(t) = \cos^3(2\pi f_1 t) = \frac{3}{4}\cos(2\pi f_1 t) + \frac{1}{4}\cos\!\big(2\pi(3f_1)t\big)$$

#### Asymmetrical Peak Clipping and Even Harmonics

Unequal compression between top and bottom waveform halves (such as an ESD diode clamping one polarity or mismatched NMOS pull-down and PMOS pull-up transistor strengths) flattens one peak more than the other. Across the $0.5$-cycle separation of $f_1$, an even harmonic such as $2f_1$ completes $1.0$ full cycle without flipping sign, shifting both extremes in the same vertical direction via the squared distortion term:

$$v_{\text{in}}^2(t) = \cos^2(2\pi f_1 t) = \frac{1}{2} + \frac{1}{2}\cos\!\big(2\pi(2f_1)t\big)$$

Real active drivers exhibit symmetrical rail compression ($3f_1, 5f_1, \dots$) and pull-up/pull-down asymmetry ($2f_1, 4f_1, \dots$) simultaneously.

#### Two-Tone Mixing and Intermodulation Products

Driving two simultaneous tones ($f_1$ and $f_2$) into a nonlinear device lets the first wave compress the transistor and modulate the gain experienced by the second wave. Expanding $(A + B)^2$ inside $v_{\text{in}}^2(t)$ produces a $2AB$ cross-term that splits via the product-to-sum identity into brand-new **sum and difference intermodulation frequencies** ($f_1 + f_2$ and $f_1 - f_2$):

$$v_{\text{in}}(t) = \cos(2\pi f_1 t) + \cos(2\pi f_2 t), \qquad (A + B)^2 = A^2 + 2AB + B^2$$

$$2\cos(2\pi f_1 t)\cos(2\pi f_2 t) = \cos\!\big(2\pi(f_1 - f_2)t\big) + \cos\!\big(2\pi(f_1 + f_2)t\big)$$

#### Why Fixed Transfer Functions Fail Under Nonlinearity

Linear transfer multiplication evaluates each frequency bin in isolation by multiplying $X(f)$ at frequency $f$ by $H(f)$. For a pure $1\text{ GHz}$ input tone $f_1$, the input spectrum at $2\text{ GHz}$ and $3\text{ GHz}$ is identically zero, so any fixed linear transfer function $H(f)$ predicts zero output at every harmonic:

$$X(2\text{ GHz}) = 0, \quad X(3\text{ GHz}) = 0 \quad \implies \quad Y(2\text{ GHz}) = H(2\text{ GHz}) \times 0 = 0$$

A fixed linear transfer function $H(f)$ can never describe a nonlinear circuit that transfers energy from $1\text{ GHz}$ into newly generated frequencies ($2\text{ GHz}$, $3\text{ GHz}$, or $f_1 \pm f_2$). An FFT can still decompose the distorted output waveform after the fact, while predicting that output requires time-domain circuit simulation or hybrid statistical-time-domain modeling.

[Chapter 3](03_Impedance_Reflections_and_Termination.md) applies these time- and frequency-domain tools to the first physical obstacle every wavefront encounters on a board: a change in characteristic impedance, deriving how wavefronts reflect at boundaries and how parasitic capacitances and inductances filter the edge spectrum derived here.

<p><em>Prefer to read this offline? <a href="../assets/docs/signal-integrity-vol1-ebook-v2.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Signal Integrity Volume 1 Ebook here.</a></em></p>
