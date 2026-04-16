# DESIGN.md Format Specification

This is the canonical structure for a DESIGN.md file. It follows the Google Stitch / VoltAgent awesome-design-md convention. Every section below is **required**, in **this exact order**, with **exactly this heading text** (the `N.` numbering is part of the heading).

> **Voice rule, above everything else:** A DESIGN.md is an argument about why a brand looks the way it does, supported by tokens. If a section contains only tables and bullet points with no interpretive prose, that section is unfinished.

---

## Title

First line of the file:

```markdown
# Design System Inspired by <Brand Name>
```

Use the brand's own capitalisation. Do not add a subtitle.

---

## Section 1 — Visual Theme & Atmosphere

**Purpose:** Set up the interpretive frame for the entire document. This is the section the reader (human or agent) skims to understand *what kind of thing* they are looking at before diving into tokens.

**Required content:**

- **2–4 paragraphs** of prose. Not bullets. Not tables.
- Name the **signature move** — the one thing that, if you removed it, the brand would no longer look like itself. (Stripe example: weight-300 sohne-var with `ss01`. Linear example: the fog-gray gradient background. Notion example: the hand-set serif.)
- Name the **atmosphere** — a single adjective or short phrase that captures the mood. "Engineered warmth." "Twilight precision." "Editorial calm."
- Identify at least one **anti-convention** — something the brand does that most competitors don't. This is almost always the most interesting sentence in the whole document.

**End with a "Key Characteristics" bullet list** of 6–10 one-line observations, each ending with a specific token value where relevant.

**Voice example (from Stripe):**

> Stripe's website is the gold standard of fintech design — a system that manages to feel simultaneously technical and luxurious, precise and warm. […] At display sizes (48px-56px), sohne-var runs at weight 300 — an extraordinarily light weight for headlines that creates an ethereal, almost whispered authority. This is the opposite of the "bold hero headline" convention; Stripe's headlines feel like they don't need to shout.

Notice: names the exact token (weight 300, 48-56px), names the convention being violated ("bold hero headline"), and uses a metaphor ("whispered authority") — all in two sentences.

### Design Decision Rules

**Purpose:** Tokens tell the agent *what values to use*. Decision Rules tell the agent *how to think* when building a new component, layout, or interaction that isn't explicitly covered by the tokens above. This is what makes a design system reproducible — not the color palette, but the reasoning behind every choice.

**Required: 6–10 rules.** Each rule must:

1. Name a **design dimension** (emphasis, spacing, depth, color usage, density, edge treatment, hierarchy, motion, etc.)
2. State the brand's **default bias** on that dimension — the choice the agent should make when two options are both plausible.
3. Explain **why** — connect the bias to the brand's identity, not just "because the source does it."

**Format:** Each rule is a single-paragraph bullet. Lead with the dimension name in bold.

**Voice example (from Stripe):**

> - **Emphasis:** When choosing how to make an element stand out, reduce weight rather than increase it. This brand treats lightness as confidence — a weight-300 headline at 56px commands more attention than a bold one because it signals "I don't need to shout." Apply this to any new heading, label, or call-out.
> - **Depth:** Every elevated element must cast a blue-tinted, multi-layer shadow. If you're adding a new floating component (tooltip, dropdown, sheet), default to the Level 3 formula and adjust the Y-offset. Never use a single-layer neutral shadow — that belongs to a different design language.
> - **Color allocation:** Purple means interactive. If the element is not clickable, tappable, or selectable, it does not get purple. When you need a new accent for a non-interactive purpose, derive it from the navy-to-slate neutral range, not from the purple.

Notice: each rule is actionable for a **new, unseen component**. An agent reading these rules can build a toast notification, a data table, or a settings panel that feels on-brand — even though none of those components exist in the token catalogue.

**The litmus test:** If you swap the color palette in your Decision Rules and they still make sense for a different brand, the rules are too generic. "Use consistent spacing" is useless. "Default to generous spacing — 64px between sections, 24px inside cards — because this brand uses whitespace as a luxury signal, not as filler" is useful.

