# Session Checkpoint (2026-11-20)

## User Context & Preferences

### User Background & Positioning
*   **Lydia Pedersen.** 20 years in engineering: 15 years in high-speed physical-layer hardware validation (`Amazon Lab126`, `Oracle`, `LSI Logic / Broadcom`) and 5 years in production AI pipeline architecture and technical communication (`Gravitee`, `Entando`), plus a B.S. in Physics with Honors (`UC Irvine`, Regents Scholar, Sigma Pi Sigma).
*   **Current Role & Bandwidth Constraint:** Started as **Solutions Engineer at Keysight Technologies** (`Everett, WA / Greater Seattle Area`, Job ID `53867`, official start date **November 9, 2026**, formatted as `Nov 2026 – Present` on Resume and `November 2026 – Present` on LinkedIn). While ramping in her full-time role at Keysight, she **paused interactive chapter-by-chapter Signal Integrity Q&A** after `Block 101` (line `294` of Chapter 5) and executed the **Two-Volume Split with Unified 21-Chapter Web Series** relaunch so `https://lyd1acla1r3.github.io` can return online immediately, while preserving 100% of long-term context to resume interactive Q&A at Chapter 5 (`lines 296–791`, starting at `#### Why Copper Foil Thickness Stops Helping While Trace Width Still Helps`) and Chapters 6–21 whenever time permits.
*   **Canonical Public Links:**
    *   **Portfolio:** `https://lyd1acla1r3.github.io` (Ready for commit, push to `origin/main`, and switching GitHub Pages Source Branch back from `None` to `main` `/ (root)`)
    *   **LinkedIn:** `www.linkedin.com/in/lydiapedersen` (`https://www.linkedin.com/in/lydiapedersen`)
    *   **GitHub:** `https://github.com/Lyd1aCla1r3`
*   **Core Narrative Philosophy:** Focus on the physical-layer standards and measurement methodologies that enable hardware infrastructure to keep pace with emerging computational patterns. Connect software-driven compute workloads to physical-layer validation (signal integrity, compliance, multi-vendor instrumentation, deterministic test automation) and first-principles technical communication.
*   **Frozen Series Rule (`AGENTS.md` & `independent_critique` — CRITICAL):** NEVER modify, edit, or touch any files, scripts, or PDFs in **Tokenization** (`blog/content/series/tokenization/*`, `blog/tokenization-*.html`, `blog/series-tokenization.html`, `assets/docs/tokenization-ebook-v1.0.pdf`, restore commit `c4b59d0ca819c8f738de44a6d296b0e70426eca4`), **Transformers** (`blog/content/series/transformers/*`, `blog/transformers-*.html`, `blog/series-transformers.html`, `assets/docs/transformers-ebook-v1.0.pdf`, restore commit `3de4f4c4765f13814c43afa313cdc4c382bb57c2`), or **Mixture of Experts** (`blog/content/series/mixture-of-experts/*`, `blog/mixture-of-experts-*.html`, `blog/series-mixture-of-experts.html`, `assets/docs/mixture-of-experts-ebook-v1.0.pdf`). Guarded permanently via `FROZEN_SERIES = new Set(['tokenization', 'transformers', 'mixture-of-experts'])` in `build_blog.mjs`.
*   **Master Resume Freeze (`Pedersen_Resume_2026.pdf`):** Leave `Pedersen_Resume_2026` (`.md`/`.html`/`.pdf` and `portfolio/assets/docs/Pedersen_Resume_2026.pdf`) **100% untouched**. Portfolio cards on `index.html` and `ebooks/index.html` bridge its `"21-Chapter Series & 2 Ebook Editions"` wording directly to Volume 1 (Expanded Second Edition) and Volume 2 (Concise First Edition).

