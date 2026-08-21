"""Build the blog article page.

Takes an existing page as the shell so the article inherits the real header,
footer, sticky CTA bar and scripts, then swaps everything between </header>
and <footer> for article content. Keeping the shell rather than hand-writing
one means the nav cannot drift out of sync with the rest of the site.
"""
import re

SITE = "/home/claude/paladin-site"
SHELL = f"{SITE}/paladin-local.html"
OUT = f"{SITE}/insight-rare-earth-recovery.html"

AUTHOR = "Luke Wray"
ROLE = "VP, Critical Materials &amp; Defense"
INITIALS = "LW"
URL = "https://paladin-envirotech.vercel.app/insight-rare-earth-recovery"
TITLE = "Why 1.5 million hard drives equal one ton of rare earths"

shell = open(SHELL, encoding="utf-8").read()
head_end = shell.find("</header>") + len("</header>")
foot_start = shell.rfind("<footer")

# --- head: title, description, canonical-ish social tags -------------------
head = shell[:head_end]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} | Paladin EnviroTech</title>", head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="The math behind domestic magnet recovery, and why only hyperscale volume makes the economics work.">',
              head, count=1)
head = re.sub(r'<meta property="og:title" content="[^"]*">',
              f'<meta property="og:title" content="{TITLE}">', head, count=1)
head = re.sub(r'<meta property="og:description" content="[^"]*">',
              '<meta property="og:description" content="The math behind domestic magnet recovery, and why only hyperscale volume makes the economics work.">',
              head, count=1)

SHARE = f'''
        <div style="margin-top: clamp(40px, 5vw, 64px); padding-top: 28px; border-top: 1px solid #E7EAEE; display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
          <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #5B7085;">Share</span>
          <a href="https://www.linkedin.com/shareArticle?mini=true&amp;url={URL}" target="_blank" rel="noopener" style="font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #0B2138; text-decoration: none; border: 1px solid #C7CFD7; padding: 9px 16px; transition: border-color 200ms, color 200ms;" style-hover="border-color: #A9832F; color: #A9832F;">LinkedIn</a>
          <a href="https://x.com/intent/tweet?url={URL}&amp;text={TITLE.replace(' ', '%20')}" target="_blank" rel="noopener" style="font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #0B2138; text-decoration: none; border: 1px solid #C7CFD7; padding: 9px 16px; transition: border-color 200ms, color 200ms;" style-hover="border-color: #A9832F; color: #A9832F;">X</a>
          <a href="mailto:?subject={TITLE.replace(' ', '%20')}&amp;body={URL}" style="font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #0B2138; text-decoration: none; border: 1px solid #C7CFD7; padding: 9px 16px; transition: border-color 200ms, color 200ms;" style-hover="border-color: #A9832F; color: #A9832F;">Email</a>
          <a href="{URL}" style="font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #5B7085; text-decoration: none; border-bottom: 1px solid #C7CFD7; padding-bottom: 3px;">Copy link</a>
        </div>'''

MORE_BY = f'''
<div data-reveal="1" style="background: #F5F6F7; padding: clamp(56px, 7vw, 96px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div style="background: #FFFFFF; outline: 1px solid #E7EAEE; padding: clamp(28px, 4vw, 48px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: clamp(28px, 4vw, 56px); align-items: start;">
      <div>
        <div style="display: flex; align-items: center; gap: 16px;">
          <div style="width: 56px; height: 56px; flex: none; background: #0B2138; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 500; letter-spacing: 1px;">{INITIALS}</div>
          <div>
            <p style="margin: 0; font-size: 18px; font-weight: 500; color: #0B2138;">{AUTHOR}</p>
            <p style="margin: 4px 0 0; font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase; color: #5B7085;">{ROLE}</p>
          </div>
        </div>
        <p style="margin: 20px 0 0; font-size: 15px; line-height: 25px; color: #47586B;">Leads Paladin's critical-materials programme, including the REcapture rare-earth recovery pathway and domestic feedstock partnerships.</p>
        <a href="/company#leadership" style="display: inline-block; margin-top: 18px; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; font-weight: 500; color: #0B2138; text-decoration: none; border-bottom: 1px solid #0B2138; padding-bottom: 4px;">See the leadership team</a>
      </div>
      <div>
        <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #5B7085;">More by {AUTHOR}</span>
        <div style="margin-top: 18px; display: flex; flex-direction: column;">
          <a href="/critical-materials" style="display: block; padding: 16px 0; border-top: 1px solid #E7EAEE; text-decoration: none;">
            <span style="display: block; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Critical materials</span>
            <span style="display: block; margin-top: 6px; font-size: 17px; line-height: 25px; font-weight: 500; color: #0B2138;">Wind turbine recycling: the recovery math nobody publishes</span>
          </a>
          <a href="/critical-materials" style="display: block; padding: 16px 0; border-top: 1px solid #E7EAEE; text-decoration: none;">
            <span style="display: block; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Critical materials</span>
            <span style="display: block; margin-top: 6px; font-size: 17px; line-height: 25px; font-weight: 500; color: #0B2138;">What a domestic magnet supply chain actually requires</span>
          </a>
          <a href="/blog" style="display: block; padding: 16px 0; border-top: 1px solid #E7EAEE; text-decoration: none;">
            <span style="display: block; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Newsroom</span>
            <span style="display: block; margin-top: 6px; font-size: 17px; line-height: 25px; font-weight: 500; color: #0B2138;">All articles by {AUTHOR}</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
'''

