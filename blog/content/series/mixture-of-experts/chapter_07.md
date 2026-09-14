# Part 7: Fine-Grained Experts and Shared Expert Isolation

<!-- SUMMARY: The elimination of static hardware capacity constraints enables a radical restructuring of the expert layer into a highly granular federation of specialized networks. Isolating a subset of these networks as universal shared experts guarantees the application of foundational linguistic patterns, allowing the remaining routed experts to achieve unprecedented expressive power through combinatorial activation without increasing the computational budget per token. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The transition to dropless computation and block-sparse matrix operations eliminates the physical capacity constraint that historically bottlenecked routing. Small numbers of massive experts were previously necessary to keep hardware utilization stable. With 64 tiny experts, token assignments become highly jagged, and under strict capacity limits, this means massive dropping or padding waste. Block-sparse execution lets the hardware process these variable-length queues efficiently, removing that limitation. This freedom opens the door to hyper-granular expert configurations, shifting the design from coarse domain buckets toward combinatorial expressivity.

## The Coarse Expert Problem

Early sparse architectures rely on a small total number of experts, typically $E=8$, selecting $k=2$ per token. To maintain a constant parameter count, each of these eight experts must contain a massive weight matrix. The limitation of this coarse configuration emerges during training. The router can only partition the token space into eight macroscopic buckets, forcing each expert to bundle vast, unrelated knowledge domains into the same physical weights.

A single coarse expert simultaneously acts as the repository for Python syntax, historical dates, and geometric reasoning. This artificial bundling dilutes the specialization of the expert. When a token requires geometric reasoning, activating the expert necessarily pulls in the dormant weights dedicated to Python syntax, wasting memory bandwidth and computational capacity on irrelevant parameters. 

Fine-grained expert segmentation, introduced in the DeepSeekMoE architecture by Dai and colleagues in 2024, solves this problem by shattering the monolithic experts into a massive federation of smaller networks. Instead of $8$ large experts, the model deploys $64$ smaller experts. To maintain identical active computation per token, the router selects $8$ of these smaller experts rather than $2$ large ones.

## Combinatorial Expressivity

The power of fine-grained segmentation stems from combinatorics rather than pure parameter scaling. The number of distinct functional pathways a token can take through the MoE layer dictates the expressive capacity of the model.

The mathematical number of distinct routing paths is calculated using the standard combinations formula, which determines the number of ways to select a subset of $k$ items from a larger set of $n$ items without regard to the order of selection:

$$
\binom{n}{k} = \frac{n!}{k!(n-k)!}
$$

The factorial $n!$ computes the total number of permutations, while the denominator $k!(n-k)!$ removes the duplicate permutations that consist of the identical chosen experts arranged in a different order.

In the coarse configuration, choosing 2 experts out of a total pool of 8 yields a strictly bounded number of possible routing combinations:

$$
\binom{8}{2} = \frac{8!}{2!(8-2)!} = 28 \text{ combinations}
$$

Shattering the layer into the fine-grained configuration, choosing 8 experts out of 64, produces an explosive expansion in the number of distinct computational paths:

$$
\binom{64}{8} = \frac{64!}{8!(64-8)!} = 4,426,165,368 \text{ combinations}
$$

Scaling to the ultra-fine granularity of DeepSeek-V3, which selects 8 experts from a pool of 256, yields approximately $4.38 \times 10^{14}$ distinct routing combinations. This combinatorial explosion allows the network to assemble a highly precise, bespoke feed-forward network for every individual token by dynamically composing atomic slivers of specialized knowledge, all without increasing the active computational budget.

## Shared Expert Isolation

Forcing all FFN parameters to undergo routing introduces a structural inefficiency. Certain linguistic components, such as grammar syntax, punctuation rules, and foundational logic, are universally required by almost every token in a sequence. If all experts are subject to dynamic routing, the network is forced to redundantly encode these universal rules across multiple routed experts to ensure they are available regardless of which specific combination the router selects.

Shared expert isolation optimizes this redundancy by explicitly partitioning the layer. A small number of experts, designated as $K_s$, are permanently isolated from the router and activated unconditionally for every token. These shared experts act as a universal memory bank for foundational patterns. The remaining experts, designated as $E_r$, act as the routed pool from which $K_r$ experts are dynamically selected. 

