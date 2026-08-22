"""Invert the facility map so it reads on the light ground.

The band moves from #14304C to the paper ground. Every colour in the map was
chosen for a dark background, and most of them fail on light: the city labels
and node dots at #8FA6BA measure 2.33:1 against #F5F6F7, and the white Tampa
label 1.08:1.

Mapped by role rather than by find-and-replace, because #8FA6BA does two jobs
in the same file. Contrast against #F5F6F7 in brackets:

  city labels     #8FA6BA -> #47586B   (6.75, text)
  node dots       #8FA6BA -> #5B7085   (4.73, graphic)
  Tampa label     #FFFFFF -> #0B2138   (15.06, text)
  legend text     #5B7085 -> unchanged (4.73, text)
  route arcs      #A9832F -> unchanged (3.25, graphic)
  grid lines      rgba(255,255,255,0.07) -> rgba(11,33,56,0.10)
  HQ marker fill  #14304C -> #F5F6F7   (matches the new ground)

The mobile routing list that motion.js builds is inverted to match, since it
replaces this same map below 760px.
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/network.html"
MOTION = f"{SITE}/motion.js"
GROUND = "#F5F6F7"

s = open(PAGE, encoding="utf-8").read()
i = s.find("<svg")
j = s.find("</svg>") + len("</svg>")
svg = s[i:j]
assert "facility network" in svg, "wrong svg matched"

# --- band ground ---------------------------------------------------------
band = s.rfind('<div style="background:', 0, i)
assert band > 0, "map band opener not found"
opener_end = s.find(">", band)
opener = s[band:opener_end]
assert "#14304C" in opener, f"unexpected map band ground: {opener[:90]}"
s = s[:band] + opener.replace("#14304C", GROUND, 1) + s[opener_end:]
i = s.find("<svg"); j = s.find("</svg>") + len("</svg>")
svg = s[i:j]

before = svg

# --- text: city labels, then the Tampa label -----------------------------
svg = re.sub(r'(<text[^>]*fill=")#8FA6BA(")', r'\g<1>#47586B\g<2>', svg)
svg = re.sub(r'(<text[^>]*fill=")#FFFFFF(")', r'\g<1>#0B2138\g<2>', svg)

# --- node dots ------------------------------------------------------------
svg = re.sub(r'(<circle[^>]*fill=")#8FA6BA(")', r'\g<1>#5B7085\g<2>', svg)

# --- HQ marker sat on the old band colour --------------------------------
svg = svg.replace("#14304C", GROUND)

# --- grid lines -----------------------------------------------------------
svg = svg.replace("rgba(255,255,255,0.07)", "rgba(11,33,56,0.10)")

# The route arcs carried stroke-opacity 0.45, which reads on navy but goes
# faint on paper. Lift it and thicken the stroke slightly.
svg = svg.replace('stroke="#A9832F" stroke-width="1" stroke-opacity="0.45"',
                  'stroke="#A9832F" stroke-width="1.2" stroke-opacity="0.75"')
svg = svg.replace("rgba(255, 255, 255, 0.07)", "rgba(11,33,56,0.10)")

assert svg != before, "nothing changed in the svg"
assert "#8FA6BA" not in svg, "a dark-ground colour survived"
assert "#FFFFFF" not in svg, "a white fill survived"
s = s[:i] + svg + s[j:]

open(PAGE, "w", encoding="utf-8").write(s)
print("map inverted for the light ground")
for k, v in [("text labels", "#47586B"), ("node dots", "#5B7085"),
             ("Tampa label", "#0B2138"), ("grid", "rgba(11,33,56,0.10)")]:
    print(f"  {k:14} -> {v}")

# --- the mobile list that replaces the map below 760px --------------------
m = open(MOTION, encoding="utf-8").read()
start = m.find("function buildMobileNetwork")
assert start > 0, "mobile network builder not found"
# the builder runs to the end of its own function; bound it by the next
# top-level function declaration after it
end = m.find("\n  function ", start + 10)
assert end > start, "could not bound the builder"
block = m[start:end]
orig = block
block = block.replace("color:#8FA6BA", "color:#5B7085")
block = block.replace("color:#DDE3E9", "color:#47586B")
block = block.replace("color:#FFFFFF", "color:#0B2138")
block = block.replace("color:#7F93A6", "color:#5B7085")
block = block.replace("background:#8FA6BA", "background:#5B7085")
block = block.replace("rgba(255,255,255,0.16)", "rgba(11,33,56,0.16)")
assert block != orig, "mobile list unchanged"
open(MOTION, "w", encoding="utf-8").write(m[:start] + block + m[end:])
print("mobile routing list inverted to match")
