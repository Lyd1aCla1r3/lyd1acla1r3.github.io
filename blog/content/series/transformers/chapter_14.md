# Part 14: Scoring Deep Context: Layer 2 Attention
<!-- SUMMARY: This installment explores the fundamental shift in Query and Key vectors during Layer 2, examining how compound semantic structures are scored using the scaled dot-product. By stabilizing the variance of these unscaled scores, the model prevents Softmax saturation and preserves gradient health during backpropagation. -->

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

In our progression through the Transformer architecture, we have reached a critical inflection point. The Query and Key vectors we extract in Layer 2 are fundamentally different from those in Layer 1. Rather than representing isolated vocabulary tokens, they now encapsulate rich, contextualized concepts fused from the entire preceding sequence. This part examines exactly how these advanced representations are scored against one another, illuminating the mathematical process by which deep neural networks decide to route high-level information.

## The Semantic Shift in Queries and Keys

When we calculated the attention scores in Layer 1, our Queries ($Q$) and Keys ($K$) were derived from raw word embeddings plus positional information. They were searching for basic relationships, such as a subject looking for a verb. In Layer 2, our input vectors have passed through the first attention mechanism and the Multi-Layer Perceptron. They have already absorbed surrounding context.

Our model is processing the sequence `<BOS> i woke up` with the goal of predicting the next token. The vectors corresponding to "woke" and "up" are no longer isolated; they have mixed their information in the residual stream. Consequently, the Layer 2 $Q_2$ and $K_2$ matrices project this mixed, abstract data into a new dimensional space. They are asking highly specific, compound questions about the sentence structure.

Let us review the exact $Q_2$ matrix and the transposed Key matrix $K_2^T$ for our first attention head in Layer 2.

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

The fundamental mechanism for determining relevance remains the dot product. By multiplying $Q_2$ and $K_2^T$, we compute the raw alignment between every contextualized query and every contextualized key. The dot product is geometrically elegant; it returns a high positive value when vectors point in similar directions, a high negative value when they are opposed, and zero when they are orthogonal.

We perform the matrix multiplication $Q_2 \cdot K_2^T$ to generate our unscaled attention scores. 

$$
\text{Scores}_{\text{unscaled}} = \begin{bmatrix}
-0.64 & -0.38 & 1.30 & 1.21 \\
-0.40 & -0.18 & 0.71 & 0.63 \\
1.31 & 0.67 & -2.48 & -2.27 \\
1.26 & 0.62 & -2.35 & -2.14
\end{bmatrix}
$$

Notice the pronounced values in the lower half of this matrix. The vectors corresponding to "woke" and "up" are exhibiting strong reactions. The mathematical projection has successfully highlighted a strong structural alignment between these specific positions. They are preparing to share profound semantic information.

## Stabilizing the Variance

We must now apply the scaling factor. As established in Phase 2, the variance of a dot product grows proportionally with the dimensionality of the vectors involved. High variance leads to extreme values in the unscaled scores. If we pass extreme values into the Softmax function, the resulting probability distribution becomes overly rigid. It assigns nearly 100% of the probability weight to a single token, operating in regions where the gradient is effectively zero. This phenomenon is known as Softmax saturation and it prevents the network from learning during backpropagation.

To maintain a healthy gradient, we divide the unscaled scores by the square root of the head dimensionality $\sqrt{d_k}$. Our model uses $d_k = 2$, so we divide by $\sqrt{2} \approx 1.414$.

$$
\text{Scores}_{\text{scaled}} = \begin{bmatrix}
-0.45 & -0.27 & 0.92 & 0.86 \\
-0.28 & -0.13 & 0.50 & 0.45 \\
0.93 & 0.47 & -1.76 & -1.60 \\
0.89 & 0.44 & -1.66 & -1.51
\end{bmatrix}
$$

By scaling these values, we preserve the relative alignments while compressing the absolute magnitudes. This ensures the upcoming probability distribution remains expressive enough to route information proportionally across multiple tokens, rather than collapsing into a rigid selection.

Our deep conceptual representations have now calculated their mutual relevance. The next mathematical step requires us to enforce causality upon these scores, ensuring that our model strictly adheres to the arrow of time during the training phase.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
