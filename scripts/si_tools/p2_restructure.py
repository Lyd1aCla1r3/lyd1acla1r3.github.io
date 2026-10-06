#!/usr/bin/env python3
"""p2_restructure.py: one-shot, mechanical S1/P2 restructure of the Signal Integrity chapters.

No prose is rewritten. The script (1) moves four sections between chapters,
(2) concatenates old 19 + old 20, (3) renames files with git mv through a temp
prefix, (4) retitles three chapters per plan Section 3.2, (5) rewrites inter-chapter
links to flat new filenames, (6) removes the source_extractions list, and
(7) points the Part 6 CTA lines at the Signal Integrity ebook.
Run once from the portfolio root. Aborts if the old layout is not present.
"""
import os
import re
import subprocess

D = 'blog/content/series/signal-integrity'


def p(name):
    return os.path.join(D, name)


def rd(name):
    return open(p(name), encoding='utf-8').read()


def wr(name, text):
    if not text.endswith('\n'):
        text += '\n'
    open(p(name), 'w', encoding='utf-8').write(text)


def extract_block(text, heading):
    """Remove and return the block starting at `heading` up to the next line beginning with '#'."""
    lines = text.split('\n')
    start = next(i for i, l in enumerate(lines) if l.strip() == heading)
    end = start + 1
    while end < len(lines) and not lines[end].startswith('#'):
        end += 1
    block = '\n'.join(lines[start:end]).rstrip('\n') + '\n\n'
    rest = '\n'.join(lines[:start] + lines[end:])
    return block, rest


def insert_before(text, heading, block):
    lines = text.split('\n')
    idx = next(i for i, l in enumerate(lines) if l.strip() == heading)
    return '\n'.join(lines[:idx] + block.rstrip('\n').split('\n') + [''] + lines[idx:])


OLD = {
    'f01': '01_Wave_Propagation_and_Transmission_Lines.md',
    'f02': '02_Impedance_Reflections_and_Termination.md',
    'f03': '03_Skin_Effect_and_Dielectric_Loss.md',
    'f04': '04_Inductance_and_Magnetic_Coupling.md',
    'f05': '05_Return_Path_Dynamics_and_Parasitic_Effects.md',
    'f06': '06_Time_Domain_Reflectometry.md',
    'f07': '07_Smith_Charts.md',
    'f08': '08_S_Parameters_and_VNA.md',
    'f09': '09_Fourier_Analysis.md',
    'f19': '19_EM_Waves.md',
    'f20': '20_Electro_Optic_Modulation.md',
    'f21': '21_Mach_Zehnder_IQ_Modulators.md',
    'f22': '22_Wideband_Signal_Analysis.md',
}
for f in OLD.values():
    assert os.path.exists(p(f)), f

# ---------------- 1. section moves ----------------
t01, t02, t05, t06, t08, t09 = (rd(OLD[k]) for k in ('f01', 'f02', 'f05', 'f06', 'f08', 'f09'))

# A. old 01 "Frequency Content of the Transition" -> new 02 (old 09), before the transition-speed section
blk, t01 = extract_block(t01, '### Frequency Content of the Transition')
t09 = insert_before(t09, '### Frequency Content Is Determined by Transition Speed', blk)

# B. old 09 "The TDR-to-S-Parameter Conversion" -> new 08, after "Converting Between Domains" (before Edge Cases)
blk, t09 = extract_block(t09, '### The TDR-to-S-Parameter Conversion')
t08 = insert_before(t08, '## Edge Cases', blk)

# C. old 02 TDR worked examples -> new 07 (old 06); masking section -> end of new 07 Edge Cases
blk1, t02 = extract_block(t02, '### Open Circuit Response on a TDR')
blk2, t02 = extract_block(t02, '### Impedance Bump and Return to Baseline')
blk3, t02 = extract_block(t02, '### Masking and Spreading of Downstream Discontinuities')
t02 = t02.replace('## Worked Examples\n\n', '', 1)  # heading is now empty; C03 re-adds worked examples
t06 = insert_before(t06, '## Edge Cases', blk1 + blk2)
t06 = t06.rstrip('\n') + '\n\n' + blk3

# D. old 05 "Reactive Impedance and Frequency Scaling" -> new 03 (old 02), end of Core Concepts
blk, t05 = extract_block(t05, '### Reactive Impedance and Frequency Scaling')
t02 = insert_before(t02, '## Architecture', blk)

