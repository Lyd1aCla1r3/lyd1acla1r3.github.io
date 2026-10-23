# Part 22: Backpropagation - Attention (Part 1: Softmax & Scores)

<!-- SUMMARY: The gradient propagates backward through the self-attention mechanism by solving the Jacobian of the softmax function and navigating the causal mask. This matrix operation accounts for coupled row probabilities and zeroes out future-looking connections, yielding the error signal for the unmasked attention scores. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

Part 21 routed the gradient down the residual stream to the output boundary of the Layer 2 attention block. Pulling this error signal backward through the self-attention mechanism requires reversing the sequence of operations that produced the attention output. In the forward pass, the mechanism applied a lower-triangular causal mask to the scaled dot-product scores, normalized each row through the Softmax function to form the attention probability matrix $P$, and multiplied $P$ by the Value matrix $V$.

## From Values to Probabilities

During the forward pass, each attention head computed its output $Z$ as the matrix product of the $4 \times 4$ probability matrix $P$ and the $4 \times 2$ Value matrix $V$:

$$
Z = P V
$$

Given the upstream gradient $d\_Z = \frac{\partial L}{\partial Z}$ of shape $4 \times 2$ arriving at the head output, the chain rule for matrix multiplication determines the gradient with respect to the attention probabilities $P$. Multiplying the incoming output gradient $d\_Z$ by the transpose of the Value matrix $V^T$ ($2 \times 4$) produces the $4 \times 4$ probability gradient matrix $d\_P$:

$$
d\_P = d\_Z V^T
$$

The matrix $d\_P$ measures how the scalar loss would change if each individual attention weight shifted in isolation. Each entry $(i, j)$ records the raw sensitivity of the loss to the routing weight connecting query token $i$ to key token $j$.

## The Calculus of Softmax

The probability gradient $d\_P$ must next pass backward through the row-wise Softmax function to recover the gradient with respect to the pre-Softmax attention scores $S$.

Softmax normalizes each row vector of unbounded scores into a coupled probability distribution summing to `1.0`. Perturbing a single score $S_{i,j}$ alters the normalization denominator for row $i$, shifting every probability in that row. Differentiating a Softmax row vector with respect to its input scores therefore yields a $4 \times 4$ Jacobian matrix per row rather than an element-wise derivative.

Contracting the upstream row gradient $d\_P_{i,:}$ with the row Jacobian reduces the backward pass through Softmax across the entire sequence to a compact matrix operation:

$$
d\_S = P \odot \left( d\_P - \text{rowsum}\left( d\_P \odot P \right) \right)
$$

In this expression, $\odot$ denotes element-wise (Hadamard) multiplication, and $\text{rowsum}(d\_P \odot P)$ sums each row across its four key columns to form a $4 \times 1$ column vector before broadcasting the subtraction across the row.

To trace this coupled derivative at four-decimal precision, consider a calibrated single-head backward state with forward causal probabilities $P$ and incoming probability gradients $d\_P$:

$$
P = \begin{bmatrix}
1.0000 & 0.0000 & 0.0000 & 0.0000 \\
0.5000 & 0.5000 & 0.0000 & 0.0000 \\
0.4530 & 0.5320 & 0.0150 & 0.0000 \\
0.5900 & 0.1510 & 0.1290 & 0.1300
\end{bmatrix}
$$

$$
d\_P = \begin{bmatrix}
 0.0242 & -0.1913 & -0.1725 & -0.0562 \\
-0.1013 &  0.0314 & -0.0908 & -0.1412 \\
 0.1466 & -0.0228 &  0.0068 & -0.1425 \\
-0.0544 &  0.0111 & -0.1151 &  0.0376
\end{bmatrix}
$$

Evaluating $d\_S = P \odot (d\_P - \text{rowsum}(d\_P \odot P))$ row by row illustrates three structural properties of the Softmax backward pass:

- **Zero Gradient on Deterministic Row 1:** Token 1 (`<BOS>`) attends exclusively to itself with probability $P_{0,0} = 1.0000$, so $\text{rowsum}_0 = 0.0242 \times 1.0000 = 0.0242$ and $d\_S_{0,0} = 1.0000 \times (0.0242 - 0.0242) = 0.0000$. A single unmasked element always normalizes to `1.0`, so shifting its score cannot alter its probability.
- **Equal-but-Opposite Coupling on Row 2:** With $P_{1,:} = [0.5000, 0.5000, 0.0000, 0.0000]$, the row dot product evaluates to $-0.1013(0.5) + 0.0314(0.5) = -0.03495$, yielding $d\_S_{1,0} = 0.5000(-0.1013 + 0.03495) = -0.0332$ and $d\_S_{1,1} = +0.0332$.
- **Zero-Sum Row Conservation:** Every row of $d\_S$ sums to zero ($-0.0332 + 0.0332 = 0$, $0.0417 - 0.0410 - 0.0007 = 0$, and $-0.0083 + 0.0078 - 0.0096 + 0.0101 = 0$), reflecting that probability mass added to one key position must be subtracted from competing positions in the same row.

Combining all four rows produces the $4 \times 4$ score gradient matrix $d\_S$:

$$
d\_S = \begin{bmatrix}
0.0000 & 0.0000 & 0.0000 & 0.0000 \\
-0.0332 & 0.0332 & 0.0000 & 0.0000 \\
0.0417 & -0.0410 & -0.0007 & 0.0000 \\
-0.0083 & 0.0078 & -0.0096 & 0.0101
\end{bmatrix}
$$

## Traversing the Causal Mask

The matrix $d\_S$ represents the gradient with respect to the masked attention scores. The final step in this stage propagates the gradient backward through the causal mask.

During the forward pass, a lower-triangular mask overwrote all entries above the main diagonal with $-\infty$ before Softmax normalization. That structural barrier prevented tokens from attending to future sequence positions, and exponentiating $-\infty$ inside the Softmax function assigned a strict `0.0000` probability to every upper-triangular connection.

In the backward pass, gradients flow only along paths that carried information forward. Overwriting the upper-triangular scores during the forward pass severed their causal influence on the loss, meaning the derivative with respect to those masked positions is identically zero.

Multiplying $d\_S$ element-wise by the binary lower-triangular mask enforces this causal boundary explicitly:

$$
d\_S_{\text{unmasked}} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix} \odot d\_S
$$

Multiplying by $P$ inside the Softmax Jacobian already zeroed out every position where $P_{i,j} = 0.0000$, so applying the binary mask leaves the lower-triangular entries unchanged and guarantees zero gradient leakage across future positions:

$$
d\_S_{\text{unmasked}} = \begin{bmatrix}
0.0000 & 0.0000 & 0.0000 & 0.0000 \\
-0.0332 & 0.0332 & 0.0000 & 0.0000 \\
0.0417 & -0.0410 & -0.0007 & 0.0000 \\
-0.0083 & 0.0078 & -0.0096 & 0.0101
\end{bmatrix}
$$

The network now holds the gradient with respect to the unmasked scaled dot-product scores. Part 23 distributes this score gradient alongside the output gradient into the Query, Key, and Value projections to update $W_Q$, $W_K$, and $W_V$.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
