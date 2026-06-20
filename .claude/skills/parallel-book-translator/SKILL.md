---
name: parallel-book-translator
description: Translate OR organize long structured books into scholarly Chinese using parallel subagents. Use this skill when the user wants to: (1) translate a book from English into Chinese, or (2) organize an existing Chinese translation (e.g. from a Word document) into individual markdown files and proofread against the English original. Invoke proactively for any multi-chapter book work — translation, organization, proofreading, gap-filling, or cleanup.
---

# Parallel Book Translator / Organizer

Two modes depending on what exists:

| Mode | Input | Main work |
|------|-------|-----------|
| **A: 翻译** | English text file | Parallel translation → Chinese .md files |
| **B: 整理** | Chinese Word/PDF + English PDF | Extract → split into chapters → proofread |

---

## Mode A: 从英文翻译

### Phase 0: Map the structure

```bash
# Extract if needed (PDF → txt)
pdftotext "book.pdf" /tmp/book.txt

# Find chapter/section boundaries
grep -n "^Chapter\|^CHAPTER\|^§" /tmp/book.txt | head -80
wc -l /tmp/book.txt
```

Build a chapter table: name, start line, end line, line count. Chapters >3000 lines need multiple agents.

### Phase 1: Assign chunks

Target **1000–1300 lines per chunk**; never exceed 1500.

- Short chapter (<1500 lines): 1 agent
- Medium (1500–3000): 2 agents, labeled 上/下
- Long (3000–5000): 3 agents, labeled 上/中/下
- Very long (>5000): ceil(lines / 1300) agents, labeled 第N部分

Non-first agents: tell them explicitly "start from line X, do not look for a section heading."

### Phase 2: Prepare output folders

Use a naming scheme that sorts correctly — **numeric prefix is essential**:

```
NNN_卷号_章名/   e.g., 101_卷一_圣经论/
```

- Volume 1 chapters = 1xx, volume 2 = 2xx, etc.
- Files within folder: `NN_中文标题.md`
- Non-overlapping number ranges for multi-agent chapters (main: 01–17, supplementary: 21–35)

### Phase 3: Launch all agents in one turn

Send **one message** with all Agent tool calls — this is what makes it parallel.

**Agent prompt template:**
```
学术翻译任务：[书名] [卷号] [章节名及行范围]

读取：sed -n 'START,ENDp' /tmp/book_vN.txt

目标文件夹：OUTPUT_PATH/NNN_卷N_章名/

[续接说明（仅续接 agent）：这是[章名]的第N部分，直接从第START行开始翻译，
无需寻找节标题，写入 NN_章名（上/中/下）.md]

各节写单独文件，命名 NN_中文标题.md（节序号从 OFFSET 开始）
节标题格式：# §N 中文标题

规则：
① 逐段完整翻译，不省略任何段落（含脚注、括注、补充说明）
② 拉丁文/希腊文保留原文，括号内附中译
③ 经文引用保留章节编号
④ 单节原文超 600 行拆（上）（下）
⑤ 文风：庄重学术

术语：[粘贴 references/theology_terms.md 中的相关表格]
```

Always include a domain-appropriate terminology list. For theology, see `references/theology_terms.md`.

### Phase 4: Handle failures

**Content filtering** — signs: agent errors or writes nothing.
- Reframe as "comparative analysis" or "historical survey"
- Split to ≤400 lines and retry
- Check if files were actually written despite error message

**Partial completion** — `ls` the folder, launch targeted retry agents for missing ranges.

**Agent writes wrong folder** — move overflow files; verify content matches folder subject.

**Subsection numbering conflicts** — rename secondary group to start at 21+.

---

## Mode B: 整理已有中文译稿

Use when the user provides an existing Chinese translation (Word or PDF) and an English PDF for proofreading.

### Phase 0: 提取中文文本

