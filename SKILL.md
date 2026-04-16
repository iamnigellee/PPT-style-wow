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
7. Answer the identity + reproducibility questions (see `reference/format-spec.md`)
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

**✅ Checkpoint — DESIGN.md ready. Proceed to Step 2.**

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

**✅ Checkpoint — Source content ready. Proceed to Step 3.**

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

**✅ Checkpoint — Template selected. Proceed to Step 3.**

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

**✅ Checkpoint — Project structure created. Proceed to Step 4.**

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

**✅ Checkpoint — Design spec complete. Auto-proceed to Step 5.**

---

## Step 5: Image Generation (Optional)

🚧 **GATE**: Step 4 complete. design_spec.md mentions image needs.

Read `${SKILL_DIR}/references/image-generator.md` for the Image_Generator role definition.

Generate images as needed using the design system colors and style:
```bash
python3 ${SKILL_DIR}/scripts/image_gen.py "prompt matching brand style" --aspect_ratio 16:9 -o <project_path>/images
```

**✅ Checkpoint — Images ready (or skipped). Proceed to Step 6.**

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

**✅ Checkpoint — All SVG pages generated. Proceed to Step 7.**

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

**✅ Checkpoint — PPTX exported. Proceed to Step 8.**

---

## Step 8: Silent Archive

🚧 **GATE**: Step 7 complete. PPTX exported successfully.

Archive this generation to history (automatic, no user action needed):

The AI should call the archive function with appropriate metadata extracted from the generation:
- source_url (if URL entry)
- source_type (url/screenshot/design_md/template)
- content_summary (brief description of the PPT content)
- tags (industry, style, scene inferred from content)
- atmosphere (from DESIGN.md §1)
- decision_rules_digest (key rule names from DESIGN.md §1)

```bash
python3 ${SKILL_DIR}/scripts/template_manager.py archive \
  --history-dir history/ \
  --design-md <project_path>/design/DESIGN.md \
  --metadata '{"source_url":"<url>","source_type":"<type>","content_summary":"<summary>","tags":{"industry":[],"style":[],"scene":[]},"atmosphere":"<atmosphere>","decision_rules_digest":[]}'
```

**Done.** Inform user of the exported PPTX path and that the design has been archived to history.

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
