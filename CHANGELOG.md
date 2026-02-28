# Changelog

All notable changes to Ignite are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] - 2026-02-28

### Added
- **Foundational Discovery** — merged into Phase 0. Structured Q&A generates `FOUNDATION.md` (technology-agnostic project context document) before any technical scaffolding. Scales with profile: Quick (1 Q&A round, abbreviated doc), Standard (2-3 rounds, full doc), Enterprise (3-5 rounds, comprehensive doc with appendices). Methodology in `ref-foundational-discovery.md`.
- **Project Profiles** — Quick/Standard/Enterprise profiles gate which phases execute and how many config questions are asked. Quick skips planning phases (0→N). Standard includes streamlined planning. Enterprise runs all phases at maximum depth. Auto-detected from project complexity, user confirms.
- **`.env` protection hook** — always installed. Blocks AI agent from reading `.env`, `secrets/`, credentials files (Read→block, Bash→warn). Registered with specific matchers (Read + Bash) to avoid intercepting all tool calls.
- **Batched initialization** — Language + Experience Level + Profile determined in a single AskUserQuestion call (was 2 separate calls). Profile pre-detection from project complexity signals.

### Changed
- **Skill renamed** `/project-workflow-init` → `/ignite`. Directory: `.claude/skills/ignite/`. 40+ references updated across 16 files.
- **Step 1 restructured** — merged project scan + Foundational Discovery into unified Discovery step. Eliminates triple-display redundancy (welcome + report + summary → single combined report).
- **Config questions profile-gated** — Quick: 0 questions. Standard: 2 (Agents + Security). Enterprise: 3 (Agents + Teams + Security). Git always auto-detected.
- **Phase 0 exit conditions updated** — now requires FOUNDATION.md + project profile in STATUS.md.
- **`advance-phase` skill** — profile-aware phase skipping. Reads profile from STATUS.md, skips inactive phases, notes skipped phases in transition summary. Legacy projects (no profile) default to all phases.
- **STATUS.md template** — added `## Project Profile` section with profile and active phases.
- Plugin manifest `name` field: `project-workflow-init` → `ignite`.

### Adoption
Major version: rename + profiles + Discovery. To adopt v2.0.0 on existing projects: re-run `/ignite`.
Legacy projects without profile section in STATUS.md default to Enterprise behavior (all phases active).

## [1.3.0] - 2026-02-20

### Added
- **`/advance-phase` skill** — automates phase transitions: validates exit conditions per phase, updates STATUS.md + CHANGELOG-DEV.md, runs doc validation. Installed for advanced users. (`_workflow/templates/skills/advance-phase/SKILL.md`)
- **Session handoff** — `session-end` hook now generates a handoff summary (current phase + recently changed files) persisted to `lorekeeper-pending.json`. `session-gate` hook displays it at next session start, eliminating re-discovery overhead.
- **Phase-specific guidance** — `session-gate` hook now shows actionable recommendations for the current phase (e.g., "Write block specs in docs/specs/" for Phase 4) instead of only reminding about Phase 0→1 transition.
- **Workflow section** in CLAUDE.md template — static phase list with "Read STATUS.md FIRST" reminder, visible even when hooks are disabled.
- **Hook expectation note** in CLAUDE.md template — explains that quality gate hooks skip checks in Phases 0-3 when tools aren't installed yet.
- **Optional Skills section** in `file-map.md` — architectural support for conditional skill installation.

### Changed
- `session-gate` hook: current phase is now ALWAYS displayed as first line of SESSION CONTEXT (was conditional). Phase 0→1 specific reminder replaced by general-purpose phase action mapping.
- `session-gate` hook: `pending` dict initialized to `{}` (was undefined when no pending file existed).
- `session-end` hook: `bash_cmd` moved to function scope (was inside conditional block).
- Hook version bumped to 1.3.0.

### Fixed
- **`code-quality-gate.py`: early-phase graceful degradation** — gates now check if the command binary exists (`shutil.which`) before running. Missing tools (e.g., `mypy` not yet installed) produce a clear "skipped" message instead of opaque failure output that blocks commits. This was the #2 friction source across 103 sessions.

