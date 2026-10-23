# Part 5: Backpropagation Through the Weight Matrices

<!-- SUMMARY: The backward pass continues through the un-embedding and embedding matrices. By deriving the element-wise gradients for both $W_U$ and $W_E$, and demonstrating how the one-hot sparsity of the input ensures only a single embedding row receives an update, the full end-to-end gradient is computed and the weight update rule is applied. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter established the gradient at the logits: $\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}$. The backward pass now continues through the weight matrices to compute the gradient at the embedding layer itself.

## Propagating Through Layer 2: $\frac{\partial \mathbf{z}}{\partial \mathbf{h}}$

The first two links of the chain have been combined to form $\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}$. The next link is $\frac{\partial \mathbf{z}}{\partial \mathbf{h}}$, measuring how the logits change when the hidden state (the embedding vector for `brown`) is altered.

Recall from Chapter 3 that the logits are computed by multiplying the hidden state $\mathbf{h}$ by the un-embedding matrix $W_U$:

$$
\mathbf{z} = \mathbf{h} \times W_U
$$

The output $\mathbf{z}$ is a $1 \times 8$ row vector containing one logit per vocabulary word (`The`, `quick`, `brown`, `fox`, `jumps`, `over`, `lazy`, `dog`, indexed $j = 0, \dots, 7$). In the toy model, $\mathbf{h}$ is a $1 \times 3$ vector (the 3-dimensional embedding for `brown`) and $W_U$ is a $3 \times 8$ matrix. Each logit $z_j$ equals the dot product of $\mathbf{h}$ with column $j$ of $W_U$.

Differentiating this projection requires expanding the operation element-wise. The index $m \in \{1, 2, 3\}$ denotes a specific **embedding dimension** in the 3-dimensional toy model. Written out for a single logit $z_j$:

$$
z_j = h_1 \cdot W_{U_{1,j}} + h_2 \cdot W_{U_{2,j}} + h_3 \cdot W_{U_{3,j}}
$$

That dot product expands into a sum of three terms, each multiplying one embedding dimension $h_m$ by its corresponding weight $W_{U_{m,j}}$. Differentiating this sum with respect to a specific embedding dimension $h_m$ measures how $z_j$ changes when $h_m$ is adjusted.

The weights $W_{U_{1,j}}$, $W_{U_{2,j}}$, and $W_{U_{3,j}}$ act as fixed constants during this step. Each term in the sum takes the form of a constant multiplying $h_m$ or a constant multiplying an independent coordinate. Differentiating with respect to $h_m$ separates the terms into two groups:

- **Active Term ($h_m \cdot W_{U_{m,j}}$):** Contains $h_m$, and differentiating a variable multiplied by a constant leaves the constant factor $W_{U_{m,j}}$.
- **Remaining Terms ($h_n \cdot W_{U_{n,j}}$ for $n \neq m$):** Do not contain $h_m$, so they act as constants with respect to $h_m$ and their derivatives evaluate to zero.

The entire sum collapses to a single surviving term:

$$
\frac{\partial z_j}{\partial h_m} = W_{U_{m,j}}
$$

The partial derivative equals the weight that multiplied $h_m$ in the forward pass. That weight $W_{U_{m,j}}$ governs how much influence the $m$-th embedding dimension exerts on the $j$-th logit: a large weight means that dimension strongly affects that logit, whereas a weight near zero means it has almost no effect.

### The Gradient at the Hidden State ($\frac{\partial L}{\partial \mathbf{h}}$)

Chaining this local derivative with $\frac{\partial L}{\partial \mathbf{z}}$ yields the gradient of the loss with respect to $\mathbf{h}$. A single embedding coordinate $h_m$ participates in all 8 dot products across $\mathbf{z}$, so the chain rule sums its contributions across all 8 vocabulary indices ($j = 0, \dots, 7$):

$$
\frac{\partial L}{\partial h_m} = \sum_{j=0}^{7} \frac{\partial L}{\partial z_j} \cdot \frac{\partial z_j}{\partial h_m} = \sum_{j=0}^{7} (\hat{y}_j - y_j) \cdot W_{U_{m,j}}
$$

