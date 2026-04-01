# Memory Classification Guide

Reference for Phase 4 (Classify) of full consolidation.

## Decision tree

For each memory file, walk through:

```
1. Is the content contradicted by CLAUDE.md or learned-patterns?
   YES -> STALE. Update memory to match current rules, or delete if fully redundant.

2. Is the content already in CLAUDE.md, rules, or another memory?
   YES -> DUPLICATE. Delete, or merge if the memory adds unique context.

3. Is the subject (project/context) still active?
   NO -> ZOMBIE. Archive (delete) unless it contains lessons applicable to future work.

4. Is this a RULE (always enforce) or CONTEXT (inform when relevant)?
   RULE -> Should it be in CLAUDE.md? Check: applies to all sessions? 3+ observations?
          YES -> PROMOTE to CLAUDE.md or learned-patterns. Delete or slim the memory.
          NO -> Keep as memory, but ensure descriptor in MEMORY.md is instructional.
   CONTEXT -> Keep as memory. Verify cross-references exist.

5. Is the memory specific enough to be useful?
   NO -> OVER-CONSOLIDATED. Split into focused memories, or trim to core value.

6. Is the MEMORY.md descriptor actionable?
   NO -> UPDATE descriptor to include an instruction, not just a label.
```

## Memory types and their lifecycle

| Type | Created when | Becomes stale when | Typical lifespan |
|---|---|---|---|
| **user** | Learning about user's profile/preferences | User's situation changes significantly | Long (months-years) |
| **feedback** | User corrects behavior | Rule is promoted to CLAUDE.md OR feedback is superseded | Medium (weeks-months) |
| **project** | New active project | Project completes or is abandoned | Medium (project duration) |
| **reference** | External resource identified | Resource moves/changes/becomes irrelevant | Variable |

## Promotion criteria

**To learned-patterns.md:**
- Pattern observed 3+ times across sessions
- OR: single observation with critical impact (prevented significant error)
- Pattern is project-specific (not cross-project)

**To project CLAUDE.md:**
- Rule must apply to every session in this project
- Rule addresses an observed failure (not preemptive)
- The instruction budget can absorb it (check current line count)

**To global CLAUDE.md:**
- Rule must apply to ALL projects
- Rule addresses an observed failure across multiple projects
- Extremely high bar - this is the most expensive real estate in the system