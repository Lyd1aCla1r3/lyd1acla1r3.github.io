# Part 5: Load Balancing: The Auxiliary Loss

<!-- SUMMARY: The progressive concentration of routing probability into a single expert necessitates an explicit penalty term in the training objective. The auxiliary loss formulation combines a non-differentiable count of hard routing assignments with a differentiable softmax probability mean, producing a gradient signal that penalizes overloaded experts while promoting utilization of starved pathways. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>

The previous chapter demonstrated that standard gradient descent concentrates routing probability into a single dominant expert. Under an aggressive learning rate, the routing distribution collapsed from $[0.25, 0.25, 0.25, 0.25]$ to $[0.9944, 0.0029, 0.0027, 0.0000]$ in just five steps. Production models under standard hyperparameters decay more gradually, but the underlying dynamic is the same. Reversing this collapse requires a secondary loss term, the auxiliary loss, that generates targeted gradients pulling probability away from overloaded experts and toward starved ones.

## The Problem: Gradient Descent Cannot See Imbalance

Standard training optimizes a single objective: the language modeling loss $\mathcal{L}_{LM}$, which measures the quality of the model's predictions. Gradient descent reduces this loss by adjusting all weights in the direction that improves prediction accuracy. The difficulty arises from the discrete Top-K selection at the core of the router.

When the router selects the top $k=2$ experts for a token, only those two experts execute their forward pass and produce outputs. During backpropagation, gradients flow backward through the operations that actually computed values. The unselected experts performed no computation, produced no output, and therefore receive no gradient update from $\mathcal{L}_{LM}$. The primary training loss is structurally blind to the existence of idle experts. An expert that receives zero tokens generates zero error signal, meaning gradient descent has no mathematical mechanism to redirect tokens toward it. This asymmetry is the root cause of expert collapse: the winners accumulate updates while the losers stagnate, widening the gap at every step.

Solving this problem requires a second loss term, one that directly measures routing imbalance and generates gradient updates for all experts, including those receiving zero tokens. This second term is the auxiliary loss $\mathcal{L}_{aux}$.

## Measuring Imbalance: The Hard Routing Fraction

The first ingredient of the auxiliary loss is a concrete measurement of how unevenly tokens are distributed across experts. The router logit matrix $H$, computed in Part 2 by projecting each token through the gating weight matrix $W_g$, produced the following values:

$$
H_{4 \times 4} = \begin{bmatrix}
0.0932 & -0.2941 & -0.0317 & -0.0777 \\
0.1712 & -0.3393 & 0.0330 & -0.0621 \\
0.1156 & -0.1155 & -0.2472 & -0.1707 \\
0.0320 & -0.1227 & -0.4794 & -0.3710
\end{bmatrix}
$$

Applying the Top-2 selection to these logits generates a boolean mask where the highest two values in each row become $1$ and the remaining values become $0$. This mask makes the final expert assignments visually explicit:

$$
\text{Mask}_{4 \times 4} = \begin{bmatrix}
1 & 0 & 1 & 0 \\
1 & 0 & 1 & 0 \\
1 & 1 & 0 & 0 \\
1 & 1 & 0 & 0
\end{bmatrix}
$$

Token 1 and Token 2 routed to Expert 0 and Expert 2. Token 3 and Token 4 routed to Expert 0 and Expert 1. Summing the ones in each column and dividing by the total number of tokens $N = 4$ yields the hard routing fraction $f_i$ for each expert.

The formal notation for this count uses the indicator function, denoted by the symbol $\mathbb{1}$. This operator evaluates the condition inside its brackets and returns exactly $1$ if the condition is true, or exactly $0$ if the condition is false. The summation iterates over every token $x$ in the training batch $\mathcal{B}$, adding $1$ each time Expert $i$ appears in that token's Top-K set:

$$
f_i = \frac{1}{N} \sum_{x \in \mathcal{B}} \mathbb{1}[\text{Expert } i \in \text{TopK}(h(x), k)]
$$

Evaluating this count for each of the four experts produces the individual hard fractions:

