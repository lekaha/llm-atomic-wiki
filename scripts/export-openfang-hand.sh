#!/usr/bin/env bash
set -e

# export-openfang-hand.sh
# Generates the OpenFang native agent Hand bundle for this repository

if [ -z "$1" ]; then
    TARGET_DIR="."
else
    TARGET_DIR="$1"
fi

HAND_DIR="$TARGET_DIR/atomic-wiki-operator"
mkdir -p "$HAND_DIR"

# Get absolute path to the repo root to resolve CLAUDE.md reliably
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Generating HAND.toml in $HAND_DIR..."
cat > "$HAND_DIR/HAND.toml" << 'EOF'
id = "atomic-wiki-operator"
name = "Atomic Wiki Operator"
description = "Autonomous agent that ingests raw material, compiles wiki pages, and performs linting for the atomic knowledge base."
category = "productivity"
icon = "📚"
version = "1.0.0"
tools = ["shell_exec", "file_read", "file_write", "file_list", "schedule_create", "schedule_list", "schedule_delete"]

[[settings]]
key = "wiki_base_path"
label = "Wiki Base Path"
description = "Base directory of the atomic wiki (where raw, atoms, and wiki folders exist)."
setting_type = "text"
default = ""

[[settings]]
key = "maintenance_schedule"
label = "Maintenance Schedule"
description = "When to automatically run linting and index regeneration"
setting_type = "select"
default = "daily_3am"

[[settings.options]]
value = "hourly"
label = "Every hour"

[[settings.options]]
value = "daily_3am"
label = "Daily at 3 AM"

[[settings.options]]
value = "weekdays_midnight"
label = "Weekdays at midnight"

[[settings.options]]
value = "manual"
label = "Manual only"

[agent]
name = "atomic-wiki-operator"
description = "Autonomous agent that ingests raw material, compiles wiki pages, and performs linting for the atomic knowledge base."
module = "builtin:chat"
model = "gemini-3.1-flash-lite-preview"
temperature = 0.3
max_iterations = 25
system_prompt = """You are the Atomic Wiki Operator for this repository. 
Your job is to manage the knowledge base according to the rigid structure defined in your SKILL.md.

**CRITICAL:** The Wiki repository is located at the directory specified by your `wiki_base_path` setting. You MUST resolve all your file paths securely to this base path, or `cd` into this path before executing any shell commands!

## Phase 0: Initialization & Scheduling
On your first run or if requested to update settings:
1. Use `schedule_list` to see existing schedules.
2. If `maintenance_schedule` is not "manual", use `schedule_create` to ensure a recurring task exists for this Hand based on the setting.
3. Cleanup old/duplicate schedules using `schedule_delete` if necessary.

## Phase 1: Operational Checks
When taking any action, you MUST follow the 4 operations:
1. Ingest: Extract atoms from raw sources.
2. Compile: Group atoms into flat wiki pages.
3. Query: Search the index.md and wiki pages to answer questions.
4. Lint: Run post-changes health checks.

## Phase 2: Knowledge Base Integrity
After ANY modification to the knowledge base (after ingesting, compiling, or modifying any wiki files), you MUST execute the operational scripts located in your Hand's scripts directory in order using the shell_exec tool. You MUST pass the `wiki_base_path` setting via the WIKI_BASE_PATH environment variable:
`WIKI_BASE_PATH="<wiki_base_path>" ./scripts/gen-index.sh`
`WIKI_BASE_PATH="<wiki_base_path>" ./scripts/log-append.sh "Brief description of changes"`
`WIKI_BASE_PATH="<wiki_base_path>" ./scripts/lint.sh`

Wait for execution of each script before proceeding. Ensure you follow all constraints specified in your SKILL.md exactly."""
EOF

echo "Generating SKILL.md in $HAND_DIR..."
cat > "$HAND_DIR/SKILL.md" << 'EOF'
---
name: atomic-wiki-operator-skill
version: "1.0.0"
description: "Rules, structures, and operations for managing the Atomic Wiki."
runtime: prompt_only
---

EOF

cat "$REPO_ROOT/CLAUDE.md" >> "$HAND_DIR/SKILL.md"

echo "Copying operational scripts into Hand bundle..."
mkdir -p "$HAND_DIR/scripts"
cp "$REPO_ROOT/scripts/gen-index.sh" "$HAND_DIR/scripts/"
cp "$REPO_ROOT/scripts/log-append.sh" "$HAND_DIR/scripts/"
cp "$REPO_ROOT/scripts/lint.sh" "$HAND_DIR/scripts/"

echo "Success! OpenFang Hand exported to $HAND_DIR."
