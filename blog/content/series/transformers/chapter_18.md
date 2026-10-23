# Part 18: Final Softmax and Predictions

<!-- SUMMARY: The unbounded vocabulary logits are transformed into a strict probability distribution using the softmax function. Analyzing this distribution reveals the untrained network's maximum mathematical uncertainty, while techniques like temperature scaling and Top-K decoding provide mechanisms to shape this entropy during actual text generation. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

Projecting the contextualized vectors from Layer 2 through the unembedding matrix $W_U$ yields a $4 \times 12$ matrix of raw vocabulary scores known as logits. Each scalar entry measures the inner-product alignment between a sequence position and one of the twelve vocabulary tokens. Raw logits establish a relative ranking across candidates, yet they span arbitrary real bounds and do not sum to $1.0$. Converting these unnormalized scores into actionable token predictions requires a row-wise normalization function.

## Normalizing Vocabulary Logits with Softmax

The architecture applies the Softmax function across the $V = 12$ vocabulary columns of each logit row. Softmax exponentiates every scalar logit $z_i$ and divides by the sum of all exponentiated logits in that row. Exponentiation maps negative and positive numbers alike onto strictly positive values while non-linearly amplifying gaps between scores: a modest lead in raw logit space translates into a multiplicative ratio in probability space. Dividing by the row sum normalizes the outputs onto the interval $(0, 1)$, creating a valid probability distribution whose entries across the $V = 12$ vocabulary columns sum to $1.0$:

$$
P(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{V} e^{z_j}}
$$

Here, $z_i$ denotes the raw logit for vocabulary index $i$ in a given sequence row, and $\sum_{j=1}^{V} e^{z_j}$ sums the exponentiated logits across all $V = 12$ vocabulary tokens. Applying this transformation row by row to the four-decimal `Logits` matrix $X_{\text{final}} W_U$ from Part 17 produces the next-token probability distributions following `<BOS>`, `i`, `woke`, and `up` (note that shifting Row 2 by a constant $-0.0450$ to `[-0.0180, -0.0135, ..., 0.0315]` yields the identical Softmax row because $\text{Softmax}(z + c) = \text{Softmax}(z)$):

$$
\text{Logits} = \begin{bmatrix}
-0.0270 & -0.0315 & -0.0360 & -0.0405 & -0.0450 & -0.0495 & -0.0540 & -0.0585 & \dots & -0.0765 \\
 0.0270 &  0.0315 &  0.0360 &  0.0405 &  0.0450 &  0.0495 &  0.0540 &  0.0585 & \dots &  0.0765 \\
-0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & -0.0675 & \dots & -0.0675 \\
 0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 &  0.0675 & \dots &  0.0675
\end{bmatrix}
$$

$$
\text{Probabilities} = \begin{bmatrix}
 0.0854 &  0.0850 &  0.0846 &  0.0843 &  0.0839 &  0.0835 &  0.0831 &  0.0828 & \dots &  0.0813 \\
 0.0813 &  0.0817 &  0.0820 &  0.0824 &  0.0828 &  0.0831 &  0.0835 &  0.0839 & \dots &  0.0854 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833 \\
 0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 &  0.0833 & \dots &  0.0833
\end{bmatrix}
$$

Row 4 of the `Probabilities` matrix holds the next-token distribution following `up`, where the training objective requires predicting `late` (vocabulary index `8`). Constant scores of $0.0675$ across all twelve columns of Row 4 in `Logits` cause every entry in Row 4 of `Probabilities` to evaluate to $1 / 12 \approx 0.0833$. A uniform distribution of $1 / 12$ across twelve classes represents maximum Shannon entropy: the untrained network considers every vocabulary token equally probable. This uniform output confirms that the uncalibrated projection matrices possess the structural topology to route information but have not yet encoded task-specific weights.

## Shaping the Output Distribution

Autoregressive text generation selects the next token from the final row of the probability matrix. Always choosing the single index with the maximum probability is known as greedy decoding; although deterministic, greedy selection frequently traps language models in repetitive phrasing. Controlling generation diversity requires reshaping the logit distribution prior to sampling.

Dividing each raw logit by a positive scalar temperature parameter $T$ before applying Softmax modulates the entropy of the output distribution:

$$
\text{Scaled Logit}_i = \frac{z_i}{T}
$$

Production inference engines combine temperature scaling with truncation filters such as Top-$K$ and Top-$P$ (nucleus) decoding:

| Decoding Strategy | Mathematical Mechanism | Effect on Output Distribution |
| :--- | :--- | :--- |
| **Greedy Decoding** | Selects `argmax_i P(z_i)` directly | Collapses generation to the single highest-probability token |
| **Low Temperature (`T < 1`)** | Divides logits by `T in (0, 1)` before Softmax | Magnifies gaps between logits, concentrating probability mass on top candidates |
| **High Temperature (`T > 1`)** | Divides logits by `T > 1` before Softmax | Compresses differences between logits, flattening the distribution toward uniform entropy |
| **Top-K Decoding** | Retains the `K` largest logits and sets remaining logits to `-inf` | Prunes low-probability tail tokens while preserving relative weights among the top `K` choices |
| **Top-P (Nucleus) Sampling** | Retains the smallest sorted token subset whose cumulative probability reaches `p` | Adapts candidate pool size dynamically to the sharpness of each step's distribution |

### Autoregressive Generation and KV-Cache Scaling

Sampling a token from Row 4 (such as `late`) during autoregressive inference appends that token to the sequence and initiates a new forward step to predict position 5. The causal mask blocks earlier tokens (`<BOS>`, `i`, `woke`, `up`) from attending to the newly appended token, so their Key and Value projections $K, V \in \mathbb{R}^{S \times d_k}$ across every layer and head remain unchanged. Caching those historical Key and Value rows in a **KV cache** avoids recomputing $X W_K$ and $X W_V$ for past positions, reducing per-step attention compute from quadratic $O(S^2 d_{\text{model}})$ to linear $O(S d_{\text{model}})$ at a memory cost of $2 \times L \times n_{\text{heads}} \times d_k \times S$ scalars ($2 \times 2 \times 3 \times 2 \times 4 = 96$ cached floats for the 4-token prompt).

Making the network predict `late` after `<BOS>` `i` `woke` `up` without relying on heuristic decoding constraints requires shifting the underlying geometry so the logit at index `8` dominates Row 4 naturally. Achieving that shift requires a loss function that quantifies the error of the uniform `0.0833` prediction (Part 19) and a backward pass that updates every weight matrix in the network (Parts 20 through 24).

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
