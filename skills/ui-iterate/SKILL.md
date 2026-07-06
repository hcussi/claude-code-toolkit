---
name: ui-iterate
description: Drive an interactive UI redesign loop on a running web app: render it via the Playwright MCP, critique it (using the ui-design-reviewer agent) against Material-informed minimalism, apply edits, re-render, and repeat according to the user's feedback until they approve. Use when iterating on a screen's look and feel with a human in the loop. Writes code, so it is user-invoked only.
disable-model-invocation: true
---

# ui-iterate

Run a human-in-the-loop redesign cycle on a live UI. Each round: render the app,
critique it, agree on changes with the user, edit the code, re-render, and show
before/after, repeating until the user is satisfied. The design bar is
**Material-informed minimalism** (see
`references/material-minimalism-rubric.md`).

This skill drives the loop and edits files; it delegates the per-round critique
to the `ui-design-reviewer` agent so review stays consistent and evidence-based.

## Why this is a skill, not just an agent

A subagent runs once and returns; it cannot pause to collect the user's feedback
mid-run. This loop is inherently multi-turn and conversational, so it lives in
the main thread (this skill) and calls the `ui-design-reviewer` agent for the
autonomous critique each round.

## Preflight

1. Confirm the **Playwright MCP** is available (`browser_*` tools). If not, ask
   the user to install it (`claude mcp add playwright npx @playwright/mcp@latest`).
2. Confirm the **dev server is running** and get the target URL (for example
   `http://localhost:3000`). Start it if needed (for example `npm run dev` in the
   background) and wait until it responds.
3. Identify the files that own the screen (framework-specific: for Next.js,
   typically the page/component, global CSS, and layout). Discover them with
   Glob/Grep; do not assume paths.
4. Ask the user for goals and any hard constraints (brand palette, must-keep
   elements, do-not-touch areas).

## The loop

Repeat until the user approves:

1. **Render**: navigate and screenshot the current UI at desktop / tablet /
   mobile via the Playwright MCP.
2. **Critique**: invoke the `ui-design-reviewer` agent on the running URL to get
   a prioritized, measured critique. On the first round this is the baseline.
3. **Propose**: summarize the top changes for this round and confirm direction
   with the user before editing. Keep each round small and reviewable.
4. **Apply**: make scoped edits to the identified files only. Introduce design
   tokens rather than scattering magic values.
5. **Verify**: re-render and screenshot; run the project's lint and build (for
   example `npm run lint` and `npm run build`); re-check AA contrast on changed
   colors; confirm focus-visible rings survive.
6. **Show + ask**: present before/after screenshots and a one-line changelog of
   what changed, then ask the user for feedback. Apply it in the next round.

Maintain a running **changelog** and keep the before/after screenshots from each
round so nothing regresses silently and the user can revert a step.

## Guardrails

- Change only what the round calls for; do not refactor unrelated code.
- Respect the project's identity and palette; use Material as the structural and
  behavioral guideline, not a mandate to look like stock Material (see the
  rubric and `references/playwright-review-checklist.md`).
- Keep accessibility intact every round: contrast, semantics, focus, and
  reduced-motion / dark-mode correctness.
- Do not change behavior or break existing tests; if the project has e2e/UI
  tests, run them after substantive changes.
- Stop and hand back when the user says the design is good. Do not commit or push
  unless explicitly asked.
