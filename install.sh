#!/usr/bin/env bash
# Install the ppt-style-wow skill into ~/.claude/skills/
# so Claude Code can load it by name.

set -euo pipefail

SKILL_NAME="ppt-style-wow"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/$SKILL_NAME"

if [[ ! -f "$SRC_DIR/SKILL.md" ]]; then
  echo "error: SKILL.md not found in $SRC_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

# Core skill file
cp "$SRC_DIR/SKILL.md" "$DEST_DIR/SKILL.md"

# Design extraction references
rm -rf "$DEST_DIR/reference"
cp -R "$SRC_DIR/reference" "$DEST_DIR/reference"

# PPT generation engine (scripts, references, templates, workflows)
rm -rf "$DEST_DIR/skills"
mkdir -p "$DEST_DIR/skills/ppt-style-wow"
cp -R "$SRC_DIR/skills/ppt-style-wow/scripts" "$DEST_DIR/skills/ppt-style-wow/scripts"
cp -R "$SRC_DIR/skills/ppt-style-wow/references" "$DEST_DIR/skills/ppt-style-wow/references"
cp -R "$SRC_DIR/skills/ppt-style-wow/templates" "$DEST_DIR/skills/ppt-style-wow/templates"
cp -R "$SRC_DIR/skills/ppt-style-wow/workflows" "$DEST_DIR/skills/ppt-style-wow/workflows"

echo "installed: $DEST_DIR"
echo ""
echo "file counts:"
echo "  reference/        $(find "$DEST_DIR/reference" -type f | wc -l | tr -d ' ') files"
echo "  scripts/          $(find "$DEST_DIR/skills/ppt-style-wow/scripts" -type f | wc -l | tr -d ' ') files"
echo "  references/       $(find "$DEST_DIR/skills/ppt-style-wow/references" -type f | wc -l | tr -d ' ') files"
echo "  templates/        $(find "$DEST_DIR/skills/ppt-style-wow/templates" -type f | wc -l | tr -d ' ') files"
echo ""
echo "done. skill '$SKILL_NAME' is now available in Claude Code."
