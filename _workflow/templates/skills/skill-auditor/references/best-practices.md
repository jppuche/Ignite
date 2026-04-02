# Skills Best Practices Reference

Guidelines for creating, editing, and auditing Claude Code skills. Compiled from Anthropic's official documentation and the skill-creator plugin's internal patterns.

---

## Sources

- **Anthropic official docs** - https://code.claude.com/docs/en/skills [2025]
- **skill-creator plugin** - Anthropic's official skill creation/evaluation skill (480 lines, agents/grader, comparator, analyzer)

---

## Anatomy of a Skill

Every skill is a directory with a `SKILL.md` file (required) plus optional supporting files:

```
skill-name/
  SKILL.md           # Instructions + frontmatter (required)
  scripts/           # Executable code for deterministic/repetitive tasks
  references/        # Docs loaded into context as needed
  assets/            # Files used in output (templates, icons, fonts)
  evals/             # Test cases and assertions (evals.json)
```

`SKILL.md` has two parts: YAML frontmatter (between `---` markers) and markdown content with instructions.

### Progressive Disclosure (3-level loading)

1. **Metadata** (name + description) - always in context (~100 words)
2. **SKILL.md body** - loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** - loaded on demand (unlimited; scripts execute without loading)

Key: keep SKILL.md focused. If approaching 500 lines, add hierarchy with pointers to reference files. For large references (>300 lines), include a table of contents.

---

## Frontmatter Reference

All fields optional. Only `description` is recommended.

| Field | Default | Purpose |
|-------|---------|---------|
| `name` | directory name | Slash command name. Lowercase, numbers, hyphens. Max 64 chars |
| `description` | first paragraph | When to use. Claude uses this for auto-invocation decisions |
| `argument-hint` | - | Autocomplete hint: `[issue-number]`, `[filename] [format]` |
| `disable-model-invocation` | `false` | `true` = manual-only (`/name`), hidden from Claude's context |
| `user-invocable` | `true` | `false` = Claude-only, hidden from `/` menu |
| `allowed-tools` | all | Restrict tools: `Read, Grep, Glob` |
| `model` | session | Override model for this skill |
| `effort` | session | `low`, `medium`, `high`, `max` (Opus 4.6 only) |
| `context` | inline | `fork` = run in isolated subagent |
| `agent` | general-purpose | Subagent type when `context: fork`. Options: `Explore`, `Plan`, custom |
| `hooks` | - | Hooks scoped to skill lifecycle |

---

## Two Content Types

### Reference skills - add knowledge inline

Conventions, patterns, domain knowledge. Runs in conversation context.

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming
- Return consistent error formats
```

### Task skills - step-by-step action

Deployments, commits, code generation. Often manual-only.

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

---

## Invocation Control Matrix

| Frontmatter | User invokes | Claude invokes | In context? |
|-------------|-------------|----------------|-------------|
| (defaults) | Yes | Yes | Description only |
| `disable-model-invocation: true` | Yes | No | No |
| `user-invocable: false` | No | Yes | Description only |

Full skill content loads only when invoked. Descriptions are always in context (unless disabled).

---

## Where Skills Live (Priority Order)

| Level | Path | Scope |
|-------|------|-------|
| Enterprise | Managed settings | All org users |
| Personal | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<name>/SKILL.md` | This project |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Where enabled |

Higher priority wins on name collision. Plugins use `plugin:skill` namespace (no conflicts).

Nested discovery: editing files in `packages/frontend/` also loads skills from `packages/frontend/.claude/skills/`.

---

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All args passed to skill |
| `$ARGUMENTS[N]` or `$N` | Positional arg (0-based) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing SKILL.md |

If `$ARGUMENTS` isn't in content, args auto-append as `ARGUMENTS: <value>`.

---

## Dynamic Context Injection

`` !`<command>` `` runs shell commands as preprocessing (before Claude sees anything):

```yaml
---
name: pr-summary
context: fork
agent: Explore
---

## Context
- PR diff: !`gh pr diff`
- Comments: !`gh pr view --comments`

## Task
Summarize this pull request...
```

Each `` !`<command>` `` executes immediately, output replaces placeholder. This is preprocessing, not Claude execution.

**Tip:** Include "ultrathink" anywhere in content to enable extended thinking.

---

## Subagent Execution

`context: fork` runs skill in isolation (no conversation history). Only makes sense with explicit task instructions - guidelines-only skills return nothing useful.

Agent options: `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`.

---

## Permission Control

Three levels:

1. **Deny Skill tool entirely** in `/permissions`: blocks all skill invocation
2. **Allow/deny specific skills**: `Skill(commit)`, `Skill(deploy *)` (prefix match)
3. **Per-skill**: `disable-model-invocation: true` removes from Claude's context

---

## Writing Effective Descriptions

The description is the **primary triggering mechanism**. Claude tends to undertrigger (not use skills when useful), so descriptions should be slightly "pushy".

### Pattern
Include BOTH what the skill does AND specific contexts/keywords for when to use it:

**Weak:** `"API design patterns for this codebase"`

**Strong:** `"Security framework for evaluating and auditing MCP servers and Skills. Use when: installing or evaluating an MCP server, installing or evaluating a Skill, verifying existing MCP servers for rug pulls, running security audits, or when the user mentions 'check my MCPs', 'verify', 'audit', or 'security check'."`

### Quantitative optimization
The skill-creator includes a description optimization loop:
1. Generate 20 eval queries (10 should-trigger, 10 should-not-trigger)
2. Queries must be realistic, detailed, with edge cases (not "Format this data")
3. Run optimization: `python -m scripts.run_loop --eval-set <path> --skill-path <path> --max-iterations 5`
4. Auto-splits 60% train / 40% test to avoid overfitting
5. Returns `best_description` selected by test score

