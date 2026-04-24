#!/usr/bin/env python3
import os
import re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_FILES = {"index.md", "index- generator.md", "generate_index.py", "2..md", "Untitled.md"}
EXCLUDE_DIRS = {".obsidian", ".git", "_attachments"}

CSS = """<style>
body {
  font-size: 20px;
  font-family: "Helvetica Neue", sans-serif;
  line-height: 1.8;
  padding: 40px;
  max-width: 900px;
  background-color: #f9f9f9;
  color: #222;
}
h2 { margin-top: 2em; color: #333; }
h3 { margin-top: 1em; margin-left: 2em; color: #555; font-size: 1em; }
h3 + ul { margin-left: 2em; }
a {
  font-size: 18px;
  color: #007acc;
  text-decoration: none;
}
a:hover { text-decoration: underline; }
</style>
"""

def num_key(name):
    match = re.match(r'^(\d+)', name)
    return (int(match.group(1)), name) if match else (9999, name)

def collect():
    # tree: { top_folder: { sub_folder: [(rel_path, title)] } }
    # root-level files go under key ("", "")
    tree = defaultdict(lambda: defaultdict(list))

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(
            [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')],
            key=num_key
        )
        for fname in sorted(filenames, key=num_key):
            if not fname.endswith('.md') or fname in EXCLUDE_FILES:
                continue
            abs_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(abs_path, ROOT)
            parts = rel_path.split(os.sep)
            title = fname[:-3]

            if len(parts) == 1:
                tree[""][""].append((rel_path, title))
            elif len(parts) == 2:
                tree[parts[0]][""].append((rel_path, title))
            else:
                # everything deeper than 2 levels: group under top/sub
                tree[parts[0]][parts[1]].append((rel_path, title))

    return tree

def generate():
    tree = collect()
    total = sum(len(files) for top in tree.values() for files in top.values())
    lines = [CSS, f"共 {total} 篇文章\n\n"]

    # Root-level files first
    for rel_path, title in tree.get("", {}).get("", []):
        url = rel_path.replace(os.sep, '/')
        lines.append(f"- [{title}]({url})\n")
    if tree.get("", {}).get("", []):
        lines.append("\n")

    # Numbered top-level folders
    for top in sorted(tree.keys(), key=num_key):
        if top == "":
            continue
        lines.append(f"## {top}\n\n")
        subs = tree[top]

        # Files directly in top folder (no subfolder)
        for rel_path, title in subs.get("", []):
            url = rel_path.replace(os.sep, '/')
            lines.append(f"- [{title}]({url})\n")
        if subs.get(""):
            lines.append("\n")

        # Subfolders
        for sub in sorted(subs.keys(), key=num_key):
            if sub == "":
                continue
            lines.append(f"### {sub}\n\n")
            for rel_path, title in subs[sub]:
                url = rel_path.replace(os.sep, '/')
                lines.append(f"- [{title}]({url})\n")
            lines.append("\n")

    output = os.path.join(ROOT, "index.md")
    with open(output, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"生成完成：{total} 篇文章 -> index.md")

if __name__ == '__main__':
    generate()
