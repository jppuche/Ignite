---
name: calibrate
description: >-
  Periodic system calibration - research official sources, audit rules/docs against
  current best practices, update documentation system, verify changes. Use when:
  "calibrate", "audit the system", "check our rules", "are we up to date",
  or every 10-15 sessions proactively.
metadata:
  version: "1.0.0"
  author: jppuche
---

# Calibrate - System Calibration Skill

Periodic recalibration of the project's documentation system, rules, and processes against verified official sources. Not cosmetic maintenance - structural verification that the system is aligned with current reality.

## When to run

- On demand: `/calibrate` or "calibra el sistema"
- Proactively: every 10-15 sessions, or after major Claude Code updates
- After incidents: when rules failed to prevent an error, or a process broke down

## Three-Phase Protocol

### Phase 1: RESEARCH (official sources only)

Gather current best practices from verified sources. Tag everything.

**Mandatory sources (fetch each, skip if unchanged since last calibration):**
1. https://code.claude.com/docs/en/memory - CLAUDE.md mechanics, loading, precedence
2. https://code.claude.com/docs/en/best-practices - writing rules, verification, failure patterns
3. https://howborisusesclaudecode.com/ - Boris Cherny maintenance philosophy
4. https://anthropic.com/engineering/effective-context-engineering-for-ai-agents - context engineering

**Optional sources (when relevant):**
- Claude Code GitHub releases/changelog for new features
- Anthropic engineering blog for new posts
- Claude Code team public posts (Boris, Thariq, etc.)

**Rules:**
- Only [FETCHED] and [DOCS] are actionable. [MEMORY] is hypothesis
- If a source contradicts previous findings, newer source wins
- Note the date of each fetch for staleness tracking

### Phase 2: AUDIT (measure current system against findings)

Apply findings to the actual system. For each file, apply the test:
> "Would removing this line cause Claude to make mistakes?"

**Audit targets (in order):**
1. `CLAUDE.md` - line count, specificity, contradictions with global `~/.claude/CLAUDE.md`
2. `.claude/rules/*.md` - each file: passes removal test? redundant with hooks? inferrable from code?
3. Best practices reference - check `${CLAUDE_SKILL_DIR}/references/best-practices.md` or project's `docs/reference/claude_md_best_practices.md` if present. Still accurate? New findings to add?
4. `.claude/skills/*/SKILL.md` - still aligned with current Claude Code skill format?
5. `.claude/hooks/` - still functional? any new hook events available?

**Audit criteria (from verified sources):**
- **Density** [DOCS]: <200 lines CLAUDE.md, shorter = better adherence
- **Specificity** [DOCS]: concrete and verifiable > vague and abstract
- **No duplication** [DOCS]: exclude what Claude infers from code
- **Hooks > rules** [DOCS]: if it MUST happen, use hook, not advisory rule
- **Emphasis** [DOCS]: IMPORTANT/YOU MUST for critical rules
- **No contradictions** [DOCS]: contradicting rules = arbitrary picks
- **Skills > rules for occasional knowledge** [DOCS]: if not needed every session, use skill

**For each proposed change, classify:**
- SAFE: no risk of reintroducing resolved errors
- MEDIUM: could lose context, needs verification after applying
- RISKY: structural change, needs spot-check with subagents

### Phase 3: APPLY + VERIFY

**Apply changes** in order: SAFE first, then MEDIUM, then RISKY.

**Verify after applying:**
1. `wc -l CLAUDE.md .claude/rules/*.md` - count total auto-loaded lines
2. `bash scripts/validate-docs.sh` - 0 errors mandatory
3. Grep for contradictions between project CLAUDE.md and global CLAUDE.md
4. **Spot-check with 3 parallel subagents** (one per concern area):
   - Subagent A: document lookup test (can Claude find files without Glob?)
   - Subagent B: process test (does Claude follow the right protocol for a complex task?)
   - Subagent C: behavioral test (does Claude push back appropriately?)
5. Lorekeeper hooks still parse correctly (no crash on simulated input)

**If any spot-check fails:** revert that specific change, log in SCRATCHPAD why.

## Output

Present calibration report to user before persisting:

```
## Calibration Report - [DATE]

### Sources checked
- [URL] - [date fetched] - [new findings: Y/N]

### Changes applied
| # | File | Change | Risk | Verified |
|---|------|--------|------|----------|

### Metrics
- Auto-loaded lines: before -> after
- CLAUDE.md: X/200 lines
- Contradictions found: N
- Spot-checks: A/B/C pass/fail

### Next calibration
- Recommended: [date, ~10-15 sessions out]
- Watch for: [specific things that might change]
```

## Configuration

```yaml
sources:
  mandatory:
    - https://code.claude.com/docs/en/memory
    - https://code.claude.com/docs/en/best-practices
    - https://howborisusesclaudecode.com/
    - https://anthropic.com/engineering/effective-context-engineering-for-ai-agents
  optional:
    - https://github.com/anthropics/claude-code/releases
audit_targets:
  - CLAUDE.md
  - .claude/rules/*.md
  - best practices reference (skill-bundled or docs/reference/)
  - .claude/skills/*/SKILL.md
  - .claude/hooks/
verification:
  validate_command: bash scripts/validate-docs.sh
  spot_check_count: 3
  max_auto_loaded_lines: 200
```

## Failure modes

| Failure | Mitigation |
|---------|-----------|
| Source unavailable (URL down) | Skip, note in report, use cached findings from best_practices.md |
| Over-pruning (reintroduce old error) | Spot-checks catch behavioral regression. If in doubt, don't remove |
| Session too short for full calibration | Run Phase 1 only (research), defer audit to next session |
| No new findings | Valid outcome. Report "system aligned, no changes needed" |