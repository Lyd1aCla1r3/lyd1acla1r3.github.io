#!/usr/bin/env python3
"""
Two-pass ebook assembly and build pipeline.
1. Reads all chapter files and applies transforms.
2. Writes frontmatter.md (title, copyright, TOC) and body.md (preface + chapters) separately.
3. Generates frontmatter.pdf (no page numbers) and body.pdf (page numbers starting at 1).
4. Merges them into tokenization-ebook-v1.0.pdf using pypdf.
"""
import os
import re
import subprocess

directory = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/tokenization'
scripts_dir = '/Users/lydia/enablement/.agents/skills/pdf_generator/scripts'
frontmatter_file = os.path.join(directory, 'frontmatter.md')
body_file = os.path.join(directory, 'body.md')
frontmatter_pdf = os.path.join(directory, 'frontmatter.pdf')
body_pdf = os.path.join(directory, 'body.pdf')
final_pdf = '/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/tokenization-ebook-v1.0.pdf'

files = ['preface.md'] + [f'chapter_{i:02d}.md' for i in range(1, 6)]

import base64

with open("/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/images/tokenization_cover.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

title_page = f"""<style>
@page :first {{
    margin: 0;
}}
</style>
<div style="position: relative; height: 100vh; overflow: hidden; width: 100%; box-sizing: border-box;">
    <img src="data:image/jpeg;base64,{encoded_string}" style="position: absolute; top: -10vh; left: -25%; height: 120vh; width: auto; opacity: 0.18; z-index: -2; max-width: none;" />
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.6) 100%); z-index: -1;"></div>
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: flex-end; padding-right: 12%; text-align: right; box-sizing: border-box;">
        <h1 style="border: none; font-size: 3.8em; margin-bottom: 0; text-align: right; line-height: 1.1;">Byte Pair Encoding</h1>
        <h2 style="border: none; font-size: 1.8em; margin-top: 15px; color: var(--text-color); font-weight: 300; text-align: right; line-height: 1.3;">A Complete Walkthrough<br>from Scratch</h2>
        <p style="margin-top: 50px; font-size: 1.4em; font-weight: 500;">By Lydia Pedersen</p>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""

copyright_page = """<div style="height: calc(100vh - 50mm); display: flex; flex-direction: column; justify-content: flex-end; font-size: 0.8em; color: var(--secondary-color);">
<p><strong>Byte Pair Encoding: A Complete Walkthrough from Scratch</strong></p>
<p>Copyright &copy; 2026 Lydia Pedersen. All rights reserved.</p>
<p>No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.</p>
</div>
<div style="page-break-after: always;"></div>
"""

toc = "<h1 style='border: none; text-align: left;'>Table of Contents</h1>\n<ul style='list-style-type: none; padding: 0; font-size: 0.9em;'>\n"

# --- Helpers ---
def escape_mermaid(match):
    mermaid_content = match.group(0)
    mermaid_content = mermaid_content.replace('<BOS>', '&lt;BOS&gt;').replace('<EOS>', '&lt;EOS&gt;').replace('<PAD>', '&lt;PAD&gt;')
    return mermaid_content

# --- Process chapters ---
content_bodies = []
for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove download CTA links from the ebook build
    content = re.sub(r'<p><em>Prefer to read this seamlessly offline\?.*?</em></p>\n*', '', content, flags=re.IGNORECASE)
    
    # Part -> Chapter renaming
    content = re.sub(r'# Part (\d+):', r'# Chapter \1:', content)
    content = re.sub(r'\bPart (\d+)\b', r'Chapter \1', content)
    content = re.sub(r'\bpart (\d+)\b', r'chapter \1', content)
    
    # Escape mermaid HTML-like tags
    content = re.sub(r'```mermaid.*?```', escape_mermaid, content, flags=re.DOTALL)
    
    # Extract title for TOC and anchor
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        anchor = title.lower().replace(' ', '-').replace(':', '').replace('&', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '')
        toc += f"<li style='margin-bottom: 8px;'><a href='#{anchor}' style='color: var(--primary-color); text-decoration: none;'>{title}</a></li>\n"
        content = re.sub(r'^#\s+(.+)$', lambda m: f'<h1 id="{anchor}">{title}</h1>', content, count=1, flags=re.MULTILINE)
        
    # Colon-context sticking (prevent page breaks between intro text and math/code)
    content = re.sub(r'(:)\n+(\s*```)', r'\1\n<div style="page-break-after: avoid;"></div>\n\n\2', content)
    content = re.sub(r'(:)\n+(\s*\$\$)', r'\1\n<div style="page-break-after: avoid;"></div>\n\n\2', content)
    
    # Diagram orphan prevention
    blocks = content.split('\n\n')
    for i in range(len(blocks)):
        if '```mermaid' in blocks[i] and i > 0:
            if not blocks[i-1].strip().startswith(('<', '#', '```')):
                blocks[i-1] = '<div style="page-break-inside: avoid;">\n\n' + blocks[i-1]
                blocks[i] = blocks[i] + '\n\n</div>'
    content = '\n\n'.join(blocks)
    
    content_bodies.append(content)

toc += "</ul>\n"

# --- Write frontmatter.md ---
frontmatter_content = title_page + copyright_page + toc
with open(frontmatter_file, 'w') as f:
    f.write(frontmatter_content)
print("Wrote frontmatter.md")

# --- Write body.md ---
body_content = ""
for i, body in enumerate(content_bodies):
    if i > 0:
        body_content += '\n\n<div style="page-break-before: always;"></div>\n\n'
    body_content += body

# Inject CSS for pill box styling to match the blog
body_content += """
<style>
.trace-container code {
  color: #8b4f5a !important;
  background-color: #ffffff !important;
  border: 1px solid #e0c6cb !important;
  border-radius: 0.4em !important;
  padding: 0.2rem 0.4rem !important;
}
.trace-container table code {
  border-radius: 100px !important;
  padding: 4px 10px !important;
}
@media (prefers-color-scheme: dark) {
  .trace-container code {
    color: #e6b3bc !important;
    background-color: #2b1d20 !important;
    border: 1px solid #6b4d53 !important;
  }
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
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"ERROR generating frontmatter.pdf: {result.stderr}")
    exit(1)
print("  Done.")

print("Generating body.pdf (with page numbers starting at 1)...")
result = subprocess.run(
    ['node', generate_pdf, body_file, body_pdf, 'true'],
    cwd=scripts_dir,
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"ERROR generating body.pdf: {result.stderr}")
    exit(1)
print("  Done.")

# --- Merge PDFs ---
print("Merging frontmatter.pdf + body.pdf -> tokenization-ebook-v1.0.pdf...")
from pypdf import PdfWriter
merger = PdfWriter()
merger.append(frontmatter_pdf)
merger.append(body_pdf)
merger.write(final_pdf)
merger.close()
print(f"  Done. Final ebook: {final_pdf}")
