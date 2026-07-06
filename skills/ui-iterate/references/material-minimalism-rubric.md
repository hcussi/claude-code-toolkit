# Material-informed minimalism rubric

The design bar for `ui-iterate` and `ui-design-reviewer`. Use Material Design as
the structural and behavioral guideline while respecting the project's own
palette and identity. Minimalism means restraint: every element earns its place;
whitespace is a feature.

## Layout and spacing

- Align to an 8dp grid (4dp for fine adjustments). Spacing should be a small,
  consistent set of steps, not arbitrary values.
- Establish clear regions and rhythm. Give content room; do not crowd.
- Responsive: verify desktop, tablet, and mobile. No horizontal overflow; touch
  targets at least 48x48dp.

## Color

- Use roles, not ad hoc colors: primary, on-primary, surface, on-surface, plus
  one restrained accent. Reserve accent for the primary action and key state.
- Contrast: body text >= 4.5:1, large text and UI components >= 3:1, measured on
  the actual surface color (not the intended one).
- Dark mode, if present, is designed on purpose: text and surface pair correctly,
  and contrast still passes.

## Typography

- A real type scale with genuine hierarchy (display / headline / title / body /
  label). One or two families.
- Confirm the font that actually renders matches the intended one (CSS overrides
  and fallbacks often defeat a loaded webfont).
- Legible sizes and line-height; tighten tracking on large headings only.

## Elevation and state

- Elevation communicates hierarchy, used sparingly. Prefer a hairline keyline or
  subtle shadow over heavy drop shadows.
- Every interactive element has visible state layers: hover, focus-visible, and
  pressed. Focus-visible rings must never be removed.

## Motion

- Short, purposeful, standard easing. Motion should guide attention or confirm an
  action, never decorate. Honor prefers-reduced-motion.

## Minimalism gate

- Remove decoration that carries no information.
- If an element does not aid comprehension or action, cut it or justify it.
- Fewer, better elements beat more elements.

## Identity (judged on its own terms)

- Material governs structure and behavior; the product's palette, brand mark, and
  voice are its own. A distinctive, non-default look is good as long as it stays
  consistent, accessible, and restrained.
