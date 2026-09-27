/* Scroll motion layer
   -------------------
   Each page already ships a small scroll runtime that drives [data-reveal],
   [data-stagger], [data-countup], [data-parallax] and [data-car]. Coverage is
   uneven: the homepage has nine reveal hooks, most interior pages have one to
   six, and contact / rare-earth-freedom-250 have no runtime at all.

   This file does two things and deliberately does NOT touch anything the page
   runtime already owns:

     1. Auto-tags untagged content blocks so every page reveals consistently.
        Tagged elements get data-mreveal and are driven here via
        IntersectionObserver. Existing [data-reveal] elements are skipped.
     2. Draws the facility map on the network page.

   Safety: the hidden state is applied by JS, never by CSS. If this file fails
   to load or throws, every element stays visible. Reduced-motion users skip
   the whole thing. */

(function () {
  'use strict';

  var EASE = 'cubic-bezier(0.2,0.7,0.1,1)';
  var reduce = false;
  try {
    reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  } catch (e) {}
  if (reduce || !('IntersectionObserver' in window)) {
    // The per-page runtime does not check the reduced-motion preference, so
    // pin its elements open on its behalf. Setting dataset.shown stops its
    // scroll handler from hiding them again.
    // The early return below means initHeroVideo() never runs for these
    // visitors, so the hero video has to be stopped here or it would autoplay
    // for exactly the people who asked it not to.
    var stopHeroVideo = function () {
      var v = document.querySelector('[data-hero-video]');
      if (!v || v.getAttribute('data-stilled') === '1') return;
      v.setAttribute('data-stilled', '1');
      try { v.pause(); } catch (e) {}
      v.removeAttribute('autoplay');
      var src = v.querySelector('source');
      if (src) src.parentNode.removeChild(src);
      v.load();
      var poster = v.getAttribute('data-still');
      if (poster) v.style.background = 'url("' + poster + '") center / cover no-repeat';
      v.style.opacity = '1';
    };

    var settle = function () {
      document.querySelectorAll('[data-timeline-beat]').forEach(function (el) {
        el.classList.add('is-in');
      });
      document.querySelectorAll('[data-chain-paladin]').forEach(function (el) {
        el.classList.add('is-in');
      });
      document.querySelectorAll('[data-chain-node]').forEach(function (el) {
        el.style.opacity = '1';
      });
      document.querySelectorAll('[data-chain-tangle]').forEach(function (el) {
        el.style.clipPath = 'none';
      });
      document.querySelectorAll('[data-reveal],[data-stagger]').forEach(function (el) {
        el.dataset.shown = '1';
        el.style.transition = 'none';
        el.style.opacity = '1';
        el.style.transform = 'none';
      });
    };
    var stampReduced = function () {
      var meta = document.querySelector('meta[name="build-version"]');
      var footer = document.querySelector('footer');
      if (!meta || !footer || footer.querySelector('[data-build-stamp]')) return;
      var dateMeta = document.querySelector('meta[name="build-date"]');
      var el = document.createElement('div');
      el.setAttribute('data-build-stamp', '');
      el.style.cssText = 'text-align:right;padding:8px clamp(24px,5vw,72px) 0;' +
        'color:#C3CDD6;font-size:11px;letter-spacing:0.6px;';
      el.textContent = 'Build ' + meta.content + (dateMeta ? ' \u00b7 ' + dateMeta.content : '');
      footer.appendChild(el);
      if (window.location.hash && window.location.hash.length > 1) {
        try {
          var t = document.querySelector(window.location.hash);
          if (t && window.scrollY < 40) {
            var h = document.querySelector('header');
            var off = h ? h.getBoundingClientRect().height : 0;
            var yy = t.getBoundingClientRect().top + window.scrollY - off - 8;
            window.scrollTo(0, yy < 0 ? 0 : yy);
          }
        } catch (e) {}
      }
      var bar = document.querySelector('[data-stickybar]');
      if (bar && bar.offsetHeight && !document.getElementById('pal-bar-clearance')) {
        var st = document.createElement('style');
        st.id = 'pal-bar-clearance';
        st.textContent = 'footer { padding-bottom: ' + (bar.offsetHeight + 52) + 'px !important; }';
        document.head.appendChild(st);
      }
    };
    var n = 0;
    var poll = function () {
      settle();
      stopHeroVideo();
      stampReduced();
      // Functional, not decorative: the sector selector must still work
      // (it steps on scroll or click; its transitions are off under reduce).
      try { initIndustries(); } catch (e) {}
      if (n++ < 40) setTimeout(poll, 100);
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', poll);
    } else {
      poll();
    }
    return;
  }

  // Elements whose subtree must not sit under a transform: a transformed
  // ancestor becomes the containing block for fixed/sticky descendants and
  // silently breaks them.
  var UNSAFE = '[data-stickybar],[data-car],[data-parallax],[style*="position: sticky"],[style*="position: fixed"]';

  function safe(el) {
    if (el.matches(UNSAFE) || el.querySelector(UNSAFE)) return false;
    var cs = getComputedStyle(el);
    if (cs.position === 'sticky' || cs.position === 'fixed') return false;
    return true;
  }

  // Pages have no <section> elements. They are a stack of full-width band
  // divs under one container, so walk past single-child wrappers to find the
  // element that actually holds the bands.
  /* Two page shapes exist. React-rendered pages wrap everything in a single
     div; /secure-itad is static HTML with <section> elements straight under
     <body>. Find whichever holds the bands. */
  function pageRoot() {
    var wrapper = document.body.querySelector(':scope > div');
    if (wrapper) {
      // React page. Mid-render the tree is briefly a chain of single children,
      // so return null rather than guessing; the caller retries. Falling back
      // to <body> here tagged the whole page as one band about half the time.
      var node = wrapper, guard = 0;
      while (node && node.children.length === 1 && guard++ < 5) node = node.children[0];
      return (node && node.children.length >= 2) ? node : null;
    }
    // Static page: the bands sit directly on <body>.
    return document.body;
  }

  function bands() {
    var node = pageRoot();
    return node ? Array.prototype.slice.call(node.children) : [];
  }

  function taggable(el) {
    if (el.hasAttribute('data-reveal') || el.hasAttribute('data-mreveal')) return false;
    if (el.hasAttribute('data-stagger') || el.hasAttribute('data-countup')) return false;
    // /secure-itad ships its own reveal runtime for these hooks.
    if (el.hasAttribute('data-fact') || el.hasAttribute('data-method')) return false;
    var tag = el.tagName.toLowerCase();
    if (tag === 'header' || tag === 'footer' || tag === 'script' || tag === 'style') return false;
    if (el.closest('header') || el.closest('footer')) return false;
    return safe(el);
  }

  function contentParent(band) {
    var node = band, guard = 0;
    while (node && node.children.length === 1 && guard++ < 4) node = node.children[0];
    return node || band;
  }

  function tagOne(el, delay) {
    if (!taggable(el)) return false;
    // Never nest a reveal inside another reveal: the child would fade in on top
    // of a parent that is itself still fading, which reads as a stutter.
    if (el.parentElement && el.parentElement.closest('[data-mreveal]')) return false;
    // The timeline rail runs its own sequence; a second fade on top stutters.
    if (el.closest('[data-timeline-rail]')) return false;
    if (el.closest('[data-chain-paladin]')) return false;
    el.setAttribute('data-mreveal', '');
    el.setAttribute('data-mdelay', String(delay));
    return true;
  }

  function tagBlocks() {
    /* The pages now ship their own reveal, tagging each band with
       [data-reveal]. Auto-tagging inner content on top of that gives two
       animations running at different offsets on the same hero, which reads
       as a bounce on load. If the page has its own reveal, leave it alone. */
    if (document.querySelector('[data-reveal]')) return;

    var tagged = 0;

    bands().forEach(function (band) {
      var tag = band.tagName.toLowerCase();
      if (tag === 'header' || tag === 'footer' || tag === 'script') return;
      if (band.getBoundingClientRect().height < 60) return;

      // Bands the page runtime already owns keep their own whole-band reveal;
      // everything else reveals its content blocks individually so interior
      // pages animate at the same granularity as the homepage.
      if (!band.hasAttribute('data-reveal')) {
        var holder = contentParent(band);
        var blocks = Array.prototype.filter.call(holder.children, function (c) {
          return c.getBoundingClientRect().height > 36;
        });
        if (blocks.length >= 2) {
          var i = 0;
          blocks.forEach(function (c) {
            if (tagOne(c, Math.min(i, 6) * 80)) { i++; tagged++; }
          });
        } else if (tagOne(band, 0)) {
          tagged++;
        }
      }

      // Inside every band, stagger rows of sibling cards, stats or columns.
      band.querySelectorAll('div').forEach(function (row) {
        var cs = getComputedStyle(row);
        if (cs.display !== 'grid' && cs.display !== 'flex') return;
        var kids = Array.prototype.slice.call(row.children).filter(function (k) {
          return k.getBoundingClientRect().height > 48;
        });
        if (kids.length < 2 || kids.length > 8) return;
        var j = 0;
        kids.forEach(function (k) {
          if (tagOne(k, 90 + Math.min(j, 5) * 90)) { j++; tagged++; }
        });
      });
    });

    return tagged;
  }

  function armReveals() {
    // Only ever arm an element once, so a second pass can pick up late
    // content without resetting anything already revealed.
    var els = document.querySelectorAll('[data-mreveal]:not([data-marmed])');
    if (!els.length) return;
    els.forEach(function (el) {
      el.setAttribute('data-marmed', '');
      el.style.willChange = 'opacity, transform';
      el.style.opacity = '0';
      el.style.transform = 'translateY(22px)';
      el.style.transition = 'opacity 620ms ' + EASE + ', transform 620ms ' + EASE;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseInt(el.getAttribute('data-mdelay'), 10) || 0;
        setTimeout(function () {
          el.style.opacity = '1';
          el.style.transform = 'none';
          setTimeout(function () { el.style.willChange = ''; }, 700);
        }, delay);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    els.forEach(function (el) { io.observe(el); });

    // Failsafe: anything still hidden after 6s is forced visible. Protects
    // against an element that never satisfies the observer (zero-height
    // parent, display toggled, clipped container).
    setTimeout(function () {
      document.querySelectorAll('[data-mreveal]').forEach(function (el) {
        if (el.style.opacity === '0') { el.style.opacity = '1'; el.style.transform = 'none'; }
      });
    }, 6000);
  }

  /* ---- Chain comparison --------------------------------------------------
     The tangled multi-vendor path draws in with scroll progress and its four
     nodes appear as the line reaches them. The Paladin line plays once when it
     comes into view. Again in motion.js rather than a page script tag. */

  function initChain() {
    var tangle = document.querySelector('[data-chain-tangle]');
    var paladin = document.querySelector('[data-chain-paladin]');
    if (!tangle || !paladin) return;
    if (tangle.getAttribute('data-chain-ready') === '1') return;
    tangle.setAttribute('data-chain-ready', '1');

    var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-chain-node]'));
    var NODE_AT = [0.2, 0.42, 0.63, 0.84];

    function showAll() {
      paladin.classList.add('is-in');
      nodes.forEach(function (n) { n.style.opacity = '1'; });
      tangle.style.clipPath = 'none';
    }

    if (reduce) { showAll(); return; }

    var ticking = false;
    function update() {
      ticking = false;
      var svg = tangle.ownerSVGElement;
      if (!svg) return;
      var r = svg.getBoundingClientRect();
      var vh = window.innerHeight || 800;
      var p = (vh * 0.85 - r.top) / (r.height + vh * 0.2);
      if (p < 0) p = 0;
      if (p > 1) p = 1;
      tangle.style.clipPath = 'inset(0 ' + ((1 - p) * 100).toFixed(2) + '% 0 0)';
      nodes.forEach(function (n) {
        if (p >= NODE_AT[parseInt(n.getAttribute('data-chain-node'), 10)]) n.style.opacity = '1';
      });
      var pr = paladin.getBoundingClientRect();
      if (pr.top < vh * 0.85 && pr.bottom > 0) paladin.classList.add('is-in');
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();

    // Fail visible: never leave the diagram half-drawn.
    setTimeout(showAll, 6000);
  }

  /* ---- Deep links --------------------------------------------------------
     The browser acts on the URL hash while the page is still empty, because
     content is React-rendered a beat later, so arriving at /company#leadership
     leaves you at the top. Once content exists, jump to the target and clear
     the sticky header's height so the section is not tucked underneath it. */

  function honourHash() {
    if (!window.location.hash || window.location.hash.length < 2) return;
    var target;
    try {
      target = document.querySelector(window.location.hash);
    } catch (e) {
      return;
    }
    if (!target) return;
    if (Math.abs(window.scrollY - (target.getBoundingClientRect().top + window.scrollY)) < 80) return;
    var header = document.querySelector('header');
    var offset = header ? header.getBoundingClientRect().height : 0;
    var y = target.getBoundingClientRect().top + window.scrollY - offset - 8;
    window.scrollTo({ top: y < 0 ? 0 : y, behavior: 'auto' });
  }

  /* ---- Hero video --------------------------------------------------------
     Below 700px, and for anyone who asked for reduced motion, drop back to the
     poster frame. A hero video is not worth several megabytes of a phone's
     data allowance, and the poster carries the same image either way. */

  function initHeroVideo() {
    var video = document.querySelector('[data-hero-video]');
    if (!video) return;
    var poster = video.getAttribute('data-still');

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
      video.style.opacity = '1';
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

    /* Autoplay is decided on the muted PROPERTY, not the attribute. Setting
       muted="" in markup does not reliably set the property, and a video the
       browser considers unmuted is refused without a user gesture. Set the
       properties directly before asking to play.

       The attribute is also only evaluated as the element enters the DOM, and
       these pages are React-rendered, so it is inserted after parse and often
       skipped entirely. */
    video.muted = true;
    video.defaultMuted = true;
    video.playsInline = true;
    video.loop = true;
    video.setAttribute('muted', '');
    video.setAttribute('loop', '');

    // Some templates mishandle a child <source>; point the element at the file
    // directly if nothing resolved.
    var source = video.querySelector('source');
    if (!video.currentSrc && !video.getAttribute('src') && source) {
      video.setAttribute('src', source.getAttribute('src'));
      video.load();
    }

    var attempts = 0;
    function tryPlay() {
      if (video.getAttribute('data-stilled') === '1') return;
      video.muted = true;
      var p = video.play();
      if (p && typeof p.catch === 'function') {
        p.catch(function (err) {
          attempts++;
          // Report once, so a blank hero can be diagnosed from the console
          // rather than guessed at.
          if (attempts === 1 && window.console) {
            console.warn('[paladin] hero video did not autoplay:',
                         err && err.name, err && err.message,
                         '| networkState', video.networkState,
                         '| readyState', video.readyState,
                         '| currentSrc', video.currentSrc || '(none)');
          }
          if (attempts >= 4) useStill();
        });
      }
    }
    // Reveal only once there are frames to show, so the hero never flashes an
    // empty box or a half-decoded frame.
    function reveal() {
      if (video.getAttribute('data-stilled') === '1') return;
      video.style.opacity = '1';
    }
    video.addEventListener('playing', reveal);
    video.addEventListener('canplay', reveal);

    /* Belt and braces on looping. The loop attribute is ignored in some cases
       when the element is inserted after parse, and a server that handles range
       requests poorly can fail the seek back to zero. Restart explicitly. */
    video.addEventListener('ended', function () {
      if (video.getAttribute('data-stilled') === '1') return;
      try { video.currentTime = 0; } catch (e) {}
      tryPlay();
    });

    video.addEventListener('loadeddata', tryPlay);
    video.addEventListener('canplay', tryPlay);
    // Some browsers pause background video on tab switch and do not resume.
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) tryPlay();
    });
    tryPlay();

    // If the remote file fails, the poster is already showing underneath.
    video.addEventListener('error', useStill);
  }

  /* ---- Industries selector ----------------------------------------------
     One sector at a time: index on the left, detail panel on the right.
     Lives here rather than in a page script tag because /industries is
     React-rendered and a tag inside the template never executes. */

  function initIndustries() {
    var root = document.querySelector('[data-ind-root]');
    if (!root || root.getAttribute('data-ind-ready') === '1') return;
    root.setAttribute('data-ind-ready', '1');

    var ROWS = [
      { num: "01", name: "Hyperscale & data centers", head: "A live facility can come down without going dark", body: "Racks, networking gear and generators come out on your schedule: zero downtime, hazardous materials handled, every asset logged as it leaves." },
      { num: "02", name: "Government & public sector", head: "Taxpayer resources, accounted for to the last unit", body: "Federal security standards, met without slowing the refresh down, and an audit trail that holds up when someone outside your agency asks to see it." },
      { num: "03", name: "Healthcare", head: "Patient trust doesn\u2019t end when the hardware does", body: "Every retired workstation, server and medical device is HIPAA-compliant destroyed and certified, from a single clinic to a multi-hospital system." },
      { num: "04", name: "Financial services", head: "The audit you\u2019re dreading becomes routine", body: "PCI DSS-compliant destruction across trading-floor systems and branch computers, documented in a way that satisfies the examiner the first time." },
      { num: "05", name: "Fortune 500 enterprise", head: "One refresh, fifty sites, one point of contact", body: "A single-point project manages the coordination across every location, so the coordination sits with us." },
      { num: "06", name: "OEMs & VARs", head: "Returned equipment becomes a managed program", body: "Take-back and warranty returns run through component harvesting and refurbishment, with recovery metrics you can put in front of customers." },
      { num: "07", name: "Manufacturing & industrial", head: "The office and the shop floor stop being two problems", body: "Corporate IT refreshes and industrial control equipment come down under the same security protocol, at facilities built to handle both." },
      { num: "08", name: "Wind & renewable energy", head: "Retiring a turbine pays for itself", body: "Steel, copper and rare-earth magnets recovered from a single turbine or an entire wind farm turn a decommissioning cost into a recovery return." }
    ];

    var list  = root.querySelector('[data-ind-list]');
    var ghost = root.querySelector('[data-ind-ghost]');
    var label = root.querySelector('[data-ind-label]');
    var copy  = root.querySelector('[data-ind-copy]');
    var head  = root.querySelector('[data-ind-head]');
    var text  = root.querySelector('[data-ind-text]');
    var count = root.querySelector('[data-ind-count]');
    if (!list || !ghost) return;

    ROWS.forEach(function (r, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pal-ind-item';
      b.setAttribute('role', 'tab');
      b.innerHTML = '<span class="pal-ind-dot"></span><span class="pal-ind-num"></span>' +
                    '<span class="pal-ind-name"></span>';
      b.querySelector('.pal-ind-num').textContent = r.num;
      b.querySelector('.pal-ind-name').textContent = r.name;
      b.addEventListener('click', function () { go(i); });
      list.appendChild(b);
    });

    var items = list.querySelectorAll('.pal-ind-item');
    var active = 0;

    function go(i) {
      active = (i + ROWS.length) % ROWS.length;
      var r = ROWS[active];
      Array.prototype.forEach.call(items, function (el, n) {
        el.setAttribute('aria-selected', n === active ? 'true' : 'false');
      });
      ghost.textContent = r.num;
      label.textContent = r.name;
      head.textContent = r.head;
      text.textContent = r.body;
      count.textContent = r.num + ' / ' + ROWS[ROWS.length - 1].num;
      if (!reduce) {
        copy.style.animation = 'none';
        void copy.offsetWidth;
        copy.style.animation = '';
      }
    }

    /* Pinned walkthrough. The section is a tall track with a sticky block
       inside; scroll position through the track picks the sector, so every
       sector is shown before the page moves on. Clicking a sector or an
       arrow scrolls to that sector's stretch, keeping the two in step. If
       the block cannot fit the screen it falls back to an ordinary section. */
    var track = root.closest('.pal-ind-track');
    var pin = track && track.querySelector('.pal-ind-pin');
    var bar = root.querySelector('[data-ind-progress]');
    var pinned = false;
    document.documentElement.classList.add('pal-ind-js');

    function hdr() { var h = document.querySelector('header'); return h ? h.offsetHeight : 0; }
    function measure() {
      if (!track || !pin) return;
      track.style.setProperty('--pal-hdr', hdr() + 'px');
      track.classList.remove('pal-ind-free');
      var inner = pin.firstElementChild;
      var fits = inner && inner.scrollHeight <= pin.clientHeight + 1;
      pinned = !!fits;
      track.classList.toggle('pal-ind-free', !pinned);
      sync();
    }
    function span() { return Math.max(1, track.offsetHeight - pin.offsetHeight); }
    function sync() {
      if (!pinned) { if (bar) bar.style.width = ''; return; }
      var p = (hdr() - track.getBoundingClientRect().top) / span();
      p = Math.min(1, Math.max(0, p));
      if (bar) bar.style.width = (p * 100).toFixed(2) + '%';
      var i = Math.min(ROWS.length - 1, Math.floor(p * ROWS.length));
      if (i !== active) go(i);
    }
    function jump(i) {
      if (!pinned) { go((i + ROWS.length) % ROWS.length); return; }
      var top = track.getBoundingClientRect().top + window.pageYOffset - hdr();
      // past either end: leave the walkthrough in that direction
      var y = i >= ROWS.length ? top + span() + 2 : i < 0 ? top - 2 : top + span() * (i + 0.5) / ROWS.length;
      window.scrollTo({ top: y, behavior: reduce ? 'auto' : 'smooth' });
    }
    if (track && pin) {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; sync(); }); }
      }, { passive: true });
      window.addEventListener('resize', measure);
      measure();
      setTimeout(measure, 600);
      // clicks on the index go through the scroll so position and sector agree
      Array.prototype.forEach.call(items, function (el, n) {
        el.addEventListener('click', function (e) { if (pinned) { e.stopImmediatePropagation(); jump(n); } }, true);
      });
    }

    root.querySelector('[data-ind-prev]').addEventListener('click', function () { jump(active - 1); });
    root.querySelector('[data-ind-next]').addEventListener('click', function () { jump(active + 1); });
    go(0);
    if (track && pin) sync();
  }

  /* ---- Build stamp -------------------------------------------------------
     Reads the version stamped into the page head and renders it discreetly at
     the end of the footer so a reviewer can always say which build they are
     looking at. */

  function buildStamp() {
    var meta = document.querySelector('meta[name="build-version"]');
    if (!meta) return;
    var footer = document.querySelector('footer');
    if (!footer || footer.querySelector('[data-build-stamp]')) return;
    var dateMeta = document.querySelector('meta[name="build-date"]');
    var el = document.createElement('div');
    el.setAttribute('data-build-stamp', '');
    el.style.cssText = 'text-align:right;padding:8px clamp(24px,5vw,72px) 0;' +
      'color:#C3CDD6;font-size:11px;letter-spacing:0.6px;';
    el.textContent = 'Build ' + meta.content + (dateMeta ? ' \u00b7 ' + dateMeta.content : '');
    footer.appendChild(el);
    clearStickyBar();
    if (window.console && console.info) {
      console.info('Paladin prototype build ' + meta.content);
    }
  }

  /* The CTA bar is fixed to the bottom of the viewport, so it sits on top of
     whatever the footer ends with once you reach the end of the page. Reserve
     its height at the foot of the footer.

     This goes in a stylesheet rule rather than an inline style: React owns the
     footer's style attribute and rewrites it on re-render, which silently
     undoes an inline padding set from here. An !important rule in a stylesheet
     outranks the inline style and survives. */
  function clearStickyBar() {
    if (document.getElementById('pal-bar-clearance')) return;
    var bar = document.querySelector('[data-stickybar]');
    if (!bar) {
      bar = Array.prototype.filter.call(
        document.querySelectorAll('body div'),
        function (e) {
          var cs = getComputedStyle(e);
          return cs.position === 'fixed' && cs.bottom === '0px' && e.offsetHeight > 20;
        }
      )[0];
    }
    if (!bar || !bar.offsetHeight) return;
    var style = document.createElement('style');
    style.id = 'pal-bar-clearance';
    style.textContent = 'footer { padding-bottom: ' + (bar.offsetHeight + 52) + 'px !important; }';
    document.head.appendChild(style);
  }

  /* The page is React-rendered and its bands measure zero until the browser
     has laid them out. Firing at DOMContentLoaded therefore tags nothing at
     all, which silently disables every reveal on the page. Wait for the load
     event, then for the bands to report real heights, before measuring. */

  function contentReady() {
    if (!document.body) return false;
    var node = pageRoot();
    if (!node || node.children.length < 2) return false;
    var tallest = 0;
    Array.prototype.forEach.call(node.children, function (c) {
      tallest = Math.max(tallest, c.getBoundingClientRect().height);
    });
    return tallest > 80;
  }

  var tries = 0;
  function init() {
    // While the access gate is up, the page is laid out but hidden. Intersection
    // observers would fire behind it and spend every reveal before the visitor
    // ever sees the page, so wait until the gate has been cleared.
    if (document.documentElement.classList.contains('pal-locked')) {
      return setTimeout(init, 120);
    }
    if (!contentReady() && tries++ < 200) {
      return setTimeout(init, 60);
    }
    buildStamp();
    // The sticky bar mounts a beat after the footer, so a single attempt here
    // races it. Retry briefly until the bar has a measurable height.
    var barTries = 0;
    (function waitForBar() {
      clearStickyBar();
      if (!document.getElementById('pal-bar-clearance') && barTries++ < 20) {
        setTimeout(waitForBar, 150);
      }
    })();
    tagBlocks();
    armReveals();
    initHeroVideo();
    initIndustries();
    initChain();
    honourHash();
    // Second pass for anything that lands after first paint (images resolving,
    // late layout). Both functions are idempotent.
    setTimeout(function () { tagBlocks(); armReveals(); initChain(); initIndustries(); honourHash(); }, 900);
  }

  if (document.readyState === 'complete') {
    init();
  } else {
    window.addEventListener('load', init);
    // Fallback in case a stalled subresource delays the load event.
    setTimeout(init, 2500);
  }
})();
