"""Generate /sitemap from the built site.

Reads every page in paladin-site/, derives the information architecture from
the real header navigation and the pages present on disk, inventories the
component patterns each page uses, and writes sitemap.html in the Paladin
design system.

Run it after adding, removing or renaming pages, or after changing the nav.
`build.sh` runs it automatically.

Deliberately not linked from the header or footer: reachable only at /sitemap.
"""
import glob
import html
import json
import os
import re
from collections import OrderedDict
from datetime import date

SITE = "/home/claude/paladin-site"
OUT = os.path.join(SITE, "sitemap.html")

# Where each page sits in the IA. Pages found on disk but not listed here are
# reported as unplaced rather than silently dropped.
GROUPS = OrderedDict([
    ("Entry", ["/"]),
    ("Platform", ["/platform", "/secure-itad", "/electronics-recycling",
                  "/paladin-local"]),
    ("Critical materials", ["/critical-materials"]),
    ("Markets", ["/industries"]),
    ("Network", ["/network"]),
    ("Company", ["/company", "/blog", "/insight-rare-earth-recovery", "/press"]),
    ("Conversion", ["/contact"]),
    ("Campaign", ["/rare-earth-freedom-250"]),
    ("Utility", ["/sitemap"]),
])

NOTES = {
    "/": "Homepage. Campaign takeover zone, capability cards, proof strip.",
    "/platform": "The integrated lifecycle: intake, destruction, recycling, recovery, reporting.",
    "/secure-itad": "Certified destruction and serial-level chain of custody.",
    "/electronics-recycling": "Domestic processing and controlled downstream handling.",
    "/paladin-local": "Hub-and-satellite coverage for regional and mid-market sites.",
    "/critical-materials": "REcapture rare-earth recovery. The primary differentiator.",
    "/industries": "Sector hub: hyperscale, OEM, enterprise, government.",
    "/network": "Facility map, hub-and-satellite footprint, certifications by entity.",
    "/company": "Who Paladin is, leadership, operating standard.",
    "/blog": "Newsroom index. Bylines link through to the article template.",
    "/insight-rare-earth-recovery": "Article template. Byline, author panel, cross-links, share row.",
    "/press": "Press releases, media contact and press kit. Linked from the main nav.",
    "/contact": "Primary conversion point. Reachable from every page.",
    "/rare-earth-freedom-250": "Campaign takeover page. Template for sponsorship activations.",
    "/sitemap": "This page. Not linked in navigation.",
}

# Component patterns, detected by signature in the rendered markup.
COMPONENTS = [
    ("Sticky masthead", r'position: sticky;\s*top: 0', "Navigation"),
    ("Mobile menu drawer", r'data-nav-toggle', "Navigation"),
    ("Platform mega menu", r'nav-menu\.js', "Navigation"),
    ("Global footer sitemap", r'<footer', "Navigation"),
    ("Persistent CTA bar", r'data-stickybar', "Conversion"),
    ("Gold-rule CTA block", r'border-left: 4px solid #A9832F', "Conversion"),
    ("Inline lead form", r'<input', "Conversion"),
    ("Timeline rail (scroll-driven)", r'data-timeline-rail', "Proof"),
    ("Statistic band", r'border-right: 1px solid rgba\(255,255,255,0\.16\)|border-right: 1px solid #E7EAEE', "Proof"),
    ("Animated count-up", r'data-countup', "Proof"),
    ("Logo / credential strip", r'Client marks are placeholders|WORKING WITH|Working with', "Proof"),
    ("Numbered capability cards", r'>0[1-9]</span>', "Explanation"),
    ("Numbered process steps", r'grid-template-columns: minmax\(48px, 90px\)', "Explanation"),
    ("Two-column text and image", r'aspect-ratio: 4 / 3', "Explanation"),
    ("Pull-quote band", r'font-size: clamp\(22px, 2\.4vw, 32px\)', "Explanation"),
    ("Facility map (SVG)", r'aria-label="Paladin facility network', "Data"),
    ("Mobile routing list", r'aria-label="Paladin facility network', "Data"),
    ("Scroll parallax band", r'data-parallax', "Motion"),
    ("Campaign takeover motion", r'data-car', "Motion"),
    ("Scroll reveal", r'data-reveal', "Motion"),
    ("Pull quote with attribution", r'<blockquote', "Editorial"),
    ("Author byline", r'>6 min read<|min read', "Editorial"),
    ("Author panel and cross-links", r'More by ', "Editorial"),
    ("Social share row", r'shareArticle\?mini=true', "Editorial"),
]


