# Part 13: The MLP Activation and Layer 2 Self-Attention

<!-- SUMMARY: The activation function serves as the critical gatekeeper within the feed-forward network, filtering the conceptual matches identified by the first layer. The subsequent linear projection then translates these activated patterns into concrete conceptual updates, writing new features back into the residual stream. As the sequence progresses through the second layer of self-attention, token vectors evolve from isolated definitions into deeply contextualized mathematical representations that evaluate high-level syntactic structures. -->

The projection matrix from the previous step expanded the residual stream into a twenty-four-dimensional space, effectively querying a vast bank of conceptual keys. The resulting matrix contained a spectrum of positive and negative values, representing the degree of resonance with each learned pattern. The network must now definitively decide which of these patterns are relevant to the current context and discard the rest. This critical filtering operation is the domain of the activation function.

The toy model employs the Rectified Linear Unit, commonly known as ReLU. The mathematical operation is elegantly simple: any negative value is set to zero, while positive values remain unchanged. Mechanistically, this acts as a strict threshold. If a token vector did not sufficiently match a specific conceptual key, the negative resonance is silenced entirely. The neuron simply does not fire. 

Applying this non-linearity to the projected state yields the activated memory representation.

$$
\text{Activated State} = \begin{bmatrix}
 0.58 &  0.00 &  0.00 &  0.00 &  0.56 &  0.00 &  1.03 &  0.71 &  0.00 & \dots &  0.00 \\
 1.01 &  0.00 &  0.00 &  0.00 &  1.50 &  0.00 &  2.30 &  0.00 &  0.00 & \dots &  1.88 \\
 0.00 &  0.00 &  0.00 &  0.29 &  0.00 &  2.81 &  0.00 &  1.72 &  3.20 & \dots &  1.24 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.03 &  2.34 &  0.00 &  0.74 &  2.29 & \dots &  1.68
\end{bmatrix}
$$

The landscape is now sparse. Only the most confident conceptual matches survive. The zeroed entries represent features deemed irrelevant to the token in its specific context, preventing noisy or contradictory signals from propagating further. 

With the precise combination of keys identified, the network moves to the extraction phase. The second half of the Multilayer Perceptron is defined by the $W_2$ weight matrix, which projects the twenty-four-dimensional space back down to the model dimension of six. Continuing the mechanistic analogy, if $W_1$ represented the "Keys" searching for patterns, $W_2$ represents the "Values" corresponding to those patterns.

$$
W_2 = \begin{bmatrix}
 0.75 &  0.19 &  0.34 &  0.44 & -0.42 & -0.78 \\
 -0.56 &  0.17 &  0.53 &  0.06 & -0.68 &  0.70 \\
 -0.80 & -0.24 & -0.28 &  0.13 &  0.55 & -0.75 \\
 -0.16 &  0.16 & -0.58 & -0.05 &  0.09 & -0.67 \\
 -0.65 & -0.03 & -0.11 &  0.11 &  1.11 &  0.45 \\
  0.22 & -0.36 &  0.47 & -0.39 &  0.78 &  0.59 \\
 -1.00 & -0.59 & -0.10 & -0.20 & -0.63 & -0.61 \\
  0.36 & -0.27 & -0.76 & -0.14 &  0.48 &  0.84 \\
  0.03 & -0.16 & -0.40 & -0.26 &  0.27 &  0.63 \\
  0.62 & -0.12 &  0.44 &  0.38 &  0.23 & -1.23 \\
 -0.03 & -0.14 &  0.66 & -0.14 &  0.23 &  0.13 \\
  0.63 &  0.38 &  0.51 &  0.75 &  0.48 &  0.39 \\
 -0.13 &  0.05 &  1.08 &  0.02 &  0.25 & -0.04 \\
 -0.15 & -1.50 &  0.86 & -0.59 & -0.42 &  0.68 \\
 -1.18 &  0.01 & -0.28 & -0.92 &  0.31 & -0.39 \\
 -0.05 & -0.21 &  0.32 &  1.13 & -0.63 &  0.43 \\
 -0.35 & -0.18 & -0.95 & -0.57 & -0.22 &  0.41 \\
  0.12 &  0.29 &  0.37 & -0.69 &  0.73 & -0.16 \\
  0.34 & -0.09 &  0.13 &  0.32 & -1.13 &  1.01 \\
  0.09 &  0.55 &  0.11 &  0.04 & -0.66 & -0.20 \\
 -1.11 & -0.08 &  0.79 & -0.94 & -0.34 & -0.19 \\
  0.58 &  0.62 &  0.03 &  0.05 & -0.08 & -0.24 \\
 -0.24 & -0.23 & -0.08 &  0.04 & -0.32 &  0.31 \\
 -0.02 &  0.27 & -0.68 & -0.35 &  0.05 &  0.14
\end{bmatrix}
$$

When a specific neuron fires in the activation phase, it triggers the retrieval of the corresponding row in $W_2$. The mathematical operation is a weighted sum. The strength of the activation dictates how forcefully that specific Value vector is added to the final output. The resulting contracted matrix represents the consolidated conceptual insights ready to be injected back into the residual stream.

