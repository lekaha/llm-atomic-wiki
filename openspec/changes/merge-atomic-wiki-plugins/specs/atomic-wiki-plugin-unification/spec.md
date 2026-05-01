## ADDED Requirements

### Requirement: Unified Plugin Registration
The `atomic-wiki` plugin MUST register its agent tools, context hooks, and memory provider through a single entry point (`__init__.py`).

#### Scenario: Successful Registration
- **WHEN** the `atomic-wiki` plugin is loaded by the Hermes framework
- **THEN** it registers tools (`atomic_wiki_gen_index`, etc.), the `pre_llm_call` hook, and the `AtomicWikiMemoryProvider`.

### Requirement: Removal of Relative Dependencies
The plugin MUST NOT rely on external file structures or relative paths pointing outside its own directory for core logic.

#### Scenario: Standalone Execution
- **WHEN** the plugin is executed or installed in an arbitrary directory
- **THEN** it functions normally without breaking due to missing sibling directories.
