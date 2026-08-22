"""Swap the homepage's 2x2 statistic grid for the timeline rail.

The supplied component is reconciled to the site rather than dropped in as-is:

  - Roboto and the Google Fonts links go; the site sets Restart Hard
  - its palette maps to the site tokens (#102030 -> #0B2138, #C79447 -> #A9832F,
    #C6CFD8 / #E6EBF0 -> #DDE3E9, #7E8B98 -> #8FA6BA)
  - fixed 88px/96px padding becomes the site's clamp() gutters and 1600px measure
  - the copy it carries had reverted two fixes from the copy pass, so the
    corrected wording is kept
  - its inline <script> is dropped: the page is React-rendered, so a script tag
    inside the template does not execute. The behaviour moves to motion.js.
  - hooks are renamed data-timeline-* because data-rail is already used by the
    horizontal rails on /platform and the article page
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/index.html"

BEATS = [
    ("0", "23:00, window opens", "minutes of downtime to the live environment during the swap"),
    ("1", "01:00, custody", "serial-level record, generated automatically as each drive is scanned"),
    ("2", "03:00, on the trucks", "outcomes from one shipment, certified destruction and recovered magnet feedstock"),
    ("1", "07:00, sun up", "morning debrief, backed by a report"),
]

CSS = """
/* Timeline rail: an alternative to the outlined statistic grid, which was
   carrying too much of the site on its own. Beats reveal in sequence and a
   gold progress line tracks scroll down the rail. */
.pal-rail { position: relative; }
.pal-rail-track { position: absolute; left: 0; top: 0; bottom: 0; width: 1px; background: rgba(255,255,255,0.16); }
.pal-rail-progress { position: absolute; left: 0; top: 0; width: 1px; height: 0; background: #A9832F; }
.pal-beats { display: flex; flex-direction: column; }
.pal-beat { display: flex; gap: clamp(16px, 2vw, 32px); padding-bottom: clamp(32px, 4vw, 52px); opacity: 0.001; transform: translateY(20px); transition: opacity 480ms cubic-bezier(0.2,0.7,0.1,1), transform 480ms cubic-bezier(0.2,0.7,0.1,1); }
.pal-beat:last-child { padding-bottom: 0; }
.pal-beat.is-in { opacity: 1; transform: none; }
.pal-beat-num { display: flex; align-items: center; min-width: clamp(84px, 9vw, 132px); }
.pal-tick { width: clamp(24px, 3vw, 40px); height: 1px; background: #A9832F; transform: scaleX(0); transform-origin: left center; transition: transform 480ms cubic-bezier(0.2,0.7,0.1,1) 80ms; }
.pal-beat.is-in .pal-tick { transform: scaleX(1); }
.pal-num { font-size: clamp(40px, 4.4vw, 64px); line-height: 1; font-weight: 300; color: #A9832F; padding-left: clamp(14px, 1.6vw, 24px); }
.pal-beat-body { padding-top: clamp(12px, 1.6vw, 20px); }
.pal-beat-time { font-size: 11px; letter-spacing: 1.4px; text-transform: uppercase; color: #8FA6BA; }
.pal-beat-text { margin-top: 10px; font-size: 16px; line-height: 1.6; font-weight: 300; color: #DDE3E9; max-width: 340px; }
@media (prefers-reduced-motion: reduce) {
  .pal-beat { opacity: 1; transform: none; transition: none; }
  .pal-tick { transform: scaleX(1); transition: none; }
}
"""


def beat_html(num, time, text):
    return (
        '<div class="pal-beat" data-timeline-beat>'
        '<div class="pal-beat-num"><div class="pal-tick"></div>'
        f'<div class="pal-num">{num}</div></div>'
        '<div class="pal-beat-body">'
        f'<div class="pal-beat-time">{time}</div>'
        f'<div class="pal-beat-text">{text}</div>'
        '</div></div>'
    )


RAIL = (
    '<div class="pal-rail" data-timeline-rail>'
    '<div class="pal-rail-track"></div>'
    '<div class="pal-rail-progress" data-timeline-progress></div>'
    '<div class="pal-beats">' + "".join(beat_html(*b) for b in BEATS) + '</div>'
    '</div>'
)

s = open(PAGE, encoding="utf-8").read()

# 1. add the component CSS to the page's own stylesheet
assert "pal-rail" not in s, "already applied"
anchor = 'input, select, textarea, button { font-family: "Restart Hard", system-ui, sans-serif; }'
assert anchor in s, "helmet style anchor not found"
s = s.replace(anchor, anchor + "\n" + CSS, 1)

# 2. replace the 2x2 grid with the rail
start = s.find('<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1px;">')
assert start > 0, "statistic grid not found"
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
assert "minutes of downtime" in old, "wrong block matched"
s = s[:start] + RAIL + s[j:]

open(PAGE, "w", encoding="utf-8").write(s)
print(f"replaced {len(old)} chars of grid with the timeline rail")
print(f"beats: {len(BEATS)}, css added: {len(CSS)} chars")