$$
\begin{aligned}
f_0 &= 4 / 4 = 1.0 \\
f_1 &= 2 / 4 = 0.5 \\
f_2 &= 2 / 4 = 0.5 \\
f_3 &= 0 / 4 = 0.0
\end{aligned}
$$

These values form the hard routing fraction vector:

$$
f = \begin{bmatrix}
1.0 & 0.5 & 0.5 & 0.0
\end{bmatrix}
$$

This vector precisely quantifies the imbalance: Expert 0 is heavily overloaded, Expert 3 is completely starved, and Experts 1 and 2 sit at moderate utilization. The hard fraction provides a perfect forward-pass diagnostic of load distribution.

## Why the Hard Fraction Cannot Drive Gradient Updates

The hard fraction $f_i$ measures imbalance accurately, yet it cannot be used directly as a loss term for backpropagation. The reason is rooted in the mechanics of the indicator function.

The Top-K selection operates on a dynamic threshold $\tau$, defined as the value of the $k$-th largest logit for a given token. This threshold cannot be determined in advance; the router must first compute all $E$ logits, sort them, and identify the boundary value separating the top $k$ winners from the remaining $E - k$ losers. The indicator function then maps each logit to a binary output based on whether it clears this threshold:

$$
\mathbb{1}[h(x)_i \geq \tau] = \begin{cases} 
1 & \text{if } h(x)_i \geq \tau \\
0 & \text{if } h(x)_i < \tau 
\end{cases}
$$

This mapping is a step-function. Below the threshold, the output is a flat $0$. Above the threshold, the output is a flat $1$. Between these two flat regions, the output jumps instantaneously from $0$ to $1$ with no smooth transition. Taking the derivative of this step-function with respect to the input logit formalizes the problem:

$$
\frac{\partial}{\partial h(x)_i} \mathbb{1}[h(x)_i \geq \tau] = \begin{cases} 
0 & \text{if } h(x)_i \neq \tau \\
\text{undefined} & \text{if } h(x)_i = \tau 
\end{cases}
$$

In the flat regions on either side of $\tau$, the derivative evaluates to exactly zero: an infinitesimal change to the logit produces absolutely no change in the binary output. At the exact threshold, the instantaneous jump renders the derivative mathematically undefined. While modern optimization frameworks can bypass isolated undefined points using subgradients, a technique regularly applied to the kink in a ReLU activation, they cannot extract learning signals from entirely flat landscapes. Since $f_i$ is constructed by summing these indicator outputs, its derivative inherits this flat topography. The gradient evaluates to exactly zero almost everywhere, reducing the weight update calculation to a multiplication by zero. The parameters remain permanently frozen, completely severing the computational graph at the Top-K boundary.

## The Differentiable Counterpart: Soft Probability Mean

The auxiliary loss needs a quantity that captures the same routing preference information as $f_i$ but remains fully differentiable. The softmax function applied to the unmasked router logits $H$ provides exactly this. Before the discrete Top-K masking occurs, the softmax converts every logit into a continuous probability, creating a smooth landscape where infinitesimal changes to logits produce proportional changes in output. Applying the softmax to the full, unmasked logit matrix $H$ produces the dense probability matrix $P$:

$$
P_{4 \times 4} = \begin{bmatrix}
0.2937 & 0.1994 & 0.2593 & 0.2476 \\
0.3065 & 0.1839 & 0.2669 & 0.2427 \\
0.3086 & 0.2449 & 0.2147 & 0.2318 \\
0.3200 & 0.2742 & 0.1919 & 0.2139
\end{bmatrix}
$$

Each row sums to $1.0$ and represents the full probability distribution over all four experts for a single token, before any masking. The soft probability mean $P_i$ averages the probability assigned to Expert $i$ across every token in the batch:

$$
P_i = \frac{1}{N} \sum_{x \in \mathcal{B}} \frac{e^{h(x)_i}}{\sum_{j=1}^{E} e^{h(x)_j}}
$$

This is equivalent to taking the column-wise mean of the $P$ matrix:

$$
\begin{aligned}
P_0 &= (0.2937 + 0.3065 + 0.3086 + 0.3200) / 4 = 0.3072 \\
P_1 &= (0.1994 + 0.1839 + 0.2449 + 0.2742) / 4 = 0.2256 \\
P_2 &= (0.2593 + 0.2669 + 0.2147 + 0.1919) / 4 = 0.2332 \\
P_3 &= (0.2476 + 0.2427 + 0.2318 + 0.2139) / 4 = 0.2340
\end{aligned}
$$

