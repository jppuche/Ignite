#!/bin/bash
# validate-docs.sh — Verifica que la documentacion del proyecto este al dia
# Uso: bash scripts/validate-docs.sh [--strict]
# --strict: warnings tambien causan exit 1

set -euo pipefail

STRICT=false
[[ "${1:-}" == "--strict" ]] && STRICT=true

ERRORS=0
WARNINGS=0
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

err()  { echo "  [FAIL] $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  [WARN] $1"; WARNINGS=$((WARNINGS + 1)); }
ok()   { echo "  [ OK ] $1"; }

# --- Load config from .claude/lorekeeper-config.json (fall back to defaults) ---
CONFIG_FILE="$ROOT/.claude/lorekeeper-config.json"
if [ -f "$CONFIG_FILE" ]; then
  # Parse config using Python (already a dependency for hooks)
  PYTHON_CMD="${CLAUDE_CODE_PYTHON_CMD:-python3}"
  # Fallback to python if python3 not found (Windows)
  command -v "$PYTHON_CMD" >/dev/null 2>&1 || PYTHON_CMD="python"
  _CONFIG_VARS=$("$PYTHON_CMD" -c "
import json, sys
try:
    with open('$CONFIG_FILE') as f:
        c = json.load(f)
    docs = c.get('docs', {})
    # Scratchpad
    sp = docs.get('scratchpad', {})
    print(f'DOC_SCRATCHPAD=\"{sp.get(\"path\", \"docs/SCRATCHPAD.md\")}\"')
    print(f'DOC_SCRATCHPAD_MAX={sp.get(\"max_lines\", 150)}')
    print(f'DOC_SCRATCHPAD_GRAD={sp.get(\"graduation_threshold\", 100)}')
    # Changelog
    cl = docs.get('changelog', {})
    print(f'DOC_CHANGELOG=\"{cl.get(\"path\", \"docs/CHANGELOG-DEV.md\")}\"')
    # Status
    st = docs.get('status', {})
    print(f'DOC_STATUS=\"{st.get(\"path\", \"docs/STATUS.md\")}\"')
    print(f'DOC_STATUS_MAX={st.get(\"max_lines\", 60)}')
    # Decisions
    dc = docs.get('decisions', {})
    print(f'DOC_DECISIONS=\"{dc.get(\"path\", \"docs/DECISIONS.md\")}\"')
    # Lessons learned
    ll = docs.get('lessons_learned', {})
    print(f'DOC_LESSONS=\"{ll.get(\"path\", \"docs/LESSONS-LEARNED.md\")}\"')
    # CLAUDE.md
    cm = c.get('claude_md', {})
    print(f'DOC_CLAUDE_MD=\"{cm.get(\"path\", \"CLAUDE.md\")}\"')
    print(f'DOC_CLAUDE_MD_MAX={cm.get(\"max_lines\", 200)}')
    print(f'DOC_CLAUDE_MD_WARN={cm.get(\"warn_threshold\", 180)}')
except Exception:
    sys.exit(1)
" 2>/dev/null) && eval "$_CONFIG_VARS" || {
    # Python parsing failed — use defaults
    DOC_SCRATCHPAD="docs/SCRATCHPAD.md"
    DOC_SCRATCHPAD_MAX=150
    DOC_SCRATCHPAD_GRAD=100
    DOC_CHANGELOG="docs/CHANGELOG-DEV.md"
    DOC_STATUS="docs/STATUS.md"
    DOC_STATUS_MAX=60
    DOC_DECISIONS="docs/DECISIONS.md"
    DOC_LESSONS="docs/LESSONS-LEARNED.md"
    DOC_CLAUDE_MD="CLAUDE.md"
    DOC_CLAUDE_MD_MAX=200
    DOC_CLAUDE_MD_WARN=180
  }
