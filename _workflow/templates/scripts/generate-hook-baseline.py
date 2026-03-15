"""Generate .claude/hook-integrity.json with SHA-256 hashes of deployed hooks.

Run from project root after deploying hooks:
    python scripts/generate-hook-baseline.py

Creates a baseline file that lorekeeper-session-gate.py uses to detect
unauthorized hook modifications at session start.
"""
import hashlib
import json
import os
import sys


def main():
    cwd = os.getcwd()
    hooks_dir = os.path.join(cwd, ".claude", "hooks")

    if not os.path.isdir(hooks_dir):
        print(f"Error: hooks directory not found at {hooks_dir}", file=sys.stderr)
        sys.exit(1)

    baseline = {}
    for root, _dirs, files in os.walk(hooks_dir):
        for filename in sorted(files):
            if not filename.endswith(".py"):
                continue
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, os.path.join(cwd, ".claude"))
            with open(full_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            baseline[rel_path.replace("\\", "/")] = file_hash

    out_path = os.path.join(cwd, ".claude", "hook-integrity.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2, sort_keys=True)
        f.write("\n")

    print(f"Baseline generated: {len(baseline)} hooks hashed -> {out_path}")
    for rel, h in sorted(baseline.items()):
        print(f"  {rel}: {h[:16]}...")


if __name__ == "__main__":
    main()
