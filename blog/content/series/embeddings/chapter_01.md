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

<!-- SUMMARY: Tokenization translates raw text into discrete integer identifiers, but neural networks require continuous representations to perform calculus. The embedding matrix solves this by projecting each discrete token into a high-dimensional vector space via one-hot encoding multiplication, acting as a simple, dense lookup table. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The preceding series on Tokenization established the rigorous mathematical process of transforming variable, unstructured text into discrete integer sequences. Through subword compression algorithms like Byte Pair Encoding, it was demonstrated how a system can organically parse language into a highly optimized, finite vocabulary.

When text passes through this tokenizer, a word like "walking" might be decomposed into two distinct subword tokens, each mapped to a specific integer ID in our vocabulary:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<b><code>walk</code></b> (ID: 4) &nbsp;&nbsp; <b><code>ing</code></b> (ID: 12)
</div>

This is where the Tokenization pipeline ends. However, handing the integer IDs `4` and `12` directly to a neural network presents an immediate mathematical dead end. 

## The Problem with Discrete Integers

Deep learning models operate through continuous mathematics: matrix multiplication, calculus, and gradient descent. Discrete integer IDs are merely categorical labels; they possess no inherent algebraic meaning. 

If the IDs `4` and `12` are fed directly into a neural network, the model will attempt to perform mathematical operations on them. It might deduce that `12` is three times as large as `4`. It might conclude that the "distance" between `walk` (4) and `ing` (12) is exactly 8. This is mathematically nonsensical. The integer ID `4` does not mean the concept of walking is "smaller" than the suffix `ing`. They are just arbitrary index numbers.

To participate in a neural network, these discrete, categorical IDs must be transformed into continuous, dense vectors where every dimension represents a tunable parameter.

## The One-Hot Encoding

The first step in this transformation is to convert the categorical ID into a mathematically neutral format: a one-hot encoded vector.

If the total vocabulary size $(V)$ is 9, the token `walk` (ID 4) can be represented as a vector of length 9 containing all zeros, except for a single `1` at the 4th index.

$$
\mathbf{x}_{walk} = \begin{bmatrix} 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}_{1 \times 9}
$$

This sparse vector allows the network to process the categorical identity of the token without accidentally inferring any false mathematical magnitude. The `1` simply states "this token is present", while the `0`s state "these other tokens are not". However, a one-hot vector is completely sparse and contains no semantic depth. It must be projected into a continuous space.

## The Embedding Matrix ($W_E$)

To give these tokens continuous algebraic meaning, a massive grid of random numbers known as the embedding matrix is initialized, typically denoted as $W_E$. 

This matrix serves as a dense lookup table. It contains exactly one row for every possible token in the architecture's predefined vocabulary, and the width of every row is defined by the network's internal model dimensionality ($d_{model}$). 

If the vocabulary size $V$ is 9, and the vector dimensionality $d_{model}$ is 512, the embedding matrix requires exactly $9 \times 512$ parameters. At the moment of initialization, every single one of these parameters is just a random decimal number.

## The Mathematical Extraction

How does the network transition from the sparse one-hot vector to the dense 512-dimensional vector? Through standard matrix multiplication.

By multiplying the one-hot vector $\mathbf{x}_{walk}$ by the embedding matrix $W_E$, the mathematics dictate that all rows multiplied by `0` are canceled out, leaving only the 4th row (multiplied by `1`) to pass through. 

$$
\mathbf{x}_{walk} = \begin{bmatrix} 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \end{bmatrix}_{1 \times 9} \times \begin{bmatrix}
w_{1,1} & \dots & w_{1,512} \\
w_{2,1} & \dots & w_{2,512} \\
w_{3,1} & \dots & w_{3,512} \\
w_{4,1} & \dots & w_{4,512} \\
\vdots & \ddots & \vdots \\
w_{9,1} & \dots & w_{9,512}
\end{bmatrix}_{9 \times 512}
$$

$$
= \begin{bmatrix} w_{4,1} & w_{4,2} & \dots & w_{4,512} \end{bmatrix}_{1 \times 512}
$$

This matrix multiplication involves no learning; it is the linear algebra mechanism for selecting a specific row from a table. The token `walk` has now been successfully mapped from a discrete integer ID into a continuous, 512-dimensional vector of random numbers. 

The gap into the continuous vector space has been bridged. The nature of these random numbers, the structure of high-dimensional geometry, and the mathematical implications of randomly scattering tokens across this landscape are explored next.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