$$
P_{\text{mean}} = \begin{bmatrix}
0.3072 & 0.2256 & 0.2332 & 0.2340
\end{bmatrix}
$$

The critical distinction between $f$ and $P_{\text{mean}}$ is differentiability. The softmax function is composed entirely of exponentials, sums, and divisions, all of which have well-defined, continuous derivatives. Changing a router logit by an infinitesimal amount produces a smooth, proportional change in the corresponding softmax probability. This means backpropagation can flow through $P_i$ to update the router weights $W_g$, even for experts that received zero tokens in the hard assignment. Expert 3, which has $f_3 = 0.0$, still maintains a non-zero soft probability of $P_3 = 0.2340$, providing a continuous gradient pathway that the hard fraction entirely lacks.

## The Dot Product: Why $f_i \cdot P_i$ Solves the Problem

The auxiliary loss must accomplish two simultaneous objectives: detect which experts are overloaded using the accurate but non-differentiable $f_i$, and generate corrective gradients through the differentiable $P_i$. The dot product $f_i \cdot P_i$ achieves both by using the hard fraction as a fixed scaling weight on the differentiable probability.

The mechanics of this product for each expert reveal the core dynamic. When gradient descent minimizes $f_i \cdot P_i$, it can only modify $P_i$ because $f_i$ has zero gradient. The hard fraction $f_i$ therefore acts as a fixed multiplier that determines how aggressively the optimizer penalizes each expert's soft probability:

- Expert 0 has $f_0 = 1.0$. The penalty term is $1.0 \times P_0$. The optimizer faces the full force of the penalty and is strongly pressured to reduce $P_0$.
- Expert 1 has $f_1 = 0.5$. The penalty term is $0.5 \times P_1$. The optimizer faces a moderate penalty on $P_1$.
- Expert 2 has $f_2 = 0.5$. The penalty term is $0.5 \times P_2$. The optimizer faces a moderate penalty on $P_2$.
- Expert 3 has $f_3 = 0.0$. The penalty term is $0.0 \times P_3 = 0$. The optimizer faces zero penalty for increasing $P_3$.

This asymmetry is the key mechanism. The overloaded expert incurs a large penalty, creating strong downward pressure on its routing probability. The starved expert incurs no penalty at all, meaning the optimizer can freely increase its probability without any resistance from the auxiliary loss. The net effect: probability mass flows away from dominant experts and toward underutilized experts, directly counteracting the rich-get-richer feedback loop.

## Computing the Auxiliary Loss

The full auxiliary loss sums these weighted products across all experts and applies two scaling constants: $E$, the number of experts, and $\alpha$, a hyperparameter controlling the strength of the penalty relative to the primary training loss:

$$
\mathcal{L}_{aux} = \alpha \cdot E \sum_{i=1}^{E} f_i \cdot P_i
$$

The scaling factor $E$ normalizes the loss so that its magnitude remains comparable regardless of the number of experts in the architecture. The hyperparameter $\alpha$ controls the tradeoff between prediction quality and load balance; typical values range from $0.001$ to $0.01$ in production systems. Setting $\alpha = 0.01$ and $E = 4$ for the toy batch, the individual terms evaluate to:

$$
\begin{aligned}
f_0 \cdot P_0 &= 1.0 \times 0.3072 = 0.3072 \\
f_1 \cdot P_1 &= 0.5 \times 0.2256 = 0.1128 \\
f_2 \cdot P_2 &= 0.5 \times 0.2332 = 0.1166 \\
f_3 \cdot P_3 &= 0.0 \times 0.2340 = 0.0000
\end{aligned}
$$

Summing these terms and applying the scaling factor:

$$
\mathcal{L}_{aux} = 0.01 \times 4 \times (0.3072 + 0.1128 + 0.1166 + 0.0000) = 0.04 \times 0.5366 = 0.0215
$$

## Theoretical Bounds of the Auxiliary Loss

