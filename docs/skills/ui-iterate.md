# ui-iterate

A user-invoked skill that runs a **human-in-the-loop UI redesign cycle** on a
running web app. Each round it renders the app via the Playwright MCP, critiques
it (delegating to the `ui-design-reviewer` agent), agrees the changes with the
user, edits the code, re-renders, and shows before/after, repeating until the
user approves. The design bar is **Material-informed minimalism**.

**Skill file:** [`skills/ui-iterate/SKILL.md`](../../skills/ui-iterate/SKILL.md)

## Why a skill plus an agent

A subagent runs once and returns; it cannot pause to collect the user's feedback
mid-run. The iterate-with-feedback loop is inherently multi-turn, so it lives in
the main thread (this skill), which edits files and talks to the user, and calls
the read-only `ui-design-reviewer` agent for the autonomous per-round critique.
Clean split: the agent is the critic, the skill is the driver.

## The loop

1. **Preflight**: confirm the Playwright MCP is available and the dev server is
   running; identify the files that own the screen; gather goals and constraints.
2. **Render**: screenshot the current UI at desktop / tablet / mobile.
3. **Critique**: invoke `ui-design-reviewer` on the running URL.
4. **Propose**: confirm the round's changes with the user before editing.
5. **Apply**: scoped edits to the identified files, using design tokens.
6. **Verify**: re-render, run lint and build, re-check AA contrast and focus
   rings.
7. **Show and ask**: present before/after plus a changelog, take feedback, and
   loop until approved.

## Bundled references

- `references/material-minimalism-rubric.md`: the design bar (shared with the
  agent).
- `references/playwright-review-checklist.md`: how to observe a running UI with
  the Playwright MCP (breakpoints, states, computed styles, accessibility).

## Prerequisites

- The **Playwright MCP** installed (`browser_*` tools available).
- The **dev server running** at a known URL.
- Optional: allowlist the browser tools to skip per-tool permission prompts. See
  the `browser_*` snippet in `references/playwright-review-checklist.md` (also in
  the `ui-design-reviewer` agent doc).

## Usage

Copy the skill directory into a project's `.claude/skills/` (or `~/.claude/skills/`
to make it available everywhere), then invoke it as `/ui-iterate`. It is
user-invoked only, since it writes code. It stops and hands back when the user is
satisfied, and does not commit or push unless explicitly asked.

## Scope

UI look and feel only. It does not change app behavior or business logic, and it
keeps accessibility intact each round. It respects the project's palette and
identity, using Material as the structural and behavioral guideline rather than a
mandate to look like stock Material.
