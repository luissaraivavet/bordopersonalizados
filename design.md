# Design: Bordô

The locked system. Every Hallmark run reads this first and pages share it. Change it on purpose; the file is the rule.

## System
- Genre: editorial
- Shape of the first page: Catalogue (`index.html`); the three discovery pages use Split Studio
- Theme: brand (logo, wine, sage, gold, Lora and Manrope, read from the project)
- Axes: light/roman-serif/chromatic-red · posture: full-palette

## Tokens
`assets/tokens.css` is the source of truth. The roles:
```css
:root {
  --color-paper: oklch(98.2% 0.005 130);  --color-paper-2: oklch(96% 0.007 132);  --color-paper-3: oklch(93% 0.01 130);
  --color-ink: oklch(28.9% 0.007 145);  --color-ink-2: oklch(41% 0.012 135);  --color-muted: oklch(50.5% 0.012 131);  --color-rule: oklch(88% 0.008 114);
  --color-accent: oklch(35.2% 0.1 4);  --color-accent-ink: oklch(98.2% 0.005 130);  --color-focus: oklch(40% 0.18 4);
  --color-display: oklch(35.2% 0.1 4);  --color-sage-deep: oklch(42.4% 0.035 138);  --color-gold: oklch(64.9% 0.087 75);
  --font-display: "Lora", Georgia, ui-serif, serif;  --font-body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 4px;  --radius-pill: 999px;  --rule-hair: 1px;  --shadow-card: none;
}
```
The spacing scale, the type scale, the easings and the durations are the scaffold's and live in `assets/tokens.css`. `assets/base.css` holds the base rules. Each page keeps its own CSS inline and imports both files.

## Roles
- Wine (`--color-accent`, `--color-display`): headings, the primary action, the footer field.
- Sage (`--color-sage-deep`): the one band per page that invites a custom order.
- Gold (`--color-gold`): the hairline under text links, nothing else.
- Weights: Lora 400; Manrope 400 and 600.

## Controls
- Primary: wine fill · 4px radius · 48px tall
- Secondary: outline in `--color-muted`, wine text · same radius and height

## Motion
- Character: still; colour changes on hover only, no reveal; under reduced motion everything ends at once.

## Exports
`assets/tokens.css` in this project. Tailwind, DTCG or shadcn blocks are added here on request.
