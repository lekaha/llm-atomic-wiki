## ADDED Requirements

### Requirement: Plugin Initialization and Configuration
The system SHALL load the plugin and prompt for the `ATOMIC_WIKI_PATHS` environment variable if missing, parsing it as a comma-separated list of absolute paths.

#### Scenario: Missing configuration
- **WHEN** the plugin loads and `ATOMIC_WIKI_PATHS` is missing
- **THEN** Hermes prompts the user to configure the paths before enabling the plugin

### Requirement: Context Injection
The system SHALL inject context into the LLM prompt indicating the active wiki paths and operational rules before every LLM turn.

#### Scenario: LLM Context injection
- **WHEN** a session starts or continues
- **THEN** the `pre_llm_call` hook injects the list of configured wiki paths and instructions to use the management tools

### Requirement: Skill Bundling
The system SHALL bundle the `atomic-wiki-operator` skill so that the agent can load the skill dynamically.

#### Scenario: Loading bundled skill
- **WHEN** the agent loads the skill via `skill_view("atomic-wiki:atomic-wiki-operator")`
- **THEN** the operational guidelines from the bundled `SKILL.md` are provided to the agent

### Requirement: Index Generation Tool
The system SHALL provide an `atomic_wiki_gen_index` tool to automatically generate the `index.md` file in the root of the specified wiki path.

#### Scenario: Generates valid index
- **WHEN** the LLM calls `atomic_wiki_gen_index` with a valid wiki path
- **THEN** an `index.md` is generated aggregating all pages inside the `wiki` subfolder, grouped by prefix

### Requirement: Log Append Tool
The system SHALL provide an `atomic_wiki_append_log` tool to add a new change entry to the `log.md` file of the specified wiki path.

#### Scenario: Appending new logs
- **WHEN** the LLM calls `atomic_wiki_append_log` with a message and wiki path
- **THEN** the `log.md` file is prepended with the new message and current date

### Requirement: Linting Tool
The system SHALL provide an `atomic_wiki_lint` tool to programmatically scan markdown files in the wiki for ghost links, orphan pages, formatting violations, and outdated markers.

#### Scenario: Running lint checks
- **WHEN** the LLM calls `atomic_wiki_lint` with a wiki path
- **THEN** a `lint-report.md` file is generated at the root of the wiki path and the tool returns a JSON summary of the findings
