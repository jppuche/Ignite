---
name: advance-phase
description: 'Advance the project to the next workflow phase. Validates exit conditions, updates STATUS.md and CHANGELOG-DEV.md, runs doc validation. Use when: "advance phase", "next phase", "close phase", "phase complete", "mark phase done".'
license: MIT
metadata:
  author: jppuche
  version: "2.2.1"
disable-model-invocation: true
---

# Advance Phase

Validates that exit conditions for the current phase are met, then transitions the project to the next phase. Updates all tracking documents and runs validation.

---

## Procedure

### 1. Read current state

- Read `docs/STATUS.md` — identify current phase from "Current phase" / "Fase actual" section
- Read `docs/STATUS.md` "Project Profile" section — identify profile (Quick/Standard/Enterprise) and active phases
- Read `docs/DECISIONS.md` — count decisions made (entries in the main table)
- If current phase is unclear or STATUS.md is missing: ask user to clarify
- If profile section is missing (legacy project): assume all phases active (Enterprise behavior)

### 2. Validate exit conditions

Check the conditions for the current phase. Report each condition as PASS or FAIL.

| Phase | Exit conditions |
|-------|----------------|
| 0: Foundation | CLAUDE.md exists AND .claude/hooks/ has at least 1 hook AND .claude/quality-gate.json exists AND docs/FOUNDATION.md exists AND Project Profile determined in STATUS.md |
| 1: Technical Landscape | >= 5 decisions in DECISIONS.md main table AND comparison matrices for major stack decisions AND ## Stack section in CLAUDE.md is populated (not placeholder) |
| 2: Tooling & Security | Candidate Ecosystem Catalog section in DECISIONS.md has entries AND every candidate has a Status (APPROVED/REJECTED/DEFERRED/SKIP) |
| 3: Intelligence-Enriched Review | Strategic Assessment section in DECISIONS.md is populated AND Architecture Directives subsection exists AND FOUNDATION.md review completed (updated or noted as "no changes needed") |
| 4: Architecture Blueprint | >= 1 spec file in docs/specs/ (not counting spec-template.md) AND security review documented (in docs/reviews/ or DECISIONS.md) AND Plan Integrity Report in DECISIONS.md |
| N: Development (N.0 Team Assembly) | **N.0:** >= 1 agent file in .claude/agents/ AND (AGENT-COORDINATION.md Section 13 has entries OR Agent Teams disabled). **N.1+:** Read the current block's spec file — check its specific exit conditions section. If no spec identified: ask user which block. |
| Final: Hardening | All pending items in STATUS.md are checked [x] AND docs/SCRATCHPAD.md has no unresolved open questions |

**If ANY condition is FAIL:**

1. Report what's missing with specific details (e.g., "3 decisions found, need >= 5")
2. Ask user: "Force advance anyway? This will log a warning in DECISIONS.md."
3. If user says force: proceed, but append to DECISIONS.md:
   ```
   | YYYY-MM-DD | Phase N force-advanced | Exit conditions not fully met: [list failures] | User override |
   ```
4. If user says no: stop. Do not advance.

**If ALL conditions are PASS:** proceed to step 3.

### 3. Execute transition

Determine the next active phase based on the project profile:

**Profile-aware phase resolution:**
- Read the active phases list from STATUS.md "Project Profile" section
- The next phase is the first phase in the standard sequence that is AFTER the current phase AND is in the active phases list
- If phases are skipped, note them in the transition summary: "Skipped Phase X (not in {profile} profile)"
- If no profile section exists (legacy project): all phases are active

**Profile → Active phases mapping:**

| Profile | Active Phases |
|---------|--------------|
| Quick | 0, N |
| Standard | 0, 1, 2, 3 (fast-path), 4, N, Final |
| Enterprise | 0, 1, 2, 3, 4, N, Final |

> **Standard Phase 3 fast-path:** Auto-skip if: no Candidate Ecosystem Catalog entries in DECISIONS.md AND single stack AND agent pre-selection is "Generalistas" or "Lorekeeper only". Otherwise, Phase 3 runs normally.

> **Phase N includes Team Assembly (N.0):** Agent installation, skill assignment, and consistency checks happen at the start of Phase N before the first development block. For Quick profile, N.0 is skipped (Lorekeeper only). For Standard, N.0 runs without AGENT-COORDINATION.md. For Enterprise, full N.0.

Do these steps in order:

1. **Update `docs/STATUS.md`:**
   - In the Completed section: add `- [x] Phase N: [name]` (or check the existing checkbox)
   - If phases were skipped: also mark them as completed with note: `- [x] Phase X: [name] (skipped — {profile} profile)`
   - In the "Current phase" / "Fase actual" section: change to the next ACTIVE phase name
   - In the Pending section: remove or update the completed phase entry

2. **Append to `docs/CHANGELOG-DEV.md`:**
   ```
   ## YYYY-MM-DD — Phase N complete: [phase name]

   - Exit conditions: [N/N passed | forced]
   - Decisions this phase: [count]
   - Notable: [1-2 key outcomes, or "routine"]
   ```

3. **Run `bash scripts/validate-docs.sh`:**
   - If errors: report them and fix before finalizing
   - If the script doesn't exist: warn and skip (early project)

4. **Append to `docs/SCRATCHPAD.md`:**
   - Under today's date section: `- [lorekeeper] Phase N → Phase N+1 transition. Exit conditions: [summary].`

### 4. Display summary

Present to the user:
- What was completed (phase name + key outcomes)
- If phases were skipped: list them with reason ("Skipped Phase X — not in {profile} profile")
- What the next phase involves (brief description)
- 2-3 recommended first actions for the new phase
- If `_workflow/guides/workflow-guide.md` exists: reference the relevant phase section

---

## Phase sequence

Standard order (adapt if project uses custom phases):

```
Phase 0: Foundation
Phase 1: Technical Landscape
Phase 2: Tooling & Security
Phase 3: Intelligence-Enriched Review
Phase 4: Architecture Blueprint
Phase N: Development Blocks (N.0: Team Assembly, N.1+: per-spec blocks)
Phase Final: Hardening
```

If current phase is "Final" or "Hardening": report "This is the last phase. No next phase to advance to." and stop.

---

## Edge cases

- **Custom phase names** (non-standard, non-English): match by phase number if present (e.g., "Fase 3" → Phase 3 conditions). If no number found: ask user for exit conditions.
- **Multiple unchecked items in Pending**: advance only the current phase (first item in Pending that matches Current phase).
- **CHANGELOG-DEV.md doesn't exist**: create it with the transition entry as the first entry.
- **User runs this mid-phase**: exit conditions won't be met → shows what's missing → safe (no silent advancement).
- **Phase N (Development Blocks)**: each block has its own exit conditions in `docs/specs/block-NN-*.md`. Ask which block if not obvious from STATUS.md.
- **Missing profile section (legacy projects)**: treat as Enterprise (all phases active). Display note: "No project profile found — assuming all phases active."
- **Profile mismatch**: if user tries to advance to a phase not in their profile, warn and ask: "Phase X is not in your {profile} profile. Advance anyway?"
