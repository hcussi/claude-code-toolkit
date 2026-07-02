# claude-code-toolkit

Reusable **agents** and **skills** for
[Claude Code](https://claude.com/claude-code), kept in one place so they can be
dropped into any project.

## Layout

```
agents/        # subagent definitions (Markdown + YAML frontmatter)
skills/        # skills (added over time)
docs/          # one doc per agent/skill, mirroring the folders above
```

To use an item, copy its file into a project's `.claude/agents/` (or
`.claude/skills/`) directory, or into `~/.claude/` to make it available
everywhere.

## Agents

| Agent | Description | Docs |
| --- | --- | --- |
| `security-reviewer` | Read-only OAuth2/OIDC security audit for any web stack. | [docs](docs/agents/security-reviewer.md) |

## Skills

| Skill | Description | Docs |
| --- | --- | --- |
| `spring-oauth2-resource-server` | Configure a Spring Boot app as an OAuth2/OIDC JWT resource server (any provider). | [docs](docs/skills/spring-oauth2-resource-server.md) |

## Repo tooling

Maintenance automations for *this* repo live under `.claude/` (committed, so
they apply to anyone who clones it). They are separate from the published items
above:

- **`new-agent` skill**: `/new-agent` scaffolds `agents/<name>.md`, its
  `docs/` mirror, and the README row in one pass.
- **`toolkit-linter` agent**: on-demand review of frontmatter, docs, and
  README consistency.
- **Hooks**: a pre-commit hook runs `.claude/scripts/lint-toolkit.sh` (valid
  frontmatter, doc mirror, README row, single-root `.gitignore`) and blocks the
  commit on failure; another blocks any non-root `.gitignore`.

## Contributing

Add one agent per file under `agents/` (or one skill per directory under
`skills/`), write a matching doc under `docs/`, and add a row to the table above.
