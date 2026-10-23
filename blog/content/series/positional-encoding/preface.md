# Preface: The Gap Between Static Geometry and Sequential Structure

<!-- SUMMARY: The preceding [Embeddings series](series-embeddings.html) delivers an embedding tensor that encodes distributional meaning but discards word order entirely. This series bridges that gap by deriving two positional encoding mechanisms from first principles: the historical sinusoidal formula (Vaswani et al., 2017) and Rotary Position Embeddings (RoPE, Su et al., 2021), the mechanism deployed in every frontier language model. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding series on Embeddings terminates with an embedding tensor $X \in \mathbb{R}^{T \times d_{model}}$ whose rows encode the distributional signatures of individual words. Each row is a dense, continuous vector shaped by billions of gradient updates into a point whose position in the embedding space reflects the statistical patterns of its token across the training corpus. But this tensor is order-agnostic: the sequences `The` `quick` `brown` `fox` and `fox` `brown` `quick` `The` produce the same set of embedding vectors, merely arranged in different rows. The embedding lookup treats each row independently and has no mechanism to encode which word appeared at which position.

The subsequent series on Transformers requires a tensor that encodes both meaning and position. The self-attention mechanism, which allows each token to attend to every other token in the sequence, is itself a set operation on unordered vectors unless positional information has been injected beforehand. Without that injection, the Transformer cannot distinguish `dog` `bites` `man` from `man` `bites` `dog`.

This series derives the mathematical mechanisms that bridge that gap.

## The Scope

The derivation proceeds through two distinct positional encoding paradigms, each worked through the same concrete toy model:

- **Vocabulary ($V = 8$):** Eight token types (`The`, `quick`, `brown`, `fox`, `jumps`, `over`, `lazy`, `dog`).
- **Embedding Dimension ($d_{model} = 3$):** Three continuous coordinates per token vector.
- **Toy Sequence ($T = 4$):** Four-token input clause (`The` `quick` `brown` `fox`).

The first paradigm is the **sinusoidal absolute positional encoding** introduced by Vaswani et al. (2017) in the original Transformer paper. This mechanism assigns a fixed, deterministic vector to each position in the sequence and adds it element-wise to the embedding vector. It is the historical starting point: the first published solution to the problem of injecting order into a set-based architecture. The series derives the sinusoidal formula from its design constraints, computes every entry of the positional encoding matrix, and demonstrates the addition operation that produces the positionally-enriched tensor.

The second paradigm is **Rotary Position Embeddings** (RoPE), introduced by Su et al. (2021). Modern frontier Transformer architectures, including the GPT, Claude, Gemini, Llama, DeepSeek, Mistral, and Qwen model families, standardize on RoPE as their primary positional encoding mechanism. Rather than adding a positional vector to the embedding, RoPE applies a position-dependent rotation to the query and key vectors inside the attention mechanism, ensuring that the dot product between any two positions depends only on their relative offset. The series derives RoPE from its complex-number foundations, computes every rotation matrix, and proves the relative-distance property that makes it the dominant mechanism in production.

The sinusoidal derivation is not wasted effort. It establishes the trigonometric vocabulary, the rotation interpretation, and the relative-distance intuition that RoPE generalizes. The two paradigms share a frequency base, and the mathematical progression from additive encoding to rotational encoding is itself the central narrative of the series.

The [Transformers series](series-transformers.html) (which follows this one in the pipeline) includes a brief treatment of sinusoidal positional encoding using a different toy model ($V = 12$, $d_{model} = 6$). Readers who complete both series will recognize the identical mathematical structure applied at different scales.

## The Architecture

The series follows the progression from the order-agnostic embedding tensor to the position-aware representations consumed by the Transformer:

1. **The Permutation Invariance Problem:** Computes the pairwise dot-product similarity matrix $S = X X^\top$ for the toy sequence and proves its invariance under row permutations, demonstrating that reordering the sequence changes row labels without altering similarity scores.
2. **Design Constraints and the Sinusoidal Formula:** Enumerates five mathematical constraints (uniqueness, boundedness, determinism, smoothness, and relative representability), derives the sinusoidal positional encoding formula satisfying all five, and computes every entry of the $4 \times 3$ positional encoding matrix.
3. **Element-Wise Addition and the Positionally-Enriched Tensor:** Adds the sinusoidal encoding element-wise to the embedding tensor to form $X_{pos} = X + PE$, recomputes the similarity matrix to prove that permutation invariance is broken, and identifies the structural limitations of additive absolute encoding (single-layer injection, absolute position labels, and length extrapolation degradation).
4. **The Query-Key Framework and the Relative Position Requirement:** Introduces learned projection matrices $W_Q$ and $W_K$ that map embeddings to query and key vectors whose dot products determine relevance scores, then states the formal relative position requirement.
5. **Rotary Position Embeddings: Deriving the Rotation Matrix:** Derives the RoPE operation from complex-number multiplication, represents each query and key dimension pair as a complex number rotated by a position-dependent angle, expands the $2 \times 2$ blocks into a block-diagonal rotation matrix, and computes the angular frequency for the toy model.
6. **Rotary Position Embeddings: Computing the Rotated Vectors:** Evaluates the rotation matrix at every position in the toy sequence ($R_0$ through $R_3$), proves orthogonality and norm preservation, and rotates every query and key vector from Chapter 4.
7. **The Relative-Distance Property of RoPE:** Proves the central algebraic identity $R_m^\top R_n = R_{n-m}$ from the angle-addition formulas for sine and cosine, and verifies numerically that the dot product of rotated queries and keys depends exclusively on relative position offset.
8. **The Modern Landscape and Frontier Extensions:** Surveys learned absolute positional embeddings, relative positional encodings (Shaw et al., 2018), ALiBi (Press et al., 2022), iRoPE (Meta, 2025), and RoPE long-context extensions (Position Interpolation, NTK-aware scaling, and YaRN), tracing the structural tradeoffs that established RoPE as the production standard.

Every trigonometric identity is derived explicitly. Every rotation matrix is computed entry by entry. Every abstract result is grounded in the toy vocabulary. The mathematics speaks for itself.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
