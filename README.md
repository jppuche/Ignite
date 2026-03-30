# Ignite

**Complete development infrastructure for Claude Code.** One command. Any stack. Full workflow.

<!-- GitHub About: Complete development infrastructure for Claude Code projects. Foundational Discovery, project profiles, session memory, quality gates, security screening, CI/CD — auto-adapted to any stack and complexity. Works on new and existing codebases. -->
<!-- Topics: claude-code, agent-skills, workflow-methodology, development-workflow, compound-engineering, security, multi-stack, automation -->

![Version](https://img.shields.io/badge/version-2.4.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8%2B-yellow)
![Platforms](https://img.shields.io/badge/platforms-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![Stacks](https://img.shields.io/badge/stacks-12%20profiles-orange)
![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple)

You start a project with Claude Code. Context vanishes after `/clear` — the same bug appears three sessions in a row. A package you installed last week has a known security flaw — nobody flagged it. Project documentation is outdated by week two — nobody enforces keeping it current. Every project starts from zero: no memory, no quality gates, no structure around the code.

Ignite understands your project first — vision, constraints, architecture — then generates the infrastructure to match. Living documentation, project memory, quality gates, security, CI/CD, and specialized agents, all adapted to your stack and complexity.

## Table of Contents

- [Quick Start](#quick-start)
- [What Ignite Does](#what-ignite-does)
- [Your Experience](#your-experience)
- [The Development Workflow](#the-development-workflow)
- [What Gets Generated](#what-gets-generated)
- [Adapts to You](#adapts-to-you)
- [Stack Support](#stack-support)
- [Requirements](#requirements)
- [After Setup](#after-setup)
- [What Makes Ignite Different](#what-makes-ignite-different)
- [FAQ](#faq)
- [Limitations](#limitations)
- [Deep Dive](#deep-dive)
- [Project Values](#project-values)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Quick Start

> [!TIP]
> Copy the `Ignite/` folder into your project root, then run:

```bash
/ignite
```

The skill auto-detects your OS, stack, and existing configuration. You answer a few questions about your project — most values resolve automatically.

<details>
<summary>Step-by-step walkthrough</summary>

1. Copy the `Ignite/` folder into your project root
2. Open Claude Code in your project directory
3. Run `/ignite`
4. Answer the setup questions (most values auto-detected)
5. Done — full workflow infrastructure generated

</details>

## What Ignite Does

- **Project Discovery** — Structured Q&A builds `FOUNDATION.md` before any technical decisions. Your project's vision, constraints, and architecture documented once, referenced by every agent downstream
- **Full infrastructure** — CLAUDE.md, docs, 5 specialized agents, context-aware rules, CI/CD pipeline — all adapted to your detected stack. 30+ placeholders resolved automatically from your project config
- **Session memory that compounds** — Every error, correction, and discovery is captured in SCRATCHPAD. When a pattern repeats 3+ times, it graduates to permanent rules in CLAUDE.md. Hooks enforce this pipeline: commits are blocked if SCRATCHPAD is stale, session-end checks identify graduation candidates. Context survives `/clear` through structured handoffs. The result: Claude Code gets measurably better at your project every session — not from retraining, from structured accumulation
- **Living documentation** — Hooks enforce that project docs stay current. Commits are blocked if documentation validation fails. Session start checks freshness of STATUS, CHANGELOG, and SCRATCHPAD. The AI writes — automation ensures it never skips
- **Strategic reflection** — `/cerebrate` mines your session for explicit knowledge and implicit insights. Four-lens analysis (confirms, challenges, opens, windows) with coherence scanning across your docs. Curated persistence, not bulk filing — the intelligence brief shows you what matters before anything is written
- **Quality enforcement** — Typecheck + lint + test gates before every commit. CI/CD pipeline generated for your stack. Doc validation on every session close
- **Security layers** — Environment protection blocks AI access to `.env`, secrets, and credentials. Cerbero screens Skills and MCP servers for prompt injection, supply-chain attacks, and typosquatting via a structured evaluation process (also available standalone: [Cerbero](https://github.com/jppuche/Cerbero))
- **Adapts to you** — Experience level (Guided/Advanced) controls interaction style. Project profile (Quick/Standard/Enterprise) controls workflow depth. A weekend script and a production API get different treatment

> [!NOTE]
> Every technical decision is documented with context and alternatives. Information surfaces when you need it, not all at once. The goal is a better development experience, not just a faster one.

## Your Experience

When you run `/ignite`, three things happen:

**Ignite asks about your project.** It scans your codebase, reads config files, then asks structured questions about your project's vision, capabilities, and constraints. The depth scales with your profile — a quick script gets 1 round of questions, an enterprise system gets 3-5. The result is `FOUNDATION.md`: a technology-agnostic document that every downstream agent reads before making decisions.

**It shows you what it will create.** A full dry-run preview lists every file that will be generated, grouped by purpose. You can adjust or cancel before anything is written.

**Then it generates everything, adapted.** Templates are processed with placeholders resolved from your project config. A 3-category overwrite system keeps your existing customizations safe during re-runs.

How much of the workflow applies to your project depends on its profile:

```
Quick:      Phase 0 ─────────────────────────────> Phase N
Standard:   Phase 0 → 1 → 2 → 3 → 4 ───────────> Phase N → Final
Enterprise: Phase 0 → 1 → 2 → 3 → 4 ───────────> Phase N → Final
```

**Quick** for scripts, POCs, and hobby projects — infrastructure + Discovery, then start building. **Standard** for apps, APIs, and libraries — streamlined planning before development. **Enterprise** for complex systems and multi-team projects — all phases at full depth.

Most users start with **Quick** profile — full infrastructure in one command, then start building immediately. Standard and Enterprise add planning phases for larger projects. Ignite suggests a profile based on your project's complexity. You confirm or override.

## The Development Workflow

`/ignite` establishes Phase 0. The remaining phases guide your project from stack decisions to production:

| Phase | Purpose |
|-------|---------|
| 0. Foundation + Discovery | Project context (FOUNDATION.md), memory, docs, agents, hooks, CI/CD |
| 1. Technical Landscape | External research, stack comparison, ecosystem scan |
| 2. Tooling & Security | Evaluate and install skills/MCPs, screened by Cerbero |
| 3. Intelligence-Enriched Review | Architecture assessment enriched by installed tools |
| 4. Architecture Blueprint | Detailed design + plan hardening |
| N. Development Blocks | Team assembly (N.0), build features with Ralph Loop |
| Final. Hardening | Security audit, performance, production readiness |

> [!IMPORTANT]
> Phase 2 (Tooling) runs before Phase 3 (Review) deliberately. This ensures architecture decisions are made with full knowledge of available tools — not speculative candidates.

Project profiles control which phases are active. Quick skips directly to building. Standard runs a streamlined planning path. Enterprise runs all phases at full depth.

## What Gets Generated

<details>
<summary>Full file tree — 30+ files across 10 categories (click to expand)</summary>

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
│   │   ├── hooks.md          # Hooks inventory and configuration reference
│   │   ├── testing.md
│   │   └── styling.md       # Conditional: only if frontend UI detected
│   ├── hooks/               # Automation hooks (always generated)
│   │   ├── lorekeeper-session-gate.py    # SessionStart: context + version check
│   │   ├── lorekeeper-commit-gate.py     # PreToolUse: blocks commits without docs
│   │   ├── lorekeeper-session-end.py     # SessionEnd: checkpoint + graduation
│   │   ├── code-quality-gate.py          # PreToolUse: typecheck + lint + test
│   │   ├── env-protection.py             # PreToolUse: blocks .env/secrets/credentials
│   │   ├── untrusted-source-reminder.py  # PreToolUse: safety reminder for WebFetch/MCP (Cerbero)
│   │   └── validate-tool-output.py       # PostToolUse: indirect injection scanner (Cerbero)
│   ├── security/
│   │   └── user-profile.json # Experience level + profile persistence
│   ├── skills/
│   │   ├── cerbero/          # Security framework (optional)
│   │   └── advance-phase/    # Phase transition automation (advanced users)
│   │   # Also available: cerebrate/ (install from _workflow/templates/skills/)
│   ├── quality-gate.json    # Stack-specific quality commands
│   ├── ignite-version.json  # Version tracking for auto-update
│   └── settings.local.json  # Hook configuration (gitignored)
├── .github/workflows/
│   └── quality.yml          # CI/CD pipeline (adapted per stack)
├── docs/
│   ├── FOUNDATION.md        # Project context from Discovery
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

</details>

## Adapts to You

Ignite adapts on two dimensions: how you interact, and how deep the workflow goes.

**Experience Level** — controls interaction style. Detected automatically from project signals; you can always override.

| Aspect | Guided | Advanced |
|--------|--------|----------|
| Setup | Minimal questions, safe defaults applied | Full control over every option |
| Preview | Summary grouped by purpose | Detailed file-by-file view |
| Phase transitions | Automatic validation | Manual with `/advance-phase` skill |

**Project Profile** — controls workflow depth. Suggested based on project complexity; you confirm or override.

| Profile | Phases | Discovery | Config Questions | Best for |
|---------|--------|-----------|-----------------|----------|
| Quick | 0 → N | 1 round, abbreviated | 0 | Scripts, POCs, hobby projects |
| Standard | 0–4, N, Final | 2-3 rounds, full | 2 | Apps, APIs, web services, libraries |
| Enterprise | All | 3-5 rounds, comprehensive | 3 | Complex systems, multi-team projects |

> [!TIP]
> You can always switch levels. Guided users can request more detail during preview; Advanced users get streamlined defaults if they prefer.

## Stack Support

Works with **any project type**. These stacks get optimized defaults (paths, test patterns, CI actions, security rules); all other projects use the Generic profile.

<details>
<summary>12 stack profiles with detection rules (click to expand)</summary>

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

</details>

## Requirements

- **Claude Code** installed and running
- **Python 3.8+** for automation hooks (stdlib only — no pip dependencies)
- **Git** initialized or available

> [!NOTE]
> **Windows:** Git for Windows must be installed. Ignite auto-configures `CLAUDE_CODE_GIT_BASH_PATH`.
> **macOS/Linux:** Python 3 available via `python3`. Verified automatically.

## After Setup

After `/ignite` completes, customize these project-specific sections:

1. **CLAUDE.md** — Fill in `Style` and `Architecture` sections
2. **Agents** — Adapt domain paths to your project layout
3. **Styling rule** — Define design tokens if applicable

Then proceed to Phase 1 — or Phase N directly if you chose the Quick profile. Full guide: `_workflow/guides/workflow-guide.md`

## What Makes Ignite Different

Most project scaffolders generate files and leave. Ignite works differently:

- **Understands before generating** — Foundational Discovery creates a project context document through structured Q&A before any technical decision. Agents don't guess your requirements — they read `FOUNDATION.md`
- **Adapts to complexity** — Three project profiles gate which phases run and how many questions you answer. A weekend script doesn't get the same treatment as a production API
- **Protects existing work** — 3-category overwrite system (merge docs, replace code, ask for rules/agents). Re-run `/ignite` without losing customizations. Mid-way integration detects existing CI/CD and conventions
- **Enforces quality automatically** — PreToolUse hooks block commits that fail typecheck, lint, or tests. Not advisory — enforced
- **Learns across sessions** — Compound engineering is the core differentiator. Errors flow into SCRATCHPAD, repeating patterns are detected and graduate to permanent CLAUDE.md rules, session handoffs preserve context across `/clear`. This isn't advisory — hooks enforce the entire pipeline. Every session Claude works on your project, it gets better. Not from retraining — from structured accumulation of what works and what doesn't
- **Reflects, not just records** — Most tools log what happened. `/cerebrate` analyzes what it means: what confirms your assumptions, what challenges them, what new opportunities appeared, and what's time-sensitive. Coherence scanning catches when updating one document makes another stale
- **Keeps documentation alive** — Hooks check doc freshness at session start and block commits when validation fails. STATUS, CHANGELOG, SCRATCHPAD, and DECISIONS stay current because the system won't let them go stale
- **Security by default** — Environment protection hooks block `.env`/secrets/credentials access. Cerbero screens Skills and MCP servers for prompt injection, supply-chain attacks, and typosquatting via structured evaluation checklists
- **Works everywhere** — Windows, macOS, Linux. 12 stack profiles. 4 languages + free text. New projects and existing codebases

## FAQ

<details>
<summary>What are project profiles?</summary>

Project profiles control how much of the workflow applies to your project. **Quick** (scripts, POCs) skips planning phases and jumps straight to building. **Standard** (apps, APIs) runs a streamlined planning path. **Enterprise** (complex systems) runs all phases at full depth. Ignite suggests a profile based on your project's complexity — you confirm or override.

</details>

<details>
<summary>Does Ignite work on existing projects?</summary>

Yes. Ignite detects existing code, CI/CD configuration, and conventions. It integrates without overwriting your customizations. The 3-category overwrite system (merge docs, replace code, ask for rules/agents) protects your existing work.

</details>

<details>
<summary>Can I re-run /ignite?</summary>

Yes. Safe re-execution analyzes what has changed since the last run. Docs are merged (missing sections added), executable code is replaced if different, and customized files (rules, agents) prompt before modification.

</details>

<details>
<summary>What if I only want some components?</summary>

Ignite generates all components but each serves an independent purpose. You can delete any agent, rule, or hook after generation without breaking the rest. Cerbero installation is optional (you are asked during setup).

</details>

<details>
<summary>Does it work without internet access?</summary>

Phase 0 (Foundation) works fully offline — all templates are local. Phase 1's ecosystem scan and Phase 2's Cerbero web research (CVE lookups, publisher reputation) require internet access.

</details>

<details>
<summary>What languages are supported?</summary>

English, Spanish, Portuguese, and French for all generated documentation and interaction. Technical elements (file names, config keys, code) remain in English. You can also enter a custom language via free text input.

</details>

## Limitations

### What Ignite doesn't do
- **Not a substitute for thinking** — generates infrastructure, not architecture decisions
- **No rollback** — if generation goes wrong, you delete and re-run (git history is your safety net)

### Cerbero security disclaimers

Cerbero is a **screening layer, not a security guarantee**. It catches common attacks but has real limits:

- **Detects:** prompt injection (normalize-then-detect pipeline with homoglyph/proximity/base64 coverage), dangerous shell commands, typosquatting, baseline changes in installed MCPs, format injection tags in external tool outputs (PostToolUse)
- **Does NOT detect:** novel prompt injection via creative paraphrasing, zero-day vulnerabilities, malware signatures (without external scanner), silent data exfiltration, post-approval behavioral changes, indirect injection in local file reads (by design — Claude's Tier 1 handles these)
- **CVE detection** is web-search-based (manual research during evaluation), not an automated database scan. For malware signature detection, install `cisco-ai-mcp-scanner` (YARA-only mode, 100% offline). Recommended for teams evaluating 5+ MCP servers or from untrusted publishers.

> [!CAUTION]
> For high-stakes environments, use Cerbero as one layer in a defense-in-depth approach, not your only protection. For standalone security screening without the full Ignite workflow, see [Cerbero](https://github.com/jppuche/Cerbero).

## Deep Dive

<details>
<summary>Skill architecture and complete feature reference (click to expand)</summary>

### Skill Architecture

The skill follows a **delegation pattern**: `SKILL.md` orchestrates the steps, while complex logic is delegated to reference files (`ref-*.md`). `file-map.md` serves as the single source of truth for all template-to-destination mappings and placeholder declarations.

```
.claude/skills/ignite/
├── SKILL.md                       # Orchestrator (Steps 0-5)
└── references/                    # Detailed logic (loaded on-demand)
    ├── file-map.md                # Template mapping + placeholders
    ├── ref-adaptive-ux.md         # Adaptive UX: detection, behavior tables, preview specs
    ├── ref-foundational-discovery.md  # Discovery methodology + FOUNDATION.md spec
    ├── ref-stack-profiles.md      # 12 stack profiles
    ├── ref-platform-detection.md  # OS/Python/Git detection
    ├── ref-generation-details.md  # Step 2.5 preview + Step 3 generation logic
    ├── ref-finalization-details.md # Step 5 detailed logic
    ├── ref-cerbero-installation.md # Security framework
    └── ref-error-handling.md      # Error recovery

.claude-plugin/plugin.json          # Standard plugin manifest
```

### Complete Feature Reference

| Feature | Description |
|---------|-------------|
| **6-step initialization** | Initialization (with profile selection), Discovery (with FOUNDATION.md), Configuration, Preview, Generation, Finalization |
| **Foundational Discovery** | Structured Q&A creates FOUNDATION.md — technology-agnostic project context. Depth scales with profile (1-5 rounds) |
| **Project Profiles** | Quick/Standard/Enterprise gate which phases execute and interaction depth |
| **12 stack profiles** | Python (Django/FastAPI/generic), Rust, Go, Node (React/Express/generic), Java/Kotlin, PHP/Laravel, Ruby/Rails, Generic |
| **30+ dynamic placeholders** | Auto-resolved from project config files (package.json, pyproject.toml, etc.) |
| **Mid-way integration** | Detects existing code, CI/CD, conventions — integrates without overwriting |
| **Overwrite protection** | 3-category system: A (merge docs), B (replace code), C (ask user) |
| **Compound engineering** | SCRATCHPAD graduation pipeline + cross-session persistence via hooks |
| **Cerbero security** | Supply-chain screening, prompt injection patterns, rug pull baselines, structured evaluation process |
| **Environment protection** | PreToolUse hook blocking AI access to .env, secrets, and credentials (Read blocks, Bash warns) |
| **Code quality gates** | PreToolUse hook enforcing typecheck + lint + test before commits |
| **CI/CD generation** | GitHub Actions workflow template adapted per stack profile |
| **Phase transitions** | `/advance-phase` skill automates validation, STATUS.md updates, and profile-aware phase skipping |
| **Hook-based enforcement** | 9 automated hooks: session lifecycle + commit gates + quality + security + indirect injection defense |
| **Multi-language** | English, Spanish, Portuguese, French + free text |
| **Adaptive UX** | 2 levels (Guided/Advanced) x 3 profiles (Quick/Standard/Enterprise): adapts questions, defaults, depth |
| **Dry-run preview** | Preview all generated files before writing — cancel, adjust, or confirm |
| **Interaction budget** | 2-9 prompts depending on profile and level |
| **Safe re-execution** | Smart overwrite analysis — re-run `/ignite` without losing customizations |
| **Debugging methodology** | Prediction Protocol: predict, observe, compare, explain, verify |
| **Post-mortem tracking** | Structured LESSONS-LEARNED.md with incident timeline and root cause analysis |
| **Auto-update notification** | Session-start version check with drift and age detection |
| **Graduation automation** | Automated detection of repeating SCRATCHPAD patterns across sessions |
| **Plugin manifest** | .claude-plugin/plugin.json — standard Claude Code plugin structure |

</details>

## Project Values

Three commitments shape every decision in this workflow.

**Transparency** — Every decision is documented with context and alternatives. Every rejected option has a reason on record. The user never has to guess why something was chosen.

**Timely, Adequate Information** — The right information at the right moment. Not everything at once (overload), not too late (surprise). Each phase surfaces what you need to decide now, and defers what you don't.

**Improved Experience** — Every automation, template, and gate exists to make development better — not just faster. Quality of the development experience is a first-class metric alongside code quality.

Complementary principles: Rigor (measurable exit conditions). Compound learning (every session builds on the last). Security-first (evaluate before install). Context economy (every token earns its place).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture overview, how to add stack profiles, templates, hooks, and rules.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License — see [LICENSE](LICENSE).

## Acknowledgments

This workflow builds on ideas and practices from:

**Methodologies**
- [Ralph Loop](https://ghuntley.com/loop) — the iterative execution pattern at the core of Development Blocks. Expanded by [vincirufus.com](https://vincirufus.com) and [paddo.dev](https://paddo.dev)
- [Compound Engineering](https://every.to/chain-of-thought/compound-engineering) — the plan/work/review cycle and session accumulation pattern. [Plugin](https://github.com/EveryInc/compound-engineering-plugin) by Every

**Practitioners**
- **Andrej Karpathy** (ex-Tesla AI Director, OpenAI founding member) — the shift from vibe coding to agentic engineering shaped Ignite's declarative approach (CLAUDE.md + rules instead of imperative scripts)
- **Boris Cherny** (Claude Code creator) — CLAUDE.md as mistake log and PostToolUse hooks directly inspired the SCRATCHPAD graduation pipeline and quality gates
- **Addy Osmani** (Google Chrome engineering lead) — spec-first development and task sizing informed the Phase 0 → Phase N workflow structure and block-based execution
- **Simon Willison** (Django co-creator) — his two-phase approach (research → production) influenced the separation between exploration phases (1-4) and development blocks (N)
- **Harper Reed** (former CTO, Obama 2012 campaign) — TDD as counter to hallucination shaped the Prediction Protocol debugging methodology and verification loops
- **paddo.dev** (Emergent Minds blog) — minimal effective structure, the 19-Agent Trap essay, and /compact timing research informed agent count decisions and context management
- **swyx** (Latent Space founder) — the IMPACT framework and conductor model influenced the multi-agent architecture and Lorekeeper's orchestration role

**Resources**
- [Claude Code docs](https://code.claude.com/docs) — best practices, agent teams, skills, MCP
- [Anthropic: Multi-Agent Research System](https://anthropic.com/engineering/multi-agent-research-system)
- [Anthropic: Effective Context Engineering](https://anthropic.com/engineering/effective-context-engineering)

---

Made by [Juan Puche](https://github.com/jppuche) — building tools that solve real problems.
