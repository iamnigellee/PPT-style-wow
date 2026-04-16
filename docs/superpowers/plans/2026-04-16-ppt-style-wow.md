# PPT-style-wow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code skill that extracts brand visual systems from websites, drives native-editable PPTX generation, and evolves a reusable template library.

**Architecture:** Three-layer pipeline — Layer 1 (Design Extractor) reuses design.skill's extraction logic, Layer 2 (PPT Generator) reuses ppt-master's SVG→PPTX pipeline with a new DESIGN.md→Strategist bridge, Layer 3 (Template Evolution) adds silent archiving, promote, and tag+LLM matching.

**Tech Stack:** Python 3.10+, Chrome DevTools MCP / Playwright MCP, ppt-master scripts (SVG→PPTX), design.skill reference files.

---

## File Structure

```
PPT-style-wow/
├── SKILL.md                              # Main skill definition (unified workflow)
├── CLAUDE.md                             # Project instructions for Claude Code
├── requirements.txt                      # Python deps (from ppt-master + new)
├── .gitignore
├── reference/                            # Design extraction refs (from design.skill)
│   ├── format-spec.md
│   ├── style-references-spec.md
│   ├── extraction.js
│   ├── example-stripe.md
│   ├── example-stripe-references.md
│   ├── preview-template.html
│   └── style-board-template.html
├── skills/
│   └── ppt-style-wow/
│       ├── references/                   # AI role definitions (from ppt-master)
│       │   ├── strategist.md             # Modified: accepts design_spec_prefill
│       │   ├── executor-base.md
│       │   ├── executor-general.md
│       │   ├── executor-consultant.md
│       │   ├── executor-consultant-top.md
│       │   ├── image-generator.md
│       │   ├── image-layout-spec.md
│       │   ├── canvas-formats.md
│       │   ├── shared-standards.md
│       │   ├── svg-image-embedding.md
│       │   └── template-designer.md
│       ├── scripts/
│       │   ├── source_to_md/             # From ppt-master (verbatim)
│       │   │   ├── pdf_to_md.py
│       │   │   ├── doc_to_md.py
│       │   │   ├── ppt_to_md.py
│       │   │   └── web_to_md.py
│       │   ├── project_manager.py        # From ppt-master (verbatim)
│       │   ├── analyze_images.py         # From ppt-master (verbatim)
│       │   ├── image_gen.py              # From ppt-master (verbatim)
│       │   ├── svg_quality_checker.py    # From ppt-master (verbatim)
│       │   ├── total_md_split.py         # From ppt-master (verbatim)
│       │   ├── finalize_svg.py           # From ppt-master (verbatim)
│       │   ├── svg_to_pptx.py            # From ppt-master (verbatim)
│       │   ├── design_bridge.py          # NEW: DESIGN.md → prefill JSON
│       │   └── template_manager.py       # NEW: promote, list, match, history
│       ├── templates/                    # From ppt-master (verbatim)
│       │   ├── layouts/
│       │   ├── charts/
│       │   ├── icons/
│       │   └── design_spec_reference.md
│       └── workflows/
│           └── create-template.md        # From ppt-master
├── history/                              # Auto-archived generation records
│   └── .gitkeep
├── templates/                            # Promoted design templates
│   └── .gitkeep
└── projects/                             # User project workspace
    └── .gitkeep
```

---

## Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `history/.gitkeep`
- Create: `templates/.gitkeep`
- Create: `projects/.gitkeep`

- [ ] **Step 1: Create .gitignore**

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
.venv/
venv/

# Environment
.env

# OS
.DS_Store
Thumbs.db

# Project workspace (user content, not tracked)
projects/*/

# History (local evolution data, not tracked)
history/*/

