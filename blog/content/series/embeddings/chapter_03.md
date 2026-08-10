# Part 3: The Architecture and the Forward Pass

<!-- SUMMARY: To understand how vector embeddings are learned, we must examine the shallow neural network designed to train them. By walking step-by-step through a concrete mathematical example, we observe how a two-layer architecture extracts a dense vector, projects it into raw logits, and uses Softmax and Cross-Entropy Loss to quantify the network's error against the ground truth. We also explore the fundamental limitations of static embeddings, setting the stage for Transformers. -->

To transform our randomly initialized embedding matrix ($W_E$) into a mathematically rigorous semantic space, we must build a mechanism to evaluate its current state. We achieve this by building a simple neural network *around* $W_E$. Its sole objective is **Next-Token Prediction**: observing a sequence of tokens and predicting the most probable subsequent token in the corpus.

## The Proxy of Prediction

Why do we predict the next word? Our ultimate goal is to capture the semantic meaning of a word, but we do not have a database of "semantic features" (e.g., `is_animal = 1.0`) to supervise the network. 

Instead, we rely on **Distributional Semantics**, famously summarized by linguist J.R. Firth: *"You shall know a word by the company it keeps."* If the network observes that the words `fox`, `wolf`, and `dog` are all frequently followed by words like `hunts`, `sleeps`, or `runs`, the calculus of the network is mathematically forced to push their vectors closer together in the geometric space. Semantic meaning is not explicitly programmed; it is an *emergent byproduct* of the next-token prediction objective.

## The 2-Layer Embedding Network

When training static embeddings from scratch, the architecture is astonishingly simple. It is a shallow neural network consisting of exactly two layers:

1. **Layer 1: The Embedding Projection ($W_E$)**. The $W_E$ matrix *is* the first layer of the network. It projects the one-hot encoded vocabulary vector (dimension $V$) into the dense, continuous vector space (dimension $d_{model}$). 
2. **Layer 2: The Un-embedding Projection ($W_U$)**. This layer projects the dense continuous vector back out into the vocabulary space (dimension $V$), producing a raw score for every possible word in the vocabulary.

### Where is the Hidden Layer?
In this architecture, the **hidden layer** is simply the state of the network between these two projections. It is the dense $d_{model}$-dimensional vector itself. The network's only true purpose is to optimize the weights of Layer 1 ($W_E$). Once training is complete, Layer 2 ($W_U$) is entirely discarded, and the hidden layer outputs (the vectors) are saved as our final embeddings.

### Where is the Activation Function?
Crucially, **there are no non-linear activation functions** (like ReLU or GELU) between Layer 1 and Layer 2. 

This is the fundamental architectural difference between an Embedding Network and the Feed-Forward Networks (FFN) you will see in Transformers. A Transformer uses non-linear activations to learn complex, non-linear logic. The Embedding Network intentionally omits them because its goal is to construct a pure, linear geometric space (where concepts like cosine similarity are mathematically sound). 

If you stack two linear matrices ($W_E$ and $W_U$) without a non-linearity, they mathematically collapse into a single operation ($W_E \times W_U = W_{combined}$). The *only* reason we keep them separated is because we want to intercept the data in the middle—at the hidden layer—to extract our embeddings.

## A Toy Mathematical Walkthrough

To eliminate handwaving, let us calculate a forward pass by hand. We will define a microscopic toy model:
- **Vocabulary Size ($V$):** 8 words ([`The`, `quick`, `brown`, `fox`, `jumps`, `over`, `lazy`, `dog`]).
- **Embedding Dimension ($d_{model}$):** 3 dimensions.

Our sequence is `The` `quick` `brown`. The network's task is to predict the next token: `fox`.

