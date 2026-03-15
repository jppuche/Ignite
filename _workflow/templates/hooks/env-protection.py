"""Env protection hook: PreToolUse — blocks access to sensitive files (.env, secrets, credentials).

Matcher: Read, Write, Edit, Bash (registered separately in settings.local.json).
- Read tool: blocks if file_path matches sensitive patterns.
- Write tool: blocks if file_path matches sensitive patterns.
- Edit tool: blocks if file_path matches sensitive patterns.
- Bash tool: warns (additionalContext) if command accesses sensitive files.
Grep tool has no PreToolUse matcher in CC (platform limitation). Grep access to
sensitive files is lower risk (returns content matches, not full file). Documented
as known limitation.

Fail-open: errors → allow + warn (consistent with all Ignite hooks).
"""
import sys
import json
import re
import os

SENSITIVE_PATTERNS = [
    (r"[/\\]?\.env$", ".env file"),
    (r"[/\\]?\.env\.\w+", ".env.* variant"),
    (r"secrets[/\\]", "secrets directory"),
    (r"credentials\.json$", "credentials file"),
    (r"[/\\]?\.aws[/\\](credentials|config)$", "AWS credentials"),
    (r"[/\\]?\.gcp[/\\]credentials\.json$", "GCP credentials"),
    (r"[/\\]?\.ssh[/\\]", "SSH directory"),
    # Security infrastructure (C-SEC-002, H-SEC-004, H-SEC-005)
    (r"[/\\]?\.claude[/\\]security[/\\]", "security audit logs"),
    (r"[/\\]?\.claude[/\\]quality-gate\.json$", "quality gate config"),
    (r"[/\\]?\.claude[/\\]hooks[/\\]", "hook scripts"),
    (r"[/\\]?\.claude[/\\]hook-integrity\.json$", "hook integrity baseline"),
    # Platform secrets (M-SEC-001)
    (r"[/\\]?\.kube[/\\]config$", "Kubernetes config"),
    (r"[/\\]?\.docker[/\\]config\.json$", "Docker config"),
    (r"(id_rsa|id_ed25519|id_ecdsa)$", "SSH private key"),
    (r"key\.pem$", "PEM private key"),
]


def _check_path(path):
    """Check if a file path matches any sensitive pattern. Returns (matched, description)."""
    if not path:
        return False, ""
    # Normalize path separators
    normalized = path.replace("\\", "/")
    for pattern, desc in SENSITIVE_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, desc
    return False, ""


def _check_bash_command(command):
    """Check if a bash command accesses sensitive files. Returns (matched, description)."""
    if not command:
        return False, ""
    for pattern, desc in SENSITIVE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, desc
    return False, ""


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # Fail-open

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        matched, desc = _check_path(file_path)
        if matched:
            json.dump({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Blocked: reading {desc} ({os.path.basename(file_path)}). "
                        "Sensitive files should not be read by AI agents. "
                        "If you need values from this file, ask the user to provide them directly."
                    ),
                }
            }, sys.stdout)
            sys.exit(0)

    elif tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        matched, desc = _check_path(file_path)
        if matched:
            action = "writing to" if tool_name == "Write" else "editing"
            json.dump({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Blocked: {action} {desc} ({os.path.basename(file_path)}). "
                        "Sensitive files should not be modified by AI agents. "
                        "If you need to update this file, ask the user to do it manually."
                    ),
                }
            }, sys.stdout)
            sys.exit(0)

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        matched, desc = _check_bash_command(command)
        if matched:
            json.dump({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "additionalContext": (
                        f"WARNING: This command may access {desc}. "
                        "Avoid reading, printing, or logging sensitive file contents. "
                        "If you need configuration values, ask the user to provide them."
                    ),
                }
            }, sys.stdout)
            sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