# Node fallback
node_modules/
```

- [ ] **Step 2: Create requirements.txt**

Clone ppt-master's requirements.txt as the base:

```bash
gh api repos/hugohe3/ppt-master/contents/requirements.txt --jq '.content' | base64 -d > requirements.txt
```

- [ ] **Step 3: Create placeholder directories**

```bash
touch history/.gitkeep templates/.gitkeep projects/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore requirements.txt history/.gitkeep templates/.gitkeep projects/.gitkeep
git commit -m "chore: project scaffolding with dependencies and directory structure"
```

---

## Task 2: Import design.skill Reference Files

**Files:**
- Create: `reference/format-spec.md`
- Create: `reference/style-references-spec.md`
- Create: `reference/extraction.js`
- Create: `reference/example-stripe.md`
- Create: `reference/example-stripe-references.md`
- Create: `reference/preview-template.html`
- Create: `reference/style-board-template.html`

- [ ] **Step 1: Clone design.skill reference directory**

```bash
mkdir -p reference
cd /tmp && git clone --depth 1 https://github.com/iamnigellee/design.skill.git
cp /tmp/design.skill/reference/* reference/
rm -rf /tmp/design.skill
```

- [ ] **Step 2: Verify all 7 reference files present**

```bash
ls reference/
```

Expected: `example-stripe-references.md`, `example-stripe.md`, `extraction.js`, `format-spec.md`, `preview-template.html`, `style-board-template.html`, `style-references-spec.md`

- [ ] **Step 3: Commit**

```bash
git add reference/
git commit -m "feat: import design.skill reference files for design extraction"
```

---

## Task 3: Import ppt-master Scripts, References, and Templates

**Files:**
- Create: `skills/ppt-style-wow/scripts/` (all scripts from ppt-master)
- Create: `skills/ppt-style-wow/references/` (all role definitions)
- Create: `skills/ppt-style-wow/templates/` (layouts, charts, icons, design_spec_reference)
- Create: `skills/ppt-style-wow/workflows/create-template.md`

- [ ] **Step 1: Clone ppt-master and copy skill contents**

```bash
cd /tmp && git clone --depth 1 https://github.com/hugohe3/ppt-master.git
mkdir -p skills/ppt-style-wow
cp -r /tmp/ppt-master/skills/ppt-master/scripts skills/ppt-style-wow/
cp -r /tmp/ppt-master/skills/ppt-master/references skills/ppt-style-wow/
cp -r /tmp/ppt-master/skills/ppt-master/templates skills/ppt-style-wow/
cp -r /tmp/ppt-master/skills/ppt-master/workflows skills/ppt-style-wow/
```

- [ ] **Step 2: Copy .env.example for image generation config**

```bash
cp /tmp/ppt-master/.env.example .env.example
rm -rf /tmp/ppt-master
```

- [ ] **Step 3: Verify directory structure**

```bash
ls skills/ppt-style-wow/scripts/
ls skills/ppt-style-wow/references/
ls skills/ppt-style-wow/templates/
```

Expected scripts: `source_to_md/`, `project_manager.py`, `analyze_images.py`, `image_gen.py`, `svg_quality_checker.py`, `total_md_split.py`, `finalize_svg.py`, `svg_to_pptx.py`, etc.

Expected references: `strategist.md`, `executor-base.md`, `executor-general.md`, `shared-standards.md`, `canvas-formats.md`, etc.

Expected templates: `layouts/`, `charts/`, `icons/`, `design_spec_reference.md`

- [ ] **Step 4: Commit**

```bash
git add skills/ .env.example
git commit -m "feat: import ppt-master scripts, references, and templates"
```

---

## Task 4: Build `design_bridge.py` (TDD)

**Files:**
- Create: `skills/ppt-style-wow/scripts/design_bridge.py`
- Create: `tests/test_design_bridge.py`
- Create: `tests/fixtures/sample_design.md`

This script parses a DESIGN.md file and extracts structured tokens into a `design_spec_prefill.json` that the Strategist can consume.

- [ ] **Step 1: Create test fixture — a minimal valid DESIGN.md**

Create `tests/fixtures/sample_design.md`:

```markdown
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
- Ultra-light headline weight (300) creates "whispered authority"
- Deep navy (#0a2540) backgrounds for hero sections
- Blue-violet (#533afd) reserved exclusively for interactive elements
- Multi-layer shadows with blue tint for elevation

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
- Primary: fill #533afd, text white, radius 8px, padding 12px 24px
- Secondary: outline 1px #533afd, text #533afd, radius 8px
- Hover: darken fill 10%, raise shadow

### Cards
- Background: #ffffff, border: 1px #e3e8ee, radius: 12px
- Shadow: 0 2px 4px rgba(0,0,0,0.05), 0 8px 16px rgba(0,0,0,0.05)
- Hover shadow: 0 4px 8px rgba(0,0,0,0.08), 0 16px 32px rgba(0,0,0,0.08)

### Icons
- Style: outlined, mono-weight, 24px default size
- Color: inherit from parent text or #425466 neutral

## 5. Layout Principles

- Max content width: 1080px centered
- Section spacing: 64px vertical
- Grid: 12-column with 24px gutters
- Card spacing: 24px gap

## 6. Depth & Elevation

| Level | Shadow | Use |
|-------|--------|-----|
| Level 0 | none | Flat content |
| Level 1 | 0 2px 4px rgba(6,24,44,0.04) | Cards at rest |
| Level 2 | 0 4px 8px rgba(6,24,44,0.06), 0 12px 24px rgba(6,24,44,0.06) | Cards on hover |
| Level 3 | 0 8px 16px rgba(6,24,44,0.08), 0 24px 48px rgba(6,24,44,0.08) | Modals, dropdowns |

## 7. Do's and Don'ts

### Do's
- Use weight 300 for display text — it is the brand signature
- Let whitespace do the work — Stripe uses space as a luxury signal
- Keep interactive elements purple — everything else neutral

### Don'ts
- Never use bold (700+) for headlines — this contradicts the brand voice
- Never apply purple to non-interactive elements
- Avoid busy backgrounds or patterns — Stripe is about clarity

## 8. Responsive Behavior

- Desktop (1440px+): full 12-column grid, 56px display text
- Tablet (768-1439px): 8-column grid, scale text to 80%
- Mobile (< 768px): single column, 40px display text, stack cards vertically

## 9. Agent Prompt Guide

### Example Prompts
1. "Build a pricing card that follows the Stripe design system"
2. "Create a hero section with deep navy background and light headlines"
3. "Design a feature comparison table using the neutral scale"

### Iteration Guide
- When adding a new component, check Decision Rules before choosing colors
- Purple is earned — only interactive elements get it
- When in doubt about spacing, go generous (64px sections, 24px cards)
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_design_bridge.py`:

```python
"""Tests for design_bridge.py — DESIGN.md → design_spec_prefill.json."""

import json
import os
import sys
import pytest

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "ppt-style-wow", "scripts"))

from design_bridge import parse_design_md, extract_colors, extract_typography, extract_decision_rules, map_font_fallback, generate_prefill

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_design.md")


@pytest.fixture
def design_content():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return f.read()


class TestParseDesignMd:
    """Test that the DESIGN.md is correctly split into 9 sections."""

    def test_returns_all_9_sections(self, design_content):
        sections = parse_design_md(design_content)
        expected_keys = [
            "visual_theme",
            "color_palette",
            "typography",
            "components",
            "layout",
            "depth",
            "dos_donts",
            "responsive",
            "agent_guide",
        ]
        for key in expected_keys:
            assert key in sections, f"Missing section: {key}"

    def test_visual_theme_contains_atmosphere(self, design_content):
        sections = parse_design_md(design_content)
        assert "engineered warmth" in sections["visual_theme"].lower()

    def test_handles_missing_section_gracefully(self):
        """A DESIGN.md with only 3 sections should still parse without error."""
        partial = """# Design System Inspired by Test

## 1. Visual Theme & Atmosphere

Minimal theme.

## 2. Color Palette & Roles

- **Blue** (`#0000ff`): Primary.

## 3. Typography Rules

Body font: Arial.
"""
        sections = parse_design_md(partial)
        assert "visual_theme" in sections
        assert "color_palette" in sections
        assert "typography" in sections
        # Missing sections should be empty strings
        assert sections.get("components", "") == ""


class TestExtractColors:
    """Test color extraction from Section 2."""

    def test_extracts_hex_codes_with_names(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        # Should find Stripe Purple
        purple = next((c for c in colors if c["hex"] == "#533afd"), None)
        assert purple is not None
        assert purple["name"] == "Stripe Purple"

    def test_extracts_at_least_5_colors(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        assert len(colors) >= 5

    def test_extracts_role_description(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        purple = next((c for c in colors if c["hex"] == "#533afd"), None)
        assert "CTA" in purple["role"] or "brand" in purple["role"].lower()


class TestExtractTypography:
    """Test typography extraction from Section 3."""

    def test_extracts_font_families(self, design_content):
        sections = parse_design_md(design_content)
        typo = extract_typography(sections["typography"])
        assert "sohne-var" in typo["heading_family"]
        assert "sohne" in typo["body_family"]

    def test_extracts_type_scale(self, design_content):
        sections = parse_design_md(design_content)
        typo = extract_typography(sections["typography"])
        assert len(typo["scale"]) >= 3
        # Display should be 56px
        display = next((s for s in typo["scale"] if s["purpose"].lower() == "display"), None)
        assert display is not None
        assert display["size"] == "56px"
        assert display["weight"] == "300"


class TestExtractDecisionRules:
    """Test decision rules extraction from Section 1."""

    def test_extracts_at_least_6_rules(self, design_content):
        sections = parse_design_md(design_content)
        rules = extract_decision_rules(sections["visual_theme"])
        assert len(rules) >= 6

    def test_each_rule_has_dimension_and_bias(self, design_content):
        sections = parse_design_md(design_content)
        rules = extract_decision_rules(sections["visual_theme"])
        for rule in rules:
            assert "dimension" in rule
            assert "description" in rule
            assert len(rule["dimension"]) > 0


class TestMapFontFallback:
    """Test web font → PowerPoint system font mapping."""

    def test_maps_sohne_to_segoe(self):
        result = map_font_fallback("sohne-var")
        assert result == "Segoe UI Light"

    def test_maps_sohne_body_to_segoe(self):
        result = map_font_fallback("sohne")
        assert result == "Segoe UI"

    def test_passes_through_system_fonts(self):
        result = map_font_fallback("Arial")
        assert result == "Arial"

    def test_passes_through_unknown_fonts(self):
        result = map_font_fallback("CustomBrandFont")
        assert result == "CustomBrandFont"


class TestGeneratePrefill:
    """Test the full prefill JSON generation."""

    def test_produces_valid_json_structure(self, design_content):
        prefill = generate_prefill(design_content)
        assert "style_objective" in prefill
        assert "color_scheme" in prefill
        assert "typography" in prefill
        assert "icon_approach" in prefill
        assert "image_strategy" in prefill
        assert "decision_rules" in prefill

    def test_color_scheme_has_primary(self, design_content):
        prefill = generate_prefill(design_content)
        assert "primary" in prefill["color_scheme"]
        assert prefill["color_scheme"]["primary"].startswith("#")

    def test_typography_has_fallback(self, design_content):
        prefill = generate_prefill(design_content)
        assert "heading_fallback" in prefill["typography"]
        # sohne-var → Segoe UI Light
        assert prefill["typography"]["heading_fallback"] == "Segoe UI Light"

    def test_decision_rules_is_list(self, design_content):
        prefill = generate_prefill(design_content)
        assert isinstance(prefill["decision_rules"], list)
        assert len(prefill["decision_rules"]) >= 6
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd /Users/nigel/project/PPT-style-wow
python3 -m pytest tests/test_design_bridge.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'design_bridge'`

- [ ] **Step 4: Implement `design_bridge.py`**

Create `skills/ppt-style-wow/scripts/design_bridge.py`:

```python
#!/usr/bin/env python3
"""Bridge DESIGN.md → design_spec_prefill.json.

Parses a DESIGN.md file (9-section format from design.skill) and extracts
structured tokens into a JSON prefill that the ppt-master Strategist can
consume to auto-fill 5 of its 8 confirmations.

Usage:
    python3 design_bridge.py <path/to/DESIGN.md> [-o output.json]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Section heading patterns (match "## N. Title" format)
SECTION_PATTERNS = {
    "visual_theme": r"##\s*1\.\s*Visual Theme",
    "color_palette": r"##\s*2\.\s*Color Palette",
    "typography": r"##\s*3\.\s*Typography",
    "components": r"##\s*4\.\s*Component",
    "layout": r"##\s*5\.\s*Layout",
    "depth": r"##\s*6\.\s*Depth",
    "dos_donts": r"##\s*7\.\s*Do.s and Don.ts",
    "responsive": r"##\s*8\.\s*Responsive",
    "agent_guide": r"##\s*9\.\s*Agent Prompt",
}

# Web font → PowerPoint system font fallback map
FONT_FALLBACK_MAP = {
    "sohne-var": "Segoe UI Light",
    "sohne": "Segoe UI",
    "inter": "Segoe UI",
    "sf pro display": "Helvetica Neue",
    "sf pro text": "Helvetica",
    "roboto": "Arial",
    "open sans": "Calibri",
    "lato": "Calibri",
    "montserrat": "Arial",
    "poppins": "Arial",
    "nunito": "Calibri",
    "raleway": "Segoe UI Light",
    "playfair display": "Georgia",
    "merriweather": "Georgia",
    "source sans pro": "Calibri",
    "dm sans": "Arial",
    "plus jakarta sans": "Segoe UI",
    "geist": "Segoe UI",
    "geist mono": "Consolas",
}


def parse_design_md(content: str) -> dict[str, str]:
    """Split DESIGN.md content into named sections.

    Returns a dict mapping section keys to their raw markdown content.
    Missing sections map to empty strings.
    """
    sections: dict[str, str] = {}
    # Find all section boundaries
    boundaries = []
    for key, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            boundaries.append((match.start(), key))

    boundaries.sort(key=lambda x: x[0])

    for i, (start, key) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(content)
        sections[key] = content[start:end].strip()

    # Fill missing sections with empty string
    for key in SECTION_PATTERNS:
        if key not in sections:
            sections[key] = ""

    return sections


def extract_colors(color_section: str) -> list[dict[str, str]]:
    """Extract color entries from Section 2.

    Each entry: {"name": "Stripe Purple", "hex": "#533afd", "role": "Primary brand..."}
    """
    colors = []
    # Match pattern: **Name** (`#hexcode`): role description
    pattern = r"\*\*(.+?)\*\*\s*\(`(#[0-9a-fA-F]{3,8})`\):\s*(.+?)(?:\n|$)"
    for match in re.finditer(pattern, color_section):
        colors.append({
            "name": match.group(1).strip(),
            "hex": match.group(2).strip().lower(),
            "role": match.group(3).strip().rstrip("."),
        })
    return colors


def extract_typography(typo_section: str) -> dict:
    """Extract font families and type scale from Section 3.

    Returns: {
        "heading_family": "sohne-var, ...",
        "body_family": "sohne, ...",
        "heading_fallback": "Segoe UI Light",
        "body_fallback": "Segoe UI",
        "scale": [{"purpose": "Display", "size": "56px", "weight": "300", "line_height": "1.1"}, ...]
    }
    """
    result = {
        "heading_family": "",
        "body_family": "",
        "heading_fallback": "",
        "body_fallback": "",
        "scale": [],
    }

    # Extract font families
    heading_match = re.search(
        r"\*\*(?:Heading|Title|Display)\s*[:\uff1a]\*\*\s*(.+?)(?:\n|$)",
        typo_section, re.IGNORECASE,
    )
    if heading_match:
        result["heading_family"] = heading_match.group(1).strip()
        first_font = result["heading_family"].split(",")[0].strip()
        result["heading_fallback"] = map_font_fallback(first_font)

    body_match = re.search(
        r"\*\*(?:Body|Text|Content)\s*[:\uff1a]\*\*\s*(.+?)(?:\n|$)",
        typo_section, re.IGNORECASE,
    )
    if body_match:
        result["body_family"] = body_match.group(1).strip()
        first_font = result["body_family"].split(",")[0].strip()
        result["body_fallback"] = map_font_fallback(first_font)

    # Extract type scale from markdown table
    # Match rows like: | Display | 56px | 300 | 1.1 |
    table_pattern = r"\|\s*(\w[\w\s]*?)\s*\|\s*(\d+px)\s*\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|"
    for match in re.finditer(table_pattern, typo_section):
        result["scale"].append({
            "purpose": match.group(1).strip(),
            "size": match.group(2).strip(),
            "weight": match.group(3).strip(),
            "line_height": match.group(4).strip(),
        })

    return result


def extract_decision_rules(visual_theme_section: str) -> list[dict[str, str]]:
    """Extract Design Decision Rules from Section 1.

    Returns: [{"dimension": "Emphasis", "description": "Reduce weight rather than..."}, ...]
    """
    rules = []
    # Match pattern: - **Dimension:** description text
    pattern = r"-\s*\*\*(.+?)[:\uff1a]\*\*\s*(.+?)(?=\n-\s*\*\*|\n\n|\n##|\Z)"
    # Look within the Decision Rules subsection
    rules_start = re.search(r"###?\s*Design Decision Rules", visual_theme_section, re.IGNORECASE)
    if not rules_start:
        return rules

    rules_text = visual_theme_section[rules_start.end():]
    # Stop at next heading or Key Characteristics
    end_match = re.search(r"\n##|\n\*\*Key Characteristics", rules_text)
    if end_match:
        rules_text = rules_text[:end_match.start()]

    for match in re.finditer(pattern, rules_text, re.DOTALL):
        rules.append({
            "dimension": match.group(1).strip(),
            "description": match.group(2).strip(),
        })

    return rules


def map_font_fallback(font_name: str) -> str:
    """Map a web font to the closest PowerPoint-safe system font.

    Returns the original font name if no mapping exists (assumed to be a system font).
    """
    return FONT_FALLBACK_MAP.get(font_name.lower().strip(), font_name)


def _extract_style_objective(visual_theme: str) -> str:
    """Extract the atmosphere/style description from Section 1."""
    # Take the first paragraph after the section heading (skip the heading line)
    lines = visual_theme.split("\n")
    paragraphs = []
    current = []
    for line in lines:
        if line.startswith("##"):
            continue
        if line.strip() == "" and current:
            paragraphs.append(" ".join(current))
            current = []
        elif line.strip():
            current.append(line.strip())
    if current:
        paragraphs.append(" ".join(current))

    return paragraphs[0] if paragraphs else ""


def _extract_icon_approach(components: str) -> str:
    """Extract icon styling info from Section 4."""
    icon_match = re.search(
        r"###?\s*Icons?\s*\n((?:.*\n)*?)(?=###|\Z)",
        components, re.IGNORECASE,
    )
    if icon_match:
        return icon_match.group(1).strip()
    return ""


def _extract_image_strategy(dos_donts: str, visual_theme: str) -> str:
    """Derive image strategy from Section 7 Do's/Don'ts and Section 1."""
    parts = []
    # Extract "Do's" section
    do_match = re.search(r"###?\s*Do.s\s*\n((?:.*\n)*?)(?=###|\Z)", dos_donts, re.IGNORECASE)
    if do_match:
        parts.append(do_match.group(1).strip())
    # Extract "Don'ts" section
    dont_match = re.search(r"###?\s*Don.ts\s*\n((?:.*\n)*?)(?=###|\Z)", dos_donts, re.IGNORECASE)
    if dont_match:
        parts.append(dont_match.group(1).strip())
    return "\n".join(parts) if parts else ""


def generate_prefill(content: str) -> dict:
    """Generate the full design_spec_prefill from DESIGN.md content.

    Returns a dict ready to be serialized as JSON.
    """
    sections = parse_design_md(content)
    colors = extract_colors(sections["color_palette"])
    typography = extract_typography(sections["typography"])
    decision_rules = extract_decision_rules(sections["visual_theme"])

    # Build color scheme with role-based keys
    color_scheme = {"semantic_names": {}}
    for color in colors:
        color_scheme["semantic_names"][color["name"]] = {
            "hex": color["hex"],
            "role": color["role"],
        }
    # Assign primary/background/accent based on role keywords
    for color in colors:
        role_lower = color["role"].lower()
        if "primary" in role_lower or "brand" in role_lower:
            color_scheme.setdefault("primary", color["hex"])
        elif "background" in role_lower or "hero" in role_lower:
            color_scheme.setdefault("background", color["hex"])
        elif "body" in role_lower or "text" in role_lower:
            color_scheme.setdefault("text_primary", color["hex"])
        elif "accent" in role_lower or "highlight" in role_lower or "secondary" in role_lower:
            color_scheme.setdefault("accent", color["hex"])

    return {
        "style_objective": _extract_style_objective(sections["visual_theme"]),
        "color_scheme": color_scheme,
        "typography": typography,
        "icon_approach": _extract_icon_approach(sections["components"]),
        "image_strategy": _extract_image_strategy(sections["dos_donts"], sections["visual_theme"]),
        "decision_rules": decision_rules,
    }


def main():
    parser = argparse.ArgumentParser(description="Bridge DESIGN.md to design_spec_prefill.json")
    parser.add_argument("design_md", help="Path to DESIGN.md file")
    parser.add_argument("-o", "--output", help="Output JSON path (default: same dir as input)")
    args = parser.parse_args()

    design_path = Path(args.design_md)
    if not design_path.exists():
        print(f"Error: {design_path} not found", file=sys.stderr)
        sys.exit(1)

    content = design_path.read_text(encoding="utf-8")
    prefill = generate_prefill(content)

    output_path = Path(args.output) if args.output else design_path.parent / "design_spec_prefill.json"
    output_path.write_text(json.dumps(prefill, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Prefill written to {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
python3 -m pytest tests/test_design_bridge.py -v
```

Expected: ALL PASS

- [ ] **Step 6: Test CLI interface**

```bash
python3 skills/ppt-style-wow/scripts/design_bridge.py tests/fixtures/sample_design.md -o /tmp/test_prefill.json
cat /tmp/test_prefill.json | python3 -m json.tool
```

Expected: Valid JSON with style_objective, color_scheme (primary=#533afd), typography (heading_family contains sohne-var, heading_fallback=Segoe UI Light), 6+ decision_rules.

- [ ] **Step 7: Commit**

```bash
git add skills/ppt-style-wow/scripts/design_bridge.py tests/
git commit -m "feat: add design_bridge.py with TDD — parses DESIGN.md into Strategist prefill JSON"
```

---

## Task 5: Build `template_manager.py` (TDD)

**Files:**
- Create: `skills/ppt-style-wow/scripts/template_manager.py`
- Create: `tests/test_template_manager.py`

This script manages the template evolution layer: archiving history, promoting to templates, listing, and tag-based matching.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_template_manager.py`:

```python
"""Tests for template_manager.py — template evolution layer."""

import json
import os
import shutil
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "ppt-style-wow", "scripts"))

from template_manager import (
    archive_to_history,
    promote_to_template,
    list_templates,
    list_history,
    match_templates_by_tags,
    remove_template,
    slugify,
)


@pytest.fixture
def workspace(tmp_path):
    """Create a temporary workspace with history/ and templates/ dirs."""
    history_dir = tmp_path / "history"
    templates_dir = tmp_path / "templates"
    history_dir.mkdir()
    templates_dir.mkdir()
    return tmp_path


@pytest.fixture
def sample_design_md(tmp_path):
    """Create a sample DESIGN.md file."""
    design = tmp_path / "DESIGN.md"
    design.write_text("# Design System Inspired by Stripe\n\n## 1. Visual Theme\n\nEngineered warmth.")
    return design


@pytest.fixture
def sample_metadata():
    return {
        "source_url": "https://stripe.com",
        "source_type": "url",
        "content_summary": "Q3 financial report",
        "tags": {
            "industry": ["fintech", "saas"],
            "style": ["minimalist", "tech"],
            "scene": ["report"],
        },
        "atmosphere": "Engineered warmth — light headlines against deep navy",
        "decision_rules_digest": ["emphasis-by-lightness", "blue-tinted-depth"],
    }


class TestSlugify:
    def test_basic_slugify(self):
        assert slugify("科技极简风") == "科技极简风"

    def test_ascii_slugify(self):
        assert slugify("Tech Minimalist") == "tech-minimalist"

    def test_strips_special_chars(self):
        assert slugify("Hello, World!") == "hello-world"


class TestArchiveToHistory:
    def test_creates_history_entry(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        entry_path = workspace / "history" / entry_id
        assert entry_path.exists()
        assert (entry_path / "DESIGN.md").exists()
        assert (entry_path / "metadata.json").exists()

    def test_metadata_has_required_fields(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        meta_path = workspace / "history" / entry_id / "metadata.json"
        meta = json.loads(meta_path.read_text())
        assert "id" in meta
        assert "created_at" in meta
        assert "source_url" in meta
        assert "tags" in meta

    def test_copies_style_references_if_present(self, workspace, sample_design_md, sample_metadata):
        refs = sample_design_md.parent / "STYLE-REFERENCES.md"
        refs.write_text("# Style References")
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
            style_references_path=refs,
        )
        assert (workspace / "history" / entry_id / "STYLE-REFERENCES.md").exists()


class TestPromoteToTemplate:
    def test_promotes_history_entry(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        slug = promote_to_template(
            history_dir=workspace / "history",
            templates_dir=workspace / "templates",
            entry_id=entry_id,
            name="科技极简风",
            tags=["tech", "minimalist"],
        )
        template_path = workspace / "templates" / slug
        assert template_path.exists()
        assert (template_path / "DESIGN.md").exists()
        meta = json.loads((template_path / "metadata.json").read_text())
        assert meta["name"] == "科技极简风"
        assert meta["usage_count"] == 0

    def test_raises_on_missing_history(self, workspace):
        with pytest.raises(FileNotFoundError):
            promote_to_template(
                history_dir=workspace / "history",
                templates_dir=workspace / "templates",
                entry_id="nonexistent",
                name="test",
            )


class TestListTemplates:
    def test_lists_empty(self, workspace):
        result = list_templates(workspace / "templates")
        assert result == []

    def test_lists_promoted_template(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        promote_to_template(
            history_dir=workspace / "history",
            templates_dir=workspace / "templates",
            entry_id=entry_id,
            name="科技极简风",
        )
        result = list_templates(workspace / "templates")
        assert len(result) == 1
        assert result[0]["name"] == "科技极简风"


class TestMatchTemplatesByTags:
    def test_matches_by_industry_tag(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        promote_to_template(
            history_dir=workspace / "history",
            templates_dir=workspace / "templates",
            entry_id=entry_id,
            name="FinTech Style",
            tags=["fintech", "minimalist"],
        )
        matches = match_templates_by_tags(
            templates_dir=workspace / "templates",
            query_tags=["fintech"],
        )
        assert len(matches) == 1
        assert matches[0]["name"] == "FinTech Style"

    def test_returns_empty_on_no_match(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        promote_to_template(
            history_dir=workspace / "history",
            templates_dir=workspace / "templates",
            entry_id=entry_id,
            name="FinTech Style",
            tags=["fintech"],
        )
        matches = match_templates_by_tags(
            templates_dir=workspace / "templates",
            query_tags=["healthcare"],
        )
        assert len(matches) == 0


class TestRemoveTemplate:
    def test_removes_existing_template(self, workspace, sample_design_md, sample_metadata):
        entry_id = archive_to_history(
            history_dir=workspace / "history",
            design_md_path=sample_design_md,
            metadata=sample_metadata,
        )
        slug = promote_to_template(
            history_dir=workspace / "history",
            templates_dir=workspace / "templates",
            entry_id=entry_id,
            name="To Remove",
        )
        remove_template(workspace / "templates", slug)
        assert not (workspace / "templates" / slug).exists()

    def test_raises_on_missing_template(self, workspace):
        with pytest.raises(FileNotFoundError):
            remove_template(workspace / "templates", "nonexistent")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
python3 -m pytest tests/test_template_manager.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'template_manager'`

- [ ] **Step 3: Implement `template_manager.py`**

Create `skills/ppt-style-wow/scripts/template_manager.py`:

```python
#!/usr/bin/env python3
"""Template evolution manager — archive, promote, list, match, remove.

Manages the lifecycle of design templates:
- Silent archiving after each PPT generation
- Promoting history entries to reusable templates
- Tag-based matching for template recommendations

Usage:
    python3 template_manager.py history   --history-dir <dir>
    python3 template_manager.py list      --templates-dir <dir>
    python3 template_manager.py promote   --history-dir <dir> --templates-dir <dir> --id <id> --name <name> [--tags t1,t2]
    python3 template_manager.py match     --templates-dir <dir> --tags t1,t2 [--top N]
    python3 template_manager.py remove    --templates-dir <dir> --id <slug>
"""

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def slugify(text: str) -> str:
    """Convert text to a URL/filesystem-safe slug.

    Preserves non-ASCII characters (e.g., Chinese) but lowercases ASCII
    and replaces spaces/special chars with hyphens.
    """
    # Lowercase ASCII only
    result = []
    for char in text:
        if char.isascii():
            result.append(char.lower())
        else:
            result.append(char)
    text = "".join(result)
    # Replace non-alphanumeric (keeping unicode letters) with hyphens
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text


def archive_to_history(
    history_dir: Path,
    design_md_path: Path,
    metadata: dict,
    style_references_path: Path | None = None,
    design_spec_path: Path | None = None,
) -> str:
    """Archive a DESIGN.md and metadata to history/.

    Returns the entry ID (directory name).
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d-%H%M%S")
    source_slug = slugify(metadata.get("content_summary", "unnamed")[:40])
    entry_id = f"{timestamp}-{source_slug}"

    entry_dir = history_dir / entry_id
    entry_dir.mkdir(parents=True, exist_ok=True)

    # Copy DESIGN.md
    shutil.copy2(design_md_path, entry_dir / "DESIGN.md")

    # Copy optional files
    if style_references_path and style_references_path.exists():
        shutil.copy2(style_references_path, entry_dir / "STYLE-REFERENCES.md")
    if design_spec_path and design_spec_path.exists():
        shutil.copy2(design_spec_path, entry_dir / "design_spec.md")

    # Write metadata
    meta = {
        "id": entry_id,
        "created_at": now.isoformat(),
        **metadata,
    }
    (entry_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return entry_id


def promote_to_template(
    history_dir: Path,
    templates_dir: Path,
    entry_id: str,
    name: str,
    tags: list[str] | None = None,
) -> str:
    """Promote a history entry to a reusable template.

    Returns the template slug (directory name).
    """
    source = history_dir / entry_id
    if not source.exists():
        raise FileNotFoundError(f"History entry not found: {entry_id}")

    slug = slugify(name)
    dest = templates_dir / slug
    dest.mkdir(parents=True, exist_ok=True)

    # Copy all files from history entry
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, dest / item.name)

    # Update metadata with template-specific fields
    meta_path = dest / "metadata.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["name"] = name
    meta["usage_count"] = 0
    meta["promoted_at"] = datetime.now(timezone.utc).isoformat()
    if tags:
        meta.setdefault("tags", {})
        meta["tags"]["custom"] = tags
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return slug


def list_templates(templates_dir: Path) -> list[dict]:
    """List all templates with their metadata."""
    results = []
    if not templates_dir.exists():
        return results
    for entry in sorted(templates_dir.iterdir()):
        meta_path = entry / "metadata.json"
        if entry.is_dir() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            results.append(meta)
    return results


def list_history(history_dir: Path) -> list[dict]:
    """List all history entries with their metadata."""
    results = []
    if not history_dir.exists():
        return results
    for entry in sorted(history_dir.iterdir(), reverse=True):
        meta_path = entry / "metadata.json"
        if entry.is_dir() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            results.append(meta)
    return results


def match_templates_by_tags(
    templates_dir: Path,
    query_tags: list[str],
    top_n: int = 5,
) -> list[dict]:
    """Phase 1 matching: filter templates by tag overlap.

    Returns templates sorted by number of matching tags (descending).
    """
    templates = list_templates(templates_dir)
    scored = []
    for tmpl in templates:
        all_tags = set()
        tags_dict = tmpl.get("tags", {})
        if isinstance(tags_dict, dict):
            for tag_list in tags_dict.values():
                if isinstance(tag_list, list):
                    all_tags.update(t.lower() for t in tag_list)
        overlap = len(all_tags & {t.lower() for t in query_tags})
        if overlap > 0:
            scored.append((overlap, tmpl))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [tmpl for _, tmpl in scored[:top_n]]


def remove_template(templates_dir: Path, slug: str) -> None:
    """Remove a template by slug."""
    target = templates_dir / slug
    if not target.exists():
        raise FileNotFoundError(f"Template not found: {slug}")
    shutil.rmtree(target)


def main():
    parser = argparse.ArgumentParser(description="Template evolution manager")
    sub = parser.add_subparsers(dest="command", required=True)

    # history
    p_hist = sub.add_parser("history", help="List history entries")
    p_hist.add_argument("--history-dir", required=True, type=Path)

    # list
    p_list = sub.add_parser("list", help="List templates")
    p_list.add_argument("--templates-dir", required=True, type=Path)

    # promote
    p_prom = sub.add_parser("promote", help="Promote history entry to template")
    p_prom.add_argument("--history-dir", required=True, type=Path)
    p_prom.add_argument("--templates-dir", required=True, type=Path)
    p_prom.add_argument("--id", required=True, help="History entry ID")
    p_prom.add_argument("--name", required=True, help="Template display name")
    p_prom.add_argument("--tags", default="", help="Comma-separated tags")

    # match
    p_match = sub.add_parser("match", help="Match templates by tags")
    p_match.add_argument("--templates-dir", required=True, type=Path)
    p_match.add_argument("--tags", required=True, help="Comma-separated query tags")
    p_match.add_argument("--top", type=int, default=5, help="Max results")

    # remove
    p_rm = sub.add_parser("remove", help="Remove a template")
    p_rm.add_argument("--templates-dir", required=True, type=Path)
    p_rm.add_argument("--id", required=True, help="Template slug")

    args = parser.parse_args()

    if args.command == "history":
        entries = list_history(args.history_dir)
        for e in entries:
            print(f"  {e['id']}  {e.get('source_url', 'N/A')}  {e.get('content_summary', '')[:50]}")
        if not entries:
            print("  (no history entries)")

    elif args.command == "list":
        templates = list_templates(args.templates_dir)
        for t in templates:
            print(f"  {t.get('name', 'unnamed')}  tags={t.get('tags', {})}  used={t.get('usage_count', 0)}x")
        if not templates:
            print("  (no templates)")

    elif args.command == "promote":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None
        slug = promote_to_template(
            history_dir=args.history_dir,
            templates_dir=args.templates_dir,
            entry_id=args.id,
            name=args.name,
            tags=tags,
        )
        print(f"Promoted to template: {slug}")

    elif args.command == "match":
        query_tags = [t.strip() for t in args.tags.split(",")]
        matches = match_templates_by_tags(args.templates_dir, query_tags, args.top)
        for m in matches:
            print(f"  {m.get('name', 'unnamed')}  atmosphere={m.get('atmosphere', 'N/A')[:60]}")
        if not matches:
            print("  (no matching templates)")

    elif args.command == "remove":
        remove_template(args.templates_dir, args.id)
        print(f"Removed template: {args.id}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
python3 -m pytest tests/test_template_manager.py -v
```

Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add skills/ppt-style-wow/scripts/template_manager.py tests/test_template_manager.py
git commit -m "feat: add template_manager.py with TDD — archive, promote, list, match, remove"
```

---

## Task 6: Write CLAUDE.md

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write CLAUDE.md**

```markdown
# CLAUDE.md

This file provides project overview for Claude Code. Before executing PPT generation tasks, **you MUST first read `SKILL.md`** for the complete workflow and rules.

## Project Overview

PPT-style-wow is an AI-driven presentation generation system with brand-aware design extraction. It combines design system extraction (from websites/screenshots) with native-editable PPTX generation through multi-role collaboration.

**Core Pipeline**: `[Design Extraction] → Source Document → Create Project → Strategist (auto-filled from DESIGN.md) → Executor → Post-processing → Export PPTX → Silent Archive`

## Three Entry Points

1. **From URL**: User provides a website URL + source document → extract DESIGN.md → generate brand-consistent PPTX
2. **From DESIGN.md**: User provides an existing DESIGN.md + source document → skip extraction → generate PPTX
3. **No preference**: User provides only source document → match from template library → generate PPTX

## Common Commands

```bash
# Source content conversion
python3 skills/ppt-style-wow/scripts/source_to_md/pdf_to_md.py <PDF_file>
python3 skills/ppt-style-wow/scripts/source_to_md/doc_to_md.py <DOCX_file>
python3 skills/ppt-style-wow/scripts/source_to_md/ppt_to_md.py <PPTX_file>
python3 skills/ppt-style-wow/scripts/source_to_md/web_to_md.py <URL>

# Project management
python3 skills/ppt-style-wow/scripts/project_manager.py init <project_name> --format ppt169
python3 skills/ppt-style-wow/scripts/project_manager.py import-sources <project_path> <source_files...> --move

# Design bridge (DESIGN.md → Strategist prefill)
python3 skills/ppt-style-wow/scripts/design_bridge.py <project_path>/design/DESIGN.md

# Template management
python3 skills/ppt-style-wow/scripts/template_manager.py list --templates-dir templates/
python3 skills/ppt-style-wow/scripts/template_manager.py history --history-dir history/
python3 skills/ppt-style-wow/scripts/template_manager.py promote --history-dir history/ --templates-dir templates/ --id <id> --name "Name" --tags tag1,tag2
python3 skills/ppt-style-wow/scripts/template_manager.py match --templates-dir templates/ --tags tag1,tag2

# Image tools
python3 skills/ppt-style-wow/scripts/analyze_images.py <project_path>/images
python3 skills/ppt-style-wow/scripts/image_gen.py "prompt" --aspect_ratio 16:9 -o <project_path>/images

# Post-processing pipeline (MUST run sequentially, one at a time)
python3 skills/ppt-style-wow/scripts/total_md_split.py <project_path>
python3 skills/ppt-style-wow/scripts/finalize_svg.py <project_path>
python3 skills/ppt-style-wow/scripts/svg_to_pptx.py <project_path> -s final
```

## SVG Technical Constraints (Non-negotiable)

**Banned features**: `mask` | `<style>` | `class` | external CSS | `<foreignObject>` | `textPath` | `@font-face` | `<animate*>` | `<script>` | `<iframe>` | `<symbol>`+`<use>`

**PPT compatibility alternatives**:

| Banned | Alternative |
|--------|-------------|
| `rgba()` | `fill-opacity` / `stroke-opacity` |
| `<g opacity>` | Set opacity on each child element individually |

## Post-processing Notes

- **NEVER** run the three post-processing steps in a single code block
- **NEVER** export directly from `svg_output/` — MUST export from `svg_final/`
- Each post-processing step must complete before running the next

## Canvas Format Quick Reference

| Format | viewBox |
|--------|---------|
| PPT 16:9 | `0 0 1280 720` |
| PPT 4:3 | `0 0 1024 768` |
| Xiaohongshu | `0 0 1242 1660` |
| WeChat Moments | `0 0 1080 1080` |
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md with project overview and command reference"
```

---

## Task 7: Write SKILL.md (Main Skill Definition)

**Files:**
- Create: `SKILL.md`

This is the most important file — the unified workflow definition that ties all three layers together.

- [ ] **Step 1: Write SKILL.md**

Create `SKILL.md` with the complete unified workflow. This integrates design.skill's extraction flow, ppt-master's generation pipeline, and the new template evolution layer.

```markdown
---
name: ppt-style-wow
description: >
  Brand-aware PPT generation with design evolution. Extracts visual systems from
  websites/screenshots, generates native-editable PPTX matching the brand, and
  evolves a reusable template library. Use when user asks to "create PPT",
  "make presentation", "generate slides", mentions a brand/website style, or
  says "用...的风格做PPT".
---

# PPT-style-wow Skill

> Brand-aware AI presentation system. Extract design DNA from any website → generate
> native-editable PPTX that matches the brand → evolve a growing template library.

**Core Pipeline**: `Design Source → Extract/Select DESIGN.md → Source Document → Project Init → Strategist (auto-prefilled) → Executor → Post-processing → PPTX Export → Silent Archive`

> [!CAUTION]
> ## Global Execution Discipline (MANDATORY)
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ require explicit user response
> 3. **NO CROSS-PHASE BUNDLING** — Each phase completes before the next begins
> 4. **NO SUB-AGENT SVG GENERATION** — Executor SVG generation MUST be done by the main agent
> 5. **SEQUENTIAL PAGE GENERATION ONLY** — SVG pages one at a time, no batching

> [!IMPORTANT]
> ## Language Rule
> - Match the language of the user's input
> - Template format files (design_spec.md) keep English structure, content values in user's language

---

## Entry Point Detection

Analyze the user's request to determine which entry point to use:

| User provides | Entry Point | Start at |
|--------------|-------------|----------|
| Website URL + source document | **URL Entry** | Step 1 |
| Existing DESIGN.md + source document | **DESIGN.md Entry** | Step 3 |
| Only source document (no style preference) | **Template Match Entry** | Step 2b |
| URL/screenshot only (no source doc) | **Extraction Only** | Step 1, stop after Step 2 |

---

## Step 1: Design Extraction (URL/Screenshot Entry Only)

🚧 **GATE**: User has provided a website URL or screenshot for style extraction.

**If URL provided:**

1. Read the format specs: `reference/format-spec.md` and `reference/style-references-spec.md`
2. Read the exemplar: `reference/example-stripe.md`
3. Navigate to URL via Chrome DevTools MCP (`new_page` → `navigate_page` → wait for network idle)
4. Run `reference/extraction.js` via `evaluate_script` to harvest CSS tokens
5. `take_screenshot` at 1440px viewport (desktop)
6. Optionally capture dark mode and 390px mobile screenshots
7. Answer the identity + reproducibility questions from SKILL (see `reference/format-spec.md`)
8. Write DESIGN.md (9 sections) to `<project_path>/design/DESIGN.md`
9. Write STYLE-REFERENCES.md to `<project_path>/design/STYLE-REFERENCES.md`
10. Generate preview.html and preview-dark.html from `reference/preview-template.html`

**If screenshot provided:**
- Read image(s) directly with vision
- Approximate tokens from rendered visuals
- Write DESIGN.md with best-effort values

**If existing DESIGN.md provided:**
- Validate it has the 9 required sections (warn on missing, proceed with available)
- Copy to `<project_path>/design/DESIGN.md`

**Checkpoint — DESIGN.md ready. Proceed to Step 2.**

---

## Step 2: Source Content Processing

🚧 **GATE**: DESIGN.md is ready (from Step 1 or user-provided).

Convert source materials to Markdown:

| Source | Command |
|--------|---------|
| PDF | `python3 ${SKILL_DIR}/scripts/source_to_md/pdf_to_md.py <file>` |
| DOCX/Office | `python3 ${SKILL_DIR}/scripts/source_to_md/doc_to_md.py <file>` |
| PPTX | `python3 ${SKILL_DIR}/scripts/source_to_md/ppt_to_md.py <file>` |
| Web URL | `python3 ${SKILL_DIR}/scripts/source_to_md/web_to_md.py <URL>` |
| Markdown | Read directly |

**Checkpoint — Source content ready. Proceed to Step 3.**

---

## Step 2b: Template Matching (No-Preference Entry Only)

🚧 **GATE**: User has not specified a style preference. Source content is available.

1. Analyze source content to extract likely tags (industry, scene type)
2. Run tag-based filtering:
   ```bash
   python3 ${SKILL_DIR}/scripts/template_manager.py match --templates-dir templates/ --tags <extracted_tags>
   ```
3. If matches found, rank candidates by reading each template's `atmosphere` and `decision_rules_digest` from metadata.json, then judge semantic fit against the content summary
4. ⛔ **BLOCKING** — Present top 2-3 templates + free design option:
   > Based on your content, I recommend:
   > A) [Template Name] — from [source], suits [reason]
   > B) [Template Name] — from [source], suits [reason]
   > C) Free design — AI designs from scratch based on content

5. If template library is empty, skip to free design (standard ppt-master flow)
6. User confirms → load selected template's DESIGN.md → proceed to Step 3

**Checkpoint — Template selected. Proceed to Step 3.**

---

## Step 3: Project Initialization

🚧 **GATE**: Source content + DESIGN.md both ready.

```bash
python3 ${SKILL_DIR}/scripts/project_manager.py init <project_name> --format <format>
python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <source_files...> --move
```

Copy DESIGN.md into the project:
```bash
mkdir -p <project_path>/design
cp <design_md_path> <project_path>/design/DESIGN.md
```

**Checkpoint — Project structure created. Proceed to Step 4.**

---

## Step 4: Design Bridge + Strategist Phase

🚧 **GATE**: Step 3 complete.

### 4a. Run the Design Bridge

```bash
python3 ${SKILL_DIR}/scripts/design_bridge.py <project_path>/design/DESIGN.md -o <project_path>/design_spec_prefill.json
```

This extracts structured tokens from DESIGN.md and pre-fills 5 of the 8 Strategist confirmations:
- Style objective (from §1 Visual Theme)
- Color scheme (from §2 Color Palette)
- Typography plan (from §3 Typography Rules, with PPT font fallbacks)
- Icon approach (from §4 Component Stylings)
- Image strategy (from §7 Do's and Don'ts)

### 4b. Read Strategist Role + Spec Reference

```
Read ${SKILL_DIR}/references/strategist.md
Read ${SKILL_DIR}/templates/design_spec_reference.md
```

### 4c. Three User Confirmations

⛔ **BLOCKING** — Present the auto-filled design spec and ask only 3 questions:

> I've extracted the design system from [source]. Here's the auto-filled spec:
>
> - **Style**: [from prefill — atmosphere description]
> - **Colors**: [from prefill — primary, background, accent with hex]
> - **Typography**: [from prefill — fonts with PPT fallbacks]
> - **Icons**: [from prefill — approach]
>
> Please confirm:
> 1. **Canvas format?** (default: PPT 16:9)
> 2. **Page count?** (recommended: N based on content volume)
> 3. **Target audience?**
>
> You can also override any auto-filled value above.

### 4d. Output design_spec.md

After user confirms, merge prefill + user answers into full `<project_path>/design_spec.md` following the template structure (Sections I–XI).

**Inject Decision Rules** from DESIGN.md §1 into design_spec.md as additional Executor constraints.

If user has images, run analysis before outputting spec:
```bash
python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/images
```

**Checkpoint — Design spec complete. Auto-proceed to Step 5.**

---

## Step 5: Image Generation (Optional)

🚧 **GATE**: Step 4 complete. design_spec.md mentions image needs.

Read `${SKILL_DIR}/references/image-generator.md` for the Image_Generator role definition.

Generate images as needed using the design system colors and style:
```bash
python3 ${SKILL_DIR}/scripts/image_gen.py "prompt matching brand style" --aspect_ratio 16:9 -o <project_path>/images
```

**Checkpoint — Images ready (or skipped). Proceed to Step 6.**

---

## Step 6: Executor — SVG Page Generation

🚧 **GATE**: Step 5 complete (or skipped).

Read the appropriate Executor role definition based on style:
- General: `${SKILL_DIR}/references/executor-general.md`
- Consulting: `${SKILL_DIR}/references/executor-consultant.md`
- Top Consulting: `${SKILL_DIR}/references/executor-consultant-top.md`

Also read: `${SKILL_DIR}/references/executor-base.md` and `${SKILL_DIR}/references/shared-standards.md`

**Critical rules:**
- Generate SVG pages **sequentially, one at a time**
- **Decision Rules from DESIGN.md are binding** — when making visual choices about color, spacing, emphasis, depth, or density, consult the Decision Rules first
- All SVG technical constraints from shared-standards.md apply
- No sub-agent delegation for SVG generation

Write each page to `<project_path>/svg_output/page_XX.svg`

**Checkpoint — All SVG pages generated. Proceed to Step 7.**

---

## Step 7: Post-Processing + PPTX Export

🚧 **GATE**: Step 6 complete. All SVG pages in svg_output/.

Run these three commands **sequentially, one at a time** (NEVER batch):

```bash
# Step 7a: Split speaker notes
python3 ${SKILL_DIR}/scripts/total_md_split.py <project_path>
# ✅ Confirm no errors before next command

# Step 7b: Finalize SVGs
python3 ${SKILL_DIR}/scripts/finalize_svg.py <project_path>
# ✅ Confirm no errors before next command

# Step 7c: Export to PPTX
python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path> -s final
```

Output: `exports/<project_name>_<timestamp>.pptx`

**Checkpoint — PPTX exported. Proceed to Step 8.**

---

## Step 8: Silent Archive

🚧 **GATE**: Step 7 complete. PPTX exported successfully.

Archive this generation to history (automatic, no user action needed):

```bash
python3 ${SKILL_DIR}/scripts/template_manager.py archive \
  --history-dir history/ \
  --design-md <project_path>/design/DESIGN.md \
  --metadata '{"source_url": "<url>", "source_type": "<type>", "content_summary": "<summary>", "tags": {...}}'
```

**Done.** Inform user of the exported PPTX path and that the design has been archived.

---

## Template Management Commands

These are user-invoked commands, not part of the main pipeline:

### /promote — Promote history to template

```bash
python3 ${SKILL_DIR}/scripts/template_manager.py promote \
  --history-dir history/ \
  --templates-dir templates/ \
  --id <history_entry_id> \
  --name "Template Name" \
  --tags tag1,tag2,tag3
```

### /templates — List available templates

```bash
python3 ${SKILL_DIR}/scripts/template_manager.py list --templates-dir templates/
```

### /history — List generation history

```bash
python3 ${SKILL_DIR}/scripts/template_manager.py history --history-dir history/
```

---

## Design Extraction Reference Files

Located in `reference/`:

| File | Purpose |
|------|---------|
| `format-spec.md` | 9-section DESIGN.md format specification |
| `style-references-spec.md` | 6-section STYLE-REFERENCES.md format |
| `extraction.js` | CSS token extraction script for Chrome DevTools |
| `example-stripe.md` | Exemplar DESIGN.md (quality calibration) |
| `example-stripe-references.md` | Exemplar STYLE-REFERENCES.md |
| `preview-template.html` | Light mode preview HTML template |
| `style-board-template.html` | Style board HTML template |
```

- [ ] **Step 2: Commit**

```bash
git add SKILL.md
git commit -m "feat: add SKILL.md — unified three-layer workflow for brand-aware PPT generation"
```

---

## Task 8: Modify Strategist Reference for Bridge Integration

**Files:**
- Modify: `skills/ppt-style-wow/references/strategist.md`

The Strategist needs to know how to consume the `design_spec_prefill.json` from the bridge.

- [ ] **Step 1: Read current strategist.md**

```bash
cat skills/ppt-style-wow/references/strategist.md
```

- [ ] **Step 2: Add prefill integration section**

Insert after the "## 1. Eight Confirmations Process" GATE instruction, before "### a. Canvas Format Confirmation":

```markdown
### Design Bridge Integration (when DESIGN.md is available)

When a `design_spec_prefill.json` exists in the project directory, the following confirmations are **auto-filled** from the extracted design system:

- **d. Style Objective** → from `style_objective` field
- **e. Color Scheme** → from `color_scheme` field (use semantic names, apply hex values directly)
- **f. Icon Usage** → from `icon_approach` field
- **g. Typography Plan** → from `typography` field (use `heading_fallback` and `body_fallback` for PPT font selection)
- **h. Image Strategy** → derived from `image_strategy` field

**Remaining user confirmations**: a. Canvas Format, b. Page Count, c. Key Information (target audience).

Present all 8 items as a bundled recommendation, with auto-filled items marked as "[Auto-filled from DESIGN.md]". The user can override any value.

**Decision Rules injection**: The `decision_rules` array from the prefill MUST be included in the design_spec.md output as an additional subsection under "III. Visual Theme". These rules are binding constraints for the Executor during SVG generation.
```

- [ ] **Step 3: Commit**

```bash
git add skills/ppt-style-wow/references/strategist.md
git commit -m "feat: add Design Bridge integration to Strategist reference"
```

---

## Task 9: Install Dependencies and Verify

**Files:** None (verification only)

- [ ] **Step 1: Install Python dependencies**

```bash
cd /Users/nigel/project/PPT-style-wow
pip install -r requirements.txt
```

- [ ] **Step 2: Run all tests**

```bash
python3 -m pytest tests/ -v
```

Expected: ALL PASS (test_design_bridge.py + test_template_manager.py)

- [ ] **Step 3: Verify design_bridge.py CLI works end-to-end**

```bash
python3 skills/ppt-style-wow/scripts/design_bridge.py tests/fixtures/sample_design.md -o /tmp/test_prefill.json
python3 -c "import json; d=json.load(open('/tmp/test_prefill.json')); print('Colors:', len(d['color_scheme']['semantic_names'])); print('Rules:', len(d['decision_rules'])); print('Font fallback:', d['typography']['heading_fallback'])"
```

Expected output:
```
Colors: 7
Rules: 6
Font fallback: Segoe UI Light
```

- [ ] **Step 4: Verify template_manager.py CLI works end-to-end**

```bash
mkdir -p /tmp/test_history /tmp/test_templates
# Archive
python3 -c "
import sys; sys.path.insert(0, 'skills/ppt-style-wow/scripts')
from template_manager import archive_to_history
from pathlib import Path
eid = archive_to_history(Path('/tmp/test_history'), Path('tests/fixtures/sample_design.md'), {'source_url': 'https://stripe.com', 'source_type': 'url', 'content_summary': 'test', 'tags': {'industry': ['tech']}, 'atmosphere': 'warm'})
print('Archived:', eid)
"
# List history
python3 skills/ppt-style-wow/scripts/template_manager.py history --history-dir /tmp/test_history
# Cleanup
rm -rf /tmp/test_history /tmp/test_templates /tmp/test_prefill.json
```

- [ ] **Step 5: Verify ppt-master scripts are importable**

```bash
python3 -c "import sys; sys.path.insert(0, 'skills/ppt-style-wow/scripts'); print('Scripts directory accessible')"
ls skills/ppt-style-wow/scripts/source_to_md/
ls skills/ppt-style-wow/references/
ls skills/ppt-style-wow/templates/layouts/ | head -5
```

- [ ] **Step 6: Final commit with all verification passing**

```bash
git add -A
git status
# If any unstaged files, add them
git commit -m "chore: verify all scripts, tests, and dependencies work end-to-end"
```

---

## Summary

| Task | What it builds | New files |
|------|---------------|-----------|
| 1 | Project scaffolding | `.gitignore`, `requirements.txt`, placeholder dirs |
| 2 | Design extraction refs | `reference/` (7 files from design.skill) |
| 3 | PPT generation engine | `skills/ppt-style-wow/` (scripts, references, templates from ppt-master) |
| 4 | DESIGN.md→Strategist bridge | `design_bridge.py` + tests |
| 5 | Template evolution | `template_manager.py` + tests |
| 6 | Project docs | `CLAUDE.md` |
| 7 | Main skill definition | `SKILL.md` |
| 8 | Strategist modification | Modified `strategist.md` |
| 9 | Verification | (no new files) |

**Total new code:** ~400 lines Python (design_bridge.py + template_manager.py), ~300 lines tests, ~400 lines SKILL.md, ~100 lines CLAUDE.md. Everything else is imported from the two source repos.
