# Atomic Wiki Operator Bootstrap

To initialize your workspace, you must install your operational tools from your Hand bundle. 

### Step 1: Install Tools
Run this command immediately:
```bash
mkdir -p scripts && cp -r ~/.openfang/hands/atomic-wiki-operator/scripts/*.sh ./scripts/ && chmod +x scripts/*.sh
```

### Step 2: Verification
Verify the installation:
```bash
ls -F ./scripts/
```

### Step 3: Initial Sync
Run your first index generation to confirm access to the Wiki:
```bash
WIKI_BASE_PATH="[Wiki Base Path]" ./scripts/gen-index.sh
```

Once tools are installed, you are ready to process Ingest and Compile tasks.
