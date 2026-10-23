# Part 20: The Beautiful Cancellation

<!-- SUMMARY: Chaining the derivatives of the cross-entropy loss and the softmax function reveals an algebraic cancellation that simplifies the output gradient. This derivation establishes the primary error signal as the direct difference between the predicted probabilities and the ground-truth one-hot targets. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

Part 19 established the geometry of the cross-entropy loss function by measuring how far the predicted probability distribution strayed from the ground-truth one-hot vector. That scalar loss value quantifies the total prediction error of the network. Assigning credit and blame for that accumulated error initiates backpropagation, starting with the gradient of the loss with respect to the final unnormalized scores, known as the logits.

## The Calculus Problem

Backpropagation relies on the chain rule of calculus. Determining how a specific weight inside the network contributed to the final error requires multiplying the local derivatives of every operation situated between that weight and the scalar loss. The backward traversal begins at the output boundary of the architecture, moving from the cross-entropy loss, through the Softmax normalization, and into the vocabulary logits.

Differentiating these two output operations in isolation introduces substantial algebraic complexity. Softmax is a coupled normalization rather than an element-wise function: perturbing the unnormalized logit for a single token alters the denominator sum and shifts the output probability of every token in the vocabulary. The derivative of a Softmax vector with respect to its logit vector forms a dense Jacobian matrix tracking all pairwise output-input interactions:

- **Diagonal Entries ($i = j$):** Evaluate to $P_i(1 - P_i)$, measuring how a logit change affects its own token probability.
- **Off-Diagonal Entries ($i \neq j$):** Evaluate to $-P_i P_j$, capturing how increasing one logit suppresses the probabilities of competing tokens.

The derivative of the cross-entropy loss $-\log(P_{\text{target}})$ introduces an inverse probability factor $-1 / P_{\text{target}}$. Multiplying that fractional gradient through the full Softmax Jacobian appears computationally expensive until the terms are combined algebraically.

## The Mathematical Elegance

Applying the chain rule to combine the cross-entropy derivative with the Softmax Jacobian causes the nonlinear fractional terms and coupling products to cancel out. For a single sequence position (or summing positional losses $L = \sum_{t=1}^S L_t$ across the sequence), the gradient of the cross-entropy loss $L$ with respect to the pre-Softmax logit tensor $z$ reduces to a linear subtraction:

$$
\frac{\partial L}{\partial z} = P - Y
$$

In this expression, $P$ denotes the $4 \times 12$ predicted probability matrix from the Softmax layer, and $Y$ denotes the $4 \times 12$ ground-truth one-hot target matrix. Averaging the loss over $S = 4$ positions scales this matrix by a constant factor of $1/4$, which is absorbed into the optimizer learning rate during parameter updates.

## Applying the Cancellation

This algebraic cancellation maps directly onto the concrete matrices of the four-token sequence. Each row compares the forward-pass probability distribution against the one-hot target token for that time step:

| Time Step | Input Token | Target Token | Target Index | Target Logit Gradient (`P_target - 1`) |
| :--- | :--- | :--- | :--- | :--- |
| **Step 1** | `<BOS>` | `i` | `3` | `-0.9157` (`0.0843 - 1.0`) |
| **Step 2** | `i` | `woke` | `5` | `-0.9169` (`0.0831 - 1.0`) |
| **Step 3** | `woke` | `up` | `7` | `-0.9167` (`0.0833 - 1.0`) |
| **Step 4** | `up` | `late` | `8` | `-0.9167` (`0.0833 - 1.0`) |

Stacking the four one-hot target vectors forms the $4 \times 12$ ground-truth matrix $Y$, where each row places a `1.0` at the target vocabulary index and `0` at the remaining eleven indices:

$$
Y = \begin{bmatrix}
 0 &  0 &  0 &  1.0 &  0 &  0 &  0 &  0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  1.0 &  0 &  0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  0 &  0 &  1.0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  0 &  0 &  0 &  1.0 & \dots &  0
\end{bmatrix}
$$

Subtracting the one-hot target matrix $Y$ from the Part 18 probability matrix $P$ produces the $4 \times 12$ logit gradient matrix $\frac{\partial L}{\partial z}$:

$$
\frac{\partial L}{\partial z} = \begin{bmatrix}
 0.0854 &  0.0850 &  0.0846 & -0.9157 &  0.0839 &  0.0835 &  0.0831 &  0.0828 &  0.0824 & \dots &  0.0813 \\
 0.0813 &  0.0817 &  0.0820 &  0.0824 &  0.0828 & -0.9169 &  0.0835 &  0.0839 &  0.0843 & \dots &  0.0854 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & -0.9167 &  0.0833 & \dots &  0.0833 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & -0.9167 & \dots &  0.0833
\end{bmatrix}
$$

## The Physical Intuition

The matrix $\frac{\partial L}{\partial z}$ encodes both the direction and magnitude of the required correction for every vocabulary logit at every position.

Gradient descent reduces loss by subtracting a scaled multiple of the gradient from the parameters. That subtraction induces opposite corrective forces on target and non-target columns:

- **Target Token Columns ($Y_{t,j} = 1.0$):** The forward pass assigned a probability near `0.083` where the target value is `1.0`, producing a large negative gradient near `-0.917`. Subtracting this negative gradient during optimization increases the unnormalized logit for the ground-truth token.
- **Non-Target Token Columns ($Y_{t,j} = 0.0$):** The subtraction $P_{t,j} - 0.0$ yields a positive gradient equal to the predicted probability mass near `+0.083`. Subtracting this positive gradient pushes down the logits of all eleven incorrect vocabulary candidates in proportion to how much probability mass the model mistakenly allocated to them.

Combining cross-entropy loss with Softmax normalization produces a self-balancing error signal at the output boundary. The next stage propagates this $4 \times 12$ gradient matrix backward through the unembedding projection $W_U$ and into the Layer 2 residual stream.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
