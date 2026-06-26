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

### VSCode 显示所有文件绿色（git 索引被 iCloud 清空）

**Symptom:** VSCode Source Control 突然显示大量文件为绿色（untracked），`git status` 输出 1000+ 行 `D ` 或 `??`，但文件全部存在于磁盘上，`git log` 也正常。

**Root cause:** 仓库在 iCloud 同步目录（`~/Library/Mobile Documents/`）下。iCloud 不理解 `.git/` 内部结构，偶尔会把 `.git/index` 文件覆盖成空文件，导致 staging area 完全清空。

**Diagnosis:**
```bash
git ls-files | wc -l   # 返回 0 → 索引为空，确认是此问题
```

**Fix:**
```bash
# 1. 检查是否有遗留锁文件（VSCode git 扩展常留下）
ls .git/index.lock

# 2. 确认没有 git 进程在运行
pgrep git   # 若无输出则安全

# 3. 删除锁文件（仅在无 git 进程时）
rm .git/index.lock

# 4. 从最近一次 commit 重建索引（不会动工作区文件）
git reset
```

`git reset` 之后 VSCode 绿色文件消失，`git status` 应只剩真正有改动的文件。

**Prevention:** 无法完全避免（iCloud sync 的已知问题）。若频繁出现，考虑把 `.git/` 加入 iCloud 的排除规则，或将仓库移出 iCloud 目录。

---

## Step 2: After pushing the fix

```bash
gh run list --limit 3   # confirm new run triggered
# wait ~1 min
gh run list --limit 1   # confirm "completed / success"
```
