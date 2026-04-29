## Context

The user manages knowledge using an Atomic Wiki methodology (structured with `raw`, `atoms`, and `wiki` subdirectories). Currently, this is automated via OpenFang bash scripts. To migrate to the Hermes Agent, these bash scripts need to be rewritten as a native Python Hermes plugin to allow the Hermes Agent to seamlessly manage and operate on multiple wiki instances.

## Goals / Non-Goals

**Goals:**
- Provide a set of tools (linting, generating index, appending logs) to the Hermes agent via a new `atomic-wiki` plugin.
- Handle multiple atomic wiki folders using the plugin's environment variables (`requires_env`).
- Ensure the plugin is debuggable (e.g., returning proper JSON errors, utilizing python logging).
- Seamless context injection so the LLM implicitly knows what folders it manages.

**Non-Goals:**
- Do not migrate or alter existing wiki data.
- Do not delete the old `atomic-wiki-operator` folder and shell scripts yet.

## Decisions

1. **Native Python Tool Implementation**: Instead of executing the legacy shell scripts via `subprocess`, the logic for generating indices, linting, and appending logs will be implemented natively in Python. This improves reliability, allows rich return payloads (JSON), and integrates cleanly with the Hermes tools API.
2. **Context Injection via `pre_llm_call`**: To inform the LLM about which wikis are available, their structure, and required operational procedures, the plugin will inject context during the `pre_llm_call` hook.
3. **Skill Bundling**: The existing `SKILL.md` will be bundled directly into the plugin under `plugins/atomic-wiki/skills/atomic-wiki-operator/SKILL.md` and registered via `ctx.register_skill()`. This allows Hermes to load the skill dynamically.
4. **Environment Variable Configuration**: `ATOMIC_WIKI_PATHS` will be requested via the `requires_env` feature, containing a comma-separated list of paths the agent should manage.
5. **Debuggability**: Handlers will return structured JSON indicating success, file paths, and any errors gracefully. Python's `logging` module will be used to track tool usage internally.

## Risks / Trade-offs

- **Risk**: Python string parsing logic for markdown links might behave slightly differently than the previous bash scripts (e.g., regex differences).
  → **Mitigation**: Implement robust regex or string manipulation in Python that matches the bash script capabilities, particularly for ghost links like `[[slug|Display]]`.
