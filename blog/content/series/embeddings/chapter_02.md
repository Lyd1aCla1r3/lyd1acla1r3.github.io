# Part 2: The Continuous Vector Space

<!-- SUMMARY: Projecting discrete tokens into a high-dimensional vector space provides the differentiable manifold required for gradient-based optimization. At initialization, these vectors are drawn from a random distribution, creating an isotropic expanse where all tokens are geometrically orthogonal and devoid of semantic relationships. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>

The linear projection of a one-hot vector through the embedding matrix $W_E$ alters the mathematical domain of the tokens, bridging the gap from a discrete categorical set ($\mathbb{Z}$) into a dense, continuous vector space ($\mathbb{R}^{d_{\text{model}}}$).

This domain transition is a structural prerequisite for deep learning.

## The Differentiable Manifold

Neural networks learn through calculus by computing partial derivatives and traversing a continuous loss landscape via backpropagation. Differential calculus requires a continuous manifold: a discrete integer ID admits no derivative, and a categorical label cannot absorb a microscopic numerical perturbation.

Projecting tokens into $\mathbb{R}^{d_{\text{model}}}$ parameterizes each vocabulary entry as a vector of floating-point coordinates. Scaling the hidden dimension from the 3-dimensional whiteboard model ($d_{\text{model}} = 3$) to a production dimensionality of $d_{\text{model}} = 512$ represents a token such as `brown` with 512 independent, tunable parameters:

$$
\mathbf{v}_{\text{brown}} = \begin{bmatrix} 0.124 & -0.841 & 0.339 & \dots & -0.052 \end{bmatrix} \in \mathbb{R}^{512}
$$

Continuous coordinates impose no discrete grid constraints on parameter updates. A single gradient descent step can apply an arbitrarily small perturbation to $\mathbf{v}_{\text{brown}}$ (such as subtracting $0.001$ from its first coordinate) to reduce the training loss incrementally. Repeated continuous perturbations allow the optimization process to translate statistical co-occurrence patterns into geometric proximity.

## The Isotropic Expanse

These initial 512 dimensions do not correspond to latent human concepts. At initialization, one dimension does not encode plurality while another encodes sentiment.

Model initialization populates the entries of $W_E$ by sampling independently from a zero-mean probability distribution, such as a Gaussian distribution $\mathcal{N}(0, \sigma^2)$ with mean $0$ and variance $\sigma^2$. Independent sampling from an identical symmetric distribution across all coordinates produces an **isotropic** vector space, meaning its statistical properties remain uniform in every direction.

High-dimensional geometry invalidates low-dimensional intuition about random point clouds. In a 512-dimensional space, a statistical phenomenon known as **concentration of measure** governs vector magnitudes. Computing the Euclidean length (norm) of a vector $\mathbf{v} \in \mathbb{R}^{d}$ requires summing its $d = 512$ squared coordinates and taking the square root:

$$
\|\mathbf{v}\| = \sqrt{\sum_{m=1}^{d} v_m^2}
$$

Summing 512 independent random variables invokes the Law of Large Numbers, causing the Euclidean norms of all randomly initialized token vectors to concentrate tightly around $\sqrt{d \cdot \sigma^2}$. Rather than forming an uneven solid cloud, random initialization places every token vector onto a thin spherical shell of radius $\sqrt{d}\sigma$, devoid of directional bias.

The exponential growth of volume across dimensions reinforces this isolation. A two-dimensional plane contains $2^2 = 4$ quadrants, so scattering a 50,000-token vocabulary across $\mathbb{R}^2$ forces thousands of tokens into the same quadrant.

A 512-dimensional space partitions into $2^{512}$ distinct sign regions, known mathematically as **orthants**. That exponent evaluates to $2^{512} \approx 1.34 \times 10^{154}$ orthants. Random sign assignment across 512 coordinates drops each initialized token into one of those $1.34 \times 10^{154}$ orthants, ensuring that every vocabulary entry begins in extreme spatial isolation with negligible probability of accidental clustering.

## The Geometry of Orthogonality

Within this isotropic expanse, a second high-dimensional invariant emerges: any two independently initialized token vectors (such as `brown` and `fox`) are nearly **orthogonal** (perpendicular) to one another.

