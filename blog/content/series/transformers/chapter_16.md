# Part 16: Deepening the Representation: MLP and Residuals in Layer 2

<!-- SUMMARY: The second layer attention updates are integrated into the residual stream and geometrically stabilized using layer normalization. The normalized vectors then flow into a multi-layer perceptron acting as a deep contextual memory bank, enabling the injection of learned knowledge into the sequence representation. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

Computing the attention probabilities and multiplying by the Value matrix in Part 15 completed the single-head retrieval stage of Layer 2. In a full three-head pass, concatenating the three $4 \times 2$ head outputs and multiplying by the Layer 2 output projection matrix $W_O^{(2)}$ ($6 \times 6$) maps the combined updates back into the $d_{\text{model}} = 6$ coordinate space.

To keep the downstream unembedding, Softmax, cross-entropy loss, and backpropagation arithmetic verifiable by hand without repeating the three-head concatenation from Parts 6 and 7, this walkthrough adopts canonicalized $4 \times 6$ tensors for the Layer 2 residual merge. Rows 1 and 2 (`<BOS>` and `i`) follow opposite-sign linear ramps across the six embedding dimensions, whereas Rows 3 and 4 (`woke` and `up`) form zero-sum step vectors whose entries cancel across the first and second halves of the embedding dimension:

$$
\text{Layer 2 Attention Output} = \begin{bmatrix}
  0.03 & -0.06 &  0.09 & -0.12 &  0.15 & -0.18 \\
 -0.03 &  0.06 & -0.09 &  0.12 & -0.15 &  0.18 \\
  0.15 &  0.15 &  0.15 & -0.15 & -0.15 & -0.15 \\
 -0.15 & -0.15 & -0.15 &  0.15 &  0.15 &  0.15
\end{bmatrix}
$$

## The First Residual Connection

The residual stream acts as the central information highway of the Transformer architecture, bypassing the attention block so that self-attention computes an additive update rather than overwriting the prior state. In this canonicalized Layer 2 trace, the foundational stream state entering the merge is:

$$
\text{Layer 1 Final Output} = \begin{bmatrix}
  0.10 & -0.20 &  0.30 & -0.40 &  0.50 & -0.60 \\
 -0.10 &  0.20 & -0.30 &  0.40 & -0.50 &  0.60 \\
  0.50 &  0.50 &  0.50 & -0.50 & -0.50 & -0.50 \\
 -0.50 & -0.50 & -0.50 &  0.50 &  0.50 &  0.50
\end{bmatrix}
$$

The network adds the Layer 2 attention output directly to this incoming stream element by element. This addition writes the newly routed structural relationships into the shared memory bus without erasing the syntactic features established earlier in the network:

$$
\text{Residual}_1 = \text{Stream}_{\text{in}} + \text{Attention}_{\text{out}}
$$

Within the prompt `<BOS>` `i` `woke` `up`, the representation for `woke` merges with `up` to encode the unified phrasal concept of waking up rather than two unrelated lexical items. Adding `Layer 2 Attention Output` to `Layer 1 Final Output` element by element yields the first Layer 2 residual state:

$$
\text{After First Residual } (\text{Residual}_1) = \begin{bmatrix}
  0.13 & -0.26 &  0.39 & -0.52 &  0.65 & -0.78 \\
 -0.13 &  0.26 & -0.39 &  0.52 & -0.65 &  0.78 \\
  0.65 &  0.65 &  0.65 & -0.65 & -0.65 & -0.65 \\
 -0.65 & -0.65 & -0.65 &  0.65 &  0.65 &  0.65
\end{bmatrix}
$$

## Layer Normalization

Following the first residual addition, the vectors undergo Layer Normalization to standardize their coordinate scale, recentering each row to a mean of zero and a variance of one:

$$
\text{Norm}_1 = \text{LayerNorm}(\text{Residual}_1)
$$

This normalization ensures that the subsequent Multi-Layer Perceptron block receives standardized inputs, preventing any single dimension from dominating the feed-forward activations.

## The Multilayer Perceptron: A Deep Contextual Memory

