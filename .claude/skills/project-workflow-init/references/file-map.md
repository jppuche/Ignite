# File Map — Template to Destination Reference

Reference for the Ignite skill (`/project-workflow-init`). Lists every template, its destination, and all placeholders.

---

## Placeholders

| Placeholder | Source | Default |
|-------------|--------|---------|
| `{{IDIOMA}}` | User input (Step 0.0) | `English` |
| `{{NOMBRE_PROYECTO}}` | User input / package.json `name` | (required) |
| `{{DESCRIPCION_CORTA}}` | User input / package.json `description` | "Proyecto {name}" |
| `{{STACK}}` | User input (summary) | (required) |
| `{{STACK_DETALLE}}` | User input (detailed) | Same as `{{STACK}}` |
| `{{STACK_BACKEND}}` | User input (backend portion) | Same as `{{STACK}}` |
| `{{STACK_FRONTEND}}` | User input (frontend portion) | Same as `{{STACK}}` |
| `{{CMD_DEV}}` | User input / package.json `scripts.dev` / stack inference | `N/A` |
| `{{CMD_BUILD}}` | User input / package.json `scripts.build` / stack inference | `N/A` |
| `{{CMD_TEST}}` | User input / package.json `scripts.test` / stack inference | `N/A` |
| `{{CMD_LINT}}` | User input / package.json `scripts.lint` / stack inference | `N/A` |
| `{{CMD_TYPECHECK}}` | User input / package.json `scripts.typecheck` / stack inference | `N/A` |
| `{{FECHA}}` | Auto (today YYYY-MM-DD) | — |
| `{{FASE_ACTUAL}}` | Auto (adapt to `{{IDIOMA}}`) | "Phase 0: Foundation" |
| `{{PENDIENTE}}` | Auto (adapt to `{{IDIOMA}}`) | "Phase 1: Technical Landscape" |
| `{{NOMBRE_BLOQUE}}` | Per-spec (not used in setup) | — |
| `{{CRITERIOS_ESPECIFICOS}}` | Per-spec (not used in setup) | — |
| `{{DOMAIN_BACKEND}}` | Stack profile (backend paths as markdown bullets) | Node/React defaults |
| `{{DOMAIN_FRONTEND}}` | Stack profile (frontend paths as markdown bullets) | Node/React defaults |
| `{{TEST_DOMAIN}}` | Stack profile (test patterns + config as markdown bullets) | Node/React defaults |
| `{{TEST_PATHS_FRONTMATTER}}` | Stack profile → YAML list format for rule frontmatter | `"**/*.test.*"`, `"**/*.spec.*"`, `"__tests__/**"` |
| `{{STYLING_PATHS_FRONTMATTER}}` | Stack profile → YAML list format for rule frontmatter | `"src/components/**"`, `"src/app/**"` |
| `{{CRITICAL_RULES_BACKEND}}` | Stack profile (security/quality rules as markdown bullets) | (per stack) |
| `{{CRITICAL_RULES_FRONTEND}}` | Stack profile (design/UX rules as markdown bullets) | (per stack) |
| `{{PACKAGE_MANAGER}}` | Lock file detection (Node only) | `npm` |
| `{{PACKAGE_MANAGER_INSTALL}}` | Derived from PACKAGE_MANAGER | `npm ci` |
| `{{CI_SETUP}}` | Stack profile (GitHub Actions setup steps as YAML) | Node.js setup |

Resolution: All `{{DOMAIN_*}}`, `{{TEST_*}}`, `{{STYLING_*}}`, `{{CRITICAL_RULES_*}}`, and `{{CI_SETUP}}` placeholders are resolved in Step 2.1 using the detected stack profile. See [ref-stack-profiles.md](ref-stack-profiles.md) for the complete mapping.

### Runtime Context (not template placeholders)

| Variable | Source | Purpose |
|----------|--------|---------|
| `USER_LEVEL` | Step 0.1 detection (profile / inferred / explicit) | Controls adaptive UX behavior throughout all steps. Values: `"guided"` or `"advanced"`. See [ref-adaptive-ux.md](ref-adaptive-ux.md). |

---

## Template Mapping

### Core (always generated)

