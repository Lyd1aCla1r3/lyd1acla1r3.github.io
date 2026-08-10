# Part 4: Training the Space: Backpropagation and Negative Sampling

<!-- SUMMARY: The optimization of the embedding matrix relies on backpropagation, where the complex derivatives of softmax and cross-entropy algebraically cancel to produce a pure error signal. Because updating the full vocabulary distribution is computationally intractable, Word2Vec employs Negative Sampling to convert the multi-class softmax objective into an efficient binary classification problem. -->

The forward pass of the Skip-gram architecture concludes by generating a scalar loss value, $L$, representing the error between the network's predicted probabilities and the ground truth context word. To optimize the randomly initialized embedding matrices ($W_{target}$ and $W_{context}$), we must utilize backpropagation to calculate the gradient of this loss with respect to every individual weight in the network.

## The Mathematical Cancellation

To calculate the gradient of the loss with respect to the raw, pre-softmax logits $\mathbf{z}$, we must apply the chain rule across two notoriously complex functions: the Cross-Entropy loss (which contains logarithmic derivatives) and the Softmax function.

As demonstrated extensively in our Transformers series, the softmax function is not an element-wise operation. Altering a single logit $z_i$ changes the sum in the denominator, which inversely alters the probability of every other word in the vocabulary. The derivative of a softmax output with respect to its input forms a full Jacobian matrix tracking the interaction of every single output with every single input.

However, a beautiful mathematical cancellation occurs when applying the chain rule to combine the derivative of the cross-entropy loss with the Jacobian of the softmax function. The complex fractional terms and off-diagonal Jacobian interactions perfectly cancel each other out.

The gradient of the loss with respect to the raw logits, $\frac{\partial L}{\partial \mathbf{z}}$, simplifies entirely to:

$$
\frac{\partial L}{\partial \mathbf{z}} = \mathbf{\hat{y}} - \mathbf{y}
$$

This derivative is stunningly simple. The error signal is exactly the predicted probability distribution minus the one-hot encoded ground truth vector. 

If the correct context word is `street` (index `482`), the one-hot ground truth vector $\mathbf{y}$ contains a `1.0` at index `482` and `0.0` everywhere else. If our network predicted a `0.14%` probability for `street` and a `6%` probability for `cat`, the error signal at the `street` index is $0.0014 - 1.0 = -0.9986$ (a massive negative gradient, pulling the logit up), while the error signal at the `cat` index is $0.06 - 0.0 = +0.06$ (a positive gradient, pushing the incorrect logit down).

## Updating the Matrices

This error signal $(\mathbf{\hat{y}} - \mathbf{y})$ represents how much each raw logit must change. By the rules of vector calculus, we propagate this error backward through the matrix multiplications to update the weights.

To update $W_{context}$, we multiply the error signal by the target word's hidden state $\mathbf{h}$. To update the target embedding matrix $W_{target}$, we pass the error signal backward through $W_{context}$ to find the gradient for $\mathbf{h}$, and then update the specific row in $W_{target}$ that generated $\mathbf{h}$.

Through millions of iterations, these cascading gradients physically rotate the vectors. Contextually similar words are pulled together by shared positive gradients, while unrelated words are pushed apart by negative gradients.

## The Intractability of Softmax

While the calculus is elegant, executing this exact mathematical process on a production corpus is computationally intractable. 

The core bottleneck lies in the denominator of the softmax function:
$$ \sum_{j=1}^{V} e^{z_j} $$

To calculate the probability of a *single* context word, the network must compute the dot product of the target vector against *every single row* in $W_{context}$, exponentiate all $V$ results, and sum them. If the vocabulary size $V$ is 100,000, this requires 100,000 dot products just to process a single word in the corpus. Over billions of training words, this normalization requirement grinds the system to a halt.

Furthermore, the backpropagation step $\mathbf{\hat{y}} - \mathbf{y}$ requires applying a tiny negative gradient to the remaining 99,999 incorrect words in $W_{context}$, meaning the entire massive matrix must be updated for every single step.

## Negative Sampling

In 2013, the creators of Word2Vec resolved this bottleneck by abandoning the full softmax distribution entirely, introducing a technique called **Negative Sampling**.

Instead of treating context prediction as a massive multi-class probability distribution across 100,000 words, Negative Sampling reframes it as a simple binary classification problem.

For a target token `walk` and its true context word `street`, we generate one "Positive Sample": (walk, street) $\rightarrow$ Label: 1.
We then randomly sample $k$ "Negative Samples" from the vocabulary (words that did not appear in the context, e.g., $k=5$):
- (walk, desk) $\rightarrow$ Label: 0
- (walk, apple) $\rightarrow$ Label: 0
- (walk, cloud) $\rightarrow$ Label: 0
- (walk, jump) $\rightarrow$ Label: 0
- (walk, blue) $\rightarrow$ Label: 0

Instead of calculating 100,000 dot products, the network calculates exactly 6 dot products. It passes each dot product through a simple sigmoid function (which scales the scalar value between 0 and 1) and calculates the binary cross-entropy loss against the 1 or 0 labels.

During backpropagation, only the vector for the positive word (`street`) and the vectors for the 5 negative words are updated. The other 99,994 rows in $W_{context}$ remain completely untouched. This architectural innovation slashed computational costs by orders of magnitude, transforming Vector Embeddings from a theoretical mathematical exercise into the foundational bedrock of modern Natural Language Processing.