This isolation allows the routed experts to shed their generalized knowledge and achieve extreme, narrow specialization. The combined forward pass mathematically merges the unconditional shared representation with the dynamic routed representation:

$$
y = x + \sum_{j=1}^{K_s} \text{FFN}_j^{shared}(x) + \sum_{i \in \mathcal{K}} g_i \cdot \text{FFN}_i^{routed}(x)
$$

This equation defines the exact computation executed for a single token. The original input token vector $x$ passes through the residual connection, ensuring the baseline representation is preserved. The first summation adds the output of all $K_s$ shared experts, applying their universal transformations unconditionally. The second summation calculates the specialized update by iterating exclusively over the subset of selected routed experts, denoted by the index set $\mathcal{K}$. Each active routed expert processes the input vector $x$, and its output is scaled by the corresponding gating weight $g_i$ assigned by the router. This scaling ensures the network dynamically adjusts the influence of each specialized expert based on the routing preference.

## The Shared and Routed Forward Pass

In production architectures, fine-grained segmentation is achieved by reducing the intermediate dimension $d_{ff}$ of each expert while proportionally increasing the number of active experts $k$. This structural division guarantees that the total active parameter count remains strictly identical to the coarse configuration, even as the combinatorial pathways explode. To demonstrate the mechanics of shared expert isolation without expanding the toy matrices to unreadable dimensions, the established configuration is partitioned to feature 1 shared expert, where $K_s = 1$, and 4 routed experts, where $E_r = 4$. The router continues to select the top 2 routed experts per token, setting $K_r = 2$, and the intermediate dimension remains $d_{ff} = 4$. The shared expert, the four routed experts, and the gating network are initialized with new, independent weight matrices.

### Step 1: Router Projection and Gating Weights

**Goal:** Determine which specialized experts process each token and assign a proportional scaling weight to the chosen paths.<br>
**Equation:** $g(x) = \text{Softmax}(\text{TopK}(xW_g))$

The sequence begins with the standard $4 \times 6$ input matrix $x$ containing the 4 embedded tokens established in the [Transformer series](series-transformers.html). All matrices are formatted to 4 decimal places for precision:

$$
x = \begin{bmatrix}
 0.0200 &  1.2900 &  0.1800 &  1.3500 &  0.0000 &  0.6700 \\
 0.7400 &  1.7600 &  0.4500 &  1.5200 &  0.2000 &  1.2300 \\
 0.8800 & -0.3100 &  1.7800 &  0.9900 &  0.0900 &  0.9100 \\
 0.1900 & -1.0300 &  1.5600 &  1.2100 &  0.5800 &  0.6900
\end{bmatrix}
$$

The router projects these tokens using the newly initialized $6 \times 4$ gating matrix $W_g$ via the operation $h(x) = xW_g$ to compute the raw affinity logits:

$$
W_g = \begin{bmatrix}
 0.1349 &  0.0401 &  0.1369 &  0.0385 \\
 0.1685 & -0.1110 &  0.0326 & -0.0836 \\
 0.2490 &  0.0928 &  0.0533 &  0.0767 \\
 0.1213 &  0.0708 & -0.0119 &  0.0210 \\
 0.0521 &  0.0813 &  0.0966 & -0.0267 \\
 0.0515 &  0.0309 &  0.0373 & -0.1251
\end{bmatrix}
$$

$$
h(x) = \begin{bmatrix}
 0.4633 & -0.0094 &  0.0633 & -0.1488 \\
 0.7668 &  0.0380 &  0.2298 & -0.2114 \\
 0.6814 &  0.3406 &  0.2360 &  0.1009 \\
 0.4531 &  0.4211 &  0.1428 &  0.1367
\end{bmatrix}
$$

To isolate the top paths, the Top-2 mask preserves the two highest values per row, pushing the remainder to negative infinity:

$$
h(x)_{masked} = \begin{bmatrix}
 0.4633 & -\infty &  0.0633 & -\infty \\
 0.7668 & -\infty &  0.2298 & -\infty \\
 0.6814 &  0.3406 & -\infty & -\infty \\
 0.4531 &  0.4211 & -\infty & -\infty
