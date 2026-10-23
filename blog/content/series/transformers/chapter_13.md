# Part 13: The MLP Activation and Layer 2 Self-Attention

<!-- SUMMARY: The activation function serves as the non-linear gatekeeper within the feed-forward network, filtering the conceptual matches identified by the first linear projection. The subsequent value projection translates these activated patterns into concrete feature updates for the residual stream. Progressing into the second layer of self-attention transforms token vectors from isolated definitions into contextualized representations that evaluate multi-token syntactic structures. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

The projection matrix from Part 10 expanded the normalized residual stream into a twenty-four-dimensional space, querying a learned bank of conceptual keys. The resulting biased projection matrix contained a spectrum of positive and negative values representing the alignment strength with each learned pattern. The network must now determine which of these candidate patterns apply to the current sequence context and discard the rest. This non-linear filtering operation is executed by the activation function.

## Non-Linear Filtering and Value Contraction

The toy model employs the Rectified Linear Unit (ReLU), defined as $\text{ReLU}(z) = \max(0, z)$. Every negative entry is clamped to zero, whereas positive entries pass through unchanged. Mechanistically, ReLU enforces a hard firing threshold. A token vector that fails to align with a specific conceptual key produces a negative dot product, which the ReLU threshold clamps to zero. That neuron remains inactive.

Applying this element-wise non-linearity to the biased projection state produces the sparse activated memory representation:

$$
\text{Activated State} = \begin{bmatrix}
 0.58 &  0.00 &  0.00 &  0.00 &  0.56 &  0.00 &  1.03 &  0.71 &  0.00 & \dots &  0.00 \\
 1.01 &  0.00 &  0.00 &  0.00 &  1.50 &  0.00 &  2.30 &  0.00 &  0.00 & \dots &  1.88 \\
 0.00 &  0.00 &  0.00 &  0.29 &  0.00 &  2.81 &  0.00 &  1.72 &  3.20 & \dots &  1.24 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.03 &  2.34 &  0.00 &  0.74 &  2.29 & \dots &  1.68
\end{bmatrix}
$$

The hidden activation landscape is now sparse: only positive conceptual matches survive. Zeroed entries correspond to features irrelevant to a token in its current context, preventing contradictory signals from propagating into the value projection.

With the active keys selected, the network enters the extraction phase. The second half of the Multi-Layer Perceptron (MLP) is parameterized by the $24 \times 6$ weight matrix $W_2$, which projects the twenty-four-dimensional hidden space back down to the model dimension $d_{\text{model}} = 6$. In the Key-Value memory analogy, the columns of $W_1$ act as the Keys that detect patterns, and the rows of $W_2$ store the corresponding Values written back into the residual stream:

$$
W_2 = \begin{bmatrix}
 0.75 &  0.19 &  0.34 &  0.44 & -0.42 & -0.78 \\
 -0.56 &  0.17 &  0.53 &  0.06 & -0.68 &  0.70 \\
 -0.80 & -0.24 & -0.28 &  0.13 &  0.55 & -0.75 \\
 -0.16 &  0.16 & -0.58 & -0.05 &  0.09 & -0.67 \\
 -0.65 & -0.03 & -0.11 &  0.11 &  1.11 &  0.45 \\
  0.22 & -0.36 &  0.47 & -0.39 &  0.78 &  0.59 \\
 -1.00 & -0.59 & -0.10 & -0.20 & -0.63 & -0.61 \\
  0.36 & -0.27 & -0.76 & -0.14 &  0.48 &  0.84 \\
  0.03 & -0.16 & -0.40 & -0.26 &  0.27 &  0.63 \\
  0.62 & -0.12 &  0.44 &  0.38 &  0.23 & -1.23 \\
 -0.03 & -0.14 &  0.66 & -0.14 &  0.23 &  0.13 \\
  0.63 &  0.38 &  0.51 &  0.75 &  0.48 &  0.39 \\
 -0.13 &  0.05 &  1.08 &  0.02 &  0.25 & -0.04 \\
 -0.15 & -1.50 &  0.86 & -0.59 & -0.42 &  0.68 \\
 -1.18 &  0.01 & -0.28 & -0.92 &  0.31 & -0.39 \\
 -0.05 & -0.21 &  0.32 &  1.13 & -0.63 &  0.43 \\
 -0.35 & -0.18 & -0.95 & -0.57 & -0.22 &  0.41 \\
  0.12 &  0.29 &  0.37 & -0.69 &  0.73 & -0.16 \\
  0.34 & -0.09 &  0.13 &  0.32 & -1.13 &  1.01 \\
  0.09 &  0.55 &  0.11 &  0.04 & -0.66 & -0.20 \\
 -1.11 & -0.08 &  0.79 & -0.94 & -0.34 & -0.19 \\
  0.58 &  0.62 &  0.03 &  0.05 & -0.08 & -0.24 \\
 -0.24 & -0.23 & -0.08 &  0.04 & -0.32 &  0.31 \\
 -0.02 &  0.27 & -0.68 & -0.35 &  0.05 &  0.14
