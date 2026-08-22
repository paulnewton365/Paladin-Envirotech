"""Swap the boxed leadership grid on /company for the roster layout.

Reconciled to the site as before: Roboto and the Google Fonts links removed,
palette mapped onto the site tokens (#E8EBEF -> #E7EAEE, #102030 -> #0B2138,
#5A6470 -> #47586B, #C9D0D8 -> #C7CFD7), and the fixed 104/72px padding
replaced with the site's clamp() gutters and 1600px measure.

The headline becomes "Leading the work".

The band keeps id="leadership": thirteen links across the site point at
/company#leadership, and they all break if it goes.
"""
import os

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/company.html"

CSS = """
/* Leadership roster: a ruled two-column list, replacing a grid of boxes. */
.pal-lead-head { border-bottom: 1px solid #0B2138; padding-bottom: clamp(28px, 3.5vw, 44px); }
.pal-lead-eyebrow { font-size: 12px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #5B7085; }
.pal-lead-headgrid { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(32px, 5vw, 96px); align-items: end; margin-top: 24px; }
.pal-lead-headgrid h2 { margin: 0; font-size: clamp(32px, 4.2vw, 58px); line-height: 1.05; font-weight: 500; letter-spacing: -0.5px; color: #0B2138; text-wrap: pretty; }
.pal-lead-intro { margin: 0 0 8px; font-size: 17px; line-height: 1.65; font-weight: 300; color: #47586B; text-wrap: pretty; }
.pal-lead-roster { display: grid; grid-template-columns: repeat(2, 1fr); column-gap: clamp(32px, 5vw, 96px); }
.pal-lead-col { display: flex; flex-direction: column; }
.pal-lead-role { display: grid; grid-template-columns: 1fr auto; align-items: baseline; gap: 24px; padding: clamp(22px, 2.4vw, 30px) 0; border-bottom: 1px solid #C7CFD7; }
.pal-lead-title { font-size: 13px; font-weight: 500; letter-spacing: 1.1px; text-transform: uppercase; color: #0B2138; }
.pal-lead-name { font-size: clamp(19px, 1.8vw, 24px); line-height: 1.2; font-weight: 300; color: #47586B; }
@media (max-width: 1024px) {
  .pal-lead-headgrid { grid-template-columns: 1fr; gap: 28px; }
  .pal-lead-roster { grid-template-columns: 1fr; column-gap: 0; }
}
@media (max-width: 560px) {
  .pal-lead-role { grid-template-columns: 1fr; gap: 6px; }
}
"""

COLUMNS = [
    [("Chief Executive Officer", "Brian Diesselhorst"),
     ("Chief Operating Officer", "Bill Vasquez"),
     ("Chief Financial Officer", "Josh Goodelman"),
     ("Chief of Staff", "Sharon Gryczka")],
    [("SVP, Global Recycling", "Dave Owens"),
     ("SVP, Remarketing", "Keith Layton"),
     ("SVP, Compliance", "Jen Rivero"),
     ("VP, Critical Materials &amp; Defense", "Luke Wray")],
]

INTRO = ("The team spans recycling operations, hyperscale and data-center asset "
         "management, remarketing, reverse logistics, compliance and "
         "critical-materials policy. Every function that touches a customer's "
         "asset has an owner on this list.")


def column(rows):
    cells = "".join(
        '<div class="pal-lead-role">'
        f'<div class="pal-lead-title">{title}</div>'
        f'<div class="pal-lead-name">{name}</div>'
        '</div>' for title, name in rows)
    return f'<div class="pal-lead-col">{cells}</div>'


BAND = f'''<div id="leadership" data-reveal="1" style="background: #E7EAEE; padding: clamp(56px, 7vw, 104px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div class="pal-lead-head">
      <div class="pal-lead-eyebrow">Leadership</div>
      <div class="pal-lead-headgrid">
        <h2>Leading the work</h2>
        <p class="pal-lead-intro">{INTRO}</p>
      </div>
    </div>
    <div class="pal-lead-roster">
      {column(COLUMNS[0])}
      {column(COLUMNS[1])}
    </div>
  </div>
</div>'''

s = open(PAGE, encoding="utf-8").read()
assert "pal-lead-roster" not in s, "already applied"

close = s.find("</style>")
assert close > 0, "no style block"
s = s[:close] + CSS + s[close:]

i = s.find('id="leadership"')
assert i > 0, "leadership band not found"
start = s.rfind("<div", 0, i)
depth, j = 0, start
while j < len(s):
    if s.startswith("<div", j):
        depth += 1; j += 4
    elif s.startswith("</div>", j):
        depth -= 1; j += 6
        if depth == 0:
            break
    else:
        j += 1
old = s[start:j]
assert "Diesselhorst" in old, "wrong band matched"
assert old.count("id=\"leadership\"") == 1

s = s[:start] + BAND + s[j:]
open(PAGE, "w", encoding="utf-8").write(s)
print(f"replaced {len(old)} chars of leadership grid with the roster")
print(f"names carried over: {sum(len(c) for c in COLUMNS)}")
