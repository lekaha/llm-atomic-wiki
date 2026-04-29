## 1. Plugin Setup

- [x] 1.1 Create `plugins/atomic-wiki` directory structure.
- [x] 1.2 Create `plugin.yaml` configuring `requires_env` for `ATOMIC_WIKI_PATHS`, declaring the provided tools (`atomic_wiki_gen_index`, `atomic_wiki_append_log`, `atomic_wiki_lint`), and `pre_llm_call` hook.

## 2. Context Injection

- [x] 2.1 Implement `schemas.py` outlining tool parameters (`wiki_path`, `message`, etc.).
- [x] 2.2 Create `__init__.py` and implement the `pre_llm_call` hook logic to inject configured atomic wiki paths and operational rules into the LLM context.

## 3. Skill Bundling

- [x] 3.1 Create `plugins/atomic-wiki/skills/atomic-wiki-operator/` directory.
- [x] 3.2 Copy the contents of the existing `atomic-wiki-operator/SKILL.md` to `plugins/atomic-wiki/skills/atomic-wiki-operator/SKILL.md`.

## 4. Tool Implementations

- [x] 4.1 Implement `atomic_wiki_gen_index` in `tools.py` (translating logic from `gen-index.sh` to native Python).
- [x] 4.2 Implement `atomic_wiki_append_log` in `tools.py` (translating logic from `log-append.sh` to native Python).
- [x] 4.3 Implement `atomic_wiki_lint` in `tools.py` (translating logic from `lint.sh` to native Python, returning a JSON report).

## 5. Final Wiring

- [x] 5.1 Wire schemas, handlers, hooks, and skill registration (`ctx.register_skill`) inside the `register(ctx)` function in `__init__.py`.
