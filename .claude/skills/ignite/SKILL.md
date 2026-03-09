---
name: ignite
description: 'This skill should be used when the user asks to "ignite", "start ignite", "initialize a project", "set up workflow", "create project foundation", "set up development infrastructure", "integrate workflow into existing project", or "run Phase 0". Establishes Phase 0: Foundation of the Ignite workflow methodology — creates project memory, documentation, agents, rules, hooks, quality gates, CI/CD, and security framework adapted to the detected stack. Supports new projects and mid-way integration into existing codebases.'
license: MIT
metadata:
  author: jppuche
  version: "2.2.0"
compatibility: Designed for Claude Code. Requires Python 3.8+ and Git.
argument-hint: "[project-directory]"
disable-model-invocation: true
---

# Setup Project

Phase 0: Foundation of the Ignite workflow methodology. Guides the user through project setup by asking questions, detecting existing configuration, and generating all project files from templates in `_workflow/templates/`. Adapts interaction density and detail level based on user experience (Guided / Advanced).

**Reference:** [file-map.md](references/file-map.md) contains the complete template-to-destination mapping and all placeholders.
**Adaptive UX:** [ref-adaptive-ux.md](references/ref-adaptive-ux.md) contains user level detection, behavior tables, preview specifications, and safe defaults.

---

## Step 0: Initialization

Before any scanning or discovery, establish language, experience level, and project profile. This ensures ALL subsequent output — discovery reports, configuration, preview, summary — is fully adaptive from the first interaction.

### 0.0 Batched initialization (1 AskUserQuestion call, 3 questions)

**Pre-detection (before asking):**

1. **Language inference:** Detect the language of the user's own project files. Priority order:
   - CLAUDE.md (if it existed before /ignite)
   - README.md / README
   - package.json `description` / pyproject.toml `description`
   - Comments in source files
   - **Ignore workflow files** (`_workflow/`, `.claude/skills/ignite/`, templates, guides) — always in Spanish by convention.
   - If no user files exist or language is ambiguous: default to English.

2. **User level pre-detection:** Read `.claude/security/user-profile.json` — if exists and valid, pre-fill level (skip asking). Otherwise, run lightweight signal scan:
   - CLAUDE.md with `## Hooks` section, `.claude/settings*.json` with `permissions.deny`, custom rules beyond defaults, sandbox/security/MCP config references, `## Learned Patterns` with 3+ entries, 5+ source files AND CI/CD AND tests.
   - 2+ signals → pre-fill `"Advanced"`.
   - Full detection logic: [ref-adaptive-ux.md](references/ref-adaptive-ux.md) (Detection Cascade).

3. **Profile pre-detection:** Quick scan for complexity signals:
   - Quick: <5 source files AND no CI/CD AND no architecture docs AND no test files
   - Standard: 5-50 source files OR existing CI/CD OR existing tests
   - Enterprise: 50+ source files OR architecture docs OR team config indicators OR multi-package/monorepo
   - Pre-fill the detected profile as recommended option.

**Batched AskUserQuestion** (present question in detected language, all 3 questions in 1 call):

```
Question 1 — Header: "Language"
"What language do you prefer for this project?
 All responses and documentation will use the selected language."
  1. English
  2. Espanol
  3. Portugues
  4. Francais
  (Other → free text)

Question 2 — Header: "Experience"
"How would you like to proceed with setup?"
  1. "Guided (Recommended)" — Safe defaults, fewer questions, plain explanations
  2. "Advanced" — Full control over every decision, detailed technical output
  (Pre-select if signal scan detected a level)

Question 3 — Header: "Profile"
"What kind of project is this?"
  1. "Quick" — Script, POC, hobby, CLI tool. Fast setup, skip planning phases.
  2. "Standard (Recommended)" — App, API, library. Full setup with streamlined planning.
  3. "Enterprise" — Complex system, multi-team, critical. All phases, maximum depth.
  (Pre-select based on complexity signals)
```

**If user level was pre-detected from profile file:** omit Question 2. Show only Language + Profile (2 questions).

**Store results:**
- `{{IDIOMA}}` — language selection. From this point forward:
  - **All human-facing text** uses the selected language
  - **Generated docs** (STATUS, DECISIONS, CHANGELOG-DEV, SCRATCHPAD, CLAUDE.md, AGENT-COORDINATION) written in selected language
  - **Technical elements stay in English:** file names, placeholder keys, JSON config keys, code, hook events
  - Templates contain Spanish as base text — adapt natural-language portions to selected language
- `USER_LEVEL` ("guided" | "advanced") — persist to `.claude/security/user-profile.json` (create `.claude/security/` if needed). All steps reference via adaptive directives — see [ref-adaptive-ux.md](references/ref-adaptive-ux.md)
- `PROJECT_PROFILE` ("quick" | "standard" | "enterprise") — stored in STATUS.md and used to gate phases/questions throughout

### 0.1 Welcome message

> **Adaptive:** Present per [ref-adaptive-ux.md](references/ref-adaptive-ux.md) (Welcome). Adapt all text to `{{IDIOMA}}`.

Present the complete workflow as an integral vision. The user understands from the first moment that they are entering a structured process. Phase 0 is presented as the first step of the journey.

