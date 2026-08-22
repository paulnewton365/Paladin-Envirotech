"""Extend the homepage's two-tone headline to the rest of the site.

The homepage accents part of a headline in copper while the rest stays white,
three times. No other page did it, so the device read as a homepage quirk
rather than part of the system.

This applies it to the hero headline of the seven capability and story pages,
one accented clause each. Kept off the utility pages (contact, press, blog),
the two article pages, and the company page, whose headline is four words and
has nothing to split. Restraint is the point: the accent stops meaning
anything if every headline has one.

The accented clause is always the differentiating half, the part a reader
should leave with, not just the last few words.

All seven heroes sit on navy, where the copper measures 4.64:1. That clears
the 3:1 needed for large text. It would not clear it on the paper-shade
ground, so this treatment is for navy and white bands only.
"""
import os

SITE = "/home/claude/paladin-site"
SPAN_OPEN = '<span style="color: #A9832F; text-wrap: balance;">'

# (file, full headline text, the clause to accent)
EDITS = [
    ("critical-materials.html",
     "Economic security is national security.", "national security."),
    ("platform.html",
     "One system, from pickup to final disposition.", "One system,"),
    ("secure-itad.html",
     "Data-bearing assets are the highest risk in any decommissioning.", "highest risk"),
    ("network.html",
     "Ten facilities. Three continents. One system.", "One system."),
    ("electronics-recycling.html",
     "Processed domestically, with every downstream step recorded.", "Processed domestically,"),
    ("paladin-local.html",
     "The hub-and-satellite model, wherever you generate assets.", "wherever you generate assets."),
    ("industries.html",
     "What you retire says something about how you operate.", "how you operate."),
]

problems, applied = [], 0
for fname, headline, clause in EDITS:
    path = os.path.join(SITE, fname)
    s = open(path, encoding="utf-8").read()
    if SPAN_OPEN in s and headline not in s:
        print(f"  {fname}: already applied")
        continue
    if s.count(headline) != 1:
        problems.append((fname, f"headline appears {s.count(headline)} times"))
        continue
    if clause not in headline:
        problems.append((fname, f"clause not inside the headline"))
        continue
    accented = headline.replace(clause, SPAN_OPEN + clause + "</span>", 1)
    s = s.replace(headline, accented, 1)
    open(path, "w", encoding="utf-8").write(s)
    applied += 1
    print(f"  {fname}: accented \"{clause}\"")

if problems:
    print("\nPROBLEMS:")
    for f, e in problems:
        print(f"  {f}: {e}")
    raise SystemExit(1)
print(f"\napplied to {applied} pages")
