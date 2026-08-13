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

<!-- SUMMARY: The preceding Tokenization series terminates with a sequence of discrete integer IDs. The subsequent Transformer series begins with a dense, continuous embedding tensor. This series bridges that gap by deriving the complete mathematical mechanism (from one-hot encoding through gradient descent) by which a static embedding matrix transforms random vectors into a semantically structured geometric space. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The preceding series on Tokenization established the mathematical process by which raw text is compressed into a sequence of discrete integer IDs. The subsequent series on Transformers begins with a dense, continuous tensor of embedding vectors already loaded with semantic meaning. Between these two endpoints exists a gap: the mechanism by which discrete integers become rich, continuous vectors whose geometric relationships encode the distributional structure of language.

This series derives that mechanism from first principles.

## The Scope

The derivation proceeds through a shallow, two-layer neural network whose sole purpose is to train the embedding matrix $W_E$. Every mathematical operation is computed explicitly using a concrete toy model:

- **Vocabulary ($V = 8$):** `The` `quick` `brown` `fox` `jumps` `over` `lazy` `dog`
- **Embedding Dimension ($d_{model}$):** 3 dimensions.

This toy model is intentionally minimal. Eight words and three dimensions are sufficient to demonstrate every operation on a whiteboard, yet complex enough to exhibit the geometric phenomena (orthogonality, convergence, linear substructures) that define trained embedding spaces at scale.

## The Architecture

The series follows the complete lifecycle of a single training step, then traces the cumulative effect of billions of such steps:

1. **One-Hot Encoding and the Embedding Matrix.** The discrete token ID is converted into a sparse one-hot vector and projected through $W_E$ to extract a dense embedding.
2. **The Continuous Vector Space.** The geometric properties of the randomly initialized embedding space (isotropy, concentration of measure, and mutual orthogonality) are derived.
3. **The Forward Pass, Softmax, and Cross-Entropy Loss.** The embedding is projected through an un-embedding matrix $W_U$ to produce logits, converted to probabilities via Softmax, and evaluated against the ground truth via Cross-Entropy Loss.
4. **Backpropagation Through Loss and Softmax.** The gradient signal is traced backwards through the loss and Softmax layers, deriving the unified $\hat{\mathbf{y}} - \mathbf{y}$ expression from first principles.
5. **Backpropagation Through the Weight Matrices.** The gradient propagates through $W_U$ and $W_E$, demonstrating how one-hot sparsity ensures only a single embedding row is updated per training example.
6. **Convergent Geometry and Linear Substructures.** The cumulative effect of billions of gradient updates is traced, showing how distributional statistics organically produce semantic clustering and vector arithmetic.
7. **The Embedding Tensor and the Limits of Static Representations.** The single-token lookup is generalized to full-sequence processing. The fundamental limitations of static embeddings (context-blindness and order-agnosticism) are identified, establishing the handoff to the Transformer architecture.

Every partial derivative is derived explicitly. Every abstract result is grounded in the toy vocabulary. The mathematics speaks for itself.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