**Display — Guided** (adapt to `{{IDIOMA}}`):

Phase list adapts to `PROJECT_PROFILE` (detected in Step 0.0). Quick shows only active phases (0 + N). Standard/Enterprise show full workflow.

**If `PROJECT_PROFILE == "quick"`:**
```
--- Ignite ---

You get code — but no structure around it. No quality gates, no memory
between sessions, no security checks. Context gets lost after every
/clear. Mistakes repeat.

Ignite sets up the infrastructure your project is missing — adapted
to your stack:

  Phase 0  Foundation ............. Project memory, docs, automation
  Phase N  Development Blocks ..... Start building immediately

Quick profile — straight to building. No planning phases needed.
We start with Phase 0. Most values are auto-detected.
```

**If `PROJECT_PROFILE == "standard"` or `"enterprise"`:**
```
--- Ignite ---

You get code — but no structure around it. No quality gates, no memory
between sessions, no security checks. Context gets lost after every
/clear. Mistakes repeat.

Ignite sets up the infrastructure your project is missing — adapted
to your stack. Here's the full workflow:

  Phase 0  Foundation ............. Project memory, docs, automation
  Phase 1  Technical Landscape .... Research, stack decisions, ecosystem
  Phase 2  Tooling & Security ..... Evaluate and install tools
  Phase 3  Intelligence Review .... Review docs with installed tools
  Phase 4  Architecture Blueprint . Detailed design + plan hardening
  Phase N  Development Blocks ..... Team setup, then build iteratively
  Final    Hardening .............. Security, performance, production

Each phase builds on the last. It handles the complex parts so you
can focus on building.

We start with Phase 0. Most values are auto-detected.
```

**Display — Advanced** (adapt to `{{IDIOMA}}`):

Phase list adapts to `PROJECT_PROFILE`. Quick shows only active phases.

**If `PROJECT_PROFILE == "quick"`:**
```
--- Ignite — Phase 0: Foundation ---

No quality gates, no session memory, no security checks — Ignite sets
up the infrastructure your project is missing. Every technical decision
is documented, every session builds on the last (compound engineering),
and quality gates enforce standards automatically.

  Phase 0  Foundation ............. Project memory, docs, agents, hooks, CI/CD
  Phase N  Development Blocks ..... Team assembly (N.0) → Ralph Loop per spec

Quick profile — phases 1-4 and Final are skipped.

Phase 0 creates the infrastructure. Steps:
  1. Discovery — scan project, detect stack, analyze context
  2. Configuration — resolve values, collect decisions
  3. Preview — dry-run of all files before writing
  4. Generation — process templates, write files
  5. Finalization — validate, cleanup, summary + next steps
```

**If `PROJECT_PROFILE == "standard"` or `"enterprise"`:**
```
--- Ignite — Phase 0: Foundation ---

No quality gates, no session memory, no security checks — Ignite sets
up the infrastructure your project is missing. Every technical decision
is documented, every session builds on the last (compound engineering),
and quality gates enforce standards automatically.

  Phase 0  Foundation ............. Project memory, docs, agents, hooks, CI/CD
  Phase 1  Technical Landscape .... External research, top-3 stack comparison, ecosystem scan
  Phase 2  Tooling & Security ..... Cerbero evaluation, skill/MCP installation
  Phase 3  Intelligence Review .... FOUNDATION.md review + decision re-evaluation with installed tools
  Phase 4  Architecture Blueprint . System design (4A) + plan hardening (4B)
  Phase N  Development Blocks ..... Team assembly (N.0) → Ralph Loop per spec
  Final    Hardening .............. Security audit, performance, accessibility

Phase 0 creates the infrastructure. Steps:
  1. Discovery — scan project, detect stack, analyze context
  2. Configuration — resolve values, collect decisions
  3. Preview — dry-run of all files before writing
  4. Generation — process templates, write files
  5. Finalization — validate, cleanup, summary + next steps
```

Phase names adapt to `{{IDIOMA}}` (e.g., "Fase 0: Fundamentos", "Fase 1: Panorama Tecnico").

---

## Step 1: Discovery

Merged scan + Foundational Discovery. Scans the project, runs structured Q&A, and generates FOUNDATION.md before any technical scaffolding.

**Full methodology:** [ref-foundational-discovery.md](references/ref-foundational-discovery.md)
**Summary:** Platform detection → Comprehensive scan → Deep exploration → Structured Q&A → FOUNDATION.md → Profile validation → Combined report

### 1.0 Platform detection (silent)

Detect OS, configure Python command and Git Bash (Windows). Store PYTHON_CMD for Step 3.2 and 4.4.

**Full logic:** [ref-platform-detection.md](references/ref-platform-detection.md)

### 1.1 Comprehensive scan (ONE pass)

Scan everything in a single pass: project files, stack detection, maturity, conventions, CI/CD, prior initialization, and mid-way detection.

