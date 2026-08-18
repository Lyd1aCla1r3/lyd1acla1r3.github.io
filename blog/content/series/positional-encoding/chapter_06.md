# Part 6: Rotary Position Embeddings: Computing the Rotated Vectors

<!-- SUMMARY: The rotation matrix derived in the preceding chapter is evaluated at every position in the toy sequence. Each 3×3 matrix is computed from cos(t) and sin(t), producing four distinct rotation matrices R_0 through R_3. These matrices are applied to every query and key vector from Chapter 4, producing the rotated vectors that the Transformer's attention mechanism will consume. The orthogonality of the rotation matrices guarantees that vector norms are preserved. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter derived the $3 \times 3$ rotation matrix for the toy model's odd-dimensional embedding space ($d_{model} = 3$). The upper-left $2 \times 2$ block rotates the complete dimension pair (dimensions 0 and 1) by the position-dependent angle $t \cdot \theta_0 = t$ radians, while the lower-right $1 \times 1$ identity block passes dimension 2 through unchanged. This chapter evaluates that matrix at every position in the toy sequence, proves its orthogonality, and applies the resulting rotations to every query and key vector.

## Computing the Rotation Matrices

Each position $t \in \{0, 1, 2, 3\}$ has a specific $3 \times 3$ rotation matrix. Because the rotation angle is exactly $t$, the nine matrix entries are derived directly from $\cos(t)$ and $\sin(t)$.

### Position $t = 0$ (rotation by $0$ radians)

$$
\cos(0) = 1.0000, \qquad \sin(0) = 0.0000
$$

$$
R_0 = \begin{bmatrix} \phantom{-}1.0000 & \phantom{-}0.0000 & 0 \\ \phantom{-}0.0000 & \phantom{-}1.0000 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

$R_0$ is the identity matrix. The first position in the sequence receives no rotation, which is consistent with the convention that position 0 is the reference orientation. All vectors at position 0 pass through unchanged.

### Position $t = 1$ (rotation by $1$ radian)

$$
\cos(1) = 0.5403, \qquad \sin(1) = 0.8415
$$

$$
R_1 = \begin{bmatrix} \phantom{-}0.5403 & -0.8415 & 0 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

The rotation by $1$ radian is substantial: $\cos(1) \approx 0.54$ and $\sin(1) \approx 0.84$. Dimensions 0 and 1 are significantly mixed by this rotation, while dimension 2 is unchanged.

### Position $t = 2$ (rotation by $2$ radians)

$$
\cos(2) = -0.4161, \qquad \sin(2) = 0.9093
$$

$$
R_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

At $2$ radians, the cosine has crossed zero and turned negative. The $90^\circ$ boundary ($\pi/2 \approx 1.57$ radians) dictates the sign of a dot product. If the angle between two vectors is less than $90^\circ$, their dot product is positive; if it exceeds $90^\circ$, the dot product is negative. Because $2 > 1.57$, the vector has rotated past this orthogonal boundary into the second quadrant. It now points away from its original orientation. The negative diagonal entries reflect this quadrant shift.

### Position $t = 3$ (rotation by $3$ radians)

$$
\cos(3) = -0.9900, \qquad \sin(3) = 0.1411
$$

$$
R_3 = \begin{bmatrix} -0.9900 & -0.1411 & 0 \\ \phantom{-}0.1411 & -0.9900 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

At 3 radians ($\approx 171.9°$), the rotation is nearly a full half-turn. The cosine is close to $-1$, meaning dimension 0 is nearly inverted, and the sine is small and positive, meaning dimension 1 contributes only a small correction. The rotation matrix is close to $\text{diag}(-1, -1, 1)$, which would be an exact $180°$ rotation at $t = \pi$.

### Summary of Rotation Matrices

| Position $t$ | Angle (radians) | $\cos(t)$ | $\sin(t)$ |
|---|---|---|---|
| $0$ | $0.0000$ | $\phantom{-}1.0000$ | $0.0000$ |
| $1$ | $1.0000$ | $\phantom{-}0.5403$ | $0.8415$ |
| $2$ | $2.0000$ | $-0.4161$ | $0.9093$ |
| $3$ | $3.0000$ | $-0.9900$ | $0.1411$ |

