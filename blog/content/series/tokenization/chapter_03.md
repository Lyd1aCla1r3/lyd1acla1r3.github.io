# Part 3: Training BPE by Hand


<style>
  .trace-container code {
    font-size: 0.75em !important;
    padding: 0.15em 0.3em !important;
  }
  .trace-container td {
    white-space: nowrap !important;
  }
  .trace-container b code {
    font-weight: 900 !important;
    color: #9a5b65 !important;
    background-color: #fdf5f6 !important;
    border: 1px solid #e0c6cb !important;
  }
  @media (prefers-color-scheme: dark) {
    .trace-container b code {
      color: #e6b3bc !important;
      background-color: #3b2a2d !important;
      border: 1px solid #6b4d53 !important;
    }
  }
</style>

<!-- SUMMARY: Executing the Byte Pair Encoding algorithm against a concrete corpus reveals exactly how abstract statistical rules collapse character-level data into optimized semantic units. Tracing the frequency counts and merge selections across a fourteen-step compression sequence demonstrates the deterministic derivation of morphological stems and suffixes without linguistic programming. -->

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The formal definition of the Byte Pair Encoding algorithm establishes a greedy, iterative mechanism for subword compression. Executing this mechanism against a concrete corpus reveals exactly how these abstract rules operate in practice. The procedure relies entirely on statistical frequency rather than linguistic programming.

## The Initial State

The training process begins with the nine distinct verbs defined in the preceding article. Each word is split into individual character tokens, terminated by the `</w>` boundary marker. Once the initial state of the corpus is established, the discrete token sequences and their absolute frequencies are tracked across the text.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code> <code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>w</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code> <code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>t</code> <code>a</code> <code>l</code> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
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


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>al</code></b> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>al</code></b> <code>k</code> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
</div>



This operation immediately alters the subsequent frequency distribution. The second merge iteration tallies adjacent pairs across the newly updated corpus. The pair `al` + `k` emerges as the most frequent pattern.


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


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alk</code></b> <code>e</code> <code>d</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alk</code></b> <code>e</code> <code>r</code> <code>&lt;/w&gt;</code>
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


After merely three iterations, the counting mechanism derives `alk`, the central morphological root shared by the majority of the corpus. This fragment serves as the structural foundation for *walking*, *walked*, *walker*, *talking*, *talked*, and *talker*. The internal representation of the text compresses significantly.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>w</code> <code>a</code> <code>k</code> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>&lt;/w&gt;</code> <code>w</code> <code>o</code> <code>k</code> <code>e</code> <code>n</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alke</code></b> <code>d</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alke</code></b> <code>r</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alk</code></b> <code>i</code> <code>n</code> <code>g</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alke</code></b> <code>d</code> <code>&lt;/w&gt;</code> <code>t</code> <b><code>alke</code></b> <code>r</code> <code>&lt;/w&gt;</code>
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


After fourteen merge operations, the original sequences of isolated characters transition into large subword fragments. The internal representation of the text demonstrates profound compression.


<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>w</code> <code>a</code> <code>k</code> <b><code>ing&lt;/w&gt;</code></b> <b><code>woke</code></b> <code>&lt;/w&gt;</code> <b><code>woke</code></b> <code>n</code> <code>&lt;/w&gt;</code> <code>w</code> <b><code>alking&lt;/w&gt;</code></b> <code>w</code> <b><code>alked&lt;/w&gt;</code></b> <code>w</code> <b><code>alker&lt;/w&gt;</code></b> <code>t</code> <b><code>alking&lt;/w&gt;</code></b> <code>t</code> <b><code>alked&lt;/w&gt;</code></b> <code>t</code> <b><code>alker&lt;/w&gt;</code></b>
</div>



## Finalization of the Vocabulary

The Byte Pair Encoding algorithm naturally halts when the maximum frequency of any adjacent pair drops to 1, because merging a pair that only occurs once offers no further compression benefit. Following step fourteen, the frequency of every remaining adjacent pair in our toy corpus has dropped to exactly 1. Therefore, the training algorithm definitively halts at this exact state. 

The execution of exactly fourteen merge operations yields a deterministic, highly compressed token inventory. It is crucial to distinguish between the final state of the corpus and the final trained vocabulary. The nine sequences shown above represent the completely compressed state of the corpus. The structural update has collapsed the original sequence of isolated characters into larger subword fragments. 

The corpus, however, does not perfectly compress into nine single-token words. This is a fundamental feature of subword tokenization: because the word *talking* only appears once in this tiny corpus, its leading consonant `t` never achieves a high enough frequency to merge with its suffix. Rare words are natively preserved as sequences of smaller, common subwords.

The *vocabulary dictionary* itself contains exactly 27 items: the 13 initial base characters plus the 14 new subwords generated during the merges. Because the vocabulary size directly dictates the architecture's input dimensions, the neural network's embedding matrix will now be instantiated with exactly 27 rows, one for each of these learned tokens.

<div class="trace-container" style="margin-bottom: 2rem; line-height: 2.2;">
<code>&lt;/w&gt;</code> <code>a</code> <b><code>al</code></b> <b><code>alk</code></b> <b><code>alke</code></b> <b><code>alked</code></b> <b><code>alked&lt;/w&gt;</code></b> <b><code>alker</code></b> <b><code>alker&lt;/w&gt;</code></b> <b><code>alking&lt;/w&gt;</code></b> <code>d</code> <code>e</code> <code>g</code> <b><code>g&lt;/w&gt;</code></b> <code>i</code> <b><code>in</code></b> <b><code>ing&lt;/w&gt;</code></b> <code>k</code> <b><code>ke</code></b> <code>l</code> <code>n</code> <code>o</code> <b><code>oke</code></b> <code>r</code> <code>t</code> <code>w</code> <b><code>woke</code></b>
</div>



The statistical frequency analysis successfully identified the structural regularities of the English language. This trained 27-token vocabulary now exists as a fixed, immutable dictionary. The subsequent article explores how this finalized dictionary processes completely new, unseen text through the corresponding encoding algorithm.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
