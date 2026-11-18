# Design: Bordô

The locked system. Every Hallmark run reads this first and pages share it. Change it on purpose; the file is the rule.

## System
- Genre: editorial
- Shape of the first page: Catalogue (`index.html`); the three discovery pages use Split Studio
- Theme: brand (logo and bordô kept; Instrument Sans for display, Manrope for body; pale rosy paper)
- Axes: light/grotesque-sans/chromatic-red · posture: full-palette

## Tokens
`assets/tokens.css` is the source of truth. The roles:
```css
:root {
  --color-paper: oklch(97.6% 0.008 30);  --color-paper-2: oklch(94.6% 0.017 15);  --color-paper-3: oklch(90.5% 0.026 10);
  --color-ink: oklch(22% 0.03 5);  --color-ink-2: oklch(38% 0.03 5);  --color-muted: oklch(50% 0.026 5);  --color-rule: oklch(86% 0.022 10);
  --color-accent: oklch(35.2% 0.1 4);  --color-accent-ink: oklch(97.6% 0.008 30);  --color-focus: oklch(40% 0.18 4);
  --color-display: oklch(30% 0.095 4);  --color-field: oklch(23.5% 0.072 4);  --color-gold-deep: oklch(58% 0.085 75);
  --font-display: "Instrument Sans", ui-sans-serif, system-ui, sans-serif;  --font-body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 2px;  --radius-arch: 999px 999px 2px 2px;  --radius-pill: 999px;  --rule-hair: 1px;  --shadow-card: none;
}
```
The spacing scale, the type scale, the easings and the durations are the scaffold's and live in `assets/tokens.css`. `assets/base.css` holds the base rules. Each page keeps its own CSS inline and imports both files.

## Type roles
- Two families only: Instrument Sans (500, italic 500; latin subset, width fixed at 100) for headings, prices and big numbers; Manrope (400, 600) for everything else. Bold text is 600, never 700+.
- Body 16px; secondary 14px (`--text-sm`); fine print 13px (`--text-xs`) is the floor. The one exception is the blog's commission line, kept at 11px on the owner's request.
- Fonts ship as woff2 (`Manrope.woff2` is a Latin subset of the variable font, weight axis 200-800). The hand-written blog pages reach this scale through `blog/assets/ponte.css`.

## Roles
- Bordô is a highlight, never a field: headings (`--color-display`), the primary action (`--color-accent`) and the footer (`--color-field`), the one dark surface on a page.
- Paper is pale and rosy; `--color-paper-2` marks a band.
- Gold (`--color-gold-deep`) is the hairline under text links, nothing else.
- Arches (`--radius-arch`) frame the collection tabs and portraits only.
- Photographs are bright and photographic: natural window light, real fabric weight and contact shadows, no dark velvet backgrounds.
- Weights: Instrument Sans 500; Manrope 400 and 600.

## Controls
- Primary: bordô fill · pill · 52px tall
- Secondary: outline in `--color-muted`, bordô text · same radius and height

## Motion
- Character: calm; one rise-and-fade reveal on scroll, a short entrance in the hero and on collection change; under reduced motion everything ends at once.
- Signature: the running stitch. The active collection tab is underlined by a dashed bordô line sewn in 16 steps (640ms) when the collection changes; the same dashed line under the header shows how much of the page has passed, driven by `animation-timeline: scroll()` where supported.
- Header: hides when scrolling down past 160px and returns on any scroll up; it never hides with the menu open, focus inside it or reduced motion.
- Hero: a scroll scene on every screen (240svh on desktop, 220svh on phones; the stage is sticky at 100svh). The intro fades out, the camera eases into the bow, three lines appear one at a time ("Cada laço começa num risco.", "Depois, ponto por ponto, vira bordado.", "E chega a quem você ama."), the bow turns into its pencil pattern (`hero-risco.webp`) from the bow outwards, the pattern dissolves back into the embroidery and the camera returns to the girl. On desktop with a mouse, a 240px lantern also reveals the pattern before scrolling. With reduced motion the hero is the still photo and the intro.
- Product photos ease 4.5% closer under a fine pointer (900ms, `scale`, so it stacks on per-photo crops).
- Feedback: in the bag, a new piece rises in and a changed quantity and price tick (220ms); the form error and the toast fade in. FAQ answers open with animated height where the browser supports `interpolate-size`.

## História (shop)
- The peak of the scroll: `--section-gap-l` around it, portrait 5fr in the arch next to a hero-scale title, the opening paragraph at reading size (`--text-xl`, 34ch; `--text-lg` on phones), and the portrait unmasking with `.revela`.

## Blog (Casa & Inspiração)
- On the shop, the band shows the guides as photo cards (`assets/guias/`, 960×640 crops of the list covers): the newest guide tall on the left, four in a 2×2 grid beside it; on phones a snap carousel with the next card peeking.
- The list pages (`blog/assets/revista.css`) follow this system: an oversized Instrument Sans numeral opens the page, a spotlight piece swaps with a vertical wipe, and the items sit in an asymmetric 7/5 and 4/4/4 grid.
- Type on the blog moves in fixed steps per breakpoint, never by viewport width.
- Ornament: embroidered stitch borders (`blog/assets/ornamentos/`) used as colour masks, gold between sections and bordô over a band.
- Motion: photo reveal by clip-path on scroll, the running stitch under the active index number, view transitions when the list is re-sorted.

## Acabamento (all pages)
- `assets/acabamento.css` is loaded by the shop, the SEO pages and the blog.
- Linen weave under the paper (16 %, multiply), from the Creative Fabrica pack in `assets/ornamentos/`.
- One word per heading in Instrument Sans italic, in bordô; the words themselves never change.
- `.costura`: an embroidered stitch border as a colour mask between sections (gold; `.folhas` in bordô).
- `.revela`: photos unmask with the scroll where the browser supports view timelines; never on the first-screen photo.

## Lookbook (Mãe & Rainha)
- The three colours are buttons: each swaps the section photo with a vertical wipe and an italic caption; "Ver as três juntas" returns to the trio. Single-colour photos sit on paper inside the same 4:3 frame, so nothing shifts.

## Exports
`assets/tokens.css` in this project. Tailwind, DTCG or shadcn blocks are added here on request.