Every derived rotation matrix $R_t$ is strictly orthogonal. This is an emergent structural property of the rotation matrix itself, rooted directly in the Pythagorean trigonometric identity $\cos^2(\alpha) + \sin^2(\alpha) = 1$.

Multiplying a $2 \times 2$ rotation block $R$ by its transpose $R^\top$ explicitly demonstrates this property:

$$
R^\top R = \begin{bmatrix} \cos(t\theta_i) & \sin(t\theta_i) \\ -\sin(t\theta_i) & \cos(t\theta_i) \end{bmatrix} \begin{bmatrix} \cos(t\theta_i) & -\sin(t\theta_i) \\ \sin(t\theta_i) & \cos(t\theta_i) \end{bmatrix}
$$

$$
= \begin{bmatrix} \cos^2(t\theta_i) + \sin^2(t\theta_i) & -\cos(t\theta_i)\sin(t\theta_i) + \sin(t\theta_i)\cos(t\theta_i) \\ -\sin(t\theta_i)\cos(t\theta_i) + \cos(t\theta_i)\sin(t\theta_i) & (-\sin(t\theta_i))^2 + \cos^2(t\theta_i) \end{bmatrix}
$$

$$
= \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} = I
$$

The off-diagonal terms cancel out completely, and the diagonal terms sum to 1, confirming that the matrix is mathematically orthogonal ($R_t^\top R_t = I$).

This orthogonality guarantees that the rotation preserves the lengths (norms) of the transformed vectors. Computing the squared norm of a rotated vector $R_t \mathbf{v}$ proves this preservation:

$$
\|R_t \mathbf{v}\|^2 = (R_t \mathbf{v})^\top (R_t \mathbf{v})
$$

$$
= \mathbf{v}^\top (R_t^\top R_t) \mathbf{v}
$$

Substituting the identity matrix $I$ for $R_t^\top R_t$:

$$
= \mathbf{v}^\top I \mathbf{v} = \mathbf{v}^\top \mathbf{v} = \|\mathbf{v}\|^2
$$

Because the squared norms are equal, the magnitudes are strictly identical ($\|R_t \mathbf{v}\| = \|\mathbf{v}\|$).

This geometric preservation of magnitude provides a major structural advantage for RoPE over absolute additive encoding (like the sinusoidal encoding from Chapter 2). Additive encoding alters the original vector's length by directly adding a positional vector to it. RoPE only changes the vector's orientation, leaving its semantic magnitude completely intact.

## Applying RoPE to the Query Vectors

The query vectors from Chapter 4 are rotated by their respective position matrices: $\mathbf{q}'_t = R_t \, \mathbf{q}_t$.

### Position $t = 0$ (`The`): $\mathbf{q}_0 = \begin{bmatrix} -0.08 & -0.13 & \phantom{-}0.21 \end{bmatrix}^\top$

$R_0$ is the identity matrix, so the query vector passes through unchanged:

$$
\mathbf{q}'_0 = R_0 \, \mathbf{q}_0 = \begin{bmatrix} \phantom{-}1.0000 & \phantom{-}0.0000 & 0 \\ \phantom{-}0.0000 & \phantom{-}1.0000 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.08 \\ -0.13 \\ \phantom{-}0.21 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.0800} \\ \mathbf{-0.1300} \\ \phantom{-}\mathbf{0.2100} \end{bmatrix}
$$

### Position $t = 1$ (`quick`): $\mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.35 & -0.17 & -0.27 \end{bmatrix}^\top$

$$
\mathbf{q}'_1 = R_1 \, \mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.5403 & -0.8415 & 0 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.35 \\ -0.17 \\ -0.27 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.3322} \\ \phantom{-}\mathbf{0.2027} \\ \mathbf{-0.2700} \end{bmatrix}
$$


### Position $t = 2$ (`brown`): $\mathbf{q}_2 = \begin{bmatrix} -0.09 & \phantom{-}0.47 & -0.07 \end{bmatrix}^\top$

