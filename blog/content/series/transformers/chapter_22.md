# Part 22: Backpropagation - Attention (Part 1: Softmax & Scores)

<!-- SUMMARY: The gradient propagates backward through the self-attention mechanism by solving the Jacobian of the softmax function and navigating the causal mask. This matrix operation handles coupled probabilities and severs the learning signal for future-looking connections, yielding the exact error for unmasked attention scores. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

The previous installment routed the gradient down the residual stream to the output of the Layer 2 attention block. The objective now requires pulling this error signal backward through the self-attention mechanism itself. This requires unpacking the sequence of operations that created the attention output. The final operations in that sequence involved multiplying the attention probabilities by the Value matrix, and prior to that, applying the softmax function to the masked attention scores.

## From Values to Probabilities

During the forward pass, the attention output emerged as the matrix product of the probability matrix $P$ and the Value matrix $V$. The gradient of the loss with respect to this output represents the exact direction required to minimize the error in the final contextualized vectors. To determine the necessary adjustment for the attention probabilities $P$, the standard chain rule for matrix multiplication is applied. The gradient with respect to $P$ equals the incoming gradient multiplied by the transpose of $V$. The resulting gradient matrix is defined as $d\_P$.

The matrix $d\_P$ dictates how the loss would change if the attention probabilities shifted. It is a square matrix mapping sequence length by sequence length, detailing the precise error signal for the attention connection between every pair of tokens in the text.

## The Calculus of Softmax

The gradient $d\_P$ must pass backward through the softmax function to uncover the gradient with respect to the raw, pre-softmax attention scores. These pre-softmax scores are defined as $S$.

The softmax function presents a unique mathematical challenge. It takes a vector of scores and normalizes them into a coupled probability distribution. Changing a single score in the input vector alters the sum in the denominator for all other elements, inherently shifting the final probability of every other element. Consequently, the derivative of a softmax output with respect to its input forms a Jacobian matrix containing the partial derivatives of every output with respect to every input.

The mathematical formula for backpropagating through softmax across an entire sequence reduces to an elegant matrix operation:

$$
d\_S = P \odot \left( d\_P - \sum \left( d\_P \odot P \right) \right)
$$

Here, $\odot$ represents element-wise multiplication. The incoming gradient $d\_P$ is multiplied by the probabilities $P$, summed along the sequence dimension, and subtracted from the original $d\_P$. The entire result is then multiplied element-wise by the probabilities $P$ again.

To anchor this physically, the network relies on the forward pass attention probabilities $P$:

$$
P = \begin{bmatrix}
1.0000 & 0.0000 & 0.0000 & 0.0000 \\
0.5000 & 0.5000 & 0.0000 & 0.0000 \\
0.4520 & 0.5320 & 0.0150 & 0.0000 \\
0.5900 & 0.1510 & 0.1290 & 0.1300
\end{bmatrix}
$$

This matrix operation captures the proportional interplay of probabilities. If a particular token received a high probability during the forward pass, its gradient heavily influences the adjustment of the pre-softmax scores. If a token was ignored and assigned a near-zero probability, the multiplication by $P$ ensures the gradient struggles to pass through, effectively severing the learning signal for that specific connection.

Applying the formula yields the precise gradient with respect to the masked scores, $d\_S$:

$$
d\_S = \begin{bmatrix}
0.0000 & 0.0000 & 0.0000 & 0.0000 \\
-0.0332 & 0.0332 & 0.0000 & 0.0000 \\
0.0417 & -0.0410 & -0.0007 & 0.0000 \\
-0.0083 & 0.0078 & -0.0096 & 0.0101
\end{bmatrix}
$$

## Traversing the Causal Mask

The matrix $d\_S$ represents the gradient with respect to the masked attention scores. The final step in this stage requires pushing the gradient through the causal mask.

During the forward pass, a lower-triangular mask was applied to the raw attention scores. All values above the diagonal were explicitly set to negative infinity. This structural intervention prevented tokens from attending to future positions, guaranteeing the model respects causality during parallel training. When the softmax function encountered negative infinity, it mapped it to a strict zero probability.

In the backward pass, gradients flow only where information flowed forward. Since the upper triangular elements of the score matrix were overwritten and ignored during the forward pass, they cannot have contributed to the final loss. The error signal for those future-looking connections must be zero.

To route the gradient through the causal mask, a binary lower-triangular mask is applied to $d\_S$, zeroing out the upper triangular portion:

$$
d\_S_{\text{unmasked}} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix} \odot d\_S
$$

The resulting unmasked scores gradient matrix remains largely identical, as the softmax gradient naturally forces the previously masked values to zero. However, this formal mathematical step guarantees the error signal cleanly respects causality:

$$
d\_S_{\text{unmasked}} = \begin{bmatrix}
0.0000 & 0.0000 & 0.0000 & 0.0000 \\
-0.0332 & 0.0332 & 0.0000 & 0.0000 \\
0.0417 & -0.0410 & -0.0007 & 0.0000 \\
-0.0083 & 0.0078 & -0.0096 & 0.0101
\end{bmatrix}
$$

The network now possesses the gradient with respect to the pure, unmasked attention scores, representing the direct scaled dot product between queries and keys. The error signal has successfully traversed the most numerically complex non-linearity in the Transformer architecture. The subsequent analysis will distribute this gradient into the Query, Key, and Value weight matrices, completing the learning cycle for the self-attention mechanism.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
