"""Rebuild /paladin-local and /electronics-recycling on the /secure-itad pattern.

secure-itad is now the reference layout: static HTML, no support.js, its own
nav toggle and reveal runtime, and five sections in a fixed rhythm.

  hero      navy, eyebrow + accented h1 + lead + image
  split     white, head grid then two rules under a gold top border
  list      paper, left column of intro against a numbered ruled list
  proof     navy, left column against a white fact card
  cta       paper, gold-ruled band

The shell is taken from secure-itad so the head, header, footer, hover-class
CSS and inline runtime are the real ones and cannot drift. Only the five
sections are authored.

All body copy is carried over verbatim from the existing pages. Nothing here
invents a claim about the business: where the new layout needs a label the old
page did not have, it reuses an existing heading.
"""
import os
import re

SITE = "/home/claude/paladin-site"
SHELL = os.path.join(SITE, "secure-itad.html")


# ---------------------------------------------------------------- patterns
def hero(eyebrow, head_html, lead, image, alt):
    return f'''<section data-screen-label="Hero" style="background: #0B2138; padding: clamp(56px, 7vw, 104px) 0 clamp(48px, 6vw, 88px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(340px, 100%), 1fr)); gap: clamp(32px, 4vw, 72px); align-items: center;">
    <div data-reveal="1">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span style="width: 8px; height: 8px; background: #A9832F;"></span>
        <span style="color: #8FA6BA; font-size: 13px; letter-spacing: 1px; text-transform: uppercase;">{eyebrow}</span>
      </div>
      <h1 style="color: #FFFFFF; font-size: clamp(32px, 4.2vw, 58px); line-height: 1.06; letter-spacing: -0.6px; font-weight: 300; margin: 22px 0 20px; text-wrap: balance;">{head_html}</h1>
      <p style="color: #DDE3E9; font-weight: 300; font-size: clamp(17px, 1.4vw, 20px); line-height: 1.55; margin: 0; max-width: 620px; text-wrap: pretty;">{lead}</p>
    </div>
    <div data-reveal="1" style="aspect-ratio: 4 / 3; background: #14304C; position: relative; overflow: hidden;"><img src="{image}" alt="{alt}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;" /></div>
  </div>
</section>'''


def split(head, intro, cards):
    def card(i, c):
        pad = ("clamp(32px, 3.4vw, 48px) clamp(28px, 3vw, 44px) clamp(40px, 4vw, 56px) 0"
               if i == 0 else
               "clamp(32px, 3.4vw, 48px) clamp(28px, 3vw, 44px) clamp(40px, 4vw, 56px) clamp(28px, 3vw, 44px)")
        return f'''<div data-reveal="1" style="background: #FFFFFF; border-top: 3px solid #A9832F; padding: {pad};">
        <div style="display: flex; align-items: baseline; gap: 14px;">
          <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">{c[0]}</span>
          <span style="flex: 1; height: 1px; background: #E7EAEE;"></span>
          <span style="font-size: 12px; letter-spacing: 0.8px; color: #7F93A6;">{i + 1:02d}</span>
        </div>
        <h3 style="margin: 20px 0 14px; font-size: clamp(24px, 2.4vw, 34px); line-height: 1.15; font-weight: 500; letter-spacing: -0.2px;">{c[1]}</h3>
        <p style="margin: 0; font-size: 16px; line-height: 1.65; font-weight: 300; color: #47586B; text-wrap: pretty;">{c[2]}</p>
      </div>'''
    return f'''<section data-screen-label="Split" style="background: #FFFFFF; padding: clamp(64px, 8vw, 128px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px);">
    <div data-reveal="1" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); gap: clamp(32px, 4vw, 64px); align-items: end; padding-bottom: 40px; border-bottom: 1px solid #0B2138;">
      <h2 style="margin: 0; font-size: clamp(30px, 3.6vw, 52px); line-height: 1.08; letter-spacing: -0.5px; font-weight: 400; max-width: 700px; text-wrap: pretty;">{head}</h2>
      <p style="margin: 0; font-size: 16px; line-height: 1.65; font-weight: 300; color: #47586B; max-width: 520px; text-wrap: pretty;">{intro}</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(340px, 100%), 1fr)); gap: 1px; background: #E7EAEE;">
      {"".join(card(i, c) for i, c in enumerate(cards))}
    </div>
  </div>
</section>'''


