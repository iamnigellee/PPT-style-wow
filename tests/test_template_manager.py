import json, os, sys, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "ppt-style-wow", "scripts"))
from template_manager import archive_to_history, promote_to_template, list_templates, list_history, match_templates_by_tags, remove_template, slugify

@pytest.fixture
def workspace(tmp_path):
    (tmp_path / "history").mkdir()
    (tmp_path / "templates").mkdir()
    return tmp_path

@pytest.fixture
def sample_design_md(tmp_path):
    d = tmp_path / "DESIGN.md"
    d.write_text("# Design System\n\n## 1. Visual Theme\n\nEngineered warmth.")
    return d

@pytest.fixture
def sample_metadata():
    return {
        "source_url": "https://stripe.com",
        "source_type": "url",
        "content_summary": "Q3 financial report",
        "tags": {"industry": ["fintech", "saas"], "style": ["minimalist", "tech"], "scene": ["report"]},
        "atmosphere": "Engineered warmth",
        "decision_rules_digest": ["emphasis-by-lightness", "blue-tinted-depth"],
    }

class TestSlugify:
    def test_chinese(self):
        assert slugify("科技极简风") == "科技极简风"
    def test_ascii(self):
        assert slugify("Tech Minimalist") == "tech-minimalist"
    def test_special_chars(self):
        assert slugify("Hello, World!") == "hello-world"

class TestArchiveToHistory:
    def test_creates_entry(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        assert (workspace/"history"/eid).exists()
        assert (workspace/"history"/eid/"DESIGN.md").exists()
        assert (workspace/"history"/eid/"metadata.json").exists()

    def test_metadata_fields(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        meta = json.loads((workspace/"history"/eid/"metadata.json").read_text())
        assert "id" in meta and "created_at" in meta and "source_url" in meta

    def test_copies_style_refs(self, workspace, sample_design_md, sample_metadata):
        refs = sample_design_md.parent / "STYLE-REFERENCES.md"
        refs.write_text("# Style References")
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata, style_references_path=refs)
        assert (workspace/"history"/eid/"STYLE-REFERENCES.md").exists()

class TestPromoteToTemplate:
    def test_promotes(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        slug = promote_to_template(workspace/"history", workspace/"templates", eid, "科技极简风", tags=["tech","minimalist"])
        assert (workspace/"templates"/slug/"DESIGN.md").exists()
        meta = json.loads((workspace/"templates"/slug/"metadata.json").read_text())
        assert meta["name"] == "科技极简风"
        assert meta["usage_count"] == 0

    def test_raises_missing(self, workspace):
        with pytest.raises(FileNotFoundError):
            promote_to_template(workspace/"history", workspace/"templates", "nonexistent", "test")

class TestListTemplates:
    def test_empty(self, workspace):
        assert list_templates(workspace/"templates") == []

    def test_lists_promoted(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        promote_to_template(workspace/"history", workspace/"templates", eid, "科技极简风")
        result = list_templates(workspace/"templates")
        assert len(result) == 1 and result[0]["name"] == "科技极简风"

class TestMatchByTags:
    def test_matches(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        promote_to_template(workspace/"history", workspace/"templates", eid, "FinTech", tags=["fintech","minimalist"])
        matches = match_templates_by_tags(workspace/"templates", ["fintech"])
        assert len(matches) == 1

    def test_no_match(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        promote_to_template(workspace/"history", workspace/"templates", eid, "FinTech", tags=["fintech"])
        assert match_templates_by_tags(workspace/"templates", ["healthcare"]) == []

class TestRemoveTemplate:
    def test_removes(self, workspace, sample_design_md, sample_metadata):
        eid = archive_to_history(workspace/"history", sample_design_md, sample_metadata)
        slug = promote_to_template(workspace/"history", workspace/"templates", eid, "ToRemove")
        remove_template(workspace/"templates", slug)
        assert not (workspace/"templates"/slug).exists()

    def test_raises_missing(self, workspace):
        with pytest.raises(FileNotFoundError):
            remove_template(workspace/"templates", "nonexistent")
