"""Ensure no two touching bands share a background.

Fixing collisions one at a time just moves them along the page, so this walks
every page's bands in order and resolves the whole sequence at once.

Bands are the top-level divs after </header>. The fixed CTA bar is skipped,
since it floats over the page rather than sitting in the stack. Each band's
ground is read from its own opening tag; where one matches the band above, it
steps to another value in the same family that also differs from the band
below, so a fix never creates the next collision.
"""
import glob
import os
import re

SITE = "/home/claude/paladin-site"

LIGHT = ["#FFFFFF", "#F5F6F7", "#E7EAEE"]
DARK = ["#0B2138", "#14304C"]


def bands(s):
    """Yield (start, end, opening_tag_end) for each top-level band."""
    out = []
    pos = s.find("</header>")
    pos = pos + len("</header>") if pos >= 0 else 0
    end_marker = s.rfind("<footer")
    limit = end_marker if end_marker > 0 else len(s)
    while pos < limit:
        nxt = s.find("<div", pos)
        if nxt < 0 or nxt >= limit:
            break
        depth, k = 0, nxt
        while k < len(s):
            if s.startswith("<div", k):
                depth += 1; k += 4
            elif s.startswith("</div>", k):
                depth -= 1; k += 6
                if depth == 0:
                    break
            else:
                k += 1
        out.append((nxt, k, s.find(">", nxt)))
        pos = k
    return out


def ground(opener):
    m = re.search(r"background:\s*(#[0-9A-Fa-f]{6})", opener)
    return m.group(1).upper() if m else None


def fix_page(path):
    s = open(path, encoding="utf-8").read()
    changes = []
    for _ in range(6):
        bs = bands(s)
        info = []
        for a, b, tag_end in bs:
            opener = s[a:tag_end]
            if "position: fixed" in opener:
                continue
            info.append((a, tag_end, ground(opener)))
        collision = None
        for i in range(1, len(info)):
            if info[i][2] and info[i][2] == info[i - 1][2]:
                collision = i
                break
        if collision is None:
            break
        a, tag_end, cur = info[collision]
        above = info[collision - 1][2]
        below = info[collision + 1][2] if collision + 1 < len(info) else None
        family = LIGHT if cur in LIGHT else DARK
        pick = next((c for c in family if c != above and c != below), None)
        if pick is None:
            pick = next((c for c in family if c != above), family[0])
        opener = s[a:tag_end]
        s = s[:a] + opener.replace(cur, pick, 1) + s[tag_end:]
        changes.append((cur, pick))
    if changes:
        open(path, "w", encoding="utf-8").write(s)
    return changes


total = 0
for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
    if os.path.basename(f) == "sitemap.html":
        continue
    ch = fix_page(f)
    if ch:
        print(f"  {os.path.basename(f)}: " + ", ".join(f"{a}->{b}" for a, b in ch))
        total += len(ch)
print(f"resolved {total} background collisions")
