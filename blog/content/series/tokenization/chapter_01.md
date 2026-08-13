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

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The preceding introduction established that neural networks cannot perform mathematical operations on text directly. Instead, these initial raw text strings need to be translated into continuous, $n$-dimensional vectors, where every dimension represents a distinct semantic feature of the string. The strings receive a randomly assigned, discrete integer ID that allows the architecture to look up the corresponding semantic vector in the embedding matrix. This mapping function necessitates a predefined vocabulary: a finite list of recognized textual elements.

The structural definition of these elements dictates two fundamental properties of the neural network. First, the size of this vocabulary defines the strict memory constraints of the model, as every recognized element requires a dedicated vector in memory. Second, the boundaries of these elements define the semantic capabilities of the architecture, as the model can only learn concepts that are cleanly isolated by its vocabulary.

## The Word-Level Explosion

Defining the vocabulary space around natural word boundaries presents an intuitive starting point. Under this paradigm, every distinct word in a corpus receives a unique integer ID.

A minimal toy corpus demonstrates the initial viability of this approach. Applying strict word-level boundaries produces a nine-element vocabulary:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<span style="font-size: 0.9em;"><b><code>waking</code></b> <b><code>woke</code></b> <b><code>woken</code></b> <b><code>walking</code></b> <b><code>walked</code></b> <b><code>walker</code></b> <b><code>talking</code></b> <b><code>talked</code></b> <b><code>talker</code></b></span>
</div>


The structural flaw emerges immediately when scaling this strategy to a realistic production corpus. A modern language contains hundreds of thousands of base words. Adding grammatical permutations, prefixes, suffixes, punctuation combinations, and typographical errors results in unbounded expansion.

Every unique token requires a dedicated row in the architecture's embedding matrix. A vocabulary of one million distinct words mandates an embedding matrix with one million rows.

$$
W_E = \begin{bmatrix}
w_{1,1} & w_{1,2} & \dots & w_{1,d_{model}} \\
w_{2,1} & w_{2,2} & \dots & w_{2,d_{model}} \\
\vdots & \vdots & \ddots & \vdots \\
w_{V,1} & w_{V,2} & \dots & w_{V,d_{model}}
\end{bmatrix}_{V \times d_{model}}
$$

If an architecture defines a vocabulary size $V$ of 1,000,000 and a dimensionality $d_{model}$ of 4096, this single matrix requires over sixteen gigabytes of memory purely to store initial representations. The parameter count explodes proportionally, rendering the system computationally intractable. Furthermore, word-level tokenization treats `walk` and `walking` as completely orthogonal dimensions. This rigid separation discards the obvious morphological relationship shared between the two strings, forcing the optimization process to encode the fundamental geometry of the action twice in unrelated vectors.

## The Character-Level Destruction

Addressing the dimensionality explosion requires constraining the vocabulary size. The opposite extreme of the tokenization spectrum defines the vocabulary around individual characters.

Applying character-level boundaries to the toy corpus decomposes the text into a tiny, highly constrained vocabulary of thirteen distinct elements, including a designated end-of-word marker `</w>`:

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>a</code> <code>d</code> <code>e</code> <code>g</code> <code>i</code> <code>k</code> <code>l</code> <code>n</code> <code>o</code> <code>r</code> <code>t</code> <code>w</code> <code>&lt;/w&gt;</code>
</div>


This approach completely resolves the memory explosion problem. The embedding matrix shrinks to a negligible size.

The catastrophic failure of this method lies in the semantic destruction of the sequence. Individual characters carry zero inherent meaning. The sequence `t`, `a`, `l`, `k` forces the neural network to expend significant computational depth merely to reconstruct the basic semantic unit of conversation. 

The sequence length also expands drastically. The core attention mechanism within a Transformer scales quadratically, requiring every token to mathematically compare itself against every other token in the sequence. If a single word decomposes into six individual characters, the computational cost for that word increases by a factor of thirty-six. A simple paragraph of text transforms into an overwhelmingly long sequence of isolated characters, completely paralyzing the architecture's ability to process long-range context efficiently.

## The Subword Compromise

Word-level boundaries provide semantic richness at the cost of infinite parameter expansion. Character-level boundaries provide extreme memory efficiency at the cost of semantic destruction and quadratic sequence scaling.

Resolving this tension requires a middle ground that balances vocabulary size against sequence length. A subword tokenization algorithm decomposes rare words into smaller, logical pieces while preserving common words as intact units. This approach achieves the necessary mathematical compromise. 

Decomposing rare and complex words into reusable subword units strictly bounds the overall vocabulary size, preserving memory efficiency. If the architecture encounters an extremely rare word, it does not need to memorize a completely new vector. Instead, it constructs the meaning using common, pre-learned subword pieces it already knows. Simultaneously, preserving common words as single tokens minimizes the overall sequence length, protecting the attention mechanism from quadratic explosion. A common word remains a single token rather than ten isolated characters, drastically reducing the computational penalty during the attention calculation.

Applying a hypothetical subword algorithm to the toy corpus reveals morphological structures hidden across different verb families. The prefixes `walk` and `talk` might remain whole, while common suffixes like `ing` and `ed` separate into independent, reusable tokens.

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<b><code>walk</code></b> <b><code>talk</code></b> <b><code>ing</code></b> <b><code>ed</code></b> <b><code>er</code></b>
</div>


The embedding matrix row corresponding to `ing` captures the geometric representation of continuous action. The architecture effectively constructs composite representations for novel combinations by adding the learned vector for a stem to the learned vector for a suffix.

## The Mechanism of Merging

Achieving this ideal subword state requires a deterministic, data-driven mathematical process rather than a manual set of linguistic rules. Byte Pair Encoding accomplishes this through a systematic sequence of merge operations.

The algorithm initializes at the absolute character level, assuming zero inherent semantic meaning. The system then scans the training corpus to identify the single most frequent adjacent pair of tokens. Upon identifying this highest-frequency pair, the algorithm fuses the two discrete elements into a single, new token. This operation increments the vocabulary size by one while simultaneously shrinking the overall length of the encoded sequence. For example, merging the individual character tokens `i` and `n` into the single token `in` adds a term to the vocabulary but reduces the representation of the word 'walking' by one token, decreasing the overall sequence length the attention mechanism must process.

This iterative process acts as a localized compression algorithm. The system continuously discovers the most common patterns and binds them together, moving steadily from individual characters up through logical suffixes, full words, and eventually common phrases.

The subsequent article formalizes this training algorithm in detail, as applied to the toy vocabulary, rigorously defining the exact frequency counting and merging rules required to initialize the character-level vocabulary and execute these merges step by step until the final subword token set is completed.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
