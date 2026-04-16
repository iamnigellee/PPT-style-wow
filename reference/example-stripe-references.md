# Style References — Stripe

## 1. Design Lineage

Stripe descends from the **Swiss International Typographic Style** — the tradition that produced Helvetica, Massimo Vignelli's Unimark International wayfinding systems, and Josef Müller-Brockmann's concert posters. The emphasis on gridded precision, generous whitespace, and typographic hierarchy as the primary design tool all trace directly to this lineage. The secondary influence is **contemporary luxury editorial design** — the kind of type-first, image-sparse layouts found in Monocle magazine or Wallpaper*.

But Stripe inverts the Swiss formula's most recognizable trait. Where classic Swiss design uses bold Akzidenz-Grotesk or Helvetica at high weights to command authority, Stripe runs its custom sohne-var at weight 300 — the lightest credible weight for display type. This is a deliberate rejection of typographic loudness: authority through restraint, not force. The blue-tinted shadow system has no historical analogue in print-era Swiss design — it's a digital-native innovation that treats the z-axis as a brand surface, extending the navy-violet palette into the space between elements.

What Stripe preserves from the tradition: the grid as invisible infrastructure, the conviction that whitespace is not empty but active, and the belief that a type system alone can carry an entire visual identity. What it discards: bold weight as the default voice, neutral-gray shadows, and the Swiss tendency toward monochrome. What it adds: chromatic depth (brand-colored shadows), a single-accent color philosophy (purple as interaction signal), and the light-dark section rhythm that creates narrative pacing in a scrollable medium.

## 2. Peer References

### Clerk
- **URL:** clerk.com
- **Shared DNA:** Same "color as signal" philosophy — a single brand accent (Clerk uses a violet-blue) reserved exclusively for interactive elements, with everything else in a navy-to-gray neutral range. Same emphasis-through-lightness approach to typography, with light font weights for headlines.
- **Key difference:** Clerk uses a higher border-radius vocabulary (12–16px on cards and buttons), giving it a softer, more approachable feel. Stripe's conservative 4–8px radius reads as financial-grade precision.

### Raycast
- **URL:** raycast.com
- **Shared DNA:** Shares the multi-layer shadow philosophy — Raycast also uses two-layer shadows with a branded tint (purple-shifted) for elevated elements, creating depth that feels colored rather than neutral.
- **Key difference:** Raycast's dark sections are the default, not an alternating rhythm. Stripe's light-dark section alternation creates a reading cadence; Raycast is immersive dark throughout, closer to Linear's approach.

### Liveblocks
- **URL:** liveblocks.io
- **Shared DNA:** Same generous whitespace strategy — sections are separated by large gaps (64px+), chrome breathes around dense technical content. Same typography approach: lightweight sans-serif headlines that command through size and tracking, not weight.
- **Key difference:** Liveblocks uses more illustrative elements and gradient decorations in its content areas. Stripe confines gradients and decorative color (ruby/magenta) to specific accent moments; the core content zone is text-and-whitespace only.

### WorkOS
- **URL:** workos.com
- **Shared DNA:** Near-identical color allocation strategy — a single purple accent for CTAs and interactive states, deep navy for headings, slate-gray for body text. The same "purple means clickable" rule applies across both systems.
- **Key difference:** WorkOS uses visible, heavy borders on components (1–2px solid) while Stripe uses subtle `#e5edf5` hairlines. WorkOS's edges are structural; Stripe's are atmospheric.

## 3. Anti-References

- **Notion:** Stripe rejects Notion's content-density-first approach. Where Notion packs maximum information into every viewport — tight 1.3 line-heights, minimal section gaps, inline controls everywhere — Stripe uses whitespace as a luxury signal. Sections breathe with 64px+ gaps, and the chrome around technical content is always more generous than the content itself. Stripe's philosophy: the empty space IS the design.

- **Vercel:** Stripe rejects Vercel's monochrome shadow philosophy. Where Vercel uses pure-black shadows at very low alpha (essentially invisible depth), Stripe's shadows are branded — blue-tinted `rgba(50,50,93,0.25)`, multi-layered, and deliberately visible. For Stripe, depth is not neutral infrastructure; it's brand expression. If you can't see the shadow's color, it's not a Stripe shadow.

