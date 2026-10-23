# Part 5: From Bytes to Billions
<!-- SUMMARY: Bridging the theoretical foundation of tokenization to production systems requires replacing arbitrary character sets with a universal byte-level fallback. Tracing the merge algorithm across raw byte integers demonstrates that morphological structure emerges without human-readable character sets, establishing the input dimensions required by the Transformer embedding matrix. -->

<style>
  .trace-container code, .trace-container table code {
    font-size: 0.65em !important;
    padding: 2px 4px !important;
    margin-right: 2px !important;
  }
  .trace-container td {
    white-space: nowrap !important;
  }
  .trace-container b code {
    font-weight: 900 !important;
    color: #9a5b65 !important; /* Dark Rose Gold */
    background-color: #fdf5f6 !important;
    border: 1px solid #e0c6cb !important;
    border-radius: 0.4em !important;
  }
  /* For dark mode if it exists */
  @media (prefers-color-scheme: dark) {
    .trace-container b code {
      color: #e6b3bc !important;
      background-color: #3b2a2d !important;
      border: 1px solid #6b4d53 !important;
      border-radius: 0.4em !important;
    }
  }
</style>

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The character-level encoding pipeline relies on a fragile assumption by limiting its initial base vocabulary to the characters observed in the training corpus. Encountering a novel symbol during inference, such as an emoji, a non-Latin script character, or an unobserved punctuation mark, drives the greedy longest-match algorithm into a dead end. The encoder cannot match the unknown character to any existing token ID, triggering an out-of-vocabulary failure state that halts processing.

## The Universal Byte-Level Foundation

Resolving this failure state requires replacing character vocabularies with raw binary units. Digital hardware stores data as bits representing binary states of `1` or `0`, and operating systems group those bits into standardized eight-bit blocks called *bytes*. An eight-bit byte spans $2^8 = 256$ distinct binary permutations, establishing a fixed integer range from `0` through `255`.

Every text symbol, regardless of script or complexity, serializes into a sequence of bytes under the UTF-8 standard. This encoding standard provides a finite, universal foundation for tokenization. Production tokenizers initialize their base vocabulary with the 256 raw byte values rather than an unpredictable inventory of human-readable characters.

A critical distinction governs how the algorithm interacts with these values. Byte Pair Encoding does not operate at the bit level and possesses no concept of the underlying ones and zeros. The algorithm treats each integer value from `[0]` to `[255]` as a single, indivisible atomic token.

### The ASCII Range and Beyond

Initializing the vocabulary with this 256-token foundation guarantees that every valid string can be encoded. Standard encoding tables exhibit a structural boundary at integer `[127]`, which corresponds to `7F` in hexadecimal. The first `128` integer values (`0` through `127`) represent the classic ASCII character set covering English letters, digits, and basic punctuation. Those `128` characters fit inside a single 8-bit byte, mapping the lowercase letter `w` to the single byte integer `119`.

The broader Unicode standard defines over one million symbols across global scripts. UTF-8 accommodates this scale while preserving backward compatibility with 1-byte ASCII systems by operating as a *variable-length* encoding. Characters outside the basic ASCII range serialize into sequences of two to four bytes: the accented character `é` maps to the two-byte sequence `[195, 169]`, and the rocket emoji 🚀 maps to the four-byte sequence `[240, 159, 154, 128]`.

The tokenizer itself never inspects raw binary bits. A host runtime such as Python first executes a standard `encode("utf-8")` call to translate an input string into an array of byte integers. Typing `é` produces the integer array `[195, 169]`, which the runtime passes directly to the tokenizer. Display rendering engines concatenate the underlying bits of that multi-byte sequence to draw a single glyph on screen, whereas the Byte Pair Encoding algorithm operates strictly on the discrete integer sequence.

### The Unicode Dimensionality Problem

The existence of over one million pre-assigned Unicode code points suggests an alternative design: initializing the base vocabulary directly with all 1.1 million Unicode characters and assigning merged combinations such as `[x]` + `[y]` &rarr; `[z]` to token IDs starting above `1,114,112`. Capping the base vocabulary at `[255]` and learning abstract entries from `[256]` onward is dictated by matrix parameter efficiency.

The embedding matrix of a Transformer allocates one row vector for every token in the vocabulary. Initializing the base vocabulary with all 1.1 million Unicode code points would instantiate more than one million embedding rows before a single subword merge occurred, dedicating billions of parameters to rare scripts and symbols that scarcely appear in the training distribution.

Capping the base vocabulary at the 256 raw bytes restricts the foundational embedding cost to 256 rows. This compact base allocation preserves the model parameter budget so the training algorithm can dedicate a 50,000-token vocabulary entirely to byte combinations that recur frequently in the training corpus.