$$
\text{Contracted Output} = \begin{bmatrix}
 -4.07 &  0.04 & -0.06 & -1.74 & -1.17 & -0.77 \\
 -6.51 &  0.18 & -0.33 & -3.85 & -0.84 & -1.43 \\
  0.82 & -3.22 &  0.39 & -2.11 &  3.22 &  6.02 \\
  1.18 & -2.83 & -0.72 & -1.89 &  1.58 &  4.39
\end{bmatrix}
$$

While the foundational architecture utilizes the straightforward ReLU function, modern state-of-the-art architectures frequently employ advanced gated activations like SwiGLU. Understanding the mechanics of SwiGLU requires a slight shift in the Key-Value analogy, elevating the filtering process to a highly nuanced operation.

Instead of a single projection matrix creating the expanded space, a SwiGLU architecture utilizes two parallel linear projections. The first projection acts as the standard feature vector, proposing the values that might be useful. The second projection acts exclusively as the gate, calculating how much of the first vector should actually be allowed through. This gating projection is passed through a smooth, non-linear function known as Swish, allowing the gate to regulate the information flow continuously.

The final activated state is the element-wise multiplication of the feature vector by the gate vector. Rather than a harsh threshold like ReLU, SwiGLU provides the network with a nuanced dial. It can selectively attenuate or amplify specific features based on complex contextual interactions. The feature projection might propose a concept, and the gate projection independently decides if that concept is truly relevant in the current context. This decoupling of feature generation and feature filtering grants the network immense expressive power, forming the backbone of highly capable contemporary models. 

Whether using a strict threshold or a nuanced gate, the fundamental operation remains the same. The Multilayer Perceptron evaluates the context-enriched tokens, selectively retrieves specialized conceptual knowledge, and prepares these refined updates for the final phase of the layer.

## Transition to Layer 2

In the first layer of the Transformer, the self-attention mechanism evaluated relationships between raw, isolated word embeddings. When the tokens for "woke" and "up" were projected into their respective Query and Key spaces, the mechanism measured their static semantic affinity. The network has since routed those localized insights back into the central residual stream, refined them through a Key-Value Multi-Layer Perceptron, and stabilized the geometry with Layer Normalization. As the second layer of self-attention begins, the token vectors no longer represent solitary dictionary definitions. They are now deeply contextualized mathematical summaries of their surrounding linguistic environment.

## The Contextualized Input

The input to Layer 2, denoted as $X_2$, is the normalized output of the first layer. The vectors occupying this matrix are profoundly different from the initial token embeddings. The first row still corresponds to the `<BOS>` token, the second to "i", the third to "woke", and the fourth to "up". Their numerical values now encode the structural and semantic relationships discovered during Layer 1. 

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

Just as in the first layer, the network must project these high-dimensional 6-element vectors into lower-dimensional 2-element subspaces to compute attention. A new set of weight matrices is initialized for the first head of Layer 2. These matrices, $W_Q^{(2)}$, $W_K^{(2)}$, and $W_V^{(2)}$, serve the exact same geometric function as their Layer 1 counterparts. They define a bilinear form, allowing disparate semantic vectors to align in a shared subspace.

$$
W_Q^{(2)} = \begin{bmatrix}
 0.10 & -0.20 \\
-0.30 &  0.40 \\
 0.50 & -0.10 \\
-0.20 &  0.30 \\
 0.40 &  0.20 \\
-0.10 & -0.50
\end{bmatrix}
$$

$$
W_K^{(2)} = \begin{bmatrix}
-0.20 &  0.30 \\
 0.40 & -0.10 \\
-0.30 &  0.50 \\
 0.10 & -0.40 \\
 0.20 &  0.20 \\
-0.50 &  0.10
\end{bmatrix}
$$

$$
W_V^{(2)} = \begin{bmatrix}
 0.30 & -0.10 \\
-0.20 &  0.40 \\
 0.10 & -0.30 \\
-0.40 &  0.20 \\
 0.50 & -0.20 \\
-0.10 &  0.50
\end{bmatrix}
$$

The Queries $Q_2$, Keys $K_2$, and Values $V_2$ are calculated by taking the dot product of the contextualized input $X_2$ with each of these respective weight matrices. 

### The Query Space

The $Q_2$ matrix represents what each contextualized token is searching for in the sequence.

$$
Q_2 = X_2 W_Q^{(2)} = \begin{bmatrix}
-0.50 &  0.66 \\
-0.17 &  0.54 \\
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
-1.47 &  0.85 \\
-1.47 &  0.71
\end{bmatrix}
$$

### The Value Space

The $V_2$ matrix represents the actual information each token will contribute to the next stage of processing if another token attends to it. 

$$
V_2 = X_2 W_V^{(2)} = \begin{bmatrix}
-1.05 &  0.82 \\
-0.51 &  0.60 \\
 0.77 & -0.13 \\
 0.71 & -0.13
\end{bmatrix}
$$

## A Shift in Abstraction

The mathematics remain identical to the first layer. An input tensor is projected through three linear transformations to prepare for a scaled dot-product attention calculation. The fundamental shift is entirely in the contents of $X_2$. The Queries and Keys in this layer are no longer matching basic vocabulary traits. They are matching high-level syntactic structures and multi-token semantic combinations. In the next step, the network calculates the attention scores for this second layer to reveal how these deep contextual representations share information.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
