# Part 17: Mapping Back to Words

<p><em>Prefer to read this seamlessly offline? <a href="/series/transformers/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

Our journey through the Transformer has transformed our input sequence into deeply contextualized mathematical representations. The residual stream emerging from Layer 2 contains rich information about what each token means in relation to the others. However, these vectors are still floating in our abstract six-dimensional model space. To produce actual text, we must translate these vectors back into the twelve-dimensional vocabulary space. This critical translation is performed by the Unembedding matrix.

## The Unembedding Matrix

Throughout the forward pass, our tokens have existed as vectors where the model dimension is 6. Our goal is to predict the next token in the sequence. To do this, we need a score for every single word in our vocabulary, which has a size of 12. 

The Unembedding matrix, often denoted as $W_U$, acts as the bridge between these two spaces. It is a linear projection matrix with dimensions $6 \times 12$. Geometrically, you can think of each column in this matrix as representing a specific word in our vocabulary. By taking the dot product of our contextualized token vector with the matrix, we are measuring how strongly our token's final state aligns with the abstract concept of each vocabulary word.

In many architectures, this matrix is independent and learned separately during training. In other models, it is simply the transpose of the original Embedding matrix, a technique known as weight tying. Weight tying assumes that the conceptual representation of a word entering the model should be geometrically similar to the representation of the word exiting the model. For our toy example, we will treat it as an independent $6 \times 12$ matrix.

## Calculating the Logits

The matrix multiplication of our final Layer 2 output with the Unembedding matrix produces our logits. Logits are the raw, unnormalized scores for each vocabulary token. 

Let us define our final Layer 2 output tensor as $X_{final}$ with dimensions $4 \times 6$, representing our sequence of four tokens: `<BOS>`, `i`, `woke`, and `up`. We multiply this by $W_U$:

$$
\text{Logits} = X_{final} W_U
$$

Since $X_{final}$ is $4 \times 6$ and $W_U$ is $6 \times 12$, the resulting Logits matrix has dimensions $4 \times 12$.

Let us examine the output for the final token in our sequence, which is `up`. We want the model to predict `late`, which is the ninth token in our vocabulary at index 8. The row corresponding to `up` in the Logits matrix will contain twelve raw numerical scores. 

$$
\text{Logits}_{\text{up}} = \begin{bmatrix}
-0.12 & 0.45 & -1.23 & 0.05 & 0.88 & -0.34 & -0.77 & 1.02 & 3.45 & \dots & -0.11
\end{bmatrix}
$$

In a well-trained model, the highest score in this vector should correspond to the correct next word. In the hypothetical vector above, the value at index 8 is 3.45, which is significantly higher than the other values. This indicates that the model's internal geometry strongly favors `late` as the next logical continuation of the sequence.

## The Need for Probabilities

While the logits provide a ranking of the most likely next words, they are unbounded raw scores. They can be positive, negative, and of any magnitude. This presents a problem for interpreting the model's confidence and for calculating the loss during backpropagation. We cannot easily determine if a score of 3.45 represents absolute certainty or just a slight preference over a score of 2.11.

To solve this, we must convert these raw scores into a strict probability distribution where all values are positive and sum exactly to one. We will explore how the final Softmax function accomplishes this in the next part.

<p><em>Prefer to read this seamlessly offline? <a href="/series/transformers/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