The auxiliary loss has a well-defined minimum and maximum, determined by the mathematical constraints on $f$ and $P$. Every token selects exactly $k$ experts, meaning the hard fractions across all experts must sum to $k$. The soft probabilities are produced by a softmax function, forcing their total sum to strictly equal one:

$$
\begin{aligned}
\sum_{i=1}^{E} f_i &= k \\
\sum_{i=1}^{E} P_i &= 1
\end{aligned}
$$

In a state of perfectly balanced routing, these totals distribute equally among all $E$ experts, yielding $f_i = k/E$ and $P_i = 1/E$ for every expert. Substituting into the auxiliary loss, all $E$ product terms become identical:

$$
\begin{aligned}
\mathcal{L}_{min} &= \alpha \cdot E \sum_{i=1}^{E} \left(\frac{k}{E} \cdot \frac{1}{E}\right) \\
&= \alpha \cdot E \cdot E \cdot \frac{k}{E^2} \\
&= \alpha \cdot k
\end{aligned}
$$

At the opposite extreme, total expert collapse concentrates all probability mass into a single expert. That expert receives every token, yielding $f_{collapse} = 1.0$ and $P_{collapse} = 1.0$, while all remaining experts receive $f_j = 0$ and $P_j = 0$. The summation reduces to a single non-zero term:

$$
\begin{aligned}
\mathcal{L}_{max} &= \alpha \cdot E \left(1.0 \cdot 1.0 + \sum_{j \neq collapse} 0 \cdot 0 \right) \\
&= \alpha \cdot E
\end{aligned}
$$

The ratio between maximum and minimum penalty is $E/k$. For this toy configuration with $E = 4$ and $k = 2$, the loss ranges from $\alpha \cdot 2 = 0.02$ at perfect balance to $\alpha \cdot 4 = 0.04$ at total collapse. For production architectures like DeepSeek-V3 with $E = 256$ and $k = 8$, the ratio is $32$, creating a steep penalty gradient between balanced and collapsed states.

## The Gradient Signal: Which Direction Each Expert Moves

The auxiliary loss produces gradient updates through standard backpropagation, functioning identically to the gradient mechanics established in the Transformer series. The hard fraction $f_i$ carries zero gradient, as demonstrated by the step-function derivative analysis above. Backpropagation therefore treats $f_i$ as a fixed constant and applies the chain rule exclusively through the differentiable soft probabilities. 

To determine exactly how the optimization algorithm adjusts a specific router logit $h(x)_j$ for a given token $x$, the partial derivative must flow backward through the auxiliary loss summation and into the softmax function. Starting from the definition of the auxiliary loss, expanding the mean probability $P_i$ into its summation over all tokens reveals how the derivative isolates the specific token $x$:

$$
\begin{aligned}
\mathcal{L}_{aux} &= \alpha \cdot E \sum_{i=1}^{E} f_i \left( \frac{1}{N} \sum_{x \in \mathcal{B}} P(x)_i \right) \\
\frac{\partial \mathcal{L}_{aux}}{\partial h(x)_j} &= \frac{\alpha \cdot E}{N} \sum_{i=1}^E f_i \frac{\partial P(x)_i}{\partial h(x)_j}
\end{aligned}
$$

As established in the core Transformer architecture, the derivative of a softmax output $P(x)_i$ with respect to a logit $h(x)_j$ evaluates to $P(x)_i(1 - P(x)_j)$ when $i = j$, and $-P(x)_i P(x)_j$ when $i \neq j$. This relationship is compactly written using the Kronecker delta as $P(x)_i(\delta_{ij} - P(x)_j)$. The Kronecker delta $\delta_{ij}$ acts as a mathematical filter that equals $1$ when $i = j$ and $0$ otherwise. 

Distributing the summation across this derivative separates the expression into two parts. The $\delta_{ij}$ filter causes the first summation to collapse entirely to the single case where $i = j$, dropping all other terms. Factoring out $P(x)_j$ from the resulting expression yields the exact analytical gradient:

