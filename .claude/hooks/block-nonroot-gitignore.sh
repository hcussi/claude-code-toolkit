#!/usr/bin/env bash
# PreToolUse (Write|Edit) hook. Enforce the single-root-.gitignore convention:
# block creating or editing any .gitignore that is not the repository root one.
set -uo pipefail

input=$(cat)
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // ""')
[[ -z "$path" ]] && exit 0
[[ "$(basename "$path")" != ".gitignore" ]] && exit 0

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
# Normalize a relative path against the project root.
[[ "$path" != /* ]] && path="$ROOT/$path"

if [[ "$path" != "$ROOT/.gitignore" ]]; then
  echo "Blocked: per-directory .gitignore is not allowed. Add rules to the single root .gitignore at $ROOT/.gitignore instead." >&2
  exit 2
fi
exit 0
