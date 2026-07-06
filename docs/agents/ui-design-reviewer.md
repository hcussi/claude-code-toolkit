# ui-design-reviewer

A read-only UI/UX reviewer that inspects a **running** web app through the
Playwright MCP and returns a prioritized, evidence-based critique. Instead of
guessing from source, it navigates the live UI, resizes to breakpoints,
captures interaction states, reads computed styles, and inspects the
accessibility tree, then judges what it observes against a **Material-informed
minimalism** bar. It recommends changes; it does not edit code.

**Agent file:** [`agents/ui-design-reviewer.md`](../../agents/ui-design-reviewer.md)

## Design bar

Material Design as the structural and behavioral guideline (8dp spacing grid,
color roles, elevation, state layers, motion, accessibility) while respecting
the project's own palette and identity. Minimalism as restraint: every element
must earn its place. It does not force a generic Material look onto a product
with its own visual language.

## What it inspects

- Screenshots at desktop / tablet / mobile breakpoints (reflow, overflow, touch
  targets).
- Hover, focus-visible, and pressed states of interactive elements.
- Computed styles (the font that actually renders, real colors, spacing, and
  measured contrast ratios), not source values.
- The accessibility tree: roles, labels, heading and focus order, visible focus.

## Prerequisites

- The **Playwright MCP** must be installed and its `browser_*` tools available
  (for example `claude mcp add playwright npx @playwright/mcp@latest`). The tool
  prefix in the agent's frontmatter must match the configured server name.
- The **app must be running**; the agent confirms the URL responds and otherwise
  asks for the dev server to be started rather than reviewing from source.

### Permissions (optional, to skip prompts)

Installing the MCP is mandatory; allowlisting is not, but without it Claude Code
prompts the first time each browser tool is used. The agent calls these eight
tools, so add them to the project's `.claude/settings.local.json` to run
prompt-free (adjust the `mcp__playwright__` prefix to your server name):

```json
{
  "permissions": {
    "allow": [
      "mcp__playwright__browser_navigate",
      "mcp__playwright__browser_resize",
      "mcp__playwright__browser_take_screenshot",
      "mcp__playwright__browser_snapshot",
      "mcp__playwright__browser_evaluate",
      "mcp__playwright__browser_hover",
      "mcp__playwright__browser_click",
      "mcp__playwright__browser_close"
    ]
  }
}
```

## Usage

Copy the agent file into a project's `.claude/agents/` directory (or into
`~/.claude/agents/` to make it available everywhere), then invoke it as
`ui-design-reviewer`, giving the target URL and which screens/states to review.
It pairs with the `ui-iterate` skill, which calls this agent as its per-round
critic.

## Output

Findings grouped by priority (High / Medium / Low), each with the screen and
element, measured evidence (a screenshot plus a value), why it matters against
the rubric, and a concrete recommended change, followed by a short note on what
already works so iterations do not regress strengths.
