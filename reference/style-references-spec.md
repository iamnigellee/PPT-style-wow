# STYLE-REFERENCES.md Format Specification

This is the canonical structure for a STYLE-REFERENCES.md file — a companion to DESIGN.md that provides concrete, tangible design references to help agents and designers extend the brand's visual language into new contexts.

> **Purpose distinction:** DESIGN.md is the *contract* (what tokens to use, what rules to follow). STYLE-REFERENCES.md is the *gallery* (what the style looks like in practice, where it comes from, and how it extends). An agent reading both should be able to build any component — not just the ones catalogued — and have it feel unmistakably on-brand.

---

## Title

First line of the file:

```markdown
# Style References — <Brand Name>
```

---

## Section 1 — Design Lineage

**Purpose:** Anchor the brand in a design tradition. Knowing *where a style comes from* helps agents and designers make intuitive decisions — if you know a system descends from Swiss typography, you can infer preferences for grid alignment, whitespace, and geometric type even when the DESIGN.md doesn't explicitly cover a scenario.

**Required content:**

- **Design school or movement** — Name the primary tradition (Swiss International Typographic Style, Editorial Design, Brutalism, Material Design, Scandinavian Minimalism, Art Deco, Bauhaus, Japanese Zen, Skeuomorphism, Flat Design, Neomorphism, Glassmorphism, etc.). Most brands blend 2–3; name the dominant one and the secondary influences.
- **Key historical references** — 2–3 specific designers, studios, or canonical works that represent the tradition this brand draws from. Not "inspired by Apple" — go deeper. (e.g., "Massimo Vignelli's Unimark International grid systems", "Dieter Rams' Braun product language", "Josef Müller-Brockmann's poster work".)
- **Contemporary evolution** — One paragraph on how this brand takes the historical tradition and adapts it for the current medium (web, mobile, SaaS). What does it preserve? What does it discard? What does it add that the historical references didn't have?

**Voice example:**

> Stripe descends from the Swiss International Typographic Style — the same tradition that gave us Helvetica, the Vignelli subway map, and the entire premise that "the grid is the message." But where classic Swiss design uses bold weights and high-contrast type to command authority, Stripe inverts the formula: weight 300 at display sizes, creating authority through restraint rather than force. The blue-tinted shadow system has no historical analogue — it's a digital-native innovation that treats the z-axis as a brand surface.

---

## Section 2 — Peer References

**Purpose:** Name 3–5 real websites or products that share meaningful design DNA with this brand. These are not "similar vibes" — each must share a specific, nameable design trait.

**Required format per entry:**

```markdown
### <Brand Name>
- **URL:** <url>
- **Shared DNA:** <What specifically they share — name the design dimension (depth philosophy, type strategy, color allocation, spacing rhythm, etc.)>
- **Key difference:** <What diverges — this prevents agents from conflating the two>
```

**Rules:**
- At least 3 entries, no more than 5.
- Each "Shared DNA" line must reference a specific Design Decision Rule from the DESIGN.md, not a generic trait like "both use sans-serif fonts."
- Each "Key difference" line must name a concrete divergence, not "different colors."
- Prefer referencing well-known, publicly accessible websites that the agent or user can actually visit.

**Voice example:**

> ### Linear
> - **URL:** linear.app
> - **Shared DNA:** Same "color as signal" philosophy — indigo is hoarded for interactive elements, everything else is neutral. Same approach to emphasis through restraint rather than boldness.
> - **Key difference:** Linear uses near-invisible shadows (alpha 0.01–0.08) while Stripe uses prominently tinted multi-layer shadows. Stripe's depth is visible and branded; Linear's depth is felt but unseen.

---

## Section 3 — Anti-References

**Purpose:** Show what the brand is *not*. Contrast sharpens understanding faster than description alone. Knowing that "this brand is NOT like Notion" immediately communicates volumes about its personality.

**Required: 2–3 entries.** Each names a well-known design system and states what specific design choice this brand rejects that the anti-reference embraces.

**Format per entry:**

```markdown
- **<Brand Name>**: <What this brand rejects from the anti-reference's approach>. <Why the rejection matters to the brand identity.>
```

**Voice example:**

> - **Notion**: Stripe rejects Notion's content-density-first approach. Where Notion packs maximum information into every viewport with tight line-heights and minimal section spacing, Stripe uses whitespace as a luxury signal — sections breathe with 64px+ gaps, and chrome is always more generous than content.
> - **Vercel**: Stripe rejects Vercel's monochrome shadow philosophy. Where Vercel uses pure-black shadows at low alpha for invisible depth, Stripe's shadows are branded — blue-tinted, multi-layered, and deliberately visible. Depth is not neutral infrastructure; it's brand expression.

---

## Section 4 — Extended Component Gallery

**Purpose:** This is the most concrete section in the entire document. It specifies 6–8 components that do NOT exist on the source website, designed by applying the Design Decision Rules from DESIGN.md. Each component is a complete recipe an agent can implement directly.

**Why this matters:** The components in DESIGN.md Section 4 are extracted from what already exists. The components HERE prove that the style can extend to new contexts. If these components feel on-brand, the Design Decision Rules are working.

**Required: 6–8 components.** Choose from this pool (prioritise components the source site does NOT have):

- Pricing table / plan comparison
- Notification toast / snackbar
- Settings panel / preference form
- Data table with sorting and pagination
- Empty state / zero-data illustration
- Login / signup form
- Dashboard summary widget / stat card
- Modal dialog / confirmation sheet
- Onboarding step wizard
- Error page (404/500)
- Testimonial / quote card
- Timeline / activity feed
- Command palette / search modal
- File upload dropzone

**Format per component:**

