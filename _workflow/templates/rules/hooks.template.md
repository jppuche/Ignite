# Hooks Configuration

Configured in .claude/settings.local.json (do not commit).

## Lorekeeper hooks
- `lorekeeper-session-gate.py` (SessionStart) — SCRATCHPAD/CHANGELOG/STATUS eval, REQUIRED ACTIONS
- `lorekeeper-commit-gate.py` (PreToolUse:Bash) — blocks commit if docs validation fails
- `lorekeeper-session-end.py` (SessionEnd) — checkpoint, graduation candidates, pending items

## Quality hooks
- `code-quality-gate.py` (PreToolUse:Bash) — typecheck/lint/test before commit

## Security hooks
- `validate-prompt.py` (UserPromptSubmit) — prompt injection scanning
- `env-protection.py` (PreToolUse:Read+Bash) — blocks .env/secrets/credentials access
- `pre-tool-security.py` (PreToolUse:Bash) — destructive command blocking
- `mcp-audit.py` (PreToolUse:mcp__*) — MCP tool audit trail
- `untrusted-source-reminder.py` (PreToolUse:WebFetch+mcp__*) — security reminder before external content
- `validate-tool-output.py` (PostToolUse:WebFetch+mcp__*) — scans external outputs for indirect injection

## Standalone (not a hook)
- `cerbero-scanner.py` — CLI scanner for file-level security checks (`python cerbero-scanner.py --file <path>`)
