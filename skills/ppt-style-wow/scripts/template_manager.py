"""
template_manager.py — Manages PPT-style-wow template evolution layer.

Provides:
  - slugify: Convert text to filesystem-safe slug
  - archive_to_history: Archive DESIGN.md + metadata to history/
  - promote_to_template: Promote a history entry to templates/
  - list_templates: List all templates sorted alphabetically
  - list_history: List all history entries sorted newest-first
  - match_templates_by_tags: Phase-1 tag-based template matching
  - remove_template: Remove a template directory

CLI subcommands: history, list, promote, match, remove
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to filesystem-safe slug.

    - Non-ASCII characters (e.g. Chinese) are preserved as-is.
    - ASCII letters are lowercased.
    - Spaces and non-alphanumeric ASCII characters are replaced with hyphens.
    - Consecutive hyphens are collapsed; leading/trailing hyphens are stripped.
    """
    result: list[str] = []
    for ch in text:
        if ord(ch) > 127:
            # Non-ASCII: preserve
            result.append(ch)
        elif ch.isalpha() or ch.isdigit():
            result.append(ch.lower())
        else:
            result.append("-")

    slug = "".join(result)
    # Collapse consecutive hyphens
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


# ---------------------------------------------------------------------------
# archive_to_history
# ---------------------------------------------------------------------------

