# Part 8: The Modern Landscape and Frontier Extensions

<!-- SUMMARY: A conceptual survey of positional encoding mechanisms beyond sinusoidal absolute PE and RoPE. Each mechanism is motivated by the shortcoming of its predecessor: learned absolute embeddings trade structural guarantees for expressive flexibility but impose a hard sequence-length ceiling, relative position biases move position information into the attention computation but require learned parameters, ALiBi achieves zero-parameter simplicity but assumes a rigid linear decay, iRoPE selectively removes positional encoding from layers that do not need it, and frequency-scaling extensions address RoPE's length extrapolation problem. The series closes by connecting the positionally-enriched tensor to the Transformer attention mechanism. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>

The preceding seven chapters constructed two positional encoding mechanisms from first principles. Chapter 1 established the permutation invariance problem in raw token embeddings, and Chapters 2 and 3 derived the sinusoidal absolute encoding of Vaswani et al. (2017), added it to the embedding tensor, and demonstrated that it breaks permutation invariance. Chapters 4 through 7 introduced the query-key framework, derived Rotary Position Embeddings (Su et al., 2021), computed the rotated vectors at each position, and proved that the resulting dot product depends only on content and relative position offset. Both mechanisms received full numerical treatment through the toy model.

These two are not the full picture. Between the original Transformer and modern long-context architectures, several alternative approaches to positional encoding were proposed, each motivated by a specific shortcoming of the mechanisms that preceded it. This chapter traces that evolution conceptually, explaining what each mechanism does, why it was designed that way, and where it falls short.

## Learned Absolute Positional Embeddings

The sinusoidal formula from Chapter 2 computes positional vectors from a fixed mathematical function. A simpler alternative is to skip the formula entirely and let the model learn its own positional vectors during training.

In this approach, a separate embedding matrix is allocated with one row per position (up to some maximum sequence length). Each row is a trainable vector, initialized randomly and updated through backpropagation alongside the token embeddings and all other model parameters. At runtime, the vector for position $t$ is looked up from this matrix and added element-wise to the token embedding at that position, matching the additive injection pattern from Chapter 3.

The appeal is maximum flexibility. Tasks whose optimal positional encoding resembles sinusoidal patterns allow the model to learn that periodic structure during training. Tasks whose optimal encoding requires a different geometry do not constrain the model to trigonometric shapes. The encoding adapts to whatever the training data rewards.

This mechanism was used in BERT (Devlin et al., 2018) with a maximum length of 512 tokens and in GPT-2 (Radford et al., 2019) with a maximum length of 1,024 tokens.

The fundamental limitation is a hard ceiling on sequence length. The embedding matrix has a fixed number of rows, determined before training begins. Position 513 in a BERT model has no entry in the matrix and cannot be represented. Extending to longer sequences requires either retraining the model with a larger matrix or interpolating between existing entries (an imprecise workaround). Context lengths expanding from 512 to 128,000 tokens and beyond made this hard ceiling untenable.

A subtler limitation is the absence of structural guarantees. None of the five design constraints from Chapter 2 (uniqueness, boundedness, determinism, smoothness, relative representability) are satisfied by construction. Whether adjacent positions receive similar vectors, whether the encoding captures relative offsets, whether the values stay bounded, all depend on what the optimizer happens to discover during training. The sinusoidal formula guarantees these properties mathematically. Learned embeddings hope that training will produce them empirically.

## Relative Positional Encoding

The sinusoidal formula and learned embeddings both share a structural assumption: position information is injected into the embedding tensor *before* the attention computation begins. Each position receives a fixed vector (computed or learned), that vector is added to the token embedding, and the combined representation flows into the query and key projections. Chapter 3 demonstrated that this additive injection entangles the content signal and the positional signal in the same vector space, forcing the model to disentangle them.

Shaw et al. (2018) proposed a different approach: inject position information directly into the attention scores, at the point where the model is actually computing relationships between tokens.

The mechanism works by adding a learned bias to the attention score between every pair of positions. This learned bias is indexed by the *relative offset* between the two positions, not by their absolute indices. Two token pairs separated by the same number of positions receive the same bias, regardless of where they sit in the sequence. The bias is a learned vector (one for each possible offset within a clipping window), so the model can learn arbitrary relationships between tokens at different separations.

