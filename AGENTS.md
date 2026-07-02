# AGENTS.md

Guidance for coding agents (and humans) working in this repository.

## What this repo is

`claude-code-toolkit` is a curated collection of reusable [Claude Code](https://claude.com/claude-code)
**agents** and **skills**, kept in one place so they can be copied into any
project. It is a content repo: there is no application to build or run.

There are two distinct layers, and they must not be confused:

1. **Published items** (what the toolkit ships): `agents/`, `skills/`, and their
   docs under `docs/`. These are meant to be copied out into other projects.
2. **Repo maintenance tooling** (particular to this repo): everything under
   `.claude/`. This is not shipped; it keeps the collection consistent.

Never put maintenance tooling in the top-level `agents/`/`skills/` folders, and
never treat a `.claude/` item as a published product.

## Layout

```
agents/<name>.md               # published subagent definition (frontmatter + prompt)
skills/<name>/SKILL.md          # published skill (may bundle references/ files)
docs/agents/<name>.md           # one doc per agent, mirroring agents/
docs/skills/<name>.md           # one doc per skill, mirroring skills/
README.md                       # index; Agents and Skills tables link to docs
.claude/                        # repo maintenance tooling (not shipped)
  agents/toolkit-linter.md      # on-demand consistency reviewer
  skills/new-agent/SKILL.md     # /new-agent scaffolder
  scripts/lint-toolkit.sh       # deterministic invariant checks
  hooks/                        # PreToolUse hooks (see settings.json)
  settings.json                 # committed hook wiring
  settings.local.json           # machine-local, gitignored
```

## Invariants (enforced by `.claude/scripts/lint-toolkit.sh`)

Every published item must satisfy all of these, or the pre-commit hook blocks
the commit:

- **Agent**: `agents/<name>.md` has frontmatter with `name` and `description`;
  the `name` equals `<name>`; a mirror `docs/agents/<name>.md` exists; and
  `README.md` has a table row linking to that doc.
- **Skill**: `skills/<name>/SKILL.md` has frontmatter `name` equal to `<name>`
  and a `description`; a mirror `docs/skills/<name>.md` exists; and `README.md`
  links to it.
- **No per-directory `.gitignore`**: use the single root `.gitignore` only.

Run the checks anytime with `./.claude/scripts/lint-toolkit.sh`. For a
qualitative pass (description quality, doc completeness, tool grants), run the
`toolkit-linter` agent.

## Adding an item

The fastest path for an agent is the `/new-agent` skill, which scaffolds the
definition, the mirrored doc, and the README row in one pass. Otherwise, by
hand:

1. Create the definition (`agents/<name>.md` or `skills/<name>/SKILL.md`).
2. Create the mirrored doc under `docs/` (purpose, scope, usage, and ideally an
   example; a one-line stub will fail qualitative review).
3. Add a row to the matching table in `README.md`.
4. Run the lint script and fix anything it reports.

### Frontmatter conventions

- **Agents**: `description` should say what it does and *when to use it* (this
  drives automatic delegation). Grant the minimal `tools`. Read-only reviewers
  should not request `Write`. `model` is optional.
- **Skills**: use `disable-model-invocation: true` for user-invoked skills that
  write files or have side effects (so they run only when explicitly called).

## House rules

- **Never use em dashes** (the `—` character) anywhere: prose, code, comments,
  commit messages. Use a comma, colon, parentheses, or two sentences.
- **Single root `.gitignore`** only. No per-directory ones (a hook blocks them).
- **Never commit or push on your own initiative.** Make the change, verify it
  (run the lint script), then stop. Commit and push only when explicitly asked.
- `.claude/settings.local.json` is machine-local and gitignored; do not commit
  it or move its contents into the committed `settings.json`.