Each term in this sum isolates how much embedding dimension $m$ of `brown`'s vector contributed to the error at vocabulary word $j$. The error at each word ($\hat{y}_j - y_j$) multiplies the weight connecting $h_m$ to that word ($W_{U_{m,j}}$), summed across all 8 vocabulary words.

Computing this sum for all three embedding dimensions ($m = 1, 2, 3$) simultaneously yields the complete hidden-state gradient in matrix notation:

$$
\frac{\partial L}{\partial \mathbf{h}} = (\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T
$$

The transpose $W_U^T$ reverses the direction of the projection. During the forward pass, $W_U$ projected the $3$-dimensional embedding $\mathbf{h}$ *up* into $8$-dimensional vocabulary space to produce the logits. During backpropagation, $W_U^T$ projects the $8$-dimensional error signal *back down* into $3$-dimensional embedding space. The result is a $1 \times 3$ gradient vector that inhabits the same coordinate system as `brown`'s embedding vector, specifying the direction and magnitude needed to nudge `brown`'s vector to reduce the loss.

### Updating $W_U$ Along the Way

Before continuing backward to Layer 1, note that $W_U$ itself contains learnable weights that require updating. Their gradients follow from the same element-wise expansion:

$$
z_j = h_1 \cdot W_{U_{1,j}} + h_2 \cdot W_{U_{2,j}} + h_3 \cdot W_{U_{3,j}}
$$

Differentiating this expression with respect to a specific *weight* $W_{U_{m,j}}$ rather than an embedding coordinate $h_m$ reverses the roles of constants and variables: the embedding coordinates $h_1, h_2, h_3$ act as fixed constants computed during the forward pass, and $W_{U_{m,j}}$ acts as the variable of differentiation.

- **Active Term ($h_m \cdot W_{U_{m,j}}$):** Contains the target variable $W_{U_{m,j}}$, and differentiating a constant multiplied by a variable leaves the constant factor $h_m$.
- **Remaining Terms ($h_n \cdot W_{U_{n,j}}$ for $n \neq m$):** Do not contain $W_{U_{m,j}}$, so their derivatives evaluate to zero.

Only the active term survives differentiation:

$$
\frac{\partial z_j}{\partial W_{U_{m,j}}} = h_m
$$

Applying the chain rule connects this local derivative to the loss gradient:

$$
\frac{\partial L}{\partial W_{U_{m,j}}} = \frac{\partial L}{\partial z_j} \cdot \frac{\partial z_j}{\partial W_{U_{m,j}}} = (\hat{y}_j - y_j) \cdot h_m
$$

Each weight's gradient equals the product of two quantities: the error signal at the vocabulary word it connects to ($\hat{y}_j - y_j$) and the embedding coordinate value that flowed through it during the forward pass ($h_m$). In matrix form across all coordinates and vocabulary words, this outer product is $\frac{\partial L}{\partial W_U} = \mathbf{h}^T \cdot (\hat{\mathbf{y}} - \mathbf{y})$. These updates are applied alongside the $W_E$ updates at the end of the step.

## Propagating Through Layer 1: $\frac{\partial \mathbf{h}}{\partial W_E}$

The backward pass now reaches the first layer, which forms the origin of the forward pass and the final link in the derivative chain. In the forward pass, the hidden state is computed as:

$$
\mathbf{h} = \mathbf{x} \times W_E
$$

where $\mathbf{x} \in \mathbb{R}^{1 \times 8}$ is the one-hot input vector for `brown`. The embedding matrix $W_E \in \mathbb{R}^{8 \times 3}$ contains 8 rows (indexed $i = 0, \dots, 7$, one per vocabulary word) and 3 columns (indexed $m = 1, 2, 3$, one per embedding dimension). Expanding the matrix product element-wise for a single embedding coordinate $h_m$ yields:

$$
h_m = x_0 \cdot W_{E_{0,m}} + x_1 \cdot W_{E_{1,m}} + x_2 \cdot W_{E_{2,m}} + \dots + x_7 \cdot W_{E_{7,m}}
$$

Each term multiplies the one-hot input value at vocabulary index $i$ ($x_0$ for `The`, $x_1$ for `quick`, $x_2$ for `brown`, through $x_7$ for `dog`) by the corresponding weight in row $i$ of $W_E$. Just as in Layer 2, the input values $x_i$ are fixed constants from the one-hot encoding and $W_{E_{i,m}}$ is the variable of differentiation. Only the term containing $W_{E_{i,m}}$ survives differentiation:

$$
\frac{\partial h_m}{\partial W_{E_{i,m}}} = x_i
$$

Applying the chain rule connects this local derivative to the loss gradient $\frac{\partial L}{\partial h_m}$ computed in the previous section:

$$
\frac{\partial L}{\partial W_{E_{i,m}}} = \frac{\partial L}{\partial h_m} \cdot \frac{\partial h_m}{\partial W_{E_{i,m}}} = \frac{\partial L}{\partial h_m} \cdot x_i
$$

The input vector $\mathbf{x}$ is one-hot encoded, so $x_i = 0$ for every vocabulary word except `brown` at index `2`, where $x_2 = 1$. Evaluating each row of $W_E$ reveals a sparse update pattern:

- **Row 0 (`The`, $i = 0$):** $\frac{\partial L}{\partial W_{E_{0,m}}} = 0 \cdot \frac{\partial L}{\partial h_m} = 0$. The gradient is zero, leaving row 0 untouched.
- **Row 1 (`quick`, $i = 1$):** $\frac{\partial L}{\partial W_{E_{1,m}}} = 0 \cdot \frac{\partial L}{\partial h_m} = 0$. The gradient is zero, leaving row 1 untouched.
- **Row 2 (`brown`, $i = 2$):** $\frac{\partial L}{\partial W_{E_{2,m}}} = 1 \cdot \frac{\partial L}{\partial h_m} = \frac{\partial L}{\partial h_m}$. The upstream gradient passes directly into row 2.
- **Rows 3 to 7 (`fox`, `jumps`, `over`, `lazy`, `dog`):** $\frac{\partial L}{\partial W_{E_{i,m}}} = 0 \cdot \frac{\partial L}{\partial h_m} = 0$. All remaining rows receive zero gradient.

This sparse gradient routing mirrors the row-extraction mechanism from the forward pass, operating in reverse. During the forward pass, multiplying by the one-hot vector extracted a single row from $W_E$. During backpropagation, multiplying by the one-hot input deposits the gradient into that same row. Only `brown`'s embedding vector receives an update from this training example; every other word in the vocabulary remains untouched.

## The Weight Update

With the gradient computed end-to-end, the gradient descent weight update rule is applied:

$$
W_{\text{new}} = W_{\text{old}} - \alpha \cdot \nabla L
$$

The scalar $\alpha$ is the **learning rate**, which governs the step size of each parameter update. Applying an unscaled gradient to jump directly to a position that predicts `fox` would corrupt the representation because `brown` does not appear in a single context. Across the training corpus, `brown` precedes `fox`, `bear`, `sugar`, `eyes`, and `shoes`. Each of these contexts generates a different gradient, pulling `brown`'s vector in a different direction in the embedding space.

An oversized learning rate causes each training example to overwrite the previous update, forcing the vector for `brown` to oscillate chaotically instead of settling into a stable position. A small learning rate ensures that each individual example contributes a microscopic nudge. Across millions of iterations, these nudges accumulate statistically: directions that are consistently reinforced across many contexts grow dominant, whereas contradictory or noisy signals cancel out. The converged position of the vector reflects not any single sentence, but the **aggregate statistical geometry** of every context in which `brown` appeared.

Completing this single training step shifts the 3-dimensional vector for `brown` by a fraction of a decimal point. That single change is imperceptible in isolation, yet training executes this identical operation billions of times across every token in the corpus, adjusting every vector that participates in each forward pass. The cumulative effect of these microscopic nudges and the geometric structure that emerges from them form the subject of the next chapter.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
