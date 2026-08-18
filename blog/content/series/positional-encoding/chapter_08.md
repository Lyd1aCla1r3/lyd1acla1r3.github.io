# Part 8: The Modern Landscape and Frontier Extensions

<!-- SUMMARY: A conceptual survey of positional encoding mechanisms beyond sinusoidal absolute PE and RoPE. Each mechanism is motivated by the shortcoming of its predecessor: learned absolute embeddings trade structural guarantees for expressive flexibility but impose a hard sequence-length ceiling, relative position biases move position information into the attention computation but require learned parameters, ALiBi achieves zero-parameter simplicity but assumes a rigid linear decay, iRoPE selectively removes positional encoding from layers that do not need it, and frequency-scaling extensions address RoPE's length extrapolation problem. The series closes by connecting the positionally-enriched tensor to the Transformer attention mechanism. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding six chapters constructed two positional encoding mechanisms from first principles. Chapters 2 and 3 derived the sinusoidal absolute encoding of Vaswani et al. (2017), added it to the embedding tensor, and demonstrated that it breaks permutation invariance. Chapters 4, 5, and 6 introduced the query-key framework, derived Rotary Position Embeddings (Su et al., 2021), and proved that the resulting dot product depends only on content and relative position offset. Both mechanisms received full numerical treatment through the toy model.

These two are not the full picture. Between the original Transformer and the frontier models deployed today, several alternative approaches to positional encoding were proposed, each motivated by a specific shortcoming of the mechanisms that preceded it. This chapter traces that evolution conceptually, explaining what each mechanism does, why it was designed that way, and where it falls short.

## Learned Absolute Positional Embeddings

The sinusoidal formula from Chapter 2 computes positional vectors from a fixed mathematical function. A simpler alternative is to skip the formula entirely and let the model learn its own positional vectors during training.

In this approach, a separate embedding matrix is allocated with one row per position (up to some maximum sequence length). Each row is a trainable vector, initialized randomly and updated through backpropagation alongside the token embeddings and all other model parameters. At runtime, the vector for position $t$ is looked up from this matrix and added element-wise to the token embedding at that position, exactly as the sinusoidal vectors are added in Chapter 3.

The appeal is maximum flexibility. If the optimal positional encoding for a given task happens to resemble sinusoidal patterns, the model is free to learn that structure. If the optimal encoding has an entirely different geometry, the model is not constrained to trigonometric shapes. The encoding adapts to whatever the training data rewards.

This mechanism was used in BERT (Devlin et al., 2018) with a maximum length of 512 tokens and in GPT-2 (Radford et al., 2019) with a maximum length of 1,024 tokens.

The fundamental limitation is a hard ceiling on sequence length. The embedding matrix has a fixed number of rows, determined before training begins. Position 513 in a BERT model has no entry in the matrix and cannot be represented. Extending to longer sequences requires either retraining the model with a larger matrix or interpolating between existing entries (an imprecise workaround). As context lengths grew from 512 to 128,000 and beyond, this ceiling became untenable.

A subtler limitation is the absence of structural guarantees. None of the five design constraints from Chapter 2 (uniqueness, boundedness, determinism, smoothness, relative representability) are satisfied by construction. Whether adjacent positions receive similar vectors, whether the encoding captures relative offsets, whether the values stay bounded, all depend on what the optimizer happens to discover during training. The sinusoidal formula guarantees these properties mathematically. Learned embeddings hope that training will produce them empirically.

## Relative Positional Encoding

The sinusoidal formula and learned embeddings both share a structural assumption: position information is injected into the embedding tensor *before* the attention computation begins. Each position receives a fixed vector (computed or learned), that vector is added to the token embedding, and the combined representation flows into the query and key projections. As Chapter 3 demonstrated, this entangles the content signal and the positional signal in the same vector space, forcing the model to disentangle them.

Shaw et al. (2018) proposed a different approach: inject position information directly into the attention scores, at the point where the model is actually computing relationships between tokens.

