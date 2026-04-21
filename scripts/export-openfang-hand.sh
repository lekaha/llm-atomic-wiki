#!/usr/bin/env bash
set -e

# export-openfang-hand.sh
# Generates a self-bootstrapping OpenFang Hand bundle

if [ -z "$1" ]; then
    TARGET_DIR="."
else
    TARGET_DIR="$1"
fi

HAND_DIR="$TARGET_DIR/atomic-wiki-operator"
mkdir -p "$HAND_DIR/scripts"

# Get absolute path to the repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Copying scripts to bundle..."
cp "$REPO_ROOT/scripts/gen-index.sh" "$HAND_DIR/scripts/"
cp "$REPO_ROOT/scripts/log-append.sh" "$HAND_DIR/scripts/"
cp "$REPO_ROOT/scripts/lint.sh" "$HAND_DIR/scripts/"

echo "Generating HAND.toml..."
cat > "$HAND_DIR/HAND.toml" << 'EOF'
id = "atomic-wiki-operator"
name = "Atomic Wiki Operator"
description = "Autonomous agent that ingests raw material, compiles wiki pages, and performs linting. Self-bootstraps its own operational tools."
category = "productivity"
icon = "📚"
version = "1.2.0"
tools = ["shell_exec", "file_read", "file_write", "file_list", "schedule_create", "schedule_list", "schedule_delete"]

[[settings]]
key = "wiki_base_path"
label = "Wiki Base Path"
description = "The absolute path to the llm-atomic-wiki repository root."
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
description = "Autonomous operator for the Atomic Wiki."
module = "builtin:chat"
provider = "gemini"
model = "gemini-3.1-flash-lite-preview"
temperature = 0.1
max_iterations = 25
system_prompt = """You are the Atomic Wiki Operator. 

## Context Awareness
You manage a wiki repository at the path specified in your **Wiki Base Path** setting.
Your operational scripts (tools) are cached in your local `./scripts/` directory.

## Core Rules
1. **Always change directory** to the `Wiki Base Path` before performing wiki operations.
2. If `./scripts/` is empty, run your **Bootstrap** procedure (see your soul/memories).
3. Always prefix wiki paths (raw/, atoms/, wiki/) with the `Wiki Base Path`.

## Knowledge Maintenance
After ANY modification to the knowledge base, you MUST run these scripts in order:
1. `WIKI_BASE_PATH="[Wiki Base Path]" "./scripts/gen-index.sh"` (Executed from the workspace, but targeting the wiki)
2. `WIKI_BASE_PATH="[Wiki Base Path]" "./scripts/log-append.sh" "[Description]"`
3. `WIKI_BASE_PATH="[Wiki Base Path]" "./scripts/lint.sh"`

Execute these relative to your workspace root."""
EOF

echo "Generating SKILL.md..."
cat > "$HAND_DIR/SKILL.md" << 'EOF'
---
name: atomic-wiki-operator-skill
version: "1.2.0"
description: "Rules, structures, and operations for managing the Atomic Wiki."
runtime: prompt_only
---

EOF
cat "$REPO_ROOT/CLAUDE.md" >> "$HAND_DIR/SKILL.md"

echo "Generating BOOTSTRAP.md..."
cat > "$HAND_DIR/BOOTSTRAP.md" << 'EOF'
# Atomic Wiki Operator Bootstrap

To initialize your workspace, you must install your operational tools. 

### Step 1: Discover Tools
Check these locations in order to find where your source `.sh` scripts are located:
1. Primary: `~/.openfang/hands/atomic-wiki-operator/scripts/`
2. Fallback: `[Wiki Base Path]/scripts/`

### Step 2: Install Tools
Once you've located the source, run this command to populate your workspace:
```bash
mkdir -p scripts && cp -r [SOURCE_PATH]/*.sh ./scripts/ && chmod +x scripts/*.sh
```

### Step 3: Verification
Verify that `./scripts/gen-index.sh` is now present and executable.

### Step 4: Maintenance Setup
If your `Maintenance Schedule` is not "manual", use `schedule_create` to register a recurring task that runs `./scripts/gen-index.sh` and `./scripts/lint.sh`.

Once tools are installed, you are ready to process Ingest and Compile tasks.
EOF

echo "Success! OpenFang Hand (v1.2.0) exported to $HAND_DIR."
echo "The bundle now contains its own scripts and will self-install them into the agent workspace."
