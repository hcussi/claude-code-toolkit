---
name: medium-article
description: "Turn an implemented PLAN.md into a Medium-style technical article: learn the author's voice from example articles, read the plan and its real code, draft a Markdown article, iterate with the user until approved, then drive Medium through the Playwright MCP to create a DRAFT (the user logs in manually; it never publishes). Use to write and stage a Medium post from a finished implementation. Writes files and controls a browser, so it is user-invoked only."
disable-model-invocation: true
argument-hint: <path-to-PLAN.md>
---

# medium-article

Write a Medium-style article from an implemented `PLAN.md` and stage it on Medium
as a **draft**. The article's code and config are lifted from the real
implementation, the voice is calibrated from the author's own example posts, and
publishing is deliberately **draft-only** with the human logging in.

Like `ui-iterate`, this is a **human-in-the-loop skill**, not a one-shot agent:
it pauses for the user's review of the draft and for the user's manual Medium
login. It bundles two references:

- `references/article-style-rubric.md`: how to extract a style guide from example
  articles, and the structure and voice to target.
- `references/medium-publish-playbook.md`: the Playwright, draft-only, human-in-
  the-loop publishing playbook (login polling, editor tactics, image upload, the
  never-publish rule, and the import-from-URL fallback).

## Argument

One argument: the path to the **implemented** `PLAN.md` (for example
`$ARGUMENTS`). If missing, ask for it. Absolutize it before reading.

## Guardrails (read first)

- **Draft only. Never publish.** The flow stops at a Medium draft; the user
  reviews formatting and clicks Publish themselves.
- **The user logs in; you never handle credentials.** Hand control over for
  login and poll for a logged-in signal (see the playbook). Never script auth.
- **Code and config are lifted from the real implementation**, never invented.
  If you cannot find a snippet in the repo, do not write it as fact.
- **No em dashes** anywhere (the user's global rule), even though the sample
  Medium posts use them. Use commas, colons, parentheses, or two sentences.
- **Review gate is mandatory.** Do not touch Medium until the user approves the
  Markdown draft.

## Workflow

### 1. Inputs and style calibration

- Confirm the PLAN path. Ask the user for **1 to 3 example Medium article URLs**
  to learn tone. Default to their own posts (for example the profile
  `https://medium.com/@hernncussi`) and to any local prior article they point at
  (for example a previous `*-article.md`).
- `WebFetch` each example and extract a short **style guide** following
  `references/article-style-rubric.md` (title/subtitle pattern, opening hook,
  section beats, voice, code presentation, closing CTA, series continuity).
- Ask whether this is part of a **series** ("Part N"); if so, note the prior
  article to reference in the opening.

### 2. Understand the implementation

- Read the PLAN and the **real** referenced files in the repo (code, config,
  `README.md`), so every snippet is quoted from source. Note the repo, the key
  files per component, and the verification / end-to-end steps that become the
  article's "prove it" section.

### 3. Draft the Markdown

- Write the draft to `<plan-stem>-article.md` next to the PLAN (or a path the
  user gives). Follow the target structure from the rubric: a
  `"[Doing X] with [Tool A, Tool B, Tool C]"` title plus a one-line subtitle; a
  problem-first hook (referencing the prior part if a series); component-per-
  section beats (vocabulary, then per service, then integration / threat model,
  then closing); code blocks lifted from the implementation; **mermaid** diagrams
  where the source article would have a figure; and a mirrored closing with a
  clone-and-run call to action.
- Match the author's voice: first person plus direct second-person address,
  present tense, **bold** on key terms and tool names. Keep the no-em-dash rule.

### 4. Review loop (human gate)

- Present the draft and iterate on the user's feedback, editing the MD each round,
  until they **explicitly approve**. Do not proceed past this point without
  sign-off.

### 5. Render diagrams

- Reuse the `mermaid-to-images` skill
  (`skills/mermaid-to-images/scripts/mermaid_to_images.py`) to render the draft's
  mermaid blocks to `diagram-N.png` files for upload. That script is the only
  renderer; do not render diagrams by hand. Keep the mermaid source in the
  canonical MD; the PNGs are for the Medium upload step.

### 6. Publish to Medium (draft only, human-in-the-loop)

Follow `references/medium-publish-playbook.md`. In short:

- **Preflight**: confirm the Playwright MCP (`browser_*` tools) is available; if
  not, tell the user to install it (`claude mcp add playwright npx @playwright/mcp@latest`)
  and stop.
- **Login**: navigate to `https://medium.com/m/signin`, hand control to the user,
  then wait for a logged-in marker with a long timeout. Never script the auth.
- **Create draft**: open `https://medium.com/new-story`; type the title, subtitle,
  and body; build headings, code blocks, and links by driving the editor toolbars
  (re-locate them with `browser_snapshot` before each action); insert images via
  the "+" menu and `browser_file_upload` using the rendered PNGs.
- **Never click Publish.** Report the draft URL and list what likely needs manual
  touch-up (code block formatting, image placement and captions).
- **Fallback**: if the article is hosted at a public URL, automate Medium's
  "Import a story" instead of driving the editor (much less fragile).

## When to stop

Stop and hand back after the draft is staged on Medium (or after the user
approves the MD if they decline the Medium step). Do not commit, push, or publish
unless the user explicitly asks.