The key insight is that attention scores should reflect how far apart two tokens are, not where each token sits in absolute terms. A verb three positions after its subject should receive a similar positional signal whether the subject appears at position 0, position 50, or position 500. Parameterizing the bias with the offset rather than the individual positions encodes that relational invariance directly into the scoring function.

This approach influenced the positional encoding designs in Transformer-XL (Dai et al., 2019) and the T5 model (Raffel et al., 2020).

The limitations mirror those of learned absolute embeddings in a different form. The bias vectors are learned parameters, so the encoding varies across training runs and provides no structural guarantees about smoothness or boundedness. The clipping window imposes a maximum relative distance: offsets beyond the window share a single bias vector, meaning the model cannot distinguish between tokens 100 positions apart and tokens 200 positions apart. And the relative relationship is stored in a lookup table of learned vectors rather than emerging from algebraic structure (as it does in RoPE, where the relative-distance property follows from the angle-addition identities).

## ALiBi (Attention with Linear Biases)

Press et al. (2022) took the idea of modifying attention scores and pushed it to its minimalist extreme: no positional encoding on the embeddings, no positional encoding on the query or key projections, and no learned parameters of any kind. A fixed linear penalty is subtracted directly from each attention score, proportional to the distance between the two tokens.

Tokens close together receive a small penalty (high attention is easy). Tokens far apart receive a large penalty (high attention is difficult). Different attention heads use different penalty slopes, set as fixed constants determined entirely by the number of heads. Some heads apply a steep penalty, creating a sharp locality bias that focuses attention on nearby tokens. Other heads apply a gentle penalty, allowing attention to spread across the full sequence.

The design motivation is simplicity and length generalization. The linear distance penalty extrapolates naturally to distances unseen during training: the penalty for a distance of 10,000 equals 10,000 times the slope, with no periodic structure to break down. The mechanism introduces zero additional parameters (the slopes are predetermined constants) and leaves the content pathway completely untouched.

ALiBi was adopted in BLOOM (BigScience, 2022) and MPT (MosaicML, 2023).

The shortcoming is rigidity. The assumption that relevance decays linearly with distance is a strong structural prior that does not match the complexity of natural language. A verb may be strongly relevant to its subject 20 tokens away but irrelevant to the adjacent comma. A pronoun at position 50 may refer to a noun at position 5, making that distant token more relevant than every intervening token.

ALiBi cannot express these content-dependent long-range patterns; it can only penalize distance uniformly. Subsequent architectures (including Llama, Mistral, Qwen, and Gemma) converged on RoPE instead, which encodes relative position through geometric rotation rather than scalar penalty, allowing the content of the tokens to interact with the positional signal in richer ways.

## iRoPE (Interleaved RoPE)

Standard RoPE models apply position-dependent rotations to query and key vectors in every attention layer. iRoPE (Meta, 2025), the architecture used in Llama 4, makes a selective choice: only some layers apply RoPE, while the remaining layers apply no positional encoding at all.

The motivation comes from observing that not all attention patterns require positional information. Some attention heads learn syntactic patterns (subject-verb agreement across specific relative positions, clause boundaries at characteristic distances) where positional information is essential. Other heads learn semantic patterns (thematic similarity, coreference, topical grouping) where the content of the tokens matters and their positions are irrelevant. Applying RoPE to every layer forces all attention heads to process position-rotated vectors, even in heads where the rotation adds noise to an otherwise clean semantic signal.

Alternating RoPE layers with position-free layers provides both pathways. The RoPE layers encode explicit relative position. The position-free layers compute attention based purely on content, relying on the model's ability to infer any necessary positional context from the surrounding RoPE layers (through residual connections that propagate information between layers). The result is a model that can dedicate some of its attention capacity to position-dependent relationships and the rest to position-agnostic relationships, rather than forcing every layer to do both simultaneously.

A secondary benefit is computational efficiency during inference. Position-free layers do not require computing or applying rotation matrices, and their key-value caches do not depend on position, enabling more flexible caching strategies during autoregressive generation.

## RoPE Extensions for Long Context