**1.1.1 Stack and files:**
```
Check for (in order):
- package.json        → extract: name, description, scripts (dev, build, test, lint, typecheck)
- tsconfig.json       → TypeScript project
- pyproject.toml      → Python project (extract: name, description, scripts)
- Cargo.toml          → Rust project
- go.mod              → Go project
- composer.json       → PHP project
- Gemfile             → Ruby project
- pom.xml / build.gradle → Java/Kotlin project

Package manager detection (Node projects only):
- yarn.lock → Yarn, pnpm-lock.yaml → pnpm, bun.lockb → Bun, package-lock.json → npm, (none) → npm default
Store as {{PACKAGE_MANAGER}}.
```

**1.1.2 Prior initialization:**
```
EXISTING_FILES = {}   # map: destination_path → { exists, category, size_lines }

For each entry in references/file-map.md Template Mapping tables:
  destination = resolved destination path
  category    = OW column value (A, B, C, or --)
  EXISTING_FILES[destination] = { exists: file_exists, category: category, size_lines: count_if_exists }

# Classify initialization state (use only "always generated" files)
core_total = count entries in "always generated" sections of file-map.md
existing_count = count entries where exists == true

STATE = "fresh" if existing_count == 0
      | "partial" if existing_count < core_total * 0.5
      | "full" otherwise
```

Ignore `.claude/skills/ignite/`, `_workflow/templates/`, `_workflow/guides/` when assessing `.claude/` initialization.

**1.1.3 Project context (mid-way detection):**
```
CONTEXT_SCAN = {
  existing_claude_md, existing_docs, existing_ci, existing_architecture,
  conventions, commit_style, maturity
}

PROJECT_MODE = "mid-way" if source_files > 0 AND STATE != "full"
             | "fresh" otherwise
```

Full context scan logic unchanged from previous version — reads CLAUDE.md sections, docs, CI/CD, architecture docs, naming conventions, git history, code maturity.

Store `EXISTING_FILES`, `STATE`, `CONTEXT_SCAN`, and `PROJECT_MODE` for Steps 2 and 3.

### 1.2 Deep exploration (profile-scaled)

Read ALL available project materials before asking questions. Depth scales with profile:
- **Quick:** Scan README + package manifest + directory structure. 1-2 min.
- **Standard:** Add existing specs, architecture docs, key source files. 3-5 min.
- **Enterprise:** Thorough reading of all project documentation, reference projects, business context. 5-10 min.

See [ref-foundational-discovery.md](references/ref-foundational-discovery.md) Section 1 for full exploration methodology.

### 1.3 Structured Q&A (profile-scaled)

Multiple-choice questions with descriptions, batched 3-4 per AskUserQuestion call. Depth scales with profile:
- **Quick:** 1 call (vision + scope + key constraint). Fast convergence.
- **Standard:** 2-3 calls. Vision → features → behaviors → constraints.
- **Enterprise:** 3-5 calls (soft limit: 8 rounds max). Comprehensive.

**Core rules:** Never assume. Each round builds on previous answers. No fixed questionnaire — categories adapt to project type. See [ref-foundational-discovery.md](references/ref-foundational-discovery.md) Section 2.

After Q&A rounds, present a brief synthesis. Stay in dialogue until the user confirms understanding is correct.

### 1.4 Profile validation

Count complexity indicators from the Q&A and project scan. If the project exceeds or falls below its profile threshold, suggest adjustment with specific reasons. User always has final say.

See [ref-foundational-discovery.md](references/ref-foundational-discovery.md) Section 5 for thresholds and logic.

### 1.5 Generate docs/FOUNDATION.md

Generate the foundational document based on Q&A results. Technology-agnostic. Includes instruction block for consuming agents.

Structure and depth adapt to project type and profile. See [ref-foundational-discovery.md](references/ref-foundational-discovery.md) Section 4.

### 1.6 Combined report

> **Adaptive:** If `USER_LEVEL == "guided"`, show abbreviated report (stack + file count + Discovery summary). If `USER_LEVEL == "advanced"`, show full report with all metrics. See references/ref-adaptive-ux.md (Phase Behavior Table).

Present ONE combined report covering scan results + Discovery summary + inferred configuration (adapt to `{{IDIOMA}}`):

```
Display:
  "--- Discovery Complete ---

   Project: {name from Q&A or package manifest}
   Stack: {detected_stack or 'pending configuration'}
   Profile: {PROJECT_PROFILE}
   Platform: {OS} / Python: {PYTHON_CMD}
   Prior initialization: {STATE} ({existing_count}/{core_total} workflow files)

   FOUNDATION.md: Generated ({line_count} lines, {section_count} sections)
   Key capabilities: {2-3 bullet summary from FOUNDATION.md}

   [if mid-way:]
   Codebase: {source_files} files (~{estimated_loc} LOC)
   CI/CD: {ci_type or 'none'}
   Tests: {has_tests ? 'found' : 'not detected'}

   Your customizations are safe — nothing is overwritten without confirmation."
```

---

## Step 2: Configuration

Resolve project configuration from Step 1 detections. Only ask the user when values cannot be inferred.

### 2.0 Language (already determined in Step 0.0)

`{{IDIOMA}}` was set during initialization (Step 0.0). Proceed to 2.1.

### 2.1 Auto-resolved values

Resolve each value using the chain: **config file → inferencia del stack → default → preguntar**. Solo preguntar como ultimo recurso si no hay datos suficientes.

