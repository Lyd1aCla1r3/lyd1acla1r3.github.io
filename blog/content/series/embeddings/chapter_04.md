# Part 4: Backpropagation Through Loss and Softmax

<!-- SUMMARY: With the loss computed, the gradient signal is traced backward through the loss and Softmax layer. Each partial derivative is derived from first principles, revealing how the coupled Softmax-Cross-Entropy pipeline collapses into the unified "predicted minus truth" gradient expression. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter ended with a single scalar: $L = 0.79$. This number represents the network's total error, a mathematical verdict on the quality of the forward pass. To learn, the network must translate this single scalar into targeted corrections across the individual weights of both matrices ($W_U$ and $W_E$).

**Backpropagation** accomplishes this credit assignment through the systematic application of the calculus chain rule, working backward from the loss through each layer of the network. The output is the **gradient**, a collection of partial derivatives that specifies how much each weight contributed to the error and which direction reduces the loss.

## From Scalar to Signal

The partial derivative $\frac{\partial L}{\partial w}$ answers a specific question: *holding every other weight in the network frozen, how does nudging this single weight $w$ by an infinitesimally small amount change the loss $L$?*

The optimization objective drives the loss toward zero, corresponding to an accurate prediction. A positive derivative indicates that increasing $w$ increases the loss. A negative derivative indicates that increasing $w$ decreases the loss. A zero derivative indicates that the weight sits at a stationary point where the loss is locally minimized. The magnitude measures how *sensitive* the loss is to this particular weight: a large magnitude means small changes to $w$ cause large swings in the loss, whereas a magnitude near zero means the weight barely affects the prediction.

Computing this derivative for a weight in the final layer is direct because that layer connects immediately to the loss. For a weight in $W_E$, located at the first layer, the relationship is indirect: a change in $W_E$ alters the hidden state $\mathbf{h}$, which alters the logits $\mathbf{z}$, which alters the Softmax probabilities $\hat{\mathbf{y}}$, which finally alters the loss $L$. The **chain rule** decomposes this dependency into a product of local derivatives:

$$
\frac{\partial L}{\partial W_E} = \frac{\partial L}{\partial \hat{\mathbf{y}}} \cdot \frac{\partial \hat{\mathbf{y}}}{\partial \mathbf{z}} \cdot \frac{\partial \mathbf{z}}{\partial \mathbf{h}} \cdot \frac{\partial \mathbf{h}}{\partial W_E}
$$

Each factor in this product is a tractable local computation. The derivation proceeds step by step from the loss backward toward $W_E$.

## The Loss Derivative: $\frac{\partial L}{\partial \hat{\mathbf{y}}}$

The first link in the chain measures how the loss changes when the predicted probabilities change.

Recall from Chapter 3 that the Cross-Entropy Loss, after collapsing under the one-hot encoded ground-truth vector, reduces to:

$$
L = -\log(\hat{y}_{\text{true}})
$$

The loss depends on a single element of the predicted distribution: $\hat{y}_{\text{true}}$, the probability the network assigned to the target word (`fox`, at index `3`). The loss expression is independent of the probabilities assigned to every other word, so the partial derivative of the loss with respect to any incorrect word's probability equals zero:

$$
\frac{\partial L}{\partial \hat{y}_k} = 0 \quad \text{for all } k \neq \text{true}
$$

For the target word, differentiation requires the derivative of $-\log(x)$ with respect to $x$. By standard calculus, the derivative of the natural logarithm $\log(x)$ is $\frac{1}{x}$, and the leading negative sign carries through:

$$
\frac{\partial L}{\partial \hat{y}_{\text{true}}} = \frac{-1}{\hat{y}_{\text{true}}}
$$

This inverse relationship calibrates the strength of the learning signal. A high predicted probability for the target word (such as $\hat{y}_{\text{true}} = 0.95$) produces a small derivative: $\frac{-1}{0.95} \approx -1.05$. The loss is barely sensitive to further changes because the prediction is already nearly accurate. A tiny predicted probability (such as $\hat{y}_{\text{true}} = 0.01$) produces a massive derivative: $\frac{-1}{0.01} = -100$. That steep slope generates a strong corrective signal, and the negative sign indicates that *increasing* $\hat{y}_{\text{true}}$ *decreases* the loss.

## The Softmax Derivative: $\frac{\partial \hat{\mathbf{y}}}{\partial \mathbf{z}}$

The second link in the chain measures how each Softmax output $\hat{y}_i$ changes when a single logit $z_j$ is adjusted.

