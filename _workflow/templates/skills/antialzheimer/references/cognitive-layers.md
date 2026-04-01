# Cognitive Layers - Where Information Belongs

Reference for understanding the full instruction/memory architecture.

## Layer model

```
┌─────────────────────────────────────────────────────┐
│  Global CLAUDE.md (~/.claude/CLAUDE.md)              │  Always loaded, ALL projects
│  Cross-project rules: language, tone, safety         │  Highest enforcement weight
│  Budget: minimal (every line costs everywhere)       │  ~100-150 tokens
├─────────────────────────────────────────────────────┤
│  Project CLAUDE.md                                   │  Always loaded, THIS project
│  Identity, stack, conventions, delegation rules      │  High enforcement weight
│  Budget: <200 lines recommended [DOCS: Anthropic]    │  ~1-1.5k tokens
├─────────────────────────────────────────────────────┤
│  .claude/rules/ (all files auto-loaded)              │  Always loaded, THIS project
│  Learned patterns, debugging, docs index, hooks      │  High enforcement weight
│  Budget: shared with CLAUDE.md line count             │  ~2-3k tokens
├─────────────────────────────────────────────────────┤
│  MEMORY.md index                                     │  Always loaded (auto-memory)
│  Instructional descriptors pointing to memory files  │  Medium-High weight (hypothesis)
│  Budget: <200 lines, truncated after that            │  ~400-600 tokens
├─────────────────────────────────────────────────────┤
│  Individual memory files                             │  On-demand (when read)
│  User profile, project context, feedback, references │  Medium weight
│  Budget: no limit, but each read adds to context     │  Variable
├─────────────────────────────────────────────────────┤
│  docs/system/ (SCRATCHPAD, STATUS, etc.)             │  On-demand
│  Session artifacts, decision log, changelog          │  Lower weight (reference)
│  Budget: per-file limits (STATUS <60, SCRATCHPAD <150)│  Variable
├─────────────────────────────────────────────────────┤
│  docs/ (strategy, research, applications, etc.)      │  On-demand
│  Living documents, evidence, work artifacts          │  Lowest weight (reference)
│  Budget: no system limit                             │  Variable
└─────────────────────────────────────────────────────┘
```

## Instruction degradation

Every line added to an always-loaded layer reduces adherence to ALL other lines in that layer:

- Frontier models (Opus, Sonnet 4): linear degradation pattern [IFScale 2025]
- Smaller models: exponential decay
- Degradation is uniform - it doesn't selectively ignore low-priority rules
- "Every low-value rule you add actively makes your high-value rules less likely to be followed" [HumanLayer]

**Practical implication**: the ROI of removing one unnecessary always-loaded line is that ALL remaining lines become slightly more likely to be followed.

## Placement decision matrix

| Information type | Should live in | Reason |
|---|---|---|
| Language/tone preferences | Global CLAUDE.md | Applies to all projects |
| Safety rules (backup, approval) | Global CLAUDE.md | Universal policy |
| Project identity/stack | Project CLAUDE.md | Project-specific, always needed |
| Delegation/model selection | Project CLAUDE.md | Affects every interaction |
| Graduated patterns | learned-patterns.md | Evidence-backed, project-specific |
| User profile (career, goals) | Memory files | Context, not instruction |
| User feedback (how to work) | Memory files OR CLAUDE.md | Depends on universality |
| Active project state | Memory files | Changes frequently |
| Completed project context | Archive or delete | Zombie candidate |
| Academic/domain rules | Memory files | Only active during relevant work |
| Session observations | SCRATCHPAD | Temporary, may graduate |
| Debugging/post-mortems | LESSONS-LEARNED | Reference for similar future issues |

## Common misplacements

| Symptom | Likely misplacement | Fix |
|---|---|---|
| Rule is often ignored | In memory instead of CLAUDE.md | Promote (if criteria met) |
| Instruction budget over limit | Too many rules in CLAUDE.md | Demote non-critical to memory |
| Memory that never gets read | Zombie or derivable from code | Delete |
| Same info in 2+ places | Duplication across layers | Consolidate to one canonical location |
| Feedback memory contradicts CLAUDE.md | Memory froze old version of a rule | Update or delete memory |