"""Third pass: 'instead of' variants and two remaining rhetorical shapes.

Two instances are kept deliberately. The turbine line compares kilograms with
grams, which is a real measurement contrast, and the '1 consolidated report
instead of a dozen vendor files' stat caption is the point of the statistic.
"""
import glob, os
SITE = "/home/claude/paladin-site"

EDITS = [
    ("Paladin processes it domestically under controlled downstream handling, instead of routing it through export and resale chains that lose track of where it ends up.",
     "Paladin processes it domestically under controlled downstream handling. Export and resale chains lose track of where material ends up.", 1),

    ("morning debrief, backed by a report instead of an assumption",
     "morning debrief, backed by a report", 1),

    ("so your team runs the business instead of chasing vendors.",
     "so the coordination sits with us.", 1),

    ("Routed through one system instead, every clinic gets the same NIST 800-88 destruction, the same serial-level record, and the same single report at the end, the kind an auditor can review in an afternoon instead of a week.",
     "Routed through one system, every clinic gets the same NIST 800-88 destruction, the same serial-level record, and one report at the end that an auditor can review in an afternoon.", 1),

    ("They sit inside the magnet, recoverable at usable quality if the equipment is processed correctly instead of shredded, exported or landfilled.",
     "They sit inside the magnet, recoverable at usable quality when the equipment is processed for recovery. Shredding, export and landfill lose them.", 1),

    ("one accounting of where the neodymium and dysprosium went, instead of reconciling records across separate vendors.",
     "one accounting of where the neodymium and dysprosium went, with no records to reconcile across vendors.", 1),

    ("A hospital protecting patient records, a bank satisfying an auditor, a hyperscaler shutting down a data center overnight, different stakes, same underlying question: can you prove where it went and what happened to it. That's what we're built to answer, sector by sector.",
     "A hospital protecting patient records, a bank satisfying an auditor and a hyperscaler closing a data center all have to prove where equipment went and what happened to it. What counts as proof varies by sector, so we work sector by sector.", 1),

    ("When an auditor asks what happened to drive serial 7F2-0441, the honest answer is usually: it depends who you ask.",
     "When an auditor asks what happened to drive serial 7F2-0441, the answer usually depends on who you ask.", 1),
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
