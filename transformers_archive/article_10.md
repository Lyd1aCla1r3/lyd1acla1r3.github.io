# Part 10: The Residual Stream and MLP Expansion

<!-- SUMMARY: The residual stream acts as a central memory bus, allowing isolated attention and feed-forward blocks to read and write context while flawlessly preserving gradient flow. Following stabilization, the feed-forward network functions as a high-dimensional key-value memory retrieval mechanism, projecting token vectors into a substantially larger geometric space to compute dot products against learned key patterns and measure alignment with higher-order conceptual features. -->

The projection matrix completes the multi-head attention mechanism by mixing the independent insights of the various heads back into the model core dimensionality. A naive architectural approach would feed this output directly into the next sequential block. The Transformer architecture abandons this sequential pipeline in favor of a central shared memory backbone known as the residual stream.

Every token representation begins its journey in the residual stream as a positionally encoded embedding. Subsequent components like attention blocks and feed-forward networks do not act as sequential filters. These blocks instead read the current state of the stream, compute specific contextual transformations, and add their results back into the stream. The residual stream functions as an information highway accumulating context step by step.

The mathematical operation executing this concept is a simple element-wise addition. The original positionally encoded input matrix directly adds to the output matrix produced by the attention block.

$$
\text{Input Stream} = \begin{bmatrix}
 0.10 &  1.00 &  0.00 &  1.00 &  0.00 &  1.00 \\
 0.84 &  1.34 &  0.35 &  1.09 &  0.21 &  1.48 \\
 0.91 & -0.62 &  1.70 &  0.70 &  0.02 &  1.01 \\
 0.14 & -1.09 &  1.38 &  1.08 &  0.40 &  0.80
\end{bmatrix}
$$

$$
\text{Attention Update} = \begin{bmatrix}
-0.08 &  0.29 &  0.18 &  0.35 &  0.00 & -0.33 \\
-0.10 &  0.42 &  0.10 &  0.43 & -0.01 & -0.25 \\
-0.03 &  0.31 &  0.08 &  0.29 &  0.07 & -0.10 \\
 0.05 &  0.06 &  0.18 &  0.13 &  0.18 & -0.11
\end{bmatrix}
$$

$$
\text{Updated Stream} = \begin{bmatrix}
 0.02 &  1.29 &  0.18 &  1.35 &  0.00 &  0.67 \\
 0.74 &  1.76 &  0.45 &  1.52 &  0.20 &  1.23 \\
 0.88 & -0.31 &  1.78 &  0.99 &  0.09 &  0.91 \\
 0.19 & -1.03 &  1.56 &  1.21 &  0.58 &  0.69
\end{bmatrix}
$$

This addition preserves the original information while layering the new semantic context discovered by the attention heads on top. Beyond managing forward information flow, the residual stream solves a critical mathematical failure point during the backpropagation phase.

Deep neural networks learn by calculating the gradient of the loss function and propagating that error signal backward through the layers. In a strictly sequential architecture, the gradient multiplies by the derivative of each layer. A sub-layer operation frequently yields a derivative matrix containing small values. An idealized sub-layer Jacobian matrix containing values of 0.1 perfectly illustrates the danger.

$$
\text{Jacobian} = \begin{bmatrix}
 0.10 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.10 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.10 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.10 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.10 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.10
\end{bmatrix}
$$

Backpropagating an error signal through four consecutive layers of this type requires multiplying the Jacobian matrix by itself four times. This exponentiation causes the gradient to decay exponentially. The resulting matrix demonstrates complete signal loss, rendering the earliest layers entirely incapable of learning.

$$
\text{Sequential Gradient Multiplier} = \begin{bmatrix}
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00
\end{bmatrix}
$$

The residual addition elegantly neutralizes this vanishing gradient problem. The mathematical derivative of an addition operation distributes the gradient equally to both inputs. When calculating the derivative of the residual equation with respect to the input stream, the original input receives a strict derivative of one. This transforms the gradient multiplier for a single layer from the Jacobian matrix alone into the Jacobian matrix added to the Identity matrix.

$$
\text{Residual Multiplier} = I + \text{Jacobian}
$$

Backpropagating through four layers utilizing residual connections multiplies this updated term by itself four times. The addition of the Identity matrix ensures the gradient mathematically survives the journey backward.

$$
\text{Residual Gradient Multiplier} = \begin{bmatrix}
 1.46 &  0.00 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  1.46 &  0.00 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  1.46 &  0.00 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  1.46 &  0.00 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  1.46 &  0.00 \\
 0.00 &  0.00 &  0.00 &  0.00 &  0.00 &  1.46
\end{bmatrix}
$$

The error signal reaches the initial embedding matrices effectively intact. The residual stream functions exactly as a gradient highway. Information flows forward to build deep semantic context, and error signals flow backward unimpeded to meticulously adjust the foundational weights. With the updated residual representations successfully computed, the architecture immediately subjects the vectors to layer normalization to stabilize their geometry.

## The MLP as a Key-Value Memory Bank

The model has successfully normalized the residual stream. The vectors are now stable, centered, and scaled, ready for the next major transformation. Up until this point, the self-attention mechanism has allowed tokens to move information *between* one another. The representation for "up" has reached out and pulled in context from "woke". Attention, however, merely routes information. It does not possess the capacity to interpret that combined information into a new, higher-level concept.

To process the newly contextualized vector, the architecture passes it into the Feed-Forward Network, often referred to as the Multi-Layer Perceptron or MLP.