$$
\begin{aligned}
\frac{\partial \mathcal{L}_{aux}}{\partial h(x)_j} &= \frac{\alpha \cdot E}{N} \sum_{i=1}^E f_i \left[ P(x)_i (\delta_{ij} - P(x)_j) \right] \\
&= \frac{\alpha \cdot E}{N} \left( \sum_{i=1}^E f_i P(x)_i \delta_{ij} - \sum_{i=1}^E f_i P(x)_i P(x)_j \right) \\
&= \frac{\alpha \cdot E}{N} \left( f_j P(x)_j - \sum_{i=1}^E f_i P(x)_i P(x)_j \right) \\
&= \frac{\alpha \cdot E}{N} \cdot P(x)_j \left( f_j - \sum_{i=1}^E f_i P(x)_i \right)
\end{aligned}
$$

The behavior of the gradient is entirely determined by the inner subtraction. The summation term represents the dot product between the global hard routing fractions and the specific token's soft probabilities. The optimization algorithm subtracts this dot product from the hard fraction $f_j$ to determine the precise direction and magnitude of the weight update.

Applying this analytical derivative to Token 1 from the toy batch perfectly demonstrates the corrective mechanics. The dot product for Token 1 evaluates to $0.5231$. Subtracting this value from the fixed $f_j$ constants and scaling by the token probabilities yields the exact gradients flowing into Token 1's logits:

$$
\begin{aligned}
\frac{\partial \mathcal{L}_{aux}}{\partial h(x_1)_0} &\propto 0.2937 \cdot (1.0 - 0.5231) = +0.1401 \\
\frac{\partial \mathcal{L}_{aux}}{\partial h(x_1)_1} &\propto 0.1994 \cdot (0.5 - 0.5231) = -0.0046 \\
\frac{\partial \mathcal{L}_{aux}}{\partial h(x_1)_2} &\propto 0.2593 \cdot (0.5 - 0.5231) = -0.0060 \\
\frac{\partial \mathcal{L}_{aux}}{\partial h(x_1)_3} &\propto 0.2476 \cdot (0.0 - 0.5231) = -0.1295
\end{aligned}
$$

A positive gradient instructs the optimization algorithm to push the corresponding logit downward, reducing the probability of future selection. A negative gradient instructs the optimization algorithm to pull the logit upward, increasing future selection probability. Expert 0 holds a massive global monopoly with a hard fraction of $1.0$, meaning it incurs a strong positive gradient that aggressively suppresses its logit. Expert 3 is entirely starved of tokens globally with a hard fraction of $0.0$, so it receives a strong negative gradient pulling its logit upward. Experts 1 and 2 sit slightly below the average distribution, resulting in small upward corrective pulls.

## Numerical Stability: The Router Z-Loss

Large router logits create a secondary failure mode entirely unrelated to load balance. The softmax denominator $\sum_{j=1}^E e^{h(x)_j}$ involves exponentiation, meaning the values grow exponentially fast as the logits increase. Modern neural networks train using 16-bit floating point precision to conserve memory and accelerate matrix multiplications, but this format enforces a strict maximum representable value of $65504$. Since $e^{11} \approx 59874$, any logit exceeding $11.1$ causes the exponentiation to surpass $65504$. The hardware registers an overflow and returns an infinite value, which cascades through the division step and permanently corrupts the softmax probabilities into a Not-a-Number state.

Preventing this overflow requires explicitly anchoring the magnitude of the logits near zero. This is achieved using a secondary penalty known as the router z-loss. The z-loss isolates the softmax denominator, takes its natural logarithm, a mathematical construct known as `logsumexp`, and penalizes its squared magnitude:

$$
\mathcal{L}_z = \frac{c_z}{N} \sum_{x \in \mathcal{B}} \left( \ln \sum_{j=1}^E e^{h(x)_j} \right)^2
$$

A toy set of logits like $[1.0, 2.0, 3.0]$ demonstrates how this prevents overflow. The actual maximum logit is $3.0$. The sum of their exponentials evaluates to $e^{1.0} + e^{2.0} + e^{3.0} \approx 30.17$. Taking the natural logarithm of this sum yields $\ln(30.17) \approx 3.4$. The `logsumexp` output is slightly larger than the maximum logit, since the sum of all exponentials must be strictly greater than the single largest exponential. However, as the logits grow, the largest exponential completely dominates the sum, making `logsumexp` behave as a smooth, differentiable upper bound on the maximum logit.

