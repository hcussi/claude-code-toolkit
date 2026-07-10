# mermaid-to-images

A user-invoked skill that **turns a Markdown file's diagrams into image files**
and rewrites each block, in place, as a Markdown image reference. Point it at a
document and every diagram becomes a
`![Diagram N](<md-stem>-diagrams/diagram-N.png)` line backed by a real image, so
the doc renders in viewers that do not understand mermaid (many editors, PDF and
print, some static-site and blog engines).

It handles two sources:

- **` ```mermaid ` fenced blocks** are rendered directly by the bundled script.
- **Hand-drawn ASCII diagrams** in plain fences (sequence, flow, or box art) are
  first translated by the model into an equivalent mermaid diagram, then rendered
  the same way. This step is deliberately model-driven: ASCII art is not
  machine-parseable, and distinguishing a real diagram from ordinary text or log
  output (a line like `GET /hello -> 200` is not a diagram) is a judgment call a
  script cannot make reliably.

**Skill file:** [`skills/mermaid-to-images/SKILL.md`](../../skills/mermaid-to-images/SKILL.md)

## What it does

Given one argument (the path to a Markdown file), the skill:

1. Surveys the document for ` ```mermaid ` blocks and for ASCII diagrams in plain
   fences.
2. For each ASCII diagram it and the user agree to convert, authors an equivalent
   ` ```mermaid ` block (previewing it first via the script's `--snippet` mode)
   and rewrites that fence in the source.
3. Runs a bundled, standard-library Python script that renders every
   ` ```mermaid ` block (native plus translated) to an image in a sibling
   `<md-stem>-diagrams/` folder (`diagram-1`, `diagram-2`, ...) and replaces each
   fenced block, in place, with a relative-path image reference.

Re-running is safe: once the fences are replaced by images there is nothing left
to convert. Plain code fences that are *not* diagrams (code, JSON, config,
console output) are left untouched.

## Rendering backends

Selected with the script's `--renderer` flag (default `auto`):

- **`mmdc`** (mermaid-cli): renders fully offline with the best fidelity.
  Requires the `mmdc` binary on `PATH`
  (`npm install -g @mermaid-js/mermaid-cli`).
- **`ink`** (mermaid.ink): the hosted renderer; needs network access. `auto`
  uses `mmdc` when it is installed and falls back to `ink` otherwise.

## Options

The script accepts a few flags beyond the required Markdown path:

- `--renderer auto|mmdc|ink` (default `auto`)
- `--format png|svg` (default `png`)
- `--theme <name>` (mermaid theme, default `default`)
- `--out <dir>` (output folder; default `<md-stem>-diagrams` next to the file)
- `--background <color>` (image background: `white`, `#ffffff`, or
  `transparent`; default `white`). An opaque background keeps mermaid's gray
  message labels readable; a transparent PNG can make them vanish on dark
  surfaces. Applies to both the `mmdc` and `ink` backends.
- `--backup` (write a transient `<file>.bak` before editing and remove it once
  the rewrite succeeds; kept only if the write fails, for recovery)
- `--snippet <out>` (render one mermaid diagram read from stdin to `<out>` and
  exit, touching no Markdown file; used to preview an ASCII translation before
  committing it into the doc)

## Usage

Copy the skill directory into a project's `.claude/skills/` (or
`~/.claude/skills/` to make it available everywhere), then invoke it as
`/mermaid-to-images <path-to-markdown-file>`. Example:

```
/mermaid-to-images docs/architecture.md
```

It is user-invoked only, since it edits the Markdown file in place. The skill
runs with `--backup` by default; the `.bak` is a transient safety net that is
removed once the rewrite succeeds (kept only if the write fails), so no backup
file is left behind. In a git repo it suggests reviewing the diff, and it does
not commit or push the generated images or the edited file unless asked.

## Prerequisites

- `python3` on `PATH` (standard library only; no pip installs needed).
- For offline rendering: `mmdc` (`npm install -g @mermaid-js/mermaid-cli`).
- For the hosted renderer: outbound network access to `https://mermaid.ink`.

## Scope

Diagrams only: ` ```mermaid ` blocks and ASCII art that clearly draws a diagram.
It does not restyle diagrams, rewrite non-diagram content, or manage image
hosting; the images are written to a local folder and referenced by relative
path. ASCII translation is conservative and asks for confirmation on ambiguous
blocks, since a misread diagram is worse than one left as text.
