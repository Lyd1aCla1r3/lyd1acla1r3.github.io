# Part 19: Cross-Entropy Loss

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

In our preceding analysis, we transformed the raw logits of the Transformer into a valid probability distribution using the Softmax function. This generated a set of predictions representing the model's current, untrained belief about the next token in the sequence. To teach the model, we must establish a rigorous metric that quantifies exactly how incorrect these beliefs are. This metric is the loss function, the single scalar value that the entire neural network is designed to minimize.

## The Geometry of Truth

To measure the error of our predictions, we first need to define what a perfect prediction looks like. When we feed the model the token `<BOS>`, the actual next token in our sequence is `i`. We can represent this ground truth as a target probability distribution. 

If the model were omniscient, it would assign a probability of 1.0 to the token `i` and 0.0 to all other tokens. This perfectly certain distribution is identical to the one-hot vectors we used to construct our initial embedding matrix. For each time step, our target is simply the one-hot representation of the correct next token. 

Our predicted distribution for the first step, however, looks very different. It is a near-uniform spread of probabilities across all twelve vocabulary words. The loss function must calculate the mathematical distance between our predicted, flat distribution and the sharp, one-hot target distribution.

## Why Cross-Entropy

A naive approach to calculating this distance might be to take the squared difference between the predicted probabilities and the target probabilities, similar to calculating Euclidean distance. While Mean Squared Error works well for continuous regression tasks, it behaves poorly for classification probabilities. When a model is confidently wrong, the gradients of Mean Squared Error shrink, slowing down the learning process precisely when it needs to make the largest corrections.

Instead, we use Cross-Entropy Loss. For a single prediction, Cross-Entropy Loss evaluates the predicted probability assigned exclusively to the correct target class. It ignores the probabilities assigned to the incorrect classes, provided the target is a pure one-hot vector.

The function is defined as the negative natural logarithm of the predicted probability of the target token:

$$
\text{Loss} = -\log(P_{\text{target}})
$$

The natural logarithm exhibits ideal properties for measuring probabilistic error. If the model predicts the correct token with a probability of 1.0, the logarithm of 1.0 is 0, resulting in zero loss. As the predicted probability approaches 0, the logarithm approaches negative infinity, resulting in an infinitely large positive loss. This asymmetric penalty heavily punishes the model for assigning very low probabilities to the true target, forcing it to aggressively adjust its weights. Furthermore, the logarithm translates the multiplication of probabilities into addition, which simplifies our calculus during backpropagation.

## Calculating the Sequence Loss

Our sequence `<BOS> i woke up` requires the model to make four distinct predictions simultaneously. We process the targets across the time steps: `i` for index 3, `woke` for index 5, `up` for index 7, and `late` for index 8.

At each step, we look up the predicted probability from the Softmax matrix we calculated in the previous part, and then we take the negative logarithm.

**Time Step 0**
The input is `<BOS>` and the target is `i`. The predicted probability for `i` is 0.0843.
$$
\text{Loss}_0 = -\log(0.0843) = 2.4734
$$

**Time Step 1**
The input is `i` and the target is `woke`. The predicted probability for `woke` is 0.0831.
$$
\text{Loss}_1 = -\log(0.0831) = 2.4877
$$

**Time Step 2**
The input is `woke` and the target is `up`. The predicted probability for `up` is 0.0833.
$$
\text{Loss}_2 = -\log(0.0833) = 2.4853
$$

**Time Step 3**
The input is `up` and the target is `late`. The predicted probability for `late` is 0.0833.
$$
\text{Loss}_3 = -\log(0.0833) = 2.4853
$$

To compute the final loss for the entire sequence, we calculate the arithmetic mean of the individual losses across all time steps. 

$$
\text{Total Loss} = \frac{2.4734 + 2.4877 + 2.4853 + 2.4853}{4} = 2.4829
$$

## The Untrained Baseline

Our final calculated loss is 2.4829. This specific value is highly informative. For a completely untrained model, the weights act as random noise, causing the Softmax function to distribute probability relatively evenly across the entire vocabulary. 

With a vocabulary size $V$ of 12, a uniform distribution assigns a probability of $\frac{1}{12}$ to every token. The theoretical Cross-Entropy Loss for a uniform distribution is $-\log(\frac{1}{12})$, which evaluates to approximately 2.4849. Our calculated loss of 2.4829 is nearly identical to this theoretical baseline. This confirms our forward pass is functioning correctly and clearly demonstrates the model's initial state of total uncertainty.

We have now reached the end of the forward pass. We possess a single scalar value that quantifies the error of our entire network. In our next installment, we will begin the backward pass, calculating the derivative of this loss to uncover an elegantly simple mathematical cancellation that drives the learning process.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/transformer_ebook_final.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
