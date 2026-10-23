# Part 5: Rotary Position Embeddings: Deriving the Rotation Matrix

<!-- SUMMARY: Rotary Position Embeddings (RoPE) encode position by rotating query and key vectors rather than adding to embeddings. This chapter derives the rotation matrix from complex number multiplication, shows how individual dimension-pair rotations combine into a block-diagonal matrix, handles the odd-dimension edge case for the toy model, and computes the angular frequency that will drive the rotations in the next chapter. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter identified the structural failure of additive positional encoding in the query-key dot product: the cross-terms between content and position depend on absolute position indices, not on relative offsets. The preview at the end of that chapter stated that Rotary Position Embeddings (RoPE) encode position by rotating query and key vectors after projection, and that the dot product of rotated vectors depends only on relative position by construction.

This chapter derives the rotation matrix that performs this encoding. The derivation begins with complex number multiplication (the conceptual foundation), recovers the real-valued rotation matrix (the computational mechanism), handles the odd-dimension edge case for the toy model, and computes the angular frequency $\theta_0$ that drives the rotations. Chapter 6 then evaluates the rotation matrix at every position to transform the query and key vectors, and Chapter 7 proves that the resulting dot product depends only on relative position.

## The RoPE Operation

The RoPE operation (Su et al., 2021) transforms any given vector $\mathbf{v} \in \mathbb{R}^{d_{model}}$ at position $t$ (which will serve as the query $\mathbf{q}_t$ or key $\mathbf{k}_t$) by applying a position-dependent rotation:

$$
f(\mathbf{v}, t) = R_t \, \mathbf{v}
$$

The matrix $R_t$ is block-diagonal. Each pair of dimensions $(2i, 2i+1)$ receives a $2 \times 2$ rotation block:

$$
R_t^{(i)} = \begin{bmatrix} \cos(t \cdot \theta_i) & -\sin(t \cdot \theta_i) \\ \sin(t \cdot \theta_i) & \cos(t \cdot \theta_i) \end{bmatrix}
$$

The angle of rotation is $t \cdot \theta_i$, where $\theta_i$ is the angular frequency for dimension pair $i$:

$$
\theta_i = \frac{1}{10000^{\,2i\,/\,d_{model}}}
$$

The variable $\theta_i$ represents the angular frequency. Standard physics notation uses $\omega$ for frequency, whereas $\theta_i$ is the canonical notation established by Su et al. (2021). The value $\theta_i$ specifies the rate of rotation (radians per position step), and $t \cdot \theta_i$ yields the total angle of rotation at position $t$.

This frequency base is identical to the one used in sinusoidal positional encoding (Chapter 2). The motivation for rotational encoding stems directly from the relative position requirement established in Chapter 4. The dot product between a query vector and a key vector is determined by the angle between them. Rotating a query at position $m$ by an angle proportional to $m$ and a key at position $n$ by an angle proportional to $n$ shifts the angle between the two vectors by an amount proportional to $n - m$. The dot product becomes a function of relative distance by pure geometric construction.

## Deriving the Rotation Matrix from Complex Multiplication

Rotating a vector in a 2D real plane requires matrix multiplication. Mapping the 2D plane to the complex plane provides a mathematical shortcut, collapsing 2D matrix rotation into a single scalar multiplication. Complex number arithmetic serves as an algebraic bridge to derive the real $2 \times 2$ rotation matrix without geometric proofs. The derivation has four steps.

### Step 1: Represent a Dimension Pair as a Complex Number

The index $i$ here identifies the *dimension pair* (e.g., $i=0$ is the first pair, $i=1$ is the second pair). For a given pair $i$, the two real components $v_{2i}$ and $v_{2i+1}$ of the generic vector $\mathbf{v}$ are treated as the real and imaginary parts of a complex number:

$$
z = v_{2i} + j \cdot v_{2i+1}
$$

where $j$ is the imaginary unit ($j^2 = -1$). That complex representation maps a pair of real dimensions to a single point in the complex plane: $v_{2i}$ determines the horizontal coordinate, $v_{2i+1}$ determines the vertical coordinate.

### Step 2: Multiply by the Position-Dependent Phase Factor

Euler's formula defines a point on the unit circle at angle $\alpha$:

$$
e^{j\alpha} = \cos(\alpha) + j\sin(\alpha)
$$

Multiplying any complex number $z$ by a point on the unit circle rotates $z$ by that angle without altering its magnitude. Setting the angle to $\alpha = t \cdot \theta_i$ encodes position $t$. The complex number $z$ is multiplied by the unit complex exponential $e^{j \, t \, \theta_i}$:

$$
e^{j \, t \, \theta_i} = \cos(t \, \theta_i) + j \, \sin(t \, \theta_i)
$$

Defining the rotation angle as a multiple of $t$ translates the absolute position index directly into a geometric orientation.

The rotated complex number is:

$$
z' = z \cdot e^{j \, t \, \theta_i} = (v_{2i} + j \, v_{2i+1})(\cos(t\theta_i) + j \, \sin(t\theta_i))
$$

