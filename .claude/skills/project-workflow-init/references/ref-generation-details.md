# Generation Details

## 2.5 Pre-generation Preview (dry-run)

After Step 2 completes (all 28 placeholders resolved, all decisions captured), display a preview before writing any files. This is the dry-run feature — the user sees exactly what will be generated and must confirm.

### 2.5.1 Build file manifest

Construct the complete list of files that will be generated, using [file-map.md](file-map.md) as the source of truth.

```
PREVIEW_MANIFEST = []

For each entry in file-map.md Template Mapping tables:
  destination = resolved destination path
  source      = template path
  category    = OW column value

  # Check generation conditions
  will_generate = true  (default)

  If file is styling.md AND STYLING_APPLICABLE == "No":
    will_generate = false

  If file is in "Cerbero Security" section AND Cerbero NOT enabled:
    will_generate = false

  If file is AGENT-COORDINATION.md AND Agent Teams NOT enabled:
    will_generate = false

  If file is backend-worker/frontend-worker AND not pre-selected:
    will_generate = false

  If will_generate:
    entry = { destination, source, category }

    # If re-run: include overwrite analysis
    If STATE != "fresh" AND EXISTING_FILES[destination].exists:
      Run category-specific analysis (3.0.1 / 3.0.2 / 3.0.3) for this file.
      entry.overwrite_action = ANALYSIS[destination].action
      entry.overwrite_icon = action_icon mapping (skip→[=], merge→[+], replace→[^], skip_customized→[~], ask→[?])
      entry.overwrite_details = ANALYSIS[destination].details

    PREVIEW_MANIFEST.append(entry)
```

Count files: `preview_count = len(PREVIEW_MANIFEST)`

### 2.5.2 Resolve key file contents (in memory only)

Resolve ONLY these files fully in memory. Do NOT write to disk.

1. **CLAUDE.md** — the most important generated file. Resolve from `CLAUDE.template.md` applying all placeholders and Step 2 decisions. Store as `PREVIEW_CONTENT["CLAUDE.md"]`.

2. **quality-gate.json** — shows the user their detected commands. Generate the JSON content with resolved `CMD_TYPECHECK`, `CMD_LINT`, `CMD_TEST`. Store as `PREVIEW_CONTENT["quality-gate.json"]`.

Do NOT resolve all templates — context economy. These 2 files are sufficient to demonstrate correct placeholder resolution and let the user verify their most important outputs.

### 2.5.3 Display preview

Check `USER_LEVEL` and display the appropriate format. Both formats are fully specified in [ref-adaptive-ux.md](ref-adaptive-ux.md) (Preview Specifications).

**Advanced:** File tree grouped by category (Project root, Documentation, Agents, Rules, Hooks, Config, CI/CD, Scripts) with file descriptions. Then resolved placeholder table (all 28). Then full CLAUDE.md preview content.

If re-run: append overwrite icons next to each existing file and include legend.

**Guided:** Simplified summary grouped by purpose (Documentation, AI Agents, Quality Rules, Automation, CI/CD Pipeline, Project Memory) with counts and plain-language descriptions. Show project name, stack, and key commands only.

### 2.5.4 Confirmation

Use AskUserQuestion. Adapt prompt to `USER_LEVEL` and `{{IDIOMA}}`. Options specified in [ref-adaptive-ux.md](ref-adaptive-ux.md) (Confirmation Options).

**Action handling:**

```
If user selects "Generate" / "Yes, set it up":
  Proceed to Step 3.
  If STATE != "fresh": ANALYSIS map is already populated from 2.5.1 — Step 3.0 can
  skip re-analysis and use existing ANALYSIS directly.

If user selects "Show me more detail" (Guided only):
  Set USER_LEVEL = "advanced" (runtime only — do NOT update persisted profile).
  Re-display preview in Advanced format (2.5.3).
  Show Advanced confirmation options.

If user selects "Adjust configuration" / "Let me change something":
  Increment LOOPBACK_COUNT.
  If LOOPBACK_COUNT > 2:
    Display (adapt to {{IDIOMA}}):
      "You've adjusted configuration multiple times.
       Consider running /project-workflow-init fresh to start over."
    Proceed with current configuration (do not block).
  Else:
    Return to Step 2.2 (re-ask questions per USER_LEVEL).
    After re-configuration, re-execute Step 2.5 (re-build manifest, re-resolve content).

If user selects "Cancel":
  Display (adapt to {{IDIOMA}}):
    "Setup cancelled. No files were created.
     Run /project-workflow-init again when ready."
  STOP EXECUTION. Do NOT proceed to Step 3 or Step 5.
  No files are written, no summary is displayed.
```