def page_url(filename):
    base = os.path.basename(filename)
    return "/" if base == "index.html" else "/" + base[:-5]


def build():
    files = sorted(glob.glob(os.path.join(SITE, "*.html")))
    by_url = {page_url(f): f for f in files}

    version = "0.0.0"
    vf = os.path.join(SITE, "version.json")
    if os.path.exists(vf):
        version = json.load(open(vf)).get("version", version)

    # component inventory: which pages use which pattern
    usage = OrderedDict()
    for name, pattern, family in COMPONENTS:
        hits = []
        for url, path in by_url.items():
            if url == "/sitemap":
                continue
            src = open(path, encoding="utf-8").read()
            if re.search(pattern, src):
                hits.append(url)
        if hits:
            usage[name] = (family, sorted(hits))

    placed = {u for urls in GROUPS.values() for u in urls}
    unplaced = [u for u in by_url if u not in placed]

    # ---- markup -------------------------------------------------------
    def esc(t):
        return html.escape(t, quote=True)

    rows = []
    for group, urls in GROUPS.items():
        live = [u for u in urls if u in by_url or u == "/sitemap"]
        if not live:
            continue
        items = []
        for u in live:
            missing = u not in by_url and u != "/sitemap"
            items.append(
                '<li style="margin: 0 0 14px; padding-left: 18px; position: relative;">'
                '<span style="position: absolute; left: 0; top: 9px; width: 6px; height: 6px; '
                'background: #A9832F;"></span>'
                f'<a href="{esc(u)}" style="color: #0B2138; font-size: 17px; font-weight: 500; '
                'text-decoration: none; border-bottom: 1px solid #C7CFD7;">'
                f'{esc(u)}</a>'
                + (' <span style="color:#B4382E;font-size:12px;">missing</span>' if missing else '')
                + f'<p style="margin: 6px 0 0; color: #47586B; font-size: 14px; font-weight: 300; '
                  f'line-height: 21px;">{esc(NOTES.get(u, ""))}</p>'
                '</li>'
            )
        rows.append(
            '<div style="padding: 32px 0; border-top: 1px solid #E7EAEE; display: grid; '
            'grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); '
            'gap: clamp(16px, 3vw, 48px);">'
            f'<div><span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; '
            f'color: #5B7085;">{esc(group)}</span>'
            f'<p style="margin: 8px 0 0; color: #8FA6BA; font-size: 13px; font-weight: 300;">'
            f'{len(live)} page{"s" if len(live) != 1 else ""}</p></div>'
            '<div style="grid-column: span 2;"><ul style="list-style: none; margin: 0; padding: 0;">'
            + "".join(items) + '</ul></div></div>'
        )

    families = OrderedDict()
    for name, (family, hits) in usage.items():
        families.setdefault(family, []).append((name, hits))

    comp_rows = []
    for family, entries in families.items():
        cells = []
        for name, hits in entries:
            cells.append(
                '<div style="padding: 20px 0; border-top: 1px solid #E7EAEE;">'
                f'<p style="margin: 0 0 6px; color: #0B2138; font-size: 16px; font-weight: 500;">{esc(name)}</p>'
                f'<p style="margin: 0; color: #5B7085; font-size: 13px; font-weight: 300; '
                f'line-height: 20px;">{esc(", ".join(hits))}</p>'
                f'<p style="margin: 6px 0 0; color: #8FA6BA; font-size: 12px; font-weight: 300;">'
                f'used on {len(hits)} page{"s" if len(hits) != 1 else ""}</p>'
                '</div>'
            )
        comp_rows.append(
            '<div style="padding: 28px 0; border-top: 1px solid #C7CFD7; display: grid; '
            'grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); '
            'gap: clamp(16px, 3vw, 48px);">'
            f'<div><span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; '
            f'color: #A9832F;">{esc(family)}</span></div>'
            '<div style="grid-column: span 2;">' + "".join(cells) + '</div></div>'
        )

    warn = ""
    if unplaced:
        warn = ('<p style="margin: 0 0 24px; padding: 14px 18px; background: #FFF4E5; '
                'border-left: 4px solid #A9832F; color: #47586B; font-size: 14px;">'
                'Pages on disk but not placed in the architecture above: '
                + esc(", ".join(sorted(unplaced))) +
                '. Add them to GROUPS in generate-sitemap.py.</p>')

    total = len([u for u in by_url if u != "/sitemap"])

    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Site structure | Paladin EnviroTech</title>