### Writing, Structural, & Mechanical Rules (MANDATORY: Enforced by `run_audit_gate.py` & `independent_critique`)
*   **No em dashes (`U+2014`) anywhere.** No prose en dashes (`U+2013`), box-drawing dashes (`U+2500`), or spaced hyphens (` - ` / ` -- `); en dashes are permitted strictly inside date ranges (`MMM YYYY – MMM YYYY` or `YYYY – YYYY`).
*   **No contractions** in formal writing (except `"Let's connect."` CTA heading in `Profile 5`).
*   **No Roman numeral `Volume I` in series/universal prose:** `lint_blog.py` scans case-insensitively for `\bI\b` and flags `Volume I` as `[PROSE-PRONOUN]`. Always write Arabic numerals **`Volume 1`** and **`Volume 2`**.
*   **No AI clichés or filler intensifiers:** Never use `simply`, `precisely`, `exact`, `exactly`, `deeply`, `truly`, `really`, `very`, `quietly`, `incredibly`, `highly`, `delve`, `leverage`, `seamless`, `seamlessly`, `robust`, `tapestry`, `testament`, `crucial`, `vital`, `pivotal`, `unlock`, `empower`, `harness`, `synergy`, `game-changing`, `cutting-edge`, `groundbreaking`, `supercharge`, `spearhead`, `actually`, `whether ... or ...`, or `high-impact`.
*   **No `-ing` participial sentence starters** (`Understanding...`, `Having...`, `Knowing...`, `Designing...`, `Running...`, `Following...`, `Scattering...`) and **no `By <verb>-ing` openers** in prose or bullets (including immediately after `**Bold Label:**` and inside `<!-- SUMMARY: ... -->` HTML comments rendered onto Part/index cards).
*   **No dependent-clause sentence openers:** Sentences must not open with `Because`, `Since`, `Given that`, `Knowing that`, `If`, `When`, `As`, `Once`, `While`, `Although`, `Though`, `Unless`, `Whereas`, or `After`.
*   **No mechanical transitions** (`For example`, `For instance`, `To address this`, `Ultimately`, `Moreover`, `Furthermore`, `Additionally`, `In conclusion`, `In summary`, `Consequently`, `Therefore`, `Thus`, `Hence`, `However`, `Nevertheless`, `Nonetheless`, `Specifically`, `Notably`, `Importantly`, `Crucially`) and **no vague `This <verb>` openers** (`This ensures`, `This allows`, `This means`, `This enables`, `This makes`, `This provides`, `This creates`, `This gives`, `This prevents`, `This guarantees`, `This results`, `This leads`, `This causes`, `This forces`, `This helps`).
*   **Sentence & Paragraph Length Caps (`D2`):** Every sentence in `Profile 2: series` must be `<= 45` words (`<= 4` commas; `>= 5` flagged). Paragraphs must be short, focused, and readable (typically 2–4 sentences, `<= 125` words). No `3+` consecutive sentences may start with the same word.
*   **Strict Grammatical Parallelism (`D3`, Rule 4):** All bullet lists, card descriptions, action links (such as `Download ...` on `ebooks/index.html`), and table cells within a group must share identical grammatical structure, and every `###` section must introduce tables/lists with 1–2 prose sentences.
*   **Table Formatting Invariant (`D3` Rule 1 & `D7` `1280px`/`390px`):** Never apply `white-space: nowrap` to `th` or prose `td` cells (`td:first-child` or `td:nth-child(-n+4)`); restrict `white-space: nowrap` strictly to `.blog-post.series-signal-integrity table:not(.trace-container table) .katex`, set `table-layout: auto; word-break: normal; overflow-wrap: normal`, and apply desktop Column-1 width caps (`width: 32%; max-width: 240px` on 2-column tables; `max-width: 220px` on 3+ column tables).
*   **Tone & Voice:** Conversational, grounded, peer-level authority. Zero first- or second-person pronouns (`I`, `we`, `you`, `your`, `our`, `us`) in technical blog series (`Profiles 1–4`).

