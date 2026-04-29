"""Tool handlers for Atomic Wiki Plugin."""

import os
import json
import datetime
import glob
import re

def atomic_wiki_gen_index(args: dict, **kwargs) -> str:
    """Generate index.md from wiki files."""
    wiki_path = args.get("wiki_path", "").strip()
    if not wiki_path or not os.path.isdir(wiki_path):
        return json.dumps({"error": f"Invalid or missing wiki_path: {wiki_path}"})
        
    wiki_dir = os.path.join(wiki_path, "wiki")
    index_file = os.path.join(wiki_path, "index.md")
    
    try:
        md_files = glob.glob(os.path.join(wiki_dir, "*.md"))
        branches = {}
        page_count = 0
        for f in md_files:
            slug = os.path.basename(f)[:-3]
            if slug in ("index", "log", "_template", "README"):
                continue
            page_count += 1
            branch = slug.split("-")[0]
            if branch not in branches:
                branches[branch] = []
            with open(f, "r", encoding="utf-8") as fh:
                title_line = fh.readline().strip()
                title = title_line.replace("# ", "") if title_line.startswith("# ") else slug
            branches[branch].append((slug, title))
            
        lines = [
            "# Wiki Index\n",
            f"> Total pages: {page_count}",
            f"> Auto-generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
            "---\n"
        ]
        
        # Original script defined an explicit branch order, but fallback to auto. We will auto-discover here.
        for branch, pages in sorted(branches.items()):
            display = branch.replace("-", " ").title()
            lines.append(f"## {display} ({len(pages)} pages)\n")
            lines.append("| Slug | Title |")
            lines.append("|------|-------|")
            for slug, title in sorted(pages):
                lines.append(f"| [[{slug}]] | {title} |")
            lines.append("\n")
            
        with open(index_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
            
        return json.dumps({"success": True, "index_file": index_file, "page_count": page_count})
    except Exception as e:
        return json.dumps({"error": f"Index generation failed: {e}"})

def atomic_wiki_append_log(args: dict, **kwargs) -> str:
    """Append entry to log.md."""
    wiki_path = args.get("wiki_path", "").strip()
    message = args.get("message", "").strip()
    
    if not wiki_path or not message:
        return json.dumps({"error": "Missing wiki_path or message"})
        
    log_file = os.path.join(wiki_path, "log.md")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    new_entry = f"## {date_str}\n\n- {message}\n\n"
    
    try:
        if not os.path.exists(log_file):
            content = f"# Wiki Change Log\n\n{new_entry}"
        else:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if len(lines) >= 2:
                lines.insert(2, new_entry)
                content = "".join(lines)
            else:
                content = "".join(lines) + f"\n{new_entry}"
                
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(content)
            
        return json.dumps({"success": True, "log_file": log_file, "message": message})
    except Exception as e:
        return json.dumps({"error": f"Log append failed: {e}"})

def atomic_wiki_lint(args: dict, **kwargs) -> str:
    """Lint atomic wiki markdown files."""
    wiki_path = args.get("wiki_path", "").strip()
    if not wiki_path or not os.path.isdir(wiki_path):
        return json.dumps({"error": "Invalid or missing wiki_path"})
        
    wiki_dir = os.path.join(wiki_path, "wiki")
    report_file = os.path.join(wiki_path, "lint-report.md")
    
    try:
        md_files = glob.glob(os.path.join(wiki_dir, "*.md"))
        errors = 0
        warnings = 0
        ghost_links = []
        orphans = []
        formats = []
        outdated = []
        
        all_links_to = {os.path.basename(f)[:-3]: 0 for f in md_files}
        link_re = re.compile(r'\[\[([^\]]+)\]\]')
        outdated_re = re.compile(r'最新版|目前最新|currently v|latest v|just released|剛出|剛推出|截至 \d{4}')
        
        slugs_to_process = []
        for f in md_files:
            slug = os.path.basename(f)[:-3]
            if slug in ("index", "log", "lint-report", "README", "_template"):
                continue
            slugs_to_process.append((slug, f))
            
        for slug, f in slugs_to_process:
            with open(f, "r", encoding="utf-8") as fh:
                content = fh.read()
                lines = content.split('\n')
                
            links = link_re.findall(content)
            for link in links:
                target = link.split('|')[0]
                if target in all_links_to:
                    all_links_to[target] += 1
                if not os.path.exists(os.path.join(wiki_dir, f"{target}.md")):
                    ghost_links.append(f"- `{slug}` → `[[{target}]]` (not found)")
                    errors += 1
                    
            if not lines or not lines[0].startswith("# "):
                first_line = lines[0] if lines else ""
                formats.append(f"- `{slug}`: first line is not `# title` → `{first_line}`")
                errors += 1
                
            if not re.match(r'^[a-z0-9\-]+$', slug):
                formats.append(f"- `{slug}`: filename contains uppercase or underscore")
                errors += 1
                
            outdated_matches = outdated_re.findall(content)
            if outdated_matches:
                outdated.append(f"### `{slug}`\n```\n{', '.join(set(outdated_matches))}\n```")
                warnings += 1

        for slug, _ in slugs_to_process:
            if all_links_to.get(slug, 0) == 0:
                orphans.append(f"- `{slug}`")
                warnings += 1
                
        report_lines = [
            "# Wiki Lint Report\n",
            f"> Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
            "## 1. Ghost Links（指向不存在頁面的連結）\n",
            "\n".join(ghost_links) if ghost_links else "None.",
            "\n## 2. Orphan Pages（沒有任何頁面連結過來的頁面）\n",
            "\n".join(orphans) if orphans else "None.",
            "\n## 3. Format Violations（格式違規）\n",
            "\n".join(formats) if formats else "None.",
            "\n## 4. Outdated Markers（時效性用語）\n",
            "\n".join(outdated) if outdated else "None.",
            "\n---\n",
            f"**Summary**: {errors} errors, {warnings} warnings across {len(slugs_to_process)} wiki pages"
        ]
        
        with open(report_file, "w", encoding="utf-8") as fh:
            fh.write("\n".join(report_lines))
            
        return json.dumps({
            "success": True, 
            "report_file": report_file, 
            "errors": errors, 
            "warnings": warnings
        })
    except Exception as e:
        return json.dumps({"error": f"Linting failed: {e}"})
