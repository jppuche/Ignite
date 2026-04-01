# Post-Session Review - Memory Triage

Lightweight operation after significant sessions. Determines what, if anything, should become or update memory.

## When to use

After sessions that involve:
- User corrections or preference revelations
- New project context or strategic decisions
- Significant changes to project structure or direction
- User explicitly says "remember this"

NOT needed after routine coding, bug fixes, or mechanical tasks.

## Flow

### 1. Session scan

Review the conversation for:

- **User corrections**: "Don't do X", "Actually, I prefer Y", "Stop doing Z"
- **Strategic context**: New information about goals, constraints, stakeholders, timelines
- **Project state changes**: Completed milestones, new blockers, changed priorities
- **Preference signals**: Strong reactions (positive or negative) to approaches taken

### 2. Filter

For each candidate, apply the NOT-memory filter:

| Question | If YES | If NO |
|---|---|---|
| Is this derivable from the codebase? | Don't save | Continue |
| Is this in git history? | Don't save | Continue |
| Is this already in CLAUDE.md or rules? | Don't save (or update existing) | Continue |
| Is this already in an existing memory? | Update existing, don't create new | Continue |
| Will this be useful in future sessions? | Continue | Don't save |

### 3. Classify survivors

Each item that passes the filter:

- **New memory**: Create a new file + add to MEMORY.md index
- **Update existing**: Read the relevant memory, propose changes
- **Graduation candidate**: Note in SCRATCHPAD for future promotion

### 4. Propose

Present candidates to user:

```
## Post-Session Memory Candidates

| # | Type | Content | Target | Rationale |
|---|------|---------|--------|-----------|
| 1 | New feedback | ... | feedback_xxx.md | JP corrected approach 2x |
| 2 | Update | ... | project_xxx.md | Status changed |
| 3 | Skip | ... | - | Derivable from git log |
```

Wait for user approval before writing anything.

### 5. Execute

For approved items:
- Write/update memory files using proper frontmatter format
- Update MEMORY.md index with actionable descriptor
- Verify no contradictions with existing memories or CLAUDE.md

Memory file format:
```markdown
---
name: descriptive name
description: one-line description for MEMORY.md discovery
type: user | feedback | project | reference
---

Content here. Include:
- The fact or rule
- **Why:** context for the correction/preference
- **How to apply:** when and how to use this information
```