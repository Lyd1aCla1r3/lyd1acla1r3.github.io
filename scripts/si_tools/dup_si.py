#!/usr/bin/env python3
"""dup_si.py: cross-chapter 8-word shingle overlap for the Signal Integrity series.

Usage:
    python3 scripts/si_tools/dup_si.py              # print total and top pairs
    python3 scripts/si_tools/dup_si.py -n 25        # show top 25 pairs
    python3 scripts/si_tools/dup_si.py 05 06        # restrict pairs to those involving the given prefixes

Metric: a shingle is 8 consecutive normalized words (lowercase, punctuation and
math removed). Prose only (code fences, display math, SUMMARY and CTA lines
skipped). CROSS-CHAPTER SHARED SHINGLES = number of DISTINCT shingles that occur
in two or more chapters. The pair table reports distinct shingles shared by each
chapter pair (chapter ids are filename prefixes).
"""
import itertools
import os
import re
import sys
from collections import defaultdict

DIR = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/signal-integrity'
K = 8


def prose_words(path):
    text = open(path, encoding='utf-8').read()
    text = re.sub(r'<!--[\s\S]*?-->', ' ', text)
    text = re.sub(r'```[\s\S]*?```', ' ', text)
    text = re.sub(r'\$\$[\s\S]*?\$\$', ' ', text)
    text = re.sub(r'\$[^$\n]+\$', ' ', text)
    text = re.sub(r'<p><em>Prefer to read.*?</em></p>', ' ', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'^#+ .*$', ' ', text, flags=re.M)
    text = re.sub(r"[^a-z0-9' \n]", ' ', text.lower())
    return text.split()


def main():
    args = sys.argv[1:]
    top = 15
    if '-n' in args:
        k = args.index('-n')
        top = int(args[k + 1])
        args = args[:k] + args[k + 2:]
    files = sorted(f for f in os.listdir(DIR) if re.match(r'^\d\d_.*\.md$', f))
    sh = defaultdict(set)
    words_total = 0
    for f in files:
        w = prose_words(os.path.join(DIR, f))
        words_total += len(w)
        for i in range(len(w) - K + 1):
            sh[' '.join(w[i:i + K])].add(f[:2])
    shared = {s: c for s, c in sh.items() if len(c) >= 2}
    pairs = defaultdict(int)
    for s, c in shared.items():
        for a, b in itertools.combinations(sorted(c), 2):
            pairs[(a, b)] += 1
    print(f"Chapters: {len(files)}   prose words: {words_total}")
    print(f"Distinct shingles total: {len(sh)}")
    print(f"CROSS-CHAPTER SHARED SHINGLES (distinct, in >=2 chapters): {len(shared)}")
    rows = sorted(pairs.items(), key=lambda x: -x[1])
    if args:
        rows = [r for r in rows if any(a in r[0] for a in args)]
    print(f"Pairs with overlap: {len(pairs)}  (top {top}{' filtered' if args else ''}):")
    for (a, b), n in rows[:top]:
        print(f"  {a} x {b}: {n}")


if __name__ == '__main__':
    main()
