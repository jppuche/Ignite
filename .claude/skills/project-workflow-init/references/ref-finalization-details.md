# Step 5: Finalization Details

## 5.5 Cleanup setup files

Move skill README, generate project README, then remove files only needed for setup. Inform the user before proceeding.

### 5.5.1 Inform user

Display:
```
Finalizando setup:

  Moviendo:
    - README.md → docs/ignite-reference.md (referencia de la skill)

  Generando:
    - README.md (README del proyecto desde template)

  Eliminando:
    - .claude/skills/project-workflow-init/ (skill de inicializacion, ya ejecutado)
    - _workflow/templates/ (templates ya procesados)

  Manteniendo:
    - _workflow/guides/ (referencia permanente del workflow)
    - .gitignore (configuracion del proyecto)
    - Todos los archivos generados
```

### 5.5.2 Execute cleanup

Execute in order:
1. Handle `README.md` → `docs/ignite-reference.md`
   - If `docs/` doesn't exist: create it (should already exist from Step 3.1)
   - **Mid-way safety:** If `PROJECT_MODE == "mid-way"` and `./README.md` exists, it is the USER's README, not the Ignite distribution README. In this case, use AskUserQuestion (adapt to `{{IDIOMA}}`):
     ```
     "Your project already has a README.md. How should we handle it?"
       1. "Keep my README (Recommended)" — Skip move, generate Ignite reference as docs/ignite-reference.md from skill README
       2. "Replace with Ignite template" — Move existing to docs/README-original.md, generate new from template
       3. "Generate alongside" — Keep existing, generate template as README-ignite.md
     ```
     If option 1: copy `_workflow/guides/workflow-guide.md` summary to `docs/ignite-reference.md` instead. Do NOT move user's README.
     If option 2: move user's README to `docs/README-original.md` (not `docs/ignite-reference.md` — avoid misattribution), then generate from template.
     If option 3: generate from template as `./README-ignite.md`.
   - **Fresh project:** Move `README.md` → `docs/ignite-reference.md` (normal behavior — this IS the Ignite README)
   - If `docs/ignite-reference.md` already exists (re-run): ask user whether to overwrite or skip
   - **Windows/OneDrive:** Use read + write + delete instead of move to avoid sync locks
2. Generate project `README.md` from `_workflow/templates/docs/README.template.md` (skip if user chose option 1 or 3 above)
   - Replace placeholders: `{{NOMBRE_PROYECTO}}`, `{{DESCRIPCION_CORTA}}`, `{{STACK}}`, `{{FECHA}}`
   - Adapt natural-language text to `{{IDIOMA}}`
   - Write to `./README.md`
3. Delete `.claude/skills/project-workflow-init/` (entire directory)
4. Delete `_workflow/templates/` (entire directory)

If `_workflow/` only contains `guides/` after deletion, keep the directory.
If `.claude/skills/` is now empty (Cerbero not enabled), remove the empty directory.

### 5.5.3 Verify

Confirm:
- `docs/ignite-reference.md` exists (moved successfully)
- `README.md` exists (generated successfully)
- Setup directories removed

If any step fails, warn user but continue with remaining steps.

---

## 5.6 Summary

> **Adaptive:** If `USER_LEVEL == "guided"`, show simplified summary grouped by purpose and 2 next-step options. If `USER_LEVEL == "advanced"`, show full file-by-file summary with configuration table and 3 next-step options. See [ref-adaptive-ux.md](ref-adaptive-ux.md) (Finalization Adaptations).

Display a comprehensive summary in `{{IDIOMA}}`. The goal: both technical and non-technical users understand everything that was installed and what each component does.

### Guided Summary

Group by purpose, omit file paths, omit configuration table (adapt to `{{IDIOMA}}`):

```
--- Setup Complete ---

 Your project is ready with:

   Documentation — 6 files for tracking status, decisions, and learning
   AI Agents — Lorekeeper is active (documentation automation)
   Quality Rules — {rule_count} rules for documentation, testing, style, debugging
   Automation — {hook_count} hooks for session management and code quality
   [if Cerbero] Security — Cerbero framework for tool and prompt safety
   CI/CD — GitHub Actions pipeline for automated checks

 Everything is saved automatically between sessions via hooks.
```

Then add Phase framing (adapt to `{{IDIOMA}}`):
```
"This was Phase 0: Foundation — your project infrastructure is ready.

 Next is Phase 1: Technical Landscape — where you define your stack
 decisions, evaluate tools, and scan the ecosystem for useful skills.

 You can start Phase 1 now or in a future session. Your progress is
 saved automatically via hooks.

 For details on any component, just ask. The full workflow guide is at _workflow/guides/workflow-guide.md."
```

Then use AskUserQuestion (in `{{IDIOMA}}`):
```
"What would you like to do?"
  1. "Start Phase 1 (Recommended)" — Define your technical landscape
  2. "Stop here" — Continue in a future session (progress saved)
```

### Advanced Summary

