# CLAUDE.md Editing Reference

> Guide for creating and maintaining CLAUDE.md files.
> Based on official Anthropic documentation.
> Last verified: 2026-03-30

**The essentials in 4 rules:**

1. Keep under 200 lines — beyond that, rules get ignored [DOCS]
2. Only include what Claude cannot infer from the code
3. Critical rules → implement as hooks, not just text [DOCS]
4. SCRATCHPAD → 3+ occurrences → graduate to CLAUDE.md

---

## 1. What is CLAUDE.md

A Markdown file read at the start of every Claude Code session. Persistent project memory: conventions, commands, architecture, and rules that Claude cannot infer from the code. Required name: `CLAUDE.md` (case-sensitive). Reloaded automatically after context compaction.

**Important mechanics** [DOCS: code.claude.com/docs/en/memory]:

- CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself
- Claude treats instructions as context, not enforced configuration — the more specific and concise, the more consistently Claude follows them
- Settings rules are enforced by the client regardless of what Claude decides. CLAUDE.md instructions shape behavior but are not a hard enforcement layer
- CLAUDE.md fully survives compaction — after `/compact`, Claude re-reads from disk and re-injects it fresh
- For system-prompt-level priority: use `--append-system-prompt` (scripts/automation only)

---

## 2. File Hierarchy

More specific takes precedence over more general:

| Type | Location | Scope | Git |
|------|----------|-------|-----|
| Enterprise policy | `C:\Program Files\ClaudeCode\CLAUDE.md` | Organization | IT/DevOps |
| User memory | `~/.claude/CLAUDE.md` | All your projects | No |
| User rules | `~/.claude/rules/*.md` | All your projects | No |
| Project memory | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team | Yes |
| Project rules | `./.claude/rules/*.md` | Team | Yes |
| Project local | `./CLAUDE.local.md` | Only you, this project | No (auto-gitignore) |
| Child dirs | `./subdir/CLAUDE.md` | On-demand when reading files in subdir | Depends on location |
| Auto memory | `~/.claude/projects/<id>/memory/` | Only you, per project | No |

Note: `.claude/rules/` files with `paths:` frontmatter are intended for conditional loading, but this feature is currently broken (anthropics/claude-code#16299 OPEN) — all rules load globally. Design your token budget assuming everything loads.

---

## 3. Recommended Structure

### Essential sections

```markdown
# Project
Brief description of the project and its main stack.

# Commands
- Build: `npm run build`
- Test: `npm run test -- --watch`
- Lint: `npm run lint`

# Code Style
- ES Modules, not CommonJS
- PascalCase components, hooks prefixed with `use`

# Workflow
- Typecheck after each series of changes
- Prefer individual tests, not the full suite
```

### Optional sections

| Section | Purpose | Example |
|---------|---------|---------|
| Architecture | Non-obvious decisions not visible in code | Monorepo: apps/web, apps/api |
| Warnings | Gotchas and common errors | NEVER modify /migrations |
| Skills | Installed skills with triggers | `/cerbero` → security evaluation |
| Hooks | Active deterministic enforcement | validate-prompt.py blocks injection |
| Terminology | Domain definitions | Sprint = 2-week iteration |
| Agent Teams | File ownership and skills per agent | See Agent Teams subsection |
| Scratchpad | Reference to session log | See `docs/SCRATCHPAD.md` |
| Learned Patterns | Patterns graduated from SCRATCHPAD | See Compound Engineering |
| Compaction | What to preserve when compacting context | See Limits and Compaction |

### Skills in CLAUDE.md

Document installed skills so Claude and agents know what to consult:

```markdown
# Skills
| Skill | Trigger | Description |
|-------|---------|-------------|
| Cerbero | /cerbero | Security evaluation of MCPs/Skills |
```

Skills are consultive knowledge — invoke BEFORE each relevant task.

### Agent Teams

When the project uses Agent Teams, CLAUDE.md must include:

- **File ownership** — Exclusive folders per worker. Two workers NEVER edit the same file.
- **Architecture** — Decisions that agents consult for coherence.
- **Skills mapping** — Which skill each agent consults before its task.

Detailed coordination goes in `docs/AGENT-COORDINATION.md`, not in CLAUDE.md.

### Imports with @

```markdown
See @docs/api-patterns.md for API conventions.
```

- Paths are relative to the containing file. Max 5 levels
- Not evaluated inside code blocks
- First use requires user approval; if rejected, they remain permanently disabled

---

## 4. Enforcement: Rules and Hooks

### Modular rules (.claude/rules/)

All `.md` files in `.claude/rules/` load with the same priority as CLAUDE.md. Conditional rules by path (note: path-based filtering is currently broken — see hierarchy note above):

```markdown
---
paths: ["src/api/**/*.ts"]
---
All endpoints must include input validation.
```

### Hooks

Deterministic enforcement for rules that CLAUDE.md alone cannot guarantee [DOCS]:

- "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens"
- "Use hooks for actions that must happen every time with zero exceptions"
- If behavior MUST be guaranteed: hook. If it is guidance: CLAUDE.md rule

| Event | When | Typical use |
|-------|------|-------------|
| `UserPromptSubmit` | When prompt is sent | Detect prompt injection |
| `PreToolUse` | Before tool execution | Block dangerous commands, audit MCP |
| `PostToolUse` | After tool execution | Logging, validation |
| `Stop` | Before Claude finishes | Quality gates, prevent premature stops |
| `PreCompact` | Before context compaction | Preserve critical information |
| `PostCompact` | After context compaction | Re-inject ephemeral state |
| `SessionStart` | When session starts | Inject dynamic context |
| `SessionEnd` | When session ends | Checkpoints, cleanup |
| `InstructionsLoaded` | After all CLAUDE.md files load | Validate configuration |
| `ConfigChange` | When settings change | Audit configuration changes |
| `WorktreeCreate` | When git worktree is created | Environment setup |
| `WorktreeRemove` | When git worktree is removed | Cleanup |
| `Elicitation` | When Claude requests clarification | Custom input handling |
| `ElicitationResult` | After user responds to elicitation | Process user input |

Configuration in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "command": "python .claude/hooks/validate-prompt.py" }],
    "PreToolUse": [{ "command": "python .claude/hooks/pre-tool-security.py", "tools": ["Bash"] }]
  }
}
```

**Rule:** If a rule is critical → implement as a hook, do not rely on text in CLAUDE.md alone.

> There are 21 hook events in total. See the [hooks documentation](https://code.claude.com/docs/en/hooks) for complete reference.

---

## 5. Compound Engineering — Evolving CLAUDE.md

Cycle for growing CLAUDE.md from real learnings, not assumptions [FETCHED: Boris Cherny]:

- "Ruthlessly edit over time until Claude's mistake rate measurably drops"
- "Claude is eerily good at writing rules for itself" — after a correction, ask Claude to add the rule
- "The whole team contributes multiple times per week"
- Failure-driven: start minimal, add rules only for observed failures

```
SCRATCHPAD.md (session) → pattern repeated 3+ times → CLAUDE.md "Learned Patterns"
```

1. **Record** — At the end of each session, note in SCRATCHPAD: errors, corrections, what worked, what did not.
2. **Detect** — Pattern 3+ times in SCRATCHPAD = graduation candidate.
3. **Graduate** — Move to the `# Learned Patterns` section of CLAUDE.md as a permanent rule.
4. **Prune** — Remove graduated entries from SCRATCHPAD. Remove obsolete patterns from CLAUDE.md.

