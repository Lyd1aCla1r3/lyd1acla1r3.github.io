# Part 7: The Embedding Tensor and the Limits of Static Representations

<!-- SUMMARY: The single-token lookup of previous chapters is generalized to full sequence processing, producing the embedding tensor for an entire input sequence. The fundamental limits of static embeddings (context-blindness and order-agnosticism) are identified, establishing the architectural handoff to the Transformer's positional encodings and self-attention mechanism. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter established the convergent geometry and linear substructures that emerge from gradient descent at scale. This final chapter examines how static embeddings operate when processing full token sequences rather than isolated words.

## From Single-Token Lookup to the Sequence Tensor

Throughout Chapters 1 through 6, the network processed a single token at a time. The input was one one-hot row vector $\mathbf{x} \in \mathbb{R}^{1 \times 8}$, and the output was one embedding vector $\mathbf{h} \in \mathbb{R}^{1 \times 3}$ extracted from a single row of $W_E$. Production language models do not process words in isolation; they ingest entire token sequences simultaneously. Generalizing from single-token lookup to full-sequence processing is the final mechanical step before handing the representation off to the Transformer architecture.

Instead of feeding a single one-hot vector into $W_E$, the lookup stacks $T$ one-hot vectors (one per token in the input sequence) into a matrix. The variable $T$ denotes the **sequence length**, representing the number of tokens processed in parallel.

Consider the full toy sequence `The` `quick` `brown` `fox`, which has a sequence length of $T = 4$ tokens. Each token maps to a one-hot row vector in $\mathbb{R}^{1 \times 8}$ (one column per vocabulary word). Constructing each one-hot vector individually places a $1$ at index `0` for `The`, index `1` for `quick`, index `2` for `brown`, and index `3` for `fox`. Stacking all four vectors vertically produces the **one-hot input matrix**:

$$
X_{\text{one-hot}} = \begin{bmatrix} 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \end{bmatrix}_{4 \times 8}
$$

The first row holds the one-hot encoding for `The` (a $1$ at index `0`, zeros elsewhere), the second row encodes `quick` (index `1`), the third row encodes `brown` (index `2`), and the fourth row encodes `fox` (index `3`). The resulting matrix has shape $T \times V = 4 \times 8$: one row per token in the sequence, and one column per word in the vocabulary.

### Batched Row Extraction

Multiplying the one-hot input matrix by the embedding matrix $W_E \in \mathbb{R}^{8 \times 3}$ from Chapter 3 projects the entire sequence into the continuous space:

$$
X = X_{\text{one-hot}} \times W_E
$$

Chapter 1 established that multiplying a single one-hot vector by $W_E$ extracts the corresponding row because the vector-matrix product zeroes out every row except the index where the $1$ appears. Matrix multiplication applies that identical extraction to each row of $X_{\text{one-hot}}$ independently, retrieving four rows from $W_E$ in a single batched operation:

$$
X = \begin{bmatrix} 0.1 & -0.4 & 0.2 \\ 0.5 & 0.1 & -0.8 \\ -0.3 & 0.9 & 0.4 \\ 0.2 & -0.2 & 0.1 \end{bmatrix}_{4 \times 3}
$$

Each row of $X$ holds the $3$-dimensional embedding vector for the corresponding token in the sequence:

| Sequence Row | Token | Vocabulary Index | Extracted Embedding Vector |
| :--- | :--- | :--- | :--- |
| **Row 0** | `The` | Index `0` | `[0.1, -0.4, 0.2]` |
| **Row 1** | `quick` | Index `1` | `[0.5, 0.1, -0.8]` |
| **Row 2** | `brown` | Index `2` | `[-0.3, 0.9, 0.4]` |
| **Row 3** | `fox` | Index `3` | `[0.2, -0.2, 0.1]` |

Row `2` recovers the vector $\mathbf{h} = \begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}$ used throughout Chapters 1 and 3 through 5 as the hidden state for `brown`. Batching the sequence operation leaves the underlying lookup mechanism unchanged.

The resulting matrix $X \in \mathbb{R}^{T \times d_{\text{model}}}$ is the **embedding tensor** for the input sequence: a grid of $T$ rows and $d_{\text{model}}$ columns encoding the full sequence as a block of continuous vectors. In the toy model, $X$ is a $4 \times 3$ matrix. In a larger model processing a 512-token sequence with $d_{\text{model}} = 512$, the tensor $X$ forms a $512 \times 512$ matrix where each of the 512 rows holds a high-dimensional vector shaped by billions of gradient updates to encode the distributional signature of its token.

## The Limits of Static Geometry

The embedding tensor $X$ is dense, continuous, and semantically structured. Each row carries the distributional signature of its token, distilled from billions of training contexts into $d_{\text{model}}$ dimensions. Static, context-independent lookup tables nevertheless impose two structural limitations that no amount of additional training can overcome.

### Limitation 1: Context-Blindness (Polysemy)

Every occurrence of a word extracts the identical row of $W_E$, regardless of the surrounding sentence. The word `apple` in *"The chef sliced a crisp apple"* and `apple` in *"The engineer opened an apple laptop"* produce identical embedding vectors. The trained vector for `apple` settles into a geometric compromise at the center of mass of all its usages, blending fruit and consumer technology without isolating either meaning. That static compromise is the **superposition** bottleneck identified at the end of Chapter 3: a single fixed vector cannot represent multiple distinct meanings across shifting contexts.

### Limitation 2: Order-Agnosticism (Positional Blindness)

The matrix multiplication $X_{\text{one-hot}} \times W_E$ treats each row of $X_{\text{one-hot}}$ independently without recording sequence order. The clauses `dog bites man` and `man bites dog` carry opposite meanings yet produce the identical set of three embedding vectors, merely permuted across the rows of $X$. The embedding matrix has no mechanism to encode word order because each row lookup depends solely on which vocabulary column contains the $1$, not on the row's position within the sequence.

### Handoff to the Transformer Architecture

These two limitations are not flaws in the gradient descent training process; they are inherent to any architecture that maps each vocabulary token to a single pre-computed vector. Resolving polysemy and encoding word order require a mechanism that inspects the entire sequence of embedding vectors and dynamically re-weights each token representation based on its neighbors.

The [Transformer architecture](series-transformers.html) provides that contextualization mechanism. The embedding tensor $X \in \mathbb{R}^{T \times d_{\text{model}}}$, carrying both its semantic geometry and its static limitations, serves as the direct input to the Transformer. [Positional encodings](series-positional-encoding.html) first inject sequence-order information that the embedding lookup cannot provide, and the self-attention mechanism then allows each vector in the sequence to attend to every other vector, dynamically resolving ambiguity and context-dependence on a per-sentence basis. The static geometry derived across this series is not the final representation; it is the foundational coordinate space from which the Transformer begins its work.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
