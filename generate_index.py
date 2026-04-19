#!/usr/bin/env python3
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

EXCLUDE_FILES = {"index.md", "index- generator.md", "generate_index.py", "2..md", "Untitled.md"}
EXCLUDE_DIRS = {".obsidian", ".git", "_attachments"}

CSS = """<style>
body {
  font-size: 24px;
  font-family: "Helvetica Neue", sans-serif;
  line-height: 1.8;
  padding: 40px;
  background-color: #f9f9f9;
  color: #222;
}

a {
  font-size: 20px;
  color: #007acc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
"""

def folder_sort_key(folder):
    """Sort folders by leading number prefix, e.g. '1. 创世记' -> 1"""
    match = re.match(r'^(\d+)', folder)
    return int(match.group(1)) if match else 9999

def file_sort_key(name):
    match = re.match(r'^(\d+)', name)
    return int(match.group(1)) if match else 9999

def collect_files():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]

        for fname in filenames:
            if not fname.endswith('.md'):
                continue
            if fname in EXCLUDE_FILES:
                continue

            abs_path = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(abs_path, ROOT)

            # display text: path without .md extension
            display = rel_path[:-3]
            entries.append((rel_path, display))

    # Sort: by top-level folder number, then full path
    def sort_key(entry):
        parts = entry[0].split(os.sep)
        top = folder_sort_key(parts[0]) if len(parts) > 1 else 0
        return (top, entry[0])

    entries.sort(key=sort_key)
    return entries

def generate():
    entries = collect_files()
    lines = [CSS, f"章节{len(entries)}\n\n"]
    for rel_path, display in entries:
        # Use forward slashes for URLs
        url = rel_path.replace(os.sep, '/')
        lines.append(f"- [{display}]({url})\n\n")

    output = os.path.join(ROOT, "index.md")
    with open(output, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"生成完成：{len(entries)} 篇文章 -> index.md")

if __name__ == '__main__':
    generate()
