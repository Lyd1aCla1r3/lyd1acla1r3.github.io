# Part 3: The Forward Pass, Softmax, and Cross-Entropy Loss

<!-- SUMMARY: Understanding how vector embeddings are learned requires examining the shallow neural network designed to train them. A step-by-step concrete mathematical example demonstrates how a two-layer architecture extracts a dense vector, projects it into raw logits, and uses Softmax and Cross-Entropy Loss to quantify the network's error against the ground truth. The fundamental limitations of static embeddings are also explored, setting the stage for Transformers. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

To transform a randomly initialized embedding matrix ($W_E$) into a mathematically rigorous semantic space, a mechanism must be built to evaluate its current state. This is achieved by constructing a simple neural network *around* $W_E$. Its sole objective is **Next-Token Prediction**: observing a sequence of tokens and predicting the most probable subsequent token in the corpus.

## The Proxy of Prediction

The choice of next-token prediction requires justification. The ultimate goal is to capture the semantic meaning of a word, but there is no database of "semantic features" (e.g., `is_animal` = `1.0`) to supervise the network. 

Instead, the system relies on **Distributional Semantics**, famously summarized by linguist J.R. Firth: *"You shall know a word by the company it keeps."* If the network observes that the words `fox`, `wolf`, and `dog` are all frequently followed by words like `hunts`, `sleeps`, or `runs`, the calculus of the network is mathematically forced to push their vectors closer together in the geometric space. Semantic meaning is not explicitly programmed; it is an *emergent byproduct* of the next-token prediction objective.

## The 2-Layer Embedding Network

When training static embeddings from scratch, the architecture is astonishingly simple. It is a shallow neural network consisting of exactly two layers:

1. **Layer 1: The Embedding Projection ($W_E$)**. The $W_E$ matrix *is* the first layer of the network. It projects the one-hot encoded vocabulary vector (which represents the current context word) into the dense, continuous vector space (dimension $d_{model}$) to extract its currently learned semantic meaning.
2. **Layer 2: The Un-embedding Projection ($W_U$)**. The $W_U$ matrix has a shape of $d_{model} \times V$. Just like $W_E$, its internal values are completely random at initialization and are learned during training. This layer projects the dense continuous vector (which now contains the contextual semantic features extracted by Layer 1) back out into the vocabulary space (dimension $V$), producing a raw score for every possible word in the vocabulary. This score represents the unnormalized likelihood that each specific word is the correct next token in the sequence.

### The Hidden Layer
In this architecture, the **hidden layer** is simply the state of the network between these two projections. It is the dense $d_{model}$-dimensional vector itself. The network's only true purpose is to optimize the weights of Layer 1 ($W_E$). Once training is complete, Layer 2 ($W_U$) is entirely discarded, and the hidden layer outputs (the vectors) are saved as the final embeddings.

### The Activation Function
Crucially, **there are no non-linear activation functions** (like ReLU or GELU) between Layer 1 and Layer 2. 

This is the fundamental architectural difference between an Embedding Network and the Feed-Forward Networks (FFN) found in Transformers. A Transformer uses non-linear activations to learn complex, non-linear logic. The Embedding Network intentionally omits them because its goal is to construct a pure, linear geometric space (where concepts like cosine similarity are mathematically sound). 

If two linear matrices ($W_E$ and $W_U$) are stacked without a non-linearity, they mathematically collapse into a single operation ($W_E \times W_U = W_{combined}$). The *only* reason they are kept separated is because the data must be intercepted in the middle—at the hidden layer—to extract the embeddings.

## A Toy Mathematical Walkthrough

The following toy model demonstrates the forward pass through explicit calculation:
- **Vocabulary ($V = 8$):** `The` `quick` `brown` `fox` `jumps` `over` `lazy` `dog`
- **Embedding Dimension ($d_{model}$):** 3 dimensions.

The sequence is `The` `quick` `brown`. The network's task is to predict the next token: `fox`.

*(Note: If the sequence is at the end of a sentence, the target is the End of Sequence `<EOS>` token. `<EOS>` is treated exactly like any other word; it receives a row in $W_E$ and its vector's geometry is learned purely through observing sentence-ending patterns.)*

### Step 1: The Input
The final word of the context, `brown`, is represented as a one-hot vector. The word `brown` is at index 2 in the vocabulary.
$$
\mathbf{x} = \begin{bmatrix} 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}
$$

### Step 2: Layer 1 (The Embedding Lookup)
The one-hot vector $\mathbf{x}$ is multiplied by the randomly initialized $8 \times 3$ embedding matrix, $W_E$.

$$
W_E = \begin{bmatrix}
0.1 & -0.4 & 0.2 \\
0.5 & 0.1 & -0.8 \\
\mathbf{-0.3} & \mathbf{0.9} & \mathbf{0.4} \\
0.2 & -0.2 & 0.1 \\
\dots & \dots & \dots \\
\end{bmatrix}
$$

Because all values in $\mathbf{x}$ are $0$ except at index 2, the dot product $\mathbf{x} \times W_E$ simply extracts row 2. 

$$
\mathbf{h} = \begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}
$$

This $3$-dimensional vector is the **hidden layer** state. It is the current, untrained embedding for `brown`.

### Step 3: Layer 2 (The Un-embedding Projection)
This hidden state is then projected back into the 8-word vocabulary space using the un-embedding matrix, $W_U$ (a $3 \times 8$ matrix). 

