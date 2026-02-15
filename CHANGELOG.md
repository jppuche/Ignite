# Changelog

All notable changes to Ignite are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
