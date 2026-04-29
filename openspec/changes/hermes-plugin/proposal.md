## Why

The user is migrating their personal AI assistant framework from OpenFang to the Hermes Agent. The previous OpenFang hand was responsible for managing atomic wikis (compiling indices, linting markdown, and appending logs), which now needs to be re-implemented as a Hermes plugin so the agent can autonomously manage the atomic wiki ecosystem.

## What Changes

- Create a new Hermes plugin named `atomic-wiki` inside the `plugins/` directory.
- Replace the legacy Bash scripts (`gen-index.sh`, `lint.sh`, `log-append.sh`) with native Python-based tools within the plugin for tighter integration, better error handling, and superior debuggability.
- Introduce `requires_env` to the plugin manifest to configure multiple atomic wiki base paths dynamically.
- Utilize the `pre_llm_call` hook to inject context about configured wiki paths and structures (raw, atoms, wiki) into the LLM context, making the agent fully aware of how to operate on them.

## Capabilities

### New Capabilities
- `atomic-wiki-management`: Enables the Hermes agent to manage multiple atomic wiki directories, including index generation, automated linting, and maintaining the change log.
- `bundled-skills`: The plugin will bundle the `atomic-wiki-operator` skill so the Hermes agent can load the operational guidelines dynamically using the `ctx.register_skill` feature.

### Modified Capabilities


## Impact

- Introduces a new `plugins/atomic-wiki` directory following the standard Hermes plugin architecture.
- Replaces reliance on external shell scripts with integrated Python tools.
- Sets the foundation to deprecate the existing `atomic-wiki-operator` folder and associated `scripts/`.
