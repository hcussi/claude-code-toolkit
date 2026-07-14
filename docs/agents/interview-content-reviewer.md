# interview-content-reviewer

A read-only quality gate for the `interview-prep` skill. It reviews a single
`content.json` against the schema, the house style, and the depth bar **before**
the pack is built and shipped, and returns a prioritized findings report. It is a
reviewer, not an author: it never edits files.

**Agent file:** [`agents/interview-content-reviewer.md`](../../agents/interview-content-reviewer.md)

## When to use it

- After authoring or editing a pack's `content.json`.
- When asked to review or QA a prep pack.
- Before running `build-editions.mjs`, to catch hard build failures early.

## What it checks

Working from the skill's own spec (`references/content-spec.md` and the SKILL.md
size table), in priority order:

1. **Schema validity** the build enforces: `meta` fields, unique category ids,
   non-empty `blocks`, plain-text `h` plus non-empty `html`, and `qa` as
   `[question, answer]` string pairs.
2. **House style (blocking):** no em dashes anywhere (including the ` - ` smuggled
   in as one), and no fabricated JD requirements or unsupported claimed experience.
3. **HTML-in-JSON rules:** single-quoted attributes, `tablewrap` for wide tables,
   `tag` label spans for callouts, no `<script>`/external images/webfonts, no
   malformed tags.
4. **Size fit:** topic count, blocks-per-topic, and Q&A-per-topic against the
   size table, reported per topic.
5. **Depth and senior framing:** mechanisms over names, each pattern with its
   tradeoff, ties to the company's real stack, interviewer-phrased Q&A, no padding.
6. **Correctness:** any technically wrong or misleading claim (the highest-impact
   check).

It prefers mechanical checks over eyeballing: `grep` for em dashes, and a
throwaway `build-editions.mjs` run to confirm the JSON parses and to read back the
real topic / block / Q&A counts.

## Output

A concise report, most severe first:

- **Verdict:** `ship` / `fix first` / `blocked` (build will fail).
- **Blocking issues** (schema, em dashes, fabrication, wrong claims), each with
  the exact location, the quoted text, and the concrete fix.
- **Should fix** (size misses, thin depth, weak framing, HTML violations).
- **Nice to have** (smaller polish).
- **Counts:** reported topics / blocks / Q&A vs. the target for the size.

It points precisely at what is wrong and what the fix is, and leaves the change to
the author.
