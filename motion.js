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
    var settle = function () {
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
  function bands() {
    var node = document.body.querySelector('div');
    var guard = 0;
    while (node && node.children.length === 1 && guard++ < 5) node = node.children[0];
    return node ? Array.prototype.slice.call(node.children) : [];
  }

  function taggable(el) {
    if (el.hasAttribute('data-reveal') || el.hasAttribute('data-mreveal')) return false;
    if (el.hasAttribute('data-stagger') || el.hasAttribute('data-countup')) return false;
    var tag = el.tagName.toLowerCase();
    if (tag === 'header' || tag === 'footer' || tag === 'script' || tag === 'style') return false;
    if (el.closest('header') || el.closest('footer')) return false;
    return safe(el);
  }

  function tagBlocks() {
    var tagged = 0;

    bands().forEach(function (band) {
      var r = band.getBoundingClientRect();

      // Whole-band reveal for bands the page runtime does not already own.
      // Uses the same treatment as the built-in runtime so pages that mix
      // both read as one system.
      if (r.height >= 80 && taggable(band)) {
        band.setAttribute('data-mreveal', '');
        band.setAttribute('data-mdelay', '0');
        tagged++;
      }

      // Inside every band, stagger rows of sibling cards, stats or columns.
      // This is the part that makes components arrive one after another
      // rather than the whole band popping in at once.
      if (band.tagName.toLowerCase() === 'header' || band.tagName.toLowerCase() === 'footer') return;
      band.querySelectorAll('div').forEach(function (row) {
        var cs = getComputedStyle(row);
        if (cs.display !== 'grid' && cs.display !== 'flex') return;
        var kids = Array.prototype.slice.call(row.children).filter(function (k) {
          return k.getBoundingClientRect().height > 48;
        });
        if (kids.length < 2 || kids.length > 8) return;
        // Only rows that lay out side by side; a stacked flex column is
        // usually a text block, not a set of components.
        var tops = kids.map(function (k) { return Math.round(k.getBoundingClientRect().top); });
        if (new Set(tops).size === kids.length) return;
        var i = 0;
        kids.forEach(function (k) {
          if (!taggable(k)) return;
          k.setAttribute('data-mreveal', '');
          k.setAttribute('data-mdelay', String(90 + Math.min(i, 5) * 90));
          i++;
          tagged++;
        });
      });
    });

    return tagged;
  }

  function armReveals() {
    var els = document.querySelectorAll('[data-mreveal]');
    if (!els.length) return;
    els.forEach(function (el) {
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

    var start = null, DUR = 1500;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min(1, (ts - start) / DUR);
      var eased = 1 - Math.pow(1 - p, 3);
      circle.setAttribute('r', String(eased * MAX_R));
      var reached = eased * MAX_R;
      cities.forEach(function (c) {
        if (c.el.style.opacity === '0' && reached > c.d - 10) c.el.style.opacity = '1';
      });
      if (p < 1) {
        requestAnimationFrame(frame);
      } else {
        // Drop the clip once complete so a later React re-render that removes
        // the injected defs can never leave the routes clipped to nothing.
        routes.removeAttribute('clip-path');
        cities.forEach(function (c) { c.el.style.opacity = '1'; });
      }
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.disconnect();
        requestAnimationFrame(frame);
      });
    }, { threshold: 0.25 });
    io.observe(svg);
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
      return '<p style="color:#8FA6BA;font-size:12px;letter-spacing:1px;' +
             'text-transform:uppercase;margin:0 0 8px;">' + label +
             ' <span style="color:#A9832F;">' + list.length + '</span></p>' +
             '<p style="color:#DDE3E9;font-size:15px;font-weight:300;line-height:1.6;' +
             'margin:0 0 22px;padding-left:14px;' +
             'border-left:1px solid rgba(255,255,255,0.16);">' + names + '</p>';
    }

    el.innerHTML =
      '<div style="padding:4px 0 8px;">' +
        '<p style="position:relative;padding-left:26px;margin:0 0 6px;color:#FFFFFF;' +
          'font-size:17px;font-weight:500;">' +
          '<span style="position:absolute;left:0;top:5px;width:13px;height:13px;' +
            'border-radius:50%;background:#A9832F;"></span>' +
          'Tampa, FL</p>' +
        '<p style="color:#7F93A6;font-size:13px;font-weight:300;margin:0 0 24px;' +
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

  // The page is React-rendered, so wait for content before measuring.
  var tries = 0;
  function init() {
    // While the access gate is up, the page is laid out but hidden. Intersection
    // observers would fire behind it and spend every reveal before the visitor
    // ever sees the page, so wait until the gate has been cleared.
    if (document.documentElement.classList.contains('pal-locked')) {
      return setTimeout(init, 120);
    }
    if (!document.querySelector('footer') && tries++ < 60) {
      return requestAnimationFrame(init);
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
    initMap();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
