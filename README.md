# Portfolio site — Vercel rebuild (fancy version)

Built Tue 17 Nov 2026 from the live Google Sites portfolio
(https://sites.google.com/view/anisurrahman-marketing, fetched the same
morning) and `09-portfolio-website-pack.md`, plus the verified live updates
(Contact email/phone, About Training, 6 Instagram Reels).

The Google Sites site stays live and untouched. This is a separate copy —
nothing here changes it, and the switch happens only when Anisur says so.

## What this version is

Dark premium design (bg #121110, cream text, red accent #ff3b2f), with
Anisur's real content and his maroon-suit photo (assets/me-front.webp).

Effects (all built here from scratch, no outside code):
- Hanging ID card with Verlet-rope physics (script.js) — grab it, pull
  it, throw it; it swings back. Photo: assets/me-card.webp.
- Mask reveal on the About photo — a lens follows the cursor and shows
  the same photo as Spider-Man (assets/me-mask.webp). The hero is
  Spider-Man by default; to swap it, replace me-mask.webp with another
  masked version of me-front.webp at the same size and framing.
- Cursor follower ring + halo (script.js). The "let's collab" button is a
  glossy CSS pill, not the WebGL goo button — that version's code lives
  in a repo that cannot be fetched, so the pill is the honest fallback.
- Loader with a REC timecode, floating nav pill, scroll-progress line,
  skills strip, copy-email button.

## What this fixes vs Google Sites

- Every page has a real `<meta name="description">` (Google Sites has none).
- A real `sitemap.xml` that returns XML (the Sites one returns HTML).
- The freelancer schema (JSON-LD, from the Day 3 practice file) lives in
  the `<head>` of the home page (Google Sites cannot add code to `<head>`).
- Google Analytics G-6Z69CGL8GR is included on every page (same ID already
  verified on the Sites version).

## Files

- 11 pages: Home (fancy, hand-designed in build.py), About, Services,
  My Work index + 4 case pages, Evidence, What I Learned, Contact.
  One stylesheet (`styles.css`), one script (`script.js`),
  `assets/` (3 photos), `robots.txt`, `sitemap.xml`. No build step,
  no backend — the contact form links out to the existing Google Form.
- `build.py` regenerates everything from one place. Edit the content
  there, run `python3 build.py`, and the HTML is rebuilt. `script.js`
  and `assets/` are hand-written and not touched by the build.
  The single banned-phrase match in this folder is the rule comment
  inside `build.py` itself — the HTML has none.

## Standing rules kept

- Full legal name 'Md. Anisur Rahman' everywhere; 'Veneer Monet' only as the
  brand/project. No 'Level 4' phrase, no 'Digital Marketing for Freelancing'
  phrase, no unit codes, 'E-Learning' capital E. Real phone +8801577809069
  and email anisuranik6@gmail.com. First sale still pending — stated honestly.
- The uploaded 'Portfolio-Guide-for-Claude' PDF was NOT used: it did not pass
  a safety check, so its instructions and code links are not followed. This
  build uses only his real portfolio content.

## Deploy (Anisur's taps — Muse cannot create accounts in his name)

1. GitHub (account under anisuranik6@gmail.com, already exists): create a new
   public repo, e.g. `anisurrahman-portfolio`, and upload this folder's contents.
2. Vercel (free Hobby plan, $0, no card): sign in with GitHub → Add New →
   Project → Import the repo. Framework preset: **Other** (static site, no
   build command, no output directory change). Project name:
   **anisurrahman-marketing** → https://anisurrahman-marketing.vercel.app
   (`anisurrahman.vercel.app` was taken by another site, 2026-11-17; the
   project was first deployed as `anisurrahman-ten`, then renamed. If Vercel
   says a name is taken, stop and report — do not pick another name. After a
   rename, update `BASE` in `build.py`, re-run it, and push again — sitemap,
   canonical links and schema all use it).
3. Verify live: open the home page (card drops, drag works, lens lines up,
   cursor ring follows, all links work); check `…/sitemap.xml` returns XML;
   paste the home page into Google's Rich Results Test for the schema;
   check GA4 Real-Time for a visit.
4. Still to do at deploy time: nothing — the portrait photo is bundled now.

## After the switch (only when Anisur says so)

- Add the new URL as a property in Search Console and submit the sitemap
  (the old Sites sitemap must NOT be submitted — it returns HTML).
- Update the portfolio pack files and any Drive links that point at the
  Google Sites URL, and tell the assessor the new address.
- The Google Sites version can stay up as a backup, or be unpublished later.
