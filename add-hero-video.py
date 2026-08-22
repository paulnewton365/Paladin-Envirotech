"""Put Paladin's own header video in the homepage hero.

NOTE: motion.js returns early for reduced-motion visitors, so initHeroVideo()
never runs for them. The reduced-motion branch stops the video separately.

Their footage rather than stock, which is the point: it removes the licensing
question and it is the company's own material, on a site that currently uses a
Getty comp for the leadership photograph.

Implemented defensively, because the file is remote and unverified:

  poster        the existing hero still, so something shows before the video
                buffers and the hero degrades to today's state if the remote
                file is ever renamed
  muted/loop    plus playsinline and autoplay, the only combination browsers
                will start without a user gesture
  preload       metadata only, so a phone does not pull the whole file to
                render the first screen
  scrim         a navy gradient over the footage. The headline is white with a
                copper accent, and copper on unpredictable video will not hold
                contrast without it
  mobile        poster only below 700px, handled in motion.js, so phones are
                not asked to download several megabytes
  reduced       prefers-reduced-motion gets the poster, consistent with the
                rest of the motion layer
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/index.html"

VIDEO = "https://paladinenvirotech.com/wp-content/uploads/2026/05/paladin_headervideo.mp4"
POSTER = "https://paladinenvirotech.com/wp-content/uploads/2026/05/IT-Asset-Disposition.jpg"

WELL_STYLE = ('flex: 1 1 360px; min-width: min(320px, 100%); aspect-ratio: 1 / 1; '
              'max-height: 520px; background: #14304C; position: relative; '
              'overflow: hidden; margin-bottom: 48px;')

NEW_WELL = (
    f'<div style="{WELL_STYLE}">'
    f'<video data-hero-video autoplay muted loop playsinline preload="metadata" '
    f'poster="{POSTER}" aria-label="Paladin operations" '
    f'style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">'
    f'<source src="{VIDEO}" type="video/mp4">'
    f'</video>'
    # Scrim: keeps the headline and copper accent legible over moving footage.
    f'<div aria-hidden="true" style="position: absolute; inset: 0; '
    f'background: linear-gradient(to right, rgba(11,33,56,0.55), rgba(11,33,56,0.15));'
    f'"></div>'
    f'</div>'
)

s = open(PAGE, encoding="utf-8").read()
old = re.search(r'<div style="flex: 1 1 360px[^"]*"><img[^>]*IT-Asset-Disposition[^>]*/?></div>', s)
assert old, "hero image well not found"
s = s[:old.start()] + NEW_WELL + s[old.end():]
open(PAGE, "w", encoding="utf-8").write(s)
print("hero image well replaced with video")

# --- mobile and reduced-motion handling, in the shared layer ---------------
MOTION = f"{SITE}/motion.js"
m = open(MOTION, encoding="utf-8").read()

HELPER = '''  /* ---- Hero video --------------------------------------------------------
     Below 700px, and for anyone who asked for reduced motion, drop back to the
     poster frame. A hero video is not worth several megabytes of a phone's
     data allowance, and the poster carries the same image either way. */

  function initHeroVideo() {
    var video = document.querySelector('[data-hero-video]');
    if (!video) return;
    var poster = video.getAttribute('poster');

    function useStill() {
      if (video.getAttribute('data-stilled') === '1') return;
      video.setAttribute('data-stilled', '1');
      try { video.pause(); } catch (e) {}
      video.removeAttribute('autoplay');
      // Drop the source so no bytes are fetched at all.
      var src = video.querySelector('source');
      if (src) src.parentNode.removeChild(src);
      video.load();
      if (poster) {
        video.style.background = 'url("' + poster + '") center / cover no-repeat';
      }
    }

    var small = window.matchMedia('(max-width: 700px)');
    if (reduce || small.matches) {
      useStill();
      return;
    }
    // Only downgrade on resize; upgrading mid-session would start a download
    // the visitor did not ask for.
    if (small.addEventListener) small.addEventListener('change', function (e) { if (e.matches) useStill(); });
    else if (small.addListener) small.addListener(function (e) { if (e.matches) useStill(); });

    // If the remote file fails, the poster is already showing underneath.
    video.addEventListener('error', useStill);
  }

'''

anchor = "  function initMap() {"
assert anchor in m, "initMap anchor not found"
m = m.replace(anchor, HELPER + anchor, 1)
m = m.replace("    initMap();\n    initTimeline();", "    initHeroVideo();\n    initMap();\n    initTimeline();", 1)
open(MOTION, "w", encoding="utf-8").write(m)
print("motion.js: initHeroVideo added")