| Placeholder | Resolution chain |
|-------------|-----------------|
| `{{NOMBRE_PROYECTO}}` | package.json `name` / pyproject.toml `name` / Cargo.toml `name` → nombre del directorio raiz → **preguntar** |
| `{{DESCRIPCION_CORTA}}` | package.json `description` / pyproject.toml `description` → generar "Proyecto {name}" automaticamente → **preguntar** |
| `{{STACK}}`, `{{STACK_DETALLE}}`, `{{STACK_BACKEND}}`, `{{STACK_FRONTEND}}` | Inferir del proyecto: archivos de config (tsconfig, pyproject, Cargo, go.mod, etc.), dependencias instaladas, estructura de carpetas. Nunca preguntar. |
| `{{CMD_DEV}}` | package.json `scripts.dev` / inferir del stack (ej: `python manage.py runserver`, `cargo run`) → `{{PACKAGE_MANAGER}} run dev` |
| `{{CMD_BUILD}}` | package.json `scripts.build` / inferir del stack → `{{PACKAGE_MANAGER}} run build` |
| `{{CMD_TEST}}` | package.json `scripts.test` / inferir del stack (ej: `pytest`, `cargo test`, `go test ./...`) → `{{PACKAGE_MANAGER}} run test` |
| `{{CMD_LINT}}` | package.json `scripts.lint` / inferir del stack → `{{PACKAGE_MANAGER}} run lint` |
| `{{CMD_TYPECHECK}}` | package.json `scripts.typecheck` / inferir del stack → `{{PACKAGE_MANAGER}} run typecheck` |

### 2.1.1 Stack profile resolution

After resolving stack values, determine the stack profile and resolve domain-specific placeholders. **Stack profiles:** [ref-stack-profiles.md](references/ref-stack-profiles.md)

1. **Select profile:** Match detected config files from Step 1.1 against the profile selection logic in references/ref-stack-profiles.md (priority-ordered: most specific framework first, Generic as fallback).

2. **Resolve domain placeholders** from the matched profile:

| Placeholder | Content |
|-------------|---------|
| `{{DOMAIN_BACKEND}}` | Backend paths as markdown bullet list with descriptions |
| `{{DOMAIN_FRONTEND}}` | Frontend paths as markdown bullet list (N/A if profile has none) |
| `{{TEST_DOMAIN}}` | Test patterns, locations, and config files as markdown bullets |
| `{{TEST_PATHS_FRONTMATTER}}` | Test path globs formatted as YAML list items (`  - "pattern"`) |
| `{{STYLING_PATHS_FRONTMATTER}}` | Styling path globs as YAML list items (empty if styling N/A) |
| `{{CRITICAL_RULES_BACKEND}}` | Security and quality rules specific to the stack |
| `{{CRITICAL_RULES_FRONTEND}}` | Design and UX rules (empty if no frontend) |
| `{{CI_SETUP}}` | GitHub Actions setup steps as YAML (actions/setup-node, setup-python, etc.) |

3. **Full-stack handling:** If both backend and frontend frameworks are detected (e.g., Next.js with React), use the backend profile for `{{DOMAIN_BACKEND}}` and frontend portion for `{{DOMAIN_FRONTEND}}`. For test/styling, use the frontend framework profile.

4. **Store `STYLING_APPLICABLE`** flag from profile (Yes/No/Conditional). Used in Step 3.3 to decide whether to generate styling.md rule.

After resolving, display summary to user (informational, not a question). Adapt to `{{IDIOMA}}`.

