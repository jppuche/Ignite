---
name: antialzheimer
description: >-
  Memory health and cognitive architecture maintenance.
  Use when: memory drift, stale memories, instruction budget bloat,
  post-refactor cleanup, "check memories", "memory health",
  "consolidate", "clean up", or periodic maintenance (~every 10-15 sessions).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
disable-model-invocation: true
---

# Anti-Alzheimer - Memory Health & Cognitive Architecture Maintenance

Version: 0.1

## Why this exists

AI agent memory systems degrade silently. Memories freeze at write-time while rules evolve. Projects complete but their memories persist. Cross-references break. Contradictions accumulate. The result: an agent that advises with full confidence but partial context.

This skill detects and repairs that drift.

## Operation Routing

| User action / argument | Read file | Modifies files? |
|---|---|---|
| `/antialzheimer` or `check` (default) | [op-health-check.md](op-health-check.md) | No - read-only scan |
| `full` or `consolidate` | [op-full-consolidation.md](op-full-consolidation.md) | Yes - backup first |
| `session` or `review` | [op-post-session.md](op-post-session.md) | Maybe - proposes, user approves |

## Cognitive Layer Model

Understanding where information belongs is the core skill. Wrong placement = wrong weight.

| Layer | Loaded | Weight | Content type | Examples |
|---|---|---|---|---|
| **CLAUDE.md** (global) | Always, all projects | Highest | Cross-project rules | Language, tone, safety |
| **CLAUDE.md** (project) | Always, this project | High | Project identity, rules | Stack, conventions, delegation |
| **.claude/rules/** | Always, this project | High | Operational patterns | Learned patterns, debugging, docs index |
| **MEMORY.md** (index) | Always | Medium-High | Instructional descriptors | One-line actionable pointers per memory |
| **Memory files** | On-demand | Medium | User context, project state | Profile, strategies, active projects |
| **docs/system/** | On-demand | Lower | Session artifacts | SCRATCHPAD, CHANGELOG, DECISIONS |

**Key insight**: every line added to an always-loaded layer reduces adherence to ALL other lines in that layer. The ROI of pruning is high. Memories in files are suggestions; rules in CLAUDE.md are enforced.

## What to detect

| Issue | Severity | Description |
|---|---|---|
| **Silent contradiction** | HIGH | Memory says X, CLAUDE.md says NOT-X. Agent receives conflicting instructions |
| **Zombie memory** | MEDIUM | Memory about completed project or obsolete context still occupying cognitive space |
| **Orphan reference** | MEDIUM | Memory references file/memory that no longer exists |
| **Missing cross-reference** | LOW | Related memories don't reference each other, risking "partial personality" advice |
| **Stale descriptor** | LOW | MEMORY.md descriptor doesn't match actual file content |
| **Budget overrun** | MEDIUM | Always-loaded tokens significantly exceed recommended limits |
| **Graduation candidate** | LOW | SCRATCHPAD pattern repeated 3+ times, should promote to learned-patterns |
| **Premature promotion** | MEDIUM | Rule in CLAUDE.md that was promoted without sufficient evidence (< 3 observations) |

## What NOT to save as memory

Before creating or keeping a memory, apply this filter:

- Code patterns, architecture, file paths -> derivable from codebase. Don't save.
- Git history, recent changes -> `git log` / `git blame` are authoritative. Don't save.
- Debugging solutions -> the fix is in the code, the context in the commit message. Don't save.
- Anything already in CLAUDE.md or rules files -> duplicate. Don't save.
- Ephemeral task state -> use tasks/plans for current conversation. Don't save.

Memory is for what is NOT derivable: user profile, strategic context, organizational knowledge, calibration feedback, project state that transcends code.

## Graduation Pipeline

The lifecycle of an observation becoming a rule:

```
Session error/discovery
    -> SCRATCHPAD.md (raw, timestamped)
        -> 3+ repetitions OR critical impact
            -> learned-patterns.md (graduated pattern)
                -> Repeated across projects OR universal applicability
                    -> CLAUDE.md (permanent rule)
```

Each promotion increases enforcement weight but consumes instruction budget. Promote deliberately.

## Failure Modes

These are the most common ways memory consolidation goes wrong:

1. **Silent contradiction** - A memory freezes a rule at write-time. The rule evolves in CLAUDE.md. Now the agent gets conflicting instructions. Detection: diff memory content against CLAUDE.md rules + learned-patterns.

2. **Partial personality** - Incomplete memory sets generate confident but incomplete advice. Origin: this was discovered when two PCs had disjoint memory sets - one knew HOW to work (process), the other knew WHY (strategy). Neither had the full decision chain.

3. **Memory hoarding** - Saving everything as memory when most of it is derivable from code, git, or docs. This bloats the system and increases noise. Test: "Could I derive this by reading the codebase?"

4. **Premature rule promotion** - Moving a single observation straight to CLAUDE.md. Every line in CLAUDE.md reduces adherence to all other lines (linear degradation for frontier models). Promote only after 3+ observations or critical impact.

5. **Over-consolidation** - Merging so much context into one memory that it loses specificity. Every memory should have a clear "when to use" - if it's always relevant, it might belong in CLAUDE.md instead.

6. **Zombie accumulation** - Completed projects, obsolete contexts, resolved decisions lingering as active memories. They compete for attention with current priorities.