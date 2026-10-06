#!/usr/bin/env python3
"""lint_si.py: writing-rule linter for the Signal Integrity series.

Usage:
    python3 scripts/si_tools/lint_si.py                 # lint all chapters, print summary by rule
    python3 scripts/si_tools/lint_si.py 05 06           # lint only chapters whose filename starts with 05 or 06
    python3 scripts/si_tools/lint_si.py -v [prefixes]   # also print every finding
    python3 scripts/si_tools/lint_si.py --json out.json # write findings as JSON

Rules (see plan Sections 0 and 6):
  EMDASH, ENDASH, CONTRACTION, BANNED, INTENSIFIER, OPENER, TRANSITION, SHORT,
  NOTXIT, RHO, LINK
Prose is checked only: fenced code, display math ($$...$$), inline math, HTML
tags, headings, tables and the SUMMARY comment are excluded from sentence rules.
RHO findings need manual triage (resistivity use is legitimate).
"""
import json
import os
import re
import sys

DIR = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/signal-integrity'

BANNED = ['delve', 'tapestry', 'leverage', 'leverages', 'leveraged', 'leveraging', 'harness', 'harnesses',
          'harnessed', 'harnessing', 'synergy', 'game-changing', 'cutting-edge', 'unlock', 'unlocks',
          'unlocked', 'unlocking', 'empower', 'empowers', 'empowered', 'seamless', 'seamlessly']
INTENSIFIERS = ['massive', 'massively', 'violent', 'violently', 'astronomical', 'astronomically', 'absolute',
                'absolutely', 'perfectly', 'literally', 'organically', 'profoundly', 'flawless', 'flawlessly',
                'remarkably', 'elegant', 'elegantly', 'with mathematical certainty']
OPENERS = ['Because', 'Since', 'Given that', 'Knowing that', 'If', 'When', 'As', 'Once', 'While', 'After']
MECH_TRANSITIONS = ['For example,', 'To address this,', 'Ultimately,', 'Moreover,', 'Furthermore,',
                    'Additionally,', 'In conclusion,']
CONTRACTION_RE = re.compile(r"\b(?:[A-Za-z]+n't|[A-Za-z]+'(?:re|ve|ll|d|m)|(?:it|that|there|here|what|who|he|she|let)'s)\b",
                            re.IGNORECASE)
NOTXIT_RE = re.compile(r"\bNot (?:a|an|the|just|only|merely)?\s*[^.]{1,60}\.\s+(?:It|This|That) (?:is|are)\b")
RHO_RE = re.compile(r'(?:\u03c1|\\rho)')


def strip_noncode(text):
    """Return list of (lineno, line) of prose lines with math, code and html removed."""
    out = []
    in_code = in_math = in_summary = False
    for i, line in enumerate(text.split('\n'), 1):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s.startswith('<!--'):
            if '-->' not in s:
                in_summary = True
            continue
        if in_summary:
            if '-->' in s:
                in_summary = False
            continue
        if s == '$$':
            in_math = not in_math
            continue
        if in_math:
            continue
        if s.startswith('$$') and s.endswith('$$') and len(s) > 4:
            continue
        if s.startswith('#') or s.startswith('|') or s.startswith('<'):
            continue
        out.append((i, line))
    return out


def clean_inline(line):
    line = re.sub(r'\$[^$]+\$', ' MATH ', line)
    line = re.sub(r'`[^`]*`', ' CODE ', line)
    line = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', line)
    line = re.sub(r'<[^>]+>', '', line)
    line = re.sub(r'[*_]{1,3}', '', line)
    line = re.sub(r'^\s*(?:[-*+]|\d+\.)\s+', '', line)
    return line


