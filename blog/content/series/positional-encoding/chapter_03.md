# Part 3: Element-Wise Addition and the Positionally-Enriched Tensor

<!-- SUMMARY: The positional encoding matrix is added element-wise to the embedding tensor, producing a positionally-enriched tensor whose similarity matrix differs from the original. Permutation invariance is broken: reversing the input sequence and reapplying position-appropriate encodings yields a different set of pairwise similarities. This chapter computes the enriched tensor, verifies the symmetry-breaking property, and identifies the structural limitations of additive positional encoding that motivate the transition to rotary embeddings. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter derived the sinusoidal positional encoding matrix $PE \in \mathbb{R}^{4 \times 3},$ a deterministic function that assigns a unique, bounded vector to each position in the sequence. The embedding tensor $X \in \mathbb{R}^{4 \times 3}$ from Chapter 1 carries the distributional signatures of the tokens `The`, `quick`, `brown`, `fox` but is invariant under row permutations. This chapter combines the two matrices, producing a tensor in which each row encodes both the identity of the token and the position it occupies.

## The Addition Operation

The positionally-enriched tensor is formed by element-wise addition:

$$
X_{pos} = X + PE
$$

Both $X$ and $PE$ are $4 \times 3$ matrices. Each entry of $X_{pos}$ is the sum of the corresponding embedding component and the corresponding positional encoding component:

$$
(X_{pos})_{tc} = X_{tc} + PE_{tc}
$$

for position $t \in \{0, 1, 2, 3\}$ and dimension $c \in \{0, 1, 2\}.$ The operation requires no learned parameters: it is a fixed arithmetic combination of the embedding lookup (from the Embeddings series) and the sinusoidal formula (from Chapter 2).

## Computing the Enriched Tensor

The two matrices to be added:

$$
X = \begin{bmatrix} \phantom{-}0.1 & -0.4 & \phantom{-}0.2 \\ \phantom{-}0.5 & \phantom{-}0.1 & -0.8 \\ -0.3 & \phantom{-}0.9 & \phantom{-}0.4 \\ \phantom{-}0.2 & -0.2 & \phantom{-}0.1 \end{bmatrix}, \quad PE = \begin{bmatrix} \phantom{-}0.0000 & \phantom{-}1.0000 & \phantom{-}0.0000 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & \phantom{-}0.0022 \\ \phantom{-}0.9093 & -0.4161 & \phantom{-}0.0043 \\ \phantom{-}0.1411 & -0.9900 & \phantom{-}0.0065 \end{bmatrix}
$$

### Position $t = 0$ (`The`)

$$
(X_{pos})_{0,0} = 0.1000 + 0.0000 = \mathbf{0.1000}
$$

$$
(X_{pos})_{0,1} = -0.4000 + 1.0000 = \mathbf{0.6000}
$$

$$
(X_{pos})_{0,2} = 0.2000 + 0.0000 = \mathbf{0.2000}
$$

The positional encoding at $t = 0$ is $\begin{bmatrix} 0 & 1 & 0 \end{bmatrix}$ (the sine components are zero, the cosine is at its maximum). Dimension 1 shifts from $-0.4$ to $0.6,$ a displacement of $+1.0.$ Dimensions 0 and 2 are unchanged.

### Position $t = 1$ (`quick`)

$$
(X_{pos})_{1,0} = 0.5000 + 0.8415 = \mathbf{1.3415}
$$

$$
(X_{pos})_{1,1} = 0.1000 + 0.5403 = \mathbf{0.6403}
$$

$$
(X_{pos})_{1,2} = -0.8000 + 0.0022 = \mathbf{-0.7978}
$$

At position 1, the $\sin(1)$ and $\cos(1)$ components carry substantial magnitude. Dimension 0 nearly triples (from $0.5$ to $1.3415$). Dimension 2, governed by the slow frequency $\omega_1 \approx 0.002154,$ shifts by less than $0.003.$

### Position $t = 2$ (`brown`)

