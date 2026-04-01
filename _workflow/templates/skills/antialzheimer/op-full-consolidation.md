# Full Consolidation - 7-Phase Memory Overhaul

Use when health check reports 4+ findings, after major project changes, or every ~15-20 sessions.

**This operation modifies files.** Phase 2 (Backup) is mandatory before any changes.

## Phase 1: Inventory

Discover the complete memory landscape:

```bash
# Memory files
ls .claude/memory/

# Always-loaded instruction files
cat CLAUDE.md
cat ~/.claude/CLAUDE.md  # global, if accessible
ls .claude/rules/

# Async knowledge system
cat docs/system/SCRATCHPAD.md
cat docs/system/STATUS.md
```

Read MEMORY.md to get the index. Read every memory file listed. Count:
- Total memory files
- Total always-loaded lines (CLAUDE.md + rules + MEMORY.md index)
- Total always-loaded tokens (estimate: lines * ~15 tokens avg)

If cross-PC sync is involved, also check for memory sets in alternate paths:
- `~/.claude/projects/<project-hash>/memory/`
- Any old project hash paths (from renames)

## Phase 2: Backup

**Mandatory.** Before any modification:

```bash
cp -r .claude/memory/ .claude/memory_backup_$(date +%Y-%m-%d)
```

Confirm backup exists and has the correct file count before proceeding.

## Phase 3: Contradiction Scan

For each memory file, compare its content against:
- CLAUDE.md rules (project + global)
- learned-patterns.md patterns
- Other memory files (inter-memory contradictions)

Common contradiction patterns:
- Memory says "always do X" but CLAUDE.md says "NOT X" (rule evolved, memory didn't)
- Two memories give conflicting advice about the same topic
- Memory references a process that was replaced

For each contradiction found, determine which version is current/correct:
- If CLAUDE.md is newer: memory is stale -> update or delete memory
- If memory has context CLAUDE.md lacks: enrich CLAUDE.md, then update memory
- If genuinely conflicting: flag for user decision

## Phase 4: Classify

For each memory, assign one action:

| Classification | Criteria | Action |
|---|---|---|
| **Keep** | Still relevant, correctly placed, no issues | No change |
| **Update** | Content is partially stale or descriptor misaligned | Edit in place |
| **Promote** | Feedback that's been validated 3+ times or is critical | Move rule to CLAUDE.md or learned-patterns, keep context in memory or delete |
| **Demote** | Rule in CLAUDE.md that lost relevance or was premature | Move back to memory or delete |
| **Merge** | Two memories cover overlapping territory | Consolidate into one, update references |
| **Archive** | Project completed, context no longer active | Delete memory, note in STATUS.md if needed |
| **Delete** | Duplicates info in CLAUDE.md, or derivable from code/git | Remove entirely |

Present classification table to user before executing.

## Phase 5: Cross-Reference

For each remaining memory, verify bidirectional links:

- **User -> Project**: Do user strategy memories reference the projects that implement them?
- **Project -> User**: Do project memories reference the user context they depend on?
- **Feedback -> Rules**: Do feedback memories reference the CLAUDE.md rules they informed?
- **Project -> Project**: Do related projects reference each other?

Add cross-references where missing. Format: "See also: [related_memory.md](related_memory.md)" or inline references.

The goal: any future Claude reading ONE memory can trace the full context chain through references, not by accident.

## Phase 6: Promote/Demote

Execute the approved promotions from Phase 4:

**Promoting to Global CLAUDE.md** (cross-project rules):
- Must apply to ALL projects, not just this one
- Must address an observed failure (not preemptive)
- Each line added reduces adherence to all other lines - be ruthless

**Promoting to learned-patterns.md** (project patterns):
- Must have 3+ observations or critical impact
- Remove the original SCRATCHPAD entries after graduation

**Demoting from CLAUDE.md**:
- Rule that was promoted but hasn't prevented errors in 10+ sessions
- Rule that is too specific for always-loaded (move to memory)

## Phase 7: Validate

Post-consolidation verification:

1. **File count**: `ls .claude/memory/` matches expectations
2. **Index match**: Every file in directory has a MEMORY.md entry, and vice versa
3. **No orphan refs**: Grep remaining memories for references to deleted files
4. **Descriptor quality**: Each MEMORY.md descriptor is actionable (instruction, not just label)
5. **Budget check**: Count always-loaded lines, compare to recommended limits
6. **validate-docs.sh**: If project has validation scripts, run them
7. **Contradiction re-scan**: Quick pass to confirm no new contradictions introduced

## Output

Present a summary:

```
## Consolidation Summary

| Metric | Before | After | Delta |
|---|---|---|---|
| Memory files | X | Y | ... |
| Always-loaded tokens | X | Y | ... |
| Contradictions | X | 0 | ... |
| Cross-references added | - | N | ... |
| Rules promoted | - | N | ... |
| Memories archived | - | N | ... |
```

Ask user to review changes before committing. If project uses git, stage and commit with descriptive message.