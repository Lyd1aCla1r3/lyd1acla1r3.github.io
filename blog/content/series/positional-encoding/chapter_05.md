# Part 5: Rotary Position Embeddings: Deriving the Rotation Matrix

<!-- SUMMARY: Rotary Position Embeddings (RoPE) encode position by rotating query and key vectors rather than adding to embeddings. This chapter derives the rotation matrix from complex number multiplication, shows how individual dimension-pair rotations combine into a block-diagonal matrix, handles the odd-dimension edge case for the toy model, and computes the angular frequency that will drive the rotations in the next chapter. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter identified the structural failure of additive positional encoding in the query-key dot product: the cross-terms between content and position depend on absolute position indices, not on relative offsets. The preview at the end of that chapter stated that Rotary Position Embeddings (RoPE) encode position by rotating query and key vectors after projection, and that the dot product of rotated vectors depends only on relative position by construction.

This chapter derives the rotation matrix that performs this encoding. The derivation begins with complex number multiplication (the conceptual foundation), recovers the real-valued rotation matrix (the computational mechanism), and applies it to every query and key vector from the toy model. The proof that the dot product depends only on relative position is the subject of the next chapter.

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

The variable $\theta_i$ represents the angular frequency. Although $\omega$ is the standard physics notation for frequency, $\theta_i$ is the canonical notation established by Su et al. (2021). The value $\theta_i$ specifies the rate of rotation (radians per position step), and $t \cdot \theta_i$ yields the total angle of rotation at position $t$.

This frequency base is identical to the one used in sinusoidal positional encoding (Chapter 2). The motivation for rotational encoding stems directly from the relative position requirement established in Chapter 4. The dot product between a query vector and a key vector is determined by the angle between them. If a query at position $m$ is rotated by an angle proportional to $m$, and a key at position $n$ is rotated by an angle proportional to $n$, the angle between the two vectors changes by an amount proportional to $n - m$. The dot product becomes a function of relative distance by pure geometric construction.

## Deriving the Rotation Matrix from Complex Multiplication

Rotating a vector in a 2D real plane requires matrix multiplication. Mapping the 2D plane to the complex plane provides a mathematical shortcut, collapsing 2D matrix rotation into a single scalar multiplication. Complex number arithmetic serves as an algebraic bridge to derive the real $2 \times 2$ rotation matrix without geometric proofs. The derivation has four steps.

### Step 1: Represent a Dimension Pair as a Complex Number

The index $i$ here identifies the *dimension pair* (e.g., $i=0$ is the first pair, $i=1$ is the second pair). For a given pair $i$, the two real components $v_{2i}$ and $v_{2i+1}$ of the generic vector $\mathbf{v}$ are treated as the real and imaginary parts of a complex number:

$$
z = v_{2i} + j \cdot v_{2i+1}
$$

where $j$ is the imaginary unit ($j^2 = -1$). This maps a pair of real dimensions to a single point in the complex plane: $v_{2i}$ determines the horizontal coordinate, $v_{2i+1}$ determines the vertical coordinate.

### Step 2: Multiply by the Position-Dependent Phase Factor

Euler's formula defines a point on the unit circle at angle $\alpha$:

$$
e^{j\alpha} = \cos(\alpha) + j\sin(\alpha)
$$

Multiplying any complex number $z$ by a point on the unit circle rotates $z$ by that angle without altering its magnitude. To encode position $t$, the angle is set to $\alpha = t \cdot \theta_i$. The complex number $z$ is multiplied by the unit complex exponential $e^{j \, t \, \theta_i}$:

$$
e^{j \, t \, \theta_i} = \cos(t \, \theta_i) + j \, \sin(t \, \theta_i)
$$

By defining the rotation angle as a multiple of $t$, the absolute position index is translated directly into a geometric orientation.

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

Because Step 1 mapped dimension $2i$ to the real part and dimension $2i+1$ to the imaginary part, the exact reverse mapping is applied to $z'$ to extract the final outputs. The new real part becomes the rotated output $v'_{2i}$, and the new imaginary coefficient becomes the rotated output $v'_{2i+1}$:

$$
v'_{2i} = \text{Re}(z') = v_{2i} \cos(t\theta_i) - v_{2i+1} \sin(t\theta_i)
$$

$$
v'_{2i+1} = \text{Im}(z') = v_{2i} \sin(t\theta_i) + v_{2i+1} \cos(t\theta_i)
$$

To convert this system of two linear equations into a single matrix multiplication, the input variables ($v_{2i}$ and $v_{2i+1}$) must be factored out from their coefficients. Rewriting the equations to explicitly group the coefficients for each variable makes this extraction clear:

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

This is the standard $2 \times 2$ rotation matrix, derived entirely from the algebraic properties of complex multiplication. The rotation angle $t \cdot \theta_i$ increases linearly with position $t$, so each successive position rotates the dimension pair by an additional $\theta_i$ radians.

## Scaling to Full Dimension (The Block-Diagonal Matrix)

