"""Add a facility spotlight to /network.

The network page lists every site at equal weight, so nothing on it tells a
story. This pulls one facility forward and signposts the newsroom piece about
it, which also gives the blog a route in from a page buyers actually visit.

Helmond is the one to spotlight: it is the European gateway, there is already a
press release about its expansion, and Dave Owens has a newsroom piece on it.

The band is navy so it separates from the light grey list above and the light
CTA below.
"""
SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/network.html"

SPOTLIGHT = '''
<div data-reveal="1" style="background: #0B2138; padding: clamp(56px, 7vw, 104px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(340px, 100%), 1fr)); gap: clamp(32px, 4vw, 72px); align-items: center;">

    <div style="aspect-ratio: 4 / 3; background: #14304C; position: relative; overflow: hidden;"><img src="assets/recycling-rare.jpeg" alt="Sorting line at the Helmond facility" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;" /></div>

    <div>
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 18px;">
        <span style="width: 8px; height: 8px; background: #A9832F;"></span>
        <span style="color: #A9832F; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">Facility spotlight</span>
      </div>
      <h2 style="color: #FFFFFF; font-size: clamp(28px, 3.2vw, 44px); line-height: 1.14; font-weight: 300; margin: 0 0 18px; text-wrap: balance;">Helmond, Netherlands</h2>
      <p style="color: #DDE3E9; font-weight: 300; font-size: 17px; line-height: 27px; margin: 0 0 28px; max-width: 560px;">The European gateway for the platform. Collection, dismantling and data sanitization run here for customers across the Benelux and DACH regions, on the same operating model and reporting used at every other site.</p>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(150px, 100%), 1fr)); gap: 1px; margin-bottom: clamp(28px, 3.5vw, 40px);">
        <div style="padding: 20px 24px 20px 0; border-right: 1px solid rgba(255, 255, 255, 0.16);">
          <div style="color: #A9832F; font-size: 28px; line-height: 1.1; font-weight: 300;">2016</div>
          <p style="color: #8FA6BA; font-size: 13px; font-weight: 300; margin: 8px 0 0;">operating since</p>
        </div>
        <div style="padding: 20px 24px; border-right: 1px solid rgba(255, 255, 255, 0.16);">
          <div style="color: #A9832F; font-size: 28px; line-height: 1.1; font-weight: 300;">R2</div>
          <p style="color: #8FA6BA; font-size: 13px; font-weight: 300; margin: 8px 0 0;">certified, verifiable per entity</p>
        </div>
        <div style="padding: 20px 0 20px 24px;">
          <div style="color: #A9832F; font-size: 28px; line-height: 1.1; font-weight: 300;">3</div>
          <p style="color: #8FA6BA; font-size: 13px; font-weight: 300; margin: 8px 0 0;">regions served from one site</p>
        </div>
      </div>

      <a href="/blog" style="display: block; background: #14304C; padding: 24px 28px; border-left: 4px solid #A9832F; transition: background 220ms;" style-hover="background: #1B3D5F;">
        <span style="display: block; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">From the newsroom</span>
        <span style="display: block; margin-top: 10px; font-size: clamp(17px, 1.5vw, 21px); line-height: 1.35; font-weight: 500; color: #FFFFFF;">Inside the Helmond facility: Europe's ITAD gateway</span>
        <span style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-top: 14px;">
          <span style="width: 30px; height: 30px; flex: none; background: #0B2138; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 500; letter-spacing: 1px;">DO</span>
          <span style="font-size: 14px; font-weight: 500; color: #DDE3E9;">Dave Owens</span>
          <span style="width: 1px; height: 12px; background: rgba(255,255,255,0.24);"></span>
          <span style="font-size: 12px; letter-spacing: 0.6px; text-transform: uppercase; color: #8FA6BA;">SVP, Global Recycling</span>
        </span>
      </a>
    </div>
  </div>
</div>
'''

s = open(PAGE, encoding="utf-8").read()

# Remove any earlier copy. A previous run anchored on the word "International",
# which also occurs inside the header, so the block landed in the masthead.
key = '<div data-reveal="1" style="background: #0B2138; padding: clamp(56px, 7vw, 104px) 0;">'
while True:
    at = s.find(key)
    if at < 0 or "Facility spotlight" not in s[at:at + 900]:
        break
    depth, k = 0, at
    while k < len(s):
        if s.startswith("<div", k):
            depth += 1; k += 4
        elif s.startswith("</div>", k):
            depth -= 1; k += 6
            if depth == 0:
                break
        else:
            k += 1
    s = s[:at] + s[k:]
    print("removed a misplaced copy")

# Walk the page's top-level bands, which begin after </header>, and find the one
# holding the map. Anchoring on the element rather than on body text avoids the
# header collision entirely.
body_start = s.find("</header>") + len("</header>")
pos, target_end = body_start, None
while pos < len(s):
    nxt = s.find("<div", pos)
    if nxt < 0:
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
    if 'aria-label="Paladin facility network' in s[nxt:k]:
        target_end = k
        break
    pos = k
assert target_end, "map band not found"

s = s[:target_end] + "\n\n" + SPOTLIGHT.strip() + "\n" + s[target_end:]
open(PAGE, "w", encoding="utf-8").write(s)
print("facility spotlight placed directly under the map")
