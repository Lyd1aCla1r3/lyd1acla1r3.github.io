#!/usr/bin/env python3
"""
Two-pass ebook assembly and build pipeline for the Signal Integrity series.
1. Reads all 18 chapter files and applies transforms.
2. Writes frontmatter.md (title, copyright, TOC) and body.md (chapters with Part dividers) separately.
3. Generates frontmatter.pdf (no page numbers) and body.pdf (page numbers starting at 1).
4. Merges them into signal-integrity-ebook-v1.0.pdf using pypdf.
"""
import os
import re
import subprocess
import base64

directory = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/signal-integrity'
scripts_dir = '/Users/lydia/.gemini/config/skills/pdf_generator/scripts'
frontmatter_file = os.path.join(directory, 'frontmatter.md')
body_file = os.path.join(directory, 'body.md')
frontmatter_pdf = os.path.join(directory, 'frontmatter.pdf')
body_pdf = os.path.join(directory, 'body.pdf')
final_pdf = '/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/signal-integrity-ebook-v1.0.pdf'

# --- Part/Chapter structure ---
parts = [
    {
        'id': 1,
        'title': 'Electromagnetic Foundations',
        'files': [
            '01_Wave_Propagation_and_Transmission_Lines.md',
            '02_Impedance_Reflections_and_Termination.md',
            '03_Skin_Effect_and_Dielectric_Loss.md',
            '04_Inductance_and_Magnetic_Coupling.md',
            '05_Return_Path_Dynamics_and_Parasitic_Effects.md',
        ],
    },
    {
        'id': 2,
        'title': 'Signal Integrity Measurement',
        'files': [
            '06_Time_Domain_Reflectometry.md',
            '07_Smith_Charts.md',
            '08_S_Parameters_and_VNA.md',
            '09_Fourier_Analysis.md',
        ],
    },
    {
        'id': 3,
        'title': 'Jitter Analysis',
        'files': [
            '10_Jitter_Decomposition_and_Measurement.md',
            '11_Dual_Dirac_Model_and_BER_Extrapolation.md',
            '12_Test_Patterns_and_Jitter_Isolation.md',
        ],
    },
    {
        'id': 4,
        'title': 'Equalization and RX Architecture',
        'files': [
            '13_Transmitter_FFE.md',
            '14_CTLE_and_DFE.md',
            '15_PAM4_Signaling_and_Gray_Coding.md',
        ],
    },
    {
        'id': 5,
        'title': 'SerDes Architecture and Clocking',
        'files': [
            '16_SerDes_Architecture_and_Eye_Diagrams.md',
            '17_CDR_and_PLL_Loop_Dynamics.md',
            '18_Line_Coding_FEC_and_Protocol_Framing.md',
        ],
    },
    {
        'id': 6,
        'title': 'Coherent Optics',
        'files': [
            '19_EM_Waves.md',
            '20_Electro_Optic_Modulation.md',
            '21_Mach_Zehnder_IQ_Modulators.md',
            '22_Wideband_Signal_Analysis.md',
        ],
    },
]