$$
(X_{pos})_{2,0} = -0.3000 + 0.9093 = \mathbf{0.6093}
$$

$$
(X_{pos})_{2,1} = 0.9000 + (-0.4161) = \mathbf{0.4839}
$$

$$
(X_{pos})_{2,2} = 0.4000 + 0.0043 = \mathbf{0.4043}
$$

The sign of dimension 0 flips: the original embedding component is $-0.3,$ but the positional encoding adds $0.9093$ (close to the maximum of $\sin$), pulling the sum to $+0.6093.$ Dimension 1 decreases because $\cos(2) \approx \mathbf{-0.4161}$ is negative at 2 radians.

### Position $t = 3$ (`fox`)

$$
(X_{pos})_{3,0} = 0.2000 + 0.1411 = \mathbf{0.3411}
$$

$$
(X_{pos})_{3,1} = -0.2000 + (-0.9900) = \mathbf{-1.1900}
$$

$$
(X_{pos})_{3,2} = 0.1000 + 0.0065 = \mathbf{0.1065}
$$

At 3 radians ($\approx 171.9°$), $\cos(3) \approx \mathbf{-0.9900}$ is near its negative extreme, pushing dimension 1 to $-1.19.$ This is the most extreme displacement in the matrix: the embedding component ($-0.2$) and the positional component ($-0.99$) reinforce each other.

### The Complete Positionally-Enriched Tensor

$$
X_{pos} = X + PE = \begin{bmatrix} \phantom{-}0.1000 & \phantom{-}0.6000 & \phantom{-}0.2000 \\ \phantom{-}1.3415 & \phantom{-}0.6403 & -0.7978 \\ \phantom{-}0.6093 & \phantom{-}0.4839 & \phantom{-}0.4043 \\ \phantom{-}0.3411 & -1.1900 & \phantom{-}0.1065 \end{bmatrix}_{4 \times 3}
$$

Each row of $X_{pos}$ is no longer the pure distributional signature of a token. Row 2 is not the embedding for `brown` as it appears across the entire training corpus. It is the embedding for `brown` combined with the positional fingerprint of position 2 in this specific sequence.

## The Similarity Matrix After Positional Encoding

In Chapter 1, the pairwise dot-product similarity matrix $S = XX^\top$ was computed for the original embedding tensor. That matrix was invariant under row permutations: reordering the sequence rearranged the entries of $S$ without changing any similarity value. The positionally-enriched tensor $X_{pos}$ produces a new similarity matrix:

$$
S_{pos} = X_{pos} \, X_{pos}^\top = \begin{bmatrix} \phantom{-}0.1000 & \phantom{-}0.6000 & \phantom{-}0.2000 \\ \phantom{-}1.3415 & \phantom{-}0.6403 & -0.7978 \\ \phantom{-}0.6093 & \phantom{-}0.4839 & \phantom{-}0.4043 \\ \phantom{-}0.3411 & -1.1900 & \phantom{-}0.1065 \end{bmatrix} \begin{bmatrix} \phantom{-}0.1000 & \phantom{-}1.3415 & \phantom{-}0.6093 & \phantom{-}0.3411 \\ \phantom{-}0.6000 & \phantom{-}0.6403 & \phantom{-}0.4839 & -1.1900 \\ \phantom{-}0.2000 & -0.7978 & \phantom{-}0.4043 & \phantom{-}0.1065 \end{bmatrix}
$$

Each entry $(S_{pos})_{ij} = \mathbf{x}^{pos}_i \cdot \mathbf{x}^{pos}_j$ is the dot product of the enriched vectors at positions $i$ and $j.$

### Computing the Entries

**Diagonal entries** (squared norms of the enriched vectors):

$$
(S_{pos})_{00} = (0.1000)^2 + (0.6000)^2 + (0.2000)^2 = \mathbf{0.41}
$$

$$
(S_{pos})_{11} = (1.3415)^2 + (0.6403)^2 + (-0.7978)^2 = \mathbf{2.85}
$$

