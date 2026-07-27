# Part 18: Final Softmax and Predictions
<!-- SUMMARY: Unbounded vocabulary logits are compressed into a strict, positive probability distribution that sums to one using the final softmax function. This transformation reveals the untrained network's maximum uncertainty, setting the foundation for the backpropagation phase. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

In the previous step, we projected our highly contextualized vectors out of the latent model space and back into the vocabulary space. This operation yielded our logits, which are raw, unbounded scores assigning a numerical value to each of the 12 possible words in our vocabulary. While logits indicate the model's geometric preference for certain words, they are not interpretable as a true probability distribution. We require a mechanism to compress these unbounded scores into a strict, positive range that sums to exactly one. The Softmax function provides this precise mathematical transformation.

## The Mechanics of Softmax

The Softmax function operates on a vector of numbers, performing two critical operations simultaneously. First, it exponentiates every value in the vector. Exponentiation serves a dual purpose: it forces all negative scores to become strictly positive fractions, and it non-linearly amplifies the differences between scores. A slightly higher logit becomes a significantly higher exponentiated value, creating a winner-take-all dynamic that helps the model confidently select a single token.

Second, the function sums all the newly exponentiated values and divides each individual value by this total sum. This normalization step guarantees that the final output vector constitutes a valid probability distribution, where all elements are positive and their collective sum is precisely 1.0. 

Mathematically, for a given logit vector $z$, the probability of the $i$-th element is defined as:

$$
P(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}
$$

## Transforming the Logits

We can now apply this function to the logits we calculated at the end of Layer 2. As a reminder, our $4 \times 12$ logit matrix represents the predictions at each of our four sequence positions across our 12-token vocabulary. The sequence positions correspond to the tokens `<BOS>`, `i`, `woke`, and `up`.

$$
\text{Logits} = \begin{bmatrix}
-0.0270 & -0.0315 & -0.0360 & -0.0405 & -0.0450 & -0.0495 & -0.0540 & -0.0585 & \dots & -0.0765 \\
-0.0180 & -0.0135 & -0.0090 & -0.0045 &  0.0000 &  0.0045 &  0.0090 &  0.0135 & \dots &  0.0315 \\
-0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & \dots & -0.0675 \\
 0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 & \dots &  0.0675
\end{bmatrix}
$$

By applying the Softmax function to each row independently, we convert these raw scores into our final probability distribution.

$$
\text{Probabilities} = \begin{bmatrix}
 0.0854 &  0.0850 &  0.0846 &  0.0843 &  0.0839 &  0.0835 &  0.0831 &  0.0828 & \dots &  0.0813 \\
 0.0813 &  0.0817 &  0.0820 &  0.0824 &  0.0828 &  0.0831 &  0.0835 &  0.0839 & \dots &  0.0854 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833
\end{bmatrix}
$$

## The Untrained State

Observe the final row of our probability matrix. This row corresponds to the final token in our sequence, the word "up". Our ultimate goal for this entire Transformer architecture is to predict the word "late" as the next logical token. 

If we look at the probabilities in that fourth row, every single value is exactly $0.0833$. In a vocabulary of 12 words, a completely uniform distribution yields a probability of exactly one divided by twelve for each word, which equals $0.0833$. The model is expressing maximum uncertainty. It considers every possible word in the vocabulary to be equally likely to follow our input phrase.

This result is entirely expected. The matrices we have used throughout this series, from the initial embeddings to the Q, K, and V projections, were arbitrarily defined for our toy example. The network possesses the structural capacity to route information, contextualize words, and generate predictions, yet it lacks the specific geometric knowledge required to understand language. It is an empty vessel.

To make the network predict "late", we need the probability at index 8 of the final row to approach a value of $1.0$, while all other probabilities approach $0.0$. Achieving this requires a mechanism to measure how wrong the current uniform prediction is and a method to systematically adjust every single matrix weight in the network to improve that prediction. 

This brings us to the final and most mathematically profound phase of neural network architecture, which is Backpropagation.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