---

## 3.0 Pre-generation analysis (overwrite protection)

If STATE == "fresh": skip entirely to 3.1.

For each file in EXISTING_FILES where exists == true, perform category-specific analysis. Store results in ANALYSIS map.

### 3.0.1 Category A analysis (docs with user data)

#### Language-aware section detection

Merge detection must match documents generated in any `{{IDIOMA}}`.
Use dual-pattern matching: section found if EITHER Spanish OR English variant matches (case-insensitive).

| Spanish (base) | English | Used in |
|----------------|---------|---------|
| "Fase actual" | "Current phase" | STATUS.md |
| "Completado" | "Completed" | STATUS.md |
| "Pendiente" | "Pending" | STATUS.md |
| "Bloqueantes" | "Blockers" | STATUS.md |
| "Notas" | "Notes" | STATUS.md |
| "Reglas" | "Rules" | SCRATCHPAD.md |
| "Formato por sesion" | "Session format" | SCRATCHPAD.md |
| "Template de incidente" | "Incident template" | LESSONS-LEARNED.md |
| "Fecha \| Decision" | "Date \| Decision" | DECISIONS.md |
| "Modelo de Orquestacion" | "Orchestration Model" | AGENT-COORDINATION.md |
| "Tipos de Ejecucion" | "Execution Types" | AGENT-COORDINATION.md |
| "Reglas de Coordinacion" | "Coordination Rules" | AGENT-COORDINATION.md |
| "Protocolo de Comunicacion" | "Communication Protocol" | AGENT-COORDINATION.md |
| "File Ownership Estricto" | "Strict File Ownership" | AGENT-COORDINATION.md |
| "Orden de Spawn" | "Spawn Order" | AGENT-COORDINATION.md |
| "Secuencia de Shutdown" | "Shutdown Sequence" | AGENT-COORDINATION.md |
| "Seguridad OWASP MCP Top 10" | "OWASP MCP Top 10 Security" | AGENT-COORDINATION.md |
| "Evaluacion Sandboxed" | "Sandboxed Evaluation" | AGENT-COORDINATION.md |
| "Best Practices de Anthropic" | "Anthropic Best Practices" | AGENT-COORDINATION.md |
| "Limitaciones Conocidas" | "Known Limitations" | AGENT-COORDINATION.md |
| "Checklist Pre-Bloque" | "Pre-Block Checklist" | AGENT-COORDINATION.md |
| "Mapeo de Skills por Agente y Bloque" | "Skills-to-Agent Block Mapping" | AGENT-COORDINATION.md |

Pattern: for each required section, search the existing file for EITHER variant (case-insensitive substring match). If either matches, the section is considered present.

For each Category A file that exists:

```
Read existing file content.
Read corresponding template (with placeholders resolved from Step 2).

ANALYSIS[file] = { action: null, details: [] }

Case docs/STATUS.md:
  Required sections (match either variant, case-insensitive):
    "Fase actual" / "Current phase"
    "Completado" / "Completed"
    "Pendiente" / "Pending"
    "Bloqueantes" / "Blockers"
    "Notas" / "Notes"
  For each required section:
    If NEITHER variant found in existing file (case-insensitive):
      details.append("Falta seccion '{section}' -> se agregara con default del template")
      action = "merge"
  If line count > 60:
    details.append("Excede 60 lineas ({count}) -> se notificara (no se trunca)")
  If no issues: action = "skip", details = ["Estructura correcta -> sin cambios"]

Case docs/DECISIONS.md:
  Check for table header: "| Fecha |" OR "| Date |" (case-insensitive)
  If missing: action = "merge", details = ["Falta header de tabla -> se agregara"]
  Else: action = "skip", details = ["Estructura correcta -> sin cambios"]
  Nota: NUNCA borrar filas existentes.

Case docs/CHANGELOG-DEV.md:
  Check for entries with format "## YYYY-MM-DD -- description"
  If no entries match: action = "merge", details = ["Sin formato correcto -> se agregara header"]
  Else: action = "skip", details = ["{count} entradas existentes -> sin cambios"]

Case docs/SCRATCHPAD.md:
  Required sections (match either variant, case-insensitive):
    "Reglas" / "Rules"
    "Formato por sesion" / "Session format"
  For each missing: action = "merge", details.append("Falta seccion '{section}'")
  If line count > 150: details.append("Excede 150 lineas ({count}) -> se notificara")
  If all present and under limit: action = "skip"

Case docs/LESSONS-LEARNED.md:
  Required sections (match either variant, case-insensitive):
    "Template de incidente" / "Incident template"
  If NEITHER variant found as heading/comment in existing file:
    action = "merge", details = ["Falta template de incidente -> se agregara"]
  Else: action = "skip", details = ["Estructura correcta -> sin cambios"]

Case docs/AGENT-COORDINATION.md:
  13 major sections (match either variant, case-insensitive — see table above):
    "Modelo de Orquestacion" / "Orchestration Model",
    "Tipos de Ejecucion" / "Execution Types",
    "Reglas de Coordinacion" / "Coordination Rules",
    "Protocolo de Comunicacion" / "Communication Protocol",
    "File Ownership Estricto" / "Strict File Ownership",
    "Orden de Spawn" / "Spawn Order",
    "Secuencia de Shutdown" / "Shutdown Sequence",
    "Seguridad OWASP MCP Top 10" / "OWASP MCP Top 10 Security",
    "Evaluacion Sandboxed" / "Sandboxed Evaluation",
    "Best Practices de Anthropic" / "Anthropic Best Practices",
    "Limitaciones Conocidas" / "Known Limitations",
    "Checklist Pre-Bloque" / "Pre-Block Checklist",
    "Mapeo de Skills por Agente y Bloque" / "Skills-to-Agent Block Mapping"
  For each missing heading: action = "merge", details.append("Falta seccion '{section}'")
  If all present: action = "skip", details = ["13/13 secciones presentes -> sin cambios"]
```