```bash
# Word (.doc/.docx) → txt (macOS)
textutil -convert txt "中文译稿.doc" -output /tmp/book_cn.txt

# PDF → txt (cross-platform)
pdftotext "中文译稿.pdf" /tmp/book_cn.txt

# Check output
wc -l /tmp/book_cn.txt
head -100 /tmp/book_cn.txt   # inspect TOC artifacts from Word
```

Word-to-txt artifacts to expect:
- `HYPERLINK \l "_TocXXX" 标题   PAGEREF _TocXXX \h N` — skip the entire TOC block
- Tab characters in some lines
- Occasional garbled/stray characters from formatting

### Phase 1: 检查章节结构

```bash
# Find all chapter headings with line numbers
grep -n "^第[一二三四五六七八九十百零]*章\|^第[0-9]*章" /tmp/book_cn.txt

# Find major part headers
grep -n "^Part\|^PART\|^神论\|^人论\|^基督论" /tmp/book_cn.txt

wc -l /tmp/book_cn.txt
```

Decide splitting granularity based on chapter sizes:
- Chapters averaging 100–500 lines → **one file per chapter** (flat structure, simpler nav)
- Chapters averaging 1000+ lines → **one file per section** (like the Pieper model)

### Phase 2: 写转换脚本

Write a Python script to split the .txt into individual .md files. Key heading-detection logic:

```python
def is_heading(lines, i):
    """Detect section headings: short standalone lines not ending with sentence terminators."""
    line = lines[i].strip()
    if not line:
        return False
    prev_blank = (i == 0 or not lines[i-1].strip())
    next_blank = (i >= len(lines)-1 or not lines[i+1].strip())
    if not (prev_blank and next_blank):
        return False
    # Colon at end = introduces a quote/list, NOT a heading
    if line.endswith(('。', '！', '？', '……', '"', '"', '：', ':')):
        return False
    if line.startswith(('"', '"', '"', '（')):
        return False
    if len(line) > 55:
        return False
    return True
```

Markdown structure per file:
- Chapter title → `# 第N章　标题` (H1)
- Part headers (神论/人论/etc.) → `> **部分标题**` (blockquote note at top)
- Detected section headings → `## 标题` (H2)
- Nested sub-sections → `### 标题` (H3)
- Body text → paragraphs as-is

File naming: `NN_第N章_简短标题.md` with two-digit prefix.

### Phase 3: 并行校对（对照英文PDF）

Group chapters into batches of 3–5 per agent. From the English PDF TOC, note the page range for each chapter.

**Proofreading agent prompt template:**
```
You are proofreading a Chinese theological translation against its English original.

Book: [English title] by [Author]
Chapters assigned: Ch N–M
Chinese files: [list file paths]
English PDF: [PDF path] (pages X–Y)

For each chapter:
1. Read the English PDF pages (max 20 pages per read — do multiple reads for long chapters)
2. Read the Chinese .md file
3. Compare and fix directly in the file:
   a) Missing paragraphs or sections
   b) Mistranslated key theological terms (see references/theology_terms.md)
   c) Heading levels (H2 for main sections, H3 for sub-sections; never mark quotations as headings)
   d) Garbled characters, typos, truncated sentences
4. Report what you changed in each file
```

---

## Phase 5: Git commit

```bash
git add [output folder]
git commit -m "翻译完成: [书名] [卷/章节范围]"
git push
```

---

## Quality principles

1. **No omissions** — every paragraph, footnote, and parenthetical must be present
2. **Consistent terminology** — parallel agents can diverge; enforce with the terms list
3. **Numeric file prefixes** — ensures correct sort order in file browsers and web views
4. **Heading hierarchy** — H2 for main sections, H3 for sub-sections; never mark quotations as headings
5. **Correct source attribution** — verify chapter content matches the right source pages/lines

---

## Reference files

- `references/theology_terms.md` — Standard English↔Chinese mappings: core doctrines, Latin, confessional documents, Pieper standard terms
