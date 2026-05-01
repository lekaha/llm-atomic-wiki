## Context

The Atomic Wiki is an Obsidian vault designed to store heavily curated, high-fidelity knowledge atoms. Currently, Hermes Agent external Memory Providers generally assume read-write access to persist conversational metadata or automatic memory chunks. We are building a custom Memory Provider, `atomic-wiki`, tailored for Hermes, to connect to this vault. To preserve the Wiki's sanctity, we must enforce a strictly read-only architecture where Hermes can query and inject context, but cannot write back.

## Goals / Non-Goals

**Goals:**
- Provide read-only search and retrieval capabilities against the Atomic Wiki for Hermes.
- Ensure the `sync_turn` and `on_memory_write` lifecycle events do not mutate the Wiki.
- Seamless integration as a standard Hermes Memory Provider plugin.

**Non-Goals:**
- The agent will NOT be able to autonomously write, append, or modify files in the Wiki.
- We are not porting or running the `gen-index.sh` or `lint.sh` bash scripts natively from within Python for this initial iteration.

## Decisions

- **Strict Read-Only Lifecycle Hooks**: The methods `sync_turn(user_content, assistant_content)` and `on_memory_write(action, target, content)` will be implemented as empty functions (`pass`).
- **Tools**: We will only expose `wiki_search` and `wiki_read` via the `get_tool_schemas` and `handle_tool_call` methods. Write-oriented tools (`wiki_write`, `wiki_append_log`) are explicitly excluded.
- **Config**: We will use `get_config_schema` to prompt for `wiki_dirs` (a comma-separated list of paths) to allow Hermes to search across multiple Obsidian vault folders simultaneously.

## Risks / Trade-offs

- [Risk] Because Hermes is unable to write conversational notes back to the Wiki, contextual "learning" from conversations within the UI is lost across sessions unless the user manually updates the wiki. 
  → Mitigation: Rely on Hermes's default `MEMORY.md` for conversational continuity, treating the Wiki strictly as an immutable reference library.
