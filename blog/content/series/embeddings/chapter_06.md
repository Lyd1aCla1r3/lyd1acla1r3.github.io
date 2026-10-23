# Part 6: Convergent Geometry and Linear Substructures

<!-- SUMMARY: The cumulative effect of billions of microscopic gradient updates on the embedding matrix reveals how distributional statistics organically produce semantic geometry. The emergent property (linear substructures where vector arithmetic captures semantic relationships) is demonstrated through concrete worked examples. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

Completing a single training step shifts the vector for `brown` by a fraction of a decimal point. One gradient, computed from one sentence, adjusts three coordinates by a microscopic amount. This update operation repeats across every sentence in the training corpus; every token that participates in a forward pass has its embedding vector nudged by the resulting gradient. A corpus of billions of words produces billions of gradient updates, each applying a tiny push in the embedding space. This chapter traces the cumulative effect of those pushes and the geometric structure that emerges from them.

## From One Nudge to a Million

Chapters 4 and 5 derived the gradient for a single training example: the sequence `The` `quick` `brown` predicting `fox`. That gradient adjusted a single row of $W_E$ (row `2`, corresponding to `brown`) in a direction that makes the network slightly more likely to predict `fox` in this context.

Across a large training corpus, `brown` does not appear solely before `fox`; it precedes thousands of distinct words:

- **`brown` `fox`:** The toy corpus example traced in Chapters 3 through 5.
- **`brown` `bear`:** A different animal noun sharing animate action contexts.
- **`brown` `sugar`:** A culinary ingredient appearing in food contexts.
- **`brown` `eyes`:** A physical trait appearing in descriptive contexts.
- **`brown` `shoes`:** An article of clothing appearing in apparel contexts.

