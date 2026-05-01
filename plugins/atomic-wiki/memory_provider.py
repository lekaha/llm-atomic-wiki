import os
import glob
import logging
from agent.memory_provider import MemoryProvider

logger = logging.getLogger(__name__)

class AtomicWikiMemoryProvider(MemoryProvider):
    @property
    def name(self) -> str:
        return "atomic-wiki"
        
    def is_available(self) -> bool:
        return True
        
    def get_config_schema(self):
        return [
            {
                "key": "wiki_dirs",
                "description": "Comma-separated absolute paths to atomic wiki directories",
                "required": True,
            }
        ]
        
    def initialize(self, session_id: str, **kwargs) -> None:
        raw_dirs = kwargs.get("config", {}).get("wiki_dirs", "")
        if not raw_dirs:
            raw_dirs = os.environ.get("ATOMIC_WIKI_PATHS", "")
        self._wiki_dirs = [d.strip() for d in raw_dirs.split(",") if d.strip()]
        self._session_id = session_id
        logger.info(f"Initialized AtomicWikiMemoryProvider with wiki_dirs: {self._wiki_dirs}")

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "wiki_search",
                    "description": "Search the atomic wiki for a given query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search term to look for in wiki contents"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "wiki_read",
                    "description": "Read the contents of a specific wiki page by slug",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "slug": {
                                "type": "string",
                                "description": "The slug of the wiki page to read (without .md extension)"
                            }
                        },
                        "required": ["slug"]
                    }
                }
            }
        ]

    def handle_tool_call(self, name: str, args: dict) -> str:
        if name == "wiki_search":
            return self._wiki_search(args.get("query", ""))
        elif name == "wiki_read":
            return self._wiki_read(args.get("slug", ""))
        return f"Unknown tool: {name}"

    def _wiki_search(self, query: str) -> str:
        if not query:
            return "Empty search query"
        results = []
        query_lower = query.lower()
        for d in self._wiki_dirs:
            wiki_dir = os.path.join(d, "wiki")
            if not os.path.exists(wiki_dir):
                continue
            for f in glob.glob(os.path.join(wiki_dir, "*.md")):
                try:
                    with open(f, "r", encoding="utf-8") as fh:
                        content = fh.read()
                        if query_lower in content.lower():
                            slug = os.path.basename(f)[:-3]
                            results.append(slug)
                except Exception as e:
                    logger.debug(f"Error reading file {f}: {e}")
        if not results:
            return f"No results found for '{query}'"
        return f"Found matching pages: {', '.join(results)}"

    def _wiki_read(self, slug: str) -> str:
        if not slug:
            return "Empty slug provided"
        for d in self._wiki_dirs:
            file_path = os.path.join(d, "wiki", f"{slug}.md")
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as fh:
                        return fh.read()
                except Exception as e:
                    return f"Error reading page: {e}"
        return f"Page not found: {slug}"

    def prefetch(self, query: str) -> str:
        """Prefetch hook to inject context"""
        if not query:
            return ""
        search_res = self._wiki_search(query)
        if search_res.startswith("Found"):
            return f"[Atomic Wiki Prefetch] Based on your recent message, the following wiki pages might be relevant: {search_res}\nUse the wiki_read tool to explore them if necessary."
        return ""

    def system_prompt_block(self) -> str:
        return (
            "You have read-only access to an Atomic Wiki via your memory provider. "
            "Use the `wiki_search` tool to find pages matching a query. "
            "Use the `wiki_read` tool to read the contents of a specific page by its slug. "
            "The wiki is strictly read-only; you do not have tools to write or modify the wiki files."
        )

    def sync_turn(self, user_content: str, assistant_content: str) -> None:
        pass

    def on_memory_write(self, action: str, target: str, content: str) -> None:
        pass
