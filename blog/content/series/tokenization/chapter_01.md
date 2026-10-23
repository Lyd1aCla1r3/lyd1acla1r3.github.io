# Part 1: Characters, Words, and the Subword Compromise


<style>
  /* Removed font size constraint */
  .trace-container td {
    white-space: nowrap !important;
  }
  .trace-container b code {
    font-weight: 900 !important;
    color: #9a5b65 !important;
    background-color: #fdf5f6 !important;
    border: 1px solid #e0c6cb !important;
    border-radius: 0.4em !important;
  }
  @media (prefers-color-scheme: dark) {
    .trace-container b code {
      color: #e6b3bc !important;
      background-color: #3b2a2d !important;
      border: 1px solid #6b4d53 !important;
      border-radius: 0.4em !important;
    }
  }
</style>

<!-- SUMMARY: The translation of raw text into a sequence of integer IDs requires defining a finite vocabulary space. Analyzing word-level and character-level boundaries reveals an inherent mathematical tradeoff between infinite vocabulary expansion and the destruction of semantic meaning, mandating a subword compression algorithm. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The preceding introduction established that neural networks cannot execute mathematical operations on raw text directly. Raw text strings must first map into continuous, $d_{\text{model}}$-dimensional vectors, where every dimension encodes a distinct semantic feature of the string. Each recognized string receives a deterministic, discrete integer ID that indexes its corresponding semantic vector in the embedding matrix $W_E$. This lookup function necessitates a predefined vocabulary: a finite inventory of recognized textual elements.

The structural definition of these elements dictates two fundamental properties of the neural network. First, the size of this vocabulary defines the strict memory constraints of the model, as every recognized element requires a dedicated vector in memory. Second, the boundaries of these elements define the semantic capabilities of the architecture, as the model can only learn concepts that are cleanly isolated by its vocabulary.

## The Word-Level Explosion

Defining the vocabulary space around natural word boundaries presents an intuitive starting point. Under this paradigm, every distinct word in a corpus receives a unique integer ID.

A minimal toy corpus demonstrates the initial viability of this approach. Applying strict word-level boundaries produces a nine-element vocabulary:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<span style="font-size: 0.9em;"><b><code>waking</code></b> <b><code>woke</code></b> <b><code>woken</code></b> <b><code>walking</code></b> <b><code>walked</code></b> <b><code>walker</code></b> <b><code>talking</code></b> <b><code>talked</code></b> <b><code>talker</code></b></span>
</div>


The structural flaw emerges immediately when scaling this strategy to a realistic production corpus. A modern language contains hundreds of thousands of base words. Adding grammatical permutations, prefixes, suffixes, punctuation combinations, and typographical errors results in unbounded expansion.

Every unique token requires a dedicated row in the architecture's embedding matrix $W_E$, where each scalar entry $w_{i,j}$ stores the learned weight for vocabulary row $i \in \{1, \dots, V\}$ at feature dimension $j \in \{1, \dots, d_{\text{model}}\}$. A vocabulary of one million distinct words mandates an embedding matrix with one million rows:

$$
W_E = \begin{bmatrix}
w_{1,1} & w_{1,2} & \dots & w_{1,d_{\text{model}}} \\
w_{2,1} & w_{2,2} & \dots & w_{2,d_{\text{model}}} \\
\vdots & \vdots & \ddots & \vdots \\
w_{V,1} & w_{V,2} & \dots & w_{V,d_{\text{model}}}
\end{bmatrix}_{V \times d_{\text{model}}}
$$

An architecture with a vocabulary size $V$ of $1,000,000$ and a model dimensionality $d_{\text{model}}$ of $4,096$ contains $4.096 \times 10^9$ embedding parameters. Storing this single matrix in 32-bit floating-point precision (4 bytes per parameter) requires $16.384\text{ GB}$ of memory solely to hold initial token representations. The parameter count scales linearly with $V$, rendering unconstrained word-level vocabularies computationally intractable. Word-level tokenization also treats `walk` and `walking` as orthogonal indices. This rigid separation discards the morphological relationship shared between the two strings, forcing gradient optimization to encode the underlying geometry of the action twice in unrelated rows.

## The Character-Level Destruction

Addressing the dimensionality explosion requires constraining the vocabulary size. The opposite extreme of the tokenization spectrum defines the vocabulary around individual characters.

