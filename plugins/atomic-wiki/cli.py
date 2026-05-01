import os
import json
import argparse
from . import tools

def get_wiki_dirs():
    raw_dirs = os.environ.get("ATOMIC_WIKI_PATHS", "")
    return [d.strip() for d in raw_dirs.split(",") if d.strip()]

def cmd_status(args):
    wiki_dirs = get_wiki_dirs()
    if wiki_dirs:
        print(f"Atomic Wiki Provider is configured with {len(wiki_dirs)} directories:")
        for d in wiki_dirs:
            print(f"  - {d}")
    else:
        print("Atomic Wiki Provider is active but no wiki_dirs configured. Set ATOMIC_WIKI_PATHS env var.")

def cmd_index(args):
    wiki_dirs = get_wiki_dirs()
    if not wiki_dirs:
        print("No wiki directories configured to index.")
        return
    
    print(f"Generating index for {len(wiki_dirs)} directories...")
    for d in wiki_dirs:
        print(f"\nProcessing {d}...")
        res = tools.atomic_wiki_gen_index({"wiki_path": d})
        res_dict = json.loads(res)
        if res_dict.get("success"):
            print(f"  Success: {res_dict.get('page_count')} pages indexed.")
            print(f"  Index file: {res_dict.get('index_file')}")
        else:
            print(f"  Error: {res_dict.get('error')}")

def cmd_lint(args):
    wiki_dirs = get_wiki_dirs()
    if not wiki_dirs:
        print("No wiki directories configured to lint.")
        return
        
    print(f"Running programmatic lint for {len(wiki_dirs)} directories...")
    for d in wiki_dirs:
        print(f"\nLinting {d}...")
        res = tools.atomic_wiki_lint({"wiki_path": d})
        res_dict = json.loads(res)
        if res_dict.get("success"):
            print(f"  Success: {res_dict.get('errors')} errors, {res_dict.get('warnings')} warnings.")
            print(f"  Report file: {res_dict.get('report_file')}")
        else:
            print(f"  Error: {res_dict.get('error')}")

def cmd_query(args):
    wiki_dirs = get_wiki_dirs()
    if not wiki_dirs:
        print("No wiki directories configured to query.")
        return
        
    query = args.query
    print(f"Querying across {len(wiki_dirs)} directories for: '{query}'\n")
    
    try:
        from .memory_provider import AtomicWikiMemoryProvider
        provider = AtomicWikiMemoryProvider()
        provider.initialize("cli-session", config={"wiki_dirs": ",".join(wiki_dirs)})
        result = provider._wiki_search(query)
        print(result)
    except Exception as e:
        print(f"Error executing query: {e}")

def cmd_ingest(args):
    wiki_dirs = get_wiki_dirs()
    if not wiki_dirs:
        print("No wiki directories configured to ingest.")
        return
        
    print(f"Checking for new materials to ingest across {len(wiki_dirs)} directories...")
    for d in wiki_dirs:
        raw_dir = os.path.join(d, "raw")
        if os.path.isdir(raw_dir):
            raw_files = [f for f in os.listdir(raw_dir) if not f.startswith('.')]
            if raw_files:
                print(f"  [{d}] Found {len(raw_files)} files in raw/ directory.")
                print(f"  -> Please use the 'atomic-wiki-operator' agent to extract atoms and update pages.")
            else:
                print(f"  [{d}] No new files in raw/ directory.")
        else:
            print(f"  [{d}] No raw/ directory found.")

def cmd_maintenance(args):
    print("Running Continuous Maintenance Tasks...\n")
    print("--- 1. Ingest (New Material) ---")
    cmd_ingest(args)
    print("\n--- 2. Generating Indexes (Post-Ingest) ---")
    cmd_index(args)
    print("\n--- 3. Running Programmatic Lint ---")
    cmd_lint(args)
    print("\nMaintenance complete. Please review the lint-report.md files for LLM Lint actions.")

def my_command(args):
    """Handler dispatched by argparse."""
    sub = getattr(args, "my_command", None)
    
    if sub == "status":
        cmd_status(args)
    elif sub == "index":
        cmd_index(args)
    elif sub == "lint":
        cmd_lint(args)
    elif sub == "query":
        cmd_query(args)
    elif sub == "ingest":
        cmd_ingest(args)
    elif sub == "maintenance":
        cmd_maintenance(args)
    else:
        print("Usage: hermes atomic-wiki <status|index|lint|query|ingest|maintenance>")

def register_cli(subparser) -> None:
    subs = subparser.add_subparsers(dest="my_command")
    
    subs.add_parser("status", help="Show atomic wiki provider status and directories")
    subs.add_parser("index", help="Manually regenerate index.md for all configured wiki directories")
    subs.add_parser("lint", help="Run programmatic lint and generate lint-report.md")
    subs.add_parser("ingest", help="Check for uningested files in raw/ directory")
    
    query_parser = subs.add_parser("query", help="Query the wiki for a keyword or phrase")
    query_parser.add_argument("query", help="The keyword or phrase to search for")
    
    subs.add_parser("maintenance", help="Run continuous maintenance tasks (ingest + index + lint)")
    
    subparser.set_defaults(func=my_command)
