## Context

The current `llm-atomic-wiki` architecture splits atomic-wiki functionality across two plugins: the main `atomic-wiki` agent plugin and a separate `atomic-wiki-memory` memory provider. The memory provider currently uses a brittle relative import (`../../atomic-wiki/tools.py`) to access the management CLI logic. Copying the logic would violate DRY. Consolidating the plugins simplifies the architecture, improves portability, and allows a single plugin to elegantly expose tools, hooks, and the memory provider.

## Goals / Non-Goals

**Goals:**
- Unify the agent tools, context hooks, and memory provider into a single distributable plugin.
- Remove fragile relative path imports.
- Make the plugin fully standalone.

**Non-Goals:**
- Changing the behavior of the `atomic-wiki` tools (indexing, linting, ingestion).
- Changing the behavior of the `AtomicWikiMemoryProvider`.

## Decisions

- **Single Plugin Structure**: Move `AtomicWikiMemoryProvider` and its associated `cli.py` logic directly into `plugins/atomic-wiki`.
  - *Rationale*: Avoids circular imports, relative paths, and code duplication while ensuring the plugin works out of the box in Hermes.
- **Register Provider in Init**: Update `plugins/atomic-wiki/__init__.py` to call `ctx.register_memory_provider(AtomicWikiMemoryProvider())`.
  - *Rationale*: Hermes natively supports multiple registrations in a single plugin module.

## Risks / Trade-offs

- **Risk**: Existing agents or environments configured to load `plugins/memory/atomic-wiki` will break.
  - *Mitigation*: Update environment variables and configurations to only load the unified `atomic-wiki` plugin.
- **Risk**: Users who only installed `atomic-wiki` (and not the memory provider) will now have a memory provider registered.
  - *Mitigation*: The memory provider is inert and will not interfere with existing tools unless explicitly activated in the agent/hand configuration.
- **Upgrade Path**: To upgrade, simply re-run the plugin installation for the local path (e.g., `hermes plugin install --local ./plugins/atomic-wiki --force`). Since Hermes creates local references, you may not even need to reinstall if you used symlinks.
