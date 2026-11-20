#!/usr/bin/env python3
"""
Two-volume ebook assembly, width-audit, and PDF build pipeline for the Signal Integrity series.
Builds:
  - Volume 1 (Chapters 1 to 5): assets/docs/signal-integrity-vol1-ebook-v2.0.pdf
  - Volume 2 (Chapters 6 to 21): assets/docs/signal-integrity-vol2-ebook-v1.0.pdf
"""
import base64
import os
import re
import subprocess
import sys

directory = os.path.dirname(os.path.abspath(__file__))
portfolio_root = os.path.abspath(os.path.join(directory, '..', '..', '..', '..'))
if not os.path.exists(os.path.join(portfolio_root, 'assets', 'images', 'signal_integrity_cover.jpg')):
    portfolio_root = os.path.abspath(os.path.join(directory, '..', '..', '..'))
scripts_dir = os.path.expanduser('~/.gemini/config/skills/pdf_generator/scripts')

frontmatter_file = os.path.join(directory, 'frontmatter.md')
body_file = os.path.join(directory, 'body.md')
body_audit_file = os.path.join(directory, 'body_audit.md')
frontmatter_pdf = os.path.join(directory, 'frontmatter.pdf')
body_pdf = os.path.join(directory, 'body.pdf')

VOLUMES = [
    {
        'key': 'vol1',
        'output_filename': 'signal-integrity-vol1-ebook-v2.0.pdf',
        'subtitle_html': 'Volume 1: Wave and Loss Foundations',
        'edition_label': 'Expanded Second Edition',
        'copyright_title': 'Signal Integrity Volume 1: Wave and Loss Foundations (Expanded Second Edition)',
        'start_chapter': 1,
        'toc_lead_note': '',
        'toc_trail_note': (
            "<p style='margin-top: 16px; color: var(--secondary-color); font-style: italic;'>"
            "Parts 2 through 6 (Chapters 6 to 21: Measurement, SerDes, and Coherent Optics) continue in "
            "<a href='https://lyd1acla1r3.github.io/assets/docs/signal-integrity-vol2-ebook-v1.0.pdf' "
            "style='color: var(--primary-color); text-decoration: none;'>"
            "Signal Integrity Volume 2: Measurement, SerDes, and Coherent Optics (Concise First Edition)</a>.</p>\n"
        ),
        'parts': [
            {
                'id': 1,
                'title': 'Wave and Loss Foundations',
                'files': [
                    '01_Wave_Propagation_and_Transmission_Lines.md',
                    '02_Frequency_Content_of_Digital_Signals.md',
                    '03_Impedance_Reflections_and_Termination.md',
                    '04_Inductance_Magnetic_Coupling_and_Crosstalk.md',
                    '05_Skin_Effect_and_Dielectric_Loss.md',
                ],
            },
        ],
    },
    {
        'key': 'vol2',
        'output_filename': 'signal-integrity-vol2-ebook-v1.0.pdf',
        'subtitle_html': 'Volume 2: Measurement, SerDes,<br>and Coherent Optics',
        'edition_label': 'Concise First Edition',
        'copyright_title': 'Signal Integrity Volume 2: Measurement, SerDes, and Coherent Optics (Concise First Edition)',
        'start_chapter': 6,
        'toc_lead_note': (
            "<p style='margin-bottom: 14px; color: var(--secondary-color); font-style: italic;'>"
            "Part 1 (Chapters 1 to 5: Wave and Loss Foundations) is published separately in "
            "<a href='https://lyd1acla1r3.github.io/assets/docs/signal-integrity-vol1-ebook-v2.0.pdf' "
            "style='color: var(--primary-color); text-decoration: none;'>"
            "Signal Integrity Volume 1: Wave and Loss Foundations (Expanded Second Edition)</a>.</p>\n"
        ),
        'toc_trail_note': '',
        'parts': [
            {
                'id': 2,
                'title': 'Discontinuities and Signal Integrity Measurement',
                'files': [
                    '06_Return_Path_Dynamics_and_Parasitic_Effects.md',
                    '07_Time_Domain_Reflectometry.md',
                    '08_S_Parameters_and_VNA.md',
                    '09_Smith_Charts.md',
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
                    '19_Light_and_the_Electro_Optic_Effect.md',
                    '20_Mach_Zehnder_IQ_Modulators.md',
                    '21_Wideband_Signal_Analysis.md',
                ],
            },
        ],
    },
]

