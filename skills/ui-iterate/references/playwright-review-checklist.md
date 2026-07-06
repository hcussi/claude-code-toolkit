# Playwright MCP review checklist

How to observe a running UI with the Playwright MCP so critiques are measured,
not guessed. Tool names below use the `mcp__playwright__` prefix; adjust it to
match the configured MCP server name.

## Setup

- Confirm the `browser_*` tools exist. If not, install the server
  (`claude mcp add playwright npx @playwright/mcp@latest`).
- Confirm the target URL responds before navigating.
- Optional, to avoid per-tool permission prompts, allowlist the browser tools in
  the project's `.claude/settings.local.json` (adjust the prefix to your server
  name):

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

## Per-review passes

1. **Navigate**: `browser_navigate` to the URL.
2. **Breakpoints**: `browser_resize` then `browser_take_screenshot` at:
   - Desktop 1440x900
   - Tablet 768 wide
   - Mobile 375 wide
   Note reflow, overflow, and whether touch targets stay >= 48px.
3. **Interaction states**: use `browser_hover` and `browser_click` to capture
   hover, focus-visible, and pressed states of buttons, links, and inputs.
   Confirm focus rings are visible.
4. **Computed styles**: `browser_evaluate` to read real values, for example:
   - `getComputedStyle(el).fontFamily` (does the intended webfont actually apply?)
   - background, text, and accent colors as rendered
   - padding/margins/gaps to check the spacing grid
   - contrast ratio of text against its background
5. **Accessibility**: `browser_snapshot` for the a11y tree: roles, accessible
   names/labels, heading order, and focus order.
6. **Modes**: if the app supports dark mode or reduced motion, emulate and
   re-screenshot to verify both paths are designed.

## Evidence

Attach a screenshot and a measured value to every finding. Prefer "heading
renders as Arial 24px, intended Geist" over "typography feels off". Keep the
per-round screenshots so before/after comparison is possible and regressions are
caught.
