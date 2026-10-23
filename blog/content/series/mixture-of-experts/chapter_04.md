# Part 4: Expert Collapse
<!-- SUMMARY: The gating network's reliance on backpropagation introduces a severe positive feedback loop that systematically starves under-utilized pathways. Without intervention, this dynamic degenerates the sparse architecture into a heavily imbalanced network, severely wasting parameter capacity. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The completed forward pass processes tokens through independent network branches and recombines them into a unified residual stream. This dynamic routing mechanism introduces a catastrophic failure mode during training.

## The Positive Feedback Loop

At initialization, the gating weights in the router matrix consist of small random values. In theory, a random initialization distributes tokens evenly across all experts. In practice, finite-batch variance guarantees that some experts receive slightly more tokens than others. Natural language amplifies this variance because token embeddings cluster tightly by syntax and semantics rather than distributing uniformly across $\mathbb{R}^{d_{model}}$. An expert whose random centroid happens to align with a frequent token cluster, such as common punctuation, captures an immediate, disproportionate share of assignments.

This initial asymmetry triggers a self-reinforcing positive feedback loop. An expert that processes a larger share of tokens during the first training step participates in more forward passes and accumulates a higher volume of gradient updates. Backpropagation then adjusts the shared router matrix during loss minimization to assign even higher routing probabilities to that already active expert.

### The Chain-Rule Centroid Collapse

The mathematical driver of this collapse lies in the chain rule of calculus applied to the linear router projection. The router computes each affinity logit $h(x)_i = x \cdot w_g^{(i)}$ as the dot product between the input token vector $x \in \mathbb{R}^{d_{model}}$ and the $i$-th expert column $w_g^{(i)} \in \mathbb{R}^{d_{model}}$ of the gating matrix $W_g$. Linear projection without an intermediate nonlinearity causes the local partial derivative of the logit with respect to the expert column to evaluate directly to the input token vector itself ($\frac{\partial h(x)_i}{\partial w_g^{(i)}} = x$).

By the chain rule, the gradient update applied to an active expert column adds a scaled copy of the processed token vector directly into $w_g^{(i)}$. Adding a scaled vector into an existing column alters the expert centroid in two permanent geometric ways:

- **Directional Alignment:** Vector addition rotates the active expert column $w_g^{(i)}$ toward the processed token vector $x$, increasing cosine similarity for future tokens from the same semantic cluster.
- **Magnitude Inflation:** Repeated vector additions increase the Euclidean norm $\|w_g^{(i)}\|$ of the active expert column relative to unselected columns, which remain frozen at their small random initialization norms.

This norm asymmetry corrupts routing on subsequent batches. Unselected experts receive zero gradient updates through the Top-$K$ mask, leaving their columns in $W_g$ as low-magnitude random noise that yields small dot products. An active expert that has accumulated multiple gradient updates possesses a larger column norm, producing a higher dot product $x_{\text{new}} \cdot w_g^{(i)} = \|x_{\text{new}}\|\,\|w_g^{(i)}\|\cos\theta$ even for unrelated tokens from new training batches. That marginal norm advantage captures a larger fraction of tokens in the next batch, which in turn delivers a larger sum of gradient updates during the backward pass. Over thousands of iterations, this compounding feedback loop concentrates all routing traffic into a single dominant expert and starves the frozen pathways.

## Simulating Progressive Starvation

A numerical simulation demonstrates this starvation dynamic over a simplified training loop. To measure the underlying preference of the network, the simulation tracks the soft routing distribution. This is the raw softmax probability calculated before the discrete top-k mask forces the unselected experts to zero.

Retrieving the raw router logits computed in Chapter 2 prior to the masking operation yields the following scores for the four tokens:

$$
H = \begin{bmatrix} 
0.0932 & -0.2941 & -0.0317 & -0.0777 \\
0.1712 & -0.3393 &  0.0330 & -0.0621 \\
0.1156 & -0.1155 & -0.2472 & -0.1707 \\
0.0320 & -0.1227 & -0.4794 & -0.3710 
\end{bmatrix}
$$

Applying the standard softmax function over these unmasked logits produces the true underlying routing probabilities for each token. 

$$
P = \begin{bmatrix} 
0.2937 & 0.1994 & 0.2593 & 0.2476 \\
0.3065 & 0.1839 & 0.2669 & 0.2427 \\
0.3086 & 0.2449 & 0.2147 & 0.2318 \\
0.3200 & 0.2742 & 0.1919 & 0.2139 
\end{bmatrix}
$$

Averaging these probabilities column-wise across the four tokens establishes the network's initial soft routing distribution across the batch. Random weight initialization places this starting distribution in a nearly balanced state:

$$
\text{Routing Distribution (Step 0)} = \begin{bmatrix} 0.3072 & 0.2256 & 0.2332 & 0.2340 \end{bmatrix}
$$

The Top-2 masking operation applied to these same logits in Chapter 2 routed all four tokens to Expert 0, distributed two tokens each to Expert 1 and Expert 2, and assigned zero tokens to Expert 3. Executing five consecutive training steps via a numerical simulation illustrates how unconstrained gradient updates amplify this initial gap. At each step, active experts and their corresponding router columns update proportionally to the tokens they process, whereas Expert 3 processes zero tokens and remains frozen at its initialized weights.

Successive training steps shift the probability mass rapidly toward Expert 0 across the five-step trajectory:

| Training Step | Expert 0 (`P_0`) | Expert 1 (`P_1`) | Expert 2 (`P_2`) | Expert 3 (`P_3`) | Routing Regime |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 0** | `0.3072` | `0.2256` | `0.2332` | `0.2340` | Near-uniform random initialization |
| **Step 1** | `0.5141` | `0.1964` | `0.2026` | `0.0869` | Expert 0 exceeds half of batch probability mass |
| **Step 2** | `0.7751` | `0.1075` | `0.1098` | `0.0076` | Expert 3 approaches starvation (`< 1%` mass) |
| **Step 3** | `0.9173` | `0.0409` | `0.0416` | `0.0002` | Expert 0 absorbs over `90%` of routing probability |
| **Step 4** | `0.9755` | `0.0123` | `0.0122` | `0.0000` | Secondary pathways decay below `1.5%` |
| **Step 5** | `0.9944` | `0.0029` | `0.0027` | `0.0000` | Complete single-expert monopoly |

By the fifth step, the routing distribution reaches total collapse, with Expert 0 monopolizing the layer while the remaining probability mass approaches zero:

$$
\text{Routing Distribution (Step 5)} = \begin{bmatrix} 0.9944 & 0.0029 & 0.0027 & 0.0000 \end{bmatrix}
$$

The consequence is severe parameter waste. Sparse routing is designed to decouple total parameter capacity from per-token computational cost. Collapsing the router to a single dominant expert degenerates the sparse layer into a narrow dense model. The hardware still allocates memory to store the dormant experts while routing every token through the same overloaded pathway, dividing the effective representational capacity of the layer by the number of experts.

Preventing this collapse requires direct intervention. An auxiliary loss function that penalizes unbalanced routing and forces the network to use all available experts is detailed in the next chapter.

<p><em>Prefer to read this offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