### 3.0.2 Category B analysis (executable code)

For each Category B file that exists (including `.claude/ignite-version.json`):

```
Read existing file content.
Read corresponding template source content (for inline-generated files like ignite-version.json, generate expected content first).

Compare content (strip trailing whitespace, normalize CRLF -> LF):
  If identical: action = "skip", details = ["Identico al template -> sin cambios"]
  If different: action = "replace", details = ["Version desactualizada -> se reemplazara"]
```

### 3.0.3 Category C analysis (rules + agents)

For each Category C file that exists:

```
Read existing file content.
Read corresponding template (with placeholders resolved).

Extract section headings (## / ###) from both files.
existing_sections = headings in existing file
template_sections = headings in template

missing_sections  = template_sections - existing_sections
extra_sections    = existing_sections - template_sections

If YAML frontmatter differs from template: treat as customized.

If missing_sections is empty AND extra_sections is empty:
  If content identical (normalized):
    action = "skip", details = ["Identico al template -> sin cambios"]
  Else:
    action = "skip_customized"
    details = ["Personalizado por el usuario (mismas secciones, contenido diferente) -> se respeta"]

Elif missing_sections is not empty:
  action = "ask"
  details = ["Falta(n) seccion(es): {missing_sections} -> preguntar al usuario"]

Elif extra_sections is not empty AND missing_sections is empty:
  action = "skip_customized"
  details = ["Secciones adicionales del usuario. Template completo -> sin cambios"]
```

### 3.0.4 Special files (Category --)

No additional analysis needed — use existing logic:
- `CLAUDE.md`: handled in 3.1 step 1 (ask before overwriting)
- `.gitignore`: handled in Step 5.3 (append-only)
- `settings.local.json`: handled in 3.2 (merge hooks without duplicating)

### 3.0.5 Display report

Build visual report grouped by category. Only show files that exist. Adapt headings and legend to `{{IDIOMA}}`.

```
Display:

"--- Existing Files Analysis ({existing_count} of {total_count}) ---

 Documents (smart merge — your data is preserved):
   docs/STATUS.md ............. {action_icon} {details}
   docs/DECISIONS.md .......... {action_icon} {details}
   docs/CHANGELOG-DEV.md ...... {action_icon} {details}
   docs/SCRATCHPAD.md ......... {action_icon} {details}
   [if exists] docs/AGENT-COORDINATION.md .. {action_icon} {details}

 Code (replace if outdated — no user data in these):
   .claude/hooks/lorekeeper-*.py ... {action_icon} {details}
   scripts/validate-*.sh .......... {action_icon} {details}
   [if exists] docs/specs/spec-template.md .. {action_icon} {details}
   [if Cerbero] .claude/hooks/cerbero-*.py . {action_icon} {details}

 Rules & Agents (your customizations are respected):
   .claude/rules/*.md ........... {action_icon} {details}
   .claude/agents/Lorekeeper.md .. {action_icon} {details}
   [if Cerbero] trusted-publishers.txt .. {action_icon} {details}

 Special handling:
   CLAUDE.md ............... will ask before any changes
   .gitignore .............. append-only (adds missing entries)
   settings.local.json ..... merge hooks without duplicating

 Legend: [=] no changes  [+] sections added  [^] updated  [~] customized  [?] needs your input"
```