| Template | Destination | Placeholders used | OW |
|----------|-------------|-------------------|----|
| `_workflow/templates/CLAUDE.template.md` | `./CLAUDE.md` | NOMBRE_PROYECTO, DESCRIPCION_CORTA, STACK_DETALLE, CMD_DEV, CMD_BUILD, CMD_TEST, CMD_LINT, CMD_TYPECHECK | -- |
| `_workflow/templates/docs/STATUS.template.md` | `./docs/STATUS.md` | NOMBRE_PROYECTO, FECHA, FASE_ACTUAL, PENDIENTE, STACK | A |
| `_workflow/templates/docs/DECISIONS.template.md` | `./docs/DECISIONS.md` | NOMBRE_PROYECTO, FECHA. Includes Candidate Ecosystem Catalog, Strategic Assessment, and Architecture Pivot Summary sections. | A |
| `_workflow/templates/docs/CHANGELOG-DEV.template.md` | `./docs/CHANGELOG-DEV.md` | NOMBRE_PROYECTO, FECHA | A |
| `_workflow/templates/docs/SCRATCHPAD.template.md` | `./docs/SCRATCHPAD.md` | NOMBRE_PROYECTO, FECHA | A |
| `_workflow/templates/docs/spec-template.md` | `./docs/specs/spec-template.md` | (copy as-is, placeholders are per-use). Includes "Candidate Tools" section for ecosystem catalog references. | B |
| `_workflow/templates/scripts/validate-docs.sh` | `./scripts/validate-docs.sh` | (copy as-is) | B |
| `_workflow/templates/scripts/validate-placeholders.sh` | `./scripts/validate-placeholders.sh` | (copy as-is) | B |
| `_workflow/templates/docs/LESSONS-LEARNED.template.md` | `./docs/LESSONS-LEARNED.md` | NOMBRE_PROYECTO, FECHA | A |
| `_workflow/templates/docs/README.template.md` | `./README.md` | NOMBRE_PROYECTO, DESCRIPCION_CORTA, STACK, FECHA | -- |

> Note: During Step 5.5, the skill's README.md is moved to `docs/ignite-reference.md` before the project README is generated from the template above. See [ref-finalization-details.md](ref-finalization-details.md).

### Agents

| Template | Destination | When included | Placeholders used | OW |
|----------|-------------|--------------|-------------------|----|
| `_workflow/templates/agents/Lorekeeper.template.md` | `./.claude/agents/Lorekeeper.md` | Always (Phase 0, during setup) | NOMBRE_PROYECTO | C |
| `_workflow/templates/agents/backend-worker.template.md` | `./.claude/agents/backend-worker.md` | Phase 5, if pre-selected | NOMBRE_PROYECTO, STACK_BACKEND, DOMAIN_BACKEND, CRITICAL_RULES_BACKEND | C |
| `_workflow/templates/agents/frontend-worker.template.md` | `./.claude/agents/frontend-worker.md` | Phase 5, if pre-selected | NOMBRE_PROYECTO, STACK_FRONTEND, DOMAIN_FRONTEND, CRITICAL_RULES_FRONTEND | C |
| `_workflow/templates/agents/Inquisidor.template.md` | `./.claude/agents/Inquisidor.md` | Phase 5, if pre-selected (opcion 1, 2 o custom) | NOMBRE_PROYECTO, TEST_DOMAIN | C |
| `_workflow/templates/agents/Sentinel.template.md` | `./.claude/agents/Sentinel.md` | Phase 5, if pre-selected (opcion 1, 2 o custom) | NOMBRE_PROYECTO | C |
| `_workflow/templates/agents/Sentinel-n8n.template.md` | `./.claude/agents/Sentinel.md` | Preset n8n: install manually for n8n projects (replaces generic Sentinel) | NOMBRE_PROYECTO | C |

> **Sentinel-n8n** is a stack-specific preset. Not auto-installed during Phase 5. User copies manually when working on n8n projects. Includes 9-phase pipeline, 11 dimensions, 6 sub-agent prompts, severity calibration, and web research protocol.

### Rules (always generated)

| Template | Destination | Placeholders used | OW |
|----------|-------------|-------------------|----|
| `_workflow/templates/rules/documentation.template.md` | `./.claude/rules/documentation.md` | (none) | C |
| `_workflow/templates/rules/testing.template.md` | `./.claude/rules/testing.md` | TEST_PATHS_FRONTMATTER | C |
| `_workflow/templates/rules/styling.template.md` | `./.claude/rules/styling.md` | STYLING_PATHS_FRONTMATTER | C (conditional: skip if no frontend UI) |
| `_workflow/templates/rules/compound-engineering.template.md` | `./.claude/rules/compound-engineering.md` | (none) | C |
| `_workflow/templates/rules/debugging.template.md` | `./.claude/rules/debugging.md` | (none) | C |

### Agent Coordination (if Agent Teams enabled)

| Template | Destination | Placeholders used | OW |
|----------|-------------|-------------------|----|
| `_workflow/templates/docs/AGENT-COORDINATION.template.md` | `./docs/AGENT-COORDINATION.md` | NOMBRE_PROYECTO | A |

### Lorekeeper Hooks (always generated)