else
  # No config file — use defaults (backwards compatible)
  DOC_SCRATCHPAD="docs/SCRATCHPAD.md"
  DOC_SCRATCHPAD_MAX=150
  DOC_SCRATCHPAD_GRAD=100
  DOC_CHANGELOG="docs/CHANGELOG-DEV.md"
  DOC_STATUS="docs/STATUS.md"
  DOC_STATUS_MAX=60
  DOC_DECISIONS="docs/DECISIONS.md"
  DOC_LESSONS="docs/LESSONS-LEARNED.md"
  DOC_CLAUDE_MD="CLAUDE.md"
  DOC_CLAUDE_MD_MAX=200
  DOC_CLAUDE_MD_WARN=180
fi

echo ""
echo "========================================"
echo "  Validacion de Docs"
echo "========================================"
echo ""

# --- 1. Existencia de archivos obligatorios ---
echo "1. Archivos obligatorios"
for f in "$DOC_CLAUDE_MD" "$DOC_STATUS" "$DOC_DECISIONS" "$DOC_CHANGELOG" "$DOC_SCRATCHPAD" "$DOC_LESSONS"; do
  if [ -f "$f" ]; then
    ok "$f existe"
  else
    err "$f NO ENCONTRADO"
  fi
done
echo ""

# --- 2. Limites de lineas ---
echo "2. Limites de lineas"
check_lines() {
  local file=$1 max=$2
  if [ ! -f "$file" ]; then return; fi
  local lines
  lines=$(wc -l < "$file" | tr -d ' ')
  if [ "$lines" -gt "$max" ]; then
    err "$file: $lines lineas (maximo $max)"
  else
    ok "$file: $lines/$max lineas"
  fi
}

check_lines "$DOC_CLAUDE_MD" "$DOC_CLAUDE_MD_MAX"
check_lines "$DOC_STATUS" "$DOC_STATUS_MAX"
check_lines "$DOC_SCRATCHPAD" "$DOC_SCRATCHPAD_MAX"
echo ""

# --- 3. Formato de DECISIONS.md ---
echo "3. Formato de DECISIONS.md"
if [ -f "$DOC_DECISIONS" ]; then
  # i18n: ES/EN/PT/FR table header variants
  if grep -q "| Fecha |" "$DOC_DECISIONS" || grep -q "| Date |" "$DOC_DECISIONS" || grep -q "| Data |" "$DOC_DECISIONS"; then
    ok "Header de tabla presente"
  else
    err "Falta header de tabla (| Fecha/Date/Data | Decision | ...)"
  fi
  # Contar decisiones (lineas que empiezan con | 20)
  DECISION_COUNT=$(grep -c "^| 20" "$DOC_DECISIONS" || true)
  ok "$DECISION_COUNT decisiones registradas"
fi
echo ""

# --- 4. Formato de CHANGELOG-DEV.md ---
echo "4. Formato de CHANGELOG-DEV.md"
if [ -f "$DOC_CHANGELOG" ]; then
  ENTRY_COUNT=$(grep -c "^## 20" "$DOC_CHANGELOG" || true)
  if [ "$ENTRY_COUNT" -gt 0 ]; then
    ok "$ENTRY_COUNT entradas en changelog"
  else
    err "Changelog vacio (sin entradas ## YYYY-MM-DD)"
  fi
fi
echo ""

# --- 5. Actualizaciones recientes ---
echo "5. Actualizaciones recientes"
TODAY=$(date +%Y-%m-%d)

check_recent() {
  local file=$1 label=$2
  if [ ! -f "$file" ]; then return; fi
  if grep -q "$TODAY" "$file"; then
    ok "$label: actualizado hoy ($TODAY)"
  else
    # Buscar la fecha mas reciente en el archivo
    LAST=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$file" | sort -r | head -1)
    warn "$label: ultima fecha $LAST (no hoy)"
  fi
}

check_recent "$DOC_STATUS" "STATUS"
check_recent "$DOC_CHANGELOG" "CHANGELOG-DEV"
check_recent "$DOC_SCRATCHPAD" "SCRATCHPAD"
echo ""

# --- 6. STATUS.md tiene fase actual ---
echo "6. Coherencia de STATUS.md"
if [ -f "$DOC_STATUS" ]; then
  # i18n: ES/EN/PT/FR variants
  if grep -qi "Fase actual\|Current phase\|Fase atual\|Phase actuelle\|## Fase\|## Phase" "$DOC_STATUS"; then
    ok "Tiene seccion de fase actual"
  else
    warn "No tiene indicador de fase actual"
  fi
  if grep -qi "Pendiente\|Pending\|Pendente\|En attente" "$DOC_STATUS"; then
    ok "Tiene seccion de pendientes"
  else
    warn "No tiene seccion de pendientes"
  fi