Applying character-level boundaries to the toy corpus decomposes the text into a compact vocabulary of thirteen distinct elements, including a designated end-of-word marker `</w>`:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>a</code> <code>d</code> <code>e</code> <code>g</code> <code>i</code> <code>k</code> <code>l</code> <code>n</code> <code>o</code> <code>r</code> <code>t</code> <code>w</code> <code>&lt;/w&gt;</code>
</div>


This approach completely resolves the memory explosion problem. The embedding matrix shrinks to a negligible size.

The catastrophic failure of this method lies in the semantic destruction of the sequence. Individual characters carry zero inherent meaning. The sequence `t`, `a`, `l`, `k` forces the neural network to expend significant computational depth merely to reconstruct the basic semantic unit of conversation. 

The sequence length also expands drastically. The self-attention mechanism within a Transformer scales quadratically with sequence length $L$, requiring every token to compare itself against every other token in the sequence. Decomposing a single six-character word into six individual tokens increases the pairwise attention cost for that word by a factor of thirty-six ($6^2$). A short paragraph of text expands into an overwhelmingly long sequence of isolated characters, paralyzing the architecture's ability to process long-range context efficiently.

## The Subword Compromise

Resolving the tension between parameter memory and sequence length requires an intermediate granularity that decomposes rare words into reusable morphemes while preserving frequent words as intact tokens:

| Granularity | Toy Vocabulary | Production Scale | Embedding Memory | Sequence & OOV Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Word-Level** | 9 whole words | Unbounded (> 1,000,000) | Extreme (16.384 GB at FP32) | Shortest sequences; fails on unseen words and splits shared stems like `walk` and `walking` |
| **Character-Level** | 13 symbols (with `</w>`) | Minimal (13 to 256) | Negligible (< 5 MB) | Zero OOV errors, but expands sequence length 5x to 7x and inflates quadratic attention cost |
| **Subword (BPE)** | 27 tokens (14 merges) | Bounded (32,000 to 128,000) | Balanced (0.5 GB to 2 GB) | Zero OOV errors; keeps frequent words intact while isolating shared suffixes (`ing`, `ed`, `er`) |

Decomposing rare and complex words into reusable subword units strictly bounds the overall vocabulary size $V$, preserving memory efficiency. An encounter with an unfamiliar compound word does not require memorizing a dedicated vector; the architecture instead constructs the representation from common, pre-learned subword pieces. Preserving frequent words as single tokens simultaneously minimizes the overall sequence length $L$, protecting the attention mechanism from quadratic scaling. A common word remains a single token rather than ten isolated characters, sharply reducing the computational cost of the attention calculation.

Applying a hypothetical subword algorithm to the toy corpus reveals morphological structures hidden across different verb families. The prefixes `walk` and `talk` might remain whole, while common suffixes like `ing` and `ed` separate into independent, reusable tokens.

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<b><code>walk</code></b> <b><code>talk</code></b> <b><code>ing</code></b> <b><code>ed</code></b> <b><code>er</code></b>
</div>


The embedding matrix row corresponding to `ing` captures the geometric representation of continuous action. The architecture effectively constructs composite representations for novel combinations by adding the learned vector for a stem to the learned vector for a suffix.

## The Mechanism of Merging

Achieving this ideal subword state requires a deterministic, data-driven mathematical process rather than a manual set of linguistic rules. Byte Pair Encoding accomplishes this through a systematic sequence of merge operations.

The algorithm initializes at the character level, assuming zero inherent lexical meaning. The training loop scans the corpus to identify the single most frequent adjacent pair of tokens and fuses those two discrete elements into a single new token. This merge operation increments the vocabulary size by one while simultaneously shrinking the encoded corpus length. Merging the adjacent character tokens `i` and `n` into the single token `in` adds one entry to the vocabulary while reducing the encoded representation of `walking` by one token. That reduction directly shortens the sequence length that the downstream attention mechanism must process.

This iterative process acts as a localized compression algorithm. The system continuously discovers the most frequent character patterns and binds them together, progressing from individual characters through morphological suffixes, root words, and common phrases.

The next chapter formalizes this training algorithm on the nine-word toy corpus. That derivation specifies the boundary initialization, adjacent-pair frequency counting, and lexicographical tie-breaking rules required to build a subword vocabulary step by step.

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
