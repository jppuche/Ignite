# Ignite

> An 8-phase development workflow for Claude Code — from project setup to production hardening.

<!-- GitHub About: Claude Code workflow methodology — 8 phases, 5 agents, 7 hooks, 12 stack profiles, security framework, compound engineering. Works on new and existing projects. -->
<!-- Topics: claude-code, agent-skills, workflow-methodology, development-workflow, compound-engineering, security, multi-stack, automation -->

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Stacks](https://img.shields.io/badge/stacks-12%20profiles-orange)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple)

You start a project with Claude Code. You get code — but no structure around it. No quality gates, no memory between sessions, no security checks. Context gets lost after every `/clear`. Mistakes repeat. Technical debt grows silently.

Ignite fixes this. One command gives you the full infrastructure: project memory, documentation, specialized agents, automation hooks, security framework, quality gates, and CI/CD — all adapted to your detected stack. Works on fresh projects and existing codebases.

## Quick Start

```
1. Copy the Ignite/ folder into your project root
2. Open Claude Code in your project directory
3. Run /project-workflow-init
4. Answer the setup questions (most values auto-detected)
5. Done — full workflow infrastructure generated
```

## What You Get

- **Workflow structure** — CLAUDE.md, docs, 5 specialized agents, context-aware rules — adapted to your stack
- **Quality gates** — automated typecheck + lint + test enforcement before every commit
- **Session memory** — mistakes are recorded and patterns graduate to permanent memory. Your Claude Code learns from past errors and gets better every session
- **Security framework** — Cerbero: supply-chain screening, known CVE detection, rug pull baseline checks
- **CI/CD pipeline** — GitHub Actions workflow generated and configured for your stack
- **Mid-way support** — detects existing code, CI/CD, and conventions — integrates without overwriting

Every technical decision is documented with context and alternatives. Information surfaces when you need it, not all at once. The goal is a better development experience, not just a faster one.

## How It Works

Ignite establishes **Phase 0: Foundation** when you run `/project-workflow-init`. This creates the infrastructure for an 8-phase development workflow:

| Phase | Purpose |
|-------|---------|
| 0. Foundation | Project memory, docs, agents, hooks, CI/CD |
| 1. Technical Landscape | Stack decisions, validation tools, ecosystem scan |
| 2. Tooling & Security | Evaluate and install skills/MCPs (via Cerbero) |
| 3. Strategic Review | Architecture assessment (enriched by installed tools) |
| 4. Architecture Blueprint | Detailed design based on actual capabilities |
| 5. Team Assembly | Configure agents, assign roles |
| N. Development Blocks | Build features iteratively with Ralph Loop |
| Final. Hardening | Security audit, performance, production readiness |

Phase 0 runs in 5 steps:

1. **Discovery** — Detect OS, scan project files, identify existing config, analyze project context, detect user level (Guided/Advanced)
2. **Configuration** — Auto-resolve values, select stack profile, ask questions adapted to user level
3. **Preview** — Dry-run showing exactly what will be generated, with confirmation before writing
4. **Generation** — Process templates with 28 dynamic placeholders, respect overwrite categories
5. **Finalization** — Security framework, git init, validate docs, cleanup, summary

## What Gets Generated

```
your-project/
├── .claude/
│   ├── agents/              # Specialized agents (user-selectable)
│   │   ├── Lorekeeper.md    # Documentation agent (always installed)
│   │   ├── Inquisidor.md    # Testing agent
│   │   ├── Sentinel.md      # Security agent
│   │   ├── backend-worker.md
│   │   └── frontend-worker.md
│   ├── rules/               # Context-aware rules (path-activated)
│   │   ├── compound-engineering.md
│   │   ├── debugging.md      # Prediction Protocol methodology
│   │   ├── documentation.md
│   │   ├── testing.md
│   │   └── styling.md       # Conditional: only if frontend UI detected
│   ├── hooks/               # Automation hooks (always generated)
│   │   ├── lorekeeper-session-gate.py    # SessionStart: context + version check
│   │   ├── lorekeeper-commit-gate.py     # PreToolUse: blocks commits without docs
│   │   ├── lorekeeper-session-end.py     # SessionEnd: checkpoint + graduation
│   │   └── code-quality-gate.py          # PreToolUse: typecheck + lint + test
│   ├── skills/cerbero/      # Security framework (optional)
│   ├── quality-gate.json    # Stack-specific quality commands
│   ├── ignite-version.json  # Version tracking for auto-update
│   └── settings.local.json  # Hook configuration (gitignored)
├── .github/workflows/
│   └── quality.yml          # CI/CD pipeline (adapted per stack)
├── docs/
│   ├── STATUS.md            # Project status (< 60 lines)
│   ├── DECISIONS.md         # Technical decisions (append-only)
│   ├── CHANGELOG-DEV.md     # Development changelog
│   ├── SCRATCHPAD.md        # Session learning log (< 150 lines)
│   ├── LESSONS-LEARNED.md   # Incident post-mortems
│   └── specs/               # Feature specifications
├── scripts/
│   └── validate-docs.sh     # Automated documentation validation
├── _workflow/guides/         # Permanent reference (kept after setup)
│   ├── workflow-guide.md
│   ├── agents-guide.md
│   └── Referencia-edicion-CLAUDE.md
├── CLAUDE.md                 # Project memory (< 200 lines)
└── README.md                 # Generated project README
```

## Stack Detection

Works with **any project type**. These stacks get optimized defaults (paths, test patterns, CI actions, security rules); all other projects use the Generic profile with the full workflow.

| Profile | Detection | Backend Paths | Test Patterns | CI Action |
|---------|-----------|--------------|---------------|-----------|
| Python (Django) | `django` in deps | app/, views/, models/ | tests/, test_*.py | setup-python@v5 |
| Python (FastAPI) | `fastapi` in deps | app/, routers/, schemas/ | tests/, test_*.py | setup-python@v5 |
| Python (generic) | pyproject.toml / setup.py | src/, lib/ | tests/, test_*.py | setup-python@v5 |
| Rust | Cargo.toml | src/, lib.rs, main.rs | tests/, #[cfg(test)] | rust-toolchain@stable |
| Go | go.mod | cmd/, pkg/, internal/ | *_test.go | setup-go@v5 |
| Node/React | react/next/vue in deps | src/lib/, src/app/api/ | *.test.ts(x) | setup-node@v4 |
| Node/Express | express/fastify in deps | src/, routes/, middleware/ | *.test.ts | setup-node@v4 |
| Node (generic) | package.json | src/, lib/ | *.test.ts | setup-node@v4 |
| Java/Kotlin | pom.xml / build.gradle | src/main/java/ | src/test/java/ | setup-java@v4 |
| PHP (Laravel) | laravel in composer.json | app/, routes/, database/ | tests/ | setup-php@v2 |
| Ruby (Rails) | rails in Gemfile | app/models/, controllers/ | spec/, test/ | setup-ruby@v1 |
| **Any other** | **(fallback)** | **src/, lib/** | **tests/, test/** | **(manual config)** |

## Requirements

- **Claude Code** installed and running
- **Python 3** (for automation hooks)
- **Windows:** Git for Windows installed. `/project-workflow-init` auto-configures `CLAUDE_CODE_GIT_BASH_PATH`.
- **macOS/Linux:** Python 3 available via `python3`. `/project-workflow-init` verifies automatically.

## Post-Setup

After `/project-workflow-init` completes, customize these project-specific sections:

1. **CLAUDE.md** — Fill in `Style` and `Architecture` sections
2. **Agents** — Adapt domain paths to your project layout
3. **Styling rule** — Define design tokens if applicable

Then follow the workflow phases:

| Phase | What happens |
|-------|-------------|
| 0. Foundation | Project structure, git, CLAUDE.md, Lorekeeper |
| 1. Technical Landscape | Stack decisions, validation tools, ecosystem scan |
| 2. Tooling & Security | Evaluate and install skills/MCPs (via Cerbero) |
| 3. Strategic Review | Architecture assessment (enriched by installed tools) |
| 4. Architecture Blueprint | Detailed design based on actual capabilities |
| 5. Team Assembly | Configure agents, assign roles |
| N. Development Blocks | Build features iteratively with Ralph Loop |
| Final. Hardening | Security audit, performance, production readiness |

Full guide: `_workflow/guides/workflow-guide.md`

## Comparison

| Feature | Ignite | claude-bootstrap | atlas-session | scaffolding |
|---------|:------:|:----------------:|:-------------:|:-----------:|
| Auto-detection | ++ | + | + | -- |
| Multi-language | ++ | -- | -- | -- |
| Mid-way integration | +++ | -- | -- | -- |
| Overwrite protection | +++ | - | ++ | -- |
| Supply-chain security | ++ | -- | -- | - |
| Compound engineering | ++ | -- | ++ | ++ |
| Hook-based enforcement | +++ | -- | -- | -- |
| Code quality gates | ++ | ++ | -- | +++ |
| CI/CD generation | ++ | ++ | -- | ++ |
| Doc validation | ++ | -- | -- | - |
| Adaptive UX (2 levels) | +++ | -- | -- | -- |
| Dry-run preview | ++ | -- | -- | -- |
| Minimal UX (0-2 prompts) | +++ | - | ++ | -- |
| Cross-platform | ++ | -- | + | + |

Legend: `+++` exceptional, `++` good, `+` basic, `-` weak, `--` absent

## Limitations

### What Ignite doesn't do
- **Not a substitute for thinking** — generates infrastructure, not architecture decisions
- **Phase time estimates are optimistic** — real architecture design takes longer than 15-30 min
- **No rollback** — if generation goes wrong, you delete and re-run (git history is your safety net)

### Cerbero security disclaimers

Cerbero is a **screening layer, not a security guarantee**. It catches common attacks but has real limits:

- **Detects:** known CVEs, obvious prompt injection phrases, dangerous shell commands, typosquatting, baseline changes in installed MCPs
- **Does NOT detect:** sophisticated prompt injection (synonyms/obfuscation bypass regex), zero-day vulnerabilities (24-48hr CVE database lag), silent data exfiltration, post-approval behavioral changes
- **mcp-scan integration is strongly recommended** — without it, you lose Snyk's tool poisoning detection and rely on regex alone

For high-stakes environments, use Cerbero as one layer in a defense-in-depth approach, not your only protection.

## Technical Details

### Skill Architecture

The skill follows a **delegation pattern**: `SKILL.md` orchestrates the phases, while complex logic is delegated to reference files (`ref-*.md`). `file-map.md` serves as the single source of truth for all template-to-destination mappings and placeholder declarations.

```
.claude/skills/project-workflow-init/
├── SKILL.md                  # Orchestrator (Steps 0-5)
├── file-map.md               # Template mapping + placeholders
├── ref-adaptive-ux.md        # Adaptive UX: detection, behavior tables, preview specs
├── ref-stack-profiles.md     # 12 stack profiles
├── ref-platform-detection.md # OS/Python/Git detection
├── ref-generation-details.md # Step 2.5 preview + Step 3 generation logic
├── ref-finalization-details.md # Step 5 detailed logic
├── ref-cerbero-installation.md # Security framework
└── ref-error-handling.md     # Error recovery

plugin-manifest.json            # Marketplace manifest
```

### Complete Feature Reference

| Feature | Description |
|---------|-------------|
| **5-step initialization** | Discovery, Configuration, Preview, Generation, Finalization |
| **12 stack profiles** | Python (Django/FastAPI/generic), Rust, Go, Node (React/Express/generic), Java/Kotlin, PHP/Laravel, Ruby/Rails, Generic |
| **28 dynamic placeholders** | Auto-resolved from project config files (package.json, pyproject.toml, etc.) |
| **Mid-way integration** | Detects existing code, CI/CD, conventions — integrates without overwriting |
| **Overwrite protection** | 3-category system: A (merge docs), B (replace code), C (ask user) |
| **Compound engineering** | SCRATCHPAD graduation pipeline + cross-session persistence via hooks |
| **Cerbero security** | Supply-chain screening, known CVE detection, prompt injection patterns, rug pull baselines |
| **Code quality gates** | PreToolUse hook enforcing typecheck + lint + test before commits |
| **CI/CD generation** | GitHub Actions workflow template adapted per stack profile |
| **Hook-based enforcement** | 7 automated hooks: session lifecycle + commit gates + security validation |
| **Multi-language** | English, Spanish, Portuguese, French + free text |
| **Adaptive UX** | 2 levels (Guided/Advanced): auto-detects user experience, adapts questions, defaults, and output detail |
| **Dry-run preview** | Preview all generated files before writing — cancel, adjust, or confirm |
| **Minimal interaction** | 0-2 prompts (Guided) to 4-5 prompts (Advanced), level-adaptive |
| **Safe re-execution** | Smart overwrite analysis — re-run `/project-workflow-init` without losing customizations |
| **Debugging methodology** | Prediction Protocol: predict, observe, compare, explain, verify |
| **Post-mortem tracking** | Structured LESSONS-LEARNED.md with incident timeline and root cause analysis |
| **Auto-update notification** | Session-start version check with drift and age detection |
| **Graduation automation** | Automated detection of repeating SCRATCHPAD patterns across sessions |
| **Marketplace manifest** | plugin-manifest.json ready for Claude Code marketplace |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture overview, how to add stack profiles, templates, hooks, and rules.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License — see [LICENSE](LICENSE).
