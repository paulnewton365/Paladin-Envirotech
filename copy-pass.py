"""Copy pass: remove the rhetorical patterns that make the site read as machine-written.

The dominant one is antithesis, "X, not Y", which appeared 25 times. It is a
persuasive-sounding shape that carries almost no information: the reader learns
what something is not, which they were not wondering about. Most instances lose
nothing by stating the positive on its own.

Also handled: "A before it is B", "the question is whether", "is what makes",
"matters more than", "rather than a pillar", and a sentence-initial "And" used
for rhythm.

Every pair is asserted, so a miss fails loudly rather than passing silently.
"""
import glob
import os

SITE = "/home/claude/paladin-site"

# (old, new, expected occurrences across the whole site)
EDITS = [
    # --- CTA repeated on three pages -------------------------------------
    ("Speak to a Paladin engineer, not a broker.",
     "Speak to one of our engineers.", 3),

    # --- company ----------------------------------------------------------
    ("Credibility is a process, not a claim.",
     "Credibility has to be auditable.", 1),
    ("Operators, not intermediaries.",
     "The people who run the work.", 1),
    ("One joined-up partnership ecosystem",
     "One joined-up partnership network", 1),

    # --- contact ----------------------------------------------------------
    ("You will speak with someone who runs the process, not a call queue or a reseller.",
     "You will speak with someone who runs the process.", 1),

    # --- critical materials ----------------------------------------------
    ("Recovery at usable quality, not just reclaimed scrap.",
     "Recovered at usable quality.", 1),
    ("as every other magnet-bearing asset on the platform, an application, not a separate business.",
     "as every other magnet-bearing asset on the platform.", 1),

    # --- electronics recycling -------------------------------------------
    ("Sorted, not landfilled", "Sorted for recovery", 1),
    ("Processed domestically. Not exported and forgotten.",
     "Processed domestically, with every downstream step recorded.", 1),

    # --- index ------------------------------------------------------------
    ("a compliance-led operator built around provable processes, not resale margins or downstream promises. For recycling to work it has to be treated as critical infrastructure, not a loose network or a bolt-on.",
     "a compliance-led operator whose processes can be proven at every step. Recycling only works when it is run as critical infrastructure.", 1),
    ("automated settlement reporting, built for audit, not retrofitted from logistics software.",
     "automated settlement reporting, all built for audit from the start.", 1),
    ("A hub-and-satellite model that reaches regional and mid-market organizations, not only large metros.",
     "A hub-and-satellite model that reaches regional and mid-market organizations as well as large metros.", 1),
    ("And the operations team has a report, not a guess, about where every one of them went.",
     "The operations team starts the day with a report showing where every one of them went.", 1),

    # --- industries -------------------------------------------------------
    ("Racks, networking gear and backup generators come out on schedule, not on your operation's terms.",
     "Racks, networking gear and backup generators come out on your schedule.", 1),
    ("Returned equipment becomes a program, not a pile",
     "Returned equipment becomes a managed program", 1),

    # --- network ----------------------------------------------------------
    ("so each location's status is shown as it stands today, not as a company-wide claim.",
     "so each location's status is shown as it stands today.", 1),

    # --- paladin local ----------------------------------------------------
    ("Regional, not just metro", "Beyond the major metros", 1),
    ("for offices and branch locations, not just hyperscale campuses.",
     "for offices and branch locations as well as hyperscale campuses.", 1),

    # --- platform ---------------------------------------------------------
    ("Recycling, domestic, not exported", "Recycling, processed domestically", 1),
    ("Built for audit, not retrofitted from logistics software.",
     "Built for audit from the start.", 1),
    ("close to where assets are generated, regional and mid-market, not only large metros.",
     "close to where assets are generated, across regional and mid-market sites as well as large metros.", 1),

    # --- freedom 250 ------------------------------------------------------
    ("These are, not coincidentally, the same organizations carrying the most sensitive data on that hardware.",
     "These are also the organizations carrying the most sensitive data on that hardware.", 1),
    ("Why this sits inside the platform, not beside it",
     "Why this sits inside the platform", 1),
    ("The constraint is not technology. Recovery at usable quality is proven. The constraint is volume, and volume is a scheduling and logistics problem, not a materials-science one.",
     "Recovery at usable quality is already proven. The constraint is volume, which is a scheduling and logistics problem.", 1),

    # --- secure itad ------------------------------------------------------
    ("matched to media type and your policy, not a one-size default.",
     "matched to media type and your policy.", 1),

    # --- article ----------------------------------------------------------
    ("Why the timeline matters more than the tonnage", "The timeline problem", 2),  # heading plus its contents-rail entry
    ("Recovery is a logistics and custody problem before it is a chemistry problem.",
     "Recovery depends on logistics and custody as much as on chemistry.", 1),
    ("and it is the reason recycling has stayed a footnote in the critical-materials conversation rather than a pillar of it.",
     "and it is why recycling has stayed a footnote in the critical-materials conversation.", 1),
    ("The question is whether the magnets inside them re-enter a domestic supply chain or leave the country as mixed scrap.",
     "Either the magnets inside them re-enter a domestic supply chain, or they leave the country as mixed scrap.", 1),
    ("Recovery at this scale is a logistics problem before it is a chemistry problem.",
     "At this scale, recovery is mostly a logistics problem.", 1),
    ("Running destruction, recovery and refining inside one system is what makes the volume usable rather than theoretical. It is also what lets a customer see, per serial, where their material went.",
     "Running destruction, recovery and refining inside one system makes that volume usable, and lets a customer see, per serial, where their material went.", 1),
]


def run():
    files = [f for f in sorted(glob.glob(os.path.join(SITE, "*.html")))
             if os.path.basename(f) != "sitemap.html"]
    sources = {f: open(f, encoding="utf-8").read() for f in files}

    misses, applied = [], 0
    for old, new, expected in EDITS:
        count = sum(s.count(old) for s in sources.values())
        if count != expected:
            misses.append((old[:70], expected, count))
            continue
        for f in sources:
            if old in sources[f]:
                sources[f] = sources[f].replace(old, new)
        applied += count

    if misses:
        print("MISMATCHES, nothing written:")
        for text, want, got in misses:
            print(f"  expected {want}, found {got}: {text}")
        return False

    for f, s in sources.items():
        open(f, "w", encoding="utf-8").write(s)
    print(f"applied {applied} replacements across {len(files)} pages")
    return True


if __name__ == "__main__":
    ok = run()
    raise SystemExit(0 if ok else 1)