$$
\mathbf{z} = \mathbf{h} \times W_U 
$$

Assume the resulting vector $\mathbf{z}$ evaluates to:
$$
\mathbf{z} = \begin{bmatrix} 1.2 & -0.5 & 0.3 & 2.1 & -1.8 & 0.7 & 0.0 & 0.4 \end{bmatrix}
$$

This vector $\mathbf{z}$ contains the **logits**. These raw, unbounded geometric scores indicate how strongly the network believes each vocabulary word is the next token.

### Step 4: The Softmax Function
To evaluate the network's performance, these arbitrary logits must be converted into a valid probability distribution where all values are strictly positive and sum to $1.0$. This is achieved mathematically via the **Softmax** function:

$$
\hat{y}_i = \frac{e^{z_i}}{\sum_{j=1}^{V} e^{z_j}}
$$

The Softmax for index 3 (`fox`) is calculated as follows:
1. **Exponentiate $z_3$:** 
$$ e^{2.1} \approx 8.16 $$
2. **Exponentiate all logits and sum them:** 
$$ e^{1.2} + e^{-0.5} + e^{0.3} + e^{2.1} + e^{-1.8} + e^{0.7} + e^{0.0} + e^{0.4} \approx 3.32 + 0.60 + 1.35 + 8.16 + 0.16 + 2.01 + 1.0 + 1.49 = 18.09 $$
3. **Divide:** 
$$ \frac{8.16}{18.09} \approx 0.45 $$

The network predicts a $45\%$ probability that `fox` is the next word. Applying this operation across all 8 indices yields our predicted probability distribution, $\mathbf{\hat{y}}$.

### Step 5: The Cross-Entropy Loss
Because the embeddings are randomly initialized, a $45\%$ prediction is the result of chance. To mathematically force the network to learn, the exact divergence of this prediction from reality must be quantified.

The ground truth, $\mathbf{y}$, is that `fox` (index 3) is definitely the next word. The true probability distribution is a one-hot vector where index 3 is $1.0$, and all other indices are $0$.

The **Cross-Entropy Loss** calculates the divergence between the predicted distribution ($\mathbf{\hat{y}}$) and the true distribution ($\mathbf{y}$). 

The choice of this specific operation stems from information theory, where its purpose is to mathematically measure "surprise." The mechanics of the equation break into two parts:

1. **The Logarithm as Surprise**: Taking the logarithm of the predicted probability ($\log(\hat{y}_i)$) converts a raw percentage into a continuous measurement of surprise. If the network predicts a $99\%$ probability for a word, its surprise is near zero ($\log(0.99) \approx -0.01$). If it predicts a $1\%$ probability, its surprise is massive ($\log(0.01) \approx -4.6$). 
2. **The Summation as Expected Value**: In statistics, the "expected value" of a system is calculated by taking every possible outcome, multiplying it by its true probability, and summing them together. By multiplying the true probability ($y_i$) by the network's surprise ($\log(\hat{y}_i)$) and summing across the entire vocabulary, the equation calculates the *expected surprise* of the network. 

By computing this expected surprise across the entire vocabulary space, the total mathematical distance between the network's holistic belief and reality is measured:

$$
L = -\sum_{i=1}^{V} y_i \log(\hat{y}_i)
$$

Because the true distribution $\mathbf{y}$ is one-hot, a simplification occurs. For every incorrect word, the true probability $y_i$ is $0$. This causes every single term in the summation to mathematically vanish, except for the one correct word where $y_i = 1.0$.

Consequently, the massive summation radically collapses into a single term evaluating only the correct answer. This reduced form is known as **Negative Log-Likelihood**:

$$
L = -\log(\hat{y}_{true})
$$

The conceptual interpretation is straightforward: 
- **Likelihood**: This is the model's predicted probability for the correct word (in this case, $0.45$ for `fox`). The objective is to maximize this value.
- **Log**: Taking the natural logarithm of a decimal between $0$ and $1$ yields a negative number (e.g., $\log(0.45) \approx -0.79$). 
- **Negative**: Multiplication by $-1$ flips this into a positive "loss" scalar. Higher confidence yields lower loss; lower confidence yields higher loss.

Plugging in our prediction for `fox`:
$$
L = -\log(0.45) \approx 0.79
$$

This scalar $L = 0.79$ represents the absolute error of the forward pass. If the network had predicted a $99\%$ probability ($-\log(0.99)$), the loss would be exponentially near zero. If it had predicted $1\%$ ($-\log(0.01)$), the loss would be massive ($4.6$). 

## The Limit of Static Embeddings: Superposition
The fundamental limitation of this architecture is **polysemy** (words with multiple meanings).

Because $W_E$ is a static matrix, there is exactly one row allocated for the word `apple`. During training, sentences like *"I ate an apple"* will mathematically pull this vector toward the fruit cluster. Conversely, sentences like *"Apple released a phone"* will pull the exact same vector toward the tech cluster. 

Over billions of words, the single vector for `apple` settles into a state of **superposition**—the mathematical center of mass between its usages. It becomes a noisy, blurred average. 

This static limitation is the exact reason the **Self-Attention** mechanism was invented. In a Transformer, Self-Attention allows the static `apple` vector to look at the surrounding words in the sequence and dynamically morph itself purely into a tech vector or purely into a fruit vector before the prediction is made. 

The physical adjustment of the vector space via gradient descent, which produces these static baseline vectors in the first place, is the subject of the next chapter.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
