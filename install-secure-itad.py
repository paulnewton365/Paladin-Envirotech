"""Install the rebuilt /secure-itad page.

Unlike the earlier article, this one arrived as plain static HTML rather than a
Claude Design bundle, and it does not use support.js at all. It carries its own
nav toggle and its own scroll-reveal runtime for [data-reveal], [data-fact] and
[data-method]. That is fine and in fact lighter, so it is kept as-is.

What it was missing was the site's shared layers:

  nav-menu.js  the Platform mega menu, which every other page has
  motion.js    build stamp, sticky-bar clearance and hash handling

gate.js, responsive.css, the favicons and the build meta were already there.

One copy fix: "one certificate per asset, not per pallet" reintroduced the
antithesis construction removed site-wide in 1.9.0.
"""
import os
import shutil

SRC = "/mnt/user-data/uploads/secure-itad.html"
SITE = "/home/claude/paladin-site"
DEST = os.path.join(SITE, "secure-itad.html")

s = open(SRC, encoding="utf-8").read()

# --- copy fix -------------------------------------------------------------
old = "one certificate per asset, not per pallet"
new = "one certificate per asset, at serial level"
assert s.count(old) == 1, f"copy anchor found {s.count(old)} times"
s = s.replace(old, new, 1)
print(f'  copy: "{old}" -> "{new}"')

# --- shared layers --------------------------------------------------------
anchor = '<link rel="stylesheet" href="/responsive.css">'
assert anchor in s, "responsive.css link not found"
assert "nav-menu.js" not in s and "motion.js" not in s, "already wired"
s = s.replace(
    anchor,
    '<script defer src="/nav-menu.js"></script>\n'
    '<script defer src="/motion.js"></script>\n' + anchor,
    1,
)
print("  linked nav-menu.js and motion.js")

# keep a copy of what the previous page looked like, in case of a rollback
if os.path.exists(DEST):
    shutil.copy(DEST, "/tmp/secure-itad.previous.html")

open(DEST, "w", encoding="utf-8").write(s)
print(f"  wrote {DEST} ({len(s) // 1024}KB)")
