#!/usr/bin/env bash
# PreToolUse (Bash) hook. When Claude runs a `git commit`, run the toolkit
# linter first and block the commit (exit 2) if it fails. Any other Bash
# command passes straight through (exit 0).
#
# Note: this only gates commits made through Claude's Bash tool. To enforce the
# same check on commits made in a plain terminal, install a git-native hook
# that runs .claude/scripts/lint-toolkit.sh.
set -uo pipefail

input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')

# Match `git [global-flags] commit ...`; ignore everything else.
if ! printf '%s' "$cmd" | grep -Eq '(^|[^[:alnum:]_])git[[:space:]]+([-][^[:space:]]+[[:space:]]+)*commit([[:space:]]|$)'; then
  exit 0
fi

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
if ! out=$("$ROOT/.claude/scripts/lint-toolkit.sh" 2>&1); then
  {
    echo "Blocked git commit: the toolkit linter failed. Fix these first"
    echo "(or run the toolkit-linter agent for a fuller review):"
    echo "$out"
  } >&2
  exit 2
fi
exit 0