# --- Cover and Part divider images ---
cover_image_path = os.path.join(portfolio_root, 'assets', 'images', 'signal_integrity_cover.jpg')
with open(cover_image_path, 'rb') as image_file:
    encoded_cover = base64.b64encode(image_file.read()).decode('utf-8')

images_dir = os.path.join(portfolio_root, 'assets', 'images')
part_images = {}
part_image_files = {
    1: 'si_part1_electromagnetic.jpg',
    2: 'si_part2_measurement.jpg',
    3: 'si_part3_jitter.jpg',
    4: 'si_part4_equalization.jpg',
    5: 'si_part5_serdes.jpg',
    6: 'si_part6_coherent_optics.jpg',
}
for p_id, img_name in part_image_files.items():
    candidate_path = os.path.join(images_dir, img_name)
    if not os.path.exists(candidate_path):
        fallback_name = 'coherent_optics_cover.jpg' if p_id == 6 else 'signal_integrity_cover.jpg'
        candidate_path = os.path.join(images_dir, fallback_name)
    with open(candidate_path, 'rb') as f:
        part_images[p_id] = base64.b64encode(f.read()).decode('utf-8')


def cleanup_temp_files():
    if '--keep-temp' in sys.argv:
        return
    for temp_path in (frontmatter_file, body_file, body_audit_file, frontmatter_pdf, body_pdf):
        if os.path.exists(temp_path):
            os.remove(temp_path)


def build_volume(vol):
    parts = vol['parts']
    parts_by_id = {p['id']: p for p in parts}
    final_pdf = os.path.join(portfolio_root, 'assets', 'docs', vol['output_filename'])

    print(f"\n=== Building {vol['output_filename']} ===")
    try:
        title_page = f"""<style>
@page :first {{
    margin: 0;
}}
</style>
<div style="position: relative; height: 100vh; overflow: hidden; width: 100%; box-sizing: border-box;">
    <img src="data:image/jpeg;base64,{encoded_cover}" style="position: absolute; top: -10vh; left: -25%; height: 120vh; width: auto; opacity: 0.32; z-index: -2; max-width: none;" />
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.6) 100%); z-index: -1;"></div>
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: flex-end; padding-right: 12%; text-align: right; box-sizing: border-box;">
        <h1 style="border: none; font-size: 3.8em; margin-bottom: 0; text-align: right; line-height: 1.1;">Signal<br>Integrity</h1>
        <h2 style="border: none; font-size: 1.8em; margin-top: 15px; color: var(--text-color); font-weight: 300; text-align: right; line-height: 1.3;">{vol['subtitle_html']}</h2>
        <h3 style="border: none; font-size: 1.5em; margin-top: 10px; color: var(--secondary-color); font-weight: 400; text-align: right; font-style: italic;">{vol['edition_label']}</h3>
        <p style="margin-top: 50px; font-size: 1.4em; font-weight: 500;">By Lydia Pedersen</p>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""

        copyright_page = f"""<div style="height: calc(100vh - 50mm); display: flex; flex-direction: column; justify-content: flex-end; font-size: 0.8em; color: var(--secondary-color);">
