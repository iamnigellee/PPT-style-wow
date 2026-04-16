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
