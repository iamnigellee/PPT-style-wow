# PPT-style-wow Design Spec

> A Claude Code skill that extracts brand visual systems from websites/screenshots, drives native-editable PPTX generation, and evolves a reusable template library over time.

## Problem

Existing AI PPT tools either ignore visual branding (generic slides) or lock you into a platform. ppt-master solves the "native editable PPTX" problem but relies on manual style decisions. design.skill solves the "extract a brand's visual DNA" problem but stops at a DESIGN.md file. Neither connects extraction to generation.

## Solution

A unified skill with three layers: **extract** a design system, **generate** brand-consistent PPTX, and **evolve** a growing template library. Users get slides that look like they belong to a specific brand — automatically.

---

## Architecture

### Three-Layer Pipeline

```
┌─────────────────────────────────────────────────────┐
│  Layer 1: Design Extractor                          │
│  Input:  URL / screenshot / existing DESIGN.md      │
│  Output: Standardized DESIGN.md + STYLE-REFERENCES  │
│  Source: design.skill core logic + reference files   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 2: PPT Generator                             │
│  Input:  Source document + DESIGN.md                 │
│  Output: Native editable PPTX                       │
│  Source: ppt-master Strategist→Executor→Export       │
│  Key:    Strategist auto-fills from DESIGN.md tokens │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  Layer 3: Template Evolution                        │
│  Silent: Archive every DESIGN.md + metadata         │
│  Promote: User /promote → history becomes template  │
│  Match:  Tag filter + LLM semantic ranking          │
└─────────────────────────────────────────────────────┘
```

### Three Entry Points

| Entry | User says | What happens |
|-------|-----------|--------------|
| **From URL** | "用 stripe.com 的风格做 PPT" | Extract DESIGN.md → auto-fill Strategist → generate PPTX |
| **From DESIGN.md** | "用这个 DESIGN.md 生成 PPT" | Skip extraction → Strategist → generate PPTX |
| **No preference** | "帮我做个 PPT" | Analyze content → match template from library → confirm → generate |

---

## Layer 1: Design Extractor

Reuses design.skill's extraction workflow verbatim. The SKILL.md references `reference/` files for format specs, extraction scripts, and exemplars.

### Input Handling

| Input | Strategy |
|-------|----------|
| URL | Chrome DevTools MCP: navigate, run `reference/extraction.js`, screenshot. Fallback to Playwright MCP. |
| Screenshot | Vision-based extraction. Approximate tokens from rendered image. |
| URL + screenshot | DOM extraction for precise tokens; screenshot as authority on which page/state matters. |
| Existing DESIGN.md | Validate structure (9 sections present), pass through directly. |

### Output

Standard 5-file bundle written to `<project>/design/`:

```
<project>/design/
  DESIGN.md              # 9-section design system
  STYLE-REFERENCES.md    # 6-section companion
  style-board.html       # Visual reference board
  preview.html           # Light mode token demo
  preview-dark.html      # Dark mode token demo
  screenshots/           # Source + peer + anti-reference captures
```

For the "existing DESIGN.md" entry point, only DESIGN.md is required. The other files are optional.

---

## Layer 2: PPT Generator

Reuses ppt-master's full pipeline: source conversion → project init → Strategist → Executor (SVG) → post-processing → PPTX export.

### Key Modification: DESIGN.md → Strategist Bridge

The Strategist's "Eight Confirmations" are partially auto-filled from DESIGN.md tokens:

| Confirmation | Source | Auto-fill? |
|-------------|--------|------------|
| Canvas format | User preference | No — default 16:9, ask user |
| Page count | Content analysis | No — ask user |
| Target audience | User context | No — ask user |
| Style objective | DESIGN.md §1 Visual Theme & Atmosphere | Yes |
| Color scheme | DESIGN.md §2 Color Palette & Roles | Yes |
| Icon approach | DESIGN.md §4 Component Stylings + §1 Decision Rules | Yes |
| Typography plan | DESIGN.md §3 Typography Rules | Yes |
| Image strategy | DESIGN.md §7 Do's and Don'ts + §1 Decision Rules | Yes |

Result: 8 confirmations reduced to **3 user-required** (canvas, page count, audience). The remaining 5 are derived from DESIGN.md and presented for user confirmation as a bundle — user can override any.

### Bridge Implementation: `design_bridge.py`

