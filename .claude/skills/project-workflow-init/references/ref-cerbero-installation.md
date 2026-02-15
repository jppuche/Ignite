# Step 4: Security (if Cerbero enabled)

Only execute if user answered Yes to Cerbero in section 2.2 (Q3: Security).

## 4.0 Protection level briefing

> **Adaptive:** If `USER_LEVEL == "guided"`, show simplified 4-line summary. If `USER_LEVEL == "advanced"`, show full briefing below. See [ref-adaptive-ux.md](ref-adaptive-ux.md) (Phase Behavior Table).

**Guided briefing** (adapt to `{{IDIOMA}}`):

```
Installing security framework (Cerbero):
  - Scans for dangerous commands before execution
  - Validates prompts for injection attempts
  - Audits external tool usage
  - Screens new tools before installation

  Coverage: ~70-80% of known attack vectors.
```

**Advanced briefing** (full, adapt to `{{IDIOMA}}`):

```
=== CERBERO — NIVEL DE PROTECCION ===

QUE PROTEGE:
  - Prompt injection directa en prompts (hook: validate-prompt.py)
  - Comandos destructivos: rm -rf, fork bombs, reverse shells (hook: pre-tool-security.py)
  - Descargas sospechosas: curl -o, wget -O [WARNING] (hook: pre-tool-security.py)
  - Tool poisoning: schemas maliciosos, inyeccion en descripciones (scanner + evaluacion)
  - Rug pulls: cambios silenciosos en herramientas MCP (baseline SHA256)
  - Skills maliciosas: Base64, HTML, zero-width, CSS invisible (scanner externo)
  - Supply chain: CVEs, typosquat, firmas invalidas (npm audit)
  - Telemetria: log de invocaciones MCP (hook: mcp-audit.py)

  Cobertura estimada: ~70-80% de vectores conocidos (OWASP MCP Top 10).

QUE NO PROTEGE:
  - Indirect prompt injection via contenido procesado (paginas, archivos)
  - Exfiltracion por canales laterales (timing, error messages)
  - Ataques de red (MITM en conexiones MCP remotas)
  - Vulnerabilidades en Claude Code / runtime Node.js
  - MCPs que cambian comportamiento segun input sin cambiar tools
  - Zero-days en dependencias sin CVE publicado

RECOMENDACIONES:
  - claude --sandbox para HIGH/CRITICAL (obligatorio para CRITICAL)
  - mcp-scan (Snyk) para deteccion adicional
  - Revisar .claude/settings.local.json periodicamente
  - /cerbero audit mensualmente
  - Monitoreo de red (GlassWire/Little Snitch) para procesos MCP
```

Continue to 4.1.

## 4.1 Install Cerbero skill (Category B)

Copy entire `_workflow/templates/skills/cerbero/` directory to `./.claude/skills/cerbero/`:
- SKILL.md
- op-evaluate-mcp.md, op-evaluate-skill.md, op-verify-existing.md, op-full-audit.md
- setup-guide.md
- trusted-publishers.txt
- hooks/ (validate-prompt.py, pre-tool-security.py, mcp-audit.py)

For each file in the skill directory:
- If not exists at destination: copy.
- If exists: compare content (normalized). If identical → skip. If different → replace. Log action.

## 4.1b User profile check (fallback)

If `.claude/security/user-profile.json` does NOT exist at this point (Ignite was not used for setup, or Step 0.1 was skipped), initialize the user profile here:

1. Check if `.claude/security/` directory exists. Create if needed (`mkdir -p .claude/security`).
2. Run the detection cascade from [ref-adaptive-ux.md](ref-adaptive-ux.md) (Detection Cascade) — read profile → infer → ask → persist.
3. This ensures the profile exists before any Cerbero operation that references `USER_LEVEL`.

If the profile already exists (set by Step 0.1): skip this step entirely.

## 4.2 Security directory

```
mkdir -p .claude/security
```

`trusted-publishers.txt` → `./.claude/security/trusted-publishers.txt` (Category C):
- If not exists: copy.
- If exists: compare with template using **set-based comparison** (one publisher per line, strip whitespace, ignore empty lines).
  - Let `template_set` = entries in template. Let `existing_set` = entries in existing file.
  - If `existing_set` == `template_set`: skip (identical).
  - If `existing_set` is a strict superset of `template_set` (user added entries beyond template): preserve user's version. Log: "trusted-publishers.txt tiene {N} entradas adicionales del usuario -> se preserva."
  - If `template_set` has entries NOT in `existing_set`: use AskUserQuestion:
    ```
    "El template de trusted-publishers.txt tiene publishers que no estan en tu lista: {missing}. Agregar?"
      1. Si, agregar los faltantes (recomendado)
      2. No, mantener mi version
    ```
  - If `existing_set` has entries NOT in `template_set` AND `template_set` is NOT a subset of `existing_set`: use AskUserQuestion:
    ```
    "Tu trusted-publishers.txt tiene publishers que ya no estan en el template: {extra}.
     El template actual solo incluye: {template_list}.
     El criterio de inclusion se ha vuelto mas estricto (ver setup-guide.md A.5)."
      1. Adoptar la lista del template (recomendado — verificar cada publisher removido con Cerbero)
      2. Mantener mi version actual
    ```

## 4.3 Install hooks (Category B)

Copy hook scripts to `./.claude/hooks/`:
- `validate-prompt.py`
- `pre-tool-security.py`
- `mcp-audit.py`
- `cerbero-scanner.py`

For each hook:
- If not exists: copy.
- If exists: compare content (normalized). If identical → skip. If different → replace. Log action.

> **Note:** `cerbero-scanner.py` is NOT registered as an automatic hook.
> It is a Tier 0 external scanner invoked manually by Sentinel or `/cerbero audit`.
> Located in `.claude/hooks/` for co-location with other security scripts, not for auto-execution.

## 4.4 Configure Cerbero hooks in settings

Read existing `.claude/settings.local.json` (created in Step 3.2 with Lorekeeper hooks).

Merge Cerbero hooks into the existing `hooks` object:

- Add `UserPromptSubmit` array: validate-prompt.py entry (Cerbero validates every prompt). Nota: `UserPromptSubmit` no soporta matchers — omitir `matcher`.
- Append to `PreToolUse` array: pre-tool-security.py (matcher: Bash) and mcp-audit.py (matcher: mcp__*)

Result after merge (paths relativos, PYTHON_CMD from Step 1.0):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-session-gate.py" }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/validate-prompt.py" }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-commit-gate.py" }]
      },
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/pre-tool-security.py" }]
      },
      {
        "matcher": "mcp__*",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/mcp-audit.py" }]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "{PYTHON_CMD} .claude/hooks/lorekeeper-session-end.py" }]
      }
    ]
  }
}
```

Where `{PYTHON_CMD}` = `python` (win32) or `python3` (darwin/linux), same as Step 3.2.

## 4.5 Update CLAUDE.md

Add to the Skills section of the generated CLAUDE.md:
```
- `Cerbero` -- Evaluar skills/MCPs antes de instalar, auditar existentes, verificar rug pulls
```
