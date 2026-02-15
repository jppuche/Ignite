# Contributing to Ignite

Guide for extending and modifying Ignite. Covers architecture, how to add new components, conventions, and distribution.

## Architecture Overview

### 5-Phase Execution Model

| Phase | Name | Purpose |
|-------|------|---------|
| 1 | Discovery | Detect OS, scan project files, identify existing config |
| 2 | Configuration | Auto-resolve placeholders, select stack profile, ask user questions |
| 3 | Generation | Process templates, resolve placeholders, respect overwrite categories |
| 4 | Security | Install Cerbero framework (optional) |
| 5 | Finalization | Git init, validate, cleanup setup files, summary |

### File Organization

```
Ignite/
├── .claude/skills/project-workflow-init/     # Skill definition
│   ├── SKILL.md              # Orchestrator (~475 lines, 5 phases)
│   ├── file-map.md           # Single source of truth: template mappings + placeholders
│   ├── ref-stack-profiles.md # 12 stack profiles with domain config
│   ├── ref-platform-detection.md
│   ├── ref-generation-details.md
│   ├── ref-finalization-details.md
│   ├── ref-cerbero-installation.md
│   └── ref-error-handling.md
├── _workflow/
│   ├── templates/            # Source templates (processed during generation)
│   │   ├── agents/           # 5 agent templates
│   │   ├── ci/               # GitHub Actions template
│   │   ├── docs/             # 8 doc templates (STATUS, DECISIONS, LESSONS-LEARNED, etc.)
│   │   ├── hooks/            # Python hooks (Lorekeeper + code quality)
│   │   ├── rules/            # 5 rule templates (incl. debugging methodology)
│   │   ├── scripts/          # Validation scripts
│   │   ├── skills/cerbero/   # Cerbero security framework
│   │   └── CLAUDE.template.md
│   └── guides/               # Permanent reference (kept after setup)
├── README.md                 # Distribution README
├── CONTRIBUTING.md           # This file
├── CHANGELOG.md              # Version history
└── LICENSE                   # MIT License
```

### Delegation Pattern

`SKILL.md` is the orchestrator. Complex logic is delegated to `ref-*.md` files, which Claude loads only when needed. This keeps the main skill file focused and reduces token consumption.

`file-map.md` is the single source of truth for:
- All template-to-destination mappings
- All placeholder declarations (name, source, default)
- Overwrite categories per file
- Directory creation list

## How to Add a Stack Profile

1. Open `ref-stack-profiles.md`
2. Add a new "Expanded Profile" section following the existing format:
   ```markdown
   ### Profile: Your Stack (Framework)
   **Detection:** description of detection criteria
   ```
3. Fill all 8 domain fields:
   - `{{DOMAIN_BACKEND}}` — backend paths as markdown bullets
   - `{{DOMAIN_FRONTEND}}` — frontend paths (or `— (no frontend)`)
   - `{{TEST_DOMAIN}}` — test patterns and config
   - `{{TEST_PATHS_FRONTMATTER}}` — YAML list for testing rule frontmatter
   - `{{CRITICAL_RULES_BACKEND}}` — security/quality rules
   - `{{CRITICAL_RULES_FRONTEND}}` — design/UX rules (or `— (no frontend)`)
   - Styling Applicable: Yes/No/Conditional
   - `{{CI_SETUP}}` — GitHub Actions setup steps as YAML
4. Add detection entry to "Profile Selection Logic" section (order = priority)
5. Add row to "Quick Reference Table"
6. Validate: `bash _workflow/templates/scripts/validate-placeholders.sh` (from `Ignite/`)

## How to Add a Template

1. Create template file in `_workflow/templates/[category]/`
   - Use `{{PLACEHOLDER}}` syntax for dynamic values
   - Only use placeholders declared in `file-map.md`
2. Add mapping to `file-map.md` in the appropriate Template Mapping section
   - Columns: Template | Destination | Placeholders used | OW (overwrite category)
3. Assign overwrite category (see table below)
4. Add generation logic to `SKILL.md` Phase 3 (or appropriate sub-phase)
5. Validate: `bash _workflow/templates/scripts/validate-placeholders.sh`

