# interview-prep

A user-invoked skill that turns a **job description** (a public URL or pasted
text) for a **software-engineering role (frontend, backend, or mobile)** into a
**tailored interview study pack** and builds two self-contained static HTML
editions from it: a **tracker edition** with per-section read checkboxes and
progress saved in the browser, and a distraction-free **reading edition**. The pack
is generated at a chosen **preparation size** (`short`, `medium`, `large`, or
`xl`), and both editions can be kept as local static files and/or published as
**private Claude artifacts**.

**Skill file:** [`skills/interview-prep/SKILL.md`](../../skills/interview-prep/SKILL.md)

## Why a skill (not an agent)

The workflow is multi-turn and produces files: fetch and parse the JD, optionally
weigh the candidate's background, pick topics, author tailored content, build the
editions, and offer to publish them. That authoring loop and the file output are a
better fit for a skill in the main thread than a one-shot subagent (the same
reason `medium-article` is a skill). It also mirrors the split used elsewhere in
the toolkit: the model authors content, a bundled script does the deterministic
rendering.

## How it works

Both editions render from **one content model** (`content.json`). The skill's real
work is reading the JD, detecting the discipline (frontend, backend, or mobile), and
authoring accurate, role-specific material; a bundled, dependency-free Node script
injects that content into two fixed HTML templates, so the presentation is
known-good and only the content changes per job. The build output is always
self-contained **static HTML**; publishing to a **private Claude artifact** is an
optional extra delivery mode.

## Workflow

1. **Ingest the JD.** `WebFetch` the URL (following cross-host redirects) or read
   pasted text. Extract role, seniority, company/domain, languages/frameworks,
   platform/data stack, responsibilities, and interview hints. Nothing is invented.
2. **Ingest background (optional).** A LinkedIn/portfolio URL or resume text biases
   topic selection and depth. Login-walled scrapes are treated as low-confidence
   and flagged.
3. **Detect the discipline** (frontend, backend, mobile, or fullstack) from the
   title, responsibilities, and stack; ask the user if it is genuinely ambiguous.
   The discipline picks the topic track and frames shared topics like system design.
4. **Settle the size** (`short`, `medium`, `large`, or `xl`) from the input, or ask
   (default `medium`). Size sets the topic count, blocks per topic, Q&A per topic,
   and depth.
5. **Select topics** from `references/topic-library.md`: always the shared core
   (language fundamentals, DS & algorithms, system design framed for the discipline,
   behavioral) plus the discipline track and any stack/framework specifics the JD
   names, trimmed or expanded to the chosen size.
6. **Author `content.json`** per `references/content-spec.md` (schema, HTML-in-JSON
   rules, depth, house style), hitting the size's per-topic counts, naming the
   discipline, and tying tradeoffs back to the company's context.
7. **Build** with `node scripts/build-editions.mjs <content.json> <out-dir>`, which
   validates the content and writes the static `tracker.html` and `reading.html`.
8. **Verify** the reported topic/block/Q&A counts and optionally eyeball the pages.
9. **Deliver in the chosen format.** Keep the **static HTML** files, and/or, if the
   environment supports hosted pages (for example Claude Code's Artifact tool),
   publish each edition as a **private Claude artifact**. Nothing is published
   publicly without approval.

## The two editions

- **Tracker edition** (`tracker.html`): sidebar table of contents, a progress ring,
  per-section **Mark read** checkboxes, and a **Resume** button. Progress persists
  in the browser's local storage, so the candidate can continue across days.
  Per-section state is keyed off `category id + block position`, so reordering
  content after progress exists would shift the saved marks.
- **Reading edition** (`reading.html`): the same topics and Q&A in a clean single
  scroll with no tracking, for reading straight through.

Both are single self-contained files (inline CSS/JS, no network, no webfonts),
theme-aware (light/dark), and responsive.

## Bundled files

- `references/content-spec.md`: the `content.json` schema and authoring rules.
- `references/topic-library.md`: the topic menu (coverage + Q&A themes per topic).
- `references/tracker-edition.template.html`, `references/reading-edition.template.html`:
  the two templates with `META`/`DATA` injection points (do not hand-edit `DATA`).
- `scripts/build-editions.mjs`: the dependency-free builder.

## Prerequisites

- **Node.js** for the build script (no packages required).
- **Network access** for `WebFetch` when the JD or background is a URL.
- Optionally a host that can publish **private** artifacts/hosted pages for the
  final share step.

## Usage

Copy the skill directory into a project's `.claude/skills/` (or
`~/.claude/skills/` to make it available everywhere), then invoke it as
`/interview-prep <job-url-or-text>`, optionally with
`| <candidate background url-or-text>` after a pipe and a size keyword
(`short`, `medium`, `large`, or `xl`; for example `size: large`). It is
user-invoked only, since it writes files.

## Scope and safety

- **Grounded in the JD.** It does not fabricate requirements or claim unstated
  candidate experience, and it flags anything derived from an unreliable scrape.
- **Private by default.** Editions are shared only privately unless the user
  explicitly approves a public location.
- It does not commit or push, and follows the house rule of no em dashes.
