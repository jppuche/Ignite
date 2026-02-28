"""Env protection hook: PreToolUse — blocks reading sensitive files (.env, secrets, credentials).

Matcher: Read, Bash (registered separately in settings.local.json).
- Read tool: blocks if file_path matches sensitive patterns.
- Bash tool: warns (additionalContext) if command accesses sensitive files.
Grep tool is not matched (lower risk: returns content matches, not full file).

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
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        # Fail-open: can't parse input → allow
        print(json.dumps({"decision": "allow"}))
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        matched, desc = _check_path(file_path)
        if matched:
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"Blocked: reading {desc} ({os.path.basename(file_path)}). "
                    "Sensitive files should not be read by AI agents. "
                    "If you need values from this file, ask the user to provide them directly."
                )
            }))
            return

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        matched, desc = _check_bash_command(command)
        if matched:
            print(json.dumps({
                "decision": "allow",
                "additionalContext": (
                    f"WARNING: This command may access {desc}. "
                    "Avoid reading, printing, or logging sensitive file contents. "
                    "If you need configuration values, ask the user to provide them."
                )
            }))
            return

    # Default: allow
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
