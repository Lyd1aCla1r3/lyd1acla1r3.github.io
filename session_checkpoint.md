# Session Checkpoint

## User Context & Preferences

### User Background
*   **Lydia Pedersen.** 20 years engineering. 15 years hardware validation (Amazon Lab126, Oracle, Broadcom/LSI), 5 years AI pipeline architecture and technical writing (Gravitee, Entando). B.S. Physics, UC Irvine.
*   **Personal branding:** "AI PIPELINE ARCHITECT & DOCUMENTATION ENGINEER" (generalized) and "SIGNAL INTEGRITY ENGINEER & AI SYSTEMS ARCHITECT" (hardware-focused, Keysight-tailored).
*   **Philosophy:** Translating ambiguous human intention into quasi-deterministic programmatic workflows. Hardware validation rigor applied to AI systems.
*   **Current interview prep:** Keysight Digital Solutions Engineer role, advancing to panel interview (4-person panel, recorded, 20-minute candidate-driven presentation + 60-75 min Q&A).

### Writing Rules (MANDATORY)
*   **No em dashes.** Ever.
*   **No contractions** in formal writing.
*   **No AI cliches** (delve, tapestry, leverage, harness, synergy, game-changing, cutting-edge, unlock, empower, seamless).
*   **No past employer proper nouns** in public-facing materials (except as job headers).
*   **No short punchy reveal sentences**, tagline-style declarations, parallel fragment pairs, or "Not X. It is Y." constructions.
*   **Lowercase internal systems** (except "AI").
*   **No generic idioms** or folksy talk.
*   **No mechanical transitions** (For example, To address this, Ultimately, Moreover, Furthermore, Additionally, In conclusion).
*   **No dependent clause openers** at sentence start. Approved strict scope (2026-10-04): Because, Since, Given that, Knowing that, If, When, As, Once, While, After. Worked-example conditionals become "Assume..." or main-clause statements.
*   **Philosophical framing:** lead with convictions and motivations, not feature lists.
*   **Editing posture:** Preserve the user's voice. Do NOT rewrite prose without strict adherence to rules.
*   **No forced analogies or assumptions or cutting corners.** Technical but fully described for laymen to understand mechanics.
*   **Reinforcement, not duplication (SI series):** explain each concept fully once at its home chapter; elsewhere reference it or reinterpret it to connect the dots.
*   **Consistent derivation depth (SI series):** governing equations are derived step by step, matching the reflection coefficient derivation.
*   **Scoping rule for standards pages:** Standards pages describe architecture and design rationale. Physics explanations belong in the SI blog series. Connect the dots as context, do not pivot to explaining the physical phenomenon.

### Acronym Scoping Rule (Keysight Domain)
*   **Do NOT spell out acronyms used across multiple Keysight pages** (CTLE, DFE, BERT, VNA, DCA-X, OMA, TDECQ, FFT, IFFT, S-parameter, CDR, ISI, BER, PRBS, EVM, OSNR, TDR).
*   **DO spell out acronyms that appear only in the instruments section** and are esoteric (LTSSM, OCWR, DP-QPSK, DP-16QAM, IM/DD).
*   **Exception:** industry shorthand (RTO, TX, RX, ED, O/E) allowed in instrument overlays.

### Resume Constraint
*   **Must NOT exceed two pages.** Non-negotiable.

### Blog Series Freeze (from portfolio/AGENTS.md)
*   **CRITICAL RULE:** NEVER modify files in `blog/content/series/tokenization/*` or `blog/content/series/transformers/*`, their PDFs, or their build scripts. Restore points in AGENTS.md.
*   The Signal Integrity series is NOT frozen. It is under active revision per the plan below.

### Visual Preferences (SI ebook)
*   Loves the palette: deep navy/near-black background, cyan glow, copper/salmon accents.
*   Rejects abstract or interpretive imagery. Visuals must be what you would see on a bench, an instrument screen, or in a textbook.

---

## Resource Locations

