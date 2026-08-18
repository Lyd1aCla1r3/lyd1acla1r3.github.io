# Preface: The Gap Between Static Geometry and Sequential Structure

<!-- SUMMARY: The preceding Embeddings series delivers an embedding tensor that encodes distributional meaning but discards word order entirely. This series bridges that gap by deriving two positional encoding mechanisms from first principles: the historical sinusoidal formula (Vaswani et al., 2017) and Rotary Position Embeddings (RoPE, Su et al., 2021), the mechanism deployed in every frontier language model. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding series on Embeddings terminates with an embedding tensor $X \in \mathbb{R}^{T \times d_{model}}$ whose rows encode the distributional signatures of individual words. Each row is a dense, continuous vector shaped by billions of gradient updates into a point whose position in the embedding space reflects the statistical patterns of its token across the training corpus. But this tensor is order-agnostic: the sequences `The` `quick` `brown` `fox` and `fox` `brown` `quick` `The` produce the same set of embedding vectors, merely arranged in different rows. The embedding lookup treats each row independently and has no mechanism to encode which word appeared at which position.

The subsequent series on Transformers requires a tensor that encodes both meaning and position. The self-attention mechanism, which allows each token to attend to every other token in the sequence, is itself a set operation on unordered vectors unless positional information has been injected beforehand. Without that injection, the Transformer cannot distinguish `dog` `bites` `man` from `man` `bites` `dog`.

This series derives the mathematical mechanisms that bridge that gap.

## The Scope

The derivation proceeds through two distinct positional encoding paradigms, each worked through the same concrete toy model:

- **Vocabulary ($V = 8$):** `The` `quick` `brown` `fox` `jumps` `over` `lazy` `dog`
- **Embedding Dimension ($d_{model}$):** 3 dimensions.
- **Toy sequence ($T = 4$):** `The` `quick` `brown` `fox`

The first paradigm is the **sinusoidal absolute positional encoding** introduced by Vaswani et al. (2017) in the original Transformer paper. This mechanism assigns a fixed, deterministic vector to each position in the sequence and adds it element-wise to the embedding vector. It is the historical starting point: the first published solution to the problem of injecting order into a set-based architecture. The series derives the sinusoidal formula from its design constraints, computes every entry of the positional encoding matrix, and demonstrates the addition operation that produces the positionally-enriched tensor.

The second paradigm is **Rotary Position Embeddings** (RoPE), introduced by Su et al. (2021). As of 2026, RoPE is the positional encoding mechanism used in every major frontier language model, including GPT-4, Claude, Gemini, Llama 3, DeepSeek, Mistral, and Qwen. Rather than adding a positional vector to the embedding, RoPE applies a position-dependent rotation to the query and key vectors inside the attention mechanism, ensuring that the dot product between any two positions depends only on their relative offset. The series derives RoPE from its complex-number foundations, computes every rotation matrix, and proves the relative-distance property that makes it the dominant mechanism in production.

The sinusoidal derivation is not wasted effort. It establishes the trigonometric vocabulary, the rotation interpretation, and the relative-distance intuition that RoPE generalizes. The two paradigms share a frequency base, and the mathematical progression from additive encoding to rotational encoding is itself the central narrative of the series.

The Transformers series (which follows this one in the pipeline) includes a brief treatment of sinusoidal positional encoding using a different toy model ($V = 12$, $d_{model} = 6$). Readers who complete both series will recognize the identical mathematical structure applied at different scales.

## The Architecture

The series follows the progression from the order-agnostic embedding tensor to the position-aware representations consumed by the Transformer:

1. **The Permutation Invariance Problem.** The pairwise dot-product similarity matrix $S = X X^\top$ is computed for the toy sequence and shown to be invariant under row permutations: reordering the sequence changes the labels but not the similarity scores. The embedding tensor carries no positional information.
2. **Design Constraints and the Sinusoidal Formula.** Five mathematical constraints (uniqueness, boundedness, determinism, smoothness, relative representability) are enumerated, and the sinusoidal positional encoding formula is derived as the function satisfying all five. Every entry of the $4 \times 3$ positional encoding matrix is computed from the formula.
3. **Element-Wise Addition and the Positionally-Enriched Tensor.** The sinusoidal encoding is added element-wise to the embedding tensor, producing $X_{pos} = X + PE$. The similarity matrix is recomputed and shown to break permutation invariance. The structural limitations of additive absolute encoding (single-layer injection, absolute position labels, length extrapolation degradation) are identified.
4. **The Query-Key Framework and the Relative Position Requirement.** The minimal query-key dot-product mechanism is introduced at the scope required by RoPE: learned projection matrices $W_Q$ and $W_K$ map embeddings to query and key vectors whose dot product determines relevance scores. The relative position requirement is stated formally.
5. **Rotary Position Embeddings: Deriving the Rotation Matrix.** The RoPE operation is derived from its complex-number foundations. Each dimension pair of the query and key vectors is represented as a complex number and rotated by a position-dependent angle. The $2 \times 2$ rotation blocks are expanded into the full block-diagonal rotation matrix, and the angular frequency for the toy model is computed.
6. **Rotary Position Embeddings: Computing the Rotated Vectors.** The rotation matrix is evaluated at every position in the toy sequence, producing four distinct rotation matrices $R_0$ through $R_3$. These matrices are applied to every query and key vector from Chapter 4, producing the rotated vectors consumed by the attention mechanism.
7. **The Relative-Distance Property of RoPE.** The central algebraic identity $R_m^\top R_n = R_{n-m}$ is proved from the angle-addition formulas for sine and cosine. The identity is verified numerically using the rotated vectors from the previous chapter: the dot product of rotated queries and keys is shown to depend only on relative position offset.
8. **The Modern Landscape and Frontier Extensions.** Learned absolute PE, relative PE (Shaw et al., 2018), ALiBi (Press et al., 2022), iRoPE (Meta, 2025), and RoPE long-context extensions (YaRN, NTK-aware scaling) are surveyed. Each mechanism is explained through its motivation, its conceptual operation, and the shortcomings that drove the field toward its successor, tracing the evolutionary arc that culminated in RoPE's dominance.

Every trigonometric identity is derived explicitly. Every rotation matrix is computed entry by entry. Every abstract result is grounded in the toy vocabulary. The mathematics speaks for itself.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
