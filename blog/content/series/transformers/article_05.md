# Article 5: Causal Masking

In our previous session, we successfully derived the scaled attention scores. We calculated the dot product between our Query and Key matrices, measuring how intensely each token seeks information from every other token, and scaled the result by $\sqrt{d_k}$ to prevent gradient saturation. 

Before we can convert these scores into a final probability distribution, we must address a critical structural flaw in how our matrix currently operates during training. 

### The Problem of Parallel Training

When training a Transformer, we do not feed tokens in one by one. We optimize for speed by passing the entire sequence through the network simultaneously. This technique is known as teacher forcing. Our matrix operations compute the attention scores for `<BOS>`, `i`, `woke`, and `up` all at the exact same time.

Let us examine the scaled attention scores from our previous calculation. The rows represent our Queries looking for information, and the columns represent our Keys offering information.

$$
\text{Scaled Scores} = \begin{bmatrix}
0.45 & 0.68 & 0.73 & 0.63 \\
0.59 & 0.87 & 0.93 & 0.79 \\
-0.09 & -0.20 & -0.26 & -0.28 \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

The first row represents the `<BOS>` token acting as a Query. It is generating attention scores against all available Keys. The second column of the first row holds a score of 0.68, representing the `<BOS>` token attending to the `i` token.

This reveals a profound issue. If the model is processing the `<BOS>` token to predict the next logical word in the sequence, it should only have access to information from the `<BOS>` token itself. In our current matrix, the `<BOS>` token has full visibility into the future tokens `i`, `woke`, and `up`. The model is effectively looking at the answer key while taking the test. The network will perfectly learn to copy the next token rather than learning the underlying linguistic patterns.

### The Causal Mask

We must physically block the flow of information from future tokens into past tokens. We achieve this by applying a lower-triangular mask to the attention scores. 

We define a mask where any position representing a Query attending to a future Key is marked for obstruction.

$$
\text{Mask} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix}
$$

Where the mask holds a 1, we keep the original scaled score. Where the mask holds a 0, we overwrite the score with negative infinity ($-\infty$). Applying this operation yields our masked attention scores.

$$
\text{Masked Scores} = \begin{bmatrix}
0.45 & -\infty & -\infty & -\infty \\
0.59 & 0.87 & -\infty & -\infty \\
-0.09 & -0.20 & -0.26 & -\infty \\
-0.18 & -0.33 & -0.39 & -0.39
\end{bmatrix}
$$

By inspecting the second row, we see the Query for the token `i` can only attend to the Key for `<BOS>` and the Key for `i`. The scores for `woke` and `up` have been obliterated. Causality is preserved.

### The Mathematical Role of Negative Infinity

We use $-\infty$ rather than zero due to the mathematical properties of the next operation in the architecture. The Softmax function will soon convert these scores into a valid probability distribution. The Softmax function exponentiates each value using $e^x$.

As $x$ approaches $-\infty$, the value of $e^x$ converges exactly to 0. When we calculate the final attention weights in the next step, any connection blocked by our causal mask will receive a probability weight of precisely 0%. Future tokens will contribute nothing to the mathematical representation of past tokens.

With our causal mask firmly in place, we are ready to safely pass these masked scores through the Softmax function and extract our final Value matrices.