Each of these contexts executes the pipeline from Chapters 4 and 5: a forward pass produces a prediction, the loss measures the error, and backpropagation computes a gradient $\frac{\partial L}{\partial \mathbf{h}} = (\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T$ that nudges `brown`'s vector. Each context produces a *different* gradient because the target word changes and the error signal $\hat{\mathbf{y}} - \mathbf{y}$ points in a different direction.

The learning rate $\alpha$ prevents any single gradient from dominating. Each individual nudge is microscopic. Across millions of iterations, these nudges accumulate *statistically*: gradient components that are consistently reinforced across many different contexts grow dominant, whereas components that point in contradictory directions cancel out. The converged position of `brown`'s vector is determined not by any single sentence, but by the aggregate statistics of every context in which `brown` appeared.

This statistical accumulation realizes the distributional hypothesis introduced in Chapter 3. Chapters 3, 4, and 5 establish the mechanism by which a neural network discovers this principle automatically: gradient descent, applied at scale, forces words with similar contextual distributions into neighboring regions of the embedding space. No explicit definition of meaning is ever provided to the network; meaning emerges as a geometric side effect of next-token prediction.

## Convergent Geometry

The distributional hypothesis explains both why a single word's vector stabilizes and why *different* words converge toward one another.

Consider two animal nouns from the toy vocabulary: `fox` and `dog`. Across a large corpus, both words frequently precede the same target words:

- **Shared Action Context:** `The` **`fox`** `jumps over the fence` / `The` **`dog`** `jumps over the fence`
- **Shared Observation Context:** `A wild` **`fox`** `appeared nearby` / `A wild` **`dog`** `appeared nearby`
- **Shared Passive Context:** `The` **`fox`** `was spotted nearby` / `The` **`dog`** `was spotted nearby`

This contextual overlap has a direct mathematical consequence. Tracing the gradient formula from Chapters 4 and 5 across two training examples that share `jumps` (index `4` in the toy vocabulary) as their target word demonstrates how shared contexts align gradient updates.

### Example 1: Context Token `fox` Predicting `jumps`

The network executes the forward pass from Chapter 3 by extracting `fox`'s embedding from $W_E$, projecting through $W_U$, and applying Softmax to produce a predicted probability distribution. Suppose the network outputs:

$$
\hat{\mathbf{y}}_{\text{fox}} = \begin{bmatrix} 0.05 & 0.05 & 0.05 & 0.10 & 0.30 & 0.20 & 0.10 & 0.15 \end{bmatrix}
$$

The network assigns $30\%$ probability to `jumps` at index `4`. The ground truth $\mathbf{y}$ is a one-hot vector with a $1$ at index `4` and $0$ everywhere else. Computing the error signal $\hat{\mathbf{y}} - \mathbf{y}$ from Chapter 4 element by element yields:

$$
\hat{\mathbf{y}}_{\text{fox}} - \mathbf{y} = \begin{bmatrix} 0.05 & 0.05 & 0.05 & 0.10 & \mathbf{-0.70} & 0.20 & 0.10 & 0.15 \end{bmatrix}
$$

Seven of the eight components are small positive numbers (the largest is $0.20$ for `over`). The eighth component at index `4` (the target word `jumps`) evaluates to $0.30 - 1 = -0.70$, a large negative value whose magnitude is more than three times larger than any other entry.

### Example 2: Context Token `dog` Predicting `jumps`

In a second sentence, `dog` serves as the input token. Distinct weights in `dog`'s embedding row cause the forward pass to produce a different probability distribution:

$$
\hat{\mathbf{y}}_{\text{dog}} = \begin{bmatrix} 0.08 & 0.03 & 0.07 & 0.12 & 0.25 & 0.15 & 0.12 & 0.18 \end{bmatrix}
$$

Sharing the target word `jumps` means $\mathbf{y}$ remains the identical one-hot vector with $1$ at index `4`:

$$
\hat{\mathbf{y}}_{\text{dog}} - \mathbf{y} = \begin{bmatrix} 0.08 & 0.03 & 0.07 & 0.12 & \mathbf{-0.75} & 0.15 & 0.12 & 0.18 \end{bmatrix}
$$

The individual predictions differ, yet the structure of the error signal matches: seven small positive values and one dominant negative value at index `4`. The largest component sits at the same index in both examples because both sentences share the target word `jumps`.

### From Error Signal to Gradient Direction

The gradient that updates each input token's embedding is $(\hat{\mathbf{y}} - \mathbf{y}) \cdot W_U^T$, where $W_U^T \in \mathbb{R}^{8 \times 3}$ is the transpose of the $3 \times 8$ un-embedding matrix. This matrix multiplication computes a weighted sum of the rows of $W_U^T$, where the eight components of $\hat{\mathbf{y}} - \mathbf{y}$ serve as the scalar weights. Let $\mathbf{r}_j \in \mathbb{R}^{1 \times 3}$ denote row $j$ of $W_U^T$, representing vocabulary word $j$'s un-embedding weights. Expanding the gradient for the `fox` example yields:

$$
\frac{\partial L}{\partial \mathbf{h}_{\text{fox}}} = 0.05 \cdot \mathbf{r}_0 + 0.05 \cdot \mathbf{r}_1 + 0.05 \cdot \mathbf{r}_2 + 0.10 \cdot \mathbf{r}_3 - 0.70 \cdot \mathbf{r}_4 + 0.20 \cdot \mathbf{r}_5 + 0.10 \cdot \mathbf{r}_6 + 0.15 \cdot \mathbf{r}_7
$$

This linear combination sums eight 3-dimensional vectors scaled by their error coefficients. The term $-0.70 \cdot \mathbf{r}_4$ dominates the sum: its coefficient has the largest magnitude by a factor of more than three, and it is the only negative term. The vector $\mathbf{r}_4$ (the un-embedding weights for `jumps`) therefore governs the resulting gradient direction.

Expanding the `dog` example produces the same structural dominance:

$$
\frac{\partial L}{\partial \mathbf{h}_{\text{dog}}} = 0.08 \cdot \mathbf{r}_0 + 0.03 \cdot \mathbf{r}_1 + 0.07 \cdot \mathbf{r}_2 + 0.12 \cdot \mathbf{r}_3 - 0.75 \cdot \mathbf{r}_4 + 0.15 \cdot \mathbf{r}_5 + 0.12 \cdot \mathbf{r}_6 + 0.18 \cdot \mathbf{r}_7
$$

The same row $\mathbf{r}_4$ dominates with a comparably large negative coefficient ($-0.75$ versus $-0.70$). Small positive contributions differ slightly between the two examples, yet the dominant pull along $\mathbf{r}_4$ (determined by the shared target `jumps`) aligns both gradients in nearly the same direction.

The words `fox` and `dog` share numerous target words across the corpus, including `jumps`, `runs`, `sleeps`, and `was`. Each shared target places the dominant component of the error signal at the same index, pulling both gradients along the same row of $W_U^T$. Across millions of training examples, these aligned pushes accumulate, drawing `fox`'s and `dog`'s vectors toward the same region of the embedding space. Conversely, words that rarely share targets (such as `fox` and `over`) receive error signals whose dominant components sit at different indices, producing divergent gradients that keep their vectors separated.

This process produces **semantic clustering**: after training, the embedding space is no longer the featureless, isotropic shell described in Chapter 2. Animals cluster near other animals, verbs cluster near other verbs, and color adjectives cluster near other color adjectives. None of this taxonomy was programmed into the network; it emerged from the co-occurrence statistics of the training data through the gradient descent updates derived in Chapters 4 and 5.

## Measuring the Geometry

Evaluating claims such as "`fox` and `dog` converge in the embedding space" requires quantifying the geometric alignment between two vectors. The standard metric is **cosine similarity**, which measures the cosine of the angle between two vectors in $d$-dimensional space.

### The Formula

Given two vectors $\mathbf{a}$ and $\mathbf{b}$, each with $d$ dimensions, their **dot product** is defined as the sum of the element-wise products across corresponding coordinates:

$$
\mathbf{a} \cdot \mathbf{b} = \sum_{m=1}^{d} a_m \cdot b_m
$$

The calculation also requires each vector's **magnitude** (its Euclidean norm), which measures the length of the vector in $d$-dimensional space:

$$
\|\mathbf{a}\| = \sqrt{\sum_{m=1}^{d} a_m^2}
$$

Cosine similarity divides the dot product by the product of the two magnitudes. This normalization removes the effect of vector length, isolating the directional alignment between the two vectors:

$$
\cos(\mathbf{a}, \mathbf{b}) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \cdot \|\mathbf{b}\|}
$$

