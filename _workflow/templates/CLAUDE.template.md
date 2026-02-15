# {{NOMBRE_PROYECTO}}

{{DESCRIPCION_CORTA}}

## Stack

{{STACK_DETALLE}}

## Project state

@docs/STATUS.md

## Style

<!-- Definir: naming conventions (archivos, variables, componentes), formato codigo, design tokens si frontend -->
<!-- Ejemplos:
- kebab-case archivos, camelCase variables/funciones, PascalCase componentes
- Color acento: #XXXXXX
- Font: ...
- Dark mode obligatorio / opcional / no aplica
-->

## Commands

<!-- Solo los que Claude no puede adivinar. Formato: - Nombre: `comando` -->

- Dev: `{{CMD_DEV}}`
- Build: `{{CMD_BUILD}}`
- Test: `{{CMD_TEST}}`
- Lint: `{{CMD_LINT}}`
- Typecheck: `{{CMD_TYPECHECK}}`
- Docs check: `bash scripts/validate-docs.sh`

## Skills (CONSULTAR ANTES de cada tarea)

<!-- Listar skills instaladas con trigger de uso -->
<!-- Formato: - `skill-name` -- Cuando usar -->
<!-- Ejemplo: - `vercel-react-best-practices` -- Crear/refactorizar componentes React o paginas Next.js -->
<!-- Mapeo por agente y bloque: @docs/AGENT-COORDINATION.md seccion 13 (se llena en Phase 5) -->

## Rules

- **ANTES de cada tarea (planificar, implementar, revisar): revisar que skills aplican a la tarea** (ver seccion Skills arriba)
- Usar skills como conocimiento especializado -- consultar cuando el trigger matchea, no usar "por si acaso"
- **SIEMPRE buscar en el codebase antes de crear algo nuevo** -- reimplementar es el error mas comun de agentes
- Typecheck y lint despues de cambios de codigo
- Tests individuales, no el suite completo (excepto en validacion de bloque)
- Validacion visual para cambios de UI (screenshots / dev tools) -- si aplica al proyecto
- Scratchpad: leer docs/SCRATCHPAD.md al inicio, append con tag [agente] al cierre
- **Persistir descubrimientos valiosos a SCRATCHPAD.md inmediatamente** -- no esperar al cierre de sesion; insights solo en contexto conversacional se pierden con compact/clear
- Post-mortems de incidentes van a docs/LESSONS-LEARNED.md (1 seccion por incidente, append-only)
- Docs check: ejecutar `bash scripts/validate-docs.sh` al cierre de cada sesion/bloque
- Lorekeeper hooks: session-start context, commit-gate validation, session-end checkpoint — actuar sobre pending items mostrados al inicio

## Architecture

<!-- Decisiones arquitectonicas que no se infieren del codigo -->
<!-- Documento completo: @docs/architecture.md (si existe) -->
<!-- Specs de bloques: @docs/specs/ -->

## Conventions

- Commits: tipo(scope): descripcion (ej: feat(auth): add login flow)
- Branches: feature/bloque-N-nombre
- Specs de bloques en docs/specs/

## Hooks

Configurados en .claude/settings.local.json (no commitear).

- `lorekeeper-session-gate.py` (SessionStart) — inyecta contexto + pending items de sesion anterior + version check (tambien post-compresion)
- `lorekeeper-commit-gate.py` (PreToolUse:Bash) — bloquea git commit si docs validation falla
- `lorekeeper-session-end.py` (SessionEnd) — checkpoint de docs + pending items + graduation candidates para siguiente sesion

## Scratchpad

@docs/SCRATCHPAD.md -- leer al inicio de cada sesion, append al cierre

## Learned Patterns (compound engineering -- actualizar al cerrar cada bloque)

<!-- Se llena con patrones, gotchas y convenciones descubiertos -->
<!-- "Anytime Claude does something incorrectly, add it here" -- Boris Cherny -->
<!-- Formato: -->
<!-- ### Block/Phase N: Name -->
<!-- - patron o error descubierto -- contexto minimo necesario -->
