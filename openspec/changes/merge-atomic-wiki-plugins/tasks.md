## 1. Migration

- [x] 1.1 Move `AtomicWikiMemoryProvider` from `plugins/memory/atomic-wiki/__init__.py` to `plugins/atomic-wiki/memory_provider.py`.
- [x] 1.2 Move `plugins/memory/atomic-wiki/cli.py` to `plugins/atomic-wiki/cli.py`.
- [x] 1.3 Refactor imports in `plugins/atomic-wiki/cli.py` to use local relative imports (e.g., `from .tools import ...`) instead of brittle `importlib` paths.
- [x] 1.4 Update `plugins/atomic-wiki/__init__.py` to import and register the `AtomicWikiMemoryProvider`.
- [x] 1.5 Update `plugins/atomic-wiki/plugin.yaml` to include the memory provider hooks (`prefetch`, `system_prompt_block`).
- [x] 2.1 Delete the legacy `plugins/memory/atomic-wiki` directory and its contents completely.

## 2. Cleanup

- [x] 2.2 Verify the `atomic-wiki` plugin loads successfully in Hermes and tools/commands execute properly.
