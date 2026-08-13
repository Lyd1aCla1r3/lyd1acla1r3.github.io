# Part 4: Backpropagation Through Loss and Softmax

<!-- SUMMARY: With the loss computed, the gradient signal is traced backwards through the loss and Softmax layer. Each partial derivative is derived from first principles, revealing how the coupled Softmax-Cross-Entropy pipeline collapses into the unified "predicted minus truth" gradient expression. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The previous chapter ended with a single scalar: $L = 0.79$. This number is the network's total error—a mathematical verdict on the quality of the forward pass. To learn, the network must translate this single number into specific, targeted corrections to thousands of individual weights distributed across two matrices ($W_U$ and $W_E$).

The mechanism that accomplishes this is **Backpropagation**: the systematic application of the chain rule from calculus, working backwards from the loss through each layer of the network. The output is the **gradient**—a vector of partial derivatives that dictates how much each weight contributed to the error, and in which direction it must move to reduce it.

## From Scalar to Signal

The expression $\frac{\partial L}{\partial w}$ asks a precise question: *if this single weight $w$ is nudged by an infinitesimally small amount, while holding every other weight in the network frozen, how does the loss $L$ change?*

The goal is to drive the loss to zero—a perfect prediction. If the derivative is positive, increasing $w$ increases the loss. If it is negative, increasing $w$ decreases the loss. When the derivative is exactly zero, the weight is sitting at a point where the loss is locally minimized. The magnitude dictates how *sensitive* the loss is to this particular weight: a large magnitude means small changes to $w$ cause large swings in the loss, while a magnitude near zero means the weight is nearly irrelevant to the prediction.

Computing this derivative for a weight in the final layer is straightforward, as it directly connects to the loss. For a weight in $W_E$, located at the first layer, the relationship is indirect: a change in $W_E$ alters the hidden state $\mathbf{h}$, which alters the logits $\mathbf{z}$, which alters the Softmax probabilities $\hat{\mathbf{y}}$, which finally alters the loss $L$. The **chain rule** decomposes this dependency into a product of simple, local derivatives:

$$
\frac{\partial L}{\partial W_E} = \frac{\partial L}{\partial \hat{\mathbf{y}}} \cdot \frac{\partial \hat{\mathbf{y}}}{\partial \mathbf{z}} \cdot \frac{\partial \mathbf{z}}{\partial \mathbf{h}} \cdot \frac{\partial \mathbf{h}}{\partial W_E}
$$

Each factor in this product is a tractable computation. Each derivative is now derived, starting from the loss and working backwards to $W_E$.

## The Loss Derivative: $\frac{\partial L}{\partial \hat{\mathbf{y}}}$

The first link in the chain is straightforward. The question is: how does the loss change when the predicted probabilities change?

Recall from Chapter 3 that the Cross-Entropy Loss, after collapsing under the one-hot encoded truth vector, reduces to:

$$
L = -\log(\hat{y}_{true})
$$

The loss depends on exactly one element of the predicted distribution: $\hat{y}_{true}$, the probability the network assigned to the correct word (`fox`, at index 3). It is completely independent of the probabilities assigned to every other word. This means the partial derivative of the loss with respect to any incorrect word's probability is simply zero:

$$
\frac{\partial L}{\partial \hat{y}_k} = 0 \quad \text{for all } k \neq true
$$

For the correct word, the derivative of $-\log(x)$ with respect to $x$ is required. This is a standard result from calculus: the derivative of $\log(x)$ is $\frac{1}{x}$, and the leading negative sign carries through:

$$
\frac{\partial L}{\partial \hat{y}_{true}} = \frac{-1}{\hat{y}_{true}}
$$

This result has a clear interpretation. If the network assigned a high probability to the correct word (say, $\hat{y}_{true} = 0.95$), the derivative is small: $\frac{-1}{0.95} \approx -1.05$. The loss is barely sensitive to further changes—the network is already nearly correct. But if the network assigned a tiny probability (say, $\hat{y}_{true} = 0.01$), the derivative is massive: $\frac{-1}{0.01} = -100$. The loss is *extremely* sensitive, generating a strong signal to fix the prediction. The negative sign indicates that *increasing* $\hat{y}_{true}$ will *decrease* the loss.