While the derivation focused on a single pair $i$, the complete RoPE operation applies this rotation to every pair in the vector simultaneously. For a vector with an even $d_{model} = 6$ (three dimension pairs), the full mathematical system is simply the $2 \times 2$ system repeated three times, using a different frequency $\theta_i$ for each pair:

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

To express this entire system as a single matrix equation $\mathbf{v}' = R_t \mathbf{v}$ the coefficients for each input component dictate the matrix entries. Because $v'_0$ and $v'_1$ depend exclusively on $v_0$ and $v_1$, the first two rows must contain zeros for all other columns. This strict independence between dimension pairs is what forces the general matrix into a block-diagonal structure.

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

Every off-diagonal block is zero, ensuring that each dimension pair is rotated independently within its own 2D plane without bleeding into the others. The frequency $\theta_i$ decreases for each subsequent block, so the first pair rotates rapidly while the final pair rotates very slowly.

## The Odd-Dimension Edge Case ($d_{model} = 3$)

The toy model has $d_{model} = 3$, an odd number. RoPE operates on dimension pairs, so the three dimensions are partitioned as follows:

- **Dimensions 0 and 1** form a complete pair ($i = 0$). The rotation angle is $t \cdot \theta_0$.
- **Dimension 2** is unpaired. No second dimension exists to form the imaginary part of a complex number.

Standard practice in production implementations is to leave unpaired dimensions unrotated: the unpaired dimension passes through unchanged, as if multiplied by the $1 \times 1$ identity matrix. Every frontier model uses an even $d_{model}$ (typically 128 per attention head), which avoids unpaired dimensions entirely. The toy model forces this edge case to the surface.

The full $3 \times 3$ rotation matrix $R_t$ is block-diagonal:

$$
R_t = \begin{bmatrix} \cos(t \cdot \theta_0) & -\sin(t \cdot \theta_0) & 0 \\ \sin(t \cdot \theta_0) & \cos(t \cdot \theta_0) & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

The upper-left $2 \times 2$ block rotates dimensions 0 and 1 by angle $t \cdot \theta_0$. The lower-right $1 \times 1$ block is the identity, leaving dimension 2 unchanged.

Expanding the full matrix-vector multiplication for a generic vector $\mathbf{v}$ demonstrates exactly how the unpaired dimension is preserved:

$$
R_t \, \mathbf{v} = \begin{bmatrix} \cos(t \cdot \theta_0) & -\sin(t \cdot \theta_0) & 0 \\ \sin(t \cdot \theta_0) & \cos(t \cdot \theta_0) & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} v_0 \\ v_1 \\ v_2 \end{bmatrix} = \begin{bmatrix} v_0 \cos(t\theta_0) - v_1 \sin(t\theta_0) \\ v_0 \sin(t\theta_0) + v_1 \cos(t\theta_0) \\ v_2 \end{bmatrix}
$$

The first two components are mixed by the rotation, but the zeros in the third row isolate $v_2$, allowing it to pass through untouched.

### Computing the Angular Frequency

The rotation angle depends on the frequency $\theta_i$, which is determined by the dimension pair index $i$ and the total dimensions $d_{model}$. The formula for $\theta_i$ is:

$$
\theta_i = \frac{1}{10000^{\,2i / d_{model}}}
$$

For the toy model ($d_{model} = 3$), the only complete dimension pair is $i = 0$. Plugging these values into the frequency formula yields exactly 1:

$$
\theta_0 = \frac{1}{10000^{\,0/3}} = \frac{1}{10000^0} = \frac{1}{1} = 1
$$

The absolute position index $t$ is simply a discrete integer ($0, 1, 2, 3$). RoPE translates this index into a geometric angle by using the frequency $\theta_i$ as a conversion factor. The frequency $\theta_i$ defines the rotation rate in **radians per position step** (where 1 radian is the standard mathematical unit for angles, equal to $\approx 57.3^\circ$).

The total rotation angle is computed by multiplying the position $t$ by this rate ($t \cdot \theta_i$). For the toy model's first dimension pair, the frequency is exactly $\theta_0 = 1$ radian per step. This means the total angle simplifies perfectly to $t \cdot 1 = t$ radians. The mathematical machinery literally reinterprets the token index integer as an angle.

This mapping dictates the precise rotations for the sequence:

- **Position 0**: $0 \text{ steps} \times 1 \text{ rad/step} = 0 \text{ radians}$ ($0^\circ$).
- **Position 1**: $1 \text{ step} \times 1 \text{ rad/step} = 1 \text{ radian}$ ($\approx 57.3^\circ$).
- **Position 2**: $2 \text{ steps} \times 1 \text{ rad/step} = 2 \text{ radians}$ ($\approx 114.6^\circ$).
- **Position 3**: $3 \text{ steps} \times 1 \text{ rad/step} = 3 \text{ radians}$ ($\approx 171.9^\circ$).


The angular frequency for the toy model's single dimension pair is exactly $\theta_0 = 1$ radian per position step. The rotation angle at each position simplifies to $t$ radians: position 0 maps to $0$ radians, position 1 to $1$ radian, position 2 to $2$ radians, and position 3 to $3$ radians. The next chapter computes the explicit rotation matrix at each of these four positions and applies the rotations to every query and key vector from the toy model.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
