# Article style rubric

How to calibrate voice from example articles, and the structure and voice to
target when drafting. The goal is an article that reads like the author wrote it,
grounded in a real implementation.

## Extracting a style guide from examples

For each example URL the user provides (`WebFetch` it), capture:

- **Title + subtitle pattern.** Note the shape. The recurring pattern here is a
  title `"[Doing X] with [Tool A, Tool B, Tool C]"` and a single subtitle line
  that is either a mechanism sentence or a short aphorism (for example "One
  Login, Two Assurance Levels").
- **Opening hook.** How the first paragraph earns attention: a cold declarative
  claim, or a named friction point, often with a callback to the prior article in
  a series ("In Part 2 we stood up a real login ...").
- **Section beats and order.** The heading sequence. Technical posts here mirror
  the request flow: vocabulary and definitions first, then one section per
  component (for example Keycloak, then Spring Boot, then Next.js), then an
  end-to-end / threat-model section, then a closing.
- **Voice.** First person (singular and plural) blended with direct second-person
  address to the reader, present tense, professional but conversational.
- **Section and paragraph length.** Usually 2 to 5 paragraphs per section,
  3 to 4 sentences per paragraph. Dense material is broken up with subsections.
- **Code presentation.** Inline backticks for identifiers, filenames, and config
  values; multi-line blocks quoted verbatim from the repo to illustrate a point.
- **Visuals.** Whether the post uses diagrams or screenshots, and that figures are
  captioned and placed inline near the relevant section.
- **Closing.** A concrete imperative call to action (clone, add one config line,
  run, click), and a restatement that mirrors the opening.
- **Signature tics.** Bold on key terms and tool names, compact near-aphoristic
  sentences, light metaphor ("seams" that must "agree"), numbered step lists.

Summarize these into a few bullet points and reuse them while drafting. Treat the
author's own posts as the canonical voice.

## Target structure for a plan-derived article

Most implementation write-ups map cleanly onto this skeleton (adapt to the topic):

1. **Hook (no heading).** The unsolved problem, made concrete (a real attack, a
   real limitation). If it is a series, open by recalling the prior part, then
   state what this iteration fixes. Name the mechanism and the versions. End the
   intro with a reproducibility promise ("clone the repo, `docker compose up`").
2. **The big picture.** One diagram plus a two or three sentence summary of the
   whole flow.
3. **The vocabulary.** Define the new artifacts claim-by-claim, each framed by
   what it is for.
4. **One section per component.** Mirror the plan's build order. Each section
   lifts the real config and code and explains the *why*, not just the *what*.
5. **Integration / threat model.** Prove the negatives: the end-to-end checks and
   what the mechanism does and does not defend. Do not overclaim.
6. **Closing.** Mirror the opener, restate the division of labor across
   components, acknowledge the cost honestly, and end with a clone-and-run CTA.

## What the article adds vs. lifts from the plan

- **Lift from the plan and code:** config keys, class and file names, the exact
  verification steps, the acceptance behavior. These must be real.
- **Add as narrative:** the motivating hook and concrete scenarios, analogies and
  framing, claim-by-claim walkthroughs, transitions, and the paired intro/closing.
- **Drop from the plan:** acceptance-mapping tables, risk checklists, deliverable
  checkboxes, and internal PRD cross-references. Keep the road taken, not the
  project-management scaffolding.

## Voice rules (non-negotiable)

- First person plus second-person address; present tense.
- **Bold** key terms and tool names on first use.
- **No em dashes.** Use commas, colons, parentheses, or two sentences. This
  overrides the sample articles, which use em dashes.
- Every code snippet and config value must come from the real implementation.