## The Softmax Derivative: $\frac{\partial \hat{\mathbf{y}}}{\partial \mathbf{z}}$

The second link in the chain is more involved. The question becomes: how does each Softmax output $\hat{y}_i$ change when a single logit $z_j$ is adjusted?

The three index variables used throughout this derivation are defined as follows:

- **$i$** — the index of the word whose **probability** is being measured (the "target" of the observation).
- **$j$** — the index of the word whose **logit** is being altered (the "cause" of the change).
- **$k$** — a summation placeholder that ranges over all $V$ words in the vocabulary. It appears only inside $\sum_k$ expressions.

Recall the Softmax definition:

$$
\hat{y}_i = \frac{e^{z_i}}{\sum_{k=1}^{V} e^{z_k}}
$$

This is a fraction: a numerator ($e^{z_i}$) divided by a denominator ($\sum_k e^{z_k}$). The denominator is a sum over *all* logits in the vocabulary. Changing a single logit $z_j$ does not only affect the probability $\hat{y}_j$ for that word—it also changes the denominator, which in turn changes *every other* probability $\hat{y}_i$.

To differentiate this fraction, the **quotient rule** from calculus is applied. For any function expressed as a fraction $\frac{f}{g}$, the quotient rule states:

$$
\frac{d}{dx}\left(\frac{f}{g}\right) = \frac{f' \cdot g \;-\; f \cdot g'}{g^2}
$$

where $f'$ denotes the derivative of the numerator and $g'$ denotes the derivative of the denominator.

Here, the Softmax numerator is $f = e^{z_i}$ and the denominator is $g = \sum_k e^{z_k}$. Applying the quotient rule requires $f'$ and $g'$—the derivatives of the numerator and denominator with respect to the logit $z_j$ being differentiated. The derivative of the numerator $e^{z_i}$ depends entirely on whether $z_j$ is the *same* variable as $z_i$ or a *different* one.

If measuring how the probability of `fox` changes when adjusting the logit for `fox` itself ($i = j$), the numerator $e^{z_{fox}}$ depends on the variable of differentiation, making its derivative non-zero. If measuring how the probability of `fox` changes when adjusting the logit for `The` ($i \neq j$), the numerator $e^{z_{fox}}$ does not contain $z_{The}$ at all—it is a constant, and its derivative is zero. This fundamental difference in the numerator's derivative produces two structurally different results, requiring the two cases to be handled separately.

### Case 1: $i = j$ (same word)

The probability $\hat{y}_i$ is differentiated with respect to its *own* logit, $z_i$. This models how the predicted probability of `fox` changes when the logit for `fox` is adjusted.

The derivatives of both the numerator and denominator with respect to $z_i$ are calculated as follows:

- **Numerator derivative**: $f' = \frac{\partial}{\partial z_i} e^{z_i} = e^{z_i}$. The exponential function is its own derivative, and since the numerator *does* contain $z_i$, the result is non-zero.
- **Denominator derivative**: $g' = \frac{\partial}{\partial z_i} \sum_k e^{z_k} = e^{z_i}$. The sum contains many terms ($e^{z_1}, e^{z_2}, \dots$), but only the one term $e^{z_i}$ depends on $z_i$. All other terms are constants with respect to $z_i$ and vanish under differentiation.

Substituting $f$, $g$, $f'$, and $g'$ into the quotient rule formula $\frac{f'g - fg'}{g^2}$:

$$
\frac{\partial \hat{y}_i}{\partial z_i} = \frac{e^{z_i} \cdot \sum_k e^{z_k} \;-\; e^{z_i} \cdot e^{z_i}}{\left(\sum_k e^{z_k}\right)^2}
$$

Factoring $e^{z_i}$ out of the numerator yields:

$$
= \frac{e^{z_i} \left(\sum_k e^{z_k} \;-\; e^{z_i}\right)}{\left(\sum_k e^{z_k}\right)^2}
$$

This single fraction is then split into a product of two fractions:

$$
= \frac{e^{z_i}}{\sum_k e^{z_k}} \cdot \frac{\sum_k e^{z_k} \;-\; e^{z_i}}{\sum_k e^{z_k}}
$$

