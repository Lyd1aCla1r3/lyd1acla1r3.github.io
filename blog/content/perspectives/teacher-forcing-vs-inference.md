# The Mathematics of Parallel Training: Teacher Forcing vs. Inference

<!-- SUMMARY: A step-by-step mathematical walkthrough contrasting the parallel nature of Transformer training with the sequential bottleneck of inference. A concrete toy example traces the tensor algebra of causal masking and cross-entropy loss, which makes the mechanics of Teacher Forcing explicit without relying on abstraction. -->

A fascinating divergence exists between how large language models are trained and how they operate upon deployment. Training a model takes months of processing trillions of tokens, yet the finished model generates a response in seconds. This discrepancy stems from a fundamental difference in how the two phases use the architecture. Training is highly parallelized, whereas deployment, commonly referred to as inference, is strictly sequential.

During inference, a model generates text one token at a time. A model writing a paragraph cannot write the third sentence without first writing the second. Training at modern model sizes would be computationally impossible with this same sequential process. Researchers avoid the problem with a mathematical technique called Teacher Forcing.

Rather than discussing these concepts abstractly, this article will construct a small toy example. Tracing the exact matrix operations makes it explicitly clear how Teacher Forcing allows a neural network to process an entire sequence simultaneously.

## The Auto-Regressive Bottleneck of Inference

Consider a scenario where the model must complete the simple sequence "i woke up", with the goal of predicting the word "late".

During inference, the model begins with the first word, "i". It performs a series of matrix multiplications to predict the next word, "woke". Next, it appends this new word to its context, creating the input "i woke", and performs all the calculations again to predict "up".

This dependency is the auto-regressive bottleneck: predicting step three mathematically requires the result from step two, so the model has no way to skip ahead.

Assume the model utilizes an embedding dimension of $d_{model} = 4$, meaning every word is translated into a vector of four numbers. The input tensor for the word "i" at time step $t=1$ then has a shape of $1 \times 1 \times 4$. The final output is a single probability distribution predicting one word.

## Bypassing the Bottleneck: Teacher Forcing

Training avoids this sequential trap entirely, because the ground truth sequence "i woke up late" is known in advance and the architecture does not need to guess one word at a time.

Instead, Teacher Forcing feeds the entire sequence into the model simultaneously. The input tensor $X$ now represents the three starting words, "i woke up", all at once. Its shape expands to $1 \times 3 \times 4$, representing one sequence, three words, and four dimensions.

However, presenting the entire sequence at once introduces a critical flaw. Processing the words "i woke up" simultaneously could allow the attention mechanism to let the word "i" look ahead at "woke" to figure out the context. A model that can see the future during training circumvents the learning process entirely.

## The Solution: The Causal Mask

To prevent the model from looking ahead, the architecture employs a mathematical tool known as a Causal Mask.

The model calculates how much each word should pay attention to the others by generating an Attention Score matrix. For the three-word sequence "i", "woke", "up", this results in a $3 \times 3$ matrix.

Assume the raw, unmasked attention scores look like this:

$$
\text{Raw Scores} = \begin{bmatrix}
1.2 & 0.5 & 0.1 \\
0.4 & 1.5 & -0.2 \\
0.8 & -0.1 & 1.1
\end{bmatrix}
$$

The first row represents how much attention the word "i" is allocating to "i", "woke", and "up". Notice that "i" is assigning a score of $0.5$ to "woke". The model is effectively looking into the future.

Before these scores are converted into final probabilities using the Softmax function, the Causal Mask is applied. This mask holds zeros on and below the diagonal and negative infinity above it:

$$
\text{Mask} = \begin{bmatrix}
0 & -\infty & -\infty \\
0 & 0 & -\infty \\
0 & 0 & 0
\end{bmatrix}
$$

Adding this mask to the raw scores turns every future score into negative infinity, because any finite number added to negative infinity becomes negative infinity:

$$
\text{Masked Scores} = \begin{bmatrix}
1.2 & -\infty & -\infty \\
0.4 & 1.5 & -\infty \\
0.8 & -0.1 & 1.1
\end{bmatrix}
$$

The rationale for using negative infinity lies in the subsequent step. The network passes these values through the Softmax function, which utilizes exponentiation, or $e^x$, to convert raw scores into probabilities between 0 and 1, and $e^{-\infty}$ evaluates to exactly zero.

$$
\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum e^{x_j}}
$$

The causal mask changed the future scores to negative infinity, so the Softmax function turns those future scores into exactly zero. This forces the probabilities to distribute entirely among the past and present words. Applying Softmax transforms the matrix into a strict probability distribution, shown here rounded to two decimal places:

$$
\text{Probabilities} = \begin{bmatrix}
1.00 & 0.00 & 0.00 \\
0.25 & 0.75 & 0.00 \\
0.36 & 0.15 & 0.49
\end{bmatrix}
$$

In the top row, the word "i" now possesses a 100 percent probability of attending to itself, and exactly 0 percent probability of attending to the future words "woke" or "up". The causal mask mathematically blinds the model to the future. This ensures it predicts the next word using only past and present context, fully solving the lookahead flaw.

## Shifted Targets and Parallel Loss

Thanks to the causal mask, the model is now generating three independent, non-cheating predictions simultaneously. The single forward pass produces one matrix containing vocabulary predictions for all three positions at once.

To evaluate the model's accuracy, the error is calculated by comparing these predictions against a shifted version of the target sequence.

*   Input Sequence: `["i", "woke", "up"]`
*   Target Sequence: `["woke", "up", "late"]`

At position 1, the model was restricted to seeing only "i", and it is penalized based on how accurately it predicted "woke". At position 2, it saw "i woke", and is penalized for its prediction of "up". At position 3, it saw "i woke up", and is penalized for "late".

The Cross-Entropy Loss is calculated for all three positions simultaneously:

$$
\mathcal{L} = - \frac{1}{L} \sum_{t=1}^{L} \sum_{v=1}^{V} y_{t,v} \log(\hat{y}_{t,v})
$$

To demystify this equation, every variable maps directly to our physical matrix dimensions:
*   $L$ represents the sequence length, which is 3 in our toy example.
*   $t$ indexes the current time step along that sequence, moving iteratively from position 1 to position 3.
*   $V$ represents the total size of our vocabulary.
*   $v$ iterates through every possible word index in that vocabulary.
*   $y$ denotes the ground truth target. This is represented as a binary one-hot vector where the correct target word is a 1 and all incorrect words are 0.
*   $\hat{y}$ represents the model's predicted probability for that specific word, such as 0.12.

Multiplying the true binary value by the logarithm of the predicted probability at every time step $t$ and every vocabulary word $v$ calculates the error across the entire sequence. Averaging this error across all $L$ positions produces a single scalar loss. One backward pass then computes the gradients for all three positions at once, so three separate examples of context update the model's weights in a single step.

## Conclusion

This mechanism is the core innovation of Teacher Forcing. Formatting the input as a full sequence, shifting the target answers by one position, and applying a negative infinity causal mask transforms what would have been three slow, sequential steps into one large, parallel matrix multiplication. This linear algebra is what makes training models on trillions of tokens computationally feasible, even as inference remains bound by the auto-regressive bottleneck.
