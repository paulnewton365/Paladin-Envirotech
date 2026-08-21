# Paladin EnviroTech — site prototype

**Build 1.2.0**

Twelve-page static prototype of the paladinenvirotech.com redesign, exported
from Claude Design and prepared for deployment.

## Deploying to Vercel

Plain static site. No build step, no dependencies.

```bash
git init
git add .
git commit -m "Paladin site prototype"
git branch -M main
git remote add origin git@github.com:YOUR-ORG/paladin-site.git
git push -u origin main
```

In Vercel: **Add New → Project → Import** the repo. Framework preset **Other**,
build command and output directory left empty. Or run `npx vercel` from this
folder to deploy without GitHub.

## Pages

| URL | File |
| --- | --- |
| `/` | index.html |
| `/platform` | platform.html |
| `/secure-itad` | secure-itad.html |
| `/electronics-recycling` | electronics-recycling.html |
| `/paladin-local` | paladin-local.html |
| `/critical-materials` | critical-materials.html |
| `/industries` | industries.html |
| `/network` | network.html |
| `/company` | company.html |
| `/blog` | blog.html |
| `/contact` | contact.html |
| `/rare-earth-freedom-250` | rare-earth-freedom-250.html |

`cleanUrls` is on, so pages resolve without the `.html` extension and all
internal links are written that way.

## What changed from the export

- Pages renamed from `Name.dc.html` to lowercase URLs; `Homepage` became
  `index.html` so Vercel serves it at the root. Every internal link was
  rewritten to match.
- `uploads/` became `assets/`, with spaces and capitals removed from
  filenames. Twelve unreferenced screenshots (878 KB) were dropped.
- `image-slot.js` and its 458 KB `.image-slots.state.json` sidecar were
  removed. Six pages loaded the script but no page contains an `<image-slot>`
  element, so both were dead weight. Re-add them if you introduce image slots
  in Claude Design.
- Titles, descriptions and social preview tags added per page. All pages are
  set to `noindex` via both a meta tag and an HTTP header.
- `responsive.css` added (see below).

## Responsive behaviour

The export shipped with no media queries. Its auto-fit grids already used
`minmax(min(Npx, 100%), 1fr)` and the mobile menu button is driven by
JavaScript, so most of the site held up; `responsive.css` covers the rest.

| Breakpoint | What changes |
| --- | --- |
| all widths | Form fields allowed to shrink inside grid tracks |
| 900px | Fixed-column grids stack to one column |
| 700px | Oversized nowrap CTAs wrap and go full width |
| 520px | Masthead compacts to one row; language toggle hidden |
| 380px | Header CTA hidden |

Verified in headless Chromium across 12 pages at 320, 360, 390, 430, 600, 768,
1024 and 1440px, with no horizontal overflow in any of those 96 combinations.
The masthead was 121px on phones before this and is now 60px.

Two deliberate trade-offs on small screens. The language toggle is hidden below
520px, and the header's "Talk to an expert" button is hidden below 380px, where
it cannot share a line with the logo and menu button at a readable size. The
hero and in-page calls to action still carry the same action, and the hamburger
keeps the full navigation reachable at every width.

Because pages are authored with inline styles, the rules in `responsive.css`
match on style-attribute substrings. If you re-export from Claude Design, the
stylesheet will not come with it and some selectors may no longer match — the
comments at the top of the file explain what to check.

## Scroll motion

Each page already shipped a small scroll runtime driving `data-reveal`,
`data-stagger`, `data-countup`, `data-parallax` and `data-car`. Coverage was
uneven: the homepage carried nine reveal hooks, most interior pages one to six,
and contact and rare-earth-freedom-250 had no runtime at all.

`motion.js` fills the gaps without touching anything the page runtime owns:

- Untagged bands get a whole-band reveal using the same easing and distance as
  the built-in one, so pages that mix both read as a single system.
- Rows of sibling cards, stats and columns inside each band are staggered so
  components arrive one after another rather than the band popping in at once.
- Elements already carrying `data-reveal` are left alone.

It drives its own elements with `IntersectionObserver` under the `data-mreveal`
attribute. The hidden state is applied by JavaScript, never by CSS, so if the
file fails to load or throws, everything stays visible. A six-second failsafe
force-shows anything the observer never fires for.

### The facility map

The nine routes on `/network` fan out from Tampa. Three carry
`stroke-dasharray` for the international styling, so a `stroke-dashoffset`
draw would make the dashes march along the path rather than extend it.
Instead the route group is clipped by a circle centred on Tampa whose radius
grows outward over 1.5s, which reads as routes leaving headquarters and behaves
identically for solid and dashed strokes. Cities fade in as the wave reaches
them, staggered by their real distance from Tampa, so Dallas lights up well
before Suwon. The clip is removed once the animation completes, so the finished
state is byte-identical to the static map.

### Reduced motion

Users with `prefers-reduced-motion: reduce` get no animation at all. The
built-in page runtime does not check that preference on its own, so
`motion.js` pins its elements open on its behalf.

## Versioning

Every build carries a `MAJOR.MINOR.PATCH` version:

- **MAJOR** — new information architecture, or a rebuild from a fresh export
- **MINOR** — new pages, new sections, reordered or rewritten content
- **PATCH** — fixes and refinements with no content change

It appears in three places: `version.json`, a `build-version` meta tag on every
page, and a discreet stamp at the foot of every page so a reviewer can always
say which build they are looking at. To cut a new build, run
`stamp-version.py X.Y.Z "notes"` before packaging.

### History

| Version | Notes |
| --- | --- |
| 1.0.0 | Single-page homepage prototype, two directions |
| 1.1.0 | Twelve-page site, deploy prep, responsive layer |
| 1.1.1 | Scroll motion layer and animated facility map |
| 1.2.0 | Card reorder, mobile stat bands, mobile network view, versioning |

## Notes

**Runtime dependency.** `support.js` loads React, ReactDOM and Babel from
unpkg.com at page load, so the site needs an internet connection and will not
render from a `file://` URL. To preview locally, run `python3 -m http.server
8000` in this folder and open `http://localhost:8000`. The script also honours
a `window.__resources` override if you ever need to point those at local copies
for an offline demo.

**Stock imagery.** `assets/leadership.jpg` was an unlicensed Getty comp with
a visible watermark, captioned as the Paladin leadership team. It has been
removed from the repo and replaced with a labelled placeholder. Every other
image in `assets/` was checked and is watermark-free, but their licences still
need confirming before this goes public.

**Remote images.** Photography and the Paladin wordmark load directly from
`paladinenvirotech.com`. If those files are renamed or moved on the live site
they will break here. Worth copying them into `assets/` before this goes to
anyone outside the team.

**Fonts.** The four Restart Hard weights are served as `.otf` from this repo,
which makes them publicly downloadable. Confirm the licence covers web
embedding before putting this on a public URL.

**Privacy.** The site is `noindex` via meta tag and HTTP header. If a client
link needs to stay private, add Vercel password protection on the project too.
