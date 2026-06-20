# Pieper Translation File Conventions

Read this file whenever you're working on chapter files under `101. 教义/Francis Pieper/`.

---

## Folder naming

```
NNN_卷N_章名/   e.g., 103_卷一_神论/
```
- Volume 1 = 1xx, Volume 2 = 2xx, Volume 3 = 3xx
- NNN encodes both volume and chapter order

## File naming within folders

```
NN_中文标题.md   e.g., 01_上帝的自然知识.md
```
- Two-digit numeric prefix (01, 02 … 36)
- **No `§` symbol in filenames** — causes URL-encoding problems on GitHub Pages
- Curly/smart quotes in filenames must be single-quoted in shell: `'02_"天使"之名.md'`

## Renaming files

Always use `git mv` so git tracks the rename:
```bash
git mv "old_§1_name.md" "new_18_name.md"
```

---

## Standard terminology (do not vary)

| Term | Standard form |
|------|--------------|
| Augsburg Confession Apology | 《辩护书》 |
| Synergism | 协同主义 |
| Melanchthon | 梅兰希顿 |
| Quenstedt | 昆斯泰特 |
| Chemnitz | 肯尼兹 |
| Gerhard | 格哈德 |
| Monergism | 独作论 / 独作主义 |
| Lord's Supper (Herrnmahl) | 主的筵席 |
| Solid Declaration | 固体宣言 |
| Oecolampadius | 俄科兰帕迪乌斯 |
| Amyraldists | 阿米洛得主义者 (NOT 亚米念主义者 — they are Reformed, not Arminian) |

> **Note**: 《协和信条的辩护》in `202_卷二_基督论/11_*.md` is a DIFFERENT document — do NOT change it to 《辩护书》.

---

## Things that look wrong but are intentional

- `算为义` vs `称义` — different theological concepts (imputation vs. justification); both correct
- `圣事` — mostly Catholic context or compounds like 神圣事务; correct as-is
- `更生` — appears only in `自力更生` idiom, not regeneration
- `《协和信条的辩护》` in 基督论/11 — different document from 《辩护书》

---

## macOS shell notes

Use `perl -i -pe` for in-place text replacement (not `sed -i`, which requires an extra empty-string arg on macOS):
```bash
perl -i -pe 's/旧文本/新文本/g' file.md
```
