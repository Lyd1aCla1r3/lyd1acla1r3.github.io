# Part 3: The Forward Pass, Softmax, and Cross-Entropy Loss

<!-- SUMMARY: Understanding how vector embeddings are learned requires examining the shallow neural network designed to train them. A step-by-step concrete mathematical example demonstrates how a two-layer architecture extracts a dense vector, projects it into raw logits, and uses Softmax and Cross-Entropy Loss to quantify the network's error against the ground truth. The fundamental limitations of static embeddings are also explored, setting the stage for Transformers. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

Transforming a randomly initialized embedding matrix ($W_E$) into a structured semantic space requires an objective function that evaluates vector positions on every training step. A shallow neural network constructed around $W_E$ provides this evaluation mechanism through **Next-Token Prediction**: observing a context token and predicting the most probable subsequent token in the corpus.

## The Proxy of Prediction

The choice of next-token prediction requires justification. The training objective aims to capture semantic relationships across words, yet no supervised database of hand-labeled semantic attributes (such as `is_animal = 1.0`) exists to guide the updates.

The architecture relies instead on **Distributional Semantics**, formulated by linguist J.R. Firth as the principle that a word is characterized by the company it keeps. Observing that the nouns `fox`, `wolf`, and `dog` frequently precede the same verbs (`hunts`, `sleeps`, `runs`) forces gradient descent to push their embedding vectors toward the same region of the coordinate space. Semantic structure is never programmed directly; it emerges as a geometric byproduct of optimizing the next-token prediction objective.

## The 2-Layer Embedding Network

Static embedding models train through a shallow neural network comprising two linear projection layers:

1. **Layer 1 (`W_E`, The Embedding Projection):** Multiplies the one-hot encoded input vector $\mathbf{x} \in \{0, 1\}^{1 \times V}$ (representing the current context token) by $W_E \in \mathbb{R}^{V \times d_{\text{model}}}$ to extract a dense, continuous hidden vector $\mathbf{h} \in \mathbb{R}^{1 \times d_{\text{model}}}$.
2. **Layer 2 (`W_U`, The Un-embedding Projection):** Multiplies the dense hidden vector $\mathbf{h}$ by a second learnable weight matrix $W_U \in \mathbb{R}^{d_{\text{model}} \times V}$ to project the representation back into the $V$-dimensional vocabulary space, producing an unnormalized score (logit) for every candidate next token.

### The Hidden Layer

The **hidden layer** of this network consists of the intermediate state $\mathbf{h} \in \mathbb{R}^{1 \times d_{\text{model}}}$ between the two projections. The training loop exists solely to optimize the rows of Layer 1 ($W_E$). Completing the training run allows the system to discard Layer 2 ($W_U$) and export the rows of $W_E$ as the static token embeddings.

### The Activation Function

The architecture omits non-linear activation functions (such as ReLU or GELU) between Layer 1 and Layer 2.

That omission distinguishes a static Embedding Network from the Feed-Forward Networks (FFNs) inside a Transformer. A Transformer applies non-linear activations to model complex feature interactions, whereas an Embedding Network preserves a pure linear projection so that directional and additive relationships (such as cosine similarity and vector offsets) remain linear across the coordinate space.

Stacking two linear matrices ($W_E$ and $W_U$) without an intervening non-linearity allows their product to collapse algebraically into a single matrix ($W_E \times W_U = W_{\text{combined}} \in \mathbb{R}^{V \times V}$). The architecture maintains $W_E$ and $W_U$ as separate factors so that the $d_{\text{model}}$-dimensional bottleneck state $\mathbf{h}$ can be intercepted between them as the compressed token embedding.

## A Toy Mathematical Walkthrough

The 8-word toy configuration demonstrates the complete forward pass through explicit numerical calculation:

- **Vocabulary ($V = 8$):** `The` (`0`), `quick` (`1`), `brown` (`2`), `fox` (`3`), `jumps` (`4`), `over` (`5`), `lazy` (`6`), `dog` (`7`).
- **Embedding Dimension ($d_{\text{model}} = 3$):** Three continuous coordinates per token.

The input sequence is `The` `quick` `brown`, and the prediction target is the subsequent token `fox` (index `3`).

