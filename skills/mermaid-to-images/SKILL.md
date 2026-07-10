---
name: mermaid-to-images
description: "Turn a Markdown file's diagrams into image files and rewrite each block as a Markdown image reference. Handles two sources: ```mermaid fenced blocks (rendered directly) and hand-drawn ASCII diagrams in plain fences (sequence/flow/box art), which are first translated to equivalent mermaid and then rendered. Uses mermaid-cli (mmdc) offline when available, or the hosted mermaid.ink service otherwise. Use when a Markdown doc must show diagrams in a viewer that does not render mermaid (many editors, PDF/print, some blog engines), or to promote ASCII art to real diagrams. Takes one argument: the path to the Markdown file. Edits the file in place, so it is user-invoked only."
disable-model-invocation: true
argument-hint: <path-to-markdown-file>
---

# mermaid-to-images

> **Non-negotiable rules. Read these first; they override any instinct to be clever.**
>
> 1. **The bundled script is the ONLY renderer.** Every image is produced by
>    running `scripts/mermaid_to_images.py`. You MUST NOT render diagrams any
>    other way. Specifically forbidden: a headless browser or Playwright
>    screenshot, a local HTTP server (`http.server`), converting SVG to PNG
>    yourself, `@1x`/`@2x` intermediates, or drawing/editing an image by hand.
> 2. **If the script cannot render, STOP and report to the user.** A failure
>    (no `mmdc`, no network to mermaid.ink) is a hard stop, not a problem to route
>    around. Relay the script's error and its remediation; do not invent a
>    fallback renderer. Producing the image by other means is a failure, not a
>    save.
> 3. **Do not choose output names, formats, or folders.** The output is exactly
>    `diagram-N.png` inside `<md-stem>-diagrams/`. Never rename to something
>    "semantic" (e.g. `assets/big-picture.png`), never emit `.svg`, never save
>    `.mmd` source, never write a `mermaid-config.json`.
> 4. **Your only edits to the doc** are: (a) turning an ASCII diagram fence into a
>    ` ```mermaid ` fence (with a `%% alt:` comment), and (b) running the script,
>    which does the fence-to-image rewrite. Nothing else.
>
> If any rule pushes you toward more work, you are misreading it: the goal is a
> boring, identical result every run. When blocked, stopping is the correct
> outcome.

Turn the diagrams in a Markdown file into image files and replace each block, in
place, with a Markdown image reference such as
`![A browser calls the server tier ...](article-diagrams/diagram-1.png)`. Images
land in a sibling folder named `<md-stem>-diagrams/` next to the document. Two
kinds of source are handled:

- **` ```mermaid ` fenced blocks** — rendered directly by the bundled script.
- **ASCII diagrams in plain fences** (hand-drawn sequence, flow, or box art) —
  *you* translate each into an equivalent mermaid diagram first, then the script
  renders it. This step is model work: ASCII art is not machine-parseable, and
  telling a real diagram from ordinary text is a judgment call.

## Do the rendering with the script (do not improvise)

All rendering and rewriting is done by the bundled, deterministic script
(`scripts/mermaid_to_images.py`, standard library only). **Always run it.** Your
job is to author mermaid (for ASCII diagrams) and to run the script; it is not to
render diagrams by hand.

This keeps every run identical and predictable:

- **Never** call `mmdc` or `mermaid.ink` yourself, hand-encode a URL, or write the
  image reference by hand. The script owns extraction, rendering, and the rewrite.
- The only outputs are `diagram-N.png` files. **Do not** produce `.svg`, save
  `.mmd` source, or write a `mermaid-config.json` or any other side artifact.
- Output is **PNG only** (the script default). Do not switch to SVG.
- Filenames are `diagram-1.png`, `diagram-2.png`, ... in document order, not
  semantic names. Re-running overwrites them in place rather than accumulating.
- Alt text is descriptive, sourced from a `%% alt:` comment you put in the block
  (see "Translating ASCII diagrams"); the script applies it deterministically.