$$
(S_{pos})_{22} = (0.6093)^2 + (0.4839)^2 + (0.4043)^2 = \mathbf{0.77}
$$

$$
(S_{pos})_{33} = (0.3411)^2 + (-1.1900)^2 + (0.1065)^2 = \mathbf{1.54}
$$

**Off-diagonal entries** (pairwise similarities):

$$
(S_{pos})_{01} = (0.1000)(1.3415) + (0.6000)(0.6403) + (0.2000)(-0.7978)
$$

$$
= 0.1341 + 0.3842 + (-0.1596) = \mathbf{0.36}
$$

$$
(S_{pos})_{02} = (0.1000)(0.6093) + (0.6000)(0.4839) + (0.2000)(0.4043)
$$

$$
= 0.0609 + 0.2903 + 0.0809 = \mathbf{0.43}
$$

$$
(S_{pos})_{03} = (0.1000)(0.3411) + (0.6000)(-1.1900) + (0.2000)(0.1065)
$$

$$
= 0.0341 + (-0.7140) + 0.0213 = \mathbf{-0.66}
$$

$$
(S_{pos})_{12} = (1.3415)(0.6093) + (0.6403)(0.4839) + (-0.7978)(0.4043)
$$

$$
= 0.8174 + 0.3098 + (-0.3226) = \mathbf{0.80}
$$

$$
(S_{pos})_{13} = (1.3415)(0.3411) + (0.6403)(-1.1900) + (-0.7978)(0.1065)
$$

$$
= 0.4576 + (-0.7620) + (-0.0849) = \mathbf{-0.39}
$$

$$
(S_{pos})_{23} = (0.6093)(0.3411) + (0.4839)(-1.1900) + (0.4043)(0.1065)
$$

$$
= 0.2078 + (-0.5758) + 0.0430 = \mathbf{-0.32}
$$

### The Complete Similarity Matrix

$$
S_{pos} = \begin{bmatrix} \phantom{-}0.41 & \phantom{-}0.36 & \phantom{-}0.43 & -0.66 \\ \phantom{-}0.36 & \phantom{-}2.85 & \phantom{-}0.80 & -0.39 \\ \phantom{-}0.43 & \phantom{-}0.80 & \phantom{-}0.77 & -0.32 \\ -0.66 & -0.39 & -0.32 & \phantom{-}1.54 \end{bmatrix}
$$

## Comparison with the Original Similarity Matrix

The original similarity matrix from Chapter 1:

$$
S = \begin{bmatrix} \phantom{-}0.21 & -0.15 & -0.31 & \phantom{-}0.12 \\ -0.15 & \phantom{-}0.90 & -0.38 & \phantom{-}0.00 \\ -0.31 & -0.38 & \phantom{-}1.06 & -0.20 \\ \phantom{-}0.12 & \phantom{-}0.00 & -0.20 & \phantom{-}0.09 \end{bmatrix}
$$

Every entry has changed. Some qualitative relationships have reversed entirely. In the original $S,$ the similarity between `The` (position 0) and `brown` (position 2) was $S_{02} = -0.31$ (the embeddings pointed in roughly opposite directions). After positional encoding, $(S_{pos})_{02} = 0.43$: the enriched vectors are now positively aligned, because the positional components at positions 0 and 2 have shifted both vectors into a region of the space where their dot product is positive.

The positional encoding has not merely perturbed the similarity scores. It has restructured the geometry of the representation. The enriched vectors encode a superposition of two signals (semantic content and sequential position), and the resulting dot products reflect both.

## Breaking Permutation Invariance

The decisive test is whether the reversed sequence `fox` `brown` `quick` `The` still produces an equivalent similarity matrix. In Chapter 1, the reversed sequence yielded $S' = PSP^\top$: the same similarity scores, relocated to new matrix positions. The question is whether the same invariance holds after positional encoding.

