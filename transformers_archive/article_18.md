# Part 18: Final Softmax and Predictions

<!-- SUMMARY: The unbounded vocabulary logits are transformed into a strict probability distribution using the softmax function. Analyzing this distribution reveals the untrained network's maximum mathematical uncertainty, while techniques like temperature scaling provide mechanisms to shape this entropy during actual text generation. -->

Projecting highly contextualized vectors out of the latent model space and back into the vocabulary space yields a matrix of raw scores known as logits. These scalar values assign a geometric magnitude to each of the twelve possible words in the vocabulary. While these magnitudes provide an ordering of likelihood, they do not constitute a mathematically rigorous probability distribution. The values extend across arbitrary bounds and lack the fundamental property of summing to exactly one. Converting these raw signals into actionable predictions requires a normalizing operation.

The architecture employs the softmax function across the vocabulary dimension of the logits matrix to enforce this transformation. The function operates by exponentiating each scalar value and dividing by the sum of all exponentiated values in that row. Exponentiation guarantees that all resultant values become strictly positive fractions while non-linearly amplifying the differences between scores. A slightly higher logit becomes a significantly higher exponentiated value, creating a dynamic that helps the network confidently select a single token. The subsequent division normalizes the outputs. This bounds all values between zero and one, creating a strict probability distribution where the sum across the vocabulary dimension equals exactly one.

$$
P(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}
$$

Applying this function to the calculated logit matrix transforms the raw scores at each sequence position. The four rows represent the predictions following the tokens start, "i", "woke", and "up".

$$
\text{Logits} = \begin{bmatrix}
-0.0270 & -0.0315 & -0.0360 & -0.0405 & -0.0450 & -0.0495 & -0.0540 & -0.0585 & \dots & -0.0765 \\
-0.0180 & -0.0135 & -0.0090 & -0.0045 &  0.0000 &  0.0045 &  0.0090 &  0.0135 & \dots &  0.0315 \\
-0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & \dots & -0.0675 \\
 0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 & \dots &  0.0675
\end{bmatrix}
$$

$$
\text{Probabilities} = \begin{bmatrix}
 0.0854 &  0.0850 &  0.0846 &  0.0843 &  0.0839 &  0.0835 &  0.0831 &  0.0828 & \dots &  0.0813 \\
 0.0813 &  0.0817 &  0.0820 &  0.0824 &  0.0828 &  0.0831 &  0.0835 &  0.0839 & \dots &  0.0854 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833
\end{bmatrix}
$$

The final row of the probability matrix corresponds to the predictions following the word "up". The ultimate objective is for the network to predict the word "late" as the next logical token. However, every single value in that final row is exactly 0.0833. In a vocabulary of twelve words, a completely uniform distribution yields a probability of exactly one divided by twelve for each word. The model is expressing maximum uncertainty, considering every possible word in the vocabulary to be equally likely. This result confirms that the initialized projection matrices act as an empty vessel. The network possesses the structural capacity to route information but lacks specific geometric knowledge.

When generating actual text, the network relies on sampling from this final probability distribution. A naive approach would always select the single highest probability value, a strategy known as greedy decoding. Relying exclusively on greedy decoding traps models in repetitive loops and eliminates the natural variance of language. Introducing controlled stochasticity requires manipulating the shape of the probability distribution before sampling occurs.

The standard technique for modulating this distribution is temperature scaling. Before applying the softmax function, each value in the logits matrix is divided by a scalar parameter termed temperature.

$$
\text{Scaled Logit} = \frac{\text{Logit}}{\text{Temperature}}
$$

Setting the temperature value below one increases the absolute magnitude of the logits. This operation geometrically stretches the distances between the values, causing the subsequent softmax operation to assign overwhelmingly high probability mass to the maximum logit. A low temperature setting forces the network toward highly deterministic outputs. Conversely, a temperature setting greater than one compresses the absolute magnitude of the logits. This shrinks the relative differences between the scores, resulting in a flatter probability distribution after the softmax step. A higher temperature injects entropy, assigning non-trivial probabilities to sub-optimal tokens and increasing generation diversity.

Modern implementations further constrain this sampling process by applying techniques like Top-K decoding. This strategy truncates the probability distribution by zeroing out all values except the top candidates, preventing the selection of statistically impossible continuations while preserving the localized entropy of temperature scaling.

To make the network predict "late" consistently without relying on artificial sampling constraints, the underlying logit for the correct token must naturally dominate the distribution. Achieving this requires a mechanism to measure how wrong the current uniform prediction is and a method to systematically adjust every single matrix weight to improve it.