fi
echo ""

# --- 7. CLAUDE.md secciones obligatorias ---
echo "7. Secciones obligatorias en CLAUDE.md"
if [ -f "$DOC_CLAUDE_MD" ]; then
  REQUIRED_SECTIONS=("## Stack" "## Commands" "## Style" "## Rules" "## Architecture" "## Conventions" "## Learned Patterns")
  for section in "${REQUIRED_SECTIONS[@]}"; do
    if grep -q "$section" "$DOC_CLAUDE_MD"; then
      ok "CLAUDE.md tiene '$section'"
    else
      err "CLAUDE.md FALTA '$section'"
    fi
  done
fi
echo ""

# --- 8. SCRATCHPAD.md tiene sesion actual ---
echo "8. Sesion actual en SCRATCHPAD.md"
if [ -f "$DOC_SCRATCHPAD" ]; then
  if grep -q "$TODAY" "$DOC_SCRATCHPAD"; then
    ok "SCRATCHPAD tiene entrada de hoy ($TODAY)"
  else
    warn "SCRATCHPAD no tiene entrada de hoy"
  fi
fi
echo ""

# --- 9. Graduacion pendiente ---
echo "9. Graduacion pendiente"
if [ -f "$DOC_SCRATCHPAD" ]; then
  SCRATCHPAD_LINES=$(wc -l < "$DOC_SCRATCHPAD" | tr -d ' ')
  if [ "$SCRATCHPAD_LINES" -gt "$DOC_SCRATCHPAD_GRAD" ]; then
    warn "SCRATCHPAD.md tiene $SCRATCHPAD_LINES lineas (>$DOC_SCRATCHPAD_GRAD) — revisar candidatos de graduacion"
  else
    ok "SCRATCHPAD.md: $SCRATCHPAD_LINES lineas (< threshold de graduacion)"
  fi
fi
echo ""

# --- 10. Limite de CLAUDE.md ---
echo "10. Limite de CLAUDE.md"
if [ -f "$DOC_CLAUDE_MD" ]; then
  CLAUDE_LINES=$(wc -l < "$DOC_CLAUDE_MD" | tr -d ' ')
  if [ "$CLAUDE_LINES" -gt "$DOC_CLAUDE_MD_WARN" ]; then
    warn "CLAUDE.md tiene $CLAUDE_LINES lineas (>$DOC_CLAUDE_MD_WARN/$DOC_CLAUDE_MD_MAX) — podar con prueba de relevancia"
  else
    ok "CLAUDE.md: $CLAUDE_LINES lineas (margen OK)"
  fi
fi
echo ""

# --- 11. Estructura de LESSONS-LEARNED.md ---
echo "11. Estructura de LESSONS-LEARNED.md"
if [ -f "$DOC_LESSONS" ]; then
  # i18n: ES/EN/PT/FR variants
  if grep -qi "Template de incidente\|Incident template\|Template de incidente\|Modele d'incident" "$DOC_LESSONS"; then
    ok "LESSONS-LEARNED.md tiene template de incidente"
  else
    warn "LESSONS-LEARNED.md falta template de incidente"
  fi
else
  ok "LESSONS-LEARNED.md no existe aun (se creara con /ignite)"
fi
echo ""

# --- Resumen ---
echo "========================================"
echo "  Resumen: $ERRORS errores, $WARNINGS warnings"
echo "========================================"

if [ "$ERRORS" -gt 0 ]; then
  echo "  RESULTADO: FALLO — documentacion necesita atencion"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  if [ "$STRICT" = true ]; then
    echo "  RESULTADO: FALLO (modo strict) — docs parcialmente al dia"
    exit 1
  else
    echo "  RESULTADO: PARCIAL — docs parcialmente al dia"
    exit 0
  fi
else
  echo "  RESULTADO: OK — documentacion al dia"
  exit 0
fi
