# Adaptive UX Layer

2-level adaptive UX system for Ignite. Same analysis and functionality at every level — only presentation and interaction density change.

**Levels:** Guided / Advanced

**Shared profile:** `.claude/security/user-profile.json` (also used by Cerbero)

---

## User Profile Schema

```json
{
  "level": "guided | advanced",
  "detected_via": "profile | inferred | explicit",
  "set_date": "YYYY-MM-DD",
  "preferences": {}
}
```

**Location:** `.claude/security/user-profile.json`

Create `.claude/security/` directory if it does not exist (may already exist if Cerbero is installed).

---

## Detection Cascade (Step 0.1)

Run once per project, during Step 0.1 (before Discovery). If the profile already exists, skip detection entirely.

`{{IDIOMA}}` is always available (set in Step 0.0 before this cascade runs).

### Cascade Step 1: Read existing profile

Read `.claude/security/user-profile.json`. If it exists and contains a valid `level` field ("guided" or "advanced"), use it. Log: `"User level: {level} (from profile)"`

If the file exists but `level` is missing or invalid, treat as not found — continue to Cascade Step 2.

### Cascade Step 2: Lightweight signal scan

Direct file checks (no Discovery catalog dependency):

**Advanced signals** (each scores 1 point):
- CLAUDE.md exists with `## Hooks` section containing specific hook configurations (quick read)
- `.claude/settings*.json` has `permissions.deny` references (quick read)
- Custom `.claude/rules/` files exist beyond template defaults (modified or added) (quick glob)
- References to sandbox, security, or MCP configurations in any config file (quick read)
- `## Learned Patterns` section in CLAUDE.md with 3+ entries (quick read)
- 5+ source files AND existing CI/CD config AND existing test files (quick glob + exists)

**Threshold:**
- 2+ advanced signals → `level = "advanced"`, `detected_via = "inferred"`
- 0-1 signals → continue to Cascade Step 3

Log: `"Advanced signals detected: {count} ({signal_list})"`

### Cascade Step 3: Ask user

Use AskUserQuestion (adapt to `{{IDIOMA}}`):

```
Question: "How would you like to proceed with setup?"
Header: "Experience"

Option 1: "Guided (Recommended)"
  Description: "Safe defaults, fewer questions, plain explanations"

Option 2: "Advanced"
  Description: "Full control over every decision, detailed technical output"
```

Store selection: `detected_via = "explicit"`

### Cascade Step 4: Persist

Write `.claude/security/user-profile.json` with detected level, method, and today's date.

Create `.claude/security/` directory first if it does not exist.

---

## Phase Behavior Table

Reference for adaptive directives throughout SKILL.md and ref files. Each row specifies what changes per level. Unlisted steps/elements behave identically at both levels.

| Step | Element | Guided | Advanced |
|------|---------|--------|----------|
| 0.2 | Welcome message | Simplified, plain language | Detailed, technical, steps listed |
| 1.0 | Platform setup | Auto-configure silently, report result | Ask before configuring (current behavior) |
| 1.3 | Discovery report | Stack + file count only | Full report with all metrics (current) |
| 1.3.1 | Extended report | Omit (proceed silently) | Full extended report (current) |
| 2.1.1 | Config summary | Project name + stack only | Full summary with all commands (current) |
| 2.2 Q0 | Mid-way integration | Simplified: 2 options (see below) | 3 options (current) |
| 2.2 Q1-Q4 | Main config | Auto-decide with safe defaults + display summary | 4 batched questions (current) |
| 2.5 | Preview display | Grouped by purpose, plain language | File tree + CLAUDE.md + placeholder table |
| 2.5 | Preview confirm | 4 options (includes "Show more detail") | 3 options |
| 4.0 | Cerbero briefing | 4-line summary | Full QUE PROTEGE / NO PROTEGE briefing (current) |
| 5.6 | Summary | Grouped by purpose | File-by-file with paths (current) |
| 5.6 | Next steps | 2 options | 3 options (current) |

---

## Safe Defaults (Guided Mode, Step 2.2)

When `USER_LEVEL == "guided"`, skip Q1-Q4 entirely. Apply these defaults:

| Decision | Default | Rationale |
|----------|---------|-----------|
| Q1 Agents | Generalistas | Covers documentation, testing, and security |
| Q2 Agent Teams | No | Simpler for non-technical users |
| Q3 Security (Cerbero) | Yes | Always beneficial, no downside |
| Q4 Git | Contextual: "Already initialized" if `.git/` exists, "Yes" otherwise | Safe in both cases |

**Exception — Q0 (mid-way only):** NOT auto-decided. Show simplified version:

```
Question (adapt to {{IDIOMA}}): "We detected an existing project. What should we do?"
Header: "Integration"

Option 1: "Set up everything (Recommended)"
  Description: "Adapt to your project, merge with existing CI/CD and docs"

Option 2: "Just scan first — show me what you'd change"
  Description: "Only analyze, don't create any files yet"
```

Map: Option 1 → `INTEGRATION_LEVEL = "full"`, Option 2 → `INTEGRATION_LEVEL = "audit"`

**Display auto-decision summary** (adapt to `{{IDIOMA}}`):

```
"--- Setup Decisions ---

 Based on your project, these defaults have been selected:
   Agents ........... Generalistas (documentation + testing + security)
   Security ......... Enabled (Cerbero framework)
   Git .............. {Already initialized / Will initialize}

 You can change any of these later by re-running /project-workflow-init."
```

---

## Preview Specifications (Step 2.5)

### Advanced Preview

Display complete file tree grouped by category, full resolved CLAUDE.md content, and placeholder resolution table.

```
"--- Generation Preview ---

 Files to be generated ({count} total):

 Project root:
   CLAUDE.md .................. project memory (~{lines} lines)
   README.md .................. project README
   .gitignore ................. git exclusions

 Documentation ({doc_count} files):
   docs/STATUS.md ............. project status tracker
   docs/DECISIONS.md .......... decision log
   docs/CHANGELOG-DEV.md ...... development changelog
   docs/SCRATCHPAD.md ......... session learning log
   docs/LESSONS-LEARNED.md .... incident post-mortems
   docs/specs/spec-template.md  feature spec template
   [if Agent Teams] docs/AGENT-COORDINATION.md — multi-agent protocol

 Agents ({agent_count}):
   .claude/agents/Lorekeeper.md  (installed now)
   [list pre-selected for workflow Phase 5]

 Rules ({rule_count}):
   .claude/rules/documentation.md
   .claude/rules/testing.md
   [if styling] .claude/rules/styling.md
   .claude/rules/compound-engineering.md
   .claude/rules/debugging.md

 Hooks ({hook_count}):
   .claude/hooks/lorekeeper-session-gate.py — SessionStart
   .claude/hooks/lorekeeper-commit-gate.py — PreToolUse
   .claude/hooks/lorekeeper-session-end.py — SessionEnd
   .claude/hooks/code-quality-gate.py — PreToolUse
   [if Cerbero] .claude/hooks/validate-prompt.py — UserPromptSubmit
   [if Cerbero] .claude/hooks/pre-tool-security.py — PreToolUse
   [if Cerbero] .claude/hooks/mcp-audit.py — PreToolUse

 Config:
   .claude/settings.local.json — hook configuration
   .claude/quality-gate.json — quality gate commands
   .claude/ignite-version.json — version tracking
   [if Agent Teams] .claude/settings.json — teams env
   [if Cerbero] .claude/security/trusted-publishers.txt

 CI/CD:
   .github/workflows/quality.yml

 Scripts:
   scripts/validate-docs.sh
   scripts/validate-placeholders.sh

--- Resolved Placeholders ---

| Placeholder | Value |
|-------------|-------|
| NOMBRE_PROYECTO | {value} |
| DESCRIPCION_CORTA | {value} |
| STACK | {value} |
| STACK_DETALLE | {value} |
| CMD_DEV | {value} |
| CMD_BUILD | {value} |
| CMD_TEST | {value} |
| CMD_LINT | {value} |
| CMD_TYPECHECK | {value} |
| PACKAGE_MANAGER | {value} |
| IDIOMA | {value} |
| FECHA | {value} |
| ... (remaining resolved placeholders) |

--- CLAUDE.md Preview ---

{resolved CLAUDE.md content}"
```

**If re-run (STATE != "fresh"):** integrate overwrite analysis icons (`[=]` `[+]` `[^]` `[~]` `[?]`) next to each file in the tree. Include legend at bottom.

### Guided Preview

Display simplified summary grouped by purpose, with key resolved values.

```
"--- What will be set up ---

 Your project will get:

   Documentation (6 files)
     Project status, decision log, changelog, learning log, post-mortems, spec template

   AI Agents (1 now + {N} later)
     Lorekeeper (documentation) — active immediately
     [list pre-selected agents for workflow Phase 5]

   Quality Rules ({rule_count} rules)
     Documentation standards, testing, code style, debugging methodology, compound learning

   Automation ({hook_count} hooks)
     Session memory, commit quality gates, code quality checks
     [if Cerbero] + security validation (prompt scanning, command safety, tool auditing)

   CI/CD Pipeline
     GitHub Actions workflow for automated quality checks

   Project Memory (CLAUDE.md)
     Your project: {NOMBRE_PROYECTO}
     Stack: {STACK}
     Commands: test ({CMD_TEST}), build ({CMD_BUILD})"
```

