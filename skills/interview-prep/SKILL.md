---
name: interview-prep
description: "Prepare for a software-engineering interview (frontend, backend, or mobile) from a job description (a public URL or pasted text): fetch and parse the posting, detect the discipline, stack, and seniority, choose a preparation size (short, medium, large, or extra large), pick a matching topic track, author reading notes and click-to-reveal Q&A at that depth, then build two self-contained static HTML editions from bundled templates: a tracker edition (per-section read checkboxes + progress saved in the browser, to continue day to day) and a distraction-free reading edition. Output as local static files and/or publish each edition as a private Claude artifact. Use to prepare for an interview from a JD. Writes files, so it is user-invoked only."
disable-model-invocation: true
argument-hint: "<job-url-or-text> [| candidate background url-or-text] [size: short|medium|large|xl]"
---

# interview-prep

Turn a **job description** for a **software-engineering role (frontend, backend,
or mobile)** into a tailored interview study pack, and output two self-contained
static HTML editions from it:

- **Tracker edition** (`tracker.html`): sidebar table of contents, a live
  progress ring, per-section **Mark read** checkboxes, and a **Resume** button.
  Progress is saved in the browser's local storage, so the candidate can stop and
  pick up where they left off the next day.
- **Reading edition** (`reading.html`): the same content in a clean,
  distraction-free single scroll, no tracking.

Both editions are generated from **one content model** (`content.json`) by a
bundled build script, so the presentation is fixed and known-good and the only
thing authored per job is the tailored content.

This is a **content-authoring skill**: the real work is reading the JD, detecting
the discipline (frontend, backend, or mobile), and writing accurate, role-specific
material. The HTML is mechanical.

**Output modes.** The build step always writes self-contained **static HTML** files
that open in any browser with no server or network. On a host that supports hosted
pages (for example Claude Code's Artifact tool), you can additionally publish each
edition as a **private Claude artifact** and hand back a link. Offer both and let
the user pick one or both.

## Arguments

Free-form. Everything before an optional `|` is the **job description**;
everything after `|` is optional **candidate background**.

- **Job description** (required): a public URL (fetch with `WebFetch`) or pasted
  text. If it is a URL that redirects cross-host, follow the redirect.
- **Candidate background** (optional): a URL (LinkedIn, portfolio) or pasted
  resume text, used to bias topic selection and depth toward what the candidate
  already knows and to surface gaps. If a URL is a login-walled scrape (e.g.
  LinkedIn), treat the result as low-confidence and say so.
- **Size** (optional): one of `short`, `medium`, `large`, or `xl`, given anywhere
  in the input (for example `size: large`, or a bare `xl`). It sets how much
  material to generate (see **Preparation size** below). If omitted, ask the user
  which size they want; default to `medium` if they have no preference.

If no job description is given, ask for one before doing anything else.

## Preparation size

The size scales the number of topics, the read-blocks per topic, the Q&A per
topic, and the depth of each block. Use it as a target, not a hard rule; adjust to
what the role actually needs.

| Size | Topics | Blocks / topic | Q&A / topic | Depth and use |
| --- | --- | --- | --- | --- |
| `short` | 4 to 5 | 1 to 2 | 2 to 3 | Highest-yield essentials only, terse bullets. A night-before refresher. |
| `medium` | 6 to 8 | 2 to 3 | 3 to 5 | Solid shared core plus the key discipline topics. The default. |
| `large` | 9 to 12 | 3 to 5 | 5 to 7 | Broad coverage including cross-cutting topics and more edge cases. |
| `xl` | 12 to 16 | 4 to 8 | 6 to 10 | Comprehensive: adds framework-specifics, deeper prose, tradeoffs, and follow-up Q&A. |

Smaller sizes drop the lowest-priority topics first (keep the shared core and the
strongest discipline topics); larger sizes add cross-cutting and framework-specific
topics and go deeper within each block.

## Workflow

1. **Ingest the JD.** Fetch the URL or read the pasted text. Extract: role title,
   seniority, company/domain, required and preferred languages/frameworks, platform
   and data stack, responsibilities, and any interview-process hints. If a field is
   absent, do not invent it.
2. **Ingest background (if provided).** Extract the candidate's strongest stack
   and likely gaps. Flag anything that came from an unreliable scrape.
3. **Detect the discipline.** Classify the role as **frontend**, **backend**,
   **mobile**, or **fullstack** from the title, responsibilities, and stack (for
   example: React/CSS/browser signals frontend; services/DB/queues signal backend;
   iOS/Android/React Native/Flutter signal mobile). If it is genuinely ambiguous,
   ask the user which track to target. The discipline selects the topic track and
   shapes how shared topics (like system design) are framed.
4. **Settle the size.** Take the size from the input if given; otherwise ask which
   of `short` / `medium` / `large` / `xl` the user wants (default `medium`). The
   size sets the topic count, blocks per topic, Q&A per topic, and depth (see the
   **Preparation size** table).
5. **Select topics.** Use `references/topic-library.md` as a menu. Always include
   the shared core (fundamentals for the primary language, problem-solving/DS &
   algorithms, system design framed for the discipline, behavioral). Then add the
   discipline track and any stack/framework specifics the JD names (for example:
   Spring for Java backend; React + performance + accessibility for frontend;
   Swift/Kotlin lifecycle + offline for mobile; auth when the product ships login;
   AI-in-production when the JD mentions models). Let the chosen size set how many
   topics to keep (short trims to the highest-yield ones; xl adds cross-cutting and
   framework-specific topics).
6. **Author `content.json`.** Follow `references/content-spec.md` exactly (schema,
   HTML-in-JSON rules, depth, and the house style). Hit the blocks-per-topic and
   Q&A-per-topic counts for the chosen size. Name the discipline in `meta.heroLead`
   and tie tradeoffs back to *this* company's context (team size, product surface,
   named stack). No em dashes anywhere.
