# Part 10: The Residual Stream and MLP Expansion

<!-- SUMMARY: The expansion phase of the feed-forward network acts as a high-dimensional key-value memory retrieval mechanism. By projecting token vectors into a substantially larger geometric space, the model computes dot products against learned key patterns to measure alignment with higher-order conceptual features. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

The calculations outlined in Parts 8 and 9 update the residual stream and stabilize the geometry of the network through layer normalization. These operations preserve forward information flow while neutralizing gradient degradation, leaving the token vectors positioned for the next architectural phase.

## The MLP as a Key-Value Memory Bank

The model has standardized the residual stream into centered, unit-variance token vectors. Up to this stage, self-attention has routed contextual information between sequence positions: the representation for `up` has pulled in contextual features from `woke`. Self-attention routes information across tokens, yet linear attention mixing alone cannot non-linearly transform those combined features into higher-order semantic concepts.

Processing each contextualized token vector individually requires the second major sub-layer of the Transformer block: the Feed-Forward Network, also called the Multi-Layer Perceptron (MLP).

Introductory treatments often describe the MLP merely as a two-layer feed-forward network that expands dimensionality and applies a non-linear activation. Mechanistic interpretability provides a concrete geometric framing: the MLP functions as a learned Key-Value memory bank stored within its weight matrices. This section examines the first linear projection of the MLP, which serves as the Key lookup stage of that memory retrieval system.

## The Geometry of the Keys

The model dimension is $d_{model} = 6$. Standard Transformer architectures expand the hidden layer of the MLP by a factor of four relative to the residual stream, setting the feed-forward dimension to $d_{ff} = 4 \times d_{model} = 24$.

The first projection matrix, $W_1$, has a shape of $6 \times 24$. The calculation multiplies the normalized residual stream $X_{norm}$ ($4 \times 6$) by $W_1$, resulting in a projected matrix of shape $4 \times 24$.

Rather than viewing $W_1$ as a monolithic block, examining its column structure clarifies its geometric role. The matrix $W_1$ consists of 24 distinct column vectors in $\mathbb{R}^6$, where each column represents a learned Key pattern.

Each Key column represents a learned spatial pattern in $\mathbb{R}^6$. Computing the dot product between a normalized token vector and a Key column measures their directional alignment, testing whether the contextualized token exhibits the specific feature combination encoded by that Key.

Defining the first column of the learned $W_1$ matrix as the key vector $k_1$ illustrates this lookup mechanism:

$$
k_1 = \begin{bmatrix}
 0.33 \\
-0.51 \\
-1.89 \\
 0.67 \\
 0.86 \\
 1.55
\end{bmatrix}
$$

The system extracts the normalized vector for the third token, `woke`, from Row 3 of the $X_{norm}$ matrix calculated in Part 9:

$$
x_{woke} = \begin{bmatrix}
 0.23 & -1.54 & 1.57 & 0.40 & -0.94 & 0.28
\end{bmatrix}
$$

Computing the dot product between $x_{woke}$ and $k_1$ quantifies how strongly the contextualized `woke` token aligns with the first Key pattern:

$$
x_{woke} \cdot k_1 = (0.23 \times 0.33) + (-1.54 \times -0.51) + (1.57 \times -1.89) + (0.40 \times 0.67) + (-0.94 \times 0.86) + (0.28 \times 1.55)
$$

$$
x_{woke} \cdot k_1 = 0.08 + 0.79 - 2.97 + 0.27 - 0.81 + 0.43 = -2.21
$$

A negative dot product indicates that the vector for `woke` points away from $k_1$ in six-dimensional space, meaning this token does not match the feature pattern represented by the first Key.

Performing this matrix multiplication across all four rows simultaneously checks every token against all 24 Keys.

## The Projection Calculation

The complete matrix multiplication $X_{norm} W_1 = X_{proj}$ follows:

$$
X_{proj} = \begin{bmatrix}
 0.64 & -0.30 & -0.93 & -0.86 &  0.53 & -1.24 &  0.88 &  0.71 & -2.13 & \dots & -0.19 \\
 1.07 & -1.32 & -0.65 & -0.96 &  1.47 & -2.19 &  2.16 & -0.20 & -2.64 & \dots &  1.73 \\
-2.21 & -0.10 & -2.12 &  0.33 & -2.18 &  2.73 & -0.92 &  1.72 &  3.32 & \dots &  1.09 \\
-0.62 & -0.74 & -0.58 & -0.56 &  0.00 &  2.26 & -0.71 &  0.74 &  2.40 & \dots &  1.53
\end{bmatrix}
$$

Each row in $X_{proj}$ corresponds to one of the four sequence tokens, and each column corresponds to one of the 24 Keys. The entry at Row 3, Column 1 equals $-2.21$, matching the manual dot product computed between `woke` and $k_1$.

Row 3, Column 9 exhibits a strong positive score of $3.32$, indicating that the contextualized representation for `woke` aligns closely with the ninth Key vector.

## The Bias Vector

In a standard linear layer, a learned bias vector $b_1$ is added immediately after the matrix multiplication. The bias vector shifts the pre-activation scores, acting as a baseline activation threshold for each of the 24 Keys:

$$
X_{proj\_biased} = X_{proj} + b_1
$$

A negative bias raises the activation threshold for a Key, requiring a large positive dot product to overcome the offset, whereas a positive bias lowers the threshold so the Key fires more readily.

Adding the learned bias vector $b_1$ across every row of $X_{proj}$ produces the pre-activation state $X_{proj\_biased}$:

$$
b_1 = \begin{bmatrix} -0.06 & 0.04 & -0.16 & -0.04 & 0.03 & 0.08 & 0.14 & 0.00 & -0.12 & \dots & 0.15 \end{bmatrix}
$$

$$
X_{proj\_biased} = \begin{bmatrix}
 0.58 & -0.26 & -1.09 & -0.90 &  0.56 & -1.16 &  1.03 &  0.71 & -2.25 & \dots & -0.04 \\
 1.01 & -1.28 & -0.81 & -1.00 &  1.50 & -2.11 &  2.30 & -0.21 & -2.75 & \dots &  1.88 \\
-2.27 & -0.07 & -2.28 &  0.29 & -2.16 &  2.81 & -0.78 &  1.72 &  3.20 & \dots &  1.24 \\
-0.69 & -0.71 & -0.74 & -0.60 &  0.03 &  2.34 & -0.56 &  0.74 &  2.29 & \dots &  1.68
\end{bmatrix}
$$

The token vectors have now queried all 24 Key patterns in the memory bank. The next stage applies a non-linear activation gate to zero out negative non-matches before projecting the surviving activations back into the residual stream.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
