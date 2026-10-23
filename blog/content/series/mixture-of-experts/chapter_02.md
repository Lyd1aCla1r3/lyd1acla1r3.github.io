# Part 2: The Router
<!-- SUMMARY: The monolithic feed-forward network is replaced by a routing mechanism that dynamically evaluates the affinity of each token for specialized sub-networks. This gating network projects the token representation into a lower-dimensional space to compute a strict probability distribution over available experts, enabling conditional computation. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The dense feed-forward bottleneck makes the case for separating total parameter count from per-token computation. The mechanism that performs this separation is a dynamic gate that decides which subset of parameters activates for any given token.

## The Gating Network

The foundational component of a Mixture of Experts layer is the router, formally known as the gating network. This mechanism is a learned linear projection that maps the incoming token representation from the model dimension $d_{model}$ into the expert dimension $E$.

The standard sequence of four token vectors, $X_{4 \times 6}$, arrives from the residual stream, and the gating network multiplies it by a weight matrix $W_g \in \mathbb{R}^{d_{model} \times E}$. Each 0-indexed column of $W_g$ (corresponding to Expert 0 through Expert 3) represents the geometric centroid of an expert within the $6$-dimensional embedding space.

$$
X_{4 \times 6} = \begin{bmatrix}
 0.0200 & 1.2900 & 0.1800 & 1.3500 & 0.0000 & 0.6700 \\
 0.7400 & 1.7600 & 0.4500 & 1.5200 & 0.2000 & 1.2300 \\
 0.8800 & -0.3100 & 1.7800 & 0.9900 & 0.0900 & 0.9100 \\
 0.1900 & -1.0300 & 1.5600 & 1.2100 & 0.5800 & 0.6900
\end{bmatrix}
$$

$$
W_g = \begin{bmatrix}
 0.0497 & -0.0138 & 0.0648 & 0.1523 \\
-0.0234 & -0.0234 & 0.1579 & 0.0767 \\
-0.0469 & 0.0543 & -0.0463 & -0.0466 \\
 0.0242 & -0.1913 & -0.1725 & -0.0562 \\
-0.1013 & 0.0314 & -0.0908 & -0.1412 \\
 0.1466 & -0.0226 & 0.0068 & -0.1425
\end{bmatrix}
$$

The dot product between the token vector and the expert centroid measures affinity. Computing this projection yields the raw router logits, $h(x) = X W_g$.

$$
h(x)_{4 \times 4} = \begin{bmatrix}
 0.0932 & -0.2941 & -0.0317 & -0.0777 \\
 0.1712 & -0.3393 & 0.0330 & -0.0621 \\
 0.1156 & -0.1155 & -0.2472 & -0.1707 \\
 0.0320 & -0.1227 & -0.4794 & -0.3710
\end{bmatrix}
$$

The resulting tensor contains the unnormalized preference of each token for each of the four available experts.

## Hard Routing and Top-K Masking

The unnormalized tensor, $h(x)$, represents the affinity of each token across the four available experts. Each row corresponds to a single token in the sequence, and each column corresponds to one of the four experts. Converting these raw logits into usable routing decisions requires normalization.

Designing a routing mechanism requires balancing differentiability, contextual adaptability, and sparse execution. Early conditional computation research explored three primary routing paradigms before converging on learned hard routing:

- **Soft Routing:** Every expert processes every token, and the layer computes a continuous weighted average across all expert outputs. Full differentiability is preserved, but activating every parameter for every token destroys the computational savings of sparsity. Sequence-level soft routing variants, which construct expert inputs as weighted averages across all tokens in a sequence, also require visibility into future tokens and violate autoregressive causal masking.
- **Hash-Based Routing:** A deterministic hash function maps each discrete token ID directly to an expert without learned gating parameters. Static hashing provides zero contextual plasticity: a polysemous token such as `"bank"` routes to the same expert whether the surrounding clause describes a river or a financial institution. Natural language token frequencies follow a Zipfian power law, so deterministic hashing maps high-frequency tokens to specific experts, creating severe load imbalance while starving experts assigned to rare tokens.
- **Learned Hard Routing (Top-$K$ Selection):** A learned gating projection scores each contextualized token vector and dispatches it to a discrete subset of $k < E$ experts, leaving all unselected experts dormant. Autoregressive decoders rely on hard top-$k$ routing to preserve causal masking while decoupling total parameter capacity from per-token compute.

