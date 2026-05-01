## Why

The Atomic Wiki serves as a curated, high-fidelity knowledge base. While it's extremely valuable for the Hermes Agent to retrieve context from it, allowing the agent to automatically write conversation logs or autonomous memory updates into the wiki could clutter it and compromise its curated nature. Making the Memory Provider read-only ensures the integrity of the wiki while still leveraging its powerful filesystem-style knowledge hierarchy for agent context.

## What Changes

- Create the `atomic-wiki` Memory Provider plugin for Hermes Agent.
- Implement read-only capabilities by omitting tools like `wiki_write` and `wiki_append_log`.
- Provide only read-oriented tools: `wiki_search` and `wiki_read`.
- Implement `sync_turn` and `on_memory_write` lifecycle hooks as no-ops (`pass`) so the agent never writes back to the wiki.
- Implement the `prefetch` hook to automatically search the wiki index based on the user's latest message.

## Capabilities

### New Capabilities
- `read-only-atomic-wiki-provider`: Provides read-only context retrieval from one or more Atomic Wikis (Obsidian vaults) into the Hermes Agent, featuring prefetching, searching, and reading tools without write access.

### Modified Capabilities
- none

## Impact

- Hermes Agent will gain persistent, cross-session knowledge retrieval from the Atomic Wiki.
- The wiki itself will remain completely unmodified by the agent, ensuring its data integrity.