The first fraction is, by definition, $\hat{y}_i$. The second fraction is $1 - \hat{y}_i$ (the full sum minus the $i$-th term, divided by the full sum). Therefore:

$$
\frac{\partial \hat{y}_i}{\partial z_i} = \hat{y}_i(1 - \hat{y}_i)
$$

This result has a natural interpretation. The derivative is largest when $\hat{y}_i \approx 0.5$—maximum uncertainty—and shrinks toward zero as $\hat{y}_i$ approaches $0$ or $1$. A confident prediction is *insensitive* to small logit perturbations; an uncertain one is highly responsive. This is a fundamental property of sigmoid-family functions, reflecting the fact that Softmax **saturates** at its extremes.

### Case 2: $i \neq j$ (different words)

The probability $\hat{y}_i$ is differentiated with respect to a *different* logit, $z_j$. This models how the predicted probability of `The` changes when the logit for `fox` is adjusted.

The numerator and denominator derivatives with respect to $z_j$ are:

- **Numerator derivative**: $f' = \frac{\partial}{\partial z_j} e^{z_i} = 0$. The numerator $e^{z_i}$ does not contain $z_j$ at all—it is a constant with respect to $z_j$—so its derivative is zero. This is the key difference from Case 1.
- **Denominator derivative**: $g' = \frac{\partial}{\partial z_j} \sum_k e^{z_k} = e^{z_j}$. Just as before, only the one term $e^{z_j}$ in the sum depends on $z_j$.

Substituting into the quotient rule formula $\frac{f'g - fg'}{g^2}$:

$$
\frac{\partial \hat{y}_i}{\partial z_j} = \frac{0 \cdot \sum_k e^{z_k} \;-\; e^{z_i} \cdot e^{z_j}}{\left(\sum_k e^{z_k}\right)^2}
$$

The first term in the numerator vanishes (anything multiplied by zero is zero), leaving:

$$
= \frac{-e^{z_i} \cdot e^{z_j}}{\left(\sum_k e^{z_k}\right)^2}
$$

This splits into a product of two fractions, each recognized as a Softmax output:

$$
= -\frac{e^{z_i}}{\sum_k e^{z_k}} \cdot \frac{e^{z_j}}{\sum_k e^{z_k}} = -\hat{y}_i \cdot \hat{y}_j
$$

Recall from Chapter 3 that all Softmax outputs must sum to exactly $1.0$. The total probability is fixed. If the logit for `fox` ($z_j$) increases, the probability of `fox` ($\hat{y}_j$) grows. To maintain a sum of $1.0$, every other word's probability must shrink.

The derivative $-\hat{y}_i \cdot \hat{y}_j$ dictates exactly how much each word loses. For example, if the probability of `fox` is $\hat{y}_{fox} = 0.45$ and the probability of `The` is $\hat{y}_{The} = 0.18$, then the rate at which `The` loses probability when the logit for `fox` is increased is $-0.18 \times 0.45 = -0.081$. If the probability of `jumps` is only $\hat{y}_{jumps} = 0.009$, it loses probability at a rate of $-0.009 \times 0.45 = -0.004$. Words holding larger probability mass have more to lose; words near zero are barely affected.

### Summary of the Softmax Derivative

These two cases fully describe how the Softmax function responds to logit changes. Case 1 dictates how a word's own probability responds to its own logit, while Case 2 dictates how every other word's probability responds. These results are now combined with the loss derivative to compute the gradient of the loss with respect to the logits, $\frac{\partial L}{\partial \mathbf{z}}$.

## Combining: The Gradient at the Logits ($\frac{\partial L}{\partial \mathbf{z}}$)

The first two links of the chain have been computed independently. The loss derivative (Step 1) dictates how the loss responds to changes in the predicted probabilities. The Softmax derivative (Step 2) dictates how the predicted probabilities respond to changes in the logits. These are combined via the chain rule to determine how the loss responds to changes in the logits:

$$
\frac{\partial L}{\partial z_i} = \sum_{k=1}^{V} \frac{\partial L}{\partial \hat{y}_k} \cdot \frac{\partial \hat{y}_k}{\partial z_i}
$$

