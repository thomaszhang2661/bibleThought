---
name: parallel-book-translator
description: >
  将英文神学文献（论文、讲义、书籍）翻译为学术中文，或整理已有中文译稿。

  【立即触发】以下任意情形均须调用本 skill：
  - 用户说"翻译这篇/这本"、"帮我翻译"、"translate this"
  - 用户提供文件路径（PDF/txt/md）+ 提到"翻译"
  - 用户说"整理译稿"、"校对翻译"、"对照英文校对"、"proof reading"、"内容校对"
  - 用户要求将多章节英文书翻译为中文

  【校对默认深度模式】凡"校对"任务，默认逐段比对中英文内容（意思准确性、
  省略、逻辑颠倒、数字/引用/术语错误），而非只查格式。

  【不触发】用户只是要修改已有中文文章内容、补充论点、调整结构，而没有提到翻译。
---

# Parallel Book Translator / Organizer

Three modes depending on input:

| Mode | Input | Main work |
|------|-------|-----------|
| **A: 翻译书籍** | 英文多章节书 | Parallel translation → per-chapter .md files |
| **B: 整理译稿** | 中文 Word/PDF + 英文 PDF | Extract → split → **深度校对**（逐段比对内容） |
| **C: 翻译单篇** | 英文单篇论文/讲义/报告 | 按行数决定 subagent 数量，输出单个 .md 文件 |

> **校对默认为「深度内容校对」**：逐段比对中英文意思，而非只查格式。
> 格式校对（英文残片、断行、遗漏节标题）只是第一遍；意思准确性（曲解、
> 省略、逻辑颠倒、数字/引用/术语错误）是必做的第二遍。见 Mode B Phase 3。

---

## Mode C 决策：单篇文档

在启动任何 agent 之前，先量出文档行数，然后按下表决定 subagent 数量：

```bash
# PDF
pdftotext "file.pdf" /tmp/doc.txt && wc -l /tmp/doc.txt

# 已是 txt/md
wc -l file.txt
```

| 行数 | Subagent 数量 | 说明 |
|------|------------|------|
| < 800 | **0（直接翻译，无 subagent）** | 在当前对话直接完整翻译，输出为单个 .md |
| 800–2000 | **2 agents**（上 / 下，各半） | 各自翻译自己的行范围，合并输出 |
| 2000–4000 | **3 agents**（上 / 中 / 下） | 每段约 700–1300 行 |
| > 4000 | **ceil(行数 / 1300) agents** | 每段不超过 1300 行 |

### Mode C 输出格式

**无 subagent（< 800 行）**：直接在对话中翻译完整文档，写入单个 .md 文件。文件名格式：
```
中文标题_作者姓_年份.md
```

**有 subagent**：每个 agent 翻译自己的行范围，写入带行范围标注的临时文件，最后合并。

Agent 提示模板（单篇）：
```
学术翻译任务：[文档名称]（第 N 部分，行 START–END）

读取：sed -n 'START,ENDp' /tmp/doc.txt

翻译规则：
① 逐段完整翻译，不省略任何内容（含脚注、括注、希腊文/拉丁文注释）
② 希腊文/拉丁文保留原文，括号内附中译
③ 经文引用保留章节编号
④ 文风：庄重学术
⑤ 输出为纯 markdown，各原始节标题保留为 ## 标题

输出文件：/tmp/doc_part_N.md
```

合并：
```bash
cat /tmp/doc_part_1.md /tmp/doc_part_2.md > 最终输出.md
```

---

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

**输出文件命名（必须）**：`NN_中文标题.md`，NN 为两位数字前缀（00、01、02…），从 00 开始按顺序编号。**没有数字前缀的文件在文件浏览器中会乱序。**

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

File naming: `NN_第N章_简短标题.md` with two-digit prefix starting from `00`. **This is mandatory — files without numeric prefixes sort incorrectly in all file browsers.**

### Phase 3: 深度并行校对（对照英文PDF，默认）

**默认为深度内容校对**：逐段比对意思，而非只检查格式。每组 **2 章**，确保校对深度。

从英文 PDF 目录找出每章的行范围（用 `grep -n "^Chapter\|^Acts [0-9]" /tmp/book_en.txt`）。

**深度校对 agent 提示模板（每组 2 章）：**
```
深度内容校对任务：[书名] 第X章 + 第Y章

英文原文：
- 第X章：sed -n 'START,ENDp' /tmp/book_en.txt
- 第Y章：sed -n 'START,ENDp' /tmp/book_en.txt

中文文件：
- [中文章节文件路径]

这是深度内容校对，不是格式校对。对每一个中文评注段落，找到英文原文对应段落，逐句比对：

1. **内容完整性**：英文段落中的每个关键论点，中文是否都有？有无整句被省略？
2. **意思准确性**：中文是否如实传达英文意思？有无曲解、夸大、弱化、逻辑颠倒？
3. **数字/年份/距离等细节**：所有具体数据必须与英文一致（"more than 40"不能译成"40"）
4. **圣经引用的书卷和章节**：书名和章节号必须与英文一致，不能有偏移
5. **专有名词**：人名地名术语必须准确（governor≠government，Barnabas=巴拿巴）
6. **神学术语**：inspired/默示、grace/恩典、repentance/悔改、spirit/灵（注意是否是圣灵）

操作：用 Edit 工具直接修改文件中的错误。
报告：只列实质内容错误（不报格式问题），说明英文原意和错误类型。
```

**批次大小建议**：
- 正常章节（< 300 EN 行）：每组 2 章
- 大章节（> 400 EN 行）：单章一个 agent
- 目标：每个 agent 覆盖不超过 600 行英文，保证逐段覆盖

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
2. **深度校对是默认** — 整理/校对任务必做逐段内容比对，不能只查格式。格式干净 ≠ 翻译正确
3. **Consistent terminology** — parallel agents can diverge; enforce with the terms list
4. **Numeric file prefixes** — ensures correct sort order in file browsers and web views
5. **Heading hierarchy** — H2 for main sections, H3 for sub-sections; never mark quotations as headings
6. **Correct source attribution** — verify chapter content matches the right source pages/lines

### 深度校对常见错误类型（实测高频）

以下是从真实校对中反复出现的错误，agent 提示中应重点提示：

- **意思颠倒/逻辑倒置**：`without seeming to deny` 译成"除非否认"；`no more competent than` 译成"没有能力"（丢失比较）；犹推古段落"正式教导"与"交谈"被对调
- **整句/整段省略**：英文三句评注中文只译第一句；关键神学论点（如"唯独因信得救"）被跳过
- **数字精度丢失**：`more than 40 years` → "40 年"；`about 15 years` → "十五年"（漏"约"）
- **方向/地理错误**：`northwest` → "以北"；`east` → "西"；`off the coast`（海岸外）→ "海岸"
- **专名/职衔误译**：`governor`（总督）→ "政府"；`Emperor`（皇帝）→ "王"；`a spirit`（一个灵）→ "圣灵"；`NIV` → "和合本"
- **神学术语弱化**：`inspired text`（受默示）→ "启示性的"；`prophesied`（预言）→ "应许"；`the power of the gospel`（福音大能）漏"大能"
- **圣经引用偏移**：`Luke 1:3` → "路加福音 1:1"；漏节号 `3:10, 11` → "3:11"

---

## Reference files

- `references/theology_terms.md` — Standard English↔Chinese mappings: core doctrines, Latin, confessional documents, Pieper standard terms
