"""Replace the two boxed location bands on /network with the split ledger.

The United States and International sections were separate bands of outlined
cards, which pushed the certification note far down the page and made the
footprint read as two unrelated lists. This is one band, two columns, numbered
01 to 11, with the note held beside the international column.

Reconciled to the site as before: Roboto and the Google Fonts links removed,
palette mapped onto the site tokens (#F4F5F7 -> #F5F6F7, #102030 -> #0B2138,
#7E8B98 -> #5B7085, #C79447 -> #A9832F, #D5DBE2 -> #C7CFD7, #5A6470 ->
#47586B), and the fixed 96/72px padding replaced with the site's clamp()
gutters and 1600px measure.

NOTE ON THE COUNT: the supplied headline says eleven sites and lists Duleek and
Dublin separately. The page H1 says "Ten facilities", the map shows them as one
combined marker, and the company page says ten. That conflict is left visible
rather than quietly resolved, because whether Duleek and Dublin are one site or
two is a question about the business.
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/network.html"

CSS = """
/* Locations ledger: one band, two regional columns, numbered continuously.
   Replaces two bands of outlined cards. */
.pal-loc-head { max-width: 760px; }
.pal-loc-eyebrow { font-size: 12px; font-weight: 500; letter-spacing: 1.2px; text-transform: uppercase; color: #5B7085; }
.pal-loc-head h2 { margin: 20px 0 0; font-size: clamp(30px, 3.8vw, 52px); line-height: 1.06; font-weight: 400; letter-spacing: -0.6px; color: #0B2138; text-wrap: pretty; }
.pal-loc-cols { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(40px, 5vw, 72px); margin-top: clamp(40px, 5vw, 64px); }
.pal-loc-region { display: flex; align-items: baseline; justify-content: space-between; padding-bottom: 16px; border-bottom: 2px solid #0B2138; }
.pal-loc-region-name { font-size: 12px; font-weight: 500; letter-spacing: 1.4px; text-transform: uppercase; color: #0B2138; }
.pal-loc-region-count { font-size: 12px; font-weight: 400; letter-spacing: 0.6px; color: #5B7085; }
.pal-loc-site { display: grid; grid-template-columns: 32px 1fr; column-gap: 20px; align-items: baseline; padding: clamp(18px, 2vw, 24px) 0; border-bottom: 1px solid #C7CFD7; }
.pal-loc-num { font-size: 12px; color: #A9832F; }
.pal-loc-name { font-size: clamp(19px, 1.7vw, 22px); line-height: 1.3; font-weight: 400; color: #0B2138; }
.pal-loc-desc { margin-top: 8px; font-size: 15px; line-height: 1.6; font-weight: 300; color: #47586B; text-wrap: pretty; }
.pal-loc-note { margin-top: clamp(32px, 4vw, 40px); border-left: 2px solid #A9832F; padding: 4px 0 4px 20px; }
.pal-loc-note p { margin: 0; font-size: 13px; line-height: 1.65; font-weight: 300; color: #47586B; text-wrap: pretty; }
@media (max-width: 1024px) {
  .pal-loc-cols { grid-template-columns: 1fr; gap: clamp(40px, 6vw, 56px); }
}
"""

US = [
    ("Tampa, Florida", "Headquarters. Downstream vendor management, data sanitization, testing, repair and materials recovery."),
    ("St. Cloud, Minnesota", "Collection, dismantling and circuit-board processing, physical and logical data sanitization."),
    ("Laurel, Maryland", "DC / Baltimore region intake and processing."),
    ("Columbus, Ohio", "Midwest intake and processing."),
    ("Olympia, Washington", "Pacific Northwest intake and processing."),
    ("Dallas / Fort Worth, Texas", "South-central intake and processing."),
    ("Phoenix, Arizona", "Southwest intake and processing."),
]
INTL = [
    ("Duleek, Ireland", "Collection, dismantling and circuit-board processing, data sanitization and materials recovery."),
    ("Dublin, Ireland", "Logistics and intake."),
    ("Helmond, Netherlands", "R&amp;L Recycling B.V., European ITAD and e-recycling platform."),
    ("Suwon, South Korea", "Daeheung M&amp;T, collection, processing and materials recovery."),
]
NOTE = ("Certifications (R2, RIOS, ISO 9001/14001/45001, WEEELABEX) are held per site "
        "and per entity. Activities at non-certified facilities, transfer, storage or "
        "consolidation, are managed under downstream vendor controls and are not "
        "included in a site's certification scope.")


def site(n, name, desc):
    return (f'<div class="pal-loc-site"><div class="pal-loc-num">{n:02d}</div><div>'
            f'<div class="pal-loc-name">{name}</div>'
            f'<div class="pal-loc-desc">{desc}</div></div></div>')


us_rows = "".join(site(i + 1, n, d) for i, (n, d) in enumerate(US))
intl_rows = "".join(site(len(US) + i + 1, n, d) for i, (n, d) in enumerate(INTL))
total = len(US) + len(INTL)

BAND = f'''<div data-reveal="1" style="background: #F5F6F7; padding: clamp(56px, 7vw, 96px) 0 clamp(64px, 8vw, 104px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div class="pal-loc-head">
      <div class="pal-loc-eyebrow">Footprint</div>
      <h2>Eleven sites, one chain of custody.</h2>
    </div>
    <div class="pal-loc-cols">
      <div>
        <div class="pal-loc-region">
          <div class="pal-loc-region-name">United States</div>
          <div class="pal-loc-region-count">{len(US)} sites</div>
        </div>
        {us_rows}
      </div>
      <div>
        <div class="pal-loc-region">
          <div class="pal-loc-region-name">International</div>
          <div class="pal-loc-region-count">{len(INTL)} sites</div>
        </div>
        {intl_rows}
        <div class="pal-loc-note"><p>{NOTE}</p></div>
      </div>
    </div>
  </div>
</div>'''

s = open(PAGE, encoding="utf-8").read()
assert "pal-loc-cols" not in s, "already applied"

close = s.find("</style>")
assert close > 0, "no style block"
s = s[:close] + CSS + s[close:]


def band_bounds(src, marker):
    i = src.find(marker)
    assert i > 0, f"marker not found: {marker}"
    start = src.rfind('<div data-reveal', 0, i)
    depth, j = 0, start
    while j < len(src):
        if src.startswith("<div", j):
            depth += 1; j += 4
        elif src.startswith("</div>", j):
            depth -= 1; j += 6
            if depth == 0:
                break
        else:
            j += 1
    return start, j


a1, b1 = band_bounds(s, ">United States<")
a2, b2 = band_bounds(s, "WEEELABEX")
assert a2 > b1, "bands are not in the expected order"
assert s[b1:a2].strip() == "", "something sits between the two bands"

old = s[a1:b2]
assert "Suwon" in old and "Tampa" in old, "wrong bands matched"
s = s[:a1] + BAND + s[b2:]

open(PAGE, "w", encoding="utf-8").write(s)
print(f"replaced {len(old)} chars across two bands with one ledger")
print(f"sites listed: {total} ({len(US)} US, {len(INTL)} international)")
