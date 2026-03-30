---
paths:
  - "docs/**"
---
- docs/STATUS.md es la fuente de verdad del estado del proyecto
- Antes de iniciar trabajo, leer docs/STATUS.md para contexto
- Al completar tarea, actualizar STATUS.md o notificar al Lorekeeper
- Decisiones tecnicas van a docs/DECISIONS.md (1 linea por entrada)
- NUNCA exceder 60 lineas en STATUS.md
- Formato de fechas: ISO 8601 (YYYY-MM-DD)

## Obligacion de SCRATCHPAD
- Todo agente DEBE append a docs/SCRATCHPAD.md con tag [agent-name] antes de cierre de sesion
- Formato: `## YYYY-MM-DD -- [descripcion breve]` luego subsecciones del template
- Si la sesion no produjo aprendizajes: escribir `[agent-name] No new patterns this session`

## Commit readiness
- El commit-gate hook ejecuta validate-docs.sh automaticamente antes de cada git commit
- Si hay errores [FAIL]: el commit se bloquea — corregir antes de reintentar
- Si hay warnings [WARN]: el commit procede con warning visible — evaluar si corregir
- No bypasear con --no-verify salvo instruccion explicita del usuario
- Modo estricto (pre-merge): `bash scripts/validate-docs.sh --strict`
- Lorekeeper es responsable de que TODAS las verificaciones pasen al cerrar bloque

## Lorekeeper Protocol (MANDATORY)

**Start:** (1) Read and ACT on SessionStart hook REQUIRED ACTIONS. (2) If SCRATCHPAD > 100 lines: graduate patterns. (3) If no entry today: create section.
**During:** (4) Update SCRATCHPAD with discoveries as they happen. (5) Run validate-docs before commits.
**Close:** (6) Verify SCRATCHPAD entry with [agent-name] tag. (7) Update CHANGELOG-DEV if significant changes. (8) Run validate-docs — 0 errors mandatory.
