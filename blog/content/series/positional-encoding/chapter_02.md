# Part 2: Design Constraints and the Sinusoidal Formula

<!-- SUMMARY: Five mathematical constraints define the requirements for a positional encoding: uniqueness, boundedness, determinism, smoothness, and relative representability. The sinusoidal formula from Vaswani et al. (2017) satisfies all five. This chapter derives the formula, computes every entry of the positional encoding matrix for the toy model, and verifies each constraint against the computed values. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter demonstrated that the embedding tensor $X$ is invariant under row permutations: reordering the sequence rearranges the similarity matrix without altering any similarity score. A mechanism is needed that assigns a distinct, position-dependent vector to each location in the sequence, such that incorporating these vectors into the embedding breaks the permutation symmetry.

This mechanism cannot be arbitrary. A random vector assigned to each position would break permutation invariance, but it would also inject noise that disrupts downstream computation. The positional encoding must satisfy a precise set of mathematical constraints to be useful.

## The Five Constraints

A positional encoding is a function $\mathbf{p}: \mathbb{Z}_{\geq 0} \rightarrow \mathbb{R}^{d_{model}}$. The notation $\mathbb{Z}_{\geq 0}$ denotes the set of non-negative integers $\{0, 1, 2, 3, \ldots\}$: every possible position index in a sequence. The codomain $\mathbb{R}^{d_{model}}$ is the same vector space that the embedding vectors occupy (for the toy model, $\mathbb{R}^3$). The function takes a single non-negative integer $t$ and returns a $d_{model}$-dimensional vector $\mathbf{p}(t)$: one encoding vector per position. For the toy sequence `The` `quick` `brown` `fox`, the position indices are $t \in \{0, 1, 2, 3\}$, and the function produces four vectors: $\mathbf{p}(0)$ for the position occupied by `The`, $\mathbf{p}(1)$ for `quick`, $\mathbf{p}(2)$ for `brown`, and $\mathbf{p}(3)$ for `fox`.

The position index $t$ is distinct from the indices $i$ and $j$ used in Chapter 1 to label rows and columns of the similarity matrix $S_{ij} = \mathbf{x}_i^\top \mathbf{x}_j$. Here, $t$ labels a single position in the sequence. Later in this chapter, $i$ will be reused with a different meaning: the dimension pair index in the sinusoidal formula. Five constraints govern the design of this function.

### Constraint 1: Uniqueness

Each position $t$ must map to a distinct vector. If $\mathbf{p}(t_1) = \mathbf{p}(t_2)$ for $t_1 \neq t_2$, the encoding cannot distinguish those two positions, and permutation invariance between them persists. Formally:

$$
t_1 \neq t_2 \implies \mathbf{p}(t_1) \neq \mathbf{p}(t_2)
$$

### Constraint 2: Boundedness

The values of $\mathbf{p}(t)$ must remain bounded, regardless of $t$. If positional encoding values grow with position, adding them to the embedding vectors would distort the magnitude of embeddings at later positions, overwhelming the semantic signal with a positional artifact.

The notation $p_k(t)$ denotes the $k$-th component of the vector $\mathbf{p}(t)$, where $k \in \{0, 1, \ldots, d_{model} - 1\}$ indexes the individual dimensions of the encoding vector (for the toy model, $k \in \{0, 1, 2\}$). The index $k$ is introduced here rather than reusing $i$ or $j$ because $i$ will serve as the dimension pair index in the sinusoidal formula later in this chapter, and $j$ already indexes columns in the similarity matrix from Chapter 1. The constraint requires that every component of every positional encoding vector remains bounded:

$$
|\,p_k(t)\,| \leq 1 \quad \text{for all } t, k
$$

The specific bound $[-1, 1]$ is chosen to match the scale of the embedding components. The toy model's embedding matrix $X$ contains values ranging from $-0.8$ to $0.9$, all within this interval. In production models, layer normalization constrains embedding components to a comparable magnitude. Because the positional encoding is added element-wise to the embedding (as derived in Chapter 3), the two signals must be of the same order: a positional encoding bounded in $[-1, 1]$ contributes a signal commensurate with the semantic content. A wider bound would allow the positional signal to dominate the embedding; a narrower bound would render it negligible.

