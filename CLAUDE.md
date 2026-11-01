# Notes for Claude — Ashah Meets World site

Astro 5 static site, deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.
Content is edited by Ashah through GitHub, Pages CMS (`.pages.yml`) and Claude, so keep the content
schema (`src/content.config.ts`), `.pages.yml` and the markdown files in sync whenever fields change.

## Structure
- `src/content/work/*.md` — portfolio case studies (frontmatter schema in `src/content.config.ts`; markdown body = the case study).
- `src/content/offers/*.md` — sales pages, rendered by `src/pages/[offer].astro` at `/<file-name>/`.
- `src/content/notes/*.md` — Field Notes covers for the home page strip.
- `src/data/site.json` — global settings (email, socials, Tally/Brevo/Discord/booking links). Empty strings are hidden.
- `src/styles/global.css` — design tokens (The Codes). `src/components/Sky.astro` — the night/dawn scenes.
- Always build internal links/images with `u()` from `src/lib/url.ts` (handles the GitHub Pages base path).

## The Codes (art direction — follow on every change)
- Night is the canvas: midnight #070B18, sapphire #16367A, indigo #22175A, violet #3A1F66, mauve #8A4C8E, dusk rose #E08C7E, peach gold #F2B48C, aqua #7FD8F0.
- One accent per skill: Creative Direction #4202E8, Ecosystem Design #03A2FF, Cultural Leadership #D82A99, Campaign Marketing #45E992.
- One light source per scene with a halo; small figure, big world; grain, not gloss.
- Type: Cormorant Garamond italic for headlines and lines to be felt; DM Sans for labels, captions, facts. Spaced caps for labels.
- Voice: speak in images. Short sentences, plain words, conviction over hype. No hype buttons, no emoji, no all-caps shouting.
- Feeling sequence: wonder → desire → energy → possibility → courage.

## Checks before committing
`npm run build` must pass (the content schema validates every file).