The relative-distance property proved in Chapter 7 holds at any sequence length: the rotation composition identity $R_m^\top R_n = R_{n-m}$ is an algebraic fact, independent of how large $m$ and $n$ become. The model's *learned attention patterns*, by contrast, are statistical regularities optimized over the rotation angles encountered during training. Evaluating a model trained on sequences of length 4,096 at a sequence length of 32,000 exposes the attention heads to rotation angles beyond 4,096 that fall outside the training distribution. The mathematical structure remains intact, but the model has never learned to interpret those unseen angles.

Three primary frequency-scaling techniques address this length extrapolation problem:

- **Position Interpolation (Chen et al., 2023):** Scales all position indices down by a uniform compression factor $\frac{T_{train}}{T_{target}}$ (for example, dividing indices by $4$ to map a $16{,}384$-token context onto a $4{,}096$-token training range), keeping all rotation angles within the trained domain at the cost of crowding adjacent tokens closer together and reducing fine-grained local resolution.
- **NTK-Aware Scaling (Bloc97, 2023):** Distributes compression non-uniformly across the frequency spectrum by rescaling the base wavelength, leaving high-frequency dimensions nearly unchanged to preserve local token discrimination while concentrating compression on low-frequency dimensions whose long wavelengths can absorb the range extension.
- **YaRN (Peng et al., 2023):** Partitions the RoPE dimensions into high-frequency (unmodified), low-frequency (fully interpolated), and medium-frequency (smoothly blended via a ramp function) bands combined with an attention-logit temperature factor, enabling long-context extensions to $128{,}000$ tokens and beyond in architectures such as DeepSeek-V3 and DeepSeek-R1.

All three extensions preserve the algebraic structure of RoPE. The rotation composition identity holds regardless of the specific frequency values, because the identity follows from the angle-addition properties of sine and cosine, not from the particular angles used. Modifying the frequencies changes the rotation angles but does not invalidate the relative-distance property. The extensions are adjustments to the frequency tuning, not alterations to the mathematical mechanism.

## Comparative Summary of Positional Encoding Paradigms

| Mechanism | Injection Point | Parameters | Relative Distance | Primary Limitation |
|---|---|---|---|---|
| **Sinusoidal PE** | Input (`X + PE`) | `0` (fixed) | Obscured by `W_Q, W_K` | Entangles content and position |
| **Learned PE** | Input (`X + PE`) | `T_max * d` | None (absolute index) | Hard sequence-length ceiling |
| **Relative Bias** | Logits (`q^T k + b`) | `O(k_max)` | Clipped offset table | Clips offsets beyond window |
| **ALiBi** | Logits (`-m * \|i-j\|`) | `0` (fixed) | Linear distance penalty | Rigid monotonic distance decay |
| **RoPE** | Queries/keys (`R_t`) | `0` (fixed) | Algebraic (`R_{n-m}`) | Needs frequency scaling past `T_train` |
| **iRoPE** | Selected layers (`R_t`) | `0` (fixed) | Algebraic in RoPE layers | Layer-schedule design tuning |

## Final Thoughts

Positional encoding solves a problem that the architecture itself created. The Transformer processes all tokens simultaneously rather than sequentially, which gives it parallelism and scalability, but strips away the one thing that recurrent networks got for free: the knowledge of which token came first. Every mechanism in this series, from sinusoidal addition to geometric rotation to linear penalty, is an attempt to restore that lost ordering information without sacrificing the parallelism that made the Transformer worth building in the first place.

The common thread across every mechanism is a single goal: inject enough positional structure that the model can distinguish token order, without distorting the semantic content that makes each token meaningful. The sinusoidal formula achieves this through additive injection. RoPE achieves it through geometric rotation. ALiBi achieves it through attention-score penalties. Each approach encodes the same fundamental information (where tokens sit relative to each other) through a different mathematical channel.

The embedding tensor, enriched with positional information, is now ready for the computation that determines how each token attends to every other token in the sequence. That computation is the subject of the next series, the [Transformers series](series-transformers.html), which takes this positionally-enriched tensor and constructs the full attention mechanism from first principles.

<p><em>Prefer to read this offline? <a href="../assets/docs/positional-encoding-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Positional Encoding Ebook here.</a></em></p>
