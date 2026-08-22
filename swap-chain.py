"""Rebuild the chain-comparison component on /platform.

Same reconciliation as the timeline rail: Roboto and the Google Fonts links go,
the palette maps onto the site tokens, fixed padding becomes the site's clamp()
gutters, and the inline <script> moves to motion.js because a script tag inside
a React-rendered template never executes.

The band keeps the tightened 44/76px padding from build 1.6.0 rather than the
component's 88/96px, and the h2 keeps its 40px cap so it stays on one line.
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/platform.html"

CSS = """
/* Chain comparison: a tangled multi-vendor path that draws in with scroll,
   against one straight Paladin line. Replaces a row of outlined boxes. */
.pal-chain-svg { width: 100%; margin-top: 20px; display: block; }
.pal-chain-label { font-size: 11px; letter-spacing: 1.4px; text-transform: uppercase; color: #8FA6BA; }
.pal-chain-label.is-amber { color: #A9832F; }
.pal-chain-caption { font-size: 14px; line-height: 1.6; font-weight: 300; color: #8FA6BA; margin-top: 8px; }
.pal-chain-divider { height: 1px; background: rgba(255,255,255,0.16); margin: clamp(28px, 3.5vw, 40px) 0; }
.pal-chain-node { opacity: 0; transition: opacity 400ms ease; }
.pal-line-a { opacity: 0; transition: opacity 400ms ease; }
.pal-line-b { opacity: 0; transition: opacity 400ms ease 900ms; }
.pal-line-c { opacity: 0; transition: opacity 500ms ease 1100ms; }
.pal-chain-caption.is-pal { color: #DDE3E9; margin-top: 16px; opacity: 0; transition: opacity 500ms ease 1300ms; }
.pal-straight { transform: scaleX(0); transform-origin: 0 35px; transition: transform 900ms cubic-bezier(0.2,0.7,0.1,1); }
.is-in .pal-line-a, .is-in .pal-line-b, .is-in .pal-line-c, .is-in .pal-chain-caption.is-pal { opacity: 1; }
.is-in .pal-straight { transform: scaleX(1); }
@media (prefers-reduced-motion: reduce) {
  .pal-chain-node, .pal-line-a, .pal-line-b, .pal-line-c, .pal-chain-caption.is-pal { opacity: 1 !important; transition: none !important; }
  .pal-straight { transform: none !important; transition: none !important; }
  .pal-tangle { clip-path: none !important; }
}
"""

NODES = [(128, 78, 52, "Broker"), (262, 108, 140, "Transport"),
         (396, 82, 54, "Processor"), (528, 100, 132, "Downstream exporter")]

circles = "".join(
    f'<circle class="pal-chain-node" data-chain-node="{i}" cx="{x}" cy="{y}" r="4" '
    f'fill="#14304C" stroke="rgba(255,255,255,0.55)" stroke-width="1.5"></circle>'
    for i, (x, y, _, _) in enumerate(NODES))
labels = "".join(
    f'<text class="pal-chain-node" data-chain-node="{i}" x="{x}" y="{ty}" text-anchor="middle" '
    f'font-size="14" font-weight="300" fill="#DDE3E9">{name}</text>'
    for i, (x, _, ty, name) in enumerate(NODES))

COMPONENT = f'''<div>
      <div class="pal-chain-label">The typical chain</div>
      <svg class="pal-chain-svg" viewBox="0 0 640 190" role="img" aria-label="A tangled path through Broker, Transport, Processor and Downstream exporter">
        <path class="pal-tangle" data-chain-tangle d="M0 95 C 60 30, 90 30, 128 78 S 200 175, 262 108 S 330 15, 396 82 S 470 178, 528 100 S 600 40, 640 95" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="1.5" stroke-dasharray="7 7"></path>
        {circles}{labels}
      </svg>
      <div class="pal-chain-caption">Four companies, four sets of paperwork, three points where custody changes hands.</div>

      <div class="pal-chain-divider"></div>

      <div class="pal-chain-label is-amber">Paladin</div>
      <div data-chain-paladin>
        <svg class="pal-chain-svg" viewBox="0 0 640 70" role="img" aria-label="One straight line from pickup to final disposition">
          <line class="pal-straight" x1="0" y1="35" x2="640" y2="35" stroke="#A9832F" stroke-width="2"></line>
          <circle class="pal-line-a" cx="8" cy="35" r="5" fill="#A9832F"></circle>
          <circle class="pal-line-b" cx="632" cy="35" r="5" fill="#A9832F"></circle>
          <text class="pal-line-a" x="8" y="14" font-size="13" font-weight="300" fill="#DDE3E9">Pickup</text>
          <text class="pal-line-b" x="632" y="14" text-anchor="end" font-size="13" font-weight="300" fill="#DDE3E9">Final disposition</text>
          <text class="pal-line-c" x="320" y="62" text-anchor="middle" font-size="16" font-weight="400" fill="#FFFFFF">One platform, pickup to final disposition</text>
        </svg>
        <div class="pal-chain-caption is-pal">One company, one record, zero custody transfers outside the system.</div>
      </div>
    </div>'''

s = open(PAGE, encoding="utf-8").read()
assert "pal-chain-svg" not in s, "already applied"

# Each page's helmet style block ends differently, so anchor on its close.
close = s.find("</style>")
assert close > 0, "no style block"
s = s[:close] + CSS + s[close:]

# replace the right-hand column of the band, which holds the old boxed chain
# derive the band bounds from the current file, after the CSS insert
i = s.find("The typical chain")
assert i > 0, "component not found"
a = s.rfind('<div data-reveal', 0, i)
depth, k = 0, a
while k < len(s):
    if s.startswith("<div", k):
        depth += 1; k += 4
    elif s.startswith("</div>", k):
        depth -= 1; k += 6
        if depth == 0:
            break
    else:
        k += 1
b = k
band = s[a:b]
marker = band.find("The typical chain")
col_start = band.rfind("<div>", 0, marker)
depth, j = 0, col_start
while j < len(band):
    if band.startswith("<div", j):
        depth += 1; j += 4
    elif band.startswith("</div>", j):
        depth -= 1; j += 6
        if depth == 0:
            break
    else:
        j += 1
old_col = band[col_start:j]
assert "Downstream exporter" in old_col, "wrong column matched"
band = band[:col_start] + COMPONENT + band[j:]
s = s[:a] + band + s[b:]

open(PAGE, "w", encoding="utf-8").write(s)
print(f"replaced {len(old_col)} chars of boxed chain with the drawn comparison")
