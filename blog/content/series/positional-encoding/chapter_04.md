# Part 4: The Query-Key Framework and the Relative Position Requirement

<!-- SUMMARY: The attention mechanism computes relevance scores between token positions using learned query and key projections. This chapter introduces the minimal query-key framework, computes the relevance score matrix for the toy model, and demonstrates that the scores are invariant under input permutations. The relative position requirement is stated formally, additive sinusoidal encoding is shown to violate it structurally, and Rotary Position Embeddings are previewed as the mechanism that satisfies it by construction. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding chapter demonstrated that additive sinusoidal positional encoding breaks permutation invariance in the dot-product similarity matrix $S_{pos} = X_{pos} X_{pos}^\top$. The three structural limitations identified (single-layer injection, absolute position labels, length extrapolation degradation) share a common root: the positional signal is added to the embedding once as a preprocessing step and then left to survive the subsequent computation.

This chapter introduces the specific component of the Transformer architecture where positional information has its greatest impact: the query-key dot product that determines which positions attend to which. The full attention mechanism (scoring, normalization, value aggregation) is the subject of the Transformers series. This chapter introduces only the two projections and the dot product that Rotary Position Embeddings operate on.

## Query and Key Projections

The attention mechanism requires a mechanism for each position in the sequence to assess the relevance of every other position. This assessment is performed through two learned linear projections that transform each embedding vector into two distinct roles.

Given the embedding vector $\mathbf{x}_t \in \mathbb{R}^{d_{model}}$ at position $t$, two projection matrices produce:

$$
\mathbf{q}_t = W_Q \, \mathbf{x}_t \qquad \text{(query vector)}
$$

$$
\mathbf{k}_t = W_K \, \mathbf{x}_t \qquad \text{(key vector)}
$$

where $W_Q, W_K \in \mathbb{R}^{d_{model} \times d_{model}}$ are learned parameter matrices. The query vector $\mathbf{q}_t$ encodes the question "what information does position $t$ seek?" and the key vector $\mathbf{k}_t$ encodes the answer "what information does position $t$ offer."

The **relevance score** between position $m$ (the querying position) and position $n$ (the attended position) is the dot product:

$$
a_{mn} = \mathbf{q}_m^\top \mathbf{k}_n
$$

Because both $\mathbf{q}_m$ and $\mathbf{k}_n$ are $d_{model} \times 1$ column vectors, the first vector must be transposed into a $1 \times d_{model}$ row vector to compute the scalar dot product via matrix multiplication. Moving the transpose to the second vector ($\mathbf{q}_m \mathbf{k}_n^\top$) would incorrectly compute a full $d_{model} \times d_{model}$ matrix. Reversing the order of the vectors entirely ($\mathbf{k}_n^\top \mathbf{q}_m$) computes the exact same scalar value, but standard mathematical convention places the querying vector on the left.

A large positive score indicates that position $m$ considers position $n$ highly relevant; a score near zero indicates low relevance; a negative score indicates that the content at position $n$ is actively irrelevant to the query at position $m$. The matrix $A \in \mathbb{R}^{T \times T}$ of all pairwise relevance scores determines the flow of information across the sequence.

The score $a_{mn}$ is not symmetric in general: position $m$ may consider position $n$ relevant without the converse holding, because $W_Q \neq W_K$ and therefore $\mathbf{q}_m^\top \mathbf{k}_n \neq \mathbf{q}_n^\top \mathbf{k}_m$.

## Defining the Projection Matrices

For the toy model with $d_{model} = 3$, the projection matrices $W_Q$ and $W_K$ are $3 \times 3$. The following hand-chosen values produce non-trivial projections with entries small enough for manual verification:

$$
W_Q = \begin{bmatrix} \phantom{-}0.2 & \phantom{-}0.1 & -0.3 \\ -0.1 & \phantom{-}0.4 & \phantom{-}0.2 \\ \phantom{-}0.3 & -0.2 & \phantom{-}0.5 \end{bmatrix}, \qquad W_K = \begin{bmatrix} \phantom{-}0.1 & \phantom{-}0.3 & -0.2 \\ \phantom{-}0.4 & -0.1 & \phantom{-}0.1 \\ -0.2 & \phantom{-}0.2 & \phantom{-}0.3 \end{bmatrix}
$$

