# ashah.world · Website design system
*v1 · 17 Oct 2026. The visual language of the live site, written down so any Claude chat (Funnel OS, Creative Director) makes changes that look like they were always there. Read with `CLAUDE.md` (how the site is built) and the `amw-codes` skill (the brand). Pair it with `Website visual reference.pdf`, which shows every page as it stands.*

## The feeling
A night world you step into: dark, cinematic, quiet, with light that comes from somewhere. Elevated but never sterile. Every page is a scene, not a template. If an element doesn't serve the page, it goes.

## Rules that hold everywhere
1. **Night is the canvas.** The page is always midnight `#070B18`. Colour arrives as light (glows, halos, skies), never as flat fills or bright blocks.
2. **One light source per scene, with a halo.** The moon, a doorway, a dawn sun, a glow behind a section. Never two competing lights.
3. **Small figure, big world.** Illustrations are vast and quiet, with tiny human scale.
4. **Grain, not gloss.** A fixed film-grain overlay (`body::after`, 7% overlay) sits on everything. No glossy gradients, no drop-shadow cards.
5. **No hard edges between areas.** Sections fade into each other. Glows are blurred radials easing to zero. If you can see the edge of a glow, it's wrong (watch for `overflow` clipping a halo).
6. **Subtle beats loud.** When in doubt, halve the opacity. Ashah consistently prefers the quieter version.
7. **No numbering.** No "01", "1 of 4", page counters or series numbers anywhere.
8. **Essentialism.** One idea per section, one ask per page.

## Colour
| Token | Hex | Use |
|---|---|---|
| midnight | #070B18 | Page background, always |
| deep | #0B1230 | Panels, depth |
| sapphire | #16367A | Night sky, cool glows (e.g. blue halo under "Open the door") |
| indigo | #22175A | Sky gradients |
| violet | #3A1F66 | The soft purple glows (top-right of contact, behind the mission) |
| mauve | #8A4C8E | Dusk glows, community warmth |
| rose | #E08C7E | Dusk, embers |
| peach | #F2B48C | Eyebrows, links that glow, the ember button, focus states |
| aqua | #7FD8F0 | Aurora, moonlight, water |
| ink / ink-2 / ink-3 | #EEEAF6 / #B9BED6 / #7E86A8 | Text: headings / body / labels |

**Skill accents** (only for the four skills): Creative Direction #7C5CFF · Ecosystem Design #03A2FF · Cultural Leadership #E04BAE · Campaign Marketing #45E992.

**Warmth:** warm tones appear as a *source* (a sun, a flame, an ember glow) or a faint dusk wash, never as a bright warm field. A full peach sunset gradient was tried on the contact page and rejected as too bright. Keep warmth low, sitting in the mauve-to-orange-red range.

## Type
- **Cormorant Garamond, italic 400:** every headline (h1 to h3), ledes, quotes, the mission. Big, soft, cinematic. h1 up to 148px, h2 up to 76px.
- **DM Sans:** body (17px/1.65, ink-2, max ~58ch) and **spaced capitals** for eyebrows and labels (eyebrow 12px, letter-spacing .32em, peach; label 11px, .26em, ink-3).
- Headlines in sentence case, usually ending with a full stop: "Four lights, one beam."
- Australian spelling. No emoji. No all-caps shouting outside eyebrows and labels.