*(Note: Reaching the end of a sentence sets the prediction target to a dedicated End-of-Sequence `<EOS>` control token. The vocabulary allocates a standard row in $W_E$ for `<EOS>`, learning its geometric coordinates by observing sentence-termination patterns across the corpus.)*

### Step 1: The Input

The active context token, `brown` (vocabulary index `2`), is encoded as a $1 \times 8$ one-hot row vector $\mathbf{x}$:

$$
\mathbf{x} = \begin{bmatrix} 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}_{1 \times 8}
$$

### Step 2: Layer 1 (The Embedding Lookup)

The forward pass multiplies the one-hot input vector $\mathbf{x}$ by the randomly initialized $8 \times 3$ embedding matrix $W_E$:

$$
W_E = \begin{bmatrix}
0.1 & -0.4 & 0.2 \\
0.5 & 0.1 & -0.8 \\
\mathbf{-0.3} & \mathbf{0.9} & \mathbf{0.4} \\
0.2 & -0.2 & 0.1 \\
\vdots & \vdots & \vdots
\end{bmatrix}_{8 \times 3}
$$

Zero entries at every position of $\mathbf{x}$ except index `2` cause the vector-matrix product $\mathbf{h} = \mathbf{x} \times W_E$ to isolate row `2`:

$$
\mathbf{h} = \begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}_{1 \times 3}
$$

This 3-dimensional row vector $\mathbf{h}$ forms the **hidden layer** state, representing the current untrained embedding for `brown`.

### Step 3: Layer 2 (The Un-embedding Projection)

The second layer projects the hidden state $\mathbf{h} \in \mathbb{R}^{1 \times 3}$ back into the 8-word vocabulary space via the un-embedding matrix $W_U \in \mathbb{R}^{3 \times 8}$:

$$
\mathbf{z} = \mathbf{h} \times W_U
$$

Evaluating this product against the current weights of $W_U$ yields the $1 \times 8$ logit vector $\mathbf{z}$:

$$
\mathbf{z} = \begin{bmatrix} 1.2 & -0.5 & 0.3 & 2.1 & -1.8 & 0.7 & 0.0 & 0.4 \end{bmatrix}_{1 \times 8}
$$

The vector $\mathbf{z}$ contains the raw **logits** ($z_0$ through $z_7$), which are unbounded real-valued scores measuring how strongly the network favors each vocabulary word as the next token.

### Step 4: The Softmax Function

Evaluating prediction accuracy requires converting the unbounded logits $\mathbf{z}$ into a valid probability distribution $\hat{\mathbf{y}}$ whose components are strictly positive and sum to $1.0$. The **Softmax** function performs this normalization across the 0-indexed vocabulary ($j \in \{0, \dots, V-1\}$):

$$
\hat{y}_i = \frac{e^{z_i}}{\sum_{j=0}^{V-1} e^{z_j}}
$$

Here $\hat{y}_i$ denotes the predicted probability assigned to token $i$, $z_i$ denotes that token's logit, $e \approx 2.718$ is the base of the natural exponential function, and the denominator sums the exponentiated logits $e^{z_j}$ across all $V = 8$ tokens in the vocabulary.

Computing the Softmax probability for the target token `fox` (index `3`, where $z_3 = 2.1$) proceeds in three steps:

1. **Exponentiate the target logit $z_3$:**
$$ e^{2.1} \approx 8.16 $$
2. **Exponentiate all eight logits and sum the results across the vocabulary:**
$$
\begin{aligned}
\sum_{j=0}^{7} e^{z_j} &= e^{1.2} + e^{-0.5} + e^{0.3} + e^{2.1} + e^{-1.8} + e^{0.7} + e^{0.0} + e^{0.4} \\
&\approx 3.32 + 0.60 + 1.35 + 8.16 + 0.16 + 2.01 + 1.0 + 1.49 = 18.09
\end{aligned}
$$
3. **Divide the target exponential by the normalization sum:**
$$ \hat{y}_3 = \frac{8.16}{18.09} \approx 0.45 $$

The network assigns a $45\%$ probability ($\hat{y}_3 = 0.45$) to `fox` appearing as the next word. Evaluating this ratio across all eight indices produces the full predicted probability vector $\hat{\mathbf{y}} \in \mathbb{R}^{1 \times 8}$.

### Step 5: The Cross-Entropy Loss

