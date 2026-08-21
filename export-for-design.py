"""Export the article page for redesign in Claude Design.

Strips the prototype's overlay layer, which belongs to the deployed build and
not to a design file:

  - gate.js, motion.js, nav-menu.js, responsive.css
  - build-version / build-date meta
  - the noindex robots tag

What is kept: the Claude Design runtime (support.js), the @font-face block,
the style-hover attributes the runtime reads, and the full page markup.

The output is written to /mnt/user-data/outputs so it can be handed over
directly. It expects assets/rare-earth-magnet.png alongside it; photography and
the wordmark load from paladinenvirotech.com.
"""
import os
import re
import shutil

SRC = "/home/claude/paladin-site/insight-rare-earth-recovery.html"
OUTDIR = "/mnt/user-data/outputs/for-claude-design"
OUT = os.path.join(OUTDIR, "InsightRareEarthRecovery.dc.html")

os.makedirs(os.path.join(OUTDIR, "assets"), exist_ok=True)

s = open(SRC, encoding="utf-8").read()

drop = [
    r'\n?<script src="/gate\.js"></script>',
    r'\n?<script defer src="/nav-menu\.js"></script>',
    r'\n?<script defer src="/motion\.js"></script>',
    r'\n?<link rel="stylesheet" href="/responsive\.css">',
    r'\n?<meta name="build-version"[^>]*>',
    r'\n?<meta name="build-date"[^>]*>',
    r'\n?<meta name="robots"[^>]*>',
]
for pattern in drop:
    s = re.sub(pattern, "", s)

# The deployed build serves fonts from /fonts; a design file sits beside them.
s = s.replace('url("fonts/', 'url("fonts/')

open(OUT, "w", encoding="utf-8").write(s)

# ship the one local image the page needs
shutil.copy("/home/claude/paladin-site/assets/rare-earth-magnet.png",
            os.path.join(OUTDIR, "assets", "rare-earth-magnet.png"))
for f in os.listdir("/home/claude/paladin-site/fonts"):
    os.makedirs(os.path.join(OUTDIR, "fonts"), exist_ok=True)
    shutil.copy(os.path.join("/home/claude/paladin-site/fonts", f),
                os.path.join(OUTDIR, "fonts", f))

print(f"wrote {OUT} ({len(s)} bytes)")
for check in ["gate.js", "motion.js", "nav-menu.js", "responsive.css", "build-version"]:
    print(f"  {check:18} present: {check in s}")
print(f"  support.js present: {'support.js' in s}")
print(f"  style-hover count : {s.count('style-hover')}")
