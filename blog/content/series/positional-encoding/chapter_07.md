# Part 7: The Relative-Distance Property of RoPE

<!-- SUMMARY: The central property of Rotary Position Embeddings is proved from first principles: the dot product of rotated query and key vectors depends only on content and relative position offset. The rotation composition identity is derived via the angle-addition identities for sine and cosine, verified numerically with the toy model, and the full post-RoPE relevance score matrix is computed and compared with the pre-RoPE baseline. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapters derived the RoPE rotation matrix from its complex-number foundations and applied it at every position to all query and key vectors from the toy model. The resulting rotated vectors $\mathbf{q}'_t = R_t \mathbf{q}_t$ and $\mathbf{k}'_t = R_t \mathbf{k}_t$ encode position through geometric orientation rather than additive modification. But the derivation stopped short of proving the property that motivated the entire construction: that the dot product of rotated vectors depends only on content and relative position.

This chapter delivers that proof. The rotation composition identity $R_m^\top R_n = R_{n-m}$ is derived from the angle-addition identities for sine and cosine, verified numerically using the toy model vectors, and applied to compute the full post-RoPE relevance score matrix. The result is then compared with the pre-RoPE matrix from Chapter 4 to demonstrate that RoPE has injected position-dependent structure into the relevance scores.

## The Central Property

For any two positions $m$ and $n$, the dot product of the rotated query at position $m$ and the rotated key at position $n$ satisfies:

$$
\mathbf{q}'^{\top}_m \mathbf{k}'_n = (R_m \mathbf{q}_m)^\top (R_n \mathbf{k}_n) = \mathbf{q}_m^\top R_m^\top R_n \, \mathbf{k}_n = \mathbf{q}_m^\top R_{n-m} \, \mathbf{k}_n
$$

The first equality substitutes the definition of rotated vectors. The second equality uses the transpose property of matrix products: $(R_m \mathbf{q}_m)^\top = \mathbf{q}_m^\top R_m^\top$. The third equality is the claim: the matrix product $R_m^\top R_n$ collapses to a single rotation matrix $R_{n-m}$ whose angle depends only on the offset $n - m$.

If this claim holds, then the relevance score between positions $m$ and $n$ is:

$$
\mathbf{q}'^{\top}_m \mathbf{k}'_n = \mathbf{q}_m^\top R_{n-m} \, \mathbf{k}_n
$$

The right-hand side depends on the content vectors $\mathbf{q}_m$ and $\mathbf{k}_n$ and on the relative offset $\Delta = n - m$, but not on the absolute positions $m$ and $n$ individually. This is exactly the relative position requirement stated in Chapter 4.

The claim rests on a single algebraic fact: the rotation composition identity $R_m^\top R_n = R_{n-m}$. The remainder of this section proves it from first principles.

## Proving the Rotation Composition Identity

### The Transpose of a Rotation Matrix

A rotation matrix $R_t$ for angle $\alpha = t \cdot \theta$ (dropping the subscript $i$ on $\theta$ for notational clarity, since the proof applies identically to each dimension pair) has the form:

$$
R_{\alpha} = \begin{bmatrix} \cos\alpha & -\sin\alpha \\ \sin\alpha & \cos\alpha \end{bmatrix}
$$

The transpose is obtained by reflecting across the main diagonal:

$$
R_{\alpha}^\top = \begin{bmatrix} \cos\alpha & \sin\alpha \\ -\sin\alpha & \cos\alpha \end{bmatrix}
$$

Because cosine is an even function ($\cos(-\alpha) = \cos\alpha$) and sine is an odd function ($\sin(-\alpha) = -\sin\alpha$), this transpose is identical to a rotation by $-\alpha$:

$$
R_{-\alpha} = \begin{bmatrix} \cos(-\alpha) & -\sin(-\alpha) \\ \sin(-\alpha) & \cos(-\alpha) \end{bmatrix} = \begin{bmatrix} \cos\alpha & \sin\alpha \\ -\sin\alpha & \cos\alpha \end{bmatrix} = R_{\alpha}^\top
$$