The reversal changes which token occupies each position. In the original ordering, `The` occupies position 0 and `fox` occupies position 3. In the reversed ordering, `fox` occupies position 0 and `The` occupies position 3. Because the positional encoding is a function of position (not of token identity), each token now receives a different positional vector than it received in the original ordering.

The reversed embedding tensor $X_{rev} = PX$ rearranges the rows of $X$ while leaving their vector components intact:

$$
X_{rev} = \begin{bmatrix} \phantom{-}0.2 & -0.2 & \phantom{-}0.1 \\ -0.3 & \phantom{-}0.9 & \phantom{-}0.4 \\ \phantom{-}0.5 & \phantom{-}0.1 & -0.8 \\ \phantom{-}0.1 & -0.4 & \phantom{-}0.2 \end{bmatrix} \begin{matrix} \leftarrow \text{fox} \\ \leftarrow \text{brown} \\ \leftarrow \text{quick} \\ \leftarrow \text{The} \end{matrix}
$$

The positionally-enriched reversed tensor is formed by adding the original positional encoding matrix $PE$ to this reversed embedding tensor:

$$
X_{pos}^{rev} = X_{rev} + PE = PX + PE
$$

Note that $PE$ is the same matrix in both cases: row $t$ of $PE$ always encodes position $t,$ regardless of which token occupies that position. This is the mechanism by which positional encoding breaks the symmetry.

$$
X_{pos}^{rev} = \begin{bmatrix} \phantom{-}0.2 & -0.2 & \phantom{-}0.1 \\ -0.3 & \phantom{-}0.9 & \phantom{-}0.4 \\ \phantom{-}0.5 & \phantom{-}0.1 & -0.8 \\ \phantom{-}0.1 & -0.4 & \phantom{-}0.2 \end{bmatrix} + \begin{bmatrix} \phantom{-}0.0000 & \phantom{-}1.0000 & \phantom{-}0.0000 \\ \phantom{-}0.8415 & \phantom{-}0.5403 & \phantom{-}0.0022 \\ \phantom{-}0.9093 & -0.4161 & \phantom{-}0.0043 \\ \phantom{-}0.1411 & -0.9900 & \phantom{-}0.0065 \end{bmatrix} = \begin{bmatrix} \phantom{-}0.2000 & \phantom{-}0.8000 & \phantom{-}0.1000 \\ \phantom{-}0.5415 & \phantom{-}1.4403 & \phantom{-}0.4022 \\ \phantom{-}1.4093 & -0.3161 & -0.7957 \\ \phantom{-}0.2411 & -1.3900 & \phantom{-}0.2065 \end{bmatrix}
$$

To compute the similarity matrix of the reversed, positionally-encoded sequence, the pairwise dot products between the rows of $X_{pos}^{rev}$ are computed by multiplying it with its transpose:

$$
S_{pos}^{rev} = X_{pos}^{rev} \, (X_{pos}^{rev})^\top = \begin{bmatrix} \phantom{-}0.2000 & \phantom{-}0.8000 & \phantom{-}0.1000 \\ \phantom{-}0.5415 & \phantom{-}1.4403 & \phantom{-}0.4022 \\ \phantom{-}1.4093 & -0.3161 & -0.7957 \\ \phantom{-}0.2411 & -1.3900 & \phantom{-}0.2065 \end{bmatrix} \begin{bmatrix} \phantom{-}0.2000 & \phantom{-}0.5415 & \phantom{-}1.4093 & \phantom{-}0.2411 \\ \phantom{-}0.8000 & \phantom{-}1.4403 & -0.3161 & -1.3900 \\ \phantom{-}0.1000 & \phantom{-}0.4022 & -0.7957 & \phantom{-}0.2065 \end{bmatrix}
$$

Performing these multiplications yields the new similarity scores:

$$
S_{pos}^{rev} = \begin{bmatrix} \phantom{-}0.69 & \phantom{-}1.30 & -0.05 & -1.04 \\ \phantom{-}1.30 & \phantom{-}2.53 & -0.01 & -1.79 \\ -0.05 & -0.01 & \phantom{-}2.72 & \phantom{-}0.61 \\ -1.04 & -1.79 & \phantom{-}0.61 & \phantom{-}2.03 \end{bmatrix}
$$

