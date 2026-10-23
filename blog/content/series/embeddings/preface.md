# Preface: The Gap Between Discrete and Continuous

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

<!-- SUMMARY: The preceding [Tokenization series](series-tokenization.html) terminates with a sequence of discrete integer IDs. The subsequent [Transformer series](series-transformers.html) begins with a dense, continuous embedding tensor. This series bridges that gap by deriving the complete mathematical mechanism (from one-hot encoding through gradient descent) by which a static embedding matrix transforms random vectors into a semantically structured geometric space. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The preceding [Tokenization series](series-tokenization.html) established the mathematical process by which raw text is compressed into a sequence of discrete integer IDs. The subsequent [Transformer series](series-transformers.html) begins with a dense, continuous tensor of embedding vectors already loaded with semantic meaning. Between these two endpoints exists a structural gap: the mechanism by which discrete integers become continuous vectors whose geometric relationships encode the distributional structure of language.

This series derives that mechanism from first principles.

## The Scope

The derivation proceeds through a shallow, two-layer neural network whose sole purpose is to train the embedding matrix $W_E \in \mathbb{R}^{V \times d_{\text{model}}}$. Every mathematical operation is computed explicitly using a concrete toy configuration:

- **Vocabulary Cardinality ($V = 8$):** Eight 0-indexed word tokens spanning indices `0` through `7`.
- **Embedding Dimensionality ($d_{\text{model}} = 3$):** Three continuous floating-point coordinates per token.

| Token ID | Token | One-Hot Vector (`1 x 8`) | Embedding Matrix Row |
| :---: | :---: | :---: | :---: |
| `0` | `The` | `[1, 0, 0, 0, 0, 0, 0, 0]` | Row `0` of `W_E` |
| `1` | `quick` | `[0, 1, 0, 0, 0, 0, 0, 0]` | Row `1` of `W_E` |
| `2` | `brown` | `[0, 0, 1, 0, 0, 0, 0, 0]` | Row `2` of `W_E` |
| `3` | `fox` | `[0, 0, 0, 1, 0, 0, 0, 0]` | Row `3` of `W_E` |
| `4` | `jumps` | `[0, 0, 0, 0, 1, 0, 0, 0]` | Row `4` of `W_E` |
| `5` | `over` | `[0, 0, 0, 0, 0, 1, 0, 0]` | Row `5` of `W_E` |
| `6` | `lazy` | `[0, 0, 0, 0, 0, 0, 1, 0]` | Row `6` of `W_E` |
| `7` | `dog` | `[0, 0, 0, 0, 0, 0, 0, 1]` | Row `7` of `W_E` |

This toy configuration is intentionally minimal. Eight words and three dimensions suffice to trace every matrix multiplication and partial derivative by hand, while remaining expressive enough to exhibit the geometric phenomena (orthogonality, convergence, and linear substructures) that govern trained embedding spaces at scale.

## The Architecture

The series follows the complete lifecycle of a single training step, then traces the cumulative effect of billions of such steps:

1. **One-Hot Encoding and the Embedding Matrix:** Converts a discrete token ID into a sparse one-hot vector and multiplies it by $W_E$ to extract a dense embedding row.
2. **The Continuous Vector Space:** Derives the high-dimensional geometric properties of randomly initialized embeddings, including isotropy, concentration of measure, and mutual orthogonality.
3. **The Forward Pass, Softmax, and Cross-Entropy Loss:** Projects the extracted embedding through an un-embedding matrix $W_U$ to produce raw logits, normalizes those scores via Softmax, and quantifies prediction error via Cross-Entropy Loss.
4. **Backpropagation Through Loss and Softmax:** Traces the error gradient backward through the loss and Softmax layers to derive the unified $\hat{\mathbf{y}} - \mathbf{y}$ logit gradient from first principles.
5. **Backpropagation Through the Weight Matrices:** Propagates the logit gradient through $W_U$ and $W_E$, proving that one-hot input sparsity restricts each weight update to a single embedding row.
6. **Convergent Geometry and Linear Substructures:** Examines the cumulative effect of millions of gradient updates, demonstrating how co-occurrence statistics produce semantic clustering and linear vector arithmetic.
7. **The Embedding Tensor and the Limits of Static Representations:** Generalizes single-token lookup to batched sequence tensors and diagnoses the structural limits of static embeddings (context-blindness and order-agnosticism) that motivate the Transformer architecture.

Every partial derivative is derived explicitly. Every abstract result is grounded in the toy vocabulary. The mathematics speaks for itself.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
