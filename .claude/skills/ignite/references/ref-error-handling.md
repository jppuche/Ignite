# Error Handling

## General
- If a template file is missing: warn the user, skip that file, continue with the rest
- If a placeholder has no value and no default: ask the user directly
- If CLAUDE.md already exists: ask before overwriting (offer merge option)
- If git is already initialized: skip git init, just create branch if needed
- If package.json scripts are missing: use npm defaults, inform user to update later

## Overwrite protection — Category A (docs with user data)
- If existing file cannot be parsed (corrupted, no recognizable headings): warn user, offer: (a) replace entirely with template, (b) keep existing, (c) abort
- If merge would exceed line limit (STATUS.md > 60, SCRATCHPAD.md > 150): proceed with warning — adding missing sections is more important than line limits during re-init
- If a required section heading exists but content is empty: treat as present (do not re-add)
- If existing file is 0 bytes: treat as corrupted, apply same warn/offer logic above

## Overwrite protection — Category B (executable code)
- If content comparison fails (encoding issues, binary content): treat as different, replace with warning
- If existing file is 0 bytes: replace without prompting
- CRLF vs LF differences: normalize before comparing (strip `\r\n` to `\n`)

## Overwrite protection — Category C (rules + agents)
- If user rejects ALL suggested additions: respect decisions and continue without changes
- If YAML frontmatter differs from template (e.g., different `paths:` patterns): treat as customized, do not merge
- If existing file is 0 bytes: offer to replace
- If file has no OW category in file-map.md: fallback to Category B with warning logged

## Report generation
- If STATE == "fresh" and somehow files are found: log inconsistency, proceed as partial
- If ANALYSIS produces zero actionable items (all skips): display "Todo esta actualizado — sin cambios necesarios." and skip global confirmation prompt
