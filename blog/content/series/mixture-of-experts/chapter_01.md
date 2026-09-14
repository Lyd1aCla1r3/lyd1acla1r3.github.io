# Part 1: The Dense FFN Bottleneck
<!-- SUMMARY: The standard dense Feed-Forward Network forces every token to activate the entire parameter bank, creating severe computational inefficiencies at scale. Replacing this monolithic structure with a Mixture of Experts architecture introduces conditional computation, allowing models to scale total parameter capacity independently of the floating-point operations executed per token. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The preceding preface established the core goal: separate a model's total parameter capacity from its per-token computational cost. Grounding this goal in concrete mathematics requires a precise accounting of the waste embedded within the standard monolithic Feed-Forward Network.

## The Dense Activation Penalty

The dense Feed-Forward Network operates as a two-layer key-value memory bank. A token vector $x$ is expanded through a weight matrix $W_1$, passed through a nonlinear activation function, and contracted through a second weight matrix $W_2$:

$$
\text{FFN}(x) = \text{ReLU}(x W_1) W_2
$$

The mathematical dimensions directly dictate the computational cost. A standard toy-scale dense model configures the representation space with a model dimension of $d_{model} = 6$ and an intermediate hidden dimension of $d_{ff} = 8$. The expansion matrix $W_1 \in \mathbb{R}^{6 \times 8}$ contains 48 parameters. The contraction matrix $W_2 \in \mathbb{R}^{8 \times 6}$ contains an identical 48 parameters. The total parameter count for the monolithic layer equals 96 parameters.

The four token representations entering the layer carry the exact geometric coordinates established in the prior Transformer series:

$$
X_{4 \times 6} = \begin{bmatrix}
0.0200 & 1.2900 & 0.1800 & 1.3500 & 0.0000 & 0.6700 \\
0.7400 & 1.7600 & 0.4500 & 1.5200 & 0.2000 & 1.2300 \\
0.8800 & -0.3100 & 1.7800 & 0.9900 & 0.0900 & 0.9100 \\
0.1900 & -1.0300 & 1.5600 & 1.2100 & 0.5800 & 0.6900
\end{bmatrix}
$$

The dense architecture forces every token to activate every parameter. Processing this specific sequence of $T = 4$ tokens requires full execution across the entire layer structure. The sequence activation demands a total of $4 \times 96 = 384$ total operations.

## The Cost of Scale

This monolithic activation strategy scales poorly. A modern 70-billion-parameter dense architecture dedicates approximately 47 billion parameters exclusively to its Feed-Forward Network layers. During text generation, every single token propagating through the network activates all 47 billion parameters. This architectural design creates an unsustainable ceiling on model capacity dictated by the sheer cost of floating-point operations.

The fix is straightforward in concept. Each token should activate only the parameters relevant to its representation, leaving the rest dormant.

## The Mixture of Experts Architecture

The Mixture of Experts paradigm replaces the single dense Feed-Forward Network with $E$ independent, smaller expert networks. A learned router, also called a gating network, examines each $6$-dimensional token vector and selects $k$ experts to process it, where $k$ is strictly less than $E$.

The toy-scale Mixture of Experts architecture establishes specific geometric configurations to match the computational footprint of the dense baseline. The dense baseline activates a total intermediate dimension of $8$. To replicate this active compute footprint, the sparse architecture halves the intermediate dimension of each expert to $d_{ff} = 4$, and sets the active expert count to $k = 2$. When exactly two experts process a token, their combined hidden dimensions perfectly equal the original baseline dimension of $8$. 

The total number of experts is arbitrarily set to $E = 4$. This establishes a pool of networks large enough to demonstrate selective routing while remaining tractable for explicit mathematical calculation. The router projects each token vector into this $4$-dimensional decision space to determine the appropriate assignment.

This structural change dramatically shifts the parameter economics. The total parameter count now far exceeds what any single token activates. The $4$ experts each contain $48$ parameters, totaling $192$ parameters. The router requires a $6 \times 4$ weight matrix, adding $24$ parameters. The complete architecture stores $216$ parameters total.

Processing a single token, however, touches only a fraction of that capacity. The token passes through the router, activating $24$ parameters, and through exactly two experts, activating $96$ parameters. The per-token cost is just $120$ active parameters. 

| Configuration | Total Parameters | Active Parameters per Token | Ratio |
|---|---|---|---|
| Dense FFN, $d_{ff}=8$ | $6 \times 8 + 8 \times 6 = 96$ | 96 | 1:1 |
| MoE, $E=4, k=2, d_{ff}=4$ | $4 \times [6 \times 4 + 4 \times 6] + 6 \times 4 = 216$ | $2 \times 48 + 24 = 120$ | 1.8:1 |

Comparing these values directly reveals the mathematical advantage. The Mixture of Experts configuration houses $2.25$ times the total parameters of the dense baseline, calculated as $216$ divided by $96$. Simultaneously, the architecture requires only $1.25$ times the active compute per token, calculated as $120$ divided by $96$. This toy-scale ratio expands dramatically in production environments, decoupling knowledge capacity from inference latency entirely.

The structural foundation for sparse computation is now established. The subsequent section formalizes the mathematics of the router, calculating exactly how the architecture maps specific tokens to targeted expert pathways.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
