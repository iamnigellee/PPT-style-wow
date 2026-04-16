"""
design_bridge.py — Parse DESIGN.md into a structured design_spec_prefill.json
for ppt-master's Strategist agent.

Usage:
    python3 design_bridge.py <DESIGN.md> [-o output.json]
"""

import re
import json
import sys
import os
import argparse
from typing import Optional

# ---------------------------------------------------------------------------
# Section key ordering (1-indexed in DESIGN.md)
# ---------------------------------------------------------------------------
SECTION_KEYS = [
    "visual_theme",    # 1
    "color_palette",   # 2
    "typography",      # 3
    "components",      # 4
    "layout",          # 5
    "depth",           # 6
    "dos_donts",       # 7
    "responsive",      # 8
    "agent_guide",     # 9
]

# ---------------------------------------------------------------------------
# Font fallback mapping
# ---------------------------------------------------------------------------
FONT_FALLBACK_MAP: dict[str, str] = {
    "sohne-var": "Segoe UI Light",
    "sohne": "Segoe UI",
    "inter": "Segoe UI",
    "roboto": "Arial",
    "open sans": "Calibri",
    "playfair display": "Georgia",
    "geist mono": "Consolas",  # must be before "geist"
    "geist": "Segoe UI",
}


def parse_design_md(content: str) -> dict[str, str]:
    """Split DESIGN.md into 9 named sections by matching '## N. Title' headings.

    Missing sections return an empty string.
    """
    # Split on any '## <digit(s)>.' heading
    parts = re.split(r"(?=^## \d+\. )", content, flags=re.MULTILINE)

    sections: dict[str, str] = {key: "" for key in SECTION_KEYS}

    for part in parts:
        m = re.match(r"^## (\d+)\. ", part)
        if not m:
            continue
        idx = int(m.group(1)) - 1  # 0-based
        if 0 <= idx < len(SECTION_KEYS):
            # Strip the heading line itself, keep the body
            body = re.sub(r"^## \d+\. [^\n]*\n?", "", part, count=1)
            sections[SECTION_KEYS[idx]] = body.strip()

    return sections


def extract_colors(color_section: str) -> list[dict]:
    """Extract colors from Section 2.

    Pattern: **Name** (`#hexcode`): role description
    Returns list of {"name", "hex", "role"}.
    """
    pattern = re.compile(
        r"\*\*([^*]+)\*\*\s+\(`(#[0-9a-fA-F]{3,8})`\):\s*(.+)"
    )
    colors = []
    for m in pattern.finditer(color_section):
        colors.append({
            "name": m.group(1).strip(),
            "hex": m.group(2).strip(),
            "role": m.group(3).strip(),
        })
    return colors


def extract_typography(typo_section: str) -> dict:
    """Extract fonts and type scale from Section 3.

    Returns {"heading_family", "body_family", "heading_fallback",
              "body_fallback", "scale": [{"purpose", "size", "weight", "line_height"}]}.
    """
    result: dict = {
        "heading_family": "",
        "body_family": "",
        "heading_fallback": "",
        "body_fallback": "",
        "scale": [],
    }

    # --- Font families ---
    heading_m = re.search(r"\*\*Heading:\*\*\s*(.+)", typo_section, re.IGNORECASE)
    body_m = re.search(r"\*\*Body:\*\*\s*(.+)", typo_section, re.IGNORECASE)

    if heading_m:
        result["heading_family"] = heading_m.group(1).strip()
        # First token before comma is the primary font name
        primary = result["heading_family"].split(",")[0].strip()
        result["heading_fallback"] = map_font_fallback(primary)

    if body_m:
        result["body_family"] = body_m.group(1).strip()
        primary = result["body_family"].split(",")[0].strip()
        result["body_fallback"] = map_font_fallback(primary)

    # --- Type scale: parse markdown table ---
    # Match table rows like: | Purpose | Size | Weight | Line Height |
    # Skip separator rows (---|---|...)
    table_row_pattern = re.compile(
        r"^\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
        re.MULTILINE,
    )
    scale = []
    for m in table_row_pattern.finditer(typo_section):
        purpose = m.group(1).strip()
        size = m.group(2).strip()
        weight = m.group(3).strip()
        line_height = m.group(4).strip()

        # Skip header row and separator row
        if purpose.lower() == "purpose" or re.match(r"^[-:]+$", purpose):
            continue
        if re.match(r"^[-:]+$", size):
            continue

        scale.append({
            "purpose": purpose,
            "size": size,
            "weight": weight,
            "line_height": line_height,
        })
    result["scale"] = scale

    return result