In a trained model, these matrices are learned through gradient descent. The distinct values of $W_Q$ and $W_K$ allow query and key vectors to capture different aspects of the same embedding vector, which is essential for the asymmetric nature of the relevance computation.

## Computing the Query Vectors

Each query vector $\mathbf{q}_t = W_Q \, \mathbf{x}_t$ is a matrix-vector product. For the four positions of the toy sequence:

### Position $t = 0$ (`The`), $\mathbf{x}_0 = \begin{bmatrix} \phantom{-}0.1 & -0.4 & \phantom{-}0.2 \end{bmatrix}^\top$

$$
q_0[0] = (0.2)(0.1) + (0.1)(-0.4) + (-0.3)(0.2) = \mathbf{-0.08}
$$

$$
q_0[1] = (-0.1)(0.1) + (0.4)(-0.4) + (0.2)(0.2) = \mathbf{-0.13}
$$

$$
q_0[2] = (0.3)(0.1) + (-0.2)(-0.4) + (0.5)(0.2) = \mathbf{0.21}
$$

$$
\mathbf{q}_0 = \begin{bmatrix} -0.08 \\ -0.13 \\ \phantom{-}0.21 \end{bmatrix}
$$

### Position $t = 1$ (`quick`), $\mathbf{x}_1 = \begin{bmatrix} \phantom{-}0.5 & \phantom{-}0.1 & -0.8 \end{bmatrix}^\top$

$$
q_1[0] = (0.2)(0.5) + (0.1)(0.1) + (-0.3)(-0.8) = \mathbf{0.35}
$$

$$
q_1[1] = (-0.1)(0.5) + (0.4)(0.1) + (0.2)(-0.8) = \mathbf{-0.17}
$$

$$
q_1[2] = (0.3)(0.5) + (-0.2)(0.1) + (0.5)(-0.8) = \mathbf{-0.27}
$$

$$
\mathbf{q}_1 = \begin{bmatrix} \phantom{-}0.35 \\ -0.17 \\ -0.27 \end{bmatrix}
$$

### Position $t = 2$ (`brown`), $\mathbf{x}_2 = \begin{bmatrix} -0.3 & \phantom{-}0.9 & \phantom{-}0.4 \end{bmatrix}^\top$

$$
q_2[0] = (0.2)(-0.3) + (0.1)(0.9) + (-0.3)(0.4) = \mathbf{-0.09}
$$

$$
q_2[1] = (-0.1)(-0.3) + (0.4)(0.9) + (0.2)(0.4) = \mathbf{0.47}
$$

$$
q_2[2] = (0.3)(-0.3) + (-0.2)(0.9) + (0.5)(0.4) = \mathbf{-0.07}
$$

$$
\mathbf{q}_2 = \begin{bmatrix} -0.09 \\ \phantom{-}0.47 \\ -0.07 \end{bmatrix}
$$

### Position $t = 3$ (`fox`), $\mathbf{x}_3 = \begin{bmatrix} \phantom{-}0.2 & -0.2 & \phantom{-}0.1 \end{bmatrix}^\top$

$$
q_3[0] = (0.2)(0.2) + (0.1)(-0.2) + (-0.3)(0.1) = \mathbf{-0.01}
$$

$$
q_3[1] = (-0.1)(0.2) + (0.4)(-0.2) + (0.2)(0.1) = \mathbf{-0.08}
$$

$$
q_3[2] = (0.3)(0.2) + (-0.2)(-0.2) + (0.5)(0.1) = \mathbf{0.15}
$$

$$
\mathbf{q}_3 = \begin{bmatrix} -0.01 \\ -0.08 \\ \phantom{-}0.15 \end{bmatrix}
$$

## Computing the Key Vectors

Each key vector $\mathbf{k}_t = W_K \, \mathbf{x}_t$ is computed identically, using $W_K$ in place of $W_Q$.

### Position $t = 0$ (`The`)

$$
k_0[0] = (0.1)(0.1) + (0.3)(-0.4) + (-0.2)(0.2) = \mathbf{-0.15}
$$

$$
k_0[1] = (0.4)(0.1) + (-0.1)(-0.4) + (0.1)(0.2) = \mathbf{0.10}
$$

$$
k_0[2] = (-0.2)(0.1) + (0.2)(-0.4) + (0.3)(0.2) = \mathbf{-0.04}
$$

