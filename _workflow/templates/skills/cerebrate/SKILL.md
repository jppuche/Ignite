---
name: cerebrate
description: >-
  Intelligent reflection on session knowledge. Harvests explicit facts and
  implicit insights, analyzes through 4 strategic lenses (Confirms, Challenges,
  Opens, Windows), presents intelligence brief, then persists premium documentation.
  Use when: end of session, after research, after strategy conversations, or
  when user says "cerebrate", "consolidate", "reflect", "update docs".
model: opus
disable-model-invocation: true
---

# Cerebrate - Intelligent Session Reflection

## Identity

A moment of deep, intelligent reflection. Mine the full conversation for both explicit knowledge (facts, decisions, data, corrections) and implicit insights (patterns the user revealed without articulating, connections between disparate topics, unstated implications, workflow patterns that emerged organically).

Two equally valuable outputs: (1) a strategic intelligence brief, and (2) premium documentation updates that make each target doc measurably more useful for future sessions.

Cerebrate operates on demand across the ENTIRE project — unlike Lorekeeper which is automated and scoped to docs/system/.

## The 4 Lenses

For each significant knowledge piece, assess through these strategic lenses:

| Lens | Meaning | Action |
|------|---------|--------|
| **CONFIRMS** | Reinforces an existing decision or direction | Increase confidence. May justify accelerating a plan. |
| **CHALLENGES** | Contradicts or weakens an existing assumption | Investigate. Recommend course correction or deeper analysis. |
| **OPENS** | Reveals new possibilities not previously considered | Explore. Bring to user's attention for discussion. |
| **WINDOWS** | Time-sensitive actionability opportunity | Flag urgently. Act before the window closes. |

Not every piece maps to a lens. Some are pure reference data — classify and persist without forcing a lens.

## Configuration

Cerebrate adapts to any project via these configuration points. Projects should define these in their CLAUDE.md or a dedicated cerebrate config:

| Config point | Purpose | Example |
|-------------|---------|---------|
| `doc_inventory` | Path to document index for coherence scanning | `.claude/rules/documents-index.md` or CLAUDE.md Architecture section |
| `validation_command` | Command to run after persistence | `bash scripts/validate-docs.sh` |
| `domain_signals` | Project-specific implicit knowledge to watch for | See Domain Signals section below |
| `persistence_targets` | Default docs to update per knowledge type | `docs/STATUS.md`, `docs/DECISIONS.md`, etc. |
| `coherence_scope` | How deep coherence scan should go | `internal` (single doc) / `cross-doc` / `project` / `objectives` |

### Domain Signals (project-specific)

Each project can define what implicit signals Cerebrate should watch for beyond standard knowledge harvesting. Examples:

- **Product project:** "Did this session reveal user needs not captured in the PRD?"
- **Research project:** "Did findings challenge or confirm the hypothesis?"
- **Career project:** "Did work demonstrate capability worth documenting in portfolio?"
- **Open source project:** "Did this session produce patterns useful for CONTRIBUTING.md?"

If no domain signals are configured, Cerebrate harvests standard explicit + implicit knowledge only.

## Flow: REFLECT -> PRESENT -> PERSIST

### REFLECT

Review the entire conversation. Harvest:
- **Explicit:** Facts, decisions, stats, corrections, preferences stated during the session.
- **Implicit:** Patterns not articulated. Connections between disparate topics. Shifts in priority or tone signaling evolving thinking. Skills demonstrated but undocumented. Workflow patterns worth codifying.
- **Domain signals:** Check project-specific signal definitions. Harvest if relevant.

Apply the 4 lenses. Discard what's already in existing docs or derivable from project context and Claude memory. Read the doc inventory source for the full document list.

**Coherence scan (4 levels):**
1. **Internal:** Does the new knowledge contradict anything within the same document?
2. **Cross-doc:** Does updating doc A mean doc B is now stale or contradictory?
3. **Project:** Does the project state still align with its declared objectives?
4. **User objectives:** Does the knowledge affect the user's broader goals beyond this project?

Include any coherence findings in the intelligence brief. This happens in REFLECT, NOT in PERSIST — the user sees the full scope before approving.

