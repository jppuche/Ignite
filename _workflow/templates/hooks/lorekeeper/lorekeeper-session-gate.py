"""Lorekeeper hook: SessionStart — context loading + cross-session pending + version check.

Also fires post-compression (compact). Uses a session marker file to detect
re-injection and remind the agent to persist any undocumented insights.
"""
import sys
import json
import os
import re

HOOK_VERSION = "1.0.0"


def _version_tuple(v):
    """Convert version string to comparable tuple. Returns (0,0,0) on error."""
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def main():
    data = json.load(sys.stdin)
    cwd = data.get("cwd", ".")

    # Detect if this is a post-compression re-injection
    # Marker stored in .claude/ (project-scoped) to avoid cross-project false positives
    marker_path = os.path.join(cwd, ".claude", "lorekeeper-session-active.marker")
    is_post_compression = os.path.exists(marker_path)

    if not is_post_compression:
        # First invocation this session — create marker
        try:
            with open(marker_path, "w") as f:
                f.write("active")
        except OSError:
            pass

    # Check for pending work from previous session
    pending_path = os.path.join(cwd, ".claude", "lorekeeper-pending.json")
    pending_items = []
    if os.path.exists(pending_path):
        try:
            with open(pending_path, "r", encoding="utf-8") as f:
                pending = json.load(f)
            pending_items = pending.get("items", [])
            os.remove(pending_path)
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
                    f"is from v{installed_version}. Consider re-running /project-workflow-init to update "
                    f"generated files."
                )

            # Age check: if installed > 30 days ago
            if installed_date and not version_msg:
                from datetime import date as dt_date
                try:
                    inst_date = dt_date.fromisoformat(installed_date)
                    days_old = (dt_date.today() - inst_date).days
                    if days_old > 30:
                        version_msg = (
                            f"Ignite config is {days_old} days old "
                            f"(installed {installed_date}). Check for updates."
                        )
                except ValueError:
                    pass
        except (json.JSONDecodeError, OSError, KeyError):
            pass  # Fail open

    # Phase transition reminder
    phase_reminder = ""
    status_path = os.path.join(cwd, "docs", "STATUS.md")
    if os.path.exists(status_path):
        try:
            with open(status_path, "r", encoding="utf-8") as f:
                status_content = f.read()
            phase_0_done = re.search(
                r"(Phase 0|Fase 0|Foundation|Fundamentos).*?"
                r"(completad|complete|done|\[x\])",
                status_content, re.IGNORECASE
            )
            phase_1_not_started = not re.search(
                r"(Phase 1|Fase 1|Technical Landscape|Panorama).*?"
                r"(completad|complete|done|in.progress|en.curso|\[x\])",
                status_content, re.IGNORECASE
            )
            if phase_0_done and phase_1_not_started:
                days_since = ""
                if os.path.exists(version_path):
                    try:
                        with open(version_path, "r", encoding="utf-8") as f:
                            vdata = json.load(f)
                        installed = vdata.get("installed_date", "")
                        if installed:
                            from datetime import date as dt_date2
                            try:
                                delta = (dt_date2.today() - dt_date2.fromisoformat(installed)).days
                                if delta > 0:
                                    days_since = f" ({delta} day{'s' if delta != 1 else ''} ago)"
                            except ValueError:
                                pass
                    except (json.JSONDecodeError, OSError):
                        pass
                phase_reminder = (
                    f"Phase 0: Foundation completed{days_since}. "
                    "Phase 1: Technical Landscape is pending — "
                    "stack decisions, validation tools, ecosystem scan. "
                    "See _workflow/guides/workflow-guide.md (Phase 1) for details."
                )
        except OSError:
            pass  # Fail open

    # Build context message (injected into Claude's conversation via additionalContext)
    if is_post_compression:
        msg = (
            "Lorekeeper [post-compression]: Context was compressed. "
            "Verify that any valuable insights discovered before compression "
            "are persisted in docs/SCRATCHPAD.md — anything only in conversational "
            "context is now reduced to a summary and details may be lost."
        )
    else:
        msg = "Lorekeeper: Read docs/SCRATCHPAD.md + docs/STATUS.md for context before working."

    if pending_items:
        msg += "\nPENDING from last session:"
        for item in pending_items:
            msg += f"\n  - {item}"
        msg += "\nAddress these items before other work."

    if version_msg:
        msg += f"\n{version_msg}"

    if phase_reminder:
        msg += f"\n{phase_reminder}"

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