## How to Add a Hook

1. Create `.py` file in `_workflow/templates/hooks/`
2. Follow existing patterns:
   - Read input from `sys.stdin` (JSON with tool_input, cwd, etc.)
   - Fail open: if config missing, warn and `sys.exit(0)` (allow)
   - Fail closed on validation errors: output JSON with `{"decision": "block", "reason": "..."}`
   - Cross-platform: use `os.path.join()`, handle Windows paths
   - Use `{PYTHON_CMD}` in settings (resolved at generation time)
3. Add to `file-map.md` in appropriate hooks section (Category B)
4. Register in `SKILL.md` Phase 3.2 settings.local.json merge:
   ```json
   { "type": "command", "command": "{PYTHON_CMD} .claude/hooks/your-hook.py" }
   ```
5. Document the hook event in SKILL.md

## How to Add a Rule

1. Create `[name].template.md` in `_workflow/templates/rules/`
2. Use YAML frontmatter for activation:
   ```yaml
   ---
   description: What this rule enforces
   paths:
     - "path/pattern/**"
   # OR
   always_apply: true
   ---
   ```
3. Add to `file-map.md` Rules section with OW category C
4. If rule is stack-dependent, add conditional logic in `SKILL.md` Phase 3.3
   (see `styling.md` pattern: check `STYLING_APPLICABLE` flag from stack profile)
5. Validate

## Overwrite Categories

When `/project-workflow-init` re-runs on an existing project, each file is handled by its category:

| Category | Strategy | When to Use |
|----------|----------|-------------|
| **A** | Smart merge: add missing sections, preserve existing content | Docs with user data (STATUS, DECISIONS, SCRATCHPAD) |
| **B** | Replace if different, skip if identical | Executable code: hooks, scripts, skill files |
| **C** | Analyze differences, ask user before modifying | Rules and agents (possibly customized by user) |
| **--** | File-specific logic (implemented per file) | CLAUDE.md (ask), .gitignore (append), settings.local.json (merge), README.md (ask) |

Defined in `file-map.md` "Overwrite Categories" section. Logic in `SKILL.md` Phase 3.0.

## Testing

### Placeholder Validation

```bash
cd Ignite
bash _workflow/templates/scripts/validate-placeholders.sh
```

Checks: declared vs used placeholders, undeclared usage, unused declarations.

**Known warnings** (expected, not errors):
- `IDIOMA` — runtime-only directive, not used in template files
- `CI_SETUP` — used in `.yml` file, scanner only checks `.md`

### Documentation Validation

```bash
bash scripts/validate-docs.sh
```

Checks: required files, line limits, format, dates, sections, graduation candidates.

## Distribution

### Claude Code Skill Distribution (2026)

Skills can be distributed via three methods:

1. **Project-scoped** — Commit `.claude/skills/project-workflow-init/` + `_workflow/` to your repo. Anyone cloning gets the skill.
2. **Personal** — Copy to `~/.claude/skills/project-workflow-init/SKILL.md` for availability across all projects.
3. **Marketplace** — Publish via `/plugin marketplace add <publisher/repo>`, users install with `/plugin install project-workflow-init`.

### SKILL.md as Metadata

The SKILL.md frontmatter is the standard metadata format for Claude Code skills:

```yaml
---
name: project-workflow-init
description: Interactive project initialization...
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---
```

No additional manifest files are required. The frontmatter is compatible with the Agent Skills standard used by Claude Code and other agent frameworks.

### Plugin Manifest

`plugin-manifest.json` at the skill root extends SKILL.md frontmatter with marketplace-specific metadata. Update it when:
- Version changes (keep in sync with CHANGELOG.md)
- Features are added/removed (agents, rules, hooks, doc_templates counts)
- New stack profiles are added (supported_stacks array)
- Tags change

### Version Tracking

Ignite uses semantic versioning tracked in `CHANGELOG.md` and `plugin-manifest.json`. Git tags mark releases (`v1.0.0`, `v1.1.0`, etc.). Auto-update check: the session-gate hook compares its embedded version with the project's installed version and notifies the user of drift.
