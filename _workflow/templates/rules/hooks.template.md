# Hooks Configuration

Configured in .claude/settings.local.json (do not commit).

| Hook | Event | Purpose |
|------|-------|---------|
| `lorekeeper-session-gate.py` | SessionStart | SCRATCHPAD/CHANGELOG/STATUS eval, REQUIRED ACTIONS |
| `lorekeeper-commit-gate.py` | PreToolUse:Bash | Blocks commit if docs validation fails |
| `lorekeeper-session-end.py` | SessionEnd | Checkpoint, graduation candidates, pending items |
| `code-quality-gate.py` | PreToolUse:Bash | Typecheck/lint/test before commit |
| `validate-prompt.py` | UserPromptSubmit | Prompt injection scanning |
| `env-protection.py` | PreToolUse:Read+Bash+Grep | Blocks .env/secrets/credentials access |
| `pre-tool-security.py` | PreToolUse:Bash | Destructive command blocking |
| `mcp-audit.py` | PreToolUse:mcp__* | MCP tool audit trail |
| `untrusted-source-reminder.py` | PreToolUse:WebFetch+mcp__* | Security reminder before external content |
| `validate-tool-output.py` | PostToolUse:WebFetch+mcp__* | Scans external outputs for indirect injection |

## Standalone (not a hook)
- `cerbero-scanner.py` — CLI scanner for file-level security checks (`python cerbero-scanner.py --file <path>`)
