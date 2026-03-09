"""Lorekeeper hook: SessionStart — real-time doc evaluation + cross-session pending + version check.

Also fires post-compression (compact). Uses a session marker file to detect
re-injection and remind the agent to persist any undocumented insights.
Pending file is NOT deleted here — session-end handles cleanup. This allows
re-injection after context compression in long sessions.
"""
import sys
import json
import os
import re
from datetime import date

HOOK_VERSION = "2.2.0"


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


def _version_tuple(v):
    """Convert version string to comparable tuple. Returns (0,0,0) on error."""
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _read_file_safe(path):
    """Read file content. Returns (content, error_msg). Fail-open."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(), None
    except OSError as e:
        return None, str(e)
    except UnicodeDecodeError:
        return None, "encoding error (not UTF-8)"


def _evaluate_scratchpad(cwd, today, scratchpad_cfg):
    """Evaluate SCRATCHPAD.md status. Returns dict with findings."""
    path = os.path.join(cwd, scratchpad_cfg["path"])
    max_lines = scratchpad_cfg.get("max_lines", 150)
    grad_threshold = scratchpad_cfg.get("graduation_threshold", 100)
    result = {"exists": False, "line_count": 0, "has_today": False, "actions": [], "max_lines": max_lines}

    if not os.path.exists(path):
        result["actions"].append(
            "SCRATCHPAD.md missing — create with session template"
        )
        return result

    content, err = _read_file_safe(path)
    if content is None:
        result["actions"].append(f"SCRATCHPAD.md unreadable ({err})")
        return result

    result["exists"] = True
    result["line_count"] = len(content.splitlines())
    result["has_today"] = today in content

    if result["line_count"] > grad_threshold:
        result["actions"].append(
            f"SCRATCHPAD.md at {result['line_count']}/{max_lines} lines "
            "— graduate repeated patterns to CLAUDE.md Learned Patterns"
        )
    if not result["has_today"]:
        result["actions"].append(
            "SCRATCHPAD.md has no entry for today — create session section with template"
        )

    return result


def _evaluate_changelog(cwd, today, changelog_cfg):
    """Evaluate CHANGELOG-DEV.md status. Returns dict with findings."""
    path = os.path.join(cwd, changelog_cfg["path"])
    result = {"exists": False, "has_today": False, "actions": []}

    if not os.path.exists(path):
        result["actions"].append(
            "CHANGELOG-DEV.md missing — create initial entry"
        )
        return result

    content, err = _read_file_safe(path)
    if content is None:
        result["actions"].append(f"CHANGELOG-DEV.md unreadable ({err})")
        return result

    result["exists"] = True
    result["has_today"] = today in content
    # No action at session start for changelog — checked at commit-gate and session-end
    return result


def _extract_current_phase(cwd, status_cfg):
    """Extract current phase description from STATUS.md. Returns string or None."""
    path = os.path.join(cwd, status_cfg["path"])
    content, _ = _read_file_safe(path)
    if not content:
        return None

    lines = content.splitlines()
    in_phase_section = False
    for line in lines:
        if re.match(r"^##\s+(Fase actual|Current phase)", line, re.IGNORECASE):
            in_phase_section = True
            continue
        if in_phase_section:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped
            if stripped.startswith("#"):
                break  # Next section reached
    return None


def _extract_pending_tasks(cwd, status_cfg, max_items=5):
    """Extract unchecked tasks from STATUS.md. Returns list of strings."""
    path = os.path.join(cwd, status_cfg["path"])
    content, _ = _read_file_safe(path)
    if not content:
        return []

    tasks = []
    for line in content.splitlines():
        match = re.match(r"^\s*-\s*\[\s*\]\s+(.+)", line)
        if match:
            tasks.append(match.group(1).strip())
            if len(tasks) >= max_items:
                break
    return tasks


_PHASE_ACTIONS = {
    "phase 0": ["Run /ignite", "Complete Discovery + FOUNDATION.md", "Verify generated files"],
    "phase 1": ["Stack decisions in DECISIONS.md", "Ecosystem scan for tools"],
    "phase 2": ["Evaluate candidates with Cerbero", "Install approved tools"],
    "phase 3": ["Strategic review of Phase 1-2 decisions", "Architecture directives"],
    "phase 4": ["Write block specs in docs/specs/", "Security review"],
    "phase 5": ["Install agents", "Assign skills", "Populate AGENT-COORDINATION Sec 13"],
    "phase n": ["Check next block spec in docs/specs/", "Follow block exit conditions"],
    "development": ["Check next block spec in docs/specs/", "Follow block exit conditions"],
    "final": ["Security audit", "Performance validation", "Documentation review"],
    "hardening": ["Security audit", "Performance validation", "Documentation review"],
}


def _get_phase_actions(phase_str, status_path="docs/STATUS.md"):
    """Return actionable guidance for the current phase. Empty list if no match."""
    if not phase_str:
        return [f"Read {status_path} to determine current phase"]
    phase_lower = phase_str.lower()
    for key, actions in _PHASE_ACTIONS.items():
        if key in phase_lower:
            return actions
    return []


def main():
    data = json.load(sys.stdin)
    cwd = data.get("cwd", ".")

    # Detect if this is a post-compression re-injection
    # Marker stored in .claude/ (project-scoped) to avoid cross-project false positives
    marker_path = os.path.join(cwd, ".claude", "lorekeeper-session-active.marker")
    is_post_compression = False
    if os.path.exists(marker_path):
        # Check marker age — stale markers (>24h) indicate a crash, not compression
        try:
            marker_age = (date.today() - date.fromisoformat(
                open(marker_path, "r").read().strip()[:10]
            )).days
            is_post_compression = marker_age < 1
        except (ValueError, OSError):
            is_post_compression = False  # Unreadable marker — treat as stale

    if not is_post_compression:
        # First invocation this session — create marker with timestamp
        try:
            os.makedirs(os.path.dirname(marker_path), exist_ok=True)
            with open(marker_path, "w") as f:
                f.write(date.today().isoformat())
        except OSError as e:
            print(f"Lorekeeper: marker creation failed at {marker_path}: {e}", file=sys.stderr)

    # Check for pending work from previous session
    pending_path = os.path.join(cwd, ".claude", "lorekeeper-pending.json")
    pending_items = []
    pending = {}
    if os.path.exists(pending_path):
        try:
            with open(pending_path, "r", encoding="utf-8") as f:
                pending = json.load(f)
            pending_items = pending.get("items", [])
            # Don't delete — session-end handles cleanup.
            # Keeps file available for re-injection after context compression.
        except (json.JSONDecodeError, OSError):
            pass

    # Check for version drift (hook updated but project config stale)
    version_msg = ""
    version_path = os.path.join(cwd, ".claude", "ignite-version.json")
    if os.path.exists(version_path):
        try:
            with open(version_path, "r", encoding="utf-8") as f:
                version_data = json.load(f)
            installed_version = version_data.get("version", "0.0.0")
            installed_date = version_data.get("installed_date", "")

            if _version_tuple(HOOK_VERSION) > _version_tuple(installed_version):
                version_msg = (
                    f"Ignite update: hooks are v{HOOK_VERSION} but project config "
                    f"is from v{installed_version}. Consider re-running "
                    "/ignite to update generated files."
                )

            # Age check: if installed > 30 days ago
            if installed_date and not version_msg:
                try:
                    inst_date = date.fromisoformat(installed_date)
                    days_old = (date.today() - inst_date).days
                    if days_old > 30:
                        version_msg = (
                            f"Ignite config is {days_old} days old "
                            f"(installed {installed_date}). Check for updates."
                        )
                except ValueError:
                    pass
        except (json.JSONDecodeError, OSError, KeyError):
            pass  # Fail open

    # --- Load config (paths + thresholds) ---
    cfg = _load_config(cwd)

    # --- Real-time file evaluation ---
    today = date.today().isoformat()
    scratchpad_eval = _evaluate_scratchpad(cwd, today, cfg["docs"]["scratchpad"])
    changelog_eval = _evaluate_changelog(cwd, today, cfg["docs"]["changelog"])
    current_phase = _extract_current_phase(cwd, cfg["docs"]["status"])
    pending_tasks = _extract_pending_tasks(cwd, cfg["docs"]["status"])

    # Build REQUIRED ACTIONS (prioritized)
    required_actions = []
    # Priority 1: Pending items from previous session
    for item in pending_items[:5]:
        required_actions.append(item)
    # Priority 2: Scratchpad actions
    for action in scratchpad_eval["actions"]:
        required_actions.append(action)
    # Priority 3: Changelog actions
    for action in changelog_eval["actions"]:
        required_actions.append(action)

    # --- Build structured message ---
    if is_post_compression:
        msg = (
            "Lorekeeper SESSION PROTOCOL [post-compression] — MANDATORY before any work:\n\n"
            "RECOVERY ACTION:\n"
            "  Context was compressed. Verify that insights from before compression\n"
            f"  are persisted in {cfg['docs']['scratchpad']['path']} — conversational context is now\n"
            "  reduced to a summary and details may be lost.\n"
        )
    else:
        msg = "Lorekeeper SESSION PROTOCOL — MANDATORY before any work:\n"

    if required_actions:
        msg += "\nREQUIRED ACTIONS (do these FIRST):\n"
        for i, action in enumerate(required_actions[:8], 1):
            msg += f"  {i}. {action}\n"

    msg += "\nSESSION CONTEXT:\n"
    status_path = cfg["docs"]["status"]["path"]
    msg += f"  CURRENT PHASE: {current_phase or f'unknown — check {status_path}'}\n"
    if scratchpad_eval["exists"]:
        msg += f"  SCRATCHPAD: {scratchpad_eval['line_count']}/{scratchpad_eval['max_lines']} lines\n"
    else:
        msg += "  SCRATCHPAD: missing\n"
    if pending_tasks:
        msg += "  Pending tasks from STATUS.md:\n"
        for task in pending_tasks:
            msg += f"    - {task}\n"

    # Phase-specific actionable guidance
    phase_actions = _get_phase_actions(current_phase, status_path)
    if phase_actions:
        msg += "  Recommended actions for this phase:\n"
        for action in phase_actions:
            msg += f"    - {action}\n"

    # Session handoff from previous session (populated by session-end hook)
    handoff = pending.get("handoff_summary", "")
    if handoff:
        msg += f"\n  SESSION HANDOFF (from previous session):\n"
        msg += f"    {handoff}\n"

    if version_msg:
        msg += f"\n  {version_msg}\n"

    msg += "\nREMINDERS:\n"
    msg += "  - Update SCRATCHPAD with errors/corrections/discoveries AS THEY HAPPEN (not at the end)\n"
    validate_script = cfg["validation_script"]
    msg += f"  - Run `bash {validate_script}` before every commit\n"
    msg += "  - Update CHANGELOG-DEV.md if significant changes are made\n"

    # Output structured JSON — additionalContext goes directly into Claude's context
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": msg,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