for k, t in (('f01', t01), ('f02', t02), ('f05', t05), ('f06', t06), ('f08', t08), ('f09', t09)):
    wr(OLD[k], t)

# ---------------- 2. Part 6 concatenation (old 19 + old 20) ----------------
t19, t20 = rd(OLD['f19']), rd(OLD['f20'])
sum_re = re.compile(r'<!--\s*SUMMARY:\s*(.*?)\s*-->\n*', re.S)
cta_re = re.compile(r'^<p><em>Prefer to read.*?</em></p>\n*', re.S | re.M)
s19 = sum_re.search(t19).group(1)
s20 = sum_re.search(t20).group(1)
body19 = cta_re.sub('', sum_re.sub('', re.sub(r'^#\s+.+\n+', '', t19, count=1)), count=1).strip('\n')
body20 = cta_re.sub('', sum_re.sub('', re.sub(r'^#\s+.+\n+', '', t20, count=1)), count=1).strip('\n')
merged = ('# Light as an Electromagnetic Wave and the Electro-Optic Effect\n\n'
          f'<!-- SUMMARY: {s19} {s20} -->\n\n'
          '@@CTA@@\n\n' + body19 + '\n\n' + body20 + '\n')
wr(OLD['f19'], merged)
os.remove(p(OLD['f20']))  # content now lives in old 19; git sees the rename/merge at commit time

# ---------------- 3. renames (temp prefix avoids collisions) ----------------
RENAME = [  # (old, new)
    (OLD['f09'], '02_Frequency_Content_of_Digital_Signals.md'),
    (OLD['f02'], '03_Impedance_Reflections_and_Termination.md'),
    (OLD['f04'], '04_Inductance_Magnetic_Coupling_and_Crosstalk.md'),
    (OLD['f03'], '05_Skin_Effect_and_Dielectric_Loss.md'),
    (OLD['f05'], '06_Return_Path_Dynamics_and_Parasitic_Effects.md'),
    (OLD['f06'], '07_Time_Domain_Reflectometry.md'),
    (OLD['f07'], '09_Smith_Charts.md'),
    (OLD['f19'], '19_Light_and_the_Electro_Optic_Effect.md'),
    (OLD['f21'], '20_Mach_Zehnder_IQ_Modulators.md'),
    (OLD['f22'], '21_Wideband_Signal_Analysis.md'),
]
for old, _ in RENAME:
    subprocess.check_call(['git', 'mv', p(old), p('tmp__' + old)])
for old, new in RENAME:
    subprocess.check_call(['git', 'mv', p('tmp__' + old), p(new)])

# old basename -> new basename (for link rewriting); old 20 merged into new 19
LINKMAP = {old: new for old, new in RENAME}
LINKMAP[OLD['f20']] = '19_Light_and_the_Electro_Optic_Effect.md'

# ---------------- 4. retitle (plan 3.2 proposed titles) ----------------
TITLES = {
    '02_Frequency_Content_of_Digital_Signals.md': 'Frequency Content of Digital Signals',
    '04_Inductance_Magnetic_Coupling_and_Crosstalk.md': 'Inductance, Magnetic Coupling, and Crosstalk',
}
for f, title in TITLES.items():
    t = rd(f)
    t = re.sub(r'^#\s+.+$', '# ' + title, t, count=1, flags=re.M)
    wr(f, t)

# ---------------- 5-7. links, source extractions, CTA ----------------
cta01 = cta_re.search(rd('01_Wave_Propagation_and_Transmission_Lines.md')).group(0).strip('\n')
link_re = re.compile(r'\]\((?:\.\./[^)]*?/)?(\d\d_[^)#]*?\.md)(#[^)]*)?\)')
for f in sorted(os.listdir(D)):
    if not re.match(r'^\d\d_.*\.md$', f):
        continue
    t = rd(f)
    t = link_re.sub(lambda m: '](' + LINKMAP.get(m.group(1), m.group(1)) + (m.group(2) or '') + ')', t)
    t = re.sub(r'\*\*Source Extractions:\*\*\n(?:- \[extraction_[^\n]*\n)+\n?', '', t)
    t = t.replace('@@CTA@@', cta01)
    if f[:2] in ('20', '21'):
        t = re.sub(r'^<p><em>Prefer to read.*?</em></p>', lambda m: cta01, t, count=1, flags=re.M)
    wr(f, t)

print('P2 restructure complete')
