# Paladin EnviroTech — site prototype

**Build 1.16.0**

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
| 1.2.1 | Build stamp visible on homepage; sticky bar no longer covers the footer |
| 1.3.0 | Access gate |
| 1.3.1 | Leadership comp image restored for internal review |
| 1.4.0 | Gate restyled to match Antenna's Conscious Compass |
| 1.5.0 | Real logo, scroll-driven map, deeper reveals, case-study rebuild, /sitemap |
| 1.6.0 | Article template with byline and share, CEO quote, copy and layout fixes |
| 1.6.1 | Platform mega menu available on every page |
| 1.7.0 | Press page and nav item, quote restyled, design export |
| 1.8.0 | Refined article page integrated from Claude Design |
| 1.9.0 | Copy pass removing machine-written rhetorical patterns |
| 1.10.0 | Favicon set, timeline rail replaces a statistic grid |
| 1.11.0 | Chain comparison rebuilt, press and facility spotlights added |
| 1.12.0 | Spotlight under the map, band grounds stepped, unbuilt nav links made inert |
| 1.13.0 | Two-tone headline treatment extended to the capability pages |
| 1.14.0 | Leadership roster replaces the boxed grid; deep links fixed |
| 1.15.0 | Locations ledger replaces the two boxed location bands |
| 1.16.0 | Facility map inverted onto the light ground |

## Access gate

`gate.js` puts a password screen in front of every page.

- **Password:** `Paladin2026`
- **Share link:** append `?client=b3zG4SPI8DiZEsLv` to any URL to open it
  without typing anything. Access is remembered in that browser afterwards.

Change both values at the top of `gate.js` before sharing. The password is
stored as a SHA-256 hash, not in plain text; the file's header comment has the
one-liners for generating a new one.

### What this is and is not

It is a front-end gate. It keeps casual visitors and search engines out, and it
makes the prototype feel like a private preview.

**It is not security.** The page HTML is served to the browser whether or not
the gate is satisfied, so anyone who opens developer tools, disables
JavaScript, or requests a page directly can read the content. Nothing
confidential should go behind it.

Real protection on Vercel is Password Protection, which runs at the edge before
any content is served. It is included on Enterprise, and on Pro as the Advanced
Deployment Protection add-on at $150/month. If the prototype needs to be
genuinely private rather than merely non-public, that is the mechanism.

### Styling

The gate matches Antenna's Conscious Compass screen: cream ground `#F0EEE7`,
near-black `#0E0E0E`, a white card with square corners, and a button that stays
grey until something is typed. Colours and measurements were sampled from the
reference screenshot rather than estimated.

The headline is sized by script rather than CSS. Antenna's typeface is not
available here, and every substitute sets at a different width, so a fixed
font-size either wrapped onto extra lines or left the column short. The script
measures the widest line and scales the type to fill the column, reproducing
the proportions rather than the point size. It re-runs on resize.

### Antenna logo

`assets/antenna-logo.png` is the supplied artwork, 784x200 with transparency,
displayed at 30px tall. If vector artwork arrives later, save it over that path
or add it ahead of the PNG in the sources list in `gate.js`.

## Building

```
./build.sh 1.5.1 "what changed"
```

Stamps the version across every page, regenerates `/sitemap` from the pages on
disk, and packages the site. Use this rather than the individual scripts, so
the sitemap cannot drift from the actual page set.

## Component variety

The outlined box and the statistic grid were carrying too much of the site.
Three components now break that up.

**Timeline rail** on the homepage, replacing a 2x2 statistic grid. Beats reveal
in sequence, a tick draws out from the rail, and a gold progress line follows
scroll down the track.

**Chain comparison** on /platform, replacing a row of outlined boxes. A tangled
multi-vendor path draws in with scroll progress and its four nodes appear as the
line reaches them, set against one straight Paladin line that plays once in
view.

**Spotlights** on /press and /network. The press page opens on the announcement
being pushed, with a dated badge, a pull quote and two calls to action, before
the undifferentiated release list. The network page pulls Helmond forward and
signposts the newsroom piece about it, which also gives the blog a route in
from a page buyers actually visit.

Both supplied components were reconciled to the site rather than dropped in
as-is: Roboto and its Google Fonts links removed, palette mapped onto the site
tokens, fixed 88/96px padding replaced with the site's clamp() gutters. Their
inline `<script>` tags were dropped and the behaviour moved into `motion.js`,
because the pages are React-rendered and a script tag inside the template never
executes. Hooks are namespaced `data-timeline-*` and `data-chain-*` since
`data-rail` was already taken.

Two integration details that repeat for any future component of this kind. The
generic reveal tagger has to skip anything that animates itself, or each part
fades twice and stutters. And every scroll-driven piece needs a fail-visible
timeout, so a wiring problem never leaves a diagram half-drawn.

## Map on the light ground

