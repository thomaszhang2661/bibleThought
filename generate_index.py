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
li { line-height: 1.5; margin: 0.05em 0; }
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

def build_lookup():
    """Build a map from filename (without .md) to relative path from ROOT."""
    lookup = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fname in filenames:
            if not fname.endswith('.md') or fname in EXCLUDE_FILES:
                continue
            rel = os.path.relpath(os.path.join(dirpath, fname), ROOT)
            key = fname[:-3]
            lookup[key] = rel
    return lookup

def get_changed_files():
    """Use git to find only new/modified .md files since last commit."""
    import subprocess
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=ROOT, capture_output=True, text=True
    )
    changed = set()
    for line in result.stdout.splitlines():
        status, path = line[:2].strip(), line[3:].strip()
        # Handle renamed files: "R old -> new"
        if ' -> ' in path:
            path = path.split(' -> ')[-1]
        if path.endswith('.md'):
            changed.add(os.path.join(ROOT, path))
    return changed

def all_md_files():
    paths = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fname in filenames:
            if fname.endswith('.md') and fname not in EXCLUDE_FILES:
                paths.append(os.path.join(dirpath, fname))
    return paths

def convert_wikilinks(lookup):
    """Convert [[WikiLink]] to [WikiLink](relative_path) in all .md files."""
    converted_count = 0
    for path in all_md_files():
        if not os.path.exists(path):
            continue

        with open(path, encoding='utf-8') as f:
            content = f.read()

        if '[[' not in content:
            continue

        file_dir = os.path.dirname(path)

        def replace_link(m):
            target = m.group(1).strip()
            if any(target.endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                return target
            if target in lookup:
                abs_target = os.path.join(ROOT, lookup[target])
                rel = os.path.relpath(abs_target, file_dir).replace(os.sep, '/')
                return f'[{target}]({rel})'
            return target

        new_content = re.sub(r'\[\[([^\]]+)\]\]', replace_link, content)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            converted_count += 1

    if converted_count:
        print(f"转换 wiki 链接：{converted_count} 个文件已更新")

def collect():
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
                tree[parts[0]][parts[1]].append((rel_path, title))

    return tree

def generate():
    lookup = build_lookup()
    convert_wikilinks(lookup)

    tree = collect()
    total = sum(len(files) for top in tree.values() for files in top.values())
    lines = [CSS, f"共 {total} 篇文章\n\n"]

    for rel_path, title in tree.get("", {}).get("", []):
        url = rel_path.replace(os.sep, '/')
        lines.append(f"- [{title}]({url})\n")
    if tree.get("", {}).get("", []):
        lines.append("\n")

    for top in sorted(tree.keys(), key=num_key):
        if top == "":
            continue
        lines.append(f"## {top}\n\n")
        subs = tree[top]

        for rel_path, title in subs.get("", []):
            url = rel_path.replace(os.sep, '/')
            lines.append(f"- [{title}]({url})\n")
        if subs.get(""):
            lines.append("\n")

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
