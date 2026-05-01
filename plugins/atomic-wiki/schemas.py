"""Tool schemas for the Atomic Wiki Hermes plugin."""

ATOMIC_WIKI_GEN_INDEX = {
    "name": "atomic_wiki_gen_index",
    "description": (
        "Generate or update the index.md file for a specified atomic wiki. "
        "It scans the 'wiki' subfolder and aggregates all pages grouped by prefix."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "wiki_path": {
                "type": "string",
                "description": "Absolute path to the atomic wiki base directory.",
            },
        },
        "required": ["wiki_path"],
    },
}

ATOMIC_WIKI_APPEND_LOG = {
    "name": "atomic_wiki_append_log",
    "description": (
        "Append a new change entry to the log.md file in the atomic wiki. "
        "Use this tool to document any modifications made to the wiki knowledge base."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "wiki_path": {
                "type": "string",
                "description": "Absolute path to the atomic wiki base directory.",
            },
            "message": {
                "type": "string",
                "description": "Description of the changes made (e.g., 'Added new security atom').",
            },
        },
        "required": ["wiki_path", "message"],
    },
}

ATOMIC_WIKI_LINT = {
    "name": "atomic_wiki_lint",
    "description": (
        "Programmatically scan markdown files in the specified atomic wiki for "
        "ghost links, orphan pages, formatting violations, and outdated markers. "
        "It outputs a lint-report.md file in the wiki path."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "wiki_path": {
                "type": "string",
                "description": "Absolute path to the atomic wiki base directory.",
            },
        },
        "required": ["wiki_path"],
    },
}

ATOMIC_WIKI_INGEST = {
    "name": "atomic_wiki_ingest",
    "description": (
        "Ingest extracted knowledge atoms into the wiki. This tool saves the provided "
        "pages to the wiki directory, automatically regenerates the index, and appends "
        "a message to the log.md file to document the changes."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "wiki_path": {
                "type": "string",
                "description": "Absolute path to the atomic wiki base directory.",
            },
            "pages": {
                "type": "array",
                "description": "List of page objects to create or update in the wiki.",
                "items": {
                    "type": "object",
                    "properties": {
                        "slug": {
                            "type": "string",
                            "description": "The file slug for the page (e.g., 'concept-ai-agents'). Do not include the .md extension."
                        },
                        "content": {
                            "type": "string",
                            "description": "The full markdown content for the page, starting with an H1 title."
                        }
                    },
                    "required": ["slug", "content"]
                }
            },
            "log_message": {
                "type": "string",
                "description": "A summary message of the ingestion to append to the log.md file."
            }
        },
        "required": ["wiki_path", "pages", "log_message"],
    },
}