## Archived (15 Oct 2026): offer off the site, nothing deleted
The site is currently a personal brand and portfolio. The paid offer is archived while it's validated through prospecting.
- `/ubiquity/` sales page: `src/content/offers/ubiquity.md` has `draft: true`. Set it to `false` to republish.
- Home page thesis, opportunity and offer sections: `SHOW_OFFER = false` in `src/pages/index.astro`. Set it to `true` to restore them (section numbers adjust automatically).
- Nav and footer links to Ubiquity are commented out in `Header.astro` and `Footer.astro`.
- Booking link: moved to `archivedBookingUrl` in `src/data/site.json` (`bookingUrl` is empty, so it's hidden).
- CTA rule ("give first"): the main ask is the newsletter or this month's free resource; the second is "say hello" or a question. No "book a call" until the offer relaunches.
- Community page: hidden 17 Oct 2026. The page is kept as `src/pages/_community.astro` (the underscore stops Astro building it). Rename it back to `community.astro` and restore the footer link to republish.

## Home page (17 Oct 2026)
- No section numbers ("01", "1 of 4") anywhere.
- After the hero: a "Hello" section (intro from `about.json`, mission quote). Then the skill stack, with the prism visual (`Prism.astro`) beside "Four lights, one beam."
- Hero CTAs: "See the work" → /work/, "Work with me" → /contact/.

## Glow language (button rule, in global.css)
- **Aurora** (`.btn.aurora`) = working together: the contact form's send button.
- **Embers** (`.btn.ember`, warm peach glow) = community: "Letters from the world" newsletter sign-ups.
- Revisit when the offer and community pages come back.

- Contact page "Letters from the world": same layout as before, plus two faint dusk halos (mauve and a muted orange-red) behind it, in the vein of the fireflies. Keep them subtle; no bright peach.
- Prism visual: built, currently off (`SHOW_PRISM` in index.astro).
- Page loads: a small script in `Base.astro` opens every new page at the top (back/forward and #anchors behave normally).
- Home page relay (`Relay.astro`, 17 Oct 2026): below the skill cards, each card's light flows down into one prism, which sends a single white beam toward Selected work. Desktop only (hidden under 860px).
- Home "Hello" section: the mission sits beside the intro in the quote style; only the background borrows the About page's MissionSky stars and ripples (faded edges, soft violet glow).
- Prism relay: built, currently off (`SHOW_RELAY` in index.astro). Ashah's note: the beams read as wires, not light.
- Home hero: elevated layered scene in `HeroScene.astro` (switch `ELEVATED_HERO` in index.astro; false = the original `Sky` night scene). Details in DESIGN.md.

## Orbit (live 25 Oct 2026)
- Free lead magnet page `/orbit/` (`src/pages/orbit.astro`), linked from the footer's second row (magnets, offers, ventures) and, since 31 Oct 2026, the header nav (Passage, Orbit, then Work, About, Contact). Aurora look; never mixed with ember/firefly.
- Sign-ups: `OrbitSignup.astro` (page, redirects home after 8 s) and `OsNudge.astro` (site pop-up, confirms in place). Both post to the Brevo form in `site.json` → `orbitFormUrl`; empty = preview mode (confirms without sending).
- The download is `public/os/Orbit-v<version>.zip`; the Brevo emails link to it, so update them when the file name changes.

## Orbit v0.4 page (30 Oct 2026)
- `/orbit/` now runs the v0.4 sections built as a mock-up: `src/orbit/sections-a.html` / `sections-b.html` (markup, split around the bottom `OrbitSignup`), `sections.js` (inline scripts) and `src/styles/orbit-v04.css` (scoped under `.nx`). Images and the sample hub (`hub-demo.html`, the real hub on made-up data) are in `public/orbit/`; `__BASE__` in the markup becomes the base path.
- Problem headline: "Spread thin across everything. Deep in nothing." The door in `AnklesScene.astro` sits lower, on its own horizon line; the lights are a faint algae blue.
- The tag reads "Orbit v0.4" and the download is `public/os/Orbit-v0.4.zip` (30 Oct). `Orbit-v0.3.3.zip` stays so links in emails already sent keep working.
- Never use people's names in sample content (Ashah's standing rule).

## Passage (live 31 Oct 2026)
- The offer's landing page is a standalone file: `public/passage/index.html` (served at /passage/). No site header, footer or mobile nav; the A·M·W mark is the only way back. It's generated outside this repo (Business Development project, `passage/source/build_final.py`), so edit the generator, not the HTML, when you can.
- Links: header nav (first, then Orbit, then the white links) and footer second row, left of Orbit. Look: nocturnal blue-violet text gradient (`.passage-link`), a counterpoint to Orbit's aurora.
- Applications post to Formspree (`https://formspree.io/f/xqpeqoab`, same as the contact form; emails Ashah, subject "Passage application: <brand>") and, in parallel, to the Google Apps Script relay ("Passage relay", bound to the Sheet "Passage applications (from ashah.world)"), which appends a row. A scheduled Claude task copies new rows into the Notion board "Passage applications" in NEW Central Hub.

## Field Notes (31 Oct 2026)
- Field Notes images load live from Instagram (`src/lib/feed.ts`, `src/lib/live.ts`): carousel posts, newest first. The series ends on 8 November 2026, so carousels posted from 9 Nov 2026 (Melbourne) are never counted (`FIELD_NOTES_END`).

## Orbit v1.1 page (31 Oct 2026)
- Customer Experience (was Client Success) has a Customer / Community / Client switch under its hub image (`.cxsw` in `sections-a.html`, script at the end of `sections.js`). Images: `public/orbit/c768620e99.jpg` (Customer), `cx-community.jpg`, `cx-client.jpg`.
- "Your rhythm" section (book, collection, single) sits just above "You stay in charge".
- Copy rule: "launch" is used sparingly in body copy, never in headers. Label sets keep one rhythm ("Your brand, Your mission, Your offer...").
- Interaction rule (Ashah): hover or reveal text must not push the content below down. Reserve the space and fade it in. Exceptions are allowed, but that's the default.

## Lucid (coming soon, 1 Nov 2026)
- `/lucid/` (`src/pages/lucid.astro`) is the coming-soon page for Lucid, Ashah's creative-sanctuary product (his personal workstation, separate from Orbit). Doors open Mon 4 January 2027; teasers from about 21 December 2026. The page shows a nights-to-go count that hides itself on the day.
- Linked from the footer's second row only (right of Orbit), never the header. Hovering the footer link pops a tiny "Coming soon" (smaller than the link) just above it with a little spark burst (no layout shift), held about 1.8 s, then it drifts off.
- Nav colours match the Lucid deck: Orbit is aurora green to violet (#5CFFB0, #2EE6C8, #4FB8FF, #A98CFF) in header and footer; Lucid is opal (#FFD6EC, #E2B8FF, #9FE6F5, #FFF6EC, #F2A8D8), slowly shifting.
- Under the hero: three small looping videos in arched door frames (`public/lucid/door-*.mp4` + poster jpgs, cut from the December launch reels). Door shapes are Lucid's framing device.
- Pre-sign-up (1 Nov 2026): `LucidSignup.astro` at the bottom of /lucid/ (#list; hero link "Save me a door"). Posts to the Brevo form in `site.json` → `lucidFormUrl`; empty = preview mode (confirms without sending). Sign-ups get Lucid by email on launch day.
- Lucid app (v0.3): runs locally like the Orbit hub. `public/lucid/app/lucid-server.py` is the engine's update copy (Start Lucid pulls it); `public/lucid/latest.json` drives the studio's update card. The Orbit hub (`public/os/hub.html`) shows an opal "Studio" door in its nav when Lucid answers at 127.0.0.1:4778/api/door.
- Look: opal (pearl, lilac, aqua, blush) in a dream where the rules bend: floating doors, a stair of light, still water, no moon. Never aurora (Orbit) or ember. Phases: Dream, Conjure, Unfold, Awaken. Rooms: optional Content plus five rooms for any craft.
- Workstations section (1 Nov 2026): "Every room has its own flow." on /lucid/, a tab switch (Content, Music, Fashion, Your craft) showing each room's inner steps as opal arches: Content = Worksheet, Macro, Micro, Approved; Music = Beat, Lyrics, Vocals; Fashion = References, Vision, Artboard, Tech pack. Ashah: this is one of the main parts of the workstation, so keep it in every Lucid build.
