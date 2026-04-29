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
