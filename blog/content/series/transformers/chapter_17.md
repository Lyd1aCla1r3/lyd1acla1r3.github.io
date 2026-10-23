# Part 17: Mapping Back to Words

<!-- SUMMARY: The contextualized mathematical representations emerging from the second layer are translated back into the vocabulary space using the unembedding matrix. This linear projection produces raw logits that quantify the geometric preference for predicting the next sequence token. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

The network has completed its two-layer contextual processing stack. The geometric coordinates emerging from Layer 2 encode contextualized representations of syntax and semantics across the four input positions. Each row captures how a token relates to the preceding sequence, yet these vectors still reside in the continuous six-dimensional model subspace ($d_{\text{model}} = 6$). Generating text requires projecting these continuous 6-dimensional vectors back into the discrete 12-dimensional vocabulary space ($V = 12$). This output projection bridges the hidden representation space of the model and the discrete tokens of the vocabulary.

## The Unembedding Matrix

Throughout the forward pass, each token position has been represented by a vector of length $d_{\text{model}} = 6$. Predicting the next token in the sequence requires assigning a scalar score to every candidate word in the $V = 12$ vocabulary.

The unembedding matrix, denoted as $W_U$, forms the linear bridge between these two spaces. It operates as a classification projection matrix of shape $d_{\text{model}} \times V = 6 \times 12$, aligning with the model dimension along its rows and the vocabulary size along its columns. Geometrically, each of the 12 columns in $W_U$ represents the target direction of a specific vocabulary token in $\mathbb{R}^6$.

Across Transformer architectures, $W_U$ is parameterized in one of two ways:

- **Untied Unembedding Weights:** Learns an independent $d_{\text{model}} \times V$ matrix during training, decoupling the output classification geometry from the input lookup table.
- **Weight Tying ($W_U = W_E^T$):** Reuses the transpose of the $V \times d_{\text{model}}$ input embedding matrix $W_E$, enforcing that tokens with similar input representations also share similar output logit projections while reducing parameter count.

For the toy walkthrough, the network uses an explicit $6 \times 12$ unembedding matrix following the linear ramp $W_U[r, c] = 0.01 \times (r + c)$ for row $r \in \{0, \dots, 5\}$ and column $c \in \{0, \dots, 11\}$:

$$
W_U = \begin{bmatrix}
   0.00 & 0.01 & 0.02 & 0.03 & 0.04 & 0.05 & 0.06 & 0.07 & 0.08 & \dots & 0.11 \\
   0.01 & 0.02 & 0.03 & 0.04 & 0.05 & 0.06 & 0.07 & 0.08 & 0.09 & \dots & 0.12 \\
   0.02 & 0.03 & 0.04 & 0.05 & 0.06 & 0.07 & 0.08 & 0.09 & 0.10 & \dots & 0.13 \\
   0.03 & 0.04 & 0.05 & 0.06 & 0.07 & 0.08 & 0.09 & 0.10 & 0.11 & \dots & 0.14 \\
   0.04 & 0.05 & 0.06 & 0.07 & 0.08 & 0.09 & 0.10 & 0.11 & 0.12 & \dots & 0.15 \\
   0.05 & 0.06 & 0.07 & 0.08 & 0.09 & 0.10 & 0.11 & 0.12 & 0.13 & \dots & 0.16
\end{bmatrix}
$$

## Calculating the Logits

The network computes the matrix product between the final Layer 2 output matrix $X_{\text{final}}$ and the unembedding matrix $W_U$. Each inner product measures the geometric alignment between a token's final 6-dimensional hidden state and the column vector of a candidate vocabulary word. A large positive inner product indicates strong alignment with that candidate word, whereas a negative value indicates opposition. The resulting $4 \times 12$ matrix stores these unnormalized alignment scores, known as logits.

With $X_{\text{final}}$ of shape $4 \times 6$ (representing the four prompt positions `<BOS>`, `i`, `woke`, and `up`) and $W_U$ of shape $6 \times 12$, the logit projection is:

$$
\text{Logits} = X_{\text{final}} W_U
$$

Multiplying the $4 \times 6$ matrix $X_{\text{final}}$ from Part 16 by the $6 \times 12$ unembedding matrix $W_U$ produces a $4 \times 12$ matrix of raw vocabulary scores (shown below rounded to two decimal places; Part 18 retains the four-decimal values from $-0.0270$ to $0.0765$ so the Softmax exponentiation captures the column slopes in Rows 1 and 2):

$$
\text{Logits} = \begin{bmatrix}
  -0.03 & -0.03 & -0.04 & -0.04 & -0.05 & -0.05 & -0.05 & -0.06 & -0.06 & \dots & -0.08 \\
   0.03 &  0.03 &  0.04 &  0.04 &  0.05 &  0.05 &  0.05 &  0.06 &  0.06 & \dots &  0.08 \\
  -0.07 & -0.07 & -0.07 & -0.07 & -0.07 & -0.07 & -0.07 & -0.07 & -0.07 & \dots & -0.07 \\
   0.07 &  0.07 &  0.07 &  0.07 &  0.07 &  0.07 &  0.07 &  0.07 &  0.07 & \dots &  0.07
\end{bmatrix}
$$

Each row in the `Logits` matrix corresponds to one of the four sequence positions (`<BOS>`, `i`, `woke`, and `up`), and the twelve columns store the unnormalized alignment scores across the twelve vocabulary tokens. The toy weights have not yet been updated by gradient descent, so these scores reflect an untrained initialization.

Examining the final sequence position (`up`, Row 4) illustrates how trained vs. untrained logits behave. Given the prompt `<BOS>` `i` `woke` `up`, the target continuation is `late`, located at vocabulary index `8` (the ninth column). In an untrained state, Row 4 assigns a flat score of $0.07$ ($0.0675$) across all twelve columns. Converged training causes Row 4 of the logit matrix to peak sharply at index `8`:

$$
\text{Logits}_{\text{up (trained)}} = \begin{bmatrix}
-0.12 & 0.45 & -1.23 & 0.05 & 0.88 & -0.34 & -0.77 & 1.02 & 3.45 & \dots & -0.11
\end{bmatrix}
$$

In that trained vector, the score at index `8` (`3.45`) dominates every competing vocabulary entry, indicating that the hidden state of `up` aligns closely with the unembedding column for `late`.

## The Need for Probabilities

Raw logits rank the candidate vocabulary tokens, yet they remain unbounded real numbers that can take arbitrary positive or negative magnitudes and do not sum to $1.0$. This lack of normalization complicates both confidence interpretation and loss calculation during backpropagation; a raw score of $3.45$ in isolation does not indicate whether the model assigns $95\%$ or $55\%$ probability to `late`.

Converting these algebraic magnitudes into interpretable probabilities requires a final row-wise normalization step. In Part 18, the Softmax function maps each logit row onto the probability simplex, where all twelve entries are strictly positive and sum to $1.0$.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
