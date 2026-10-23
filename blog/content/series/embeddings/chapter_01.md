# Part 1: One-Hot Encoding and the Embedding Matrix

<style>
  .trace-container b code {
    font-weight: 900 !important;
    color: #9a5b65 !important;
    background-color: #fdf5f6 !important;
    border: 1px solid #e0c6cb !important;
    border-radius: 0.4em !important;
  }
  @media (prefers-color-scheme: dark) {
    .trace-container b code {
      color: #e6b3bc !important;
      background-color: #3b2a2d !important;
      border: 1px solid #6b4d53 !important;
      border-radius: 0.4em !important;
    }
  }
</style>

<!-- SUMMARY: Tokenization translates raw text into discrete integer identifiers, but neural networks require continuous representations to perform calculus. The embedding matrix solves this by projecting each discrete token into a high-dimensional vector space via one-hot encoding multiplication, acting as a dense lookup table. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The preceding [Tokenization series](series-tokenization.html) established the mathematical process of transforming variable, unstructured text into discrete integer sequences. Subword compression algorithms such as Byte Pair Encoding parse raw text into a finite, fixed-size vocabulary where every entry maps to a unique integer index.

Applying this vocabulary lookup to the 8-word toy corpus introduced in the Preface (`The` `quick` `brown` `fox` `jumps` `over` `lazy` `dog`, where $V = 8$) maps each word to a 0-indexed integer identifier from `0` through `7`. Extracting two adjectives from that vocabulary yields two discrete integer IDs:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<b><code>brown</code></b> (ID: 2) &nbsp;&nbsp; <b><code>lazy</code></b> (ID: 6)
</div>

The tokenization pipeline terminates at these integer assignments. Passing the raw integers `2` and `6` directly into a neural network creates an immediate mathematical contradiction.

## The Problem with Discrete Integers

Deep learning models operate through continuous mathematics: matrix multiplication, calculus, and gradient descent. Discrete integer IDs function purely as categorical lookup keys and possess no intrinsic algebraic magnitude or metric distance.

Feeding the integer IDs `2` and `6` directly into a linear layer forces the network to treat arbitrary dictionary indices as continuous scalar magnitudes. The arithmetic implies that `lazy` (`6`) is three times as large as `brown` (`2`), and that the numerical distance between `brown` (`2`) and `lazy` (`6`) equals `4`. That numerical ordering is an artifact of dictionary assignment rather than a linguistic relationship; the integer `2` does not make the color brown algebraically smaller than the adjective lazy.

Participating in gradient-based optimization requires transforming these discrete categorical indices into continuous, dense vectors where every coordinate serves as an independently tunable parameter.

## The One-Hot Encoding

The first step in this transformation converts each integer token ID into a mathematically neutral representation: a **one-hot encoded vector** $\mathbf{x} \in \{0, 1\}^{1 \times V}$.

A vocabulary of size $V = 8$ represents the token `brown` (index `2` under 0-based indexing) as a row vector of length $8$ containing zeros at every position except index `2`, which holds a single `1`:

$$
\mathbf{x}_{\text{brown}} = \begin{bmatrix} 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}_{1 \times 8}
$$

This sparse basis vector encodes the categorical identity of the token without introducing false numerical ordering across vocabulary entries. The `1` at index `2` marks the presence of `brown`, while the `0` entries at indices `0, 1, 3, 4, 5, 6, 7` mark the absence of every other vocabulary token. A one-hot vector remains completely sparse and fixed, providing no tunable parameters to capture semantic similarity. Encoding continuous relationships requires projecting this sparse vector into a learnable coordinate space.

## The Embedding Matrix ($W_E$)

Projecting discrete tokens into a continuous vector space requires initializing a two-dimensional parameter grid called the **embedding matrix**, denoted as $W_E \in \mathbb{R}^{V \times d_{\text{model}}}$.

The matrix $W_E$ operates as a parameterized lookup table. The matrix allocates one row for each of the $V$ tokens in the vocabulary, and the width of each row equals the model hidden dimensionality $d_{\text{model}}$.

The toy configuration with vocabulary size $V = 8$ and embedding dimension $d_{\text{model}} = 3$ instantiates an $8 \times 3$ embedding matrix containing $8 \times 3 = 24$ learnable parameters (whereas a production architecture with $V = 50,000$ and $d_{\text{model}} = 512$ instantiates $50,000 \times 512 = 25,600,000$ parameters). At initialization, every entry $w_{i,m}$ (representing vocabulary row $i \in \{0, \dots, V-1\}$ and embedding dimension $m \in \{1, \dots, d_{\text{model}}\}$) is sampled as a random floating-point number.

## The Mathematical Extraction

Standard vector-matrix multiplication maps the sparse one-hot row vector $\mathbf{x}_{\text{brown}} \in \mathbb{R}^{1 \times 8}$ to its dense embedding vector $\mathbf{h} \in \mathbb{R}^{1 \times 3}$.

Multiplying the one-hot vector $\mathbf{x}_{\text{brown}}$ by the embedding matrix $W_E$ scales every row $i \neq 2$ by $0$ and scales row $2$ by $1$, isolating the third row of the matrix:

$$
\mathbf{h} = \mathbf{x}_{\text{brown}} \times W_E = \begin{bmatrix} 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}_{1 \times 8} \times \begin{bmatrix}
w_{0,1} & w_{0,2} & w_{0,3} \\
w_{1,1} & w_{1,2} & w_{1,3} \\
\mathbf{w_{2,1}} & \mathbf{w_{2,2}} & \mathbf{w_{2,3}} \\
w_{3,1} & w_{3,2} & w_{3,3} \\
\vdots & \vdots & \vdots \\
w_{7,1} & w_{7,2} & w_{7,3}
\end{bmatrix}_{8 \times 3}
$$

$$
\mathbf{h} = \begin{bmatrix} w_{2,1} & w_{2,2} & w_{2,3} \end{bmatrix}_{1 \times 3} = \begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}_{1 \times 3}
$$

Here $\mathbf{h}$ denotes the extracted $1 \times 3$ hidden embedding vector for `brown`, populated with the concrete initial weights $\begin{bmatrix} -0.3 & 0.9 & 0.4 \end{bmatrix}$ traced throughout Chapters 3 through 7. This vector-matrix multiplication performs a linear row-selection operation: the one-hot encoding plucks row `2` from $W_E$, mapping the discrete integer ID `2` into a continuous vector of tunable parameters.

The projection through $W_E$ bridges the boundary between discrete token indices and continuous vector geometry. The next chapter examines the high-dimensional geometric structure of these randomly initialized vectors and the mathematical consequences of scattering tokens across a high-dimensional space.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