## Components (reuse these; don't invent new ones)
- **Eyebrow:** small peach spaced capitals above a heading ("Hello", "The skill stack", "Selected work").
- **`.go` link:** text with a line under it and an arrow, never a pill button. Hover widens the gap and turns it peach. `.go.glow` is peach by default. `.go.aurora-line` has an animated aurora underline (the hero's "Work with me").
- **Buttons, and the glow language:**
  - `.btn` (default): peach outline, fills on hover.
  - `.btn.aurora`: aurora gradient with a tinsel sweep = **working together** (the contact form's send button).
  - `.btn.ember`: warm peach-rose gradient that breathes = **community** ("Letters from the world" sign-ups). It matches the fireflies and the dawn scene.
- **`.halo`:** a blurred coloured circle (blur 60–90px, opacity .15–.6) placed behind content for atmosphere. This is the main tool for adding colour to a section. Keep halos inside a full-width section so they aren't clipped.
- **Cards** (skill cards, work cards): thin `--line` border, dark translucent fill, a soft accent glow in the top corner, an icon, label, serif title, italic metaphor, body.
- **Quote:** serif italic with a thin peach line on the left (`.quote`).
- **Signup ("Letters from the world"):** serif title, one-line promise, email field and ember button.
- **Reveal:** elements with `.rv` fade up gently as they scroll into view.

## The hero (elevated 18 Oct 2026)
`HeroScene.astro` replaces the old night `Sky` on the home hero (switch: `ELEVATED_HERO`). It's the same world, built as layers:
- **Sky:** a deep gradient, twinkling stars, a slow aurora (aqua to blue to violet, with a mint ribbon, blurred and drifting), and a shooting star every ~13s.
- **The light:** the moon with a disc, bloom and a breathing halo.
- **The city:** a hazy far skyline, the lit near skyline (flickering windows, pink beacons), and reflections where every light becomes a soft swaying streak on the water.
- **The water:** soft ripple flecks, the moon's road (blurred glints with a light pillar), and drifting mist along the horizon.
- **Small figure on the jetty** (desktop only), plus a few motes of light rising off the water.
- **Depth:** layers drift at different speeds on scroll, and lean gently toward the pointer on desktop. Motion is off for people with reduced motion turned on.
- **Two compositions:** on desktop the horizon sits at 70%, the moon at 59%, and the city is on the right so the headline sits in open sky. On a phone the horizon is at 44%: the moon and city fill the top half and the words sit on the dark water.
- **Lesson:** blurred SVG layers need generous filter and mask regions (`userSpaceOnUse`), or hard edges appear.

## Scenes (illustration components)
All hand-built SVG in `src/components`, in the night world: `Sky` (night city on water with moon, and a `dawn` variant with palms and sun), `MissionSky` (twinkling stars and slow ripples), `DawnSky`, `Door` (light spilling from a doorway), `Lighthouse`, `Fireflies` (community), `Constellation`, `Waterline`, `Flame`, `Everywhere` (meteor shower), `LuminaryLight`, `SkillIcon`.
- New visuals should come from this world: sea, shore, stars, moon, aurora, lighthouses, doors, lanterns, fireflies, city lights, water.
- Every illustration is an analogy. If it doesn't make an idea clearer, it doesn't go in.
- **Tried and dropped (17 Oct):** a glass prism beside "Four lights, one beam" (felt overstated; the small version looked awkward), and a prism "relay" with beams from the skill cards into the work section (read as wires or tubes, not light). Both are kept switched off (`SHOW_PRISM`, `SHOW_RELAY`). Lesson: light must look like light (soft, bloomed, travelling), never like lines or cables.

## Page structure (as of v10)
- **Home:** hero (the elevated night scene, `HeroScene.astro`, "Ashah Meets World", "See the work" and "Work with me" → contact) → **Hello** (intro left; the mission right, in the quote style (thin peach line, label underneath), with the About page's stars and ripples faintly behind it) → **The skill stack** (four cards) → **Selected work** → **From the feed** (Instagram) → **Meet the world** (dawn scene, "Say hello", Letters sign-up).
- **About:** "Where the light crosses." (intro with the night-city reflection image) → the mission (full MissionSky treatment) → "The story so far." (five chapters on a lit timeline) → "The luminary." (positioning) → "Step inside." (the door scene, links to work and contact).
- **Contact:** "Open the door." with soft violet (top right) and sapphire (left) halos → form with the aurora button → Letters from the world, same layout as before, with two faint dusk halos (mauve plus a muted orange-red) behind it.
- **Hidden, not deleted:** Ubiquity offer page and home sections (`SHOW_OFFER`), Community page (`_community.astro`). Instructions in `CLAUDE.md`.

## How Ashah gives feedback, and how to act on it
- He reacts to what he sees. Always show a rendered preview (screenshots, desktop and mobile) before calling a change done.
- Expect "too much" more often than "too little". Start subtle.
- When he says "keep it exactly how it was, except…", change only that one thing.
- Ideas he floats ("might look cool, might look ass") are experiments. Build them behind a switch so they can be turned off without being lost.
- Log every visual decision here or in `CLAUDE.md`, so the next chat doesn't repeat a rejected idea.