The masked logit tensor is the direct output of an algorithmic selection operation applied to the raw logits, rather than the result of a matrix multiplication. For a configuration where $k=2$, an algorithmic pass evaluates each row independently, identifies the two highest numerical values, and explicitly masks all other values in that row to negative infinity. The output tensor takes the following form:

$$
\text{TopK}(h(x), 2)_{4 \times 4} = \begin{bmatrix}
 0.0932 & -\infty & -0.0317 & -\infty \\
 0.1712 & -\infty & 0.0330 & -\infty \\
 0.1156 & -0.1155 & -\infty & -\infty \\
 0.0320 & -0.1227 & -\infty & -\infty
\end{bmatrix}
$$

This discrete masking operation introduces a fundamental differentiability barrier. In continuous calculus, a derivative measures how an infinitesimally small perturbation in an input variable alters the output. The algorithmic selection of the top two elements acts as a discontinuous step function. A slight increase in a raw logit that fails to cross the ranking threshold leaves the discrete routing assignment unchanged. An infinitesimal perturbation in the input logit produces zero change in the discrete selection mask, causing the selection gradient to evaluate to zero. Without a continuous gradient path through the ranking threshold, the discrete selection step itself is non-differentiable.

## Softmax Normalization

The top-$k$ masking operation identifies the surviving experts without normalizing their values. To combine the outputs of the selected experts proportionally, the masked logits pass through a row-wise softmax function. This operation converts the surviving logits into a valid probability distribution over the selected experts, ensuring their weights sum to $1.0$:

$$
g(x)_{4 \times 4} = \text{Softmax}(\text{TopK}(h(x), 2))
$$

$$
g(x)_{4 \times 4} = \begin{bmatrix}
 0.5312 & 0.0000 & 0.4688 & 0.0000 \\
 0.5345 & 0.0000 & 0.4655 & 0.0000 \\
 0.5575 & 0.4425 & 0.0000 & 0.0000 \\
 0.5386 & 0.4614 & 0.0000 & 0.0000
\end{bmatrix}
$$

The resulting gating weights, $g(x)$, specify the proportional contribution each selected expert provides to the final token representation. Indexing the four expert columns from $0$ to $3$, the first and second tokens route to Expert 0 and Expert 2, while the third and fourth tokens route to Expert 0 and Expert 1.

Applying a continuous softmax function does not make the discrete ranking step differentiable; instead, the normalization provides a continuous gradient path exclusively for the logits that survived the mask. During backpropagation, gradients flow backward from the language modeling loss, through the softmax operator, and into the unmasked entries of the logit tensor. Surviving entries retain their original dot-product values, allowing the gradient to pass cleanly into the corresponding columns of $W_g$.

Replacing unselected logits with $-\infty$ severs the backward path for dormant experts through the properties of the exponential function. Inside the softmax operator, $e^{-\infty}$ evaluates to $0$, and the local derivative $\lim_{z \to -\infty} \frac{d}{dz} e^z = 0$ vanishes as well. Multiplying this zero-valued local derivative into the backward chain rule zeroes out the gradient for every masked column of $W_g$ without producing undefined numerical states.

This selective gradient flow carries a critical training consequence. The gating network receives zero gradient signal from the primary loss for unselected experts, whereas surviving pathways receive continuous updates. Discrete ranking boundaries remain invisible to standard backpropagation, so gradient descent adjusts only the centroids of experts that were already selected. This asymmetry motivates a dedicated load-balancing mechanism, derived in Chapter 4 and Chapter 5, to prevent the router from reinforcing the same subset of experts indefinitely.

The gating network has resolved the routing decisions for the sequence. The execution of the independent expert feed-forward computations and their subsequent weighted combination is detailed in the next section.

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