# --- Cover image ---
cover_image_path = '/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/images/signal_integrity_cover.jpg'
with open(cover_image_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# --- Part divider images ---
images_dir = '/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/images'
part_images = {}
part_image_files = {
    1: 'si_part1_electromagnetic.jpg',
    2: 'si_part2_measurement.jpg',
    3: 'si_part3_jitter.jpg',
    4: 'si_part4_equalization.jpg',
    5: 'si_part5_serdes.jpg',
    6: 'si_part6_coherent_optics.jpg',
}
for part_id, filename in part_image_files.items():
    with open(os.path.join(images_dir, filename), 'rb') as f:
        part_images[part_id] = base64.b64encode(f.read()).decode('utf-8')

title_page = f"""<style>
@page :first {{
    margin: 0;
}}
</style>
<div style="position: relative; height: 100vh; overflow: hidden; width: 100%; box-sizing: border-box;">
    <img src="data:image/jpeg;base64,{encoded_string}" style="position: absolute; top: -10vh; left: -25%; height: 120vh; width: auto; opacity: 0.32; z-index: -2; max-width: none;" />
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.6) 100%); z-index: -1;"></div>
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: flex-end; padding-right: 12%; text-align: right; box-sizing: border-box;">
        <h1 style="border: none; font-size: 3.8em; margin-bottom: 0; text-align: right; line-height: 1.1;">Signal<br>Integrity</h1>
        <h2 style="border: none; font-size: 1.8em; margin-top: 15px; color: var(--text-color); font-weight: 300; text-align: right; line-height: 1.3;">From Waves to SerDes</h2>
        <p style="margin-top: 50px; font-size: 1.4em; font-weight: 500;">By Lydia Pedersen</p>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""

# FIX Issue 2: Removed page-break-after from copyright page.
# The copyright page is the last page in frontmatter.pdf. The page break
# between frontmatter and body is handled by the PDF merge boundary itself,
# so an explicit break here produced a blank page.
copyright_page = """<div style="height: calc(100vh - 50mm); display: flex; flex-direction: column; justify-content: flex-end; font-size: 0.8em; color: var(--secondary-color);">
<p><strong>Signal Integrity: From Waves to SerDes</strong></p>
<p>Copyright &copy; 2026 Lydia Pedersen. All rights reserved.</p>
<p>No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.</p>
</div>
"""

# --- Build TOC with Part/Chapter hierarchy ---
toc = "<h1 style='border: none; text-align: left;'>Table of Contents</h1>\n"
toc += "<div style='font-size: 0.9em;'>\n"

chapter_num = 0
toc_entries = []  # (part_id, chapter_num, title, anchor) for body assembly

for part in parts:
    part_anchor = f"part-{part['id']}"
    toc += f"<p style='margin-top: 16px; margin-bottom: 4px; font-weight: bold; font-size: 1.1em;'><a href='#{part_anchor}' style='color: var(--primary-color); text-decoration: none;'>Part {part['id']}: {part['title']}</a></p>\n"
    toc += "<ul style='list-style-type: none; padding-left: 20px; margin-top: 0;'>\n"

    for filename in part['files']:
        chapter_num += 1
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename
        anchor = title.lower().replace(' ', '-').replace(':', '').replace('&', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace('/', '-')

        toc += f"<li style='margin-bottom: 6px;'><a href='#{anchor}' style='color: var(--primary-color); text-decoration: none;'>Chapter {chapter_num}: {title}</a></li>\n"
        toc_entries.append({
            'part_id': part['id'],
            'chapter_num': chapter_num,
            'title': title,
            'anchor': anchor,
            'filename': filename,
        })

    toc += "</ul>\n"

toc += "</div>\n"

# --- Build filename-to-anchor map for cross-reference resolution ---
filename_to_anchor = {}
for entry in toc_entries:
    filename_to_anchor[entry['filename']] = '#' + entry['anchor']

# --- Process chapters and build body ---
content_bodies = []
current_part_id = 0

for entry in toc_entries:
    # Insert Part divider page if we are entering a new Part
    if entry['part_id'] != current_part_id:
        current_part_id = entry['part_id']
        part = parts[current_part_id - 1]
        part_divider = f"""<div style="page-break-before: always;"></div>
<a id="part-{part['id']}"></a>
<div style="position: relative; height: 100vh; overflow: hidden; width: 100%; box-sizing: border-box;">
    <img src="data:image/jpeg;base64,{part_images[part['id']]}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.25; z-index: -2;" />
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.7) 50%, rgba(255,255,255,0.3) 100%); z-index: -1;"></div>
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <p style="font-size: 1.2em; color: var(--secondary-color); margin-bottom: 10px; letter-spacing: 3px; text-transform: uppercase;">Part {part['id']}</p>
        <h1 style="border: none; font-size: 2.8em; margin: 0; line-height: 1.2;">{part['title']}</h1>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""
        content_bodies.append(part_divider)

    # Read and process chapter content
    filepath = os.path.join(directory, entry['filename'])
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove download CTA links
    content = re.sub(r'<p><em>Prefer to read this seamlessly offline\?.*?</em></p>\n*', '', content, flags=re.IGNORECASE)

    # Remove SUMMARY comments
    content = re.sub(r'<!--\s*SUMMARY:[\s\S]*?-->\n*', '', content)

    # Strip source extraction links (file 17 references ../../source_extractions/)
    content = re.sub(r'^-\s*\[extraction_[^\]]*\]\(\.\./\.\./source_extractions/[^)]*\).*$\n?', '', content, flags=re.MULTILINE)
    # Clean up orphaned "Source Extractions:" header if all its list items were removed
    content = re.sub(r'\*\*Source Extractions:\*\*\s*\n(?=\s*\n|\*\*|\Z)', '', content)

    # Convert inter-chapter .md links to #anchor links for the ebook
    def resolve_md_link(m):
        full_path = m.group(1)
        basename = os.path.basename(full_path)
        if basename in filename_to_anchor:
            return '(' + filename_to_anchor[basename] + ')'
        return m.group(0)  # leave unchanged if not found

    content = re.sub(r'\((?:\.\./[^)]*?/)?(\d{2}_[^)]*?\.md)\)', resolve_md_link, content)

    # Add anchor before the title
    content = re.sub(
        r'^#\s+(.+)$',
        lambda m: f'<a id="{entry["anchor"]}"></a>\n# Chapter {entry["chapter_num"]}: {m.group(1)}',
        content,
        count=1,
        flags=re.MULTILINE,
    )

    # Colon-context sticking (prevent page breaks between intro text and math/code)
    content = re.sub(r'(:)\n+(\s*```)', r'\1\n<div style="page-break-after: avoid;"></div>\n\n\2', content)
    content = re.sub(r'(:)\n+(\s*\$\$)', r'\1\n<div style="page-break-after: avoid;"></div>\n\n\2', content)

    # Diagram orphan prevention
    blocks = content.split('\n\n')
    for i in range(len(blocks)):
        if '```mermaid' in blocks[i] and i > 0:
            if not blocks[i - 1].strip().startswith(('<', '#', '```')):
                blocks[i - 1] = '<div style="page-break-inside: avoid;">\n\n' + blocks[i - 1]
                blocks[i] = blocks[i] + '\n\n</div>'
    content = '\n\n'.join(blocks)

    content_bodies.append(content)