- **Tailwind UI:** Stripe rejects Tailwind UI's "bold headlines, generous padding, large radius" component aesthetic. Tailwind's components default to weight 600–700 headings, 12–16px radius, and bright saturated colors for status. Stripe uses weight 300, 4–8px radius, and desaturated navy tones. The entire posture is different: Tailwind UI is friendly and approachable; Stripe is authoritative and refined.

## 4. Extended Component Gallery

### Notification Toast

**Context:** Transient feedback after a user action — payment confirmed, API key copied, webhook configured. Appears bottom-right of viewport.

**Structure:** Horizontal bar with icon (left), message (center), dismiss button (right). Single line for short messages; wraps to two lines max.

**Token specification:**
- Background: Pure White (`#ffffff`)
- Border: `1px solid #e5edf5` (Border Default)
- Shadow: Level 3 — `rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px`
- Radius: 6px (Comfortable)
- Status icon: 16px, color matches status — Success Green (`#15be53`), Ruby (`#ea2261`) for error, Stripe Purple (`#533afd`) for info
- Message: 14px sohne-var weight 400, `"ss01"`, color Deep Navy (`#061b31`)
- Dismiss: 16px ghost icon button, Body (`#64748d`), hover background `rgba(83,58,253,0.05)`
- Padding: 12px 16px
- Max width: 400px
- Gap between icon and text: 12px
- Animation: slide-up 200ms ease-out, auto-dismiss fade-out after 5s

**Why it looks this way:** The blue-tinted Level 3 shadow (Depth rule) gives the toast branded presence instead of a generic drop shadow. Weight 400 for the message text because it's UI feedback, not reading content (Emphasis rule). The dismiss button follows the interactive-state philosophy — hover adds a subtle purple tint, doesn't change base color.

### Pricing Table

**Context:** Plan comparison for Stripe's payment products. 3–4 column layout comparing feature tiers.

**Structure:** Horizontal card row. Each card is a vertical stack: plan name, price, feature list, CTA button. The recommended plan gets a Stripe Purple top border accent.

**Token specification:**
- Card background: Pure White (`#ffffff`)
- Card border: `1px solid #e5edf5`
- Card shadow: Level 2 — `rgba(23,23,23,0.08) 0px 15px 35px`
- Card radius: 6px (Comfortable)
- Recommended card: adds `3px solid #533afd` top border, shadow upgrades to Level 3
- Plan name: 14px sohne-var weight 400, `"ss01"`, Label (`#273951`), uppercase, letter-spacing +0.5px
- Price: 48px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`), letter-spacing -0.96px
- Price period: 14px weight 300, Body (`#64748d`), inline after price
- Feature list: 14px weight 300, `"ss01"`, Body (`#64748d`), 12px vertical gap between items
- Feature check icon: 14px, Success Green (`#15be53`)
- Feature missing icon: 14px, `#c4cdd5` (dimmed border gray)
- CTA (recommended): Primary Purple button — `#533afd` bg, white text, 4px radius
- CTA (other tiers): Ghost button — transparent bg, `#533afd` text, `1px solid #b9b9f9`, 4px radius
- Card padding: 32px
- Card gap: 24px
- Section background: Pure White with 96px top/bottom padding

**Why it looks this way:** Price at weight 300 / 48px follows the Emphasis rule — large and light, not large and bold. The recommended card earns the only purple accent (Color allocation rule — purple = interactive signal, and the top border is a directional signal). Shadow elevation separates the recommended card from peers, following the Depth rule's multi-layer branded approach.

### Data Table

**Context:** Transaction history, API log, or webhook event list. Paginated, sortable columns.

**Structure:** Full-width table with sticky header row, alternating row shading, pagination controls at bottom.