The mechanism works by adding a learned bias to the attention score between every pair of positions. Crucially, this bias is indexed by the *relative offset* between the two positions, not by their absolute indices. Two token pairs separated by the same number of positions receive the same bias, regardless of where they sit in the sequence. The bias is a learned vector (one for each possible offset within a clipping window), so the model can learn arbitrary relationships between tokens at different separations.

The key insight is that attention scores should reflect how far apart two tokens are, not where each token sits in absolute terms. A verb three positions after its subject should receive a similar positional signal whether the subject appears at position 0, position 50, or position 500. By parameterizing the bias with the offset rather than the individual positions, this mechanism structurally encodes that insight.

This approach influenced the positional encoding designs in Transformer-XL (Dai et al., 2019) and the T5 model (Raffel et al., 2020).

The limitations mirror those of learned absolute embeddings in a different form. The bias vectors are learned parameters, so the encoding varies across training runs and provides no structural guarantees about smoothness or boundedness. The clipping window imposes a maximum relative distance: offsets beyond the window share a single bias vector, meaning the model cannot distinguish between tokens 100 positions apart and tokens 200 positions apart. And the relative relationship is stored in a lookup table of learned vectors rather than emerging from algebraic structure (as it does in RoPE, where the relative-distance property follows from the angle-addition identities).

## ALiBi (Attention with Linear Biases)

Press et al. (2022) took the idea of modifying attention scores and pushed it to its minimalist extreme: no positional encoding on the embeddings, no positional encoding on the query or key projections, and no learned parameters of any kind. Instead, a fixed linear penalty is subtracted from each attention score, proportional to the distance between the two tokens.

Tokens close together receive a small penalty (high attention is easy). Tokens far apart receive a large penalty (high attention is difficult). Different attention heads use different penalty slopes, set as fixed constants determined entirely by the number of heads. Some heads apply a steep penalty, creating a sharp locality bias that focuses attention on nearby tokens. Other heads apply a gentle penalty, allowing attention to spread across the full sequence.

The design motivation is simplicity and length generalization. Because the penalty is a linear function of distance, it extrapolates naturally to distances unseen during training: the penalty for a distance of 10,000 is simply 10,000 times the slope, with no periodic structure to break down. The mechanism introduces zero additional parameters (the slopes are predetermined constants) and leaves the content pathway completely untouched.

ALiBi was adopted in BLOOM (BigScience, 2022) and MPT (MosaicML, 2023).

The shortcoming is rigidity. The assumption that relevance decays linearly with distance is a strong structural prior that does not match the complexity of natural language. A verb may be highly relevant to its subject 20 tokens away but irrelevant to the adjacent comma. A pronoun at position 50 may refer to a noun at position 5, making that distant token more relevant than every intervening token. ALiBi cannot express these patterns; it can only penalize distance uniformly. Subsequent frontier models (GPT-4, Claude, Gemini, Llama 3) adopted RoPE instead, which encodes relative position through geometric rotation rather than scalar penalty, allowing the content of the tokens to interact with the positional signal in richer ways.

## iRoPE (Interleaved RoPE)

Standard RoPE models apply position-dependent rotations to query and key vectors in every attention layer. iRoPE (Meta, 2025), the architecture used in Llama 4, makes a selective choice: only some layers apply RoPE, while the remaining layers apply no positional encoding at all.

The motivation comes from observing that not all attention patterns require positional information. Some attention heads learn syntactic patterns (subject-verb agreement across specific relative positions, clause boundaries at characteristic distances) where positional information is essential. Other heads learn semantic patterns (thematic similarity, coreference, topical grouping) where the content of the tokens matters and their positions are irrelevant. Applying RoPE to every layer forces all attention heads to process position-rotated vectors, even in heads where the rotation adds noise to an otherwise clean semantic signal.

By alternating RoPE layers with position-free layers, the architecture provides both pathways. The RoPE layers encode explicit relative position. The position-free layers compute attention based purely on content, relying on the model's ability to infer any necessary positional context from the surrounding RoPE layers (through residual connections that propagate information between layers). The result is a model that can dedicate some of its attention capacity to position-dependent relationships and the rest to position-agnostic relationships, rather than forcing every layer to do both simultaneously.

