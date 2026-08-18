# Part 6: Convergent Geometry and Linear Substructures

<!-- SUMMARY: The cumulative effect of billions of microscopic gradient updates on the embedding matrix reveals how distributional statistics organically produce semantic geometry. The emergent property (linear substructures where vector arithmetic captures semantic relationships) is demonstrated through concrete worked examples. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

After a single training step, the vector for `brown` has shifted by a fraction of a decimal point. One gradient, computed from one sentence, adjusts three numbers by a microscopic amount. This operation repeats across every sentence in the training corpus; every token that participates in a forward pass has its embedding vector nudged by the resulting gradient. A corpus of billions of words means billions of gradient updates, each one a tiny push in the embedding space. This chapter traces the cumulative effect of those pushes—and the geometric structure that organically emerges from them.

## From One Nudge to a Million

In Chapters 4 and 5, the gradient was derived for a single training example: the sequence `The` `quick` `brown` predicting `fox`. That gradient adjusted exactly one row of $W_E$—the row for `brown`—in a direction that would make the network slightly more likely to predict `fox` in this context.

But `brown` does not appear only before `fox`. Across a large training corpus, `brown` precedes thousands of different words:

- `brown` `fox` — our toy example
- `brown` `bear` — a different animal
- `brown` `sugar` — a food ingredient
- `brown` `eyes` — a physical description
- `brown` `shoes` — an article of clothing