The normalized vectors next enter the Layer 2 Multi-Layer Perceptron (MLP). Self-attention routes information horizontally across sequence positions, whereas the MLP transforms features vertically within each individual token vector. This second feed-forward block operates as a Key-Value memory bank over phrase-level abstractions rather than isolated word embeddings. The network projects the normalized vectors through an expansion layer, applies the Rectified Linear Unit (ReLU) activation function, and contracts the active features back to $d_{\text{model}} = 6$.

### The Key Expansion

The first linear transformation, parameterized by $W_1^{(2)}$ ($6 \times 24$) and bias $b_1^{(2)}$, expands the 6-dimensional vectors into the 24-dimensional intermediate space to test whether specific multi-token patterns are present:

$$
\text{Hidden} = \text{ReLU}(\text{Norm}_1 W_1^{(2)} + b_1^{(2)})
$$

The Rectified Linear Unit (ReLU) activation serves as a non-linear firing threshold. Positive alignment scores, such as a token vector matching the combined `woke` + `up` phrasal pattern, pass through the gate unchanged, whereas negative scores are clamped to zero.

### The Value Contraction

Active neurons in the hidden layer trigger the second linear transformation, parameterized by $W_2^{(2)}$ ($24 \times 6$) and bias $b_2^{(2)}$, which projects the 24-dimensional state back down to $d_{\text{model}} = 6$:

$$
\text{MLP}_{\text{out}} = \text{Hidden} W_2^{(2)} + b_2^{(2)}
$$

Active neurons scale their corresponding rows in $W_2^{(2)}$, writing learned semantic updates back into the 6-dimensional subspace. This memory retrieval step injects phrase-level updates into each token representation, yielding the canonicalized Layer 2 MLP output:

$$
\text{Layer 2 MLP Output} = \begin{bmatrix}
  0.02 & -0.04 &  0.06 & -0.08 &  0.10 & -0.12 \\
 -0.02 &  0.04 & -0.06 &  0.08 & -0.10 &  0.12 \\
  0.10 &  0.10 &  0.10 & -0.10 & -0.10 & -0.10 \\
 -0.10 & -0.10 & -0.10 &  0.10 &  0.10 &  0.10
\end{bmatrix}
$$

## The Final Integration

The architecture concludes Layer 2 with a final residual connection, adding the output of the Multi-Layer Perceptron back to $\text{Residual}_1$ to form the definitive output tensor $X_{\text{final}}$ of the second layer. This additive skip connection preserves an unimpeded gradient highway during backpropagation while retaining the accumulated structural context from both layers:

$$
\text{Output}_{\text{Layer 2}} = \text{Residual}_1 + \text{MLP}_{\text{out}}
$$

Adding `Layer 2 MLP Output` to `After First Residual` produces the final $4 \times 6$ representation $X_{\text{final}}$ exiting the Transformer blocks:

$$
\text{Layer 2 Final Output } (X_{\text{final}}) = \begin{bmatrix}
  0.15 & -0.30 &  0.45 & -0.60 &  0.75 & -0.90 \\
 -0.15 &  0.30 & -0.45 &  0.60 & -0.75 &  0.90 \\
  0.75 &  0.75 &  0.75 & -0.75 & -0.75 & -0.75 \\
 -0.75 & -0.75 & -0.75 &  0.75 &  0.75 &  0.75
\end{bmatrix}
$$

*(Note: Adding `0.05/-0.05` and `0.03/0.02` in an uncalibrated variant would shift Row 3 away from zero-sum symmetry; maintaining strict zero-sum step symmetry `0.75/-0.75` on Rows 3 and 4 guarantees that the unembedding projection in Part 17 maps `woke` and `up` to uniform `-0.0675` and `+0.0675` logits.)*

The initial token embeddings have now been transformed twice by multi-head attention blocks and twice by feed-forward memory banks. The discrete vocabulary indices that entered Layer 1 have evolved into continuous geometric coordinates that encapsulate grammar, context, and phrasal meaning tailored to the input sequence. In Part 17, the unembedding matrix $W_U$ projects this $4 \times 6$ tensor back into the 12-token vocabulary space to score the next-word candidates.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