def sentences(prose_lines):
    """Split into sentences, keeping the starting line number. List items are separate paragraphs."""
    paras, cur, start = [], [], None
    for ln, line in prose_lines:
        is_item = bool(re.match(r'^\s*(?:[-*+]|\d+\.)\s+', line))
        if line.strip() == '' or is_item:
            if cur:
                paras.append((start, ' '.join(cur)))
            cur, start = [], None
        if line.strip() == '':
            continue
        if start is None:
            start = ln
        cur.append(clean_inline(line).strip())
    if cur:
        paras.append((start, ' '.join(cur)))
    res = []
    for ln, p in paras:
        for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"\(])', p):
            if s.strip():
                res.append((ln, s.strip()))
    return res


def lint_file(path):
    findings = []
    text = open(path, encoding='utf-8').read()
    name = os.path.basename(path)

    def add(rule, ln, msg):
        findings.append({'file': name, 'rule': rule, 'line': ln, 'msg': msg[:160]})

    for i, line in enumerate(text.split('\n'), 1):
        if '\u2014' in line:
            add('EMDASH', i, line.strip())
        if '\u2013' in line:
            add('ENDASH', i, line.strip())

    prose = strip_noncode(text)
    possessive_ok = ("it's", "that's", "there's", "here's", "what's", "who's", "he's", "she's", "let's")
    for ln, line in prose:
        c = clean_inline(line)
        for m in CONTRACTION_RE.finditer(c):
            w = m.group(0)
            if w.lower().endswith("'s") and w.lower() not in possessive_ok:
                continue
            add('CONTRACTION', ln, w)
        low = c.lower()
        for w in BANNED:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                add('BANNED', ln, w)
        for w in INTENSIFIERS:
            if re.search(r'\b' + re.escape(w) + r'\b', low):
                add('INTENSIFIER', ln, w)
        if RHO_RE.search(line):
            add('RHO', ln, line.strip())

    for ln, s in sentences(prose):
        for op in OPENERS:
            if s.startswith(op + ' ') or s.startswith(op + ','):
                add('OPENER', ln, s)
                break
        for tr in MECH_TRANSITIONS:
            if s.startswith(tr):
                add('TRANSITION', ln, s)
        words = [w for w in re.split(r'\s+', s) if re.search(r'[A-Za-z0-9]', w)]
        if 0 < len(words) <= 6 and not s.endswith(':') and not s.endswith('?'):
            add('SHORT', ln, s)
    flat = '\n'.join(clean_inline(l) for _, l in prose)
    for m in NOTXIT_RE.finditer(flat):
        add('NOTXIT', 0, m.group(0))

    for i, line in enumerate(text.split('\n'), 1):
        for m in re.finditer(r'\]\(([^)]+)\)', line):
            tgt = m.group(1).split('#')[0]
            if tgt.endswith('.md'):
                if not os.path.exists(os.path.normpath(os.path.join(DIR, tgt))):
                    add('LINK', i, tgt)
            elif 'source_extractions' in tgt or 'coherent-optics-ebook' in tgt:
                add('LINK', i, tgt)
    return findings


def main():
    args = sys.argv[1:]
    verbose = '-v' in args
    args = [a for a in args if a != '-v']
    jpath = None
    if '--json' in args:
        k = args.index('--json')
        jpath = args[k + 1]
        args = args[:k] + args[k + 2:]
    files = sorted(f for f in os.listdir(DIR) if re.match(r'^\d\d_.*\.md$', f))
    if args:
        files = [f for f in files if any(f.startswith(a) for a in args)]
    allf = []
    for f in files:
        allf += lint_file(os.path.join(DIR, f))
    if verbose:
        for x in allf:
            print(f"{x['file']}:{x['line']} [{x['rule']}] {x['msg']}")
        print()
    print(f"Files linted: {len(files)}")
    for r in sorted({x['rule'] for x in allf}):
        print(f"  {r:12s} {sum(1 for x in allf if x['rule'] == r)}")
    print(f"  TOTAL        {len(allf)}")
    if jpath:
        json.dump(allf, open(jpath, 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
