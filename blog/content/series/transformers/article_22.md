# Article 22: Backpropagating Through Attention: The Softmax and the Mask

We left off with the gradient flowing down the residual stream, reaching the output of our Layer 2 attention block. Our objective now is to pull this error signal backward through the self-attention mechanism itself. This requires us to unpack the sequence of operations that created the attention output. The final operations in that sequence involved multiplying the attention probabilities by the Value matrix, and prior to that, applying the Softmax function to the masked attention scores.

## From Values to Probabilities

During the forward pass, the attention output is computed as the matrix product of the probability matrix $P$ and the Value matrix $V$. The gradient of the loss with respect to this output represents the exact direction we must move to minimize the error in our final contextualized vectors. To determine how to adjust the attention probabilities $P$, we apply the standard chain rule for matrix multiplication. The gradient with respect to $P$ is the incoming gradient multiplied by the transpose of $V$. We will define this resulting gradient matrix as $d\_P$.

The matrix $d\_P$ tells us how the loss would change if we tweaked the attention probabilities. It is a sequence-by-sequence square matrix, detailing the precise error signal for the attention connection between every pair of tokens in our text.

## The Calculus of Softmax

We must push this gradient $d\_P$ backward through the Softmax function to find the gradient with respect to the raw, pre-Softmax attention scores. We will define these pre-Softmax scores as $S$. 

The Softmax function presents a unique mathematical challenge. It takes a vector of scores and normalizes them into a coupled probability distribution. Changing a single score in the input vector alters the sum in the denominator for all other elements, inherently shifting the final probability of every other element. Consequently, the derivative of a Softmax output with respect to its input is a Jacobian matrix containing the partial derivatives of every output with respect to every input.

The mathematical formula for backpropagating through Softmax across an entire sequence reduces to an elegant matrix operation:

$$
d\_S = P \odot (d\_P - \sum (d\_P \odot P))
$$

Here, $\odot$ represents element-wise multiplication. We multiply the incoming gradient $d\_P$ by the probabilities $P$, sum those results along the sequence dimension, and subtract that sum from the original $d\_P$. We then multiply the entire result element-wise by the probabilities $P$ again.

This formulation captures the proportional interplay of probabilities. If a particular token received a high probability during the forward pass, its gradient heavily influences the adjustment of the pre-Softmax scores. If a token was ignored and assigned a near-zero probability, the multiplication by $P$ ensures the gradient struggles to pass through, effectively severing the learning signal for that specific connection.

## Traversing the Causal Mask

We have successfully calculated $d\_S$, representing the gradient with respect to the masked attention scores. The final step in this stage is to push the gradient through the causal mask.

During the forward pass, we applied a lower-triangular mask to the raw attention scores. We explicitly set all values above the diagonal to negative infinity. This structural intervention prevented tokens from attending to future positions, guaranteeing our model respects causality during parallel training. When the Softmax function encountered negative infinity, it mapped it to a strict zero probability.

In the backward pass, gradients flow only where information flowed forward. Since the upper triangular elements of the score matrix were overwritten and ignored during the forward pass, they cannot have contributed to the final loss. The error signal for those future-looking connections must be zero. 

To route the gradient through the causal mask, we simply apply a binary lower-triangular mask to $d\_S$, zeroing out the upper triangular portion:

$$
d\_S\_{unmasked} = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1
\end{bmatrix} \odot d\_S
$$

We now possess the gradient with respect to the pure, unmasked attention scores, representing the direct scaled dot product $Q K^T / \sqrt{d_k}$. Our error signal has successfully traversed the most numerically complex non-linearity in the Transformer architecture. In our next installment, we will distribute this gradient into the Query, Key, and Value weight matrices, completing the learning cycle for the self-attention mechanism.
