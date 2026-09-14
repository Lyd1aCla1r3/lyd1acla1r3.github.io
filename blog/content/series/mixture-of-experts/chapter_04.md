# Part 4: Expert Collapse
<!-- SUMMARY: The gating network's reliance on backpropagation introduces a severe positive feedback loop that systematically starves under-utilized pathways. Without intervention, this dynamic degenerates the sparse architecture into a heavily imbalanced network, severely wasting parameter capacity. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The completed forward pass processes tokens through independent network branches and recombines them into a unified residual stream. This dynamic routing mechanism introduces a catastrophic failure mode during training.

## The Positive Feedback Loop

At initialization, the gating weights in the router matrix are random noise. In theory, this random state distributes tokens evenly across all experts. In practice, perfect balance never occurs. Even under a perfectly random distribution, standard variance guarantees that some experts will receive slightly more tokens than others. Natural language makes the problem worse: it is heavily clustered rather than uniformly distributed. If an expert's random initialization happens to align with a frequent token cluster, such as common punctuation, it receives an immediate, disproportionate share of assignments.

This microscopic initial imbalance creates a severe positive feedback loop. An expert that randomly processes a slightly larger share of tokens during the first training step participates in more forward passes, thereby receiving a higher volume of gradient updates. As the optimization algorithm minimizes the prediction error, backpropagation adjusts the shared router matrix to assign even higher routing probabilities to this active expert.

The mechanism driving this collapse is rooted in the chain rule of calculus. The router computes an affinity score by taking the dot product between the input token vector and an expert's column in the router matrix. The token vector possesses $d_{model}$ dimensions, and the router matrix possesses dimensions of $d_{model} \times E$. Consequently, each expert's column acts as a vector perfectly dimensioned to share the exact same geometric space as the tokens. This forward operation is a purely linear matrix multiplication containing no activation functions. The local derivative of this operation therefore evaluates strictly to the input token vector itself. The chain rule dictates that the final gradient applied to the router matrix is the upstream loss derivative multiplied by this local derivative. Consequently, the gradient update mathematically adds a scaled copy of the processed token vector directly into the active expert's column. In linear algebra, adding one vector to another inherently rotates the receiving vector to point more in the direction of the added vector. This geometric update alters the active expert's column in two permanent ways: it aligns the column's direction with the token, and it increases the column's overall numerical magnitude.

When a completely unrelated token from a new training batch passes through the layer, the router computes new dot products against all available experts independently. An expert that was never selected during initialization remains completely frozen. Its column in the router matrix consists entirely of tiny, randomly initialized noise, yielding a correspondingly small dot product. The active expert, having accumulated multiple gradient updates, possesses a numerically larger column vector. The dot product between the new token and this enlarged column produces a mathematically higher score strictly because the underlying vector magnitude is greater. While a single gradient update is small, this magnitude advantage initiates a compounding statistical effect. By possessing a marginally larger vector, the active expert is mathematically guaranteed to capture a slightly higher percentage of tokens in the next training batch. This increased token volume delivers a correspondingly larger sum of gradient updates during the subsequent backward pass, accelerating the vector's growth. This compounding imbalance guarantees that the active expert will absorb an increasingly wider variety of tokens over thousands of iterations, ultimately driving the complete starvation of the frozen pathways.

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

Averaging these probabilities across the four tokens establishes the network's initial routing distribution across the batch. As expected from a randomly initialized matrix, the distribution begins in a nearly balanced state.

$$
\text{Routing Distribution (Step 0)} = \begin{bmatrix} 0.3072 & 0.2256 & 0.2332 & 0.2340 \end{bmatrix}
$$

The top-k masking operation applied to these same logits in Chapter 2 forced all four tokens to the first expert, distributed two tokens each to the second and third experts, and assigned zero tokens to the fourth expert. The subsequent training steps are executed algorithmically via a numerical simulation script. The simulation calculates gradient updates identically to the dense baseline architecture detailed in the [Transformer series](series-transformers.html), updating the active experts proportionally to the tokens they process. The fourth expert, having processed zero tokens, receives zero updates and remains completely frozen at its initialized state.

As the simulation progresses, the probability mass shifts violently toward the heavily utilized first expert.

$$
\text{Routing Distribution (Step 1)} = \begin{bmatrix} 0.5141 & 0.1964 & 0.2026 & 0.0869 \end{bmatrix}
$$

$$
\text{Routing Distribution (Step 2)} = \begin{bmatrix} 0.7751 & 0.1075 & 0.1098 & 0.0076 \end{bmatrix}
$$

By the third step, the first expert absorbs over ninety percent of the total probability mass. The unfavored experts rapidly lose relevance as the positive feedback loop accelerates.

$$
\text{Routing Distribution (Step 3)} = \begin{bmatrix} 0.9173 & 0.0409 & 0.0416 & 0.0002 \end{bmatrix}
$$

$$
\text{Routing Distribution (Step 4)} = \begin{bmatrix} 0.9755 & 0.0123 & 0.0122 & 0.0000 \end{bmatrix}
$$

The routing distribution achieves total collapse at the fifth step. The first expert completely dominates the layer, while the remaining probability mass approaches mathematical zero.

$$
\text{Routing Distribution (Step 5)} = \begin{bmatrix} 0.9944 & 0.0029 & 0.0027 & 0.0000 \end{bmatrix}
$$

The consequence is a massive waste of parameters. The entire point of sparse routing is to decouple total parameter count from computational cost. When the router collapses to a single expert, the architecture degenerates into a constrained dense model. The system dedicates enormous memory to storing the inactive experts while processing every token through a single narrow pathway. The effective capacity of the network is divided by the number of experts, rendering the architectural expansion useless.

Preventing this collapse requires direct intervention. An auxiliary loss function that penalizes unbalanced routing and forces the network to use all available experts is detailed in the next chapter.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
