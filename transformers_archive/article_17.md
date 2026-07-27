# Part 17: Mapping Back to Words

<!-- SUMMARY: The deeply contextualized mathematical representations emerging from the second layer are translated back into the vocabulary space using the unembedding matrix. This critical linear projection produces raw logits that quantify the geometric preference for predicting the next sequence token. -->

The network has completed its deep processing phase. The geometric coordinates within the residual stream emerging from Layer 2 now contain dense, highly abstracted representations of grammar and semantics. The vectors contain rich information about what each token means in relation to the others. However, these vectors are still floating in an abstract six-dimensional model space. To generate actual text, the architecture must translate these continuous vectors back into the discrete twelve-dimensional vocabulary space. This operation bridges the gap between the hidden dimensionality of the model and the tangible tokens that comprise language.

## The Unembedding Matrix

Throughout the forward pass, the tokens have existed as vectors where the model dimension is 6. The goal is to predict the next token in the sequence. To do this, the network needs a score for every single word in the vocabulary, which has a size of 12.

The unembedding matrix, often denoted as $W_U$, acts as the bridge between these two spaces. It functions as a linear classifier projection matrix with dimensions $6 \times 12$. Its dimensions align with the model dimension on one axis and the total vocabulary size on the other. Geometrically, each column in this matrix represents a specific word in the vocabulary.

In many architectures, this matrix is independent and learned separately during training. Allowing the unembedding layer to learn independent weights provides the network with greater flexibility to optimize its output distribution. In other models, it is simply the transpose of the original embedding matrix, a technique known as weight tying. Weight tying assumes that the conceptual representation of a word entering the model should be geometrically similar to the representation of the word exiting the model. For this implementation, the network uses an independent $6 \times 12$ matrix.

$$
\text{Unembedding Matrix } W_U = \begin{bmatrix}
   0.00 &    0.01 &    0.02 &    0.03 &    0.04 &    0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 \\
   0.01 &    0.02 &    0.03 &    0.04 &    0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 &    0.12 \\
   0.02 &    0.03 &    0.04 &    0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 &    0.12 &    0.13 \\
   0.03 &    0.04 &    0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 &    0.12 &    0.13 &    0.14 \\
   0.04 &    0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 &    0.12 &    0.13 &    0.14 &    0.15 \\
   0.05 &    0.06 &    0.07 &    0.08 &    0.09 &    0.10 &    0.11 &    0.12 &    0.13 &    0.14 &    0.15 &    0.16
\end{bmatrix}
$$

## Calculating the Logits

The network computes the dot product between the final Layer 2 output matrix and the unembedding matrix. This multiplication measures the geometric alignment between the contextualized sequence vectors and every possible vocabulary concept. By taking this dot product, the network is measuring how strongly a token's final state aligns with the abstract concept of each vocabulary word. A high positive scalar value indicates a strong semantic match, whereas a negative value indicates an unlikely candidate. The resulting matrix contains these unnormalized scores, which are formally known as logits.

The final Layer 2 output tensor $X_{final}$ has dimensions $4 \times 6$, representing the sequence of four tokens: `<BOS>`, `i`, `woke`, and `up`. The network multiplies this by $W_U$:

$$
\text{Logits} = X_{final} W_U
$$

Since $X_{final}$ is $4 \times 6$ and $W_U$ is $6 \times 12$, the resulting Logits matrix has dimensions $4 \times 12$.

$$
\text{Logits} = \begin{bmatrix}
  -0.03 &   -0.03 &   -0.04 &   -0.04 &   -0.05 &   -0.05 &   -0.05 &   -0.06 &   -0.06 &   -0.07 &   -0.07 &   -0.08 \\
   0.03 &    0.03 &    0.04 &    0.04 &    0.05 &    0.05 &    0.05 &    0.06 &    0.06 &    0.07 &    0.07 &    0.08 \\
  -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 &   -0.07 \\
   0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07 &    0.07
\end{bmatrix}
$$

Each row in the logits matrix corresponds to a specific position in the input sequence. The twelve columns represent the raw confidence for each token in the vocabulary being the correct subsequent word. While these values encode the network's raw predictions, they represent an untrained state.

The theoretical output for the final token in the sequence, `up`, provides a clear example. The network aims to predict `late`, which is the ninth token in the vocabulary at index 8. In a fully optimized scenario, the row corresponding to `up` in the Logits matrix will contain twelve raw numerical scores that heavily favor the correct token.

$$
\text{Logits}_{\text{up}} = \begin{bmatrix}
-0.12 & 0.45 & -1.23 & 0.05 & 0.88 & -0.34 & -0.77 & 1.02 & 3.45 & \dots & -0.11
\end{bmatrix}
$$

In a well-trained model, the highest score in this vector corresponds to the correct next word. In the hypothetical vector above, the value at index 8 is 3.45, which is significantly higher than the other values. This highest value indicates that the internal geometry strongly favors `late` as the next logical continuation of the sequence.

## The Need for Probabilities

While the logits provide a ranking of the most likely next words, they are unbounded raw scores. They can be positive, negative, and of any magnitude. The values extend infinitely in both positive and negative directions and do not sum to one. This presents a problem for interpreting the model's confidence and for calculating the loss during backpropagation. It is impossible to easily determine if a score of 3.45 represents absolute certainty or just a slight preference over a score of 2.11.

Transforming these raw algebraic magnitudes into interpretable probabilities requires a final normalization step. The network must convert these raw scores into a strict probability distribution where all values are positive and sum exactly to one.
