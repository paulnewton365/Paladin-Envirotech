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
      var poster = v.getAttribute('poster');
      if (poster) v.style.background = 'url("' + poster + '") center / cover no-repeat';
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
        'color:#5B7085;font-size:11px;letter-spacing:0.6px;';
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

  /* ---- Facility map ------------------------------------------------------
     The nine routes fan out from Tampa at (390, 262) in a 1200x420 viewBox.
     Three of them carry stroke-dasharray for the international styling, so a
     stroke-dashoffset draw would make the dashes march rather than extend.
     Instead the whole route group is clipped by a circle centred on Tampa
     whose radius grows outward, which reads as routes leaving HQ and works
     the same for solid and dashed strokes. Cities fade in as the wave passes,
     staggered by their real distance from Tampa. */

  var HQ_X = 390, HQ_Y = 262, MAX_R = 780;

  function animateMap(svg) {
    if (svg.getAttribute('data-mapped') === '1') return;
    svg.setAttribute('data-mapped', '1');

    var groups = svg.querySelectorAll('g');
    var routes = null;
    groups.forEach(function (g) {
      if (!routes && g.querySelector('path')) routes = g;
    });
    if (!routes) return;

    var NS = 'http://www.w3.org/2000/svg';
    var clipId = 'pal-map-wipe';
    var defs = document.createElementNS(NS, 'defs');
    var clip = document.createElementNS(NS, 'clipPath');
    clip.setAttribute('id', clipId);
    clip.setAttribute('clipPathUnits', 'userSpaceOnUse');
    var circle = document.createElementNS(NS, 'circle');
    circle.setAttribute('cx', HQ_X);
    circle.setAttribute('cy', HQ_Y);
    circle.setAttribute('r', '0');
    clip.appendChild(circle);
    defs.appendChild(clip);
    svg.insertBefore(defs, svg.firstChild);
    routes.setAttribute('clip-path', 'url(#' + clipId + ')');

    // Cities: every circle/text except the HQ marker at the origin.
    var cities = [];
    svg.querySelectorAll('circle, text').forEach(function (el) {
      var x, y;
      if (el.tagName.toLowerCase() === 'circle') {
        x = parseFloat(el.getAttribute('cx'));
        y = parseFloat(el.getAttribute('cy'));
      } else {
        x = parseFloat(el.getAttribute('x'));
        y = parseFloat(el.getAttribute('y'));
      }
      if (isNaN(x) || isNaN(y)) return;
      var d = Math.sqrt(Math.pow(x - HQ_X, 2) + Math.pow(y - HQ_Y, 2));
      if (d < 30) return; // HQ marker and its label stay put
      cities.push({ el: el, d: d });
      el.style.opacity = '0';
      el.style.transition = 'opacity 420ms ease-out';
    });

    /* Scroll-driven rather than timed. A timed animation can finish before the
       reader has scrolled the map into view, so the routes appear already
       drawn. Tying the wipe radius to scroll position means the lines always
       flow out of Tampa as the section moves up the screen, and rewind if the
       reader scrolls back. */

    var clipId2 = clipId;
    function draw(p) {
      // Guard: if a React re-render dropped the injected defs, the clip would
      // point at nothing and hide every route. Detach rather than hide.
      if (!document.getElementById(clipId2)) {
        routes.removeAttribute('clip-path');
        cities.forEach(function (c) { c.el.style.opacity = '1'; });
        return;
      }
      routes.setAttribute('clip-path', 'url(#' + clipId2 + ')');
      var eased = Math.pow(p, 1.35);
      var reached = eased * MAX_R;
      circle.setAttribute('r', String(reached));
      cities.forEach(function (c) {
        c.el.style.opacity = reached > c.d - 12 ? '1' : '0';
      });
    }

    var ticking = false;
    function update() {
      ticking = false;
      var r = svg.getBoundingClientRect();
      if (!r.height) return;
      var vh = window.innerHeight || 800;
      // 0 when the top of the map reaches the bottom of the viewport,
      // 1 by the time it has travelled to just above the middle.
      var span = vh * 0.62;
      var p = (vh - r.top) / span;
      if (p < 0) p = 0;
      if (p > 1) p = 1;
      draw(p);
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
  }

  /* ---- Timeline rail -----------------------------------------------------
     Beats reveal in sequence and a gold progress line follows scroll down the
     rail. This lives here rather than in a script tag on the page because the
     page is React-rendered and a tag inside the template never executes. */

  function initTimeline() {
    var rail = document.querySelector('[data-timeline-rail]');
    if (!rail || rail.getAttribute('data-timeline-ready') === '1') return;
    rail.setAttribute('data-timeline-ready', '1');

    var progress = rail.querySelector('[data-timeline-progress]');
    var beats = Array.prototype.slice.call(rail.querySelectorAll('[data-timeline-beat]'));
    if (!beats.length) return;

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var i = beats.indexOf(entry.target);
        setTimeout(function () { entry.target.classList.add('is-in'); }, Math.max(0, i) * 90);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.4 });
    beats.forEach(function (b) { io.observe(b); });

    var ticking = false;
    function update() {
      ticking = false;
      if (!progress) return;
      var r = rail.getBoundingClientRect();
      if (!r.height) return;
      var line = window.innerHeight * 0.62;
      var p = (line - r.top) / r.height;
      if (p < 0) p = 0;
      if (p > 1) p = 1;
      progress.style.height = (p * 100).toFixed(2) + '%';
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();

    // Failsafe: if the observer never fires, show the beats anyway.
    setTimeout(function () {
      beats.forEach(function (b) { b.classList.add('is-in'); });
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

    /* The autoplay attribute is evaluated when the element enters the DOM.
       These pages are React-rendered, so the element is inserted after parse
       and the browser often skips it, which is why the video appeared only
       sometimes. Ask for playback explicitly, and again once data arrives. */
    function tryPlay() {
      if (video.getAttribute('data-stilled') === '1') return;
      var p = video.play();
      if (p && typeof p.catch === 'function') {
        p.catch(function () { /* blocked; the poster is already showing */ });
      }
    }
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

  function initMap() {
    var svg = document.querySelector('svg[aria-label*="facility network"]');
    if (svg) { buildMobileNetwork(svg); animateMap(svg); }
  }

  /* ---- Mobile network view ----------------------------------------------
     The map is a 1200x420 landscape diagram. On a portrait phone it scales
     down to roughly a third of its design size and the city labels become
     unreadable, so below 760px it is replaced with a vertical routing spine
     built from the SVG's own labels. Desktop is untouched, and the two views
     cannot drift apart because the list is derived from the same source. */

  function buildMobileNetwork(svg) {
    var wrap = svg.parentElement;
    if (!wrap || wrap.querySelector('[data-mobile-network]')) return;

    // International routes are the dashed ones. Their endpoints are the three
    // furthest cities, so classify by matching each city to the dashed paths'
    // end coordinates rather than hard-coding names.
    var intl = [];
    svg.querySelectorAll('path[stroke-dasharray]').forEach(function (p) {
      var d = p.getAttribute('d') || '';
      var nums = d.replace(/[^0-9.\- ]/g, ' ').trim().split(/\s+/).map(parseFloat);
      if (nums.length >= 6) intl.push({ x: nums[nums.length - 2], y: nums[nums.length - 1] });
    });

    var cities = [];
    svg.querySelectorAll('circle').forEach(function (c) {
      var x = parseFloat(c.getAttribute('cx')), y = parseFloat(c.getAttribute('cy'));
      if (isNaN(x) || isNaN(y)) return;
      if (Math.abs(x - HQ_X) < 30 && Math.abs(y - HQ_Y) < 30) return; // HQ marker
      // nearest text label to this dot
      var best = null, bestD = 1e9;
      svg.querySelectorAll('text').forEach(function (t) {
        var tx = parseFloat(t.getAttribute('x')), ty = parseFloat(t.getAttribute('y'));
        if (isNaN(tx) || isNaN(ty)) return;
        var d = Math.pow(tx - x, 2) + Math.pow(ty - y, 2);
        if (d < bestD) { bestD = d; best = t; }
      });
      if (!best) return;
      var name = (best.textContent || '').trim();
      if (!name || /Tampa/.test(name)) return;
      var isIntl = intl.some(function (p) {
        return Math.abs(p.x - x) < 12 && Math.abs(p.y - y) < 12;
      });
      if (cities.some(function (c2) { return c2.name === name; })) return;
      cities.push({ name: name, intl: isIntl });
    });
    if (!cities.length) return;

    var domestic = cities.filter(function (c) { return !c.intl; });
    var international = cities.filter(function (c) { return c.intl; });

    var el = document.createElement('div');
    el.setAttribute('data-mobile-network', '');
    el.style.display = 'none';

    function group(label, list) {
      if (!list.length) return '';
      var names = list.map(function (c) { return c.name; }).join('  \u00b7  ');
      return '<p style="color:#5B7085;font-size:12px;letter-spacing:1px;' +
             'text-transform:uppercase;margin:0 0 8px;">' + label +
             ' <span style="color:#A9832F;">' + list.length + '</span></p>' +
             '<p style="color:#47586B;font-size:15px;font-weight:300;line-height:1.6;' +
             'margin:0 0 22px;padding-left:14px;' +
             'border-left:1px solid rgba(11,33,56,0.16);">' + names + '</p>';
    }

    el.innerHTML =
      '<div style="padding:4px 0 8px;">' +
        '<p style="position:relative;padding-left:26px;margin:0 0 6px;color:#0B2138;' +
          'font-size:17px;font-weight:500;">' +
          '<span style="position:absolute;left:0;top:5px;width:13px;height:13px;' +
            'border-radius:50%;background:#A9832F;"></span>' +
          'Tampa, FL</p>' +
        '<p style="color:#5B7085;font-size:13px;font-weight:300;margin:0 0 24px;' +
          'padding-left:26px;">Headquarters. Every route below runs through here.</p>' +
        group('Domestic routing', domestic) +
        group('International', international) +
      '</div>';

    wrap.insertBefore(el, svg.nextSibling);

    var mq = window.matchMedia('(max-width: 760px)');
    function apply() {
      var small = mq.matches;
      svg.style.display = small ? 'none' : 'block';
      el.style.display = small ? 'block' : 'none';
    }
    if (mq.addEventListener) mq.addEventListener('change', apply);
    else if (mq.addListener) mq.addListener(apply);
    apply();
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
      'color:#5B7085;font-size:11px;letter-spacing:0.6px;';
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
    initMap();
    initTimeline();
    initChain();
    honourHash();
    // Second pass for anything that lands after first paint (images resolving,
    // late layout). Both functions are idempotent.
    setTimeout(function () { tagBlocks(); armReveals(); initMap(); initTimeline(); initChain(); honourHash(); }, 900);
  }

  if (document.readyState === 'complete') {
    init();
  } else {
    window.addEventListener('load', init);
    // Fallback in case a stalled subresource delays the load event.
    setTimeout(init, 2500);
  }
})();
