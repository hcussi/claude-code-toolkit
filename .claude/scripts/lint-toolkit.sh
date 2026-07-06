#!/usr/bin/env bash
# Validate claude-code-toolkit invariants. Deterministic checks shared by the
# pre-commit hook and the toolkit-linter agent:
#   * every published agent/skill has valid frontmatter (name, description),
#     with no unquoted value that would break YAML parsing
#   * the frontmatter name matches the file/directory name
#   * a mirrored doc exists under docs/
#   * README.md has a table row linking to that doc
#   * no per-directory .gitignore (single root .gitignore convention)
# Exit 0 and print "toolkit-lint: OK" when clean; exit 1 and list problems on
# stderr otherwise.
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
cd "$ROOT" || { echo "toolkit-lint: cannot cd to $ROOT" >&2; exit 1; }

errors=()

# Print the value of a top-level key inside the leading --- YAML frontmatter.
frontmatter_value() {
  awk -v key="$2" '
    NR==1 && $0=="---" { infm=1; next }
    infm && $0=="---" { exit }
    infm && $0 ~ "^"key":" { sub("^"key":[ \t]*",""); print; exit }
  ' "$1"
}

# Print the key of any top-level frontmatter line whose unquoted value contains a
# colon followed by a space or end of line. YAML reads that as a nested mapping
# and fails to parse (as GitHub's frontmatter renderer does). Quoting the value
# fixes it. URLs are safe because "://" is a colon followed by "/", not a space.
frontmatter_yaml_hazards() {
  awk '
    NR==1 && $0=="---" { infm=1; next }
    infm && $0=="---" { exit }
    infm && /^[A-Za-z0-9_-]+:/ {
      key=$0; sub(/:.*/,"",key)
      val=$0; sub(/^[A-Za-z0-9_-]+:[ \t]*/,"",val)
      if (val=="") next
      c=substr(val,1,1)
      if (c=="\"" || c=="\047" || c=="[" || c=="{" || c=="|" || c==">") next
      if (val ~ /:([ \t]|$)/) print key
    }
  ' "$1"
}

# check_item <file> <expected-name> <doc-path>
check_item() {
  local file="$1" expected="$2" doc="$3" name desc
  name=$(frontmatter_value "$file" name)
  desc=$(frontmatter_value "$file" description)
  [[ -z "$name" ]] && errors+=("$file: missing 'name' in frontmatter")
  [[ -z "$desc" ]] && errors+=("$file: missing 'description' in frontmatter")
  if [[ -n "$name" && "$name" != "$expected" ]]; then
    errors+=("$file: frontmatter name '$name' does not match path name '$expected'")
  fi
  [[ ! -f "$doc" ]] && errors+=("$file: missing mirrored doc at $doc")
  if [[ ! -f README.md ]] || ! grep -q "$doc" README.md; then
    errors+=("$file: no README row linking to $doc")
  fi
  while IFS= read -r badkey; do
    [[ -n "$badkey" ]] && errors+=("$file: frontmatter '$badkey' has an unquoted value containing ': '; wrap the value in quotes (breaks YAML parsing)")
  done < <(frontmatter_yaml_hazards "$file")
}

# Agents: agents/<name>.md -> docs/agents/<name>.md
if compgen -G "agents/*.md" >/dev/null; then
  for f in agents/*.md; do
    base=$(basename "$f" .md)
    check_item "$f" "$base" "docs/agents/$base.md"
  done
fi

# Skills: skills/<name>/SKILL.md -> docs/skills/<name>.md
if compgen -G "skills/*/SKILL.md" >/dev/null; then
  for f in skills/*/SKILL.md; do
    base=$(basename "$(dirname "$f")")
    check_item "$f" "$base" "docs/skills/$base.md"
  done
fi

# Single-root .gitignore convention. git ls-files respects .gitignore, so
# ignored paths (e.g. .idea/.gitignore) are correctly excluded.
while IFS= read -r gi; do
  [[ -z "$gi" || "$gi" == ".gitignore" ]] && continue
  errors+=("$gi: per-directory .gitignore not allowed (use the single root .gitignore)")
done < <(git ls-files -co --exclude-standard 2>/dev/null | grep -E '(^|/)\.gitignore$' || true)

if ((${#errors[@]})); then
  echo "toolkit-lint: ${#errors[@]} problem(s) found:" >&2
  for e in "${errors[@]}"; do echo "  - $e" >&2; done
  exit 1
fi
echo "toolkit-lint: OK"
exit 0