The facility map moved from `#14304C` to the paper ground, so every colour in
it had to be remapped. Most were chosen for a dark background and fail on
light: the city labels and node dots measured 2.33:1 against `#F5F6F7`, the
white Tampa label 1.08:1.

Remapped by role rather than by find-and-replace, because `#8FA6BA` was doing
two jobs in the same file. Contrast against `#F5F6F7` in brackets:

| Element | Was | Now |
| --- | --- | --- |
| City labels | `#8FA6BA` (2.33) | `#47586B` (6.75) |
| Node dots | `#8FA6BA` (2.33) | `#5B7085` (4.73) |
| Tampa label | `#FFFFFF` (1.08) | `#0B2138` (15.06) |
| Grid lines | `rgba(255,255,255,0.07)` | `rgba(11,33,56,0.10)` |
| HQ marker fill | `#14304C` | `#F5F6F7` |
| Route arcs | `#A9832F` at 0.45 opacity | same colour at 0.75, 1.2px |
| Legend text | `#5B7085` | unchanged (4.73) |

The arcs needed the opacity lift separately: 0.45 reads on navy but goes faint
on paper. The mobile routing list that replaces this map below 760px is built
by `motion.js` and was inverted to match.

## Open question: how many facilities

The site states its own footprint three different ways:

| Where | Says |
| --- | --- |
| `/network` H1 | Ten facilities. Three continents. |
| `/network` map | 10 markers, Duleek and Dublin combined as one |
| `/network` ledger | Eleven sites, Duleek and Dublin listed separately |
| `/network` stat band | 7 facilities across the United States, 3 countries outside the US |
| `/company` stat band | 10 facilities operating under one standard |

Seven US sites plus four international is eleven; ten holds only if Duleek and
Dublin count as one facility. Whether they do is a question about the business,
so the conflict is left visible rather than quietly resolved. Pick a number and
it needs changing in four places.

## Deep links

Arriving at `/company#leadership` used to leave you at the top of the page. The
browser acts on the URL hash while the document is still empty, because content
is React-rendered a beat later, so there is nothing to scroll to yet. Thirteen
links across the site point at that anchor from the footer, and every one of
them was landing in the wrong place.

`motion.js` now re-applies the hash once content exists, offsetting by the
sticky header's height so the target is not tucked underneath it. Pages opened
without a hash are left alone.

## Headline accent

The homepage sets part of a headline in copper against white. It now appears on
the hero headline of the seven capability and story pages as well, one accented
clause each, so it reads as part of the system.

Deliberately not everywhere. Contact, press and blog stay plain because they
are utility pages, the two articles stay plain because editorial headlines are
already doing their own work, and the company page has a four-word headline
with nothing worth splitting. The accent stops meaning anything if every
headline carries one.

The accented clause is the differentiating half, not simply the last few words:
`national security`, `One system`, `highest risk`, `Processed domestically`.

Two things to watch when adding more. Avoid starting the accent on an article
or preposition, since a wrap can leave it orphaned in copper at the end of a
line, which is what happened first on secure-itad before it was tightened from
"the highest risk" to "highest risk". And copper measures 4.64:1 on navy and
3.51:1 on white, both clearing the 3:1 large-text threshold, but only 2.91:1 on
the paper-shade ground, so keep the treatment off `#E7EAEE` bands.

`accent-headlines.py` records what was applied where.

## Band grounds

No two touching bands share a background. Adjacent sections on the same ground
read as one long section with an unexplained gap, which is what made the
company-page quote look broken.

`normalise-bands.py` enforces it. Fixing collisions one at a time just moves
them down the page, so the script walks each page's bands in order and resolves
the whole sequence: where a band matches the one above, it steps to another
value in the same family that also differs from the band below. Light bands
step through `#FFFFFF`, `#F5F6F7`, `#E7EAEE`; dark through `#0B2138`, `#14304C`.
The fixed CTA bar is skipped, since it floats over the stack rather than
sitting in it.

Run it after adding or reordering any band. It reports what it changed and is
safe to run repeatedly.

## Navigation link states

Only mega-menu items with a page of their own are links. The rest render as
dimmed, unclickable text, so the menu never promises a destination that does
not exist. Six of the eighteen are live.

Three previously pointed at an approximate page: Chain-of-custody ERP and
Neodymium & dysprosium went to pages that cover them only as a section, and
Wind turbine & energy assets to the critical materials page. Those now sit
inactive until they have somewhere real to go.

The rule lives in `GROUPS` at the top of `nav-menu.js`: give an item a URL and
it becomes a link on every page at once, including the homepage's own
React-owned panel, whose anchors are swapped for inert text when they have no
target.

Still outstanding elsewhere: Privacy, Terms, the language switcher, and two
press-kit download links are placeholders pointing at `#`.

## Favicon