---

## Section 2 — Color Palette & Roles

**Purpose:** Every color the agent will use, with a semantic name and a functional role. Hex codes alone are worthless — the value is in *why* each color exists.

**Required structure:** Subsections grouped by function. Use these group names (omit any that are empty):

- **Primary** — the 2–3 colors that anchor the brand
- **Brand & Dark** — deep backgrounds, immersive sections, dark surfaces
- **Accent Colors** — colors used for decoration, gradients, highlights
- **Interactive** — link, hover, active, selected, focus variants
- **Neutral Scale** — heading, label, body, caption, disabled text colors
- **Status** — success, warning, error, info (if the source uses them)
- **Surface & Borders** — backgrounds, dividers, card borders
- **Shadow Colors** — every shadow color extracted, with alpha

**For each color, write a single line in this format:**

```markdown
- **Semantic Name** (`#hexcode`): One-sentence role description. [Optional: `--css-var-name` if the source exposes it.]
```

**Voice example:**

> - **Stripe Purple** (`#533afd`): Primary brand color, CTA backgrounds, link text, interactive highlights. A saturated blue-violet that anchors the entire system.
> - **Deep Navy** (`#061b31`): `--hds-color-heading-solid`. Primary heading color. Not black, not gray — a very dark blue that adds warmth and depth to text.

The phrase "not black, not gray" is doing real work. It tells the agent what the color is **not**, which is often more useful than what it is.

---

## Section 3 — Typography Rules

**Purpose:** Exhaustive type hierarchy with enough precision that an agent can reproduce any text style without guessing.

**Required subsections:**

### Font Family

List primary and fallback. Name any mono companion. List any OpenType features that are enabled globally (e.g. `ss01`, `tnum`, `cv02`). Call out variable-font axes if used.

### Hierarchy