### Confirmation Options

**Advanced:**
```
Question (adapt to {{IDIOMA}}): "Proceed with generation?"
Header: "Preview"

Option 1: "Yes, generate all files"
  Description: "{count} files will be created"

Option 2: "Adjust configuration"
  Description: "Go back to change your selections"

Option 3: "Cancel"
  Description: "Abort without creating any files"
```

**Guided:**
```
Question (adapt to {{IDIOMA}}): "Ready to set up your project?"
Header: "Preview"

Option 1: "Yes, set it up (Recommended)"
  Description: "{count} files will be created"

Option 2: "Show me more detail"
  Description: "Switch to detailed view with full file list and CLAUDE.md preview"

Option 3: "Let me change something"
  Description: "Go back to change configuration"

Option 4: "Cancel"
  Description: "Abort without creating any files"
```

**"Show me more detail" behavior:** Set `USER_LEVEL = "advanced"` (runtime only, do NOT update persisted profile), re-display the preview in Advanced format, then show Advanced confirmation options.

### Cancel Behavior

Cancel in Step 2.5 = **abort completely**. No files are written, no Step 5 summary. Display:

```
"Setup cancelled. No files were created. Run /project-workflow-init again when ready."
```

This differs from Step 3.0 cancel (which sets all actions to "skip" and proceeds to Step 5 summary). In Step 2.5, nothing has been written yet, so a summary would be empty/useless.

### Loop-back ("Adjust configuration")

Return to Step 2.2 for re-configuration, then re-execute Step 2.5. Maximum 2 loop-backs. On the third attempt, display:

```
"You've adjusted configuration multiple times. Consider running /project-workflow-init fresh to start over."
```

Then proceed with current configuration (do not block).

---

## Directive Syntax

Inline directives in SKILL.md and ref files reference this document:

```markdown
> **Adaptive:** Present per ref-adaptive-ux.md ({Section Name})
```

Example:
```markdown
> **Adaptive:** Present per ref-adaptive-ux.md (Step 2.2 — Safe Defaults)
```

The directive tells Claude to:
1. Read the current `USER_LEVEL`
2. Look up the referenced section in this file
3. Apply the level-specific behavior described there

If `USER_LEVEL` is not set (should not happen after Step 0.1), default to `"advanced"` (preserves current behavior as fallback).

---

## Finalization Adaptations (Step 5.6)

### Guided Summary

Group by purpose, omit file paths, omit configuration table. Add Phase framing after the summary:

```
"--- Setup Complete ---

 Your project is ready with:

   Documentation — 6 files for tracking status, decisions, and learning
   AI Agents — Lorekeeper is active (documentation automation)
   Quality Rules — {rule_count} rules for documentation, testing, style, debugging
   Automation — {hook_count} hooks for session management and code quality
   [if Cerbero] Security — Cerbero framework for tool and prompt safety
   CI/CD — GitHub Actions pipeline for automated checks

 Everything is saved automatically between sessions via hooks.

 This was Phase 0: Foundation — your project infrastructure is ready.

 Next is Phase 1: Technical Landscape — where you define your stack
 decisions, evaluate tools, and scan the ecosystem for useful skills.

 You can start Phase 1 now or in a future session. Your progress is
 saved automatically via hooks."
```

### Guided Next Steps

```
Question (adapt to {{IDIOMA}}): "What would you like to do?"
Header: "Next"

Option 1: "Start Phase 1 (Recommended)"
  Description: "Define your technical landscape"

Option 2: "Stop here"
  Description: "Continue in a future session (progress saved)"
```

### Advanced Summary and Next Steps

Current behavior in ref-finalization-details.md — updated with Phase framing and Phase 1 references.

---

## Integration with Cerbero Adaptive UX

This file defines the **shared schema and detection cascade** for user level. The Cerbero-specific `ref-adaptive-ux.md` (in `.claude/skills/cerbero/`) references this schema and adds Cerbero-specific presentation tables (verdict formats, report sections, decision points).

**Profile is shared:** Both Ignite and Cerbero read/write the same `.claude/security/user-profile.json`. Whichever runs first performs the detection; the other reads the persisted result.

If Cerbero runs on a project that was NOT set up with Ignite (no profile exists), Cerbero's own detection cascade runs (defined in its `ref-adaptive-ux.md`) and creates the profile.