A secondary benefit is computational efficiency during inference. Position-free layers do not require computing or applying rotation matrices, and their key-value caches do not depend on position, enabling more flexible caching strategies during autoregressive generation.

## RoPE Extensions for Long Context

The relative-distance property proved in Chapter 7 holds at any sequence length: the rotation composition identity $R_m^\top R_n = R_{n-m}$ is an algebraic fact, independent of how large $m$ and $n$ become. But the model's *learned attention patterns* are not algebraic identities. They are statistical regularities optimized over the rotation angles encountered during training. When a model trained on sequences of length 4,096 encounters a sequence of length 32,000, the rotation angles at positions beyond 4,096 fall outside the training distribution. The mathematical structure is intact, but the model has never learned to interpret those angles.

This is the length extrapolation problem, and several approaches have been proposed to address it.

**Position Interpolation** (Chen et al., 2023) takes the most straightforward approach: scale all position indices by a compression factor so that the extended sequence maps onto the same range of rotation angles the model saw during training. A model trained on length 4,096 that needs to handle length 16,384 divides every position index by 4, so position 16,384 produces the same rotation angle that position 4,096 produced during training. The cost is reduced positional resolution: positions that were previously one unit apart now appear one-quarter of a unit apart, making it harder for the model to distinguish fine-grained positional differences.

**NTK-aware scaling** (Bloc97, 2023) observes that uniform compression damages some dimensions more than others. High-frequency dimensions (which capture fine-grained positional distinctions, like the difference between position 5 and position 6) are more sensitive to compression than low-frequency dimensions (which capture coarse positional structure, like the difference between position 0 and position 500). NTK-aware scaling applies different compression factors to different frequency dimensions: high-frequency dimensions are left mostly unchanged, preserving fine-grained resolution, while low-frequency dimensions absorb most of the compression, extending the effective range of the encoding. The interpolation pressure is concentrated on the dimensions that can absorb it.

**YaRN** (Peng et al., 2023) extends this idea further by partitioning all frequency dimensions into three groups (high-frequency, medium-frequency, low-frequency) and applying a different scaling strategy to each. High-frequency dimensions receive no modification. Low-frequency dimensions receive full interpolation. Medium-frequency dimensions receive a smooth blend between the two extremes. This fine-grained partitioning, combined with an attention-score temperature adjustment to compensate for the changed variance, produces the most precise frequency management of the three approaches. YaRN was adopted by DeepSeek V3 and R1 for extending RoPE to context lengths of 128,000 tokens and beyond.

All three extensions preserve the algebraic structure of RoPE. The rotation composition identity holds regardless of the specific frequency values, because the identity follows from the angle-addition properties of sine and cosine, not from the particular angles used. Modifying the frequencies changes the rotation angles but does not invalidate the relative-distance property. The extensions are adjustments to the frequency tuning, not alterations to the mathematical mechanism.

## Final Thoughts

Positional encoding solves a problem that the architecture itself created. The Transformer processes all tokens simultaneously rather than sequentially, which gives it parallelism and scalability, but strips away the one thing that recurrent networks got for free: the knowledge of which token came first. Every mechanism in this series, from sinusoidal addition to geometric rotation to linear penalty, is an attempt to restore that lost ordering information without sacrificing the parallelism that made the Transformer worth building in the first place.

The common thread across every mechanism is a single goal: inject enough positional structure that the model can distinguish token order, without distorting the semantic content that makes each token meaningful. The sinusoidal formula achieves this through additive injection. RoPE achieves it through geometric rotation. ALiBi achieves it through attention-score penalties. Each approach encodes the same fundamental information (where tokens sit relative to each other) through a different mathematical channel.

The embedding tensor, enriched with positional information, is now ready for the computation that determines how each token attends to every other token in the sequence. That computation is the subject of the next series, Transformers, which takes this positionally-enriched tensor and constructs the full attention mechanism from first principles.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