The ratio produces a single scalar bounded between $-1$ and $+1$:

- **Aligned Vectors ($+1$):** Point in the identical direction, indicating maximum directional similarity.
- **Orthogonal Vectors ($0$):** Meet at a $90^\circ$ angle, indicating zero directional relationship.
- **Opposite Vectors ($-1$):** Point in diametrically opposed directions, indicating maximum directional dissimilarity.

### A Concrete Computation

To ground this formula in the 3-dimensional toy model, suppose billions of gradient updates have converged the vectors for `fox` and `dog` to the following coordinates:

$$
\mathbf{v}_{\text{fox}} = \begin{bmatrix} 0.9 & -0.4 & 0.3 \end{bmatrix}, \quad \mathbf{v}_{\text{dog}} = \begin{bmatrix} 0.7 & -0.1 & 0.5 \end{bmatrix}
$$

1. **Dot Product:** Multiply each pair of corresponding dimensions and sum the products:

$$
\mathbf{v}_{\text{fox}} \cdot \mathbf{v}_{\text{dog}} = (0.9)(0.7) + (-0.4)(-0.1) + (0.3)(0.5) = 0.63 + 0.04 + 0.15 = 0.82
$$

2. **Euclidean Magnitudes:** Square each coordinate, sum the squares, and extract the square root:

$$
\|\mathbf{v}_{\text{fox}}\| = \sqrt{0.9^2 + (-0.4)^2 + 0.3^2} = \sqrt{0.81 + 0.16 + 0.09} = \sqrt{1.06} \approx 1.030
$$

$$
\|\mathbf{v}_{\text{dog}}\| = \sqrt{0.7^2 + (-0.1)^2 + 0.5^2} = \sqrt{0.49 + 0.01 + 0.25} = \sqrt{0.75} \approx 0.866
$$

3. **Cosine Similarity:** Divide the dot product by the product of the two magnitudes:

$$
\cos(\mathbf{v}_{\text{fox}}, \mathbf{v}_{\text{dog}}) = \frac{0.82}{1.030 \times 0.866} = \frac{0.82}{0.892} \approx 0.92
$$

A cosine similarity of $0.92$ (near the maximum of $+1.0$) reflects the fact that both words are animal nouns appearing in strongly overlapping contexts. That alignment contrasts sharply with the initialization state derived in Chapter 2, where randomly initialized vectors in high-dimensional space start out mutually orthogonal with cosine similarities near $0.0$. Training transforms the isotropic initialization shell into a geometric manifold where directional proximity encodes semantic similarity.

## Linear Substructures

Beyond semantic clustering, the emergent geometry of trained embeddings exhibits **linear substructures**, where vector addition and subtraction capture semantic and syntactic analogies.

A classic demonstration involves the words `king`, `queen`, `man`, and `woman`. Those four words lie outside the 8-word toy vocabulary, yet the geometric relationship they illustrate emerges in any embedding space trained on a sufficiently large corpus, where the following vector arithmetic holds to a close approximation:

$$
\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}} + \mathbf{v}_{\text{woman}} \approx \mathbf{v}_{\text{queen}}
$$

The difference $\mathbf{v}_{\text{king}} - \mathbf{v}_{\text{man}}$ defines a **displacement vector** pointing from `man`'s coordinates to `king`'s coordinates in the embedding space. Subtracting $\mathbf{v}_{\text{man}}$ cancels the shared masculine and human attributes while isolating the concept of royalty as a spatial direction and magnitude. Adding that same displacement vector to $\mathbf{v}_{\text{woman}}$ translates `woman`'s coordinates along the royalty axis, arriving near the converged position of `queen` in the embedding space.

This relational geometry extends across the vocabulary. Trained embedding spaces organize consistent linear substructures along numerous semantic and grammatical axes:

- **Gender Axis:** Encodes gender offsets where $\mathbf{v}_{\text{brother}} - \mathbf{v}_{\text{sister}} \approx \mathbf{v}_{\text{king}} - \mathbf{v}_{\text{queen}}$.
- **Verb Tense Axis:** Encodes temporal inflections where $\mathbf{v}_{\text{walking}} - \mathbf{v}_{\text{walked}} \approx \mathbf{v}_{\text{swimming}} - \mathbf{v}_{\text{swam}}$.
- **Capital-Country Axis:** Encodes geopolitical relationships where $\mathbf{v}_{\text{Paris}} - \mathbf{v}_{\text{France}} \approx \mathbf{v}_{\text{Tokyo}} - \mathbf{v}_{\text{Japan}}$.

None of these linear relationships were explicitly programmed. No loss function instructed the network to encode gender as a linear direction or verb tense as a constant vector offset. These substructures emerged from the distributional statistics of the training corpus through the gradient descent process from Chapters 4 and 5, applying the $(\hat{\mathbf{y}} - \mathbf{y})$ error signal billions of times under the next-token prediction objective.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