### Signal Integrity Revision (ACTIVE)
*   **Living revision plan (BINDING, read every session):** `/Users/lydia/.gemini/antigravity/brain/628163fe-9db3-499c-9b7f-f47c1314aafa/si_ebook_revision_plan.md`
*   **Audit reports (exact quotes and line numbers, pre-S1 file names):** `/Users/lydia/.gemini/antigravity/brain/628163fe-9db3-499c-9b7f-f47c1314aafa/scratch/audit_reports.md`
*   **Q&A extraction source (session 6a9d1c47, "UI layout and code review"):** `/Users/lydia/.gemini/antigravity/brain/628163fe-9db3-499c-9b7f-f47c1314aafa/scratch/prev_qa.md`
*   **Series directory:** `/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/signal-integrity/`
*   **Ebook build script:** `.../signal-integrity/assemble_and_build.py` (`parts` list now 21 chapters, Part 1 = 01-06, Part 2 = 07-09, Part 6 = 19-21)
*   **Blog build:** `/Users/lydia/Desktop/personal/career/resumes/portfolio/build_blog.mjs` (`siParts` near the top; SI-only `.md` href rewrite)
*   **SI tooling:** `scripts/si_tools/lint_si.py`, `scripts/si_tools/dup_si.py`, `scripts/si_tools/p2_restructure.py` (one-shot, already run)
*   **Baseline restore point (pre-revision SI files):** git commit `a336477ad7223f293e875627a90e2c4a27352993`; v1.0 PDF archive at `assets/docs/archive/`
*   **Current ebook:** `assets/docs/signal-integrity-ebook-v1.0.pdf` (target v2.0/v2.1)
*   **Current images:** `assets/images/signal_integrity_cover.jpg`, `assets/images/si_part1..6_*.jpg`
*   **Editing the plan from a new conversation:** the edit tools refuse to write into conversation 628163fe's brain directory. Edit the plan with a Python exact-replace script run in the shell. Preferred helper (S3): `/Users/lydia/.gemini/antigravity/brain/c17722a0-6aff-409c-ae4f-433c03c03731/scratch/plan_multi.py <updates.py>`, where `updates.py` defines `REPS = [(old, new), ...]` (each `old` must match exactly once; examples: `upd_c03.py` and `upd_end.py` in the same dir). Older single-replace helper: `/Users/lydia/.gemini/antigravity/brain/6f6ab956-b6e4-44b6-af45-e913a4dffd21/scratch/plan_edit.py <old.txt> <new.txt>`. Plan backups: `.../6f6ab956-.../scratch/plan_backup_pre_S2_end.md` and `.../c17722a0-.../scratch/plan_backup_pre_S3.md`.
*   **S5 helpers:** plan update scripts and number checks in `/Users/lydia/.gemini/antigravity/brain/44e0fc7b-4ec7-47d9-8304-04fc113d3f58/scratch/` (`upd_s5.py`, `c07_nums.py`, backup `plan_backup_pre_S5.md`). Plan edits still use `plan_multi.py` from the S3 dir.
*   **S7 helpers:** plan update scripts (`upd_c10.py`, `upd_s7.py`), the number check (`c10_c11_nums.py`) and backup `plan_backup_pre_S7.md` in `/Users/lydia/.gemini/antigravity/brain/2fb9af03-15ac-424a-8b72-382f48cc198f/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **S8 helpers:** plan update scripts (`upd_c12.py`, `upd_s8.py`), number checks (`c12_nums.py`, `c13_nums.py`) and backup `plan_backup_pre_S8.md` in `/Users/lydia/.gemini/antigravity/brain/73b14b8a-a306-45b7-aa0b-f0b8fd9d9a98/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **S9 helpers:** plan update scripts (`upd_c14.py`, `upd_s9.py`), number checks (`c14_c15_nums.py`, `c14_train.py`) and backup `plan_backup_pre_S9.md` in `/Users/lydia/.gemini/antigravity/brain/ae36597a-2bb9-4f5f-b1a5-6f151e15e8e6/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **S6 helpers:** plan update scripts (`upd_c08.py`, `upd_s6.py`), number checks (`c08_nums.py`, `c09_nums.py`) and backup `plan_backup_pre_S6.md` in `/Users/lydia/.gemini/antigravity/brain/b7b9b6bc-0836-48c9-92d1-9b26a5b34d09/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **S10 helpers:** plan update scripts (`upd_c16.py`, `upd_s10.py`), number checks (`c16_nums.py`, `c17_nums.py`) and backup `plan_backup_pre_S10.md` in `/Users/lydia/.gemini/antigravity/brain/061bf0dd-b497-40a6-825e-a1b64dc7048d/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **S11 helpers:** plan update scripts (`upd_c18.py`, `upd_c19.py`, `upd_c20.py`, `upd_s11.py`), number checks (`c18_nums.py`, `c19_21_nums.py`) and backup `plan_backup_pre_S11.md` in `/Users/lydia/.gemini/antigravity/brain/978596e2-9167-455c-9b75-61db163db456/scratch/`. Plan edits still use `plan_multi.py` from the S3 dir.
*   **KaTeX parse checker (offline):** `/Users/lydia/.gemini/antigravity/brain/6f6ab956-b6e4-44b6-af45-e913a4dffd21/scratch/katex/check.js` (run `node check.js <absolute chapter.md> ...` from the `katex` directory; katex@0.16.8, matching the blog CDN version).


### Keysight Presentation Design (v2)
*   **Shared CSS/JS:** `css/keysight.css`, `js/keysight.js`
*   **Hub page:** `keysight.html`; child pages in `keysight/` (customer, convergence, architecture, translation, value, close, standards, instruments)
*   **Standards Research Data:** `/Users/lydia/.gemini/antigravity/brain/e97cd174-b5ea-407a-8b00-4130299ad110/standards_research_data.md`
*   **Instrument Deep Dive Plan:** `/Users/lydia/.gemini/antigravity/brain/5107c8bf-6579-4c63-9172-84f7c519070f/instrument_deep_dive_plan.md`
*   **"When Not to Use" Plan:** `/Users/lydia/.gemini/antigravity/brain/11dd77d1-0c56-45f1-a929-4cfabba20839/when_not_to_use_revision_plan.md`
*   **Keysight JD:** `/Users/lydia/Desktop/personal/career/Solutions Engineer - Seattle Area in Everett, Washington | Keysight Technologies, Inc..pdf`
*   **JD Gap Analysis:** `/Users/lydia/.gemini/antigravity/brain/44a0721d-ba14-43bd-be12-6a0b0b7fd847/gap_analysis_and_plan.md`

### Standards Session Documents (Q&A Extractions)
*   Computer Bus: `/Users/lydia/.gemini/antigravity/brain/a8452752-20c3-481c-b7e9-2a85b4e9a027/computer_bus_interfaces_summary.md`
*   Datacenter & Optical: `/Users/lydia/.gemini/antigravity/brain/27a4b6d4-12a9-4682-ab21-cbeda7aa4b82/datacenter_optical_summary.md`
*   Memory: `/Users/lydia/.gemini/antigravity/brain/1104f560-c7a6-46c7-9568-79e993f48880/memory_interfaces_summary.md`
*   Mobile/MIPI: `/Users/lydia/.gemini/antigravity/brain/49dcaa99-dd1e-4b1e-9ef3-c36babdb20f0/mobile_iot_summary.md`
*   Automotive: `/Users/lydia/.gemini/antigravity/brain/8ff9edae-ac19-492a-bbcc-c5962d689204/automotive_networks_summary.md`

---

### Past Accomplishments (Condensed)
1.  **SI Taxonomy & Blog Migration:** 5-folder SI taxonomy from Q&A sessions; v2.0/v3.0 concept-guide PDFs; blog migration.
2.  **Keysight Hub & Child Pages:** bento grids, animated SVG flows, accordion cards, glass dossiers.
3.  **Standards Framework & Deep-Dives:** 5 hardware standard categories mapped to physical layers, Keysight equipment, validation challenges.
4.  **JD Gap Analysis.**
5.  **Coherent Optics Q&A:** integrated into SI series as Part 6.
6.  **Architecture page folder-tab UI; global UI polish.**
7.  **Instrument matrix; standards and instrument overlays revision; adaptive Flexbox bento grids.**
8.  **SI Physics Q&A (session 6a9d1c47):** RHR and skin effect, Ampere/Faraday/Lenz, four induction cases, NEXT/FEXT, S-parameter notation, dB vs dBm, VNA phase, harmonics vs bandwidth, TDR vs VNA R/L/C separation, Fourier synthesis of square waves and step responses.
9.  **SI Series Comprehensive Revision (S1-S15):** Audited and fully rebuilt all 22 chapters to eliminate redundancy, establish single-home concepts, and enforce consistent derivation depth. Fixed 60+ factual errors. Executed rigorous language polish (no em dashes, no contractions, no AI cliches). Regenerated and audited all visuals. Published the finalized v2.0 Signal Integrity ebook and blog pages.
10. **Conceptual Q&A and Extraction Ledger:** Answered 9 conceptual questions across PAM4, CTLE/DFE, and PLL Loop Dynamics, mapping them to Chapters 14, 15, 16, and 17 in a formal integration plan.

---

## Work Accomplished in Current Session
1. **Integrated Conceptual Clarifications (SI Series v2.1):** Executed the Q&A Extraction Plan by integrating all 9 conceptual clarifications directly into the corresponding canonical chapters (Ch14, Ch15, Ch16, Ch17) while strictly adhering to the mandated writing rules (no em dashes, no contractions, no AI cliches, specific dependent clause rules).
2. **Rebuilt Assets:** Re-ran `build_blog.mjs` and `assemble_and_build.py` to compile the updated v2.1 PDF (`assets/docs/signal-integrity-ebook-v2.0.pdf`) and the static site blog files.

---

## Next Steps
*   **Dual Version Publishing:** Figure out how to cleanly publish and display both v1.0 and v2.x of the Signal Integrity ebook as separate "Beginner" and "Advanced" editions on the portfolio. The user will provide detailed requirements in the next session.