The script also has a `--snippet OUT` preview mode (reads one mermaid diagram from
stdin, renders it to `OUT`) for checking a translation before writing it into the
doc. Previews go to a scratch path, never into the document's diagram folder.

## Argument

One argument: the path to the Markdown file to process (for example
`$ARGUMENTS`). If it is missing, ask the user for it. Resolve it to an absolute
path before running.

## Renderer

Two backends, selected by the script's `--renderer` flag (default `auto`):

- **`mmdc`** (mermaid-cli): renders fully offline, best fidelity, respects
  themes cleanly. Requires the `mmdc` binary on `PATH`
  (`npm install -g @mermaid-js/mermaid-cli`).
- **`ink`** (mermaid.ink): the hosted renderer the user referenced; needs
  network access. `auto` falls back to this when `mmdc` is absent.

Prefer `mmdc` when it is installed. **If neither `mmdc` nor network access is
available, the script will fail: that is a hard stop.** Report the script's error
and remediation (install `mmdc`, or enable network for the command) and wait for
the user. Do not reach for a browser, a local server, or any other renderer to
get around it. A missing renderer is the user's to resolve, not yours to
engineer around.

## Steps

1. **Resolve the file.** Confirm the argument points to an existing Markdown
   file. Absolutize the path.
2. **Survey the diagrams.** Two passes:
   - Count ` ```mermaid ` blocks (for example `grep -c '```mermaid' <file>`).
   - Scan the plain ` ``` ` fences for **ASCII diagrams** (see "Translating ASCII
     diagrams" below). If there are neither, say so and stop.
3. **Pick the renderer.** Detect `mmdc` (`command -v mmdc`). Use it if present;
   otherwise use `ink` and note that it needs network access. The `ink` backend
   reaches `https://mermaid.ink`, so if the environment sandboxes network the
   Bash call may need network access enabled.
4. **Translate ASCII diagrams to mermaid** (skip if there are none). For each
   ASCII diagram you and the user agree to convert, replace the plain fence's
   contents with an equivalent ` ```mermaid ` block, editing the source file
   directly. Preview first (see below) so a bad translation never lands.
5. **Run the script**, defaulting to `--backup` (a transient safety net: the
   `.bak` is written before the overwrite and removed on success, so nothing is
   left behind unless the write fails):

   ```bash
   python3 skills/mermaid-to-images/scripts/mermaid_to_images.py \
     "<absolute-md-path>" --backup
   ```

   This converts every ` ```mermaid ` block (native plus the ones you just
   authored) to PNG images and rewrites each fence as an image reference. Leave
   the defaults alone: they produce `diagram-N.png` deterministically. Add
   `--renderer mmdc|ink`, `--theme <name>`, `--background <color>`, or
   `--out <dir>` only when the user explicitly asks; do not reach for `--format
   svg`. Copy the script alongside the skill when it has been installed into a
   project's `.claude/skills/`.
6. **Report.** State how many blocks were converted (mermaid vs ASCII-derived),
   where the images were written, and that the Markdown now references them. If
   the user is inside a git repo, suggest reviewing the diff before committing.

## Idempotency and determinism

The conversion is designed to be repeatable and side-effect-free:

- **Deterministic names.** Blocks become `diagram-1.png`, `diagram-2.png`, ... in
  document order. A re-run overwrites the same files in place; it never creates a
  `diagram-3.png` variant or a semantically named copy.
- **Safe re-runs.** Once a fence is replaced by an image reference there is no
  ` ```mermaid ` block left, so running the script again is a no-op ("No mermaid
  blocks found"). It will not double-convert or duplicate images.
- **No stray artifacts.** The only thing written under `<md-stem>-diagrams/` is
  the `diagram-N.png` set. If you see `.svg`, `.mmd`, or `*-config.json` files
  there, they did not come from this script and should not be created.
- **One writer.** Only the script edits the Markdown and the image folder. If you
  need to change a rendered diagram, edit its mermaid source (re-inserting the
  ` ```mermaid ` block if it was already converted) and run the script again,
  rather than editing the PNG or the reference by hand.

