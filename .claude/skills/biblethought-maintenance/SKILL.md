---
name: biblethought-maintenance
description: Maintain the BibleThought Jekyll/GitHub Pages site at ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought. Use this skill whenever the user wants to: publish a new article, fix a GitHub Pages build failure, update the article index, debug Jekyll errors, rename or reorganize Pieper translation files, or check why a page isn't visible on the web. Invoke proactively when the user says a file "can't be seen on the web", mentions a build failure, or adds new content to the repo.
---

# BibleThought Site Maintenance

BibleThought is a personal theology/Bible-study Jekyll site hosted on GitHub Pages.
Repo: `git@github.com:thomaszhang2661/bibleThought`
Local path: `/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought`

---

## Site architecture (know this first)

- **Static site generator**: Jekyll 3.10.0, via `actions/jekyll-build-pages@v1` (GitHub manages the build — you only push markdown)
- **`_config.yml`**: applies `layout: default` to ALL files via `defaults`. This means EVERY `.md` file in the repo becomes a Jekyll page, and YAML front matter rules apply universally.
- **`index.md`**: the article directory. **Auto-generated** by `generate_index.py` — do NOT edit by hand.
- **`_data/nav.json`**: prev/next navigation per page. **Auto-generated** by `generate_index.py` — do NOT edit by hand.
- **`generate_index.py`**: walks the entire repo and regenerates both `index.md` and `_data/nav.json`. Run it manually with `python3 generate_index.py` if needed.
- **`.git/hooks/pre-commit`**: runs `generate_index.py` automatically before every `git commit`. `index.md` and `nav.json` are always in sync with the actual files.
- **`_layouts/default.html`**: single layout for all pages; uses `site.data.nav`.

---

## Workflow 1: Publishing a new article

1. **Write the article** — save it in the correct subfolder (e.g., `98. 讲道框架/`, `99. 讲道/`).

2. **Check the file's first line** — the most common build-breaking mistake:
   - **BAD**: file starts with `---` but no closing `---` → Jekyll treats the whole file as broken YAML front matter
   - **OK**: file starts with a heading like `# Title` (no front matter at all)
   - **OK**: file starts with `---` then valid YAML then `---` (e.g., `body_class: index-page`)
   - A lone `---` at line 1 followed immediately by content (not another `---`) will crash the build

3. **Commit and push** — the pre-commit hook regenerates `index.md` and `nav.json` automatically:
   ```bash
   git add <new-file>
   git commit -m "添加文章：<标题>"
   git push
   ```

4. **Verify the build** — GitHub Actions auto-triggers; check within ~2 minutes:
   ```bash
   gh run list --limit 3
   ```

---

## Workflow 2: Debugging a GitHub Pages build failure

### Step 1: Get the error message
```bash
gh run list --limit 5
# grab the latest run ID, then:
gh run view <RUN_ID> --log | grep "Build with Jekyll"
```

Look for the line containing `ERROR: YOUR SITE COULD NOT BE BUILT`. The message immediately after tells you the exact file and problem.

### Step 2: Common errors and fixes

**"Invalid YAML front matter in /path/to/file.md"**
- Open the file and check line 1
- If line 1 is `---` but there's no closing `---` before the content → remove the opening `---`
- If the YAML between `---` delimiters contains a line starting with `#` → that's a YAML comment, it's valid; look for other issues (unquoted colons, etc.)
- After fixing, commit and push

**Liquid template errors (`{% %}` or `{{ }}` in content)**
```bash
grep -rl "{%" --include="*.md" . | grep -v ".git"
grep -rl "{{" --include="*.md" . | grep -v ".git"
```
If found in a content file (not a layout), wrap the offending text with `{% raw %}...{% endraw %}`.

**Check all files with `---` at line 1** (to find others with the same YAML problem):
```bash
find . -name "*.md" -not -path "./.git/*" | while read f; do
  [ "$(head -1 "$f")" = "---" ] && echo "$f"
done
```
Then verify each one has a proper closing `---`.

### Step 3: After pushing the fix
```bash
gh run list --limit 3   # confirm new run triggered
# wait ~1 minute, then:
gh run list --limit 1   # confirm "completed / success"
```

---

## Workflow 3: Pieper translation file conventions

The Francis Pieper *Christian Dogmatics* translation lives under:
`101. 教义/Francis Pieper/`

### Folder naming
```
NNN_卷N_章名/   e.g., 103_卷一_神论/
```
- Volume 1 = 1xx, Volume 2 = 2xx, Volume 3 = 3xx
- NNN encodes both volume and chapter order

### File naming within folders
```
NN_中文标题.md   e.g., 01_上帝的自然知识.md
```
- Two-digit numeric prefix (01, 02 … 36)
- **No `§` symbol in filenames** — causes URL-encoding problems. Use numbers only.
- Curly/smart quotes in filenames (e.g., `02_"天使"之名.md`) must be quoted in shell commands: `'02_"天使"之名.md'`

### Renaming files
Always use `git mv` so git tracks the rename:
```bash
git mv "old_§1_name.md" "new_18_name.md"
```

### Standard terminology (do not vary)
| Term | Standard form |
|------|--------------|
| Augsburg Confession Apology | 《辩护书》 |
| Synergism | 协同主义 |
| Melanchthon | 梅兰希顿 |
| Quenstedt | 昆斯泰特 |
| Chemnitz | 肯尼兹 |
| Gerhard | 格哈德 |

Note: 《协和信条的辩护》in `202_卷二_基督论/11_*.md` is a DIFFERENT document — do NOT change it to 《辩护书》.

---

## Key files quick reference

| File | Purpose |
|------|---------|
| `generate_index.py` | Regenerates `index.md` + `nav.json`; runs automatically on every commit |
| `.git/hooks/pre-commit` | Triggers `generate_index.py` before each commit (local only, not git-tracked) |
| `_config.yml` | Jekyll config; `defaults` applies layout to all files |
| `_layouts/default.html` | Single page layout with TTS, nav, font size |
| `_data/nav.json` | Prev/next navigation; auto-generated, do not edit by hand |

### Checking nav.json validity
```bash
python3 -c "import json; json.load(open('_data/nav.json')); print('OK')"
```

---

## Things that look wrong but are intentional

- `算为义` vs `称义` — different theological concepts (imputation vs. justification); both correct
- `圣事` — mostly Catholic context or compounds like 神圣事务; correct as-is
- `更生` — appears only in `自力更生` idiom, not regeneration
- `《协和信条的辩护》` in 基督论/11 — different document from 《辩护书》

---

## macOS shell notes

- Use `perl -i -pe` for in-place text replacement (not `sed -i`, which requires an extra arg on macOS):
  ```bash
  perl -i -pe 's/旧文本/新文本/g' file.md
  ```
- When filenames contain curly quotes or special chars, single-quote the path.