### The Symmetry Is Broken

In Chapter 1, the similarity between `fox` and `brown` was $-0.20$ regardless of their positions in the sequence. After positional encoding, the similarity between these two tokens depends on where they appear:

| Token Pair | Original $S$ | $S_{pos}$ (original order) | $S_{pos}^{rev}$ (reversed order) |
|---|---|---|---|
| (`The`, `quick`) | $-0.15$ | $\phantom{-}0.36$ | $\phantom{-}0.61$ |
| (`The`, `brown`) | $-0.31$ | $\phantom{-}0.43$ | $-1.79$ |
| (`The`, `fox`) | $\phantom{-}0.12$ | $-0.66$ | $-1.04$ |
| (`quick`, `brown`) | $-0.38$ | $\phantom{-}0.80$ | $-0.01$ |
| (`quick`, `fox`) | $\phantom{-}0.00$ | $-0.39$ | $-0.05$ |
| (`brown`, `fox`) | $-0.20$ | $-0.32$ | $\phantom{-}1.30$ |

No pair retains the same similarity across the two orderings. The entry for (`brown`, `fox`) shifts from $-0.32$ in the original ordering to $1.30$ in the reversed ordering, a change not only in magnitude but in sign. The sequences `The` `quick` `brown` `fox` and `fox` `brown` `quick` `The` are no longer indistinguishable to any mechanism that computes dot-product similarities between the enriched vectors.

The algebraic reason is direct. In Chapter 1, $S' = PSP^\top$ held because $PX$ was simply a rearrangement of the same row vectors. After positional encoding, $X_{pos}^{rev} = PX + PE \neq P(X + PE) = PX_{pos}.$ The positional encoding matrix $PE$ is added based on position, not based on token identity. Permuting the tokens and then adding position-based encodings produces different vectors than adding the encodings first and then permuting.

## The Meaning of a Positionally-Enriched Vector

The vector for `brown` in the original embedding tensor $X$ is $\begin{bmatrix} -0.3 & \phantom{-}0.9 & \phantom{-}0.4 \end{bmatrix}.$ This is the abstract distributional signature shared by every occurrence of `brown` across the training corpus: `brown` at position 0, `brown` at position 47, `brown` at position 1000 all receive the same vector.

After positional encoding, the vector for `brown` at position 2 is $\begin{bmatrix} 0.6093 & 0.4839 & 0.4043 \end{bmatrix}.$ This is not the universal distributional signature of `brown`. It is `brown` at position 2 in this specific sequence. If `brown` appeared at position 5, it would receive a different positional encoding ($\mathbf{p}_5 \neq \mathbf{p}_2$) and produce a different enriched vector. The embedding now carries two signals: what the token means (from $X$) and where it occurs (from $PE$).

## The Information-Theoretic Cost of Additive Encoding

The addition $X_{pos} = X + PE$ superimposes the semantic signal and the positional signal in the same $d_{model}$ dimensions. The three components of the enriched vector for `brown` at position 2 ($0.6093,$ $0.4839,$ $0.4043$) encode both the distributional identity of `brown` and the positional fingerprint of position 2, entangled in each coordinate.

This element-wise addition irreversibly fuses the two signals. Given only the enriched sum $0.6093$ from the first component, there is no algebraic method to separate it back into its constituent parts ($-0.3$ and $0.9093$) without providing the independent positional vector $\mathbf{p}_2.$ The original embedding and the positional encoding are permanently entangled. Because the semantic meaning of the token and its sequential position must share the exact same $d_{model} = 3$ numerical coordinates, they compete for representational space. The network must expend parameter capacity in its subsequent layers (attention and feedforward transformations) to isolate and utilize these intertwined signals.

