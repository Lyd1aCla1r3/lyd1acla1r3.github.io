# The Mathematics of Parallel Training: Teacher Forcing vs. Inference

<!-- SUMMARY: A step-by-step mathematical walkthrough contrasting the parallel nature of Transformer training with the sequential bottleneck of inference. A concrete toy example traces the tensor algebra of causal masking and cross-entropy loss, which makes the mechanics of Teacher Forcing explicit without relying on abstraction. -->

A fundamental operational divergence exists between how large language models are trained and how they execute upon deployment. Training a model requires months of processing trillions of tokens, yet the deployed model generates a response in seconds. This discrepancy stems from how the two phases utilize the Transformer architecture. Training is massively parallelized across entire token sequences, whereas deployment, commonly referred to as inference, is strictly sequential.

During inference, a model generates text one token at a time. A model generating a paragraph cannot produce the third token without first generating the second. Training at modern parameter scales would be computationally intractable under that sequential dependency. Transformer training bypasses this bottleneck through a mathematical technique called Teacher Forcing.

A concrete numerical walkthrough makes this architectural divide explicit. Tracing the step-by-step matrix operations demonstrates how Teacher Forcing enables a neural network to process an entire token sequence simultaneously.

## The Auto-Regressive Bottleneck of Inference

Consider a scenario where the model must complete the three-token sequence `"i woke up"` with the goal of predicting the next token, `"late"`.

During inference, the model begins with the first token, `"i"`. It executes a full forward pass of matrix multiplications to predict the next token, `"woke"`. Next, it appends that predicted token to its running context, forming the two-token input `"i woke"`, and repeats the entire forward pass to predict `"up"`.

This serial dependency defines the auto-regressive bottleneck: predicting step three mathematically requires the output generated at step two, leaving no way to skip ahead during generation.

Assume the model uses an embedding dimension of $d_{\text{model}} = 4$, mapping every token to a four-element vector. The input tensor for the single token `"i"` at time step $t=1$ has a shape of $1 \times 1 \times 4$, representing a batch size of $1$, a sequence length of $1$, and an embedding dimension of $4$. The forward pass yields a single probability distribution predicting one next token.

## Bypassing the Bottleneck: Teacher Forcing

Training avoids this sequential trap because the complete ground-truth sequence `"i woke up late"` is already available in the training corpus, so the architecture does not need to wait for its own prior predictions before advancing to subsequent positions.

Instead, Teacher Forcing feeds the entire input sequence into the model simultaneously. The input tensor $X$ encapsulates all three starting tokens, `"i woke up"`, in a single batch. Its shape expands to $1 \times 3 \times 4$, representing one sequence, three tokens, and four embedding dimensions.

Presenting the entire sequence at once introduces a structural flaw: information leakage from future positions. Processing the sequence `"i woke up"` simultaneously allows an unmasked attention mechanism to let the token `"i"` attend to `"woke"` and `"up"` before predicting them. A model that observes future tokens during training circumvents the next-token learning objective entirely.

## The Solution: The Causal Mask

To prevent future tokens from leaking backward in time, the self-attention layer applies an upper-triangular additive matrix called a Causal Mask.

### Unmasked Attention Scores

The self-attention mechanism measures pairwise token affinities by computing an Attention Score matrix $S$. For the three-token sequence `"i"`, `"woke"`, `"up"`, scaled dot-product attention produces a $3 \times 3$ matrix of raw logits:

$$
S = \begin{bmatrix}
1.2 & 0.5 & 0.1 \\
0.4 & 1.5 & -0.2 \\
0.8 & -0.1 & 1.1
\end{bmatrix}
$$

The first row represents the attention scores that the query token `"i"` assigns to the key tokens `"i"`, `"woke"`, and `"up"`. Notice that `"i"` assigns a positive score of $0.5$ to `"woke"` and $0.1$ to `"up"`, meaning position $1$ is reading information from future positions $2$ and $3$.

### Upper-Triangular Masking

The attention layer adds the Causal Mask matrix $M$ to the raw scores $S$ before applying the Softmax function. This mask holds $0$ on and below the main diagonal and $-\infty$ strictly above the diagonal:

$$
M = \begin{bmatrix}
0 & -\infty & -\infty \\
0 & 0 & -\infty \\
0 & 0 & 0
\end{bmatrix}
$$