$$
\mathbf{q}'_2 = R_2 \, \mathbf{q}_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.09 \\ \phantom{-}0.47 \\ -0.07 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.3899} \\ \mathbf{-0.2774} \\ \mathbf{-0.0700} \end{bmatrix}
$$

### Position $t = 3$ (`fox`): $\mathbf{q}_3 = \begin{bmatrix} -0.01 & -0.08 & \phantom{-}0.15 \end{bmatrix}^\top$

$$
\mathbf{q}'_3 = R_3 \, \mathbf{q}_3 = \begin{bmatrix} -0.9900 & -0.1411 & 0 \\ \phantom{-}0.1411 & -0.9900 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.01 \\ -0.08 \\ \phantom{-}0.15 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0212} \\ \phantom{-}\mathbf{0.0778} \\ \phantom{-}\mathbf{0.1500} \end{bmatrix}
$$

### Rotated Query Vectors Summary

<div style="font-size: 0.9em; overflow-x: auto;">

| Position | Token | $\mathbf{q}_t$ (before RoPE) | $\mathbf{q}'_t$ (after RoPE) |
|---|---|---|---|
| $0$ | `The` | $[-0.0800, -0.1300, \phantom{-}0.2100\;]$ | $[-0.0800, -0.1300, \phantom{-}0.2100\;]$ |
| $1$ | `quick` | $[\phantom{-}0.3500, -0.1700, -0.2700\;]$ | $[\phantom{-}0.3322, \phantom{-}0.2027, -0.2700\;]$ |
| $2$ | `brown` | $[-0.0900, \phantom{-}0.4700, -0.0700\;]$ | $[-0.3899, -0.2774, -0.0700\;]$ |
| $3$ | `fox` | $[-0.0100, -0.0800, \phantom{-}0.1500\;]$ | $[\phantom{-}0.0212, \phantom{-}0.0778, \phantom{-}0.1500\;]$ |

The third component of every vector is unchanged (the identity block for the unpaired dimension). The first two components are rotated by increasing angles: 0, 1, 2, 3 radians. At position 0, no rotation occurs. At position 2, the rotation of $2$ radians has reversed the sign of $q'_2[1]$ (from $0.47$ to $-0.2774$) and driven $q'_2[0]$ more negative (from $-0.09$ to $-0.3899$). These are not additive modifications; the vector has been geometrically reoriented in the 2D plane formed by dimensions 0 and 1.

</div>

## Applying RoPE to the Key Vectors

The key vectors from Chapter 4 are rotated identically: $\mathbf{k}'_t = R_t \, \mathbf{k}_t$.

### Position $t = 0$ (`The`): $\mathbf{k}_0 = \begin{bmatrix} -0.15 & \phantom{-}0.10 & -0.04 \end{bmatrix}^\top$

$$
\mathbf{k}'_0 = R_0 \, \mathbf{k}_0 = \begin{bmatrix} \phantom{-}1.0000 & \phantom{-}0.0000 & 0 \\ \phantom{-}0.0000 & \phantom{-}1.0000 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.15 \\ \phantom{-}0.10 \\ -0.04 \end{bmatrix} = \begin{bmatrix} \mathbf{-0.1500} \\ \phantom{-}\mathbf{0.1000} \\ \mathbf{-0.0400} \end{bmatrix}
$$

### Position $t = 1$ (`quick`): $\mathbf{k}_1 = \begin{bmatrix} \phantom{-}0.24 & \phantom{-}0.11 & -0.32 \end{bmatrix}^\top$

$$
\mathbf{k}'_1 = R_1 \, \mathbf{k}_1 = \begin{bmatrix} \phantom{-}0.5403 & -0.8415 & 0 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.24 \\ \phantom{-}0.11 \\ -0.32 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0371} \\ \phantom{-}\mathbf{0.2614} \\ \mathbf{-0.3200} \end{bmatrix}
$$

### Position $t = 2$ (`brown`): $\mathbf{k}_2 = \begin{bmatrix} \phantom{-}0.16 & -0.17 & \phantom{-}0.36 \end{bmatrix}^\top$