*(Note: If the sequence was at the end of a sentence, the target would be the End of Sequence `<EOS>` token. `<EOS>` is treated exactly like any other word; it gets a row in $W_E$ and its vector's geometry is learned purely through observing sentence-ending patterns.)*

### Step 1: The Input
We take the final word of our context, `brown`, and represent it as a one-hot vector. The word `brown` is at index 2 in our vocabulary.
$$
\mathbf{x} = [0, 0, 1, 0, 0, 0, 0, 0]
$$

### Step 2: Layer 1 (The Embedding Lookup)
We multiply our one-hot vector $\mathbf{x}$ by our randomly initialized $8 \times 3$ embedding matrix, $W_E$.

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
\mathbf{h} = [-0.3, 0.9, 0.4]
$$

This $3$-dimensional vector is our **hidden layer** state. It is the current, untrained embedding for `brown`.

### Step 3: Layer 2 (The Un-embedding Projection)
We now project this hidden state back into our 8-word vocabulary space using the un-embedding matrix, $W_U$ (a $3 \times 8$ matrix). 

$$
\mathbf{z} = \mathbf{h} \times W_U 
$$

Let us assume the resulting vector $\mathbf{z}$ evaluates to:
$$
\mathbf{z} = \begin{bmatrix} 1.2 & -0.5 & 0.3 & 2.1 & -1.8 & 0.7 & 0.0 & 0.4 \end{bmatrix}
$$

This vector $\mathbf{z}$ contains the **logits**. These raw, unbounded geometric scores indicate how strongly the network believes each vocabulary word is the next token.

### Step 4: The Softmax Function
To evaluate the network's performance, we must convert these arbitrary logits into a valid probability distribution where all values are strictly positive and sum to $1.0$. We achieve this mathematically via the **Softmax** function:

$$
\hat{y}_i = \frac{e^{z_i}}{\sum_{j=1}^{V} e^{z_j}}
$$

Let's calculate the Softmax for index 3 (`fox`):
1. **Exponentiate $z_3$:** 
$$ e^{2.1} \approx 8.16 $$
2. **Exponentiate all logits and sum them:** 
$$ e^{1.2} + e^{-0.5} + e^{0.3} + e^{2.1} + e^{-1.8} + e^{0.7} + e^{0.0} + e^{0.4} \approx 3.32 + 0.60 + 1.35 + 8.16 + 0.16 + 2.01 + 1.0 + 1.49 = 18.09 $$
3. **Divide:** 
$$ \frac{8.16}{18.09} \approx 0.45 $$

The network predicts a $45\%$ probability that `fox` is the next word. Applying this operation across all 8 indices yields our predicted probability distribution, $\mathbf{\hat{y}}$.

### Step 5: The Cross-Entropy Loss
Because our embeddings are randomly initialized, a $45\%$ prediction is purely coincidental. To mathematically force the network to learn, we must quantify exactly *how wrong* this prediction is compared to reality.

The ground truth, $\mathbf{y}$, is that `fox` (index 3) is definitely the next word. The true distribution is a one-hot vector where index 3 is $1.0$.

The **Cross-Entropy Loss** calculates the divergence between our prediction $\mathbf{\hat{y}}$ and the truth $\mathbf{y}$. Because the truth is one-hot, the equation radically simplifies into the Negative Log-Likelihood of the correct answer:

$$
L = -\log(\hat{y}_{true})
$$

Plugging in our prediction for `fox`:
$$
L = -\log(0.45) \approx 0.79
$$

This loss scalar $L$ represents the absolute error of the forward pass. If the network had predicted a $99\%$ probability ($-\log(0.99)$), the loss would be exponentially near zero. If it had predicted $1\%$ ($-\log(0.01)$), the loss would be massive ($4.6$). 

## The Limit of Static Embeddings: Superposition
Before moving on to how backpropagation resolves this loss, we must acknowledge the fundamental limitation of this architecture: **polysemy** (words with multiple meanings).

Because $W_E$ is a static matrix, there is exactly one row allocated for the word `apple`. During training, sentences like *"I ate an apple"* will mathematically pull this vector toward the fruit cluster. Conversely, sentences like *"Apple released a phone"* will pull the exact same vector toward the tech cluster. 

Over billions of words, the single vector for `apple` settles into a state of **superposition**—the mathematical center of mass between its usages. It becomes a noisy, blurred average. 

This static limitation is the exact reason the **Self-Attention** mechanism was invented. In a Transformer, Self-Attention allows the static `apple` vector to look at the surrounding words in the sequence and dynamically morph itself purely into a tech vector or purely into a fruit vector before the prediction is made. 

But to understand how we acquire those static baseline vectors in the first place, we must examine the mechanism of learning. This physical adjustment of the vector space via gradient descent is the subject of the next chapter.
