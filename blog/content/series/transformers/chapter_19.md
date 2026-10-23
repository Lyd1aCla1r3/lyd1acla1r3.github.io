# Part 19: The Cross-Entropy Loss Function

<!-- SUMMARY: The error of the raw predictions is formalized by calculating the cross-entropy loss against the one-hot target distribution. This asymmetric logarithmic penalty heavily punishes confidently incorrect predictions, yielding a mathematically clean error signal for the network to optimize. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>

The final Softmax operation completes the forward pass by producing a strict probability distribution over the vocabulary for every position in the sequence. Assessing the quality of these predictions requires a metric that quantifies how far the current hypotheses deviate from the ground truth. That metric is the loss function, which produces the single scalar value that the entire architecture is trained to minimize.

## Defining the Target Distribution

Measuring prediction error first requires defining an ideal prediction. At the first time step where the input sequence begins with `<BOS>`, the actual next token in the training sequence is `i`. An ideal probability distribution assigns a probability of `1.0` to the target token and `0.0` to all other vocabulary tokens. That target distribution is identical to the one-hot vector used to look up the initial token embedding in Part 1. The loss function measures the divergence between the predicted probability distribution and this one-hot target state.

A naive approach to measuring this divergence takes the squared difference between the predicted probabilities and the target probabilities. Mean squared error performs well for continuous regression tasks, yet it degrades optimization over classification probabilities. Confidently wrong predictions push the Softmax output into flat asymptotic regions where mean squared error gradients shrink, slowing parameter updates when the network requires the largest structural corrections.

The architecture instead uses cross-entropy loss. Against a one-hot target vector, cross-entropy evaluates only the predicted probability assigned to the ground-truth target class, defined as the negative natural logarithm of the target probability:

$$
\text{Loss} = -\log(P_{\text{target}})
$$

The natural logarithm has three mathematical properties suited to probabilistic error measurement:

- **Zero Penalty at Certainty:** Assigning a probability of `1.0` to the target token yields $-\log(1.0) = 0$, producing zero loss.
- **Asymmetric Divergence Near Zero:** Decreasing the target probability toward `0.0` drives $-\log(P_{\text{target}})$ toward $+\infty$, penalizing confident misclassifications and forcing large corrective gradients.
- **Additive Log-Likelihood:** Taking the logarithm converts the product of independent sequence probabilities into a sum of positional log-losses, simplifying the chain-rule derivatives during backpropagation.

## Teacher Forcing Across the Sequence

The architecture evaluates predictions across all sequence positions in parallel using teacher forcing. The input sequence consists of the four tokens `<BOS>`, `i`, `woke`, and `up`. The target sequence shifts one position forward, requiring the network to predict `i`, `woke`, `up`, and `late` across a probability tensor of shape $B \times S \times V = 1 \times 4 \times 12$.

| Position | Input Token | Target Token (`Index`) | Target Probability (`P_target`) | Positional Loss (`-log P_target`) |
| :--- | :--- | :--- | :--- | :--- |
| **Step 1** | `<BOS>` | `i` (`3`) | `0.0843` | `2.4734` |
| **Step 2** | `i` | `woke` (`5`) | `0.0831` | `2.4877` |
| **Step 3** | `woke` | `up` (`7`) | `0.0833` | `2.4853` |
| **Step 4** | `up` | `late` (`8`) | `0.0833` | `2.4853` |

Extracting the probability assigned to the ground-truth target index at each of the four time steps from the Part 18 probability matrix and applying the negative natural logarithm produces the four-element positional loss vector:

$$
\text{Loss} = \begin{bmatrix}
   -\log(P_{\text{i}}) \\
   -\log(P_{\text{woke}}) \\
   -\log(P_{\text{up}}) \\
   -\log(P_{\text{late}}) 
\end{bmatrix} = \begin{bmatrix}
   -\log(0.0843) \\
   -\log(0.0831) \\
   -\log(0.0833) \\
   -\log(0.0833) 
\end{bmatrix} = \begin{bmatrix}
   2.4734 \\
   2.4877 \\
   2.4853 \\
   2.4853
\end{bmatrix}
$$

## Evaluating the Untrained Baseline

Averaging the four positional penalties across the sequence length $S = 4$ reduces the loss vector to a single scalar objective:

$$
\text{Mean Loss} = \frac{2.4734 + 2.4877 + 2.4853 + 2.4853}{4} = 2.4829
$$

This mean loss of `2.4829` reflects the uniform uncertainty of an untrained network. Uncalibrated weight matrices distribute probability mass nearly evenly across all $V = 12$ vocabulary tokens, assigning each token a baseline probability near $1/12 \approx 0.0833$. A uniform distribution over twelve classes produces a theoretical cross-entropy loss of $-\log(1/12) = \log(12) \approx 2.4849$.

The proximity of the calculated loss (`2.4829`) to the uniform entropy baseline (`2.4849`) verifies the numerical integrity of the forward pass and confirms that the initialized network begins near maximum entropy. The backward pass next applies the chain rule of calculus to differentiate this scalar loss and propagate parameter updates back through the network.

<p><em>Prefer to read this offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Transformer Ebook here.</a></em></p>