> **Adaptive:** If `USER_LEVEL == "guided"`, show only project name and stack (omit command breakdown — it's not actionable for non-technical users). If `USER_LEVEL == "advanced"`, show full summary. See references/ref-adaptive-ux.md (Phase Behavior Table).

**Advanced summary:**
```
"--- Configuration Summary ---

   Project:   {nombre}
   About:     {desc}
   Stack:     {stack detalle}
   Profile:   {profile name}

   Commands:
     dev ........... {cmd_dev}
     build ......... {cmd_build}
     test .......... {cmd_test}
     lint .......... {cmd_lint}
     typecheck ..... {cmd_typecheck}

   Values marked N/A will be skipped in quality gates and CI."
```

**Guided summary:**
```
"--- Configuration ---
   Project: {nombre} — {desc}
   Stack:   {stack detalle}"
```

### 2.2 Project configuration

> **Adaptive:** If `USER_LEVEL == "guided"`, skip Q1-Q4 entirely and auto-decide with safe defaults. Q0 is shown in simplified form if mid-way project detected. See references/ref-adaptive-ux.md (Safe Defaults, Phase Behavior Table).

Present in `{{IDIOMA}}` (selected in Step 0.0).

#### Q0: Integration Level (header: "Integration") — only if PROJECT_MODE == "mid-way"

**Skip this question entirely if PROJECT_MODE == "fresh".**

**Advanced (3 options):**

Use AskUserQuestion with 1 question BEFORE the main configuration block:

```
Question (adapt to {{IDIOMA}}): "Existing project detected. What integration level do you prefer?"
  1. "Full integration (Recommended)" — Adapt CLAUDE.md to the project, merge CI/CD, respect existing conventions and architecture
  2. "Workflow only" — Install only the workflow framework (docs, hooks, rules) without touching existing CI/CD or CLAUDE.md
  3. "Audit first" — Only scan and report findings, generate nothing yet
```

**Guided (2 options, simplified language):**

```
Question (adapt to {{IDIOMA}}): "We detected an existing project. What should we do?"
  1. "Set up everything (Recommended)" — Adapt to your project, merge with existing CI/CD and docs
  2. "Just scan first — show me what you'd change" — Only analyze, don't create any files yet
```

Map: Guided option 1 → `INTEGRATION_LEVEL = "full"`, Guided option 2 → `INTEGRATION_LEVEL = "audit"`.

Store as `INTEGRATION_LEVEL` ("full" | "workflow_only" | "audit").

If `INTEGRATION_LEVEL == "audit"`: display CONTEXT_SCAN results in detail, then stop execution. User can re-run `/ignite` later with decisions made.

If `INTEGRATION_LEVEL == "workflow_only"`: set flags `SKIP_CICD_MERGE = true`, `SKIP_CLAUDE_MERGE = true`.

Then proceed to main configuration for "full" and "workflow_only" modes.

#### Profile-gated configuration

The number of config questions depends on `PROJECT_PROFILE`:

| Profile | Questions | Behavior |
|---------|-----------|----------|
| **Quick** | 0 | Auto-decide all: Lorekeeper only, no teams, no Cerbero, git auto-detected |
| **Standard** | 2 (Agents + Security) | Git auto-detected, Teams auto-decided (No) |
| **Enterprise** | 3 (Agents + Teams + Security) | Git auto-detected |

Git is always auto-detected (not asked): if `.git/` exists → "Already initialized", add `.gitignore` entries. If not → `git init` + main branch + `.gitignore`.

**Quick profile auto-decisions:**

| Decision | Default | Stored as |
|----------|---------|-----------|
| Agents | Lorekeeper only | Pre-selected: Lorekeeper only |
| Agent Teams | No | Agent Teams = disabled |
| Security | No (Cerbero) | Cerbero = disabled |
| Git | Contextual | Auto-detected from .git/ |

Display brief summary (adapt to `{{IDIOMA}}`):
```
"Quick profile — auto-configured: Lorekeeper only, no security framework.
 Git: {Already initialized / Will initialize}."
```
Then proceed directly to Step 2.5 (Preview).

#### Main configuration — Guided mode (auto-decide)

If `USER_LEVEL == "guided"` AND `PROJECT_PROFILE != "quick"`: skip remaining questions. Apply safe defaults:

| Decision | Default | Stored as |
|----------|---------|-----------|
| Q1 Agents | Generalistas | Pre-selected: Lorekeeper + Inquisidor + Sentinel |
| Q2 Agent Teams | No | Agent Teams = disabled |
| Q3 Security | Yes (Cerbero) | Cerbero = enabled |
| Q4 Git | "Already initialized" if `.git/` exists, "Yes" otherwise | Git = contextual |

Display auto-decision summary (adapt to `{{IDIOMA}}`):

```
"--- Setup Decisions ---

 Based on your project, these defaults have been selected:
   Agents ........... Generalistas (documentation + testing + security)
   Security ......... Enabled (Cerbero framework)
   Git .............. {Already initialized / Will initialize}

 You can change any of these later by re-running /ignite."
```

Register selections in STATUS.md (same as Advanced mode). Then proceed to Step 2.5 (Preview).

#### Main configuration — Advanced mode (profile-gated questions)

If `USER_LEVEL == "advanced"` AND `PROJECT_PROFILE != "quick"`:

Combine decisions into **one AskUserQuestion call**. Number of questions depends on profile:
- **Standard:** 2 questions (Q1 Agents + Q3 Security). Q2 Teams auto-decided (No), Q4 Git auto-detected.
- **Enterprise:** 3 questions (Q1 Agents + Q2 Teams + Q3 Security). Q4 Git auto-detected.

Use AskUserQuestion:

#### Q1: Agents (header: "Agents")

Question (adapt to `{{IDIOMA}}`): "Which agents to install? (Lorekeeper always included)"

Build options contextually:

- **Option 1 (always first):** Generalistas — Lorekeeper + Inquisidor + Sentinel. Description: covers documentation, testing, and security.
- **Option 2 (contextual, only if full-stack/backend+frontend detected):**
  - Full-stack (frontend + backend) → "Generalists + Workers" — + backend-worker + frontend-worker
  - API/backend only → "Generalists + backend-worker"
  - Frontend only → "Generalists + frontend-worker"
- **Last option (always):** "Lorekeeper only" — minimal, just automatic documentation.
  Description: "Only compound engineering and documentation. No testing agent (Inquisidor), no security audits (Sentinel). Quality gates rely entirely on hooks."

If full-stack/backend+frontend detected: recommend "Generalists + Workers" (move to first position with "(Recommended)").
Otherwise: recommend "Generalists" as first option with "(Recommended)".

Register selection in STATUS.md. Actual agent installation (except Lorekeeper) happens in Phase N (Step N.0: Team Assembly) of the project workflow.

#### Q2: Teams (header: "Teams")

Question (adapt to `{{IDIOMA}}`): "Enable Agent Teams for multi-agent coordination?"

Recommendation criteria:
- Full-stack with frontend/backend separation → recommend Yes (first option)
- Monorepo with multiple packages/workspaces → recommend Yes (first option)
- Simple project, CLI, library, or script → recommend No (first option)

2 options: Yes / No. Add "(Recommended)" to the recommended one and place it first. Include reasoning in description (e.g., "Full-stack with frontend/backend separation" or "Simple project / CLI / library").

#### Q3: Security (header: "Security")

Question (adapt to `{{IDIOMA}}`): "Install Cerbero security framework? Evaluates MCPs/Skills, detects rug pulls, blocks prompt injection."

2 options (always the same):
1. "Yes (Recommended)" — description: First-line defense — catches known CVEs, destructive commands, obvious injection. Not comprehensive (see Limitations in README)
2. "No" — description: No security framework

#### Q4: Git (header: "Git")

Question (adapt to `{{IDIOMA}}`): "Initialize git repository?"

Build options based on detection:
- If `.git/` detected: 2 options
  1. "Already initialized (Recommended)" — description: Detected .git/ on {branch} — just add .gitignore entries
  2. "Reinitialize" — description: git init from scratch (destructive)
- If `.git/` NOT detected: 2 options
  1. "Yes (Recommended)" — description: git init + main branch + .gitignore
  2. "No" — description: No version control

### Auto-generated values (do not ask)

| Placeholder | Value |
|-------------|-------|
| `{{FECHA}}` | Today's date (YYYY-MM-DD) |
| `{{FASE_ACTUAL}}` | "Phase 0: Foundation" (adapt to `{{IDIOMA}}` — see below) |
| `{{PENDIENTE}}` | "Phase 1: Technical Landscape" (adapt to `{{IDIOMA}}` — see below) |

> **IDIOMA adaptation for FASE_ACTUAL / PENDIENTE:**
> - English: "Phase 0: Foundation" / "Phase 1: Technical Landscape"
> - Espanol: "Fase 0: Fundamentos" / "Fase 1: Panorama Tecnico"
> - Portugues: "Fase 0: Fundacao" / "Fase 1: Panorama Tecnico"
> - Francais: "Phase 0: Fondation" / "Phase 1: Paysage Technique"

---

## Step 2.5: Preview (dry-run)

After all placeholders are resolved and all decisions are captured, display a preview of what will be generated. The user must confirm before any files are written.

> **Adaptive:** Preview format and confirmation options adapt to `USER_LEVEL`. See [ref-adaptive-ux.md](references/ref-adaptive-ux.md) (Preview Specifications).

**Full logic:** [ref-generation-details.md](references/ref-generation-details.md) — sections 2.5.1 through 2.5.4.

**Summary:**

1. **Build file manifest** from [file-map.md](references/file-map.md) — resolve conditions (styling, Cerbero, Teams) to determine which files will actually be generated.
2. **Resolve key files in memory** (do NOT write yet): CLAUDE.md and quality-gate.json.
3. **Display preview** — Advanced: file tree + resolved CLAUDE.md + placeholder table. Guided: grouped by purpose in plain language.
4. **Ask confirmation:**
   - **Generate** → proceed to Step 3.
   - **Adjust** → return to Step 2.2 (max 2 loop-backs).
   - **Cancel** → abort completely, no files written, no Step 5 summary.
   - **Show more detail** (Guided only) → switch to Advanced preview, re-display.

If re-run (STATE != "fresh"): the preview integrates the overwrite analysis from Step 3.0, showing icons (`[=]` `[+]` `[^]` `[~]` `[?]`) next to each file.

---

## Step 3: Generation

Read each template from `_workflow/templates/`, replace placeholders with collected values, write to destination. See [file-map.md](references/file-map.md) for the complete mapping.

### 3.0 Pre-generation analysis (overwrite protection)

If STATE == "fresh": skip to 3.1. Otherwise, analyze each existing file by category (A/B/C) to determine action (skip/merge/replace/ask). Display report and get user confirmation.

**Full logic:** [ref-generation-details.md](references/ref-generation-details.md) — sections 3.0.1 through 3.0.7 and 3.1.

### 3.1 Core files

Generate CLAUDE.md, docs (STATUS, DECISIONS, CHANGELOG-DEV, SCRATCHPAD, LESSONS-LEARNED, spec-template), and scripts (validate-docs.sh, validate-placeholders.sh). Respect overwrite analysis from 3.0.

**Full logic:** [ref-generation-details.md](references/ref-generation-details.md) — section 3.1 (9 files with per-category handling).

### 3.2 Lorekeeper + hooks (always, immediately after core files)

Lorekeeper se instala siempre en Step 3 (Phase 0). Es el unico agente necesario durante setup.

1. `./.claude/agents/Lorekeeper.md` (Category C):
   - If not exists: read template → replace placeholders → write.
   - If action == "skip" or "skip_customized": no changes.
   - If action == "merge": add missing sections from template, preserve existing content.

2. Install Lorekeeper hooks (Category B, copy as-is, no placeholders):
   - `lorekeeper-session-gate.py` — SessionStart: context + pending items + version check
   - `lorekeeper-commit-gate.py` — PreToolUse: blocks commits if docs stale
   - `lorekeeper-session-end.py` — SessionEnd: checkpoint + pending items + graduation candidate analysis
   For each hook (session-gate, commit-gate, session-end):
   - If not exists: copy from `_workflow/templates/hooks/lorekeeper/`.
   - If action == "skip": no changes. Log: "{hook} esta actualizado."
   - If action == "replace": overwrite. Log: "{hook} actualizado a nueva version."

3. Create or merge `.claude/settings.local.json` with Lorekeeper hook configuration.

> **Nota cross-platform:** Paths relativos (no `$CLAUDE_PROJECT_DIR`) para compatibilidad. `$CLAUDE_PROJECT_DIR` no se expande en Windows (bug: [#6023](https://github.com/anthropics/claude-code/issues/6023), [#5049](https://github.com/anthropics/claude-code/issues/5049)).

> **Python command:** Usar PYTHON_CMD detectado en Step 1.0 (`python` en Windows, `python3` en macOS/Linux).

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-session-gate.py" }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/env-protection.py" }]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-commit-gate.py" },
          { "type": "command", "command": "{PYTHON_CMD} .claude/hooks/code-quality-gate.py" },
          { "type": "command", "command": "{PYTHON_CMD} .claude/hooks/env-protection.py" }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-session-end.py" }]
      }
    ]
  }
}
```

> Si `.claude/settings.local.json` ya existe (re-run de /ignite), leer y mergear hooks sin duplicar.

> **Hook ordering:** All PreToolUse hooks fire before tool execution; any `exit(2)` blocks the tool. Registration order affects feedback order only (which hook's message the user sees first), not blocking priority.

> **Consolidation note:** Lorekeeper hooks (Step 3.2) and Cerbero hooks (Step 4.4) are kept in separate entries for modularity. Performance impact is negligible.

4. Add default `permissions.deny` to `settings.local.json` (defense-in-depth complementing pre-tool-security.py):

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf /)",
      "Bash(rm -rf ~)",
      "Bash(:(){ :|:& };:)",
      "Bash(*curl*|*sh*)",
      "Bash(*wget*|*bash*)"
    ]
  }
}
```