Where `action_icon` maps to: skip→`[=]`, merge→`[+]`, replace→`[^]`, skip_customized→`[~]`, ask→`[?]`.

### 3.0.6 User confirmation

**Step 1 — Category C decisions** (only if any file has action == "ask"):

For each file with action == "ask", use AskUserQuestion:

```
"{file} tiene secciones faltantes: {missing_sections}.
 Esto puede ser intencional o porque el template se actualizo."
  1. Agregar las secciones faltantes (recomendado)
  2. Dejar como esta (el usuario lo personalizo)
```

Update ANALYSIS based on response:
- Option 1: change action to "merge"
- Option 2: change action to "skip_customized"

**Step 2 — Global confirmation**:

If ALL files have action == "skip" or "skip_customized": display "Todo esta actualizado — sin cambios necesarios." and skip confirmation.

Otherwise, use AskUserQuestion:

```
"Se aplicaran los cambios mostrados arriba. Continuar?"
  1. Si, aplicar todos los cambios
  2. No, cancelar (no se modifica ningun archivo)
```

If user chooses option 2: set all actions to "skip" and proceed to Step 5 (no files generated/modified).

---

## 3.1 Core files (respecting overwrite analysis)

Before writing each file, check ANALYSIS from Step 3.0:
- If file does NOT exist: write normally (fresh install path).
- If ANALYSIS[file].action == "skip": do not write. Log: "{file} sin cambios."
- If ANALYSIS[file].action == "merge": execute merge logic below.
- If ANALYSIS[file].action == "replace": overwrite entirely.

1. Generate `./CLAUDE.md` (Category --; existing ask-before-overwrite logic):
   a. **Primero**, leer `_workflow/guides/Referencia-edicion-CLAUDE.md` — aplicar sus criterios durante toda la generacion (< 200 lineas, solo lo que Claude no puede inferir, estilo imperativo directo, sin duplicacion).
   b. Leer `_workflow/templates/CLAUDE.template.md` → reemplazar placeholders.
   c. Completar seccion `## Style` basado en el stack (inferir convenciones del framework).
   d. Completar seccion `## Architecture` si el stack sugiere estructura.
   e. Si Cerbero habilitado: agregar entrada Cerbero (skill de seguridad) a seccion `## Skills`.
   f. Antes de escribir, verificar contra el checklist de la guia (seccion 8): conteo de lineas, prueba de relevancia, sin credenciales, sin duplicacion.
   g. Escribir `./CLAUDE.md`.

2. `./docs/STATUS.md` (Category A):
   - If not exists: read template → replace placeholders → write.
   - If action == "skip": no changes.
   - If action == "merge":
     ```
     Read existing content.
     For each missing section identified in 3.0.1:
       Find section block in resolved template (heading + content until next heading).
       Append section block to end of existing file.
     Update "Ultima actualizacion" date to today if present.
     Write merged result.
     ```

3. `./docs/DECISIONS.md` (Category A):
   - If not exists: read template → replace placeholders → write.
   - If action == "skip": no changes.
   - If action == "merge":
     ```
     Read existing content.
     If table header missing:
       Prepend: H1 heading + append-only note + table header row + separator row.
       Append all existing content below (preserve all rows).
     Write merged result. NEVER delete existing rows.
     ```

4. `./docs/CHANGELOG-DEV.md` (Category A):
   - If not exists: read template → replace placeholders → write.
   - If action == "skip": no changes.
   - If action == "merge":
     ```
     Read existing content.
     If H1 heading or format instruction missing:
       Prepend: H1 heading + append-only note + format instruction.
       Append all existing entries below.
     Write merged result.
     ```

5. `./docs/SCRATCHPAD.md` (Category A):
   - If not exists: read template → replace placeholders → write.
   - If action == "skip": no changes.
   - If action == "merge":
     ```
     Read existing content.
     For each missing section ("Reglas" or "Formato por sesion"):
       Find section in resolved template.
       Insert AFTER the H1 heading and BEFORE any session entries (## YYYY-MM-DD).
     Preserve all existing session entries untouched.
     Write merged result.
     ```

6. `./docs/specs/spec-template.md` (Category B):
   - If not exists: copy as-is.
   - If action == "skip": no changes.
   - If action == "replace": overwrite.

7. `./scripts/validate-docs.sh` (Category B):
   - If not exists: copy as-is.
   - If action == "skip": no changes.
   - If action == "replace": overwrite. Log: "Script actualizado."