This summation ranges over every word in the vocabulary, because changing a single logit $z_i$ affects every Softmax output $\hat{y}_k$. However, Step 1 established that $\frac{\partial L}{\partial \hat{y}_k} = 0$ for every $k \neq true$. This means every term in the sum where $k$ is an incorrect word multiplies by zero and vanishes. Only the term where $k = true$ survives:

$$
\frac{\partial L}{\partial z_i} = \frac{-1}{\hat{y}_{true}} \cdot \frac{\partial \hat{y}_{true}}{\partial z_i}
$$

The appropriate Softmax derivative case is substituted depending on whether $z_i$ is the logit for the correct word or an incorrect word.

**For the correct class ($i = true$):** Case 1 is used, where $\frac{\partial \hat{y}_{true}}{\partial z_{true}} = \hat{y}_{true}(1 - \hat{y}_{true})$:

$$
\frac{\partial L}{\partial z_{true}} = \frac{-1}{\hat{y}_{true}} \cdot \hat{y}_{true}(1 - \hat{y}_{true})
$$

The $\hat{y}_{true}$ in the denominator cancels with the $\hat{y}_{true}$ in the numerator:

$$
= -(1 - \hat{y}_{true}) = \hat{y}_{true} - 1
$$

**For every incorrect class ($i \neq true$):** Case 2 is used, where $\frac{\partial \hat{y}_{true}}{\partial z_i} = -\hat{y}_{true} \cdot \hat{y}_i$:

$$
\frac{\partial L}{\partial z_i} = \frac{-1}{\hat{y}_{true}} \cdot (-\hat{y}_{true} \cdot \hat{y}_i)
$$

The two negative signs cancel each other, and $\hat{y}_{true}$ cancels between the numerator and denominator:

$$
= \hat{y}_i
$$

### The Unified Gradient Expression

The two results are summarized as follows:

- **For the correct class** ($i = true$, which is `fox` at index 3): the gradient is $\hat{y}_{true} - 1$.
- **For every incorrect class** ($i \neq true$, such as `The`, `quick`, `brown`, etc.): the gradient is $\hat{y}_i$.

These appear as two different formulas. However, the true label vector $\mathbf{y}$ is one-hot encoded—it contains $1$ at index 3 (`fox`) and $0$ at every other index. Writing each case as $\hat{y}_i - y_i$ yields the following:

- For `fox` (index 3): $y_3 = 1$, so $\hat{y}_3 - y_3 = \hat{y}_{true} - 1$. This matches our correct-class result.
- For `The` (index 0): $y_0 = 0$, so $\hat{y}_0 - y_0 = \hat{y}_0 - 0 = \hat{y}_0$. This matches our incorrect-class result.
- For `quick` (index 1): $y_1 = 0$, so $\hat{y}_1 - y_1 = \hat{y}_1$. Same pattern.

Both cases follow the identical formula: $\hat{y}_i - y_i$. The one-hot structure of $\mathbf{y}$ naturally absorbs the case distinction—the $-1$ only appears at the correct class because that is the only index where $y_i$ is non-zero. The gradient for *every* logit in the vocabulary is therefore expressed as a single, unified vector expression:

$$
\frac{\partial L}{\partial \mathbf{z}} = \hat{\mathbf{y}} - \mathbf{y}
$$

The entire pipeline—quotient rules, logarithmic derivatives, case-splitting across the Softmax—reduces entirely to **predicted minus truth**.

Cross-Entropy Loss is mathematically structured to pair with Softmax and produce this result. The logarithm in the loss algebraically cancels with the exponential in Softmax, and the normalization structure ensures the gradient is always bounded and well-behaved. This coupling is why Cross-Entropy is the standard loss function for classification: it guarantees numerically stable gradients pointing directly toward the correct answer.

For our toy network, this gradient is interpretable at a glance. Every incorrect word in the vocabulary receives a *positive* gradient (its predicted probability minus zero), signaling that its logit should decrease. The correct word `fox` receives a *negative* gradient ($\hat{y}_{fox} - 1$, a number less than zero), signaling that its logit should increase. The magnitudes are self-calibrating—the most overconfident wrong answers receive the strongest corrections.


The gradient at the logits has been established. The next chapter continues the backward pass through the weight matrices.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
