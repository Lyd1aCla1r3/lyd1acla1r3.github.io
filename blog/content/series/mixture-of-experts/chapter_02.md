# Part 2: The Router
<!-- SUMMARY: The monolithic feed-forward network is replaced by a routing mechanism that dynamically evaluates the affinity of each token for specialized sub-networks. This gating network projects the token representation into a lower-dimensional space to compute a strict probability distribution over available experts, enabling conditional computation. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The dense feed-forward bottleneck makes the case for separating total parameter count from per-token computation. The mechanism that performs this separation is a dynamic gate that decides which subset of parameters activates for any given token.

## The Gating Network

The foundational component of a Mixture of Experts layer is the router, formally known as the gating network. This mechanism is a learned affine projection that maps the incoming token representation from the model dimension into the expert dimension.

Given the standard sequence of four token vectors, $X_{4 \times 6}$, moving along the residual stream, the gating network applies a weight matrix, $W_g \in \mathbb{R}^{d_{model} \times E}$. Each column of $W_g$ represents the geometric centroid of an expert within the embedding space.

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

Early conditional computation architectures experimented with soft routing. In a soft routing paradigm, every token is processed by every expert, and the final representation is computed as a weighted average of all expert outputs based on a continuous probability distribution. While this preserves smooth differentiability, activating all parameters for all tokens defeats the computational efficiency that originally motivated the architecture. The combined parameter count of the routing mechanism and all experts far exceeds the size of a dense model, resulting in an unacceptable increase in computational cost. Furthermore, modern soft routing variants construct expert inputs by taking a weighted average of all tokens in the sequence. This operation requires visibility into future tokens, mandating a violation of causal masking. Consequently, production causal models, which are autoregressive decoders that generate text left-to-right, utilize hard routing exclusively. Hard routing strictly limits computation by dispatching each token to a discrete, restricted subset of experts, ensuring that unselected experts perform zero computation.

An alternative mechanism, hash-based routing, attempted to eliminate the learned gating network entirely by assigning tokens using a deterministic hash function applied to the token ID. This approach was initially pursued because it requires zero routing parameters. The method was swiftly abandoned due to two critical flaws. First, it provided zero contextual plasticity. A token like "bank" routes to the exact same expert regardless of whether the surrounding sequence describes a river or a financial institution. The fixed routing mechanism cannot adapt to the shifting semantic meaning of the contextualized hidden state. Second, human vocabulary follows Zipf's law, meaning a small handful of tokens appear with extreme frequency. A deterministic hash function that assigns highly frequent tokens to a specific expert causes that expert to suffer catastrophic load imbalance, while experts assigned to rare words starve.

The standard mechanism that resolves these limitations is top-$k$ selection, a direct implementation of hard routing. This operation successfully decouples the total parameter capacity of the model from the active computational cost per token.

The masked logit tensor is the direct output of an algorithmic selection operation applied to the raw logits, rather than the result of a matrix multiplication. For a configuration where $k=2$, an algorithmic pass evaluates each row independently, identifies the two highest numerical values, and explicitly masks all other values in that row to negative infinity. The output tensor takes the following form:

$$
\text{TopK}(h(x), 2)_{4 \times 4} = \begin{bmatrix}
 0.0932 & -\infty & -0.0317 & -\infty \\
 0.1712 & -\infty & 0.0330 & -\infty \\
 0.1156 & -0.1155 & -\infty & -\infty \\
 0.0320 & -0.1227 & -\infty & -\infty
\end{bmatrix}
$$

This discrete masking operation introduces a mathematical friction. In continuous calculus, a derivative measures how an infinitesimally small change in an input variable affects the output. The algorithmic selection of the top two elements acts as a discontinuous step function. If a raw logit increases slightly but fails to alter the ranking threshold, the discrete routing assignment remains entirely unchanged. An infinitesimal change in the input logit produces precisely zero change in the routing selection, causing the mathematical gradient to evaluate to zero. Without a continuous gradient signal, the optimizer cannot update the gating weights, rendering the step non-differentiable.

## Softmax Normalization

The top-$k$ masking operation identifies the surviving experts without normalizing their values. To combine the outputs of the selected experts proportionally, the masked logits pass through a continuous softmax function. This operation converts the surviving logits into a strict probability distribution over the selected experts, ensuring their weights sum to exactly one.

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

The resulting gating weights, $g(x)$, specify the exact proportional contribution each selected expert provides to the final token representation. The first token is routed to Experts 1 and 3. The second token undergoes an identical routing path. The third and fourth tokens are routed to Experts 1 and 2.

The application of a continuous softmax function does not circumvent the non-differentiability of the algorithmic masking step; it simply provides a differentiable path for the values that survived the mask. During backpropagation, gradients flow backward from the final loss, through the softmax function, and strictly into the non-masked elements of the logit tensor. These selected elements are mathematically identical to the original raw logits, allowing the gradient to pass cleanly through to the corresponding columns of $W_g$. 

The masking operation replaces unselected logits with a constant value of negative infinity. The negative infinity is a mathematically rigorous trick to set the derivative to exactly zero, cleanly severing the backward path without throwing any errors or causing undefined behavior. This substitution is safely evaluated by the exponential function inside the softmax operator, where $e^{-\infty}$ equals zero. In continuous calculus, the derivative of the exponential function $e^x$ as $x$ approaches negative infinity evaluates cleanly to zero. When the chain rule multiplies this zero-valued local derivative backward, the mathematical path is severed. The gating network receives no gradient signal for unselected experts, while gradients continue to flow unaffected through the independent paths of the surviving logits. The discrete ranking boundaries remain invisible to calculus, preventing the architecture from learning which experts to select directly via gradient descent. Gradient descent only adjusts the centroids of the experts already selected. This structural limitation necessitates a dedicated load balancing mechanism, explored in a subsequent chapter, to prevent the routing mechanism from endlessly reinforcing the same subset of parameters.

The gating network has successfully resolved the routing decisions for the sequence. The execution of the independent expert feed-forward computations and their subsequent weighted combination is detailed in the next section.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