If the session produced no significant knowledge, say so and stop.

### PRESENT

Show the intelligence brief:
- **Headline:** The most important insight from this session (1-2 sentences)
- **4-lens assessment:** Table or prose — whichever is clearer for the content
- **Implicit insights:** What emerged that wasn't explicitly stated
- **Domain signals:** Only if project-specific signals were triggered
- **Actionability windows:** Only if time-sensitive items exist
- **Coherence findings:** Docs that need updating due to ripple effects, not just direct new knowledge
- **Persistence plan:** What goes where, what's discarded, docs not affected

Wait for user approval before touching any file.

### PERSIST

Execute the approved plan. Each update is curated, not filed — it should make the target doc measurably more useful. The coherence work was already identified in REFLECT and approved in PRESENT; no scope surprises here.

Run the configured validation command after all updates. Report results.

## Interaction with Lorekeeper

Cerebrate and Lorekeeper have complementary scopes:

| | Cerebrate | Lorekeeper |
|---|-----------|-----------|
| **Trigger** | On demand (user invokes) | Automated (session start/end hooks) |
| **Scope** | Entire project — any doc, any insight | docs/system/ only (SCRATCHPAD, CHANGELOG, STATUS, CLAUDE.md) |
| **Depth** | Strategic (4 lenses, coherence scan, implicit insights) | Operational (freshness, graduation, pending items) |
| **Updates** | Any project document the user approves | Only docs it owns (append-only where required) |

**Sequencing:** If Lorekeeper SessionEnd fires after Cerebrate, it should find docs already current. If both update the same file, Cerebrate's curated update takes precedence — Lorekeeper should detect freshness as satisfied and skip redundant updates.

**Shared constraints:** Both respect STATUS < 60 lines, SCRATCHPAD < 150 lines, append-only rules where declared.

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| **Session too short** | No significant knowledge to harvest | Say so and stop. Don't force insights from trivial sessions. |
| **Scope creep in PERSIST** | Coherence scan discovers cascade of stale docs | All coherence findings are presented in PRESENT. User approves scope BEFORE any file is touched. |
| **Conflicting with Lorekeeper** | Both try to update SCRATCHPAD | Cerebrate runs first (on demand). Lorekeeper detects freshness and skips. |
| **Doc inventory stale** | Coherence scan misses documents | Use glob search as fallback if doc inventory is missing or outdated. |
| **Large session context** | Too many knowledge pieces to analyze manually | Use subagents for parallel coherence checks (efficient when 5+ pieces vs doc base). |
| **No validation command** | Can't verify doc integrity after updates | Warn user that no validation was run. Suggest adding one to project config. |

## Calibration

The flow adapts to session size. Claude decides the appropriate scope, subagent usage, and depth autonomously:
- **Small session (1-3 knowledge pieces):** Direct grep/read, no subagents
- **Medium session (4-8 pieces):** Mixed approach, subagents for coherence
- **Large session (9+ pieces):** Full subagent delegation for parallel analysis

## Example (domain-agnostic)

In a session where a team discussed API redesign with performance benchmarks:

**Headline:** The v2 API redesign validates the caching hypothesis but invalidates the timeline — the auth migration dependency was undiscovered until today.

| Knowledge | Lens | Implication |
|---|---|---|
| Benchmarks show 3x throughput with cache layer | CONFIRMS | Caching investment justified. Accelerate implementation. |
| Auth service uses deprecated OAuth flow | CHALLENGES | Timeline assumed auth was v2-ready. Migration required first. |
| Competitor launched GraphQL API yesterday | WINDOWS | Market window for REST-first advantage closing. Ship v2 before they iterate. |
| Team member revealed deep gRPC experience | OPENS | gRPC gateway option not previously considered. Evaluate as v2.1. |

**Implicit:** The team's instinct to benchmark before committing reveals an engineering culture worth codifying as a project decision-making pattern.

**Coherence:** Updating ROADMAP.md with auth dependency requires SPRINT-PLAN.md timeline adjustment and STATUS.md milestone revision.

**Persisted:** 4 files updated. Validation: 0 errors.