### Triggering behavior
Skills only trigger for tasks Claude can't handle with basic tools alone. Simple one-step queries may not trigger even with perfect descriptions. Design eval queries that are substantive enough to need a skill.

---

## Best Practices for Writing Skills

### Keep SKILL.md under 500 lines
- Move detailed reference to separate files
- Link from SKILL.md: `For details, see [reference.md](reference.md)`

### Use `disable-model-invocation: true` for side effects
- Deploy, send messages, commit, delete - anything irreversible
- Forces manual `/name` invocation

### Restrict tools when possible
- `allowed-tools: Read, Grep, Glob` for read-only skills
- Minimizes blast radius of skill execution

### Explain the why, not just the what
Today's LLMs respond better to reasoning than rigid directives. If you find yourself writing ALWAYS or NEVER in all caps, reframe with the reasoning behind it. Theory of mind > imperative commands.

### Use imperative form
Write instructions as commands: "Run the test suite" not "You should run the test suite".

### Domain organization
When a skill supports multiple domains/frameworks:
```
cloud-deploy/
  SKILL.md (workflow + selection)
  references/
    aws.md
    gcp.md
    azure.md
```
Claude reads only the relevant reference file.

### Bundle repeated work as scripts
If test runs show subagents independently writing similar helper scripts, that's a signal to bundle the script in `scripts/` and reference it from the skill. Saves every future invocation from reinventing the wheel.

### Test both invocation paths
- Auto: phrase request to match description keywords
- Manual: `/skill-name [args]`

---

## Evaluation Framework

### Test cases (evals.json)

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": ["The output includes X", "The skill used script Y"]
    }
  ]
}
```

### Evaluation loop
1. **Spawn parallel runs**: with-skill AND baseline (no skill or old version) for each test case
2. **Draft assertions** while runs are in progress - objectively verifiable, descriptive names
3. **Capture timing** from task notifications (`total_tokens`, `duration_ms`)
4. **Grade**: assertions against outputs -> `grading.json` (fields: `text`, `passed`, `evidence`)
5. **Aggregate**: `benchmark.json` with pass_rate, time, tokens per configuration (mean +/- stddev)
6. **Analyze**: surface non-discriminating assertions, high-variance evals, time/token tradeoffs
7. **Review**: launch viewer for human feedback -> iterate

### Improvement principles
- **Generalize** from feedback - don't overfit to test cases
- **Keep prompts lean** - remove unproductive instructions (read transcripts, not just outputs)
- **Explain the why** - reasoning > rigid rules
- **Look for repeated work** - bundle common scripts

---

## Audit Checklist

When evaluating an existing skill:

### Structure (5 checks)
- [ ] Has `SKILL.md` with valid YAML frontmatter
- [ ] `description` is present, specific, and "pushy" (includes trigger keywords)
- [ ] `name` follows convention (lowercase, hyphens, max 64 chars)
- [ ] Supporting files referenced from SKILL.md actually exist
- [ ] Total SKILL.md under 500 lines; references have TOC if >300 lines

### Security (5 checks)
- [ ] Skills with side effects have `disable-model-invocation: true`
- [ ] `allowed-tools` restricts to minimum needed (flag if missing on task skills)
- [ ] No secrets/credentials in skill content
- [ ] Shell commands in dynamic injection are safe (no user-controlled input)
- [ ] `context: fork` used for tasks that shouldn't access conversation history

### Quality (7 checks)
- [ ] Instructions are explicit enough for `context: fork` (if used)
- [ ] `$ARGUMENTS` or positional args used correctly
- [ ] Description matches actual behavior (not misleading)
- [ ] No overlap/conflict with other skills at same priority level
- [ ] `argument-hint` provided if skill content references `$ARGUMENTS`
- [ ] Imperative form used in instructions
- [ ] Reasoning provided for constraints (not just "ALWAYS do X")

### Context budget (2 checks)
- [ ] Description length reasonable (<500 chars) to fit within 2% context budget
- [ ] If many skills (>10), check for context budget exhaustion via `/context`

### Progressive disclosure (3 checks)
- [ ] SKILL.md focuses on workflow/navigation, not exhaustive detail
- [ ] Reference files clearly linked with guidance on when to read them
- [ ] Scripts execute without needing to be loaded into context

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Skill not triggering | Description too narrow or query too simple. Add trigger keywords. Test with substantive queries |
| Triggers too often | Description too vague. Add specificity or `disable-model-invocation: true` |
| Skills missing from context | Too many skills exceed char budget. Check `/context`. Set `SLASH_COMMAND_TOOL_CHAR_BUDGET` |
| `context: fork` returns empty | Skill has only guidelines, no explicit task. Add concrete instructions |
| Supporting files not found | Use relative paths from SKILL.md location, or `${CLAUDE_SKILL_DIR}` |
| Subagents reinvent wheel | Bundle common scripts in `scripts/`, reference from SKILL.md |
| Description optimization stalls | Eval queries too easy (obvious triggers/non-triggers). Add near-miss edge cases |

---

## Distribution

- **Project**: commit `.claude/skills/` to version control
- **Plugins**: create `skills/` directory in plugin
- **Managed**: deploy org-wide through managed settings

---

## Visual Output Pattern

Skills can bundle scripts that generate HTML visualizations. Use only built-in libraries for portability. Works for dependency graphs, test coverage, API docs, schema visualizations.