### Constraint 3: Determinism

The encoding must be a fixed, deterministic function of position, not a set of learned parameters. A learned positional embedding (a trainable matrix $W_P \in \mathbb{R}^{T_{max} \times d_{model}}$) introduces $T_{max} \times d_{model}$ additional parameters and imposes a hard maximum sequence length $T_{max}$. Because each position's vector is an independent parameter, the mechanism cannot generalize to positions unseen during training: if a model is trained exclusively on sequences up to $1024$ tokens, it possesses no vector for position $1024$ during inference, and lacks a mathematical rule to generate one. A deterministic function avoids these limitations: it requires no training, imposes no maximum length, and evaluates validly for any position index $t$ on demand.

### Constraint 4: Smoothness

Nearby positions should produce nearby encoding vectors. If $\mathbf{p}(t)$ and $\mathbf{p}(t+1)$ are distant in $\mathbb{R}^{d_{model}}$, the encoding treats adjacent positions as unrelated. This discards the assumption that sequential proximity implies structural relevance: words located next to each other are structurally more related than words separated by a large distance. Formally, the Euclidean distance $\|\mathbf{p}(t) - \mathbf{p}(t+1)\|$ should be small relative to $\|\mathbf{p}(t) - \mathbf{p}(t+\Delta)\|$ for offset $\Delta > 1$.

### Constraint 5: Relative Representability

The relationship between any two positions $t$ and $t + \Delta$ should be expressible as a fixed linear transformation that depends only on the offset $\Delta$, not on the absolute positions. This means there exists a matrix $M_\Delta$ (independent of $t$) such that:

$$
\mathbf{p}(t + \Delta) = M_\Delta \, \mathbf{p}(t)
$$

This constraint enables the model to learn relative positional relationships (the token 3 positions ahead) rather than memorizing absolute position labels (position 7). Relative relationships generalize across different positions in the sequence and across different sequence lengths.

## Trigonometric Functions as the Natural Solution

The five constraints collectively point to a narrow family of functions. The requirements of boundedness ($[-1, 1]$) and smoothness (continuous, nearby outputs for nearby inputs) immediately suggest periodic functions with bounded range. The requirement of determinism excludes learned parameters. The requirement of uniqueness excludes any single periodic function (which repeats values), but a vector of periodic functions at different frequencies can produce unique combinations across all positions, much as a vector of clock hands at different speeds (seconds, minutes, hours) uniquely identifies any moment in the day.

Trigonometric functions ($\sin$ and $\cos$) satisfy the first four constraints by construction:

- **Bounded** in $[-1, 1]$ for all inputs.
- **Smooth** (infinitely differentiable).
- **Deterministic** (fixed functions with no parameters).
- **Unique** when combined at multiple frequencies (the vector of values at different frequencies produces a distinct fingerprint for each position).

The fifth constraint (relative representability) is the decisive one. The angle-addition identities for sine and cosine provide the required linear transformation. For a single frequency $\omega$, the value at an offset position $t + \Delta$ expands algebraically into cross-terms:

$$
\sin(\omega(t + \Delta)) = \sin(\omega t)\cos(\omega \Delta) + \cos(\omega t)\sin(\omega \Delta)
$$

$$
\cos(\omega(t + \Delta)) = \cos(\omega t)\cos(\omega \Delta) - \sin(\omega t)\sin(\omega \Delta)
$$

This system of equations can be factored into a matrix multiplication applied to the vector at position $t$:

$$
\begin{bmatrix} \sin(\omega(t + \Delta)) \\ \cos(\omega(t + \Delta)) \end{bmatrix} = \begin{bmatrix} \cos(\omega \Delta) & \sin(\omega \Delta) \\ -\sin(\omega \Delta) & \cos(\omega \Delta) \end{bmatrix} \begin{bmatrix} \sin(\omega t) \\ \cos(\omega t) \end{bmatrix}
$$

