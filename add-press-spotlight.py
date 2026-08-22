"""Add a spotlight announcement to /press.

A press page needs one thing above everything else: the announcement being
pushed this week. The page currently opens with a title band and drops
straight into an undifferentiated release list, so there is nowhere to put the
story a journalist is being pointed at.

This inserts a spotlight band between the two: a dated, categorised lead
announcement with a pull quote, sitting on the light ground so it separates
from the navy hero above and the white release list below.
"""
SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/press.html"

SPOTLIGHT = '''
<div data-reveal="1" style="background: #F5F6F7; padding: clamp(48px, 6vw, 80px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap; margin-bottom: clamp(20px, 2.5vw, 28px);">
      <span style="background: #A9832F; color: #0B2138; font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 12px;">Latest announcement</span>
      <span style="font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #5B7085;">Critical materials</span>
      <span style="width: 1px; height: 13px; background: #C7CFD7;"></span>
      <span style="font-size: 13px; font-weight: 300; color: #5B7085;">18 August 2026</span>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(360px, 100%), 1fr)); gap: clamp(32px, 4vw, 72px); align-items: start;">
      <div>
        <h2 style="font-size: clamp(30px, 3.6vw, 50px); line-height: 1.1; font-weight: 300; margin: 0 0 20px; color: #0B2138; text-wrap: balance;">REcapture begins domestic rare-earth magnet recovery with CMR</h2>
        <p style="font-size: clamp(17px, 1.4vw, 20px); line-height: 1.5; font-weight: 300; color: #47586B; margin: 0 0 28px;">The joint venture recovers neodymium, praseodymium, dysprosium and terbium from retired hard drives, motors and wind turbine generators, refining them into high-purity oxides for domestic manufacturing.</p>
        <div style="display: flex; gap: 16px; flex-wrap: wrap;">
          <a href="/critical-materials" style="display: inline-block; padding: 16px 28px; font-size: 13px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #FFFFFF; background-image: linear-gradient(to right, #14304C 50%, #0B2138 50%); background-size: 200% 100%; background-position: 100% 0; transition: background-position 220ms cubic-bezier(0.2,0.7,0.1,1);" style-hover="background-position: 0 0;">Read the announcement</a>
          <a href="/contact" style="display: inline-block; padding: 16px 28px; font-size: 13px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #0B2138; outline: 1px solid #C7CFD7; outline-offset: -1px; transition: outline-color 200ms;" style-hover="outline-color: #A9832F;">Request an interview</a>
        </div>
      </div>

      <div style="background: #FFFFFF; padding: clamp(28px, 3.5vw, 44px); border-left: 4px solid #A9832F;">
        <blockquote style="margin: 0; font-size: clamp(19px, 1.7vw, 24px); line-height: 1.4; font-weight: 300; color: #0B2138;">&ldquo;The assets are already here. What has been missing is a domestic pathway that takes them from retirement to usable oxide without the material leaving the country.&rdquo;</blockquote>
        <div style="margin-top: 22px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
          <div style="width: 38px; height: 38px; flex: none; background: #0B2138; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 500; letter-spacing: 1px;">LW</div>
          <span style="font-size: 15px; font-weight: 500; color: #0B2138;">Luke Wray</span>
          <span style="width: 1px; height: 13px; background: #C7CFD7;"></span>
          <span style="font-size: 12px; letter-spacing: 0.6px; text-transform: uppercase; color: #5B7085;">VP, Critical Materials &amp; Defense</span>
        </div>
      </div>
    </div>
  </div>
</div>
'''

s = open(PAGE, encoding="utf-8").read()
assert "Latest announcement" not in s, "already applied"

# insert between the navy hero band and the release list
marker = s.find("Latest releases")
assert marker > 0, "release list not found"
band_start = s.rfind('<div data-reveal="1"', 0, marker)
assert band_start > 0

s = s[:band_start] + SPOTLIGHT.strip() + "\n\n" + s[band_start:]
open(PAGE, "w", encoding="utf-8").write(s)
print("spotlight announcement inserted before the release list")