Three 0-based index variables ($i, j, k \in \{0, \dots, V-1\}$) govern this derivation:

- **Output Index ($i$):** Identifies the vocabulary word whose **predicted probability** $\hat{y}_i$ is being measured.
- **Input Index ($j$):** Identifies the vocabulary word whose **logit** $z_j$ is being perturbed.
- **Summation Index ($k$):** Ranges across all $V$ words in the vocabulary inside the normalization denominator $\sum_{k=0}^{V-1} e^{z_k}$.

Recall the Softmax definition from Chapter 3:

$$
\hat{y}_i = \frac{e^{z_i}}{\sum_{k=0}^{V-1} e^{z_k}}
$$

The Softmax expression forms a fraction with numerator $e^{z_i}$ and denominator $\sum_{k=0}^{V-1} e^{z_k}$. The denominator sums the exponentiated logits across the entire vocabulary. Adjusting a single logit $z_j$ alters both the probability $\hat{y}_j$ for that word and the shared denominator, which shifts *every other* probability $\hat{y}_i$ in the distribution.

Differentiating this ratio requires the **quotient rule** from calculus. For any differentiable ratio $\frac{f}{g}$, the quotient rule states:

$$
\frac{d}{dx}\left(\frac{f}{g}\right) = \frac{f' \cdot g \;-\; f \cdot g'}{g^2}
$$

where $f'$ denotes the derivative of the numerator and $g'$ denotes the derivative of the denominator.

The Softmax numerator is $f = e^{z_i}$ and the denominator is $g = \sum_{k=0}^{V-1} e^{z_k}$. Applying the quotient rule requires the derivatives $f'$ and $g'$ of the numerator and denominator with respect to the target logit $z_j$. The derivative of the numerator $e^{z_i}$ depends on whether $z_j$ is the *same* variable as $z_i$ or a *different* variable.

Differentiating the probability of `fox` with respect to the logit for `fox` itself ($i = j$) means the numerator $e^{z_{\text{fox}}}$ contains the variable of differentiation, yielding a non-zero derivative. Differentiating the probability of `fox` with respect to the logit for `The` ($i \neq j$) means the numerator $e^{z_{\text{fox}}}$ does not contain $z_{\text{The}}$, so the numerator acts as a constant whose derivative is zero. This structural distinction splits the Softmax derivative into two cases.

### Case 1: $i = j$ (Same Word)

In the diagonal case, the probability $\hat{y}_i$ is differentiated with respect to its *own* logit, $z_i$, measuring how the predicted probability of `fox` changes when the logit for `fox` is adjusted.

The derivatives of both the numerator and denominator with respect to $z_i$ evaluate as follows:

