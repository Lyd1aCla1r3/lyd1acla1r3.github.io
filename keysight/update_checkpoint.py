import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/session_checkpoint.md', 'r', encoding='utf-8') as f:
    checkpoint = f.read()

# Update current session and next steps
new_work = """## Work Accomplished in Current Session

### UI Refinements & Structural Grids
1.  **Adaptive Grid System:** Ripped out hardcoded grid ratios for the bento overlays in both `instruments.html` and `standards.html`. 
    *   **Instruments:** Dynamically computed character density ratios for the "When to Use" and "When Not to Use" cards to eliminate vertical whitespace while maintaining equal heights.
    *   **Standards:** Re-architected `.detail-bento` to use Flexbox and precise `calc()` widths, allowing multiple rows in the same container to independently adapt their proportions (e.g., 62%/38% vs 46%/54%). Applied a square root softening curve to character counts to prevent extreme wrapping in narrow columns.
2.  **Typography & White Space:** 
    *   Added a subtle 1px themed border (`rgba(var(--theme-rgb), 0.15)`) beneath every paragraph and list item across all overlays to break up dense walls of text.
    *   Increased right padding on the left-column text blocks (`.standard-row > div:first-child`) to a massive 4rem (`var(--ks-space-2xl)`) buffer, ensuring titles wrap early without crowding the description text.
3.  **Hyphenation Protection:** Replaced all standard hyphens (`-`) in the subtitles with non-breaking HTML entities (`&#8209;`) to physically prevent the browser from snapping phrases like `10GBASE-T1`, `Co-Packaged`, or `D-PHY` in half across lines.
4.  **Header Title Updates:** Updated `<title>` tags and `<h1>` elements for both pages to read "Hardware Standards Deep Dive" and "Instruments Deep Dive".

### Content Accuracy & Consistency
1.  **Standards Subtitles:** Synchronized the main grid subtitles with the exact acronyms detailed in the overlays (e.g., swapping out internal taxonomy "DDR (Design and Test)" for `DDR5, LPDDR5X, GDDR6, HBM3`, and dropping MIPI version numbers for cleanliness).
2.  **Instrumentation Subtitles:** Stripped all software suite references (`PLTS`, `89600 VSA Software`) from the instrument subtitles so they purely reflect hardware. Crucially, identified and replaced a major error where Teledyne LeCroy competitor equipment (`PXP-Series`) was listed, swapping it out for Keysight's actual flagship PCIe protocol analyzers (`P5500 Series, U4301B`).

---

## Next Steps
*   **Handoff:** The deep dives are polished, historically accurate, technically dense, and stylistically constrained to the user's specific branding rules. Await user confirmation to run the handoff script for the next session.
"""

checkpoint = re.sub(r'## Work Accomplished in Current Session.*', new_work, checkpoint, flags=re.DOTALL)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/session_checkpoint.md', 'w', encoding='utf-8') as f:
    f.write(checkpoint)
