// Chrome DevTools MCP / Playwright evaluate_script payload.
//
// Usage from a skill: pass the BODY of this IIFE as the `function` arg to
// `mcp__plugin_chrome-devtools-mcp_chrome-devtools__evaluate_script`.
// (Chrome DevTools MCP wants an arrow function; Playwright MCP wants a
// function body. Both work — just strip or keep the outer wrapper.)
//
// Returns a JSON-serializable snapshot of the page's visual tokens:
//   - cssVars:  key/value map of --custom-property values from :root / html rules
//   - samples:  computed style snapshot for representative element roles
//   - colors:   up to 80 unique color strings observed in the first ~2000 elements
//   - fonts:    up to 20 unique font-family stacks
//   - shadows:  up to 20 unique non-none box-shadows
//   - radii:    up to 20 unique non-zero border-radii
//   - title/url/viewport: bookkeeping
//
// The snapshot is designed to be digested by the LLM, not post-processed by code.
// It is intentionally noisy — the LLM decides which tokens matter.

(() => {
  // ---------- 1. CSS custom properties on :root / html ----------
  const cssVars = {};
  for (const sheet of Array.from(document.styleSheets)) {
    let rules;
    try { rules = sheet.cssRules; } catch (_) { continue; } // cross-origin
    if (!rules) continue;
    for (const rule of Array.from(rules)) {
      if (!rule.selectorText) continue;
      const sel = rule.selectorText;
      if (sel === ':root' || sel === 'html' || sel === '*' || sel.includes(':root')) {
        for (let i = 0; i < rule.style.length; i++) {
          const prop = rule.style[i];
          if (prop && prop.startsWith('--')) {
            cssVars[prop] = rule.style.getPropertyValue(prop).trim();
          }
        }
      }
    }
  }

  // ---------- 2. Computed-style snapshot of representative elements ----------
  const ROLES = {
    body: 'body',
    h1: 'h1',
    h2: 'h2',
    h3: 'h3',
    h4: 'h4',
    p: 'p',
    small: 'small, .caption, figcaption',
    link: 'a[href]',
    button_primary:
      'button[class*="primary"], a[class*="primary"], [class*="btn-primary"], button',
    button_secondary:
      'button[class*="secondary"], button[class*="ghost"], button[class*="outline"]',
    input: 'input[type="text"], input[type="email"], input:not([type="checkbox"]):not([type="radio"]), textarea',
    card: '[class*="card"], article, section > div',
    nav: 'nav, header',
    code: 'code, pre',
  };

  const PROPS = [
    'color', 'backgroundColor', 'backgroundImage',
    'fontFamily', 'fontSize', 'fontWeight', 'fontStyle',
    'lineHeight', 'letterSpacing', 'textTransform',
    'fontFeatureSettings', 'fontVariationSettings',
    'padding', 'margin', 'gap',
    'borderRadius', 'border', 'borderColor', 'borderWidth',
    'boxShadow', 'backdropFilter', 'filter',
    'display', 'textAlign',
  ];

  const snapshot = (el) => {
    const s = getComputedStyle(el);
    const out = {};
    for (const p of PROPS) out[p] = s[p];
    return out;
  };

  const samples = {};
  for (const [role, selector] of Object.entries(ROLES)) {
    const el = document.querySelector(selector);
    if (el) samples[role] = snapshot(el);
  }

  // ---------- 3. Frequency survey across the first 2000 elements ----------
  const colors = new Set();
  const backgrounds = new Set();
  const fonts = new Set();
  const shadows = new Set();
  const radii = new Set();
  const fontSizes = new Set();
  const fontWeights = new Set();

  const nodes = document.querySelectorAll('body *');
  const limit = Math.min(nodes.length, 2000);
  for (let i = 0; i < limit; i++) {
    const el = nodes[i];
    if (!(el instanceof Element)) continue;
    const s = getComputedStyle(el);
    if (s.color) colors.add(s.color);
    if (s.backgroundColor && s.backgroundColor !== 'rgba(0, 0, 0, 0)') {
      backgrounds.add(s.backgroundColor);
    }
    if (s.borderTopColor && parseFloat(s.borderTopWidth) > 0) {
      colors.add(s.borderTopColor);
    }
    if (s.fontFamily) fonts.add(s.fontFamily);
    if (s.boxShadow && s.boxShadow !== 'none') shadows.add(s.boxShadow);
    if (s.borderRadius && s.borderRadius !== '0px') radii.add(s.borderRadius);
    if (s.fontSize) fontSizes.add(s.fontSize);
    if (s.fontWeight) fontWeights.add(s.fontWeight);
  }

  const take = (set, n) => Array.from(set).slice(0, n);

  // ---------- 4. Fonts actually loaded by the page ----------
  const loadedFonts = [];
  if (document.fonts && document.fonts.forEach) {
    document.fonts.forEach((f) => {
      loadedFonts.push({
        family: f.family,
        weight: f.weight,
        style: f.style,
        status: f.status,
      });
    });
  }

  // ---------- 5. Return the full snapshot ----------
  return {
    url: location.href,
    title: document.title,
    viewport: { w: innerWidth, h: innerHeight, dpr: devicePixelRatio },
    cssVars,
    samples,
    colors: take(colors, 80),
    backgrounds: take(backgrounds, 40),
    fonts: take(fonts, 20),
    shadows: take(shadows, 20),
    radii: take(radii, 20),
    fontSizes: take(fontSizes, 40),
    fontWeights: take(fontWeights, 20),
    loadedFonts: loadedFonts.slice(0, 30),
  };
})();
