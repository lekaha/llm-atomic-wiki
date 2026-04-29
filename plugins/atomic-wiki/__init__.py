import os
from .schemas import ATOMIC_WIKI_GEN_INDEX, ATOMIC_WIKI_APPEND_LOG, ATOMIC_WIKI_LINT
from .tools import atomic_wiki_gen_index, atomic_wiki_append_log, atomic_wiki_lint

def pre_llm_call(ctx, **kwargs):
    """Inject configured atomic wiki paths into the LLM context."""
    paths_env = os.environ.get("ATOMIC_WIKI_PATHS", "")
    if not paths_env:
        return
        
    paths = [p.strip() for p in paths_env.split(",") if p.strip()]
    if not paths:
        return
        
    context_msg = "You are managing the following Atomic Wikis:\n"
    for p in paths:
        if os.path.isdir(p):
            context_msg += f"- {p}\n"
            
    if context_msg != "You are managing the following Atomic Wikis:\n":
        context_msg += "\nPlease use the registered tools to interact with them and follow the atomic-wiki-operator guidelines."
        ctx.inject_context(context_msg)

def register(ctx):
    """Register the atomic wiki plugin components."""
    # Register hooks
    ctx.register_hook("pre_llm_call", pre_llm_call)
    
    # Register tools
    ctx.register_tool(ATOMIC_WIKI_GEN_INDEX, atomic_wiki_gen_index)
    ctx.register_tool(ATOMIC_WIKI_APPEND_LOG, atomic_wiki_append_log)
    ctx.register_tool(ATOMIC_WIKI_LINT, atomic_wiki_lint)
    
    # Register bundled skill
    skill_path = os.path.join(os.path.dirname(__file__), "skills", "atomic-wiki-operator", "SKILL.md")
    if os.path.exists(skill_path):
        ctx.register_skill("atomic-wiki-operator", skill_path)