<meta name="description" content="Information architecture and component inventory for the Paladin EnviroTech prototype.">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#0B2138">
<meta name="robots" content="noindex, nofollow">
<meta name="build-version" content="{version}">
<meta name="build-date" content="{date.today().isoformat()}">
<script src="/gate.js"></script>
<link rel="stylesheet" href="/responsive.css">
<style>
  @font-face {{ font-family: "Restart Hard"; src: url("fonts/RestartHard-Light.otf") format("opentype"); font-weight: 300; }}
  @font-face {{ font-family: "Restart Hard"; src: url("fonts/RestartHard-Regular.otf") format("opentype"); font-weight: 400; }}
  @font-face {{ font-family: "Restart Hard"; src: url("fonts/RestartHard-Medium.otf") format("opentype"); font-weight: 500; }}
  @font-face {{ font-family: "Restart Hard"; src: url("fonts/RestartHard-SemiBold.otf") format("opentype"); font-weight: 600; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #F5F6F7; color: #0B2138;
         font-family: "Restart Hard", system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
  a:hover {{ border-bottom-color: #A9832F !important; }}
</style>
</head>
<body>
<div>
  <header style="background: #0B2138; padding: 22px clamp(24px, 5vw, 72px);">
    <a href="/" style="display: inline-flex; align-items: center; gap: 11px; text-decoration: none;">
      <span style="color: #FFFFFF; font-size: 15px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;">Paladin EnviroTech</span>
    </a>
  </header>

  <div style="max-width: 1200px; margin: 0 auto; padding: clamp(48px, 7vw, 96px) clamp(24px, 5vw, 72px) clamp(64px, 8vw, 120px);">
    <span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Internal reference</span>
    <h1 style="font-size: clamp(32px, 4.4vw, 56px); line-height: 1.1; font-weight: 300; margin: 16px 0 18px;">Site structure</h1>
    <p style="font-size: clamp(17px, 1.4vw, 20px); line-height: 1.5; font-weight: 300; color: #47586B; margin: 0 0 8px; max-width: 720px;">
      The information architecture and component inventory for this prototype, generated from the
      pages themselves. It is not linked from the navigation and updates whenever the site is rebuilt.
    </p>
    <p style="color: #8FA6BA; font-size: 13px; font-weight: 300; margin: 0 0 48px;">
      {total} pages &middot; {len(usage)} component patterns &middot; build {version} &middot; {date.today().isoformat()}
    </p>

    {warn}

    <h2 style="font-size: clamp(24px, 2.4vw, 32px); font-weight: 500; margin: 0 0 8px;">Architecture</h2>
    <p style="color: #47586B; font-size: 15px; font-weight: 300; line-height: 24px; margin: 0 0 8px; max-width: 720px;">
      Grouped by the role each page plays rather than by business unit, so new acquisitions and
      capabilities slot into an existing branch instead of adding a top-level item.
    </p>
    {''.join(rows)}

    <h2 style="font-size: clamp(24px, 2.4vw, 32px); font-weight: 500; margin: 64px 0 8px;">Component patterns</h2>
    <p style="color: #47586B; font-size: 15px; font-weight: 300; line-height: 24px; margin: 0 0 8px; max-width: 720px;">
      Detected by signature in the built markup, so this reflects what is actually on the pages.
      Patterns used on one page only are candidates either for wider reuse or for removal.
    </p>
    {''.join(comp_rows)}

    <p style="margin: 56px 0 0; padding-top: 20px; border-top: 1px solid #E7EAEE; color: #5B7085; font-size: 12px; letter-spacing: 0.6px;">
      Generated by generate-sitemap.py &middot; build {version} &middot; {date.today().isoformat()}
    </p>
  </div>
</div>
</body>
</html>
'''
    open(OUT, "w", encoding="utf-8").write(doc)
    print(f"wrote {OUT}")
    print(f"  {total} pages across {len([g for g in GROUPS if any(u in by_url for u in GROUPS[g])])} groups")
    print(f"  {len(usage)} component patterns detected")
    if unplaced:
        print(f"  WARNING unplaced pages: {unplaced}")


if __name__ == "__main__":
    build()
