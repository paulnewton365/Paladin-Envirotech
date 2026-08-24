/* Access gate
   -----------
   Puts a password screen in front of the prototype so a link can be shared
   with a client without it being openly browsable.

   READ THIS BEFORE RELYING ON IT
   This is a front-end gate. It keeps casual visitors and search engines out.
   It is NOT security. The page HTML ships to the browser either way, so anyone
   who opens developer tools, disables JavaScript, or requests a page directly
   can read the content without passing the gate. Do not put anything
   confidential behind it. For real protection use Vercel's Password
   Protection, which runs at the edge before any content is served.

   TO CHANGE THE PASSWORD
   Store the SHA-256 hash, not the password. Generate one with:
     node -e "console.log(require('crypto').createHash('sha256').update('YOUR PASSWORD').digest('hex'))"
   or in a browser console:
     crypto.subtle.digest('SHA-256', new TextEncoder().encode('YOUR PASSWORD'))
       .then(b => console.log([...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')))

   SHARE LINKS
   Appending ?client=<ACCESS_TOKEN> unlocks without typing the password, so a
   single link can be pasted into an email. The token is remembered afterwards.
*/

(function () {
  'use strict';

  // SHA-256 of "Paladin2026". Change both of these before sharing.
  var PASSWORD_HASH = 'ed9eba37f409c0b0347174f48da48a5d98ef68938f368a3b93159c4f8b11e60a';
  var ACCESS_TOKEN = 'b3zG4SPI8DiZEsLv';

  // Palette and metrics measured from the Conscious Compass gate.
  var CREAM = '#F0EEE7';
  var INK = '#0E0E0E';
  var MUTED = '#5D5A51';
  var DISABLED = '#C5C5C5';
  var COLUMN = 620;
  var FONT = '-apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, Helvetica, Arial, sans-serif';

  var STORE_KEY = 'paladin-prototype-access';
  var LOCK_CLASS = 'pal-locked';

  function stored() {
    try { return window.localStorage.getItem(STORE_KEY); } catch (e) { return null; }
  }
  function remember() {
    try { window.localStorage.setItem(STORE_KEY, ACCESS_TOKEN); } catch (e) {}
  }

  function tokenInUrl() {
    var m = window.location.search.match(/[?&]client=([^&]+)/);
    return m ? decodeURIComponent(m[1]) : null;
  }

  if (stored() === ACCESS_TOKEN || tokenInUrl() === ACCESS_TOKEN) {
    if (tokenInUrl() === ACCESS_TOKEN) remember();
    return;
  }

  // Lock immediately, while the document is still parsing, so no page content
  // is ever painted behind the gate.
  var lockStyle = document.createElement('style');
  lockStyle.textContent =
    'html.' + LOCK_CLASS + ' { overflow: hidden !important; }' +
    'html.' + LOCK_CLASS + ' body > *:not(#pal-gate) { visibility: hidden !important; }' +
    '#pal-gate input::placeholder { color: #9A968C; opacity: 1; }';
  (document.head || document.documentElement).appendChild(lockStyle);
  document.documentElement.classList.add(LOCK_CLASS);

  function sha256Hex(text) {
    if (!window.crypto || !window.crypto.subtle) return Promise.resolve(null);
    return window.crypto.subtle
      .digest('SHA-256', new TextEncoder().encode(text))
      .then(function (buf) {
        return Array.prototype.map
          .call(new Uint8Array(buf), function (b) { return b.toString(16).padStart(2, '0'); })
          .join('');
      });
  }

  function unlock() {
    remember();
    document.documentElement.classList.remove(LOCK_CLASS);
    var gate = document.getElementById('pal-gate');
    if (gate) {
      gate.style.opacity = '0';
      setTimeout(function () { if (gate.parentNode) gate.parentNode.removeChild(gate); }, 320);
    }
    // The page measured its layout while the gate was covering it.
    window.dispatchEvent(new Event('resize'));
  }

  function build() {
    if (document.getElementById('pal-gate')) return;

    var gate = document.createElement('div');
    gate.id = 'pal-gate';
    gate.style.cssText = [
      'position:fixed', 'inset:0', 'z-index:99999',
      'background:' + CREAM,
      'display:flex', 'align-items:center', 'justify-content:center',
      'padding:32px 24px', 'overflow-y:auto',
      'font-family:' + FONT,
      'transition:opacity 300ms ease'
    ].join(';');

    gate.innerHTML =
      '<div style="width:100%;max-width:' + COLUMN + 'px;">' +
        '<div id="pal-gate-logo" style="height:30px;margin:0 0 34px;"></div>' +
        '<h1 id="pal-gate-head" style="color:' + INK + ';line-height:0.98;font-size:56px;' +
          'font-weight:700;letter-spacing:-0.022em;margin:0 0 38px;">' +
          '<span style="display:block;white-space:nowrap;">Consequential brands</span>' +
          '<span style="display:block;white-space:nowrap;">are conscious brands</span></h1>' +
        '<div style="background:#FFFFFF;padding:24px;">' +
          '<h2 style="color:' + INK + ';font-size:20px;line-height:1.25;font-weight:700;' +
            'letter-spacing:-0.01em;margin:0 0 6px;">Paladin Envirotech</h2>' +
          '<p style="color:' + MUTED + ';font-size:14px;line-height:1.45;' +
            'margin:0 0 22px;">Website prototype. Enter the password you were given ' +
            'to access.</p>' +
          '<label for="pal-gate-input" style="position:absolute;width:1px;height:1px;' +
            'overflow:hidden;clip:rect(0 0 0 0);">Password</label>' +
          '<input id="pal-gate-input" type="password" autocomplete="current-password" ' +
            'placeholder="Password" style="width:100%;box-sizing:border-box;' +
            'background:' + CREAM + ';border:1px solid ' + INK + ';border-radius:0;' +
            'color:' + INK + ';font-family:inherit;font-size:15px;' +
            'padding:13px 14px;outline:none;-webkit-appearance:none;">' +
          '<p id="pal-gate-error" role="alert" aria-live="polite" style="color:#B4382E;' +
            'font-size:13px;margin:0;height:0;overflow:hidden;opacity:0;' +
            'transition:opacity 160ms ease;">That password was not recognised.</p>' +
          '<button id="pal-gate-submit" type="button" disabled style="margin-top:13px;' +
            'width:100%;padding:13px 20px;border:0;border-radius:0;cursor:not-allowed;' +
            'font-family:inherit;font-size:12px;font-weight:600;letter-spacing:1.4px;' +
            'text-transform:uppercase;color:#FFFFFF;background:' + DISABLED + ';' +
            'transition:background-color 180ms ease;">View prototype</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(gate);

    // Antenna logo. Prefers an SVG; falls back to the PNG in assets, then to
    // a plain wordmark if neither is present.
    var logoBox = gate.querySelector('#pal-gate-logo');
    // PNG is what ships. If vector artwork arrives later, save it over this
    // path or add it ahead of the PNG here.
    var sources = ['/assets/antenna-logo.de7012a5.png'];
    (function tryLogo(i) {
      if (i >= sources.length) {
        var fallback = document.createElement('div');
        fallback.style.cssText = 'color:' + INK + ';font-size:17px;font-weight:700;' +
          'letter-spacing:-0.01em;';
        fallback.textContent = 'antenna group';
        logoBox.appendChild(fallback);
        return;
      }
      var img = new Image();
      img.alt = 'Antenna Group';
      img.style.cssText = 'height:30px;width:auto;display:block;';
      img.onload = function () { logoBox.appendChild(img); };
      img.onerror = function () { tryLogo(i + 1); };
      img.src = sources[i];
    })(0);

    /* The reference gate sets its headline in Antenna's own typeface, which is
       not available here. Any substitute sets at a different width, so a fixed
       font-size would either wrap onto extra lines or leave the column short.
       Measure the widest line instead and scale the type so it fills the
       column, which reproduces the proportions rather than the point size. */
    var head = gate.querySelector('#pal-gate-head');
    var lines = head.querySelectorAll('span');
    function fitHeadline() {
      var column = head.parentElement.clientWidth;
      if (!column) return;
      head.style.fontSize = '100px';
      lines[0].style.whiteSpace = 'nowrap';
      lines[1].style.whiteSpace = 'nowrap';
      var widest = 0;
      Array.prototype.forEach.call(lines, function (l) {
        widest = Math.max(widest, l.scrollWidth);
      });
      if (!widest) return;
      var size = Math.floor(100 * (column * 0.985) / widest);
      if (size > 62) size = 62;
      if (size < 24) {
        // Narrow screens: let the lines wrap rather than shrink to nothing.
        size = 24;
        lines[0].style.whiteSpace = 'normal';
        lines[1].style.whiteSpace = 'normal';
      }
      head.style.fontSize = size + 'px';
    }
    fitHeadline();
    window.addEventListener('resize', fitHeadline);

    var input = gate.querySelector('#pal-gate-input');
    var error = gate.querySelector('#pal-gate-error');
    var submit = gate.querySelector('#pal-gate-submit');

    function setEnabled(on) {
      submit.disabled = !on;
      submit.style.background = on ? INK : DISABLED;
      submit.style.cursor = on ? 'pointer' : 'not-allowed';
    }

    input.addEventListener('input', function () {
      setEnabled(!!input.value);
      error.style.opacity = '0';
      error.style.height = '0';
      error.style.margin = '0';
    });

    function attempt() {
      var value = input.value || '';
      if (!value) return;
      sha256Hex(value).then(function (hex) {
        if (hex === PASSWORD_HASH) {
          unlock();
        } else {
          error.style.opacity = '1';
          error.style.height = 'auto';
          error.style.margin = '8px 0 0';
          input.value = '';
          setEnabled(false);
          input.focus();
        }
      });
    }

    submit.addEventListener('click', attempt);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); attempt(); }
    });

    setTimeout(function () { input.focus(); }, 60);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
