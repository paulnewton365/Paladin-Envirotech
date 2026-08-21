"""Stamp a build version across the site.

Usage:  python3 stamp-version.py 1.2.0 "short description"

Writes version.json, adds a <meta name="build-version"> to every page, and
lets motion.js render a discreet stamp in the footer so a reviewer can always
say which build they are looking at.

Scheme is MAJOR.MINOR.PATCH:
  MAJOR  new information architecture or a rebuild from a fresh export
  MINOR  new pages, new sections, reordered or rewritten content
  PATCH  fixes and refinements with no content change
"""
import glob, json, os, re, sys
from datetime import date

SITE = "/home/claude/paladin-site"

version = sys.argv[1] if len(sys.argv) > 1 else None
notes = sys.argv[2] if len(sys.argv) > 2 else ""
if not version or not re.match(r'^\d+\.\d+\.\d+$', version):
    sys.exit("usage: stamp-version.py X.Y.Z [notes]")

built = date.today().isoformat()

json.dump(
    {"version": version, "built": built, "notes": notes},
    open(os.path.join(SITE, "version.json"), "w"),
    indent=2,
)

meta = f'<meta name="build-version" content="{version}">\n<meta name="build-date" content="{built}">'
n = 0
for path in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r'\n?<meta name="build-version"[^>]*>', "", s)
    s = re.sub(r'\n?<meta name="build-date"[^>]*>', "", s)
    anchor = '<meta name="robots" content="noindex, nofollow">'
    if anchor not in s:
        print(f"  ! {os.path.basename(path)}: no anchor, skipped")
        continue
    s = s.replace(anchor, anchor + "\n" + meta, 1)
    open(path, "w", encoding="utf-8").write(s)
    n += 1

print(f"stamped v{version} ({built}) into {n} pages" + (f" - {notes}" if notes else ""))