def archive_to_history(
    history_dir: Path,
    design_md_path: Path,
    metadata: dict,
    style_references_path: Optional[Path] = None,
    design_spec_path: Optional[Path] = None,
) -> str:
    """Copy DESIGN.md + metadata.json to history/<timestamp>-<slug>/.

    Adds "id" and "created_at" to metadata.json.
    Optionally copies STYLE-REFERENCES.md and design_spec.md.

    Returns the entry_id (directory name).
    """
    history_dir = Path(history_dir)
    design_md_path = Path(design_md_path)

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")

    # Derive slug from content_summary or source_url
    slug_source = metadata.get("content_summary") or metadata.get("source_url", "entry")
    slug = slugify(slug_source)[:60]  # cap length

    entry_id = f"{timestamp}-{slug}"
    entry_dir = history_dir / entry_id
    entry_dir.mkdir(parents=True, exist_ok=True)

    # Copy DESIGN.md
    shutil.copy2(design_md_path, entry_dir / "DESIGN.md")

    # Optional files
    if style_references_path is not None:
        shutil.copy2(Path(style_references_path), entry_dir / "STYLE-REFERENCES.md")
    if design_spec_path is not None:
        shutil.copy2(Path(design_spec_path), entry_dir / "design_spec.md")

    # Write metadata.json (mutate a copy, keep original dict clean)
    meta_out = dict(metadata)
    meta_out["id"] = entry_id
    meta_out["created_at"] = now.isoformat()
    (entry_dir / "metadata.json").write_text(
        json.dumps(meta_out, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return entry_id


# ---------------------------------------------------------------------------
# promote_to_template
# ---------------------------------------------------------------------------

def promote_to_template(
    history_dir: Path,
    templates_dir: Path,
    entry_id: str,
    name: str,
    tags: Optional[list[str]] = None,
) -> str:
    """Copy history entry to templates/<slug>/.

    Adds name, usage_count=0, promoted_at to metadata.
    If tags provided, adds as tags.custom.

    Returns the slug.
    Raises FileNotFoundError if history entry is missing.
    """
    history_dir = Path(history_dir)
    templates_dir = Path(templates_dir)

    entry_dir = history_dir / entry_id
    if not entry_dir.exists():
        raise FileNotFoundError(f"History entry not found: {entry_dir}")

    slug = slugify(name)
    template_dir = templates_dir / slug
    shutil.copytree(entry_dir, template_dir, dirs_exist_ok=True)

    # Update metadata
    meta_path = template_dir / "metadata.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    else:
        meta = {}

    meta["name"] = name
    meta["usage_count"] = 0
    meta["promoted_at"] = datetime.now(timezone.utc).isoformat()

    if tags:
        existing_tags = meta.get("tags", {})
        if isinstance(existing_tags, dict):
            existing_tags["custom"] = tags
        else:
            existing_tags = {"custom": tags}
        meta["tags"] = existing_tags

    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return slug


# ---------------------------------------------------------------------------
# list_templates
# ---------------------------------------------------------------------------

def list_templates(templates_dir: Path) -> list[dict]:
    """Return metadata of all templates sorted alphabetically by directory name."""
    templates_dir = Path(templates_dir)
    results: list[dict] = []

    for entry in sorted(templates_dir.iterdir()):
        if entry.is_dir():
            meta_path = entry / "metadata.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                results.append(meta)

    return results


# ---------------------------------------------------------------------------
# list_history
# ---------------------------------------------------------------------------

def list_history(history_dir: Path) -> list[dict]:
    """Return metadata of all history entries sorted newest-first."""
    history_dir = Path(history_dir)
    results: list[dict] = []

    for entry in history_dir.iterdir():
        if entry.is_dir():
            meta_path = entry / "metadata.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                results.append(meta)

    # Sort newest-first by created_at (ISO strings sort lexicographically)
    results.sort(key=lambda m: m.get("created_at", ""), reverse=True)
    return results


# ---------------------------------------------------------------------------
# match_templates_by_tags
# ---------------------------------------------------------------------------

def match_templates_by_tags(
    templates_dir: Path,
    query_tags: list[str],
    top_n: int = 5,
) -> list[dict]:
    """Phase-1 tag matching.

    Collect all tags from template metadata (across all tag categories),
    count overlap with query_tags, return sorted by overlap descending.
    Only templates with overlap > 0 are included.
    """
    templates_dir = Path(templates_dir)
    query_set = set(query_tags)
    scored: list[tuple[int, dict]] = []

    for entry in templates_dir.iterdir():
        if not entry.is_dir():
            continue
        meta_path = entry / "metadata.json"
        if not meta_path.exists():
            continue

        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        tags_field = meta.get("tags", {})

        # Collect all tag values across all categories
        all_tags: set[str] = set()
        if isinstance(tags_field, dict):
            for values in tags_field.values():
                if isinstance(values, list):
                    all_tags.update(values)
        elif isinstance(tags_field, list):
            all_tags.update(tags_field)

        overlap = len(query_set & all_tags)
        if overlap > 0:
            scored.append((overlap, meta))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored[:top_n]]


# ---------------------------------------------------------------------------
# remove_template
# ---------------------------------------------------------------------------

def remove_template(templates_dir: Path, slug: str) -> None:
    """Remove template directory.

    Raises FileNotFoundError if template is missing.
    """
    templates_dir = Path(templates_dir)
    template_dir = templates_dir / slug
    if not template_dir.exists():
        raise FileNotFoundError(f"Template not found: {template_dir}")
    shutil.rmtree(template_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="template_manager",
        description="Manage PPT-style-wow template evolution layer.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # history subcommand
    p_history = sub.add_parser("history", help="List history entries")
    p_history.add_argument("history_dir", type=Path, help="Path to history/ directory")

    # list subcommand
    p_list = sub.add_parser("list", help="List templates")
    p_list.add_argument("templates_dir", type=Path, help="Path to templates/ directory")

    # promote subcommand
    p_promote = sub.add_parser("promote", help="Promote a history entry to a template")
    p_promote.add_argument("history_dir", type=Path)
    p_promote.add_argument("templates_dir", type=Path)
    p_promote.add_argument("entry_id", help="History entry ID")
    p_promote.add_argument("name", help="Template display name")
    p_promote.add_argument("--tags", nargs="*", default=None, help="Custom tags")

    # match subcommand
    p_match = sub.add_parser("match", help="Match templates by tags")
    p_match.add_argument("templates_dir", type=Path)
    p_match.add_argument("tags", nargs="+", help="Query tags")
    p_match.add_argument("--top-n", type=int, default=5)

    # remove subcommand
    p_remove = sub.add_parser("remove", help="Remove a template")
    p_remove.add_argument("templates_dir", type=Path)
    p_remove.add_argument("slug", help="Template slug to remove")

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "history":
        entries = list_history(args.history_dir)
        print(json.dumps(entries, ensure_ascii=False, indent=2))

    elif args.command == "list":
        templates = list_templates(args.templates_dir)
        print(json.dumps(templates, ensure_ascii=False, indent=2))

    elif args.command == "promote":
        slug = promote_to_template(
            args.history_dir,
            args.templates_dir,
            args.entry_id,
            args.name,
            tags=args.tags,
        )
        print(f"Promoted to template slug: {slug}")

    elif args.command == "match":
        matches = match_templates_by_tags(args.templates_dir, args.tags, top_n=args.top_n)
        print(json.dumps(matches, ensure_ascii=False, indent=2))

    elif args.command == "remove":
        remove_template(args.templates_dir, args.slug)
        print(f"Removed template: {args.slug}")


if __name__ == "__main__":
    main()