\end{bmatrix}
$$

Applying the softmax function normalizes these surviving logits into the gating weights, $g(x) = \text{Softmax}(h(x)_{masked})$. For the first token, the surviving logits for Expert 0 and Expert 2 are exponentiated and divided by their sum:

$$
g_{0} = \frac{e^{0.4633}}{e^{0.4633} + e^{0.0633}} = \frac{1.5893}{1.5893 + 1.0653} = 0.5987
$$

$$
g_{2} = \frac{e^{0.0633}}{e^{0.4633} + e^{0.0633}} = \frac{1.0653}{1.5893 + 1.0653} = 0.4013
$$

Repeating this calculation across all four rows yields the final dynamic gating weights. The shared expert bypasses the router entirely, receiving no gating weight and remaining completely excluded from this matrix:

$$
g(x)_{routed} = \begin{bmatrix}
 0.5987 &  0.0000 &  0.4013 &  0.0000 \\
 0.6311 &  0.0000 &  0.3689 &  0.0000 \\
 0.5844 &  0.4156 &  0.0000 &  0.0000 \\
 0.5080 &  0.4920 &  0.0000 &  0.0000
\end{bmatrix}
$$

### Step 2: The Shared Expert Projection

**Goal:** Compute a universal foundational knowledge update applied unconditionally to every token in the sequence.<br>
**Equation:** $\text{FFN}^{shared}(x) = \text{ReLU}(xW_1^{shared})W_2^{shared}$

The shared expert processes all four tokens unconditionally. The input matrix $x$ is first multiplied by the shared expansion matrix $W_1^{shared}$ to produce the pre-activation intermediate state:

$$
W_1^{shared} = \begin{bmatrix}
 0.1900 &  0.0209 &  0.0895 & -0.1181 \\
 0.0274 &  0.0603 & -0.0661 & -0.1044 \\
-0.0581 & -0.0356 &  0.0294 & -0.1797 \\
-0.0389 &  0.0449 & -0.0474 &  0.1164 \\
-0.1230 &  0.0987 & -0.0816 & -0.1758 \\
 0.0696 & -0.0021 &  0.0502 &  0.2658
\end{bmatrix}
$$

$$
x W_1^{shared} = \begin{bmatrix}
 0.0227 &  0.1310 & -0.1086 &  0.1659 \\
 0.1644 &  0.1909 & -0.0636 &  0.1168 \\
 0.0690 & -0.0123 &  0.1430 & -0.0501 \\
-0.1532 & -0.0036 &  0.0610 &  0.0270
\end{bmatrix}
$$

Applying the ReLU activation function zeroes out all negative values, yielding the shared hidden state:

$$
h(x)^{shared} = \text{ReLU}(x W_1^{shared}) = \begin{bmatrix}
 0.0227 &  0.1310 &  0.0000 &  0.1659 \\
 0.1644 &  0.1909 &  0.0000 &  0.1168 \\
 0.0690 &  0.0000 &  0.1430 &  0.0000 \\
 0.0000 &  0.0000 &  0.0610 &  0.0270
\end{bmatrix}
$$

Contracting this hidden state with $W_2^{shared}$ produces the universal contextual update applied unconditionally to the entire sequence:

$$
W_2^{shared} = \begin{bmatrix}
 0.1086 & -0.0163 &  0.0553 &  0.2289 & -0.0042 & -0.0750 \\
 0.0174 & -0.1575 &  0.0263 & -0.0501 & -0.1176 &  0.0356 \\
-0.0988 &  0.0885 & -0.0187 &  0.0981 &  0.0876 &  0.1117 \\
 0.0134 &  0.0494 &  0.0907 &  0.1858 & -0.0702 &  0.0442
\end{bmatrix}
$$

$$
\text{FFN}^{shared}(x) = h(x)^{shared} W_2^{shared} = \begin{bmatrix}
 0.0070 & -0.0128 &  0.0198 &  0.0295 & -0.0271 &  0.0103 \\
 0.0228 & -0.0270 &  0.0247 &  0.0498 & -0.0313 & -0.0004 \\
