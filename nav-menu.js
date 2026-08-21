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

  var GROUPS = [
    { label: 'Technology lifecycle', items: [
      ['How it works', '/platform'],
      ['Secure data destruction', '/secure-itad'],
      ['Asset value recovery', '#'],
      ['Global logistics', '#'],
      ['Chain-of-custody ERP', '/platform']
    ]},
    { label: 'Recycling', items: [
      ['Electronics recycling', '/electronics-recycling'],
      ['Paladin Local', '/paladin-local'],
      ['Wind turbine & energy assets', '/critical-materials'],
      ['Metallurgical lab', '#']
    ]},
    { label: 'Critical materials', items: [
      ['REcapture magnet recovery', '/critical-materials'],
      ['Neodymium & dysprosium', '/critical-materials'],
      ['Domestic feedstock programs', '#'],
      ['CMR joint venture', '#']
    ]},
    { label: 'Platform companies', items: [
      ['IRT', '#'],
      ['R&L Recycling B.V.', '#'],
      ['CMR', '#'],
      ['Daeheung', '#'],
      ['R2 / RIOS certificates by site', '/network']
    ]}
  ];

  // One flat lookup so an existing panel can be reconciled by link text.
  var TARGETS = {};
  GROUPS.forEach(function (g) {
    g.items.forEach(function (it) { TARGETS[it[0].toLowerCase()] = it[1]; });
  });

  var PANEL_ID = 'pal-mega';

  function esc(t) {
    return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function panelHTML() {
    var cols = GROUPS.map(function (g) {
      var links = g.items.map(function (it) {
        return '<a href="' + it[1] + '" style="color:#FFFFFF;font-size:15px;font-weight:300;' +
               'text-decoration:none;">' + esc(it[0]) + '</a>';
      }).join('');
      return '<div style="display:flex;flex-direction:column;gap:12px;">' +
             '<span style="font-size:13px;letter-spacing:1px;text-transform:uppercase;' +
             'color:#8FA6BA;">' + esc(g.label) + '</span>' + links + '</div>';
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
      if (TARGETS[key]) a.setAttribute('href', TARGETS[key]);
    });
  }

  function platformItem(header) {
    var nav = header.querySelector('nav');
    if (!nav) return null;
    var candidates = nav.querySelectorAll('a, button');
    for (var i = 0; i < candidates.length; i++) {
      var t = (candidates[i].textContent || '').trim().toLowerCase();
      if (t === 'platform' || t.indexOf('platform') === 0) return candidates[i];
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

    var existing = existingPanel(header);
    if (existing) {
      reconcile(existing);
      return true; // homepage: template owns the menu
    }

    if (document.getElementById(PANEL_ID)) return true;

    var item = platformItem(header);
    if (!item) return false;

    var panel = document.createElement('div');
    panel.id = PANEL_ID;
    panel.style.cssText = 'display:none;background:#14304C;' +
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
