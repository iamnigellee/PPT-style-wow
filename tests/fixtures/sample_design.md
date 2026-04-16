# Design System Inspired by Stripe

## 1. Visual Theme & Atmosphere

Stripe's website feels simultaneously technical and luxurious. The signature move is weight-300 sohne-var headlines at 48-56px — an ethereal lightness that commands attention by refusing to shout. The atmosphere is "engineered warmth."

### Design Decision Rules

- **Emphasis:** Reduce weight rather than increase it. Lightness signals confidence.
- **Depth:** Every elevated element must cast a blue-tinted, multi-layer shadow.
- **Color allocation:** Purple means interactive. Non-clickable elements stay neutral.
- **Density:** Generous spacing — 64px between sections, 24px inside cards.
- **Edge treatment:** Rounded corners at 12px default, 16px for cards.
- **Typography contrast:** Headlines at weight 300, body at weight 400. Never use bold for headings.

**Key Characteristics:**
- Ultra-light headline weight (300)
- Deep navy (#0a2540) backgrounds
- Blue-violet (#533afd) for interactive elements
- Multi-layer shadows with blue tint

## 2. Color Palette & Roles

### Primary
- **Stripe Purple** (`#533afd`): Primary brand color, CTA backgrounds, link text.
- **Deep Navy** (`#0a2540`): Primary heading color, hero backgrounds.

### Accent Colors
- **Cyan Glow** (`#00d4ff`): Data highlights, secondary accents.

### Neutral Scale
- **Slate** (`#425466`): Body text color.
- **Light Gray** (`#f6f9fc`): Page background.

### Surface & Borders
- **Card White** (`#ffffff`): Card backgrounds.
- **Border Gray** (`#e3e8ee`): Dividers and borders.

## 3. Typography Rules

### Font Family
- **Heading:** sohne-var, system-ui, sans-serif
- **Body:** sohne, system-ui, sans-serif

### Type Scale
| Purpose | Size | Weight | Line Height |
|---------|------|--------|-------------|
| Display | 56px | 300 | 1.1 |
| H1 | 48px | 300 | 1.15 |
| H2 | 36px | 400 | 1.2 |
| Body | 17px | 400 | 1.65 |
| Caption | 14px | 400 | 1.5 |

## 4. Component Stylings

### Buttons
- Primary: fill #533afd, text white, radius 8px
- Secondary: outline 1px #533afd, text #533afd, radius 8px

### Cards
- Background: #ffffff, border: 1px #e3e8ee, radius: 12px
- Shadow: 0 2px 4px rgba(0,0,0,0.05)

### Icons
- Style: outlined, mono-weight, 24px default size
- Color: inherit from parent text or #425466 neutral

## 5. Layout Principles

- Max content width: 1080px centered
- Section spacing: 64px vertical
- Grid: 12-column with 24px gutters

## 6. Depth & Elevation

| Level | Shadow | Use |
|-------|--------|-----|
| Level 0 | none | Flat content |
| Level 1 | 0 2px 4px rgba(6,24,44,0.04) | Cards at rest |
| Level 2 | 0 4px 8px rgba(6,24,44,0.06) | Cards on hover |

## 7. Do's and Don'ts

### Do's
- Use weight 300 for display text
- Let whitespace do the work
- Keep interactive elements purple

### Don'ts
- Never use bold (700+) for headlines
- Never apply purple to non-interactive elements
- Avoid busy backgrounds or patterns

## 8. Responsive Behavior

- Desktop (1440px+): full 12-column grid
- Tablet (768-1439px): 8-column grid
- Mobile (< 768px): single column

## 9. Agent Prompt Guide

### Example Prompts
1. "Build a pricing card that follows the Stripe design system"
2. "Create a hero section with deep navy background"
3. "Design a feature comparison table"

### Iteration Guide
- Check Decision Rules before choosing colors
- Purple is earned — only interactive elements get it