-0.0066 &  0.0115 &  0.0011 &  0.0298 &  0.0122 &  0.0108 \\
-0.0057 &  0.0067 &  0.0013 &  0.0110 &  0.0034 &  0.0080
\end{bmatrix}
$$

### Step 3: The Routed Expert Projections

**Goal:** Calculate the specialized knowledge updates from the dynamically selected experts and scale them by the router weights.<br>
**Equation:** $\sum_{i \in \mathcal{K}} g_i \cdot \text{ReLU}(x W_{1}^i) W_{2}^i$

The routed experts execute precisely as established in Chapter 3. For the first token $x_1$, representing the top row of the input matrix:

$$
x_1 = \begin{bmatrix} 0.0200 &  1.2900 &  0.1800 &  1.3500 &  0.0000 &  0.6700 \end{bmatrix}
$$

The gating weights selected Expert 0 with a weight of $0.5987$ and Expert 2 with a weight of $0.4013$. The input vector $x_1$ processes through both selected experts independently, beginning with Expert 0:

$$
W_{1}^0 = \begin{bmatrix}
-0.0858 &  0.1568 &  0.0854 &  0.0191 \\
 0.0918 & -0.0121 &  0.1162 &  0.0184 \\
-0.1392 & -0.0155 &  0.0807 & -0.1635 \\
 0.0704 & -0.0682 &  0.0967 & -0.0827 \\
-0.0214 &  0.0187 & -0.1148 & -0.0308 \\
 0.0752 &  0.1173 &  0.0543 &  0.1065
\end{bmatrix}
$$

$$
x_1 W_{1}^0 = \begin{bmatrix} 0.2371 & -0.0288 &  0.3331 & -0.0455 \end{bmatrix}
$$

$$
\text{ReLU}(x_1 W_{1}^0) = \begin{bmatrix} 0.2371 &  0.0000 &  0.3331 &  0.0000 \end{bmatrix}
$$

$$
W_{2}^0 = \begin{bmatrix}
-0.1096 &  0.1749 &  0.0480 &  0.2847 &  0.1152 & -0.0293 \\
 0.0495 &  0.0632 &  0.1409 & -0.0550 &  0.0751 &  0.0101 \\
 0.0140 & -0.1351 &  0.1549 &  0.0681 &  0.1143 &  0.0490 \\
-0.1525 & -0.0256 & -0.1034 & -0.0042 &  0.0229 &  0.0153
\end{bmatrix}
$$

$$
\text{FFN}_0^{routed}(x_1) = \text{ReLU}(x_1 W_{1}^0) W_{2}^0 = \begin{bmatrix} -0.0213 & -0.0035 &  0.0630 &  0.0902 &  0.0654 &  0.0094 \end{bmatrix}
$$

Simultaneously, the exact same sequence occurs through the isolated weights of Expert 2:

$$
W_{1}^2 = \begin{bmatrix}
 0.0032 &  0.0383 & -0.0037 & -0.0823 \\
 0.1951 &  0.1210 & -0.1178 &  0.1946 \\
 0.1508 &  0.1624 &  0.0205 &  0.0223 \\
-0.0420 &  0.0245 & -0.0983 &  0.3138 \\
-0.0995 &  0.0733 & -0.2226 & -0.1422 \\
-0.0029 &  0.0092 & -0.0723 &  0.0773
\end{bmatrix}
$$

$$
x_1 W_{1}^2 = \begin{bmatrix} 0.2203 &  0.2254 & -0.3296 &  0.7288 \end{bmatrix}
$$

$$
\text{ReLU}(x_1 W_{1}^2) = \begin{bmatrix} 0.2203 &  0.2254 &  0.0000 &  0.7288 \end{bmatrix}
$$

$$
W_{2}^2 = \begin{bmatrix}
-0.1325 &  0.0881 &  0.0487 & -0.1447 &  0.0746 &  0.0377 \\
-0.0167 &  0.0899 &  0.0047 & -0.0092 &  0.0864 & -0.0298 \\
-0.0321 &  0.0243 & -0.1140 &  0.0633 & -0.0287 &  0.1643 \\
 0.0522 &  0.0875 &  0.0189 &  0.0342 &  0.1409 & -0.2146