$$
\mathbf{k}_0 = \begin{bmatrix} -0.15 \\ \phantom{-}0.10 \\ -0.04 \end{bmatrix}
$$

### Position $t = 1$ (`quick`)

$$
k_1[0] = (0.1)(0.5) + (0.3)(0.1) + (-0.2)(-0.8) = \mathbf{0.24}
$$

$$
k_1[1] = (0.4)(0.5) + (-0.1)(0.1) + (0.1)(-0.8) = \mathbf{0.11}
$$

$$
k_1[2] = (-0.2)(0.5) + (0.2)(0.1) + (0.3)(-0.8) = \mathbf{-0.32}
$$

$$
\mathbf{k}_1 = \begin{bmatrix} \phantom{-}0.24 \\ \phantom{-}0.11 \\ -0.32 \end{bmatrix}
$$

### Position $t = 2$ (`brown`)

$$
k_2[0] = (0.1)(-0.3) + (0.3)(0.9) + (-0.2)(0.4) = \mathbf{0.16}
$$

$$
k_2[1] = (0.4)(-0.3) + (-0.1)(0.9) + (0.1)(0.4) = \mathbf{-0.17}
$$

$$
k_2[2] = (-0.2)(-0.3) + (0.2)(0.9) + (0.3)(0.4) = \mathbf{0.36}
$$

$$
\mathbf{k}_2 = \begin{bmatrix} \phantom{-}0.16 \\ -0.17 \\ \phantom{-}0.36 \end{bmatrix}
$$

### Position $t = 3$ (`fox`)

$$
k_3[0] = (0.1)(0.2) + (0.3)(-0.2) + (-0.2)(0.1) = \mathbf{-0.06}
$$

$$
k_3[1] = (0.4)(0.2) + (-0.1)(-0.2) + (0.1)(0.1) = \mathbf{0.11}
$$

$$
k_3[2] = (-0.2)(0.2) + (0.2)(-0.2) + (0.3)(0.1) = \mathbf{-0.05}
$$

$$
\mathbf{k}_3 = \begin{bmatrix} -0.06 \\ \phantom{-}0.11 \\ -0.05 \end{bmatrix}
$$

## The Relevance Score Matrix

The full $4 \times 4$ relevance score matrix $A$ contains the dot product $a_{ij} = \mathbf{q}_i^\top \mathbf{k}_j$ for every pair of positions. Each entry measures how relevant position $j$ is to the query at position $i$.

**Row 0** (`The` queries each position):

$$
a_{00} = (-0.08)(-0.15) + (-0.13)(0.10) + (0.21)(-0.04) = \mathbf{-0.0094}
$$

$$
a_{01} = (-0.08)(0.24) + (-0.13)(0.11) + (0.21)(-0.32) = \mathbf{-0.1007}
$$

$$
a_{02} = (-0.08)(0.16) + (-0.13)(-0.17) + (0.21)(0.36) = \mathbf{0.0849}
$$

$$
a_{03} = (-0.08)(-0.06) + (-0.13)(0.11) + (0.21)(-0.05) = \mathbf{-0.0200}
$$

**Row 1** (`quick` queries each position):

$$
a_{10} = (0.35)(-0.15) + (-0.17)(0.10) + (-0.27)(-0.04) = \mathbf{-0.0587}
$$

$$
a_{11} = (0.35)(0.24) + (-0.17)(0.11) + (-0.27)(-0.32) = \mathbf{0.1517}
$$

$$
a_{12} = (0.35)(0.16) + (-0.17)(-0.17) + (-0.27)(0.36) = \mathbf{-0.0123}
$$

$$
a_{13} = (0.35)(-0.06) + (-0.17)(0.11) + (-0.27)(-0.05) = \mathbf{-0.0262}
$$

**Row 2** (`brown` queries each position):

$$
a_{20} = (-0.09)(-0.15) + (0.47)(0.10) + (-0.07)(-0.04) = \mathbf{0.0633}
$$

$$
a_{21} = (-0.09)(0.24) + (0.47)(0.11) + (-0.07)(-0.32) = \mathbf{0.0525}
$$

$$
a_{22} = (-0.09)(0.16) + (0.47)(-0.17) + (-0.07)(0.36) = \mathbf{-0.1195}
$$