$$
\mathbf{k}'_2 = R_2 \, \mathbf{k}_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} \phantom{-}0.16 \\ -0.17 \\ \phantom{-}0.36 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0880} \\ \phantom{-}\mathbf{0.2162} \\ \phantom{-}\mathbf{0.3600} \end{bmatrix}
$$

### Position $t = 3$ (`fox`): $\mathbf{k}_3 = \begin{bmatrix} -0.06 & \phantom{-}0.11 & -0.05 \end{bmatrix}^\top$

$$
\mathbf{k}'_3 = R_3 \, \mathbf{k}_3 = \begin{bmatrix} -0.9900 & -0.1411 & 0 \\ \phantom{-}0.1411 & -0.9900 & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} -0.06 \\ \phantom{-}0.11 \\ -0.05 \end{bmatrix} = \begin{bmatrix} \phantom{-}\mathbf{0.0439} \\ \mathbf{-0.1174} \\ \mathbf{-0.0500} \end{bmatrix}
$$

### Rotated Key Vectors Summary

<div style="font-size: 0.9em; overflow-x: auto;">

| Position | Token | $\mathbf{k}_t$ (before RoPE) | $\mathbf{k}'_t$ (after RoPE) |
|---|---|---|---|
| $0$ | `The` | $[-0.1500, \phantom{-}0.1000, -0.0400\;]$ | $[-0.1500, \phantom{-}0.1000, -0.0400\;]$ |
| $1$ | `quick` | $[\phantom{-}0.2400, \phantom{-}0.1100, -0.3200\;]$ | $[\phantom{-}0.0371, \phantom{-}0.2614, -0.3200\;]$ |
| $2$ | `brown` | $[\phantom{-}0.1600, -0.1700, \phantom{-}0.3600\;]$ | $[\phantom{-}0.0880, \phantom{-}0.2162, \phantom{-}0.3600\;]$ |
| $3$ | `fox` | $[-0.0600, \phantom{-}0.1100, -0.0500\;]$ | $[\phantom{-}0.0439, -0.1174, -0.0500\;]$ |

</div>

## What Has Been Accomplished

The RoPE operation has injected positional information into every query and key vector through geometric rotation, without adding any vector to the embeddings. The key structural properties of this encoding:

**Nothing is added.** Unlike sinusoidal PE (Chapter 3), RoPE does not add a positional vector to the embedding. The embedding tensor $X$ is untouched. The positional signal exists only in the rotated orientation of the query and key vectors, not in their magnitudes.

**Norms are preserved.** Because $R_t$ is an orthogonal matrix, $\|\mathbf{q}'_t\| = \|\mathbf{q}_t\|$ and $\|\mathbf{k}'_t\| = \|\mathbf{k}_t\|$. The semantic magnitude of each vector is unaltered; only its direction in the 2D subspace formed by dimensions 0 and 1 has changed.

**Each position receives a distinct rotation.** Position 0 is the reference orientation (no rotation). Position 1 is rotated by 1 radian. Position 2 by 2 radians. Position 3 by 3 radians. The rotation angle increases linearly with position, producing a unique geometric orientation for each position index.

**The unpaired dimension carries no positional signal.** Dimension 2 passes through the identity for all positions. In the toy model with $d_{model} = 3$, two out of three dimensions carry positional information. In production models with even $d_{model}$, all dimensions are paired and all carry positional signal.

The rotated query and key vectors are now ready to be consumed directly by the Transformer's attention mechanism. It is critical to understand that the Transformer never "decodes" these rotated vectors back into their original absolute positions. Instead, the positional information is structurally baked into the vectors, and the attention mechanism computes the dot product ($(\mathbf{q}'_m)^\top \mathbf{k}'_n$) between them. Because the Value vectors ($V$) are not rotated by RoPE, the positional information influences *only* the attention scores (which tokens pay attention to which), not the semantic content that is ultimately extracted.

The next chapter proves the central geometric property of RoPE: how the dot product of two rotated vectors $(\mathbf{q}'_m)^\top \mathbf{k}'_n$ mathematically collapses to depend exclusively on their relative distance ($m - n$), satisfying the relative positional requirement established in Chapter 4.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