\end{bmatrix}
$$

$$
\text{FFN}_2^{routed}(x_1) = \text{ReLU}(x_1 W_{1}^2) W_{2}^2 = \begin{bmatrix}  0.0051 &  0.1034 &  0.0256 & -0.0090 &  0.1386 & -0.1548 \end{bmatrix}
$$

With both experts having processed the token, their final outputs are scalar-multiplied by their assigned gating weights:

$$
0.5987 \cdot \text{FFN}_0^{routed}(x_1) = \begin{bmatrix} -0.0128 & -0.0021 &  0.0377 &  0.0540 &  0.0392 &  0.0056 \end{bmatrix}
$$

$$
0.4013 \cdot \text{FFN}_2^{routed}(x_1) = \begin{bmatrix} 0.0020 &  0.0415 &  0.0103 & -0.0036 &  0.0556 & -0.0621 \end{bmatrix}
$$

Summing these two scaled vectors forms the combined routed output for the first token. This entire mathematical pipeline is evaluated automatically for the remaining three tokens:

$$
\sum_{i \in \mathcal{K}} g_i \cdot \text{FFN}_i^{routed}(x) = \begin{bmatrix}
-0.0107 &  0.0394 &  0.0480 &  0.0504 &  0.0948 & -0.0565 \\
-0.0096 &  0.0386 &  0.0795 &  0.0500 &  0.1232 & -0.0539 \\
 0.0012 & -0.0315 &  0.0275 & -0.0137 &  0.0422 &  0.0260 \\
-0.0083 & -0.0267 & -0.0126 & -0.0322 &  0.0309 &  0.0292
\end{bmatrix}
$$

### Step 4: Merging the Forward Pass

**Goal:** Merge the original token representations with the new universal and specialized knowledge updates to prevent representation collapse.<br>
**Equation:** $y = x + \text{FFN}^{shared}(x) + \sum_{i \in \mathcal{K}} g_i \cdot \text{FFN}_i^{routed}(x)$

The MoE layer concludes by summing the original input vector $x$, the universal shared output, and the specialized routed output. This addition operation merges the foundational linguistic structures with the bespoke, combinatorially selected knowledge fragments. Expanding the specific addition for the first token demonstrates the final residual merge:

$$
y_1 = x_1 + \text{FFN}^{shared}(x_1) + \text{Routed}(x_1)
$$

$$
\begin{aligned}
y_1 &= \begin{bmatrix} 0.0200 &  1.2900 &  0.1800 &  1.3500 &  0.0000 &  0.6700 \end{bmatrix} \\
&+ \begin{bmatrix} 0.0070 & -0.0128 &  0.0198 &  0.0295 & -0.0271 &  0.0103 \end{bmatrix} \\
&+ \begin{bmatrix} -0.0107 &  0.0394 &  0.0480 &  0.0504 &  0.0948 & -0.0565 \end{bmatrix}
\end{aligned}
$$

$$
y_{final} = \begin{bmatrix}
 0.0163 &  1.3166 &  0.2478 &  1.4299 &  0.0677 &  0.6238 \\
 0.7531 &  1.7717 &  0.5542 &  1.6198 &  0.2918 &  1.1757 \\
 0.8745 & -0.3299 &  1.8086 &  1.0061 &  0.1445 &  0.9468 \\
 0.1761 & -1.0499 &  1.5487 &  1.1888 &  0.6144 &  0.7272
\end{bmatrix}
$$

The shared and routed components are now successfully merged back into the central residual stream, producing a mathematically complete forward pass that maximizes parameter expressivity. The shared expert bypasses the router, meaning load balancing applies exclusively to the routed experts. However, to train this highly fragmented architecture effectively, the standard auxiliary loss must be abandoned entirely. When attempting to balance hundreds of fine-grained routed experts, the traditional auxiliary loss severely distorts the routing gradients. The optimizer is forced to route tokens sub-optimally simply to satisfy the aggressive load balancing penalty, actively degrading the primary language modeling performance. DeepSeek-V3 resolves this conflict in favor of auxiliary-loss-free dynamic bias updates that operate entirely outside the bounds of backpropagation, a mechanism examined next.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
