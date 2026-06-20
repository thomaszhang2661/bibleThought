# Jekyll / GitHub Pages Debugging

Read this file when diagnosing a build failure or when articles aren't appearing on the site.

---

## Step 1: Get the error message

```bash
gh run list --limit 5
gh run view <RUN_ID> --log | grep -A5 "Build with Jekyll"
```

Look for `ERROR: YOUR SITE COULD NOT BE BUILT`.

---

## Common errors and fixes

### "Invalid YAML front matter in /path/to/file.md"

Check line 1 of the file:
- Line 1 is `---` with no closing `---` before content → remove the opening `---`
- YAML between `---` delimiters has unquoted colons or other syntax errors → fix them

Scan all files with `---` at line 1:
```bash
find . -name "*.md" -not -path "./.git/*" | while read f; do
  [ "$(head -1 "$f")" = "---" ] && echo "$f"
done
```

### Liquid template errors

```bash
grep -rl "{%" --include="*.md" . | grep -v ".git"
grep -rl "{{" --include="*.md" . | grep -v ".git"
```

Wrap offending text with `{% raw %}...{% endraw %}`.

### Articles not visible on the site

Run the index generator and commit — the pre-commit hook does this automatically, but if you need to trigger it manually:
```bash
python3 .claude/skills/biblethought-maintenance/scripts/generate_index.py
git add index.md _data/nav.json
git commit -m "rebuild index"
git push
```

### nav.json broken

```bash
python3 -c "import json; json.load(open('_data/nav.json')); print('OK')"
```

If invalid, regenerate via `generate_index.py` (above).

---

## Step 2: After pushing the fix

```bash
gh run list --limit 3   # confirm new run triggered
# wait ~1 min
gh run list --limit 1   # confirm "completed / success"
```