**Token specification:**
- Container background: Pure White (`#ffffff`)
- Container border: `1px solid #e5edf5`
- Container radius: 6px
- Container shadow: Level 1 — `rgba(23,23,23,0.06) 0px 3px 6px`
- Header row: background `#f6f9fc`, border-bottom `1px solid #e5edf5`
- Header text: 12px sohne-var weight 400, `"ss01"`, Label (`#273951`), uppercase, letter-spacing +0.5px
- Body text: 14px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`)
- Secondary text: 14px weight 300, Body (`#64748d`)
- Numeric columns: 14px weight 300, `"tnum"` (tabular numerals), right-aligned
- Row height: 48px (comfortable click target)
- Row hover: background `rgba(83,58,253,0.02)` — barely-visible purple tint
- Row border: `1px solid #f0f4f8` between rows
- Selected row: background `rgba(83,58,253,0.05)`, left border `3px solid #533afd`
- Pagination: 14px weight 400, Body (`#64748d`), active page uses Stripe Purple
- Sort indicator: 10px arrow icon, Stripe Purple when active, Body when inactive

**Why it looks this way:** Numeric data uses `"tnum"` (Typography rule — tabular numerals for financial data only). Row hover uses a purple tint at nearly-invisible alpha (Interactive state philosophy — hover "presses into" the brand color, doesn't highlight). Header is uppercase with positive letter-spacing, inverting the negative-tracking display convention for small utility text.

### Settings Panel

**Context:** Account configuration — profile, billing, API keys, team permissions. Sidebar-plus-content layout.

**Structure:** Left sidebar with section nav links, right content area with form groups. Each form group has a heading, description, and input controls.

**Token specification:**
- Page background: `#f6f9fc` (lightest surface)
- Sidebar background: Pure White (`#ffffff`)
- Sidebar border-right: `1px solid #e5edf5`
- Sidebar width: 240px
- Sidebar link: 14px sohne-var weight 400, `"ss01"`, Body (`#64748d`)
- Sidebar link active: Deep Navy (`#061b31`), left border `3px solid #533afd`, background `rgba(83,58,253,0.03)`
- Content card background: Pure White (`#ffffff`)
- Content card border: `1px solid #e5edf5`
- Content card radius: 6px
- Content card shadow: Level 1 — `rgba(23,23,23,0.06) 0px 3px 6px`
- Content card padding: 32px
- Group heading: 18px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`)
- Group description: 14px weight 300, Body (`#64748d`), margin-bottom 16px
- Label: 14px weight 400, Label (`#273951`)
- Input: 14px weight 300, Deep Navy (`#061b31`), border `1px solid #e5edf5`, radius 4px, padding 8px 12px, focus `1px solid #533afd`
- Save button: Primary Purple (per DESIGN.md Section 4)
- Cancel button: Ghost (per DESIGN.md Section 4)
- Destructive action: text `#ea2261` (Ruby), no button background, hover background `rgba(234,34,97,0.05)`

**Why it looks this way:** Group headings at weight 300 / 18px — still light, still the brand voice (Emphasis rule). The active sidebar link gets the only purple accent in the navigation (Color allocation rule). Destructive actions use Ruby but as text-only with hover tint, not as a filled button — restraint in expressing danger, matching the overall whispered-authority personality.

### Empty State

**Context:** Zero-data screen — no transactions yet, no API keys created, no webhooks configured.

**Structure:** Vertically centered in the content area. Icon or illustration above, heading, description, primary action button.

**Token specification:**
- Container: no visible boundary, centered in available space
- Icon: 48px, outline style, Body (`#64748d`), stroke width 1.5px
- Heading: 22px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`), letter-spacing -0.22px
- Description: 16px weight 300, `"ss01"`, Body (`#64748d`), max-width 400px, text-align center, line-height 1.4
- CTA button: Primary Purple (per DESIGN.md Section 4)
- Secondary link: 14px weight 400, Stripe Purple (`#533afd`), no underline, hover underline
- Spacing: 16px icon→heading, 8px heading→description, 24px description→CTA
- Vertical padding: 96px top and bottom (generous, following the spacing rule)

**Why it looks this way:** The 96px vertical padding is the Spacing rule in action — even an empty state gets the luxury treatment. The heading stays at weight 300 (Emphasis rule), and the only purple element is the CTA button (Color allocation rule). The description uses a 400px max-width to maintain comfortable line length, respecting the same reading rhythm as the main site.

### Login Form

**Context:** Developer sign-in to the Stripe Dashboard.

**Structure:** Centered card on a light background. Logo above, email/password fields, primary submit button, secondary links below.

**Token specification:**
- Page background: `#f6f9fc`
- Card background: Pure White (`#ffffff`)
- Card border: `1px solid #e5edf5`
- Card shadow: Level 3 — `rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px`
- Card radius: 6px
- Card width: 400px
- Card padding: 40px
- Logo: Stripe wordmark, 32px height, centered
- Heading: 22px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`), text-align center
- Label: 14px weight 400, `"ss01"`, Label (`#273951`)
- Input: per DESIGN.md Section 4 (Inputs & Forms)
- Input gap: 16px between fields
- Submit: full-width Primary Purple button, 48px height
- "Forgot password": 14px weight 400, Stripe Purple (`#533afd`), text-align right above password field
- "Sign up" link: 14px weight 400, Body (`#64748d`), with Stripe Purple link text
- Divider: `1px solid #e5edf5` with centered "or" text in 12px Body
- Social login: Ghost button style, full width, icon left-aligned

**Why it looks this way:** The login card uses Level 3 shadow — the same branded depth as feature cards (Depth rule). It's the most elevated element on a minimal page, making it the clear focal point. The 40px padding is generous for a form (Spacing rule). The heading "Sign in to Stripe" uses weight 300, consistent with every other heading in the system.

### Modal Dialog

**Context:** Confirmation before destructive actions — delete API key, cancel subscription, remove team member.

**Structure:** Centered overlay card with backdrop blur. Icon, heading, description, two-button action row.

**Token specification:**
- Backdrop: `rgba(6,27,49,0.5)` — Deep Navy at 50% alpha, brand-tinted overlay
- Card background: Pure White (`#ffffff`)
- Card shadow: Level 4 — `rgba(3,3,39,0.25) 0px 14px 21px -14px, rgba(0,0,0,0.1) 0px 8px 17px -8px`
- Card radius: 8px (Large — modals get the most generous radius in the system)
- Card width: 480px
- Card padding: 32px
- Warning icon: 24px, Ruby (`#ea2261`) for destructive, Stripe Purple for neutral
- Heading: 18px sohne-var weight 300, `"ss01"`, Deep Navy (`#061b31`)
- Description: 16px weight 300, `"ss01"`, Body (`#64748d`), line-height 1.4
- Action row: right-aligned, 12px gap between buttons
- Cancel: Ghost button
- Confirm (destructive): `#ea2261` background, white text, 4px radius, hover `#d41d55`
- Confirm (neutral): Primary Purple button
- Spacing: 16px icon→heading, 8px heading→description, 24px description→actions
- Animation: backdrop fade-in 150ms, card scale-up from 95% with 200ms ease-out

**Why it looks this way:** The backdrop uses Deep Navy tint, not neutral black — even the overlay is on-brand (Color allocation rule extended to non-interactive elements, but only structural ones). The card uses Level 4 shadow, the deepest in the system, because modals demand the highest elevation (Depth rule). Destructive confirmation is the ONLY context where a non-purple colored button appears — Ruby earns a filled button because the visual weight signals irreversibility.

### Command Palette

**Context:** Quick-action search overlay, triggered by `Cmd+K`. Search input with filtered results list.

**Structure:** Centered overlay card (no backdrop tint — this is a utility, not a blocking modal). Search input at top, scrollable results list below, keyboard hints at bottom.

**Token specification:**
- Card background: Pure White (`#ffffff`)
- Card border: `1px solid #e5edf5`
- Card shadow: Level 4 — `rgba(3,3,39,0.25) 0px 14px 21px -14px, rgba(0,0,0,0.1) 0px 8px 17px -8px`
- Card radius: 8px
- Card width: 560px
- Card max-height: 400px
- Search input: 18px sohne-var weight 300, `"ss01"`, Deep Navy, no border, padding 16px 20px, placeholder Body (`#64748d`)
- Search icon: 18px, Body (`#64748d`), left of input
- Divider below input: `1px solid #e5edf5`
- Result item: 14px weight 400, Deep Navy, padding 10px 20px
- Result item hover: background `rgba(83,58,253,0.03)`, left border `2px solid #533afd`
- Result item icon: 16px, Body (`#64748d`)
- Result item shortcut: 12px SourceCodePro weight 500, Body (`#64748d`), right-aligned, `#f0f4f8` pill background, 4px radius
- Selected result: background `rgba(83,58,253,0.05)`
- Footer hint bar: 12px weight 400, Body (`#64748d`), border-top `1px solid #e5edf5`, padding 8px 20px

**Why it looks this way:** Search input uses the Display-weight approach — 18px weight 300, because the search query IS the primary content of this component (Emphasis rule). Result hover uses the near-invisible purple tint (Interactive state philosophy). Keyboard shortcuts use SourceCodePro in pills, consistent with the mono companion pattern from DESIGN.md.

## 5. Style Vocabulary

### Visual Adjectives
Luminous, engineered, restrained, twilight-precise, premium, weightless, confident, architectural, clean-edged, typographically-driven

### Texture & Material Metaphors
Brushed titanium with a violet tint. Silk-weight paper under museum lighting. Frosted glass at blue hour. A financial report typeset by a luxury magazine art director. Polished concrete with embedded sapphire.

### Spatial & Motion Descriptors
Generous breathing room. Vertical float — elements hover rather than sit. Parallax depth via multi-layer shadows. Slow, confident transitions (200ms ease-out). Whitespace as active, not empty. Rhythmic light-dark pacing.

### Negative Keywords
Loud, playful, dense, organic, textured, hand-drawn, brutalist, neon, chunky, rounded, bubbly, warm-toned, casual, sketchy

## 6. Cross-Medium Application Guide

### Email / Newsletter
- **Preserve:** Deep Navy headings (`#061b31`), Stripe Purple CTA buttons, generous vertical spacing between content blocks, the light-dark section rhythm (alternate white and dark navy background rows).
- **Adapt:** Replace sohne-var with the fallback stack (`SF Pro Display`, `-apple-system`, `Helvetica Neue`). Weight 300 may not render reliably in email clients — use weight 400 but keep sizes large (24px+ for headings) to maintain the "light and confident" feel through size rather than weight. Simplify shadows to `border: 1px solid #e5edf5` since email clients strip box-shadow.
- **Drop:** Multi-layer blue-tinted shadows (not supported). Negative letter-spacing (inconsistent support). OpenType `"ss01"` features (not supported). Ghost/outlined buttons (border rendering is unreliable — use solid purple CTAs only).

### Presentation Deck
- **Preserve:** Weight 300 sohne-var for all headings (install the font). Deep Navy text on white backgrounds. The single-accent purple for highlights, data callouts, and key figures. Blue-tinted background for "dark slide" moments.
- **Adapt:** Increase minimum body text to 18px (projection readability). Use `#1c1e54` (Brand Dark) backgrounds for emphasis slides instead of the full section-rhythm alternation. Simplify the shadow system to a single subtle drop shadow on floating elements. Charts use the ruby/magenta accent palette for data series, not the purple (purple is reserved for callouts).
- **Drop:** Letter-spacing precision (PowerPoint/Keynote tracking controls are too coarse). Responsive behavior. Component hover states. The 4px border-radius (presentation elements are typically unrounded or use larger radius).

### Documentation Site
- **Preserve:** sohne-var with `"ss01"`, weight 300 for page titles and section headings, weight 400 for body text. Deep Navy headings, slate body text. SourceCodePro for all code blocks with `"tnum"` for numeric examples. Purple for links and interactive elements only.
- **Adapt:** Increase body line-height to 1.6 (reading-optimised, up from 1.4). Add a sidebar navigation in Pure White with `#e5edf5` right border. Compress heading scale: page title at 32px, section at 24px, sub-section at 18px (the 48–56px display sizes are too large for documentation). Use Level 1 shadow for code blocks instead of Level 3 (code blocks are reference material, not feature showcases). Add a subtle `#f6f9fc` background for inline code.
- **Drop:** The 56px Display Hero size (too large for documentation). Dark navy (`#1c1e54`) immersive sections (these are for marketing, not reference material). Ruby/magenta decorative accents (documentation should be purple-and-neutral only).
