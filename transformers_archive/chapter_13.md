# Part 13: Layer 2 Self-Attention
<!-- SUMMARY: As the sequence progresses through the second layer of self-attention, token vectors evolve from isolated definitions into deeply contextualized mathematical representations. These advanced abstractions are projected into query, key, and value subspaces to evaluate high-level syntactic structures. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

In the first layer of our Transformer, the self-attention mechanism evaluated relationships between raw, isolated word embeddings. When we projected the tokens for "woke" and "up" into their respective Query and Key spaces, we measured their static semantic affinity. We have since routed those localized insights back into the central residual stream, refined them through a Key-Value Multi-Layer Perceptron, and stabilized the geometry with Layer Normalization. As we begin the second layer of self-attention, our token vectors no longer represent solitary dictionary definitions. They are now deeply contextualized mathematical summaries of their surrounding linguistic environment.

## The Contextualized Input

The input to Layer 2, which we will denote as $X_2$, is the normalized output of our first layer. The vectors occupying this matrix are profoundly different from the initial token embeddings. The first row still corresponds to the `<BOS>` token, the second to "i", the third to "woke", and the fourth to "up". Their numerical values now encode the structural and semantic relationships discovered during Layer 1. 

$$
X_2 = \begin{bmatrix}
-2.00 & 1.22 & 0.50 & 0.19 & -0.28 & 0.37 \\
-1.91 & 1.28 & 0.52 & -0.49 & 0.21 & 0.39 \\
0.04 & -1.55 & 0.18 & -0.82 & 0.52 & 1.62 \\
0.20 & -1.72 & 0.01 & -0.55 & 0.49 & 1.57
\end{bmatrix}
$$

When Layer 2 computes self-attention, it is not merely asking if "woke" is related to "up". It is evaluating whether the complex concept of a sequence beginning with a first-person pronoun performing a waking action should attend to the temporal concept of the word "up". The attention mechanism is now operating on abstractions.

## The Second Layer Projections

Just as we did in Layer 1, we must project these high-dimensional 6-element vectors into lower-dimensional 2-element subspaces to compute attention. We initialize a new set of weight matrices for Head 1 of Layer 2. These matrices, $W_Q^{(2)}$, $W_K^{(2)}$, and $W_V^{(2)}$, serve the exact same geometric function as their Layer 1 counterparts. They define a bilinear form, allowing disparate semantic vectors to align in a shared subspace.

$$
W_Q^{(2)} = \begin{bmatrix}
0.10 & -0.20 \\
-0.30 & 0.40 \\
0.50 & -0.10 \\
-0.20 & 0.30 \\
0.40 & 0.20 \\
-0.10 & -0.50
\end{bmatrix}
$$

$$
W_K^{(2)} = \begin{bmatrix}
-0.20 & 0.30 \\
0.40 & -0.10 \\
-0.30 & 0.50 \\
0.10 & -0.40 \\
0.20 & 0.20 \\
-0.50 & 0.10
\end{bmatrix}
$$

$$
W_V^{(2)} = \begin{bmatrix}
0.30 & -0.10 \\
-0.20 & 0.40 \\
0.10 & -0.30 \\
-0.40 & 0.20 \\
0.50 & -0.20 \\
-0.10 & 0.50
\end{bmatrix}
$$

We calculate the Queries $Q_2$, Keys $K_2$, and Values $V_2$ by taking the dot product of our contextualized input $X_2$ with each of these respective weight matrices. 

### The Query Space

The $Q_2$ matrix represents what each contextualized token is searching for in the sequence.

$$
Q_2 = X_2 W_Q^{(2)} = \begin{bmatrix}
-0.50 & 0.66 \\
-0.17 & 0.54 \\
0.77 & -1.60 \\
0.69 & -1.58
\end{bmatrix}
$$

### The Key Space

The $K_2$ matrix represents the features each contextualized token is advertising to the sequence. 

$$
K_2 = X_2 W_K^{(2)} = \begin{bmatrix}
0.52 & -0.57 \\
0.53 & -0.16 \\
-1.47 & 0.85 \\
-1.47 & 0.71
\end{bmatrix}
$$

### The Value Space

The $V_2$ matrix represents the actual information each token will contribute to the next stage of processing if another token attends to it. 

$$
V_2 = X_2 W_V^{(2)} = \begin{bmatrix}
-1.05 & 0.82 \\
-0.51 & 0.60 \\
0.77 & -0.13 \\
0.71 & -0.13
\end{bmatrix}
$$

## A Shift in Abstraction

The mathematics remain identical to the first layer. We project an input tensor through three linear transformations to prepare for a scaled dot-product attention calculation. The fundamental shift is entirely in the contents of $X_2$. The Queries and Keys in this layer are no longer matching basic vocabulary traits. They are matching high-level syntactic structures and multi-token semantic combinations. In our next installment, we will calculate the attention scores for this second layer and observe how these deep contextual representations choose to share information.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