The transpose of a rotation matrix is its inverse: rotating by angle $\alpha$ and then by $-\alpha$ returns to the original orientation. Equivalently, $R_\alpha^\top R_\alpha = I$.

### Multiplying Two Rotation Matrices

The composition identity states that rotating by $-\alpha$ and then by $\beta$ is equivalent to a single rotation by $\beta - \alpha$. Written as a matrix equation:

$$
R_\alpha^\top R_\beta = R_{-\alpha} \cdot R_\beta = R_{\beta - \alpha}
$$

To prove this, the product of $R_{-\alpha}$ and $R_\beta$ is computed directly:

$$
R_{-\alpha} \cdot R_\beta = \begin{bmatrix} \cos\alpha & \sin\alpha \\ -\sin\alpha & \cos\alpha \end{bmatrix} \begin{bmatrix} \cos\beta & -\sin\beta \\ \sin\beta & \cos\beta \end{bmatrix} = \begin{bmatrix} \mathbf{\cos\alpha\cos\beta + \sin\alpha\sin\beta} & \mathbf{-\cos\alpha\sin\beta + \sin\alpha\cos\beta} \\ \mathbf{-\sin\alpha\cos\beta + \cos\alpha\sin\beta} & \mathbf{\sin\alpha\sin\beta + \cos\alpha\cos\beta} \end{bmatrix}
$$

### Applying the Angle-Addition Identities

The angle-addition identities for cosine and sine are:

$$
\cos(\beta - \alpha) = \cos\beta\cos\alpha + \sin\beta\sin\alpha
$$

$$
\sin(\beta - \alpha) = \sin\beta\cos\alpha - \cos\beta\sin\alpha
$$

Each entry of the product matrix is now matched to one of these identities:

**Entry $(0, 0)$:**

$$
\cos\alpha\cos\beta + \sin\alpha\sin\beta = \mathbf{\cos(\beta - \alpha)}
$$

**Entry $(0, 1)$:**

$$
-\cos\alpha\sin\beta + \sin\alpha\cos\beta = -(\cos\alpha\sin\beta - \sin\alpha\cos\beta) = \mathbf{-\sin(\beta - \alpha)}
$$

**Entry $(1, 0)$:**

$$
-\sin\alpha\cos\beta + \cos\alpha\sin\beta = \cos\alpha\sin\beta - \sin\alpha\cos\beta = \mathbf{\sin(\beta - \alpha)}
$$

**Entry $(1, 1)$:**

$$
\sin\alpha\sin\beta + \cos\alpha\cos\beta = \mathbf{\cos(\beta - \alpha)}
$$

### The Result

Substituting the angle-addition identities into the product matrix:

$$
R_{-\alpha} \cdot R_\beta = \begin{bmatrix} \cos(\beta - \alpha) & -\sin(\beta - \alpha) \\ \sin(\beta - \alpha) & \cos(\beta - \alpha) \end{bmatrix} = R_{\beta - \alpha}
$$

This is the standard $2 \times 2$ rotation matrix for angle $\beta - \alpha$. Therefore:

$$
R_\alpha^\top R_\beta = R_{\beta - \alpha}
$$

Setting $\alpha = m\theta_i$ and $\beta = n\theta_i$ for any dimension pair $i$ yields the rotation matrix for the relative angle $(n-m)\theta_i$:

$$
R_{m\theta_i}^\top R_{n\theta_i} = R_{(n-m)\theta_i}
$$

Because this relative-angle identity holds independently for every block on the diagonal, the full position-dependent matrix satisfies:

$$
R_m^\top R_n = R_{n-m}
$$

The product of the transposed rotation at position $m$ and the rotation at position $n$ is a single rotation whose angle depends only on the offset $n - m$. This is the rotation composition identity, and it is exact (not an approximation), because it follows from the algebraic properties of sine and cosine.

For the full $3 \times 3$ block-diagonal matrix used in the toy model, the identity applies to the upper-left $2 \times 2$ block, and the lower-right $1 \times 1$ identity block trivially satisfies $1 \cdot 1 = 1$. The composition identity therefore holds for the full $3 \times 3$ rotation matrix at every position.

