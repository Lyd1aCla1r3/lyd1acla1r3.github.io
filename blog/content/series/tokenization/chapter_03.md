# Part 3: Training BPE by Hand

<!-- SUMMARY: Executing the Byte Pair Encoding algorithm against a concrete corpus reveals exactly how abstract statistical rules collapse character-level data into optimized semantic units. Tracing the frequency counts and merge selections across a fourteen-step compression sequence demonstrates the deterministic derivation of morphological stems and suffixes without linguistic programming. -->

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The formal definition of the Byte Pair Encoding algorithm establishes a greedy, iterative mechanism for subword compression. Executing this mechanism against a concrete corpus reveals exactly how these abstract rules operate in practice. The procedure relies entirely on statistical frequency rather than linguistic programming.

## The Initial State

The training process begins with the nine distinct verbs defined in the preceding article. Each word is split into individual character tokens, terminated by the `</w>` boundary marker. Once the initial state of the corpus is established, the discrete token sequences and their absolute frequencies are tracked across the text.


| |
|---|
| `w` `a` `k` `i` `n` `g` `</w>` |
| `w` `o` `k` `e` `</w>` |
| `w` `o` `k` `e` `n` `</w>` |
| `w` `a` `l` `k` `i` `n` `g` `</w>` |
| `w` `a` `l` `k` `e` `d` `</w>` |
| `w` `a` `l` `k` `e` `r` `</w>` |
| `t` `a` `l` `k` `i` `n` `g` `</w>` |
| `t` `a` `l` `k` `e` `d` `</w>` |
| `t` `a` `l` `k` `e` `r` `</w>` |

## The First Merges: Deriving Roots

The algorithm evaluates the frequency of every adjacent token pair in this initial state. The pairs `a` + `l`, `k` + `e`, and `l` + `k` tie for the highest frequency with six occurrences each. Lexicographical sorting dictates the selection of `a` + `l` for the inaugural merge operation. The new token `al` is formally registered, and the corpus representation is updated globally.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 1 | `a` + `l` | $\rightarrow$ `al` | 6 occurrences |

| |
|---|
| `w` `a` `k` `i` `n` `g` `</w>` |
| `w` `o` `k` `e` `</w>` |
| `w` `o` `k` `e` `n` `</w>` |
| `w` `al` `k` `i` `n` `g` `</w>` |
| `w` `al` `k` `e` `d` `</w>` |
| `w` `al` `k` `e` `r` `</w>` |
| `t` `al` `k` `i` `n` `g` `</w>` |
| `t` `al` `k` `e` `d` `</w>` |
| `t` `al` `k` `e` `r` `</w>` |

This operation immediately alters the subsequent frequency distribution. The second merge iteration tallies adjacent pairs across the newly updated corpus. The pair `al` + `k` emerges as the most frequent pattern.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 2 | `al` + `k` | $\rightarrow$ `alk` | 6 occurrences |

| |
|---|
| `w` `a` `k` `i` `n` `g` `</w>` |
| `w` `o` `k` `e` `</w>` |
| `w` `o` `k` `e` `n` `</w>` |
| `w` `alk` `i` `n` `g` `</w>` |
| `w` `alk` `e` `d` `</w>` |
| `w` `alk` `e` `r` `</w>` |
| `t` `alk` `i` `n` `g` `</w>` |
| `t` `alk` `e` `d` `</w>` |
| `t` `alk` `e` `r` `</w>` |

The merge operation fuses these tokens, creating the cohesive `alk` unit. The third merge iteration establishes that the pair `alk` + `e` occurs four times, binding the root verb to the start of its suffixes.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 3 | `alk` + `e` | $\rightarrow$ `alke` | 4 occurrences |

After merely three iterations, the counting mechanism derives `alk`, the central morphological root shared by the majority of the corpus. This fragment serves as the structural foundation for *walking*, *walked*, *walker*, *talking*, *talked*, and *talker*. The internal representation of the text compresses significantly.


| |
|---|
| `w` `a` `k` `i` `n` `g` `</w>` |
| `w` `o` `k` `e` `</w>` |
| `w` `o` `k` `e` `n` `</w>` |
| `w` `alk` `i` `n` `g` `</w>` |
| `w` `alke` `d` `</w>` |
| `w` `alke` `r` `</w>` |
| `t` `alk` `i` `n` `g` `</w>` |
| `t` `alke` `d` `</w>` |
| `t` `alke` `r` `</w>` |