Adding $M$ to the raw score matrix $S$ converts every upper-triangular future entry into $-\infty$, because any finite real number added to $-\infty$ yields $-\infty$:

$$
S + M = \begin{bmatrix}
1.2 & -\infty & -\infty \\
0.4 & 1.5 & -\infty \\
0.8 & -0.1 & 1.1
\end{bmatrix}
$$

### Softmax Probability Normalization

The rationale for using negative infinity lies in the subsequent normalization step. The network passes each row of masked scores through the Softmax function, which applies the exponential function $e^x$ to convert raw logits into normalized probabilities between $0$ and $1$, where $e^{-\infty} = 0$:

$$
\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{L} e^{x_j}}
$$

Setting upper-triangular entries to $-\infty$ prior to exponentiation drives their Softmax outputs to $0$. Zeroing out those future positions restricts each row's probability mass exclusively to past and present tokens. Applying Softmax row by row transforms the masked logits into the attention probability matrix $P$, shown below rounded to two decimal places:

$$
P = \begin{bmatrix}
1.00 & 0.00 & 0.00 \\
0.25 & 0.75 & 0.00 \\
0.36 & 0.15 & 0.49
\end{bmatrix}
$$

In the top row, the token `"i"` assigns $100\%$ of its attention probability to itself and $0\%$ to the future tokens `"woke"` and `"up"`. The causal mask mathematically blinds each query position to subsequent tokens, restricting next-token predictions to past and present context.

## Shifted Targets and Parallel Loss

With the causal mask enforced, a single forward pass generates three causal predictions in parallel, producing a $3 \times V$ matrix of vocabulary logits across all three sequence positions simultaneously.

### Position-Shifted Target Alignment

Evaluating prediction accuracy across all three positions requires comparing the output probabilities against a target sequence shifted left by one token position (`["woke", "up", "late"]` for the input `["i", "woke", "up"]`):

| Position | Input Token | Unmasked Context | Shifted Target |
| :--- | :--- | :--- | :--- |
| Step 1 | `"i"` | `"i"` | `"woke"` |
| Step 2 | `"woke"` | `"i woke"` | `"up"` |
| Step 3 | `"up"` | `"i woke up"` | `"late"` |

### Parallel Cross-Entropy Loss

The training objective computes Cross-Entropy Loss across all three positions simultaneously:

$$
\mathcal{L} = - \frac{1}{L} \sum_{t=1}^{L} \sum_{v=1}^{V} y_{t,v} \log(\hat{y}_{t,v})
$$

Every variable in the Cross-Entropy Loss objective maps directly to a dimension of the forward-pass tensors:

*   **Sequence Length ($L$):** Specifies the total number of token positions evaluated in parallel, which equals $3$ in this toy sequence.
*   **Time Step Index ($t$):** Indexes the sequence position from $t = 1$ to $t = 3$.
*   **Vocabulary Size ($V$):** Defines the total number of unique tokens in the model vocabulary.
*   **Vocabulary Index ($v$):** Iterates across every candidate token index $v \in \{1, \dots, V\}$ in the vocabulary.
*   **Ground-Truth Target ($y_{t,v}$):** Encodes the true target at position $t$ as a binary one-hot indicator that equals $1$ for the ground-truth next token and $0$ for all other $V - 1$ vocabulary entries.
*   **Predicted Probability ($\hat{y}_{t,v}$):** Denotes the model's Softmax probability assigned at position $t$ to vocabulary token $v$, such as $0.12$.

Multiplying the binary target indicator $y_{t,v}$ by the natural logarithm of the predicted probability $\hat{y}_{t,v}$ at every time step $t$ and vocabulary index $v$ extracts the negative log-likelihood of the true target token at each position. Averaging this loss across all $L$ positions produces a single scalar objective $\mathcal{L}$. A single backward pass then computes gradients for all three sequence positions simultaneously, updating the model weights from three distinct context windows in one optimization step.

## Conclusion

This parallel formulation is the core computational mechanism of Teacher Forcing. Packing the full token sequence into a single input tensor, shifting the ground-truth target labels by one position, and applying an upper-triangular $-\infty$ causal mask converts $L$ sequential forward passes into one parallelized matrix multiplication pipeline. That linear algebra structure makes pre-training Transformer models on trillions of tokens computationally tractable, even though deployment inference remains bound by the sequential auto-regressive bottleneck.
