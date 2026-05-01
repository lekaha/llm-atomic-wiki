## ADDED Requirements

### Requirement: Configure Wiki Directories
The plugin SHALL prompt the user to configure absolute paths to one or more Wiki directories during the `hermes memory setup` process.

#### Scenario: User runs setup
- **WHEN** the user executes `hermes memory setup` and selects `atomic-wiki`
- **THEN** the setup wizard prompts for the `wiki_dirs` configuration (accepting a comma-separated list of paths)

### Requirement: Prevent Autonomous Writes
The plugin SHALL NOT write to the file system during memory lifecycle events (`sync_turn` and `on_memory_write`).

#### Scenario: Conversation turn completes
- **WHEN** Hermes calls `sync_turn` after generating a response
- **THEN** the plugin performs a no-op (`pass`) and does not modify the wiki files

#### Scenario: Built-in memory is updated
- **WHEN** Hermes calls `on_memory_write` to mirror a `MEMORY.md` update
- **THEN** the plugin performs a no-op (`pass`) and does not modify the wiki files

### Requirement: Provide Read-Only Tools
The plugin SHALL expose exactly two tools to the agent: `wiki_search` and `wiki_read`.

#### Scenario: Agent requests tools
- **WHEN** Hermes calls `get_tool_schemas` on the memory provider
- **THEN** the plugin returns schemas only for `wiki_search` and `wiki_read` tools

### Requirement: Prefetch Context
The plugin SHALL automatically retrieve context from the wiki before the agent responds.

#### Scenario: User sends a message
- **WHEN** Hermes calls `prefetch(query)` before generating a response
- **THEN** the plugin searches the wiki based on the user's query and injects the results into the context