## Numerical Verification with the Toy Model

The algebraic proof establishes the identity in general. This section verifies it concretely using the rotated vectors from Chapter 6. The pair chosen for verification is `quick` (position 1) and `fox` (position 3), with offset $\Delta = n - m = 2$.

### Method 1: Direct Dot Product of Rotated Vectors ($\mathbf{q}'^{\top}_1 \mathbf{k}'_3$)

The rotated vectors at positions 1 and 3, computed in Chapter 6:

$$
\mathbf{q}'_1 = \begin{bmatrix} \phantom{-}0.3322 \\ \phantom{-}0.2027 \\ -0.2700 \end{bmatrix}, \qquad \mathbf{k}'_3 = \begin{bmatrix} \phantom{-}0.0439 \\ -0.1174 \\ -0.0500 \end{bmatrix}
$$

The dot product is computed term by term:

$$
\mathbf{q}'^{\top}_1 \mathbf{k}'_3 = (0.3322)(0.0439) + (0.2027)(-0.1174) + (-0.2700)(-0.0500) = \mathbf{0.0043}
$$

### Method 2: Relative Rotation Applied to Unrotated Vectors ($\mathbf{q}_1^\top R_2 \, \mathbf{k}_3$)

The relative position requirement predicts that the same score can be obtained by applying the relative rotation $R_{\Delta} = R_{3-1} = R_2$ to the unrotated key vector, then taking the dot product with the unrotated query vector.

The unrotated vectors from Chapter 4:

$$
\mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.35 \\ -0.17 \\ -0.27 \end{bmatrix}, \qquad \mathbf{k}_3 = \begin{bmatrix} -0.06 \\ \phantom{-}0.11 \\ -0.05 \end{bmatrix}
$$

First, compute $R_2 \mathbf{k}_3$. The rotation matrix at $t = 2$ (from Chapter 6):

$$
R_2 = \begin{bmatrix} -0.4161 & -0.9093 & 0 \\ \phantom{-}0.9093 & -0.4161 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

Applying $R_2$ to $\mathbf{k}_3$, component by component:

$$
(R_2 \mathbf{k}_3)[0] = (-0.4161)(-0.06) + (-0.9093)(0.11) = \mathbf{-0.0751}
$$

$$
(R_2 \mathbf{k}_3)[1] = (0.9093)(-0.06) + (-0.4161)(0.11) = \mathbf{-0.1003}
$$

$$
(R_2 \mathbf{k}_3)[2] = -0.05 \qquad \text{(identity, unpaired dimension)}
$$

$$
R_2 \mathbf{k}_3 = \begin{bmatrix} -0.0751 \\ -0.1003 \\ -0.0500 \end{bmatrix}
$$

Now compute $\mathbf{q}_1^\top (R_2 \mathbf{k}_3)$:

$$
\mathbf{q}_1^\top (R_2 \mathbf{k}_3) = (0.35)(-0.0751) + (-0.17)(-0.1003) + (-0.27)(-0.0500) = \mathbf{0.0043}
$$

### Verification

Both methods produce the same scalar:

$$
\mathbf{q}'^{\top}_1 \mathbf{k}'_3 = \mathbf{0.0043} = \mathbf{q}_1^\top R_2 \, \mathbf{k}_3
$$

The direct dot product of the rotated vectors (Method 1) equals the dot product obtained by applying only the relative rotation $R_2$ to the unrotated key (Method 2). The absolute positions 1 and 3 have disappeared from the computation; only the offset $\Delta = 2$ remains.

This is the relative-distance property in action. If `quick` appeared at position 5 and `fox` at position 7 (same content, same offset $\Delta = 2$), the same rotation $R_2$ would produce the same relevance score. The score $0.0043$ is determined by the content of `quick` and `fox` and by their separation of 2 positions, regardless of where in the sequence that separation occurs.

## The Full Post-RoPE Relevance Score Matrix

The dot product $A'_{ij} = \mathbf{q}'^{\top}_i \mathbf{k}'_j$ is now computed for all 16 pairs of positions using the rotated vectors from Chapter 6:

<div style="font-size: 0.85em; overflow-x: auto;">

$$
\mathbf{q}'_0 = \begin{bmatrix} -0.0800 \\ -0.1300 \\ \phantom{-}0.2100 \end{bmatrix}, \quad \mathbf{q}'_1 = \begin{bmatrix} \phantom{-}0.3322 \\ \phantom{-}0.2027 \\ -0.2700 \end{bmatrix}, \quad \mathbf{q}'_2 = \begin{bmatrix} -0.3899 \\ -0.2774 \\ -0.0700 \end{bmatrix}, \quad \mathbf{q}'_3 = \begin{bmatrix} \phantom{-}0.0212 \\ \phantom{-}0.0778 \\ \phantom{-}0.1500 \end{bmatrix}
$$

$$
\mathbf{k}'_0 = \begin{bmatrix} -0.1500 \\ \phantom{-}0.1000 \\ -0.0400 \end{bmatrix}, \quad \mathbf{k}'_1 = \begin{bmatrix} \phantom{-}0.0371 \\ \phantom{-}0.2614 \\ -0.3200 \end{bmatrix}, \quad \mathbf{k}'_2 = \begin{bmatrix} \phantom{-}0.0880 \\ \phantom{-}0.2162 \\ \phantom{-}0.3600 \end{bmatrix}, \quad \mathbf{k}'_3 = \begin{bmatrix} \phantom{-}0.0439 \\ -0.1174 \\ -0.0500 \end{bmatrix}
$$

</div>

**Row 0** (`The` queries each position):

$$
A'_{00} = (-0.0800)(-0.1500) + (-0.1300)(0.1000) + (0.2100)(-0.0400) = \mathbf{-0.0094}
$$

$$
A'_{01} = (-0.0800)(0.0371) + (-0.1300)(0.2614) + (0.2100)(-0.3200) = \mathbf{-0.1041}
$$

$$
A'_{02} = (-0.0800)(0.0880) + (-0.1300)(0.2162) + (0.2100)(0.3600) = \mathbf{0.0405}
$$

$$
A'_{03} = (-0.0800)(0.0439) + (-0.1300)(-0.1174) + (0.2100)(-0.0500) = \mathbf{0.0012}
$$

**Row 1** (`quick` queries each position):

$$
A'_{10} = (0.3322)(-0.1500) + (0.2027)(0.1000) + (-0.2700)(-0.0400) = \mathbf{-0.0188}
$$

$$
A'_{11} = (0.3322)(0.0371) + (0.2027)(0.2614) + (-0.2700)(-0.3200) = \mathbf{0.1517}
$$

$$
A'_{12} = (0.3322)(0.0880) + (0.2027)(0.2162) + (-0.2700)(0.3600) = \mathbf{-0.0241}
$$

$$
A'_{13} = (0.3322)(0.0439) + (0.2027)(-0.1174) + (-0.2700)(-0.0500) = \mathbf{0.0043}
$$

**Row 2** (`brown` queries each position):

$$
A'_{20} = (-0.3899)(-0.1500) + (-0.2774)(0.1000) + (-0.0700)(-0.0400) = \mathbf{0.0335}
$$

$$
A'_{21} = (-0.3899)(0.0371) + (-0.2774)(0.2614) + (-0.0700)(-0.3200) = \mathbf{-0.0646}
$$

$$
A'_{22} = (-0.3899)(0.0880) + (-0.2774)(0.2162) + (-0.0700)(0.3600) = \mathbf{-0.1195}
$$

$$
A'_{23} = (-0.3899)(0.0439) + (-0.2774)(-0.1174) + (-0.0700)(-0.0500) = \mathbf{0.0190}
$$

**Row 3** (`fox` queries each position):

$$
A'_{30} = (0.0212)(-0.1500) + (0.0778)(0.1000) + (0.1500)(-0.0400) = \mathbf{-0.0014}
$$

$$
A'_{31} = (0.0212)(0.0371) + (0.0778)(0.2614) + (0.1500)(-0.3200) = \mathbf{-0.0269}
$$

