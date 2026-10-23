# Part 5: Causal Masking

<!-- SUMMARY: Parallel training introduces a structural vulnerability by allowing past tokens computational access to future context. Causality is preserved by applying a lower-triangular mask of negative infinity, establishing a mathematical barrier that neutralizes future information when passed through the softmax function. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

The scaled attention scores have now been derived. The dot product between the Query and Key matrices was calculated to measure how strongly each token seeks information from every other token, and the result was scaled by $\sqrt{d_k}$ to prevent gradient saturation. 

Before converting these scores into a final probability distribution, a structural constraint governing parallel training must be enforced.

## The Problem of Parallel Training

During Transformer training, tokens are not processed sequentially one step at a time. Parallel training passes the entire target sequence through the network simultaneously using a technique known as teacher forcing. Matrix multiplications compute the attention scores for `<BOS>`, `i`, `woke`, and `up` concurrently in a single forward pass.

Examining the scaled attention scores from the previous calculation illustrates this behavior. The rows represent the Queries seeking information, and the columns represent the Keys offering information:

$$
\text{Scaled Scores} = \begin{bmatrix}
0.45 & 0.68 & 0.73 & 0.63 \\
0.59 & 0.87 & 0.93 & 0.79 \\
-0.09 & -0.20 & -0.26 & -0.28 \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

The first row represents the `<BOS>` token acting as a Query. It generates attention scores against all available Keys. The second column of the first row holds a score of `0.68`, representing the `<BOS>` token attending to the `i` token.

That non-zero weight exposes a causality violation during parallel training. Predicting the token immediately following `<BOS>` permits the model to condition only on `<BOS>` itself. In the unmasked score matrix, the first row grants `<BOS>` direct visibility into the future tokens `i`, `woke`, and `up`. Allowing past positions to read future positions leaks the target labels into the forward pass, teaching the network to copy upcoming tokens rather than modeling causal structure.

## The Causal Mask

Preserving autoregressive causality requires blocking information flow from future tokens into past positions. Applying a lower-triangular causal mask to the scaled score matrix enforces this directional boundary.

A mask is defined where any position representing a Query attending to a future Key is marked for obstruction:

$$
\text{Mask} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix}
$$

Where the mask holds a `1`, the original scaled score is retained. Where the mask holds a `0`, the score is overwritten with negative infinity ($-\infty$). Applying this operation yields the masked attention scores:

$$
\text{Masked Scores} = \begin{bmatrix}
0.45 & -\infty & -\infty & -\infty \\
0.59 & 0.87 & -\infty & -\infty \\
-0.09 & -0.20 & -0.26 & -\infty \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

Inspecting the second row confirms that the Query for the token `i` can attend only to the Key for `<BOS>` and the Key for `i`. The upper-triangular scores for `woke` and `up` are masked out, preserving temporal causality.

## The Mathematical Role of Negative Infinity

The value $-\infty$ is used rather than zero due to the algebraic properties of the Softmax normalization step that follows. The Softmax function converts each row of scores into a probability distribution by exponentiating every entry via $e^x$.

In the limit $x \to -\infty$, the exponential $e^x$ evaluates to $0$. Normalizing the masked rows through the Softmax function assigns a probability weight of $0.00$ to every upper-triangular entry, ensuring that future tokens contribute zero weight to the representation of past tokens.

With the causal mask in place, the masked scores can pass through the Softmax function to weight the Value vectors.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
