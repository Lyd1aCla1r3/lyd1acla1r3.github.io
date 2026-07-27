# Part 14: Final Layer 1 Residuals, Norms, and Layer 2 Attention
<!-- SUMMARY: The Multilayer Perceptron output is added back into the residual stream, preserving the original contextual information while integrating the newly activated conceptual features. A final layer normalization step stabilizes the vector geometry, preparing the enriched representations for Layer 2. The query and key vectors then undergo a fundamental mathematical shift as compound semantic structures are scored using the scaled dot-product. Stabilizing the variance of these unscaled scores prevents softmax saturation and preserves gradient health during backpropagation. -->

The completion of the Multilayer Perceptron marks the end of the conceptual feature extraction phase. The network has successfully identified relevant patterns within the token vectors and projected those insights back into the original six-dimensional space. The next crucial step involves integrating this newly extracted knowledge with the existing representation.

This integration occurs via the residual stream. Rather than replacing the prior state entirely, the output of the feed-forward network is added directly to the original token vectors that entered the block. This architectural design ensures that the fundamental identity of the token is preserved alongside its newly refined conceptual context. The additive nature of the residual connection provides a direct gradient path during backpropagation, circumventing the risk of signal decay.

The state of the residual stream prior to the feed-forward network is represented by the following matrix.

$$
\text{Original Residual Stream} = \begin{bmatrix}
 0.02 &  1.29 &  0.18 &  1.35 &  0.00 &  0.67 \\
 0.74 &  1.76 &  0.45 &  1.52 &  0.20 &  1.23 \\
 0.88 & -0.31 &  1.78 &  0.99 &  0.09 &  0.91 \\
 0.19 & -1.03 &  1.56 &  1.21 &  0.58 &  0.69
\end{bmatrix}
$$

The network then adds the contracted output from the Multilayer Perceptron directly to this stream.

$$
\text{MLP Output} = \begin{bmatrix}
-4.07 &  0.04 & -0.06 & -1.74 & -1.17 & -0.77 \\
-6.51 &  0.18 & -0.33 & -3.85 & -0.84 & -1.43 \\
 0.82 & -3.22 &  0.39 & -2.11 &  3.22 &  6.02 \\
 1.18 & -2.83 & -0.72 & -1.89 &  1.58 &  4.39
\end{bmatrix}
$$

The resulting addition produces a deeply enriched representation. The network has successfully woven complex, localized conceptual features into the broader contextual fabric established by the self-attention mechanism.

$$
\text{New Residual Stream} = \begin{bmatrix}
-4.05 &  1.33 &  0.12 & -0.39 & -1.17 & -0.10 \\
-5.77 &  1.94 &  0.12 & -2.33 & -0.64 & -0.20 \\
 1.70 & -3.53 &  2.17 & -1.12 &  3.31 &  6.93 \\
 1.37 & -3.86 &  0.84 & -0.68 &  2.16 &  5.08
\end{bmatrix}
$$

Before these vectors can progress to the subsequent layer, their geometric properties must be stabilized. The addition operation inherently shifts the mean and expands the variance of the token representations. Left unchecked, this numerical drift would destabilize the learning process.

The application of layer normalization corrects this drift. The operation recalculates the mean and variance independently for each token vector and scales the values to achieve a mean of zero and a variance of one. The magnitude of the vectors is constrained while preserving the vital directional information encoded within their relative dimensions.

$$
\text{Normalized Layer 2 Input} = \begin{bmatrix}
-2.00 &  1.22 &  0.50 &  0.19 & -0.28 &  0.37 \\
-1.91 &  1.28 &  0.52 & -0.49 &  0.21 &  0.39 \\
 0.04 & -1.55 &  0.18 & -0.82 &  0.52 &  1.62 \\
 0.20 & -1.72 &  0.01 & -0.55 &  0.49 &  1.57
\end{bmatrix}
$$

This normalization step concludes the first complete layer of the Transformer architecture. The initial embeddings have been profoundly transformed. The vectors no longer represent isolated vocabulary tokens. The representation has evolved into a rich amalgamation of semantic identity, positional context, and localized conceptual features.