$$
A'_{32} = (0.0212)(0.0880) + (0.0778)(0.2162) + (0.1500)(0.3600) = \mathbf{0.0727}
$$

$$
A'_{33} = (0.0212)(0.0439) + (0.0778)(-0.1174) + (0.1500)(-0.0500) = \mathbf{-0.0157}
$$

### The Complete Post-RoPE Relevance Score Matrix

$$
A' = \begin{bmatrix} -0.0094 & -0.1041 & \phantom{-}0.0405 & \phantom{-}0.0012 \\ -0.0188 & \phantom{-}0.1517 & -0.0241 & \phantom{-}0.0043 \\ \phantom{-}0.0335 & -0.0646 & -0.1195 & \phantom{-}0.0190 \\ -0.0014 & -0.0269 & \phantom{-}0.0727 & -0.0157 \end{bmatrix}
$$

## Comparison with the Pre-RoPE Matrix

The pre-RoPE relevance score matrix from Chapter 4:

$$
A = \begin{bmatrix} -0.0094 & -0.1007 & \phantom{-}0.0849 & -0.0200 \\ -0.0587 & \phantom{-}0.1517 & -0.0123 & -0.0262 \\ \phantom{-}0.0633 & \phantom{-}0.0525 & -0.1195 & \phantom{-}0.0606 \\ -0.0125 & -0.0592 & \phantom{-}0.0660 & -0.0157 \end{bmatrix}
$$

Several structural observations emerge from comparing $A$ and $A'$.

**The diagonal is unchanged.** The diagonal entries $A'_{ii} = A_{ii}$ for all $i$:

| Position | $A_{ii}$ | $A'_{ii}$ |
|---|---|---|
| 0 (`The`) | $-0.0094$ | $-0.0094$ |
| 1 (`quick`) | $\phantom{-}0.1517$ | $\phantom{-}0.1517$ |
| 2 (`brown`) | $-0.1195$ | $-0.1195$ |
| 3 (`fox`) | $-0.0157$ | $-0.0157$ |

This is a direct consequence of the rotation composition identity. For the diagonal, $m = n$, so the relative rotation is $R_{n-n} = R_0 = I$ (the identity matrix). The self-relevance score $\mathbf{q}_i^\top R_0 \mathbf{k}_i = \mathbf{q}_i^\top \mathbf{k}_i$ is the same as the unrotated dot product. A token's relevance to itself is unaffected by its absolute position, because the relative offset to itself is always zero.

**Off-diagonal entries have changed.** Every off-diagonal entry differs between $A$ and $A'$:

| Token Pair | Offset $\Delta$ | $A_{ij}$ (pre-RoPE) | $A'_{ij}$ (post-RoPE) |
|---|---|---|---|
| `The` $\to$ `quick` | $\phantom{-}1$ | $-0.1007$ | $-0.1041$ |
| `The` $\to$ `brown` | $\phantom{-}2$ | $\phantom{-}0.0849$ | $\phantom{-}0.0405$ |
| `The` $\to$ `fox` | $\phantom{-}3$ | $-0.0200$ | $\phantom{-}0.0012$ |
| `quick` $\to$ `The` | $-1$ | $-0.0587$ | $-0.0188$ |
| `quick` $\to$ `brown` | $\phantom{-}1$ | $-0.0123$ | $-0.0241$ |
| `quick` $\to$ `fox` | $\phantom{-}2$ | $-0.0262$ | $\phantom{-}0.0043$ |
| `brown` $\to$ `The` | $-2$ | $\phantom{-}0.0633$ | $\phantom{-}0.0335$ |
| `brown` $\to$ `quick` | $-1$ | $\phantom{-}0.0525$ | $-0.0646$ |
| `brown` $\to$ `fox` | $\phantom{-}1$ | $\phantom{-}0.0606$ | $\phantom{-}0.0190$ |
| `fox` $\to$ `The` | $-3$ | $-0.0125$ | $-0.0014$ |
| `fox` $\to$ `quick` | $-2$ | $-0.0592$ | $-0.0269$ |
| `fox` $\to$ `brown` | $-1$ | $\phantom{-}0.0660$ | $\phantom{-}0.0727$ |

