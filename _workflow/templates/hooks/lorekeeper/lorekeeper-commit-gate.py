"""Lorekeeper hook: PreToolUse — block commits with stale documentation."""
import sys
import json
import re
import subprocess
import os


def main():
    data = json.load(sys.stdin)
    command = data.get("tool_input", {}).get("command", "")
    cwd = data.get("cwd", ".")

    # Only intercept git commit commands
    if not re.search(r"\bgit\s+commit\b", command):
        sys.exit(0)

    # Escape hatch: --no-verify bypasses docs check
    if "--no-verify" in command:
        print(
            "Lorekeeper: --no-verify detected, skipping docs validation.",
            file=sys.stderr,
        )
        sys.exit(0)

    # Run validate-docs.sh
    script_path = os.path.join(cwd, "scripts", "validate-docs.sh")
    if not os.path.isfile(script_path):
        print(
            "Lorekeeper WARNING: scripts/validate-docs.sh not found, cannot validate docs.",
            file=sys.stderr,
        )
        sys.exit(0)

    try:
        bash_cmd = os.environ.get("CLAUDE_CODE_GIT_BASH_PATH", "bash")
        result = subprocess.run(
            [bash_cmd, script_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=cwd,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(
            f"Lorekeeper WARNING: validate-docs.sh failed to run: {e}",
            file=sys.stderr,
        )
        sys.exit(0)

    has_fail = "[FAIL]" in result.stdout
    has_warn = "[WARN]" in result.stdout

    if has_fail:
        fail_lines = [
            l.strip() for l in result.stdout.splitlines() if "[FAIL]" in l
        ]
        reason = "Lorekeeper: documentation validation FAILED. Fix before committing:\n"
        for line in fail_lines[:5]:
            reason += f"  {line}\n"
        reason += "Run: bash scripts/validate-docs.sh for full report."

        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            },
            sys.stdout,
        )
        sys.exit(0)

    if has_warn:
        warn_lines = [
            l.strip() for l in result.stdout.splitlines() if "[WARN]" in l
        ]
        msg = "Lorekeeper WARNING: documentation has warnings:\n"
        for line in warn_lines[:5]:
            msg += f"  {line}\n"
        print(msg, file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
