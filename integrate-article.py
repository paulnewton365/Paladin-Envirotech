"""Integrate the refined article page returned from Claude Design.

The upload is a self-contained bundle: the template plus its fonts, hero image
and runtime inlined as UUID-keyed resources. Shipping it as-is would add 1.6MB
and a second private copy of the four fonts, so this extracts the template and
points it back at the site's shared assets.

What it does:
  1. decodes the template out of the bundle
  2. rewrites font, image and runtime UUIDs to the shared paths
  3. rewrites Name.dc.html links to the site's clean URLs
  4. adds the Press nav item, which post-dates the design handover
  5. re-links the overlay layer stripped for the handover: gate, responsive,
     nav-menu, motion, plus the social and robots meta
"""
import base64
import json
import os
import re
import zlib

SITE = "/home/claude/paladin-site"
BUNDLE = "/mnt/user-data/uploads/Paladin-Insight-RareEarthRecovery.html"
OUT = os.path.join(SITE, "insight-rare-earth-recovery.html")

raw = open(BUNDLE, encoding="utf-8", errors="replace").read()


def script_block(kind):
    tag = f'<script type="__bundler/{kind}">'
    i = raw.find(tag)
    j = raw.find("</script>", i)
    return raw[i + len(tag):j].strip()


manifest = json.loads(script_block("manifest"))
template = json.loads(script_block("template"))

# ---- resources -----------------------------------------------------------
# The four @font-face rules appear in weight order 300, 400, 500, 600.
font_ids = re.findall(r'src: url\("([0-9a-f-]{36})"\)', template)
weights = re.findall(r'src: url\("[0-9a-f-]{36}"\) format\("opentype"\); font-weight: (\d+)', template)
WEIGHT_FILE = {"300": "RestartHard-Light.otf", "400": "RestartHard-Regular.otf",
               "500": "RestartHard-Medium.otf", "600": "RestartHard-SemiBold.otf"}

for fid, w in zip(font_ids, weights):
    template = template.replace(f'url("{fid}")', f'url("fonts/{WEIGHT_FILE[w]}")')
    print(f"  font {w} -> fonts/{WEIGHT_FILE[w]}")

# hero image: write it out and compare with what the site already ships
img_id = next((k for k, v in manifest.items() if v["mime"].startswith("image/")), None)
if img_id:
    blob = manifest[img_id]
    data = base64.b64decode(blob["data"])
    if blob.get("compressed"):
        data = zlib.decompress(data)
    existing = os.path.join(SITE, "assets", "rare-earth-magnet.png")
    same = os.path.exists(existing) and open(existing, "rb").read() == data
    if same:
        print("  hero image identical to assets/rare-earth-magnet.png, reusing")
    else:
        open(os.path.join(SITE, "assets", "insight-hero.png"), "wb").write(data)
        print(f"  hero image differs, wrote assets/insight-hero.png ({len(data)//1024}KB)")
    target = "assets/rare-earth-magnet.png" if same else "assets/insight-hero.png"
    template = template.replace(f'src="{img_id}"', f'src="{target}"')

# the Claude Design runtime
runtime_id = re.search(r'<script src="([0-9a-f-]{36})"></script>', template)
if runtime_id:
    template = template.replace(f'<script src="{runtime_id.group(1)}"></script>',
                                '<script src="./support.js"></script>')
    print("  runtime -> ./support.js")

# ---- links ---------------------------------------------------------------
URLS = {
    "Homepage.dc.html": "/", "Platform.dc.html": "/platform",
    "SecureITAD.dc.html": "/secure-itad",
    "ElectronicsRecycling.dc.html": "/electronics-recycling",
    "PaladinLocal.dc.html": "/paladin-local",
    "CriticalMaterials.dc.html": "/critical-materials",
    "Industries.dc.html": "/industries", "Network.dc.html": "/network",
    "Company.dc.html": "/company", "Blog.dc.html": "/blog",
    "Contact.dc.html": "/contact",
    "RareEarthFreedom250.dc.html": "/rare-earth-freedom-250",
}
for old, new in URLS.items():
    template = template.replace(f'href="{old}#', f'href="{new}#')
    template = template.replace(f'href="{old}"', f'href="{new}"')
left = re.findall(r'href="([A-Za-z]+\.dc\.html)"', template)
print(f"  links rewritten, {len(set(left))} unresolved: {sorted(set(left))}")

# ---- Press ---------------------------------------------------------------
# The handover already carried a Press nav item, but the redesign pointed it
# at Blog. Repoint it rather than adding a second one.
before = template.count('>Press</a>')
template = re.sub(r'(<a href=")/blog("[^>]*>Press</a>)', r'\g<1>/press\g<2>', template)
if template.count('href="/press"') == 1:
    print(f"  Press item repointed to /press ({before} Press item in nav)")
else:
    hdr_end = template.find("</header>")
    head_part = template[:hdr_end]
    m = re.search(r'<a href="/blog"[^>]*>Blog</a>', head_part)
    if m and 'href="/press"' not in head_part:
        PRESS = ('<a href="/press" style="color: #FFFFFF; font-size: 14px; font-weight: 300; '
                 'letter-spacing: 0.4px; padding-bottom: 4px; border-bottom: 1px solid transparent; '
                 'transition: border-color 200ms;" style-hover="border-bottom-color: #A9832F;">Press</a>')
        template = head_part[:m.end()] + PRESS + head_part[m.end():] + template[hdr_end:]
        print("  Press added to the nav")
    else:
        print("  ! Press nav item needs checking")

# ---- share targets -------------------------------------------------------
# The redesign kept the share row but dropped the URLs, leaving three dead
# links. Restore them by link text so a future re-import self-heals.
URL = "https://paladin-envirotech.vercel.app/insight-rare-earth-recovery"
TITLE_ENC = "Why%201.5%20million%20hard%20drives%20equal%20one%20ton%20of%20rare%20earths"
SHARE = {
    "LinkedIn": f"https://www.linkedin.com/shareArticle?mini=true&amp;url={URL}",
    "X": f"https://x.com/intent/tweet?url={URL}&amp;text={TITLE_ENC}",
    "Email": f"mailto:?subject={TITLE_ENC}&amp;body={URL}",
}
restored = 0
for label, target in SHARE.items():
    pattern = r'<a href="#"([^>]*)>' + re.escape(label) + r'</a>'
    template, n = re.subn(pattern, f'<a href="{target}" target="_blank" rel="noopener"\\g<1>>{label}</a>',
                          template, count=1)
    restored += n
print(f"  share links restored: {restored}/3")

# ---- overlay layer -------------------------------------------------------
EXTRA = ('<meta name="robots" content="noindex, nofollow">\n'
         '<meta property="og:title" content="Why 1.5 million hard drives equal one ton of rare earths">\n'
         '<meta property="og:description" content="The math behind domestic magnet recovery, and why only hyperscale volume makes the economics work.">\n'
         '<meta property="og:image" content="/assets/preview.webp">\n'
         '<meta property="og:type" content="article">\n'
         '<script src="/gate.js"></script>\n'
         '<script defer src="/nav-menu.js"></script>\n'
         '<script defer src="/motion.js"></script>\n'
         '<link rel="stylesheet" href="/responsive.css">\n'
         '<script src="./support.js"></script>')
assert '<script src="./support.js"></script>' in template
template = template.replace('<script src="./support.js"></script>', EXTRA, 1)
template = template.replace("<html>", '<html lang="en">', 1)

open(OUT, "w", encoding="utf-8").write(template)
print(f"\nwrote {OUT} ({len(template)//1024}KB, was 1637KB as a bundle)")