Each of these contexts runs the same pipeline from Chapter 4: a forward pass produces a prediction, the loss measures the error, and backpropagation computes a gradient $\frac{\partial L}{\partial \mathbf{h}} = (\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T$ that nudges `brown`'s vector. But each context produces a *different* gradient, because the target word is different and the error signal $\hat{\mathbf{y}} - \mathbf{y}$ points in a different direction.

The learning rate $\alpha$ ensures that no single gradient dominates. Each individual nudge is microscopic. Over millions of iterations, these nudges accumulate *statistically*: gradient components that are consistently reinforced across many different contexts grow dominant, while components that point in contradictory directions cancel out. The final position of `brown`'s vector is not determined by any single sentence—it is the aggregate result of every context in which `brown` ever appeared.

This is a mathematical realization of the distributional hypothesis introduced in Chapter 3. Chapters 3, 4, and 5 demonstrate the precise mechanism by which a neural network discovers this principle on its own: gradient descent, applied at scale, forces words with similar contextual distributions into similar regions of the embedding space. No explicit notion of "meaning" is ever provided to the network. Meaning emerges as a geometric side effect of learning to predict the next word.

## Convergent Geometry

The distributional hypothesis does not only explain why a single word's vector stabilizes—it explains why *different* words end up near each other.

Consider two words from our toy vocabulary: `fox` and `dog`. Both are animals. In a large corpus, when they appear as the input token, they frequently predict the same next words:

<ul>
<li><code>The</code> <b><code>fox</code></b> <code>jumps over the fence</code> / <code>The</code> <b><code>dog</code></b> <code>jumps over the fence</code></li>
<li><code>A wild</code> <b><code>fox</code></b> <code>appeared nearby</code> / <code>A wild</code> <b><code>dog</code></b> <code>appeared nearby</code></li>
<li><code>The</code> <b><code>fox</code></b> <code>was spotted nearby</code> / <code>The</code> <b><code>dog</code></b> <code>was spotted nearby</code></li>
</ul>

This overlap has a direct mathematical consequence. To see it precisely, the gradient formula from Chapters 4 and 5 is traced for two specific training examples, both using `jumps` (index 4 in our toy vocabulary) as the shared target.

**Example 1: `fox` as input, predicting `jumps`.** The network runs the forward pass from Chapter 3—extracting `fox`'s embedding from $W_E$, projecting through $W_U$, and applying Softmax—to produce a predicted probability distribution. Suppose the network outputs:

$$
\hat{\mathbf{y}}_{fox} = \begin{bmatrix} 0.05 & 0.05 & 0.05 & 0.10 & 0.30 & 0.20 & 0.10 & 0.15 \end{bmatrix}
$$

The network assigns $30\%$ probability to `jumps` at index 4. The ground truth $\mathbf{y}$ is a one-hot vector with a $1$ at index 4 and $0$ everywhere else. Computing the error signal $\hat{\mathbf{y}} - \mathbf{y}$ from Chapter 4 element by element:

$$
\hat{\mathbf{y}}_{fox} - \mathbf{y} = \begin{bmatrix} 0.05 & 0.05 & 0.05 & 0.10 & \mathbf{-0.70} & 0.20 & 0.10 & 0.15 \end{bmatrix}
$$

Seven of the eight components are small positive numbers (the largest is $0.20$ for `over`). The eighth—at index 4, the correct answer `jumps`—is $0.30 - 1 = -0.70$: a large negative value whose magnitude is more than three times larger than any other component.

**Example 2: `dog` as input, also predicting `jumps`.** In a different sentence, `dog` is the input token. Because `dog`'s embedding is different from `fox`'s, the forward pass produces a different prediction:

$$
\hat{\mathbf{y}}_{dog} = \begin{bmatrix} 0.08 & 0.03 & 0.07 & 0.12 & 0.25 & 0.15 & 0.12 & 0.18 \end{bmatrix}
$$

But the target is the same word `jumps`, so $\mathbf{y}$ is the same one-hot vector:

$$
\hat{\mathbf{y}}_{dog} - \mathbf{y} = \begin{bmatrix} 0.08 & 0.03 & 0.07 & 0.12 & \mathbf{-0.75} & 0.15 & 0.12 & 0.18 \end{bmatrix}
$$

The individual predictions differ, but the structure of the error signal is the same: seven small positive values, and one large negative value at index 4. The dominant component sits at the same index in both cases, because both examples share the same target word.

**From error signal to gradient direction.** The gradient that updates each input token's embedding is $(\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T$. Recall that $W_U^T$ is an $8 \times 3$ matrix (the transpose of our $3 \times 8$ un-embedding matrix). This matrix multiply computes a weighted sum of the rows of $W_U^T$, where the eight components of $\hat{\mathbf{y}} - \mathbf{y}$ serve as the weights. Let $\mathbf{r}_j$ denote row $j$ of $W_U^T$—a 3-dimensional vector representing vocabulary word $j$'s un-embedding weights. Expanding the `fox` example:

$$
\frac{\partial L}{\partial \mathbf{h}_{fox}} = 0.05 \cdot \mathbf{r}_0 + 0.05 \cdot \mathbf{r}_1 + 0.05 \cdot \mathbf{r}_2 + 0.10 \cdot \mathbf{r}_3 - 0.70 \cdot \mathbf{r}_4 + 0.20 \cdot \mathbf{r}_5 + 0.10 \cdot \mathbf{r}_6 + 0.15 \cdot \mathbf{r}_7
$$

This is a sum of eight 3-dimensional vectors, each scaled by its coefficient. The term $-0.70 \cdot \mathbf{r}_4$ dominates the sum: its coefficient has the largest magnitude by a factor of more than three, and it is the only negative term. The gradient direction is therefore determined primarily by $\mathbf{r}_4$—the un-embedding weights for `jumps`.

For the `dog` example, the same expansion gives:

$$
\frac{\partial L}{\partial \mathbf{h}_{dog}} = 0.08 \cdot \mathbf{r}_0 + 0.03 \cdot \mathbf{r}_1 + 0.07 \cdot \mathbf{r}_2 + 0.12 \cdot \mathbf{r}_3 - 0.75 \cdot \mathbf{r}_4 + 0.15 \cdot \mathbf{r}_5 + 0.12 \cdot \mathbf{r}_6 + 0.18 \cdot \mathbf{r}_7
$$

The same row $\mathbf{r}_4$ dominates, with a similarly large negative coefficient ($-0.75$ vs. $-0.70$). The small positive contributions differ between the two examples, but the dominant direction—determined by the shared target `jumps` through $\mathbf{r}_4$—is the same. Both gradients push both embeddings in approximately the same direction.

The words `fox` and `dog` share *many* targets across the corpus: `jumps`, `runs`, `sleeps`, `was`, and countless others. Each shared target places the dominant component of the error signal at the same index, causing both gradients to be pulled through the same row of $W_U^T$. Over millions of training examples, these consistent pushes accumulate, pulling `fox`'s and `dog`'s vectors toward the same region of the embedding space. Meanwhile, words that rarely share targets—like `fox` and `over`—receive error signals whose dominant components sit at different indices, producing dissimilar gradients that keep their vectors distant.

The result is **semantic clustering**: after training, the embedding space is no longer the featureless, isotropic expanse described in Chapter 2. It has acquired structure. Animals cluster near other animals. Verbs cluster near other verbs. Adjectives describing color cluster near other color adjectives. None of this structure was programmed into the network—it emerged organically from the statistics of the training data, mediated entirely by the gradient descent process derived in Chapters 4 and 5.

## Measuring the Geometry

To make precise claims like "`fox` and `dog` are close in the embedding space," the geometric relationship between two vectors must be quantified. The standard metric is **cosine similarity**, which measures the cosine of the angle between two vectors in $d$-dimensional space.

### The Formula

Given two vectors $\mathbf{a}$ and $\mathbf{b}$, each with $d$ dimensions, their **dot product** is first defined as the element-wise product of corresponding dimensions, summed into a single scalar:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{m=1}^{d} a_m \cdot b_m
$$

Each vector's **magnitude** (its Euclidean norm) is also required—the length of the vector in $d$-dimensional space:

$$
\|\mathbf{a}\| = \sqrt{\sum_{m=1}^{d} a_m^2}
$$

Cosine similarity divides the dot product by the product of the two magnitudes. This normalization removes the effect of vector length, isolating the purely directional relationship between the two vectors:

$$
\cos(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \cdot \|\mathbf{b}\|}
$$

The result is a single scalar between $-1$ and $+1$:

- **$+1$**: The vectors point in exactly the same direction. Maximum similarity.
- **$0$**: The vectors are perpendicular (orthogonal). No directional relationship.
- **$-1$**: The vectors point in exactly opposite directions. Maximum dissimilarity.

### A Concrete Computation

To ground this formula in our toy model, consider two hypothetical post-training vectors. After billions of gradient updates, suppose the 3-dimensional vectors for `fox` and `dog` have settled at:

$$
\mathbf{v}_{fox} = \begin{bmatrix} 0.9 & -0.4 & 0.3 \end{bmatrix}, \quad \mathbf{v}_{dog} = \begin{bmatrix} 0.7 & -0.1 & 0.5 \end{bmatrix}
$$

**Dot product** — multiply each pair of corresponding dimensions and sum:

$$
\mathbf{v}_{fox} \cdot \mathbf{v}_{dog} = (0.9)(0.7) + (-0.4)(-0.1) + (0.3)(0.5) = 0.63 + 0.04 + 0.15 = 0.82
$$

**Magnitudes** — square each dimension, sum, and take the square root:

$$
\|\mathbf{v}_{fox}\| = \sqrt{0.9^2 + (-0.4)^2 + 0.3^2} = \sqrt{0.81 + 0.16 + 0.09} = \sqrt{1.06} \approx 1.030
$$

$$
\|\mathbf{v}_{dog}\| = \sqrt{0.7^2 + (-0.1)^2 + 0.5^2} = \sqrt{0.49 + 0.01 + 0.25} = \sqrt{0.75} \approx 0.866
$$

**Cosine similarity** — divide the dot product by the product of the magnitudes:

$$
\cos(\mathbf{v}_{fox}, \mathbf{v}_{dog}) = \frac{0.82}{1.030 \times 0.866} = \frac{0.82}{0.892} \approx 0.92
$$

A cosine similarity of $0.92$—close to the maximum of $+1.0$—reflects the fact that both words are animals that appear in highly overlapping contexts. This contrasts with the result from Chapter 2: at initialization, randomly initialized vectors in high-dimensional space are mutually orthogonal, with cosine similarities near $0.0$. Training transforms the geometry into a space where semantic relationships are encoded as directional proximity.

## Linear Substructures

Beyond semantic clustering, the emergent geometry of trained embeddings exhibits **linear substructures**, where simple vector arithmetic captures semantic and syntactic relationships.

The most famous example involves the words `king`, `queen`, `man`, and `woman`. These four words are not in the 8-word toy vocabulary, but the phenomenon they illustrate emerges in any embedding space trained on a sufficiently large corpus. After training, the following vector arithmetic holds to a close approximation:

$$
\mathbf{v}_{king} - \mathbf{v}_{man} + \mathbf{v}_{woman} \approx \mathbf{v}_{queen}
$$

The difference $\mathbf{v}_{king} - \mathbf{v}_{man}$ is a **displacement vector**—an arrow pointing from `man`'s position to `king`'s position in the embedding space. This displacement captures everything that distinguishes `king` from `man` while discarding everything they share. What remains is, approximately, the concept of royalty—encoded as a direction and magnitude in the vector space. Adding this same displacement to $\mathbf{v}_{woman}$ translates `woman`'s position along the "royalty" direction, arriving at a point that combines "woman" with "royalty." That point is, approximately, where `queen` sits in the embedding space.

This is not an isolated curiosity. Trained embedding spaces exhibit consistent linear substructures along many different axes:

- **Gender**: $\mathbf{v}_{brother} - \mathbf{v}_{sister} \approx \mathbf{v}_{king} - \mathbf{v}_{queen}$
- **Tense**: $\mathbf{v}_{walking} - \mathbf{v}_{walked} \approx \mathbf{v}_{swimming} - \mathbf{v}_{swam}$
- **Geography**: $\mathbf{v}_{Paris} - \mathbf{v}_{France} \approx \mathbf{v}_{Tokyo} - \mathbf{v}_{Japan}$

None of these relationships were explicitly programmed. No loss function asked the network to encode gender as a linear direction, or verb tense as a consistent vector offset. They emerged purely from the distributional statistics of the training corpus—the same gradient descent process from Chapters 4 and 5, operating on the same $(\hat{\mathbf{y}} - \mathbf{y})$ error signal, applied billions of times. The training objective was simply next-token prediction. The geometric structure is a side effect.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
