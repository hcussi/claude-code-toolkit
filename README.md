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

None yet.

## Contributing

Add one agent per file under `agents/` (or one skill per directory under
`skills/`), write a matching doc under `docs/`, and add a row to the table above.