### Step 3: Expand the Complex Product

Expanding the complex product using the distributive property and $j^2 = -1$:

$$
z' = v_{2i} \cos(t\theta_i) + j \, v_{2i} \sin(t\theta_i) + j \, v_{2i+1} \cos(t\theta_i) + j^2 \, v_{2i+1} \sin(t\theta_i)
$$

$$
= v_{2i} \cos(t\theta_i) + j \, v_{2i} \sin(t\theta_i) + j \, v_{2i+1} \cos(t\theta_i) - v_{2i+1} \sin(t\theta_i)
$$

Collecting the real terms (those without $j$) and the imaginary terms (those with $j$):

$$
\text{Re}(z') = v_{2i} \cos(t\theta_i) - v_{2i+1} \sin(t\theta_i)
$$

$$
\text{Im}(z') = v_{2i} \sin(t\theta_i) + v_{2i+1} \cos(t\theta_i)
$$

### Step 4: Map Back to the Real Vector Space

Transformers do not process complex numbers; they operate exclusively on real-valued tensors. The complex plane was merely a temporary computational workspace used to perform the rotation easily. Now that the rotation is complete, the new complex number $z'$ must be disassembled back into two standard real numbers. 

The original, unrotated inputs are $v_{2i}$ and $v_{2i+1}$. The goal is to compute their rotated outputs, which are denoted with primes ($v'_{2i}$ and $v'_{2i+1}$) to distinguish them from the inputs. 

Step 1 mapped dimension $2i$ to the real part and dimension $2i+1$ to the imaginary part, so the reverse mapping extracts the final outputs from $z'$. The new real part becomes the rotated output $v'_{2i}$, and the new imaginary coefficient becomes the rotated output $v'_{2i+1}$:

$$
v'_{2i} = \text{Re}(z') = v_{2i} \cos(t\theta_i) - v_{2i+1} \sin(t\theta_i)
$$

$$
v'_{2i+1} = \text{Im}(z') = v_{2i} \sin(t\theta_i) + v_{2i+1} \cos(t\theta_i)
$$

Converting this system of two linear equations into a single matrix multiplication requires factoring out the input variables ($v_{2i}$ and $v_{2i+1}$) from their coefficients. Rewriting the equations to explicitly group the coefficients for each variable makes this extraction clear:

$$
v'_{2i} \,= \big(\cos(t\theta_i)\big) v_{2i} + \big(-\sin(t\theta_i)\big) v_{2i+1}
$$

$$
v'_{2i+1} = \big(\sin(t\theta_i)\big) v_{2i} + \big(\cos(t\theta_i)\big) v_{2i+1}
$$

By the definition of matrix-vector multiplication, these grouped coefficients become the rows of a $2 \times 2$ matrix, and the isolated variables form a column vector on the right. This factorization yields the final real-valued rotation matrix:
$$
\begin{bmatrix} v'_{2i} \\ v'_{2i+1} \end{bmatrix} = \begin{bmatrix} \cos(t\theta_i) & -\sin(t\theta_i) \\ \sin(t\theta_i) & \cos(t\theta_i) \end{bmatrix} \begin{bmatrix} v_{2i} \\ v_{2i+1} \end{bmatrix}
$$

That $2 \times 2$ matrix is the standard planar rotation operator, derived entirely from the algebraic properties of complex multiplication. The rotation angle $t \cdot \theta_i$ increases linearly with position $t$, so each successive position rotates the dimension pair by an additional $\theta_i$ radians.

## Scaling to Full Dimension (The Block-Diagonal Matrix)

The single-pair derivation for index $i$ extends across the full vector by applying this rotation to every dimension pair simultaneously. For a vector with an even $d_{model} = 6$ (three dimension pairs), the full mathematical system repeats the $2 \times 2$ system three times with a distinct frequency $\theta_i$ for each pair:

$$
v'_0 = v_0 \cos(t\theta_0) - v_1 \sin(t\theta_0)
$$

$$
v'_1 = v_0 \sin(t\theta_0) + v_1 \cos(t\theta_0)
$$

$$
v'_2 = v_2 \cos(t\theta_1) - v_3 \sin(t\theta_1)
$$

$$
v'_3 = v_2 \sin(t\theta_1) + v_3 \cos(t\theta_1)
$$

$$
v'_4 = v_4 \cos(t\theta_2) - v_5 \sin(t\theta_2)
$$

$$
v'_5 = v_4 \sin(t\theta_2) + v_5 \cos(t\theta_2)
$$

Expressing this entire system as a single matrix equation $\mathbf{v}' = R_t \mathbf{v}$ maps the coefficients for each input component to the corresponding matrix entries. Components $v'_0$ and $v'_1$ depend exclusively on $v_0$ and $v_1$, so the first two rows contain zeros in all other columns. This strict independence between dimension pairs forces the general matrix into a block-diagonal structure.

Assembling the full $6 \times 6$ matrix multiplication demonstrates this decomposition:

