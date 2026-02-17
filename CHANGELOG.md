# Changelog

All notable changes to Ignite are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