> **Relevance test:** "If I remove this line, would Claude make mistakes?" If NO → remove. [DOCS]

### When to update

| Signal | Action |
|--------|--------|
| Claude repeats an avoidable error | Add rule |
| Claude asks something CLAUDE.md should answer | Improve phrasing |
| Claude gets it right without needing the rule | Remove (prune) |
| New tools or workflows | Update commands |

---

## 6. Limits and Compaction

| Constraint | Value | Impact |
|------------|-------|--------|
| CLAUDE.md root lines | 50-100, max 300 | More lines = rules ignored [DOCS] |
| Effective instructions | ~150-200 (system prompt uses ~50) | Only ~100-150 of yours are followed |
| Auto memory | First 200 lines | Move details to topical files |
| Skills budget | 2% of context window (~16k chars) | Excess skills silently excluded |
| Context window | Finite, degrades | Use /clear between tasks |

"Context rot" — as token count increases, the model's ability to accurately recall information decreases. This is a performance gradient, not a cliff. [FETCHED: Anthropic Engineering]

### Compaction

When context fills (~95%), Claude Code compacts (summarizes) the conversation. CLAUDE.md reloads after compaction, but session instructions may be lost.

- Add directives in CLAUDE.md: `When compacting, preserve the list of modified files and test commands`
- `/compact <instructions>` for directed manual compaction
- `/context` shows current context usage and warnings about excluded skills

### Verification > Instructions [DOCS]

- "Claude performs dramatically better when it can verify its own work"
- "This is the single highest-leverage thing you can do"
- Tests, screenshots, expected outputs, linters — any mechanism for Claude to self-check produces higher-quality output than more instructions alone

---

## 7. Content Criteria

### What to include [DOCS]

- Commands Claude cannot guess
- Style rules that differ from standard conventions
- Test runners and specific configuration
- Repository conventions (branches, commits, PRs)
- Architectural decisions specific to the project
- Developer environment quirks (required env vars)
- Gotchas and non-obvious behaviors
- Installed skills with triggers
- Active hooks and their purpose

### What NOT to include [DOCS]

- Conventions Claude already knows by default
- Extensive documentation (link with @imports instead)
- Information that changes frequently
- Credentials or API keys
- Task-specific instructions (→ Skills)
- Detailed agent coordination (→ docs/)
- Self-evident practices like "write clean code"

### Anti-patterns