Quantifying the directional alignment between two vectors $\mathbf{a}, \mathbf{b} \in \mathbb{R}^{d}$ requires computing their **cosine similarity**, defined as the cosine of the angle $\theta$ between them. The geometric dot product relates the two vectors through the identity $\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\| \|\mathbf{b}\| \cos(\theta)$, where $\|\mathbf{a}\|$ and $\|\mathbf{b}\|$ denote the Euclidean norms of $\mathbf{a}$ and $\mathbf{b}$. Dividing both sides by the product of the norms isolates $\cos(\theta)$:

$$
\cos(\theta) = \frac{\mathbf{a} \cdot \mathbf{b}}{\|\mathbf{a}\| \|\mathbf{b}\|} = \frac{\sum_{m=1}^{d} a_m b_m}{\|\mathbf{a}\| \|\mathbf{b}\|}
$$

This identity demonstrates that the cosine of the angle $\theta$ is directly proportional to the algebraic **dot product**: the sum of the element-wise products $a_m b_m$ across all $d$ coordinates.

Multiplying two coordinates $a_m$ and $b_m$ drawn independently from a symmetric distribution centered at zero produces a positive product when their signs match and a negative product with equal probability ($p = 0.5$) when their signs oppose.

In a 3-dimensional toy space ($d = 3$), the dot product sums only three random products. Small sample sizes exhibit high variance: all three terms share the same sign with probability $2 \times (0.5)^3 = 0.25$, producing wide fluctuations in $\cos(\theta)$ that frequently align random vectors in similar directions.

In a 512-dimensional space ($d = 512$), the dot product sums 512 independent zero-mean products. Law of Large Numbers convergence shrinks the relative variance of the normalized dot product at a rate of $1/\sqrt{d}$:

- **Sign Balance:** Expected sign symmetry yields roughly 256 positive products ($a_m b_m > 0$) and 256 negative products ($a_m b_m < 0$).
- **Magnitude Symmetry:** Symmetric sampling around zero ensures that the positive terms and negative terms share the same expected magnitude.
- **Mutual Cancellation:** Summing all 512 terms cancels the positive half against the negative half, driving the expected dot product $\mathbf{a} \cdot \mathbf{b}$ and the resulting cosine similarity $\cos(\theta)$ toward $0.0$ (with standard deviation $1/\sqrt{512} \approx 0.044$).

| Spatial Regime | Dimensionality (`d`) | Distinct Orthants (`2^d`) | Dot-Product Terms | Pairwise Cosine Similarity |
| :--- | :--- | :--- | :--- | :--- |
| **2D Plane** | `2` | `4` | `2` | High variance (`0.71` std dev); severe crowding |
| **3D Whiteboard Model** | `3` | `8` | `3` | Moderate variance (`0.58` std dev); frequent alignment |
| **Production Space** | `512` | `2^512` (`~1.34e154`) | `512` | Tight concentration near `0.0` (`0.044` std dev); near-orthogonal |

An angle whose cosine equals $0.0$ measures $90^\circ$. Every pair of randomly initialized tokens in a high-dimensional embedding matrix begins geometrically orthogonal to one another.

## A Feature, Not a Bug

Near-orthogonality at initialization provides a foundational structural advantage for gradient-based optimization.

Orthogonal vectors establish an unentangled coordinate baseline. Random initial clustering would force early training steps to expend gradient updates untangling spurious correlations between unrelated words. Initializing every token at roughly $90^\circ$ from every other token presents the optimizer with an uncorrelated geometric slate, allowing backpropagation to pull co-occurring tokens together and push unrelated tokens apart purely in response to corpus statistics.

The initialized embedding matrix $W_E$ thus begins as a nearly orthogonal set of points on a hypersphere, encoding neither semantic clusters nor grammatical hierarchy. Imposing linguistic structure onto this isotropic expanse requires evaluating predictions and updating the weights of $W_E$ through the forward and backward passes derived in the next three chapters.

<p><em>Prefer to read this offline? <a href="../assets/docs/embeddings-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Vector Embeddings Ebook here.</a></em></p>