8. `./scripts/validate-placeholders.sh` (Category B):
   - If not exists: copy as-is.
   - If action == "skip": no changes.
   - If action == "replace": overwrite. Log: "Script actualizado."

9. `./docs/LESSONS-LEARNED.md` (Category A):
   - If not exists: read template, replace placeholders, write.
   - If action == "skip": no changes.
   - If action == "merge":
     Read existing content.
     Check for "Template de incidente" section heading or comment.
     If missing: prepend header + template section. Preserve all existing incidents.
     Write merged result. NEVER delete existing entries.

---

## 3.0.7 Mid-way project integration (only if PROJECT_MODE == "mid-way")

Skip this section entirely if `PROJECT_MODE == "fresh"` or `INTEGRATION_LEVEL == "audit"`.

### CLAUDE.md section-level merge

If `SKIP_CLAUDE_MERGE == true` (workflow_only mode): treat existing CLAUDE.md as untouchable. Only generate if it doesn't exist.

If `SKIP_CLAUDE_MERGE == false` (full integration):

```
If CLAUDE.md exists:
  Read existing CLAUDE.md.
  Read template CLAUDE.md (resolved from CLAUDE.template.md with Step 2 values).

  For each section in template (## Stack, ## Commands, ## Skills, etc.):
    existing_section = find matching section in existing CLAUDE.md (case-insensitive heading match)

    If existing_section exists AND has >3 lines of content:
      KEEP existing content (user has meaningful data here).
      If template section has subsections not in existing: APPEND missing subsections only.

    If existing_section exists AND has <=3 lines:
      REPLACE with template version (likely placeholder/empty).

    If existing_section does NOT exist:
      APPEND template section at the appropriate position.

  Preserve any sections in existing CLAUDE.md that are NOT in the template
  (user-added custom sections). Place them after the standard sections.

  Apply CONTEXT_SCAN data to enrich generated sections:
    - ## Style: populate with CONTEXT_SCAN.conventions (variable naming, file naming)
    - ## Commands: cross-reference with detected package.json scripts
    - ## Architecture: reference CONTEXT_SCAN.existing_architecture files if found
    - ## Conventions > Commits: use CONTEXT_SCAN.commit_style if detected

  Verify final CLAUDE.md < 200 lines. If over, compress by removing comments and examples.
  Write merged result.
Else:
  Generate from template normally (same as fresh install).
```

### CI/CD integration

If `SKIP_CICD_MERGE == true`: skip CI/CD generation entirely (Step 3.5). Log: "CI/CD generation skipped (workflow_only mode)."

If `SKIP_CICD_MERGE == false` AND `CONTEXT_SCAN.existing_ci.type != "none"`:

```
For GitHub Actions specifically (CONTEXT_SCAN.existing_ci.type == "github_actions"):
  Read existing workflow files.
  Read generated quality.yml content.

  Strategy: ADD a new workflow file, don't modify existing ones.
    Write to: .github/workflows/workflow-quality.yml (prefixed to avoid conflict)
    Add comment header: "# Generated by Ignite — quality gates for workflow methodology"

  If existing workflows already have equivalent steps (typecheck, lint, test):
    Log to user: "Existing CI already includes quality checks.
     Generated workflow-quality.yml may duplicate some steps.
     Review and merge manually, or delete if existing CI is sufficient."

For non-GitHub CI (gitlab, jenkins, etc.):
  Do NOT generate .github/workflows/quality.yml.
  Instead, display recommendations:
    "Existing {ci_type} CI detected. Recommended quality gate steps:
     - Typecheck: {CMD_TYPECHECK}
     - Lint: {CMD_LINT}
     - Test: {CMD_TEST}
     - Build: {CMD_BUILD}
     Add these to your existing CI configuration."
```

### Existing docs integration

If `CONTEXT_SCAN.existing_docs.count > 0`:

```
For each Ignite doc that would be generated (STATUS.md, DECISIONS.md, etc.):
  Check if a functional equivalent exists in the project's doc structure:
    - STATUS.md equivalents: ROADMAP.md, TODO.md, PROJECT_STATUS.md
    - DECISIONS.md equivalents: ADR/, ARCHITECTURE_DECISIONS.md
    - CHANGELOG-DEV.md equivalents: CHANGELOG.md (at root)

  If equivalent found:
    Log: "Equivalent found: {existing_file} ↔ {template_file}"
    Generate the template version anyway (the workflow depends on specific formats).
    Add cross-reference note at top of generated file:
      "Note: This project also has {existing_file} — consider consolidating."

  If no equivalent: generate normally.
```
