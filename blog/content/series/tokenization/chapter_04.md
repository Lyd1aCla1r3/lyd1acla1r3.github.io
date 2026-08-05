# Part 4: Encoding and Decoding
<!-- SUMMARY: The deployment of a static vocabulary and ordered list of merge rules enables the rigorous tokenization of novel text. This process mathematically guarantees consistency with the training distribution while gracefully decomposing unseen words into familiar subword units. -->

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>

The 14-step training algorithm successfully halted by discovering a final 27-token vocabulary built upon the exact morphological patterns of the corpus. The resulting list of learned merge rules now stands as a static, ordered mapping protocol. Deploying this protocol to tokenize unseen text forms the critical next phase of the subword pipeline.

## The Ordered Merge Algorithm

The encoding process abandons the dynamic frequency counting that drove the training phase. The algorithm relies entirely instead on the exact sequence of merge operations acquired during training. These rules are applied to any incoming text strictly in the order they were learned. 

This sequential application constitutes a greedy, longest-match algorithm. Enforcing the original chronological order of merges guarantees that the resulting tokenization mathematically reflects the most dominant statistical patterns of the training data. The algorithm begins by splitting the incoming text into individual characters and appending the boundary marker `</w>`.

## Encoding the Known Distribution

The application of this static protocol to words from the original training distribution yields highly optimized subword representations. The encoding of the word `walked`, which exists in the original training corpus, demonstrates the systematic execution of these ordered rules.

Initial: `w` `a` `l` `k` `e` `d` `</w>`  
Step 1: `a` + `l` $\rightarrow$ `w` **`al`** `k` `e` `d` `</w>` (Rule 1)  
Step 2: **`al`** + `k` $\rightarrow$ `w` **`alk`** `e` `d` `</w>` (Rule 2)  
Step 3: **`alk`** + `e` $\rightarrow$ `w` **`alke`** `d` `</w>` (Rule 3)  
Step 4: **`alke`** + `d` $\rightarrow$ `w` **`alked`** `</w>` (Rule 8)  
Step 5: **`alked`** + `</w>` $\rightarrow$ `w` **`alked</w>`** (Rule 10)  


The algorithm completely ignores rules 4, 5, 6, 7, and 9 as the necessary adjacent pairs do not exist in the current sequence. The word systematically collapses down to two final tokens: `w` and `alked</w>`. 

A similar execution dictates the encoding of `waking`, which is also present in the original training corpus.

Initial: `w` `a` `k` `i` `n` `g` `</w>`  
Step 1: `g` + `</w>` $\rightarrow$ `w` `a` `k` `i` `n` **`g</w>`** (Rule 4)  
Step 2: `i` + `n` $\rightarrow$ `w` `a` `k` **`in`** **`g</w>`** (Rule 5)  
Step 3: **`in`** + **`g</w>`** $\rightarrow$ `w` `a` `k` **`ing</w>`** (Rule 6)  


The training process naturally halted before discovering a sequence unifying `w`, `a`, and `k`, causing the final encoding to remain fractured across four distinct tokens: `w`, `a`, `k`, and `ing</w>`.

## Subword Generalization on Novel Text

The true power of the Byte Pair Encoding algorithm emerges when encountering text wholly absent from the training corpus. The system leverages familiar morphological patterns to parse unseen words without suffering an out-of-vocabulary collapse.

Processing the novel word `stalking`, which does not exist in the training corpus, demonstrates this exact mechanism. The algorithm processes the string using the identical static rule sequence.

Initial: `s` `t` `a` `l` `k` `i` `n` `g` `</w>`  
Step 1: `a` + `l` $\rightarrow$ `s` `t` **`al`** `k` `i` `n` `g` `</w>` (Rule 1)  
Step 2: **`al`** + `k` $\rightarrow$ `s` `t` **`alk`** `i` `n` `g` `</w>` (Rule 2)  
Step 3: `g` + `</w>` $\rightarrow$ `s` `t` **`alk`** `i` `n` **`g</w>`** (Rule 4)  
Step 4: `i` + `n` $\rightarrow$ `s` `t` **`alk`** **`in`** **`g</w>`** (Rule 5)  
Step 5: **`in`** + **`g</w>`** $\rightarrow$ `s` `t` **`alk`** **`ing</w>`** (Rule 6)  
Step 6: **`alk`** + **`ing</w>`** $\rightarrow$ `s` `t` **`alking</w>`** (Rule 7)  


The algorithm isolates the unknown prefix `s` and `t` at the fundamental character level, while assembling the highly frequent suffix `alking</w>` learned from the training data. The resulting three-token sequence `s`, `t`, and `alking</w>` requires no new mathematical components.

The novel word `awoke`, similarly absent from the original corpus, undergoes an identical decomposition.

Initial: `a` `w` `o` `k` `e` `</w>`  
Step 1: `k` + `e` $\rightarrow$ `a` `w` `o` **`ke`** `</w>` (Rule 12)  
Step 2: `o` + **`ke`** $\rightarrow$ `a` `w` **`oke`** `</w>` (Rule 13)  
Step 3: `w` + **`oke`** $\rightarrow$ `a` **`woke`** `</w>` (Rule 14)  


The algorithm discovers the familiar sequence `woke`, leaving the independent prefix `a` and the final boundary marker `</w>` as separate units.

## The Triviality of Decoding

Reversing this process to recover raw text from a token sequence requires no complex algorithms or stored rules. Decoding acts as a pure concatenation operation. The system simply joins the sequence of string tokens together and transforms the `</w>` boundary markers back into standard spaces. This trivial inverse guarantees that the original text is recovered with perfect fidelity.

The tokenization pipeline is now mathematically complete, reliably transforming variable text into discrete integer sequences. This system remains bound to an arbitrary initial character set, however. If the encoder encounters a string containing any symbol absent from the original 13 base characters, such as a capital letter or punctuation, the entire process fails. The underlying dictionary possesses no mathematical representation for the unknown input, triggering a catastrophic out-of-vocabulary error. The subsequent section abandons this limitation entirely, examining how modern production systems drive Byte Pair Encoding down to the raw byte level to achieve true universal text encoding.

<p><em>Prefer to read this seamlessly offline? <a href="/assets/docs/tokenization-ebook-v1.0.pdf">Download the complete, formatting-optimized Tokenization Ebook here.</a></em></p>