> Merge into existing `permissions.deny` array without duplicating entries.

5. Install code quality gate hook (Category B, copy as-is):
   - From: `_workflow/templates/hooks/code-quality-gate.py`
   - To: `./.claude/hooks/code-quality-gate.py`
   - If not exists: copy. If exists and identical: skip. If different: replace.

6. Install env protection hook (Category B, copy as-is):
   - From: `_workflow/templates/hooks/env-protection.py`
   - To: `./.claude/hooks/env-protection.py`
   - If not exists: copy. If exists and identical: skip. If different: replace.
   - Register in `settings.local.json` with **two specific matchers** (Read + Bash):
   ```json
   {
     "PreToolUse": [
       {
         "matcher": "Read",
         "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/env-protection.py" }]
       },
       {
         "matcher": "Bash",
         "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/env-protection.py" }]
       }
     ]
   }
   ```
   > **Note:** Grep tool has no PreToolUse matcher in CC. Grep access to .env is lower risk (returns content matches, not full file contents). This limitation is documented.
   > **Behavior:** Read → **block** (deny + reason). Bash → **warn** (allow + additionalContext).

7. Generate `.claude/quality-gate.json` with resolved commands from Step 2.1:

```json
{
  "commands": {
    "typecheck": "{{CMD_TYPECHECK}}",
    "lint": "{{CMD_LINT}}",
    "test": "{{CMD_TEST}}"
  },
  "timeout_seconds": 60
}
```