Random weight initialization means this $45\%$ prediction reflects untrained parameter values rather than learned linguistic structure. Driving gradient updates requires a scalar objective function that quantifies the divergence between the predicted distribution $\hat{\mathbf{y}}$ and the ground-truth distribution $\mathbf{y}$.

The ground-truth label $\mathbf{y} \in \{0, 1\}^{1 \times 8}$ specifies that `fox` (index `3`) is the observed next token, forming a one-hot vector with $y_3 = 1.0$ and $y_i = 0$ at every other index.

**Cross-Entropy Loss** measures the divergence between the predicted distribution $\hat{\mathbf{y}}$ and the target distribution $\mathbf{y}$ using two foundational constructs from information theory:

1. **The Natural Logarithm as Surprise ($\log(\hat{y}_i)$):** Applying the natural logarithm (base $e$) to a predicted probability $\hat{y}_i \in (0, 1]$ maps a raw probability into a continuous measure of surprisal. Assigning a $99\%$ probability to the observed token yields near-zero surprise ($\log(0.99) \approx -0.01$), whereas assigning a $1\%$ probability produces a steep penalty ($\log(0.01) \approx -4.61$).
2. **The Weighted Summation as Expected Value:** Multiplying each token's true probability $y_i$ by its log-probability $\log(\hat{y}_i)$ and negating the sum across all $V$ vocabulary entries computes the expected surprisal of the model under the ground-truth distribution:

$$
L = -\sum_{i=0}^{V-1} y_i \log(\hat{y}_i)
$$

Here $L$ denotes the scalar Cross-Entropy Loss, $y_i \in \{0, 1\}$ denotes the ground-truth probability for token $i$, and $\log(\hat{y}_i)$ denotes the natural logarithm of the model's predicted probability for token $i$.

The one-hot structure of the target distribution $\mathbf{y}$ simplifies this summation algebraically. Every incorrect vocabulary entry carries a ground-truth weight of $y_i = 0$, annihilating seven of the eight terms in the sum and leaving only the target index where $y_{\text{true}} = 1.0$.

Dropping the seven zeroed terms reduces the full summation to a single expression known as **Negative Log-Likelihood**:

$$
L = -\log(\hat{y}_{\text{true}})
$$

Each component of the Negative Log-Likelihood expression performs a distinct role:

- **Likelihood ($\hat{y}_{\text{true}}$):** Extracts the predicted probability assigned to the ground-truth token ($0.45$ for `fox`), which the training objective seeks to maximize toward $1.0$.
- **Natural Logarithm ($\log$):** Maps a probability on $(0, 1)$ to a negative real number ($\log(0.45) \approx -0.79$), penalizing low-confidence predictions non-linearly.
- **Negation ($-$):** Multiplies the negative log-probability by $-1$ to produce a positive loss scalar $L \ge 0$ that approaches $0$ as confidence approaches $1.0$.

Substituting the predicted probability $\hat{y}_3 = 0.45$ for `fox` yields the loss for this forward pass:

$$
L = -\log(0.45) \approx 0.79
$$

This scalar $L = 0.79$ quantifies the total prediction error of the forward pass, providing the starting point for the backward pass derived in Chapter 4.

## The Limit of Static Embeddings: Superposition

A structural limitation of a static embedding table is **polysemy**: a single word form carrying multiple distinct meanings.

The static lookup matrix $W_E$ allocates only one row vector for the token `apple`. Corpus contexts such as *"The orchard harvested a ripe apple"* pull that single row vector toward agricultural and fruit coordinates, whereas technology contexts such as *"Apple released a new laptop"* pull the same row vector toward consumer electronics coordinates.

Across billions of training updates, the single vector for `apple` converges to a state of **superposition**, resting at the frequency-weighted center of mass between its competing senses.

Resolving that contextual ambiguity motivates the **Self-Attention** mechanism in the [Transformer architecture](series-transformers.html). Self-Attention enables the static `apple` vector to attend to surrounding tokens in the active sequence and dynamically shift its representation toward either the fruit subspace or the technology subspace before the final prediction layer.

Before examining sequence-level contextualization in Chapter 7, Chapters 4 and 5 derive the backpropagation equations that physically adjust the weights of $W_U$ and $W_E$ via gradient descent.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