- **Numerator Derivative ($f'$):** $f' = \frac{\partial}{\partial z_i} e^{z_i} = e^{z_i}$. The natural exponential function is its own derivative, and the numerator contains $z_i$, producing a non-zero result.
- **Denominator Derivative ($g'$):** $g' = \frac{\partial}{\partial z_i} \sum_{k=0}^{V-1} e^{z_k} = e^{z_i}$. The sum contains $V$ terms ($e^{z_0}, e^{z_1}, \dots, e^{z_{V-1}}$), but only the single term $e^{z_i}$ depends on $z_i$. Every other term acts as a constant with respect to $z_i$ and vanishes under differentiation.

Substituting $f$, $g$, $f'$, and $g'$ into the quotient rule formula $\frac{f'g - fg'}{g^2}$ yields:

$$
\frac{\partial \hat{y}_i}{\partial z_i} = \frac{e^{z_i} \cdot \sum_{k=0}^{V-1} e^{z_k} \;-\; e^{z_i} \cdot e^{z_i}}{\left(\sum_{k=0}^{V-1} e^{z_k}\right)^2}
$$

Factoring $e^{z_i}$ out of the numerator produces:

$$
= \frac{e^{z_i} \left(\sum_{k=0}^{V-1} e^{z_k} \;-\; e^{z_i}\right)}{\left(\sum_{k=0}^{V-1} e^{z_k}\right)^2}
$$

Splitting this single fraction into a product of two ratios isolates the Softmax terms:

$$
= \frac{e^{z_i}}{\sum_{k=0}^{V-1} e^{z_k}} \cdot \frac{\sum_{k=0}^{V-1} e^{z_k} \;-\; e^{z_i}}{\sum_{k=0}^{V-1} e^{z_k}}
$$

The first fraction equals $\hat{y}_i$ by definition, and the second fraction simplifies to $1 - \hat{y}_i$ (the full sum minus the $i$-th term, divided by the full sum), yielding the diagonal Softmax derivative:

$$
\frac{\partial \hat{y}_i}{\partial z_i} = \hat{y}_i(1 - \hat{y}_i)
$$

This quadratic expression peaks at $\hat{y}_i = 0.5$ (maximum uncertainty, where $\hat{y}_i(1 - \hat{y}_i) = 0.25$) and shrinks toward zero as $\hat{y}_i$ approaches $0$ or $1$. Confident predictions near the boundaries are *insensitive* to small logit perturbations, whereas uncertain predictions near the midpoint respond strongly because Softmax **saturates** at its extremes.

### Case 2: $i \neq j$ (Different Words)

In the off-diagonal case, the probability $\hat{y}_i$ is differentiated with respect to a *different* logit, $z_j$, measuring how the predicted probability of `The` changes when the logit for `fox` is adjusted.

The numerator and denominator derivatives with respect to $z_j$ evaluate as follows:

- **Numerator Derivative ($f'$):** $f' = \frac{\partial}{\partial z_j} e^{z_i} = 0$. The numerator $e^{z_i}$ does not contain $z_j$ and acts as a constant with respect to $z_j$, so its derivative evaluates to zero.
- **Denominator Derivative ($g'$):** $g' = \frac{\partial}{\partial z_j} \sum_{k=0}^{V-1} e^{z_k} = e^{z_j}$. Only the single term $e^{z_j}$ in the summation depends on $z_j$.

Substituting into the quotient rule formula $\frac{f'g - fg'}{g^2}$ yields:

$$
\frac{\partial \hat{y}_i}{\partial z_j} = \frac{0 \cdot \sum_{k=0}^{V-1} e^{z_k} \;-\; e^{z_i} \cdot e^{z_j}}{\left(\sum_{k=0}^{V-1} e^{z_k}\right)^2}
$$

The first term in the numerator vanishes, leaving:

$$
= \frac{-e^{z_i} \cdot e^{z_j}}{\left(\sum_{k=0}^{V-1} e^{z_k}\right)^2}
$$

Factoring the expression into a product of two ratios isolates the Softmax probabilities for indices $i$ and $j$:

$$
= -\frac{e^{z_i}}{\sum_{k=0}^{V-1} e^{z_k}} \cdot \frac{e^{z_j}}{\sum_{k=0}^{V-1} e^{z_k}} = -\hat{y}_i \cdot \hat{y}_j
$$

Chapter 3 established that all Softmax outputs sum to $1.0$, fixing the total probability mass. Increasing the logit for `fox` ($z_j$) raises the probability of `fox` ($\hat{y}_j$), forcing every other word's probability to shrink so the distribution continues to sum to $1.0$.

The off-diagonal derivative $-\hat{y}_i \cdot \hat{y}_j$ quantifies each competing word's rate of probability loss. With $\hat{y}_{\text{fox}} = 0.45$ and $\hat{y}_{\text{The}} = 0.18$ from Chapter 3, increasing the logit for `fox` reduces the probability of `The` at an instantaneous rate of $-0.18 \times 0.45 = -0.081$. By contrast, `jumps` holds a much smaller probability of $\hat{y}_{\text{jumps}} = 0.009$ and loses mass at a rate of only $-0.009 \times 0.45 = -0.004$. Words holding larger probability mass surrender more probability; words near zero remain barely affected.

### Summary of the Softmax Derivative

These two cases specify the complete Jacobian of the Softmax function. Case 1 governs how a word's probability responds to its own logit, while Case 2 governs how every competing word's probability responds. Combining these two cases with the loss derivative yields the gradient of the loss with respect to the logits, $\frac{\partial L}{\partial \mathbf{z}}$.

## Combining: The Gradient at the Logits ($\frac{\partial L}{\partial \mathbf{z}}$)

The first two links of the chain have been derived independently. The loss derivative governs how the loss responds to changes in the predicted probabilities, and the Softmax derivative governs how the predicted probabilities respond to changes in the logits. Chaining these two factors sums across all $V$ intermediate probabilities:

$$
\frac{\partial L}{\partial z_i} = \sum_{k=0}^{V-1} \frac{\partial L}{\partial \hat{y}_k} \cdot \frac{\partial \hat{y}_k}{\partial z_i}
$$

This summation ranges over every word in the vocabulary because changing a single logit $z_i$ affects every Softmax output $\hat{y}_k$. Step 1 established that $\frac{\partial L}{\partial \hat{y}_k} = 0$ for every $k \neq \text{true}$, so every term in the sum where $k$ is an incorrect word multiplies by zero and vanishes. Only the single term where $k = \text{true}$ survives:

$$
\frac{\partial L}{\partial z_i} = \frac{-1}{\hat{y}_{\text{true}}} \cdot \frac{\partial \hat{y}_{\text{true}}}{\partial z_i}
$$

Substituting the appropriate Softmax derivative case depends on whether $z_i$ is the logit for the target word or an incorrect word.

**For the target class ($i = \text{true}$):** Substituting Case 1, where $\frac{\partial \hat{y}_{\text{true}}}{\partial z_{\text{true}}} = \hat{y}_{\text{true}}(1 - \hat{y}_{\text{true}})$, yields:

$$
\frac{\partial L}{\partial z_{\text{true}}} = \frac{-1}{\hat{y}_{\text{true}}} \cdot \hat{y}_{\text{true}}(1 - \hat{y}_{\text{true}})
$$

Canceling $\hat{y}_{\text{true}}$ between the denominator and numerator simplifies the expression:

$$
= -(1 - \hat{y}_{\text{true}}) = \hat{y}_{\text{true}} - 1
$$

**For every incorrect class ($i \neq \text{true}$):** Substituting Case 2, where $\frac{\partial \hat{y}_{\text{true}}}{\partial z_i} = -\hat{y}_{\text{true}} \cdot \hat{y}_i$, yields:

$$
\frac{\partial L}{\partial z_i} = \frac{-1}{\hat{y}_{\text{true}}} \cdot (-\hat{y}_{\text{true}} \cdot \hat{y}_i)
$$

The two negative signs cancel each other, and $\hat{y}_{\text{true}}$ cancels between the numerator and denominator:

$$
= \hat{y}_i
$$

### The Unified Gradient Expression

The two cases produce two apparent expressions:

- **Target Class ($i = \text{true}$, `fox` at index `3`):** The logit gradient evaluates to $\hat{y}_{\text{true}} - 1$.
- **Incorrect Classes ($i \neq \text{true}$, such as `The`, `quick`, `brown`):** The logit gradient evaluates to $\hat{y}_i$.

The one-hot target vector $\mathbf{y}$ unifies both formulas because $y_i = 1$ at index `3` (`fox`) and $y_i = 0$ at every other index. Expressing the gradient at every index $i$ as $\hat{y}_i - y_i$ recovers both cases simultaneously:

| Vocabulary Token | Index (`i`) | One-Hot Target (`y_i`) | Unified Formula | Evaluated Form | Toy Numerical Gradient |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `The` | `0` | `y_0 = 0` | `y_hat_0 - 0` | `y_hat_0` (Incorrect class) | `+0.18` |
| `quick` | `1` | `y_1 = 0` | `y_hat_1 - 0` | `y_hat_1` (Incorrect class) | `+0.03` |
| `fox` (Target) | `3` | `y_3 = 1` | `y_hat_3 - 1` | `y_hat_true - 1` (Target class) | `0.45 - 1 = -0.55` |

Both cases obey the identical algebraic rule: $\hat{y}_i - y_i$. The one-hot structure of $\mathbf{y}$ absorbs the case distinction because the $-1$ subtraction occurs solely at the target index where $y_i = 1$. Stacking all $V$ indices yields a single vector equation for the gradient across the entire vocabulary:

$$
\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}
$$

The entire derivation across quotient rules, logarithmic derivatives, and Softmax case-splitting collapses to **predicted minus truth**.

Cross-Entropy Loss is mathematically structured to pair with Softmax and produce this cancellation. The logarithm in the loss inverts the exponential in Softmax, and the normalization denominator keeps the resulting gradient bounded between $-1$ and $+1$. This algebraic pairing makes Cross-Entropy the standard loss function for classification, guaranteeing numerically stable gradients that point directly toward the target distribution.

In the 8-word toy network, this gradient vector is interpretable at a glance. Every incorrect word in the vocabulary receives a *positive* gradient ($\hat{y}_i - 0 = \hat{y}_i$), signaling that its logit should decrease under gradient descent. The target word `fox` receives a *negative* gradient ($\hat{y}_{\text{fox}} - 1 = -0.55$), signaling that its logit should increase. The magnitudes are self-calibrating: the most overconfident wrong predictions receive the largest positive gradients and the strongest downward corrections.

The gradient at the logits has been established. The next chapter continues the backward pass through the weight matrices.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
