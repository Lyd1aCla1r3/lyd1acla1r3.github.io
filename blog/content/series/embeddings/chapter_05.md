# Part 5: Backpropagation Through the Weight Matrices

<!-- SUMMARY: The backward pass continues through the un-embedding and embedding matrices. By deriving the element-wise gradients for both $W_U$ and $W_E$, and demonstrating how the one-hot sparsity of the input ensures only a single embedding row receives an update, the full end-to-end gradient is computed and the weight update rule is applied. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter established the gradient at the logits: $\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}$. The backward pass now continues through the weight matrices to compute the gradient at the embedding layer itself.

## Propagating Through Layer 2: $\frac{\partial \mathbf{z}}{\partial \mathbf{h}}$

The first two links of the chain have been combined to form $\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}$. The next link is $\frac{\partial \mathbf{z}}{\partial \mathbf{h}}$: how do the logits change when the hidden state (the embedding vector for `brown`) is altered?

Recall from Chapter 3 that the logits are computed by multiplying the hidden state $\mathbf{h}$ by the un-embedding matrix $W_U$:

$$
\mathbf{z} = \mathbf{h} \times W_U
$$

The result $\mathbf{z}$ is a vector with 8 elements—one logit per vocabulary word (`The`, `quick`, `brown`, `fox`, `jumps`, `over`, `lazy`, `dog`). In our toy model, $\mathbf{h}$ is a $1 \times 3$ vector (the 3-dimensional embedding for `brown`) and $W_U$ is a $3 \times 8$ matrix. Each logit $z_j$ is therefore the dot product of $\mathbf{h}$ with column $j$ of $W_U$.

To differentiate this, the operations are expanded element-wise. The index $m$ refers to a specific **embedding dimension** (ranging from 1 to 3 in this model). Written out for a single logit $z_j$:

$$
z_j = h_1 \cdot W_{U_{1,j}} + h_2 \cdot W_{U_{2,j}} + h_3 \cdot W_{U_{3,j}}
$$

This is a sum of three terms, each multiplying one embedding dimension $h_m$ by its corresponding weight $W_{U_{m,j}}$. Differentiating this sum with respect to a specific embedding dimension $h_m$ models how $z_j$ changes when $h_m$ is adjusted:

The weights $W_{U_{1,j}}$, $W_{U_{2,j}}$, and $W_{U_{3,j}}$ are constants—they are fixed parameters of the network during this step. So each term in the sum has the form "constant $\times$ variable" or "constant $\times$ unrelated variable." Taking the derivative with respect to $h_m$:

- The term $h_m \cdot W_{U_{m,j}}$ contains $h_m$, and the derivative of a variable multiplied by a constant is simply the constant: $W_{U_{m,j}}$.
- Every other term (e.g., $h_1 \cdot W_{U_{1,j}}$ when $m \neq 1$) does not contain $h_m$ at all. These are constants with respect to $h_m$, and their derivatives are zero.

The entire sum collapses to a single surviving term:

$$
\frac{\partial z_j}{\partial h_m} = W_{U_{m,j}}
$$

The derivative is simply the weight that multiplied $h_m$ in the forward pass. This makes intuitive sense: the weight $W_{U_{m,j}}$ controls exactly how much influence the $m$-th embedding dimension has on the $j$-th logit. A large weight means that dimension has a strong effect on that logit; a weight near zero means it has almost none.

### The Gradient at the Hidden State ($\frac{\partial L}{\partial \mathbf{h}}$)

This result is chained with $\frac{\partial L}{\partial \mathbf{z}}$ to yield the gradient of the loss with respect to $\mathbf{h}$. A single embedding dimension $h_m$ contributes to *every* logit in $\mathbf{z}$ (it participates in all 8 dot products). This requires a sum over all 8 vocabulary words:

$$
\frac{\partial L}{\partial h_m} = \sum_{j=1}^{8} \frac{\partial L}{\partial z_j} \cdot \frac{\partial z_j}{\partial h_m} = \sum_{j=1}^{8} (\hat{y}_j - y_j) \cdot W_{U_{m,j}}
$$

Each term in this sum isolates how much embedding dimension $m$ of `brown`'s vector contributed to the error at vocabulary word $j$. The error at each word ($\hat{y}_j - y_j$) is multiplied by the weight connecting $h_m$ to that word ($W_{U_{m,j}}$), and summed across all 8 words.

Computing this for all three embedding dimensions ($m = 1, 2, 3$) simultaneously yields the complete gradient in matrix notation:

$$
\frac{\partial L}{\partial \mathbf{h}} = (\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T
$$

The transpose $W_U^T$ reverses the direction of the projection. During the forward pass, $W_U$ projected the $3$-dimensional embedding $\mathbf{h}$ *up* into $8$-dimensional vocabulary space to produce the logits. Now, $W_U^T$ projects the $8$-dimensional error signal *back down* into $3$-dimensional embedding space. The result is a $1 \times 3$ gradient vector that lives in the same coordinate system as `brown`'s embedding vector—it tells us the exact direction and magnitude that `brown`'s vector should be nudged to reduce the loss.

### Updating $W_U$ Along the Way

Before continuing backward, note that $W_U$ itself contains weights that require updating. Their gradients are derived from the same element-wise equation:

$$
z_j = h_1 \cdot W_{U_{1,j}} + h_2 \cdot W_{U_{2,j}} + h_3 \cdot W_{U_{3,j}}
$$

This time, the expression is differentiated with respect to a specific *weight* $W_{U_{m,j}}$ instead of an embedding dimension $h_m$. The roles flip: the embedding values $h_1$, $h_2$, $h_3$ are constants (computed during the forward pass and fixed), and $W_{U_{m,j}}$ is the variable.

- The term $h_m \cdot W_{U_{m,j}}$ contains our variable, and the derivative of a constant multiplied by a variable is the constant: $h_m$.
- Every other term (e.g., $h_1 \cdot W_{U_{1,j}}$ when $m \neq 1$) does not contain $W_{U_{m,j}}$, so its derivative is zero.

Therefore:

$$
\frac{\partial z_j}{\partial W_{U_{m,j}}} = h_m
$$

Applying the chain rule to get the gradient of the loss:

$$
\frac{\partial L}{\partial W_{U_{m,j}}} = \frac{\partial L}{\partial z_j} \cdot \frac{\partial z_j}{\partial W_{U_{m,j}}} = (\hat{y}_j - y_j) \cdot h_m
$$

Each weight's gradient is the product of two values: the error signal at the vocabulary word it connects to ($\hat{y}_j - y_j$), and the embedding dimension value that flowed through it during the forward pass ($h_m$). These updates are applied alongside the $W_E$ updates at the end.

## Propagating Through Layer 1: $\frac{\partial \mathbf{h}}{\partial W_E}$

The backward pass now reaches the first layer—the origin of the forward pass and the last link in the chain. Recall:

$$
\mathbf{h} = \mathbf{x} \times W_E
$$

where $\mathbf{x}$ is the one-hot input vector for `brown`. This is another matrix multiplication, identical in structure to the one just differentiated. The $W_E$ matrix has 8 rows (one per vocabulary word) and 3 columns (one per embedding dimension). Written element-wise for a single embedding dimension $h_m$:

$$
h_m = x_1 \cdot W_{E_{1,m}} + x_2 \cdot W_{E_{2,m}} + x_3 \cdot W_{E_{3,m}} + \dots + x_8 \cdot W_{E_{8,m}}
$$

Each term multiplies the input value at a vocabulary index ($x_1$ for `The`, $x_2$ for `quick`, $x_3$ for `brown`, etc.) by the corresponding weight in row $i$ of $W_E$. Just as in Layer 2, the input values $x_i$ are constants (fixed from the one-hot encoding) and $W_{E_{i,m}}$ is the variable. Only the term containing $W_{E_{i,m}}$ survives differentiation:

$$
\frac{\partial h_m}{\partial W_{E_{i,m}}} = x_i
$$

The chain rule is applied to connect this to the loss. Because $\frac{\partial L}{\partial h_m}$ was computed in the previous section:

$$
\frac{\partial L}{\partial W_{E_{i,m}}} = \frac{\partial L}{\partial h_m} \cdot \frac{\partial h_m}{\partial W_{E_{i,m}}} = \frac{\partial L}{\partial h_m} \cdot x_i
$$

But $\mathbf{x}$ is one-hot: $x_i = 0$ for every vocabulary word except `brown` (index 2), where $x_2 = 1$. This means:

- For the row of `The` ($i = 0$): $\frac{\partial L}{\partial W_{E_{0,m}}} = 0 \cdot \frac{\partial L}{\partial h_m} = 0$. The gradient is zero. That row is untouched.
- For the row of `quick` ($i = 1$): $\frac{\partial L}{\partial W_{E_{1,m}}} = 0 \cdot \frac{\partial L}{\partial h_m} = 0$. Same—zero gradient.
- For the row of `brown` ($i = 2$): $\frac{\partial L}{\partial W_{E_{2,m}}} = 1 \cdot \frac{\partial L}{\partial h_m} = \frac{\partial L}{\partial h_m}$. The gradient passes through directly.
- For every remaining row (`fox`, `jumps`, `over`, `lazy`, `dog`): zero gradient.

This is the identical "plucking" mechanism observed in the forward pass, operating in reverse. During the forward pass, the one-hot vector *extracted* a single row from $W_E$. During backpropagation, it *deposits* the gradient into that same single row. Only `brown`'s vector receives an update from this training example. Every other word in the vocabulary remains untouched.

## The Weight Update

With the gradient computed end-to-end, the fundamental weight update rule is applied:

$$
W_{new} = W_{old} - \alpha \cdot \nabla L
$$

The scalar $\alpha$ is the **learning rate**, and its role is critical. Why not apply the full gradient and move directly to the position that would perfectly predict `fox`? Because `brown` does not exist in a single context. Across the training corpus, `brown` precedes `fox`, but also `bear`, `sugar`, `eyes`, and `shoes`. Each of these contexts generates a different gradient, pulling `brown`'s vector in a different direction in the embedding space.

If the learning rate is too large, each training example violently overwrites the previous one. The vector for `brown` oscillates chaotically, never settling into a meaningful position. A small learning rate ensures each individual example contributes only a microscopic nudge. Over millions of iterations, these nudges accumulate statistically: directions that are consistently reinforced across many contexts grow dominant, while contradictory or noisy signals cancel out. The final resting position of the vector reflects not any single sentence, but the **aggregate statistical geometry** of every context in which `brown` appeared.

After this single training step, the 3-dimensional vector for `brown` has shifted by a fraction of a decimal point. The change is imperceptible. But the same operation is about to execute billions of times, across every token in the corpus, adjusting every vector that participates in each forward pass. The cumulative effect of these microscopic nudges—and the geometric structure that organically emerges from them—is the subject of the next chapter.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
