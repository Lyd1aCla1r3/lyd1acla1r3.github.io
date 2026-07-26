# Part 16: Deepening the Representation: MLP and Residuals in Layer 2
<!-- SUMMARY: Integrate the Layer 2 attention updates into the Residual Stream and stabilize the geometry using Layer Normalization. The normalized vectors then flow into a Multi-Layer Perceptron acting as a deep contextual memory bank, enabling the injection of learned knowledge into the sequence representation. -->

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>

We have arrived at the final stages of the forward pass for our second Transformer layer. In the previous installment, we computed the attention probabilities and combined them with the Value matrix to create contextualized updates. Now, we must integrate these updates into the central nervous system of our model: the Residual Stream, and pass them through the final Multi-Layer Perceptron (MLP) memory bank.

## The First Residual Connection

Recall that the Residual Stream acts as the central information highway of the Transformer architecture. The attention mechanism does not replace the representations in the stream; it computes an update to be added to them. We take the output of our Layer 2 attention block and add it point-wise to the vectors that entered Layer 2 (which were the outputs of Layer 1).

$$
\text{Residual}_1 = \text{Stream}_{\text{in}} + \text{Attention}_{\text{out}}
$$

This addition allows the model to preserve all previous contextual information while overlaying the new insights gained from Layer 2's attention heads. For our sequence `<BOS> i woke up`, the representation for "woke" now fundamentally intertwines with "up", deeply embedding the semantic concept of "waking up" rather than just the individual words.

Using our toy example math, the first residual output is:

$$
\text{Residual}_1 = \begin{bmatrix}
   0.15 & -0.30 &  0.45 & -0.60 &  0.75 & -0.90 \\
  -0.15 &  0.30 & -0.45 &  0.60 & -0.75 &  0.90 \\
   0.75 &  0.75 &  0.75 & -0.75 & -0.75 & -0.75 \\
  -0.75 & -0.75 & -0.75 &  0.75 &  0.75 &  0.75
\end{bmatrix}
$$

## Layer Normalization

Following the addition, we stabilize the vectors using Layer Normalization. As we explored in Phase 3, this step recenters and scales the vectors so that their mean is zero and their variance is one. 

$$
\text{Norm}_1 = \text{LayerNorm}(\text{Residual}_1)
$$

This normalization guarantees that the subsequent MLP block receives inputs that are geometrically well-behaved, preventing any single feature from disproportionately dominating the activations.

## The MLP: A Deep Contextual Memory

The normalized vectors now flow into Layer 2's Multi-Layer Perceptron. While the attention mechanism moves information *between* tokens, the MLP processes information *within* each token. We can think of this MLP as a sophisticated Key-Value memory bank, just like we did in Layer 1, but now operating on highly abstract, contextualized representations.

### The Key Expansion

The first linear transformation ($W_1$) projects our vectors into a higher-dimensional space ($d_{ff}$). In our toy model, we expand from $d_{model} = 6$ to $d_{ff} = 24$. This projection acts as a set of "Keys," checking if specific complex patterns exist within the token's representation.

$$
\text{Hidden} = \text{ReLU}(\text{Norm}_1 W_1 + b_1)
$$

The ReLU activation function serves as the firing threshold. If a pattern is detected, for instance if the vector now strongly represents the combined "woke up" concept, the corresponding neurons fire. If not, they remain silent (zero).

### The Value Contraction

The active neurons then trigger the second linear transformation ($W_2$), which acts as the "Values." This step projects the data back down to our original $d_{model}$ dimension of 6.

$$
\text{MLP}_{\text{out}} = \text{Hidden} W_2 + b_2
$$

When a specific neuron fires in the hidden layer, it causes $W_2$ to write a corresponding conceptual vector into the output. This allows the MLP to inject learned knowledge about the world into our representations. Our simulated output yields:

$$
\text{MLP}_{\text{out}} = \begin{bmatrix}
   0.03 &  0.02 &  0.04 &  0.02 &  0.05 &  0.02 \\
   0.02 &  0.03 &  0.02 &  0.04 &  0.02 &  0.05 \\
   0.04 &  0.04 &  0.04 &  0.02 &  0.02 &  0.02 \\
   0.02 &  0.02 &  0.02 &  0.04 &  0.04 &  0.04
\end{bmatrix}
$$

## The Final Integration

Finally, we add the output of the MLP back into the Residual Stream to form the definitive output of Layer 2.

$$
\text{Output}_{\text{Layer 2}} = \text{Residual}_1 + \text{MLP}_{\text{out}}
$$

Our sequence representation has now evolved significantly:

$$
\text{Output}_{\text{Layer 2}} = \begin{bmatrix}
   0.18 & -0.28 &  0.49 & -0.58 &  0.80 & -0.88 \\
  -0.13 &  0.33 & -0.43 &  0.64 & -0.73 &  0.95 \\
   0.79 &  0.79 &  0.79 & -0.73 & -0.73 & -0.73 \\
  -0.73 & -0.73 & -0.73 &  0.79 &  0.79 &  0.79
\end{bmatrix}
$$

Our initial embeddings have now been transformed twice by attention and twice by MLPs. The vectors residing in the Residual Stream are profoundly rich. They no longer represent mere words; they represent complex syntactic roles, semantic meanings, and contextual relationships tailored precisely to our specific sequence. In the next phase, we will map these final representations back into our vocabulary space to predict the next word.

<p><em>Prefer to read this seamlessly offline? <a href="../assets/docs/transformers-ebook-v1.0.pdf">Download the complete, formatting-optimized 100-page Transformer Ebook here.</a></em></p>
