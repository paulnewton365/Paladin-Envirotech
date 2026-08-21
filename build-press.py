"""Build the Press page.

Same approach as the article: take an existing page as the shell so the header,
footer, sticky CTA and scripts are the real ones, and author only the content
between </header> and <footer>.

Release items are prototype placeholders drawn from publicly known activity.
They are not approved announcements.
"""
import re

SITE = "/home/claude/paladin-site"
SHELL = f"{SITE}/blog.html"
OUT = f"{SITE}/press.html"

RELEASES = [
    ("Company", "Paladin EnviroTech expands European processing capacity in Helmond",
     "The Netherlands site adds throughput for regional ITAD and recycling volume.", "/network"),
    ("Critical materials", "REcapture begins domestic rare-earth magnet recovery with CMR",
     "The joint venture targets neodymium, praseodymium and dysprosium recovered from retired assets.", "/critical-materials"),
    ("Partnership", "Paladin joins the Freedom 250 grid as a critical-materials partner",
     "A season-long activation putting domestic recovery in front of a motorsport audience.", "/rare-earth-freedom-250"),
    ("Company", "Paladin EnviroTech completes acquisition, extending the platform footprint",
     "The addition brings further certified capacity into the single operating model.", "/company"),
    ("Compliance", "R2 and RIOS certification maintained across the operating network",
     "Certification is issued per site and per legal entity, and published as it stands today.", "/network"),
]


def card(cat, title, dek, href):
    return f'''<a href="{href}" style="display: block; padding: 28px 0; border-top: 1px solid #E7EAEE; text-decoration: none;">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); gap: clamp(16px, 3vw, 48px); align-items: start;">
            <div>
              <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">{cat}</span>
              <p style="margin: 8px 0 0; font-size: 13px; font-weight: 300; color: #8FA6BA;">Press release</p>
            </div>
            <div style="grid-column: span 2;">
              <h3 style="margin: 0; font-size: clamp(19px, 1.8vw, 24px); line-height: 1.3; font-weight: 500; color: #0B2138;">{title}</h3>
              <p style="margin: 8px 0 0; font-size: 15px; line-height: 25px; color: #47586B;">{dek}</p>
            </div>
          </div>
        </a>'''


shell = open(SHELL, encoding="utf-8").read()
head_end = shell.find("</header>") + len("</header>")
foot_start = shell.rfind("<footer")

head = shell[:head_end]
head = re.sub(r"<title>.*?</title>", "<title>Press | Paladin EnviroTech</title>", head, count=1)
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Press releases, media contacts and brand assets for Paladin EnviroTech.">',
              head, count=1)
head = re.sub(r'<meta property="og:title" content="[^"]*">',
              '<meta property="og:title" content="Press | Paladin EnviroTech">', head, count=1)

# The shell is the blog page, so Blog arrives marked active. Move the active
# treatment onto Press.
ACTIVE = 'font-weight: 500; letter-spacing: 0.4px; padding-bottom: 4px; border-bottom: 1px solid #A9832F;'
IDLE = 'font-weight: 300; letter-spacing: 0.4px; padding-bottom: 4px; border-bottom: 1px solid transparent;'
head = re.sub(r'(<a href="/blog"[^>]*?)' + re.escape(ACTIVE), r'\g<1>' + IDLE, head, count=1)
head = re.sub(r'(<a href="/press"[^>]*?)' + re.escape(IDLE), r'\g<1>' + ACTIVE, head, count=1)