BODY = f'''

<div data-reveal="1" style="background: #0B2138; padding: clamp(48px, 6vw, 88px) 0 clamp(40px, 5vw, 64px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <a href="/blog" style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #8FA6BA; text-decoration: none;">&larr; Newsroom</a>
    <span style="display: block; margin-top: 28px; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Critical materials</span>
    <h1 style="color: #FFFFFF; font-size: clamp(32px, 4.2vw, 60px); line-height: 1.08; font-weight: 300; margin: 16px 0 0; max-width: 1100px; text-wrap: balance;">{TITLE}</h1>
    <div style="margin-top: clamp(24px, 3vw, 36px); display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
      <div style="width: 40px; height: 40px; flex: none; background: #14304C; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 500; letter-spacing: 1px;">{INITIALS}</div>
      <span style="color: #FFFFFF; font-size: 15px; font-weight: 500;">{AUTHOR}</span>
      <span style="width: 1px; height: 14px; background: rgba(255,255,255,0.24);"></span>
      <span style="color: #8FA6BA; font-size: 13px; letter-spacing: 0.6px; text-transform: uppercase;">{ROLE}</span>
      <span style="width: 1px; height: 14px; background: rgba(255,255,255,0.24);"></span>
      <span style="color: #7F93A6; font-size: 13px; font-weight: 300;">6 min read</span>
    </div>
  </div>
</div>

<div data-reveal="1" style="background: #FFFFFF; padding: 0 0 clamp(48px, 6vw, 88px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div style="aspect-ratio: 21 / 9; background: #14304C; position: relative; overflow: hidden; margin-top: clamp(-32px, -3vw, -20px);"><img src="assets/rare-earth-magnet.png" alt="Retired hard drives on a processing line" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;" /></div>
    <div style="max-width: 760px; margin: clamp(40px, 5vw, 72px) 0 0;">
      <p style="font-size: clamp(19px, 1.6vw, 22px); line-height: 1.55; font-weight: 300; color: #0B2138; margin: 0 0 28px;">The math behind domestic magnet recovery is unforgiving, and it is the reason recycling has stayed a footnote in the critical-materials conversation rather than a pillar of it.</p>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0 0 20px;">A single enterprise hard drive contains a voice-coil magnet weighing a few grams. Neodymium, praseodymium and dysprosium make up a fraction of that. Run the arithmetic across a full ton of recovered rare-earth oxide and the number lands somewhere near 1.5 million drives, which is not a figure a regional processor can reach in a year.</p>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0 0 20px;">That single constraint explains most of what looks strange about this market. Recovery only works where the volume already exists, which means hyperscale data centres, large enterprise refresh cycles and energy assets reaching end of life at the same moment. Everyone else is operating below the threshold where the chemistry pays for itself.</p>
      <h2 style="font-size: clamp(24px, 2.4vw, 32px); line-height: 1.25; font-weight: 500; color: #0B2138; margin: 40px 0 16px;">Why the timeline matters more than the tonnage</h2>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0 0 20px;">Opening a new mine in the United States takes close to three decades once permitting is counted, and the country holds almost no heavy rare earths in the ground regardless. Recycling is the only lever that moves on the same timescale as demand from defence programmes, AI infrastructure and the energy transition.</p>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0 0 20px;">The assets are already here. They are sitting in racks that will be decommissioned this quarter. The question is whether the magnets inside them re-enter a domestic supply chain or leave the country as mixed scrap.</p>
      <h2 style="font-size: clamp(24px, 2.4vw, 32px); line-height: 1.25; font-weight: 500; color: #0B2138; margin: 40px 0 16px;">What has to be true operationally</h2>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0 0 20px;">Recovery at this scale is a logistics problem before it is a chemistry problem. Drives arrive as data-bearing assets, so destruction has to happen first, under NIST 800-88, documented per serial. Only then does the magnet become feedstock. A chain that hands off between four companies loses both the paperwork and the material.</p>
      <p style="font-size: 17px; line-height: 29px; color: #47586B; margin: 0;">Running destruction, recovery and refining inside one system is what makes the volume usable rather than theoretical. It is also what lets a customer see, per serial, where their material went.</p>
      {SHARE}
    </div>
  </div>
</div>
{MORE_BY}
<div data-reveal="1" style="background: #F5F6F7; padding: 0 0 clamp(80px, 9vw, 128px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); background: #0B2138; border-left: 4px solid #A9832F; padding: clamp(28px, 4vw, 56px) clamp(28px, 4.5vw, 64px); display: flex; align-items: center; justify-content: space-between; gap: 40px; flex-wrap: wrap;">
    <p style="color: #FFFFFF; font-weight: 300; font-size: clamp(22px, 2.4vw, 32px); line-height: 1.3; margin: 0; max-width: 1180px;">If your refresh cycle is generating drives at volume, that material has a recovery pathway. Let's model it.</p>
    <a href="/contact" style="flex: none; display: inline-block; padding: 20px 32px; white-space: nowrap; font-size: 15px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #0B2138; background-image: linear-gradient(to right, #9FB4C7 50%, #FFFFFF 50%); background-size: 200% 100%; background-position: 100% 0; transition: background-position 220ms cubic-bezier(0.2,0.7,0.1,1);" style-hover="background-position: 0 0;">Talk to an expert</a>
  </div>
</div>

'''

out = head + BODY + shell[foot_start:]
open(OUT, "w", encoding="utf-8").write(out)
print(f"wrote {OUT} ({len(out)} bytes)")