| Source | Destination | OW |
|--------|-------------|----|
| `_workflow/templates/hooks/lorekeeper/lorekeeper-session-gate.py` | `./.claude/hooks/lorekeeper-session-gate.py` | B |
| `_workflow/templates/hooks/lorekeeper/lorekeeper-commit-gate.py` | `./.claude/hooks/lorekeeper-commit-gate.py` | B |
| `_workflow/templates/hooks/lorekeeper/lorekeeper-session-end.py` | `./.claude/hooks/lorekeeper-session-end.py` | B |

### Code Quality (always generated)

| Source | Destination | OW |
|--------|-------------|----|
| `_workflow/templates/hooks/code-quality-gate.py` | `./.claude/hooks/code-quality-gate.py` | B |

> Note: `code-quality-gate.py` is copy as-is (no placeholders). It reads `.claude/quality-gate.json` at runtime for stack-specific commands. The JSON config is generated inline during Step 3.5.

### Version Tracking (always generated)

| Source | Destination | OW |
|--------|-------------|----|
| (generated inline, Step 3.2 step 7) | `./.claude/ignite-version.json` | B |

### User Profile (generated by Step 0.1)

| Source | Destination | OW |
|--------|-------------|----|
| (generated inline, Step 0.1) | `./.claude/security/user-profile.json` | -- |

> Note: `user-profile.json` stores the detected user experience level (guided/advanced). Written once during first run, read on subsequent runs. Shared with Cerbero. See [ref-adaptive-ux.md](ref-adaptive-ux.md).

### CI/CD (always generated)

| Template | Destination | Placeholders used | OW |
|----------|-------------|-------------------|----|
| `_workflow/templates/ci/quality.template.yml` | `./.github/workflows/quality.yml` | CMD_TYPECHECK, CMD_LINT, CMD_TEST, CMD_BUILD, CI_SETUP | B |

> Note: Steps with commands resolved as "N/A" are omitted during generation.

### Cerbero Security (if enabled)

| Source | Destination | OW |
|--------|-------------|----|
| `_workflow/templates/skills/cerbero/` (entire directory) | `./.claude/skills/cerbero/` | B |
| `_workflow/templates/skills/cerbero/trusted-publishers.txt` | `./.claude/security/trusted-publishers.txt` | C |
| `_workflow/templates/skills/cerbero/hooks/validate-prompt.py` | `./.claude/hooks/validate-prompt.py` | B |
| `_workflow/templates/skills/cerbero/hooks/pre-tool-security.py` | `./.claude/hooks/pre-tool-security.py` | B |
| `_workflow/templates/skills/cerbero/hooks/mcp-audit.py` | `./.claude/hooks/mcp-audit.py` | B |
| `_workflow/templates/skills/cerbero/hooks/cerbero-scanner.py` | `./.claude/hooks/cerbero-scanner.py` | B |

---

## Overwrite Categories (OW)

Cuando /project-workflow-init se re-ejecuta en un proyecto existente, los archivos destino se manejan segun su categoria:

| Cat | Estrategia | Aplica a |
|-----|-----------|----------|
| A | Merge inteligente: agregar secciones faltantes, preservar contenido existente | Docs con datos del usuario |
| B | Reemplazar si difiere, skip si identico (sin datos del usuario) | Codigo ejecutable: hooks, scripts, skill files |
| C | Analizar diferencias y preguntar al usuario antes de modificar | Reglas y agentes (posiblemente personalizados) |
| -- | Logica especifica por archivo (ya implementada) | CLAUDE.md (ask), .gitignore (append), settings.local.json (merge), README.md (ask) |

Detalle de la logica en SKILL.md Step 3.0.

---

## Distribution Files (not generated to target project)

These files exist at the root of the Ignite package for distribution and discovery purposes. They are NOT copied into target projects during `/project-workflow-init` execution.

| File | Purpose |
|------|---------|
| `README.md` | Distribution README (moved to `docs/ignite-reference.md` during Step 5.5) |
| `LICENSE` | MIT License (hardcoded — no license type placeholder; replace manually if needed) |
| `CONTRIBUTING.md` | Contributor guide (architecture, how to add profiles/templates/hooks/rules) |
| `CHANGELOG.md` | Version history (semantic versioning) |
| `.claude-plugin/plugin.json` | Standard Claude Code plugin manifest (JSON) |

### Skill Reference Files

| File | Purpose |
|------|---------|
| `ref-adaptive-ux.md` | Adaptive UX layer: user level detection, phase behavior tables, preview specs, safe defaults, directive syntax |

---

## Directories Created

Always:
```
docs/
docs/specs/
scripts/
secrets/
.claude/agents/
.claude/rules/
.claude/hooks/
.github/workflows/
```

Always (if Guided/Advanced detection persists profile):
```
.claude/security/
```

If Cerbero:
```
.claude/skills/cerbero/
.claude/skills/cerbero/hooks/
.claude/security/  (already created by Step 0.1 if profile was persisted)
```

If Agent Teams:
```
(no extra directories, just .claude/settings.json)
```
