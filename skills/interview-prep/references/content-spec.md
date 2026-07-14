# content.json specification

The build script (`scripts/build-editions.mjs`) reads one JSON file and injects it
into both HTML templates. Author this file per job. Both editions render from the
same content, so write it once, well.

## Schema

```json
{
  "meta": {
    "role": "Senior Backend Engineer",
    "tagline": "Company · primary stack in a few words",
    "heroTitle": "Short headline for the landing hero",
    "heroLead": "One or two sentences framing the pack and the company's context."
  },
  "categories": [
    {
      "id": "oop",
      "name": "OOP & SOLID",
      "sub": "One-line description shown under the topic title.",
      "blocks": [
        { "h": "Section heading", "html": "<ul><li>Reading notes as HTML.</li></ul>" }
      ],
      "qa": [
        ["A question an interviewer would actually ask?", "A crisp, correct answer."]
      ]
    }
  ]
}
```

### Fields

- **meta.role / meta.tagline**: fill the sidebar brand. Keep the tagline short
  (company + a few key technologies).
- **meta.heroTitle / meta.heroLead**: the landing header. `heroLead` is a good
  place to name the company's context (team size, product surface, stack) that the
  answers should tie back to.
- **categories[].id**: short, unique, kebab/lower (`oop`, `java`, `system-design`).
  Used for anchors and, in the tracker edition, to derive stable per-section
  checkbox ids. Do not reorder categories/blocks after someone has started
  tracking progress, or their saved checkmarks will shift.
- **categories[].name / .sub**: topic title and one-line subtitle.
- **blocks[]**: the readable units. Each `{ h, html }` becomes one section with,
  in the tracker edition, its own **Mark read** checkbox. `h` is plain text; `html`
  is a trusted HTML string. The number of blocks per topic follows the chosen
  preparation size (see the size table in `SKILL.md`).
- **qa[]**: array of `[question, answer]` string pairs. Rendered as click-to-reveal
  cards. Both strings are plain text (light inline HTML in the answer is fine). The
  number of Q&A per topic follows the chosen preparation size.

## HTML-in-JSON rules

The `html` strings are inserted verbatim via `innerHTML`. Because they live inside
JSON:

- Use **single quotes** for HTML attributes (`<span class='tag'>`) so you never
  need to escape double quotes inside JSON strings.
- Allowed building blocks (already styled by the templates):
  - `<ul>/<ol>/<li>`, `<p>`, `<strong>`, `<em>`, `<code>`, `<blockquote>`.
  - Tables: wrap in `<div class='tablewrap'>...<table>...</table></div>` so wide
    tables scroll instead of breaking the layout.
  - Callouts: `<div class='callout'>` (neutral/warn tone),
    `<div class='callout tip'>` (positive), `<div class='callout warn'>` (danger),
    each starting with `<span class='tag'>LABEL</span>`.
- Keep snippets short; this is study material, not documentation. Prefer bullets
  over long paragraphs.
- Do not include `<script>`, external images, or webfonts. The templates are
  self-contained and the build escapes stray `</script>` defensively, but keep
  content inert.

## Depth and quality bar

- **Explain mechanisms, not just names.** "volatile guarantees visibility but not
  atomicity" beats "volatile is a keyword."
- **Name the tradeoff and when it flips.** For every pattern, say what it costs and
  when you would NOT use it. This is what reads as senior.
- **Tie to the company's context.** Reference the actual stack/domain from the JD
  (for example: if they run Postgres, mention row-level security and isolation
  levels; if mobile-first, mention idempotency and cursor pagination). Put the
  framing in `heroLead` and reinforce it in callouts.
- **Q&A should be interview-shaped.** Write the question the way a person would ask
  it out loud, and answer in 2 to 5 sentences.
- **Scale depth to the chosen size.** For `short`, keep only the highest-yield
  point in each block; for `large` and `xl`, add edge cases, a second tradeoff, and
  follow-up Q&A. Do not pad: more material must mean more substance, not repetition.

## House style

- **No em dashes** anywhere. Use commas, colons, parentheses, or two sentences.
- Prefer active voice and concrete nouns.
- Do not fabricate JD requirements or candidate experience. If the JD is silent on
  something, either omit it or mark it as an assumption.

## Minimal example

```json
{
  "meta": {
    "role": "Backend Engineer",
    "tagline": "Acme · Go · Postgres · AWS",
    "heroTitle": "Prep for Acme",
    "heroLead": "Acme is a small team on a Postgres/AWS stack. Tie answers to that."
  },
  "categories": [
    {
      "id": "concurrency",
      "name": "Go Concurrency",
      "sub": "Goroutines, channels, the race detector.",
      "blocks": [
        { "h": "Goroutines & channels",
          "html": "<ul><li>Goroutines are cheap; the scheduler multiplexes them onto OS threads.</li><li><code>select</code> multiplexes channel ops; a <code>default</code> makes it non-blocking.</li></ul><div class='callout warn'><span class='tag'>Trap</span>A nil channel blocks forever; a closed channel is always ready.</div>" }
      ],
      "qa": [
        ["What is a data race, and how do you catch it?", "Concurrent access to the same memory with at least one write and no synchronization, giving undefined behavior. Catch it by running tests and the app with the -race detector, and fix with a mutex or by passing ownership through a channel."]
      ]
    }
  ]
}
```