<p><strong>{vol['copyright_title']}</strong></p>
<p>Copyright &copy; 2026 Lydia Pedersen. All rights reserved.</p>
<p>No part of this publication may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the publisher, except in the case of brief quotations embodied in critical reviews and certain other noncommercial uses permitted by copyright law.</p>
</div>
"""

        toc = "<h1 style='border: none; text-align: left;'>Table of Contents</h1>\n"
        toc += "<div style='font-size: 0.9em;'>\n"
        if vol['toc_lead_note']:
            toc += vol['toc_lead_note']

        chapter_num = vol['start_chapter'] - 1
        toc_entries = []

        for part in parts:
            part_anchor = f"part-{part['id']}"
            toc += (
                f"<p style='margin-top: 16px; margin-bottom: 4px; font-weight: bold; font-size: 1.1em;'>"
                f"<a href='#{part_anchor}' style='color: var(--primary-color); text-decoration: none;'>"
                f"Part {part['id']}: {part['title']}</a></p>\n"
            )
            toc += "<ul style='list-style-type: none; padding-left: 20px; margin-top: 0;'>\n"

            for filename in part['files']:
                chapter_num += 1
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else filename
                anchor = (
                    title.lower()
                    .replace(' ', '-')
                    .replace(':', '')
                    .replace('&', '')
                    .replace('(', '')
                    .replace(')', '')
                    .replace(',', '')
                    .replace('.', '')
                    .replace('/', '-')
                )

                toc += (
                    f"<li style='margin-bottom: 6px;'>"
                    f"<a href='#{anchor}' style='color: var(--primary-color); text-decoration: none;'>"
                    f"Chapter {chapter_num}: {title}</a></li>\n"
                )
                toc_entries.append({
                    'part_id': part['id'],
                    'chapter_num': chapter_num,
                    'title': title,
                    'anchor': anchor,
                    'filename': filename,
                })

            toc += "</ul>\n"

        if vol['toc_trail_note']:
            toc += vol['toc_trail_note']
        toc += "</div>\n"

        filename_to_anchor = {entry['filename']: '#' + entry['anchor'] for entry in toc_entries}

        content_bodies = []
        current_part_id = 0

        for entry in toc_entries:
            if entry['part_id'] != current_part_id:
                current_part_id = entry['part_id']
                part = parts_by_id[current_part_id]
                part_divider = f"""<div style="page-break-before: always;"></div>
<a id="part-{part['id']}"></a>
<div style="position: relative; height: 100vh; overflow: hidden; width: 100%; box-sizing: border-box;">
    <img src="data:image/jpeg;base64,{part_images[part['id']]}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.25; z-index: -2;" />
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(to bottom, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.7) 50%, rgba(255,255,255,0.3) 100%); z-index: -1;"></div>
    <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
        <p style="font-size: 1.2em; color: var(--secondary-color); margin-bottom: 10px; letter-spacing: 3px; text-transform: uppercase;">Part {part['id']}</p>
        <h1 style="border: none; font-size: 2.8em; margin: 0 auto; line-height: 1.2; max-width: 50%; text-align: center;">{part['title']}</h1>
    </div>