The $2 \times 2$ matrix on the right depends exclusively on the offset $\Delta$ and the frequency $\omega$, completely independent of the absolute position $t$. This is the standard formulation of a two-dimensional rotation matrix. Shifting the position index from $t$ to $t + \Delta$ increases the function's argument by exactly $\omega \Delta$. Geometrically, adding an angle to a vector's current angular position is the definition of a rotation. Thus, advancing the sequence position is mathematically equivalent to rotating the vector $[\sin, \cos]^\top$ by an angle of $\omega \Delta$. 

Trigonometric functions are the unique solution to this constraint. Mathematically, the only continuous functions that can translate an additive shift ($t + \Delta$) into a fixed linear transformation (a matrix multiplication independent of $t$) are exponential functions and sinusoids. Because real exponentials either explode to infinity or decay to zero (violating the boundedness constraint), sinusoids remain as the sole elementary function family capable of providing this translation-invariant property while maintaining a stable magnitude.

## The Sinusoidal Positional Encoding Formula

Vaswani et al. (2017) defined the positional encoding as follows. For position index $t$ and dimension pair index $i$:

$$
PE(t, 2i) = \sin\!\left(\frac{t}{10000^{\,2i\,/\,d_{model}}}\right)
$$

$$
PE(t, 2i+1) = \cos\!\left(\frac{t}{10000^{\,2i\,/\,d_{model}}}\right)
$$

The formula requires two independent variables to compute a specific entry in the $T \times d_{model}$ positional encoding matrix:

- $t \in \{0, 1, \ldots, T-1\}$ is the **position index** (the matrix row). It identifies where the token sits in the sequence. To encode a single position $t$, the formula must generate an entire $d_{model}$-dimensional vector.
- $i$ is the **dimension pair index** (the matrix column pair). It sweeps across the dimensions of the vector being generated. The maximum $i$ is determined by halving $d_{model}$ and zero-indexing. For a production architecture with $d_{model} = 128$, the index ranges from $i = 0$ through $i = 63$. Each increment of $i$ fills two adjacent columns: an even dimension $2i$ with a sine evaluation, and an odd dimension $2i+1$ with a cosine evaluation.
- $d_{model}$ is the **embedding dimension**, which dictates the total number of frequencies needed.
- $10000$ is a **base constant** that determines the minimum frequency.

The argument to the trigonometric functions can be written as $t \cdot \omega_i$, where the **angular frequency** for pair $i$ is:

$$
\omega_i = \frac{1}{10000^{\,2i\,/\,d_{model}}}
$$

As the column pair index $i$ increases, the exponent $2i / d_{model}$ increases, the denominator grows, and the frequency $\omega_i$ decreases. The first dimension pair ($i = 0$) oscillates rapidly with a wavelength of $2\pi \approx 6.28$ positions. The final dimension pair oscillates extremely slowly, taking approximately $2\pi \cdot 10000 \approx 62{,}832$ positions to complete a single cycle. 

This spectrum of frequencies allows the encoding to operate at multiple scales simultaneously. The rapid oscillations act as a fine-grained signal, pinpointing exact local offsets (separating adjacent positions). The slow oscillations act as a coarse-grained signal, identifying broad regional placement (distinguishing the beginning of a document from the end).

## Wavelengths for the Toy Model ($d_{model} = 3$)

For $d_{model} = 3$, the individual vector components are indexed by $k \in \{0, 1, 2\}$. The formula populates these components by iterating the pair index $i$:

**Pair $i = 0$ (dimensions 0 and 1):**

$$
\omega_0 = \frac{1}{10000^{\,0/3}} = \frac{1}{10000^0} = \frac{1}{1} = \mathbf{1}
$$

The wavelength (the number of positions for one complete cycle) is:

$$
\lambda_0 = \frac{2\pi}{\omega_0} = \frac{2\pi}{1} = 2\pi \approx 6.2832 \text{ positions}
$$

Dimension 0 receives $\sin(t \cdot 1) = \sin(t)$, and dimension 1 receives $\cos(t \cdot 1) = \cos(t)$. This is the fastest oscillation: the sine and cosine values cycle through a full period every $\approx 6.28$ positions.