7. **Build the editions.** Run the build script:
   `node <skill>/scripts/build-editions.mjs <content.json> <output-dir>`
   It validates the content, injects it into both templates, and writes the static
   `tracker.html` and `reading.html`. Fix any validation error it reports and
   re-run.
8. **Verify.** Confirm the script reported the expected topic/block/Q&A counts, and
   that they roughly match the chosen size. Optionally open the files to eyeball
   rendering.
9. **Deliver, and let the user choose the format.** Report where the two static
   files are. Then offer, as separate options the user can pick one or both of:
   (a) keep the **static HTML** files as-is, and (b) if the host supports it (for
   example Claude Code's Artifact tool), publish each edition as a **private
   Claude artifact** and hand back the links. Do not publish anything publicly
   without asking.

## Bundled files

- `references/content-spec.md`: the `content.json` schema, the HTML-in-JSON
  authoring rules, depth guidance, and the house style (no em dashes, tie to
  context, senior framing).
- `references/topic-library.md`: a menu of interview topics with what each should
  cover and sample Q&A themes, so content is strong and consistent across runs.
- `references/tracker-edition.template.html` and
  `references/reading-edition.template.html`: the two self-contained templates
  with `META`/`DATA` injection points. Do not hand-edit their `DATA`; the build
  script fills it.
- `scripts/build-editions.mjs`: dependency-free Node builder
  (`node build-editions.mjs <content.json> [outDir]`).

## Guardrails

- **Ground everything in the JD.** Do not fabricate requirements, and do not
  claim a candidate has experience the background did not state.
- **Flag unreliable inputs.** LinkedIn and similar scrapes are often partial or
  wrong; label anything derived from them as unverified.
- **Private by default.** Never publish an edition to a public/shared location
  without explicit approval; prefer private artifacts.
- **No em dashes** anywhere (house rule). Use commas, colons, parentheses, or two
  sentences.
- **Do not commit or push.** Write the files, report, and stop.