</div>
<div style="page-break-after: always;"></div>
"""
                content_bodies.append(part_divider)

            filepath = os.path.join(directory, entry['filename'])
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove download CTA links
            content = re.sub(
                r'<p><em>Prefer to read(?: this)?(?:\s+seamlessly)? offline\?.*?</em></p>\n*',
                '',
                content,
                flags=re.IGNORECASE,
            )

            # Remove SUMMARY comments
            content = re.sub(r'<!--\s*SUMMARY:[\s\S]*?-->\n*', '', content)

            # Strip source extraction links if present
            content = re.sub(
                r'^-\s*\[extraction_[^\]]*\]\(\.\./\.\./source_extractions/[^)]*\).*$\n?',
                '',
                content,
                flags=re.MULTILINE,
            )
            content = re.sub(r'\*\*Source Extractions:\*\*\s*\n(?=\s*\n|\*\*|\Z)', '', content)

            # Convert intra-volume .md links to #anchor and cross-volume .md links to live web URLs
            def resolve_md_link(m):
                stem = m.group(1)
                frag = m.group(2) or ''
                basename = stem + '.md'
                if basename in filename_to_anchor:
                    return '](' + filename_to_anchor[basename] + ')'
                return f'](https://lyd1acla1r3.github.io/blog/signal-integrity-{stem}.html{frag})'

            content = re.sub(
                r'\]\((?:\.\./[^)\s]*?/)?(\d{2}_[^)#\s]*?)\.md(#[^)\s]*)?\)',
                resolve_md_link,
                content,
            )

            # Add anchor before chapter title
            content = re.sub(
                r'^#\s+(.+)$',
                lambda m: f'<a id="{entry["anchor"]}"></a>\n# Chapter {entry["chapter_num"]}: {m.group(1)}',
                content,
                count=1,
                flags=re.MULTILINE,
            )

            # Inline math + punctuation sticking
            content = re.sub(
                r'(\x24[^\x24\n]+?\x24)([.,;:)\]])',
                r'<span style="white-space: nowrap">\1\2</span>',
                content,
            )

            # Prevent orphaned ##/###/#### headings, orphaned colon-intro lines before equations/code,
            # and orphaned intro paragraphs before Mermaid diagrams using atomic break-inside wrappers
            blocks = content.split('\n\n')
            grouped_blocks = []
            idx = 0
            while idx < len(blocks):
                stripped = blocks[idx].strip()
                if re.match(r'^#{2,4}\s+', stripped):
                    end = idx + 1
                    while end < len(blocks) and re.match(r'^#{2,4}\s+', blocks[end].strip()):
                        end += 1
                    group_end = end
                    if group_end < len(blocks) and not blocks[group_end].strip().startswith('<div style="page-break-before:'):
                        first_body = blocks[group_end].strip()
                        group_end += 1
                        if group_end < len(blocks):
                            next_blk = blocks[group_end].strip()
                            if '```mermaid' in next_blk or (
                                first_body.endswith(':')
                                and (next_blk.startswith('$$') or (next_blk.startswith('```') and len(next_blk.splitlines()) <= 20))
                            ):
                                group_end += 1
                    grouped_blocks.append(
                        '<div class="heading-keep">\n\n'
                        + '\n\n'.join(blocks[idx:group_end])
                        + '\n\n</div>'
                    )
                    idx = group_end
                elif (
                    idx + 1 < len(blocks)
                    and not stripped.startswith(('<', '#', '```', '$$', '|'))
                    and (
                        '```mermaid' in blocks[idx + 1]
                        or (
                            stripped.endswith(':')
                            and (
                                blocks[idx + 1].strip().startswith('$$')
                                or (blocks[idx + 1].strip().startswith('```') and len(blocks[idx + 1].splitlines()) <= 20)
                            )
                        )
                    )
                ):
                    grouped_blocks.append(
                        '<div class="heading-keep">\n\n'
                        + blocks[idx]
                        + '\n\n'
                        + blocks[idx + 1]
                        + '\n\n</div>'
                    )
                    idx += 2
                else:
                    grouped_blocks.append(blocks[idx])
                    idx += 1
            content = '\n\n'.join(grouped_blocks)

            content_bodies.append(content)

        frontmatter_content = title_page + copyright_page
        with open(frontmatter_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter_content)
        print("  Wrote frontmatter.md")

        body_content = toc + '\n\n'
        for body in content_bodies:
            if not body.strip().startswith('<div style="page-break-before: always;">'):
                body_content += '\n\n<div style="page-break-before: always;"></div>\n\n'
            body_content += body

        style_tail = """
