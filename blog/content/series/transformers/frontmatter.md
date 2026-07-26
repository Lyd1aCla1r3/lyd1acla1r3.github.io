<div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
<h1 style="border: none; font-size: 2.5em; margin-bottom: 0; text-align: center;">The Transformer Architecture</h1>
<h2 style="border: none; font-size: 1.5em; margin-top: 10px; color: var(--text-color); font-weight: 300; text-align: center;">A Geometric Toy Example from Scratch</h2>
<p style="margin-top: 50px; font-size: 1.2em;">By Lydia Pedersen</p>
</div>
<div style="page-break-after: always;"></div>
<div style="height: 100vh; display: flex; flex-direction: column; justify-content: flex-end; font-size: 0.8em; color: var(--secondary-color);">
<p><strong>The Transformer Architecture: A Geometric Toy Example from Scratch</strong></p>
<p>Copyright &copy; 2026 Lydia Pedersen. All rights reserved.</p>
<p>No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.</p>
</div>
<div style="page-break-after: always;"></div>
<h1 style='border: none; text-align: left;'>Table of Contents</h1>
<ul style='list-style-type: none; padding: 0; font-size: 0.9em;'>
<li style='margin-bottom: 8px;'><a href='#preface-the-big-picture--tensor-notation' style='color: var(--primary-color); text-decoration: none;'>Preface: The Big Picture & Tensor Notation</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-1-tokens-one-hot-encodings-and-the-embedding-matrix' style='color: var(--primary-color); text-decoration: none;'>Chapter 1: Tokens, One-Hot Encodings, and the Embedding Matrix</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-2-the-permutation-invariance-problem--positional-encoding' style='color: var(--primary-color); text-decoration: none;'>Chapter 2: The Permutation Invariance Problem & Positional Encoding</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-3-the-motivation-for-q-k-and-v-asymmetric-similarity' style='color: var(--primary-color); text-decoration: none;'>Chapter 3: The Motivation for Q, K, and V (Asymmetric Similarity)</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-4-the-attention-score-and-$\sqrt{d_k}$' style='color: var(--primary-color); text-decoration: none;'>Chapter 4: The Attention Score and $\sqrt{d_k}$</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-5-causal-masking' style='color: var(--primary-color); text-decoration: none;'>Chapter 5: Causal Masking</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-6-from-scores-to-synthesis-softmax-and-the-value-matrix' style='color: var(--primary-color); text-decoration: none;'>Chapter 6: From Scores to Synthesis: Softmax and The Value Matrix</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-7-the-cross-head-mixer-and-the-projection-matrix' style='color: var(--primary-color); text-decoration: none;'>Chapter 7: The Cross-Head Mixer and The Projection Matrix</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-8-the-residual-stream-and-the-central-memory-bus' style='color: var(--primary-color); text-decoration: none;'>Chapter 8: The Residual Stream and the Central Memory Bus</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-9-taming-the-stream-the-geometry-of-layer-normalization' style='color: var(--primary-color); text-decoration: none;'>Chapter 9: Taming the Stream: The Geometry of Layer Normalization</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-10-the-mlp-as-a-key-value-memory-bank-expansion' style='color: var(--primary-color); text-decoration: none;'>Chapter 10: The MLP as a Key-Value Memory Bank (Expansion)</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-11-the-mlp---activation-and-contraction' style='color: var(--primary-color); text-decoration: none;'>Chapter 11: The MLP - Activation and Contraction</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-12-completing-layer-1-residuals-and-normalization' style='color: var(--primary-color); text-decoration: none;'>Chapter 12: Completing Layer 1 Residuals and Normalization</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-13-layer-2-self-attention' style='color: var(--primary-color); text-decoration: none;'>Chapter 13: Layer 2 Self-Attention</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-14-scoring-deep-context-layer-2-attention' style='color: var(--primary-color); text-decoration: none;'>Chapter 14: Scoring Deep Context: Layer 2 Attention</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-15-the-final-blend-masking-softmax-and-values-in-layer-2' style='color: var(--primary-color); text-decoration: none;'>Chapter 15: The Final Blend: Masking, Softmax, and Values in Layer 2</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-16-deepening-the-representation-mlp-and-residuals-in-layer-2' style='color: var(--primary-color); text-decoration: none;'>Chapter 16: Deepening the Representation: MLP and Residuals in Layer 2</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-17-mapping-back-to-words' style='color: var(--primary-color); text-decoration: none;'>Chapter 17: Mapping Back to Words</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-18-final-softmax-and-predictions' style='color: var(--primary-color); text-decoration: none;'>Chapter 18: Final Softmax and Predictions</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-19-cross-entropy-loss' style='color: var(--primary-color); text-decoration: none;'>Chapter 19: Cross-Entropy Loss</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-20-the-beautiful-cancellation' style='color: var(--primary-color); text-decoration: none;'>Chapter 20: The Beautiful Cancellation</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-21-backpropagating-through-the-unembedding-and-residual-stream' style='color: var(--primary-color); text-decoration: none;'>Chapter 21: Backpropagating Through the Unembedding and Residual Stream</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-22-backpropagating-through-attention-the-softmax-and-the-mask' style='color: var(--primary-color); text-decoration: none;'>Chapter 22: Backpropagating Through Attention: The Softmax and the Mask</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-23-backpropagation-through-attention-chapter-2-routing-to-q-k-and-v' style='color: var(--primary-color); text-decoration: none;'>Chapter 23: Backpropagation Through Attention (Chapter 2: Routing to Q, K, and V)</a></li>
<li style='margin-bottom: 8px;'><a href='#chapter-24-updating-the-embeddings-and-conclusion' style='color: var(--primary-color); text-decoration: none;'>Chapter 24: Updating the Embeddings and Conclusion</a></li>
</ul>