\end{bmatrix}
$$

Each active neuron in the hidden layer retrieves its corresponding row from the full 24-row Value matrix $W_2$ introduced in Part 11. Multiplying the activated state by $W_2$ and adding the bias vector $b_2$ (`[-0.06, 0.12, -0.15, -0.08, 0.04, 0.09]`) computes a weighted sum of Value rows, producing the consolidated $4 \times 6$ update matrix for the residual stream:

$$
\text{Contracted Output} = \begin{bmatrix}
 -4.07 &  0.04 & -0.06 & -1.74 & -1.17 & -0.77 \\
 -6.51 &  0.18 & -0.33 & -3.85 & -0.84 & -1.43 \\
  0.82 & -3.22 &  0.39 & -2.11 &  3.22 &  6.02 \\
  1.18 & -2.83 & -0.72 & -1.89 &  1.58 &  4.39
\end{bmatrix}
$$

### Gated Feed-Forward Networks: SwiGLU

Foundational Transformer architectures apply a single ReLU threshold, whereas contemporary large language models frequently substitute gated activation units such as SwiGLU (Swish-Gated Linear Unit). SwiGLU replaces the single expansion matrix $W_1$ with two parallel linear projections:

- **Feature Projection ($x W_{\text{up}}$):** Maps the normalized token vector into the expanded intermediate space to propose candidate conceptual features.
- **Gate Projection ($\text{Swish}(x W_{\text{gate}})$):** Maps the same input through an independent weight matrix and applies the smooth non-linear $\text{Swish}(z) = z \cdot \sigma(z)$ activation to compute a continuous gating scalar for each hidden dimension.

Element-wise multiplication combines the two branches before the final $W_2$ contraction projects the gated state back to $d_{\text{model}}$:

$$
\text{SwiGLU}(x) = \left(\text{Swish}(x W_{\text{gate}}) \odot (x W_{\text{up}})\right) W_2
$$

Rather than enforcing a binary zero floor like ReLU, SwiGLU acts as a continuous, context-dependent dial. The feature branch proposes a semantic candidate, and the gate branch independently scales or suppresses that candidate based on token interactions. Decoupling feature generation from feature gating increases the expressive capacity of the feed-forward memory bank.

Whether an architecture uses a ReLU threshold or a SwiGLU gate, the structural role of the MLP remains identical: the block evaluates context-enriched token vectors, retrieves learned conceptual features, and writes those updates into the residual stream.

## Transition to Layer 2

In the first layer of the Transformer, the self-attention mechanism evaluated relationships between positionally encoded word embeddings. Projecting the tokens `woke` and `up` into their Layer 1 Query and Key spaces measured their initial lexical affinity. The network then routed those localized updates into the residual stream, refined them through the Key-Value Multi-Layer Perceptron, and standardized their geometry with Layer Normalization. Entering the second layer of self-attention, the token vectors no longer represent isolated dictionary definitions; each row now encodes a contextualized summary of its surrounding linguistic environment.

## The Contextualized Input

