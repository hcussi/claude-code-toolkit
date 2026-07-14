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
| `ui-design-reviewer` | Read-only UI review of a running app via the Playwright MCP, against Material-informed minimalism. | [docs](docs/agents/ui-design-reviewer.md) |

## Skills

| Skill | Description | Docs |
| --- | --- | --- |
| `medium-article` | Turn an implemented PLAN.md into a Medium-style article (voice-matched draft, review gate), then stage it on Medium as a draft via the Playwright MCP. | [docs](docs/skills/medium-article.md) |
| `mermaid-to-images` | Render a Markdown file's diagrams (mermaid blocks, plus ASCII art translated to mermaid) to image files and rewrite each block as an image reference. | [docs](docs/skills/mermaid-to-images.md) |
| `spring-oauth2-resource-server` | Configure a Spring Boot app as an OAuth2/OIDC JWT resource server (any provider). | [docs](docs/skills/spring-oauth2-resource-server.md) |
| `ui-iterate` | Human-in-the-loop UI redesign loop on a running app (Playwright MCP + ui-design-reviewer). | [docs](docs/skills/ui-iterate.md) |

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