Historically, the MLP has been described simply as a function that "expands dimensions" and introduces non-linearity. Mechanistic interpretability offers a far more precise and compelling geometric framing. One can view the MLP as a massive Key-Value memory bank stored directly within the weights of the network. The following section will focus entirely on the first linear layer of the MLP, which acts as the "Keys" in this memory retrieval system.

## The Geometry of the Keys

The model dimensionality is $d_{model} = 6$. The standard architecture of a Transformer dictates that the hidden layer of the MLP is significantly wider than the residual stream, typically expanding the dimensionality by a factor of four. Therefore, the feed-forward dimension is $d_{ff} = 24$.

The first projection matrix, $W_1$, has a shape of $6 \times 24$. The calculation multiplies the normalized residual stream $X_{norm}$ with a shape of $4 \times 6$ by $W_1$, resulting in a projected matrix of shape $4 \times 24$.

Rather than viewing $W_1$ as a monolithic mathematical operation, consider its internal structure. $W_1$ consists of 24 distinct column vectors, each existing in the 6-dimensional space. Each of these 24 columns represents a specific "Key."

A Key is a learned spatial pattern. When computing the dot product of a token's vector with one of these column vectors, the operation is measuring geometric similarity. It is asking the model a very specific question. Does the contextualized token contain the features described by this Key?

Consider defining the first column of the learned $W_1$ matrix as the key $k_1$:

$$
k_1 = \begin{bmatrix}
-0.07 \\
 0.44 \\
-0.31 \\
 0.31 \\
 0.61 \\
 0.05
\end{bmatrix}
$$

Next, the system extracts the normalized vector for the third token, "woke", from the $X_{norm}$ matrix calculated in the previous step:

$$
x_{woke} = \begin{bmatrix}
-0.17 & -2.12 & 1.29 & 0.01 & -1.45 & -0.12
\end{bmatrix}
$$

To determine how strongly the "woke" token aligns with the pattern defined by $k_1$, the process computes their dot product:

$$
x_{woke} \cdot k_1 = (-0.17 \times -0.07) + (-2.12 \times 0.44) + (1.29 \times -0.31) + (0.01 \times 0.31) + (-1.45 \times 0.61) + (-0.12 \times 0.05)
$$

$$
x_{woke} \cdot k_1 = 0.01 - 0.93 - 0.40 + 0.00 - 0.88 - 0.01 = -2.21
$$

A negative dot product indicates that the vector for "woke" points in the opposite direction of the key $k_1$. This specific token does not contain the conceptual features that $k_1$ is looking for.

By performing this multiplication across the entire matrix, the system simultaneously checks every token against all 24 Keys.

## The Projection Calculation

The complete matrix multiplication $X_{norm} W_1 = X_{proj}$ follows. To keep the display manageable while rigorously showing the math, the following matrix presents the full result of checking the 4 sequence tokens against all 24 Keys.

$$
X_{proj} = \begin{bmatrix}
 0.64 & -0.30 & -0.93 & -0.86 &  0.53 & -1.24 &  0.88 &  0.71 & -2.13 & \dots & -0.19 \\
 1.07 & -1.32 & -0.65 & -0.96 &  1.47 & -2.19 &  2.16 & -0.20 & -2.64 & \dots &  1.73 \\
-2.21 & -0.10 & -2.12 &  0.33 & -2.18 &  2.73 & -0.92 &  1.72 &  3.32 & \dots &  1.09 \\
-0.62 & -0.74 & -0.58 & -0.56 &  0.00 &  2.26 & -0.71 &  0.74 &  2.40 & \dots &  1.53
\end{bmatrix}
$$

Each row in $X_{proj}$ represents a token. Each column corresponds to one of the 24 Keys. Notice the value at Row 3, Column 1. It is $-2.21$, exactly as calculated manually for the "woke" token interacting with $k_1$.

Conversely, observe Row 3, Column 9. The value is a highly positive $3.32$. This indicates that the "woke" token strongly activated the 9th Key in the network. The pattern has been successfully recognized.

## The Bias Vector

In a standard linear layer, a learned bias vector $b_1$ is applied immediately after the matrix multiplication. The bias vector shifts the results, acting as a baseline activation threshold for each of the 24 Keys.

$$
X_{proj\_biased} = X_{proj} + b_1
$$

If a particular Key requires a very strict match to activate, the network can learn a highly negative bias for that position, forcing the dot product to be exceedingly large to overcome the penalty. If a Key should trigger easily, the network learns a positive bias.

For this model, the architecture applies a randomly initialized $b_1$ vector of length 24 to every row in $X_{proj}$, yielding the final pre-activation state:

$$
X_{proj\_biased} = \begin{bmatrix}
 0.58 & -0.26 & -1.09 & -0.90 &  0.56 & -1.16 &  1.03 &  0.71 & -2.25 & \dots & -0.04 \\
 1.01 & -1.28 & -0.81 & -1.00 &  1.50 & -2.11 &  2.30 & -0.21 & -2.75 & \dots &  1.88 \\
-2.27 & -0.07 & -2.28 &  0.29 & -2.16 &  2.81 & -0.78 &  1.72 &  3.20 & \dots &  1.24 \\
-0.69 & -0.71 & -0.74 & -0.60 &  0.03 &  2.34 & -0.56 &  0.74 &  2.29 & \dots &  1.68
\end{bmatrix}
$$

The vectors have successfully probed the memory bank. The calculation has measured exactly how well each token aligns with the 24 internal Key patterns. The next step is determining which of these patterns actually "fires," dropping irrelevant matches to zero before writing new conceptual information back into the residual stream. This thresholding introduces non-linearity, bringing the network to the Activation Function.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