$$
a_{23} = (-0.09)(-0.06) + (0.47)(0.11) + (-0.07)(-0.05) = \mathbf{0.0606}
$$

**Row 3** (`fox` queries each position):

$$
a_{30} = (-0.01)(-0.15) + (-0.08)(0.10) + (0.15)(-0.04) = \mathbf{-0.0125}
$$

$$
a_{31} = (-0.01)(0.24) + (-0.08)(0.11) + (0.15)(-0.32) = \mathbf{-0.0592}
$$

$$
a_{32} = (-0.01)(0.16) + (-0.08)(-0.17) + (0.15)(0.36) = \mathbf{0.0660}
$$

$$
a_{33} = (-0.01)(-0.06) + (-0.08)(0.11) + (0.15)(-0.05) = \mathbf{-0.0157}
$$

### The Complete Relevance Score Matrix

$$
A = \begin{bmatrix} -0.0094 & -0.1007 & \phantom{-}0.0849 & -0.0200 \\ -0.0587 & \phantom{-}0.1517 & -0.0123 & -0.0262 \\ \phantom{-}0.0633 & \phantom{-}0.0525 & -0.1195 & \phantom{-}0.0606 \\ -0.0125 & -0.0592 & \phantom{-}0.0660 & -0.0157 \end{bmatrix}
$$

The matrix is not symmetric: $a_{01} = -0.1007$ but $a_{10} = -0.0587$. Position 0 (`The`) considers position 1 (`quick`) moderately irrelevant, while position 1 (`quick`) considers position 0 (`The`) less irrelevant. This asymmetry is a direct consequence of $W_Q \neq W_K$: the two matrices extract different linear combinations of the embedding components, so the dot product $\mathbf{q}_m^\top \mathbf{k}_n$ is not the same operation as $\mathbf{q}_n^\top \mathbf{k}_m$.

## Permutation Invariance in the Relevance Score Matrix

The similarity matrix $S = XX^\top$ from Chapter 1 exhibited permutation invariance: reversing the sequence produced $S' = PSP^\top$, a rearrangement of the same scores. The relevance score matrix $A$ inherits this invariance.

The step-by-step vector projections ($\mathbf{q}_t = W_Q \mathbf{x}_t$) treat each embedding as a $3 \times 1$ column vector. In the full $4 \times 3$ embedding tensor $X$, however, each token's embedding is a row ($\mathbf{x}_t^\top$).

To compute the entire set of queries simultaneously as a single matrix operation, the projection equation is transposed:

$$
\mathbf{q}_t^\top = (W_Q \mathbf{x}_t)^\top = \mathbf{x}_t^\top W_Q^\top
$$

Multiplying a row vector by $W_Q^\top$ projects it into a query row. Stacking all four positions into the full $4 \times 3$ matrix $Q$ reveals the complete operation:

$$
Q = \begin{bmatrix} \leftarrow & \mathbf{q}_0^\top & \rightarrow \\ \leftarrow & \mathbf{q}_1^\top & \rightarrow \\ \leftarrow & \mathbf{q}_2^\top & \rightarrow \\ \leftarrow & \mathbf{q}_3^\top & \rightarrow \end{bmatrix} = \begin{bmatrix} \leftarrow & \mathbf{x}_0^\top & \rightarrow \\ \leftarrow & \mathbf{x}_1^\top & \rightarrow \\ \leftarrow & \mathbf{x}_2^\top & \rightarrow \\ \leftarrow & \mathbf{x}_3^\top & \rightarrow \end{bmatrix} W_Q^\top = X W_Q^\top
$$

The same derivation applies to the key vectors, yielding the compact matrix definitions:

$$
Q = X W_Q^\top, \qquad K = X W_K^\top
$$

For the reversed sequence `fox` `brown` `quick` `The`, the embedding tensor is permuted: $X_{rev} = PX$. To see exactly why the linear projections cannot break this permutation, the row operations can be tracked visually.

First, consider projecting the permuted tensor ($X_{rev} W_Q^\top$). The permutation matrix $P$ moves the rows of $X$ into reverse order, and then the projection $W_Q^\top$ transforms each row:

$$
Q_{rev} = (PX) W_Q^\top = \begin{bmatrix} 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} \leftarrow & \mathbf{x}_0^\top & \rightarrow \\ \leftarrow & \mathbf{x}_1^\top & \rightarrow \\ \leftarrow & \mathbf{x}_2^\top & \rightarrow \\ \leftarrow & \mathbf{x}_3^\top & \rightarrow \end{bmatrix} W_Q^\top
$$

$$
= \begin{bmatrix} \leftarrow & \mathbf{x}_3^\top & \rightarrow \\ \leftarrow & \mathbf{x}_2^\top & \rightarrow \\ \leftarrow & \mathbf{x}_1^\top & \rightarrow \\ \leftarrow & \mathbf{x}_0^\top & \rightarrow \end{bmatrix} W_Q^\top = \begin{bmatrix} \leftarrow & \mathbf{q}_3^\top & \rightarrow \\ \leftarrow & \mathbf{q}_2^\top & \rightarrow \\ \leftarrow & \mathbf{q}_1^\top & \rightarrow \\ \leftarrow & \mathbf{q}_0^\top & \rightarrow \end{bmatrix}
$$

Now consider permuting the already-projected query matrix ($PQ$). Here, $X$ is projected into query vectors first, and then the permutation matrix $P$ shuffles those query vectors into reverse order:

$$
PQ = \begin{bmatrix} 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{bmatrix} \left( \begin{bmatrix} \leftarrow & \mathbf{x}_0^\top & \rightarrow \\ \leftarrow & \mathbf{x}_1^\top & \rightarrow \\ \leftarrow & \mathbf{x}_2^\top & \rightarrow \\ \leftarrow & \mathbf{x}_3^\top & \rightarrow \end{bmatrix} W_Q^\top \right)
$$

$$
= \begin{bmatrix} 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} \leftarrow & \mathbf{q}_0^\top & \rightarrow \\ \leftarrow & \mathbf{q}_1^\top & \rightarrow \\ \leftarrow & \mathbf{q}_2^\top & \rightarrow \\ \leftarrow & \mathbf{q}_3^\top & \rightarrow \end{bmatrix} = \begin{bmatrix} \leftarrow & \mathbf{q}_3^\top & \rightarrow \\ \leftarrow & \mathbf{q}_2^\top & \rightarrow \\ \leftarrow & \mathbf{q}_1^\top & \rightarrow \\ \leftarrow & \mathbf{q}_0^\top & \rightarrow \end{bmatrix}
$$

Both paths produce the exact same matrix. Multiplication on the left ($PX$) rearranges the row order without modifying the vectors themselves. Multiplication on the right ($X W_Q^\top$) projects each vector independently; the query vector for a given token is computed solely from its own embedding, completely unaffected by the other tokens in the sequence. Because the left-side permutation only alters positions and the right-side projection only alters internal values, the two operations never interfere. Projecting a shuffled sequence yields the exact same matrix as shuffling a projected sequence.

The same visual expansion holds for the key matrix ($K_{rev} = PK$).

This property is significant because it proves that the linear projections of the attention mechanism cannot break permutation invariance on their own. The relevance score matrix for the permuted sequence inherits the exact same invariance as the original dot-product similarity matrix $S = X X^\top$:

$$
A_{rev} = Q_{rev} \, K_{rev}^\top = (PQ)(PK)^\top = PQ K^\top P^\top = P A P^\top
$$

The same algebraic identity that governed $S' = PSP^\top$ in Chapter 1 governs the relevance score matrix. Computing $A_{rev}$ directly from the permuted embedding tensor:

$$
A_{rev} = \begin{bmatrix} -0.0157 & \phantom{-}0.0660 & -0.0592 & -0.0125 \\ \phantom{-}0.0606 & -0.1195 & \phantom{-}0.0525 & \phantom{-}0.0633 \\ -0.0262 & -0.0123 & \phantom{-}0.1517 & -0.0587 \\ -0.0200 & \phantom{-}0.0849 & -0.1007 & -0.0094 \end{bmatrix}
$$

Every score in $A$ appears in $A_{rev}$, relocated according to the permutation. The self-relevance of `quick` is $a_{11} = 0.1517$ in the original ordering and $(A_{rev})_{22} = 0.1517$ in the reversed ordering (because `quick` moved from position 1 to position 2). The score from `brown` querying `fox` is $a_{23} = 0.0606$ in the original and $(A_{rev})_{10} = 0.0606$ in the reversed ordering.