A table with these columns (omit columns that don't apply to the source):

| Role | Font | Size | Weight | Line Height | Letter Spacing | Features | Notes |

Role names should be semantic and consistent: **Display Hero, Display Large, Section Heading, Sub-heading Large, Sub-heading, Body Large, Body, Button, Link, Caption, Micro, Nano, Code Body, Code Label**. Not every source uses all of them — include only the ones that exist.

Sizes in both `px` and `rem`. Weight as an integer. Line height as a decimal (not `150%`). Letter spacing in px, with sign.

### Principles

3–6 prose bullets explaining the *ideas* behind the hierarchy. This is where you name choices that would otherwise feel arbitrary — e.g. "weight 300 as signature", "progressive tracking tightens with size", "tabular numerals for financial data only".

---

## Section 4 — Component Stylings

**Purpose:** A small catalogue of the most common UI pieces, each with a complete set of tokens and at least one state variant.

**Required components (include all that exist in the source):**

- **Buttons** — primary, ghost/outlined, tertiary/info, disabled, destructive. For each: background, text, padding, radius, font size/weight/family, border, hover state, use case.
- **Cards & Containers** — background, border, radius, shadow(s), hover behavior
- **Badges / Tags / Pills** — neutral, success, warning, error, info variants
- **Inputs & Forms** — border, radius, focus ring, label color, text color, placeholder color, error state
- **Navigation** — container, link style, CTA placement, backdrop behavior, mobile toggle
- **Decorative Elements** — dashed borders, gradient accents, brand-immersion sections, illustration patterns

Use **bold component sub-headings** (not h3) within each category to name variants, followed by bullet lists of exact tokens. See the exemplar.

---

## Section 5 — Layout Principles

**Purpose:** Spacing scale, grid system, and whitespace philosophy.

**Required subsections:**

- **Spacing System** — base unit, full scale, notable irregularities
- **Grid & Container** — max content width, hero strategy, feature section pattern, full-width section treatment
- **Whitespace Philosophy** — 2–3 prose sentences about *how* the brand uses empty space (dense vs generous, rhythmic vs uniform, etc.)
- **Border Radius Scale** — every distinct radius the source uses, from micro to large, with use cases

---

## Section 6 — Depth & Elevation

**Purpose:** Everything about z-axis layering — shadows, surface hierarchy, focus rings.

**Required content:**

- A **table** of elevation levels (Level 0 flat → Level 4 deep/modal), each with its full shadow formula and typical use
- A **Shadow Philosophy** paragraph — 4–6 sentences. This is often the most distinctive technical section in a brand's system. Name the choice (tinted? neutral? multi-layer? spread? inset?) and say why it matters.
- If the source uses decorative depth (gradient overlays, backdrop-filter blur, immersive brand sections), document it in a short subsection

---

## Section 7 — Do's and Don'ts

**Purpose:** Behavioural guardrails. This is where the agent learns what the brand *refuses* to do.

**Required structure:**

### Do

6–10 bullets. Each should name a specific token or rule. Generic advice ("use consistent spacing") is forbidden.

### Don't

6–10 bullets. Each should name a specific thing the brand does **not** do, ideally contrasting with a common convention. These are the most brand-specific lines in the whole document.

**Voice example:**

> - Don't use weight 600-700 for sohne-var headlines — weight 300 is the brand voice
> - Don't use the magenta/ruby accents for buttons or links — they're decorative/gradient only

Each don't explicitly forbids a plausible agent mistake.

---

## Section 8 — Responsive Behavior

**Purpose:** How the system behaves at different widths.

**Required subsections:**

- **Breakpoints** — table with Name, Width range, Key changes
- **Touch Targets** — minimum sizes for buttons, links, controls on mobile
- **Collapsing Strategy** — hero scaling, nav collapse, grid degradation, typography scale compression, section spacing reduction
- **Image Behavior** — how illustrations, screenshots, code blocks adapt

---

## Section 9 — Agent Prompt Guide

**Purpose:** A quick-copy section designed specifically for AI agents generating UI. This is what gets pasted into other prompts.

**Required structure:**

### Quick Color Reference

A flat bullet list of the 8–12 most-used colors, each as `Role: Name (hex)`. No subsections, no rationale — this is a lookup table.

### Example Component Prompts

**At least 3, ideally 5** ready-to-use prompts an agent can paste verbatim. Each should be one long sentence specifying tokens for a specific component (hero, card, badge, nav, dark section). Use the voice of a designer briefing an implementer.

### Iteration Guide

A numbered list of 6–10 rules an agent should keep in mind while generating. These compress the whole document into a checklist — think of them as the "if you only read one section, read this" summary.

**The Iteration Guide must include at least 3 rules derived from the Design Decision Rules in Section 1** — not restated as token values, but as decision-making principles. These are the rules that let an agent build a component that isn't in the catalogue and still have it feel on-brand.

---

## Genericness Test (enforced)

Before delivering the DESIGN.md, apply these three checks. If any fails, the document is not done.

1. **Palette swap test.** Mentally replace every color in the document with a different palette. Read Section 1 and the Design Decision Rules again. If they still sound correct for the swapped palette, the identity description is too generic — it's describing tokens, not the design's soul. Rewrite until the prose would be *wrong* for a different color scheme.

2. **Blind component test.** Imagine an agent that has only read Section 1 (including the Decision Rules) and Section 9 — no token tables, no component catalogue. Could it build a toast notification, a settings panel, or a pricing table that a designer would recognise as belonging to this brand? If not, the Decision Rules are too vague.

3. **Twin test.** Compare your output against the Stripe exemplar (`reference/example-stripe.md`). If the two documents feel interchangeable once you swap the brand name and colors, something is wrong. The structure should be the same; the *voice*, *rules*, and *identity* must be different.

---

## Formatting rules (enforced)

- Use `#` h1 only for the file title, `##` h2 for the 9 sections, `###` h3 for subsections inside a section.
- Hex codes always lowercase and always in backticks: `` `#533afd` ``.
- CSS variable names in backticks with the leading double-dash: `` `--hds-color-heading-solid` ``.
- Em-dash (`—`) for interruption, not double-hyphen.
- No emoji. No screenshots or image links. No tables of contents. No conclusion section.
