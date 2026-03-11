"""Lorekeeper hook: PreToolUse — block commits with stale documentation.

Blocks on [FAIL] (hard gate). Warnings ([WARN] + freshness checks) are
emitted as additionalContext — injected into Claude's conversation so the
agent can act on them after the commit proceeds.
"""
import sys
import json
import re
import subprocess
import os
from datetime import date

HOOK_VERSION = "2.2.1"


def _load_config(cwd):
    """Load lorekeeper config. Returns defaults if not found/corrupt."""
    config_path = os.path.join(cwd, ".claude", "lorekeeper-config.json")
    DEFAULTS = {
        "docs": {
            "scratchpad": {"path": "docs/SCRATCHPAD.md", "max_lines": 150, "graduation_threshold": 100},
            "changelog": {"path": "docs/CHANGELOG-DEV.md", "check_freshness": True},
            "status": {"path": "docs/STATUS.md", "max_lines": 60},
            "decisions": {"path": "docs/DECISIONS.md"},
            "lessons_learned": {"path": "docs/LESSONS-LEARNED.md"},
        },
        "claude_md": {"path": "CLAUDE.md", "max_lines": 200, "warn_threshold": 180},
        "validation_script": "scripts/validate-docs.sh",
    }
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for role, defs in DEFAULTS["docs"].items():
            if role not in cfg.get("docs", {}):
                cfg.setdefault("docs", {})[role] = defs
            else:
                for k, v in defs.items():
                    cfg["docs"][role].setdefault(k, v)
        for k, v in DEFAULTS["claude_md"].items():
            cfg.setdefault("claude_md", {}).setdefault(k, v)
        cfg.setdefault("validation_script", DEFAULTS["validation_script"])
        return cfg
    except (OSError, json.JSONDecodeError, ValueError):
        return DEFAULTS


def _check_freshness(cwd, cfg):
    """Check if SCRATCHPAD and CHANGELOG-DEV.md have today's date. Returns list of warnings."""
    today = date.today().isoformat()
    warnings = []

    scratchpad_path = os.path.join(cwd, cfg["docs"]["scratchpad"]["path"])
    if os.path.isfile(scratchpad_path):
        try:
            with open(scratchpad_path, "r", encoding="utf-8") as f:
                if today not in f.read():
                    warnings.append(
                        "SCRATCHPAD.md has no entry for today — add session section"
                    )
        except (OSError, UnicodeDecodeError):
            pass

    changelog_path = os.path.join(cwd, cfg["docs"]["changelog"]["path"])
    if os.path.isfile(changelog_path):
        try:
            with open(changelog_path, "r", encoding="utf-8") as f:
                if today not in f.read():
                    warnings.append(
                        "CHANGELOG-DEV.md has no entry for today "
                        "— add entry if significant changes were made"
                    )
        except (OSError, UnicodeDecodeError):
            pass

    return warnings


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

    cfg = _load_config(cwd)

    # Run validate-docs.sh
    script_path = os.path.join(cwd, cfg["validation_script"])
    if not os.path.isfile(script_path):
        print(
            f"Lorekeeper WARNING: {cfg['validation_script']} not found, cannot validate docs.",
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

    # Hard gate: [FAIL] blocks the commit
    if has_fail:
        fail_lines = [
            l.strip() for l in result.stdout.splitlines() if "[FAIL]" in l
        ]
        reason = "Lorekeeper: documentation validation FAILED. Fix before committing:\n"
        for line in fail_lines[:5]:
            reason += f"  {line}\n"
        reason += f"Run: bash {cfg['validation_script']} for full report."

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

    # --- Accumulate all warnings (validate-docs [WARN] + freshness) ---
    all_warnings = []

    if has_warn:
        warn_lines = [
            l.strip() for l in result.stdout.splitlines() if "[WARN]" in l
        ]
        all_warnings.extend(warn_lines[:5])

    # Freshness checks (only run if commit isn't blocked)
    freshness_warnings = _check_freshness(cwd, cfg)
    all_warnings.extend(freshness_warnings)

    # Emit warnings as additionalContext (injected into Claude's conversation)
    if all_warnings:
        msg = "Lorekeeper commit warnings — act on these after committing:\n"
        for w in all_warnings:
            msg += f"  - {w}\n"
        json.dump(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "additionalContext": msg,
                }
            },
            sys.stdout,
        )
        sys.exit(0)

    # Clean pass — no output needed
    sys.exit(0)


if __name__ == "__main__":
    main()