def ruled_list(anchor, eyebrow, head, lead, rows, cta=None):
    link = ""
    if cta:
        link = f'''<a href="{cta[1]}" style="display: inline-flex; align-items: center; gap: 12px; margin-top: 28px; color: #0B2138; font-size: 14px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; border-bottom: 1px solid #0B2138; padding-bottom: 6px;">{cta[0]}</a>'''
    items = "".join(
        f'''<div data-method="1" style="display: grid; grid-template-columns: 56px 1fr; column-gap: clamp(20px, 2.5vw, 40px); align-items: baseline; padding: clamp(24px, 2.6vw, 36px) 0; border-bottom: 1px solid #DCE0E5; transition: padding-left 220ms cubic-bezier(0.2,0.7,0.1,1);" class="h{11 + (i % 3)}">
        <span style="font-size: 12px; letter-spacing: 0.8px; color: #A9832F;">{i + 1:02d}</span>
        <div>
          <div style="font-size: clamp(22px, 2.2vw, 32px); line-height: 1.15; font-weight: 500; letter-spacing: -0.2px;">{r[0]}</div>
          <div style="margin-top: 8px; font-size: 15px; line-height: 1.6; font-weight: 300; color: #47586B; text-wrap: pretty;">{r[1]}</div>
        </div>
      </div>''' for i, r in enumerate(rows))
    return f'''<section id="{anchor}" data-screen-label="Detail" style="background: #F5F6F7; padding: clamp(64px, 8vw, 128px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr)); gap: clamp(40px, 6vw, 96px);">
    <div data-reveal="1" style="position: sticky; top: clamp(96px, 12vh, 140px); align-self: start;">
      <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">{eyebrow}</span>
      <h2 style="margin: 18px 0 20px; font-size: clamp(30px, 3.6vw, 52px); line-height: 1.08; letter-spacing: -0.5px; font-weight: 400; text-wrap: pretty;">{head}</h2>
      <p style="margin: 0; font-size: 17px; line-height: 1.65; font-weight: 300; color: #47586B; max-width: 460px; text-wrap: pretty;">{lead}</p>
      {link}
    </div>
    <div data-reveal="1" style="border-top: 1px solid #0B2138;">
      {items}
    </div>
  </div>
</section>'''


def proof(eyebrow, head, lead, cta, card_title, facts):
    rows = "".join(
        f'''<div data-fact="1" style="display: flex; align-items: baseline; justify-content: space-between; gap: 20px; padding: clamp(16px, 1.8vw, 22px) 0; border-bottom: 1px solid #E7EAEE;">
        <span style="font-size: 15px; line-height: 1.5; font-weight: 300; color: #47586B; max-width: 320px;">{f[0]}</span>
        <span style="font-size: 13px; letter-spacing: 0.8px; text-transform: uppercase; color: #0B2138; white-space: nowrap;">{f[1]}</span>
      </div>''' for f in facts)
    return f'''<section data-screen-label="Proof" style="background: #0B2138; padding: clamp(64px, 8vw, 128px) 0;">
  <div style="max-width: 1600px; margin: 0 auto; padding: 0 clamp(24px, 5vw, 72px); display: grid; grid-template-columns: repeat(auto-fit, minmax(min(320px, 100%), 1fr)); gap: clamp(40px, 5vw, 88px); align-items: start;">
    <div data-reveal="1" style="position: sticky; top: clamp(96px, 12vh, 140px); align-self: start;">
      <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #A9832F;">{eyebrow}</span>
      <h2 style="margin: 18px 0 22px; color: #FFFFFF; font-size: clamp(30px, 3.6vw, 52px); line-height: 1.08; letter-spacing: -0.5px; font-weight: 300; text-wrap: pretty;">{head}</h2>
      <p style="margin: 0 0 32px; color: #DDE3E9; font-size: 17px; line-height: 1.65; font-weight: 300; max-width: 520px; text-wrap: pretty;">{lead}</p>
      <a href="{cta[1]}" style="display: inline-flex; align-items: center; gap: 12px; color: #A9832F; font-size: 14px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; border-bottom: 1px solid #A9832F; padding-bottom: 6px;">{cta[0]}</a>
    </div>
    <div data-reveal="1" style="background: #FFFFFF; padding: clamp(24px, 2.6vw, 36px);">
      <div style="display: flex; align-items: baseline; justify-content: space-between; padding-bottom: 16px; border-bottom: 1px solid #0B2138;">
        <span style="font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #0B2138;">{card_title}</span>
      </div>
      {rows}
    </div>
  </div>
</section>'''