Processing the UTF-8 array for `é` presents the tokenizer with the integer `[195]` followed by `[169]`. Those two byte values co-occur whenever `é` appears in the corpus, causing the BPE frequency tally to rank `[195, 169]` as a high-frequency pair and fuse it into a single abstract token ID (`[195]` + `[169]` &rarr; `[257]`). Scaling this byte-level merge loop across large datasets fuses multi-byte characters, morphological suffixes such as `i` `n` `g`, and whole words such as `t` `h` `e` into single token IDs within a compact, data-driven vocabulary.

### Decoding and the UTF-8 Guarantee

The restriction to abstract integers necessitates a dedicated text reconstruction protocol. Transforming the abstract token `[257]` back into the printable character `é` requires reversing the merge operations.

The tokenizer maintains a lookup table of every merge rule learned during training. During the decoding phase, when the neural network emits token `[257]`, the decoder references this table to invert the merge, expanding `[257]` back into its constituent byte pair `[195, 169]` and returning the raw byte array to the host language.

Reconstructing characters from a flat byte array requires an unambiguous framing rule to determine whether `[195, 169]` represents the single two-byte character `é` or two separate single-byte characters (`Ã` followed by `©`). The UTF-8 specification resolves this ambiguity by partitioning bytes into **Start Bytes** and **Continuation Bytes** using dedicated binary bit prefixes:

| Binary Bit Prefix | Byte Classification | Sequence Length | Framing Behavior |
| :--- | :--- | :--- | :--- |
| `0xxxxxxx` | **ASCII Byte** | 1 byte | Encodes a standalone 7-bit ASCII character (`0` to `127`) |
| `110xxxxx` | **2-Byte Start Byte** | 2 bytes | Opens a two-byte code point followed by one continuation byte |
| `1110xxxx` | **3-Byte Start Byte** | 3 bytes | Opens a three-byte code point followed by two continuation bytes |
| `11110xxx` | **4-Byte Start Byte** | 4 bytes | Opens a four-byte code point followed by three continuation bytes |
| `10xxxxxx` | **Continuation Byte** | Trailing byte | Carries payload bits immediately following a multi-byte start byte |

Every trailing byte inside a multi-byte character carries the `10` binary prefix. The integer `195` equals `11000011` in binary, marking a two-byte Start Byte, while `169` equals `10101001` in binary, marking a Continuation Byte. A UTF-8 text engine cannot misinterpret `[195, 169]` as two separate characters because a `10xxxxxx` continuation byte is syntactically invalid as a standalone character.

This prefix structure makes a UTF-8 byte stream self-synchronizing. A parser that indexes into the middle of a byte array and reads a `10xxxxxx` prefix immediately detects an interior continuation byte, scans backward to locate the governing Start Byte, and reads the declared number of bytes forward.

### The Genius of Partial Merges

The strict limitation of merging only adjacent pairs prevents the algorithm from compressing a 3-byte or 4-byte character in a single operation.

Encountering a 3-byte character, such as a Hindi Devanagari symbol represented by `[224]` `[164]` `[185]`, forces the tokenizer to merge the sequence iteratively. First, it will merge `[224]` + `[164]` into a new abstract token like `[350]`. Later, it will merge `[350]` + `[185]` into `[412]`.

Leaving a character partially merged as `[350]` and `[185]` poses zero risk of corrupting the text.

Tokens are never decoded in isolation. The neural network emits a sequence of token IDs, and the tokenizer expands the entire sequence into a contiguous byte array before invoking the UTF-8 decoder. Whether those bytes originated from one merged token or three separate tokens has no effect on decoding: the presence of `[224, 164, 185]` in the output stream directs the Start Byte (`224`, binary `11100000`) to consume all three bytes and render the Devanagari character.

Partial merges also provide a structural compression advantage across non-Latin scripts. The Unicode standard groups characters from the same writing system into contiguous code point blocks, causing most Hindi Devanagari characters to share the leading byte pair `[224, 164]`. Merging those first two bytes into a single token `[350]` establishes a shared script-prefix token. The model can then represent individual Devanagari characters as a two-token composition (`[Devanagari_Prefix]` + `[Terminal_Byte]`) without allocating thousands of separate whole-character entries.

## Re-Training the Toy Example in Bytes

To prove that the mechanical logic remains mathematically identical, the toy corpus is completely detached from human-readable characters and converted into raw integers.

