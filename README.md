# PPT-style-wow

AI-driven presentation generation system with brand-aware design extraction. Extract the visual DNA from any website, then generate native-editable PPTX files that match the brand — all through Claude Code.

## How It Works

```
Website/Screenshot ──→ DESIGN.md ──→ Strategist ──→ Executor ──→ SVG ──→ PPTX
                       (design system)  (spec)       (pages)     (post)  (export)
```

**Three entry points:**

| You have | What happens |
|----------|-------------|
| Website URL + source doc | Extracts design system → generates brand-consistent PPTX |
| Existing DESIGN.md + source doc | Skips extraction → generates PPTX directly |
| Source doc only | Matches from template library or free design |

## Installation

### Prerequisites

- Python 3.10+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Chrome (for design extraction via DevTools MCP)

### Setup

```bash
# Clone
git clone https://github.com/user/PPT-style-wow.git
cd PPT-style-wow

# Install Python dependencies
pip install -r requirements.txt

# Install as Claude Code skill
./install.sh
```

This installs the skill to `~/.claude/skills/ppt-style-wow/`, making it available in any Claude Code session.

## Usage

In Claude Code, simply describe what you need:

```
# From a website style
"用 Stripe 官网的风格，把这个 PDF 做成 PPT"
"Create a presentation matching the Airbnb website style from this document"

# From an existing design system
"Use this DESIGN.md and turn my notes into slides"

# No style preference
"Make a presentation from this PDF"
```

The skill handles the full pipeline: source conversion → design extraction → strategist review → page generation → PPTX export.

## Project Structure

```
PPT-style-wow/
├── SKILL.md                          # Skill definition (workflow & rules)
├── CLAUDE.md                         # AI agent instructions
├── install.sh                        # Skill installer
├── requirements.txt                  # Python dependencies
│
├── reference/                        # Design extraction layer
│   ├── format-spec.md                #   DESIGN.md format specification
│   ├── style-references-spec.md      #   STYLE-REFERENCES.md format
│   ├── extraction.js                 #   CSS token extraction (Chrome DevTools)
│   ├── example-stripe.md             #   Exemplar DESIGN.md
│   ├── example-stripe-references.md  #   Exemplar STYLE-REFERENCES.md
│   └── preview-template.html         #   Preview HTML template
│
├── skills/ppt-style-wow/
│   ├── scripts/                      # PPT generation engine
│   │   ├── source_to_md/             #   Source converters (PDF, DOCX, PPTX, Web)
│   │   ├── project_manager.py        #   Project init & source import
│   │   ├── design_bridge.py          #   DESIGN.md → Strategist prefill
│   │   ├── image_gen.py              #   AI image generation
│   │   ├── analyze_images.py         #   Image analysis for spec
│   │   ├── total_md_split.py         #   Post-processing: split speaker notes
│   │   ├── finalize_svg.py           #   Post-processing: finalize SVGs
│   │   ├── svg_to_pptx.py            #   Post-processing: export PPTX
│   │   └── template_manager.py       #   Template archive/promote/match
│   ├── references/                   #   Role definitions (Strategist, Executor, etc.)
│   ├── templates/                    #   SVG component templates (layouts, charts, icons)
│   └── workflows/                    #   Workflow definitions
│
├── templates/                        # Reusable template library
├── history/                          # Generation archive
├── projects/                         # Active project workspaces
├── tests/                            # Test suite
└── docs/                             # Documentation
```

## Key Concepts

### Design Extraction

Navigates to a target website via Chrome DevTools, runs CSS token extraction, captures screenshots, and produces a structured `DESIGN.md` with 9 sections: theme, colors, typography, components, spacing, imagery, do's/don'ts, and decision rules.

### Strategist Phase

Takes the extracted design system and auto-fills a design spec. The user only needs to confirm 3 things: canvas format, page count, and target audience. Everything else is derived from the brand.

### Executor Phase

Generates SVG pages one at a time, strictly following the design spec and brand decision rules. SVGs use a PPT-compatible subset (no `<style>`, `mask`, `foreignObject`, etc.) to ensure clean PPTX conversion.

### Template Evolution

Every generation is silently archived. Users can promote good designs to the template library, building a reusable collection that improves over time.

## Canvas Formats

| Format | Dimensions |
|--------|-----------|
| PPT 16:9 | 1280 × 720 |
| PPT 4:3 | 1024 × 768 |
| Xiaohongshu | 1242 × 1660 |
| WeChat Moments | 1080 × 1080 |

## CLI Commands Reference

### Source Conversion

```bash
python3 skills/ppt-style-wow/scripts/source_to_md/pdf_to_md.py <file>
python3 skills/ppt-style-wow/scripts/source_to_md/doc_to_md.py <file>
python3 skills/ppt-style-wow/scripts/source_to_md/ppt_to_md.py <file>
python3 skills/ppt-style-wow/scripts/source_to_md/web_to_md.py <URL>
```

### Project Management

```bash
python3 skills/ppt-style-wow/scripts/project_manager.py init <name> --format ppt169
python3 skills/ppt-style-wow/scripts/project_manager.py import-sources <path> <files...> --move
```

### Template Management

```bash
python3 skills/ppt-style-wow/scripts/template_manager.py list --templates-dir templates/
python3 skills/ppt-style-wow/scripts/template_manager.py history --history-dir history/
python3 skills/ppt-style-wow/scripts/template_manager.py promote --history-dir history/ --templates-dir templates/ --id <id> --name "Name" --tags tag1,tag2
python3 skills/ppt-style-wow/scripts/template_manager.py match --templates-dir templates/ --tags tag1,tag2
```

### Post-processing (run sequentially)

```bash
python3 skills/ppt-style-wow/scripts/total_md_split.py <project_path>
python3 skills/ppt-style-wow/scripts/finalize_svg.py <project_path>
python3 skills/ppt-style-wow/scripts/svg_to_pptx.py <project_path> -s final
```

## License

MIT