### Adoption
To adopt v1.3.0 on existing projects: re-run `/project-workflow-init`.
Hooks auto-update (Cat B). Review CLAUDE.md merge prompt for new sections.
`/advance-phase` installs for advanced users.

## [1.2.0] - 2026-02-17

### Fixed (integrity audit — 17 issues resolved)

#### Critical
- Version mismatch: `ignite-version.json` was hardcoded as "1.0.0" while hooks expected "1.1.0", causing false update warnings on every session

#### High
- `validate-docs.sh` only matched ES/EN section headers — extended to all 4 supported languages (PT/FR)
- Category A merge detection in `ref-generation-details.md` only covered ES/EN — expanded to quad-language
- Mid-way integration silently moved user's existing README — added confirmation prompt with 3 options

#### Medium
- Pending items cap mismatch between session-end (8) and session-gate (5) — aligned to 5
- `IDIOMA` default contradicted between `file-map.md` (ES) and `SKILL.md` (EN) — aligned to English
- `session-end.py` bare file reads could crash on encoding errors — added error handling
- STATE classification inflated by conditional files — documented core-only counting
- `pre-tool-security.py` Python pattern too broad — narrowed to block only dangerous os calls

#### Low
- `ref-platform-detection.md` incorrect parenthetical about step ordering removed
- Guided summary hardcoded "5 rules" — changed to dynamic `{rule_count}`
- Advanced summary omitted `validate-placeholders.sh` — added
- Session marker had no TTL — added 24h expiration
- Session marker write failed in fresh projects without `.claude/` — added `makedirs`
- `validate-prompt.py` base64 pattern matched git hashes — tightened to 60+ chars, excluded hex-only
- `mcp-audit.py` log grew without limit — added rotation at 1MB (keep last 500 entries)
- `file-map.md` CMD defaults assumed Node.js for all stacks — changed to N/A

### Changed
- `ignite-version.json` generation now reads version dynamically from `plugin.json` (single source of truth)
- Version bump checklist added to CONTRIBUTING.md

## [1.1.0] - 2026-02-16

### Security
- Security best practices section added to generated CLAUDE.md (secrets management, env vars, MCP permissions)
- Generated .gitignore now includes `secrets/`, `.env`, `.env.*` by default

### Documentation
- README intro rewritten for three audiences (non-technical users, developers, AI discovery)
- GitHub About metadata optimized with searchable terms
- Acknowledgments section: methodology references, practitioner credits, Anthropic resources
- Author tagline added to footer

## [1.0.0] - 2026-02-15

Initial public release.

### Core
- 8-phase development workflow methodology (Foundation → Hardening)
- 5-step initialization: Discovery, Configuration, Preview, Generation, Finalization
- 28 dynamic placeholders auto-resolved from project config files
- 12 stack profiles with optimized defaults (Python, Rust, Go, Node, Java, PHP, Ruby, Generic)
- Multi-language support (English, Spanish, Portuguese, French + free text)
- Cross-platform support (Windows, macOS, Linux)

### Adaptive UX
- 2 experience levels: Guided (0-2 prompts, safe defaults) and Advanced (full control)
- Automatic level detection from project signals with manual override
- Dry-run preview before writing any files (confirm, adjust, or cancel)

### Agents & Automation
- 5 agent templates (Lorekeeper, Inquisidor, Sentinel, backend-worker, frontend-worker)
- 7 automation hooks (session lifecycle, commit gates, code quality, security)
- 5 context-aware rules (documentation, testing, styling, compound-engineering, debugging)
- Compound engineering: SCRATCHPAD graduation pipeline + cross-session persistence

### Quality & Security
- Code quality gates: typecheck + lint + test enforcement before commits
- GitHub Actions CI/CD pipeline adapted per stack profile
- Documentation validation scripts
- Cerbero security framework (v0.9): supply-chain screening, CVE detection, prompt injection patterns

### Integration
- Mid-way project support: detects existing code, CI/CD, and conventions
- 3-category overwrite protection (A: merge docs, B: replace code, C: ask user)
- Prediction Protocol debugging methodology
- Post-mortem tracking with root cause analysis