**Principle:** Each file/component gets a brief parenthetical description explaining its purpose. Descriptions are not fixed — adapt to context, but always informative.

**Format (adapt language and descriptions to `{{IDIOMA}}`):**

> **Note:** Section headings below are illustrative (Spanish). Translate all natural-language headings and descriptions to `{{IDIOMA}}` at generation time. Technical names (file paths, hook events) stay in English.

```
## Setup Completado

### Archivos creados

**Docs:**
- docs/ignite-reference.md (Ignite reference — moved from setup README)
- docs/STATUS.md (tracks current project phase and status)
- docs/DECISIONS.md (records architectural and technical decisions)
- docs/CHANGELOG-DEV.md (development changelog for internal tracking)
- docs/SCRATCHPAD.md (error log for agents — essential for compound engineering)
- docs/LESSONS-LEARNED.md (incident post-mortems with root cause analysis)
- docs/specs/spec-template.md (reusable template for feature specifications)
[If Agent Teams: docs/AGENT-COORDINATION.md (multi-agent coordination protocol)]

**Agents:**
- .claude/agents/Lorekeeper.md (automatic documentation agent)

**Rules:**
- .claude/rules/documentation.md (documentation standards and requirements)
- .claude/rules/testing.md (testing requirements and conventions)
- .claude/rules/styling.md (code style conventions)
- .claude/rules/compound-engineering.md (agent learning from past errors)
- .claude/rules/debugging.md (systematic debugging via Prediction Protocol)

**Hooks:** (automated scripts triggered by Claude Code events)
- .claude/hooks/lorekeeper-session-gate.py — SessionStart (injects project context at session start)
- .claude/hooks/lorekeeper-commit-gate.py — PreToolUse (blocks commits without valid documentation)
- .claude/hooks/lorekeeper-session-end.py — SessionEnd (saves pending items for next session)
[If Cerbero:]
- .claude/hooks/validate-prompt.py — UserPromptSubmit (scans prompts for injection attempts)
- .claude/hooks/pre-tool-security.py — PreToolUse (validates command security)
- .claude/hooks/mcp-audit.py — PreToolUse (audits MCP tool invocations)

**Scripts:**
- scripts/validate-docs.sh (validates documentation structure and content)
- scripts/validate-placeholders.sh (validates placeholder resolution in generated files)

[If Cerbero:]
**Security:**
- .claude/skills/cerbero/ (security skill — evaluates MCPs/Skills before install)
- .claude/security/trusted-publishers.txt (trusted publisher list — intentionally minimal, see setup-guide.md A.5)

**Config:**
- .claude/settings.local.json (hook event configuration)
- .claude/ignite-version.json (tracks installed Ignite version for update checks)
- .claude/security/user-profile.json (user experience level — guided/advanced)
[If Agent Teams: .claude/settings.json (teams environment config)]

**Project root:**
- README.md (project README — generated from template)

**Modified:**
- CLAUDE.md — added sections: Stack, Commands, Style, Rules, Architecture, Learned Patterns
- .gitignore — added workflow entries

### Configuration

| Setting | Value |
|---------|-------|
| Stack | {detected stack} |
| Profile | {stack profile name} |
| Agents | {pre-selected agents} |
| Agent Teams | {Yes/No} |
| Security (Cerbero) | {Yes/No} |
| Git | {Yes/No/Already initialized} |
| User Level | {USER_LEVEL} |
| Validation | {errors} errors, {warnings} warnings |
[If PROJECT_MODE == "mid-way":  | Integration | {INTEGRATION_LEVEL} |]

Lorekeeper is active — 3 hooks configured in .claude/settings.local.json.
Agent pre-selection recorded in docs/STATUS.md (installation happens in workflow Phase 5).

Phase 0: Foundation complete.

Next: Phase 1 — Technical Landscape
  - Evaluate technical choices within your stack (auth, ORM, state management)
  - Define validation tools (linters, type checkers, visual testing)
  - Ecosystem scan: discover skills/MCPs relevant to your stack
  - Document all decisions in docs/DECISIONS.md

Full workflow phases: _workflow/guides/workflow-guide.md
```

If STATE != "fresh", add a post-generation report section after the summary above:

```
### Existing Files Processed

| File | Action | Detail |
|------|--------|--------|
[For each file in ANALYSIS where exists == true:]
| {file} | {action_icon} {action_label} | {one-line detail} |

Legend: [=] unchanged  [+] sections added  [^] updated  [~] kept your version  [?] asked
```

After the summary, add:

```
"For details on any component, just ask. The full workflow guide is at _workflow/guides/workflow-guide.md."
```

Then use AskUserQuestion (in `{{IDIOMA}}`):
```
"Phase 0 complete. What would you like to do next?"
  1. "Start Phase 1 (Recommended)" — Technical Landscape: stack decisions + ecosystem scan
  2. "Review generated files" — Inspect what was created before proceeding
  3. "Stop here" — Continue in a future session (progress saved via hooks)
```