$$
\begin{bmatrix} v'_0 \\ v'_1 \\ v'_2 \\ v'_3 \\ v'_4 \\ v'_5 \end{bmatrix} = \begin{bmatrix} 
\cos(t\theta_0) & -\sin(t\theta_0) & 0 & 0 & 0 & 0 \\ 
\sin(t\theta_0) & \cos(t\theta_0) & 0 & 0 & 0 & 0 \\ 
0 & 0 & \cos(t\theta_1) & -\sin(t\theta_1) & 0 & 0 \\ 
0 & 0 & \sin(t\theta_1) & \cos(t\theta_1) & 0 & 0 \\ 
0 & 0 & 0 & 0 & \cos(t\theta_2) & -\sin(t\theta_2) \\ 
0 & 0 & 0 & 0 & \sin(t\theta_2) & \cos(t\theta_2) 
\end{bmatrix} \begin{bmatrix} v_0 \\ v_1 \\ v_2 \\ v_3 \\ v_4 \\ v_5 \end{bmatrix}
$$

Every off-diagonal block is zero, ensuring that each dimension pair is rotated independently within its own 2D plane without bleeding into the others. The frequency $\theta_i$ decreases for each subsequent block, so the first pair rotates rapidly while the final pair rotates at a much lower rate.

## The Odd-Dimension Edge Case ($d_{model} = 3$)

The toy model has $d_{model} = 3$, an odd number. RoPE operates on dimension pairs, so the three dimensions are partitioned as follows:

- **Dimensions 0 and 1 ($i = 0$):** Form a complete 2D plane rotated by the angle $t \cdot \theta_0$.
- **Dimension 2 (unpaired):** Lacks a partner coordinate to form a complex number and passes through unrotated.

Standard practice in production implementations is to leave unpaired dimensions unrotated: the unpaired dimension passes through unchanged, as if multiplied by the $1 \times 1$ identity matrix. Every frontier model uses an even $d_{model}$ (typically 128 per attention head), which avoids unpaired dimensions entirely. The toy model forces this edge case to the surface.

The full $3 \times 3$ rotation matrix $R_t$ is block-diagonal:

$$
R_t = \begin{bmatrix} \cos(t \cdot \theta_0) & -\sin(t \cdot \theta_0) & 0 \\ \sin(t \cdot \theta_0) & \cos(t \cdot \theta_0) & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

The upper-left $2 \times 2$ block rotates dimensions 0 and 1 by angle $t \cdot \theta_0$. The lower-right $1 \times 1$ block is the identity, leaving dimension 2 unchanged.

Expanding the full matrix-vector multiplication for a generic vector $\mathbf{v}$ demonstrates how the unpaired dimension is preserved:

$$
R_t \, \mathbf{v} = \begin{bmatrix} \cos(t \cdot \theta_0) & -\sin(t \cdot \theta_0) & 0 \\ \sin(t \cdot \theta_0) & \cos(t \cdot \theta_0) & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} v_0 \\ v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} v_0 \cos(t\theta_0) - v_1 \sin(t\theta_0) \\ v_0 \sin(t\theta_0) + v_1 \cos(t\theta_0) \\ v_2 \end{bmatrix}
$$

The first two components are mixed by the rotation, but the zeros in the third row isolate $v_2$, allowing it to pass through untouched.

### Computing the Angular Frequency

The rotation angle depends on the frequency $\theta_i$, which is determined by the dimension pair index $i$ and the total dimensions $d_{model}$. The formula for $\theta_i$ is:

$$
\theta_i = \frac{1}{10000^{\,2i / d_{model}}}
$$

For the toy model ($d_{model} = 3$), the only complete dimension pair is $i = 0$. Substituting these values into the frequency formula yields $1$:

$$
\theta_0 = \frac{1}{10000^{\,0/3}} = \frac{1}{10000^0} = \frac{1}{1} = 1
$$

The absolute position index $t$ is a discrete integer ($0, 1, 2, 3$). RoPE translates this index into a geometric angle by using the frequency $\theta_i$ as a conversion factor defining the rotation rate in **radians per position step** ($1\text{ radian} \approx 57.3^\circ$). Multiplying the position $t$ by the unit rate $\theta_0 = 1\text{ rad/step}$ reduces the total rotation angle to $t \cdot 1 = t$ radians, reinterpreting the token index integer directly as an angle across the four sequence positions:

- **Position 0:** $0 \text{ steps} \times 1 \text{ rad/step} = 0 \text{ radians}$ ($0^\circ$).
- **Position 1:** $1 \text{ step} \times 1 \text{ rad/step} = 1 \text{ radian}$ ($\approx 57.3^\circ$).
- **Position 2:** $2 \text{ steps} \times 1 \text{ rad/step} = 2 \text{ radians}$ ($\approx 114.6^\circ$).
- **Position 3:** $3 \text{ steps} \times 1 \text{ rad/step} = 3 \text{ radians}$ ($\approx 171.9^\circ$).

The next chapter evaluates the explicit $3 \times 3$ rotation matrix at each of these four angles and applies the resulting rotations to every query and key vector from the toy model.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
