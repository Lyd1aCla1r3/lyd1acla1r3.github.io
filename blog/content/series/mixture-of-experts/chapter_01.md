# Part 1: The Dense FFN Bottleneck
<!-- SUMMARY: The standard dense Feed-Forward Network forces every token to activate the entire parameter bank, creating severe computational inefficiencies at scale. Replacing this monolithic structure with a Mixture of Experts architecture introduces conditional computation, allowing models to scale total parameter capacity independently of the floating-point operations executed per token. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The preceding preface established the core goal: separate a model's total parameter capacity from its per-token computational cost. Grounding this goal in concrete mathematics requires a precise accounting of the waste embedded within the standard monolithic Feed-Forward Network.

## The Dense Activation Penalty

The dense Feed-Forward Network operates as a two-layer key-value memory bank. A token vector $x$ is expanded through a weight matrix $W_1$, passed through a nonlinear activation function, and contracted through a second weight matrix $W_2$:

$$
\text{FFN}(x) = \text{ReLU}(x W_1) W_2
$$

The mathematical dimensions directly dictate the computational cost. A standard toy-scale dense model configures the representation space with a model dimension of $d_{model} = 6$ and an intermediate hidden dimension of $d_{ff} = 8$. The expansion matrix $W_1 \in \mathbb{R}^{6 \times 8}$ contains 48 parameters. The contraction matrix $W_2 \in \mathbb{R}^{8 \times 6}$ contains an identical 48 parameters. The total parameter count for the monolithic layer equals 96 parameters.

The four token representations entering the layer carry the four-token coordinate matrix established in the prior [Transformer series](series-transformers.html):

$$
X_{4 \times 6} = \begin{bmatrix}
0.0200 & 1.2900 & 0.1800 & 1.3500 & 0.0000 & 0.6700 \\
0.7400 & 1.7600 & 0.4500 & 1.5200 & 0.2000 & 1.2300 \\
0.8800 & -0.3100 & 1.7800 & 0.9900 & 0.0900 & 0.9100 \\
0.1900 & -1.0300 & 1.5600 & 1.2100 & 0.5800 & 0.6900
\end{bmatrix}
$$

The dense architecture forces every token to activate every parameter. Processing this sequence of $T = 4$ tokens requires full execution across the entire layer structure, demanding $4 \times 96 = 384$ parameter activations across the batch.

## The Cost of Scale

This monolithic activation strategy scales poorly. A modern 70-billion-parameter dense architecture dedicates approximately 47 billion parameters exclusively to its Feed-Forward Network layers. During text generation, every single token propagating through the network activates all 47 billion parameters. This architectural design creates an unsustainable ceiling on model capacity dictated by the sheer cost of floating-point operations.

The fix is straightforward in concept. Each token should activate only the parameters relevant to its representation, leaving the rest dormant.

## The Mixture of Experts Architecture

The Mixture of Experts paradigm replaces the single dense Feed-Forward Network with $E$ independent, smaller expert networks. A learned router, also called a gating network, examines each $6$-dimensional token vector and selects $k$ experts to process it, where $k$ is strictly less than $E$.

The toy-scale Mixture of Experts architecture establishes specific geometric dimensions to match the active computational footprint of the dense baseline. The dense baseline activates an intermediate dimension of $8$. To replicate this active hidden width, the sparse architecture halves the intermediate dimension of each expert to $d_{ff} = 4$ and sets the active expert count to $k = 2$. Routing a token through two selected experts yields a combined hidden dimension of $2 \times 4 = 8$, matching the original baseline dimension.

The total number of experts is set to $E = 4$. This configuration establishes a pool of sub-networks large enough to demonstrate selective routing while remaining tractable for explicit matrix calculation. The router projects each token vector into this $4$-dimensional decision space to determine the expert assignment.

This structural change shifts the parameter economics by decoupling stored capacity from active computation. Each of the $4$ experts contains $6 \times 4 + 4 \times 6 = 48$ parameters, totaling $192$ expert parameters. The router requires a $6 \times 4$ weight matrix, adding $24$ parameters and bringing the complete architecture to $216$ total parameters. Processing a single token activates only the router ($24$ parameters) and two selected experts ($2 \times 48 = 96$ parameters), resulting in $120$ active parameters per token.

| Configuration | Layer Hyperparameters | Total Parameters | Active Parameters per Token | Total-to-Active Ratio |
| :--- | :--- | :--- | :--- | :--- |
| **Dense FFN** | `d_model = 6`, `d_ff = 8` | `6 * 8 + 8 * 6 = 96` | `96` | `1.0 : 1` |
| **Sparse MoE** | `E = 4`, `k = 2`, `d_ff = 4` | `4 * (6 * 4 + 4 * 6) + 6 * 4 = 216` | `2 * 48 + 24 = 120` | `1.8 : 1` |

Comparing these values reveals the mathematical advantage of conditional computation. Within the sparse layer, total parameter capacity exceeds active per-token compute by a ratio of $1.8:1$ ($216$ total parameters versus $120$ active parameters). Relative to the dense baseline, the Mixture of Experts configuration stores $2.25$ times the total parameters ($216 / 96$) while requiring $1.25$ times the active parameters per token ($120 / 96$). In production environments where expert matrices far outweigh the router projection, this ratio expands dramatically, decoupling knowledge capacity from inference latency.

The structural foundation for sparse computation is now established. The next chapter formalizes the mathematics of the router, calculating how the gating network maps specific tokens to targeted expert pathways.

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
