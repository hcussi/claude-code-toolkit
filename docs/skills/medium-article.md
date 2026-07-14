# medium-article

A user-invoked skill that turns an **implemented `PLAN.md` into a Medium-style
technical article** and stages it on Medium as a **draft**. It calibrates the
author's voice from example posts, lifts code and config from the real
implementation, drafts a Markdown article, iterates with the user until approved,
and only then drives Medium through the Playwright MCP, with the user logging in
manually and no auto-publish.

**Skill file:** [`skills/medium-article/SKILL.md`](../../skills/medium-article/SKILL.md)

## Why a skill (not an agent)

The workflow is multi-turn and gated on the human: ask for style examples, draft,
**wait for the user's review**, **wait for the user's Medium login**, then stage
the post. A one-shot subagent cannot pause for approval or login mid-run, so the
driver lives in the main thread as a skill (the same reason `ui-iterate` is a
skill). It reuses the `mermaid-to-images` skill to render diagrams and the same
`browser_*` Playwright MCP tools the `ui-design-reviewer` agent uses.

## Workflow

1. **Inputs and style calibration.** Take the implemented PLAN path; ask for 1 to
   3 example Medium URLs (defaulting to the author's own posts), `WebFetch` them,
   and extract a style guide (title/subtitle pattern, hook, section beats, voice,
   code presentation, closing CTA, series continuity).
2. **Understand the implementation.** Read the PLAN and the real referenced code,
   config, and README so every snippet is quoted from source.
3. **Draft the Markdown.** Write `<plan-stem>-article.md` in the author's voice
   and the observed structure (title + subtitle, problem-first hook, component-
   per-section beats, integration / threat-model, mirrored closing with a clone-
   and-run CTA). Diagrams are authored as mermaid.
4. **Review loop.** Present the draft and iterate until the user explicitly
   approves. Nothing touches Medium before sign-off.
5. **Render diagrams.** Reuse `mermaid-to-images` to render mermaid blocks to
   `diagram-N.png` for upload.
6. **Publish to Medium (draft only).** Preflight the Playwright MCP; navigate to
   sign-in and wait for the user to log in; open a new story; type title,
   subtitle, and body; build headings, code blocks, links, and image uploads via
   the editor toolbars. It never clicks Publish; it reports the draft URL and what
   needs manual touch-up. A less fragile "Import a story from a public URL"
   fallback is documented.

## Bundled references

- `references/article-style-rubric.md`: how to extract a style guide from example
  articles, the target structure, and the voice rules (including no em dashes).
- `references/medium-publish-playbook.md`: the Playwright, human-in-the-loop,
  draft-only publishing playbook (login polling, editor tactics, image upload, the
  never-publish rule, and the import-from-URL fallback).

## Prerequisites

- An **implemented `PLAN.md`** and access to its repo (code is lifted from source).
- The **Playwright MCP** installed (`browser_*` tools) for the publish step.
- Network access for `WebFetch` (style examples) and for `mermaid-to-images` if it
  renders via mermaid.ink rather than a local `mmdc`.
- A **Medium account**; the user logs in manually during the run.

## Usage

Copy the skill directory into a project's `.claude/skills/` (or `~/.claude/skills/`
to make it available everywhere), then invoke it as
`/medium-article <path-to-PLAN.md>`. It is user-invoked only, since it writes
files and controls a browser.

## Scope and safety

- **Draft only.** It never publishes; the user reviews formatting and publishes
  manually.
- **The user logs in.** It never scripts authentication or handles credentials.
- **Facts come from the implementation.** Code and config are quoted from the
  repo, not invented.
- It does not commit or push, and follows the house rule of no em dashes even
  though the sample Medium posts use them.