`favicon.ico`, `favicon-16.png`, `favicon-32.png` and `apple-touch-icon.png`
are generated from the supplied shield, trimmed to its ink and padded onto the
brand navy so it reads against light browser chrome. A `theme-color` of
`#0B2138` is set for mobile browser UI.

**The source artwork is 23x29 pixels.** That is enough for the 16 and 32px
favicons, which is where the icon actually lives, but the 180px Apple touch
icon is an upscale and looks soft on a home screen. Vector or a large PNG of
the shield would fix it. I tried sharpening the upscale and it distorted the
geometry, so the honest soft version is what ships.

## Copy conventions

A sweep removed the rhetorical patterns that made the writing read as
machine-generated. The dominant one was antithesis, "X, not Y", which appeared
25 times: it sounds persuasive but carries almost no information, since the
reader learns what something is not, which they were not wondering about.

Removed across the site:

| Pattern | Count |
| --- | --- |
| "X, not Y" | 25 |
| "rather than Y" | 7 |
| "instead of Y" | 6 |
| "different X, same Y" | 1 |
| "the honest answer is" | 1 |
| "is what makes", "matters more than", "before it is a" | 4 |
| sentence-initial "And" for rhythm | 1 |

Two instances were kept on purpose. The turbine line compares kilograms with
grams, which is a real measurement contrast, and the "1 consolidated report
instead of a dozen mismatched vendor files" caption is the point of that
statistic.

The passes are `copy-pass.py`, `copy-pass2.py` and `copy-pass3.py`. Each pair
is asserted against an expected occurrence count, so a miss fails loudly rather
than silently skipping. They are one-time scripts, kept as a record of what
changed.

Worth watching in future rounds: a redesign or a new page from Claude Design
will reintroduce these shapes, since they are a default of the medium. The
grep patterns in those scripts are the quickest way to check.

## Design handover and re-import

`export-for-design.py` writes a clean copy of a page to `for-claude-design/`,
stripped of the overlay layer that belongs to the deployed build rather than to
a design file: the access gate, the motion and nav-menu scripts, the responsive
stylesheet, the build-version meta and the noindex tag. It keeps the Claude
Design runtime, the `@font-face` block and the `style-hover` attributes.

`integrate-article.py` brings a refined page back. Claude Design returns a
self-contained bundle, roughly 1.6MB, with the fonts, hero image and runtime
inlined as UUID-keyed resources. Shipping that as-is would carry a second
private copy of the four fonts, so the script extracts the template and points
it back at the shared assets, taking the page from 1637KB to 32KB.

It also repairs what a round trip through the design tool changes:

- `Name.dc.html` links become the site's clean URLs
- font, image and runtime UUIDs become shared paths, and the hero image is
  compared against what the site already ships rather than duplicated
- the Press nav item, which the redesign repointed at Blog, is repointed back
- the social share row, which the redesign emptied to `#`, is restored
- the overlay layer and social meta are re-linked

Each of those is a real change the tool made, so expect to re-run the script
after every design pass rather than treating the returned file as final.

## /sitemap

An internal reference page at `/sitemap`, deliberately absent from the header
and footer so it is reachable only by URL. It is generated by
`generate-sitemap.py`, not hand-maintained:

- **Architecture** is grouped by the role each page plays rather than by
  business unit, so a new acquisition slots into an existing branch instead of
  adding a top-level item. Groups are declared in `GROUPS` at the top of the
  generator. A page found on disk but not placed in a group is flagged on the
  page itself rather than silently omitted.
- **Component patterns** are detected by signature in the built markup, so the
  inventory reflects what is actually on the pages. A pattern used on only one
  page is a candidate either for wider reuse or for removal.

Adding, removing or renaming a page means editing `GROUPS`, then rebuilding.

## Notes## Notes## Notes

**Runtime dependency.** `support.js` loads React, ReactDOM and Babel from
unpkg.com at page load, so the site needs an internet connection and will not
render from a `file://` URL. To preview locally, run `python3 -m http.server
8000` in this folder and open `http://localhost:8000`. The script also honours
a `window.__resources` override if you ever need to point those at local copies
for an offline demo.

**Stock imagery.** `assets/leadership.jpg` is a Getty comp with the watermark
still visible, used on the Company page as the leadership photograph. It is in
place deliberately for internal review. It must be replaced with a licensed or
commissioned image before this is shown to the client or made public. Every
other image in `assets/` is watermark-free, but their licences still need
confirming.

**Remote images.** Photography and the Paladin wordmark load directly from
`paladinenvirotech.com`. If those files are renamed or moved on the live site
they will break here. Worth copying them into `assets/` before this goes to
anyone outside the team.

**Fonts.** The four Restart Hard weights are served as `.otf` from this repo,
which makes them publicly downloadable. Confirm the licence covers web
embedding before putting this on a public URL.

**Privacy.** The site is `noindex` via meta tag and HTTP header. If a client
link needs to stay private, add Vercel password protection on the project too.