<style>
h4 {
  color: var(--secondary-color);
  font-size: 1.05em;
  font-weight: 600;
  margin-top: 16px;
  margin-bottom: 8px;
}
.heading-keep {
  page-break-inside: avoid;
  break-inside: avoid;
}
.katex-display {
  font-size: 0.9em !important;
}
mjx-container[display="true"] {
  font-size: 95% !important;
  overflow-x: hidden !important;
}
@media print {
  h1, h2, h3, h4 {
    page-break-after: avoid !important;
    break-after: avoid !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
  .heading-keep {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }
}
</style>
"""
        body_content += style_tail
        with open(body_file, 'w', encoding='utf-8') as f:
            f.write(body_content)
        print("  Wrote body.md")

        audit_widths = os.path.join(scripts_dir, 'audit_widths.mjs')
        generate_pdf = os.path.join(scripts_dir, 'generate_pdf.mjs')

        # Pack assembled chapter blocks into <=18k-word slices so MathJax SVG payloads stay well under Puppeteer's 30s setContent cap
        chapter_only_bodies = [b for b in content_bodies if '<a id="part-' not in b]
        slices = []
        cur_slice = []
        cur_words = 0
        for block in chapter_only_bodies:
            w = len(block.split())
            if cur_slice and cur_words + w > 18000:
                slices.append(cur_slice)
                cur_slice = [block]
                cur_words = w
            else:
                cur_slice.append(block)
                cur_words += w
        if cur_slice:
            slices.append(cur_slice)

        with open(audit_widths, 'r', encoding='utf-8') as af:
            audit_widths_esm = (
                af.read()
                .replace(
                    "puppeteer.launch({ headless: 'new' })",
                    "puppeteer.launch({ headless: 'new', protocolTimeout: 600000 })",
                )
                .replace(
                    "{ waitUntil: 'networkidle0' }",
                    "{ waitUntil: 'load', timeout: 0 }",
                )
            )

        for s_idx, s_blocks in enumerate(slices, 1):
            slice_content = '\n\n'.join(s_blocks) + style_tail
            with open(body_audit_file, 'w', encoding='utf-8') as f:
                f.write(slice_content)
            label = f"{vol['key']} slice {s_idx}/{len(slices)}"
            print(f"  Running audit_widths.mjs on {label}...")
            audit_res = subprocess.run(
                ['node', '--input-type=module', '-', body_audit_file],
                input=audit_widths_esm,
                cwd=scripts_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            last_line = audit_res.stdout.strip().splitlines()[-1] if audit_res.stdout.strip() else ''
            print(f"    -> {last_line}")
            if audit_res.returncode != 0:
                print(f"ERROR in audit_widths.mjs ({label}):\n{audit_res.stdout}\n{audit_res.stderr}")
                sys.exit(audit_res.returncode)
        if os.path.exists(body_audit_file):
            os.remove(body_audit_file)

        with open(generate_pdf, 'r', encoding='utf-8') as gf:
            gen_pdf_esm = gf.read().replace(
                "puppeteer.launch({ headless: 'new' })",
                "puppeteer.launch({ headless: 'new', protocolTimeout: 600000 })",
            )

        print("  Generating frontmatter.pdf (no page numbers)...")
        res_fm = subprocess.run(
            ['node', '--input-type=module', '-', frontmatter_file, frontmatter_pdf, 'false'],
            input=gen_pdf_esm,
            cwd=scripts_dir,
            capture_output=True,
            text=True,
            timeout=180,
        )
        if res_fm.returncode != 0:
            print(f"ERROR generating frontmatter.pdf: {res_fm.stderr}")
            sys.exit(1)

        print("  Generating body.pdf (page numbers starting at 1)...")
        res_body = subprocess.run(
            ['node', '--input-type=module', '-', body_file, body_pdf, 'true'],
            input=gen_pdf_esm,
            cwd=scripts_dir,
            capture_output=True,
            text=True,
            timeout=900,
        )
        if res_body.returncode != 0:
            print(f"ERROR generating body.pdf: {res_body.stderr}")
            sys.exit(1)

        print(f"  Merging frontmatter.pdf + body.pdf -> {vol['output_filename']}...")
        from pypdf import PdfWriter
        merger = PdfWriter()
        merger.append(frontmatter_pdf)
        merger.append(body_pdf)
        merger.write(final_pdf)
        merger.close()
        print(f"  Done. Final ebook: {final_pdf}")
    finally:
        cleanup_temp_files()


def main():
    selected = VOLUMES
    if '--vol1' in sys.argv and '--vol2' not in sys.argv:
        selected = [v for v in VOLUMES if v['key'] == 'vol1']
    elif '--vol2' in sys.argv and '--vol1' not in sys.argv:
        selected = [v for v in VOLUMES if v['key'] == 'vol2']

    for vol in selected:
        build_volume(vol)


if __name__ == '__main__':
    main()