An alternative approach would concatenate the two signals rather than add them, producing vectors of dimension $2 \cdot d_{model}.$ Concatenation preserves both signals without interference but doubles the dimensionality, doubling the computational cost of every subsequent matrix multiplication. In production, $d_{model}$ is typically 4096 or larger; doubling it is prohibitively expensive. The additive approach accepts the cost of superposition to avoid the cost of doubled dimensionality.

A third approach (introduced in Chapter 4) avoids adding anything to the embedding at all, instead encoding position through a geometric operation applied inside the attention mechanism. This avoids both the superposition cost of addition and the dimensionality cost of concatenation.

## Structural Limitations of Absolute Additive Positional Encoding

The sinusoidal positional encoding satisfies the five design constraints enumerated in Chapter 2 and successfully breaks permutation invariance, as verified above. Three structural properties of the additive mechanism limit its effectiveness in practice.

### Single-Layer Injection

The positional encoding is added to the embedding tensor once, at the input to the first layer of the Transformer. Subsequent layers (attention, layer normalization, feedforward networks) transform the enriched vectors through nonlinear operations. With each successive transformation, the positional signal becomes increasingly entangled with the semantic signal and increasingly diluted. By the deeper layers of a model with dozens or hundreds of layers, the positional information injected at the input may have degraded substantially.

The model has no mechanism to refresh the positional signal at intermediate layers. Whatever positional information reaches the deeper layers must survive the intervening transformations intact. Empirical evidence confirms the limitation: models using additive positional encoding show degraded position-sensitivity in their deeper layers.

### Absolute Position Labels

The sinusoidal encoding assigns a fixed vector to each absolute position: position 0 always receives $\begin{bmatrix} 0 & 1 & 0 \end{bmatrix},$ position 1 always receives $\begin{bmatrix} 0.8415 & 0.5403 & 0.0022 \end{bmatrix},$ and so on, regardless of the sequence length or context. The token at position 5 carries the label "I am at position 5," not the relationally richer signal "I am 3 positions after the token at position 2."

Chapter 2 demonstrated that the sinusoidal formula satisfies relative representability (the relationship between any two positions can be expressed as a fixed rotation by angle $\omega \Delta$). This property exists in the encoding, but the additive injection mechanism does not exploit it directly. The positional signal is added to the embedding before the linear projections that produce the query and key vectors used in attention. After projection, the positional and semantic components are linearly combined, and the clean rotational relationship between positions is obscured by the projection weights. The model must learn to extract relative positional information from the entangled representation, rather than receiving it in a form that is relative by construction.

### Length Extrapolation Degradation

A model trained on sequences of maximum length $T_{train}$ encounters the positional encoding vectors $\mathbf{p}_0$ through $\mathbf{p}_{T_{train} - 1}$ during training. At inference, if a sequence of length $T > T_{train}$ is presented, the model must process positional vectors $\mathbf{p}_{T_{train}}, \ldots, \mathbf{p}_{T - 1}$ that it has never seen.

The sinusoidal formula produces well-defined values at any position $t$ (unlike learned positional embeddings, which have no representation beyond $T_{max}$). The values at unseen positions are valid points on the sinusoidal curves. The difficulty is that the model's learned attention patterns were calibrated to the range of positional encodings seen during training, and the statistical distribution of enriched vectors at positions beyond $T_{train}$ differs from what the model was trained on. In practice, this distributional shift causes performance degradation on sequences longer than the training length, even though the encoding itself remains mathematically well-defined.

## Looking Forward

The three limitations share a common root: the additive mechanism treats positional encoding as a preprocessing step, applied once to the input and then left to survive the subsequent computation. The position information is a static addendum to the embedding, not an active participant in the attention computation that determines which tokens attend to which.

The next chapter introduces the query-key framework that underlies the attention mechanism and formalizes the requirement that positional encoding should produce relevance scores that depend on relative position, not absolute position labels. That requirement motivates a fundamentally different approach: encoding position not by adding a vector to the embedding, but by rotating vectors inside the attention mechanism itself.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
