"""Remove the visible handoff before the hero video starts.

The poster was a different photograph from the footage, so the hero showed one
image and then cut to another. Three changes:

  1. preconnect and dns-prefetch to the video's origin, and a rel=preload hint,
     so the fetch starts as early as the parser can start it rather than when
     the element is constructed.

  2. No poster on desktop. The well is already navy, so the hero now goes navy
     to video rather than photo to video. The video fades in over 400ms once it
     can play, so there is no hard pop either.

  3. The photograph is kept, but only where a still is actually wanted: mobile
     and reduced-motion. It is applied as a background by motion.js in those
     cases, so those visitors still get an image rather than an empty navy box.

The real determinant of how fast it starts is file size and origin. The file is
served from their WordPress on a different host, which costs a DNS lookup, a TLS
handshake and whatever that server's throughput is. Hosting a compressed copy in
assets/ would do more for perceived speed than any markup change here.
"""
import re

SITE = "/home/claude/paladin-site"
PAGE = f"{SITE}/index.html"

VIDEO = "https://paladinenvirotech.com/wp-content/uploads/2026/05/paladin_headervideo.mp4"
STILL = "https://paladinenvirotech.com/wp-content/uploads/2026/05/IT-Asset-Disposition.jpg"

s = open(PAGE, encoding="utf-8").read()

# --- 1. start the fetch as early as possible -----------------------------
HINTS = (
    '<link rel="preconnect" href="https://paladinenvirotech.com" crossorigin>\n'
    '<link rel="dns-prefetch" href="https://paladinenvirotech.com">\n'
    f'<link rel="preload" as="video" href="{VIDEO}" type="video/mp4">\n'
)
anchor = '<meta name="robots" content="noindex, nofollow">'
assert anchor in s, "head anchor not found"
assert "rel=\"preload\" as=\"video\"" not in s, "already applied"
s = s.replace(anchor, HINTS + anchor, 1)

# --- 2. drop the poster, remember the still for the fallbacks ------------
old_poster = f'poster="{STILL}" '
assert old_poster in s, "poster attribute not found"
s = s.replace(old_poster, f'data-still="{STILL}" ', 1)

# fade in rather than pop
s = s.replace(
    'style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">'
    '<source',
    'style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; '
    'opacity: 0; transition: opacity 400ms ease;">'
    '<source',
    1,
)

open(PAGE, "w", encoding="utf-8").write(s)
print("head hints added, poster removed, fade-in prepared")

# --- 3. motion.js: reveal on canplay, still image only for the fallbacks --
MOTION = f"{SITE}/motion.js"
m = open(MOTION, encoding="utf-8").read()

m = m.replace(
    "    var poster = video.getAttribute('poster');",
    "    var poster = video.getAttribute('data-still');",
    1,
)
m = m.replace(
    "      var poster = v.getAttribute('poster');",
    "      var poster = v.getAttribute('data-still');",
    1,
)

old_play = "    video.addEventListener('loadeddata', tryPlay);"
new_play = """    // Reveal only once there are frames to show, so the hero never flashes an
    // empty box or a half-decoded frame.
    function reveal() {
      if (video.getAttribute('data-stilled') === '1') return;
      video.style.opacity = '1';
    }
    video.addEventListener('playing', reveal);
    video.addEventListener('canplay', reveal);

    video.addEventListener('loadeddata', tryPlay);"""
assert old_play in m
m = m.replace(old_play, new_play, 1)

# the still fallback has to become visible, since opacity now starts at 0
m = m.replace(
    """      if (poster) {
        video.style.background = 'url("' + poster + '") center / cover no-repeat';
      }""",
    """      if (poster) {
        video.style.background = 'url("' + poster + '") center / cover no-repeat';
      }
      video.style.opacity = '1';""",
    1,
)
m = m.replace(
    """      if (poster) v.style.background = 'url("' + poster + '") center / cover no-repeat';""",
    """      if (poster) v.style.background = 'url("' + poster + '") center / cover no-repeat';
      v.style.opacity = '1';""",
    1,
)

open(MOTION, "w", encoding="utf-8").write(m)
print("motion.js: fade-in on canplay, still reserved for mobile and reduced motion")
