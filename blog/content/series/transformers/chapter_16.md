# Part 16: Deepening the Representation: MLP and Residuals in Layer 2

<!-- SUMMARY: The second layer attention updates are integrated into the residual stream and geometrically stabilized using layer normalization. The normalized vectors then flow into a multi-layer perceptron acting as a deep contextual memory bank, enabling the injection of learned knowledge into the sequence representation. -->

The forward pass for the second Transformer layer reaches its final stages after the attention probabilities are computed and combined with the Value matrix to create contextualized updates. The calculation of self-attention concludes by taking the dot products of the Queries and Keys, masking the results to maintain sequence causality, and applying the Softmax function. These normalized attention probabilities weight the Value matrix to extract the deeply contextualized features identified by the attention heads. A final projection matrix mixes these independent insights back into the primary model dimension. The resulting matrix represents the complete output of the second layer attention block. These updates must now be integrated into the central nervous system of the model, which is the residual stream, and passed through the final multilayer perceptron memory bank.

$$
\text{Layer 2 Attention Output} = \begin{bmatrix}
  0.05 & -0.10 &  0.15 & -0.20 &  0.25 & -0.30 \\
 -0.05 &  0.10 & -0.15 &  0.20 & -0.25 &  0.30 \\
  0.25 &  0.25 &  0.25 & -0.25 & -0.25 & -0.25 \\
 -0.25 & -0.25 & -0.25 &  0.25 &  0.25 &  0.25
\end{bmatrix}
$$

## The First Residual Connection

The residual stream acts as the central information highway of the Transformer architecture, bypassing the attention block entirely. The attention mechanism does not replace the representations in the stream; it computes an update to be added to them. The output of the first layer flows directly forward and acts as the foundational state.

$$
\text{Layer 1 Final Output} = \begin{bmatrix}
  0.10 & -0.20 &  0.30 & -0.40 &  0.50 & -0.60 \\
 -0.10 &  0.20 & -0.30 &  0.40 & -0.50 &  0.60 \\
  0.50 &  0.50 &  0.50 & -0.50 & -0.50 & -0.50 \\
 -0.50 & -0.50 & -0.50 &  0.50 &  0.50 &  0.50
\end{bmatrix}
$$

The network adds the newly computed attention output directly to this pristine first layer output point-wise. This addition operation writes the latest structural discoveries into the shared memory bus without erasing the fundamental syntactic properties established earlier in the network. The addition allows the model to preserve all previous contextual information while overlaying the new insights gained from the attention heads of the second layer.

$$
\text{Residual}_1 = \text{Stream}_{\text{in}} + \text{Attention}_{\text{out}}
$$

For a sequence containing the words "woke" and "up", the representation for the word "woke" now fundamentally intertwines with the word "up", deeply embedding the semantic concept of waking up rather than just the individual words. Using the established mathematical values, the first residual output is calculated as follows.

$$
\text{After First Residual} = \begin{bmatrix}
  0.15 & -0.30 &  0.45 & -0.60 &  0.75 & -0.90 \\
 -0.15 &  0.30 & -0.45 &  0.60 & -0.75 &  0.90 \\
  0.75 &  0.75 &  0.75 & -0.75 & -0.75 & -0.75 \\
 -0.75 & -0.75 & -0.75 &  0.75 &  0.75 &  0.75
\end{bmatrix}
$$

## Layer Normalization

Following the addition step, the vectors undergo layer normalization to stabilize their variance. This step recenters and scales the vectors so that their mean is zero and their variance is one.

$$
\text{Norm}_1 = \text{LayerNorm}(\text{Residual}_1)
$$

This normalization guarantees that the subsequent multilayer perceptron block receives inputs that are geometrically well-behaved, preventing any single feature from disproportionately dominating the activations.

## The Multilayer Perceptron: A Deep Contextual Memory

The normalized vectors now flow into the second layer's multilayer perceptron. While the attention mechanism moves information between tokens, the multilayer perceptron processes information within each token. This block functions as a sophisticated key-value memory bank, similar to the first layer, but now operating on highly abstract and contextualized representations. For the purpose of mathematical clarity in this conceptual stage, the second layer operations are represented within a condensed constant dimensional space. The network projects the normalized vectors through a dense linear layer, applies the Rectified Linear Unit activation function, and projects the results back out. This final feature extraction isolates the most abstract token representations.

### The Key Expansion

The first linear transformation, denoted as $W_1$, projects the vectors into a higher-dimensional space. In the toy model, the dimension expands from 6 to 24. This projection acts as a set of keys checking if specific complex patterns exist within the token representations.

$$
\text{Hidden} = \text{ReLU}(\text{Norm}_1 W_1 + b_1)
$$

The Rectified Linear Unit activation function serves as the firing threshold. If a pattern is detected, for instance if the vector now strongly represents the combined waking up concept, the corresponding neurons fire. If not, they remain silent with a value of zero.

### The Value Contraction

The active neurons then trigger the second linear transformation, denoted as $W_2$, which acts as the values. This step projects the data back down to the original model dimension.

$$
\text{MLP}_{\text{out}} = \text{Hidden} W_2 + b_2
$$

When a specific neuron fires in the hidden layer, it causes the second weight matrix to write a corresponding conceptual vector into the output. This allows the network to inject learned knowledge about the world into the sequence representations. The simulated output yields the following highly refined semantic combinations.

$$
\text{Layer 2 MLP Output} = \begin{bmatrix}
  0.03 &  0.02 &  0.04 &  0.02 &  0.05 &  0.02 \\
  0.02 &  0.03 &  0.02 &  0.04 &  0.02 &  0.05 \\
  0.04 &  0.04 &  0.04 &  0.02 &  0.02 &  0.02 \\
  0.02 &  0.02 &  0.02 &  0.04 &  0.04 &  0.04
\end{bmatrix}
$$

## The Final Integration

The architecture concludes the second layer with one final residual connection. The output of the multilayer perceptron is added back to the main residual stream to form the definitive output of the second layer. This ensures the gradients flow unobstructed during backpropagation and guarantees the network retains all prior structural information.

$$
\text{Output}_{\text{Layer 2}} = \text{Residual}_1 + \text{MLP}_{\text{out}}
$$

The sequence representation has now evolved significantly.

$$
\text{Layer 2 Final Output} = \begin{bmatrix}
  0.18 & -0.28 &  0.49 & -0.58 &  0.80 & -0.88 \\
 -0.13 &  0.33 & -0.43 &  0.64 & -0.73 &  0.95 \\
  0.79 &  0.79 &  0.79 & -0.73 & -0.73 & -0.73 \\
 -0.73 & -0.73 & -0.73 &  0.79 &  0.79 &  0.79
\end{bmatrix}
$$

The initial embeddings have now been transformed twice by attention blocks and twice by multilayer perceptrons. The vectors residing in the residual stream are profoundly rich. This matrix represents the culmination of the forward pass through the deep processing layers. The simple vocabulary IDs that entered the network have been transformed into complex geometric coordinates that encapsulate grammar, context, and abstract meaning tailored precisely to the specific sequence. The network is now fully prepared to map these internal representations back into the vocabulary space to generate the prediction for the next word.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
