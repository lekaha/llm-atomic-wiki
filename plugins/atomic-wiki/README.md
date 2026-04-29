# Atomic Wiki Plugin for Hermes

This is a native Python plugin for the [Hermes Agent](https://hermes-agent.nousresearch.com/), designed to autonomously manage your Atomic Wiki knowledge base.

## What is it?

The Atomic Wiki Plugin provides a set of tools and context hooks to allow an LLM to seamlessly operate and maintain an atomic knowledge base. It bundles the `atomic-wiki-operator` skill, which provides the agent with strict guidelines and operational rules for structuring, writing, and maintaining atomic notes.

It provides three primary native tools:
- **`atomic_wiki_gen_index`**: Scans the wiki and auto-generates a structured `index.md` grouping all pages by their prefix.
- **`atomic_wiki_append_log`**: Safely appends new maintenance entries to the wiki's `log.md`.
- **`atomic_wiki_lint`**: Programmatically scans markdown files for ghost links, orphan pages, formatting violations, and outdated markers, outputting a detailed JSON summary and a `lint-report.md`.

## Why did we build it?

Previously, the Atomic Wiki was managed via a set of external bash scripts (`gen-index.sh`, `lint.sh`, `log-append.sh`) orchestrated by an OpenFang "Hand". 

Migrating to a native Hermes Plugin offers several significant advantages:
1. **Debuggability & Reliability**: Native Python implementations return structured JSON directly to the LLM, making error handling and reasoning much more robust than parsing standard out/error from bash scripts.
2. **Context Injection**: By using the `pre_llm_call` hook, the plugin can dynamically look at environment variables and automatically inject the managed wiki paths directly into the LLM's system context.
3. **Skill Bundling**: Hermes allows plugins to bundle their own `SKILL.md` guidelines. This ensures the agent perfectly understands the philosophy and strict rules of the atomic wiki lifecycle without polluting global configurations.
4. **Cross-Platform Compatibility**: Removing bash scripts ensures the wiki manager can run cleanly on macOS, Linux, or Windows.

## How to use it

### Configuration

To use the plugin, the Hermes Agent requires the `ATOMIC_WIKI_PATHS` environment variable to be set. This defines which folders the agent should manage.

```bash
export ATOMIC_WIKI_PATHS="/path/to/my-atomic-wiki"
```

You can manage multiple wiki paths by separating them with a comma:

```bash
export ATOMIC_WIKI_PATHS="/path/to/my-atomic-wiki,/path/to/another-wiki"
```

### Integration

Load the plugin when starting your Hermes Agent. The plugin uses the standard `register(ctx)` interface:

1. **Hooks**: The `pre_llm_call` hook automatically reads the `ATOMIC_WIKI_PATHS` and appends a message to the context instructing the agent to manage these directories.
2. **Skills**: It automatically registers the `atomic-wiki-operator` skill. If the LLM needs to know the exact rules for creating an atom, it can reference this bundled skill.
3. **Tools**: The LLM will have immediate access to `atomic_wiki_gen_index`, `atomic_wiki_append_log`, and `atomic_wiki_lint`. If you ask the agent to "Lint my wiki" or "Update the wiki index", it will invoke these native Python tools.

### Example Interaction

**User**: *"Can you run a health check on my private atomic wiki?"*

**Hermes Agent**:
1. Checks the context and sees it manages `/path/to/my-atomic-wiki`.
2. Invokes the `atomic_wiki_lint` tool with the path.
3. The tool generates `/path/to/my-atomic-wiki/lint-report.md` and returns a JSON summary (e.g., `{"success": true, "errors": 2, "warnings": 1}`).
4. The agent reads the JSON and responds: *"I found 2 ghost links and 1 orphan page. I have generated a full report at `lint-report.md`."*
