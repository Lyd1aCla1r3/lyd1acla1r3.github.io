# Part 3: Training BPE by Hand


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

<!-- SUMMARY: Executing the Byte Pair Encoding algorithm against a concrete corpus reveals how abstract statistical rules collapse character-level data into optimized semantic units. Tracing the frequency counts and merge selections across a fourteen-step compression sequence demonstrates the deterministic derivation of morphological stems and suffixes without linguistic programming. -->

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The formal definition of the Byte Pair Encoding algorithm establishes a greedy, iterative mechanism for subword compression. Executing this mechanism against a concrete corpus demonstrates how these abstract rules operate in practice. The procedure relies entirely on statistical frequency rather than linguistic programming.

## The Initial State

The training process begins with the nine distinct inflected word forms defined in the preceding chapter. Each word splits into individual character tokens terminated by the `</w>` boundary marker. This initialized corpus state allows the algorithm to track discrete token sequences and their absolute frequencies across the text.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
</div>



## The First Merges: Deriving Roots

The algorithm evaluates the frequency of every adjacent token pair in this initial state. The pairs `a` + `l`, `k` + `e`, and `l` + `k` tie for the highest frequency with six occurrences each. Lexicographical sorting dictates the selection of `a` + `l` for the inaugural merge operation. The new token `al` is formally registered, and the corpus representation is updated globally.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 1</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>a</code> + <code>l</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>al</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">6 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
</div>



This merge operation immediately alters the subsequent frequency distribution. The second merge iteration tallies adjacent pairs across the updated corpus, where `al` + `k` and `k` + `e` tie for the highest frequency at six occurrences each. Lexicographical tie-breaking selects `al` + `k` as the next merge target.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 2</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>al</code></b> + <code>k</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alk</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">6 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
</div>



The merge operation fuses these tokens, creating the cohesive `alk` unit. The third merge iteration establishes that the pair `alk` + `e` occurs four times, binding the root verb to the start of its suffixes.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 3</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alk</code></b> + <code>e</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">4 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


Three merge iterations suffice for the counting mechanism to derive `alk`, the central morphological root shared by two-thirds of the corpus. This fragment serves as the structural foundation for *walking*, *walked*, *walker*, *talking*, *talked*, and *talker*, compressing the internal representation of the text.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alke</code></b> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alke</code></b> <code>r</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alke</code></b> <code>d</code> <code>&lt;/w&gt;</code><br>
<code>t</code> <b><code>alke</code></b> <code>r</code> <code>&lt;/w&gt;</code>
</div>



## Assembling Suffixes

The subsequent three merge iterations reveal how boundary markers influence the derivation of suffixes. Iteration four evaluates the updated sequences and identifies the highest frequency pair ending the gerund verbs.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 4</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>g</code> + <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">3 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


Iteration five targets the interior of the suffix, binding the preceding characters.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 5</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>i</code> + <code>n</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>in</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">3 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


Iteration six combines these two newly formed tokens.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 6</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>in</code></b> + <b><code>g&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>ing&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">3 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


This sequence formally registers the morphological `-ing` suffix into the subword vocabulary. The token boundary marker `</w>` guarantees that this newly minted token `ing</w>` specifically represents the suffix at the end of a word, preventing it from incorrectly matching the substring "ing" in the middle of an unrelated word.

## Accelerated Convergence

The iterative compression rapidly integrates the remaining structure. The next five iterations bind the derived roots and suffixes into complete semantic units.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 7</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alk</code></b> + <b><code>ing&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alking&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 8</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alke</code></b> + <code>d</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alked</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 9</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alke</code></b> + <code>r</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alker</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 10</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alked</code></b> + <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alked&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 11</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><b><code>alker</code></b> + <code>&lt;/w&gt;</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>alker&lt;/w&gt;</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


The initial `alk` fragment transforms into three complete lexical structures: `alking</w>`, `alked</w>`, and `alker</w>`. The counting procedure then evaluates the remaining verb family.


