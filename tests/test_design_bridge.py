import json, os, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "ppt-style-wow", "scripts"))
from design_bridge import parse_design_md, extract_colors, extract_typography, extract_decision_rules, map_font_fallback, generate_prefill

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "sample_design.md")

@pytest.fixture
def design_content():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return f.read()

class TestParseDesignMd:
    def test_returns_all_9_sections(self, design_content):
        sections = parse_design_md(design_content)
        for key in ["visual_theme","color_palette","typography","components","layout","depth","dos_donts","responsive","agent_guide"]:
            assert key in sections, f"Missing section: {key}"

    def test_visual_theme_contains_atmosphere(self, design_content):
        sections = parse_design_md(design_content)
        assert "engineered warmth" in sections["visual_theme"].lower()

    def test_handles_missing_section_gracefully(self):
        partial = "# Design System\n\n## 1. Visual Theme & Atmosphere\n\nMinimal.\n\n## 2. Color Palette & Roles\n\n- **Blue** (`#0000ff`): Primary.\n\n## 3. Typography Rules\n\nBody: Arial."
        sections = parse_design_md(partial)
        assert "visual_theme" in sections
        assert sections.get("components", "") == ""

class TestExtractColors:
    def test_extracts_hex_with_names(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        purple = next((c for c in colors if c["hex"] == "#533afd"), None)
        assert purple is not None
        assert purple["name"] == "Stripe Purple"

    def test_extracts_at_least_5_colors(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        assert len(colors) >= 5

    def test_extracts_role(self, design_content):
        sections = parse_design_md(design_content)
        colors = extract_colors(sections["color_palette"])
        purple = next((c for c in colors if c["hex"] == "#533afd"), None)
        assert "brand" in purple["role"].lower() or "CTA" in purple["role"]

class TestExtractTypography:
    def test_extracts_font_families(self, design_content):
        sections = parse_design_md(design_content)
        typo = extract_typography(sections["typography"])
        assert "sohne-var" in typo["heading_family"]
        assert "sohne" in typo["body_family"]

    def test_extracts_type_scale(self, design_content):
        sections = parse_design_md(design_content)
        typo = extract_typography(sections["typography"])
        assert len(typo["scale"]) >= 3
        display = next((s for s in typo["scale"] if s["purpose"].lower() == "display"), None)
        assert display is not None
        assert display["size"] == "56px"
        assert display["weight"] == "300"

class TestExtractDecisionRules:
    def test_extracts_at_least_6_rules(self, design_content):
        sections = parse_design_md(design_content)
        rules = extract_decision_rules(sections["visual_theme"])
        assert len(rules) >= 6

    def test_each_rule_has_dimension_and_description(self, design_content):
        sections = parse_design_md(design_content)
        rules = extract_decision_rules(sections["visual_theme"])
        for rule in rules:
            assert "dimension" in rule
            assert "description" in rule
            assert len(rule["dimension"]) > 0

class TestMapFontFallback:
    def test_maps_sohne_var(self):
        assert map_font_fallback("sohne-var") == "Segoe UI Light"
    def test_maps_sohne(self):
        assert map_font_fallback("sohne") == "Segoe UI"
    def test_passes_through_system_fonts(self):
        assert map_font_fallback("Arial") == "Arial"
    def test_passes_through_unknown(self):
        assert map_font_fallback("CustomBrandFont") == "CustomBrandFont"

class TestGeneratePrefill:
    def test_valid_structure(self, design_content):
        prefill = generate_prefill(design_content)
        for key in ["style_objective","color_scheme","typography","icon_approach","image_strategy","decision_rules"]:
            assert key in prefill

    def test_color_scheme_has_primary(self, design_content):
        prefill = generate_prefill(design_content)
        assert "primary" in prefill["color_scheme"]
        assert prefill["color_scheme"]["primary"].startswith("#")

    def test_typography_has_fallback(self, design_content):
        prefill = generate_prefill(design_content)
        assert prefill["typography"]["heading_fallback"] == "Segoe UI Light"

    def test_decision_rules_count(self, design_content):
        prefill = generate_prefill(design_content)
        assert isinstance(prefill["decision_rules"], list)
        assert len(prefill["decision_rules"]) >= 6