The input to Layer 2, denoted as $X_2$, is the normalized output of the first layer derived in Part 12. The vectors occupying this matrix differ substantially from the initial token embeddings. The first row corresponds to `<BOS>`, the second to `i`, the third to `woke`, and the fourth to `up`, and their coordinates now encode the structural and semantic relationships assembled during Layer 1:

$$
X_2 = \begin{bmatrix}
-2.00 & 1.22 & 0.50 & 0.19 & -0.28 & 0.37 \\
-1.91 & 1.28 & 0.52 & -0.49 & 0.21 & 0.39 \\
0.04 & -1.55 & 0.18 & -0.82 & 0.52 & 1.62 \\
0.20 & -1.72 & 0.01 & -0.55 & 0.49 & 1.57
\end{bmatrix}
$$

Layer 2 self-attention does not merely test whether `woke` relates to `up` in isolation. The mechanism evaluates how a verb phrase already linked to the subject `i` aligns with the particle `up` to form a compound phrasal concept. Self-attention in deeper layers operates on multi-token abstractions.

## The Second Layer Projections

Just as in Layer 1, the network projects these 6-element residual vectors into 2-element head subspaces ($d_k = 2$) to compute attention. A dedicated set of weight matrices initializes the first head of Layer 2. These matrices, $W_Q^{(2)}$, $W_K^{(2)}$, and $W_V^{(2)}$, serve the same geometric role as their Layer 1 counterparts, defining a bilinear form that aligns contextualized semantic vectors in a shared subspace:

$$
W_Q^{(2)} = \begin{bmatrix}
 0.10 & -0.20 \\
-0.30 &  0.40 \\
 0.50 & -0.10 \\
-0.20 &  0.30 \\
 0.40 &  0.20 \\
-0.10 & -0.50
\end{bmatrix}
$$

$$
W_K^{(2)} = \begin{bmatrix}
-0.20 &  0.30 \\
 0.40 & -0.10 \\
-0.30 &  0.50 \\
 0.10 & -0.40 \\
 0.20 &  0.20 \\
-0.50 &  0.10
\end{bmatrix}
$$

$$
W_V^{(2)} = \begin{bmatrix}
 0.30 & -0.10 \\
-0.20 &  0.40 \\
 0.10 & -0.30 \\
-0.40 &  0.20 \\
 0.50 & -0.20 \\
-0.10 &  0.50
\end{bmatrix}
$$

Multiplying the full-precision normalized Layer 1 output $X_2$ by each weight matrix and rounding to two decimal places produces the Layer 2 Queries $Q_2$, Keys $K_2$, and Values $V_2$.

### The Query Space

The $Q_2$ matrix represents the contextual patterns each token searches for across the sequence:

$$
Q_2 = X_2 W_Q^{(2)} = \begin{bmatrix}
-0.50 &  0.66 \\
-0.17 &  0.54 \\
 0.77 & -1.60 \\
 0.69 & -1.58
\end{bmatrix}
$$

### The Key Space

The $K_2$ matrix represents the compound features each contextualized token advertises to the sequence:

$$
K_2 = X_2 W_K^{(2)} = \begin{bmatrix}
 0.52 & -0.57 \\
 0.53 & -0.16 \\
-1.47 &  0.85 \\
-1.47 &  0.71
\end{bmatrix}
$$

### The Value Space

The $V_2$ matrix stores the contextualized payload each token contributes to downstream positions that attend to it:

$$
V_2 = X_2 W_V^{(2)} = \begin{bmatrix}
-1.05 &  0.82 \\
-0.51 &  0.60 \\
 0.77 & -0.13 \\
 0.71 & -0.13
\end{bmatrix}
$$

## A Shift in Abstraction

The linear algebra remains identical to Layer 1: an input tensor projects through three $6 \times 2$ transformations to prepare for scaled dot-product attention. The shift lies entirely in the information carried by $X_2$. Queries and Keys in Layer 2 no longer match isolated lexical traits; they match multi-token syntactic structures and composite semantic roles. Part 14 verifies the Layer 1 to Layer 2 residual boundary and computes the scaled attention scores from $Q_2$ and $K_2$.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