The rotation has modified the relevance landscape. Consider the pair `The` $\to$ `brown` (positions 0 and 2): the pre-RoPE score $0.0849$ drops to $0.0405$ after RoPE. The rotation $R_2$ applied to the relative offset $\Delta = 2$ has reduced the apparent relevance. Meanwhile, `quick` $\to$ `fox` (positions 1 and 3, same offset $\Delta = 2$) shifts from $-0.0262$ to $0.0043$, crossing from negative to positive. The same relative rotation $R_2$ produces different effects on different content pairs, because the rotation interacts with the content vectors differently. This is by design: the score depends on both content and relative position.

**Permutation invariance is broken.** The pre-RoPE matrix $A$ satisfies $A_{rev} = PAP^\top$ (Chapter 4): reversing the input sequence rearranges the scores but does not change them. The post-RoPE matrix $A'$ does not satisfy this property. In the reversed sequence `fox` `brown` `quick` `The`, the token `fox` would occupy position 0 and `The` would occupy position 3. Their relative offset would be $\Delta = 3 - 0 = 3$ (not $\Delta = -3$ as in the original sequence). Because $R_3 \neq R_{-3}$, the relevance score between `fox` and `The` would differ from the original ordering. RoPE has broken permutation invariance through the mechanism of position-dependent rotation.

## Grounding the Result

The relevance score between `quick` (position 1) and `fox` (position 3) is $A'_{13} = 0.0043$. This score depends on the semantic content of `quick` and `fox` (encoded in the query vector $\mathbf{q}_1$ and key vector $\mathbf{k}_3$) and on the offset $\Delta = 2$ between their positions (encoded in the rotation $R_2$). It does not depend on the absolute position indices 1 and 3.

If `quick` appeared at position 5 and `fox` at position 7, the content vectors $\mathbf{q}$ and $\mathbf{k}$ would be identical (same tokens, same projection matrices), and the relative rotation would be $R_{7-5} = R_2$ (same offset). The relevance score would be $\mathbf{q}^\top R_2 \mathbf{k} = 0.0043$, unchanged. If `quick` appeared at position 100 and `fox` at position 102, the score would again be $0.0043$. The absolute positions are irrelevant; only the offset $\Delta = 2$ between the two tokens determines the rotational transformation.

This is the relative position requirement from Chapter 4, now satisfied by algebraic construction.

## Why This Property Matters

The relative-distance property of RoPE has three consequences that distinguish it from additive positional encoding.

**Relative relationships, not absolute labels.** The model learns how tokens at different separations interact, not what happens at position 47 specifically. A verb three positions after its subject receives the same relative rotation regardless of whether the subject appears at position 0, position 50, or position 500. This aligns with the linguistic observation that syntactic and semantic relationships between tokens typically depend on their relative displacement, not on their absolute indices within the sequence.

**Length generalization.** Because the rotation $R_\Delta$ depends only on the offset $\Delta$, the mechanism encounters a rotation for offset $\Delta = 200$ during inference even if the longest training sequence had length 150 (provided $\Delta = 200$ arose in some training context). Sinusoidal absolute PE, by contrast, assigns absolute position encodings that degrade for unseen positions. RoPE's relative encoding extends more naturally to sequence lengths beyond the training distribution, though practical generalization still requires careful frequency scaling (the subject of Chapter 8).

**Exact algebraic identity.** The property $R_m^\top R_n = R_{n-m}$ is not an approximation learned during training, nor an empirical observation that holds approximately for most inputs. It is an algebraic identity that follows from the angle-addition formulas for sine and cosine. Every rotated dot product in every attention head at every layer satisfies this property exactly, because it is a consequence of the mathematical structure of rotation matrices, not of the learned parameters. The model's positional encoding is correct by construction.

The rotation composition identity, proved from the angle-addition identities and verified numerically with the toy model, completes the mathematical foundation of RoPE. The next chapter surveys the broader landscape of positional encoding mechanisms, including learned absolute encodings, relative position biases, ALiBi, iRoPE, and frequency-scaling extensions for long-context generalization.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
