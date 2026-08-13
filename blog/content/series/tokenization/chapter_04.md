# Part 4: Encoding and Decoding

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

<!-- SUMMARY: The deployment of a static vocabulary and ordered list of merge rules enables the rigorous tokenization of novel text. This process mathematically guarantees consistency with the training distribution while gracefully decomposing unseen words into familiar subword units. -->

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The 14-step training algorithm successfully halted by discovering a final 27-token vocabulary built upon the exact morphological patterns of the corpus. The resulting list of learned merge rules now stands as a static, ordered mapping protocol. Deploying this protocol to tokenize unseen text forms the critical next phase of the subword pipeline.

## The Ordered Merge Algorithm

The encoding process abandons the dynamic frequency counting that drove the training phase. The algorithm relies entirely instead on the exact sequence of merge operations acquired during training. These rules are applied to any incoming text strictly in the order they were learned. 

This sequential application constitutes a greedy, longest-match algorithm. Enforcing the original chronological order of merges guarantees that the resulting tokenization mathematically reflects the most dominant statistical patterns of the training data. The algorithm begins by splitting the incoming text into individual characters and appending the boundary marker `</w>`.

## Encoding the Known Distribution

The application of this static protocol to words from the original training distribution yields highly optimized subword representations. The encoding of the word `walked`, which exists in the original training corpus, demonstrates the systematic execution of these ordered rules.

<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Initial</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;"></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 1</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>a</code> + <code>l</code> &rarr; <code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 1)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 2</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>al</code></b> + <code>k</code> &rarr; <code>w</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 2)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 3</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alk</code></b> + <code>e</code> &rarr; <code>w</code> <b><code>alke</code></b> <code>d</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 3)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 4</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alke</code></b> + <code>d</code> &rarr; <code>w</code> <b><code>alked</code></b> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 8)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 5</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alked</code></b> + <code>&lt;/w&gt;</code> &rarr; <code>w</code> <b><code>alked&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 10)</td>
    </tr>
  </tbody>
</table>
</div>



The algorithm completely ignores rules 4, 5, 6, 7, and 9 as the necessary adjacent pairs do not exist in the current sequence. The word systematically collapses down to two final tokens: `w` and `alked</w>`. 

A similar execution dictates the encoding of `waking`, which is also present in the original training corpus.

<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Initial</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;"></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 1</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>g</code> + <code>&lt;/w&gt;</code> &rarr; <code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 4)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 2</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>i</code> + <code>n</code> &rarr; <code>w</code> <code>a</code> <code>k</code> <b><code>in</code></b> <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 5)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 3</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>in</code></b> + <b><code>g&lt;/w&gt;</code></b> &rarr; <code>w</code> <code>a</code> <code>k</code> <b><code>ing&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 6)</td>
    </tr>
  </tbody>
</table>
</div>



The training process naturally halted before discovering a sequence unifying `w`, `a`, and `k`, causing the final encoding to remain fractured across four distinct tokens: `w`, `a`, `k`, and `ing</w>`.

## Subword Generalization on Novel Text

The true power of the Byte Pair Encoding algorithm emerges when encountering text wholly absent from the training corpus. The system leverages familiar morphological patterns to parse unseen words without suffering an out-of-vocabulary collapse.

Processing the novel word `stalking`, which does not exist in the training corpus, demonstrates this exact mechanism. The algorithm processes the string using the identical static rule sequence.

<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Initial</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>s</code> <code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;"></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 1</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>a</code> + <code>l</code> &rarr; <code>s</code> <code>t</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 1)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 2</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>al</code></b> + <code>k</code> &rarr; <code>s</code> <code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 2)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 3</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>g</code> + <code>&lt;/w&gt;</code> &rarr; <code>s</code> <code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 4)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 4</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>i</code> + <code>n</code> &rarr; <code>s</code> <code>t</code> <b><code>alk</code></b> <b><code>in</code></b> <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 5)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 5</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>in</code></b> + <b><code>g&lt;/w&gt;</code></b> &rarr; <code>s</code> <code>t</code> <b><code>alk</code></b> <b><code>ing&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 6)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 6</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alk</code></b> + <b><code>ing&lt;/w&gt;</code></b> &rarr; <code>s</code> <code>t</code> <b><code>alking&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 7)</td>
    </tr>
  </tbody>
</table>
</div>



The algorithm isolates the unknown prefix `s` and `t` at the fundamental character level, while assembling the highly frequent suffix `alking</w>` learned from the training data. The resulting three-token sequence `s`, `t`, and `alking</w>` requires no new mathematical components.

The novel word `awoke`, similarly absent from the original corpus, undergoes an identical decomposition.

<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Initial</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>a</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;"></td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 1</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>k</code> + <code>e</code> &rarr; <code>a</code> <code>w</code> <code>o</code> <b><code>ke</code></b> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 12)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 2</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>o</code> + <b><code>ke</code></b> &rarr; <code>a</code> <code>w</code> <b><code>oke</code></b> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 13)</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 3</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>w</code> + <b><code>oke</code></b> &rarr; <code>a</code> <b><code>woke</code></b> <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">(Rule 14)</td>
    </tr>
  </tbody>
</table>
</div>



The algorithm discovers the familiar sequence `woke`, leaving the independent prefix `a` and the final boundary marker `</w>` as separate units.

## The Triviality of Decoding

Reversing this process to recover raw text from a token sequence requires no complex algorithms or stored rules. Decoding acts as a pure concatenation operation. The system simply joins the sequence of string tokens together and transforms the `</w>` boundary markers back into standard spaces. This trivial inverse guarantees that the original text is recovered with perfect fidelity.

The tokenization pipeline is now mathematically complete, reliably transforming variable text into discrete integer sequences. This system remains bound to an arbitrary initial character set, however. If the encoder encounters a string containing any symbol absent from the original 13 base characters, such as a capital letter or punctuation, the entire process fails. The underlying dictionary possesses no mathematical representation for the unknown input, triggering a catastrophic out-of-vocabulary error. The subsequent section abandons this limitation entirely, examining how modern production systems drive Byte Pair Encoding down to the raw byte level to achieve true universal text encoding.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
