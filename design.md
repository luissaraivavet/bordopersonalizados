# Design: Bordô

The locked system. Every Hallmark run reads this first and pages share it. Change it on purpose; the file is the rule.

## System
- Genre: editorial
- Shape of the first page: Catalogue (`index.html`); the three discovery pages use Split Studio
- Theme: brand (logo and bordô kept; Cormorant Garamond for display, Manrope for body; pale rosy paper)
- Axes: light/high-contrast-serif/chromatic-red · posture: full-palette

## Tokens
`assets/tokens.css` is the source of truth. The roles:
```css
:root {
  --color-paper: oklch(97.6% 0.008 30);  --color-paper-2: oklch(94.6% 0.017 15);  --color-paper-3: oklch(90.5% 0.026 10);
  --color-ink: oklch(22% 0.03 5);  --color-ink-2: oklch(38% 0.03 5);  --color-muted: oklch(50% 0.026 5);  --color-rule: oklch(86% 0.022 10);
  --color-accent: oklch(35.2% 0.1 4);  --color-accent-ink: oklch(97.6% 0.008 30);  --color-focus: oklch(40% 0.18 4);
  --color-display: oklch(30% 0.095 4);  --color-field: oklch(23.5% 0.072 4);  --color-gold-deep: oklch(58% 0.085 75);
  --font-display: "Cormorant Garamond", Georgia, ui-serif, serif;  --font-body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 2px;  --radius-arch: 999px 999px 2px 2px;  --radius-pill: 999px;  --rule-hair: 1px;  --shadow-card: none;
}
```
The spacing scale, the type scale, the easings and the durations are the scaffold's and live in `assets/tokens.css`. `assets/base.css` holds the base rules. Each page keeps its own CSS inline and imports both files.

## Roles
- Bordô is a highlight, never a field: headings (`--color-display`), the primary action (`--color-accent`) and the footer (`--color-field`), the one dark surface on a page.
- Paper is pale and rosy; `--color-paper-2` marks a band.
- Gold (`--color-gold-deep`) is the hairline under text links, nothing else.
- Arches (`--radius-arch`) frame the collection tabs and portraits only.
- Photographs are bright and photographic: natural window light, real fabric weight and contact shadows, no dark velvet backgrounds.
- Weights: Cormorant Garamond 500; Manrope 400 and 600.

## Controls
- Primary: bordô fill · pill · 52px tall
- Secondary: outline in `--color-muted`, bordô text · same radius and height

## Motion
- Character: calm; one rise-and-fade reveal on scroll, a short entrance in the hero and on collection change; under reduced motion everything ends at once.
- Signature: the running stitch. The active collection tab is underlined by a dashed bordô line sewn in 16 steps (640ms) when the collection changes.
- Feedback: in the bag, a new piece rises in and a changed quantity and price tick (220ms); the form error and the toast fade in. FAQ answers open with animated height where the browser supports `interpolate-size`.

## Exports
`assets/tokens.css` in this project. Tailwind, DTCG or shadcn blocks are added here on request.