A dedicated boundary token, `</w>`, marks the end of each word. The boundary marker `</w>` does not serialize into its literal four-character ASCII byte sequence (`<`, `/`, `w`, `>`). This marker functions as an abstract control token injected by the pre-tokenizer rather than literal text from the document. Production tokenizers prevent control-token collisions with raw text by assigning control tokens to integer IDs above the `0` through `255` byte range, reserving `[256]` for `</w>` and minting merged subword tokens starting at `[257]`.

<div class="trace-container">
<p>INITIAL CORPUS:</p>
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[110]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <code>[97]</code> <code>[108]</code> <code>[107]</code> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
  </tbody>
</table>

<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0;">Step 1 &nbsp;&nbsp;&nbsp;&nbsp; <code>a</code> + <code>l</code> &rarr; <b><code>al</code></b> &nbsp;&nbsp;&nbsp;&nbsp; <code>[97]</code> + <code>[108]</code> &rarr; <b><code>[257]</code></b></td>
    </tr>
  </tbody>
</table>
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[110]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[257]</code></b> <code>[107]</code> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
  </tbody>
</table>

<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0;">Step 2 &nbsp;&nbsp;&nbsp;&nbsp; <code>al</code> + <code>k</code> &rarr; <b><code>alk</code></b> &nbsp;&nbsp;&nbsp;&nbsp; <code>[257]</code> + <code>[107]</code> &rarr; <b><code>[258]</code></b></td>
    </tr>
  </tbody>
</table>
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[97]</code> <code>[107]</code> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <code>[111]</code> <code>[107]</code> <code>[101]</code> <code>[110]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[258]</code></b> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[258]</code></b> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>w</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[119]</code> <b><code>[258]</code></b> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[258]</code></b> <code>[105]</code> <code>[110]</code> <code>[103]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[258]</code></b> <code>[101]</code> <code>[100]</code> <code>[256]</code></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0;"><code>t</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0;"><code>[116]</code> <b><code>[258]</code></b> <code>[101]</code> <code>[114]</code> <code>[256]</code></td>
    </tr>
  </tbody>
</table>

<div style="text-align: center; margin: 2rem 0; font-size: 1.5rem; color: var(--text-muted);">&#8942;</div>
</div>

The byte-level training loop halts at the same 14-step boundary as the character-based model. The identical subword hierarchy emerges because the underlying pair-frequency counts remain invariant under integer relabeling. Operating on raw UTF-8 bytes preserves morphological discovery while eliminating out-of-vocabulary failures.

## The Embedding Matrix Connection

### Vocabulary Size and Sequence Scaling

Establishing a 256-byte foundation allows the training algorithm to scale across multi-gigabyte corpora. Production tokenizers such as SentencePiece and `tiktoken` execute this greedy pair-counting and merging loop tens of thousands of times across large training datasets.

The configured number of merge iterations determines the final vocabulary size, $V$. A small vocabulary leaves words fragmented into short subpieces, lengthening the token sequences that the quadratic self-attention mechanism must process. A larger vocabulary consolidates frequent words into single token IDs such as `[270]`, shortening sequence lengths while adding one embedding row per new token. Production language models balance sequence compression against embedding memory by targeting a vocabulary size $V$ between `32,000` and `100,000` tokens.

### Embedding Matrix Lookup Geometry

The vocabulary cardinality $V$ defines the input dimension of the Transformer network. The initial step of a Transformer forward pass maps each discrete token ID into a continuous vector space through the embedding matrix, denoted as $W_E$.

The embedding matrix $W_E$ functions as a parameterized coordinate lookup table containing one row vector for each of the $V$ tokens in the vocabulary. The width of each row matches the hidden state dimensionality of the model, $d_{\text{model}}$, locking the matrix dimensions to $V \times d_{\text{model}}$:

$$
W_E = \begin{bmatrix}
\text{Coordinate vector for token } [0] \\
\text{Coordinate vector for token } [1] \\
\text{Coordinate vector for token } [2] \\
\vdots \\
\text{Coordinate vector for token } [V-1]
\end{bmatrix}_{V \times d_{\text{model}}}
$$

Training a Byte Pair Encoding tokenizer to a vocabulary size of $V = 50,257$ tokens for a Transformer with hidden dimensionality $d_{\text{model}} = 768$ instantiates an embedding matrix with $50,257 \times 768 = 38,597,376$ learnable parameters.

This dimensional coupling completes the input transformation pipeline: raw text serializes into UTF-8 bytes, ordered BPE merge rules fuse frequent byte sequences into subword tokens, the vocabulary dictionary maps each token to an integer index, and that integer index selects the corresponding row vector from $W_E$. The companion [Embeddings series](series-embeddings.html) examines how gradient descent optimizes those continuous coordinate vectors to encode semantic relationships.

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