def extract_decision_rules(visual_theme_section: str) -> list[dict]:
    """Extract Design Decision Rules from Section 1.

    Pattern: - **Dimension:** description
    Returns list of {"dimension", "description"}.
    """
    pattern = re.compile(r"^- \*\*([^*:]+):\*\*\s*(.+)", re.MULTILINE)
    rules = []
    for m in pattern.finditer(visual_theme_section):
        rules.append({
            "dimension": m.group(1).strip(),
            "description": m.group(2).strip(),
        })
    return rules


def map_font_fallback(font_name: str) -> str:
    """Map web font names to PowerPoint system fonts.

    Unknown fonts pass through unchanged.
    """
    key = font_name.strip().lower()
    # Check longest-match first to avoid "geist" matching "geist mono"
    for web_font, system_font in FONT_FALLBACK_MAP.items():
        if key == web_font:
            return system_font
    return font_name  # pass through unchanged


def _assign_color_roles(colors: list[dict]) -> dict:
    """Assign semantic color roles (primary, background, text_primary, accent)
    by scanning role text for keywords."""
    role_map: dict[str, Optional[str]] = {
        "primary": None,
        "background": None,
        "text_primary": None,
        "accent": None,
    }

    keyword_priority = [
        # (role_key, keywords to check in role text)
        ("primary", ["primary brand", "primary", "brand"]),
        ("background", ["background", "hero"]),
        ("text_primary", ["body text", "body", "text"]),
        ("accent", ["accent", "highlight", "secondary"]),
    ]

    for color in colors:
        role_text = color["role"].lower()
        for role_key, keywords in keyword_priority:
            if role_map[role_key] is not None:
                continue  # already assigned
            for kw in keywords:
                if kw in role_text:
                    role_map[role_key] = color["hex"]
                    break

    return {k: v for k, v in role_map.items() if v is not None}


def _extract_style_objective(visual_theme_section: str) -> str:
    """Pull the atmosphere/intro paragraph from Section 1."""
    lines = visual_theme_section.splitlines()
    paragraphs = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            current.append(stripped)
        else:
            if current:
                paragraphs.append(" ".join(current))
                current = []
    if current:
        paragraphs.append(" ".join(current))
    # Return first non-empty paragraph (the atmosphere paragraph)
    for para in paragraphs:
        if para.startswith("###") or para.startswith("**"):
            continue
        if para.startswith("-"):
            continue
        return para
    return visual_theme_section.strip()


def _extract_icon_approach(components_section: str) -> str:
    """Pull the Icons subsection from Section 4."""
    m = re.search(
        r"### Icons\s*\n((?:(?!###).)+)",
        components_section,
        re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    return ""


def _extract_image_strategy(dos_donts_section: str) -> str:
    """Pull a summary of image strategy from Section 7 Do's and Don'ts."""
    # Return the full dos_donts section as the image_strategy for now
    return dos_donts_section.strip()


def generate_prefill(content: str) -> dict:
    """Full pipeline: parse → extract all → assemble prefill JSON structure."""
    sections = parse_design_md(content)

    colors = extract_colors(sections["color_palette"])
    typo = extract_typography(sections["typography"])
    rules = extract_decision_rules(sections["visual_theme"])

    # Color scheme
    role_assignments = _assign_color_roles(colors)
    semantic_names = {c["name"]: {"hex": c["hex"], "role": c["role"]} for c in colors}
    color_scheme = {**role_assignments, "semantic_names": semantic_names}

    # Style objective from Section 1
    style_objective = _extract_style_objective(sections["visual_theme"])

    # Icon approach from Section 4
    icon_approach = _extract_icon_approach(sections["components"])

    # Image strategy from Section 7
    image_strategy = _extract_image_strategy(sections["dos_donts"])

    return {
        "style_objective": style_objective,
        "color_scheme": color_scheme,
        "typography": typo,
        "icon_approach": icon_approach,
        "image_strategy": image_strategy,
        "decision_rules": rules,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse DESIGN.md into a Strategist prefill JSON."
    )
    parser.add_argument("design_md", help="Path to the DESIGN.md file")
    parser.add_argument(
        "-o", "--output",
        help="Output JSON path (default: <input_dir>/design_spec_prefill.json)",
        default=None,
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.design_md)
    if not os.path.isfile(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    prefill = generate_prefill(content)

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        input_dir = os.path.dirname(input_path)
        output_path = os.path.join(input_dir, "design_spec_prefill.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prefill, f, indent=2, ensure_ascii=False)

    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
