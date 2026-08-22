"""Second copy pass: the 'rather than' variants of the same rhetorical move."""
import glob, os
SITE = "/home/claude/paladin-site"

EDITS = [
    # Homepage H1. The gold span is kept, so the visual device survives.
    ('End-to-end control, <span style="color: #A9832F; text-wrap: balance;">not patchwork recycling.</span>',
     'End-to-end control, <span style="color: #A9832F; text-wrap: balance;">from pickup to final disposition.</span>', 1),

    ("produces certificates and settlement reporting by default, rather than reconstructing history on request.",
     "produces certificates and settlement reporting as the work happens.", 1),
    ("Acquisitions integrated onto one operating platform rather than run as a holding company",
     "Acquisitions integrated onto one operating platform", 1),
    ("refining them into high-purity oxides that re-enter domestic manufacturing rather than a landfill or an export container.",
     "refining them into high-purity oxides that re-enter domestic manufacturing.", 1),
    ("Recovered from circuit boards and connectors rather than lost to bulk shredding.",
     "Recovered from circuit boards and connectors, which bulk shredding destroys.", 1),
    ("the materials inside have to be recovered rather than shipped away.",
     "the materials inside have to be recovered and kept in domestic supply.", 1),
    ("asset-level history, available by default rather than on request.",
     "asset-level history, available by default.", 1),
]

files = [f for f in sorted(glob.glob(os.path.join(SITE, "*.html")))
         if os.path.basename(f) != "sitemap.html"]
src = {f: open(f, encoding="utf-8").read() for f in files}
misses, applied = [], 0
for old, new, exp in EDITS:
    c = sum(s.count(old) for s in src.values())
    if c != exp:
        misses.append((old[:70], exp, c)); continue
    for f in src:
        if old in src[f]: src[f] = src[f].replace(old, new)
    applied += c
if misses:
    print("MISMATCHES, nothing written:")
    for t, w, g in misses: print(f"  expected {w}, found {g}: {t}")
    raise SystemExit(1)
for f, s in src.items(): open(f, "w", encoding="utf-8").write(s)
print(f"applied {applied} replacements")
