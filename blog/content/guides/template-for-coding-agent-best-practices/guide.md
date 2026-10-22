# Template for Coding Agent Best Practices: Setup Guide

<!-- SUMMARY: A step-by-step setup guide for the coding agent operating layer: copying a tested template tree into a project, then wiring always-on rules, on-demand skills, isolated subagents, hook guards with a Git pre-commit backstop, permissions, model roles, and session state, with a verification check for each layer across seven supported agent targets. -->
<style>
  /* code-drop: collapsible code block. Markup: details.code-drop > summary > span.code-drop__name + span.code-drop__meta, then a fenced block. */
  .blog-post details.code-drop { margin: var(--space-lg) 0; border: 1px solid var(--border-medium); border-radius: var(--radius-md); background: var(--bg-card); box-shadow: var(--shadow-sm); overflow: hidden; }
  .blog-post details.code-drop > summary { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-xs) var(--space-sm); padding: var(--space-sm) var(--space-md); cursor: pointer; list-style: none; user-select: none; transition: background-color 0.2s ease; }
  .blog-post details.code-drop[open] > summary { background: var(--rose-gold-glow); }
  .blog-post details.code-drop > summary::-webkit-details-marker { display: none; }
  .blog-post details.code-drop > summary::marker { content: ""; }
  .blog-post details.code-drop > summary::before { content: ""; flex: none; width: 0.45em; height: 0.45em; margin: 0 var(--space-xs); border-right: 2px solid var(--rose-gold); border-bottom: 2px solid var(--rose-gold); transform: rotate(-45deg); transition: transform 0.2s ease; }
  .blog-post details.code-drop[open] > summary::before { transform: rotate(45deg); }
  .blog-post details.code-drop > summary:hover { background: var(--rose-gold-subtle); }
  .blog-post details.code-drop > summary:focus-visible { outline: 2px solid var(--text-accent); outline-offset: -2px; border-radius: var(--radius-md); }
  .blog-post details.code-drop .code-drop__name { flex: 1 1 16ch; min-width: 0; overflow-wrap: anywhere; font-family: var(--font-mono); font-size: var(--fs-sm); color: var(--text-primary); }
  .blog-post details.code-drop .code-drop__meta { margin-left: auto; white-space: nowrap; font-family: var(--font-body); font-size: var(--fs-xs); color: var(--text-muted); }
  .blog-post > pre, .blog-post details.code-drop > pre { padding: var(--space-md) var(--space-lg); background: var(--bg-secondary); overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .blog-post > pre { margin: var(--space-md) 0 var(--space-lg); border: 1px solid var(--border-medium); border-left: 3px solid var(--rose-gold); border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
  .blog-post details.code-drop > pre { margin: 0; border-top: 1px solid var(--border-medium); }
  .blog-post > pre > code, .blog-post details.code-drop > pre > code { display: block; padding: 0; background: none; border-radius: 0; font-family: var(--font-mono); font-size: var(--fs-sm); line-height: 1.65; color: var(--text-primary); white-space: pre; }
  .blog-post ul { list-style: disc; padding-left: 1.5rem; margin: var(--space-md) 0 var(--space-lg); }
  .blog-post ol { list-style: decimal; padding-left: 1.5rem; margin: var(--space-md) 0 var(--space-lg); }
  .blog-post li { margin-bottom: var(--space-sm); color: var(--text-secondary); line-height: 1.75; }
  .blog-post li::marker { color: var(--rose-gold); font-weight: var(--fw-semibold); }
  .blog-post li > strong:first-child { color: var(--text-primary); }
  @media (prefers-reduced-motion: reduce) {
    .blog-post details.code-drop > summary, .blog-post details.code-drop > summary::before { transition: none; }
  }
  /* table: bordered card with horizontal row dividers and alternating palette shades. */
  .blog-post table { width: 100%; margin: var(--space-lg) 0; border-collapse: separate; border-spacing: 0; border: 1px solid var(--border-medium); border-radius: var(--radius-md); background: var(--bg-card); box-shadow: var(--shadow-sm); overflow: hidden; }
  .blog-post thead tr { background: var(--rose-gold-glow); }
  .blog-post th { padding: var(--space-sm) var(--space-md); font-weight: var(--fw-semibold); color: var(--rose-gold-dark); border-bottom: 2px solid var(--border-medium); }
  .blog-post tbody tr:nth-child(odd) { background: var(--bg-secondary); }
  .blog-post tbody tr:nth-child(even) { background: var(--blush-glow); }
  .blog-post td { padding: var(--space-sm) var(--space-md); border-bottom: 1px solid var(--border-medium); color: var(--text-secondary); }
  .blog-post td:first-child { font-weight: var(--fw-medium); color: var(--text-primary); }
  .blog-post tbody tr:last-child td { border-bottom: none; }
  @media (min-width: 769px) {
    .blog-post th:first-child, .blog-post td:first-child { white-space: nowrap; }
  }
  @media (max-width: 768px) {
    .blog-post table { overflow-x: auto; }
  }
</style>

The [Architecture and Configuration](template-for-coding-agent-best-practices-configuration.html) chapter explains why the operating layer splits into rules, skills, subagents, hooks, and state. This guide installs that layer in an existing project. Every file it references lives in the [template repository](https://github.com/Lyd1aCla1r3/coding-agent-best-practices), which holds one tested drop-in tree per tool, so the steps below show short excerpts and link to the full files. Claude Code paths serve as the running example, and Step 2 maps them to the other six trees.

## Prerequisites

| Requirement | Details |
|---|---|
| Coding agent | Claude Code, Cursor, Google Antigravity, Posit Assistant, Windsurf (now Devin Desktop), or Cline. The Universal tree suits any other agent that reads `AGENTS.md`. |
| Git | Any recent version, for the commit backstop. |
| jq | The JSON processor the guard scripts use to read each payload (`brew install jq` or `apt install jq`). |
| Python | Version 3.10 or later, for the linter, the style hooks, the Cline hook, and the test harness. |
| Bash | Standard macOS or Linux shell, or WSL2 on Windows, for the guard and helper scripts. |
| Operating system<br>sandbox | Optional workspace confinement enabled in five of the agent trees. |

## Step 1: Get the Templates

Clone the [template repository](https://github.com/Lyd1aCla1r3/coding-agent-best-practices) into the home folder, then copy one platform tree into the root of the target project. Replace `<tool>` with a folder name from Step 2, such as `claude-code`. Copying `.` rather than `*` brings along hidden folders such as `.claude/` and `.githooks/`.

```bash
git clone <repo-url> ~/tpl
cd ~/tpl/platforms/<tool>
cp -R . /path/to/project/
```

The copy overwrites files with the same names, including `CLAUDE.md`, `AGENTS.md`, `session_checkpoint.md`, and existing tool settings, so merge those by hand in a project that already has them. Then activate the Git backstop from the project root:

```bash
cd /path/to/project
git config core.hooksPath \
  .githooks
```

Five trees need one more step after the copy:

- **Cursor**: Open the project in a trusted workspace so project hooks load.
- **Posit Assistant**: Run `/trust` in the session to enable project hooks.
- **Cline**: Turn on **Enable Hooks** in the extension settings.
- **Google Antigravity and Windsurf**: Merge `.agents/cli-settings.example.json` or `.devin/user-config.example.json` into the user configuration for model, sandbox, and permission choices.

**Verification**:

```bash
git config core.hooksPath
```

The command prints `.githooks`.

## Step 2: Layout per Tool

Every tree carries the same shared files at its root: the checkpoint, three policy lists, the commit hook, and two scripts. Claude Code adds `CLAUDE.md` at the root, Cursor and Cline add no root instruction file, and the other four trees add `AGENTS.md`. Inside each tool folder, rules live in `rules/`, skills in `skills/`, and subagents in `agents/`, except in three trees:

- **Posit Assistant**: Keeps subagent prompts in `handoffs/` instead of `agents/`.
- **Cline**: Places numbered rules directly in `.clinerules/`, subagent prompts in `newtask-prompts/` inside it, and skills in `.cline/skills/`.
- **Universal**: Inlines every rule into `AGENTS.md` and keeps `handoffs/` at the root.

| Tool | Tool folder | Hook wiring |
|---|---|---|
| Claude Code | `.claude/` | `settings.json` |
| Cursor | `.cursor/` | `hooks.json` |
| Google Antigravity | `.agents/` | `hooks.json` |
| Posit Assistant | `.posit/assistant/` | `settings.json` |
| Windsurf | `.devin/` | `hooks.v1.json` |
| Cline | `.clinerules/` | `hooks/PreToolUse` |
| Universal | `.agents/` | Git hook only |

Windsurf reads `hooks.v1.json` for its default Devin Local agent and `hooks.json` for the older Cascade agent. The trees below show each [platform folder](https://github.com/Lyd1aCla1r3/coding-agent-best-practices/tree/main/platforms), with the six skill folders folded into one line.

<details class="code-drop">
<summary><span class="code-drop__name">platforms/claude-code/</span><span class="code-drop__meta">Tree · 32 lines</span></summary>

```text
platforms/claude-code/
  .claude/
    agents/
      codebase-explorer.md
      style-auditor.md
      web-researcher.md
    hooks/
      check-style.sh
      guard-destructive.sh
      guard-freeze.sh
      guard-network.sh
      guard-secrets.sh
    plans/
    rules/
      agency.md
      freeze-paths.md
      ground-truth.md
      planning-mode.md
      writing-style.md
    skills/            6 skill folders, one SKILL.md each (see Step 4)
    settings.json
  .githooks/
    pre-commit
  checkpoints/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  CLAUDE.md
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/cursor/</span><span class="code-drop__meta">Tree · 33 lines</span></summary>

```text
platforms/cursor/
  .cursor/
    agents/
      codebase-explorer.md
      style-auditor.md
      web-researcher.md
    hooks/
      check-style.sh
      guard-destructive.sh
      guard-freeze.sh
      guard-network.sh
      guard-secrets.sh
    plans/
    rules/
      agency.mdc
      freeze-paths.mdc
      ground-truth.mdc
      planning-mode.mdc
      writing-style.mdc
    skills/            6 skill folders, one SKILL.md each (see Step 4)
    hooks.json
    permissions.json
    sandbox.json
  .githooks/
    pre-commit
  checkpoints/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/antigravity/</span><span class="code-drop__meta">Tree · 33 lines</span></summary>

```text
platforms/antigravity/
  .agents/
    agents/
      codebase-explorer.md
      style-auditor.md
      web-researcher.md
    hooks/
      check-style.sh
      guard-destructive.sh
      guard-freeze.sh
      guard-network.sh
      guard-secrets.sh
    plans/
    rules/
      agency.md
      freeze-paths.md
      ground-truth.md
      planning-mode.md
      writing-style.md
    skills/            6 skill folders, one SKILL.md each (see Step 4)
    cli-settings.example.json
    hooks.json
  .githooks/
    pre-commit
  checkpoints/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  AGENTS.md
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/posit-assistant/</span><span class="code-drop__meta">Tree · 33 lines</span></summary>

```text
platforms/posit-assistant/
  .githooks/
    pre-commit
  .posit/
    assistant/
      handoffs/
        codebase-explorer-prompt.md
        style-auditor-prompt.md
        web-researcher-prompt.md
      hooks/
        check-style.sh
        guard-destructive.sh
        guard-freeze.sh
        guard-network.sh
        guard-secrets.sh
      plans/
      rules/
        agency.md
        freeze-paths.md
        ground-truth.md
        planning-mode.md
        writing-style.md
      skills/            6 skill folders, one SKILL.md each (see Step 4)
      settings.json
  checkpoints/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  AGENTS.md
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/windsurf/</span><span class="code-drop__meta">Tree · 35 lines</span></summary>

```text
platforms/windsurf/
  .devin/
    agents/
      codebase-explorer.md
      style-auditor.md
      web-researcher.md
    hooks/
      check-style.sh
      guard-destructive.sh
      guard-freeze.sh
      guard-network.sh
      guard-secrets.sh
    plans/
    rules/
      agency.md
      freeze-paths.md
      ground-truth.md
      planning-mode.md
      writing-style.md
    skills/            6 skill folders, one SKILL.md each (see Step 4)
    config.json
    hooks.json
    hooks.v1.json
    user-config.example.json
  .githooks/
    pre-commit
  checkpoints/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  AGENTS.md
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/cline/</span><span class="code-drop__meta">Tree · 27 lines</span></summary>

```text
platforms/cline/
  .cline/
    skills/            6 skill folders, one SKILL.md each (see Step 4)
  .clinerules/
    hooks/
      PreToolUse
    newtask-prompts/
      codebase-explorer-prompt.md
      style-auditor-prompt.md
      web-researcher-prompt.md
    01-agency.md
    02-ground-truth.md
    03-planning-mode.md
    04-writing-style.md
    05-freeze-paths.md
  .githooks/
    pre-commit
  checkpoints/
  plans/
  scripts/
    lint_prose.py
    plan.sh
  .clineignore
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  session_checkpoint.md
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">platforms/universal/</span><span class="code-drop__meta">Tree · 19 lines</span></summary>

```text
platforms/universal/
  .agents/
    skills/            6 skill folders, one SKILL.md each (see Step 4)
  .githooks/
    pre-commit
  checkpoints/
  handoffs/
    codebase-explorer-prompt.md
    style-auditor-prompt.md
    web-researcher-prompt.md
  plans/
  scripts/
    lint_prose.py
    plan.sh
  .freeze-paths.txt
  .style-denylist.txt
  .style-phrases.txt
  AGENTS.md
  session_checkpoint.md
```

</details>

## Step 3: Always-On Rules

Five short rule files shape every turn:

| Rule | Purpose |
|---|---|
| Agency | Act on unambiguous tasks, search locally before asking, and fix root causes. |
| Ground truth | Read a file before describing it, and tag every claim with an evidence tier. |
| Planning mode | Stop for questions and an approved plan before changing three or more files, a shared interface, a build pipeline, or the dependencies. |
| Writing style | Keep terminology consistent, use active voice, spell out acronyms on first use, and format code identifiers in backticks. |
| Freeze paths | Treat `published/` and `archive/` as read-only, and record a restore-point commit before shared build files change. |

Customize the rule and style files before the first session, noting how each tool wraps the [shared rule bodies](https://github.com/Lyd1aCla1r3/coding-agent-best-practices/tree/main/core/rules):

- **Writing conventions**: Replace the example conventions in the [writing-style rule](https://github.com/Lyd1aCla1r3/coding-agent-best-practices/blob/main/core/rules/writing-style.md) with the team's own.
- **Mechanical bans**: Replace the sample term in `.style-denylist.txt` and add phrases to `.style-phrases.txt`, where the linter and the style hook enforce them.
- **Rule frontmatter**: Keep or adjust the trigger frontmatter that Cursor, Antigravity, and Windsurf add to each rule body and the `paths:` frontmatter that Claude Code and Cline use to scope the writing rule to Markdown files.
- **Native plan mode**: Review the tool-specific section at the bottom of the planning rule so it matches the team's preferred plan-mode command or default setting.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/rules/planning-mode.md</span><span class="code-drop__meta">Markdown · 11 lines</span></summary>

```markdown
# Planning Gate and Approval Protocol

## When to Trigger the Planning Gate
- **Trigger Conditions:** Enter the planning gate before writing application code when a task modifies 3 or more files, alters shared interfaces, touches build pipelines, or introduces new dependencies.
- **Clarify Before Planning:** Ask focused clarifying questions to resolve underspecified requirements before drafting the plan.
- **Approval Boundary:** Present the structured plan (objective, affected files, verification commands, and rollback steps) and wait for explicit user approval (`"approved"` or `"proceed"`) before executing edits.

## Native Plan Mode Integration (Claude Code)
- **Mode Activation:** Start complex sessions in native Plan mode (`Shift+Tab`, `/plan`, or `claude --permission-mode plan`), or set `permissions.defaultMode` to `"plan"` in `.claude/settings.json`.
- **Durable Plan File:** Pair native Plan mode with `bash scripts/plan.sh new <slug>` so the approved plan persists in `.claude/plans/` across sessions.
- **Doc Reference:** https://code.claude.com/docs/en/permission-modes
```

</details>

**Verification**: Start a session and ask the agent when it must stop to plan. The answer should restate the three-file trigger.

## Step 4: Skills

Each skill is a folder containing a `SKILL.md` file. The agent indexes every name and description at startup and loads a body only when a task matches it or the developer calls the skill by name:

| Skill | Purpose |
|---|---|
| `checkpoint` | Rewrites `session_checkpoint.md` and archives a detailed session log. |
| `handoff` | Prints a bootstrap prompt for the next session. |
| `tree-of-thought` | Scores three or more candidate approaches before one is chosen. |
| `adversarial-self-audit` | Attacks a plan, diff, or draft for failure modes and style violations. |
| `deep-research` | Gathers primary documentation and tags each claim with its evidence tier. |
| `autonomous-debugger` | Isolates failures through hypothesis-driven reproduction. |

Every skill has the same shape: a one-sentence description that decides when it loads, then numbered steps. New skills need a description specific enough for the agent to match it to a task.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/skills/tree-of-thought/SKILL.md</span><span class="code-drop__meta">Markdown · 19 lines</span></summary>

```markdown
---
name: tree-of-thought
description: Evaluate architectural decisions across three or more distinct candidate branches before implementation.
---

# Tree of Thought (ToT) Decision Protocol

## When to Invoke
Invoke this skill when choosing between competing architectures, data schemas, state-management strategies, or tool integrations where a single-path assumption risks a local optimum.

## Execution Steps
1. **Define the Decision Axis:** State the engineering problem and the hard constraints (latency, security, portability, maintenance cost) in two sentences.
2. **Generate Candidate Branches:** Formulate at least 3 genuinely distinct approaches (Branch A, Branch B, Branch C). Do not include strawman options.
3. **Evaluate Against Constraints:** Build a comparison table scoring each branch across:
   - **Primary Strength:** What the branch solves best.
   - **Failure Mode / Risk:** Where the branch breaks under load or edge cases.
   - **Verification Cost:** How the branch can be tested deterministically.
   - **Verdict:** `Reject` or `Selected` with a one-sentence justification.
4. **Record Selection:** Write the chosen branch and its rationale into the active plan file or `session_checkpoint.md` before writing implementation code.
```

</details>

**Verification**: Ask the agent which skills it can load. The reply should name all six.

## Step 5: Subagents

Three roles keep heavy reading and critique out of the main conversation:

| Subagent | Role |
|---|---|
| Codebase explorer | Runs read-only searches and returns a file map with line-range citations. |
| Web researcher | Fetches primary vendor documentation and tags each claim as documented or unconfirmed. |
| Style auditor | Reviews drafts in read-only mode against the writing rule and restricted-term lists on a strong reasoning model. |

In Claude Code, the `tools:` line limits each role to the tools it needs and the `model:` line pins its model, so the explorer below cannot write files even when a prompt asks it to.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/agents/codebase-explorer.md</span><span class="code-drop__meta">Markdown · 16 lines</span></summary>

```markdown
---
name: codebase-explorer
description: Read-only codebase mapping specialist for tracing symbol definitions, call graphs, and configuration layouts without polluting main-thread context.
tools: Read, Grep, Glob
model: sonnet
---

You are a read-only codebase exploration subagent. Your role is to locate files, trace symbol usages, and summarize architectural boundaries so the main agent receives a compact, citation-backed map without filling its context window with raw search logs.

## Operating Constraints
- **Strictly Read-Only:** Do not create, modify, rename, or delete any files.
- **Line-Range Citations:** Cite every finding with its project-relative file path and line range (`path/to/file.ext:L10-L25`).
- **Structured Output:** Return a concise report with three sections:
  1. `### Entrypoints & File Map`
  2. `### Data & Control Flow`
  3. `### Key Interfaces & Constraints`
```

</details>

Posit Assistant, Cline, and the Universal tree have no subagent files. Their trees ship the three roles as handoff prompts to paste into a fresh session, which keeps the isolation at the cost of one manual step.

## Step 6: Hooks and Pre-Commit

Hooks turn the rules that matter most into code. The runtime pipes each proposed command or file edit to a guard as JSON, the guard reads only the target path or command, and a match returns the tool's block signal. Every tree except Universal ships five guards covering frozen paths, destructive commands, network safety, secrets, and prose style on file writes and edits. Five of the agent trees keep them as separate scripts in `hooks/`, and Cline folds all five into `.clinerules/hooks/PreToolUse`.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/hooks/guard-destructive.sh</span><span class="code-drop__meta">Bash · 20 lines</span></summary>

```bash
#!/usr/bin/env bash
# Deterministic destructive-command guard for Claude Code (blocks via exit code 2).
# Rejects recursive force-deletes, hard resets, force pushes, and schema drops.

set -euo pipefail

CMD=$(jq -r '.tool_input.command // empty')

if [ -z "$CMD" ]; then
  exit 0
fi

DESTRUCTIVE_PAT="(rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f|rm[[:space:]]+-[a-zA-Z]*f[a-zA-Z]*r|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+push[[:space:]]+(--force|-f)|git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f|DROP[[:space:]]+TABLE)"
if printf '%s\n' "$CMD" |
   grep -qE "$DESTRUCTIVE_PAT"; then
  echo "BLOCKED [guard-destructive]: destructive command pattern detected." >&2
  exit 2
fi

exit 0
```

</details>

Claude Code wires the guards in `.claude/settings.json`. Shell commands pass the four guards shown below, and a second matcher sends every Write or Edit through the freeze, secrets, and style checks.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/settings.json</span><span class="code-drop__meta">JSON · 27-line excerpt</span></summary>

```json
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/guard-freeze.sh",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "bash .claude/hooks/guard-destructive.sh",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "bash .claude/hooks/guard-network.sh",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "bash .claude/hooks/guard-secrets.sh",
            "timeout": 10
          }
        ]
      },
```

</details>

Each tree's scripts already return their tool's block signal:

| Tool | Block signal |
|---|---|
| Claude Code | `exit 2` |
| Cursor | `"permission": "deny"` plus `exit 2` |
| Google Antigravity | `"decision": "deny"` |
| Posit Assistant | `exit 2` |
| Windsurf | `exit 2` |
| Cline | `"cancel": true` |
| Universal | `exit 1` from the commit hook |

Agent hooks can be switched off, and some runtimes let an action through when a hook crashes. The Git hook from Step 1 repeats the checks at commit time: it blocks staged paths that match `.freeze-paths.txt`, scans added lines for credentials and private keys, and sends staged Markdown to the prose linter.

<details class="code-drop">
<summary><span class="code-drop__name">.githooks/pre-commit</span><span class="code-drop__meta">Bash · 40-line excerpt</span></summary>

```bash
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMRD)
if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

# 1. Freeze guard against staged paths
FREEZE_REGEX="^(published|archive)/"
if [ -f ".freeze-paths.txt" ]; then
  CUSTOM_PAT=$(
    grep -vE "^(#|[[:space:]]*$)" .freeze-paths.txt | paste -sd "|" - || true
  )
  if [ -n "$CUSTOM_PAT" ]; then
    FREEZE_REGEX="^($CUSTOM_PAT)"
  fi
fi

if printf '%s\n' "$STAGED_FILES" |
   grep -qE "$FREEZE_REGEX"; then
  echo "BLOCKED [pre-commit]: staged changes touch a frozen path matching $FREEZE_REGEX" >&2
  exit 1
fi

# 2. Secret scan against staged additions
ADDED_LINES=$(git diff --cached -U0 | grep -E "^\+[^+]" || true)
SECRET_PAT="(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
if printf '%s\n' "$ADDED_LINES" |
   grep -qE "$SECRET_PAT"; then
  echo "BLOCKED [pre-commit]: staged diff contains a high-confidence secret or private key." >&2
  exit 1
fi

# 3. Deterministic prose & hygiene linter on staged markdown files
MD_FILES=$(
  git diff --cached --name-only --diff-filter=ACMR |
  grep -E "\.(md|mdx)$" || true
)
if [ -n "$MD_FILES" ] && [ -f "scripts/lint_prose.py" ]; then
  # Pass staged markdown files to lint_prose.py
  printf '%s\n' "$MD_FILES" | xargs python3 scripts/lint_prose.py
fi
```

</details>

Only the commit hook reads `.freeze-paths.txt`. The per-turn freeze guards and permission deny lists name `published/` and `archive/` directly, so add any new protected folder to those files as well.

**Verification**: Run the [hook test harness](https://github.com/Lyd1aCla1r3/coding-agent-best-practices/blob/main/tests/run_hook_tests.py) from the clone to test every guard and the commit tooling against sample payloads for each supported tool.

```bash
cd ~/tpl/tests
python3 run_hook_tests.py
```

A passing run prints `Passed 96/96 checks.` Sample payloads test the scripts rather than the live agent runtime, so finish with one live case in an agent tree: leave plan mode, ask the agent to run `echo DROP TABLE demo`, and confirm that the destructive guard blocks it.

## Step 7: Permissions, Sandbox, MCP

Permissions decide what the agent may run without asking, and the sandbox limits what a permitted command can reach. The Claude Code tree allows read-only Git commands and the two project scripts, asks before commits and pushes, denies reads of `.env` files and writes to the frozen folders, and starts in plan mode with the sandbox on.

<details class="code-drop">
<summary><span class="code-drop__name">.claude/settings.json</span><span class="code-drop__meta">JSON · 25-line excerpt</span></summary>

```json
{
  "model": "opusplan",
  "permissions": {
    "defaultMode": "plan",
    "allow": [
      "Bash(git status*)",
      "Bash(git diff*)",
      "Bash(python3 scripts/lint_prose.py*)",
      "Bash(bash scripts/plan.sh*)"
    ],
    "ask": [
      "Bash(git commit*)",
      "Bash(git push*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Write(./published/**)",
      "Write(./archive/**)"
    ]
  },
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  },
```

</details>

Each agent tree defines its permission and sandbox rules in its own configuration files; review the list before the first session:

| Tool | Permission and Sandbox Configuration |
|---|---|
| Claude Code | Allow, ask, deny, and sandbox rules in `settings.json` |
| Cursor | Terminal allowlist in `permissions.json` and workspace sandbox in `sandbox.json` |
| Google Antigravity | Permission and sandbox settings in `.agents/cli-settings.example.json` |
| Posit Assistant | Permission policy and sandbox setting in `settings.json` |
| Windsurf | Permission policy in `.devin/config.json` and sandbox setting in `.devin/user-config.example.json` |
| Cline | Auto-approve toggles in extension settings plus `.clineignore` |

The template ships no MCP servers. Add them in the tool's own file, such as `.mcp.json` for Claude Code or `.cursor/mcp.json` for Cursor, and scope each server as narrowly as the permission lists.

## Step 8: Model Routing

The template assigns work to four roles rather than to product names:

| Role | Model Tier and Use |
|---|---|
| Strategy and constraints | A frontier reasoning model for planning, audits, and tree-of-thought comparisons. |
| Daily driver | A fast model with reliable tool calling for implementation, debugging, research, and exploration. |
| Long-context archivist | A model with an extended context window for whole-repository audits and checkpoint condensation. |
| Local privacy vault | An open-weight model on the workstation for scrubbing logs and for offline tasks. |

Five trees pin those roles with their own model aliases:

- **Claude Code**: Sets `"model": "opusplan"` in `settings.json` to plan on the top tier and execute on the daily tier, with `sonnet` on the explorer and researcher and `opus` on the auditor.
- **Cursor**: Sets `model: inherit` in its subagent files so every subagent follows the session model.
- **Google Antigravity**: Sets `"model": "pro"` in the example settings, with `flash` on the explorer and researcher and `pro` on the auditor.
- **Windsurf**: Sets `"model": "opus"` and `"subagent_model": "sonnet"` in the example settings, with `sonnet` on the explorer and researcher and `opus` on the auditor.
- **Posit Assistant**: Maps the low, medium, and high tiers in `settings.json` to `haiku`, `sonnet`, and `opus`.

No tree pins the local privacy role. Point it at a local endpoint, such as the Ollama server from the [Solo Developer Stack](solo-developer-stack-guide.html), wherever the tool accepts a custom provider.

## Step 9: State and Continuity

Session state lives in files. The agent reads `session_checkpoint.md` first in every session, and the file stays at 150 lines or fewer. Fill in the project name, restore point, and frozen paths before the first session:

<details class="code-drop">
<summary><span class="code-drop__name">session_checkpoint.md</span><span class="code-drop__meta">Markdown · 21 lines</span></summary>

```markdown
# Session Checkpoint

## Project & Scope
- **Project:** <project-name>
- **Active Phase:** Phase 1 (Initial Implementation)
- **Restore Point SHA:** <record git rev-parse HEAD before integration edits>
- **Frozen Paths:** `published/`, `archive/` (configured in `.freeze-paths.txt`)

## Constraints & Decisions
- **Verification Policy:** Every quantitative metric traces to a command output; every platform claim cites an official vendor documentation URL.
- **Style Policy:** Prose follows the `writing-style` rule, and `python3 scripts/lint_prose.py` reports zero violations.
- **Selected Architecture:** <summarize chosen Tree of Thought branch and rationale>

## Accomplished & Verified
- [x] Initialized configuration layout, rules, skills, subagents, and deterministic hooks.
- [x] Verified hook guards against synthetic allow and deny payloads.

## Next Phase Tasks
1. Read `session_checkpoint.md` and the active plan in full before editing.
2. Execute the next scoped deliverable and verify with `python3 scripts/lint_prose.py`.
3. Run the `checkpoint` and `handoff` skills before closing the session.
```

</details>

Plans are dated Markdown files created by `scripts/plan.sh`, which finds the tool's plans folder on its own:

```bash
bash scripts/plan.sh new demo
bash scripts/plan.sh active
```

Close every session by running `checkpoint`, which rewrites `session_checkpoint.md` within its line cap and saves a detailed log in `checkpoints/`. Then run `handoff` to print a prompt naming the next objective, the files to read first, and the frozen paths so the next session starts in a clean context window.

**Verification**: The first command prints `Created plan:` followed by a dated path. Archive the test plan with `bash scripts/plan.sh done <path>`, and confirm with `wc -l session_checkpoint.md` that the checkpoint stays at 150 lines or fewer.

## Verification

The following checks confirm that every layer is installed and active.

| Check | Command | Expected Result |
|---|---|---|
| Git backstop | `git config core.hooksPath` | Prints `.githooks` |
| Rules | Ask when the agent must stop to plan | Restates the three-file trigger |
| Skills | Ask the agent to list its skills | Names all six skills |
| Hook harness | `python3 run_hook_tests.py` | Prints `Passed 96/96 checks.` |
| Live guard (agent trees) | Ask the agent to run `echo DROP TABLE demo` | Blocks with `guard-destructive` |
| Commit backstop | Stage a file in `published/`, then commit | Stops with `BLOCKED [pre-commit]` |
| Plans | `bash scripts/plan.sh new demo` | Prints `Created plan:` and a dated path |
| Checkpoint | Run the `checkpoint` skill | Rewrites `session_checkpoint.md` within 150 lines |

The harness check runs in `~/tpl/tests`, and the rest run in the project. The operating layer is in place once all eight checks pass.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Guards never fire | Trust the workspace, or turn on Enable Hooks in Cline |
| Hook output shows `jq: command not found` | Install `jq`, since tools differ on whether a failing hook blocks or allows |
| Commits skip the checks | Rerun the Step 1 `git config` command and confirm the hook is executable |
| A new frozen folder is still writable | Add it to the freeze guard and any deny list, not only `.freeze-paths.txt` |
| A safe command is blocked | Narrow the pattern in the guard script, then rerun the harness |

## References

1. Claude Code Documentation: Hooks, Settings, and Subagents, Anthropic.
2. Cursor Documentation: Rules, Hooks, and Permissions, Anysphere Inc.
3. Google Antigravity Documentation, Google DeepMind.
4. Posit Assistant Documentation, Posit Software, PBC.
5. Devin Desktop and Windsurf Documentation, Cognition AI.
6. Cline Documentation: Rules, Skills, and Hooks, Cline Bot Inc.
7. Agent Skills Specification, Agent Skills Open Standard.
8. Model Context Protocol Specification, Anthropic and MCP Steering Group.
9. Git Documentation: githooks and core.hooksPath, Software Freedom Conservancy.
10. jq Manual, jq Project.