For commands that are "N/A" for the detected stack (e.g., no typecheck for Python without mypy): include as `"N/A"`. The hook skips N/A commands at runtime.

Overwrite: replace if different (Category B).

8. Generate `.claude/ignite-version.json` (version tracking for auto-update):

Read the `version` field from `.claude-plugin/plugin.json` (canonical source of truth for Ignite version). Use that value as `{{IGNITE_VERSION}}` below:

```json
{
  "version": "{{IGNITE_VERSION}}",
  "installed_date": "{{FECHA}}",
  "source": "Ignite"
}
```

Overwrite: replace if different (Category B). This file tracks when /ignite was last run and which version was installed. The session-gate hook compares its embedded version constant with this file to detect version drift.

9. Generate `.claude/lorekeeper-config.json` (Lorekeeper context adaptation):

Build the config mapping logical doc roles to actual paths and thresholds. All Lorekeeper hooks and `validate-docs.sh` read this config at runtime instead of using hardcoded paths.

**For greenfield projects** (standard structure), use defaults:

```json
{
  "version": "1.0",
  "docs": {
    "scratchpad":      { "path": "docs/SCRATCHPAD.md",      "max_lines": 150, "graduation_threshold": 100 },
    "changelog":       { "path": "docs/CHANGELOG-DEV.md",   "check_freshness": true },
    "status":          { "path": "docs/STATUS.md",           "max_lines": 60 },
    "decisions":       { "path": "docs/DECISIONS.md" },
    "lessons_learned": { "path": "docs/LESSONS-LEARNED.md" }
  },
  "claude_md": {
    "path": "CLAUDE.md",
    "max_lines": 200,
    "warn_threshold": 180
  },
  "validation_script": "scripts/validate-docs.sh"
}
```

