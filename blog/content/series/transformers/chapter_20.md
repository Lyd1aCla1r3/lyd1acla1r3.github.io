# Part 20: The Beautiful Cancellation

<p><em>Prefer to read this seamlessly offline? <a href="/series/transformers/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

In the previous part, we established the geometry of the Cross-Entropy loss function. We calculated exactly how far our model's predicted probability distribution strayed from the ground truth one-hot vector. That scalar loss value represents the total error of our network. Now, we must assign blame for that error. We are entering the backpropagation phase of our Transformer, and our very first step is to calculate the gradient of the loss with respect to the final unnormalized scores, known as the logits. 

## The Calculus Problem

Backpropagation relies entirely on the Chain Rule of calculus. To find out how a specific weight deep inside the network contributed to the final error, we must multiply the gradients of every operation between that weight and the final loss. Our journey backward begins at the very end of the network, tracing from the scalar Cross-Entropy loss, through the Softmax function, and into the logits.

Taking the derivative of these two functions individually is notoriously messy. The Softmax function is not an element-wise operation; changing the logit for the word "late" inherently changes the probability of every other word in the vocabulary, since they must all sum to one. Consequently, the derivative of Softmax is not a simple vector, rather it is a full Jacobian matrix tracking the interaction of every output with every input. Furthermore, the derivative of the Cross-Entropy loss involves the derivative of a logarithm, which yields fractional terms. 

Multiplying a fractional gradient by a complex Jacobian matrix sounds like a recipe for a computational nightmare. Yet, a profound mathematical elegance emerges when we combine these two specific functions.

## The Mathematical Elegance

When we apply the Chain Rule to calculate the gradient of the Cross-Entropy loss ($L$) with respect to the pre-Softmax logits ($z$), the complex terms of the Jacobian matrix and the logarithmic derivatives perfectly cancel each other out. The mathematical proof of this cancellation is a staple of vector calculus, yielding a final derivative that is stunningly simple.

$$
\frac{\partial L}{\partial z} = P - Y
$$

In this equation, $P$ represents our predicted probability distribution, and $Y$ represents the ground truth one-hot encoded target vector. The gradient of the loss with respect to the logits is simply the difference between what the model predicted and what the target actually was. 

## Applying the Cancellation

We can observe this cancellation directly using the matrices from our toy example. We have our sequence of predicted probabilities for the four time steps, and we have the target tokens we wish the model had predicted.

| Time Step | Input Token | Target Token | Target Index |
| :--- | :--- | :--- | :--- |
| 1 | `<BOS>` | `i` | 3 |
| 2 | `i` | `woke` | 5 |
| 3 | `woke` | `up` | 7 |
| 4 | `up` | `late` | 8 |

We represent the target tokens as a matrix of one-hot vectors ($Y$), where each row corresponds to a time step and the column of the correct token contains a `1.0`.

$$
Y = \begin{bmatrix}
 0 &  0 &  0 &  1.0 &  0 &  0 &  0 &  0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  1.0 &  0 &  0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  0 &  0 &  1.0 &  0 & \dots &  0 \\
 0 &  0 &  0 &  0 &  0 &  0 &  0 &  0 &  1.0 & \dots &  0
\end{bmatrix}
$$

Next, we take the predicted probabilities ($P$) that we calculated in Part 18. To find the gradient, we simply subtract the target matrix ($Y$) from our predictions ($P$).

$$
\frac{\partial L}{\partial z} = \begin{bmatrix}
 0.0854 &  0.0850 &  0.0846 & -0.9157 &  0.0839 &  0.0835 &  0.0831 &  0.0828 &  0.0824 & \dots &  0.0813 \\
 0.0813 &  0.0817 &  0.0820 &  0.0824 &  0.0828 & -0.9169 &  0.0835 &  0.0839 &  0.0843 & \dots &  0.0854 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & -0.9167 &  0.0833 & \dots &  0.0833 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & -0.9167 & \dots &  0.0833
\end{bmatrix}
$$

## The Physical Intuition

This resulting matrix represents the direction and magnitude of the necessary corrections for the unnormalized logits. We can read this gradient physically as a set of forces acting upon the network's outputs.

During gradient descent, we subtract the gradient from our weights to minimize the error. For the correct token in each sequence, the model predicted a small probability (around `0.084`) when it should have predicted `1.0`. The subtraction yields a negative gradient (roughly `-0.916`). When the optimizer subtracts this negative value during the update step, it will increase the logit for the correct token. 

Conversely, for all the incorrect tokens, the target was `0.0`. The subtraction yields a positive gradient equal to the predicted probability. When the optimizer subtracts this positive value, it will decrease the logits for all incorrect tokens. 

The mathematical cancellation of Softmax and Cross-Entropy results in an exceedingly pure learning signal. It gently suppresses the logits of wrong answers proportional to how strongly the model believed them, while aggressively pulling up the logit of the correct answer. With this gradient vector firmly established at the output of our network, we are now ready to propagate this learning signal backward through the Unembedding matrix and into the heart of the Transformer.

<p><em>Prefer to read this seamlessly offline? <a href="/series/transformers/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
