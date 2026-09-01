/* Platform mega menu
   ------------------
   The homepage template builds this menu itself, bound to that page's React
   state. No other page has it, so on every interior page "Platform" was a
   plain link and the menu was unreachable.

   Rather than paste the panel into thirteen templates, where it would drift
   the moment the menu changed, this builds it from one definition:

     - Pages that already have a panel (the homepage) keep theirs, and only
       have their link targets reconciled against the map below.
     - Every other page gets the panel injected and its Platform nav item
       wired up as a toggle.

   The menu only takes over the Platform item at widths where the desktop nav
   is actually on screen. Below that the nav collapses into the hamburger
   drawer, where Platform stays a normal link. */

(function () {
  'use strict';

  /* Only items with a page of their own are links. The rest render as plain
     text, dimmed and not clickable, so the menu never promises a destination
     that does not exist. Three items previously pointed at an approximate page
     (Chain-of-custody ERP and Neodymium & dysprosium at pages that cover them
     only as a section) and now sit inactive until they have one. Give an item
     a URL here and it becomes a link everywhere at once. */
  var GROUPS = [
    { label: 'Technology lifecycle', items: [
      ['How it works', '/platform'],
      ['Secure data destruction', '/secure-itad'],
      ['Asset value recovery', null],
      ['Global logistics', null],
      ['Chain-of-custody ERP', null]
    ]},
    { label: 'Recycling', items: [
      ['Electronics recycling', '/electronics-recycling'],
      ['Regional coverage', '/paladin-local'],
      ['Wind turbine & energy assets', null],
      ['Metallurgical lab', null]
    ]},
    { label: 'Critical materials', items: [
      ['REcapture magnet recovery', '/critical-materials'],
      ['Neodymium & dysprosium', null],
      ['Domestic feedstock programs', null],
      ['CMR joint venture', null]
    ]},
    { label: 'Platform companies', items: [
      ['IRT', null],
      ['R&L Recycling B.V.', null],
      ['CMR', null],
      ['Daeheung', null],
      ['R2 / RIOS certificates by site', '/network']
    ]}
  ];

  // One flat lookup so an existing panel can be reconciled by link text.
  var TARGETS = {};
  GROUPS.forEach(function (g) {
    g.items.forEach(function (it) { TARGETS[it[0].toLowerCase()] = it[1]; });
  });

  var INACTIVE = 'color:#8CA0B3;font-size:15px;font-weight:300;cursor:default;';
  var ACTIVE = 'color:#FFFFFF;font-size:15px;font-weight:300;text-decoration:none;';

  var PANEL_ID = 'pal-mega';

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }


  /* The panel is built here rather than living in the markup, so its hover
     has to be a real stylesheet rule. Inline styles cannot express :hover.
     Matches the footer, where links go to gold-400. */

  /* Logo hover: the gold lockup sits behind the white one as a background and
     is revealed by fading the white image out. Same artwork, same pixel
     dimensions, so nothing shifts. Swapping the src instead would flash on
     first hover while the second file downloads. */
  function ensureLogoHover() {
    if (!document.getElementById('pal-logo-hover')) {
      var st = document.createElement('style');
      st.id = 'pal-logo-hover';
      st.textContent =
        '.pal-logo-link { display: inline-block; position: relative; ' +
          'background-image: url("/assets/paladin-lockup-gold.440d6b2f.webp"); ' +
          'background-size: contain; background-repeat: no-repeat; ' +
          'background-position: left center; }' +
        '.pal-logo-link img[data-logo] { transition: opacity 180ms cubic-bezier(0.2,0.7,0.1,1); }' +
        '.pal-logo-link:hover img[data-logo] { opacity: 0; }' +
        '@media (prefers-reduced-motion: reduce) { .pal-logo-link img[data-logo] { transition: none; } }';
      document.head.appendChild(st);
    }
    // Class the parent link rather than relying on :has(), whose support is
    // still uneven and which would fail silently.
    document.querySelectorAll('img[data-logo]').forEach(function (img) {
      var a = img.closest('a');
      if (a) a.classList.add('pal-logo-link');
    });
  }

  function ensureHoverRule() {
    if (document.getElementById('pal-mega-style')) return;
    var st = document.createElement('style');
    st.id = 'pal-mega-style';
    st.textContent =
      '.pal-mega-panel a { transition: color 180ms cubic-bezier(0.2,0.7,0.1,1); }' +
      '.pal-mega-panel a:hover { color: #D9A441 !important; }' +
      'header nav a, header nav button { transition: color 180ms cubic-bezier(0.2,0.7,0.1,1), border-color 200ms; }' +
      'header nav a:hover, header nav button:hover { color: #D9A441 !important; }';
    document.head.appendChild(st);
  }

  function panelHTML() {
    var cols = GROUPS.map(function (g) {
      var links = g.items.map(function (it) {
        if (!it[1]) {
          return '<span style="' + INACTIVE + '" title="Page not built yet">' +
                 esc(it[0]) + '</span>';
        }
        return '<a href="' + it[1] + '" style="' + ACTIVE + '">' + esc(it[0]) + '</a>';
      }).join('');
      return '<div style="display:flex;flex-direction:column;gap:12px;">' +
             '<span style="font-size:13px;letter-spacing:1px;text-transform:uppercase;' +
             'color:#8CA0B3;">' + esc(g.label) + '</span>' + links + '</div>';
    }).join('');
    return '<div style="max-width:1600px;margin:0 auto;padding:40px clamp(24px,5vw,72px) 44px;' +
           'display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));' +
           'gap:40px;">' + cols + '</div>';
  }

  // Does this page's template already ship the menu?
  function existingPanel(header) {
    var spans = header.querySelectorAll('span');
    for (var i = 0; i < spans.length; i++) {
      if ((spans[i].textContent || '').trim() === 'Technology lifecycle') {
        var node = spans[i];
        while (node && node.parentElement !== header) node = node.parentElement;
        return node;
      }
    }
    return null;
  }

  // Keep every panel's targets in step with the map above, including the
  // homepage's own, so the two versions cannot say different things.
  function reconcile(panel) {
    panel.querySelectorAll('a').forEach(function (a) {
      var key = (a.textContent || '').trim().toLowerCase();
      if (!(key in TARGETS)) return;
      var target = TARGETS[key];
      if (target) {
        a.setAttribute('href', target);
        return;
      }
      // No page yet: swap the anchor for inert text so it cannot be clicked.
      var span = document.createElement('span');
      span.textContent = a.textContent;
      span.setAttribute('style', INACTIVE);
      span.title = 'Page not built yet';
      a.parentNode.replaceChild(span, a);
    });
  }

  function platformItem(header) {
    var nav = header.querySelector('nav');
    if (!nav) return null;
    var candidates = nav.querySelectorAll('a, button');
    // Match on the destination first. The label has already been renamed once,
    // from "Platform" to "One system", and matching on text meant the menu
    // silently stopped appearing on twelve pages.
    for (var i = 0; i < candidates.length; i++) {
      if (candidates[i].getAttribute('href') === '/platform') return candidates[i];
    }
    for (var i = 0; i < candidates.length; i++) {
      var t = (candidates[i].textContent || '').trim().toLowerCase();
      if (t === 'one system' || t.indexOf('one system') === 0 || t.indexOf('platform') === 0) {
        return candidates[i];
      }
    }
    return null;
  }

  function drawerMode(nav) {
    // The hamburger drawer positions the nav absolutely; the desktop bar does not.
    return getComputedStyle(nav).position === 'absolute';
  }

  function setup() {
    var header = document.querySelector('header');
    if (!header) return false;
    var nav = header.querySelector('nav');
    if (!nav) return false;

    ensureHoverRule();
    ensureLogoHover();
    var existing = existingPanel(header);
    if (existing) {
      existing.classList.add('pal-mega-panel');
      reconcile(existing);
      return true; // homepage: template owns the menu
    }

    if (document.getElementById(PANEL_ID)) return true;

    var item = platformItem(header);
    if (!item) return false;

    var panel = document.createElement('div');
    panel.id = PANEL_ID;
    panel.className = 'pal-mega-panel';
    panel.style.cssText = 'display:none;background:#12293F;' +
      'border-top:1px solid rgba(255,255,255,0.16);';
    panel.innerHTML = panelHTML();
    header.appendChild(panel);

    // Caret, matching the homepage's affordance.
    var caret = document.createElement('span');
    caret.textContent = ' +';
    caret.setAttribute('aria-hidden', 'true');
    caret.style.cssText = 'margin-left:4px;';
    item.appendChild(caret);

    item.setAttribute('aria-expanded', 'false');
    item.setAttribute('aria-controls', PANEL_ID);

    var open = false;
    function setOpen(next) {
      open = next;
      panel.style.display = open ? 'block' : 'none';
      item.setAttribute('aria-expanded', open ? 'true' : 'false');
      caret.textContent = open ? ' \u2013' : ' +';
    }

    item.addEventListener('click', function (e) {
      // In drawer mode Platform stays a plain link to the overview page.
      if (drawerMode(nav)) return;
      e.preventDefault();
      setOpen(!open);
    });

    // Close on Escape, on outside click, and once a destination is chosen.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && open) setOpen(false);
    });
    document.addEventListener('click', function (e) {
      if (!open) return;
      if (item.contains(e.target)) return;
      if (!panel.contains(e.target)) setOpen(false);
    });
    panel.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (open && drawerMode(nav)) setOpen(false);
    });

    return true;
  }

  var tries = 0;
  function init() {
    // Wait for the gate, then for the React-rendered header.
    if (document.documentElement.classList.contains('pal-locked')) {
      return setTimeout(init, 120);
    }
    if (!setup() && tries++ < 200) setTimeout(init, 60);
  }

  if (document.readyState === 'complete') {
    init();
  } else {
    window.addEventListener('load', init);
    setTimeout(init, 2500);
  }
})();