<div class="trace-container">
<table style="width: 100%; border: none; margin-bottom: 2rem; border-collapse: collapse;">
  <tbody>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 12</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>k</code> + <code>e</code></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>ke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 13</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>o</code> + <b><code>ke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>oke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
    <tr>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">Step 14</td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;"><code>w</code> + <b><code>oke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: left;">&rarr; <b><code>woke</code></b></td>
      <td style="border: none; padding: 0.25rem 0; text-align: right;">2 occurrences</td>
    </tr>
  </tbody>
</table>
</div>


Fourteen merge operations transform the original sequences of isolated characters into consolidated subword fragments. The internal representation of the text achieves substantial sequence compression.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>w</code> <code>a</code> <code>k</code> <b><code>ing&lt;/w&gt;</code></b><br>
<b><code>woke</code></b> <code>&lt;/w&gt;</code><br>
<b><code>woke</code></b> <code>n</code> <code>&lt;/w&gt;</code><br>
<code>w</code> <b><code>alking&lt;/w&gt;</code></b><br>
<code>w</code> <b><code>alked&lt;/w&gt;</code></b><br>
<code>w</code> <b><code>alker&lt;/w&gt;</code></b><br>
<code>t</code> <b><code>alking&lt;/w&gt;</code></b><br>
<code>t</code> <b><code>alked&lt;/w&gt;</code></b><br>
<code>t</code> <b><code>alker&lt;/w&gt;</code></b>
</div>



## Finalization of the Vocabulary

The Byte Pair Encoding algorithm halts when the maximum frequency of every remaining adjacent pair drops to `1`, as merging a pair that occurs only once provides no generalizable compression across words. Step 14 reduces the frequency of every remaining adjacent pair in the toy corpus to `1`, terminating the training loop.

Executing these 14 merge operations produces a deterministic, compressed token inventory. A structural distinction separates the final encoded corpus from the trained vocabulary dictionary. The nine sequences displayed above represent the compressed state of the training corpus, where repeated character patterns have collapsed into larger subword units.

The encoded corpus does not collapse into nine single-token words. This partial compression reflects a core design property of subword tokenization: the word *talking* appears only once in the corpus, so its leading consonant `t` never reaches the pair frequency required to merge with `alking</w>`. Rare words remain represented as compositions of smaller, shared subwords.

The trained *vocabulary dictionary* contains 27 tokens: the 13 initial base characters plus the 14 subword tokens minted across the merge sequence. This vocabulary count directly governs the input dimensions of the neural network, instantiating the embedding matrix with 27 rows corresponding to the 27 learned tokens.

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2; text-align: left;">
<code>&lt;/w&gt;</code> <code>a</code> <b><code>al</code></b> <b><code>alk</code></b> <b><code>alke</code></b> <b><code>alked</code></b> <b><code>alked&lt;/w&gt;</code></b> <b><code>alker</code></b> <b><code>alker&lt;/w&gt;</code></b> <b><code>alking&lt;/w&gt;</code></b> <code>d</code> <code>e</code> <code>g</code> <b><code>g&lt;/w&gt;</code></b> <code>i</code> <b><code>in</code></b> <b><code>ing&lt;/w&gt;</code></b> <code>k</code> <b><code>ke</code></b> <code>l</code> <code>n</code> <code>o</code> <b><code>oke</code></b> <code>r</code> <code>t</code> <code>w</code> <b><code>woke</code></b>
</div>






The statistical frequency analysis identified the recurring morphological regularities of the corpus. This trained 27-token vocabulary now stands as a fixed, immutable dictionary. The next chapter explores how this finalized dictionary processes unseen text through the corresponding encoding algorithm.

<p><em>Prefer to read this offline? <a href="../assets/docs/tokenization-ebook-v1.0.pdf" target="_blank" rel="noopener">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