### Pedagogical, Difficulty-Calibration, & Mathematical Standards (`Standards 0–6` — MANDATORY)
1.  **Standard 0 (Forward Physical Causality, Layman-Clear Building Blocks, & the Four Reader Questions):**
    *   **Consistent Difficulty Across Chapters (Match Chapters 1–5):** Break complex physical phenomena into small, intuitive, self-contained building blocks in plain, accessible English. **Never** use cheap everyday analogies ("carrots", "coins", "sandwiches", "submerged paddle wheels", "ripples on a pond") and **never** gloss over real technical mechanics; simultaneously, **never** get lost in heavy field-theory notation or clever calculus/complex-algebra tricks (`\sqrt{j}`, coupled PDEs, improper complex integrals, unmotivated special functions).
    *   **Always Satisfy the Four Reader Questions at Every Step:** (1) *Why does this matter / why do we care?* (2) *What is physically happening here, and why?* (3) *What does this physical quantity or relationship mean in concrete terms?* (4) *How does this relate to everything else established in prior chapters and earlier sections?*
    *   **Concepts First, Math Quantifies Concepts Second.** Unified top-down narrative (never conversational Q&A patch fragments).
2.  **Standard 1 (Minimal Foundational Equations, Step-by-Step Transparent Algebra, & Zero Unmotivated Drops):**
    *   Never drop named laws, theorems, PDEs, integrals, or transforms out of thin air. Display any recalled equation on its own standalone `$$ ... $$` line immediately above where it is substituted. Never use the internal meta-phrase `"pillar equation"` (`[D5-META-JARGON]`) or unanchored `"Equation N"` tags. Define every variable, subscript, and SI unit explicitly before use; zero ASCII art diagrams.
