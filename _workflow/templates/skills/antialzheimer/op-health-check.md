# Health Check - Read-Only Memory Scan

Default operation. Detects drift without modifying anything.

## Flow

### 1. Gather context

Read these files (all are needed for cross-validation):

```
CLAUDE.md (project)
~/.claude/CLAUDE.md (global, if accessible)
.claude/rules/learned-patterns.md
.claude/memory/MEMORY.md
All individual memory files listed in MEMORY.md
docs/system/SCRATCHPAD.md (for graduation candidates)
```

### 2. Run checks

For each memory file, evaluate:

**Contradiction scan** (HIGH severity):
- Compare each memory's content against CLAUDE.md rules and learned-patterns
- Flag any case where memory says X but a rule says NOT-X or a different version of X
- Pay special attention to feedback memories - they freeze corrections at write-time

**Zombie detection** (MEDIUM severity):
- Is the memory about a project/context that is completed or no longer active?
- Check STATUS.md pending items - if the project isn't listed, is the memory still relevant?
- Project memories with all items marked complete are zombie candidates

**Orphan references** (MEDIUM severity):
- Does the memory reference other memory files? Do those files exist?
- Does the memory reference docs that have been moved/deleted?

**Cross-reference gaps** (LOW severity):
- Are related memories linked to each other?
- User strategy memories should reference the project memories that implement them
- Project memories should reference the user context they depend on

**Descriptor alignment** (LOW severity):
- Does each MEMORY.md descriptor accurately summarize the file's content?
- Is the descriptor actionable (an instruction, not just a label)?

**Budget check** (MEDIUM severity):
- Count lines in all always-loaded files (CLAUDE.md + rules/ + MEMORY.md)
- Compare against recommended limits
- Flag if significantly over budget

**Graduation candidates** (LOW severity):
- Check SCRATCHPAD.md for patterns repeated 3+ times
- Check for observations tagged as "critical impact"
- These should be promoted to learned-patterns.md

### 3. Report

Present findings as a table:

```
| # | Severity | Issue | File | Description | Suggested action |
|---|----------|-------|------|-------------|------------------|
```

Sort by severity (HIGH first).

### 4. Recommend

- 0 findings: "Memory system is healthy. Next check in ~10 sessions."
- 1-3 findings: "Minor drift detected. Address individually or defer to next full consolidation."
- 4+ findings: "Significant drift. Recommend `/antialzheimer full` to consolidate."

Do NOT modify any files. Present findings and let the user decide.