## Assembling Suffixes

The subsequent three merge iterations reveal how boundary markers influence the derivation of suffixes. Iteration four evaluates the updated sequences and identifies the highest frequency pair ending the gerund verbs.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 4 | `g` + `</w>` | $\rightarrow$ `g</w>` | 3 occurrences |

Iteration five targets the interior of the suffix, binding the preceding characters.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 5 | `i` + `n` | $\rightarrow$ `in` | 3 occurrences |

Iteration six combines these two newly formed tokens.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 6 | `in` + `g</w>` | $\rightarrow$ `ing</w>` | 3 occurrences |

This sequence formally registers the morphological `-ing` suffix into the subword vocabulary. The token boundary marker `</w>` guarantees that this newly minted token `ing</w>` specifically represents the suffix at the end of a word, preventing it from incorrectly matching the substring "ing" in the middle of an unrelated word.

## Accelerated Convergence

The iterative compression rapidly integrates the remaining structure. The next five iterations bind the derived roots and suffixes into complete semantic units.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 7 | `alk` + `ing</w>` | $\rightarrow$ `alking</w>` | 2 occurrences |
| Step 8 | `alke` + `d` | $\rightarrow$ `alked` | 2 occurrences |
| Step 9 | `alke` + `r` | $\rightarrow$ `alker` | 2 occurrences |
| Step 10 | `alked` + `</w>` | $\rightarrow$ `alked</w>` | 2 occurrences |
| Step 11 | `alker` + `</w>` | $\rightarrow$ `alker</w>` | 2 occurrences |

The initial `alk` fragment transforms into three complete lexical structures: `alking</w>`, `alked</w>`, and `alker</w>`. The counting procedure then evaluates the remaining verb family.


| Step | Operation | Result | Frequency |
|:---|:---|:---|---:|
| Step 12 | `k` + `e` | $\rightarrow$ `ke` | 2 occurrences |
| Step 13 | `o` + `ke` | $\rightarrow$ `oke` | 2 occurrences |
| Step 14 | `w` + `oke` | $\rightarrow$ `woke` | 2 occurrences |

After fourteen merge operations, the original sequences of isolated characters transition into large subword fragments. The internal representation of the text demonstrates profound compression.


| |
|---|
| `w` `a` `k` `ing</w>` |
| `woke` `</w>` |
| `woke` `n` `</w>` |
| `w` `alking</w>` |
| `w` `alked</w>` |
| `w` `alker</w>` |
| `t` `alking</w>` |
| `t` `alked</w>` |
| `t` `alker</w>` |

## Finalization of the Vocabulary

The Byte Pair Encoding algorithm naturally halts when the maximum frequency of any adjacent pair drops to 1, because merging a pair that only occurs once offers no further compression benefit. Following step fourteen, the frequency of every remaining adjacent pair in our toy corpus has dropped to exactly 1. Therefore, the training algorithm definitively halts at this exact state. 

The execution of exactly fourteen merge operations yields a deterministic, highly compressed token inventory. It is crucial to distinguish between the final state of the corpus and the final trained vocabulary. The nine sequences shown above represent the completely compressed state of the corpus. The structural update has collapsed the original sequence of isolated characters into larger subword fragments. 

The corpus, however, does not perfectly compress into nine single-token words. This is a fundamental feature of subword tokenization: because the word *talking* only appears once in this tiny corpus, its leading consonant `t` never achieves a high enough frequency to merge with its suffix. Rare words are natively preserved as sequences of smaller, common subwords.

The *vocabulary dictionary* itself contains exactly 27 items: the 13 initial base characters plus the 14 new subwords generated during the merges. Because the vocabulary size directly dictates the architecture's input dimensions, the neural network's embedding matrix will now be instantiated with exactly 27 rows, one for each of these learned tokens.

| | | | | |
|---|---|---|---|---|
| `</w>` | `a` | `al` | `alk` | `alke` |
| `alked` | `alked</w>` | `alker` | `alker</w>` | `alking</w>` |
| `d` | `e` | `g` | `g</w>` | `i` |
| `in` | `ing</w>` | `k` | `ke` | `l` |
| `n` | `o` | `oke` | `r` | `t` |
| `w` | `woke` | | | |

The statistical frequency analysis successfully identified the structural regularities of the English language. This trained 27-token vocabulary now exists as a fixed, immutable dictionary. The subsequent article explores how this finalized dictionary processes completely new, unseen text through the corresponding encoding algorithm.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