def cta_band(text, label="Talk to an expert", href="/contact"):
    return f'''<section data-screen-label="Contact" style="background: #F5F6F7; padding: clamp(56px, 7vw, 96px) 0 clamp(80px, 9vw, 128px);">
  <div style="max-width: 1600px; margin: 0 auto; padding: clamp(28px, 4vw, 56px) clamp(28px, 4.5vw, 64px); background: #0B2138; border-left: 4px solid #A9832F; display: flex; align-items: center; justify-content: space-between; gap: 40px; flex-wrap: wrap;">
    <p style="color: #FFFFFF; font-weight: 300; font-size: clamp(22px, 2.4vw, 32px); line-height: 1.3; margin: 0; max-width: 1180px;">{text}</p>
    <a href="{href}" style="flex: none; display: inline-block; padding: 20px 32px; white-space: nowrap; font-size: 15px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; color: #0B2138; background-image: linear-gradient(to right, #9FB4C7 50%, #FFFFFF 50%); background-size: 200% 100%; background-position: 100% 0; transition: background-position 220ms cubic-bezier(0.2,0.7,0.1,1);" class="h9">{label}</a>
  </div>
</section>'''


# ------------------------------------------------------------------ pages
GOLD = '<span style="color: #A9832F;">'

PAGES = {
    "paladin-local.html": dict(
        title="Paladin Local | Paladin EnviroTech",
        description="Secure ITAD and recycling closer to where assets are generated.",
        sections=[
            hero("Platform &middot; Paladin Local",
                 f'The hub-and-satellite model, {GOLD}wherever you generate assets.</span>',
                 "Clinics, campuses, branch offices and regional facilities generate retired technology too, usually in volumes too small for a national ITAD provider to serve well. Paladin Local brings the same controls, the same reporting and the same chain of custody to those locations.",
                 "assets/old-phones.webp", "Collected devices at a regional intake site"),
            split("One model, two kinds of site.",
                  "A satellite runs the same operating model as a hub. What changes is the distance to the customer, not the standard applied.",
                  [("Hub", "Regional processing", "Full processing capability, downstream vendor management and materials recovery for the surrounding region."),
                   ("Satellite", "Local collection", "Satellite sites shorten transport routes for organizations with distributed locations.")]),
            ruled_list("coverage", "Reach", "What every site runs",
                       "The same operating standard applies at a single branch office and at a hyperscale campus.",
                       [("Beyond the major metros", "Satellite sites shorten transport routes for organizations with distributed locations."),
                        ("Same controls, every site", "No downgraded process for smaller volumes, every location runs the full standard."),
                        ("Built for smaller volumes", "Right-sized scheduling and pickup for offices and branch locations as well as hyperscale campuses."),
                        ("One record across all sites", "A multi-site organization sees every location on the same chain-of-custody record.")],
                       cta=("See the network", "/network")),
            proof("Reporting", "One record across all sites",
                  "A multi-site organization sees every location on the same chain-of-custody record, whichever site handled the collection.",
                  ("See how the platform works", "/platform"), "On every collection",
                  [("Pickup manifest, serial-scanned at the dock", "Every site"),
                   ("Certificate of destruction, issued per asset", "Serial level"),
                   ("Materials and settlement reporting", "One ledger"),
                   ("Certification status shown per site and entity", "Per entity")]),
            cta_band("Have locations spread across a region? Let's map coverage against your footprint."),
        ]),
    "electronics-recycling.html": dict(
        title="Electronics Recycling | Paladin EnviroTech",
        description="Domestic electronics processing with controlled downstream handling.",
        sections=[
            hero("Platform &middot; Electronics recycling",
                 f'{GOLD}Processed domestically,</span> with every downstream step recorded.',
                 "Once data is destroyed, what remains still has value: ferrous and non-ferrous metals, precious metals, plastics. Paladin processes it domestically under controlled downstream handling. Export and resale chains lose track of where material ends up.",
                 "assets/recycling-rare.jpeg", "Sorting line at a Paladin processing facility"),
            split("Destruction first, then recovery.",
                  "Recycling begins only once the data-bearing assets in a shipment have been destroyed and documented, so nothing enters the materials stream unaccounted for.",
                  [("Before", "Data neutralised", "Data-bearing assets are destroyed and certified per serial before anything moves into materials processing."),
                   ("After", "Materials recovered", "What remains is separated into metals, precious metals and plastics, each routed to an audited downstream processor.")]),
            ruled_list("materials", "Materials", "What comes back",
                       "Every stream is separated domestically and tracked to the processor that receives it.",
                       [("Ferrous &amp; non-ferrous", "Separated and sorted domestically for direct return into manufacturing supply."),
                        ("Gold, silver, palladium", "Recovered from circuit boards and connectors, which bulk shredding destroys."),
                        ("Sorted for recovery", "Housings and casings routed to controlled downstream processors, tracked the same way as everything else."),
                        ("No unaccountable downstream", "Every downstream partner is audited; nothing leaves the record once it enters intake.")],
                       cta=("See critical materials", "/critical-materials")),
            proof("Control", "Nothing leaves the record",
                  "Every downstream partner is audited, and each transfer is logged against the same chain-of-custody record the destruction certificates feed.",
                  ("See the full lifecycle", "/platform"), "Downstream handling",
                  [("Processing kept in domestic facilities", "Domestic"),
                   ("Downstream partners audited before use", "Audited"),
                   ("Transfers logged against the original intake", "Tracked"),
                   ("Magnet-bearing assets continue to REcapture", "Recovered")]),
            cta_band("Recycling is step three of five. Magnet-bearing assets continue on to REcapture.",
                     "See critical materials", "/critical-materials"),
        ]),
}


# ------------------------------------------------------------------ build
shell = open(SHELL, encoding="utf-8").read()
head_end = shell.find("</header>") + len("</header>")
foot_start = shell.rfind("<footer")
head, footer = shell[:head_end], shell[foot_start:]

for fname, spec in PAGES.items():
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{spec['title']}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">',
               f'<meta name="description" content="{spec["description"]}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">',
               f'<meta property="og:title" content="{spec["title"]}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">',
               f'<meta property="og:description" content="{spec["description"]}">', h, count=1)

    # the shell marks Secure ITAD as the current page; move that to this one
    slug = "/" + fname[:-5]
    h = h.replace('<a href="/secure-itad" style="color: #FFFFFF; font-weight: 500;',
                  '<a href="/secure-itad" style="color: #FFFFFF; font-weight: 300;')
    body = "\n\n".join(spec["sections"])
    out = h + "\n\n" + body + "\n\n" + footer
    open(os.path.join(SITE, fname), "w", encoding="utf-8").write(out)
    print(f"  {fname}: {len(spec['sections'])} sections, {len(out) // 1024}KB")
