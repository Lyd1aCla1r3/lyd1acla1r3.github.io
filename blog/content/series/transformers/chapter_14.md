# Part 14: Final Layer 1 Residuals, Norms, and Layer 2 Attention

<!-- SUMMARY: The multi-layer perceptron output is added back into the residual stream, preserving the prior contextual state while integrating the newly activated conceptual features. A final layer normalization step stabilizes the vector geometry, preparing the enriched representations for the second layer. The query and key vectors then undergo a mathematical shift as compound semantic structures are scored using the scaled dot-product. Stabilizing the variance of these unscaled scores prevents softmax saturation and preserves gradient flow during backpropagation. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

## Auditing the Layer 1 to Layer 2 Boundary

Completing the Multi-Layer Perceptron contraction in Part 13 concluded the feature extraction phase of Layer 1. Before scoring the Layer 2 Query and Key projections derived at the end of Part 13, this section audits the residual addition and Layer Normalization boundary that produced the Layer 2 input matrix $X_2$.

Integrating the extracted MLP features with the post-attention representation occurs through the second residual connection of Layer 1. Rather than overwriting the intermediate state, the network adds the contracted MLP output directly to the normalized vectors that entered the feed-forward block. This additive skip connection preserves the contextual identity of each token alongside its newly retrieved conceptual features and maintains a direct gradient highway during backpropagation.

Prior to the feed-forward network, the post-attention residual stream held the following $4 \times 6$ matrix (from Part 8):

$$
\text{Original Residual Stream} = \begin{bmatrix}
 0.02 &  1.29 &  0.18 &  1.35 &  0.00 &  0.67 \\
 0.74 &  1.76 &  0.45 &  1.52 &  0.20 &  1.23 \\
 0.88 & -0.31 &  1.78 &  0.99 &  0.09 &  0.91 \\
 0.19 & -1.03 &  1.56 &  1.21 &  0.58 &  0.69
\end{bmatrix}
$$

The network adds the contracted $4 \times 6$ output from the Multi-Layer Perceptron directly to this stream:

$$
\text{MLP Output} = \begin{bmatrix}
-4.07 &  0.04 & -0.06 & -1.74 & -1.17 & -0.77 \\
-6.51 &  0.18 & -0.33 & -3.85 & -0.84 & -1.43 \\
 0.82 & -3.22 &  0.39 & -2.11 &  3.22 &  6.02 \\
 1.18 & -2.83 & -0.72 & -1.89 &  1.58 &  4.39
\end{bmatrix}
$$

Summing the two matrices element by element produces an enriched composite representation that merges localized conceptual features with the contextual routing established by Layer 1 self-attention:

$$
\text{New Residual Stream} = \begin{bmatrix}
-4.05 &  1.33 &  0.12 & -0.39 & -1.17 & -0.10 \\
-5.77 &  1.94 &  0.12 & -2.33 & -0.64 & -0.20 \\
 1.70 & -3.53 &  2.17 & -1.12 &  3.31 &  6.93 \\
 1.37 & -3.86 &  0.84 & -0.68 &  2.16 &  5.08
\end{bmatrix}
$$

Before these vectors advance into Layer 2, their coordinate distributions must be standardized. Element-wise residual addition shifts the row means and expands the variance of the token representations; left unchecked across stacked layers, this numerical drift destabilizes both forward activations and backward gradients.

Applying Layer Normalization corrects this drift by recalculating the mean and variance independently across the six features of each row and rescaling every row to zero mean and unit variance. The normalization constrains vector magnitudes while preserving the directional geometry encoded in the relative coordinate ratios:

$$
\text{Normalized Layer 2 Input } (X_2) = \begin{bmatrix}
-2.00 &  1.22 &  0.50 &  0.19 & -0.28 &  0.37 \\
-1.91 &  1.28 &  0.52 & -0.49 &  0.21 &  0.39 \\
 0.04 & -1.55 &  0.18 & -0.82 &  0.52 &  1.62 \\
 0.20 & -1.72 &  0.01 & -0.55 &  0.49 &  1.57
\end{bmatrix}
$$

This standardized $4 \times 6$ matrix $X_2$ completes Layer 1 of the Transformer architecture. Each row now integrates lexical identity, sinusoidal position, multi-head contextual routing, and feed-forward memory retrieval.