```markdown
### <Component Name>

**Context:** <When and where this component would appear in the brand's product.>

**Structure:**
<Describe the layout: what elements, in what arrangement, at what hierarchy level.>

**Token specification:**
<Full design spec — background, text colors, font size/weight/features, padding, border, radius, shadow, hover/focus states. Reference DESIGN.md tokens by semantic name. Derive any new values from the Design Decision Rules, noting which rule you applied.>

**Why it looks this way:**
<1–2 sentences connecting the choices back to the Design Decision Rules. This is the educational bridge — it teaches the reader how to apply the rules themselves.>
```

**Voice example (for Stripe):**

> ### Notification Toast
>
> **Context:** Transient feedback after a user action — payment confirmed, API key copied, webhook configured.
>
> **Structure:** Horizontal bar, icon left, message center, dismiss button right. Anchored to bottom-right of viewport, 24px from edges.
>
> **Token specification:**
> - Background: Pure White (`#ffffff`)
> - Border: `1px solid #e5edf5` (Border Default)
> - Shadow: Level 3 — `rgba(50,50,93,0.25) 0px 30px 45px -30px, rgba(0,0,0,0.1) 0px 18px 36px -18px` — the toast floats with branded depth
> - Radius: 6px (Comfortable)
> - Icon: 16px, color matches status — `#15be53` (success), `#ea2261` (error)
> - Message: 14px sohne-var weight 400, `"ss01"`, color Deep Navy (`#061b31`)
> - Dismiss: ghost icon button, `#64748d` (Body), hover `rgba(83,58,253,0.05)`
> - Padding: 12px 16px
> - Max width: 400px
> - Animation: slide-up 200ms ease-out, fade-out after 5s
>
> **Why it looks this way:** The blue-tinted Level 3 shadow (Depth rule) gives the toast branded presence instead of a generic drop shadow. The dismiss button uses the interactive-state philosophy — hover darkens via tint, doesn't change color. Message weight is 400 (UI text), not 300 (reading text), following the emphasis rule.

---

## Section 5 — Style Vocabulary

**Purpose:** A curated word list for prompting other AI tools — Midjourney, DALL-E, Figma AI, Galileo, or any system that takes natural-language style descriptions. These words encode the brand's feel in a way that generative tools can interpret.

**Required subsections:**

### Visual Adjectives
8–12 adjectives that capture the visual feel. Ordered from most to least defining. Each should be specific enough that two designers reading the list would converge on a similar mood.

### Texture & Material Metaphors
4–6 metaphors that describe what the design "feels like" in physical terms. These are for AI image generation and mood boards.

### Spatial & Motion Descriptors
4–6 terms describing how space and movement behave. These help with layout and animation prompting.

### Negative Keywords
4–6 words that describe what the design is NOT. Useful as negative prompts in generative tools.

**Voice example (for Stripe):**

> ### Visual Adjectives
> Luminous, engineered, restrained, precise, twilight, premium, weightless, confident, architectural, clean-edged
>
> ### Texture & Material Metaphors
> Brushed titanium with violet tint. Silk-weight paper under museum lighting. Frosted glass at blue hour. A financial report typeset by a luxury magazine.
>
> ### Spatial & Motion Descriptors
> Generous breathing room. Vertical float. Elements hover rather than sit. Parallax depth. Slow, confident transitions.
>
> ### Negative Keywords
> Loud, playful, dense, organic, textured, hand-drawn, brutalist, neon, chunky

---

## Section 6 — Cross-Medium Application Guide

**Purpose:** How the extracted style translates beyond the web page. Many brands need their style applied to email templates, mobile apps, presentation decks, documentation sites, or print materials. This section provides adaptation rules — not full specs, but directional guidance.

**Required: At least 3 of the following contexts.** Choose the most relevant ones for the brand:

- **Email / Newsletter** — How the style adapts to email rendering constraints (no custom fonts, limited CSS, table-based layout). Which tokens survive? Which need substitution?
- **Mobile App (Native)** — How the style maps to iOS/Android platform conventions. Where does brand override platform? Where does platform win?
- **Presentation Deck** — Slide layout, title treatment, background strategy, chart styling.
- **Documentation Site** — Reading-optimised adaptation. How does the type hierarchy compress for long-form content? Sidebar treatment, code block styling.
- **Print / PDF** — CMYK considerations, paper-appropriate shadows (or lack thereof), type size adjustments for physical media.

**Format per context:**

```markdown
### <Context Name>
- **Preserve:** <2–3 brand traits that must survive the adaptation>
- **Adapt:** <2–3 traits that need modification for this medium, with specific guidance>
- **Drop:** <1–2 traits that don't translate and should be omitted>
```

---

## Formatting rules (enforced)

- Use `#` h1 only for the file title, `##` h2 for the 6 sections, `###` h3 for subsections and individual entries.
- Reference DESIGN.md tokens by their semantic name (e.g., "Stripe Purple") and hex code. Do not invent new names.
- Reference Design Decision Rules by their dimension name (e.g., "the Emphasis rule", "the Depth rule").
- Hex codes always lowercase and in backticks: `` `#533afd` ``.
- Em-dash (`—`) for interruption, not double-hyphen.
- No emoji. No image links.
- URLs must be real and publicly accessible. Do not fabricate URLs.

---

## Quality bar

The document is not done if:

- Extended Component Gallery has fewer than 6 components or any component lacks a full token specification.
- Any component in the gallery could belong to a different brand without modification. Each must reference at least one Design Decision Rule that makes it brand-specific.
- Peer References use only superficial comparisons ("both are dark mode"). Each must name a specific design dimension.
- Style Vocabulary adjectives are generic ("modern", "clean", "minimalist"). Each should be specific enough to distinguish this brand from its peers.
- Cross-Medium Application section says nothing more than "use the same colors." It must address what changes and what breaks in each medium.