A script that reads a DESIGN.md and outputs a partial `design_spec.md` (ppt-master's Strategist output format) with the 5 auto-filled fields populated.

```
Input:  <project>/design/DESIGN.md
Output: <project>/design_spec_prefill.json
```

The JSON contains structured data the Strategist can consume:

```json
{
  "style_objective": "Engineered warmth — light headlines, blue-violet accents, ...",
  "color_scheme": {
    "primary": "#533afd",
    "background": "#0a2540",
    "text_primary": "#425466",
    "accent": "#00d4ff",
    "semantic_names": { ... }
  },
  "typography": {
    "heading_family": "sohne-var, sans-serif",
    "body_family": "sohne, sans-serif",
    "heading_weight": 300,
    "scale": [ ... ]
  },
  "icon_approach": "Outlined mono-weight icons in neutral tones, ...",
  "image_strategy": "Full-bleed hero images with gradient overlays, ...",
  "decision_rules": [ ... ]
}
```

The Strategist reads this prefill, incorporates it into the full `design_spec.md`, and asks the user only the 3 remaining questions.

### SVG Generation Constraint

DESIGN.md Decision Rules (§1) are injected into the Executor's context as additional constraints. When generating SVG for each slide, the Executor must respect:

- Color allocation rules (which colors are interactive vs. decorative)
- Emphasis rules (weight vs. size vs. whitespace)
- Depth rules (shadow formulas, elevation system)
- Density rules (spacing philosophy)

These rules supplement ppt-master's existing SVG technical constraints (banned features, PPT compatibility, etc.).

### Scripts (from ppt-master)

All ppt-master scripts are placed under `skills/ppt-style-wow/scripts/`. The full list:

- `source_to_md/` — PDF, DOCX, PPTX, web → Markdown converters
- `project_manager.py` — Project init, validate, import sources
- `analyze_images.py` — Image analysis
- `image_gen.py` — AI image generation (multi-provider)
- `svg_quality_checker.py` — SVG quality check
- `total_md_split.py` — Speaker notes splitting
- `finalize_svg.py` — SVG post-processing
- `svg_to_pptx.py` — PPTX export

Plus new scripts:

- `design_bridge.py` — DESIGN.md → design_spec prefill
- `template_manager.py` — Template CRUD, promote, match

---

## Layer 3: Template Evolution

### Silent Collection

Every PPT generation run automatically archives:

```
history/
  <timestamp>-<slug>/
    DESIGN.md
    STYLE-REFERENCES.md    # if available
    metadata.json
    design_spec.md          # the final Strategist output
```

No user action required. This happens as part of the normal generation pipeline.

### metadata.json Structure

```json
{
  "id": "2026-04-16-stripe-q3report",
  "source_url": "https://stripe.com",
  "source_type": "url",
  "created_at": "2026-04-16T14:30:00Z",
  "content_summary": "Q3 financial performance report...",
  "tags": {
    "industry": ["fintech", "saas"],
    "style": ["minimalist", "tech"],
    "scene": ["report", "internal"]
  },
  "atmosphere": "Engineered warmth — light headlines against deep navy...",
  "decision_rules_digest": ["emphasis-by-lightness", "blue-tinted-depth", "purple-means-interactive"]
}
```

### Promote: History → Template

User command: `/promote <history-id> --name "科技极简风" --tags tech,minimalist,report`

What happens:

1. Copy `history/<id>/` → `templates/<slug>/`
2. Add `usage_count: 0` to metadata
3. User can optionally edit the DESIGN.md to refine (strip content-specific tokens, generalize)
4. Template is now available for matching

### Template Matching (No-Preference Entry)

Two-phase matching when user provides content but no style preference:

**Phase 1 — Tag filter:**
- Analyze source content → extract likely tags (industry, scene type)
- Filter templates whose tags overlap
- If 0-2 templates match, skip to Phase 2 with all templates
- If 3+ match, pass filtered set to Phase 2

**Phase 2 — LLM semantic ranking:**
- Input: content summary + each candidate template's `atmosphere` + `decision_rules_digest`
- LLM ranks by "fit" — how well the design language suits this content
- Present top 2-3 to user with reasoning

If template library is empty (cold start), fall back to ppt-master's free design mode.

---

## Directory Structure

```
PPT-style-wow/
├── SKILL.md                          # Main skill definition
├── CLAUDE.md                         # Project instructions for Claude
├── requirements.txt                  # Python dependencies
├── skills/
│   └── ppt-style-wow/
│       ├── references/               # AI role definitions (from ppt-master)
│       │   ├── strategist.md
│       │   ├── executor.md
│       │   ├── canvas-formats.md
│       │   └── shared-standards.md
│       ├── scripts/                  # All runnable scripts
│       │   ├── source_to_md/         # Content converters (from ppt-master)
│       │   ├── project_manager.py    # Project management (from ppt-master)
│       │   ├── design_bridge.py      # NEW: DESIGN.md → Strategist bridge
│       │   ├── template_manager.py   # NEW: Template CRUD + matching
│       │   ├── analyze_images.py
│       │   ├── image_gen.py
│       │   ├── svg_quality_checker.py
│       │   ├── total_md_split.py
│       │   ├── finalize_svg.py
│       │   └── svg_to_pptx.py
│       ├── templates/                # Layout + chart templates (from ppt-master)
│       │   ├── layouts/
│       │   ├── charts/
│       │   ├── icons/
│       │   └── design_spec_reference.md
│       └── workflows/
│           └── create-template.md
├── reference/                        # Design extraction references (from design.skill)
│   ├── format-spec.md
│   ├── style-references-spec.md
│   ├── extraction.js
│   ├── example-stripe.md
│   ├── example-stripe-references.md
│   ├── preview-template.html
│   └── style-board-template.html
├── history/                          # Auto-archived generation records
├── templates/                        # Promoted design templates
└── projects/                         # User project workspace
```

---

## Workflow: Full Pipeline (URL Entry)

```
1. User: "用 stripe.com 的风格，把 report.pdf 做成 PPT"

2. [Layer 1] Extract design system
   - Navigate to stripe.com via Chrome DevTools MCP
   - Run extraction.js, capture screenshots
   - Write DESIGN.md + STYLE-REFERENCES.md + previews

3. [Layer 2] Convert source & init project
   - python3 scripts/source_to_md/pdf_to_md.py report.pdf
   - python3 scripts/project_manager.py init stripe-q3 --format ppt169
   - python3 scripts/project_manager.py import-sources ... --move

4. [Layer 2] Bridge: DESIGN.md → Strategist prefill
   - python3 scripts/design_bridge.py <project>/design/DESIGN.md
   - Output: design_spec_prefill.json (5/8 confirmations filled)

5. [Layer 2] Strategist phase (3 user confirmations)
   ⛔ BLOCKING — present auto-filled spec + ask:
   - Canvas format? (default 16:9)
   - Page count range?
   - Target audience?
   
6. [Layer 2] Executor → SVG generation
   - Sequential page-by-page (ppt-master rule)
   - Decision Rules from DESIGN.md injected as constraints

7. [Layer 2] Post-processing → PPTX export
   - total_md_split.py → finalize_svg.py → svg_to_pptx.py
   - Sequential, one at a time (ppt-master rule)

8. [Layer 3] Silent archive
   - Copy DESIGN.md + metadata.json → history/<timestamp>-<slug>/
```

---

## Workflow: Template Match (No-Preference Entry)

```
1. User: "帮我把 report.pdf 做成 PPT"

2. Convert source, analyze content summary

3. [Layer 3] Template matching
   - Extract content tags (industry, scene)
   - Phase 1: tag filter on templates/*/metadata.json
   - Phase 2: LLM ranks candidates by atmosphere fit
   
4. ⛔ BLOCKING — present top 2-3 templates + free design option:
   "基于你的内容，推荐以下风格：
    A) 科技极简风 — 来自 stripe.com 提取，适合...
    B) 学术严谨风 — 来自 nature.com 提取，适合...
    C) 自由设计 — AI 根据内容自行发挥"

5. User confirms → proceed with selected template's DESIGN.md
   → same pipeline as URL entry from step 3 onward
```

---

## Workflow: Promote Template

```
1. User: "/promote 2026-04-16-stripe-q3report --name 科技极简风"

2. python3 scripts/template_manager.py promote \
     --id 2026-04-16-stripe-q3report \
     --name "科技极简风" \
     --tags tech,minimalist,report

3. Copies history entry → templates/tech-minimalist/
4. Confirms: "已将 stripe-q3report 提升为模板「科技极简风」"
```

---

## New Scripts to Build

### `design_bridge.py`

- **Input:** Path to DESIGN.md
- **Output:** `design_spec_prefill.json`
- **Logic:** Parse each section, extract structured tokens (colors as hex+name, fonts as family+weight+scale, decision rules as list). Map to ppt-master's design_spec fields.
- **Validation:** Verify DESIGN.md has all 9 required sections. Warn on missing sections but proceed with available data.
- **Font fallback:** If DESIGN.md specifies web fonts not available in PowerPoint, map to the closest system font (e.g., `sohne-var` → `Segoe UI Light`). Include both original and fallback in the prefill so the Strategist can note the substitution.

### `template_manager.py`

Subcommands:

| Command | Description |
|---------|-------------|
| `promote --id <id> --name <name> [--tags ...]` | Move history entry to templates/ |
| `list` | List all templates with tags and atmosphere summary |
| `match --content <summary> [--top N]` | Tag-filter + return candidates for LLM ranking |
| `history` | List all history entries |
| `remove --id <id>` | Remove a template |

---

## Technical Constraints (Inherited from ppt-master)

All SVG constraints from ppt-master apply without modification:

- Banned SVG features: `mask`, `<style>`, `class`, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<script>`, `<iframe>`, `<symbol>`+`<use>`
- Conditionally allowed: `marker-start`/`marker-end` (triangle/diamond/circle only), `clipPath` on `<image>` (single shape child)
- PPT compatibility: `fill-opacity`/`stroke-opacity` instead of `rgba()`, no `<g opacity>`
- Sequential page generation only, no sub-agent SVG generation
- Post-processing steps run sequentially, never batched

---

## Dependencies

- Python 3.10+
- `requirements.txt` from ppt-master (pip install)
- Chrome DevTools MCP or Playwright MCP (for URL extraction)
- Node.js 18+ (optional, fallback for WeChat sites)
- Pandoc (optional, for legacy document formats)

---

## Out of Scope (for v1)

- Multi-brand blending (combining 2+ DESIGN.md into a hybrid)
- Template sharing/marketplace
- Real-time collaboration
- Version control for templates (just overwrite for now)
- Auto-promote based on scoring (user-driven only)