Adding this term to the total training loss forces the backpropagation algorithm to minimize it. Squaring the `logsumexp` constructs a parabolic loss landscape with its absolute minimum at exactly zero. The mechanics of gradient descent always push network parameters down the slope of the loss landscape toward the minimum. If the maximum logit drifts into high positive numbers, the `logsumexp` evaluates to a positive value, generating a positive gradient that instructs the optimizer to decrease the network weights and pull the logits down. Conversely, if the maximum logit drops into deep negative numbers, the `logsumexp` evaluates to a negative value. Squaring a negative number yields a positive loss, which generates a negative gradient that instructs the optimizer to increase the weights, pulling the logits back up. This bidirectional gradient explicitly pins the `logsumexp` precisely at zero. 

Since the `logsumexp` is always slightly larger than the true maximum logit, pinning the `logsumexp` at zero forces the maximum logit to settle safely just below zero. This global downward shift avoids disrupting the routing assignments because the softmax function is translationally invariant. Subtracting a constant scalar $c$ from every logit does not alter the final probability distribution. The mathematical proof relies on the algebraic rules of exponents: 

$$
\text{Softmax}(x_i - c) = \frac{e^{x_i - c}}{\sum e^{x_j - c}} = \frac{e^{-c} \cdot e^{x_i}}{e^{-c} \sum e^{x_j}} = \frac{e^{x_i}}{\sum e^{x_j}}
$$

The shift constant $e^{-c}$ factors completely out of both the numerator and the denominator, perfectly canceling itself out. A logit cluster of $[10, 11]$ yields the exact same probability distribution as a cluster of $[-1, 0]$. The z-loss therefore acts as a physical anchor. It applies a uniform gravitational pull that keeps the entire group of logits safely centered near zero, ensuring no single logit ever reaches the $11.1$ overflow boundary, while preserving the relative distances between the logits that determine the actual routing assignments.

Applying $c_z = 0.001$ to the four-token batch yields a z-loss of $0.001653$.

## Combining All Losses: The Total Training Objective

The complete training objective combines the primary language modeling loss with both routing penalties through addition:

$$
\mathcal{L}_{total} = \mathcal{L}_{LM} + \alpha \mathcal{L}_{aux} + c_z \mathcal{L}_z
$$

Addition works for multi-objective optimization because the gradient of a sum equals the sum of the individual gradients. During backpropagation, the optimizer independently computes how each loss would adjust the router weights and then sums these adjustments into a single update vector. Each loss contributes its own directional pressure without interfering with the computation of the others.

This additive structure creates a deliberate tension between two competing forces. The primary loss $\mathcal{L}_{LM}$ optimizes prediction accuracy by routing tokens to the most capable experts. Due to the Top-K selection, $\mathcal{L}_{LM}$ generates gradient updates exclusively for the winning experts, reinforcing their dominance and driving the system toward collapse. The auxiliary loss $\mathcal{L}_{aux}$ counteracts this by computing gradients through the unmasked softmax probabilities $P_i$, which exist for every expert regardless of selection. The auxiliary loss generates corrective signals for all experts simultaneously, including those receiving zero tokens, because $P_i$ is computed before the Top-K mask is applied.

The hyperparameter $\alpha$ controls the balance of power between these competing objectives. A small $\alpha$ allows the primary loss to dominate, producing better predictions at the risk of mild imbalance. A large $\alpha$ enforces strict load balance at the cost of suboptimal routing, because the optimizer may be forced to send tokens to less capable experts simply to equalize counts. This tradeoff between prediction quality and routing balance is inherent to the auxiliary loss formulation, and motivates the auxiliary-loss-free alternatives explored in a later chapter.

The auxiliary loss and z-loss together provide the mathematical guardrails necessary to stabilize the router during training. While these penalties prevent expert starvation at the level of routing probability, physical hardware imposes a separate constraint: each expert can only process a finite number of tokens per batch before its computational buffer overflows. Managing this physical limitation requires the introduction of explicit capacity factors and token dropping mechanics.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/mixture-of-experts-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Mixture of Experts Ebook here.</a></em></p>