**Pair $i = 1$ (dimension 2 only, the odd-dimension edge case):**

$$
\omega_1 = \frac{1}{10000^{\,2/3}} = \frac{1}{464.1589} \approx \mathbf{0.002154}
$$

The wavelength is:

$$
\lambda_1 = \frac{2\pi}{\omega_1} = 2\pi \cdot 10000^{2/3} = 2\pi \cdot 464.1589 \approx 2916.40 \text{ positions}
$$

Because $d_{model} = 3$ is odd, the second pair is incomplete. Dimension $2i = 2$ exists and receives $\sin(t \cdot \omega_1)$, but the corresponding cosine component would require dimension $2i + 1 = \mathbf{3}$. Because the vector only has three dimensions (indexed 0, 1, and 2), this cosine component has no dimension to occupy.

The sinusoidal formula allocates frequencies in sine-cosine pairs precisely because of the algebraic expansion derived in Constraint 5. To express a relative positional offset as a rotation, the mechanism must compute a linear combination of two orthogonal components. As established by the identity $\sin(\omega(t + \Delta)) = \sin(\omega t)\cos(\omega \Delta) + \cos(\omega t)\sin(\omega \Delta)$, the unshifted cosine component $\cos(\omega t)$ is strictly required to determine the shifted sine value. Because the two components are algebraically entangled, the rotation cannot be performed without evaluating both a sine and a cosine at the same frequency. 

When an architecture specifies an odd embedding dimension, the dimension count cannot accommodate full pairs. The final frequency is structurally truncated to a solitary sine component. Without its paired cosine, this final dimension cannot undergo 2D rotation and thus fails the relative representability constraint. Production architectures universally avoid this structural failure by specifying even dimensions (typically multiples of 64 or 128 per attention head).

The slow rate of change in dimension 2 is determined entirely by its assigned frequency, independent of the truncation. For this dimension, the pair index is $i = 1$, which yields the constant frequency $\omega_1 \approx 0.002154$. As the formula evaluates sequence positions from row $t = 0$ to row $t = 3$, this constant frequency is multiplied by the row index to produce the argument for the sine function ($t \cdot \omega_1$). Because the frequency is so small, the resulting argument grows extremely slowly: from $0$ at the first position to just $3 \times 0.002154 \approx 0.006463$ radians at the final position. For angles this small, the sine function is nearly linear ($\sin(\theta) \approx \theta$). Consequently, dimension 2 contains values very close to zero that increase steadily, acting as a coarse positional signal across the sequence.

## Computing the Positional Encoding Matrix

The positional encoding matrix $PE \in \mathbb{R}^{4 \times 3}$ has one row per position ($t \in \{0, 1, 2, 3\}$) and one column per dimension. To prevent the reader from having to constantly cross-reference the general formula and the wavelength derivations, the specific formula for each of the three columns is instantiated here using the computed frequencies ($\omega_0 = 1$ and $\omega_1 \approx 0.002154$):

- **Dimension 0** ($i= 0$, even): $PE(t, 0) = \sin(t \cdot \omega_0) = \sin(t \cdot 1)$
- **Dimension 1** ($i= 0$, odd): $PE(t, 1) = \cos(t \cdot \omega_0) = \cos(t \cdot 1)$
- **Dimension 2** ($i= 1$, even): $PE(t, 2) = \sin(t \cdot \omega_1) = \sin(t \cdot 0.002154)$

These three column formulas are evaluated for each row index $t$ to produce the full matrix.

### Position $t = 0$

Substituting $t = 0$ into the three column formulas:

$$
PE(0, 0) = \sin(0 \cdot 1) = \sin(0) = \mathbf{0.0000}
$$

$$
PE(0, 1) = \cos(0 \cdot 1) = \cos(0) = \mathbf{1.0000}
$$

$$
PE(0, 2) = \sin(0 \cdot 0.002154) = \sin(0) = \mathbf{0.0000}
$$

Position 0 receives the vector $\begin{bmatrix} 0 & 1 & 0 \end{bmatrix}$. The sine components are zero at the origin, and the cosine component is at its maximum. These are exact values, not approximations.