<div style="font-size: 0.9em;">

| Token Pair | Score in $A$ | Position in $A$ | Score in $A_{rev}$ | Position in $A_{rev}$ |
|---|---|---|---|---|
| `The` queries `quick` | $-0.1007$ | $A_{01}$ | $-0.1007$ | $(A_{rev})_{32}$ |
| `quick` queries `quick` | $\phantom{-}0.1517$ | $A_{11}$ | $\phantom{-}0.1517$ | $(A_{rev})_{22}$ |
| `quick` queries `brown` | $-0.0123$ | $A_{12}$ | $-0.0123$ | $(A_{rev})_{21}$ |
| `brown` queries `fox` | $\phantom{-}0.0606$ | $A_{23}$ | $\phantom{-}0.0606$ | $(A_{rev})_{10}$ |
| `fox` queries `brown` | $\phantom{-}0.0660$ | $A_{32}$ | $\phantom{-}0.0660$ | $(A_{rev})_{01}$ |

</div>

The permutation invariance problem from Chapter 1 manifests identically in the query-key relevance scores. The sequences `The` `quick` `brown` `fox` and `fox` `brown` `quick` `The` produce the same set of relevance scores, differing only in their assignment to matrix positions. No mechanism operating on these scores can distinguish the two orderings.

## The Relative Position Requirement

The fundamental problem is not merely that the relevance scores lack positional information. The problem is more specific: the ideal positional encoding should produce scores that depend on the *relative* offset between positions, not on their absolute indices.

The requirement can be stated formally. A positional encoding function $f$ transforms query and key vectors into position-aware variants:

$$
\tilde{\mathbf{q}}_m = f(\mathbf{q}_m, m), \qquad \tilde{\mathbf{k}}_n = f(\mathbf{k}_n, n)
$$

The encoded relevance score is:

$$
\tilde{a}_{mn} = \tilde{\mathbf{q}}_m^\top \tilde{\mathbf{k}}_n
$$

The **relative position requirement** is that $\tilde{a}_{mn}$ depends on the content vectors $\mathbf{q}_m, \mathbf{k}_n$ and the relative offset $\Delta = m - n$, but not on the absolute positions $m$ and $n$ individually. Formally, for any positions $m, n, m', n'$ with $m - n = m' - n'$:

$$
f(\mathbf{q}, m)^\top f(\mathbf{k}, n) = f(\mathbf{q}, m')^\top f(\mathbf{k}, n')
$$

for the same content vectors $\mathbf{q}$ and $\mathbf{k}$. The score between `quick` and `fox` separated by an offset of 2 should be the same whether they occupy positions $(1, 3)$ or positions $(5, 7)$ or positions $(100, 102)$, provided the content vectors are identical.

This requirement aligns with a linguistic observation: the relationship between two tokens typically depends on how far apart they are, not on where in the sequence they happen to appear. A verb that is three positions after its subject carries the same syntactic relationship regardless of whether the subject appears at position 0 or position 50.

## Why Additive Sinusoidal PE Fails the Relative Position Requirement

Chapter 3 demonstrated that additive sinusoidal PE successfully breaks permutation invariance. The question is whether it satisfies the relative position requirement in the query-key dot product.

With additive PE, the positionally-enriched embedding is $\mathbf{x}_t^{pos} = \mathbf{x}_t + \mathbf{p}_t$, where $\mathbf{p}_t$ is the sinusoidal encoding at position $t$. The query and key vectors become:

$$
\mathbf{q}_m^{pos} = W_Q (\mathbf{x}_m + \mathbf{p}_m) = W_Q \mathbf{x}_m + W_Q \mathbf{p}_m = \mathbf{q}_m + W_Q \mathbf{p}_m
$$

$$
\mathbf{k}_n^{pos} = W_K (\mathbf{x}_n + \mathbf{p}_n) = W_K \mathbf{x}_n + W_K \mathbf{p}_n = \mathbf{k}_n + W_K \mathbf{p}_n
$$

The linearity of the projection produces a clean decomposition: each positionally-encoded query (or key) is the sum of a content component and a position component. The relevance score expands as a four-term product:

$$
(\mathbf{q}_m^{pos})^\top \mathbf{k}_n^{pos} = (\mathbf{q}_m + W_Q \mathbf{p}_m)^\top (\mathbf{k}_n + W_K \mathbf{p}_n)
$$

$$
= \underbrace{\mathbf{q}_m^\top \mathbf{k}_n}_{\text{content-content}} + \underbrace{\mathbf{q}_m^\top W_K \mathbf{p}_n}_{\text{content-position}} + \underbrace{(W_Q \mathbf{p}_m)^\top \mathbf{k}_n}_{\text{position-content}} + \underbrace{(W_Q \mathbf{p}_m)^\top W_K \mathbf{p}_n}_{\text{position-position}}
$$

The first term is the original content-only relevance score (invariant to position). The fourth term depends only on the positions $m$ and $n$ (invariant to content). But the second and third terms are cross-terms that entangle content and absolute position: $\mathbf{q}_m^\top W_K \mathbf{p}_n$ depends on the content at position $m$ and the absolute position $n$, not the relative offset $m - n$.

To verify concretely, the four-term decomposition for the pair (`The`, `quick`) at positions $(m = 0, n = 1)$:

$$
\text{content-content: } \mathbf{q}_0^\top \mathbf{k}_1 = -0.1007
$$

$$
\text{content-position: } \mathbf{q}_0^\top W_K \mathbf{p}_1 = -0.0689
$$

$$
\text{position-content: } (W_Q \mathbf{p}_0)^\top \mathbf{k}_1 = 0.1320
$$

$$
\text{position-position: } (W_Q \mathbf{p}_0)^\top W_K \mathbf{p}_1 = 0.1496
$$

$$
\text{sum} = -0.1007 + (-0.0689) + 0.1320 + 0.1496 = \mathbf{0.1120}
$$

The cross-terms ($-0.0689$ and $0.1320$) depend on the specific absolute positions 0 and 1, not on the offset $\Delta = 0 - 1 = -1$. If the same tokens appeared at positions $(5, 6)$ (same offset $\Delta = -1$, same content), the cross-terms would differ because $\mathbf{p}_5 \neq \mathbf{p}_0$ and $\mathbf{p}_6 \neq \mathbf{p}_1$.

The sinusoidal formula does encode a rotational relationship between positions: Chapter 2 demonstrated that the positional encoding satisfies relative representability (the relationship between any two positions can be expressed as a fixed rotation). But the additive injection mechanism does not preserve this relationship through the projection. After multiplication by $W_Q$ and $W_K$, the rotational structure of the positional encodings is obscured by the projection weights, and the clean relative-distance property is lost.

## Preview: Rotation as Position Encoding

The relative position requirement demands that the relevance score $\tilde{\mathbf{q}}_m^\top \tilde{\mathbf{k}}_n$ depend only on content and relative offset. The failure of additive PE stems from a structural mismatch: the positional signal is injected *before* the projection, and the projection entangles it with content in a way that breaks the relative-distance property.

The solution is to encode position *after* the projection, directly on the query and key vectors themselves. Rotary Position Embeddings (RoPE) apply a position-dependent rotation to each query and key vector:

$$
\tilde{\mathbf{q}}_m = R_m \, \mathbf{q}_m, \qquad \tilde{\mathbf{k}}_n = R_n \, \mathbf{k}_n
$$

where $R_t$ is a rotation matrix that depends on position $t$. The dot product of rotated vectors satisfies:

$$
\tilde{\mathbf{q}}_m^\top \tilde{\mathbf{k}}_n = (R_m \mathbf{q}_m)^\top (R_n \mathbf{k}_n) = \mathbf{q}_m^\top R_m^\top R_n \, \mathbf{k}_n = \mathbf{q}_m^\top R_{n-m} \, \mathbf{k}_n
$$

The product $R_m^\top R_n$ collapses to a single rotation $R_{n-m}$ that depends only on the offset $\Delta = n - m$, because rotation matrices compose by adding angles. The resulting score depends on the content vectors and the relative offset, satisfying the requirement by algebraic construction rather than by learned approximation.

Nothing is added to the embedding vectors. No information is superimposed in the same dimensions. The positional signal is encoded in the geometric orientation of the query and key vectors, not in their coordinates. The next chapter derives the rotation matrix, computes it for every position in the toy model, and applies it to the query and key vectors computed in this chapter.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
