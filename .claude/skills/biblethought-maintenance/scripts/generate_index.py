#!/usr/bin/env python3
import os
import re
import json
import subprocess
from collections import defaultdict

ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip()

EXCLUDE_FILES = {"index.md", "index- generator.md", "generate_index.py", "2..md", "Untitled.md"}
EXCLUDE_DIRS = {".obsidian", ".git", "_attachments"}

INDEX_HEADER = '---\nbody_class: index-page\n---\n\n'
INDEX_FOOTER = ''

def folder_id(*parts):
    """Generate anchor ID for a folder from one or more path components."""
    combined = '-'.join(parts)
    combined = re.sub(r'[\s._]+', '-', combined)
    combined = re.sub(r'-+', '-', combined).strip('-')
    return combined

def make_id(text):
    """Generate anchor id from heading text: keep Chinese chars, ASCII word chars, hyphens."""
    result = text.replace(' ', '-')
    result = re.sub(r'[^一-鿿㐀-䶿a-zA-Z0-9\-]', '', result)
    result = re.sub(r'-+', '-', result).strip('-')
    # Strip leading digit-hyphen prefix so IDs don't start with digits
    # (kramdown requires IDs to start with a letter)
    result = re.sub(r'^\d[\d-]*-', '', result)
    return result

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

def convert_wikilinks(lookup):
    """Convert [[WikiLink]] to [WikiLink](relative_path) in changed .md files only."""
    changed_files = get_changed_files()
    if not changed_files:
        return
    converted_count = 0
    for path in changed_files:
        fname = os.path.basename(path)
        if fname in EXCLUDE_FILES or not os.path.exists(path):
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
    # tree[top][sub][subsub] = [(rel_path, title)]
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

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
                tree[""][""][""].append((rel_path, title))
            elif len(parts) == 2:
                tree[parts[0]][""][""].append((rel_path, title))
            elif len(parts) == 3:
                tree[parts[0]][parts[1]][""].append((rel_path, title))
            else:
                tree[parts[0]][parts[1]][parts[2]].append((rel_path, title))

    return tree

def generate():
    lookup = build_lookup()
    convert_wikilinks(lookup)

    tree = collect()
    total = sum(len(files) for top in tree.values() for sub in top.values() for files in sub.values())
    lines = [INDEX_HEADER, f"共 {total} 篇文章\n\n"]

    def make_url(rel_path):
        # Strip .md so links point directly to Jekyll page URLs,
        # bypassing jekyll-relative-links which drops underscores.
        url = rel_path.replace(os.sep, '/')
        if url.endswith('.md'):
            url = url[:-3]
        return url

    for rel_path, title in tree.get("", {}).get("", {}).get("", []):
        url = make_url(rel_path)
        lines.append(f'<a class="tree-file" href="{url}">{title}</a>\n')

    for top in sorted(tree.keys(), key=num_key):
        if top == "":
            continue
        tid = folder_id(top)
        lines.append(f'\n<details class="tree-folder" id="{tid}">\n<summary class="tree-dir">{top}<a class="anchor-link" href="#{tid}">#</a></summary>\n')
        subs = tree[top]

        for rel_path, title in subs.get("", {}).get("", []):
            url = make_url(rel_path)
            lines.append(f'<a class="tree-file" href="{url}">{title}</a>\n')

        for sub in sorted(subs.keys(), key=num_key):
            if sub == "":
                continue
            sid = folder_id(top, sub)
            lines.append(f'<details class="tree-folder" id="{sid}">\n<summary class="tree-dir">{sub}<a class="anchor-link" href="#{sid}">#</a></summary>\n')
            subsubs = subs[sub]

            for rel_path, title in subsubs.get("", []):
                url = make_url(rel_path)
                lines.append(f'<a class="tree-file" href="{url}">{title}</a>\n')

            for subsub in sorted([k for k in subsubs.keys() if k != ""], key=num_key):
                ssid = folder_id(top, sub, subsub)
                lines.append(f'<details class="tree-folder" id="{ssid}">\n<summary class="tree-dir">{subsub}<a class="anchor-link" href="#{ssid}">#</a></summary>\n')
                for rel_path, title in subsubs[subsub]:
                    url = make_url(rel_path)
                    lines.append(f'<a class="tree-file" href="{url}">{title}</a>\n')
                lines.append(f'</details>\n')

            lines.append(f'</details>\n')

        lines.append(f'</details>\n')

    lines.append(INDEX_FOOTER)
    output = os.path.join(ROOT, "index.md")
    with open(output, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    # Build ordered flat page list for prev/next navigation
    ordered = []
    for rel_path, title in tree.get("", {}).get("", {}).get("", []):
        ordered.append((rel_path, title))
    for top in sorted(tree.keys(), key=num_key):
        if top == "":
            continue
        for rel_path, title in tree[top].get("", {}).get("", []):
            ordered.append((rel_path, title))
        for sub in sorted(tree[top].keys(), key=num_key):
            if sub == "":
                continue
            for rel_path, title in tree[top][sub].get("", []):
                ordered.append((rel_path, title))
            for subsub in sorted([k for k in tree[top][sub].keys() if k != ""], key=num_key):
                for rel_path, title in tree[top][sub][subsub]:
                    ordered.append((rel_path, title))

    nav_data = []
    for i, (rel_path, title) in enumerate(ordered):
        entry = {
            "path": rel_path.replace(os.sep, '/'),
            "title": title,
        }
        if i > 0:
            prev_path, prev_title = ordered[i - 1]
            entry["prev_url"] = prev_path.replace(os.sep, '/')[:-3]
            entry["prev_title"] = prev_title
        if i < len(ordered) - 1:
            next_path, next_title = ordered[i + 1]
            entry["next_url"] = next_path.replace(os.sep, '/')[:-3]
            entry["next_title"] = next_title
        nav_data.append(entry)

    nav_output = os.path.join(ROOT, "_data", "nav.json")
    with open(nav_output, 'w', encoding='utf-8') as f:
        json.dump(nav_data, f, ensure_ascii=False, indent=2)

    print(f"生成完成：{total} 篇文章 -> index.md，{len(nav_data)} 条导航 -> _data/nav.json")

if __name__ == '__main__':
    generate()
