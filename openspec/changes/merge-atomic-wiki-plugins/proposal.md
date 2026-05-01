## Why

The current architecture splits atomic-wiki functionality across two plugins: the main `atomic-wiki` agent plugin and a separate `atomic-wiki-memory` memory provider. The memory provider currently uses a brittle relative import (`../../atomic-wiki/tools.py`) to access the management CLI logic. Copying the logic would violate DRY. Consolidating the plugins simplifies the architecture, improves portability, and allows a single plugin to elegantly expose tools, hooks, and the memory provider.

## What Changes

- Consolidate the `atomic-wiki-memory` logic (read-only MemoryProvider, prefetch hooks) into the main `atomic-wiki` plugin.
- Migrate the `cli.py` logic from the memory provider directly into the main `atomic-wiki` plugin structure.
- Update `plugins/atomic-wiki/__init__.py` to call `ctx.register_memory_provider(AtomicWikiMemoryProvider())`.
- Delete the legacy `plugins/memory/atomic-wiki` directory completely.

## Capabilities

### New Capabilities
- `atomic-wiki-plugin-unification`: Unifies the agent tools, context hooks, and memory provider into a single distributable plugin.

### Modified Capabilities

## Impact

- **Code:** Removes the fragile relative path imports. Simplifies module discovery.
- **Dependencies:** None.
- **Configuration:** Users will only need to install and configure one plugin (`atomic-wiki`) instead of two.