The architecture is now prepared to pass these enriched vectors into Layer 2. The subsequent operations repeat the self-attention and feed-forward mechanisms, yet the mathematical focus shifts entirely. Rather than computing relationships between isolated words, the next layer computes relationships between these highly complex, contextualized representations, facilitating a crucial leap toward hierarchical abstraction.

In the progression through the Transformer architecture, the network reaches a critical inflection point. The Query and Key vectors extracted in Layer 2 are fundamentally different from those in Layer 1. Rather than representing isolated vocabulary tokens, they now encapsulate rich, contextualized concepts fused from the entire preceding sequence. This section examines exactly how these advanced representations are scored against one another, illuminating the mathematical process by which deep neural networks decide to route high-level information.

## The Semantic Shift in Queries and Keys

When the attention scores were calculated in Layer 1, the Queries $Q$ and Keys $K$ were derived from raw word embeddings plus positional information. They were searching for basic relationships, such as a subject looking for a verb. In Layer 2, the input vectors have passed through the first attention mechanism and the Multi-Layer Perceptron. They have already absorbed surrounding context.

The model is processing the sequence `<BOS> i woke up` with the goal of predicting the next token. The vectors corresponding to "woke" and "up" are no longer isolated; they have mixed their information in the residual stream. Consequently, the Layer 2 $Q_2$ and $K_2$ matrices project this mixed, abstract data into a new dimensional space. They are asking highly specific, compound questions about the sentence structure.

The exact $Q_2$ matrix and the transposed Key matrix $K_2^T$ for the first attention head in Layer 2 are presented below.

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

The fundamental mechanism for determining relevance remains the dot product. By multiplying $Q_2$ and $K_2^T$, the network computes the raw alignment between every contextualized query and every contextualized key. The dot product is geometrically elegant; it returns a high positive value when vectors point in similar directions, a high negative value when they are opposed, and zero when they are orthogonal.

The matrix multiplication $Q_2 \cdot K_2^T$ is performed to generate the unscaled attention scores.

$$
\text{Scores}_{\text{unscaled}} = \begin{bmatrix}
-0.64 & -0.38 & 1.30 & 1.21 \\
-0.40 & -0.18 & 0.71 & 0.63 \\
1.31 & 0.67 & -2.48 & -2.27 \\
1.26 & 0.62 & -2.35 & -2.14
\end{bmatrix}
$$

Notice the pronounced values in the lower half of this matrix. The vectors corresponding to "woke" and "up" exhibit strong reactions. The mathematical projection has successfully highlighted a strong structural alignment between these specific positions. They are preparing to share profound semantic information.

## Stabilizing the Variance

The scaling factor must now be applied. As established in Phase 2, the variance of a dot product grows proportionally with the dimensionality of the vectors involved. High variance leads to extreme values in the unscaled scores. If extreme values are passed into the Softmax function, the resulting probability distribution becomes overly rigid. It assigns nearly 100% of the probability weight to a single token, operating in regions where the gradient is effectively zero. This phenomenon is known as Softmax saturation and it prevents the network from learning during backpropagation.

To maintain a healthy gradient, the unscaled scores are divided by the square root of the head dimensionality $\sqrt{d_k}$. The model uses $d_k = 2$, so the division is by $\sqrt{2} \approx 1.414$.

$$
\text{Scores}_{\text{scaled}} = \begin{bmatrix}
-0.45 & -0.27 & 0.92 & 0.86 \\
-0.28 & -0.13 & 0.50 & 0.45 \\
0.93 & 0.47 & -1.76 & -1.60 \\
0.89 & 0.44 & -1.66 & -1.51
\end{bmatrix}
$$

By scaling these values, the relative alignments are preserved while the absolute magnitudes are compressed. This ensures the upcoming probability distribution remains expressive enough to route information proportionally across multiple tokens, rather than collapsing into a rigid selection.

The deep conceptual representations have now calculated their mutual relevance. The next mathematical step requires enforcing causality upon these scores, ensuring that the model strictly adheres to the arrow of time during the training phase.