3.  **Standard 2 (Explicit Function Arguments):** Write explicit spatial and temporal arguments ($v(z, t)$, $i(z, t)$, $\Phi_B(t)$, $B(r, t)$ in time domain; $V(z)$, $I(z)$ in frequency domain).
4.  **Standard 3 (Explicit Derivative Notation):** Never use unexplained prime notation ($f', R', L'$); use per-unit-length $R_{\text{DC}}, R_{\text{AC}}, L, G, C$ and explicit derivatives.
5.  **Standard 4 (Zero Symbol Collisions):** $\rho_r$ for resistivity ($\Omega\cdot\text{m}$), $\sigma$ for conductivity ($\text{S/m}$); $\ell$ length, $w$ width, $t_{\text{Cu}}$ foil thickness, $d_{\text{gap}}$ dielectric gap, $x$ inward copper depth; $\delta$ skin depth vs. compound $\tan\delta$ loss tangent; uppercase $K$ sheet current density ($\text{A/m}$) and $K_r$ roughness multiplier; lowercase $k_b, k_f$ crosstalk coefficients; $\tau_{\text{skin}}$ skin time scale (never reuse wire radius $a$); $T_V$ voltage transmission coefficient (never $\tau$); $v_{-1}, v_0, v_1$ ISI cursors.
6.  **Standard 5 (All Equations on Standalone `$$ ... $$` Lines — `[D2-INLINE-EQUATION]` & `[D5-INLINE-MATH-CHAIN]`):** Restrict inline `$ ... $` strictly to standalone symbols or single scalar values with units (`0` inline equalities `=` or relational expressions in prose).
7.  **Standard 6 (`###` / `####` Subsections Instead of Multi-Sentence Bullet Walls — `[D2-BULLET-WALL]`):** Bullets `<= 65` words with parallel `- ` markers and structure; multi-sentence explanations use `###`/`####` subsections with 2–4 sentence paragraphs.

### Standing Long-Term Master Plan (Retained for Future Continuation of Ch 5 `L296–791` & Ch 6–21)
1.  **Level 1: Per-Chapter 3-Stage Process:**
    *   **Stage 1:** Full-chapter top-to-bottom rework for `Standards 0–6`, `node build_blog.mjs`, and `0` violations / `0` advisories on `run_audit_gate.py --profile series --strict-heuristics --skip-visual`.
    *   **Stage 2:** Interactive first-principles Q&A on `localhost:8080`, logging every block in `QA_ChXX_*.md` (and cross-chapter items in `SI_Cross_Chapter_Parking_Lot.md`), live-distilling into the chapter, rebuilding, and re-verifying the gate.
    *   **Stage 3:** Sync revised chapter via `sync_keysight_guides.py` into `Keysight_preparation/guides/` (stripping web download banners and remapping legacy Part subdirectory filenames/links).
2.  **Level 2: Part-Boundary Batch Audits & Volume Ebook Rebuilds:**
    *   At each Part boundary (`Volume 1`: Part 1 = Ch 1–5; `Volume 2`: Part 2 = Ch 6–9, Part 3 = Ch 10–12, Part 4 = Ch 13–15, Part 5 = Ch 16–18, Part 6 = Ch 19–21), apply `SI_Cross_Chapter_Parking_Lot.md` items, rebuild HTML (`node build_blog.mjs`) + Volume PDFs (`python3 blog/content/series/signal-integrity/assemble_and_build.py`), run full 8-dimension `run_audit_gate.py` + direct `verify_visual_and_pdf.mjs` (`1280x800` & `390x844`), and run isolated Cold-Reader Subagents (`research`, 2–5 files per subagent) per `independent_critique`.

---

## Exact Status of Signal Integrity Chapters & Artifacts (`2026-11-20` Relaunch State)

*   **Volume 1 (`Part 1 = Chapters 01–05`, Expanded Second Edition — `signal-integrity-vol1-ebook-v2.0.pdf`):**
    *   **Chapters 1–4 (`01_Wave_Propagation_and_Transmission_Lines.md`, `02_Frequency_Content_of_Digital_Signals.md`, `03_Impedance_Reflections_and_Termination.md`, `04_Inductance_Magnetic_Coupling_and_Crosstalk.md`):** Completed full Stage 1 rework, Stage 2 interactive Q&A (`Blocks 1–84`), `Standards 0–6` mechanical cleanup (`0` violations, `0` advisories on `--strict-heuristics`, `0` inline `=` in prose), isolated Cold-Reader Subagent audits + 100% remediation, and `Keysight_preparation/guides/` sync (`0` violations, `0` advisories, `0` broken links).
    *   **Chapter 5 (`05_Skin_Effect_and_Dielectric_Loss.md` — `791` lines):** Completed full Stage 1 `Standards 0–6` rework (`0` violations, `0` advisories on `--strict-heuristics`), Stage 2 interactive Q&A through line `294` (`Blocks 85–101`), isolated Cold-Reader Subagent audit across all `791` lines (with dedicated scrutiny of `lines 296–791`, including Hammerstad vs. Huray 3D roughness physics, Debye/Djordjevic-Sarkar dielectric dispersion, causal precursor $v_{-1}$ around $t'_0$, and smooth vs. rough stripline `39.7 \Omega` / `340 nH/m` consistency), and `Keysight_preparation/guides/` sync. Ready to resume interactive Stage 2 Q&A at line `296` (`#### Why Copper Foil Thickness Stops Helping While Trace Width Still Helps`) whenever bandwidth permits.
    *   **Compiled PDF:** `/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/signal-integrity-vol1-ebook-v2.0.pdf` (`5/5` `audit_widths.mjs` slices passed natively; `verify_visual_and_pdf.mjs` passed cleanly).
*   **Volume 2 (`Part 2 = Chapters 06–09` and `Parts 3–6 = Chapters 10–21`, Concise First Edition — `signal-integrity-vol2-ebook-v1.0.pdf`):**
    *   Regrouped `Part 2` to `Chapters 06–09` (*Discontinuities and Signal Integrity Measurement*), resolved symbol collisions (`\tau -> T_V` in `Ch 07–08`; `K_b/2K_b -> k_b/2k_b` in `Ch 08` & `Ch 16`), extracted all `120` `[D5-INLINE-MATH-CHAIN]` expressions onto standalone `$$ ... $$` lines, updated offline banners to Volume 2, and verified **`0` blocking violations** across all `16` chapters (`290` D2 concise-edition advisories deferred until future interactive expansion).
    *   **Compiled PDF:** `/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/signal-integrity-vol2-ebook-v1.0.pdf` (`6/6` `audit_widths.mjs` slices passed natively; `verify_visual_and_pdf.mjs` passed cleanly).
*   **Retired Legacy Artifacts:**
    *   Removed obsolete `assets/docs/src/signal-integrity-v1/` (`22` files) and single-volume `assets/docs/signal-integrity-ebook-v1.0.pdf` / `v2.0.pdf` via `git rm`.

---

## Resource Locations

*   **Relaunch Architecture Plan & Verbatim Cold-Reader Audit Reports (`plans/`, git-ignored):**
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/plans/si_relaunch_architecture_plan.md` (5-Phase Execution Plan — `0` violations, `0` advisories)
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/plans/audit_si_relaunch_plan_2026-11-19.md` (`16` architecture plan findings resolved)
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/plans/audit_si_ch01_03_2026-11-20.md` (`17` Cold-Reader findings resolved across Chapters `01–03`)
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/plans/audit_si_ch04_05_2026-11-20.md` (`18` Cold-Reader findings resolved across Chapters `04–05`)
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/plans/audit_web_surfaces_2026-11-20.md` (`17` Cold-Reader findings resolved across web entry, Part, and Keysight pages)
*   **Portfolio Entrypoints, Templates, & Builders:**
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/AGENTS.md`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/index.html`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/ebooks/index.html`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/close.html`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/build_blog.mjs`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/blog_template.html`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/index.html`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/series-signal-integrity.html`
*   **Signal Integrity Source & Ebook Pipeline:**
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/signal-integrity/` (`01`–`21` `.md` files + `assemble_and_build.py` supporting `--vol1` and `--vol2`)
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/signal-integrity-vol1-ebook-v2.0.pdf`
    *   `/Users/lydia/Desktop/personal/career/resumes/portfolio/assets/docs/signal-integrity-vol2-ebook-v1.0.pdf`
*   **Q&A Logs, Parking Lot, & Keysight Guides:**
    *   Ch 1 (`Blocks 1–35`): `/Users/lydia/Desktop/personal/career/resumes/concept_guides/EE_and_SI_Running_QA_Extractions.md`
    *   Ch 2 (`Blocks 36–50`): `/Users/lydia/Desktop/personal/career/resumes/concept_guides/QA_Ch02_Frequency_Content.md`
    *   Ch 3 (`Blocks 51–62`): `/Users/lydia/Desktop/personal/career/resumes/concept_guides/QA_Ch03_Impedance_Reflections.md`
    *   Ch 4 (`Blocks 63–84`): `/Users/lydia/Desktop/personal/career/resumes/concept_guides/QA_Ch04_Inductance_Crosstalk.md`
    *   Ch 5 (`Blocks 85–101`): `/Users/lydia/Desktop/personal/career/resumes/concept_guides/QA_Ch05_Skin_Effect_Dielectric_Loss.md`
    *   Cross-Chapter Parking Lot: `/Users/lydia/Desktop/personal/career/resumes/concept_guides/SI_Cross_Chapter_Parking_Lot.md`
    *   Keysight Concept Guides: `/Users/lydia/Desktop/personal/career/resumes/concept_guides/Keysight_preparation/guides/`
*   **Audit & PDF Skills/Scripts:**
    *   `/Users/lydia/.gemini/config/skills/independent_critique/SKILL.md`
    *   `/Users/lydia/.gemini/config/skills/independent_critique/references/domain_profiles.md`
    *   `/Users/lydia/.gemini/config/skills/independent_critique/scripts/run_audit_gate.py`
    *   `/Users/lydia/.gemini/config/skills/independent_critique/scripts/verify_visual_and_pdf.mjs`
    *   `/Users/lydia/.gemini/config/skills/pdf_generator/SKILL.md`
    *   `/Users/lydia/.gemini/config/skills/pdf_generator/scripts/audit_widths.mjs`

---

## Past Accomplishments
*   **`2026-10-23` to `2026-11-12`:** Built Master Resume (`Pedersen_Resume_2026.pdf`), LinkedIn Blueprint, Keysight Presentation (`keysight/`), 5 AI Ebooks, and `independent_critique` 8-dimension CLI gate; completed Signal Integrity Chapters 1–4 Q&A distillations (`Blocks 1–84`) and initial Ch 5 Q&A (`Blocks 85–92`).
*   **`2026-11-12` to `2026-11-19`:** Completed Stage 1 full rework of Chapter 5 (`05_Skin_Effect_and_Dielectric_Loss.md`), Stage 2 Q&A `Blocks 93–101`, and authored + adversarially audited the Two-Volume Signal Integrity Relaunch Plan (`plans/si_relaunch_architecture_plan.md`).

---

## Work Accomplished in Current Session (`2026-11-20`)
1.  **Phase 1 (Freeze Guard, Table CSS, & `.gitignore`):** Restored all `41` dirtied `tokenization`, `transformers`, and `mixture-of-experts` HTML files via `git checkout HEAD`, added `FROZEN_SERIES` write-guards in `build_blog.mjs`, fixed `.blog-post.series-signal-integrity` table wrapping in `blog/blog_template.html` (restricting `white-space: nowrap` strictly to `.katex` and capping desktop Column-1 widths), and updated `.gitignore`.
2.  **Phase 2 (Volume 1 `Standards 5–6` Cleanup & Keysight Sync):** Resolved all `57` D5 violations and `275` D2 advisories across Chapters `01–03`, aligned Volume 1 offline banners across `01–05.md`, and synced stripped/remapped `Ch 01–05` into `Keysight_preparation/guides/` (`0` violations, `0` advisories, `0` broken links).
3.  **Phase 3 (Volume 2 Mechanical Gate Hygiene):** Fixed `Ch 07–08` and `Ch 16` symbol collisions (`\tau -> T_V`, `K_b/2K_b -> k_b/2k_b`), extracted `120` `[D5-INLINE-MATH-CHAIN]` expressions onto standalone `$$ ... $$` lines across `Ch 06–21`, and aligned Volume 2 offline banners (`0` blocking violations across all `21` chapters).
4.  **Phase 4 (Web Regrouping, Two-Volume PDF Build, Shelf Updates, & `git rm`):** Regrouped `siParts` (`Part 1 = Ch 01–05`, `Part 2 = Ch 06–09`, Volume 1/2 `.series-group` containers), refactored `assemble_and_build.py` (with `<= 18,000`-word slice `audit_widths.mjs` checks and `#anchor`-safe cross-volume link resolution) to build `signal-integrity-vol1-ebook-v2.0.pdf` and `signal-integrity-vol2-ebook-v1.0.pdf`, updated `index.html`, `ebooks/index.html`, and `keysight/close.html`, and `git rm`'d retired `v1.0` sources and legacy PDFs.
5.  **Phase 5 (Full 8-Dimension Audit, 3 Cold-Reader Subagents, 100% Remediation, & Visual Verification):** Executed `3` isolated Cold-Reader `research` subagent audits (`Ch 01–03`, `Ch 04–05`, and web/Keysight surfaces), saved all `3` reports 100% verbatim to `plans/`, remediated all `52` findings (`0` deferrals), rebuilt HTML, Keysight study guides, and Volume 1 PDF, and verified `0` blocking violations across all deterministic and `1280px`/`390px` visual/PDF gates (`66/66 PASS`) with `0` frozen-series diffs.

---

## Next Steps
1.  **Immediate Relaunch (`git commit`, `git push`, & GitHub Pages):**
    *   Commit staged/tracked changes, push to `origin/main`, and switch GitHub Pages Source Branch back from `None` to `main` (`/ (root)`) to bring `https://lyd1acla1r3.github.io` live.
2.  **Future Continuation (Whenever Schedule Permits):**
    *   Resume interactive Stage 2 Q&A in Chapter 5 (`05_Skin_Effect_and_Dielectric_Loss.md`) starting at line `296` (`#### Why Copper Foil Thickness Stops Helping While Trace Width Still Helps`, after `Block 101` in `QA_Ch05_Skin_Effect_Dielectric_Loss.md`), then proceed chapter-by-chapter through Chapters `06–21` to elevate Volume 2 to Expanded Second Edition depth.
