---
name: new-agent
description: Scaffold a new agent in this claude-code-toolkit repo (create agents/<name>.md, the mirrored docs/agents/<name>.md, and add the README table row) following repo conventions. Use when adding a new agent to the toolkit.
disable-model-invocation: true
---

# new-agent

Scaffold a new toolkit **agent** so every entry lands consistent: the
definition, its mirrored doc, and the README table row, in one pass.

## Inputs

Ask the user for these if not provided:

- **name**: kebab-case, unique (becomes `agents/<name>.md`). Verify it does not
  already exist under `agents/`.
- **description**: one or two sentences covering *what it does* and *when to
  use it*. This drives automatic delegation, so make it specific.
- **tools**: the minimal set the agent needs (e.g. `Read, Grep, Glob, Bash`
  for a read-only reviewer). Omit to inherit all tools.
- **model**: optional (`sonnet`, `opus`, `haiku`); omit to inherit.

## Steps

1. **Create `agents/<name>.md`** with this frontmatter, then the system prompt
   body:

   ```markdown
   ---
   name: <name>
   description: <description>
   tools: <comma-separated tools>   # omit line to inherit all
   model: <model>                   # omit line to inherit
   ---

   <System prompt: role, scope, method, and reporting/output format.>
   ```

2. **Create `docs/agents/<name>.md`**: the human-facing doc covering purpose, scope,
   how to use it, and ideally a short example of its output. Go beyond the
   frontmatter; a one-line stub will fail review.

3. **Add a README row.** In the `## Agents` table in `README.md`, add:

   ```
   | `<name>` | <short description> | [docs](docs/agents/<name>.md) |
   ```

4. **Validate.** Run `.claude/scripts/lint-toolkit.sh` and fix anything it
   reports. For a qualitative pass, suggest the user invoke the
   `toolkit-linter` agent.

## Notes

- Keep the top-level `agents/`/`skills/` folders for *published* toolkit items
  only. Repo-maintenance tooling lives in `.claude/`.
- Follow repo conventions: no em dashes; single root `.gitignore`.
- The pre-commit hook runs the lint script automatically, so a scaffold that
  skips step 2 or 3 will block the commit until fixed.
