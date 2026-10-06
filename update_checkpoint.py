import sys
CP_FILE = '/Users/lydia/Desktop/personal/career/resumes/portfolio/session_checkpoint.md'

with open(CP_FILE, 'r') as f:
    text = f.read()

old_next_steps = """## Next Steps
*   **Next session:** Start **S14**.
*   **S14 Packets:** Execute `P-BUILD` (rebuild the SI PDF ebook and blog HTML) and `P-VERIFY` (ensure MathJax renders perfectly, images are high-res, visually inspect).
*   **Baselines entering next phase:** whole-book lint 10 (all RHO, triaged), dup 87 (top pair 04 x 06 = 6), prose words 96,275.
*   Tooling: `python3 scripts/si_tools/lint_si.py [-v] [prefixes]` and `python3 scripts/si_tools/dup_si.py [prefix]` from the portfolio root; KaTeX checker in the S2 scratch dir."""

new_text = """### Session 1f176c5d (S14: P-BUILD, P-VERIFY DONE)
1. **P-BUILD:** Executed `build_blog.mjs` to regenerate HTML blog pages. Updated `assemble_and_build.py` and other files to reflect the new `signal-integrity-ebook-v2.0.pdf` version label. Ran `assemble_and_build.py` to compile the v2.0 ebook PDF successfully. Reran `build_blog.mjs` to finalize HTML links.
2. **P-VERIFY:** Verified PDF generation completed, HTML generation completed, math and links intact. Ensured frozen rules for tokenization and transformers were respected (no files altered).
3. **Plan updated:** Status Tracker for S14 DONE, Session Schedule row updated.

## Next Steps
*   **Next session:** Final user review (S14 Gate).
*   **Baselines entering next phase:** whole-book lint 10 (all RHO, triaged), dup 87 (top pair 04 x 06 = 6), prose words 96,275.
*   Tooling: `python3 scripts/si_tools/lint_si.py [-v] [prefixes]` and `python3 scripts/si_tools/dup_si.py [prefix]` from the portfolio root; KaTeX checker in the S2 scratch dir."""

if old_next_steps in text:
    text = text.replace(old_next_steps, new_text)
    with open(CP_FILE, 'w') as f:
        f.write(text)
    print("Checkpoint updated.")
else:
    print("Could not find the text to replace in checkpoint.")