| Anti-pattern | Solution |
|--------------|---------|
| > 300 lines | Prune. If Claude gets it right without the rule, remove it |
| Vague instructions | Specific: "2 spaces, semicolons always" |
| Outdated content | Treat as living code, review periodically |
| Duplication | Once, clear and direct |
| Everything in one file | Modularize with `.claude/rules/` |
| Rules without enforcement | Implement as hook |
| Task-specific info | Move to Skills |
| Inline agent coordination | Move to `docs/AGENT-COORDINATION.md` |

### Writing rules effectively [DOCS]

- Direct imperative: "Use X", "Do not do Y"
- One instruction per bullet
- `IMPORTANT` or `NEVER` for critical rules
- Concrete examples over abstract explanations
- "For an LLM, examples are the 'pictures' worth a thousand words" [FETCHED: Anthropic Engineering]
- Avoid contradictions across files — Claude picks arbitrarily when two rules conflict

---

## 8. Verification and Diagnostics

### Pre-commit checklist

- [ ] Under 200 lines (ideally 50-100 in root)
- [ ] Every line passes the relevance test
- [ ] No credentials or sensitive information
- [ ] Commands tested and up to date
- [ ] No duplication
- [ ] Skills with triggers documented
- [ ] Critical hooks implemented (not just text)
- [ ] Task-specific content in Skills, not in CLAUDE.md
- [ ] Agent coordination in docs/, not inline
- [ ] Imports (@) point to existing files

### Diagnostics

| Command | What it shows |
|---------|--------------|
| `/memory` | Loaded memory files and their sources |
| `/context` | Context usage and warnings about excluded skills |
| `claude --debug` | Detail of executed hooks and matching |
| `Ctrl+O` | Verbose mode: thinking, hooks, internal reasoning |

### Common problems

| Symptom | Probable cause | Solution |
|---------|---------------|---------|
| Claude ignores instructions | CLAUDE.md too long | Prune below 200 lines |
| Instructions lost after long session | Compaction removed context | Add compaction directives |
| Claude asks things that are in CLAUDE.md | Ambiguous phrasing | Rewrite in direct imperative |
| Hook does not execute | Incorrect configuration | Verify with `claude --debug` |
| Skill does not appear | Char budget exceeded | Verify with `/context` |

---

## 9. Ecosystem

| Tool | Relationship with CLAUDE.md |
|------|-----------------------------|
| `.claude/rules/` | Same priority, automatic load. Modularizes rules |
| `CLAUDE.local.md` | Local override (sandbox URLs, test data). Auto-gitignore |
| `.claude/skills/` | Consultive knowledge. Document in Skills section |
| `.claude/agents/` | Sub-agents with own system prompt and tools. Consume CLAUDE.md |
| Hooks | Deterministic enforcement. 21 events available |
| Auto memory | Claude's notes to itself. Graduation candidates |
| `SCRATCHPAD.md` | Session log. Source for Learned Patterns |
| `.claude/commands/` | Custom slash commands. Independent of CLAUDE.md |
| Plugins | Distributable packages (skills + hooks + agents). Own namespace |

---

## Karpathy Principles for AI Coding

1. **Don't assume** — verify before acting; ask when uncertain
2. **Don't hide confusion** — surface inconsistencies rather than guessing
3. **Surface tradeoffs** — present options with pros/cons, do not silently pick one
4. **Goal-driven execution** — stay focused on the actual objective
5. **Don't overcomplicate** — 100 lines when 100 suffice, not 1000
6. **Don't touch what you don't understand** — avoid changing unrelated code as side effects

---

## Appendix: Template-Based Generation

For teams that initialize projects frequently, CLAUDE.md can be generated from templates:

```
_workflow/templates/CLAUDE.template.md  →  ./CLAUDE.md (target project)
```

- Placeholder format: `{{PLACEHOLDER_NAME}}`
- Declare ALL placeholders in a mapping file (e.g., `file-map.md`)
- Bidirectional rule: placeholder in mapping file ↔ placeholder in template
- Generation skill with `disable-model-invocation: true` — deterministic processing

---

## Sources

**Official** [DOCS]:
- Memory: https://code.claude.com/docs/en/memory
- Best Practices: https://code.claude.com/docs/en/best-practices
- Hooks: https://code.claude.com/docs/en/hooks
- Skills: https://code.claude.com/docs/en/skills
- Blog — CLAUDE.md Files: https://claude.com/blog/using-claude-md-files

**Fetched and verified** [FETCHED]:
- Boris Cherny (Claude Code creator): https://howborisusesclaudecode.com/
- Anthropic Engineering — Effective Context Engineering: https://anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Community** [AGGREGATOR, lower rigor]:
- Builder.io: https://www.builder.io/blog/claude-md-guide
- HumanLayer: https://www.humanlayer.dev/blog/writing-a-good-claude-md
- Dometrain: https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/
- Gend.co: https://www.gend.co/blog/claude-skills-claude-md-guide

**Rigor assessment:** [DOCS] = authoritative, treat as ground truth. [FETCHED] = verified against live source, high confidence. [AGGREGATOR] = useful heuristics, verify before relying on specifics.