### Position $t = 1$

Substituting $t = 1$ into the three column formulas:

$$
PE(1, 0) = \sin(1 \cdot 1) = \sin(1) = \mathbf{0.8415}
$$

$$
PE(1, 1) = \cos(1 \cdot 1) = \cos(1) = \mathbf{0.5403}
$$

$$
PE(1, 2) = \sin(1 \cdot 0.002154) = \sin(0.002154) = \mathbf{0.0022}
$$

The first dimension pair ($\sin(1)$, $\cos(1)$) has moved substantially from its starting point. The argument is 1 radian, approximately $57.3°$ of the $2\pi$-radian cycle. The third dimension has barely moved: $\sin(0.002154) \approx \mathbf{0.002154}$, reflecting the extremely long wavelength of the second frequency.

### Position $t = 2$

Substituting $t = 2$ into the three column formulas:

$$
PE(2, 0) = \sin(2 \cdot 1) = \sin(2) = \mathbf{0.9093}
$$

$$
PE(2, 1) = \cos(2 \cdot 1) = \cos(2) = \mathbf{-0.4161}
$$

$$
PE(2, 2) = \sin(2 \cdot 0.002154) = \sin(0.004309) = \mathbf{0.0043}
$$

At 2 radians ($\approx 114.6°$), the cosine component has crossed zero and turned negative, while the sine component is near its maximum. The third dimension has increased by another increment of approximately $0.002154$, remaining close to zero.

### Position $t = 3$

Substituting $t = 3$ into the three column formulas:

$$
PE(3, 0) = \sin(3 \cdot 1) = \sin(3) = \mathbf{0.1411}
$$

$$
PE(3, 1) = \cos(3 \cdot 1) = \cos(3) = \mathbf{-0.9900}
$$

$$
PE(3, 2) = \sin(3 \cdot 0.002154) = \sin(0.006463) = \mathbf{0.0065}
$$

At 3 radians ($\approx 171.9°$), the sine has dropped back toward zero (it will reach zero at $\pi \approx 3.14$), and the cosine is near its negative extreme. The third dimension continues its near-linear ascent.

### The Complete Positional Encoding Matrix

$$
PE = \begin{bmatrix} \phantom{-}0.0000 & \phantom{-}1.0000 & \phantom{-}0.0000 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & \phantom{-}0.0022 \\ \phantom{-}0.9093 & -0.4161 & \phantom{-}0.0043 \\ \phantom{-}0.1411 & -0.9900 & \phantom{-}0.0065 \end{bmatrix}_{4 \times 3}
$$

Each row is the positional encoding vector for the corresponding position. Row 0 encodes position 0 (the location of `The` in the toy sequence), row 1 encodes position 1 (`quick`), row 2 encodes position 2 (`brown`), and row 3 encodes position 3 (`fox`). The first two columns oscillate rapidly with the pattern of $\sin(t)$ and $\cos(t)$. The third column changes by approximately $0.002$ per position, reflecting the slow frequency $\omega_1 \approx 0.002154$.

## Verification Against the Design Constraints

### Uniqueness

To verify uniqueness, let $\mathbf{p}_t$ denote the positional encoding vector for position $t$ (row $t$ of the $PE$ matrix). The Euclidean distance between any two vectors is zero if and only if the vectors are mathematically identical. Therefore, demonstrating that the distance between every pair of rows is strictly positive proves that no two rows are the same.

For example, the distance between the vectors for position 0 and position 1 is computed by summing the squared differences of their components and taking the square root:

$$
\|\mathbf{p}_0 - \mathbf{p}_1\| = \sqrt{(0.0000 - 0.8415)^2 + (1.0000 - 0.5403)^2 + (0.0000 - 0.0022)^2}
$$
$$
\|\mathbf{p}_0 - \mathbf{p}_1\| = \sqrt{0.7081 + 0.2113 + 0.0000} \approx \mathbf{0.9589}
$$

Computing the distances between all six possible pairs of rows yields:

| Pair (Offset) | Distance |
|---|---|
| $\|\mathbf{p}_0 - \mathbf{p}_1\|$ ($\Delta = 1$) | $0.9589$ |
| $\|\mathbf{p}_0 - \mathbf{p}_2\|$ ($\Delta = 2$) | $1.6829$ |
| $\|\mathbf{p}_0 - \mathbf{p}_3\|$ ($\Delta = 3$) | $1.9950$ |
| $\|\mathbf{p}_1 - \mathbf{p}_2\|$ ($\Delta = 1$) | $0.9589$ |
| $\|\mathbf{p}_1 - \mathbf{p}_3\|$ ($\Delta = 2$) | $1.6829$ |
| $\|\mathbf{p}_2 - \mathbf{p}_3\|$ ($\Delta = 1$) | $0.9589$ |

Every distance is strictly positive, confirming uniqueness. Furthermore, the distances reveal a specific pattern: pairs separated by the same relative offset $\Delta$ share the identical distance (e.g., all adjacent positions where $\Delta = 1$ are exactly $0.9589$ units apart). 

This regularity is a geometric consequence of the rotation structure. Each dimension pair traces a path along a 2D circle at its assigned frequency. The complete encoding vector, composed of multiple pairs, traces a path on a high-dimensional torus (the mathematical product of multiple circles). Because shifting position by an offset $\Delta$ applies a fixed rotational angle to each circle, a shift of $\Delta$ always translates the point by a constant Euclidean distance across the surface of the torus, independent of the absolute starting position $t$.

### Boundedness

Every entry of $PE$ lies in $[-1, 1]$. The minimum value is $-0.9900$ (dimension 1, position 3), and the maximum is $1.0000$ (dimension 1, position 0). This bound holds for all positions, not just $t \in \{0, 1, 2, 3\}$. Geometrically, the trigonometric functions represent the $y$ and $x$ coordinates of a point traversing the unit circle (a circle with a radius of exactly 1). Because the radius is 1, no coordinate can ever exceed 1 or fall below $-1$. This structural property ensures that the output of $\sin(x)$ and $\cos(x)$ for any arbitrary real input $x$ is strictly bounded by $[-1, 1]$, perfectly satisfying the constraint.

### Determinism

Every entry of $PE$ was computed from the closed-form formula $\sin(t \cdot \omega_i)$ or $\cos(t \cdot \omega_i)$ with fixed constants ($\omega_0 = 1$, $\omega_1 \approx 0.002154$). No training was involved, no data was consulted, and the values are identical on every evaluation. Position $t = 2$ always receives the vector $\begin{bmatrix} \phantom{-}0.9093 & -0.4161 & \phantom{-}0.0043 \end{bmatrix}$, regardless of the sequence content or length.

### Smoothness

The Euclidean distances between adjacent positions are:

$$
\|\mathbf{p}_0 - \mathbf{p}_1\| = 0.9589, \quad \|\mathbf{p}_1 - \mathbf{p}_2\| = 0.9589, \quad \|\mathbf{p}_2 - \mathbf{p}_3\| = 0.9589
$$

These are smaller than the distances between non-adjacent positions ($1.6829$ for $\Delta = 2$, $1.9950$ for $\Delta = 3$). Nearby positions produce nearby encoding vectors, and the distance increases monotonically with the offset. The equal spacing of adjacent distances follows from the constant angular step on the unit circle traced by the first dimension pair.

### Relative Representability

As derived in the trigonometric motivation above, shifting position by $\Delta$ applies a fixed linear transformation (a rotation by angle $\omega_i \Delta$) to each dimension pair. The transformation depends only on $\Delta$, not on the absolute position $t$. This property is inherited directly from the angle-addition identities for sine and cosine and will be verified numerically in a later chapter.

## Looking Forward

The positional encoding matrix $PE$ is now fully computed. Each of its four rows is a three-dimensional vector that uniquely identifies a position in the sequence. The next chapter adds this matrix element-wise to the embedding tensor $X$ from Chapter 1, producing the positionally-enriched tensor $X_{pos} = X + PE$ whose similarity matrix is no longer invariant under row permutations.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