body = f'''

<div data-reveal="1" style="background: #0B2138; padding: clamp(56px, 7vw, 104px) 0 clamp(48px, 6vw, 80px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div style="display: flex; align-items: center; gap: 12px;">
      <span style="width: 8px; height: 8px; background: #A9832F;"></span>
      <span style="color: #8FA6BA; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">Press</span>
    </div>
    <h1 style="color: #FFFFFF; font-size: clamp(32px, 4.4vw, 60px); line-height: 1.08; font-weight: 300; margin: 22px 0 18px; max-width: 1000px; text-wrap: balance;">Announcements, coverage and media contacts.</h1>
    <p style="color: #DDE3E9; font-weight: 300; font-size: clamp(17px, 1.4vw, 20px); line-height: 1.5; max-width: 680px; margin: 0;">Official releases from Paladin EnviroTech, plus the assets and contacts journalists need to file quickly.</p>
  </div>
</div>

<div data-reveal="1" style="background: #FFFFFF; padding: clamp(56px, 7vw, 96px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #5B7085;">Latest releases</span>
    <div style="margin-top: 28px;">
      {''.join(card(*r) for r in RELEASES)}
    </div>
  </div>
</div>

<div data-reveal="1" style="background: #F5F6F7; padding: clamp(56px, 7vw, 96px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr)); gap: clamp(28px, 4vw, 64px); align-items: start;">
    <div>
      <span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Media contact</span>
      <h2 style="font-size: clamp(24px, 2.4vw, 32px); line-height: 1.25; font-weight: 500; margin: 14px 0 14px;">For journalists on deadline.</h2>
      <p style="font-size: 16px; line-height: 26px; color: #47586B; margin: 0 0 18px;">Interview requests, facility visits and technical background on chain of custody, destruction standards or rare-earth recovery.</p>
      <a href="/contact" style="display: inline-block; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; font-weight: 500; color: #0B2138; text-decoration: none; border-bottom: 1px solid #0B2138; padding-bottom: 4px;">Contact the press office</a>
    </div>
    <div>
      <span style="font-size: 13px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">Press kit</span>
      <h2 style="font-size: clamp(24px, 2.4vw, 32px); line-height: 1.25; font-weight: 500; margin: 14px 0 14px;">Logos, imagery and boilerplate.</h2>
      <div style="display: flex; flex-direction: column;">
        <a href="#" style="padding: 14px 0; border-top: 1px solid #E7EAEE; font-size: 16px; color: #0B2138; text-decoration: none;">Brand assets and logo files</a>
        <a href="#" style="padding: 14px 0; border-top: 1px solid #E7EAEE; font-size: 16px; color: #0B2138; text-decoration: none;">Facility and operations imagery</a>
        <a href="/company" style="padding: 14px 0; border-top: 1px solid #E7EAEE; font-size: 16px; color: #0B2138; text-decoration: none;">Company boilerplate and leadership</a>
        <a href="/network" style="padding: 14px 0; border-top: 1px solid #E7EAEE; font-size: 16px; color: #0B2138; text-decoration: none;">Certifications by site and entity</a>
      </div>
    </div>
  </div>
</div>

<div data-reveal="1" style="background: #F5F6F7; padding: 0 0 clamp(80px, 9vw, 128px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); background: #0B2138; border-left: 4px solid #A9832F; padding: clamp(28px, 4vw, 56px) clamp(28px, 4.5vw, 64px); display: flex; align-items: center; justify-content: space-between; gap: 40px; flex-wrap: wrap;">
    <p style="color: #FFFFFF; font-weight: 300; font-size: clamp(22px, 2.4vw, 32px); line-height: 1.3; margin: 0; max-width: 1180px;">Writing about critical materials, data destruction or domestic supply? We can put you in front of the people who run it.</p>
    <a href="/contact" style="flex: none; display: inline-block; padding: 20px 32px; white-space: nowrap; font-size: 15px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #0B2138; background-image: linear-gradient(to right, #9FB4C7 50%, #FFFFFF 50%); background-size: 200% 100%; background-position: 100% 0; transition: background-position 220ms cubic-bezier(0.2,0.7,0.1,1);" style-hover="background-position: 0 0;">Talk to an expert</a>
  </div>
</div>

'''

open(OUT, "w", encoding="utf-8").write(head + body + shell[foot_start:])
print(f"wrote {OUT}")
