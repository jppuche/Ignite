---
name: skill-auditor
description: >-
  Audit and review Claude Code skills against best practices. Use when:
  the user says "audit skills", "review skills", "check my skills",
  "skill health check", "/skill-auditor", or when running scheduled
  skill maintenance. Evaluates structure, security, quality, description
  effectiveness, progressive disclosure, and context budget.
disable-model-invocation: true
argument-hint: "[skill-name|all]"
metadata:
  version: "1.0.0"
  author: jppuche
---

# Skill Auditor

Systematic auditor for Claude Code skills. Discovers, evaluates, and recommends improvements based on Anthropic's official best practices and skill-creator patterns.

## Reference

Before evaluating any skill, read `${CLAUDE_SKILL_DIR}/references/best-practices.md` for the full audit checklist, frontmatter reference, evaluation framework, and troubleshooting guide.

## Workflow

### Phase 1: Discovery

Scan all skill locations and build an inventory:

```
Personal:  ~/.claude/skills/*/SKILL.md
Project:   .claude/skills/*/SKILL.md
Plugins:   ~/.claude/plugins/**/skills/*/SKILL.md (read-only, flag but don't fix)
```

If `$ARGUMENTS` specifies a skill name, audit only that skill. If `all` or empty, audit everything in personal + project. Skip plugins unless explicitly requested.

For each skill, record:
- Name, location, scope (personal/project/plugin)
- Line count of SKILL.md
- Supporting file count (scripts/, references/, assets/, evals/)
- Whether it has evals (evals/evals.json)

### Phase 2: Evaluate

Read each skill's full SKILL.md and apply all 5 checklist categories from the reference doc. The categories are:

**2A. Structure** (5 checks) - frontmatter validity, description presence and specificity, name convention, file references, line count

**2B. Security** (5 checks) - side-effect protection, tool restriction, no secrets, safe dynamic injection, appropriate context isolation

**2C. Quality** (7 checks) - fork explicitness, argument handling, description accuracy, no skill collisions, argument hints, imperative form, reasoning over rigid directives

**2D. Context Budget** (2 checks) - description length, total skill count budget pressure

**2E. Progressive Disclosure** (3 checks) - SKILL.md focus, reference linking, script bundling

#### Description quality deep-check

Beyond the basic "is it present" check, evaluate descriptions against the skill-creator's triggering guidance:
- Does it include BOTH what the skill does AND specific trigger keywords?
- Is it "pushy" enough? (Claude undertriggers by default)
- Are near-miss scenarios addressed? (keywords that sound similar but shouldn't trigger)
- Would a substantive query (not a trivial one-step request) reliably trigger it?

#### Repeated work detection

If the skill has been used (check for workspace directories, eval results, or transcripts), look for patterns where subagents independently wrote similar helper scripts. Flag as "bundle candidate" - the script should live in `scripts/`.

### Phase 3: Score and Report

For each skill, assign per-category and overall:
- **PASS** - all checks pass in category
- **WARN** - minor issues (missing argument-hint, description could be more specific, no evals)
- **FAIL** - critical issues (security gaps, broken file references, misleading description)

#### Report format

```markdown
## Skill Audit Report - YYYY-MM-DD

### Summary
| Skill | Scope | Lines | Structure | Security | Quality | Context | Disclosure | Overall |
|-------|-------|-------|-----------|----------|---------|---------|------------|---------|

### Detailed Findings

#### [skill-name] - [PASS|WARN|FAIL]
Location: [path]
Lines: [count] / 500 max
Supporting files: [count] ([list])
Has evals: [yes/no]

**Structure**
- [PASS] Valid frontmatter
- [WARN] Description present but generic: "[current]"
  Suggested: "[improved version with trigger keywords]"

**Security**
- [PASS] allowed-tools restricts to: Read, Bash, Glob, Grep
- [FAIL] Uses Bash but no disable-model-invocation

**Quality**
- [WARN] No argument-hint despite using $ARGUMENTS
- [WARN] Line 45: "ALWAYS verify" - consider explaining why instead

**Progressive Disclosure**
- [PASS] References split into separate files with clear pointers
- [WARN] references/api-docs.md is 450 lines with no TOC

**Recommended actions (priority order):**
1. [CRITICAL] Add `disable-model-invocation: true` (security)
2. [HIGH] Improve description with trigger keywords
3. [LOW] Add argument-hint: "[skill-name|all]"
```

### Phase 4: Fix (optional, with confirmation)

**Auto-fixable** (offer, apply with user confirmation):
- Add missing `argument-hint` based on `$ARGUMENTS` usage
- Add missing `disable-model-invocation: true` to side-effect skills
- Add missing `allowed-tools` based on actual tool usage in content
- Improve description with trigger keywords (present before/after diff)

**Manual-fix only** (report, never auto-apply):
- Restructure skill content or progressive disclosure
- Change `context: fork` behavior
- Rewrite skill logic
- Bundle scripts from repeated work

Always present the diff clearly before applying any change.

## Constraints

- Read-only by default. Only modify in Phase 4 with explicit user approval
- Never modify plugin skills (third-party)
- Flag but don't fail intentionally minimal skills (<20 lines is OK for reference skills)
- When unsure if something is a "side effect", flag as WARN not FAIL
- Report generation: use a structured format that can be compared across audit runs
