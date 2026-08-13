# Part 7: The Embedding Tensor and the Limits of Static Representations

<!-- SUMMARY: The single-token lookup of previous chapters is generalized to full sequence processing, producing the embedding tensor for an entire input sequence. The fundamental limits of static embeddings—context-blindness and order-agnosticism—are identified, and the handoff to the Transformer architecture, whose positional encodings and self-attention mechanism resolve exactly these limitations, is established. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter established the convergent geometry and linear substructures that emerge from gradient descent at scale. This chapter examines how these embeddings operate when processing full sequences rather than individual tokens.

Throughout Chapters 1 through 4, a single token was processed at a time. The input was one one-hot vector $\mathbf{x} \in \mathbb{R}^{1 \times 8}$, and the output was one embedding vector $\mathbf{h} \in \mathbb{R}^{1 \times 3}$—a single row extracted from $W_E$. But real language models do not process one word in isolation. They ingest entire sequences. The generalization from single-token lookup to full-sequence processing is natural—and it is the final mechanical step before handing off to the Transformer architecture.

Instead of feeding a single one-hot vector into $W_E$, $T$ one-hot vectors—one per token in the input sequence—are stacked into a matrix. The variable $T$ denotes the **sequence length**: the number of tokens being processed simultaneously.

Consider our full toy sentence: `The` `quick` `brown` `fox`. This is a sequence of $T = 4$ tokens. Each token has a one-hot representation in $\mathbb{R}^{1 \times 8}$ (one element per vocabulary word). Each one-hot vector is constructed individually—`The` places a $1$ at index 0, `quick` at index 1, `brown` at index 2, and `fox` at index 3—then all four are stacked vertically into the **one-hot input matrix**:

$$
X_{\text{one-hot}} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \end{bmatrix}_{4 \times 8}
$$

The first row is the one-hot encoding for `The` (a $1$ at index 0, zeros elsewhere). The second row is `quick` (a $1$ at index 1). The third row is `brown` (index 2), and the fourth row is `fox` (index 3). The shape of this matrix is $T \times V = 4 \times 8$: one row per token in the sequence, one column per word in the vocabulary.

This matrix is then multiplied by the same $W_E \in \mathbb{R}^{8 \times 3}$ from Chapter 3:

$$
X = X_{\text{one-hot}} \times W_E
$$

As established in Chapter 1, multiplying a single one-hot vector by $W_E$ extracts the corresponding row—the dot product with a one-hot vector zeroes out every row except the one where the $1$ appears. The same mechanism applies to each row of $X_{\text{one-hot}}$ independently. The matrix multiply performs all four lookups simultaneously, extracting four rows from $W_E$ in a single operation:

$$
X = \begin{bmatrix} 0.1 & -0.4 & 0.2 \\ 0.5 & 0.1 & -0.8 \\ -0.3 & 0.9 & 0.4 \\ 0.2 & -0.2 & 0.1 \end{bmatrix}_{4 \times 3}
$$

Each row of $X$ is the embedding vector for one token in the sequence:

- Row 0: $\begin{bmatrix} 0.1 & -0.4 & 0.2 \end{bmatrix}$ — the embedding for `The`
- Row 1: $\begin{bmatrix} 0.5 & 0.1 & -0.8 \end{bmatrix}$ — the embedding for `quick`
- Row 2: $\begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}$ — the embedding for `brown`
- Row 3: $\begin{bmatrix} 0.2 & -0.2 & 0.1 \end{bmatrix}$ — the embedding for `fox`

Row 2 is precisely the vector $\mathbf{h} = \begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}$ used throughout Chapters 3 and 4 as the hidden state for `brown`. The sequence operation has not changed the lookup mechanism—it has simply batched it.

The result $X \in \mathbb{R}^{T \times d_{model}}$ is the **embedding tensor** for the input sequence: a matrix of $T$ rows and $d_{model}$ columns, encoding the entire sequence as a block of continuous vectors. In our toy model, this is a $4 \times 3$ matrix. In a production model processing a 512-token sequence with $d_{model} = 512$, this would be a $512 \times 512$ matrix—each of its 512 rows a rich, high-dimensional vector whose position has been shaped by billions of gradient updates into a point that encodes the distributional signature of its token.

## The Limits of Static Geometry

The embedding tensor $X$ is dense, continuous, and semantically structured. Each row carries the distributional signature of its token, distilled from billions of training contexts into $d_{model}$ dimensions. But this representation has two fundamental limitations that no amount of additional training can overcome—because they are structural consequences of using a static, context-independent embedding matrix.

**Context-blindness.** Every occurrence of a word looks up the *same* row of $W_E$, regardless of the surrounding sentence. The word `apple` in "I ate a delicious `apple`" and `apple` in "I bought an `apple` laptop" produce identical embedding vectors. The trained vector for `apple` is a compromise—the geometric center-of-mass of all its usages, capturing some blend of "fruit" and "technology" but faithfully representing neither. This is the **superposition** problem identified at the end of Chapter 3: a single static vector cannot represent multiple distinct meanings.

**Order-agnosticism.** The matrix multiplication $X_{\text{one-hot}} \times W_E$ treats each row of $X_{\text{one-hot}}$ independently. It does not know or care which row comes first. The sequences `dog bites man` and `man bites dog`—which carry very different meanings—produce the *same set* of embedding vectors, merely arranged in different rows of $X$. The embedding matrix has no mechanism to encode word order, because each row's lookup depends only on which vocabulary index contains the $1$—not on the row's position within the sequence.

These limitations are not flaws in the training process. They are inherent to the architecture: a fixed lookup table that maps each word to a single, pre-computed vector cannot incorporate the dynamic context of a specific sentence. Resolving context-dependence and encoding positional information requires a fundamentally different mechanism—one that can examine the *entire* sequence of embedding vectors and dynamically re-weight each one based on its neighbors.

That mechanism is the subject of an entirely different architecture. The embedding tensor $X \in \mathbb{R}^{T \times d_{model}}$—with all its semantic richness and all its limitations—is exactly what enters the **Transformer**. There, positional encodings inject word-order information that the embedding lookup cannot provide, and the self-attention mechanism allows each vector in the sequence to attend to every other vector, dynamically resolving ambiguity and context-dependence on a per-sentence basis. The static geometry built across this series is not the final representation—it is the starting point from which the Transformer begins its work.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
