# Ashah Meets World — website

Creative direction and worldbuilding for culture-driven brands.
Built with [Astro](https://astro.build). All content is plain files, so it can be edited three ways:
in GitHub, in a visual editor (Pages CMS), or by asking Claude.

## What lives where

| What | File(s) | Shows up at |
|---|---|---|
| Portfolio pieces | `src/content/work/*.md` (one file each) | `/work/` and `/work/<file-name>/` |
| Sales pages | `src/content/offers/*.md` (one file each) | `/<file-name>/` (e.g. `/ubiquity/`) |
| Field Notes covers | `src/content/notes/*.md` | Home page strip |
| Site settings: email, socials, form links, Discord, booking | `src/data/site.json` | Everywhere |
| Images | `public/images/...` | Referenced as `/images/...` |
| Colours, fonts, spacing (The Codes) | `src/styles/global.css` (top of file) | Everywhere |
| Page layouts | `src/pages/` | — |

## Editing

**In GitHub:** open a file, click the pencil, edit, commit. To add a portfolio piece, copy an existing
file in `src/content/work/`, rename it (the name becomes the web address) and change the details.
Upload images into `public/images/work/<piece>/` with *Add file → Upload files*.
The site rebuilds and goes live by itself about 1–2 minutes after every commit.

**In Pages CMS (visual editor):** go to https://app.pagescms.org, sign in with GitHub, choose this repo.
You'll see *Portfolio*, *Field Notes*, *Sales pages* and *Site settings* with proper forms and image uploads.
Saving there commits to GitHub, so the site rebuilds the same way.

**With Claude:** connect this repo to Claude (GitHub connector or Claude Code) and say what you want changed —
"add a case study for the Realism drop", "change the Launch price to $750", "new sales page for X".
`CLAUDE.md` tells Claude how the project is laid out.

## Connecting the forms

In `src/data/site.json` (or *Site settings* in Pages CMS):
- `contactFormEmbed` — paste Tally's embed code (Share → Embed → Standard). The contact page uses it.
- `newsletterEmbed` — paste Brevo's form embed HTML. Or `newsletterUrl` for its hosted link.
- `discordUrl`, `bookingUrl`, `email`, `socials` — fill in and they appear in the nav, footer and contact page.
Empty values are hidden automatically.

## Going live on GitHub Pages

1. Create a new repo on GitHub (e.g. `ashah-meets-world`) and upload everything in this folder
   (or `git init && git add . && git commit -m "first draft" && git push`).
2. In the repo: **Settings → Pages → Source: GitHub Actions**.
3. Push to `main`. The site appears at `https://<username>.github.io/<repo-name>/`.

**Custom domain later:** Settings → Pages → Custom domain, add your domain and follow the DNS steps.
Then in **Settings → Secrets and variables → Actions → Variables** add
`SITE_URL = https://yourdomain.com` and `BASE_PATH = /`, and re-run the deploy.

## Running it on your computer (optional)

```
npm install
npm run dev     # http://localhost:4321
```