Passing $X_2$ into Layer 2 repeats the self-attention and feed-forward sub-layers at a higher level of abstraction. Rather than scoring isolated vocabulary embeddings, Layer 2 scores relationships between composite phrase representations. The remainder of this chapter traces how the Layer 2 Query and Key projections are aligned and scaled.

## The Semantic Shift in Queries and Keys

Layer 1 attention derived its Queries $Q$ and Keys $K$ from static token embeddings combined with positional encodings, probing basic pairwise relationships such as matching a subject with a verb. Entering Layer 2, the input vectors have already passed through the first attention block and the Multi-Layer Perceptron, absorbing surrounding sequence context.

Processing the prompt `<BOS>` `i` `woke` `up` to predict the next token now operates on mixed representations: the vectors for `woke` and `up` already share features in the residual stream. Projecting these composite representations into $Q_2$ and $K_2$ tests compound syntactic relationships across the phrase.

The $Q_2$ matrix and the transposed Key matrix $K_2^T$ for the first attention head in Layer 2 (derived in Part 13) take the following values:

$$
Q_2 = \begin{bmatrix}
-0.50 & 0.66 \\
-0.17 & 0.54 \\
0.77 & -1.60 \\
0.69 & -1.58
\end{bmatrix}
$$

$$
K_2^T = \begin{bmatrix}
0.52 & 0.53 & -1.47 & -1.47 \\
-0.57 & -0.16 & 0.85 & 0.71
\end{bmatrix}
$$

## Calculating the Unscaled Alignment

The mechanism for measuring pairwise relevance remains the inner product. Multiplying $Q_2$ ($4 \times 2$) by $K_2^T$ ($2 \times 4$) computes the raw alignment score between every contextualized query and every contextualized key. Vectors pointing in similar directions within the 2-dimensional head subspace produce positive dot products, opposing vectors produce negative dot products, and orthogonal vectors evaluate to zero.

Evaluating the matrix multiplication $Q_2 \cdot K_2^T$ generates the $4 \times 4$ unscaled attention score matrix:

$$
\text{Scores}_{\text{unscaled}} = \begin{bmatrix}
-0.64 & -0.38 & 1.30 & 1.21 \\
-0.40 & -0.18 & 0.71 & 0.63 \\
1.31 & 0.67 & -2.48 & -2.27 \\
1.26 & 0.62 & -2.35 & -2.14
\end{bmatrix}
$$

The lower half of this matrix exhibits distinct structural contrast. The rows corresponding to `woke` (Row 3) and `up` (Row 4) assign positive alignment scores (`1.31, 0.67` and `1.26, 0.62`) to the initial anchor positions `<BOS>` and `i` while assigning negative scores (`-2.48, -2.27` and `-2.35, -2.14`) to the verb-particle cluster itself.

## Stabilizing the Variance

Before normalizing these scores into probabilities, the scaling factor must be applied. Part 4 established that the variance of a dot product grows proportionally with the dimensionality $d_k$ of the projected vectors. Unchecked variance produces large-magnitude dot products in the unscaled score matrix. Passing extreme positive or negative values into the Softmax function drives the output distribution toward a one-hot step function, operating in flat asymptotic regions where the Softmax gradient approaches zero. This Softmax saturation stalls weight updates during backpropagation.

Dividing the unscaled scores by the square root of the head dimension ($\sqrt{d_k} = \sqrt{2} \approx 1.4142$) restores unit variance:

$$
\text{Scores}_{\text{scaled}} = \begin{bmatrix}
-0.45 & -0.27 & 0.92 & 0.86 \\
-0.28 & -0.13 & 0.50 & 0.45 \\
0.93 & 0.47 & -1.76 & -1.60 \\
0.89 & 0.44 & -1.66 & -1.51
\end{bmatrix}
$$

Scaling by $\sqrt{d_k}$ preserves the relative alignment rankings while compressing the absolute magnitudes. This variance stabilization keeps the subsequent Softmax distribution in a smooth regime with non-zero gradients, routing information proportionally across multiple tokens rather than collapsing onto a single position.

With the scaled Layer 2 alignment scores established, Part 15 applies the lower-triangular causal mask, normalizes the masked scores via Softmax, and multiplies by $V_2$ to extract the Head 1 output.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
