# Preface: From Dense to Sparse
<!-- SUMMARY: The dense Feed-Forward Network within a Transformer activates every parameter for every token, creating an unsustainable computation bottleneck at frontier scale. The Mixture of Experts architecture solves this inefficiency by decoupling the total parameter capacity from the per-token floating-point operations. This architectural evolution bridges the gap between the original Transformer design and modern sparse models. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The 24-part [Transformer series](series-transformers.html) concluded by tracing the full forward and backward pass through a dense two-layer decoder architecture. Within that dense structure, the Feed-Forward Network activates every single parameter for every token passing through the residual stream. At small parameter scales, this dense execution remains tractable. At frontier scale, where Feed-Forward Network parameters constitute approximately two-thirds of total model capacity, dense activation creates a severe computational bottleneck.

The Mixture of Experts architecture resolves this bottleneck by separating knowledge capacity from per-token compute cost. A dense model locks these two quantities together: doubling the parameters doubles the cost of processing every token. A sparse Mixture of Experts model breaks this link, storing a large parameter pool while activating only a small, targeted subset for each token. Production architectures such as Mixtral, DeepSeek-V3, Gemini, and Grok rely on sparse expert routing to scale model capacity without a proportional increase in per-token floating-point operations.

## Prerequisites and Context

This series serves as the direct architectural successor to the [Transformer series](series-transformers.html). The derivation assumes familiarity with the material covered in Part 10 through Part 14 of that prior series. A practitioner entering without having read the [Transformer series](series-transformers.html) must understand the Feed-Forward Network as a two-layer affine projection with a nonlinear activation function.

An affine projection is a geometric operation consisting of a linear transformation followed by a translation. Within the Feed-Forward Network, a token vector is multiplied by a learned weight matrix to rotate and scale the geometric space, and a bias vector is subsequently added to shift the origin. The standard dense Feed-Forward Network operates as a key-value memory bank through two such projections. 

The first affine projection expands the vector dimensionality. A nonlinear activation function then enforces sparsity. A second affine projection subsequently contracts the vector back to the original model dimension. The Mixture of Experts architecture replaces this single monolithic memory bank with multiple smaller, independent Feed-Forward Networks and a learned gating mechanism to route tokens between them. The token representations used throughout this series are identical to those computed in the [Transformer series](series-transformers.html), maintaining strict numerical and geometric continuity.

## Chapter Roadmap

The progression of the series systematically deconstructs the routing mechanics, pathologies, and economics of sparse architectures:

1. **Chapter 1: The Dense FFN Bottleneck:** Establishes the floating-point operation counts and parameter waste of the standard monolithic architecture.
2. **Chapter 2: The Router:** Details the gating network mathematics, top-$k$ masking, and softmax normalization.
3. **Chapter 3: The MoE Forward Pass:** Computes the independent expert projections and weighted output synthesis for a four-token batch.
4. **Chapter 4: Expert Collapse:** Simulates the positive feedback loop that causes unconstrained routing distributions to degenerate.
5. **Chapter 5: Load Balancing: The Auxiliary Loss:** Derives the auxiliary loss objective, its analytical softmax gradients, and the router z-loss stability penalty.
6. **Chapter 6: Capacity, Token Dropping, and the Switch Transformer:** Traces static hardware buffer limits, residual token dropping, Top-1 routing, and block-sparse execution.
7. **Chapter 7: Fine-Grained Experts and Shared Expert Isolation:** Explores combinatorial parameter segmentation and unconditionally active shared expert pathways.
8. **Chapter 8: The Frontier: Auxiliary-Loss-Free Routing:** Computes auxiliary-loss-free Sigmoid routing and out-of-graph dynamic bias adjustments that eliminate gradient distortion.
9. **Chapter 9: The Economics of Sparsity:** Synthesizes the parameter-to-FLOP scaling laws, memory bandwidth constraints, and device-limited All-to-All communication topologies.

Chapter 1 begins by quantifying the computational cost of the dense Feed-Forward Network and establishing the parameter economics of a sparse alternative, before Chapter 2 constructs the mathematical routing mechanism.

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