## Translating ASCII diagrams

ASCII art is not machine-parseable, so this is model work, not something the
script can do. Be conservative and get the user's sign-off before rewriting.

1. **Decide what is actually a diagram.** Convert only blocks that *draw* a
   structure: sequence diagrams (lifelines with arrows between actors), flow or
   box-and-arrow diagrams, state machines. **Do not** convert code, JSON, config,
   or **console/log output** just because it contains `->` or `|`. For example
   `GET /hello (same jti twice) -> 200, then 401` is log output, not a diagram,
   even though a naive scan flags the arrow.
2. **Author the mermaid.** Reproduce the actors/nodes, the messages/edges, their
   order and direction, and any inline notes. Pick the fitting diagram type
   (`sequenceDiagram` for actor-to-actor message flows, `flowchart` for
   box-and-arrow). Keep labels faithful to the original wording.
3. **Add descriptive alt text.** Put a `%% alt:` comment inside the block, one
   sentence describing what the diagram shows. Mermaid ignores `%%` comments, so
   it does not affect the render; the script reads it and uses it as the image's
   alt text (falling back to `Diagram N` if you omit it). For example:

   ```
   sequenceDiagram
     %% alt: A single protected call: the browser sends a session cookie to the Next.js server tier, which signs a DPoP proof and calls Spring Boot; the backend verifies the proof against cnf.jkt and returns the greeting.
     ...
   ```
4. **Give the boxes breathing room.** Mermaid's defaults pack text tight against
   box borders, and long actor labels make some boxes far wider than others. Add
   an `init` directive that increases the internal margins and wraps long labels
   so boxes are padded and evenly sized. For a `sequenceDiagram`, a good starting
   point (tune per diagram, and preview) is:

   ```
   %%{init: {"sequence": {"noteMargin": 18, "boxTextMargin": 10, "boxMargin": 12, "messageMargin": 40, "wrap": true, "width": 200}}}%%
   ```

   `wrap` plus a fixed `width` is the only way to add horizontal padding to actor
   boxes (mermaid otherwise sizes them tight to the label); raise `width` if a
   message label wraps when you did not want it to.
5. **Preview before writing** with snippet mode, then look at the result:

   ```bash
   python3 skills/mermaid-to-images/scripts/mermaid_to_images.py \
     --snippet /tmp/preview.png <<'MMD'
   sequenceDiagram
     ...your translation...
   MMD
   ```

   Read the produced image and compare it against the ASCII source. Fix the
   mermaid (and the padding) and re-preview until it matches and reads cleanly.
6. **Confirm with the user**, especially when several blocks are borderline.
   Show which blocks you plan to convert and which you are leaving as text, then
   rewrite the agreed fences in the source (step 4 of the main steps) and run the
   script.

## Guardrails

- The script edits the Markdown in place. Always run with `--backup` (or confirm
  the file is tracked in git) so the original is recoverable. The `.bak` is
  transient: it is removed automatically once the rewrite succeeds, and kept only
  if the write itself fails.
- Do not hand-edit ` ```mermaid ` fences into image links yourself; let the
  script do that extraction and rewrite so indentation and offsets stay correct.
  Your only manual edit is turning an ASCII fence into a ` ```mermaid ` fence.
- Be conservative with ASCII: when a block is ambiguous, leave it as text and ask
  rather than guessing. A wrong diagram is worse than an untouched one.
- Keep images readable: the default background is opaque `white` on purpose.
  Mermaid draws message/edge labels in a light gray meant for a white backdrop,
  so a transparent PNG can make those labels vanish on dark surfaces. Only pass
  `--background transparent` when the doc is known to render on a light
  background.
- Do not commit or push the generated images or the edited file unless the user
  explicitly asks.
