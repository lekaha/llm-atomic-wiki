## 1. Project Scaffolding

- [x] 1.1 Create `plugins/memory/atomic-wiki/` directory structure.
- [x] 1.2 Create `plugin.yaml` specifying name and hooks (`prefetch`, `system_prompt_block`).

## 2. Core Provider Implementation

- [x] 2.1 Implement `get_config_schema` to prompt for `wiki_dirs` (comma-separated).
- [x] 2.2 Implement `initialize` to load search capabilities across all configured `wiki_dirs`.
- [x] 2.3 Implement `prefetch` hook to query the wiki and inject context.
- [x] 2.4 Implement `system_prompt_block` to instruct Hermes on how to use read-only context.
- [x] 2.5 Implement `sync_turn` and `on_memory_write` as no-ops (`pass`).

## 3. Read-Only Tools

- [x] 3.1 Implement `wiki_search` tool schema and handler in `get_tool_schemas` and `handle_tool_call`.
- [x] 3.2 Implement `wiki_read` tool schema and handler.

## 4. CLI Implementation

- [x] 4.1 Create `cli.py` to register custom commands for `atomic-wiki`.
- [x] 4.2 Implement `hermes atomic-wiki status` command.
- [x] 4.3 Implement `hermes atomic-wiki index` command for manual re-indexing.

## 5. Testing

- [x] 5.1 Write automated E2E tests for `AtomicWikiMemoryProvider` ensuring tools are routed and hooks fire correctly.
- [x] 5.2 Validate that `sync_turn` and `on_memory_write` do not modify the file system.