**For mid-way projects** (Ignite installed in existing project with custom doc structure): scan `docs/` during Step 1.1 and map existing files to logical roles by name matching (e.g., `docs/system/status.md` → role `status`). Present the inferred mapping as **1 confirmation question** via AskUserQuestion:

> "Lorekeeper detected this doc structure for session management. Is this correct?"
> - Option 1: "Yes, use this mapping" (Recommended)
> - Option 2: "Adjust" — user provides corrections

If no existing docs match a role, use the default path (Ignite will create the file in Step 3.1).

Overwrite: replace if different (Category B). If config already exists and differs, replace — the config reflects the current project state. If identical, skip.

Los demas agentes (Inquisidor, Sentinel, backend-worker, frontend-worker) se instalan en Phase N Step N.0 (Team Assembly) del workflow, cuando la arquitectura este definida y las skills asignadas. La pre-seleccion del usuario (seccion 2.2) queda registrada en `docs/STATUS.md`.

### 3.3 Rules (respecting overwrite analysis)

For each rule template in `_workflow/templates/rules/` (all Category C):

Before writing each rule, check ANALYSIS:
- If not exists: read template → write destination.
- If action == "skip": identical to template, no changes.
- If action == "skip_customized": user has customized, do not touch.
- If action == "merge": add missing sections from template to existing file.

1. `documentation.template.md` → `./.claude/rules/documentation.md`
2. `testing.template.md` → `./.claude/rules/testing.md` (replace `{{TEST_PATHS_FRONTMATTER}}`)
3. `styling.template.md` → `./.claude/rules/styling.md` (replace `{{STYLING_PATHS_FRONTMATTER}}`)
   - **Conditional generation:** Check `STYLING_APPLICABLE` flag from Step 2.1.1:
     - If "No": skip generation entirely. Log: "styling.md omitido: proyecto sin frontend UI detectado."
     - If "Conditional" with condition: verify condition is met (e.g., templates/ directory exists). Skip if not met.
     - If "Yes": generate normally.
4. `compound-engineering.template.md` → `./.claude/rules/compound-engineering.md` (no placeholders)
5. `debugging.template.md` → `./.claude/rules/debugging.md` (no placeholders)

### 3.4 Agent Coordination (if Agent Teams enabled, Category A)

- If not exists: read template → replace placeholders → write `./docs/AGENT-COORDINATION.md`.
- If action == "skip": all 13 sections present, no changes.
- If action == "merge": insert missing sections at their correct ordinal position. Preserve all existing content within existing sections.

### 3.5 CI/CD Infrastructure

Generate GitHub Actions workflow from the CI template. The code-quality-gate hook (item 5) and quality-gate.json (item 7) are already installed in Step 3.2.

1. Generate GitHub Actions workflow from template:
   - Read: `_workflow/templates/ci/quality.template.yml`
   - Replace: `{{CMD_TYPECHECK}}`, `{{CMD_LINT}}`, `{{CMD_TEST}}`, `{{CMD_BUILD}}`, `{{CI_SETUP}}`
   - **Remove** steps where the command is `"N/A"` (do not include them in the final yml)
   - Write to: `./.github/workflows/quality.yml`
   - If not exists: write. If exists and different: replace (Category B).

---

## Step 4: Security (if Cerbero enabled)

**Skip entirely for Quick profile** (Cerbero auto-disabled).

Only execute if user answered Yes to Cerbero in Step 2.2 (Q3: Security). Installs Cerbero skill, security hooks, trusted-publishers list, and configures hooks in settings.local.json.

**Full logic:** [ref-cerbero-installation.md](references/ref-cerbero-installation.md) — sections 4.0 through 4.5.

---

## Step 5: Finalization

### 5.1 Agent Teams configuration (if enabled)

Create `.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TEAMS": "true"
  }
}
```

### 5.2 Git initialization (if requested)

```bash
git init
git checkout -b main
# Suggest initial commit but let user decide
```

### 5.3 Create .gitignore (if not exists)

Append workflow-relevant entries (do not overwrite existing):
```
.claude/settings.local.json
.claude/security/audit-*.log
.claude/lorekeeper-pending.json
*.local.md
secrets/
.env
.env.*
```

### 5.4 Validate

Run: `bash scripts/validate-docs.sh`

If errors: fix automatically before continuing.

### 5.5-5.6 Cleanup and Summary

Move skill README.md to docs/ignite-reference.md, generate project README.md from template (README.template.md with NOMBRE_PROYECTO, DESCRIPCION_CORTA, STACK, FECHA), cleanup setup files (skill dir, templates/), display comprehensive summary with AskUserQuestion for next steps.

**Full logic:** [ref-finalization-details.md](references/ref-finalization-details.md)

---

## Error Handling

Covers: missing templates, missing placeholders, existing CLAUDE.md, git conflicts, and per-category overwrite protection edge cases (corrupted files, encoding, empty files, line limits).

**Full logic:** [ref-error-handling.md](references/ref-error-handling.md)
