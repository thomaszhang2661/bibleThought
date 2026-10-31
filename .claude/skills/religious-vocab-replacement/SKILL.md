---
name: religious-vocab-replacement
description: >
  将讲道稿、神学文章中的基督教宗教词汇批量替换为学术性或中性词汇，生成适合微信公众号发布的版本。

  【立即触发】以下任意情形均须调用本 skill，不得自行改写：
  - 用户说"洗稿"、"处理一下"、"公众号版本"、"发公众号"、"适合公众号"、"准备发公众号"
  - 用户提供文件路径 + 提到"公众号"或"微信"
  - 用户说"替换宗教词汇"、"词汇替换"、"发布前处理"
  - 用户提到内容审查、绕过审查、中性化处理讲道稿
  - 用户说"合规审校"、"审一下能不能发"、"公众号合规"

  【不触发】用户只是要修改文章内容、补充论点、调整结构，而没有提到公众号/微信/洗稿。
---

# 宗教词汇替换

## 标准流程（直接调脚本）

给定源文件路径后，执行以下步骤：

**第一步：预览替换内容**

```bash
python "/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/.claude/skills/religious-vocab-replacement/scripts/replace_vocab.py" \
  "<源文件路径>" \
  --dry-run
```

**第二步：确认无误后正式写入**

```bash
python "/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/.claude/skills/religious-vocab-replacement/scripts/replace_vocab.py" \
  "<源文件路径>"
```

脚本会将洗稿版本直接写入 `302.公众号洗稿/<原文件名>`，**源文件保持不变**。

**第三步：合规扫描（写入后脚本自动运行；也可单独跑）**

```bash
python ".../scripts/replace_vocab.py" "<文件或目录>" --audit-only
```

按 `references/audit-rules.json` 扫描：规避检测写法、"苦刑柱"、"神"的误伤（大至高者、至高者迹……）、
未替换残留与多种写法并存、政治/医疗/低俗/惊悚标题、网页残留与外链、经文缩写、中英混杂等。
**只报告，不修改。** 标【需作者确认】的条目不得自行决定。

**第四步：人工审校**

脚本查不到的（政治影射的语境、翻译稿导读与出处、标题是否悬念式、事实核对、AI 辅助声明等），
按 `references/compliance-checklist.md` 逐节检查。风险内容只做"删除"或"泛化"，
绝不使用拆字、缩写、谐音、拼音、插入符号等方式规避检测；能改一个词不改一句，能改一句不删一段。

输出给用户：
1. 替换统计 + 合规扫描结果
2. 修改清单（表格：原文 / 改后 / 原因 / 规范条款）
3. "需作者确认"清单（政治相关修改、可能改变原意的修改、多种写法并存）
4. 发布提醒（是否勾选原创/AI 辅助声明、是否补授权说明、翻译稿是否有导读和出处）

**维护**：每发现新的误伤词，补到 `references/shen-protected.json`（保护不被替换）
和 `audit-rules.json` 的 `shen-false-positive`；每发现新的残留类型，补到 `audit-rules.json`。

---

## 算法说明

脚本使用两步替换：

1. **多字词**：按原词字数从长到短排列，顺序执行 `str.replace`。  
   例："神学"（2字）先于"神"（1字）处理 → "神学" → "关于至高者的学说"，之后"神"替换时文本中已无"神学"。

2. **单字"神"**：逐字扫描，检查前后字符，并对照 `references/shen-protected.json`，
   跳过"精神""神奇""神秘""大神""神迹"等普通汉语词汇。

词汇表见 `references/vocab.json`，如需新增替换对，直接在 `vocab.json` 中添加 `["原词", "替换词"]` 条目即可（脚本读取时自动按长度降序排序）。

**输出路径注意**：脚本默认输出到 `302.公众号洗稿/<原文件名>`（根目录），需手动 `mv` 到对应子文件夹（如 `302.公众号洗稿/03.标杆人生/`）。
