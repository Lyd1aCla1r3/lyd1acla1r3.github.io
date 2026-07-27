# Part 5: Causal Masking

<!-- SUMMARY: Parallel training introduces a structural vulnerability by allowing past tokens computational access to future context. Causality is preserved by applying a lower-triangular mask of negative infinity, establishing a mathematical barrier that neutralizes future information when passed through the softmax function. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

The scaled attention scores have now been successfully derived. The dot product between the Query and Key matrices was calculated to measure how intensely each token seeks information from every other token, and the result was scaled by $\sqrt{d_k}$ to prevent gradient saturation. 

Before converting these scores into a final probability distribution, a critical structural flaw in how the matrix currently operates during training must be addressed. 

## The Problem of Parallel Training

During Transformer training, tokens are not fed in sequentially. The process optimizes for speed by passing the entire sequence through the network simultaneously. This technique is known as teacher forcing. The matrix operations compute the attention scores for `<BOS>`, `i`, `woke`, and `up` at the exact same time.

Examining the scaled attention scores from the previous calculation provides further clarity. The rows represent the Queries looking for information, and the columns represent the Keys offering information.

$$
\text{Scaled Scores} = \begin{bmatrix}
0.45 & 0.68 & 0.73 & 0.63 \\
0.59 & 0.87 & 0.93 & 0.79 \\
-0.09 & -0.20 & -0.26 & -0.28 \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

The first row represents the `<BOS>` token acting as a Query. It generates attention scores against all available Keys. The second column of the first row holds a score of 0.68, representing the `<BOS>` token attending to the `i` token.

This reveals a profound issue. If the model processes the `<BOS>` token to predict the next logical word in the sequence, it should only have access to information from the `<BOS>` token itself. In the current matrix, the `<BOS>` token has full visibility into the future tokens `i`, `woke`, and `up`. The model effectively views the answer key while taking the test. The network will perfectly learn to copy the next token rather than learning the underlying linguistic patterns.

## The Causal Mask

The flow of information from future tokens into past tokens must be physically blocked. This is achieved by applying a lower-triangular mask to the attention scores. 

A mask is defined where any position representing a Query attending to a future Key is marked for obstruction.

$$
\text{Mask} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix}
$$

Where the mask holds a 1, the original scaled score is retained. Where the mask holds a 0, the score is overwritten with negative infinity ($-\infty$). Applying this operation yields the masked attention scores.

$$
\text{Masked Scores} = \begin{bmatrix}
0.45 & -\infty & -\infty & -\infty \\
0.59 & 0.87 & -\infty & -\infty \\
-0.09 & -0.20 & -0.26 & -\infty \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

Inspecting the second row reveals the Query for the token `i` can only attend to the Key for `<BOS>` and the Key for `i`. The scores for `woke` and `up` have been obliterated. Causality is preserved.

## The Mathematical Role of Negative Infinity

The value $-\infty$ is used rather than zero due to the mathematical properties of the next operation in the architecture. The Softmax function will soon convert these scores into a valid probability distribution. The Softmax function exponentiates each value using $e^x$.

As $x$ approaches $-\infty$, the value of $e^x$ converges exactly to 0. When the final attention weights are calculated in the next step, any connection blocked by the causal mask will receive a probability weight of precisely 0%. Future tokens will contribute nothing to the mathematical representation of past tokens.

With the causal mask firmly in place, the masked scores can safely pass through the Softmax function to extract the final Value matrices.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