# --- Write frontmatter.md ---
frontmatter_content = title_page + copyright_page
with open(frontmatter_file, 'w') as f:
    f.write(frontmatter_content)
print("Wrote frontmatter.md")

# --- Write body.md ---
# FIX Issue 2: TOC goes at the start of body. The first Part divider already
# has page-break-before: always, so no explicit page break is needed between
# the TOC and the first content block. Removed the extra break that produced
# a blank page after the TOC.
body_content = toc + '\n\n'
for i, body in enumerate(content_bodies):
    if not body.strip().startswith('<div style="page-break-before: always;">'):
        body_content += '\n\n<div style="page-break-before: always;"></div>\n\n'
    body_content += body

# Inject CSS for math sizing and overflow containment
body_content += """
<style>
.katex-display {
  font-size: 0.9em !important;
}
mjx-container[display="true"] {
  font-size: 95% !important;
  overflow-x: hidden !important;
}
</style>
"""

with open(body_file, 'w') as f:
    f.write(body_content)
print("Wrote body.md")

# --- Generate PDFs ---
generate_pdf = os.path.join(scripts_dir, 'generate_pdf.mjs')

print("Generating frontmatter.pdf (no page numbers)...")
result = subprocess.run(
    ['node', generate_pdf, frontmatter_file, frontmatter_pdf, 'false'],
    cwd=scripts_dir,
    capture_output=True, text=True,
    timeout=120
)
if result.returncode != 0:
    print(f"ERROR generating frontmatter.pdf: {result.stderr}")
    exit(1)
print("  Done.")

print("Generating body.pdf (with page numbers starting at 1)...")
result = subprocess.run(
    ['node', generate_pdf, body_file, body_pdf, 'true'],
    cwd=scripts_dir,
    capture_output=True, text=True,
    timeout=600
)
if result.returncode != 0:
    print(f"ERROR generating body.pdf: {result.stderr}")
    exit(1)
print("  Done.")

# --- Merge PDFs ---
print("Merging frontmatter.pdf + body.pdf -> signal-integrity-ebook-v1.0.pdf...")
from pypdf import PdfWriter
merger = PdfWriter()
merger.append(frontmatter_pdf)
merger.append(body_pdf)
merger.write(final_pdf)
merger.close()
print(f"  Done. Final ebook: {final_pdf}")
